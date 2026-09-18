# Anonproxy — does it already solve this?

Repo: https://github.com/jfreemansh/Anonproxy · MIT · created 2026-06-25 · last push 2026-09-05
Solo author (John Freeman, `jfreemansh`, MSc student, affiliated with Nethemba, a Slovak pentest firm)
57 commits · 7 stars · 2 forks · 0 watchers · 8 releases · PyPI 0.2.1 · ~980 downloads
~4,750 LOC Python · 120 test functions (159 cases, all passing) · CI on every push

**Correction to an earlier reading: this was not three months of work.** 51 of the 57 commits landed in a
single ~18-hour window on 2026-08-24. The final commit deletes an accidentally-committed 3,125-line AI
agent session transcript. It was one AI-assisted sprint. That explains both the uniform polish and the
shallowness — see the defects below.

**Context that matters more than Anonproxy itself:** its README says it is a reimplementation of
`zeroc00I/DontFeedTheAI`, which has **655 stars and 78 forks**. Anonproxy is the less-adopted entrant in
a category that already has a leader. Citing its 7 stars as evidence of an empty market would be a
mistake; the adjacent tool's 655 is the number that matters.

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
| Format-preserving surrogates, **partially** | hashes → same-length hex; AWS keys keep `AKIA`; IPs → valid RFC 5737 TEST-NET; cards → 16 Luhn-valid digits, same grouping. **But** SSN is typed `IDENTIFIER` and becomes an alphanumeric blob (`123-45-6789` → `jaNt0J6APX7`); no date handling at all; no amount handling; the name pool is 16×16 Anglo/unisex, so `Aisha Okonkwo` → `Morgan Nolan` and `Wei Zhang` → `Casey Nolan` |
| Layered local detection, no cloud LLM in the hot path | regex floor (always on) + Ollama (local) + GLiNER + GLiNER2-PII + Piiranha + OpenAI Privacy Filter + a purpose-built Qwen3 SLM. Chain set by `ANONPROXY_DETECTORS`, lazily loaded, degrades gracefully |
| User dictionary | `detectors/scope_detector.py` — engagement scope list, deterministic, part of the floor |
| **Tolerant streaming restoration, benchmarked** | `restorer.py` + `proxy/streaming.py`; normalised projection with index map back to original; per-content-block hold-back buffer for surrogates split across SSE deltas. Published benchmark: naive `str.replace` 78%, their restorer 100% on 77 mangling cases |
| Tool-call JSON handling | `test_tool_calls.py`, `test_streaming_tooljson.py`; restores inside streamed tool-call arguments |
| MCP support (partial) | `mcp_wrapper.py` — stdio shim; anonymises **server → host** (tool results) |
| Adversarial self-test | `python -m anonproxy verify`: leak, round-trip, adversarial-echo, tool-call-payload, benign-pattern probes; runs in CI |
| Local vault viewer | `audit.py`, token-gated, loopback — a live table of vault state, **not an event log** |
| Surfaces | Burp extension, macOS menu-bar app (`anonbar.swift`), webapp, CLI, Docker, PyPI |
| Honest threat model | `THREAT-MODEL.md` states plainly: "this is risk reduction, not a guarantee" |

Two things there we had underrated. **Restoration fidelity is the hard engineering problem**, not
detection — they measured it and fixed it, and the failure modes they enumerate (case folding,
markdown emphasis inside the token, unicode hyphens, splits across streaming chunks) are real and
non-obvious. And their detector chain is **richer than the one we specced**.

## Defects found by reading and running the code

These were not visible from the README and they change the assessment.

1. **Raw passthrough on OpenAI's current primary API.** Only `/v1/messages`, `/v1/chat/completions`,
   `/v1/completions`, `/v1beta/*` and `count_tokens` are redacted. Everything else under `/v1/*` is
   forwarded unmodified (`proxy/app.py:334-357`). Driving the app against a mock upstream with a body
   containing a real SSN: `/v1/responses`, `/v1/embeddings`, `/v1/files` and `/v1/audio/transcriptions`
   all leak it verbatim. `/v1/responses` is what a current OpenAI SDK or the Agents SDK uses by default.
   `ANONPROXY_STRICT=true` turns these into 404s, but `strict_mode` defaults to **False**
   (`config.py:153`), commented "Off by default so odd/legacy clients keep working."
2. **The MCP entry point does not run.** `cli.py:116` declares a positional `cmd` with
   `nargs=REMAINDER` inside the `mcp` subparser, which overwrites the subparser dest, so the guard at
   `cli.py:244` never fires. `anonproxy mcp -- <server>` exits 0 having spawned nothing. Undetected
   because the tests call `mcp_wrapper.wrap()` directly and never touch the CLI.
3. **Fail-open by default, and confidence is decorative.** Every detector records a confidence; nothing
   anywhere branches on it. No bypass budget, no ask-the-user path. Detector crashes are caught and
   execution continues, so a regex-floor failure means that request went out with zero deterministic
   coverage.
4. **Partial-name references do not restore.** Possessives, case changes, markdown and line splits all
   work. `Mr. Brooks`, `M. Brooks` and bare last names do not — the user reads the fake name.

## What it genuinely does not have

1. **Per-provider unlinkability.** Surrogates are keyed on engagement id only. `THREAT-MODEL.md`
   lists "query-pattern correlation — consistent surrogates are linkable across turns by design"
   as an explicit residual risk, mitigated manually by "rotate engagement id per session."
   The same person is the same surrogate to every provider, so profiles can still be built and joined.
2. **Agent-swarm mediation.** The MCP wrapper is a stdio shim for one server and, by its own
   docstring, passes host → server traffic **untouched** ("tool-call arguments originate locally").
   No per-agent capability manifests, no need-to-know scoping, no taint tracking, no contextual-integrity
   check, no gating of detokenisation at an action boundary. `grep -rn "manifest\|capability\|taint"` returns nothing.
3. **Any event log at all.** This is worse than "not tamper-evident." `audit.py` renders a live view of
   the current vault mapping. There is no record anywhere of what crossed the boundary, when, to which
   provider, under what policy. Repo-wide grep for `merkle|rekor|sigstore|hash_chain|prev_hash|tamper|
   ed25519|ecdsa` returns zero hits. The close-out "evidence trail" is an unsigned JSON and CSV dump the
   operator can edit.
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

Blunt: items 1 and 4 are each a day to two weeks for this author. Item 1 is roughly ten lines — adding a
provider string to the HMAC input. Item 5 is a research project. Item 6 is a benchmark, which is a
distribution asset rather than a moat.

Two things are genuinely hard. **Item 2**, the agent gateway with manifests and taint tracking, is months
of work and a policy model no shipping product has. **Item 3**, a signed externally-verifiable ledger, is
the only claim with zero counterpart anywhere in this category, and it is hard for him specifically
because his user *is* the operator and trusts himself. That assumption does not hold for a regulated
buyer, which is exactly why it is worth building.

## The structural argument, which is the important one

Cross-provider unlinkability and a log that proves what a provider did *not* receive both require the
verifier to distrust the provider. A frontier lab can ship provider-side redaction tomorrow; it
structurally cannot ship either of those, because both are assertions against itself. That asymmetry is
the only durable answer to "why won't OpenAI or Anthropic just add this," and it happens to be precisely
the property Anonproxy discards by sharing one vault across all providers.

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
