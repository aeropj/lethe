#!/usr/bin/env python3
"""Lethe local demo: watch what each party in the request path can see, step by step.

One process plays all five parties, each handed only the bytes it would really receive:
  device   scrubs the prompt locally, spends one blind credential, seals the request
  issuer   signs credentials blind when you subscribe; never sees a prompt
  relay    sees your IP and a fixed-size sealed blob it cannot open
  gateway  opens the blob, checks the credential, forwards under Lethe's own key
  lab      OpenAI or OpenRouter; gets one scrubbed question from "Lethe"

Every ask and replay is recorded as a trace: one timed span per step, holding the real bytes that step
handled. The page's Observability view (#/trace) shows them.

Run:  python3 demo/server.py   then open http://localhost:8787
Key:  paste an OpenAI key in the browser. It is kept in this process's memory only. OPENAI_API_KEY or
      OPENROUTER_API_KEY in demo/.env or the environment still work as presets. Without a key it can run dry.
      Verification mode sends "store": true, so you can check on OpenAI's side what it received
      (see VERIFY.md). It is on by default; LETHE_OPENAI_STORE=0 or 1 presets it.
"""
import contextvars
import hashlib
import json
import os
import re
import secrets
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, deque
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lethe_crypto as lc  # noqa: E402
from scrub import Scrubber  # noqa: E402

DEMO_ACCOUNT = "sarah.miller@gmail.com"
DEMO_CARD = "Visa ending 4242"
CREDENTIALS_PER_SUBSCRIPTION = 5
MAX_TRACES = 50
USER_AGENT = "Lethe-Gateway/0.1"
OPENAI_API = "https://api.openai.com/v1"
PREFERRED_MODELS = ("gpt-5.6-luna", "gpt-5.6-sol", "gpt-5.5", "gpt-5.4-mini", "gpt-5-mini", "gpt-4.1-mini",
                    "gpt-4o-mini")
NOT_CHAT = ("audio", "realtime", "transcribe", "tts", "image", "search", "instruct")
DRY_RUN = {"name": "Dry run", "url": f"{OPENAI_API}/responses", "key": None, "source": None,
           "models": {"GPT-5.6 Luna": "gpt-5.6-luna"}}
REFUSED = {"invalid": "Credential signature is invalid.", "spent": "Credential already spent. Replays are refused."}


def load_env():
    f = HERE / ".env"
    if f.exists():
        for line in f.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip("\"'"))


def env_flag(name: str, default: bool) -> bool:
    v = os.getenv(name, "").strip().lower()
    return default if not v else v not in ("0", "false", "no", "off")


def preset_provider():
    """A key preset in the environment or demo/.env, if there is one."""
    if os.getenv("OPENROUTER_API_KEY"):
        return {"name": "OpenRouter", "url": "https://openrouter.ai/api/v1/chat/completions",
                "key": os.environ["OPENROUTER_API_KEY"], "source": "environment",
                "models": {"GPT": os.getenv("LETHE_MODEL_GPT", "openai/gpt-5.6-luna"),
                           "Claude": os.getenv("LETHE_MODEL_CLAUDE", "anthropic/claude-haiku-5.5"),
                           "Gemini": os.getenv("LETHE_MODEL_GEMINI", "google/gemini-3.5-flash-lite")}}
    if os.getenv("OPENAI_API_KEY"):
        return {"name": "OpenAI", "url": f"{OPENAI_API}/responses", "key": os.environ["OPENAI_API_KEY"],
                "source": "environment",
                "models": {"GPT-5.6 Luna": "gpt-5.6-luna", "GPT-5.6 Sol": "gpt-5.6-sol",
                           "GPT-5.4 mini": "gpt-5.4-mini"}}
    return dict(DRY_RUN)


def mask(key: str | None) -> str | None:
    """sk-…abcd: enough to recognise a key, never enough to use it."""
    return f"{key[:3]}…{key[-4:]}" if key and len(key) > 12 else ("…" if key else None)


def model_label(model_id: str) -> str:
    """gpt-5.6-luna -> GPT-5.6 Luna, gpt-4o-mini -> GPT-4o mini."""
    parts = model_id.split("-")
    if len(parts) < 2 or parts[0] != "gpt":
        return model_id
    return " ".join(["GPT-" + parts[1]] + [p if p in ("mini", "nano") else p.capitalize() for p in parts[2:]])


def openai_models(key: str) -> dict:
    """Check a key with GET /v1/models and pick up to three chat models it can use."""
    req = urllib.request.Request(f"{OPENAI_API}/models",
                                 headers={"Authorization": "Bearer " + key, "User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            ids = {m.get("id", "") for m in json.load(r).get("data", [])}
    except urllib.error.HTTPError as e:
        raise ValueError({
            401: "OpenAI did not accept this key (401 Unauthorized). Check that you copied all of it and that "
                 "it has not been revoked.",
            403: "OpenAI refused this key (403 Forbidden). It may be a restricted key without model access.",
            429: "OpenAI is rate limiting this key (429). Wait a moment, or check the project's billing.",
        }.get(e.code, f"OpenAI answered {e.code} while checking the key. Try again in a moment.")) from None
    except (OSError, ValueError) as e:  # no network, DNS, timeout, or a garbled reply
        raise ValueError(f"Could not reach api.openai.com to check the key ({getattr(e, 'reason', e)}). "
                         "Check this machine's internet connection.") from None
    picked = [m for m in PREFERRED_MODELS if m in ids][:3] or sorted(
        (m for m in ids if m.startswith("gpt-") and not any(w in m for w in NOT_CHAT)
         and not re.search(r"\d{4}-\d{2}-\d{2}$", m)), reverse=True)[:3]
    if not picked:
        raise ValueError("This key works, but its project cannot use any GPT models. Allow model access for the "
                         "project on platform.openai.com, or use another key.")
    return {model_label(m): m for m in picked}


def short(x) -> str:
    h = x.hex() if isinstance(x, bytes) else format(x, "x")
    return h[:20] + "…"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()[:16]


def for_display(inner: bytes) -> str:
    """The sealed JSON exactly as built, with the long credential values shortened to fit on screen."""
    text = inner.decode()
    cred = json.loads(text)["credential"]
    for v in (cred["nonce"], cred["sig"]):
        text = text.replace(v, v[:16] + "…", 1)
    return text


class LabError(Exception):
    pass


class NoRoute(Exception):
    pass


# ======================================================================== tracing
class Trace:
    """One request's journey. Each step adds a span, timed inside the code path that does the work.

    The clock starts at the first span, so a one-off subscribe before the first ask is not counted.
    """

    def __init__(self, kind: str, model: str, prompt: str):
        self.t0 = None
        self.id = "tr_" + secrets.token_hex(5)
        self.d = {"id": self.id, "created_at": time.time(), "kind": kind, "status": "ok", "model": model,
                  "prompt_original": prompt, "spans": [], "summary": {}, "verification": None}

    def now_ms(self) -> float:
        if self.t0 is None:
            self.t0 = time.perf_counter()
        return (time.perf_counter() - self.t0) * 1000

    def data(self, key: str) -> dict:
        return next((s["data"] for s in self.d["spans"] if s["key"] == key), {})

    def finish(self, error: str | None = None):
        total = self.now_ms()
        lab, usage = self.data("lab"), self.data("lab").get("usage") or {}
        lab_ms = lab.get("latency_ms") or 0.0
        if self.data("open").get("check") in REFUSED:
            self.d["status"] = "refused"
        elif error:
            self.d["status"], self.d["error"] = "error", error
        self.d["summary"] = {
            "total_ms": round(total, 2), "lethe_ms": round(total - lab_ms, 2), "lab_ms": round(lab_ms, 2),
            "tokens_in": usage.get("prompt_tokens"), "tokens_out": usage.get("completion_tokens"),
            "hidden_count": len(self.data("detect").get("entities", [])),
            "wire_bytes_out": self.data("relay").get("bytes_in", 0),
            "wire_bytes_back": self.data("relay").get("bytes_back", 0)}

    def brief(self) -> dict:
        d, v = self.d, self.d["verification"]
        return {"id": d["id"], "created_at": d["created_at"], "kind": d["kind"], "status": d["status"],
                "model": d["model"], "prompt": d["prompt_original"][:120], **d["summary"],
                "verified": None if not v else ("clean" if not v["originals_found"] else "found")}


_current_trace = contextvars.ContextVar("lethe_trace", default=None)


@contextmanager
def span(key: str, title: str, party: str):
    """Time one step of the current trace and collect what it handled. Yields the span's data dict.

    Fill the dict after the `with` block when building the display data costs more than the step itself.
    """
    trace, data = _current_trace.get(), {}
    if trace is None:
        yield data
        return
    s = {"key": key, "title": title, "party": party, "start_ms": round(trace.now_ms(), 3), "dur_ms": 0.0,
         "status": "ok", "data": data}
    trace.d["spans"].append(s)
    t = time.perf_counter()
    try:
        yield data
    except Exception as e:
        data["error"] = str(e)
        raise
    finally:
        s["dur_ms"] = round((time.perf_counter() - t) * 1000, 4)
        if "error" in data:
            s["status"] = "error"


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
    with store on, OpenAI keeps it, and GET /v1/responses/{id}/input_items returns exactly the
    input OpenAI received.
    """

    def __init__(self, provider, store: bool):
        self.p = provider
        self.store = store and provider["name"] == "OpenAI"

    def _post(self, payload: bytes):
        headers = {"Content-Type": "application/json", "User-Agent": USER_AGENT}
        req = urllib.request.Request(self.p["url"], data=payload,
                                     headers=dict(headers, Authorization="Bearer " + self.p["key"]))
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.load(r), r.headers, r.status
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
        payload, url = json.dumps(body).encode(), urllib.parse.urlsplit(self.p["url"])
        key = self.p["key"]
        # the headers in the order urllib puts them on the wire; the key itself never enters a trace
        wire = {"Accept-Encoding": "identity", "Content-Length": str(len(payload)), "Host": url.netloc,
                "Content-Type": "application/json", "User-Agent": USER_AGENT,
                "Authorization": f"Bearer {mask(key)} (redacted)" if key else "Bearer <no key: dry run>",
                "Connection": "close"}
        sent = {"provider": self.p["name"], "url": self.p["url"], "request_line": f"POST {url.path} HTTP/1.1",
                "headers": wire, "body": body, "request_bytes": len(payload), "stored": self.store}
        view = {"request": f"POST {self.p['url']}",
                "headers": {"Content-Type": "application/json", "User-Agent": USER_AGENT,
                            "Authorization": "Bearer <the gateway's key: Lethe's pooled key in production; "
                                             "the key you configured in this local POC>"},
                "body": body}
        with span("lab", f"{self.p['name'] if key else 'The lab'} answers", "lab") as d:
            d.update(sent)
            if not key:
                answer = ("Dry run: add an OpenAI key for a real answer. "
                          "The request above is exactly what would be sent.")
                d.update(dry_run=True, answer_raw=answer)
                return answer, None, view, 0.0
            t = time.perf_counter()
            data, headers, status = self._post(payload)
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
        d.update(http_status=status, latency_ms=round(ms, 2), answered_by=view["answered_by"],
                 response_id=view["response_id"], request_id=view["request_id"],
                 processing_ms=view["processing_ms"], usage=usage, answer_raw=content, response=data,
                 response_headers={k.lower(): v for k, v in headers.items()
                                   if k.lower() in ("content-type", "x-request-id", "openai-processing-ms", "openai-version")
                                   or k.lower().startswith("x-ratelimit-")})
        return content, usage, view, ms

    def stored_input(self, response_id: str) -> list[str]:
        """Ask OpenAI for the input it stored for this response: an independent check of what it received."""
        url = f"{OPENAI_API}/responses/{response_id}/input_items?limit=100&order=asc"
        req = urllib.request.Request(url, headers={"Authorization": "Bearer " + self.p["key"]})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                items = json.load(r).get("data", [])
        except urllib.error.HTTPError as e:
            raise LabError(f"OpenAI returned {e.code}: {e.read().decode(errors='replace')[:200]}")
        except urllib.error.URLError as e:
            raise LabError(f"Could not reach OpenAI: {e.reason}")
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
        with span("open", "Gateway opens it and checks the credential", "gateway") as d:
            plaintext, k_res = lc.open_request(self.sk, self.pk, blob)
            req = json.loads(plaintext)
            nonce, sig = bytes.fromhex(req["credential"]["nonce"]), int(req["credential"]["sig"], 16)
            tag = hashlib.sha256(nonce).hexdigest()[:16]
            check = "invalid" if not lc.verify(self.n, self.e, nonce, sig) else "spent" if tag in self.spent else "valid"
            if check == "valid":
                self.spent.add(tag)
            else:
                d["error"] = REFUSED[check]
        d.update(came_from=peer, bytes_in=len(blob), bytes_opened=len(plaintext), plaintext=for_display(plaintext),
                 plaintext_sha256=sha(plaintext), credential=short(sig), credential_tag=tag, check=check,
                 spent_total=len(self.spent), model=req["model"], messages=len(req["messages"]))
        view = {"from": peer, "credential": short(sig), "credential_tag": tag, "model": req["model"],
                "messages": req["messages"], "bytes_opened": len(plaintext),
                "status": "accepted" if check == "valid" else "rejected"}
        reply = {}
        if check != "valid":
            reply["error"] = REFUSED[check]
            print(f"[gateway] refused: {reply['error']}", flush=True)
        else:
            try:
                answer, usage, self.lab_view, ms = self.lab.complete(req["model"], req["messages"])
                reply = {"answer": answer, "usage": usage, "lab_ms": round(ms)}
                lv = self.lab_view
                print(f"[gateway] credential ok · {req['model']} · response {lv.get('response_id')} · "
                      f"request {lv.get('request_id')} · store={lv.get('stored')}", flush=True)
            except LabError as e:
                reply["error"] = str(e)
                print(f"[gateway] lab error: {e}", flush=True)
        view["spent_total"] = len(self.spent)
        self.view = view
        with span("seal_back", "Gateway seals the answer", "gateway") as d:
            out = json.dumps(reply).encode()
            sealed = lc.seal_response(k_res, out)
        d.update(carries="answer" if "answer" in reply else "refusal" if check != "valid" else "error",
                 answer_bytes=len(out), padded_bytes=lc.bucket(len(out)),
                 ciphertext_bytes=len(sealed) - lc.NONCE_BYTES, sealed_bytes=len(sealed),
                 nonce=sealed[:lc.NONCE_BYTES].hex(), head=sealed[:128].hex(), algorithm=lc.ALGORITHM)
        return sealed, view


class Relay:
    """Sees who is connecting, and a sealed blob of a fixed size. Strips the IP before forwarding."""

    def __init__(self, gateway: Gateway):
        self.gateway = gateway
        self.view = None

    def forward(self, client_ip: str, blob: bytes) -> bytes:
        target = "Lethe gateway (fixed: the relay cannot see which lab)"
        with span("relay", "Relay passes it on", "relay") as d:
            d.update(client_ip=client_ip, bytes_in=len(blob), forwards_bytes=len(blob), forwards_ip=None,
                     target=target, preview=blob[:28].hex())
        resp = self.gateway.handle(blob, peer="relay (your IP stripped)")[0]
        d["bytes_back"] = len(resp)
        self.view = {"client_ip": client_ip, "request_bytes": len(blob), "response_bytes": len(resp),
                     "preview": blob[:28].hex(), "target": target}
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
        self.last_prompt = self.last_model = None
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
        with span("detect", "Find private details", "device") as d:
            scrubbed = self.scrubber.scrub(prompt, hide)
        self.originals |= {f["original"] for f in scrubbed["found"]}
        d.update(prompt=prompt, sent=scrubbed["text"], orig_segments=scrubbed["orig_segments"],
                 scrub_segments=scrubbed["scrub_segments"], entities=scrubbed["found"], always_hide=hide,
                 detector=self.scrubber.mode, scrub_ms=scrubbed["ms"], chat_originals=sorted(self.originals),
                 chat_standins=sorted(self.scrubber.vault))

        with span("credential", "Spend one blind credential", "device") as d:
            cred = next(c for c in self.wallet if not c["spent"])
            cred["spent"] = True
        d.update(credential=short(int(cred["sig"], 16)), nonce=cred["nonce"][:16] + "…",
                 wallet=self.wallet_view(), issuer=self.issuer.view)

        with span("seal", "Seal it for the gateway", "device") as d:
            messages = self.history + [{"role": "user", "content": scrubbed["text"]}]
            inner = json.dumps({"credential": {"nonce": cred["nonce"], "sig": cred["sig"]},
                                "model": model, "messages": messages}).encode()
            blob, k_res = lc.seal_request(self.gateway_pk, inner)
        enc, nonce, ct = lc.split_request(blob)
        d.update(plaintext=for_display(inner), plaintext_bytes=len(inner), plaintext_sha256=sha(inner),
                 padded_bytes=lc.bucket(len(inner)), ciphertext_bytes=len(ct), sealed_bytes=len(blob),
                 algorithm=lc.ALGORITHM, ephemeral_pk=enc.hex(), nonce=nonce.hex(), ciphertext_head=ct[:256].hex(),
                 blob_sha256=sha(blob))

        self.last_blob, self.last_k_res = blob, k_res
        self.last_prompt, self.last_model = prompt, model
        reply = self._receive(k_res, self.relay.forward(client_ip, blob))
        result = {"scrub": scrubbed, "spent_credential": short(int(cred["sig"], 16)),
                  "timing": {"scrub_ms": scrubbed["ms"]}}
        if "error" in reply:
            self.history = messages[:-1]
            result["error"] = reply["error"]
            return result
        self.history = messages + [{"role": "assistant", "content": reply["answer"]}]

        with span("restore", "Put the real names back", "device") as d:
            marked, restored = self.scrubber.restore(reply["answer"])
        d.update(answer_raw=reply["answer"], answer=marked, vault=self.scrubber.vault_view(),
                 restorations=[{"standin": s, "original": self.scrubber.vault[s][0], "count": n}
                               for s, n in Counter(restored).items()])
        result.update(answer_raw=reply["answer"], answer=marked, restored=restored, usage=reply.get("usage"))
        return result

    def _receive(self, k_res: bytes, sealed: bytes) -> dict:
        with span("open_back", "Your device opens the answer", "device") as d:
            plaintext = lc.open_response(k_res, sealed)
        reply = json.loads(plaintext)
        d.update(bytes_in=len(sealed), bytes_decrypted=len(plaintext), algorithm=lc.ALGORITHM,
                 carries="answer" if "answer" in reply else "error", reply_error=reply.get("error"))
        return reply

    def replay(self, client_ip: str):
        if not self.last_blob:
            return {"error": "Ask something first, then replay its sealed request."}
        with span("resend", "Re-send the captured request, byte for byte", "device") as d:
            blob = self.last_blob
        d.update(sealed_bytes=len(blob), blob_sha256=sha(blob))
        reply = self._receive(self.last_k_res, self.relay.forward(client_ip, blob))
        return {"error": reply["error"]} if "error" in reply else {"error": "Replay was accepted (unexpected)."}

    def new_chat(self):
        self.scrubber.new_chat()
        self.history = []
        self.originals = set()


# ======================================================================== app wiring
class App:
    def __init__(self):
        load_env()
        self.lock = threading.Lock()
        self.store_pref = env_flag("LETHE_OPENAI_STORE", True)  # verification mode; the UI toggle changes it
        self.provider = preset_provider()
        self.issuer = Issuer()
        self.gateway = Gateway((self.issuer.key.n, self.issuer.key.e), Lab(self.provider, self.store_pref))
        self.relay = Relay(self.gateway)
        self.device = Device(self.issuer, self.relay, self.gateway.pk)
        self.traces: deque[Trace] = deque(maxlen=MAX_TRACES)
        self.traces_lock = threading.Lock()
        self.last_ask_trace = None

    # ------------------------------------------------------------ key and settings
    def use(self, provider):
        self.provider = provider
        self.gateway.lab = Lab(provider, self.store_pref)

    def redact(self, text: str) -> str:
        key = self.provider.get("key")
        return text.replace(key, mask(key)) if key else text

    def set_key(self, body: dict):
        key = str(body.get("key") or "").strip()
        if not key:
            raise ValueError("Paste your OpenAI API key first.")
        if not key.isascii() or not key.isprintable() or " " in key:
            raise ValueError("That does not look like an OpenAI API key. Keys start with sk- and have no spaces.")
        models = openai_models(key)  # a network call: outside the lock, so the page stays responsive
        with self.lock:
            self.store_pref = bool(body.get("store", True))
            self.use({"name": "OpenAI", "url": f"{OPENAI_API}/responses", "key": key, "source": "browser",
                      "models": models})
            print(f"[setup] OpenAI key {mask(key)} connected · models {', '.join(models.values())} · "
                  f"verification mode {'on' if self.store_pref else 'off'}", flush=True)
            return self.status()

    # ------------------------------------------------------------ traces
    def traced(self, kind: str, model: str, prompt: str, run, **extra):
        trace = Trace(kind, model, prompt)
        trace.d.update(extra)
        token = _current_trace.set(trace)
        try:
            result = run()
            trace.finish(result.get("error"))
        except Exception as e:
            trace.finish(self.redact(str(e)))
            raise
        finally:
            _current_trace.reset(token)
            with self.traces_lock:
                self.traces.append(trace)
        s = trace.d["summary"]
        result["trace_id"] = trace.id
        result["timing"] = {**result.get("timing", {}), "lab_ms": round(s["lab_ms"]),
                            "total_ms": round(s["total_ms"]), "lethe_ms": round(s["lethe_ms"], 1)}
        return result

    def trace_list(self):
        with self.traces_lock:
            return {"traces": [t.brief() for t in reversed(self.traces)]}

    def trace(self, trace_id: str):
        with self.traces_lock:
            return next((t for t in self.traces if t.id == trace_id), None)

    def views(self):
        return {"issuer": self.issuer.view, "relay": self.relay.view, "gateway": self.gateway.view,
                "lab": self.gateway.lab_view, "wallet": self.device.wallet_view(),
                "vault": self.device.scrubber.vault_view(), "turns": len(self.device.history) // 2,
                "issuer_saw": self.issuer.seen_blinded[-10:], "trace_count": len(self.traces)}

    def status(self):
        p = self.provider
        return {"provider": p["name"], "has_key": bool(p["key"]), "masked_key": mask(p["key"]),
                "key_source": p.get("source"), "store": self.store_pref,
                "models": p["models"], "detector": self.device.scrubber.mode,
                "account": DEMO_ACCOUNT, "card": DEMO_CARD, **self.views()}

    def verify(self, trace_id: str | None = None):
        """Fetch what OpenAI stored for one traced request and look for any private original in it."""
        with self.traces_lock:
            traces = list(self.traces)
        if trace_id:
            trace = next((t for t in traces if t.id == trace_id), None)
            if not trace:
                raise ValueError("No such trace. Traces live in memory and reset when the server restarts.")
        else:
            trace = next((t for t in reversed(traces) if t.data("lab").get("response_id")), None)
            if not trace:
                raise ValueError("Ask something first (with a real OpenAI key).")
        lab = trace.data("lab")
        if not lab.get("response_id"):
            raise ValueError("Nothing to check: this request never reached OpenAI (dry run, replay or error).")
        if not lab.get("stored"):
            raise ValueError("This request was sent with store=false, so OpenAI kept nothing to fetch. "
                             "Turn on Verification mode in the key settings and ask again.")
        if self.provider["name"] != "OpenAI":
            raise ValueError("Connect an OpenAI key to check what OpenAI stored.")
        texts = self.gateway.lab.stored_input(lab["response_id"])
        joined = "\n".join(texts).lower()
        detect = trace.data("detect")
        originals, standins = detect.get("chat_originals", []), detect.get("chat_standins", [])
        result = {"trace_id": trace.id, "response_id": lab["response_id"], "request_id": lab.get("request_id"),
                  "checked_at": time.time(), "stored_input": texts, "originals_checked": len(originals),
                  "originals": originals, "originals_found": [o for o in originals if o.lower() in joined],
                  "standins_found": [s for s in standins if s.lower() in joined]}
        trace.d["verification"] = result
        return result

    def handle(self, path: str, body: dict, client_ip: str):
        if path == "/api/key":
            return self.set_key(body)
        with self.lock:
            if path == "/api/status":
                return self.status()
            if path == "/api/key/forget":
                self.use(dict(DRY_RUN))
                print("[setup] key forgotten", flush=True)
                return self.status()
            if path == "/api/settings":
                self.store_pref = bool(body.get("store"))
                self.use(self.provider)
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
                result = self.traced("ask", model, prompt, lambda: self.device.ask(prompt, model, hide, client_ip))
                self.last_ask_trace = result["trace_id"]
                return {"result": result, **self.views()}
            if path == "/api/replay":
                if not self.device.last_blob:
                    return {"result": self.device.replay(client_ip), **self.views()}
                result = self.traced("replay", self.device.last_model, self.device.last_prompt,
                                     lambda: self.device.replay(client_ip), replay_of=self.last_ask_trace)
                return {"result": result, **self.views()}
            if path == "/api/verify":
                return self.verify(body.get("trace_id"))
            if path == "/api/new_chat":
                self.device.new_chat()
                return self.views()
        raise NoRoute(path)


APP = None
ALLOWED_HOSTS = {"localhost", "127.0.0.1", "::1"} | {
    h.strip().lower() for h in os.getenv("LETHE_ALLOWED_HOSTS", "").split(",") if h.strip()}


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

    def _local(self) -> bool:
        """This server holds a key and private prompts, so it only answers to localhost names.

        That stops a web page from reaching it through DNS rebinding. LETHE_ALLOWED_HOSTS adds names.
        """
        host = (urllib.parse.urlsplit("//" + self.headers.get("Host", "")).hostname or "").lower()
        return host in ALLOWED_HOSTS or host.endswith(".localhost")

    def do_GET(self):
        path = urllib.parse.urlsplit(self.path).path
        if path == "/healthz":  # no lock: answers even while a request is waiting on the lab
            return self._json(200, {"ok": True})
        if not self._local():
            return self._json(403, {"error": "Open this demo at http://localhost (or set LETHE_ALLOWED_HOSTS)."})
        if path in ("/", "/index.html"):
            return self._send(200, (HERE / "static" / "index.html").read_bytes(), "text/html; charset=utf-8")
        if path == "/api/status":
            return self._json(200, APP.handle("/api/status", {}, self.client_address[0]))
        if path == "/api/traces":  # no lock: the list stays readable while a request is in flight
            return self._json(200, APP.trace_list())
        if path.startswith("/api/traces/"):
            trace = APP.trace(path.rsplit("/", 1)[1])
            return self._json(200, trace.d) if trace else self._json(
                404, {"error": "No such trace. Traces live in memory and reset when the server restarts."})
        self._json(404, {"error": "not found"})

    def do_POST(self):
        if not self._local():
            return self._json(403, {"error": "Open this demo at http://localhost (or set LETHE_ALLOWED_HOSTS)."})
        if not self.headers.get("Content-Type", "").startswith("application/json"):
            return self._json(415, {"error": "Send JSON."})  # plain HTML forms from other sites cannot
        length = int(self.headers.get("Content-Length") or 0)
        try:
            body = json.loads(self.rfile.read(length) or b"{}")
            self._json(200, APP.handle(self.path, body, self.client_address[0]))
        except NoRoute:
            self._json(404, {"error": "not found"})
        except Exception as e:  # surface every failure in the UI, never the key
            self._json(400, {"error": APP.redact(str(e))})


def main():
    global APP
    APP = App()
    port = int(os.getenv("LETHE_PORT", "8787"))
    host = os.getenv("LETHE_HOST", "127.0.0.1")  # the container sets 0.0.0.0; publish it to localhost only
    server = ThreadingHTTPServer((host, port), Handler)
    p = APP.provider
    key = f"{p['name']} key from the environment ({mask(p['key'])})" if p["key"] else "no key yet: paste one in the page"
    print(f"Lethe demo on http://localhost:{port}  ·  {key}  ·  detector: {APP.device.scrubber.mode}  ·  "
          f"verification mode: {'on' if APP.store_pref else 'off'}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
