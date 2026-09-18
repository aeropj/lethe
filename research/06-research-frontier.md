# What the research actually says — survey, 2026-09-18

Two findings below invalidate parts of the plan. Read §3 first.

# Lethe: What the Research Actually Says

*Survey, 2026-09-18. Numbers read from fetched sources (PDFs text-extracted locally). Claims I could not verify are marked.*

---

## 1. Anonymization vs utility — the hard numbers

**Deußer et al. 2026** ([arXiv:2609.11335](https://arxiv.org/abs/2609.11335)), 5 models × 11 benchmarks. Average degradation: **Qwen2.5-72B −6.9pp, Teuken-7B −2.3pp**. Most tasks drop <5pp. Two outliers: **RGB (retrieval) collapses 0.80→0.32 for GPT-4o-mini (−48pp), 0.82→0.38 for Qwen (−44pp)**; TruthfulQA *improves* (+8pp Llama-3.1-8B). MMLU-PRO −8 to −10pp. Reversible schemes beat irreversible: on MUSR, pseudonymization 0.70 vs redaction 0.52, generalization 0.58.

**Read the methodology before you cite this.** Their "pseudonymization" is `<LOC>-1` tags, not realistic surrogates. Their own ARC example replaces *Earth* and *Sun* with `<LOC>-1`/`<LOC>-2` and flips a correct answer to wrong. Much of the headline cost is over-redaction of non-personal entities plus tag tokenization — **not** an inherent cost of surrogate substitution. This supports your design choice, and it also means the paper is weaker evidence for "anonymization costs capability" than it appears.

**PAPILLON/PUPA** (NAACL 2025, [arXiv:2410.17127](https://arxiv.org/abs/2410.17127), [ACL](https://aclanthology.org/2025.naacl-long.173/)). 901 WildChat turns, 2.86–3.01 PII units/query. GPT-4o-mini unredacted: **88.2% quality / 100% leakage**. Naive redaction: **77.2% / 0%**. Optimized PAPILLON (Llama-3.1-8B local + GPT-4o-mini): **85.5% / 7.5%**. So redaction costs **11pp of quality**, and the best local-remote pipeline recovers 8 of those 11 points but **still leaks PII on 7.5% of queries**.

**Yermilov et al.** (TrustNLP 2023, [arXiv:2306.05561](https://arxiv.org/abs/2306.05561)) is the cleanest task split: classification is nearly free (F 88.42→87.65–88.15), generation is not (**ROUGE-L 36.33→27.43–29.36**, a 19–25% relative loss).

**HaS** ([arXiv:2309.03057](https://arxiv.org/abs/2309.03057)): classification −0.24 to −1.16% F1; translation **−0.85 to −5.65% METEOR**. **Casper** ([arXiv:2408.07004](https://arxiv.org/abs/2408.07004)): 98.5% PII detection, 89.9% topic identification, **14.7% performance overhead**. **Tau-Eval** ([arXiv:2506.05979](https://arxiv.org/abs/2506.05979)) shows the frontier directly: Presidio preserves downstream tasks almost perfectly (95.1 vs 95.2, 77.5 vs 77.6) but scores only 66.4 on privacy; LLM rewriters hit 95–99 privacy while dropping downstream tasks to 41–57.

**SurrogateShield** ([arXiv:2606.29567](https://arxiv.org/abs/2606.29567), June 2026) is your mechanism, already published: client-side proxy, 22 PII types, AES-256-GCM local vault ("ShadowMap"), realistic surrogates, local re-identification of the response. **98.87% detection F1; BERTScore 94.85% vs 81.59% for placeholder redaction (+13.26pp)**. Read its limitations section — it concedes exactly what the attack literature shows matters: no defence against contextual/implicit identity, no traffic analysis, no unlinkability, synthetic corpus only.

**2026 work recovering the loss:** **AURA** ([arXiv:2605.30848](https://arxiv.org/abs/2605.30848)) retains **74.9–80.3%** unit-level utility at 0–5/27 re-identification. **SEAL** ([arXiv:2506.01420](https://arxiv.org/abs/2506.01420)) distils GPT-4-grade anonymization into **8B local models**. **IntentAnony** ([arXiv:2601.04265](https://arxiv.org/abs/2601.04265)) claims **+30%** on the joint frontier.

**Gap worth owning: nobody has measured realistic-surrogate substitution on standard capability benchmarks.** Deußer measured tags; SurrogateShield measured BERTScore on synthetic queries. That experiment is unrun.

---

## 2. Attribute inference and re-identification — the attack side

**Staab et al., "Beyond Memorization"** (ICLR 2024, [arXiv:2310.07298](https://arxiv.org/abs/2310.07298)). 520 Reddit profiles, 5,814 comments, 1,066 labels. GPT-4: **85% top-1 / 95% top-3**, at **100× lower cost and 240× faster** than humans. The number that matters for you: **after Azure Language Service anonymization, GPT-4 still infers at 43.9–64.2%** by hardness tier.

**Staab et al., "LLMs are Advanced Anonymizers"** (ICLR 2025, [arXiv:2402.13846](https://arxiv.org/abs/2402.13846)). Adversarial loop: **86.7% → 66.3% (round 1) → ~50% → 45.3% → 41.6% (round 5)**. Azure alone only reaches 66.3%, with human-rated readability 0.38 vs 0.89. **After five rounds of full LLM rewriting, 41.6% of attributes are still inferable.** The authors state guarantees against arbitrary adversaries "has proven to be difficult."

**RAT-Bench** (Krčo, Yao, Meeus, de Montjoye, [arXiv:2602.12806](https://arxiv.org/abs/2602.12806)) is the most damaging single table. Re-identification success rate after anonymization, explicit identifiers (easy/hard/avg) and implicit:

| Tool | Easy | Hard | Avg | Implicit |
|---|---|---|---|---|
| No anonymization | 100% | 98% | 99% | 32% |
| **Presidio** | 41% | 77% | **59%** | **30%** |
| Azure | 22% | 33% | 28% | 21% |
| GPT-4.1 + Anthropic PII-purifier | 26% | 58% | 42% | 19% |
| Staab iterative, *ideal* attribute list | 2% | 18% | — | 18% |
| Staab iterative, Presidio attribute list | 56% | 84% | — | 26% |

The regulatory threshold they cite is **5%**. Nothing reaches it. And the iterative anonymizer only works if you already know exactly which attributes matter — with a generic list it degrades to Presidio.

**Profiling for Pennies** ([arXiv:2605.06232](https://arxiv.org/abs/2605.06232)): IcebergExplorer on 30 consenting real participants, **93.05% fact accuracy, ~10 minutes, under $3 per target, 0% refusal rate**.

**RedactionBench** ([arXiv:2606.18782](https://arxiv.org/abs/2606.18782)): best agentic frontier LLM **R-Score 0.71** (0.81 on the user-study split vs **0.77** human baseline); best BERT-NER 0.58. Human annotators agree on mandatory redactions 89.4% and safe preservations 94.1% but **only 47.7% on contextual redactions** — "what is sensitive" is not a well-defined target.

**And users cannot do it themselves.** [arXiv:2509.12152](https://arxiv.org/abs/2509.12152), 240 US participants: they predicted which attributes an LLM could infer **only slightly above chance**, and their rewrites were less effective than ChatGPT's.

**Implication: entity replacement is necessary and provably insufficient.** Presidio leaves 59% re-identification risk. The best available rewriting leaves 41.6% attribute inference. This is not a tuning problem.

---

## 3. Unlinkability — your key question

**The answer is that the literature says no, and the measurement is recent and specific.**

**Lermen, Paleka, Swanson, Aerni, Carlini, Tramèr, "Large-scale online deanonymization with LLMs"** ([arXiv:2602.16800](https://arxiv.org/abs/2602.16800)) builds exactly your threat model: two sets of pseudonymous profiles containing only unstructured text, match them.

- **LinkedIn ↔ Hacker News** (direct identifiers stripped): **54.2% recall @ 90% precision, 45.1% @ 99%**. The Netflix-Prize-style classical baseline: **0.1%**.
- **Same-person temporal split on Reddit** — one profile before, one after, a **one-year window deleted** so no shared current events: full attack recovers most users at 90% precision and **deanonymizes a third of all users at 99% precision**. This is the account-rotation scenario.
- **Scaling:** 68.3% recall at 1k candidates, 55.2% at 89k; extrapolated **~35–45% at 1M candidates, ~27% at 100M**, all at 90% precision.
- **Even when almost nobody is linkable:** at π = 0.0001 (1-in-10,000 prior of a match existing), the attack holds **≥9% recall at 90% precision**.
- **Cost: $1–$4 per deanonymization; the whole paper cost under $2,000.**
- Topic-only signal, no micro-data (Reddit movie reviews): 8.5% @ 90% precision, rising to **48.1% for users sharing 10+ movies**.

The authors honestly flag that their 67%-of-338 Hacker News figure is biased upward because those profiles are "much easier to identify than most pseudonymous accounts."

**Pure stylometry is the weaker channel.** **SALA** (CISPA, [arXiv:2602.23079](https://arxiv.org/abs/2602.23079)) on news articles: zero-shot open-world F1 **0.000–0.068**; with a candidate database and 500 samples per candidate, **F1 0.827 (1 target) / 0.595 (3 targets)**. Style needs a candidate set. **Topic and micro-data do not.**

**Obfuscation works but costs the text.** "I Am No One" ([arXiv:2609.12341](https://arxiv.org/abs/2609.12341), Sept 2026): baseline authorship F1 66.45 (10 authors) / 76.78 (9 authors) → best style-aware LLM rewrite **26.02 / 20.76 with perplexity preserved (42.47 vs 41 original)**. ALISON gets F1 29.53 but PPL **368.30**. Strict DP (ε=25) gets F1 7.13 at PPL **8,770** — unreadable. Generic paraphrasing barely helps (F1 53.10).

**Two structural results say this cannot be patched at the metadata layer.** The **anonymity trilemma** (Das, Meiser, Mohammadi, Kate, IEEE S&P 2018, [eprint 2017/954](https://eprint.iacr.org/2017/954)): strong anonymity, low bandwidth, low latency — pick two. And statistical disclosure / intersection attacks ([arXiv:1910.07603](https://arxiv.org/abs/1910.07603)) show persistent behaviour defeats per-session pseudonyms by accumulation.

**Direct answer: rotating surrogates per provider buys you nothing against linkage.** The surrogate is not the linkage channel. Topic distribution, expertise, project specifics, recurring entities-by-description, and timing are. The measured attack achieves 90%-precision linkage across a one-year gap at $1–4 per target, and it scales to 100M candidates at ~27% recall.

**Two gaps I confirmed by search, not by finding papers: there is no published unlinkability metric for text, and no published defence against LLM-driven cross-session linkage.** Searches for both returned nothing on point. That is a research-shaped hole.

---

## 4. Cryptographic and systems approaches

**FHE.** Frontier is **Cerium** ([arXiv:2512.11269](https://arxiv.org/abs/2512.11269)): BERT-base/128 tokens in **8.8 s on 8×B200**; **Llama3-8B, 128-token prompt, first token only: 134 s on 8×B200 / 675 s on 1×A100**. That is ~10⁴× plaintext. NEXUS (NDSS 2025, [eprint 2024/136](https://eprint.iacr.org/2024/136)) reports 51.84 s for Llama-3-8B on 4×A100 but **amortized over 32 batched inputs**; THOR ([eprint 2024/1881](https://eprint.iacr.org/2024/1881)) estimates the unamortized figure at ~2.7 hours. AEGIS ([arXiv:2604.03425](https://arxiv.org/abs/2604.03425)): BERT-base at 2048 tokens needs **>700 GB of encoded weights**. Euston (IEEE S&P 2026) was cryptographically broken this year. Nothing above 8B.

**MPC.** SIGMA (PoPETs 2024): Llama2-13B **37.59 s and 18.90 GB per inference**, plus **419 GB of FSS key material** taking 356 s to transfer. PUMA: LLaMA-7B **200 s / 1.79 GB**. The 2026 breakthrough — Gupta, Katz & Miers ([eprint 2026/1849](https://eprint.iacr.org/2026/1849)) — hits **Llama-2-70B at 5.21 s/token, 135.62 MB/token**, but **only for open weights**. A Sept-2026 SoK ([eprint 2026/2005](https://eprint.iacr.org/2026/2005)) finds that of 58 works, 25 evaluate BERT-base and **only 6 reach billion-parameter models**.

**PIR is solved.** **SandwichPIR** ([eprint 2026/1816](https://eprint.iacr.org/2026/1816)): 4 GB DB in **8.2 ms with 688 KB**, English Wikipedia at **2,500 queries/s/GPU, $0.20 per million queries**. Private *top-k over embeddings* is not: Tiptoe runs **~190× plaintext at recall@10 of 0.11–0.28**.

**Split inference is dead as a privacy technology.** Transformer hidden states are provably injective ([arXiv:2510.15511](https://arxiv.org/abs/2510.15511)) — zero collisions across billions of tests, exact text recovered in linear time. "Depth Gives a False Sense of Privacy" (USENIX Security 2025, [arXiv:2507.16372](https://arxiv.org/abs/2507.16372)): a **4,112-token medical prompt recovered at 86.88 F1 from a middle Llama-3 layer**; **DP at ε = 5,000 still leaks**.

**TEEs are the only thing that works today.** H100 confidential computing ([arXiv:2409.03992](https://arxiv.org/abs/2409.03992)): **Llama-3.1-8B 6.85%, Phi-3-14B 4.58%** throughput overhead; TTFT is the real cost at **19–26%**. NVIDIA's Blackwell numbers (July 2026): **−1% to −8%** on a 397B MoE. Intel TDX: 5.51–10.68% single-socket, 12.11–23.81% dual ([arXiv:2509.18886](https://arxiv.org/abs/2509.18886)).

**But the TEE threat model broke physically in 2025–26.** **Battering RAM** (IEEE S&P 2026, **$47.62 of parts**, [batteringram.eu](https://batteringram.eu/)) forges SGX and SEV-SNP attestation. **WireTap** (CCS 2025, <$1,000, [wiretap.fail](https://wiretap.fail/)) extracts the SGX Quoting Enclave ECDSA key. **TEE.Fail** ([tee.fail](https://tee.fail/)) extends this to **Intel TDX, SEV-SNP, and NVIDIA CC on H100/H200 and B100/B200**. All three vendors declare physical attacks out of scope.

**Apple PCC.** Apple's own attack analysis concedes node homogeneity, geographic leakage via the relay, that **external tool calls are exposed to the tool gateway and provider**, and that **"it is not possible to prove that the published PCC binaries are compiled from the published source code."** As of June 2026 PCC runs on Google Cloud with TDX and NVIDIA CC — inheriting exactly the broken model.

**And the one shipped unlinkable-inference system has a linkability bug.** *Unlocking Apple's Private Cloud Compute* (WiSec 2026, [arXiv:2605.24239](https://arxiv.org/abs/2605.24239)) — PCC's central claim is that "user input and user accounts are unlinkable." The reverse-engineering found the one-time token nonce is `SHA256(TGT‖OTTSalt)`, so **tokens can be linked back to the ticket**; OTTs replay 2–5 times; **TGT signature validation is disabled in production**.

---

## 5. Metadata, authentication, payment

**OHTTP (RFC 9458)** hides client IP from the gateway and content from the relay. It explicitly does **not** cover traffic analysis, and an API key inside the request re-links everything. Non-collusion is normative. Deployed by Apple PCC via Cloudflare and Fastly. I found **no published end-to-end OHTTP latency benchmark**.

**Tor** (live Tor Metrics, fetched today): ~9,200–10,167 relays, **1.19–1.26 Tbit/s advertised**, 2.82–3.56M daily users; median TTFB **110 ms (DE) / 270 ms (US) / 530 ms (HK)**. Usable for streaming, but exit IPs are blocked by API providers.

**Private Relay is easier to correlate than Tor.** ASIA CCS '23 ([UMass PDF](https://people.cs.umass.edu/~amir/papers/AsiaCCS23-Private-Relay.pdf)): **DeepCorr TPR 1.0 at FPR 10⁻³** on 350-packet flows (vs 0.8 for Tor); website fingerprinting **96.5–99.2%** closed-world — no fixed cells, no cover traffic.

**Mixnets are incompatible with streaming.** Nym's own docs: **50 packets/s, ~100 KB/s ceiling, ~1 Mbps of cover traffic whether idle or not**, and explicitly unsuitable for streaming — though explicitly *good* at "calling APIs." Third-party latency: median 448 ms, **p99 3,026 ms**. The nearest research design is **funion** ([arXiv:2505.18398](https://arxiv.org/abs/2505.18398)) — store-compute-store over Echomix with quantized latency buckets, sender-receiver unlinkable — but it is a security analysis, not a deployment.

**Anonymous credentials are the mature piece.** Privacy Pass **RFC 9576/9577/9578** (June 2024), VOPRF **RFC 9497**. Cloudflare's **ARC** (Oct 2025): issuance **1.62 ms / 672 B**, presentation **735 µs / 288 B**, ~70× faster than batched VOPRF — **not deployed**. **ACT (Anonymous Credit Tokens)**, `draft-schlesinger-cfrg-act` (July 2026, Google + Cloudflare), is designed for **usage-based billing** with information-theoretic issuance↔spend unlinkability, ~2.2 kB per spend proof. Also not deployed. Post-quantum variants cost 85–173 kB — unaffordable.

**Payment is the hard gap.** GNU Taler v1.0 (2025) is Switzerland/CHF-only with no merchants. EU AMLR **bans anonymity-enhancing coins at CASPs from 1 July 2027**. Selling prepaid API credits makes you a prepaid access provider — a **FinCEN MSB**, with state money transmitter licences stacked on. The only working template is **Mullvad**: random account number, no email, cash by mail and retail vouchers — which works because it sells **flat-rate time, not metered usage**, and pushes KYC to the retailer.

---

## 6. Differential privacy for prompts

The picture genuinely improved, and you should update. **Private PoEtry** ([arXiv:2602.05012](https://arxiv.org/abs/2602.05012), Feb 2026), Qwen3-4B at **ε=4**: AGNews 87.0 vs 87.8 non-private; **GSM8k 43.1 vs 46.0**. **dps-mozo** ([arXiv:2501.19287](https://arxiv.org/abs/2501.19287)): ε=2 with **0.3% ROUGE-L drop**. **AdaDPSyn** (ICLR 2025) beats prior work at every ε.

Three caveats kill naive adoption. DP-ICL amortizes ε over a **fixed 10,000-query budget** and costs **10–100 LLM calls per user query** ([arXiv:2305.01639](https://arxiv.org/abs/2305.01639)). On domain-shifted data it collapses — Aug-PE OpenReview is **23.2pp** below non-private; HoC cancer F1 goes **71.6 → 11.0** at ε=1 ([arXiv:2508.20452](https://arxiv.org/abs/2508.20452)). And in several papers **the zero-private-data baseline beats the DP method** (AGNews: ε=0 instruction-only 68.0 vs ε=1 DP 64.1).

**Local-DP prompt rewriting should not ship.** Its ε is a metric-LDP parameter, not a DP ε — CusText's authors state ε_DP = ε′·d_max themselves; DP-Prompt's guarantee **grows linearly with output length**. Empirically: word-level DP at ε=8–12 is reconstructed at **72.18% (Llama-2-70B), 91.2% (GPT-4o), 94.01% (Claude-3.5-Sonnet)** ([arXiv:2410.12443](https://arxiv.org/abs/2410.12443)); ~50% of tokens at ε=4 ([arXiv:2410.17052](https://arxiv.org/abs/2410.17052)); authorship MCC **0.90 at ε=10** vs 0.98 unprotected ([arXiv:2205.02130](https://arxiv.org/abs/2205.02130)). That is theatre with a Greek letter on it.

---

## 7. Contextual integrity for agents

**PrivacyLens** (NeurIPS 2024, [arXiv:2409.00138](https://arxiv.org/abs/2409.00138)) is the decisive result: **GPT-4 answers 97.57% of norm-probing questions correctly and then leaks in 25.68% of agent trajectories**; Llama-3-70B leaks **38.69%**. Privacy prompting buys 1–6pp. **AirGapAgent** (CCS 2024, [arXiv:2405.05175](https://arxiv.org/abs/2405.05175)): context hijacking drops Gemini Ultra protection **94% → 45%**; the air-gap restores **97%**, at roughly **10pp** utility. **ConfAIde** (ICLR 2024): GPT-4 reveals secrets 22% of the time at Tier 3, ChatGPT 93%. **CI-Work** (ACL 2026 Industry): violation rates **15.8–50.9%**, and **higher task utility correlates with more violations**. **MCPTox** ([arXiv:2508.14925](https://arxiv.org/abs/2508.14925)): o1-mini ASR **72.8%**; best refusal rate **under 3%**. **AgentLeak** ([arXiv:2602.11510](https://arxiv.org/abs/2602.11510)): internal channels carry **2.1× more violations than final outputs (57.8% vs 27.2%)** — output-only audits are structurally blind.

**What works is deterministic information-flow control, not prompting.** **Progent** ([arXiv:2504.11703](https://arxiv.org/abs/2504.11703)): AgentDojo ASR **39.9% → 1.0%**, ~72% task utility. **FIDES** ([arXiv:2505.23643](https://arxiv.org/abs/2505.23643)): 163 → 1 successful attacks. **RTBAS** ([arXiv:2502.08966](https://arxiv.org/abs/2502.08966)): all targeted attacks prevented at **−2% utility**. **CaMeL** ([arXiv:2503.18813](https://arxiv.org/abs/2503.18813)): near-zero ASR at 2.8× token cost — authors concede three residual side channels. Counterweight: adaptive attacks break all eight tested defences at **>50% ASR** ([arXiv:2503.00061](https://arxiv.org/abs/2503.00061)), though those are mostly detection-based. Realistic residual for a well-built IFC agent: **~2–5% per task under adaptive attack**.

---

## 8. Memorization — overstated as background risk, understated as stage-dependent risk

**Sample-level membership inference against pretrained LLMs is largely dead as evidence.** Duan et al. (COLM 2024, [arXiv:2402.07841](https://arxiv.org/abs/2402.07841)): AUC **0.469–0.565**. Das, Zhang & Tramèr ([arXiv:2406.16201](https://arxiv.org/abs/2406.16201)): blind baselines that never touch the model beat SOTA MIAs on **8 of 8** benchmarks. CheckMIABench (2026, [arXiv:2606.17464](https://arxiv.org/abs/2606.17464)): a bag-of-words classifier hits **94.7% TPR@5%FPR on WikiMIA without the model**; on clean benchmarks all MIAs sit at **0.487–0.513**. Morris et al. ([arXiv:2505.24832](https://arxiv.org/abs/2505.24832)): **3.6 bits/parameter**; above ~10² tokens/parameter, extraction is generalization.

**But the risk is entirely a function of which training stage your data enters.** Google DeepMind ([arXiv:2406.11715](https://arxiv.org/abs/2406.11715)): data used for **SFT → 17.6% memorized**, with PII-like paths regurgitated in **50–54.8%** of completions; **DPO/IPO → 18.2–19.5%**; **reward-model/RL only → 0.9%**. Nasr et al.'s famous **$200 → 10,000 examples, 16.9% of generations containing memorized PII** ([arXiv:2311.17035](https://arxiv.org/abs/2311.17035)) was about pretraining corpora, and the attack was patched. Verbatim extraction is still alive in 2026 ([arXiv:2601.02671](https://arxiv.org/abs/2601.02671): 76.8% recall on Gemini 2.5 Pro).

**There is no public measurement of the rate at which providers train on consumer conversations or of extraction rates for that data.** Treat that absence as the open problem, not as reassurance. Your existing risk ranking — logging/retention/human review first, training-in last — is well supported.

---

## 9. Open problems the literature names

RAT-Bench: indirect identifiers dominate residual risk and are missed by every tool; NER is brittle to non-standard forms and non-English; better utility metrics are needed, **specifically for post-training on anonymized chat**. AURA: privacy protection "is difficult to make future-proof" — stronger attackers expose residual risk; anonymization must be a **continuous risk-management process, not one-time redaction**. The 2025 survey ([arXiv:2508.21587](https://arxiv.org/abs/2508.21587)) §9.3 names quasi-identifiers, contextual information, and **linguistic style** as the unsolved frontier. RedactionBench: contextual redaction is unsolved and humans agree only 47.7% on it. Lermen et al.: LLM deanonymization scales to internet-size candidate pools, and no defence is proposed.

---

## What the research says is impossible or impractical

1. **Entity replacement alone can never deliver non-profiling access.** Presidio leaves **59%** re-identification risk on explicit identifiers and **30%** on implicit (RAT-Bench). Five rounds of full adversarial LLM rewriting — far more destructive than tokenization — still leaves **41.6%** attribute inference (Staab ICLR 2025). The regulatory bar is 5%. Do not build a product whose privacy claim rests on the surrogate layer.
2. **Per-provider surrogate rotation does not produce unlinkability.** Lermen et al. link same-person profiles across a one-year gap at **90% precision**, ~35–45% recall at 1M candidates and ~27% at 100M, for **$1–4 per target**. Surrogates are not the linkage channel; topic, expertise and micro-data are.
3. **FHE and MPC for frontier proprietary models.** 134 s for a single Llama3-8B token on 8×B200; 419 GB of key material for 13B under MPC; the one 70B result requires public weights. A decade out, minimum.
4. **Split/oblivious inference as a privacy boundary.** Hidden states are provably injective; exact text recovered in linear time; DP at **ε=5,000 still leaks**. Closed.
5. **Local-DP prompt rewriting (InferDPT/SanText/CusText class).** 72–94% reconstruction at the epsilons where utility survives, with epsilons not comparable to real DP.
6. **Mixnets for interactive token streaming.** ~100 KB/s and p99 of 3 s, plus the anonymity trilemma.
7. **Asking the user to judge what is sensitive.** 240 participants performed **barely above chance**; annotators agree only **47.7%** on contextual redaction.
8. **Anonymous metered payment you can operate legally today.** Prepaid credits make you an MSB; EU bans privacy coins at CASPs from July 2027; Taler is CHF-only with no merchants.

---

## The five most promising tractable directions, ranked

**1. Build the unlinkability layer nobody has built — and the metric to score it.**
There is **no published unlinkability metric for text** and **no published defence against LLM-driven cross-session linkage**. Lermen et al. ([arXiv:2602.16800](https://arxiv.org/abs/2602.16800)) is the attack; the defence side is empty. A local model that scores a draft prompt's linkage risk against the user's own prior sessions — and suppresses the specific carrying details — is a defensible, publishable, ownable product. Supporting: SALA ([arXiv:2602.23079](https://arxiv.org/abs/2602.23079)) shows style needs a candidate DB; "I Am No One" ([arXiv:2609.12341](https://arxiv.org/abs/2609.12341)) shows F1 66→26 is achievable at zero perplexity cost. This is the thing your current design completely lacks and the thing the research says matters most.

**2. Local adversarial anonymization with an inference-aware budget, not a PII list.**
RAT-Bench proves attribute-list-driven anonymizers collapse when the list is generic (2% → 56%). The winning shape is a local adversary-in-the-loop. **SEAL** ([arXiv:2506.01420](https://arxiv.org/abs/2506.01420)) shows **8B models match GPT-4 anonymizers**; **AURA** ([arXiv:2605.30848](https://arxiv.org/abs/2605.30848)) retains 74.9–80.3% utility at 0–5/27 re-identification with on-device Qwen3.5 backbones. Keep your reversible surrogate vault for explicit identifiers — Deußer confirms reversible beats irreversible — and put an adversarial inference loop on top of it.

**3. Deterministic information-flow control for the agent surface.**
The clearest evidence base in the whole survey. Progent **39.9%→1.0%** ASR at ~72% utility; RTBAS all targeted attacks blocked at **−2% utility**; FIDES 163→1. Meanwhile prompting fails (PrivacyLens 97.6% awareness, 25.7% leakage) and AgentLeak shows **68.8%** of inter-agent messages leak while output-only audits see 27.2%. You have an agent gateway in the architecture already; this is the correct way to build it, and it is where your enterprise buyer actually feels pain.

**4. Own the PAPILLON frontier: local-remote delegation with measured quality.**
PAPILLON is **85.5% quality / 7.5% leakage** vs redaction's 77.2%/0% and raw 88.2%/100%. That 7.5% residual leak and the 2.7pp quality gap are both attackable, and the benchmark (PUPA) already exists to prove improvement. Combine with **SandwichPIR** ([eprint 2026/1816](https://eprint.iacr.org/2026/1816)) at **$0.20 per million queries** for any retrieval component — that piece is genuinely solved and cheap.

**5. Prototype the unlinkable access path, and be honest it is a research bet.**
OHTTP (RFC 9458) + **ACT** anonymous credit tokens (`draft-schlesinger-cfrg-act`, Google + Cloudflare, designed for usage-based billing, ~2.2 kB per spend) + **ARC** for rate limiting + voucher purchase through a merchant of record + constant-rate response padding. Every component exists; **none is deployed**. Two warnings: the PCC WiSec 2026 result ([arXiv:2605.24239](https://arxiv.org/abs/2605.24239)) shows the only shipped unlinkable-inference system has a token-salt linkability bug, and DeepCorr hits **TPR 1.0 at FPR 10⁻³** against un-padded two-hop relays, so token-timing padding is mandatory, not optional.

**What I would deprioritize:** TEE-based positioning (works today at 5–8% overhead, but Battering RAM at **$47.62**, WireTap, and TEE.Fail forge attestation and the vendors will not fix it — do not make it your trust story), DP-for-prompts (the 2026 numbers are real but the query-budget and domain-shift cliffs make it a compliance artifact, not a product), and any FHE/MPC narrative.

**The blunt summary:** your mechanism is correct as a component, already published as SurrogateShield ([arXiv:2606.29567](https://arxiv.org/abs/2606.29567)), and insufficient as a product thesis. The stated goal — no provider or coalition can build a profile or link activity across sessions — is **not achieved by reversible identity tokenization**, and the literature has the numbers to prove it. The defensible company is the one that measures and defends the linkage channel, because that is the part of the problem the research has attacked hard and defended not at all.

---

## Independent verification (done directly, not via subagent)

Both load-bearing claims fetched from arXiv on 2026-09-18:

**SurrogateShield** — arXiv:2606.29567, "Beyond Redaction for High-Utility, Privacy-Preserving LLM
Interactions", Sherwin Vishesh Jathanna, submitted 28 June 2026. Abstract confirms: client-side proxy,
type-consistent surrogates, restores originals in the response, "No real PII crosses the network
boundary", three-stage detection cascade over 22 PII types, **and quasi-identifier combinations grounded
in Sweeney's k-anonymity** — so it also covers the QI scoring we listed as a gap. Mappings sealed in an
AES-256-GCM per-conversation "ShadowMap" that never leaves the device.

Important qualifier: this is a **single-author preprint, not a company or a shipped product**. It blocks
a novelty claim and it will be cited at us in any technical diligence. It is not a competitor.

**Large-scale online deanonymization with LLMs** — arXiv:2602.16800, Lermen, Paleka, Swanson, Aerni,
Carlini, Tramèr. Submitted 18 Feb 2026, **published at USENIX Security 2026**. Abstract headline:
**up to 68% recall at 90% precision, versus near 0% for the best non-LLM method.** The per-target cost
figure of $1–4 is from the body, not the abstract — treat as read-from-PDF rather than headline.

This is a top-tier venue, from the group that defined LLM memorisation research. It is the single
strongest piece of evidence against surrogate rotation as an unlinkability mechanism.
