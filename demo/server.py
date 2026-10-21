#!/usr/bin/env python3
"""Lethe local demo: watch what each party in the request path can see.

One process plays all five parties, each handed only the bytes it would really receive:
  device   scrubs the prompt locally, spends one blind credential, seals the request
  issuer   signs credentials blind when you subscribe; never sees a prompt
  relay    sees your IP and a fixed-size sealed blob it cannot open
  gateway  opens the blob, checks the credential, forwards under Lethe's own key
  lab      OpenAI or OpenRouter; gets one scrubbed question from "Lethe"

Run:  python3 demo/server.py   then open http://localhost:8787
Key:  OPENROUTER_API_KEY or OPENAI_API_KEY in demo/.env or the environment. Without one it runs dry.
      LETHE_OPENAI_STORE=1 lets you verify on OpenAI's side what it received (see VERIFY.md).
"""
import hashlib
import json
import os
import sys
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lethe_crypto as lc  # noqa: E402
from scrub import Scrubber  # noqa: E402

DEMO_ACCOUNT = "sarah.miller@gmail.com"
DEMO_CARD = "Visa ending 4242"
CREDENTIALS_PER_SUBSCRIPTION = 5


def load_env():
    f = HERE / ".env"
    if f.exists():
        for line in f.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip("\"'"))


def make_provider():
    if os.getenv("OPENROUTER_API_KEY"):
        return {"name": "OpenRouter", "url": "https://openrouter.ai/api/v1/chat/completions",
                "key": os.environ["OPENROUTER_API_KEY"],
                "models": {"GPT": os.getenv("LETHE_MODEL_GPT", "openai/gpt-5.6-luna"),
                           "Claude": os.getenv("LETHE_MODEL_CLAUDE", "anthropic/claude-haiku-5.5"),
                           "Gemini": os.getenv("LETHE_MODEL_GEMINI", "google/gemini-3.5-flash-lite")}}
    if os.getenv("OPENAI_API_KEY"):
        return {"name": "OpenAI", "url": "https://api.openai.com/v1/responses",
                "key": os.environ["OPENAI_API_KEY"],
                "models": {"GPT-5.6 Luna": "gpt-5.6-luna", "GPT-5.6 Sol": "gpt-5.6-sol",
                           "GPT-5.4 mini": "gpt-5.4-mini"}}
    return {"name": "Dry run", "url": "https://api.openai.com/v1/responses", "key": None,
            "models": {"GPT-5.6 Luna": "gpt-5.6-luna"}}


def short(x) -> str:
    h = x.hex() if isinstance(x, bytes) else format(x, "x")
    return h[:20] + "…"


class LabError(Exception):
    pass


# ======================================================================== the parties
class Issuer:
    """Knows who pays. Signs credentials it cannot see."""

    def __init__(self):
        self.key = lc.IssuerKey()
        self.seen_blinded: list[str] = []
        self.view = None

    def subscribe(self, account: str, card: str, blinded: list[int]) -> list[int]:
        self.seen_blinded += [short(b) for b in blinded]
        self.view = {"account": account, "card": card, "blinded": [short(b) for b in blinded],
                     "key_id": self.key.key_id, "issued_total": len(self.seen_blinded)}
        return self.key.sign_blinded(blinded)


class Lab:
    """The model provider. Gets whatever the gateway sends, under the gateway's key.

    OpenAI is called through the Responses API so every request can be checked afterwards:
    with LETHE_OPENAI_STORE=1 OpenAI keeps it, and GET /v1/responses/{id}/input_items returns
    exactly the input OpenAI received.
    """

    def __init__(self, provider):
        self.p = provider
        self.store = provider["name"] == "OpenAI" and os.getenv("LETHE_OPENAI_STORE") == "1"

    def _post(self, body):
        headers = {"Content-Type": "application/json", "User-Agent": "Lethe-Gateway/0.1"}
        req = urllib.request.Request(self.p["url"], data=json.dumps(body).encode(),
                                     headers=dict(headers, Authorization="Bearer " + self.p["key"]))
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.load(r), r.headers
        except urllib.error.HTTPError as e:
            raise LabError(f"{self.p['name']} returned {e.code}: {e.read().decode(errors='replace')[:300]}")
        except urllib.error.URLError as e:
            raise LabError(f"Could not reach {self.p['name']}: {e.reason}")

    def complete(self, model: str, messages: list[dict]):
        if self.p["name"] == "OpenRouter":
            body = {"model": model, "messages": messages}
            if os.getenv("LETHE_ZDR") == "1":
                body["provider"] = {"data_collection": "deny"}
        else:
            body = {"model": model, "input": messages, "store": self.store}
        view = {"request": f"POST {self.p['url']}",
                "headers": {"Content-Type": "application/json", "User-Agent": "Lethe-Gateway/0.1",
                            "Authorization": "Bearer <the gateway's key: Lethe's pooled key in production; "
                                             "the key you configured in this local POC>"},
                "body": body}
        if not self.p["key"]:
            return ("Dry run: set OPENAI_API_KEY or OPENROUTER_API_KEY for a real answer. "
                    "The request above is exactly what would be sent."), None, view, 0.0
        t = time.perf_counter()
        data, headers = self._post(body)
        ms = (time.perf_counter() - t) * 1000
        if self.p["name"] == "OpenRouter":
            content = data["choices"][0]["message"].get("content") or ""
            if isinstance(content, list):
                content = "".join(part.get("text", "") for part in content if isinstance(part, dict))
            usage = data.get("usage")
        else:
            content = "".join(c.get("text", "") for item in data.get("output", []) if item.get("type") == "message"
                              for c in item.get("content", []) if c.get("type") == "output_text")
            u = data.get("usage") or {}
            usage = {"prompt_tokens": u.get("input_tokens"), "completion_tokens": u.get("output_tokens")}
        view.update(answered_by=data.get("model", model), response_id=data.get("id"),
                    request_id=headers.get("x-request-id"), processing_ms=headers.get("openai-processing-ms"),
                    stored=bool(body.get("store")))
        return content, usage, view, ms

    def stored_input(self, response_id: str) -> list[str]:
        """Ask OpenAI for the input it stored for this response: an independent check of what it received."""
        url = f"https://api.openai.com/v1/responses/{response_id}/input_items?limit=100&order=asc"
        req = urllib.request.Request(url, headers={"Authorization": "Bearer " + self.p["key"]})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                items = json.load(r).get("data", [])
        except urllib.error.HTTPError as e:
            raise LabError(f"OpenAI returned {e.code}: {e.read().decode(errors='replace')[:200]}")
        texts = []
        for it in items:
            content = it.get("content")
            if isinstance(content, str):
                texts.append(f"{it.get('role', '')}: {content}")
            elif isinstance(content, list):
                texts.append(f"{it.get('role', '')}: " + "".join(c.get("text", "") for c in content))
        return texts


class Gateway:
    """Opens sealed requests, checks credentials, forwards under Lethe's key. Never sees an IP or account."""

    def __init__(self, issuer_pub, lab: Lab):
        self.sk, self.pk = lc.gateway_keypair()
        self.n, self.e = issuer_pub
        self.lab = lab
        self.spent: set[str] = set()
        self.view = None
        self.lab_view = None

    def handle(self, blob: bytes, peer: str):
        plaintext, k_res = lc.open_request(self.sk, self.pk, blob)
        req = json.loads(plaintext)
        nonce, sig = bytes.fromhex(req["credential"]["nonce"]), int(req["credential"]["sig"], 16)
        tag = hashlib.sha256(nonce).hexdigest()[:16]
        view = {"from": peer, "credential": short(sig), "credential_tag": tag, "model": req["model"],
                "messages": req["messages"], "bytes_opened": len(plaintext)}
        reply = {}
        if not lc.verify(self.n, self.e, nonce, sig):
            view["status"], reply["error"] = "rejected", "Credential signature is invalid."
        elif tag in self.spent:
            view["status"], reply["error"] = "rejected", "Credential already spent. Replays are refused."
        else:
            self.spent.add(tag)
            view["status"] = "accepted"
            try:
                answer, usage, self.lab_view, ms = self.lab.complete(req["model"], req["messages"])
                reply = {"answer": answer, "usage": usage, "lab_ms": round(ms)}
                lv = self.lab_view
                print(f"[gateway] credential ok · {req['model']} · response {lv.get('response_id')} · "
                      f"request {lv.get('request_id')} · store={lv.get('stored')}", flush=True)
            except LabError as e:
                reply["error"] = str(e)
                print(f"[gateway] lab error: {e}", flush=True)
        if view["status"] != "accepted":
            print(f"[gateway] refused: {reply['error']}", flush=True)
        view["spent_total"] = len(self.spent)
        self.view = view
        return lc.seal_response(k_res, json.dumps(reply).encode()), view


class Relay:
    """Sees who is connecting, and a sealed blob of a fixed size. Strips the IP before forwarding."""

    def __init__(self, gateway: Gateway):
        self.gateway = gateway
        self.view = None

    def forward(self, client_ip: str, blob: bytes) -> bytes:
        resp = self.gateway.handle(blob, peer="relay (your IP stripped)")[0]
        self.view = {"client_ip": client_ip, "request_bytes": len(blob), "response_bytes": len(resp),
                     "preview": blob[:28].hex(), "target": "Lethe gateway (fixed: the relay cannot see which lab)"}
        return resp


class Device:
    """Your machine: the only place the real prompt, the credentials and the vault ever exist."""

    def __init__(self, issuer: Issuer, relay: Relay, gateway_pk: bytes):
        self.issuer, self.relay, self.gateway_pk = issuer, relay, gateway_pk
        self.scrubber = Scrubber()
        self.wallet: list[dict] = []
        self.history: list[dict] = []
        self.last_blob = None
        self.last_k_res = None
        self.originals: set[str] = set()

    def subscribe(self):
        n, e = self.issuer.key.n, self.issuer.key.e
        pending = [lc.blind(n, e) for _ in range(CREDENTIALS_PER_SUBSCRIPTION)]
        signed = self.issuer.subscribe(DEMO_ACCOUNT, DEMO_CARD, [b for _, _, b in pending])
        for (nonce, r, _), sb in zip(pending, signed):
            sig = lc.unblind(n, e, nonce, r, sb)
            self.wallet.append({"nonce": nonce.hex(), "sig": format(sig, "x"), "spent": False})

    def wallet_view(self):
        return {"unspent": sum(not c["spent"] for c in self.wallet), "spent": sum(c["spent"] for c in self.wallet)}

    def ask(self, prompt: str, model: str, hide: list[str], client_ip: str):
        if not any(not c["spent"] for c in self.wallet):
            self.subscribe()  # happens once per subscription, not per request: kept out of the timing
        t0 = time.perf_counter()
        scrubbed = self.scrubber.scrub(prompt, hide)
        self.originals |= {f["original"] for f in scrubbed["found"]}
        cred = next(c for c in self.wallet if not c["spent"])
        cred["spent"] = True
        messages = self.history + [{"role": "user", "content": scrubbed["text"]}]
        inner = json.dumps({"credential": {"nonce": cred["nonce"], "sig": cred["sig"]},
                            "model": model, "messages": messages}).encode()
        blob, k_res = lc.seal_request(self.gateway_pk, inner)
        self.last_blob, self.last_k_res = blob, k_res
        reply = json.loads(lc.open_response(k_res, self.relay.forward(client_ip, blob)))
        total_ms = (time.perf_counter() - t0) * 1000
        result = {"scrub": scrubbed, "spent_credential": short(int(cred["sig"], 16)),
                  "timing": {"scrub_ms": scrubbed["ms"], "lab_ms": reply.get("lab_ms", 0),
                             "total_ms": round(total_ms)}}
        if "error" in reply:
            self.history = messages[:-1]
            result["error"] = reply["error"]
            return result
        self.history = messages + [{"role": "assistant", "content": reply["answer"]}]
        marked, restored = self.scrubber.restore(reply["answer"])
        result.update(answer_raw=reply["answer"], answer=marked, restored=restored, usage=reply.get("usage"))
        result["timing"]["lethe_ms"] = round(total_ms - reply.get("lab_ms", 0), 1)
        return result

    def replay(self, client_ip: str):
        if not self.last_blob:
            return {"error": "Ask something first, then replay its sealed request."}
        reply = json.loads(lc.open_response(self.last_k_res, self.relay.forward(client_ip, self.last_blob)))
        return {"error": reply.get("error")} if "error" in reply else {"error": "Replay was accepted (unexpected)."}

    def new_chat(self):
        self.scrubber.new_chat()
        self.history = []
        self.originals = set()


# ======================================================================== app wiring
class App:
    def __init__(self):
        load_env()
        self.provider = make_provider()
        self.lock = threading.Lock()
        self.issuer = Issuer()
        self.gateway = Gateway((self.issuer.key.n, self.issuer.key.e), Lab(self.provider))
        self.relay = Relay(self.gateway)
        self.device = Device(self.issuer, self.relay, self.gateway.pk)

    def views(self):
        return {"issuer": self.issuer.view, "relay": self.relay.view, "gateway": self.gateway.view,
                "lab": self.gateway.lab_view, "wallet": self.device.wallet_view(),
                "vault": self.device.scrubber.vault_view(), "turns": len(self.device.history) // 2,
                "issuer_saw": self.issuer.seen_blinded[-10:]}

    def status(self):
        return {"provider": self.provider["name"], "has_key": bool(self.provider["key"]),
                "store": self.gateway.lab.store,
                "models": self.provider["models"], "detector": self.device.scrubber.mode,
                "account": DEMO_ACCOUNT, "card": DEMO_CARD, **self.views()}

    def verify(self):
        """Fetch what OpenAI stored for the last request and look for any private original in it."""
        lab = self.gateway.lab_view or {}
        if not lab.get("response_id"):
            raise ValueError("Ask something first (with a real OpenAI key).")
        if not lab.get("stored"):
            raise ValueError("This request was sent with store=false, so OpenAI kept nothing to fetch. "
                             "Restart with LETHE_OPENAI_STORE=1 to verify.")
        texts = self.gateway.lab.stored_input(lab["response_id"])
        joined = "\n".join(texts).lower()
        originals = sorted(self.device.originals)
        standins = [v["standin"] for v in self.device.scrubber.vault_view()]
        return {"response_id": lab["response_id"], "stored_input": texts,
                "originals_checked": len(originals),
                "originals_found": [o for o in originals if o.lower() in joined],
                "standins_found": [s for s in standins if s.lower() in joined]}

    def handle(self, path: str, body: dict, client_ip: str):
        with self.lock:
            if path == "/api/status":
                return self.status()
            if path == "/api/subscribe":
                self.device.subscribe()
                return self.views()
            if path == "/api/ask":
                prompt = str(body.get("prompt", "")).strip()
                if not prompt:
                    raise ValueError("Type a question first.")
                model = self.provider["models"].get(body.get("model")) or next(iter(self.provider["models"].values()))
                hide = [t for t in str(body.get("hide", "")).split(",") if t.strip()]
                return {"result": self.device.ask(prompt, model, hide, client_ip), **self.views()}
            if path == "/api/replay":
                return {"result": self.device.replay(client_ip), **self.views()}
            if path == "/api/verify":
                return self.verify()
            if path == "/api/new_chat":
                self.device.new_chat()
                return self.views()
        raise KeyError(path)


APP = None


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def _send(self, code: int, payload: bytes, ctype: str):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        try:
            self.wfile.write(payload)
        except (BrokenPipeError, ConnectionResetError):
            pass  # the client went away; nothing to do

    def _json(self, code: int, obj):
        self._send(code, json.dumps(obj).encode(), "application/json")

    def do_GET(self):
        if self.path == "/healthz":  # no lock: answers even while a request is waiting on the lab
            return self._json(200, {"ok": True})
        if self.path in ("/", "/index.html"):
            return self._send(200, (HERE / "static" / "index.html").read_bytes(), "text/html; charset=utf-8")
        if self.path == "/api/status":
            return self._json(200, APP.handle("/api/status", {}, self.client_address[0]))
        self._json(404, {"error": "not found"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        try:
            body = json.loads(self.rfile.read(length) or b"{}")
            self._json(200, APP.handle(self.path, body, self.client_address[0]))
        except KeyError:
            self._json(404, {"error": "not found"})
        except Exception as e:  # surface every failure in the UI
            self._json(400, {"error": str(e)})


def main():
    global APP
    APP = App()
    port = int(os.getenv("LETHE_PORT", "8787"))
    host = os.getenv("LETHE_HOST", "127.0.0.1")  # the container sets 0.0.0.0; publish it to localhost only
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Lethe demo on http://localhost:{port}  ·  lab: {APP.provider['name']}  ·  detector: "
          f"{APP.device.scrubber.mode}  ·  OpenAI store: {'on' if APP.gateway.lab.store else 'off'}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
