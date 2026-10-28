# Lethe

**The privacy layer for AI.** Use GPT, Claude and Gemini at full capability without handing over who you
are. It starts with your own questions; the same layer is meant to sit under every app, service and agent
that calls a model.

Pranjal Joshi · Prashil Bulbule · Vaibhav

![Lethe demo film](demo/video/out/poster.png)

## Try it

Needs Python 3.10+ (macOS or Linux; on Windows use WSL) and an OpenAI API key.

```bash
git clone https://github.com/aeropj/lethe && cd lethe && ./demo/run.sh
```

Open http://localhost:8787 and paste your key. It stays in this process's memory and goes only to
api.openai.com. The first start installs dependencies and downloads the on-device model (~1.2 GB) and a city
list once; after that, detection runs offline.

Type a question the way you normally would. As you type, **Will be sent as** shows exactly what would leave
your machine: names, places, organisations, contacts, IDs, exact ages and occupations are found by a
multilingual model running locally, and swapped or generalised. Click any word to hide it, or any highlight
to keep it. If nothing personal is found, Lethe says so before anything is sent. The **Observability** tab
traces every request in nine timed steps with the real bytes, and **Prove it** asks OpenAI for its own stored
copy to check none of your details are in it ([demo/VERIFY.md](demo/VERIFY.md)).

**How well detection works**, on prompts in 13 languages and styles (lowercase, voice-typed, Hinglish,
Chinese, Arabic…), reproducible with `python demo/eval/run_eval.py`:

| | 45 tuning prompts | 30 fresh prompts |
|---|---|---|
| Identifiers removed | 98.3% | 100% |
| Prompts with nothing identifying left | 95.6% | 100% |
| Exact ages and occupations generalised | 100% | 100% |
| Useful terms kept | 98.8% | 96.2% |
| Median detection time on a laptop CPU | 85 ms | 87 ms |

The fresh prompts were written after tuning; one later fix (lowercase generic phrases such as "family court"
being hidden) came from a miss in that set.

Known limits: names that are ordinary words ("hope and will are getting married"), venue names like hotels,
and some over-hiding of generic phrases ("family court"). The live preview is there for exactly these. In this
local demo all parties run in one process with your key, so OpenAI still sees your account and IP; hiding
those needs the relay and gateway run by separate operators. Details: [demo/README.md](demo/README.md).

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
