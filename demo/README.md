# Lethe local demo

Ask a frontier model a personal question and watch what every party in the path actually sees.
This is the first piece of Lethe, a privacy layer for AI. It starts with your own questions. The same
layer is meant to sit later under browsers, health apps, email, coding agents, company tools and agent
swarms: anywhere a request leaves for a model.

![the film](video/out/poster.png)

## Run it

```bash
pip install cryptography          # the only dependency
cp demo/.env.example demo/.env    # then put your OpenAI or OpenRouter key in it
python3 demo/server.py            # open http://localhost:8787
```

With no key it runs dry: every step happens, and the lab card shows the exact request that would be sent.
`demo/.env` is git-ignored.

## What happens when you press "Ask privately"

| Party | Gets | Never gets |
|---|---|---|
| **Your device** | everything; it scrubs the prompt in ~1–4 ms, keeps the vault | — |
| **Issuer** (at subscribe) | your account and card, and 5 *blinded* credentials it signs | which credential you spend, any prompt |
| **Relay** | your IP and a sealed blob padded to a fixed size | the prompt, the credential, the lab |
| **Gateway** | a valid one-time credential and the scrubbed question | your IP, account, card, real names |
| **Lab** | one request from Lethe's key, with stand-ins | anything about you |

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
