# Lethe — strategy, remapped

2026-09-18. Supersedes everything in `paper/` and `yc-application.md`.
Evidence: `research/05` through `research/10`.

---

## What the evidence killed

**1. Reversible PII tokenisation is not a company.** Published as SurrogateShield (arXiv:2606.29567,
June 2026) with the same architecture we specified, including the quasi-identifier scoring we claimed as
a gap. Shipped by Skyflow, Protecto, WitnessAI, Kong, Tonic, and fifteen open-source projects. OpenAI
gave away the detector in April under Apache-2.0.

**2. Per-provider surrogate rotation does not produce unlinkability.** Lermen, Paleka, Swanson, Aerni,
Carlini and Tramèr, USENIX Security 2026 (arXiv:2602.16800): up to 68% recall at 90% precision linking
the same person's pseudonymous profiles, against near zero for the best non-LLM method, including across
a deliberately removed one-year gap, at a few dollars a head. The surrogate was never the linkage
channel. Topic, expertise and recurring specifics are.

**3. The mechanism is patented, and by a licensing company.** Anonos US12417317, granted 2025-09-16,
claims per-element substitution in input to an AI model plus the recovery mapping, with dependent claims
on generative AI and on re-identifying the model's response. US12614034B2, granted 2026-04-28, adds NLP
span detection, reversible semantic tokens into an LLM, and selective reversal at authorised endpoints.
Anonos has live continuations publishing in 2026, so they can still draft claims at whatever we ship.

**4. The consumer thesis has a graveyard.** Brave converts 101M privacy-selected users into ~100k VPN
subscribers, a tenth of one percent. Mozilla earns $66.4M from subscriptions and advertising combined
across ~200M users, growing 2.5% a year. Crosshatch, the closest funded attempt at per-agent data
scopes, shut down in July 2025. Blyss died on the encrypted-inference thesis with a Stanford and Apple
team. Piiano abandoned its vault after four years and became an agent governance plane.

**5. The Datavant analogue is backwards.** Datavant holds the master salt, and holding it *is* the
business. Our local key custody deliberately destroys the only asset they monetise. The linkable version
of that business, LiveRamp, sold at 2.7x revenue.

**6. Enterprise ACV is a third of what we assumed.** Median for comparable AI data-protection products
is ~$25k, not $150k. The closest structural exit comp, Palo Alto buying Portkey, was $117M disclosed.

---

## What the evidence found instead

Ten channels build a profile. Our old design closed one of them, partially.

| # | Channel | Defence | Utility cost | Status |
|---|---|---|---|---|
| 4 | Account and authentication | Blind-signature tokens, RFC 9474 / 9576-9578 | **zero** | shipped by Apple, Meta, Kagi, Brave |
| 5 | Payment | Flat-rate vouchers via a merchant of record | **zero** | shipped by Mullvad |
| 6 | Network metadata | Oblivious HTTP, RFC 9458, plus response padding | **zero** | shipped by Apple, Meta, Google, Mozilla |
| 9 | Cross-service join | Per-provider egress diversity, distinct relays | **zero** | nobody |
| 7 | Device fingerprint | One pinned TLS stack, uniform client | zero | browsers |
| 10 | Provider memory | Do not use it; keep memory locally | high | us |
| 1 | Content PII | Reversible tokenisation | low | commodity |
| 2 | Quasi-identifiers | Local adversarial rewriting | **high** | nobody in production |
| 3 | Writing style | Style-aware paraphrase | **high** | nobody |
| 8 | Timing | Queue, jitter, batch | zero, but latency | research |

**Four channels close with cryptography at zero cost to answer quality.** Apple and Meta have both
shipped the entire stack — anonymous credentials, oblivious transport, attested compute — in production,
at hundreds of millions of users, for their own models. **Nobody offers it as access to frontier
models.** That is the gap.

And one measured fact makes channel 9 urgent. On 2026-09-18, `api.openai.com`, `api.anthropic.com`,
`api.mistral.ai`, `api.x.ai`, `api.together.xyz`, `api.groq.com` and `openrouter.ai` all return
`server: cloudflare`. **One commercial party terminates TLS for at least seven major providers.** The
cross-service join requires no data broker and no subpoena, only a query against one edge network's logs.

---

## The remapped company

Lethe sells **anonymous access to frontier models**, not prompt redaction.

> You use GPT, Claude and Gemini at full capability. No provider knows who you are, because your
> credential is a blind signature. No provider can link your payment to your usage. No edge network can
> join your traffic across providers, because each one leaves by a different oblivious path. What you
> write still reaches the model, and we measure what that carries before it leaves.

The last sentence is the honest part and it must stay. The model has to read the prompt. Anything that
claims otherwise is selling a feeling.

**Why this is defensible where the old plan was not.**

- Zero utility cost on the four channels we lead with. The entire privacy-versus-capability tradeoff,
  which was the old plan's central weakness, does not apply to them.
- No dependence on detector recall. The old plan's guarantee was only as good as its weakest NER pass.
- It is a *cannot*, not a *promise*. Blind signatures mean the provider is structurally unable to
  identify the account, in the same sense that Kagi cannot link a search to a subscriber.
- Anonos's patents read on PII substitution, which we demote to a measured feature. They do not read on
  anonymous credentials or oblivious transport.
- The patent white space is exactly here: no filing claims per-recipient unlinkability for *model
  providers*, negative-disclosure attestation, or detokenisation bound to a tool's action boundary.

---

## Build order

**Tier 1, ship first. Cryptographic, zero utility cost, weeks each against known-good specs.**

1. Blind-signature access tokens. Kagi's February 2025 implementation is the template: 216-byte
   single-use tokens, ~1 second to mint 500.
2. Oblivious HTTP with a third-party relay. Fastly and Cloudflare both sell it. **Do not pick a relay
   that also fronts the upstream provider** — that irony would void the whole claim.
3. Flat-rate prepaid vouchers through a merchant of record. Sells time, not metered usage, which
   sidesteps both the money-transmitter question and the unstandardised anonymous-metering crypto.
4. Constant-rate response padding. Mandatory, not optional: the token-length side channel reconstructs
   27% of streamed responses and the topic of 53%, and OHTTP explicitly does not cover it.
5. Uniform client. One pinned TLS stack, fixed JA4, fixed header order.

**Tier 2, real cost and real benefit.** A local quasi-identifier pass using adversary-in-the-loop
rewriting rather than a PII list, spent against a per-session risk budget. Timing decorrelation.
Memory abstinence by default.

**Tier 3, optional.** Style obfuscation, per session, for high-risk use only. It is the worst
privacy-per-unit-cost item on the list: it damages the text, partly fails against a retrained attacker,
and is itself detectable at F1 0.87, which makes "this user obfuscates" a durable label.

**Do not build.** Mixnets. Homomorphic or multi-party inference for proprietary weights. Word-level
differential privacy rewriting. Post-quantum Privacy Pass at 85 to 175 kB per token. Anonymous *metered*
credit until ACT or an equivalent reaches a standard.

---

## The two constraints that decide whether this is a company

**1. Reseller terms.** Anthropic's commercial terms prohibit reselling except as expressly approved.
A pooled-account intermediary is not a clever proxy, it is a partnership, and it has to be negotiated
before anything else matters. **This is the go/no-go and it should be tested in week one, not month
six.** The fallback if the answer is no: sell the harness to enterprises who bring their own provider
contract, where pooling is internal and no resale occurs.

**2. The anonymity set is the subscriber base.** A blind signature is only as anonymous as the crowd
holding one. Below a few thousand active users the guarantee is thin and we must say so. This makes the
privacy story and the growth story the same story, which is unusual and worth stating plainly rather
than hiding.

---

## What to file

In order of strength, drafted narrowly against Datavant and Anonos:

1. Provider-scoped surrogate derivation, where the salt is bound to the **recipient model provider's
   identity**, the purpose is preventing rather than enabling linkage, and resolution is device-local.
2. Negative-disclosure attestation: a hash-chained signed ledger committing to the set of entities
   **withheld** at a boundary. Transparency logs universally attest to what happened; attesting to what
   did not is inverted and appears unclaimed.
3. Action-boundary detokenisation, binding the release of a true value to a specific tool, action type
   and parameter position in a capability manifest.

Do not file on PII detection, surrogate substitution as such, vault round trips, or format-preserving
encryption. All four are owned or are pre-2020 prior art.

**Before committing engineering to any tokenisation architecture, have counsel answer one question:**
are the AI-inference limitations in Anonos US12417317 supported by the 2013 provisional, or only by the
2021-2022 continuations-in-part? If the latter, the effective date moves and a large body of 2021-2023
prior art becomes available.

---

## One cheap asset

The paper everyone cites for "anonymisation makes models dumber" (Deußer et al. 2026) measured bracketed
tags, not realistic surrogates, and its own worked example redacts the words *Earth* and *Sun*. Nobody has
run the experiment properly. A paired benchmark measuring realistic-surrogate substitution against
capability benchmarks across three frontier models is a few weeks of work, is publishable, and would let
us own the evaluation frame for the category.
