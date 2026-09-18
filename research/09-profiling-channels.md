# The profiling channels — complete enumeration and state of the art (2026-09-18)

**Scope.** A user wants frontier-model capability with it *structurally impossible* for any provider or coalition to profile them. Our current design (reversible PII tokenization, local vault) closes one channel. This enumerates all ten, gives the state of the art for each, and says what is honestly achievable.

Companion to `06-research-frontier.md` (which surveys the anonymization/linkage literature). This document is organised by **channel**, adds the **deployed-systems** comparison, and ends with **sequencing**. New primary findings in this document: Meta's WhatsApp Private Processing v2 whitepaper, live measurement of who fronts the AI APIs, Kagi's shipped Privacy Pass, and prompt-level stylometry numbers.

---

## 1. Master table

| # | Channel | How a profile gets built | State-of-the-art defence | Maturity | Cost (eng / utility / UX) | Who has done it |
|---|---|---|---|---|---|---|
| 1 | **Content PII** | Names, IDs, addresses in the prompt | Reversible format-preserving tokenization, local vault | **Shipped** (ours, Anonproxy, Presidio, SurrogateShield) | Low / low / low | Us; many |
| 2 | **Quasi-identifiers + semantics** | LLM infers location/age/income/employer from free text | Local **adversarial anonymization** (adversary-in-the-loop rewrite), not PII lists | **Research→early product** | Med / **high** / med | Nobody in production |
| 3 | **Writing style** | Authorship attribution / cross-session linkage | Style-aware LLM paraphrase; aggregation-aware rewriting | **Research** | Med / **high** / high | Nobody |
| 4 | **Account / auth** | API key, login, phone, gov ID | **Blind-signature / VOPRF tokens** (Privacy Pass RFC 9576–9578, RFC 9474) | **Deployed elsewhere** | Med / **zero** / low | Apple PCC, Apple PAT, Meta ACS, Kagi, Brave |
| 5 | **Payment** | Card in your name → usage | Vouchers / x402 / Lightning; **ACT** anonymous credit tokens for metering | **Deployed (flat-rate)**, prototype (metered) | Med / zero / med | Mullvad, Venice, Maple AI |
| 6 | **Network metadata** | IP, TLS FP, packet sizes, cadence | **OHTTP (RFC 9458)** + constant-rate response padding | **Deployed** | Med / zero / low | Apple PCC, Meta, Chrome SB, Firefox |
| 7 | **Device / client FP** | JA4 TLS, HTTP/2 settings, header order, UA | Uniform client profile (Tor Browser model), single pinned TLS stack | **Deployed** (browsers) | **Low** / zero / low | Tor Browser, Brave |
| 8 | **Timing / behaviour** | Circadian rhythm, session cadence, typing | Queue + jitter, batch dispatch, decouple send from compose | **Research** | Low / zero / **med** | Nym (at heavy cost) |
| 9 | **Cross-service join** | One party sees traffic to several providers | Per-provider egress diversity; OHTTP with distinct relays | **Partially deployable** | Med / zero / low | Nobody |
| 10 | **Provider memory** | Persistent profile the provider builds for you | Don't use it; per-scope pseudonymous memory held locally | **Shipped** (opt-out) | Low / **high** / high | Us (locally) |

---

## 2. Deep dive — stylometry

**The attack, at scale.** The anchor numbers span fourteen years. Narayanan et al. (IEEE S&P 2012, 100,000 blogs, 2.4M posts, style-only features by construction) get **~20% top-1** and ~35% top-20 from ~900 words, and crucially **>80% precision at 50% recall** once the attacker is allowed to abstain; the median case narrows 100,000 candidates to **100–200**. Accuracy falls roughly **10–13 points per decade of pool size** (DeepStyle: P@1 64.8% at 50 users → 21.4% at 7,026). Length matters as much as pool: AuthBench (arXiv [2609.06771](https://arxiv.org/abs/2609.06771), 153,825 authors) reports verification EER **0.104 for 1–10-token texts → 0.048 above 500 tokens**.

**Prompts specifically.** This was a literature gap until 2026. **PromptPrint** (arXiv [2606.06755](https://arxiv.org/abs/2606.06755)) uses **20,680 real prompts from 1,034 users**, 20 prompts each: **64.2% top-1** / 79.3% top-5 across the full 1,034-user gallery; 76.9% at 100 users, 62.3% at 1,034. Performance plateaus at **N=10 prompts**. Synonym substitution at 20% costs the attacker **0.1 points**; full semantic paraphrase drops top-1 to **42.9%** and pushes EER from 0.421 to 0.703. So: prompts are identifying, ten of them suffice, and only rewriting that changes meaning-bearing choices helps.

**But style is the weaker channel.** SALA (arXiv [2602.23079](https://arxiv.org/abs/2602.23079)) shows zero-shot **open-world** candidate search finds the true author in only **1.2%** of 20-candidate shortlists — but **78.1%** when the attacker has a warm candidate database. A provider holding every user's history is in the database-augmented regime by default. And Lermen et al. (USENIX Sec 2026, arXiv [2602.16800](https://arxiv.org/abs/2602.16800)) show that what actually links sessions is **content**: 55.2% recall at 90% precision against 89,000 candidates, extrapolating to **~27% at 100M candidates**, at **$1–4 per target**. Aggregation dominates everything: AAST (arXiv [2608.22161](https://arxiv.org/abs/2608.22161)) finds unprotected Reddit text reaches **100 R@8 at K=8** bundled messages under LUAR.

**Does obfuscation work? Measured cost, then the catch.**

| System | Attribution drop | Utility cost |
|---|---|---|
| Mutant-X (PoPETs 2019) | 59–64% on EBG | METEOR **0.54–0.55** (≈half the surface overlap gone) |
| TAROT-DPO (EMNLP-F 2024) | 99.8% → **17.3%** | downstream utility 79.5 → 60.7 (**−19 pts**) |
| "I Am No One" (Interspeech 2026, [2609.12341](https://arxiv.org/abs/2609.12341)) | F1 66.45 → **26.02** | **perplexity preserved** (42.5 vs 41.0) |
| ALISON | acc → 0.31–0.58 | METEOR worst-in-class, but USE cosine 0.969 |
| Word-level DP, ε=6 | MCC 0.98 → 0.12 (static) | GPT-2 PPL **44.5 → 5,003** — destroyed |

Three catches, all load-bearing. **(a) Adaptive attackers recover most of it.** Zhai et al. (ACL 2022) retrain the attributor on obfuscated text: Mutant-X's effect collapses from −32 points to **−5 points**. Mattern et al. (NAACL-F 2022): word-level DP at ε=6 leaves author MCC at **0.58 adaptive** versus 0.12 static; at ε=12, **0.95**. Only *generation*-based obfuscation (TAROT) has been shown to survive retraining, in one paper. **(b) Obfuscation is itself detectable** at **F1 0.87** (arXiv [2005.00702](https://arxiv.org/abs/2005.00702)) — in a provider threat model, "this user obfuscates" is itself a durable label. **(c) PAN abandoned the task after 2018** precisely because no submission was ever simultaneously safe, sound and sensible; the organizers' own summary is that approaches are "somewhat safe but… unreadable" or "sound and sensible… but not safe."

**Verdict.** Style obfuscation is the worst privacy-per-unit-cost item on the list. It is expensive, it damages the text, it partially fails against a retraining adversary, it announces itself, and the channel it closes is weaker than the content channel sitting right next to it.

---

## 3. Deep dive — anonymous authentication

**The cryptography is finished and deployed — just not by AI labs.**

- **Privacy Pass**: RFC **9576** (architecture), **9577** (HTTP `PrivateToken` scheme), **9578** (issuance), all June 2024. Two token types: `0x0001` VOPRF(P-384) — 48-byte authenticator, privately verifiable; `0x0002` blind RSA-2048 (**RFC 9474**) — 256-byte authenticator, publicly verifiable. VOPRF itself is **RFC 9497**.
- **Apple Private Access Tokens** (iOS 16+/macOS Ventura+, June 2022): iCloud is the attester, **Cloudflare or Fastly the issuer**, the site the origin. Cloudflare reports **>65%** of its customers already run the prerequisite Managed Challenge. This is blind-signature anonymous auth at hundreds of millions of devices.
- **Apple Private Cloud Compute authorizes LLM inference with RSA blind signatures** plus a third-party OHTTP relay. That is anonymous authentication to a frontier-class model, in production. It is simply not exposed as an API.
- **Meta's Anonymous Credential Service** — VOPRF + blind signatures + KDFs, with attributes; **open source** at `github.com/facebookresearch/acs`; deployed at Meta scale and now gating WhatsApp's AI features. Credentials are usable "a finite number of times," which is how rate limiting survives anonymity.
- **Kagi Privacy Pass** (shipped **13 Feb 2025**, blog.kagi.com/kagi-privacy-pass) is the closest commercial analogue: RFC 9576–9578, shared origin/attester/issuer, **216-byte single-use tokens**, **2,000–3,000/month** per account, **~1 second to mint 500**, expiring at the end of the following month. Kagi can no longer link a search to an account. Brave issues **unlinkable tokens** for Leo Premium on the same family of primitives.

**The unsolved piece is metered spend.** `draft-ietf-privacypass-rate-limit-tokens` **expired**. The current answer is Cloudflare's October 2025 work ([blog.cloudflare.com/private-rate-limiting](https://blog.cloudflare.com/private-rate-limiting), framed explicitly around AI agents): **ARC** issues one credential good for 1,000 unlinkable presentations in **1.35 ms**, 288-byte presentations, ~70× faster than batching VOPRF tokens; **ACT** is a *stateful* credential carrying a credit balance proven in zero knowledge by range proof — **251 µs issuance, 1,867-byte presentation** — decremented per request in proportion to resources consumed, and revocable. `draft-meunier-privacypass-reverse-flow-07` adds refunds for cheap requests. Academic frontier: SMA2RT (CRYPTO 2026, eprint 2026/518) names *metered paywalls* as a target. Post-quantum variants cost **85–175 KB per token** — unaffordable.

**What the labs actually require.** Anthropic's own help centre states that a text-capable, **non-VoIP** phone number is mandatory at signup and "there isn't a way to skip this step." OpenAI requires phone verification for a first API key and **government ID via Persona** for top models (one org per ID per 90 days). No statute requires this — the EU AI Act's Art. 50 is a *disclosure* duty running provider→user, and an inference seller is a merchant, not a money transmitter. This is abuse-control policy, and OpenAI says so. **Practical constraint:** Anthropic's commercial terms forbid reselling "except as expressly approved," which is the real blocker on a pooled-account intermediary, not law.

---

## 4. Deep dive — network metadata

**The LLM-specific side channel is real and mostly unmitigated.** Weiss, Ayzenshteyn, Amit & Mirsky (USENIX Security 2024, [usenix.org/conference/usenixsecurity24/presentation/weiss](https://www.usenix.org/conference/usenixsecurity24/presentation/weiss)) exploit the **token-length side channel**: streamed responses emit one chunk per token, so an eavesdropper reads a sequence of token lengths and reconstructs **27% of responses** and infers the **topic of 53%** (arXiv preprint reports 29%/55%), against ChatGPT-4 and Copilot, browser *and* API traffic. **Whisper Leak** (arXiv [2511.03675](https://arxiv.org/abs/2511.03675), Nov 2025) generalises it to packet size *and* timing across **28 models**, hitting **>98% AUPRC** topic classification and 100% precision on some sensitive topics even at a **10,000:1** noise ratio — and finds that random padding, token batching and packet injection each leave gaps. Server-side cousins exist too: KV- and semantic-cache timing recovers other users' prompts (*Early Bird*, arXiv [2409.20002](https://arxiv.org/abs/2409.20002); *InputSnatch*, [2411.18191](https://arxiv.org/abs/2411.18191)).

**Transport.** OHTTP (**RFC 9458**, Thomson/Mozilla & Wood/Cloudflare, Jan 2024) splits the relay (sees IP, not content) from the gateway (sees content, not IP) and is genuinely deployed: Apple PCC, Chrome Safe Browsing (Fastly relay), Firefox telemetry, Flo Health, and **WhatsApp Private Processing** (Fastly relay). Its security considerations are explicit that it does **not** defend against relay–gateway collusion or **traffic analysis by timing and size** — which is exactly the Weiss/Whisper channel. An API key inside the request re-links everything, which is why OHTTP only works *composed with* channel 4.

The heavier options don't fit interactive inference. Tor's design explicitly excludes a global passive adversary and its exits are widely blocked by API providers. Apple Private Relay is *easier* to correlate than Tor (DeepCorr **TPR 1.0 at FPR 10⁻³** on 350-packet flows) because it has no fixed cells or cover traffic. Nym's own defaults are **15 ms/hop, ~50 packets/s, ~1 Mbps of cover traffic whether idle or not**, with third-party p99 around **3 s** — the anonymity trilemma in product form.

**Device and client.** For a native client the surface is small and cheap to flatten: JA4/JA4+ TLS fingerprints, HTTP/2 SETTINGS and header order, UA. Browser-uniqueness numbers argue for the Tor Browser approach over randomization: Eckersley (2010) found **83.6%** unique, AmIUnique (2016) **89.4%**, but Gómez-Boix's large-scale study (WWW 2018) only **33.6%** overall and **18.5%** on mobile — uniformity at scale beats entropy-adding.

**Who can already join it all — measured today.** DNS and response headers for the major inference endpoints, fetched 2026-09-18:

| Endpoint | Edge |
|---|---|
| `api.openai.com`, `chatgpt.com` | `server: cloudflare`, `cf-ray` present |
| `api.anthropic.com`, `claude.ai` | `server: cloudflare`, `cf-ray` present |
| `api.mistral.ai`, `api.x.ai`, `api.together.xyz`, `api.groq.com`, `openrouter.ai` | `server: cloudflare`, `cf-ray` present |
| `generativelanguage.googleapis.com` | Google (`HTTPServer2`) |
| `api.deepseek.com` | AWS CloudFront |

**One commercial party terminates TLS for at least seven major providers, including all three of OpenAI, Anthropic and Mistral.** The cross-service join does not need a data broker or a subpoena; it needs a query against one edge network's logs. (I did not attempt to characterise third-party trackers on the web apps: `chatgpt.com` returned 403 and `claude.ai` served a Cloudflare challenge, so that check is inconclusive — and the challenge is itself further confirmation.)

---

## 5. Comparative study — who has actually built this

| System | Closes | Leaves open | Cost | Adoption |
|---|---|---|---|---|
| **Apple PCC** | Account (RSA blind sigs), IP (3rd-party OHTTP relay), retention (stateless, key randomized per reboot), code (transparency log, binaries public within 90 days) | **Content** — plaintext inside the enclave; stylometry; hardware-vendor collusion out of scope; routing to ChatGPT leaves the boundary | Custom silicon, VRE, bounty programme | Hundreds of millions of devices |
| **Meta WhatsApp Private Processing** (v2 whitepaper, 16 Mar 2026) | Account (**ACS**: VOPRF+blind sigs, finite-use), IP (**Fastly** relay, which *also* distributes ACS/OHTTP key configs so Meta can't key-target), compute (**AMD SEV-SNP** CVM + **H100 CC**), code (artifact transparency) | Content in the enclave; each CVM serves multiple users; "collusion with our hardware vendors… is out of scope" | Full CC stack, ~4–8% throughput overhead | WhatsApp scale |
| **Kagi Privacy Pass** | Payment↔usage link, account↔query link | IP, timing, query content (Kagi says so plainly) | ~1 s per 500 tokens, 216 B/request | Paid tiers, Feb 2025 |
| **Mullvad** | Identity entirely (random account number, cash by mail, Monero) | Everything above the VPN | Works only because it sells **flat-rate time, not metered usage** | Widely adopted |
| **Signal** | Content (E2EE), sender metadata (sealed sender), contacts (SGX CDS) | Sealed sender is **breakable in ~5 messages** via delivery-receipt timing (Martiny et al., NDSS 2021); registration still needs a phone number | **$14M/yr infra**, of which **$6M is registration fees**; ~$50M/yr projected | ~50 staff, global |
| **Tor** | IP | Explicitly **not** a global passive adversary; exits blocked by AI APIs | Latency; ~2.8–3.5M daily users | Niche |
| **Nym** | IP + traffic analysis | Unusable for streaming (~100 KB/s, p99 ~3 s) | 1 Mbps cover traffic always | Minimal |
| **DuckDuckGo Duck.ai** | IP (stripped before forwarding) | Content — protection is **contractual**: named providers (Anthropic, Azure OpenAI, OpenAI, together.ai), no-training, deletion "at most within 30 days" | Trivial | Broad |
| **Brave Leo** | Subscription↔usage (unlinkable tokens), IP (anonymizing servers), retention (discarded) | Content at the model provider | Low | ~tens of millions MAU |
| **Proton Lumo** | Stored history (zero-access encryption), no account required | **Inference itself** — the prompt is plaintext in Proton's datacenter; "zero-access" covers storage, not compute | Low | Proton base |
| **Venice.ai / Maple AI / Tinfoil** | Payment+account (x402 USDC, $5 min, **no account at all**; Maple: ID+password, BTC/Lightning, no email), compute (TEE + attestation) | On-chain wallet is a **permanent public pseudonym**; open-weights only for the attested tiers | 4–8% TEE overhead | Small |

Two observations. First, the **existence proof is complete**: Apple and Meta have both shipped anonymous-credential + oblivious-transport + attested-compute for LLM workloads. Second, **not one of them closes the content channel**, and neither does any research system — because a hosted frontier model must read the prompt. PCC's own reverse-engineering (WiSec 2026, arXiv [2605.24239](https://arxiv.org/abs/2605.24239)) also found the one shipped "unlinkable" system has a linkability bug: the one-time-token nonce is `SHA256(TGT‖OTTSalt)`, OTTs replayed **2–5 times**, and TGT signature validation was **disabled in production**.

---

## 6. What "non-profiling" can honestly mean in 2026

**"Structurally impossible to profile" is not achievable and should not be claimed.** Three reasons, in order of severity:

1. **The model must read the prompt.** Everything identifying survives into the model's context. TEEs move the trust from "the provider promises" to "AMD/NVIDIA/Apple silicon plus an attestation chain" — a real upgrade, at 4–8% throughput and 20–28% TTFT — but every vendor declares physical attacks out of scope, and 2025–26 produced working attestation forgeries at hobbyist cost. FHE and MPC are 10³–10⁴× off and only for open weights.
2. **The content channel is the strong one and it has no defence.** Lermen et al. link the same person across a **one-year gap** at 90% precision and deanonymize a third of users at **99%** precision, scaling to ~27% recall at 100M candidates for $1–4 each. Staab's five-round adversarial rewrite — far more destructive than tokenization — still leaves **41.6%** attribute inference. Azure's commercial PII removal leaves **74%** of information inferable on clinical text and moves WildChat re-identification only 40.5% → 17.7%.
3. **Per-provider pseudonym rotation buys nothing against this.** The surrogate is not the linkage channel; topic, expertise, recurring projects and cadence are.

**The honest claim, which is still strong and which nobody offers today:**

> *No provider, and no coalition of providers, can link your requests to your identity, to your payment, or to each other — because the account credential is a blind signature, the payment is unlinkable to the spend, and the network path is oblivious. What you write still reaches the model; we measure that residual risk before it leaves and tell you what it carries.*

That is four channels closed **cryptographically and structurally** (4, 5, 6, 9), two closed **cheaply and completely** (7, 10), one closed **mechanically** (1), and three closed **only partially and measurably** (2, 3, 8). Say exactly that. The difference between "we promise" and "we cannot" is the product; pretending it extends to the content channel is the thing that will get us taken apart in diligence.

---

## 7. Sequencing

Ordered by privacy gained per unit of engineering and user friction.

**Tier 1 — do first. Cryptographic, zero utility cost, nobody has done it for frontier models.**

1. **Blind-signature access tokens** (RFC 9474 type `0x0002`, or VOPRF `0x0001` for size). Kagi's shipped implementation is the template: mint in the background, 216-byte tokens, monthly cap. Weeks of work against a known-good spec. Closes channel 4 outright.
2. **OHTTP transport** (RFC 9458) with a third-party relay — Fastly and Cloudflare both sell this, and both already run it for Apple, Google, Mozilla and Meta. Closes channel 6's IP component and, with distinct relays per provider, most of channel 9. *Note the irony to design around: Cloudflare already fronts seven of the endpoints, so pick a relay operator that is not also the upstream edge.*
3. **Voucher-based payment.** Flat-rate prepaid codes sold through a merchant of record — Mullvad's model, which works precisely because it sells time, not metered usage. Sidesteps the MSB question and the unsolved metering crypto.
4. **Response padding / constant-rate streaming.** Mandatory, not optional: Weiss and Whisper Leak make the streaming channel a content leak that OHTTP explicitly does not cover. Small latency cost, no utility cost.
5. **Client uniformity.** One pinned TLS stack, fixed JA4, fixed header order, fixed UA, no locale leakage. Nearly free; the Tor Browser lesson is uniformity beats randomization.

**Tier 2 — do next. Real cost, real benefit.**

6. **Local quasi-identifier pass** — adversary-in-the-loop rewriting on-device, not a PII list. This is where the actual profiling power lives. Expect meaningful utility cost and accept it selectively (per-session risk budget, not blanket).
7. **Timing decorrelation** — decouple compose from dispatch, jitter, batch. Cheap engineering; the UX cost of deliberate latency is the real price.
8. **Memory abstinence by default** — provider memory off, temporary/incognito chat on, our own memory held locally and injected per scope. Gemini Apps Activity is on by default with 18-month retention (72 h even when off, human-reviewed chats kept **3 years** disconnected from the account); Anthropic's consumer terms since 28 Aug 2025 mean 5-year retention if training is allowed, 30 days if not.

**Tier 3 — last, and only as an option.**

9. **Style obfuscation**, offered per-session for high-risk use. Section 2 is the argument: expensive, damages the text, partly defeated by retraining, and detectable as obfuscation.

**Not worth building.** Mixnets (bandwidth and p99 incompatible with streaming). FHE/MPC for proprietary weights. Word-level DP rewriting (ε values that aren't DP ε, 72–94% reconstruction where utility survives). Post-quantum Privacy Pass (85–175 KB/token). Anonymous *metered* credit until ACT or SMA2RT lands in a standard — take the flat-rate voucher shortcut instead.

**Two constraints to design around, not through.** Anthropic's commercial terms prohibit reselling without approval, so a pooled-account intermediary needs a partnership, not a clever proxy. And an anonymity set is only as large as the paying subscriber base — the honest claim scales with adoption, which means the privacy story and the growth story are the same story.
