# Lethe — Competitive Landscape & Prior Art (as of 2026-09-14)

_Research agent output, lightly formatted. See citations at the end._

## 0. TL;DR

- **Reversible PII tokenization in front of LLMs is not novel.** It ships today in WitnessAI, Wald.ai, Protecto, Skyflow, Kong's AI PII Sanitizer (restore mode), Google Sensitive Data Protection, LLM Guard's Vault, LangChain's `PresidioReversibleAnonymizer`, and half a dozen GitHub proxies.
- **Detection is fully commoditized.** OpenAI released an Apache-2.0, 1.5B-param (50M active) local PII model in April 2026 [1]; GLiNER2-PII (0.3B, 42 types) beats it on span F1 [2]. Lethe's moat cannot be the detector.
- **What nobody ships as one product:** device-side key custody + swarm-wide consistent bijection across agents/tool calls/A2A messages + detokenization at the tool boundary + a legal posture built on the Sept-2025 CJEU *EDPS v SRB* ruling. That is the actual white space, and it is narrower than the pitch.
- **"Near-zero intelligence loss" and "cannot be profiled" are both contested by 2026 research** (§4, §6). Treat them as hypotheses, not features.

## 1. Comparison table

| Company | Detection | Reversible? | Deployment | Stage (2026) | Gap vs Lethe |
|---|---|---|---|---|---|
| Limina (ex-Private AI) [3][4] | Proprietary NER, 50+ entities, 52 langs | Pseudonymize/synthetic; re-ID not headline | Container on-prem/VPC | ~$8M; rebranded Mar 2026 | Data-pipeline de-ID, not runtime agent gateway; no MCP/A2A |
| Protecto [5] | Proprietary ("99.9%", 200+ types) | Yes, consistent per namespace, unmask by permission | SaaS / VPC / on-prem / SDK | Private; GCP Marketplace Mar 2026 | Closest enterprise analogue; cloud-first, org-side not user-side |
| Skyflow LLM Privacy Vault [6][7] | Skyflow detection + dictionary | Yes, deterministic tokens, RBAC re-ID | SaaS vault (plaintext in Skyflow) | Growth | Shifts trust to third-party vault |
| WitnessAI [8][9] | Classifier | Yes, tokenizes before model, rehydrates response | Single-tenant, BYOK, network | $58M | Enterprise network control point; sees plaintext |
| Wald.ai [10][11] | "Contextual" classifier | Yes, placeholders re-populated on screen | SaaS + browser | $4M seed (Dec 2024) | Closest consumer analogue; no agent/MCP path |
| Nightfall AI [12][13] | Cloud ML | No (redact/block/coach) | Ext, endpoint, API, MCP inspection | Funded | One-way DLP, cloud detection |
| Lakera Guard [14] | Classifier | No | SaaS/self-host | Acquired by Check Point ~$300M (Sep 2025) | Injection-first |
| Portkey / Prisma AIRS AI Gateway [15][16] | Guardrail plugins | Plugin-dependent | Gateway | Acquired by Palo Alto (May 2026) | No user-side key custody |
| Cloudflare AI Gateway [17] | Llama Guard + DLP | No | Edge | Public | Sees plaintext |
| Kong AI PII Sanitizer [18] | External anonymizer | Optional restoration | Enterprise gateway | Public | No cross-session/agent consistency |
| LiteLLM + Presidio [19][20] | Presidio | Yes, but bugs on Anthropic path and tool-call args | OSS proxy | OSS | Brittle across tool calls |
| Microsoft Presidio [21] | spaCy + regex | Yes (encrypt/decrypt) | Library | OSS | Building block |
| AWS Bedrock Guardrails [22] | ML + regex | No (one-way placeholders) | Bedrock only | Public | **Does not evaluate tool-call args, results, or definitions** |
| Google SDP + Model Armor [23][24] | SDP infoTypes | Yes, deterministic crypto tokens | Google Cloud | Public | Google sees plaintext |
| LLM Guard (Protect AI → Palo Alto) [31] | Presidio-based | Yes, Vault + Deanonymize | OSS | OSS | Single-session, no MCP |
| Strac [32] | Classifier | Mostly one-way on MCP | SaaS MCP gateway | Private | Not reversible by design |
| Apple PCC [40][41] | n/a (TEE) | n/a | Apple + Google Cloud since Jun 2026 | Big tech | Apple stack only |
| Privatemode (Edgeless) [42] | n/a (TEE) | n/a | API €0.43/M tokens | Private | Open-weight only |
| Tinfoil [43][44] | n/a (TEE, NVIDIA CC) | n/a | Consumer chat + API | YC X25 | Open-weight only; positions *against* redaction |
| Confer [45][46] | n/a (E2EE + TEE) | n/a | Consumer app | Launched Jan 2026 | No frontier closed models |
| Duck.ai / Brave Leo [47] | IP-stripping proxy | n/a | Free | Big/mid | Forward plaintext prompts |
| OSS proxies & extensions [49]–[54] | Presidio/GLiNER/Gemini Nano | Mostly yes, per-session | Local | Hobby-scale | No swarm consistency, no compliance posture |

Notes: Kong's restoration flag shows gateways absorb reversibility as a feature. Bedrock documents that its PII filter does not evaluate `toolUse.input`, `toolResult`, or `toolSpec` [22]. `daslabhq/pii-proxy` is the closest OSS prototype (regex + GLiNER/Ollama, bijective session mapping, MIT, 7 stars) [49]. No YC company found doing reversible PII tokenization as a gateway; adjacent: Tinfoil (X25), PromptArmor, Alter (S25), Evervault (S18) [55]. Incumbents entering MCP governance: Proofpoint, Snowflake Cortex AI Gateway, MintMCP, Lasso ($30M A, Sep 2026) [56][57][58].

## 2. Standards and compliance hooks

- **GDPR pseudonymization (Art. 4(5), Rec. 26).** EDPB Guidelines 01/2025 restate pseudonymised data remains personal data for anyone who can link it [59]. **CJEU *EDPS v SRB* (C-413/23 P, Sep 4 2025): identifiability is assessed from the recipient's perspective**; if the recipient lacks reasonable means to re-identify, the data may not be personal data for that recipient [60][61]. Strongest legal hook for on-device keys. Caveat: residual quasi-identifiers.
- **HIPAA Safe Harbor**: 18 identifiers [62]. Free-text medical facts are not identifiers; including them is a product choice.
- **PCI DSS Tokenization Guidelines** [63]; vaultless FF1/FF3-1 (NIST SP 800-38G Rev. 1) works for numbers, not names [64][65].
- **EU AI Act**: general application Aug 2 2026; Digital Omnibus pushed Annex III high-risk to Dec 2 2027 [66][67]. Data minimization comes from GDPR Art. 5(1)(c).
- **Assurance**: ISO/IEC 42001 [68]; NIST AI RMF [69]; CSA AI Controls Matrix v1.1 (Jul 2026; 247 controls) and STAR for AI 42001 [70][71]; HITRUST AI Security Assessment [72]; BSI C5:2026 includes confidential-computing/attestation criteria [42]. SOC 2 has no AI-specific criteria. No formal government AI trust mark exists.

## 3. Provider data policies (2026)

| Provider | API | Consumer |
|---|---|---|
| OpenAI | 30-day abuse logs by default; ZDR only via Enterprise Agreement [73]. Court preservation order (May–Oct 2025); ~20M logs ordered produced [74][75][76] | Training on by default; **Memory + "Dreaming V3" (Jun 2026)** builds a persistent self-updating profile; disabling training does not disable memory [77][78] |
| Anthropic | Not retained by default; ZDR by arrangement. **Covered Models (Fable 5/5.1, Mythos 5/5.1) require 30-day retention, ZDR unavailable** (since Jun 2026); flagged content up to 2 years [79][80] | Since Sep 2025 training opt-out; if on, retention up to 5 years [81] |
| Google | Paid API not used for training; free tier is, with human review [82] | Gemini Apps Activity on by default; Personal Intelligence (Jan 2026) reasons across Gmail/Photos/Search [78] |
| xAI | 30-day retention [83] | Training on by default; employees may access chats [83] |
| Meta | — | Trains on interactions; keystroke/screenshot initiative paused Jun 2026 [84] |

Trend: more provider-side retention for frontier models and richer memory profiles, not less.

## 4. Technical prior art

**Detection (local-capable):** OpenAI Privacy Filter (1.5B/50M active, Apache 2.0, 8 categories, English-first, 257-token window, "not a standalone anonymization guarantee") [1][85]; GLiNER2-PII (0.3B, 42 types) and Knowledgator gliner-pii edge/small/base/large with ONNX INT8 [2][86]; DeBERTa on ai4privacy (F1 0.976) [87]; Presidio [21].

**Reversible mapping:** Presidio encrypt/decrypt; LangChain PresidioReversibleAnonymizer [88]; LLM Guard Vault [31]; LiteLLM output_parse_pii [19]; Kong restoration [18]; Google SDP deterministic tokens [23]; FF1/FF3-1 [64].

**Papers:** HaS (2023) [89]; PAPILLON (NAACL 2025) + PUPA benchmark, PrivacyPAD [90][91]; Rescriber (CHI 2025): Llama3-8B on-device detection on par with GPT-4o [92]; Casper [93]; ProPILE [94]; InferDPT [95].
- **Utility loss:** *On the Impact of Anonymization on LLM Performance* (Sep 2026): reversible, uniqueness-preserving anonymization beats redaction, but retrieval tasks show "catastrophic decline"; **more capable models suffer larger drops** [96]. *Need to Know* / DelegateCI-Bench (Jun 2026): type-based redaction over-discloses and over-removes [97].
- **Re-identification:** AURA (May 2026): web-search agents re-identify from weak cues [98]. RedactionBench (Jun 2026): humans agree only 47.7% on contextual redactions [99]. Also [100]–[103].
- **Agentic leakage:** AgentLeak [104]; PrivacyChecker cut MCP+A2A leak rate 24.3% → 6.7% [105]; MCPHunt [106]; MCP server logs hold PII [107]; Ghost Tool Calls [108]; AgenTEE [109].
- **Contextual integrity:** AirGapAgent, PrivacyLens, CI-Bench, CI-Work (Apr 2026), POLAR-Bench, PrivacyAlign [110]–[112].

## 5. Market signal

- Cyberhaven 2026: 39.7% of enterprise AI interactions involve sensitive data (34.8% in 2025, 10.7% two years earlier); one-third use personal accounts [113][114].
- IBM Cost of a Data Breach 2025: 20% of breaches involved shadow AI, +$670K per breach [115][116].
- Samsung: 2023 ban → Jun 2026 rollout of ChatGPT Enterprise to all Korea employees [117][118]. Enterprises resolve fear with contracts.
- Gartner (Aug 2026): securing-AI market $4.8B in 2027; **AI gateway segment only $251M (2026) → $429M (2027)** [119].
- Consolidation: Check Point–Lakera, SentinelOne–Prompt, Palo Alto–Protect AI/Portkey, Cato–Aim, F5–SurePath, Akamai–LayerX, NVIDIA–Gretel, Databricks–Antimatter. Fresh money: HiddenLayer $100M B, Lasso $30M A, Noma $100M B, Wald.ai $4M seed.

## 6. Differentiated vs not

**Differentiated:** (1) device/org-side key custody + swarm-wide consistency with detokenization at the tool boundary; (2) tool-call coverage is a documented hole (Bedrock docs, LiteLLM bugs, MCPHunt/AgentLeak); (3) CJEU *EDPS v SRB* legal posture unexploited; (4) scope beyond NER (relationships, employer, health, contextual-integrity rewriting).

**Not differentiated / overreach:** (1) detection is a commodity; (2) reversible tokenization is old prior art; (3) "near-zero intelligence loss" unsupported for retrieval/knowledge/date-math tasks, stronger models degrade more; (4) "cannot be profiled" not achievable with consistent pseudonyms alone (PERSON_1 profile); per-context rotation trades utility; (5) TEE camp attacks the same fear with a stronger promise, limited to open weights; (6) consumer willingness to pay weak; memory is the feature users want; (7) enterprise consolidating into platforms; standalone gateway market small; (8) multimodal/code unaddressed.

**Honest positioning:** the privacy substrate for agent swarms (tool-boundary detokenization, swarm-consistent mapping, contextual-integrity rewriting, on-device keys with a CJEU-grounded legal story), not "anonymize ChatGPT."

## Citations

1. https://openai.com/index/introducing-openai-privacy-filter/
2. https://arxiv.org/abs/2605.09973
3. https://www.getlimina.ai/en/blog/private-ai-rebrands-limina-sensitive-data-privacy
4. https://www.getlimina.ai/en
5. https://www.protecto.ai/
6. https://www.skyflow.com/product/llm-privacy-vault
7. https://docs.skyflow.com/docs/fundamentals/patterns/llm-privacy
8. https://witness.ai/blog/pii-protection/
9. https://witness.ai/
10. https://wald.ai/
11. https://www.securityweek.com/wald-ai-raises-4m-in-seed-funding-to-protect-data-in-conversations-with-ai-assistants/
12. https://www.nightfall.ai/firewall-for-ai
13. https://www.nightfall.ai/blog/ai-agent-identity-authorization
14. https://www.checkpoint.com/press-releases/check-point-acquires-lakera-to-deliver-end-to-end-ai-security-for-enterprises/
15. https://www.paloaltonetworks.com/company/press/2026/palo-alto-networks-completes-acquisition-of-portkey-to-secure-ai-agents
16. https://www.paloaltonetworks.com/blog/2026/07/announcing-general-availability-of-prisma-airs-ai-gateway/
17. https://blog.cloudflare.com/guardrails-in-ai-gateway/
18. https://developer.konghq.com/plugins/ai-sanitizer/
19. https://docs.litellm.ai/docs/proxy/guardrails/pii_masking_v2
20. https://github.com/BerriAI/litellm/issues/22821 ; https://github.com/BerriAI/litellm/pull/32014
21. https://github.com/microsoft/presidio/tree/main/presidio-anonymizer
22. https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-sensitive-filters.html
23. https://docs.cloud.google.com/sensitive-data-protection/docs/pseudonymization
24. https://cloud.google.com/security/products/model-armor
25. https://siliconangle.com/2026/05/04/opaque-buys-post-quantum-cryptographic-ai-tech-abu-dhabis-tii/
26. https://techcrunch.com/2026/03/24/databricks-buys-two-startups-lakewatch-antimatter-siftd-ai-security/
27. https://www.sentinelone.com/press/sentinelone-to-acquire-prompt-security-to-advance-genai-security/
28. https://techcrunch.com/2026/09/02/hiddenlayer-nabs-100m-as-enterprises-rush-to-secure-their-ai-deployments/
29. https://www.enkryptai.com/
30. https://shield.docs.arthur.ai/docs/pii-leakage
31. https://appsecsanta.com/llm-guard
32. https://www.strac.io/blog/mcp-gateway
33. https://docs.piiano.com/api/operations/tokenize
34. https://evervault.com/solutions/pii
35. https://www.tonic.ai/press-releases/tonic-announces-unstructured-data-catalog-for-tonic-textual
36. https://techcrunch.com/2025/03/19/nvidia-reportedly-acquires-synthetic-data-startup-gretel
37. https://dualitytech.com/blog/llm-data-privacy/
38. https://www.harmonic.security/
39. https://aurascape.ai/answers/ai-security-landscape-2026/
40. https://www.infoq.com/news/2026/07/apple-pcc-google-cloud/
41. https://security.apple.com/blog/private-cloud-compute/
42. https://www.privatemode.ai/pricing ; https://www.privatemode.ai/blog
43. https://www.ycombinator.com/launches/NZ8-tinfoil-verifiable-privacy-for-cloud-ai
44. https://next.redhat.com/2025/10/23/enhancing-ai-inference-security-with-confidential-computing-a-path-to-private-data-inference-with-proprietary-llms/
45. https://confer.to/blog/
46. https://www.webpronews.com/signal-founder-moxie-marlinspike-launches-encrypted-ai-assistant-confer/
47. https://www.evenfall.ai/guides/best-private-ai-chat-apps-2026
48. https://github.com/zylon-ai/private-gpt
49. https://github.com/daslabhq/pii-proxy
50. https://github.com/francesco-stimola/llm-proxy-pii-rust
51. https://github.com/ma2za/pseudonymize
52. https://philterd.ai/philter-ai-proxy/
53. https://github.com/kaispriestersbach/pii-shield-extension
54. https://github.com/Mr-Neutr0n/pii-guard ; https://github.com/gacabartosz/presidio-local-anonymizer ; https://github.com/akazah/prompt-anonymizer ; https://anonym.legal/features/chrome-extension
55. https://www.ycombinator.com/companies/tinfoil ; https://www.ycombinator.com/companies/promptarmor
56. https://www.proofpoint.com/us/blog/corporate-news/stop-ai-agents-losing-data
57. https://www.snowflake.com/en/blog/enterprise-ai-security-agentic-mcp-governance/
58. https://siliconangle.com/2026/09/02/lasso-security-launches-cpu-only-ai-guardrail-raises-30m/
59. https://www.edpb.europa.eu/system/files/2025-01/edpb_guidelines_202501_pseudonymisation_en.pdf
60. https://curia.europa.eu/site/upload/docs/application/pdf/2025-09/cp250107en.pdf
61. https://fpf.org/blog/rethinking-personal-data-the-cjeus-contextual-turn-in-edps-vs-srb/
62. https://www.accountablehq.com/post/complete-list-of-the-18-hipaa-identifiers-for-de-identification-safe-harbor
63. https://www.pcisecuritystandards.org/documents/Tokenization_Guidelines_Info_Supplement.pdf
64. https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-38Gr1-draft.pdf
65. https://www.fortanix.com/blog/legacy-vaulted-tokenization-vs-vaultless-format-preserving-encryption-fpe
66. https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/
67. https://www.praxikon.com/en/posts/digital-omnibus-high-risk-postponement-december-2027
68. https://insights.pecb.com/iso-certification-ai-trust/
69. https://www.nist.gov/itl/ai-risk-management-framework
70. https://cloudsecurityalliance.org/blog/2026/07/14/ai-controls-matrix-v1-1-strengthening-the-foundation-for-trustworthy-ai
71. https://cloudsecurityalliance.org/blog/2025/08/20/announcing-the-ai-controls-matrix-and-iso-iec-42001-mapping-and-the-roadmap-to-star-for-ai-42001
72. https://hitrustalliance.net/assessments-and-certifications/aisecurityassessment
73. https://developers.openai.com/api/docs/guides/your-data
74. https://openai.com/index/response-to-nyt-data-demands/
75. https://startupnews.fyi/2025/10/12/openai-no-longer-has-to-preserve-all-of-its-chatgpt-data-with-some-exceptions/
76. https://natlawreview.com/article/openai-loses-privacy-gambit-20-million-chatgpt-logs-likely-headed-copyright
77. https://openai.com/index/chatgpt-memory-dreaming/
78. https://www.aipolicydesk.com/blog/chatgpt-memory-dreaming-v3-privacy-governance-2026
79. https://platform.claude.com/docs/en/manage-claude/api-and-data-retention
80. https://support.claude.com/en/articles/15425996-data-retention-practices-for-covered-models
81. https://www.anthropic.com/news/updates-to-our-consumer-terms
82. https://meetily.ai/llm-privacy/gemini
83. https://meetily.ai/llm-privacy/xai
84. https://www.techtarget.com/searchcio/feature/Metas-AI-training-with-keystrokes-Progress-or-privacy-issue
85. https://huggingface.co/openai/privacy-filter
86. https://huggingface.co/knowledgator/gliner-pii-edge-v1.0 ; https://grepture.com/blog/best-open-source-models-pii-redaction
87. https://arxiv.org/pdf/2605.25816
88. https://python.langchain.com/api_reference/experimental/data_anonymizer/langchain_experimental.data_anonymizer.presidio.PresidioReversibleAnonymizer.html
89. https://arxiv.org/abs/2309.03057
90. https://aclanthology.org/2025.naacl-long.173/
91. https://github.com/Columbia-NLP-Lab/PAPILLON
92. https://arxiv.org/abs/2410.11876
93. https://www.researchgate.net/publication/398265736_Casper_Prompt_Sanitization_for_Protecting_User_Privacy_in_Web-Based_Large_Language_Models
94. https://arxiv.org/abs/2307.01881
95. https://arxiv.org/abs/2310.12214
96. https://arxiv.org/html/2609.11335
97. https://arxiv.org/abs/2606.04067
98. https://arxiv.org/abs/2605.30848
99. https://arxiv.org/abs/2606.18782
100. https://arxiv.org/pdf/2402.13846
101. https://arxiv.org/pdf/2602.12806
102. https://direct.mit.edu/coli/article/48/4/1053/112770/
103. https://arxiv.org/pdf/2604.21211
104. https://arxiv.org/pdf/2512.16310
105. https://arxiv.org/pdf/2509.17488
106. https://arxiv.org/pdf/2604.27819
107. https://arxiv.org/html/2606.21338v1
108. https://arxiv.org/pdf/2606.02483
109. https://arxiv.org/pdf/2604.18231
110. https://arxiv.org/html/2605.19127
111. https://arxiv.org/pdf/2604.21308
112. https://arxiv.org/html/2606.21710v1
113. https://www.cyberhaven.com/blog/sensitive-data-flowing-into-ai-tools
114. https://www.cyberhaven.com/press-releases/cyberhaven-2026-ai-adoption-risk-report
115. https://www.ibm.com/think/x-force/2025-cost-of-a-data-breach-navigating-ai
116. https://passwork.pro/blog/cost-data-breach-2026-ai-threat/
117. https://www.upi.com/amp/Top_News/World-News/2026/06/22/samsung-electronics-openai-chatgpt/6391782171192/
118. https://www.forbes.com/sites/siladityaray/2023/05/02/samsung-bans-chatgpt-and-other-chatbots-for-employees-after-sensitive-code-leak/
119. https://www.gartner.com/en/newsroom/press-releases/2026-08-26-gartner-forecasts-the-market-for-securing-ai-will-reach-almost-5-billion-in-2027
120. https://www.securityweek.com/cato-networks-acquires-ai-security-firm-aim-security/
121. https://noma.security/blog/noma-security-raises-100m-to-drive-adoption-of-ai-agent-security
122. https://siliconangle.com/2025/04/08/aurascape-launches-50m-funding-bring-security-observability-ai-apps/

Caveats: Tinfoil's "$504M raised" figure is not credible; treat as seed. The IBM 2026 "43%" shadow-AI figure is from a secondary blog. Google/xAI policy summaries are from secondary aggregators.
