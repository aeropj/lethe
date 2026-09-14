# Lethe

A privacy harness for the agentic era. Identity-bearing data is replaced with realistic surrogates before anything leaves your device or VPC; the keys never leave; the answer is re-identified locally. The model gets a convincing double.

*Lethe: the river in Hades whose water erases memory. Mnemosyne: the pool that restores it.* The model drinks from Lethe. You keep Mnemosyne.

## Layout

- `paper/lethe.tex` — concept paper, 6 pages. Pranjal Joshi and Prashil Bulbule.
- `paper/slides.tex` — 15-slide concept deck that mirrors the paper section by section.
- `paper/figs/` — TikZ figures. `hero` (the two shores), `fanout` (the problem), `cardanalogy` (the insight), `story-personal` and `story-enterprise` (worked examples), `stacks` (where it sits), `pipeline` (detection layers), `swarm` (the agent gateway), `mini` (title mark).
- `paper/lethe-iso.tex` — isometric TikZ macro library, palette, card and fit helpers.
- `research/` — background: competitive landscape, naming and mythology, LLM first principles, technical architecture.

## Build

```bash
cd paper && latexmk -pdf lethe.tex && latexmk -pdf slides.tex
```

Requires TeX Live 2025 with Inter and IBM Plex Mono, TikZ, tcolorbox, adjustbox. Figures are vector TikZ so both documents scale to any size and stay diffable in git.
