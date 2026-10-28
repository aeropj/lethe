# Lethe local demo

Ask a frontier model a personal question and watch what every party in the path actually sees.
This is the first piece of Lethe, a privacy layer for AI. It starts with your own questions. The same
layer is meant to sit later under browsers, health apps, email, coding agents, company tools and agent
swarms: anywhere a request leaves for a model.

![the film](video/out/poster.png)

## Run it

With Docker (recommended), straight from [Docker Hub](https://hub.docker.com/r/aeropj/lethe-demo):

```bash
docker run --rm -p 127.0.0.1:8787:8787 aeropj/lethe-demo     # open http://localhost:8787
```

To build it yourself instead: `docker build -t lethe-demo demo`.

The page opens on a key screen. Paste an OpenAI API key and press Connect. The server checks it against
`GET /v1/models`, picks up to three GPT models your project can use, and keeps the key in the container's
memory only: it is never written to disk, logged, or sent anywhere except api.openai.com. The key menu in
the header shows it masked, and can change or forget it. "Try a dry run" skips the key: every step still
happens, and the trace shows the exact request that would be sent.

Presets still work: `-e OPENAI_API_KEY` (or `OPENROUTER_API_KEY`) skips the key screen, and
`LETHE_OPENAI_STORE=0` or `1` sets verification mode. `docker compose up --build` reads them from
`demo/.env`, which is git-ignored and excluded from the image.

Without Docker:

```bash
pip install cryptography
python3 demo/server.py
```

The port is published to localhost only. The server spends your key and has no login, so do not expose it.

## Observability

Every question and replay is traced. Open **Observability** in the header, or **Open trace** under an
answer, to see one request end to end:

- **KPIs**: total latency, Lethe's overhead (a few milliseconds, well under 1% of a model call), model
  latency, tokens, details hidden, sealed bytes on the wire, verification status.
- **Waterfall**: the nine steps on one clock, coloured by party. "Zoom Lethe steps" compresses the model
  call so the on-device and gateway steps are readable.
- **The journey**: each step's real input and output. The highlighted swap and entity table, the sealed
  request as a hex dump with its sizes (plaintext, padded, ciphertext, on the wire), what the relay saw,
  the gateway's decrypted payload and credential check, the exact HTTP request and response from OpenAI,
  the sealed answer, and the restore as a side-by-side diff with the vault.
- **Prove it**: fetches OpenAI's stored copy of the request and searches it for every private detail.
  Copy the response and request IDs, or a `curl` to check yourself. See [VERIFY.md](VERIFY.md).
- **Export trace JSON** downloads the whole trace. Traces live in memory (the last 50) and the key never
  enters one.

**Verify on OpenAI's side** that it never received your real details: [VERIFY.md](VERIFY.md). With
verification mode on (the default) OpenAI keeps each request for 30 days, so "Verify with OpenAI" can
fetch it back and search it for everything you typed. Turn it off in the key menu for normal use.

## What happens when you press "Ask privately"

| Party | Gets | Never gets |
|---|---|---|
| **Your device** | everything; it scrubs the prompt in ~1–4 ms, keeps the vault | — |
| **Issuer** (at subscribe) | your account and card, and 5 *blinded* credentials it signs | which credential you spend, any prompt |
| **Relay** | your IP and a sealed blob padded to a fixed size | the prompt, the credential, the lab |
| **Gateway** | a valid one-time credential and the scrubbed question | your IP, account, card, real names |
| **Lab** | one request from the gateway's key, with stand-ins | anything about you (in production; in this local POC it sees your key and IP) |

- **Swaps on device.** Names, emails and phones become consistent stand-ins that are swapped back into the
  answer. Cities become their state, insurers and employers their category. SSNs, card numbers, street
  addresses and ZIPs are removed. Anything in "Always hide" becomes a codename. Stand-ins rotate per chat.
- **Blind credentials.** RSA-FDH blind signatures, the idea behind Privacy Pass (RFC 9474/9578).
- **Sealed requests.** X25519 + HKDF + ChaCha20-Poly1305, the shape of Oblivious HTTP (RFC 9458), padded to
  fixed buckets.
- **Single use.** "Replay the last sealed request" is refused: abuse is rate-limited without identity.
- **Optional local model.** `LETHE_LOCAL_MODEL=qwen3:1.7b` (after `ollama pull qwen3:1.7b`) adds a small
  on-device model to the rules.

Demo-grade: real primitives, one process, not audited. The relay and gateway would be separate operators.

## Four tested examples

`python3 demo/run_examples.py` runs a parent's medication question (two turns), a non-compete question, a
tenant's deposit question with an SSN, and a confidential work email, then a replay. Results:
[examples/RESULTS.md](examples/RESULTS.md).

## The film

`video/lethe-video.html` is the film as an HTML timeline. `python3 demo/video/render.py` captures it frame by
frame with headless Chrome, `music.py` synthesises the score, and ffmpeg muxes them into
`video/out/lethe-demo.mp4`.
