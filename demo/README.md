# Lethe local demo

Ask a frontier model a personal question and watch what every party in the path actually sees.
This is the first piece of Lethe, a privacy layer for AI. It starts with your own questions. The same
layer is meant to sit later under browsers, health apps, email, coding agents, company tools and agent
swarms: anywhere a request leaves for a model.

![the film](video/out/poster.png)

## Run it

```bash
./demo/run.sh            # from the repo root; open http://localhost:8787
```

It makes a local Python environment in `demo/.venv`, installs `requirements.txt` (CPU PyTorch, GLiNER,
phonenumbers, cryptography), and starts the server. The first start downloads the PII model (~1.2 GB, from
Hugging Face) and the GeoNames city list once. The page is usable while the model loads (~20–40 s); the
header shows when detection is ready.

The page opens on a key screen. Paste an OpenAI API key and press Connect. The server checks it against
`GET /v1/models`, picks up to three GPT models your project can use, and keeps the key in the container's
memory only (this process, or the container): it is never written to disk, logged, or sent anywhere except api.openai.com. The key menu in
the header shows it masked, and can change or forget it. "Try a dry run" skips the key: every step still
happens, and the trace shows the exact request that would be sent.

Presets still work: `OPENAI_API_KEY` (or `OPENROUTER_API_KEY`) in the environment or in `demo/.env`
(git-ignored) skips the key screen, and `LETHE_OPENAI_STORE=0` or `1` sets verification mode.
A `Dockerfile` is included if you prefer a container (`docker build -t lethe-demo demo`).

Without Docker:

```bash
pip install cryptography
python3 demo/server.py
```

The port is published to localhost only. The server spends your key and has no login, so do not expose it.

## Observability

Every question and replay is traced. Open **Observability** in the header, or **Open trace** under an
answer, to see one request end to end:

- **KPIs**: total latency, Lethe's overhead (mostly the on-device model, ~0.1–0.4 s), model
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
| **Your device** | everything; its model finds personal details in ~0.1–0.4 s, keeps the vault | — |
| **Issuer** (at subscribe) | your account and card, and 5 *blinded* credentials it signs | which credential you spend, any prompt |
| **Relay** | your IP and a sealed blob padded to a fixed size | the prompt, the credential, the lab |
| **Gateway** | a valid one-time credential and the scrubbed question | your IP, account, card, real names |
| **Lab** | one request from the gateway's key, with stand-ins | anything about you (in production; in this local POC it sees your key and IP) |

- **Finds details on device.** A multilingual PII model ([GLiNER](https://github.com/urchade/GLiNER),
  `urchade/gliner_multi_pii-v1`) runs locally and tags people, places, organisations, street addresses, ages,
  occupations and IDs in any casing or language. Checksummed patterns add emails, phone numbers for any country,
  cards, IBANs, crypto wallets and national IDs (SSN, PAN, Aadhaar, NINO, NHS, CPF, SIN, RFC/CURP and more).
  A GeoNames gazetteer (CC BY 4.0) maps any city to its state and country. See [eval/](eval/) for the scores.
- **Swaps, generalises or removes.** People, contacts, organisations and "always hide" terms become stand-ins
  that are swapped back into the answer. Cities become their state, exact adult ages a decade ("60-something"),
  occupations a category ("teacher"), well-known employers their kind. IDs, cards, street addresses and postcodes
  are removed. Stand-ins rotate per chat.
- **You stay in control.** The live preview shows what would be sent; click any word to hide it or any highlight
  to keep it. If nothing is found, sending needs a second click.
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
