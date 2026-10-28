# Lethe

**The privacy layer for AI.** Use GPT, Claude and Gemini at full capability without handing over who you
are. It starts with your own questions; the same layer is meant to sit under every app, service and agent
that calls a model.

Pranjal Joshi · Prashil Bulbule · Vaibhav

![Lethe demo film](demo/video/out/poster.png)

## Try it in one command

Needs Docker and an OpenAI API key.

```bash
docker run --rm -p 127.0.0.1:8787:8787 aeropj/lethe-demo
```

Open http://localhost:8787 and paste your key. It stays in the container's memory and goes only to
api.openai.com. Works on Intel and Apple-silicon machines ([Docker Hub](https://hub.docker.com/r/aeropj/lethe-demo)).

Ask a personal question and watch what each party receives: your device swaps names, places and IDs for
stand-ins, a blind credential pays for the request, a relay sees only sealed bytes, and the model gets one
scrubbed question. The **Observability** tab traces every request in nine timed steps, with the real bytes,
and **Prove it** asks OpenAI for its own stored copy to show none of your details are in it.
Steps to check it yourself on platform.openai.com: [demo/VERIFY.md](demo/VERIFY.md).

More: [demo/README.md](demo/README.md) · four tested examples in
[demo/examples/RESULTS.md](demo/examples/RESULTS.md) · the films in [demo/video/out/](demo/video/out/).

## Read

| | |
|---|---|
| [LETHE.md](LETHE.md) | The complete document: thesis, evidence, plan, risks, next steps. Start here. |
| [pitch/three.pdf](pitch/three.pdf) | Three pages, no prose: why and what, how, money and funding. |
| [pitch/crypto.pdf](pitch/crypto.pdf) | Why encryption alone can't hide you from a model, and what can. |
| [research/landscape/landscape.pdf](research/landscape/landscape.pdf) | Competitive landscape and the frank verdict, October 2026. |
| [reports/](reports/) | The long-form landscape report. |
| [research/](research/) | The research behind it: the nearest open-source build, the academic frontier, startup and YC sweeps, profiling channels, patents, bitchat, OpenRouter. |

## Superseded, kept for the record

- `paper/lethe.tex`, `proposal/index.html` — pitch the private-pool model the October research disproved.
- `paper/slides.tex` — the original tokenisation plan.
- `STRATEGY.md`, `yc-application.md` — early drafts, replaced by `LETHE.md`.

## What changed, and when

The project began as a reversible identity-tokenisation harness. Research in September 2026 showed that
the mechanism was already published and patented, that per-provider surrogate rotation does not defeat
linkage, and that four of the ten channels through which a profile gets built close with cryptography at
no cost to answer quality. The company moved from hiding what is in a prompt to hiding who is asking, and
the demo now does both: stand-ins on the device for what you say, blind credentials and a sealed relay for
who you are. `LETHE.md` §4 records what the evidence killed and why.
