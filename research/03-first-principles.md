# Lethe: A First-Principles Technical Brief

_Research agent output, lightly formatted. Privacy harness design against the actual frontier-lab pipeline, as of September 2026._

## 0. TL;DR

- **The pipeline does not care whether "Alice" is real.** Tokenizers, pretraining, and post-training operate on token statistics; a realistic, well-formed, consistently-mapped surrogate is indistinguishable from real data to every stage. Abstract tags (`[PERSON_1]`, `⟨PERSON_3⟩`) fight the pipeline: they fragment into 5–9 tokens and measurably degrade reasoning.
- **Utility loss from entity replacement is small on generation tasks (≈1 point/10) but catastrophic on retrieval/grounding and quantitative tasks when the wrong things are masked** (RGB retrieval: 0.80 → 0.32; monetary placeholders flip exchange-rate reasoning). Rule: tokenize *identifiers*, preserve *semantics and quantities*.
- **Honest risk ranking of PII in prompts:** (1) inference-time logging/retention/subpoena/human review, (2) agent/tool traces and injection exfiltration, (3) memory features, (4) being trained in.
- **Anonymizing names is necessary but insufficient**: LLMs infer location/age/income from free text at 85% top-1, and a $3 agent run rebuilds a profile at >90% accuracy. v2 must generalize quasi-identifiers and shard context.

## 1. The pipeline, first principles

### 1.1 Tokenization

| String | GPT-4o (`o200k`) | Llama 3.2 | Qwen3 | Notes |
|---|---|---|---|---|
| `Michael Brooks` | 2 | 2 | 2 | realistic surrogate |
| `John Smith` | 2 | 2 | 2 | |
| `Priya Raghunathan` | 6 | 6 | 6 | real names fragment too |
| `PERSON_1` | 3 | 3 | 3 | |
| `[PERSON_1]` | 5 | 5 | 5 | |
| `<LOC>-1` | 4 | 4 | 4 | scheme used in Deußer et al. 2026 |
| `⟨PERSON_3⟩` | **9** | 6 | 5 | Unicode brackets → byte-fallback |
| `$4,250.00` | 6 | 6 | 9 | Qwen splits every digit |
| `123-45-6789` | 6 | 6 | 11 | |

A surrogate name costs 2 tokens in the densest region of the embedding table; a bracketed tag costs 4–9 tokens of punctuation and fragments the model has seen mostly in code. Consistent surrogates remove the reassembly tax on every mention. Replacing an amount with a tag removes the only thing the model can reason over.

### 1.2 Pretraining and deduplication

Memorization grows log-linearly with model size, duplication, and context length ([Carlini et al. 2022](https://arxiv.org/abs/2202.07646)). Deduplicated training emits memorized text ~10x less ([Lee et al. 2022](https://arxiv.org/abs/2107.06499)); a sequence appearing 10x is regenerated ~1000x more often ([Kandpal et al. 2022](https://arxiv.org/abs/2202.06539)). A single user prompt is a singleton in a multi-trillion-token corpus; duplication raises risk.

### 1.3 Post-training

SFT → RLHF with reward model ([InstructGPT](https://arxiv.org/abs/2203.02155)); RLAIF / Constitutional AI ([Bai et al. 2022](https://arxiv.org/abs/2212.08073)); DPO ([Rafailov et al. 2023](https://arxiv.org/abs/2305.18290)); GRPO / RLVR ([DeepSeekMath](https://arxiv.org/abs/2402.03300), [Tülu 3](https://arxiv.org/pdf/2411.15124), [DeepSeek-R1](https://arxiv.org/abs/2501.12948)). Preference data comes from thumbs-up/down and opt-in logs, stored with the full conversation; membership inference on RLHF preference data is demonstrated ([Amazon Science](https://www.amazon.science/publications/exposing-privacy-gaps-membership-inference-attack-on-preference-data-for-llm-alignment)).

### 1.4 Lab practice, 2025–2026

| | Consumer chat | Feedback | API | Retention |
|---|---|---|---|---|
| **OpenAI** | Trains unless opted out; Temporary Chats excluded | Thumbs-up/down may be used even if opted out | Not trained since Mar 2023; 30-day abuse logs; ZDR on listed endpoints | NYT litigation forced preservation May–Sept 2025; Aug 2026 "Private Safety Processing" |
| **Anthropic** | Since Aug 28 2025, Free/Pro/Max train unless opted out; opt-in kept **5 years** | 5 years | Commercial: not trained. **Since June 9 2026 Covered Models require 30-day retention even under ZDR** | Deleted ≤30 days; T&S violations 2 years |
| **Google** | Gemini Apps Activity on → training with human review; off → still 72 h; human-reviewed kept 3 years | Same | Paid API not used; **free tier used, human reviewers may read** | |

Retention windows are policy; they change quarterly; safety review involves humans reading raw prompts. A harness that never emits raw PII is robust to policy drift.

## 2. Memorization and extraction

| Result | Number | Source |
|---|---|---|
| GPT-2 emits verbatim sequences incl. names, phones, emails | 604 of 1,800 | [Carlini 2021](https://arxiv.org/abs/2012.07805) |
| ChatGPT divergence attack | $200 → >10,000 examples; **16.9% of generations contained memorized PII** | [Nasr, Carlini et al. 2023](https://arxiv.org/abs/2311.17035) |
| PII in fine-tuned GPT-2 on ECHR | recalls 23% of PII | [Lukas et al. 2023](https://arxiv.org/abs/2302.00539) |
| Llama 3.1 70B reproduces Harry Potter 1 | near-verbatim | [Cooper et al. 2025](https://arxiv.org/abs/2505.12546) |
| Re-examining PII "memorization" | driven by surface-form cues; cue-free extraction has very low TPR | [2026](https://arxiv.org/abs/2601.03791) |

**Risk ranking:** (1) logging/retention/human review/subpoena — highest, certain; (2) agent/tool traces — high, growing ([EchoLeak CVE-2025-32711](https://arxiv.org/abs/2509.10540); [MCP tool poisoning](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks); [Profiling for Pennies: >90% profile for <$3](https://arxiv.org/abs/2605.06232)); (3) memory features — medium; (4) being trained in — lowest but irreversible.

## 3. Does anonymization hurt intelligence?

| Study | Setup | Result |
|---|---|---|
| [Deußer et al., Sept 2026](https://arxiv.org/abs/2609.11335) | 5 models × 11 benchmarks, `<LOC>-1` pseudonyms | Qwen2.5-72B **−6.9 pp**, Teuken-7B −2.3 pp. **RGB retrieval collapse** 0.80→0.32 (query and docs anonymized independently). Reversible uniqueness-preserving beats redaction (MedQA 0.83 vs ~0.70). `$1.36`→`<MONETARYVALUE>-1` flipped an answer. |
| [Pasch & Cha 2025](https://aclanthology.org/2025.privatenlp-main.3/) | Cover letters, emails | ~**1 point / 10** loss at 97–99% masking |
| [PAPILLON, NAACL 2025](https://arxiv.org/abs/2410.17127) | 901 WildChat prompts (PUPA) | Raw 88.2 quality / 100 leakage. **Naive redaction 77.2 / 0.** Optimized 85.5 / 7.5 |
| [Yermilov et al. 2023](https://aclanthology.org/2023.trustnlp-1.20/) | Pseudonymized classification/summarization | Realistic context-consistent pseudonyms ~10x better than tags |
| [Tau-Eval 2025](https://arxiv.org/pdf/2506.05979) | LLM anonymizers | Up to 42% loss on toxicity detection |
| [MathEd-PII 2026](https://arxiv.org/abs/2602.16571) | Tutoring transcripts | Presidio F1 **0.379** (numbers look like IDs) |
| [Staab et al., ICLR 2025](https://arxiv.org/abs/2402.13846) | Adversarial LLM anonymization | Higher utility and privacy than Azure |

**Failure modes:** gender/culture coherence (names carry priors: [Haim et al. 2024](https://arxiv.org/abs/2402.14875)); surrogates must match gender, culture, formality; "plausible unknown names" pool ([PUN 2026](https://arxiv.org/abs/2608.21206)). Do not mask amounts/ages/durations/dosages. Shift dates by a per-session offset. Retrieval collapse is a *consistency* bug: apply one mapping to prompt, history, retrieved chunks, tool outputs and model outputs.

**Design rules:** *Tokenize* names, contacts, IDs, accounts, exact addresses, identifying employers, rare-disease+location combos. *Preserve* quantities, shifted dates, roles, relationships, sentiment, domain terms. *Format-preserve* every replacement.

## 4. Where the layer runs

### 4.1 On-device detection

| Component | Accuracy | Latency |
|---|---|---|
| GLiNER-PII (Knowledgator) | F1 ~81–83 (synthetic) | Rust runtime 4x CPU |
| GLiNER Guard (2026) | 145–209M params | **19–20 ms/request** on A100; 40x throughput vs 7B guard |
| DeBERTa-v3 on ai4privacy | F1 **0.9757** in-distribution | ~180M params |
| Same on PIIBench (48 types, 2.4M seq) | **All <0.14 span-F1** ([PIIBench 2026](https://arxiv.org/abs/2604.15776)) | — |
| Context-aware SLM | Recall 94% vs 63% commercial ([2025](https://arxiv.org/abs/2512.04120)) | 8–14B |
| Apple on-device 3B | — | 0.6 ms/token TTFT, 30 tok/s on iPhone 15 Pro |

PIIBench is the most important number: off-the-shelf PII NER collapses under distribution shift. Lethe must fine-tune on its users' distribution, layer validators, use an SLM only for context-dependent decisions, and treat detection as the weakest link.

### 4.2 Confidential computing

| Option | Trust anchor | Overhead | Does NOT protect against |
|---|---|---|---|
| TDX / SEV-SNP + NVIDIA CC | CPU vendor + NVIDIA attestation | GPU TEE 4–8%; TDX serving TTFT +22–28% | Operator's application logging; model owner |
| Privatemode / Continuum | Above + open attested stack | Same | Open-weight only |
| Apple PCC | Apple boot chain; transparency log; OHTTP relay | Undisclosed | Apple as model owner |
| Lethe surrogate layer | User's device/org boundary | ms | Semantic leakage |

These compose. None alone suffices.

### 4.3 Semantic leakage

{ZIP, DOB, sex} identifies 87% of Americans ([Sweeney](https://dataprivacylab.org/projects/identifiability/paper1.pdf)); 15 attributes re-identify 99.98% ([Rocher 2019](https://www.nature.com/articles/s41467-019-10933-3)). GPT-4 infers location/income/sex at **85% top-1** from Reddit text ([Staab, ICLR 2024](https://arxiv.org/abs/2310.07298)). v2: generalize quasi-identifiers with k-anonymity budgets; per-session ephemeral identities; context sharding across providers (no empirical study yet).

## 5. Complementing the lab pipeline

(a) Realistic surrogates keep priors intact. (b) Session-consistent bijection preserves coreference; apply to outputs and re-inject. (c) Tool calls are just more text; detokenize only at side effects inside the boundary. (d) Need-to-know for swarms = contextual integrity ([Nissenbaum 2004](https://digitalcommons.law.uw.edu/wlr/vol79/iss1/10/)); models don't enforce it themselves: GPT-4 leaks in **25.68%** of agent actions ([PrivacyLens](https://arxiv.org/abs/2409.00138)); one hijack drops Gemini Ultra 94%→45% while an architectural minimizer holds 97% ([AirGapAgent](https://arxiv.org/abs/2405.05175)); CI supervisor 0.87 utility / 0.01 leakage ([DeepMind 2024](https://arxiv.org/abs/2408.02373)); [CI-Bench](https://arxiv.org/abs/2409.13903); [CI-Work 2026](https://arxiv.org/pdf/2604.21308). (e) Attestation: Merkle log (RFC 6962 / Sigstore Rekor) of (policy version, detector hash, mapping commitment, outbound hash); ZK-regex proofs of absence ([zk-regex](https://docs.zk.email/zk-regex), [ε-NFA 2026](https://eprint.iacr.org/2026/1284)); ZK proofs of NER not practical (zkLLM 986 s + 803 s per forward pass).

## 6. Threat model

| Adversary | Lethe v1 | Notes |
|---|---|---|
| Provider logging / abuse review / human review | **Full** identifiers; partial quasi-IDs | Reviewer sees a coherent fictional person |
| Provider training | **Full** identifiers; partial semantic | Surrogates map to nobody |
| Provider breach / insider | **Full**; partial | Vault is the crown jewel |
| Subpoena | **Full**; partial | Cannot produce what it never had |
| Memory features | **Partial** | Needs per-session IDs |
| Malicious tool / MCP | **Partial** | Exfiltrates surrogates only |
| Prompt injection | **Partial** | Semantic content still exfiltrable |
| Another agent | **Partial → full** with scoped views | Structural enforcement |
| Attribute inference from free text | **Not mitigated** in v1 | v2 |
| Detector miss | **Not mitigated** | Layer validators, SLM, user review |

## 7. Ten engineering principles

1. **Surrogates, not tags.** In-distribution, format-preserving, gender- and culture-matched.
2. **Identifiers in, semantics out.** Never mask amounts.
3. **One bijection per scope, applied everywhere.** Retrieval collapse is a consistency bug.
4. **Detection is the weak link; layer it.** Assume <0.14 F1 on your real distribution until proven.
5. **Detokenize only at side effects, inside the boundary, signed.**
6. **Need-to-know is structural.** Don't rely on the model to withhold.
7. **Ephemeral identities per session.**
8. **Assume retention is longer than the contract says.**
9. **Make the claim checkable.** Merkle-logged signed outbound hashes; ZK-regex proofs of absence.
10. **Measure intelligence loss continuously.** Paired eval on the user's own traffic ([Preempting 2024](https://arxiv.org/abs/2411.11521)).

## 8. Honestly unsolved

Semantic re-identification; detector generalization; context sharding (no study); ZK proof of redaction beyond regex; memory-feature interaction; provider-side detokenization needs.
