Confirmed the white space. Writing the report now.

---

# Lethe — Freedom-to-Operate and White-Space Study
**Date:** 2026-09-18 · **Sources:** WIPO PATENTSCOPE full-text, Google Patents XHR API, FreePatentsOnline full text, USPTO

**Method note on verification.** Google Patents rate-limited midway through this study and my WebSearch quota was exhausted, so the bulk of verification was done against WIPO PATENTSCOPE full-text search and FreePatentsOnline claim text. Every claim I summarize below was read from the actual claim text unless explicitly flagged "**claims not read**." Where I list a patent from a search index without opening it, I say so. I have invented no patent numbers.

---

## 1. Headline finding

Two references sit almost directly on Lethe's core loop, and one of them is granted:

**US12417317 (Anonos IP LLC), granted 2025-09-16** — *"Systems and methods for dynamic de-identification and anonymity for user input to artificial intelligence (AI)-based models."* Claim 1, read in full: receive an input to an AI model from a client; identify sensitive data elements within it; generate a *different* dynamically-changing, temporally unique identifier (DDID) for each; replace every occurrence in the input; and store the information needed to recover the original from the DDID. Claim 3 recites generative AI. Claim 7 covers re-identifying the *model's response*. Claim 2 covers cross-input token reuse.

That is Lethe's mechanism, claimed at system level, already granted. Worse, the priority chain — which I read from the cross-reference section — runs back through a ladder of CIPs to **provisional 61/899,096, filed 1 Nov 2013**. Anonos also has live continuations publishing in 2026 (US20260057176, US20260220300), meaning they can still draft claims aimed at whatever we ship.

**US20250254051A1 (Insight Direct USA, Inc.)**, priority 2024-02-02 (prov. 63/549,029), filed 2025-02-03, published 2025-08-07, **pending**. Claim 1 verbatim in substance: receive unencrypted information → identify a word to encrypt → replace it with an automatically generated key → replace *all* instances to maintain referential integrity → save the word–key pair in a database → send to the large language model with a prompt → receive encrypted output → replace all instances of the key with the word to produce unencrypted output. This is Lethe's round trip, written as a method claim, with the LLM named. It is not yet granted, which matters.

---

## 2. Risk table

| Patent / App | Assignee | Priority | Status | What it claims | Risk |
|---|---|---|---|---|---|
| [US12417317](https://www.freepatentsonline.com/12417317.html) | Anonos IP LLC | 2013-11-01 chain (claims likely supported only from 2021/2022 CIPs) | **Granted** 2025-09-16 | Per-element DDID substitution in input to an AI model + recovery mapping; dep. claims cover generative AI and response re-identification | **HIGH** |
| [US12614034B2](https://patents.google.com/patent/US12614034B2/en) | Anonos Innovations LLC | 2024-08-26 | **Granted** 2026-04-28 | NLP detection of sensitive spans in unstructured text, hierarchical sensitivity labels, reversible semantic tokens into an LLM, selective token reversal at authorized endpoints post-inference | **HIGH** |
| [US20250254051A1](https://www.freepatentsonline.com/y2025/0254051.html) | Insight Direct USA | 2024-02-02 | Pending | Full surrogate round trip through an LLM with referential integrity + word-key vault | **HIGH** |
| [US20240313973A1](https://www.freepatentsonline.com/y2024/0313973.html) | Springcoin, Inc. | filed 2023-11-09 | Pending | Reversible tokens for language-model input using **two** tokenization processors with split secrets; "short label token" substitution for output fidelity; dep. claim 2 covers deterministic *vs* non-deterministic tokens | **MED-HIGH** |
| [US20220067206A1](https://www.freepatentsonline.com/y2022/0067206.html) / US20240184923A1 | Open Text Holdings | 2020-08-28 | Pending (sibling [US12292999B2](https://patents.google.com/patent/US12292999B2/en) granted 2025-05-06 for structured data) | Tokenize **unstructured text** with self-describing tokens having a preconfigured pattern + protection-strategy indicator; store originals in a secure vault; later "reveal" by pattern-matching the tokens | **HIGH** (pre-LLM but generic) |
| [US9361481B2](https://patents.google.com/patent/US9361481B2/en) and Anonos DDID family (US9087215B2, US9129133B2, US9619669B2, US10043035B2, US10572684B2, US11790117B2, US12093426B2, US12591709B2) | Anonos | 2013-11-01 | Granted; term to ~2033-34 | DDIDs re-associated per time/place/purpose; two keys yielding two different *views* of the same identifier | **HIGH** (this is the unlinkability primitive) |
| [US10454901B2](https://patents.google.com/patent/US10454901B2/en) | Datavant | 2016-01-19 | Granted | De-identify at source using a **project-specific key value**; hash removed identifiers; match across sites at a third server to build a universal de-identified set | **MED** |
| [US11755779B1](https://patents.google.com/patent/US11755779B1/en) / US11550956 | Datavant | 2020-09-30 | Granted | Central platform issues per-site keys and tokenizing rules; **tokens unique to the first client site and the subject**; bridge file links them | **MED-HIGH** (closest prior art to per-provider salting) |
| [US11120144B1](https://www.freepatentsonline.com/11120144.html) | Datavant | 2018-04-12 | Granted | Central management platform assigning a unique encryption key + permissions + config to each remotely deployed tokenization instance | **MED** |
| [US12688261](https://www.freepatentsonline.com/12688261.html) | Daon Technology | filed 2026-02-27 | **Granted** 2026-07-21 | Authorizing an autonomous AI agent's tool invocation via fidelity + integrity signals, policy at an authorization checkpoint, and a machine-verifiable **delegation artifact encoding permitted action type, scope, and bounded validity interval** | **HIGH** (for our capability manifests) |
| [US20260267882A1](https://www.freepatentsonline.com/y2026/0267882.html) | Vijay Madisetti | filed 2026-03-11 | Pending | **Host-side enforcement wrapper interposed between an LLM agent and servers**; evaluates an action object against session policy; allow/block/no-op/approval-gate; without modifying agent or servers | **MED-HIGH** (this is an MCP gateway) |
| US20250328560A1 | Vijay Madisetti | 2023-05-04 | Pending | Security for multi-agent generative AI applications — **claims not read** | MED |
| [EP4733974A1](https://patents.google.com/patent/EP4733974A1/en) | Google LLC | 2024-10-24 | Pending | On-device generative model strips PII from a prompt, inspects for residual PII, uploads only if clean. **No re-identification step** | **LOW-MED** |
| US20250068764A1 | Microsoft | 2023 | Pending | PII scrubbing + DP during fine-tuning — **claims not read**; different problem (training, not inference round trip) | LOW |
| [US20240427928A1](https://www.freepatentsonline.com/y2024/0427928.html) | Microsoft | 2024-01-19 | Pending | Consent-gated access to additional sensitive user data to improve a response | **LOW** |
| [US20250086310A1](https://www.freepatentsonline.com/y2025/0086310.html) | IBM | 2023-09-13 | Pending | Prompt pre-processing + topic modeling + normalization; PII removal only in dep. claim 2 | **LOW** |
| US20250350455A1 / US20250350445A1 / US20250350467A1 | Apple | 2024 | Pending | Private Cloud Compute: secure supplemental LLM processing, immutable system properties, E2E-encrypted load balancing — **claims not read** | LOW (orthogonal; relevant only to an attestation extension) |
| US11979500B2 | TokenEx | 2019-05-24 | Granted | Data format-preserving encryption, tokenization and access control — **claims not read** | MED |
| US8578176B2 / US20140059088 / US12153693B2 | Protegrity | 2008 / 2012 / 2017 | Granted | Tokenization of sensitive character sets; date tokenization; sensitive data classification. No LLM filings found | LOW-MED (mostly useful as prior art) |
| US20240331576A1, US20250106208A1, US20250322095A1, US20240045988A1 | Skyflow | 2021-2024 | All pending, none granted | Polymorphic vault encryption, multi-vault reporting, API trust — **claims not read** | LOW-MED |
| US11689508B1 / US11036885B1 | Very Good Security | 2018-01-06 | Granted | Aliasing proxy for sensitive data — **claims not read (fetch failed)** | MED — resolve before launch |
| US20250258938A1 | Kong Inc. | 2024-02-13 | Pending | Egress web gateway regulating AI application queries — **claims not read** | MED — resolve |
| US20240403560A1 / EP4471640 | CrowdStrike | 2023 | Pending | Prompt-injection prevention *by tokenization* — **claims not read** | MED — resolve |
| US20150339496A1 | Privacy Analytics | 2014 | Granted family | Date shifting in de-identification | LOW (prior art asset) |
| WO2024/26152 | NEC Laboratories Europe | 2023 | Pending | "Secure and privacy preserving querying of large language models" — **claims not read** | MED — resolve |

**Assignees checked with no relevant patents found:** Nightfall, Cyberhaven, Piiano, Evervault, Protecto (AI), Comforte, Baffle, Anjuna, Edgeless, LeapYear, Inpher, Opaque, TripleBlind (holds federated-learning patents only, e.g. US11991156B2), Truata, Anthropic, OpenAI. Securiti.ai returned nothing resolvable under that name. Palo Alto, Zscaler, Netskope and Check Point have LLM-security filings but none on reversible PII substitution. Duality and Enveil are entirely in HE/MPC, not tokenization.

---

## 3. What appears genuinely unclaimed — the white space

I ran four independent query formulations specifically targeting per-recipient unlinkability for AI providers (`"AI provider"/"model provider"/"LLM provider"` × `unlinkable`/`cross-provider`/`cannot be correlated`; `"distinct pseudonym" AND "each recipient"`; `"per-provider"`; `site/recipient/party-specific salt`). **Nobody claims it for AI or LLM providers.** The hits were gambling platforms, telecom, and unrelated noise.

The primitive is old and owned in adjacent domains — Anonos owns "same subject, different identifier per time/place/purpose" (US9361481B2 claims 4-7) and Datavant owns "per-site, per-project token derivation" for healthcare record linkage (US11755779B1, US10454901B2). But nobody has claimed **deriving surrogates per model provider so that two frontier-LLM vendors holding the same user's traffic cannot join their datasets.** That is a real, defensible gap — though see §5 for why it must be claimed narrowly.

Also unclaimed, as far as I can find:

- **k-anonymity / quasi-identifier scoring applied to a prompt before egress.** The `"quasi-identifier" AND prompt` search returned nothing on point. Privacy Analytics owns risk-scoring for *datasets* (US11380441, US20160155061) but not for conversational prompts.
- **A hash-chained, signed ledger attesting to what was withheld.** Every hit was generic AI-governance anchoring (R.J. Mitchell's US20260228755A1/US20260238651A1, Sangam Das's WO filings). Nobody claims a tamper-evident proof whose subject is *the set of entities that never crossed the boundary* — a negative-disclosure attestation. This is unusual and non-obvious.
- **Detokenization gated at a tool's action boundary.** Daon (US12688261) gates the *invocation*; Madisetti (US20260267882A1) gates the *action object*. Neither couples the release of the real identity value to the moment of the action. The join — the agent reasons over surrogates throughout and the vault releases the true value only into the outbound side-effect — is open.
- **On-device local vault.** Anonos, Insight Direct and Open Text all claim server- or system-side vaults. Google's EP4733974A1 is on-device but has no re-identification step.

---

## 4. What we would likely need to license or design around

**Anonos is the single existential issue.** US12417317 is granted, is drafted at exactly our altitude, and its owner is a licensing-driven IP company with a decade-deep continuation ladder. Options, in order of preference:

1. **Attack the priority date.** The claims of US12417317 recite "input to an artificial intelligence (AI) model." The 2013 provisional is titled "Dynamic Identity Masking and Management System" and is about DDIDs for data subjects, not prompts to generative models. If the AI-inference limitations are only supported by the Oct-2021 or Oct-2022 CIPs, the effective filing date moves to 2021/2022 — which opens the door to 2021-2023 prior art. This requires a written-description analysis by counsel and is the highest-leverage defensive move available.
2. **Design around the storage limitation.** Claim 1 requires storing "information that, when used in combination with an associated [DDID], is needed to recover the sensitive data element." A design where the surrogate is a *deterministic, keyed, format-preserving encryption of the plaintext* — so the original is recovered by decryption with a key never associated to a particular DDID, and no per-element recovery record is stored — arguably falls outside. This is also a better architecture.
3. **Take a license.** Anonos licenses; this is a normal outcome and should be budgeted.

**Insight Direct** is pending, not granted. File third-party prior-art observations now. Their claim 1 is broad enough that Open Text's US20220067206A1 (2020 priority — vault + unstructured text + reveal) plus Microsoft Presidio's public releases plus the enormous 2023 body of prompt-redaction work should force substantial narrowing.

**Open Text / Voltage** is the sleeper. US20220067206A1 claims tokenizing unstructured text with self-describing tokens and a vault reveal, with no AI limitation at all. Applying it to LLM prompts is arguably just a use. If it grants as filed it taxes the whole category. Watch it; consider opposition.

**Springcoin** is narrower than it looks — claim 1 requires *two* distinct tokenization processors sharing split secrets. Lethe's single local vault should read out. But their claim 2 explicitly covers non-deterministic tokens that hide whether two source values are identical, which is adjacent to our unlinkability story. Review the whole 8-member family before filing.

**Daon US12688261** is granted and covers delegation artifacts with action type, scope and validity interval. Our capability manifests should avoid reciting biometric/behavioral binding to a person (their "fidelity signal" is the distinguishing limitation) and should be framed as *data-scope* manifests, not authorization tokens.

**Unresolved — do before launch:** read claim 1 of VGS US11689508B1, Kong US20250258938A1, CrowdStrike US20240403560A1, TokenEx US11979500B2, NEC WO2024/26152, and the four Skyflow applications. I could not retrieve these within this session's constraints.

---

## 5. What we could plausibly file ourselves

Ranked by strength. Each should be drafted with the surrounding art in mind so it is narrow enough to survive and specific enough to be worth something.

1. **Provider-scoped surrogate derivation for unlinkability across model providers.** Claim it as: deriving the surrogate for entity *e* destined for provider *p* as a keyed function of (*e*, provider-identity *p*, vault master key), such that surrogates for the same *e* differ across providers and are non-correlatable without the vault; with a single local vault resolving all provider-scoped surrogates back to *e* on ingress. The distinguishing art is Datavant (per-*site*, healthcare, central platform issuing keys, purpose is *enabling* linkage) and Anonos (per-time/place/purpose, no provider concept, server-side). Our differentiators: the salt is bound to the *recipient model provider's identity*, the purpose is *preventing* linkage rather than enabling it, and resolution is device-local. Draft around those three.
2. **Negative-disclosure attestation.** A hash-chained, locally signed ledger in which each entry commits to the set of sensitive entities *detected and withheld* at a boundary crossing, producing a verifiable proof that a named entity never left the device. No art found. The non-obviousness is that transparency logs (Certificate Transparency) and audit logs universally attest to what *happened*; attesting to what *did not* is inverted.
3. **Action-boundary detokenization.** Releasing a true identity value from the vault only at the instant an agent's tool call performs an externally visible effect, with the agent's reasoning context holding only surrogates throughout — and binding the release to the specific tool, action type and parameter position declared in a capability manifest. Threads between Daon (gates invocation, requires behavioral binding) and Madisetti (gates the action object, no PII coupling). The PII-release coupling is the novel join.
4. **Pre-egress k-anonymity scoring of a prompt.** Computing a re-identification risk score over the *residual quasi-identifiers* remaining in a prompt after surrogate substitution, against a population model, and blocking or further generalizing when the equivalence class falls below *k*. Privacy Analytics owns dataset-level analogues; nobody has claimed it for conversational text at egress.
5. **Cross-agent surrogate consistency within a swarm.** Maintaining referential integrity of surrogates across multiple agents and multiple providers in one task, while keeping the per-provider mappings mutually unlinkable. Insight Direct claims referential integrity within one session with one model; the multi-agent, multi-provider, unlinkable variant is open.

Do not bother filing on: PII detection in text, surrogate substitution *per se*, vault-and-restore round trips, or format-preserving encryption. All four are comprehensively owned or are pre-2020 prior art.

---

## 6. Defensive posture — prior art we can point to

Strong, datable, public art exists to attack broad claims filed after ~2023:

- **PCI tokenization (2005-2012).** Protegrity US8578176B2 (priority 2008-03-26, "tokenization of sensitive sets of characters"), US20140059088 (date tokenization). Establishes vault-and-restore surrogates as routine.
- **Format-preserving encryption.** NIST SP 800-38G (FF1/FF3, 2016); Intel US9436839B2 (2014, "tokenization using multiple reversible transformations"); CA US10607017B2 (2017). Establishes format-preserving reversible surrogates.
- **HIPAA Safe Harbor de-identification and date shifting.** Privacy Analytics US20150339496A1 (2014). Establishes realistic-surrogate substitution that preserves analytic utility.
- **Datavant / Universal Patient Key (2016-2020).** US10454901B2, US11004548, US11120144B1. Establishes per-project/per-site keyed tokens and the central-management pattern — the strongest art against any *broad* per-recipient-salt claim, including ours. Our own filing must be narrowed against it.
- **Microsoft Presidio** — open source, public since 2019, documented anonymize/deanonymize with an operator-result mapping. This is the best single piece of art against post-2023 "detect PII in text and substitute reversibly" claims, including Insight Direct's.
- **ARX Data Anonymization Tool** — open source since ~2012, k-anonymity/l-diversity/t-closeness. Art against risk-scoring claims.
- **Anonos's own 2013-2016 DDID disclosures** cut both ways: they are excellent art against anyone *else's* per-context-identifier claims, including any competitor who tries to fence our unlinkability idea.

One asymmetry worth noting: the 2024-2026 filing wave in this space is dominated by pending applications, not grants. Anonos and Daon are the only granted references that genuinely bite. That means there is still time to file — but roughly 12-18 months of it, and the Anonos priority question should be answered by counsel before significant engineering is committed to the current architecture.
