# Lethe — YC application answers

Draft. Founder-specific facts are marked **[FILL]** — do not submit with those in place.
Written after studying https://github.com/jfreemansh/Anonproxy, which implements much of the v1 plan
already; see `research/05-anonproxy.md`. These answers assume that and do not pretend otherwise.

---

## What tech stack are you using, or planning to use, to build this product? Include AI models and AI coding tools you use.

Python 3.12 for the engine and detector orchestration, because every PII model ships Python-first and
detection semantics are still moving. Rust for the hot path once those semantics settle: the regex and
Aho-Corasick floor, the streaming detokeniser, and the vault, compiled to one binary and to WASM for the
browser extension. FastAPI and uvicorn for the local proxy, which speaks the OpenAI and Anthropic wire
formats including server-sent events, plus MCP over stdio and HTTP.

Detection is a layered local chain and nothing in it calls a cloud model. A deterministic floor of regex
and checksums (Luhn, mod-97, SSN structure, E.164). Then an on-device encoder tier: GLiNER2-PII at 0.3B
and OpenAI's Apache-2.0 Privacy Filter, 1.5B total with 50M active, both through ONNX Runtime with CoreML
on Apple silicon. Then a small local model for contextual PII that encoders miss, Qwen3 at 0.6B or 1.7B,
served by MLX on macOS and llama.cpp elsewhere, LoRA fine-tuned on our own traffic distribution because
the published benchmarks collapse out of distribution. Then the user's own dictionary, which is the
cheapest and highest-recall layer we have.

The vault is SQLite with SQLCipher. The data key is wrapped by a non-exportable key in the Apple Secure
Enclave, TPM 2.0 on Windows and Linux, and KMS or CloudHSM in the enterprise gateway. Surrogates are
derived by HMAC-SHA256 over a scope key produced with HKDF, where the scope includes tenant, user,
session and **provider** — that last term is what makes two providers unable to join profiles.

The ledger is hash-chained, signed with Ed25519, and checkpointed to a Sigstore Rekor transparency log so
a third party can verify it. The enterprise control plane is Go, deployed by Helm, with OIDC and a SIEM
feed over OTLP. A later confidential tier runs in Intel TDX or AMD SEV-SNP with NVIDIA H100 confidential
computing, attested through Intel Trust Authority.

For evaluation we run a paired harness: the same task with and without the harness, across GPT, Claude
and Gemini, scored by a judge blinded to condition, with exact match where the answer is structured. We
use DSPy to optimise the detection chain rather than hand-tuning prompts.

AI coding tools: Claude Code is the primary agent and writes most of the first draft of everything, with
Codex CLI used as an adversarial second reader on security-sensitive diffs, and Cursor for edit-heavy
refactors. Models are Claude Opus and Fable for architecture and review, Haiku for bulk mechanical work.
We dogfood: our own agents reach those models **through Lethe**, so our repository, our customer notes and
our own identities are tokenised by the thing we are shipping. That has been our best bug-finder, because
every restoration failure shows up as a broken code review rather than as a silent test.

---

## What is your company going to make?

Lethe is a privacy layer that sits between a person, or their agents, and every AI model they use.

It replaces identity-bearing data — names, government IDs, account numbers, addresses, employers, health
details — with realistic fake data *before* anything leaves the device or the company network, and puts the
real values back into the answer on the way in. The substitution is deliberately not a placeholder like
`[PERSON_1]`; it is a plausible person with a matching gender, culture and name length, a structurally
valid identifier, a date shifted by a constant so every interval survives. The model reasons over a
coherent double and answers correctly. Amounts, ages and dates are never touched, because the answer
depends on them.

It ships two ways. On a laptop it is a background daemon you point a tool at with one environment
variable, and it covers coding agents, desktop chat, the browser and the share sheet. In a company it is a
gateway in the VPC that every agent, tool call and model request routes through, where each agent carries
a signed manifest of what it is allowed to see, and real values re-enter only at the instant a tool
actually acts.

Three properties make it a product rather than a script. The mapping is one consistent bijection applied
to the prompt, the history, retrieved documents, tool arguments, tool results and the model's own output,
because applying it inconsistently is what destroys answer quality. The surrogate a given person gets is
derived per provider, so OpenAI and Anthropic hold two unrelated strangers and cannot join them into one
profile. And every crossing is written to a signed, hash-chained log checkpointed to a public transparency
log, so "the provider never received this" is a receipt you can hand an auditor rather than a promise we
make.

---

## Why did you pick this idea to work on? Do you have domain expertise in this area? How do you know people need what you're making?

**[FILL — the honest origin story. The strongest version is a specific moment where one of you had real
data, a model that would have answered well, and no safe way to combine them. Name the company, the data,
the workaround you built. If either of you has shipped security, privacy, infrastructure or ML-inference
work, name the system and the scale. Do not generalise; YC reads hundreds of these and specificity is the
only signal.]**

What we can show without relying on our own story:

People already do this by hand, badly, at scale. A third of employees use personal accounts for AI work.
The share of enterprise AI traffic carrying sensitive data went from 10.7% to 39.7% in two years. The
standard corporate response has been a ban followed by a contract, which is a legal control over a
technical problem.

The sharpest evidence is that practitioners keep building this for themselves. `DontFeedTheAI` has 655
stars. Anonproxy is a cleaner reimplementation of it, 4,700 lines with 120 tests and eight PyPI releases,
written by one person at a pentest firm who needed to send client data to Claude and would not. There are
half a dozen more proxies and browser extensions doing a weaker version. Nobody builds this much
infrastructure for a problem they do not have, and nobody would build it at all if something were
purchasable.

And the trigger that makes it urgent now is agents rather than chat. One prompt is one hop you approved.
A swarm is forty hops across tools nobody audited, and AWS documents that its own guardrails do not
inspect tool-call arguments or results at all. The exposure grew by an order of magnitude and the controls
did not move.

How we would know we are wrong: if we cannot get fifty developers to leave the daemon running for a month,
the pull is not there, and no amount of enterprise narrative will rescue it.

---

## Who are your competitors? What do you understand about your business that they don't?

**Org-side reversible tokenisation** — Protecto, WitnessAI, Skyflow, Kong's AI Sanitizer with its restore
flag. Closest to us in mechanism. In all of them the vendor holds the keys, and none has an agent or MCP path.

**Consumer and open source** — Wald.ai, plus a set of local proxies. `DontFeedTheAI` has 655 stars;
Anonproxy is a cleaner reimplementation of it with 7. Anonproxy already has the local proxy,
format-preserving surrogates for structured identifiers, a layered all-local detector chain, a user
dictionary, and a tolerant streaming restorer it benchmarked from 78% to 100% including JSON tool-call
arguments. We read every line of it. We treat that transport layer as table stakes we will match or reuse
in two weeks, not as a moat, and we have dropped "realistic surrogates" and "no cloud model in the hot
path" from our differentiator list because they are already shipped under an MIT licence.

**Guardrails and AI gateways** — Bedrock Guardrails, Prisma AIRS (formerly Portkey), Cloudflare, Lakera.
One-way redaction bolted to one vendor's control plane.

**Confidential compute** — Tinfoil, Confer, Privatemode, Apple's Private Cloud Compute. A different and
in some ways stronger promise, but limited to open-weight models, and explicitly positioned against
redaction.

**Detection itself is no longer a competitor, it is a commodity.** A frontier lab open-sourced a capable
local PII model in April 2026. Anyone can assemble the detector in a weekend, so nobody should build a
company on it, including us.

### What we understand that they don't

**Consistency is the product; detection is the commodity.** Everyone benchmarks detection F1. The failure
that actually loses a user is a broken round trip or a broken coreference chain. The only catastrophic
utility result in the literature — retrieval quality falling from 0.80 to 0.32 — happened because the
query and the documents were anonymised independently. That is a consistency bug, not a cost of
anonymisation, and it means the primary engineering object is one bijection applied identically across
prompt, history, retrieved chunks, tool arguments, tool results and model output. Nobody treats it as the
primary object.

**Consistent surrogates are themselves a profiling vector, and everyone shipping this has the default
wrong.** If a person is always the same fake person, the provider accumulates a complete dossier on that
fake person, and the day one real detail leaks the entire history de-anonymises backwards. Anonproxy's
threat model concedes exactly this and offers a manual workaround. We put the provider and the session in
the key derivation, so the same human is two unrelated strangers to two labs. The cryptography is trivial;
what is hard, and what we think is the actual product work, is making rotation *useful* when memory
features and multi-session continuity are pulling the other way.

**The value moved to the tool boundary the moment agents arrived.** Everyone is protecting the prompt. In a
swarm the prompt is a minority of the traffic, and the only place a real value is genuinely required is
the instant a tool acts on it. Design around that and injection resistance falls out for free: an agent
that never held the SSN cannot be argued into exfiltrating it. Anonproxy's MCP wrapper deliberately passes
host-to-server traffic untouched. Bedrock does not inspect tool arguments at all. This is the gap.

**The buyer wants a provable negative, and nobody sells one.** "We didn't send your data" is unfalsifiable
and every vendor says it. An exact-match egress gate over the final bytes, plus a signed hash-chained log
checkpointed publicly, turns it into a receipt. Paired with the CJEU's September 2025 holding that
identifiability is judged from the recipient's perspective, customer-held keys become a legal argument
nobody is making in market.

**The platforms cannot ship the part that matters, and that is structural rather than a head start.**
A frontier lab can add provider-side redaction next quarter, and probably will. It cannot ship
cross-provider unlinkability, because that is a promise about what a *competitor* must not be able to
correlate. It cannot ship a log proving what it did not receive, because a claim by the observed party
about the observer is not evidence. Both of our core guarantees are assertions against the provider, so
they can only be issued by something the provider does not control. That is the whole company.

**And we understand that our own v1 is not defensible.** The local proxy is a table stake that already
exists for free. We are not planning to win there. We plan to win on the three things Anonproxy's author
explicitly put out of scope, in writing: unlinkability across providers, structural need-to-know for
swarms, and a verifiable negative.

---

## How do or will you make money? How much could you make?

**Free, open-source local daemon.** Deliberate, and not only for distribution. The claim is "keys never
leave your device," and that claim is worthless if the code is closed. It is also the only sane response
to a good MIT-licensed competitor.

**Teams — $30 per seat per month.** A hosted control plane for a 10 to 50 seat AI-forward team: shared
dictionaries, policy sync, the ledger service, SSO. Self-serve, lands without a sales call.

**Enterprise gateway — $75k to $150k per year.** Priced against the workload it unblocks, not per seat.
HSM key custody, per-agent manifests, SIEM integration, the compliance evidence pack, and someone who sits
in the audit. The buyer is the security or platform owner, and the budget line already exists under AI
governance.

**The Mnemosyne Mark — annual certification fee.** Revocable, with a public verifier, for products built
on Lethe. Slow to start and the smallest line for years. It is also the only one that turns us into a
standard rather than a vendor, which is why it exists from the beginning.

### How much

Honestly, two different answers depending on which company this becomes.

Priced as an AI gateway, the ceiling is low. Gartner puts that segment at $251M in 2026 and $429M in 2027,
inside a securing-AI market of roughly $4.8B, and it is consolidating into platforms. A good outcome on
that path is 300 enterprise accounts at $120k plus 100k paid seats, about $70M of ARR in five years. That
is a real company and not a venture-scale one.

The bet is the other path: that identity tokenisation becomes infrastructure every AI product embeds
rather than a control a security team buys, and that the Mark ends up on other companies' pricing pages
the way a payment badge does. That is a per-call business with the shape of Stripe or Twilio, and it is
worth an order of magnitude more. We do not have evidence for it yet, and we would rather say so than
model it.

What we would need to see in the first year to believe the second path: agent builders adopting the
gateway without being sold to, and at least one buyer asking for the Mark before we offer it.
