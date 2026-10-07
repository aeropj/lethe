# Lethe

**Anonymous access to frontier AI models.**

Pranjal Joshi · Prashil Bulbule

You use GPT, Claude and Gemini at full capability. No provider knows who you are, because your credential
is a blind signature rather than an account. No provider can link your payment to your usage. No edge
network can join your traffic across providers. What you write still reaches the model, and we measure
what that text carries before it leaves rather than pretending we removed it.

## Start here

**[LETHE.md](LETHE.md)** — the complete document. Thesis, evidence, plan, risks, what to file, next steps.

## Layout

- `research/landscape/landscape.pdf` — **competitive landscape and verdict, October 2026.** Read before pitching anything. Long form: `reports/Private AI access competitive landscape.md`.

- `proposal/index.html` — **the proposal as a launch page.** Open it in any browser; it loads nothing from the network.

- `LETHE.md` — the single source of truth.
- `research/` — ten research files behind it: source study of the nearest open-source implementation,
  the academic frontier, the startup and YC sweeps, the profiling-channel enumeration, and the patent
  freedom-to-operate study.
- `paper/lethe.tex` — **the full proposal**, five pages: the private pool for frontier AI. Answers the five
  questions inline: what we are making, why us, competitors, technical stack, and revenue.
  Build with `cd paper && latexmk -pdf lethe.tex`.
- `paper/slides.tex` — **stale.** Still describes the superseded tokenisation plan. Do not send it.
- `STRATEGY.md`, `yc-application.md` — earlier drafts, superseded by `LETHE.md`.

## What changed, and when

The project began as a reversible identity-tokenisation harness. Research in September 2026 showed that
the mechanism was already published and patented, that per-provider surrogate rotation does not defeat
linkage, and that four of the ten channels through which a profile gets built close with cryptography at
no cost to answer quality. The company moved from hiding what is in a prompt to hiding who is asking.
`LETHE.md` §4 records what the evidence killed and why.
