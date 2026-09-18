# The profiling channels — complete enumeration and state of the art (2026-09-18)

**Scope.** A user wants frontier-model capability with it *structurally impossible* for any provider or coalition to profile them. Our design (reversible PII tokenization, local vault) closes one channel. This enumerates all ten, gives the state of the art for each, and says what is honestly achievable.

Companion to `06-research-frontier.md`, which surveys the anonymization/linkage literature. This document is organised by **channel**, adds the **deployed-systems** comparison and **sequencing**. Load-bearing new findings here: Meta's WhatsApp Private Processing whitepaper (v2, 16 Mar 2026); live measurement of who fronts the AI APIs; Kagi's shipped Privacy Pass; prompt-level stylometry numbers; and the fact that the cross-service join is **already happening**, via browser extensions rather than clouds.

---

## 1. Master table

| # | Channel | How a profile gets built | State-of-the-art defence | Maturity | Cost (eng / utility / UX) | Who has done it |
|---|---|---|---|---|---|---|
| 1 | **Content PII** | Names, IDs, addresses in the prompt | Reversible format-preserving tokenization, local vault | **Shipped** | Low / low / low | Us; Anonproxy; Presidio |
| 2 | **Quasi-identifiers + semantics** | LLM infers location/age/income/employer from free text | Local **adversarial anonymization** (adversary-in-the-loop rewrite), not PII lists | **Research → early product** | Med / **high** / med | Nobody in production |
| 3 | **Writing style** | Authorship attribution; cross-session linkage | Style-aware LLM paraphrase; aggregation-aware rewriting | **Research** | Med / **high** / high | Nobody |
| 4 | **Account / auth** | API key, login, phone, gov ID | **Blind-signature / VOPRF tokens** (RFC 9576–9578, RFC 9474, RFC 9497) | **Deployed elsewhere** | Med / **zero** / low | Apple PCC & PAT, Meta ACS, Kagi, Brave |
| 5 | **Payment** | Card in your name → usage | Flat-rate vouchers / cash / Monero; **ACT** credit tokens for metering | **Deployed (flat-rate)**; prototype (metered) | Med / zero / med | Mullvad, Venice, Maple AI |
| 6 | **Network metadata** | IP, TLS FP, **packet sizes, token cadence** | **OHTTP (RFC 9458)** + constant-rate response padding | **Deployed** | Med / zero / low | Apple PCC, Meta, Chrome SB, Firefox |
| 7 | **Device / client** | JA4 TLS, HTTP/2 settings, header order — **and extensions in the page** | Uniform pinned client; **native app, not a browser surface** | **Deployed** (browsers) | **Low** / zero / low | Tor Browser, Brave |
| 8 | **Timing / behaviour** | Circadian rhythm, session cadence, typing | Decouple compose from dispatch; jitter; batch | **Research** | Low / zero / **med** | Nym, at ruinous cost |
| 9 | **Cross-service join** | One party observes traffic to several providers | Per-provider relay diversity; get off the browser | **Partially deployable** | Med / zero / low | Nobody |
| 10 | **Provider memory** | Persistent dossier the provider builds, now an **ad-targeting input** | Don't use it; local per-scope memory | **Shipped** (opt-out) | Low / **high** / high | Us (locally) |

---

## 2. Deep dive — stylometry

**The attack, at scale.** Narayanan et al. (IEEE S&P 2012; 100,000 blogs, style-only features) get **~20% top-1** from ~900 words and **>80% precision at 50% recall** once allowed to abstain; the median case narrows 100,000 candidates to **100–200**. Accuracy falls **10–13 points per decade of pool size** (DeepStyle: P@1 64.8% at 50 users → 21.4% at 7,026). Length matters as much: AuthBench (arXiv [2609.06771](https://arxiv.org/abs/2609.06771), 153,825 authors) reports verification EER **0.104 at 1–10 tokens → 0.048 above 500**.

**Prompts specifically** — a literature gap until this year. **PromptPrint** (arXiv [2606.06755](https://arxiv.org/abs/2606.06755)) uses **20,680 real prompts from 1,034 users**, 20 each: **64.2% top-1**, 79.3% top-5 across the full gallery; 76.9% at 100 users, 62.3% at 1,034. Performance plateaus at **N=10 prompts**. Synonym substitution at 20% costs the attacker **0.1 points**; full semantic paraphrase drops top-1 to **42.9%**. Ten prompts identify you, and only rewriting that changes meaning-bearing choices helps.

**But style is the weaker channel, and this is the key strategic fact.** SALA (arXiv [2602.23079](https://arxiv.org/abs/2602.23079)) finds zero-shot **open-world** candidate search puts the true author in a 20-candidate shortlist only **1.2%** of the time — but **78.1%** with a warm candidate database. A provider holding every user's history is in the database-augmented regime by default. And Lermen et al. (USENIX Sec 2026, arXiv [2602.16800](https://arxiv.org/abs/2602.16800)) show what actually links sessions is **content**: **55.2% recall at 90% precision** against 89,000 candidates, extrapolating to **~27% at 100M**, at **$1–4 per target**. Aggregation dominates: AAST (arXiv [2608.22161](https://arxiv.org/abs/2608.22161)) finds unprotected Reddit text reaches **100 R@8 at K=8** bundled messages under LUAR.

**Measured cost of obfuscation.**

| System | Attribution drop | Utility cost |
|---|---|---|
| Mutant-X (PoPETs 2019) | 59–64% on EBG | METEOR **0.54–0.55** |
| TAROT-DPO (EMNLP-F 2024) | 99.8% → **17.3%** | downstream utility 79.5 → 60.7 (**−19 pts**) |
| "I Am No One" (Interspeech 2026, [2609.12341](https://arxiv.org/abs/2609.12341)) | F1 66.45 → **26.02** | **perplexity preserved** (42.5 vs 41.0) |
| Word-level DP, ε=6 | MCC 0.98 → 0.12 (static) | GPT-2 PPL **44.5 → 5,003** — destroyed |

Three catches. **(a) Adaptive attackers recover most of it.** Zhai et al. (ACL 2022): retraining the attributor on obfuscated text collapses Mutant-X's effect from −32 points to **−5**. Mattern et al. (NAACL-F 2022): word-level DP at ε=6 leaves author MCC at **0.58 adaptive** vs 0.12 static; at ε=12, **0.95**. Only *generation*-based obfuscation has survived retraining, in one paper. **(b) Obfuscation is detectable** at **F1 0.87** (arXiv [2005.00702](https://arxiv.org/abs/2005.00702)) — "this user obfuscates" is itself a durable label. **(c) PAN abandoned the task after 2018**: per the organizers, approaches are either "somewhat safe but… unreadable" or "sound and sensible… but not safe."

**Verdict: worst privacy-per-unit-cost on the list.** Expensive, damages the text, partly defeated by retraining, announces itself, and closes a weaker channel than the content beside it.

---

## 3. Deep dive — anonymous authentication

**The cryptography is finished and deployed — just not by AI labs.**

- **Privacy Pass**: RFC **9576** (architecture), **9577** (`PrivateToken` scheme), **9578** (issuance), June 2024. Type `0x0001` VOPRF(P-384), 48-byte authenticator, privately verifiable; type `0x0002` blind RSA-2048 (**RFC 9474**), 256-byte, publicly verifiable. VOPRF is **RFC 9497**.
- **Apple Private Access Tokens** (iOS 16+, June 2022): iCloud attests, **Cloudflare or Fastly issues**, the site is the origin. **>65%** of Cloudflare customers already run the prerequisite Managed Challenge.
- **Apple Private Cloud Compute authorizes LLM inference with RSA blind signatures** plus a third-party OHTTP relay — anonymous auth to a frontier-class model, in production, just not exposed as an API. Private Relay uses the same primitive with **daily-rotated** tokens.
- **Meta's Anonymous Credential Service** — VOPRF + blind signatures + KDFs with attributes, **open source** (`github.com/facebookresearch/acs`), at Meta scale, now gating WhatsApp AI. Credentials are usable "a finite number of times": that is how rate limiting survives anonymity.
- **Kagi Privacy Pass** (shipped **13 Feb 2025**) is the closest commercial analogue: RFC 9576–9578, **216-byte single-use tokens**, 2,000–3,000/month, **~1 s to mint 500**. Kagi can no longer link a search to an account. **Brave** issues unlinkable Leo Premium tokens via `challenge-bypass-ristretto` (VOPRF over ristretto255).

**The unsolved piece is metered spend.** `draft-ietf-privacypass-rate-limit-tokens` **expired**. The live answer is Cloudflare's October 2025 work ([blog.cloudflare.com/private-rate-limiting](https://blog.cloudflare.com/private-rate-limiting), framed around AI agents): **ARC** issues one credential good for 1,000 unlinkable presentations in **1.35 ms**, 288-byte presentations, ~70× faster than batched VOPRF; **ACT** is *stateful*, carrying a credit balance proven by range proof — **251 µs issuance, 1,867-byte presentation** — decremented per request and revocable. `draft-meunier-privacypass-reverse-flow-07` adds refunds for cheap requests. Post-quantum variants cost **85–175 KB/token** — unaffordable.

**What the labs require.** Anthropic's help centre states a text-capable **non-VoIP** phone number is mandatory and "there isn't a way to skip this step." OpenAI requires phone verification for a first API key and **government ID via Persona** for top models. No statute compels this — the EU AI Act's Art. 50 is a *disclosure* duty running provider→user, and an inference seller is a merchant, not a money transmitter. It is abuse control, and OpenAI says so. **The real blocker is contractual:** Anthropic's commercial terms forbid reselling "except as expressly approved," so a pooled-account intermediary needs a partnership, not a clever proxy.

---

## 4. Deep dive — network metadata

**The LLM-specific side channel is real and unmitigated.** Weiss, Ayzenshteyn, Amit & Mirsky (USENIX Security 2024) exploit the **token-length side channel**: streamed responses emit one chunk per token, so an eavesdropper reads a sequence of token lengths and reconstructs **27% of responses** and infers the **topic of 53%**, against ChatGPT-4 and Copilot, browser *and* API traffic. **Whisper Leak** (arXiv [2511.03675](https://arxiv.org/abs/2511.03675)) generalises to size *and* timing across **28 models**, hitting **>98% AUPRC** topic classification and 100% precision on some sensitive topics at a **10,000:1** noise ratio — and finds padding, batching and packet injection each leave gaps. Server-side cousins recover other users' prompts from KV- and semantic-cache timing (*Early Bird*, arXiv [2409.20002](https://arxiv.org/abs/2409.20002); *InputSnatch*, [2411.18191](https://arxiv.org/abs/2411.18191)).

**Transport.** OHTTP (**RFC 9458**) splits relay (sees IP, not content) from gateway (sees content, not IP) and is genuinely deployed: Apple PCC, Chrome Safe Browsing (Fastly relay), Firefox telemetry, Flo Health, and **WhatsApp Private Processing**. Its security considerations are explicit that it does **not** defend against relay–gateway collusion or **traffic analysis by timing and size** — exactly the Weiss/Whisper channel. An API key inside the request re-links everything, which is why OHTTP only works *composed with* channel 4.

The heavier options don't fit. Tor's design paper concedes it "does not protect against" a global passive adversary; median circuit latency is **110 ms (DE) / 270 ms (US) / 530 ms (HK)** across **9,351 relays**, and **≥3.67% of top-1,000 sites plus ~1.3M IPs block Tor exits** (NDSS 2016). Apple Private Relay is *easier* to correlate than Tor — no fixed cells, no cover traffic — and costs **−87% download, +60% median page-load time** in France (PAM 2023); its entire IPv4 egress pool is **106,621 addresses**, which is why it trips reputation gates. Nym's defaults are **15 ms/hop, ~50 packets/s, ~1 Mbps of cover traffic idle or not**, with only **60 of 866 nodes** in the active set per hourly epoch; Nym's own roadmap says it "is simply too slow for everyday usage." A token stream is the one workload that *fits* a mixnet — tiny payloads hiding inside padding already paid for — but the p99 tail breaks it.

**Who can already join it — measured today (2026-09-18, `dig`/`curl`).**

| Endpoint | Edge |
|---|---|
| `api.openai.com`, `chatgpt.com`, `platform.openai.com`, `auth.openai.com` | **Cloudflare** (`cf-ray`; explicit `…cdn.cloudflare.net` CNAMEs) |
| `api.anthropic.com`, `claude.ai` | IPs in **Anthropic's own ARIN block** — but `server: cloudflare` + `cf-ray`, i.e. **Cloudflare BYOIP** |
| `api.mistral.ai`, `api.x.ai`, `api.together.xyz`, `api.groq.com`, `openrouter.ai` | **Cloudflare** |
| `generativelanguage.googleapis.com`, `gemini.google.com` | Google only |

**One commercial party terminates TLS for OpenAI *and* Anthropic, plus five more providers.** DNS and WHOIS alone give the wrong answer for Anthropic. Google is the exception: it fronts itself end to end, so Google observes only Google.

---

## 5. Comparative study — who has actually built this

| System | Closes | Leaves open | Cost | Adoption |
|---|---|---|---|---|
| **Apple PCC** | Account (RSA blind sigs), IP (3rd-party OHTTP relay), retention (key randomized every reboot), code (transparency log, binaries public ≤90 days) | **Content** in the enclave; stylometry; hardware-vendor collusion; ChatGPT hand-offs leave the boundary | Custom silicon, VRE, bounty | ~All Apple devices |
| **Meta WhatsApp Private Processing** (v2, 16 Mar 2026) | Account (**ACS**, finite-use), IP (**Fastly** relay, which *also* distributes ACS/OHTTP key configs so Meta can't key-target), compute (**SEV-SNP** CVM + **H100 CC**), code (artifact transparency) | Content in the enclave; each CVM serves many users; "collusion with our hardware vendors… is out of scope" | Full CC stack | WhatsApp scale |
| **Kagi Privacy Pass** | Payment↔usage, account↔query | IP, timing, query content — Kagi says so plainly | ~1 s/500 tokens, 216 B/request | Paid tiers, Feb 2025 |
| **Mullvad** | Identity at the schema level — the account is **two columns**, number and expiry; cash by post and Monero; **563/563 relays diskless**; a **2023 police raid left with nothing** | Everything timing: one trusted hop sees source and destination | Near zero; **€5/mo since 2009** | Wide |
| **Signal** | Content (E2EE), sender metadata (sealed sender), contacts (SGX + Path ORAM) | Sealed sender **breaks in as few as 5 messages** via delivery receipts users cannot disable, *above* Tor/VPN (Martiny, Kaptchuk, Aviv, Roche & Wustrow, NDSS 2021); phone still required | **$14M/yr infra — $6M of it SMS registration fees**; ~$50M/yr projected | Global |
| **Tor** | Source↔destination vs any single observer | **Explicitly not** a global passive adversary | 110–530 ms; ≥3.67% of top sites block it | ~3.2M daily |
| **Nym** | IP + traffic analysis | Unusable interactively; 60-node set per epoch | ~1 Mbps always-on | "thousands" |
| **Brave Leo** | Subscription↔usage (unlinkable tokens), IP | **Content** — a single Brave-run reverse proxy; plaintext at Brave and the provider; non-retention is policy | Low | 120M MAU claimed |
| **DuckDuckGo Duck.ai** | IP (stripped before forwarding) | Content — **contractual** only: named providers, no-training, deletion "at most within 30 days" | Trivial | Broad |
| **Proton Lumo** | Internal pipeline (per-request AES key PGP-encrypted to the LLM server: "no intermediate system inside Proton can read the message"); history at rest is real E2EE | **Inference** — Proton states it "need[s] to provide the LLM with cleartext"; no TEE, no attestation, server code closed | Conversation re-sent every turn | 10M+ |
| **Tinfoil / Maple / Venice / Phala** | Compute (SEV-SNP/TDX + H100/B300 CC, reproducible builds, dm-verity weights); Venice takes **no account at all** via x402 USDC; Maple, no email | Identity and IP fully visible; wallets are permanent public pseudonyms; open weights only | See §6 | Small |

Two conclusions. First, the **existence proof is complete**: Apple and Meta have both shipped anonymous credentials + oblivious transport + attested compute for LLM workloads. Second, **not one system closes the content channel**, because a hosted frontier model must read the prompt.

The sharpest datum in the comparison is Proton's transparency report: **8,313 of 9,301 Mail orders complied with in 2025 (89.4%; 88.4% over 2017–2025) versus 410 of 410 Proton VPN orders denied — 100%**, because, in Proton's words, they are unable to comply "even if they are legally binding." That is *will not* versus *cannot*, measured. It is the argument for this entire product line.

A caution, though: the one shipped "unlinkable" inference system has a linkability bug. PCC's reverse-engineering (WiSec 2026, arXiv [2605.24239](https://arxiv.org/abs/2605.24239)) found the one-time-token nonce is `SHA256(TGT‖OTTSalt)`, OTTs replayed **2–5 times**, and TGT signature validation **disabled in production**.

---

## 6. What "non-profiling" can honestly mean in 2026

**"Structurally impossible to profile" is not achievable and must not be claimed.**

1. **The model must read the prompt.** TEEs move trust from "the provider promises" to "AMD/NVIDIA/Apple silicon plus an attestation chain" — a real upgrade, but every vendor puts physical attacks out of scope, and 2025–26 produced working attestation forgeries at hobbyist cost. Performance is also worse than the headline: vendor and 2024 academic figures say **<9%**, but Tinfoil's June 2026 measurements span **1% to ~118%** — tensor-parallel 8 at batch 1 runs **~2× slower**, speculative decoding pushes single-GPU overhead to **~70%**, and pinned CPU→GPU bandwidth collapses **55.7 → 4–11 GB/s**. Confidential computing gets relatively *worse* each GPU generation: the encrypted-link toll is fixed while compute accelerates. FHE and MPC remain 10³–10⁴× off and open-weights-only — a fact Nillion conceded by shipping a TEE.
2. **The content channel is the strong one and has no defence.** Lermen et al. link the same person across a **one-year gap** at 90% precision and deanonymize a third of users at **99%**, for $1–4 each. Staab's five-round adversarial rewrite still leaves **41.6%** attribute inference; Azure's PII removal leaves **74%** of information inferable on clinical text.
3. **Per-provider pseudonym rotation buys nothing.** The surrogate is not the linkage channel; topic, expertise, recurring projects and cadence are.

**The honest claim — still strong, and nobody offers it:**

> *No provider, and no coalition of providers, can link your requests to your identity, to your payment, or to each other — because the credential is a blind signature, the payment is unlinkable to the spend, and the network path is oblivious. What you write still reaches the model; we measure that residual risk before it leaves and tell you what it carries.*

Four channels closed **cryptographically** (4, 5, 6, 9), two **cheaply and completely** (7, 10), one **mechanically** (1), three **only partially and measurably** (2, 3, 8). Claiming the content channel is where this gets taken apart in diligence.

---

## 7. Cross-service correlation and provider memory — the two channels that got worse this year

**The join already exists, and it is not a cloud.** Koi Security found **eight extensions from one publisher, 8M+ installs** (Urban VPN Proxy alone: 6M Chrome + 1.3M Edge) intercepting conversations from **ten AI platforms including ChatGPT, Claude, Gemini, Copilot and Perplexity** — capturing prompts and responses before they render, no opt-out, added silently in **v5.5.0 on 9 July 2025**, flowing to **Urban Cyber Security Inc., affiliated with the data broker BiScience**. A single party holds one person's traffic across all five providers today, with no subpoena and no cloud-level access.

Second: **Couture v. OpenAI Global LLC**, No. 3:26-cv-03000-H-GC (S.D. Cal., filed **13 May 2026**) alleges — with packet captures dated 28 April 2026 — that chatgpt.com shipped **conversation titles** plus Facebook IDs (`c_user`) and `fr`/`_fbp` cookies to **Meta's Pixel**, and titles plus **hashed email** and Google profile ID (`Secure-3PSID`) to **Google Analytics**. *(Untested allegations.)* The adjacent fact I verified myself: `gemini.google.com`'s CSP permits `googleadservices.com`, `googleads.g.doubleclick.net`, `bid.g.doubleclick.net` and `pagead2.googlesyndication.com` across `script-src`, `connect-src` and `frame-src`. An allowlist proves permission, not execution — but on a Google property the distinction is thin.

Third: **memory became an ad input.** OpenAI published **"Dreaming: Better memory for a more helpful ChatGPT"** on **4 June 2026** — background consolidation building **narrative prose dossiers** (work, hobbies, travel, education) between sessions. **Ads shipped 9 Feb 2026** on US free and Go tiers, targeted on **conversation topic, past chats, and prior ad interactions**. The clearest statement of stakes is OpenAI's own EU policy (14 Aug 2026): **consented** personalized ads may use personal data, ad history and interests; **non-consented** contextual ads are limited to the live conversation and rough location and **explicitly exclude chat history and memory**. The industry has already conceded that memory-as-ad-input needs affirmative consent.

Against that: **Gemini's** Keep Activity is on by default, **18-month** retention, **72 hours even when off**, and **human-reviewed chats kept up to 3 years, disconnected from the account and unaffected by deletion**. **Anthropic's** 28 Aug 2025 consumer terms give **5-year** retention if you allow training, 30 days if not (Free/Pro/Max only). The one good precedent: **Claude's memory is project-scoped** — "each project has its own separate memory" — exactly the per-scope architecture we want, shipped by a frontier lab.

The legal arc matters too: the NYT preservation order (Judge Ona Wang, **13 May 2025**) was **terminated in October 2025**, then superseded by a **5 Jan 2026** order to produce **20 million de-identified conversations** to an adverse litigant. A retention order became a disclosure order — and de-identification of full conversation text is precisely the guarantee that does not hold.

---

## 8. Sequencing

**Tier 1 — do first. Cryptographic, zero utility cost, nobody does it for frontier models.**

1. **Blind-signature access tokens** (RFC 9474 type `0x0002`, or VOPRF `0x0001` for size). Kagi's shipped implementation is the template. Weeks against a known-good spec. Closes channel 4 outright.
2. **OHTTP transport** (RFC 9458) with a third-party relay — Fastly and Cloudflare both sell this and already run it for Apple, Google, Mozilla and Meta. Closes channel 6's IP component and most of 9. *Design note: Cloudflare already fronts seven of these endpoints, so the relay operator must not be the upstream edge — Meta's use of Fastly for both relay and key-config distribution is the pattern to copy.*
3. **Voucher-based payment.** Flat-rate prepaid codes through a merchant of record — Mullvad's model, which works precisely because it sells time, not metered usage. Sidesteps the MSB question and the unsolved metering crypto entirely.
4. **Response padding / constant-rate streaming.** Mandatory, not optional: Weiss and Whisper Leak make the streaming channel a content leak that OHTTP explicitly does not cover.
5. **Ship a native client, not a browser extension, and pin one TLS profile.** The BiScience finding makes the page itself a live exfiltration path across all five providers; a native app removes an entire adversary class for almost no engineering. Uniformity beats randomization — Brave sunset its own Strict mode because **<0.5%** adoption made those users *more* identifiable.

**Tier 2 — real cost, real benefit.**

6. **Local quasi-identifier pass** — adversary-in-the-loop rewriting on device, not a PII list. This is where the profiling power lives. Expect meaningful utility cost; spend it per-session against a risk budget, not blanket.
7. **Timing decorrelation** — decouple compose from dispatch, jitter, batch. Cheap to build; deliberate latency is the real price.
8. **Memory abstinence by default**, with our own memory held locally and injected per scope — and adopt Claude's **project-scoped** shape rather than a global dossier.

**Tier 3 — last, and only as an option.** Style obfuscation, offered per-session for high-risk use. §2 is the argument.

**Not worth building.** Mixnets (p99 and the always-on bandwidth floor). FHE/MPC for proprietary weights. Word-level DP rewriting. Post-quantum Privacy Pass at 85–175 KB/token. Anonymous *metered* credit until ACT or SMA2RT standardizes — take the flat-rate voucher shortcut.

**Two constraints to design around, not through.** Anthropic's commercial terms prohibit reselling without approval. And an anonymity set is only as large as the paying subscriber base — the privacy story and the growth story are the same story.

---

### Confidence notes
Verified directly this session: the Cloudflare edge measurements; Kagi, Brave, Mullvad, Proton, DuckDuckGo and Meta Private Processing primary docs; the Gemini CSP; Anthropic's phone requirement, memory rollout and consumer-terms dates; RFC and arXiv contents. **Secondary-sourced and flagged:** all OpenAI facts (openai.com 403s our fetcher) — Dreaming, the ads rollout, the EU consent policy, phone/ID verification, and the NYT order timeline. **Allegations, untested:** Couture v. OpenAI. **Known-stale:** Mullvad's 555,541-account figure and Brave's 120M MAU carry no as-of date.
