# TypeSafe AI — what it is, and what it means for Lethe

Checked 2026-10-01.

## What it is

Not a privacy company. A new model lab. Its first model, **Jev**, is what TypeSafe calls a *System One
Model*: you send unstructured text plus a typed schema, and it returns typed answers (Choice, Score or
Null) each with a confidence value. It never generates text.

| | |
|---|---|
| Founders | Diogo Almeida (ex-OpenAI, co-inventor of RLHF), Erik Gafni, Sasha Sheng |
| Funding | $40M seed led by DCVC |
| Launch | 15 September 2026, after ~2 years in stealth |
| Context | 32,000 tokens |
| Latency | 70–500 ms; one independent measurement put the median at 76 ms, upper quartile 270 ms |
| Price | $0.042 per million input tokens; output free |
| Limits | 255 options per choice; weak at counting, arithmetic and date comparison |
| Use cases they name | classify, route, score, extract, verify; guardrails that "run on every call" |
| Launch customers | Vercel (safety classifier, 5–18x faster than an OpenAI model, higher accuracy); Bryo AI (email triage, 10–20x cheaper than Gemini, slightly less accurate) |
| Deployment | **Hosted API only.** No self-hosted, on-prem or on-device option found |
| Data | No training on customer data. Zero data retention only for enterprise, via sales |

## Criticism worth knowing

- Calibration is a property of a model *on a distribution*, not of a model. One tester got 0.92 confidence
  on heads for a fair coin; another found calibration tracks the ideal line poorly across large ranges.
- Their own docs warn it "can still emit a completely wrong valid value."
- The core primitive — reading logit probabilities over a fixed choice set — reproduces locally in about
  25 lines with a 0.6B Qwen model under llama.cpp. The fair concession is that Jev is a zero-shot
  classifier on day one, with managed serving.

## What it means for us

1. **Not a competitor, but one product decision away from one.** Guardrails on every call is a named use
   case. A PII classifier on Jev would be a cheap, fast cloud API — the exact positioning we already
   abandoned.
2. **It is what "our engine is small trained models" will be compared to.** A partner who read the
   TechCrunch piece will ask why we do not just call Jev. The answer is the product: deciding what is
   private by sending it to a fourth company defeats the purpose. Same class of model, run on the
   laptop. The local 0.6B Qwen approach in the critique is our L2 detector design.
3. **Its launch is the pitch template.** A contrarian headline ("we took the opposite research
   direction"), two multipliers against the incumbent, named customers on day one, and no parameter count.
4. **Calibration is our problem too.** The bypass budget in our design depends on per-span confidence.
   Anonproxy computed confidence and never used it. Measure calibration on our own traffic or do not
   rely on it.

## Sources

- TechCrunch, 18 Sep 2026: https://techcrunch.com/2026/09/18/a-new-kind-of-ai-model-from-a-chatgpt-inventor-is-thrilling-developers/
- InfoQ, Oct 2026: https://www.infoq.com/news/2026/10/typesafe-ai-jev-released/
- TrueFoundry: https://www.truefoundry.com/blog/typesafe-ai-jev
- Critique, DEV Community: https://dev.to/jamilxt/typesafes-jev-costs-400x-less-than-an-llm-these-25-lines-of-python-do-the-same-job-for-free-3ddd
- Funding: https://finance.yahoo.com/technology/ai/articles/typesafe-ai-emerges-stealth-40m-190000776.html
- Legal: https://docs.typesafe.ai/legal
