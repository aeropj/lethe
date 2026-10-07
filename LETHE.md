# Lethe

**The private pool for frontier AI.**

Pranjal Joshi · Prashil Bulbule · 18 September 2026

This is the complete document. It supersedes `paper/`, `yc-application.md` and `STRATEGY.md`, all of
which describe an earlier plan that the evidence did not support. Sources are in `research/`.

---

## 0. Read this first: the October 2026 research verdict

A full competitive study (`research/landscape/landscape.pdf`, 18 pages; long-form report in
`reports/Private AI access competitive landscape.md`) tested the strategy below against every company in
the space. **Its verdict: as pitched in sections 1, 5 and 8, Lethe would not be funded by a seed investor
or YC.** Sections 1 to 13 are kept as written so the team can see what changed; where a claim has been
disproved it is marked *Corrected*.

**What the study found**

- **Pooling is not new.** More than a dozen products already put many users behind one provider account
  in front of GPT, Claude and Gemini: Duck.ai, Brave Leo, Kagi, Venice's Anonymous mode, 1Privacy,
  nullsink, Apple's signed-out ChatGPT extension.
- **The core primitive already ships.** OpenAnonymity (Stanford and Michigan PhD students) puts Privacy
  Pass blind signatures in front of GPT, Claude and Gemini through shared OpenRouter accounts, free, and
  is building a local memory "secretary". LLMTor and the Ethereum Foundation's zkAPI ship other pieces.
- **Consumer demand is proven; institutional demand is not.** Venice is profitable at more than $70M ARR
  and was valued at $1B in July 2026. No bank, fund or law firm on record wants to hide its identity
  from the lab. JPMorgan, Goldman, Morgan Stanley, Balyasny and Freshfields already use frontier models,
  often through Bedrock or Azure where the lab cannot see their data. When Anthropic imposed 30-day
  retention, the big banks negotiated **custody** of the monitoring logs, not anonymity.
- **The labs' safety rules work against an anonymous pool.** Top models now require misuse detection
  across sessions, and the newest are limited to approved partners. Mixing firms and anonymous
  consumers in one account is the pattern those rules target.
- **The unclaimed gap is accountable anonymity:** giving a lab the cross-session safety signal it now
  insists on without giving it identity. Nobody offers that at commercial quality, with a provider's
  approval.

**The reshaped strategy, ranked by the study**

1. **Accountable anonymity as a paid consumer and prosumer product**, at the $15 to $20 a month that
   Venice and Duck.ai validated, with margin. Rate-limited anonymous credentials, an independent relay,
   an attested gateway so "we don't log" is checkable, padding, a published anonymity-set size, memory
   on the device, and Lethe as the accountable customer running misuse monitoring under its own keys
   without learning identity. The pitch is "Duck.ai with proofs", not "a dark pool for AI".
2. **License that layer** to intermediaries that already pool users (Kagi has not brought Privacy Pass to
   its Assistant) and to apps in sensitive categories.
3. **Provider-blind, firm-audited access for mid-size firms** that cannot get zero retention or
   customer-held monitoring on their own, priced like a gateway, with anonymity as a feature.
4. **Keep the institutional dark pool as an option with a trigger**, such as a lab launching a trading
   or advisory business. Not a pitch today.

**Stop:** leading with "dark pool for AI" and $100k to $500k memberships; claiming nobody does this;
putting firms and consumers in one provider account; pricing the consumer app at break-even.

**What would reverse the institutional verdict, testable in thirty days:** three funds signing letters
of intent that name hiding their identity from the lab as the reason; one lab agreeing in writing to
serve pooled anonymous institutional traffic; one regulated firm's risk team confirming it could onboard
such a pool.

---

## 1. The thesis in one paragraph

Lethe is a shared anonymity pool in front of GPT, Claude and Gemini. Firms and people send their AI work
through it, and the providers see a crowd instead of a customer: credentials are blind signatures rather
than accounts, payment cannot be linked to usage, and traffic leaves by a different oblivious path per
provider. Every member makes every other member harder to identify, so the pool gets stronger as it grows.
Firms pay for membership because, for a fund or a bank, the question itself is the secret. People get a
memory that lives on their own machine, priced near break-even, and they are what makes the pool large.
What you write still reaches the model; we measure what that text carries rather than pretending we
removed it.

The last sentence is load-bearing. A hosted model must read the prompt. Any product claiming otherwise is
selling a feeling, and will be taken apart in technical diligence.

---

## 2. Why now

Three things became true in 2026 that were not true when the previous attempts at this failed.

**The profile became a revenue line.** OpenAI shipped ads in February on US free and Go tiers, targeted
on conversation topic, past chats and prior ad interactions. In June it published *Dreaming*, background
consolidation that builds narrative prose dossiers about a user between sessions. OpenAI's own EU policy
concedes that using memory for personalised ads requires affirmative consent, while non-consented
contextual ads are limited to the live conversation. The industry has already admitted what memory is
for. This is no longer a retention-policy problem that a contract can fix; it is a business model, and it
will get better at its job rather than worse.

**The cross-provider join stopped being hypothetical.** On 18 September 2026, `api.openai.com`,
`api.anthropic.com`, `api.mistral.ai`, `api.x.ai`, `api.together.xyz`, `api.groq.com` and `openrouter.ai`
all return `server: cloudflare`. Anthropic's endpoint resolves into Anthropic's own address block but
still answers with Cloudflare headers, so DNS and WHOIS give the wrong answer. Google is the only major
provider fronting itself. One commercial party terminates TLS for at least seven providers. Joining one
person's activity across all of them needs no data broker and no subpoena, only a query against one edge
network's logs.

**And a cruder join is already running.** Koi Security found eight browser extensions from a single
publisher, more than eight million installs, capturing prompts and responses from ten AI platforms
including ChatGPT, Claude, Gemini, Copilot and Perplexity before they render, with no opt-out, added
silently in a July 2025 update, flowing to a company affiliated with the data broker BiScience.

**Meanwhile the tools to stop it finished.** Privacy Pass became RFC 9576, 9577 and 9578 in June 2024.
Oblivious HTTP is RFC 9458 and is deployed by Apple, Google, Mozilla and Meta. Apple Private Cloud
Compute and Meta's WhatsApp Private Processing both ship anonymous credentials plus oblivious transport
plus attested compute for LLM workloads, in production, at hundreds of millions of users. Kagi shipped
blind-signature tokens for paid search in February 2025 and can no longer link a query to a subscriber.

Every primitive exists. *Corrected October 2026:* pieces of this have already been assembled in front of
frontier models (OpenAnonymity and LLMTor use blind tokens; Brave and zkAPI unlink payment). What nobody
offers is the full stack, under a provider contract, at commercial quality.

---

## 3. The ten channels

A profile is built through ten channels. Our original design closed one of them, partially.

| # | Channel | How the profile gets built | Defence | Cost to answer quality | Who has shipped it |
|---|---|---|---|---|---|
| 4 | Account | API key, login, phone, ID | Blind-signature tokens (RFC 9474 / 9576-78) | **none** | Apple, Meta, Kagi, Brave |
| 5 | Payment | Card in your name, tied to usage | Flat-rate vouchers via merchant of record | **none** | Mullvad |
| 6 | Network | IP, TLS fingerprint, packet sizes, cadence | Oblivious HTTP plus constant-rate padding | **none** | Apple, Meta, Google, Mozilla |
| 9 | Cross-service | One party sees traffic to many providers | Per-provider egress diversity, distinct relays | **none** | nobody |
| 7 | Device | JA4, HTTP/2 settings, header order | Native client, one pinned TLS profile | none | Tor Browser, Brave |
| 10 | Memory | The provider's own persistent dossier | Do not use it; keep memory local | high | us |
| 1 | Content PII | Names and identifiers in the prompt | Reversible tokenisation | low | commodity |
| 2 | Quasi-identifiers | Employer plus city plus condition | Local adversarial rewriting | **high** | nobody in production |
| 3 | Writing style | Authorship attribution across sessions | Style-aware paraphrase | **high** | nobody |
| 8 | Timing | Circadian rhythm, session cadence | Queue, jitter, batch | none, but latency | Nym, at heavy cost |

**Four of these close with cryptography at no cost to the answer.** That is the entire reframe. The
privacy-versus-capability tradeoff, which was the previous plan's central weakness, simply does not apply
to channels 4, 5, 6 and 9.

---

## 4. What the evidence killed

The previous plan was reversible identity tokenisation with per-provider surrogates. Six findings ended it.

**The mechanism was already published.** *SurrogateShield* (arXiv:2606.29567, Sherwin Vishesh Jathanna,
28 June 2026) describes a client-side proxy that substitutes type-consistent surrogates before
transmission and restores originals in the response, with mappings sealed in an AES-256-GCM per-conversation
vault that never leaves the device, and a detection cascade covering 22 PII types plus quasi-identifier
combinations grounded in Sweeney's k-anonymity. That is our architecture including the k-anonymity
scoring we claimed as a gap. It is a solo preprint rather than a company, so it blocks a novelty claim
without being a competitor.

**Per-provider surrogate rotation does not produce unlinkability.** Lermen, Paleka, Swanson, Aerni,
Carlini and Tramèr, USENIX Security 2026 (arXiv:2602.16800), link the same person's pseudonymous profiles
at up to 68% recall at 90% precision, against near zero for the best non-LLM method, including across a
deliberately removed one-year gap, for a few dollars a target, scaling to roughly 27% recall against a
hundred million candidates. The surrogate was never the linkage channel. Topic, expertise and recurring
specifics are. Rotating a fake name buys nothing.

**Entity replacement is provably insufficient even at its best.** RAT-Bench measures re-identification
after anonymisation: Presidio leaves 59% on explicit identifiers and 30% on implicit. Five rounds of full
adversarial LLM rewriting, far more destructive than tokenisation, still leave 41.6% attribute inference
(Staab et al., ICLR 2025). The regulatory threshold is 5%. Nothing reaches it.

**The mechanism is patented, by a licensing company.** Anonos US12417317, granted 16 September 2025,
claims per-element substitution in input to an AI model plus the recovery mapping, with dependent claims
on generative AI and on re-identifying the model's response. US12614034B2, granted 28 April 2026, adds
NLP span detection, reversible semantic tokens into an LLM, and selective reversal at authorised
endpoints. Anonos has live continuations publishing in 2026 and can still draft claims aimed at whatever
we ship.

**The consumer privacy thesis has a graveyard.** Brave converts 101 million privacy-selected users into
roughly 100,000 VPN subscribers, one tenth of one percent. Mozilla earns $66.4M from subscriptions and
advertising combined across about 200 million users, growing 2.5% a year. Crosshatch, the closest funded
attempt at per-agent data scopes, shut down in July 2025. Blyss died on the encrypted-inference thesis
with a Stanford and Apple team, two years before Tinfoil raised on the same idea. Piiano abandoned its
vault after four years and became an agent governance plane.

**The Datavant comparison is backwards.** Datavant holds the master salt, and holding it *is* the
business. Local key custody deliberately destroys the only asset they monetise. The linkable version of
that business, LiveRamp, sold to Publicis at about 2.7x revenue with 107% net revenue retention.

---

## 5. The company

Lethe sells membership in a pool, not prompt redaction and not a chat app.

**Why this is not a wrapper.** A wrapper puts a screen on someone else's model; it is no better with a
million users than with ten, a customer can rebuild it in a weekend, and the provider usually ships it
themselves. A pool is the opposite on all three counts. Its value rises with every member, because
anonymity loves company (Dingledine and Mathewson, WEIS 2006). No customer can build it alone, because a
firm running its own proxy is still the one firm using that proxy. And the provider cannot build it,
because hiding a customer from yourself is a promise against yourself. A competitor does not need a better
UI to catch up. It needs a bigger crowd.

**Why this is defensible where the old plan was not.**

- Zero utility cost on the four channels we lead with.
- No dependence on detector recall. The old guarantee was only as strong as its weakest NER pass.
- It is a *cannot*, not a *promise*, and there is a number for what that is worth. Proton complied with
  88.4% of legal orders against Mail between 2017 and 2025, and denied 410 of 410 against VPN, because
  they are unable to comply even when the order binds. That gap is the product line, measured.
- Anonos's patents read on PII substitution, which we demote to a measured feature. They do not read on
  anonymous credentials or oblivious transport.
- The patent white space sits exactly here. No filing claims per-recipient unlinkability for *model
  providers*, negative-disclosure attestation, or detokenisation bound to a tool's action boundary.

**What we still say plainly.** The model reads the prompt. Content and quasi-identifiers are measured and
reported, never claimed to be zero. A blind signature is only as anonymous as the crowd holding one, so
below a few thousand active users the guarantee is thin and we say so on the page.

---

## 6. Build order

**Tier 1. Cryptographic, no utility cost, weeks each against published specs.**

1. **Blind-signature access tokens.** Kagi's February 2025 implementation is the template: 216-byte
   single-use tokens, about one second to mint 500, 2,000 to 3,000 per month per subscriber.
2. **Oblivious HTTP with a third-party relay.** Fastly and Cloudflare both sell it. Do not pick a relay
   that also fronts the upstream provider; that irony would void the claim.
3. **Flat-rate prepaid vouchers through a merchant of record.** Selling time rather than metered usage
   sidesteps both the money-transmitter question and the unstandardised anonymous-metering cryptography.
4. **Constant-rate response padding.** Mandatory. The token-length side channel reconstructs 27% of
   streamed responses and the topic of 53%, and OHTTP explicitly does not cover traffic analysis.
5. **A native client, not a browser extension**, with one pinned TLS profile, fixed JA4 and fixed header
   order. Removes an entire adversary class for almost no engineering. Uniformity beats randomisation;
   Brave retired its own Strict mode because sub-0.5% adoption made those users more identifiable.

**Tier 2. Real cost, real benefit.**

6. A local quasi-identifier pass using adversary-in-the-loop rewriting rather than a PII list, spent
   against a per-session risk budget instead of applied blanket.
7. Timing decorrelation: decouple compose from dispatch, jitter, batch.
8. Memory abstinence by default, with memory held locally instead.

**Tier 3. Optional, high-risk sessions only.** Style obfuscation. It has the worst privacy per unit cost
on the list: it damages the text, loses most of its effect against a retrained attacker, and is itself
detectable at F1 0.87, which makes "this user obfuscates" a durable label.

**Do not build.** Mixnets, which cap at roughly 100 KB/s with p99 near three seconds. Homomorphic or
multi-party inference for proprietary weights, which is three to four orders of magnitude off and only
works on open weights. Word-level differential privacy rewriting, which is reconstructed at 72% to 94% at
the epsilons where utility survives. Post-quantum Privacy Pass at 85 to 175 kB per token. Anonymous
*metered* credit until ACT or an equivalent reaches a standard.

**Do not lean on confidential compute for the trust story.** Independent 2026 measurements put overhead
between 1% and 118%, not the sub-9% vendors quote, and Battering RAM forges attestation with $47.62 of
parts. Use it as defence in depth, never as the claim.

---

## 7. Competition

**Reversible tokenisation, org-side.** Protecto, WitnessAI, Skyflow, Kong's sanitizer with its restore
flag, Tonic. The vendor holds the keys and none has an agent path. Skyflow repositioned in 2026 as
runtime AI data control and ships a de-identify/re-identify LLM gateway.

**Reversible tokenisation, open source.** Anonproxy is the best-engineered (4,750 lines, 120 tests, eight
PyPI releases) but has 7 stars and was built in essentially one AI-assisted day. `DontFeedTheAI`, which it
reimplements, has 655. Presidio has 10,931 and left Microsoft for a neutral foundation. Dataiku ships a
fully reversible proxy as Apache-2.0 with no paid tier. LLM Guard, the most-cited comparison, was archived
in July 2026. Detection itself is free from OpenAI and NVIDIA.

**Confidential compute.** Tinfoil (YC X25), Confer, Privatemode, Apple PCC. A stronger promise on the
content channel, limited to open weights, and explicitly positioned against redaction. Tinfoil's own YC
profile calls PII redaction a band-aid that does not work in practice. That objection is coming and must
be answered first, not fourth.

**Anonymous access.** 1Privacy.ai, nullsink and Venice.ai are the nearest. Venice is the important one:
roughly $70M ARR, profitable, about two years old, on an explicit no-logging pitch. The lesson is that
paid AI privacy rides the $20/month AI anchor, not the $5/month privacy anchor.

**Inside YC.** Across 2,398 companies in thirteen batches nobody is doing reversible tokenisation with
local key custody. But LogosGuard (F25) is one-way on-device redaction, Egoist Machines (S26) is per-app
scopes with audit receipts, and the agent-authorisation lane has at least six bets: Alter, Multifactor,
Agentic Fabriq, Decawork, Clawvisor, Golf. Lead with the access primitive; the agent gateway now reads as
me-too.

---

## 8. Business model

**Institutions already pay to hide what they are about to do.** Roughly 15 to 18% of US equity volume
trades in dark pools, and around 44% off-exchange in total, so that a large order does not move the market
before it fills. Lethe is a dark pool for AI. The firms that pay are the ones whose questions are worth
more than their answers: hedge funds, private equity, investment banks and corporate development, large
law firms, pharmaceutical research. *Corrected October 2026:* the 2023 restrictions are out of date. JPMorgan,
Goldman Sachs, Morgan Stanley, Balyasny and Freshfields now use frontier models at scale, often through
Bedrock or Azure where the lab cannot see their data, and no firm on record asks to hide its identity
from the lab.

Three revenue lines:

1. **Firm membership, $100,000 to $500,000 a year by size.** The profit centre. Includes the firm's own
   compliance ledger, policy controls and single sign-on. Anchors: analysts already pay $10,000 to
   $20,000 a seat for AI research tools such as AlphaSense and Hebbia, Rogo was valued at $2B in April,
   and hedge funds average $1.6M a year on alternative data.
2. **A per-query fee on usage passed through at cost.** The way a dark pool charges per share. We never
   subsidise anyone's tokens, so heavy users cannot sink the margin.
3. **The consumer memory app at about $20 a month, near break-even.** Not where we make money. Its job is
   to make the pool large, because a large pool is what the firms are paying for. Every member protects
   every other member, consumers included.

**Compliance is a selling point, not an obstacle.** US regulators have fined financial firms more than
$2 billion since 2021 for business communications they failed to record. Anonymous AI that left no record
would be a liability. Lethe writes every request to a ledger the firm holds: the compliance team keeps
everything, the provider keeps nothing that points to the firm.

**Lethe holds the provider contracts.** Members are anonymous behind it. A firm bringing its own contract
would be identified by it, so that option gets content protection only and is not the product. The pitch
to the providers is net-new demand: the work in the pool is work they do not get today.

**How big, honestly.** Illustrative, not a forecast: 500 member firms at $250,000 a year is $125M of annual
revenue before usage fees, 2,000 is $500M. That is a different company from the security-tool path, where
the median contract is about $25,000 and the closest exit, Portkey, sold for $117M. The constraint is not
price, it is the crowd: a pool with one fund in it hides nobody. Capital discipline still applies; raise
what the founding cohort needs, not more.

**Nobody does this.** *Corrected October 2026:* narrowly true for institutions, because no institution
has asked for it. For individuals, pooled anonymous access to frontier models is already widespread; see
section 0.
---

## 9. The two things that decide whether this is a company

**Accountability for anonymous users.** An earlier draft of this document called reseller terms the
go/no-go. That was wrong for the shape we are building. Anthropic's commercial terms explicitly permit
using the API "to power products and services Customer makes available to its own customers and end
users" (clause A.1). What they restrict is reselling the Services themselves except as expressly approved
(clause D.4). So an app serving our own subscribers is permitted; selling anonymous raw API access to
developers would look like resale and needs approval. The real constraint is that we stay responsible for
our users' compliance with the usage policy, and anonymous users make abuse prevention our problem. The
answer is the one Apple, Meta and Kagi already use: credentials that are rate-limited by construction, so
each one is good for a finite number of requests. We have read Anthropic's terms; OpenAI's and Google's
still need the same read.

**The pool starts empty.** A blind signature is only as anonymous as the crowd holding one, and a pool
with one fund in it hides nobody. This is the classic network-effect cold start, and it is the single
biggest risk. Dark pools solved it by launching with a founding consortium of buyers; we plan the same, a
founding cohort of firms who join together, with the consumer app filling the crowd from day one. Until
the pool is large, we say on the page how large it is.

**Institutional access needs the providers' approval.** An app serving our own members is permitted.
Pooled access for a firm's own agents is closer to reselling and needs approval. We believe the providers
want the demand; we have not yet asked.

**The pool hides who, not what.** If only one member is asking about a particular company, the question is
a signal even when nobody can tell whose. We measure and show this; we never claim zero.

---

## 10. What to file

Drafted narrowly against Datavant and Anonos, in order of strength:

1. Provider-scoped surrogate derivation where the salt binds to the **recipient model provider's
   identity**, the purpose is preventing rather than enabling linkage, and resolution is device-local.
2. Negative-disclosure attestation: a hash-chained signed ledger committing to the set of entities
   **withheld** at a boundary. Transparency logs attest to what happened; attesting to what did not is
   inverted and appears unclaimed.
3. Action-boundary detokenisation, binding release of a true value to a specific tool, action type and
   parameter position declared in a capability manifest.

Do not file on PII detection, surrogate substitution as such, vault round trips, or format-preserving
encryption. All four are owned or pre-2020 prior art.

**Before committing engineering to any tokenisation architecture**, have counsel answer one question: are
the AI-inference limitations in Anonos US12417317 supported by the 2013 provisional, or only by the 2021
and 2022 continuations-in-part? If the latter, the effective date moves and a large body of 2021 to 2023
prior art becomes available.

---

## 11. Next thirty days

1. Talk to ten firms, funds first, and find the three who would join a founding cohort. Ask what they
   do today instead of using frontier models for deal work, and what they would pay to stop.
2. Read OpenAI's and Google's commercial terms the way we read Anthropic's, and open the conversation
   with one provider about institutional access through the pool.
3. Stand up blind-signature tokens plus OHTTP against one provider and measure added latency end to end.
4. Run the paired capability benchmark nobody has run. The paper everyone cites for "anonymisation makes
   models dumber" (Deußer et al. 2026) measured bracketed tags, not realistic surrogates, and its own
   worked example redacts the words *Earth* and *Sun*. Measuring realistic surrogates properly across
   three frontier models is a few weeks, is publishable, and would let us own the evaluation frame.
5. Ask counsel the Anonos priority question.
6. Email John Freeman, who wrote Anonproxy. He is the best-informed person on this problem outside the
   team, has eight open issues and no contributors, and the conversation costs nothing.

---

## 12. Research index

| File | Contents |
|---|---|
| `research/01-landscape.md` | Competitive landscape, standards, provider data policies |
| `research/02-naming.md` | Lethe, alternatives, component naming |
| `research/03-first-principles.md` | LLM pipeline, memorisation, utility evidence |
| `research/04-architecture.md` | Detailed technical architecture of the tokenisation design |
| `research/05-anonproxy.md` | Full source study of the closest open-source implementation |
| `research/06-research-frontier.md` | Academic frontier, with independent verification of key papers |
| `research/07-startup-landscape.md` | Startups, funding, M&A, the graveyard, consumer monetisation |
| `research/08-yc-landscape.md` | All 2,398 YC companies across thirteen batches, filtered |
| `research/09-profiling-channels.md` | The ten channels, deployed systems, sequencing |
| `research/10-patents.md` | Freedom to operate, white space, what to file |

`paper/lethe.tex` is the current proposal. `paper/slides.tex` is stale and still describes the superseded plan.
figures and for the record.

---

## 13. On the name

*Lethe: the river in Hades whose water erases memory. Mnemosyne: the pool that restores it.* Orphic
initiates were told to avoid the first and drink from the second.

The name still fits the new thesis, and fits it better. The provider drinks from Lethe and never learns
who was asking. You, and your compliance team, keep Mnemosyne.
