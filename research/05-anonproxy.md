# Anonproxy — does it already solve this?

Repo: https://github.com/jfreemansh/Anonproxy · MIT · created 2026-06-25 · last push 2026-09-05
Solo author (John Freeman, `jfreemansh`) · 57 commits · 7 stars · 2 forks · 8 releases · on PyPI at 0.2.1
~4,750 LOC Python · 120 test functions · CI on every push

## Short answer

**Yes. It is the same idea, executed, shipped, and in places better specified than our v1 was.**
It is scoped to one vertical (pentesters sending client data to LLMs), but the machinery is general.

Anything in the Lethe v1 plan that is not on the "genuinely missing" list below should be treated as
already-solved prior art, not as differentiation.

## What it already has

| Capability | Evidence |
|---|---|
| Local proxy speaking OpenAI **and** Anthropic wire formats, incl. SSE | `anonproxy/proxy/app.py`, `streaming.py`; `python -m anonproxy serve` |
| Reversible tokenisation with a per-engagement vault | `vault.py` (SQLite, isolated per engagement) |
| Deterministic surrogates, HMAC-keyed | `surrogates.py`; keyed on engagement id; survives restart and vault loss |
| **Format-preserving, realistic surrogates** | hashes → hex of same length; AWS keys keep `AKIA`; IPs → valid RFC 5737 TEST-NET; cards → 16 Luhn-valid digits with same grouping; small name pools so PERSON/ORG "read like real names" (`surrogates.py:33`) |
| Layered local detection, no cloud LLM in the hot path | regex floor (always on) + Ollama (local) + GLiNER + GLiNER2-PII + Piiranha + OpenAI Privacy Filter + a purpose-built Qwen3 SLM. Chain set by `ANONPROXY_DETECTORS`, lazily loaded, degrades gracefully |
| User dictionary | `detectors/scope_detector.py` — engagement scope list, deterministic, part of the floor |
| **Tolerant streaming restoration, benchmarked** | `restorer.py` + `proxy/streaming.py`; normalised projection with index map back to original; per-content-block hold-back buffer for surrogates split across SSE deltas. Published benchmark: naive `str.replace` 78%, their restorer 100% on 77 mangling cases |
| Tool-call JSON handling | `test_tool_calls.py`, `test_streaming_tooljson.py`; restores inside streamed tool-call arguments |
| MCP support (partial) | `mcp_wrapper.py` — stdio shim; anonymises **server → host** (tool results) |
| Adversarial self-test | `python -m anonproxy verify`: leak, round-trip, adversarial-echo, tool-call-payload, benign-pattern probes; runs in CI |
| Local audit dashboard | `audit.py`, token-gated, loopback |
| Surfaces | Burp extension, macOS menu-bar app (`anonbar.swift`), webapp, CLI, Docker, PyPI |
| Honest threat model | `THREAT-MODEL.md` states plainly: "this is risk reduction, not a guarantee" |

Two things there we had underrated. **Restoration fidelity is the hard engineering problem**, not
detection — they measured it and fixed it, and the failure modes they enumerate (case folding,
markdown emphasis inside the token, unicode hyphens, splits across streaming chunks) are real and
non-obvious. And their detector chain is **richer than the one we specced**.

## What it genuinely does not have

1. **Per-provider unlinkability.** Surrogates are keyed on engagement id only. `THREAT-MODEL.md`
   lists "query-pattern correlation — consistent surrogates are linkable across turns by design"
   as an explicit residual risk, mitigated manually by "rotate engagement id per session."
   The same person is the same surrogate to every provider, so profiles can still be built and joined.
2. **Agent-swarm mediation.** The MCP wrapper is a stdio shim for one server and, by its own
   docstring, passes host → server traffic **untouched** ("tool-call arguments originate locally").
   No per-agent capability manifests, no need-to-know scoping, no taint tracking, no contextual-integrity
   check, no gating of detokenisation at an action boundary. `grep -rn "manifest\|capability\|taint"` returns nothing.
3. **Tamper-evident ledger.** The audit surface is a local dashboard. No hash chain, no signatures,
   no external checkpoint, nothing a third party can verify.
4. **Hardware key custody.** Vault protection is an opt-in AES-GCM envelope from
   `ANONPROXY_VAULT_PASSPHRASE`, or ephemeral mode. No Secure Enclave, TPM or HSM.
5. **Quasi-identifier risk scoring.** None. `README.md:601` marks generalisation
   "not applicable to pentest infra data."
6. **Answer-quality measurement.** Their benchmark measures *restoration fidelity* — did the
   surrogate come back. It does not measure whether the model's answer got worse. Nobody has
   published that.
7. **ICP beyond pentesting.** Everything is framed around engagements, scope lists, and client
   infrastructure.

## How defensible is that list

Blunt: items 1, 3 and 4 are each somewhere between a day and two weeks of work for this author.
Item 5 is a research project with unclear payoff. Item 6 is a benchmark, which is a distribution
asset rather than a moat. **Only item 2 is a different product shape**, and it is months of work
plus a policy model that does not exist yet in any shipping product.

## What this means for the plan

The wedge as written — "a local daemon any coding agent adopts with one environment variable" —
is exactly what Anonproxy already ships, MIT-licensed, on PyPI. That wedge is gone as a
differentiator. It remains a necessary table stake.

The defensible ground is precisely what the repo's own threat model declares out of scope:
unlinkability across providers, structural need-to-know for agent swarms, and a verifiable
negative. Those are also the three things that only matter once agents, not chat, are the
dominant traffic — which is the actual bet.

Second conclusion: we should contribute to or fork Anonproxy rather than reimplement its
restorer. Re-deriving 100% round-trip tolerance from scratch is pure waste.
