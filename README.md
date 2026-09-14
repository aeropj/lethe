# Lethe

A privacy harness for the agentic era: reversible identity tokenisation between people, their agent swarms, and every frontier model. The model drinks from Lethe and forgets who you are, because it never knew. You keep Mnemosyne.

## Layout

- `paper/lethe.tex` — concept paper (4 pages: 3-page body + references/appendix). Build with `pdflatex lethe.tex` twice, or `latexmk -pdf lethe.tex`.
- `paper/slides.tex` — 12-slide ideation deck reusing the same figures.
- `paper/figs/` — TikZ figures (isometric hero, detection pipeline, worked example, agent-swarm gateway).
- `paper/lethe-iso.tex` — isometric TikZ macro library and palette.
- `research/` — background research: competitive landscape, naming and mythology, LLM first principles, technical architecture.

## Build

```bash
cd paper && latexmk -pdf lethe.tex && latexmk -pdf slides.tex
```

Requires TeX Live 2025 (Inter and IBM Plex Mono type1 packages, TikZ, tcolorbox).
