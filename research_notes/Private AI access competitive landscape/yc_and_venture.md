# YC and venture-funded startups offering private, anonymous or non-profiling access to AI models (2024-2026), and what the funding record says about fundability

Research date: 7 October 2026. Method note: I enumerated YC companies offline from the yc-oss mirror of the YC directory ([yc-oss all.json](https://yc-oss.github.io/api/companies/all.json), downloaded 2026-10-07). The snapshot has 1,950 companies across W24, S24, F24, W25, X25 (Spring 2025), S25, F25, W26, X26 (Spring 2026), S26 and F26. F26 shows 118 companies, so it may be incomplete. I ran regex passes over one-liners, long descriptions and tags. Terms: privacy, private, anonym, confidential, enclave, TEE, attestation, PII, redact, encrypt, gateway, DLP, data leak, shadow AI, on-device, local-first, self-host, sovereign, personal context, memory layer. I also checked the W23/S23 starting points. Every hit was then checked against its YC profile page. I did not query api.ycombinator.com directly; yc-oss mirrors the same directory data.

---

## Which YC companies are closest to "anonymous access to frontier models for institutions and consumers"? Is anyone already doing the pooled-anonymity model?

### Takeaway
No YC company in W24 to F26 runs a pooled-anonymity proxy in front of GPT, Claude or Gemini. The nearest YC companies each cover one piece:
- **Tinfoil (X25):** confidential inference on open-weight models only.
- **LogosGuard (F25):** client-side redaction of prompts sent to frontier chatbots. It protects content, not identity.
- **Unbound (S24):** enterprise AI gateway for data-leak prevention. It runs under the enterprise's own identity.
- **Egoist Machines (S26):** user-owned portable context.

The pooled frontier-proxy model already exists outside YC. Venice.ai routes encrypted requests "through external proxies to access OpenAI and Anthropic models anonymously" and raised $65M at a $1B valuation in July 2026. DuckDuckGo's Duck.ai does the same with an anonymizing proxy and contractual no-training terms.

### Cited Findings

**How sparse the category is in YC**
- The yc-oss snapshot has 1,950 companies across the 11 target batches. Only about 4 directly sell private or anonymous access to AI models or to the prompts sent to them: Tinfoil, LogosGuard, Unbound and Egoist Machines. About 10 more are adjacent (listed below). — [yc-oss dataset](https://yc-oss.github.io/api/companies/all.json) (my count; method above)
- In the yc-oss data, YC's "Privacy" industry tag covers only Tinfoil, Unbound, Clearly AI, Egoist Machines and Petrarch in the target batches. Before them: Blyss (W23), Dynamo AI (W22), Optery (W22) and Reality Defender (W22). — [yc-oss dataset](https://yc-oss.github.io/api/companies/all.json); [YC Privacy industry page](https://www.ycombinator.com/companies/industry/privacy)

**Core YC profiles (direct private or anonymous AI access)**

- **Tinfoil (X25 / Spring 2025, San Francisco, team of 5, active)**
  - Product: "Encrypted AI with verifiable privacy." It runs inference on NVIDIA Hopper/Blackwell confidential-computing GPUs so that "we can't see and don't log your queries" is provable, "not even by Tinfoil or the cloud provider." — [YC profile](https://www.ycombinator.com/companies/tinfoil)
  - Founders: Tanya (Cloudflare cryptography team), Sacha (MIT PhD, privacy-preserving cryptography), Jules (MIT PhD, trusted hardware; worked with NVIDIA and Microsoft Research) and Nate (Tor). — [Launch HN mirror](https://hn.nuxt.dev/item/43996555)
  - Launch HN, May 15, 2025: free chat with limits, $20/month unlimited, OpenAI-compatible API at $2 per 1M tokens, custom Docker deployments. Targets were sensitive-document analysis, proprietary code copilots and AI apps processing user data. The server code is AGPL, and founders said the moat is "UX/tooling, not IP." — [Launch HN](https://news.ycombinator.com/item?id=43996555)
  - Current models are open-weight only (DeepSeek V4, Gemma 4, Kimi K2.6, GLM 5.1). Chat is $20/month and the API comes with $5 of free credit. — [Launch HN mirror / product listing](https://hn.nuxt.dev/item/43996555)
  - The blog from Aug 2025 to Sep 2026 lists only open-weight launches (gpt-oss-120b, qwen3-coder-480B). There is no closed frontier model and no funding or customer announcement. — [Tinfoil blog](https://tinfoil.sh/blog)
  - June 2026 post proposes "Verifiable Clean Rooms," in which a lab supplies weights and an auditor supplies evals. This is a frontier-lab-facing use case, not anonymous access to frontier models. — [Tinfoil blog post](https://tinfoil.sh/blog/2026-06-09-auditing-frontier-model-without-weights)
- **LogosGuard (F25, San Francisco, team of 2)**
  - YC one-liner: "The sensitive data redaction layer for AI… redacts your private information before the prompt ever leaves your device," for ChatGPT, Claude and Gemini. — [yc-oss dataset / YC profile](https://www.ycombinator.com/companies/logosguard)
  - Founders: Sukrut Oak and Abel John, both Stanford CS BS/MS and ex-Apple AI engineers. — [YC profile](https://www.ycombinator.com/companies/logosguard)
  - The homepage sells a local browser extension: "No account, no sign-up, no servers." It replaces names and account numbers with placeholders across ChatGPT, Claude, Gemini, Copilot, Perplexity and Grok. — [logosguard.com](https://logosguard.com/)
  - **Conflict:** my fetch of the YC profile summarized it as an enterprise "AI governance and assessment platform" (NIST AI RMF and ISO 42001 control baselines, PII-handling evals). That may be a launch post or a broadening toward enterprise governance; the homepage still sells redaction. — [YC profile](https://www.ycombinator.com/companies/logosguard) vs [logosguard.com](https://logosguard.com/)
- **Unbound (S24, San Francisco, team of 7)**
  - "Use AI tools without fear of data leakage." It discovers which AI apps employees use, sets access policies, and monitors and blocks prompts that carry confidential data. The YC page cites the figure that "over 55% of all prompts contain some form of PII." — [YC profile](https://www.ycombinator.com/companies/unbound)
  - The AI Gateway plugs into Cursor, Roo, Cline and internal copilots for real-time protection, model routing and usage analytics. — [Pulse 2.0](https://pulse2.com/unbound-4-million-raised-for-helping-enterprises-with-ai-tools)
  - Founders: Rajaram Srinivasan (ex-Palo Alto Networks and Imperva data security) and Vignesh Subbiah. — [Pulse 2.0](https://pulse2.com/unbound-4-million-raised-for-helping-enterprises-with-ai-tools)
- **Egoist Machines (S26, San Francisco, team of 2, founded 2026)**
  - Product: "AI Passport," a user-controlled portable profile of personal context that moves across ChatGPT, Claude and other apps. Apps authenticate through OAuth-style "Sign in with AI Passport," which grants scoped, time-limited, revocable access. The backend uses per-user isolated memory stores with "cryptographic access control at the memory layer." Planned: a local hardware device ("Digital Domovoy"). — [YC profile](https://www.ycombinator.com/companies/egoist-machines)
  - Founders: Erin Meryl McGurk (Cambridge Land Economy; built a 1M+ social following; advised OpenAI on social strategy) and Dr. David Khachaturov (Cambridge CS PhD, ex-OpenAI ML researcher on PaperBench). — [YC profile](https://www.ycombinator.com/companies/egoist-machines)
- **Caution (S26, listed in George Town, Cayman Islands, team of 5, founded 2025)**
  - A hosting platform that deploys workloads to secure enclaves "in minutes." It produces cryptographic proof that production runs the exact reviewed source, build, configuration and runtime. — [yc-oss / YC profile](https://www.ycombinator.com/companies/caution)
  - The platform is fully open source. AWS Nitro Enclaves are supported today; Intel TDX, AMD SEV-SNP, TPM 2.0 and NVIDIA CC are in development. Customers include crypto infrastructure, digital-asset lending and "private AI inference." — [YC profile](https://www.ycombinator.com/companies/caution)
  - Founders: Anton Livaja (co-founder of Distrust), Lance Vick (ex-security lead at Turnkey, BitGo, Unit 410 and Pebble; founder of the Stagex Linux distro) and Ksenia Lesko. — [YC profile](https://www.ycombinator.com/companies/caution)
- **Credal.ai (W23, New York, team of 14)**
  - Now "The Control Plane for Enterprise Agents." — [YC profile](https://www.ycombinator.com/companies/credal-ai)
  - Its 2023 positioning was a secure bridge from enterprise data to cloud LLMs: automatic redaction and anonymization before sending, audit logs per LLM provider, and permission mirroring. — [TechCrunch, Oct 2023](https://techcrunch.com/2023/10/26/credal-aims-to-connect-company-data-to-llms-securely/)
- **Blyss (W23, inactive)**
  - "End-to-end encrypted AI." It ran AI workloads in GPU secure enclaves with an on-prem-like privacy model, and pitched itself as Signal/WhatsApp for AI. — [YC profile](https://www.ycombinator.com/companies/blyss)
  - Founders: Samir Menon and Neil Movva. It used NVIDIA Hopper and AMD Genoa enclaves. — [Extruct](https://www.extruct.ai/hub/blyss-dev/)

**Adjacent YC companies (privacy for AI, but not anonymous model access)**
- Candor (W25): agentic DLP and insider risk; catches employees sharing sensitive data with third parties. — [YC profile](https://www.ycombinator.com/companies/candor-security)
- Golf (X25): visibility into shadow AI and control over agents and MCP. — [YC profile](https://www.ycombinator.com/companies/golf)
- compliant-llm (W23): detects data leaks into third-party GenAI tools by monitoring employee interactions. — [YC profile](https://www.ycombinator.com/companies/compliant-llm)
- Galini (F24): compliance guardrails as a service. — [YC profile](https://www.ycombinator.com/companies/galini)
- Inth (X26, London): catches product privacy-compliance issues in PRs, code and websites. — [YC profile](https://www.ycombinator.com/companies/inth)
- Clearly AI (S24): automates security and privacy reviews. — [YC profile](https://www.ycombinator.com/companies/clearly-ai)
- On-device or local inference:
  - Sentient OS (F26): a local LLM on the Mac; cloud inference over your whole life is called "a privacy nightmare." — [YC profile](https://www.ycombinator.com/companies/sentient-os)
  - RunAnywhere (W26): open models on-prem, BYOC or on-device "so code and data never leave their network." — [YC profile](https://www.ycombinator.com/companies/runanywhere)
  - Cactus Compute (S25): on-device AI for phones and wearables. — [YC profile](https://www.ycombinator.com/companies/cactus-compute)
- Local-first, user-owned memory:
  - Epicenter (S25): "ChatGPT's memory feature in an open, portable format," stored as local plain text and SQLite. — [YC profile](https://www.ycombinator.com/companies/epicenter)
  - Skillsync (W26): portable agent sessions; "nothing leaves unless you choose." — [YC profile](https://www.ycombinator.com/companies/skillsync)
- AI gateways without a privacy-first pitch: Respan (W24, observability plus gateway; 2T+ tokens/month), Codag (S26), Experiential Labs (S26, open-source gateway) and LiteLLM (W23). — [Respan](https://www.ycombinator.com/companies/respan), [Codag](https://www.ycombinator.com/companies/codag), [Experiential Labs](https://www.ycombinator.com/companies/experiential-labs), [LiteLLM](https://www.ycombinator.com/companies/litellm)
- Agent identity and permissions (adjacent to "identity for AI"): Multifactor (F25), Alter (S25), Agentic Fabriq (W26). — [Multifactor](https://www.ycombinator.com/companies/multifactor), [Alter](https://www.ycombinator.com/companies/alter), [Agentic Fabriq](https://www.ycombinator.com/companies/agentic-fabriq)

**Who already runs a pooled-anonymity proxy for frontier models (non-YC)**
- **Venice.ai.** It "encrypts user requests before routing them through external proxies to access OpenAI and Anthropic models anonymously." It does not store prompts, offers end-to-end encryption on paid plans, and lists 200+ models. — [The Block](https://www.theblock.co/post/406934/venice-ai-funding-equity-valuation-dragonfly); [TechCrunch](https://techcrunch.com/2026/07/01/venice-ai-becomes-a-unicorn-with-65m-series-a-as-its-privacy-first-ai-platform-takes-off/)
- **Duck.ai (DuckDuckGo).**
  - Every conversation passes through DuckDuckGo's anonymizing proxy, which strips identifying information. No account is needed, history stays on the device, and OpenAI and Anthropic are contractually barred from training on the chats. — [CyberInsider](https://cyberinsider.com/duckduckgo-makes-privacy-respecting-ai-chat-service-widely-available/)
  - Search snippets say paid Plus and Pro tiers exist, with Pro giving access to Claude Opus 4.6. This is uncertain: I could not tie it to a specific primary page. — [DuckDuckGo Spread Privacy blog (AI tag)](https://spreadprivacy.com/tag/ai/)
- **NEAR AI** (protocol-funded, not a classic venture startup).
  - Private Chat and NEAR AI Cloud launched in December 2025 on Intel TDX and NVIDIA CC. — [NEAR AI blog](https://near.ai/blog/introducing-near-ai-cloud-private-chat)
  - In March 2026 it integrated with Venice.ai for private text and image inference, and it added staking-based payment for confidential inference. — [NEAR AI blog](https://near.ai/blog); [NEAR AI staking](https://near.ai/blog/staking-for-near-ai)

### Inferences
- Lethe's thesis is to pool many users' or firms' queries under one intermediary identity so the frontier provider cannot profile any individual or firm. Venice and Duck.ai have proven that consumer version, with big-name traffic behind it. Inside YC the slot is open; outside YC it is not.
- YC's privacy bets split into three camps:
  - Cryptographic or hardware infra: Tinfoil, Caution, and Blyss before them.
  - Content redaction and data-leak prevention: LogosGuard, Unbound, Candor, compliant-llm.
  - User-owned context: Egoist, Epicenter, Skillsync.
  
  None combines identity-unlinkability with frontier-model quality. A privacy-pool pitch can present itself as the missing fourth camp.
- Tinfoil is the YC team closest in spirit. Its explicit choice of open-weight models in enclaves is the opposite trade-off from a frontier-model pool: verifiable privacy, but no frontier models. LogosGuard is complementary rather than competitive: it hides content but not who is asking.
- For institutions, no one found here anonymizes firm identity toward the provider. Credal and Unbound route traffic under the enterprise's own contracts and keys. Opaque and Confident Security wrap inference engines rather than pool callers. This "institutional pool" angle appears unoccupied.

### Gaps
- YC directory descriptions are self-reported and some are empty (for example Unbound's long description), so a keyword sweep can miss stealthy or vaguely described companies. F26 may be incomplete in the snapshot.
- I could not confirm whether LogosGuard has pivoted (the sources conflict).
- I found no public data on what share of Venice's usage or revenue comes from proxied closed models versus hosted open models.
- I did not verify Duck.ai's paid-tier details against a primary DuckDuckGo page.

---

## What did investors fund, and what traction did those companies show at raise time?

### Takeaway
Money has gone to three shapes:
1. **Consumer private AI with real revenue, funded by crypto investors.** Venice: $65M Series A at $1B, profitable, $70M+ annualized revenue.
2. **Enterprise confidential-AI platforms with blue-chip customers.** Opaque: $24M Series B at $300M, customers include ServiceNow, Anthropic and Accenture.
3. **Enterprise AI data-leak gateways.** WitnessAI $58M; Harmonic $17.5M; Prompt Security and Aim Security acquired for roughly $250-375M.

Pure confidential-inference startups (Confident Security $4.2M; Unbound $4M; Credal $4.8M seed; Tinfoil with no disclosed priced round) have raised only seed-sized amounts.

### Cited Findings

**Non-YC rounds, 2025-2026**
- **Venice.ai, Series A, July 1, 2026: $65M at a $1B equity valuation.**
  - Investors: lead Dragonfly, with North Island Ventures, Coinbase Ventures, F-Prime, Archetype, Liquid2 Ventures and Morgan Creek. — [The Block](https://www.theblock.co/post/406934/venice-ai-funding-equity-valuation-dragonfly); [TechCrunch](https://techcrunch.com/2026/07/01/venice-ai-becomes-a-unicorn-with-65m-series-a-as-its-privacy-first-ai-platform-takes-off/)
  - Terms: 8.98% equity, a vesting grant of 1.5M VVV tokens, and warrants on 5M VVV over 8 years. Total potential capital is $131.5M if the warrants are exercised. — [The Block](https://www.theblock.co/post/406934/venice-ai-funding-equity-valuation-dragonfly)
  - Traction at raise:
    - $70M+ annualized run-rate revenue; profitable since Q1. — [The Block](https://www.theblock.co/post/406934/venice-ai-funding-equity-valuation-dragonfly)
    - Users reported three ways: "3+ million active users" ([TechCrunch](https://techcrunch.com/2026/07/01/venice-ai-becomes-a-unicorn-with-65m-series-a-as-its-privacy-first-ai-platform-takes-off/)), "3 million users (as of April)" ([The Block](https://www.theblock.co/post/406934/venice-ai-funding-equity-valuation-dragonfly)), and "3.5M+ registered users" in search snippets. The figures conflict slightly.
    - 1.7M API calls per day; about 8% of users pay in crypto. — [TechCrunch](https://techcrunch.com/2026/07/01/venice-ai-becomes-a-unicorn-with-65m-series-a-as-its-privacy-first-ai-platform-takes-off/)
  - Business model: freemium subscription plus API. The VVV token launched in January 2026 and DIEM in August 2025; staking VVV mints DIEM worth "$1 worth of AI credits per day." Planned use of funds: buy GPUs and build its own data centers. — [TechCrunch](https://techcrunch.com/2026/07/01/venice-ai-becomes-a-unicorn-with-65m-series-a-as-its-privacy-first-ai-platform-takes-off/)
  - This was Venice's first outside round. The company says "most pre-sell to VCs… and promise to build a product or find users later," and that it did the opposite. — [The Block](https://www.theblock.co/post/406934/venice-ai-funding-equity-valuation-dragonfly)
  - Positioning is "private and uncensored." — [SiliconANGLE](https://siliconangle.com/2026/07/01/venice-raises-65m-1b-valuation-private-uncensored-ai/)
- **OPAQUE, Series B, Feb 12, 2026: $24M at about $300M post-money.**
  - Investors: lead Walden Catalyst; returning Intel Capital, Race Capital, Storm Ventures and Thomvest; new backer ATRC. Total raised is $55.5M. — [PR Newswire](https://www.prnewswire.com/news-releases/opaque-raises-24m-series-b-at-300m-valuation-to-advance-confidential-ai-for-the-enterprise-302685635.html)
  - Customers and partners named: ServiceNow, Anthropic, Encore Capital and Accenture. No ARR was disclosed. It spun out of UC Berkeley's RISELab. — [PR Newswire](https://www.prnewswire.com/news-releases/opaque-raises-24m-series-b-at-300m-valuation-to-advance-confidential-ai-for-the-enterprise-302685635.html); [Unite.AI](https://www.unite.ai/opaque-secures-24m-in-series-b-at-a-300-million-valuation-to-push-confidential-ai-forward/)
- **Confident Security, seed, closed July 18, 2025: $4.2M** from Decibel, South Park Commons, Ex Ante and Swyx.
  - CONFSEC is "an enterprise-level implementation of Apple's Private Cloud Compute" that lets LLM providers, hyperscalers, governments and enterprises wrap inference engines. Pitched as "the Signal for AI." CEO: Jonathan Mortensen. — [FinSMEs](https://www.finsmes.com/2025/07/confident-security-raises-4-2m-in-funding.html); [Pulse 2.0](https://pulse2.com/confident-security-4-2-million-raised-to-enable-provably-private-ai-interactions)
  - No traction metrics were disclosed at raise; the company came out of stealth with the round.
- **Zama (FHE), Series B, June 25, 2025: $57M at $1B+.** Co-led by Blockchange Ventures and Pantera Capital; total raised is $150M+. Billed as the "first FHE unicorn"; positioned on encryption for public blockchains, not AI access. — [The Block](https://www.theblock.co/post/359659/zama-raises-57m-in-series-b-to-bring-end-to-end-encryption-to-public-blockchains)
- **WitnessAI, Series B, Jan 13, 2026: $58M.** Led by Sound Ventures with Fin Capital, Forgepoint, Qualcomm Ventures and Samsung Ventures. Traction: ARR grew more than 500% and headcount 5x. Covers shadow AI detection, blocking and compliance. — [Axios](https://axios.com/2026/01/13/witnessai-funding-enterprise-ai); [WitnessAI](https://witness.ai/resources/witnessai-raises-58-million-for-global-expansion-and-announces-new-ways-to-secure-ai-agents/)
- **Harmonic Security, Series A, Oct 2024: $17.5M.** Led by Next47; Ten Eleven Ventures led the earlier $7M seed. Total raised is $26M+, with "enterprise customers already in double figures." — [Harmonic](https://www.harmonic.security/blog-posts/harmonic-security-raises-17-5-million-series-a-to-accelerate-zero-touch-data-protection-to-market); [Dark Reading](https://www.darkreading.com/cybersecurity-operations/harmonic-security-raises-17-5m-zero-touch-data-protection)
- **Edgeless Systems (Privatemode).**
  - Its last disclosed round I found was a $5M seed in March 2023 (Paua Ventures and angels). — [CB Insights](https://www.cbinsights.com/company/edgeless-systems/financials); [Structure Research](https://www.structureresearch.net/2023/03/23/edgeless-systems-raises-seed-round-to-focus-on-securing-public-cloud-workloads/)
  - I found no 2025-2026 round, although the Privatemode product keeps shipping (Kimi K2.6 private model, May 2026). — [deutsche-startups.de](https://www.deutsche-startups.de/tag/edgeless-systems/)
- **Phala.** Rebranded in September 2025 from a Web3 project to "phala.com, a global confidential AI infrastructure company." It shipped confidential GPU VMs on Intel TDX plus NVIDIA CC. No new funding round was found. — [Phala 2025 report](https://phala.com/posts/phala-2025-report)
- **Maple AI / OpenSecret.** An end-to-end encrypted AI chat on open models in enclaves. It is supported by the Human Rights Foundation; I found no VC round. — [HRF](https://hrf.org/latest/hrf-announces-support-for-projects-advancing-ai-for-individual-rights/)

**YC-company rounds**
- **Credal.ai.**
  - Seed: $4.8M led by Spark Capital (October 2023). At raise it had 11 customers, several with "six-figure" contracts, 250K+ LLM calls and about 100K documents ingested, about six months after its April 2023 launch. — [TechCrunch](https://techcrunch.com/2023/10/26/credal-aims-to-connect-company-data-to-llms-securely/)
  - Series A: reportedly November 2024, amount undisclosed. **Uncertain**; the source is an aggregator. — [vcbacked.co](https://www.vcbacked.co/company/credalai)
- **Unbound.**
  - Seed: $4M, oversubscribed, announced May 2025. Led by Race Capital with Wayfinder Ventures, YC, Massive Tech Ventures and angels. — [Pulse 2.0](https://pulse2.com/unbound-4-million-raised-for-helping-enterprises-with-ai-tools); [SecurityWeek](https://www.securityweek.com/unbound-raises-4-million-to-secure-gen-ai-adoption/amp/)
  - A pre-seed is listed for September 2024. — [Seedtable](https://seedtable.com/companies/unbound-security-2/funding-rounds/pre-seed-2024-09)
- **Tinfoil.**
  - Crunchbase and PitchBook show $125K from YC in May 2025, with Pioneer Fund also listed as an investor. — [PitchBook](https://pitchbook.com/profiles/company/770982-94); [Crunchbase](https://www.crunchbase.com/organization/tinfoil/financial_details)
  - PitchBook also lists an undisclosed May 2026 round from Tekedia Capital. **Uncertain.** — [PitchBook](https://pitchbook.com/profiles/company/770982-94)
  - One aggregator claims "$500M raised." That figure is clearly wrong: it conflates Tinfoil with the older Tinfoil Security. — [startuphub.ai](https://www.startuphub.ai/startups/tinfoil); [Tracxn on Tinfoil Security](https://tracxn.com/d/companies/tinfoil-security/__TvjB2dlll8hcHzIGv-KjjgH098RjAsK6ReJXVsLkRQk/funding-and-investors)
- **Blyss.** Last raised $500K (Feb 22, 2023, which matches the YC deal) and is now inactive. — [Extruct](https://www.extruct.ai/hub/blyss-dev-funding); [YC profile](https://www.ycombinator.com/companies/blyss)

**Acquisitions (the exit path for enterprise AI-privacy gateways)**
- **Prompt Security → SentinelOne**, closed Sep 5, 2025. Consideration was about $133.6M cash plus 1,555,099 Class A shares and 415,109 assumed options, per SEC filings. Press estimates put it at about $250-300M. — [SentinelOne 10-Q](https://www.sec.gov/Archives/edgar/data/1583708/000158370825000159/s-20251031.htm); [Globes](https://en.globes.co.il/en/article-1001518079)
- **Aim Security → Cato Networks**, September 2025. The value was undisclosed; a PitchBook estimate of about $375M was reported. Aim protected enterprises adopting public and private AI apps. — [CyberScoop](https://cyberscoop.com/cato-networks-acquires-ai-security-startup-aim-security/); [Globes](https://en.globes.co.il/en/article-1001520614)
- **Mithril Security → H Company**, 2024. Mithril began with privacy tools (BlindLlama, a "Zero Trust AI API" for confidential LLM inference), then shifted to LaVague, an open-source web-automation framework, before H acquired it. — [Techleap](https://finder.techleap.nl/news/feed/h-company-acquires-mithril-security-startup); [BlindLlama docs](https://blindllama.readthedocs.io/en/latest/docs/getting-started/quick-tour/)

**Published investor theses**
- Decibel (Jess Leao, on Confident Security): "Privacy is now the critical barrier to AI adoption in enterprise… the future of AI depends on trust built into the infrastructure itself. Without solutions like this, many enterprises simply can't move forward with AI." — [Pulse 2.0](https://pulse2.com/confident-security-4-2-million-raised-to-enable-provably-private-ai-interactions)
- Walden Catalyst (Young Sohn, on Opaque): "Enterprises will continue to struggle to bring AI into production until they have verifiable guarantees that their most sensitive data and models are protected." — [PR Newswire](https://www.prnewswire.com/news-releases/opaque-raises-24m-series-b-at-300m-valuation-to-advance-confidential-ai-for-the-enterprise-302685635.html)
- TII (Dr. Najwa Aaraj, Opaque round): "There is no such thing as sovereign AI without verifiable guarantees." — [PR Newswire](https://www.prnewswire.com/news-releases/opaque-raises-24m-series-b-at-300m-valuation-to-advance-confidential-ai-for-the-enterprise-302685635.html)
- a16z crypto (Jan 11, 2026): "Privacy is a prerequisite for moving the world's finance onchain, and it is poised to become the biggest moat in crypto." Framed for crypto finance, not AI access. — [a16z crypto](https://a16zcrypto.substack.com/p/the-forces-shaping-crypto-this-year); [a16z crypto 8 big ideas 2026](https://a16zcrypto.substack.com/p/8-big-ideas-for-2026-and-more-trends)
- Dragonfly: secondary coverage describes the Venice round as Dragonfly's first privacy check and first AI check. **Uncertain**; I did not verify this against a Dragonfly primary source. — [Unite.AI coverage via search](https://www.unite.ai/?p=431875); [parsers.vc](https://parsers.vc/news/260708-venice-ai-achieves-unicorn-status-with-65/)

### Inferences
- Private AI is fundable at scale, but in two specific shapes:
  - Consumer revenue first, with crypto capital and tokens (Venice).
  - Enterprise "verifiable guarantee" platforms sold to large regulated customers (Opaque). These raised only after landing names like ServiceNow and Anthropic.
- Seed-stage confidential-inference teams with strong technical founders but no disclosed revenue (Confident Security, Tinfoil, Edgeless) cluster at roughly $4-5M or less. That looks like conviction-light "infra option value" money.
- The highest-dollar outcomes in "privacy in front of LLMs" were enterprise DLP/shadow-AI gateways sold to CISOs and bought by security incumbents (SentinelOne, Cato). The budget line is security, not privacy-as-a-product.
- No mainstream generalist firm named in the brief (Sequoia, Menlo, Greylock, Lightspeed, Paradigm, Electric Capital) led any round found here. The leads were security specialists (Race, Next47, Decibel, Walden Catalyst, Sound) or crypto funds (Dragonfly, Pantera, Blockchange, Coinbase Ventures).

### Gaps
- I found no published private-AI or confidential-compute thesis from Sequoia, Menlo, Greylock, Lightspeed, Paradigm or Electric Capital. The search returned only general AI market maps (for example [Lightspeed AI enterprise market map](https://venturemarketmaps.substack.com/p/lightspeed-ai-enterprise-market-map)).
- Funding amounts for NEAR AI's private-inference effort (it appears to be foundation-funded), Phala's 2025 pivot and Nillion were not found.
- Tinfoil's post-YC financing is unconfirmed: one undisclosed PitchBook entry, no press release.
- Confident Security and Tinfoil revenue and customer counts are not public.
- Credal's Series A amount is undisclosed.

---

## What patterns distinguish funded from unfunded or dead companies in this space?

### Takeaway
Survivors and big raisers have one of three things:
- Revenue at scale: Venice, about $70M run-rate and profitable.
- Named enterprise logos plus a CISO or compliance budget: Opaque, WitnessAI, Harmonic, Prompt and Aim.
- A widening from "privacy" into a broader control plane: Credal moved from redaction to agents.

The dead and stalled companies sold privacy as the product to developers before hardware or demand was ready (Blyss, W23), or pivoted out of privacy entirely (Mithril → web agents → acquired). Hyperscalers and labs are now shipping their own confidential-cloud AI, which squeezes the generic "confidential inference" layer.

### Cited Findings

**Dead or pivoted**
- **Blyss (W23).** Same thesis as Tinfoil two years earlier (GPU enclaves, "end-to-end encrypted AI"). It raised only the $500K YC deal and is now marked Inactive. — [YC profile](https://www.ycombinator.com/companies/blyss); [Extruct](https://www.extruct.ai/hub/blyss-dev-funding)
- **Mithril Security.** Pivoted from privacy tooling (BlindLlama/BlindChat confidential inference) to LaVague web agents, then was acquired by H Company in 2024. — [Techleap](https://finder.techleap.nl/news/feed/h-company-acquires-mithril-security-startup)
- **Credal (W23).** Moved from "redact and anonymize data before it reaches cloud LLMs" (2023) to "The Control Plane for Enterprise Agents." — [TechCrunch 2023](https://techcrunch.com/2023/10/26/credal-aims-to-connect-company-data-to-llms-securely/); [YC profile](https://www.ycombinator.com/companies/credal-ai)
- **LogosGuard (F25).** Possibly broadening from consumer redaction toward enterprise AI governance and assessment; the sources conflict. — [YC profile](https://www.ycombinator.com/companies/logosguard); [logosguard.com](https://logosguard.com/)
- **Other inactive companies:** CodeStory (S23; "AI-native, privacy-first IDE"), TectoAI (S25; AI governance) and Vizly (S23; Privacy-tagged). — [CodeStory](https://www.ycombinator.com/companies/codestory); [TectoAI](https://www.ycombinator.com/companies/tectoai); [yc-oss dataset](https://yc-oss.github.io/api/companies/all.json)
- **Edgeless Systems.** No disclosed raise since its 2023 $5M seed despite continued Privatemode launches. — [CB Insights](https://www.cbinsights.com/company/edgeless-systems/financials); [deutsche-startups.de](https://www.deutsche-startups.de/tag/edgeless-systems/)

**Incumbents absorbing the infra layer**
- Google launched Private AI Compute (November 2025). It runs Gemini in the cloud on TPUs with "Titanium Intelligence Enclaves," remote attestation and a "no access" policy even for Google engineers. It is live in Pixel 10 Magic Cue and Recorder. — [TechInformed](https://techinformed.com/google-launches-private-ai-compute-for-cloud-gemini-with-on-device-level-privacy/); [CyberInsider](https://cyberinsider.com/google-debuts-private-ai-compute-to-bridge-cloud-power-and-local-privacy/)
- OpenAI said in August 2025 it is "very serious" about encrypting ChatGPT, likely starting with temporary chats, though "we don't have a timeline." Altman pushes "AI privilege" for medical and legal chats. — [Axios](https://www.axios.com/2025/08/18/altman-openai-chatgpt-encrypted-chats)
- Confident Security explicitly targets LLM providers and hyperscalers as customers wrapping their own engines, which suggests the infra layer is being sold to, and absorbed by, the frontier providers. — [Pulse 2.0](https://pulse2.com/confident-security-4-2-million-raised-to-enable-provably-private-ai-interactions)

**Funded-company traits**
- Opaque: research pedigree (Berkeley RISELab), named customers (ServiceNow, Anthropic, Accenture) and strategic investors (Intel Capital). — [PR Newswire](https://www.prnewswire.com/news-releases/opaque-raises-24m-series-b-at-300m-valuation-to-advance-confidential-ai-for-the-enterprise-302685635.html)
- Credal at seed: 11 customers with six-figure contracts within six months. — [TechCrunch](https://techcrunch.com/2023/10/26/credal-aims-to-connect-company-data-to-llms-securely/)
- WitnessAI: ARR up 500%+. — [Axios](https://axios.com/2026/01/13/witnessai-funding-enterprise-ai)
- Harmonic: double-digit enterprise customers at its Series A. — [Harmonic](https://www.harmonic.security/blog-posts/harmonic-security-raises-17-5-million-series-a-to-accelerate-zero-touch-data-protection-to-market)
- Unbound: founder with Palo Alto Networks and Imperva data-security pedigree. — [Pulse 2.0](https://pulse2.com/unbound-4-million-raised-for-helping-enterprises-with-ai-tools)
- Venice: users and revenue before taking any VC, a token economy, and an "uncensored" positioning alongside privacy. — [The Block](https://www.theblock.co/post/406934/venice-ai-funding-equity-valuation-dragonfly); [SiliconANGLE](https://siliconangle.com/2026/07/01/venice-raises-65m-1b-valuation-private-uncensored-ai/)

### Inferences
- **Pattern 1: buyer clarity.** Enterprise companies that framed privacy as data-leak or compliance risk, with a CISO as the buyer, raised Series A/B rounds or exited at $250M+. Companies that framed privacy as a cryptographic property for developers mostly stayed at seed or died.
- **Pattern 2: timing and hardware.** Blyss (2023) preceded broad availability of NVIDIA confidential-computing GPUs. Tinfoil (2025) launched on Hopper and Blackwell CC. Enabling hardware arrived, but so did Google, Apple and OpenAI moves. The window for "generic confidential inference" as a standalone venture is narrowing.
- **Pattern 3: frontier-model access drives consumer demand.** Venice's scale coincides with offering OpenAI and Anthropic models anonymously alongside open models. Tinfoil, Maple, Privatemode and NEAR offer open-weight models only and have disclosed no comparable traction. This is correlation, not proof; Venice's "uncensored" angle and crypto community are confounders.
- **Pattern 4: privacy as a wedge, then broaden.** Credal and possibly LogosGuard moved from redaction to governance or agent control. Mithril left privacy entirely. A pure privacy-pool company should expect investors to ask what the broader platform becomes.
- **Pattern 5: who funds consumer privacy.** At scale, crypto-native funds wrote the checks (Dragonfly, Coinbase Ventures, Pantera, Blockchange), often with token components. Generalist VCs funded the enterprise side.

### Gaps
- No primary-source shutdown post-mortem was found for Blyss, CodeStory or TectoAI, so the reasons they died are inferred, not documented.
- No data on churn or retention for any private-AI consumer product.
- I could not determine whether Venice's frontier-model proxying is covered by explicit agreements with OpenAI and Anthropic (Duck.ai's is contractual) or simply runs on standard API terms.

---

## What would a YC partner likely object to in a privacy-pool pitch, based on what YC has funded and seen fail?

### Takeaway
Based on YC's own portfolio and the public critiques of Tinfoil's launch, the likely objections are:
1. "Venice and DuckDuckGo already do this, and the labs and Google are building it in."
2. "Your whole product depends on the labs' API terms and goodwill."
3. "Why trust you? You are a new honeypot."
4. "Consumers don't pay for privacy, and enterprises buy this as a DLP feature from security vendors."
5. "We funded Blyss in W23 and it died."

YC still funds privacy infrastructure in 2026 (Egoist, Caution, Inth), so the category itself is not a disqualifier. The team will need a demand proof, not a cryptography proof.

### Cited Findings
- **Incumbent and hyperscaler objection, as voiced at Tinfoil's Launch HN:** cloud providers "aren't going to care… Nobody wants you as a service provider. Everyone wants Gemini, OpenAI." Azure and GCP already offer confidential VMs. Tinfoil's founders answered that they enable others rather than compete with frontier labs. — [Launch HN](https://news.ycombinator.com/item?id=43996555)
- **Trust and honeypot objection:** HN commenters objected that enclaves require trusting Intel, AMD and NVIDIA. They also called a partial trust boundary an "illusion of trust" and raised side channels. — [Launch HN](https://news.ycombinator.com/item?id=43996555)
- **Enterprise readiness objection:** commenters cited missing SOC 2, HIPAA and FedRAMP certifications. Tinfoil said its SOC 2 audit was about a week from completion (May 2025). — [Launch HN](https://news.ycombinator.com/item?id=43996555)
- **"Why not local?" objection:** commenters argued for air-gapped or local deployment, or FHE, as the only true guarantee. — [Launch HN](https://news.ycombinator.com/item?id=43996555). YC has also funded several on-device or local-first AI companies in this window: Sentient OS, RunAnywhere, Cactus Compute, Epicenter, Skillsync. — [Sentient OS](https://www.ycombinator.com/companies/sentient-os); [RunAnywhere](https://www.ycombinator.com/companies/runanywhere); [Epicenter](https://www.ycombinator.com/companies/epicenter)
- **Existing pooled-proxy competitors:** Venice proxies OpenAI and Anthropic anonymously, with 3M users and $70M+ run-rate. — [The Block](https://www.theblock.co/post/406934/venice-ai-funding-equity-valuation-dragonfly). Duck.ai is a free anonymizing proxy to OpenAI and Anthropic with no-training contracts. — [CyberInsider](https://cyberinsider.com/duckduckgo-makes-privacy-respecting-ai-chat-service-widely-available/)
- **First-party privacy from labs and Google:** Google Private AI Compute is live for Gemini features. — [TechInformed](https://techinformed.com/google-launches-private-ai-compute-for-cloud-gemini-with-on-device-level-privacy/). OpenAI is weighing ChatGPT encryption. — [Axios](https://www.axios.com/2025/08/18/altman-openai-chatgpt-encrypted-chats)
- **YC's own failure precedent:** Blyss (W23, end-to-end encrypted AI via GPU enclaves) is inactive. — [YC profile](https://www.ycombinator.com/companies/blyss)
- **YC's Requests for Startups:** the Spring 2026 RFS priorities listed in coverage were AI-native PM systems, AI hedge funds, AI agencies, stablecoin finance, government AI tooling, metal mills and real-time physical-work guidance. Privacy-first AI access was not on the list; privacy reportedly appears only as "table stakes" for AI aimed at the aging population (wording reported in secondary coverage). — [Let's Data Science](https://letsdatascience.com/news/yc-requests-ai-native-startups-across-industries-1c422935). The Fall 2026 RFS (13 ideas) also had no privacy item in coverage. — [explainx.ai](https://explainx.ai/blog/yc-requests-for-startups-fall-2026)
- **Counter-evidence that YC still funds privacy:** S26 included Egoist Machines (user-owned context with cryptographic access control) and Caution (attested enclave hosting, with private AI inference customers). X26 included Inth (privacy compliance). — [Egoist](https://www.ycombinator.com/companies/egoist-machines); [Caution](https://www.ycombinator.com/companies/caution); [Inth](https://www.ycombinator.com/companies/inth)
- **Enterprise budget sits with security:** prompt and data-leak gateway companies were bought by SentinelOne and Cato. — [SentinelOne 10-Q](https://www.sec.gov/Archives/edgar/data/1583708/000158370825000159/s-20251031.htm); [CyberScoop](https://cyberscoop.com/cato-networks-acquires-ai-security-startup-aim-security/). YC's own enterprise bets here (Unbound, Candor, Golf, compliant-llm) are DLP and governance tools, not anonymity tools. — [Unbound](https://www.ycombinator.com/companies/unbound); [Candor](https://www.ycombinator.com/companies/candor-security); [Golf](https://www.ycombinator.com/companies/golf)

### Inferences
Likely objections, and the evidence that would answer them:
1. **"Isn't this Venice or Duck.ai?"**
   - Answer: an institutional pool (firm identity unlinkable from the provider), which neither offers. Or a verifiable proxy (attested, open-source, with no logs provable via enclaves like Tinfoil or Caution), rather than Venice's trust-us proxy.
   - Venice's numbers are the best "is there demand" proof available. Pitch it as category validation, not as a reason the space is taken.
2. **Platform risk.** Pooling many users or firms behind one API account could breach provider usage policies (account sharing, KYC, abuse attribution). A partner will ask what happens when OpenAI or Anthropic rate-limit or ban the pool.
   - Mitigation evidence would be a commercial agreement like Duck.ai's no-training contracts.
   - I found no source on the providers' specific stance toward anonymous pools; that is a gap.
3. **"Labs will ship this."** Google already has. OpenAI says it is "very serious." Answer: the lab's privacy protects content from the lab's own staff, but the lab still knows who you are. Anonymity from the provider is structurally something a lab cannot offer about itself. This is the cleanest wedge, and it is an inference, not a documented market fact.
4. **Honeypot and trust.** Expect the same HN critique Tinfoil got. Answer: remote attestation plus reproducible builds (Caution's approach) and an open-source proxy. SOC 2 is the minimum for institutions.
5. **"Consumers won't pay for privacy."** Counter-evidence: Venice's run-rate and Tinfoil's $20/month pricing. Caveat: Venice's "uncensored" angle and crypto community confound privacy demand.
6. **"Blyss died."** Answer: Blyss sold infra to developers before the hardware matured. A pool sells frontier-model access, a product people already want, with privacy built in. That sidesteps the "nobody wants you as a service provider, everyone wants OpenAI" objection.
7. **Overall fundability (inference).** A privacy pool in front of GPT, Claude and Gemini looks fundable in late 2026 at seed, in the $4-5M range seen for Confident Security and Unbound, if the team shows early paid usage or design-partner institutions. Series-A-scale money has so far gone only to companies with large revenue (Venice) or blue-chip enterprise logos (Opaque, WitnessAI). Crypto-native funds are the demonstrated large-check writers for consumer private AI.

### Gaps
- I found no public YC partner commentary (blog, podcast or Office Hours) specifically on privacy-pool or anonymous-proxy businesses. The objections above are inferred from the portfolio, the Launch HN critiques and market facts.
- I found no source on OpenAI, Anthropic or Google API terms regarding anonymous pooled resale or proxying in this research pass. This is critical for the platform-risk objection and should be checked against current usage policies.
- I could not establish whether Venice's proxied closed-model traffic has drawn any provider enforcement.
