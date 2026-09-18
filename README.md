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

- `LETHE.md` — the single source of truth.
- `research/` — ten research files behind it: source study of the nearest open-source implementation,
  the academic frontier, the startup and YC sweeps, the profiling-channel enumeration, and the patent
  freedom-to-operate study.
- `paper/` — an earlier concept paper and deck describing a superseded plan. Kept for the figures and
  for the record. Build with `cd paper && latexmk -pdf lethe.tex && latexmk -pdf slides.tex`.
- `STRATEGY.md`, `yc-application.md` — earlier drafts, superseded by `LETHE.md`.

## What changed, and when

The project began as a reversible identity-tokenisation harness. Research in September 2026 showed that
the mechanism was already published and patented, that per-provider surrogate rotation does not defeat
linkage, and that four of the ten channels through which a profile gets built close with cryptography at
no cost to answer quality. The company moved from hiding what is in a prompt to hiding who is asking.
`LETHE.md` §4 records what the evidence killed and why.
