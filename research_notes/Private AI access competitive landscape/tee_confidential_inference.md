# Private AI Access Built on Confidential Computing (TEE / Enclave Inference Startups), as of October 2026

Scope note: research done 2026-10-07. Search snippets were checked against primary pages where possible. Figures from aggregators (Tracxn, PitchBook, vcbacked, review sites) are marked as secondary. "Historical" means older than about 6 months or describing launch-era state. Crypto-network TEE providers (Phala, NEAR AI, etc.) get only a brief mention because another researcher covers them.

---

## Q1. Tinfoil (tinfoil.sh, YC X25/P25): product, trust model, models, metadata, pricing, funding, roadmap

### Takeaway
Tinfoil is the most technically transparent pure-play. It runs open-weight models only, on NVIDIA confidential GPUs behind AMD SEV-SNP (and Intel TDX for Containers). Client SDKs check attestation against a Sigstore transparency log, and the attestation covers firmware, kernel, config and model weights (dm-verity). It protects content only. Its own Sept 2026 privacy policy says it collects email/OAuth identity, Stripe/Apple/Google billing data, IP addresses and per-request usage metadata.

### Cited Findings
**Product and team**
- Products: Private Chat (web and iOS), an OpenAI-compatible Private Inference API, a Local Proxy, Tinfoil Containers (private deployments), plus coding-agent tutorials — [Tinfoil docs index](https://docs.tinfoil.sh/llms.txt); [Tinfoil blog](https://tinfoil.sh/blog); [App Store](https://apps.apple.com/app/id6745201750)
- Launch HN was 15 May 2025. Founders: Tanya (cryptography team at Cloudflare), Jules (MIT PhD in trusted hardware, worked with NVIDIA and Microsoft Research), Sacha (MIT PhD in privacy-preserving cryptography) and Nate (Tor background) — [Launch HN: Tinfoil (YC X25)](https://news.ycombinator.com/item?id=43996555). Full names Tanya Verma and Jules Drean — [startupintros](https://startupintros.com/people/tanya-verma) (secondary)
- Historical (launch, May 2025): free limited chat, $20/mo unlimited, API at $2 per 1M tokens, models Llama and DeepSeek R1 70B — [Launch HN](https://news.ycombinator.com/item?id=43996555)

**Architecture and what is attested**
- CPU TEE is AMD SEV-SNP, validated against AMD root certs and the AMD KDS. At boot, each NVIDIA GPU is checked for confidential-compute mode with NVIDIA's `local-gpu-verifier` — [Tinfoil attestation architecture](https://docs.tinfoil.sh/verification/attestation-architecture)
- Measured: OVMF firmware, kernel and initrd (from a read-only root filesystem), and the hash of `tinfoil-config.yml` in the kernel command line. Read-only model-weight volumes are checked against "modelwrap" commitments with dm-verity — [attestation architecture](https://docs.tinfoil.sh/verification/attestation-architecture)
- A GitHub Action builds each release and commits the measurements to a public append-only transparency log as a signed Sigstore bundle. The attestation includes an enclave-generated TLS public key, and the client checks that the server's TLS key matches the attested key. SDKs verify "automatically on each connection" — [attestation architecture](https://docs.tinfoil.sh/verification/attestation-architecture); [docs intro](https://docs.tinfoil.sh/)
- Feb 3, 2026 post "How Tinfoil Proves Model Identity": cryptographic verification that the weights are untampered — [Tinfoil blog](https://tinfoil.sh/blog/2026-02-03-proving-model-identity)
- Founders say users must still trust the silicon vendor ("we're assuming trust in vendor silicon"). They call physical side channels "difficult to mount", and they argue that on hyperscaler confidential VMs "the service operator can SSH into the VM", whereas Tinfoil cannot — [Launch HN](https://news.ycombinator.com/item?id=43996555); [Side channels post, May 2025](https://tinfoil.sh/blog/2025-05-15-side-channels)
- July 14, 2026 "Architecting Secure Prompt Caching": cache secrets are held client-side — [Tinfoil blog](https://tinfoil.sh/blog)

**Models (open-weight only)**
- Sept 14, 2026, verbatim: "All our hosted models are open-weight and widely available via other providers" — [Safety Without Compromising on Privacy](https://tinfoil.sh/blog/2026-09-14-safety-without-compromising-privacy)
- Models named across pages: GPT-OSS 120B, Kimi K2.5, DeepSeek R1, Voxtral, Qwen3-VL 30B, Llama 3.3 70B — [Tinfoil overview](https://tinfoil.sh/overview); DeepSeek V4, Gemma 4, Kimi K2.6, GLM 5.1 — [everydev listing](https://www.everydev.ai/tools/tinfoil-private-chat) (secondary); qwen3-coder-480B — [Tinfoil blog](https://tinfoil.sh/blog). The live catalog loads dynamically, so I could not scrape per-token prices — [tinfoil.sh/models](https://tinfoil.sh/models)
- Safety (Sept 2026): models are tested against 297 prompts before hosting and rejected if they fail more than 5%. Safeguard classifiers ("gpt-oss-safeguard and Kimi-K3") run inside the enclave, so "the conversation itself stays private, as does the category that was violated". The post also contrasts Tinfoil with OpenAI and Anthropic running classifiers on all conversations — [Tinfoil safety post](https://tinfoil.sh/blog/2026-09-14-safety-without-compromising-privacy)

**Tinfoil Containers (Mar 10, 2026): the path to proprietary models**
- Customers deploy Docker images, including "proprietary models", into Intel TDX or AMD SEV-SNP confidential VMs with NVIDIA CC, up to eight H200 or B200 GPUs per container, on bare metal. "Your application doesn't need to be [open source] for attestation to work." The named partner is Workshop Labs, which is building private post-training and inference "for finetuning frontier models" where "even Workshop Labs cannot access" the data — [Introducing Tinfoil Containers](https://tinfoil.sh/blog/2026-03-10-tinfoil-containers)
- June 9, 2026: with Pour Demain (Brussels AI-policy think tank), ran gray-box evals with vllm-lens on GLM-5.1 (~744B parameters) inside enclaves. The weights "never leave the enclave", which they pitch as "verifiable clean rooms" for labs and auditors. Interpretability under CC added 33-38% latency, mostly from disabling CUDA Graphs — [Auditing Frontier Model Without Weights](https://tinfoil.sh/blog/2026-06-09-auditing-frontier-model-without-weights)

**Identity, payment, network metadata**
- Privacy policy effective Sept 22, 2026. Collected: names, emails, account IDs and OAuth data (via Clerk); subscription tier, payment status, invoices and transaction IDs (Stripe, RevenueCat, Apple, Google); request counts, token use, feature use and timestamps; IP addresses, browser/device type and approximate region; Plausible analytics; Sentry crash telemetry. Retention: account data for the account's lifetime plus 30 days, billing records ~7 years, IP and request logs "managed by Clerk". The policy also says "confidential computing does not eliminate all security risk" — [Tinfoil privacy policy](https://tinfoil.sh/privacy)
- Self-serve payments run only through Stripe; enterprise can arrange other methods — [Tinfoil pricing](https://tinfoil.sh/pricing)

**Pricing**
- Private Chat $20/mo (free trial). API is pay-as-you-go per input/output token, and new sign-ups get $5 free credit. Enterprise is custom — [Tinfoil pricing](https://tinfoil.sh/pricing); [Product Hunt](https://www.producthunt.com/products/tinfoil-private-ai-chat) (secondary for the $5 credit)

**Funding and traction (uncertain)**
- YC-backed with Pioneer Fund. Tracxn says an undisclosed round from Tekedia Capital in May 2026 — [Tracxn](https://tracxn.com/d/companies/tinfoil/__UDLjo0TGvK5WU1UvCYyhSGWQhSf1Z71WqXl2gHdLMms) (secondary, low confidence)
- One aggregator says $1.1M total, last a pre-seed in July 2024 — [vcbacked](https://www.vcbacked.co/company/tinfoil) (secondary). Another says $500K — [aitinkerers](https://one-shot.aitinkerers.org/p/unlocking-private-ai-tinfoil-s-vision-on-end-to-end-confidential-ai-with-provable-security) (secondary). The startuphub.ai page titled "$500M Raised" is almost certainly an error — [startuphub](https://www.startuphub.ai/startups/tinfoil)

**Roadmap signals**
- June 16, 2026 "Towards Search, Memory, and More" (semantic search, cross-chat memory). Sept 2026 safety post promises image and video generation models and open-sourced eval code — [Tinfoil blog](https://tinfoil.sh/blog); [safety post](https://tinfoil.sh/blog/2026-09-14-safety-without-compromising-privacy)

### Inferences
- Tinfoil's trust model is "operator cannot read content". It is not "operator does not know who you are". Identity, payment, IP and usage timing all sit with Tinfoil and its processors (Clerk, Stripe, Plausible, Sentry).
- Containers plus the GLM-5.1 clean-room demo are Tinfoil's bet on a closed-weights future: a lab could ship encrypted weights into an attested enclave that neither Tinfoil nor the end user can read. No frontier lab is named as a partner.

### Gaps
- No primary-source funding announcement. The size of any seed after YC is unknown.
- Current per-model token prices (the catalog is JS-rendered).
- No user, revenue or customer counts beyond Workshop Labs.
- No public response found to TEE.fail or Battering RAM.

---

## Q2. Confer (Moxie Marlinspike): product, trust model, models, metadata, pricing, Meta deal, Confidential Workers

### Takeaway
Confer is a consumer E2EE AI assistant. Passkey-derived keys encrypt on the device. Inference runs in an attested confidential VM whose whole root filesystem is measured (dm-verity), built reproducibly (Nix/mkosi) and published to a Sigstore log, with attestation bound into a Noise Pipes handshake. It uses open-weight models. In March 2026 Moxie announced that Confer's technology will underpin Meta AI while Confer stays independent. In September 2026 Confer added "Confidential Workers": attested, single-use Linux VMs for tool use.

### Cited Findings
- Soft-launched in Dec 2025, with wide coverage in Jan 2026. Free tier is 20 messages/day and 5 active chats. Paid is $35/month for unlimited use, "advanced models" and personalization. Models are open-weight (none named). Message encryption uses a WebAuthn passkey, which works best on mobile and macOS Sequoia, while Windows/Linux go through a password manager — [TechCrunch, Jan 18 2026](https://techcrunch.com/2026/01/18/moxie-marlinspike-has-a-privacy-conscious-alternative-to-chatgpt)
- Moxie's framing: AI chat "actively invites confession", and ads combined with chat is like "someone paying your therapist to convince you to buy something" — [TechCrunch](https://techcrunch.com/2026/01/18/moxie-marlinspike-has-a-privacy-conscious-alternative-to-chatgpt)
- Blog timeline: "Confessions to a data lake" (Dec 23 2025); "Making end-to-end encrypted AI chat feel like logging in" (Dec 29 2025); "Private inference" (Jan 5 2026); "Sorting secrets" (Jan 21 2026); Meta post (Mar 17 2026); "Memory that forgets to tell anyone" (Mar 29 2026); "Connectors without confiding" (Apr 8 2026, email/docs/calendar connectors); "How to search documents we can't read" (Aug 1 2026); "Confidential workers for private AI" (Sep 5 2026) — [Confer blog](https://confer.to/blog/)
- Private-inference architecture: confidential VM; hardware quote at boot over kernel, initrd and cmdline; dm-verity Merkle tree "to cover everything" in the root filesystem; reproducible builds with Nix and mkosi ("anyone can clone the repository, run the build, and get the exact same measurements"); signed releases in an append-only Sigstore transparency log. The client checks the quote signature, the binding of the public key to the channel, and a match against a logged release. Attestation is embedded in a Noise Pipes handshake with ephemeral keys for forward secrecy — [Private inference](https://confer.to/blog/2026/01/private-inference/)
- Meta (Mar 17, 2026): "As Confer continues to operate as an independent entity, I will also work to integrate Confer's privacy technology so that it underpins Meta AI", and it will be "part of the foundation of everything that is to come" as Meta builds beyond chat. Moxie recalls integrating the Signal Protocol into WhatsApp ten years earlier. The post has no technical details or timeline — [Confer is bringing foundational AI privacy to Meta](https://confer.to/blog/2026/03/encrypted-meta/)
- Press coverage says the technology goes into Meta AI across WhatsApp, Instagram, Facebook and Messenger. In March 2026 the Confer iOS app was "just waiting on Apple review" — [PiunikaWeb](https://piunikaweb.com/2026/03/18/signal-founder-confer-tech-coming-to-meta-ai/); [aiforautomation](https://aiforautomation.io/news/2026-03-20-confer-signal-founder-encrypted-ai-meta-partnership) (secondary). Coverage also notes Meta removed E2EE from Instagram DMs on May 8, which raised questions — [search coverage summary via thedailyperspective](https://thedailyperspective.org/article/2026-03-19-signals-privacy-technology-heads-to-meta-ai-raising-both-hope-and-questions-6b607bc1) (secondary; I did not verify the date)
- Confidential Workers (Sep 5, 2026): "small Linux VM with an ordinary shell and a temporary workspace" inside a TEE with encrypted memory. The inference proxy checks the hardware quote, the SSH-key binding, the Sigstore release signature and measurements against a signed manifest, and pins the host key from the attestation. The image is reproducible (Nix + mkosi, pinned Ubuntu packages, dm-verity). Each worker accepts exactly one connection and then closes its socket. It has no public IP, no admin login and no persistent home, and its firewall blocks everything except PyPI. Tools cover PDFs, docs, spreadsheets with formulas and charts, presentations, images and data analysis — [Confidential workers for private AI](https://confer.to/blog/2026/09/confidential-workers-for-private-ai/)

### Inferences
- Confer's measured surface (whole-rootfs dm-verity plus reproducible builds plus attested Noise handshake) is the strictest consumer design found. It extends the same attestation chain to agent tool execution, which no other startup here has documented.
- The account is passkey-based, so content keys never reach Confer. But the $35/mo paid tier means a payment relationship exists, and I found no evidence of anonymous payment or IP-hiding relays.
- The Meta tie-up is the first time a frontier-scale AI operator has publicly adopted a TEE-startup's privacy tech, but it covers Meta's own (Llama-family/Meta AI) models. It is not GPT, Claude or Gemini.

### Gaps
- TEE vendor (SEV-SNP vs TDX) and GPU type for Confer inference were not stated in what I could retrieve.
- Model names; payment processor; whether IP or account metadata is logged; funding (none found); team size; user numbers.
- Whether Confidential Workers is available on the free tier, and its price.
- Concrete Meta AI rollout status as of Oct 2026.

---

## Q3. Privatemode (formerly Continuum AI) by Edgeless Systems

### Takeaway
Privatemode is a German, EU-hosted confidential inference service (API, web chat, desktop app) on NVIDIA H100/B200 inside confidential computing environments, orchestrated by Edgeless's Contrast. It is open-weight only (GLM-5.3, gpt-oss-120b and similar), priced in euros. It targets government and regulated industries, and its pricing is the cheapest published here.

### Cited Findings
- Privatemode AI was "formerly called Continuum AI" and was renamed in v1.6.0 — [Continuum/Privatemode release notes](https://docs.edgeless.systems/continuum/release). Launched Feb 19, 2025 — [Edgeless press](https://www.edgeless.systems/press). Historical: Continuum was billed as the first confidential LLM platform on NVIDIA H100 — [Edgeless blog](https://www.edgeless.systems/blog/launching-confidential-llm-platform-continuum-ai)
- Mar 12, 2026 press release: "Edgeless Systems Brings Confidential AI to Government and Regulated Industries Across Europe With NVIDIA" ("cryptographically verifiable AI inference for government, healthcare, and regulated industries") — [Edgeless press](https://www.edgeless.systems/press)
- Architecture: NVIDIA H100 or B200 in "Confidential Computing Environments". The Contrast Coordinator attests GenAI inference instances and a Secret Service. The client-side privatemode-proxy runs remote attestation. The Secret Service "agrees on a prompt encryption key with each client through attested key exchange" and releases keys only to verified workers. Infrastructure runs on Scaleway and Lyceum Technology in the EU. Claim: "we can never access your data" — [Privatemode architecture](https://docs.privatemode.ai/architecture/overview)
- Pricing (Oct 2026, ex-VAT): Free tier with 5M tokens on signup plus 1M/month and no credit card. Pay-as-you-go "from €0.65 / 1M output tokens". Enterprise adds SLAs, custom models and SSO. Per 1M tokens (input/output/cached): GLM-5.3 €1.55/€5.74/€0.15; GLM-5.3-Flash €0.20/€0.65/€0.05; gpt-oss-120b €0.20/€0.65/€0.04; DeepSeek-OCR-2 €0.77/€1.27; Qwen3-Embedding 4B €0.13 input; Voxtral Mini 3B €0.004/min; Whisper large-v3 €0.014/min — [Privatemode pricing](https://www.privatemode.ai/pricing)
- GLM-5.3 and GLM-5.3 Flash (vision) were added Sept 21, 2026. A "Privatemode Decisions" product was added Sept 24, 2026 — search-result summary of [Edgeless press/blog](https://www.edgeless.systems/press) (unverified on a primary page. The snippet's description, "a confidential alternative to Jev", is garbled.)
- Edgeless cooperates with Airbus, NVIDIA, IBM and Schwarz Group — [Edgeless about](https://www.edgeless.systems/about-us)
- Funding (historical): €1.45M seed (Acequia, Inventures, SIX Group, Venture Creator) — [Edgeless blog](https://www.edgeless.systems/blog/we-raised-1-45m-to-build-the-open-source-stack-for-confidential-computing); $5M (reported $5.3M) led by SquareOne, Mar 2023 — [Tech.eu](https://tech.eu/2023/03/07/edgeless-systems-raises-5million-for-public-cloud-security/); [Edgeless](https://www.edgeless.systems/edgeless-systems-raises-5m-to-advance-confidential-computing)

### Inferences
- GLM-5.x is open-weight: Tinfoil hosts GLM 5.1 and says all its hosted models are open-weight. So despite an automated summary calling GLM "closed", Privatemode is open-weight only.
- EU-only hosting (Scaleway, Lyceum) plus Contrast-based attestation is aimed at GDPR and sovereignty buyers rather than anonymity. The service needs an account and API key, and I found no anonymity features.

### Gaps
- No post-2023 funding round found. Revenue and customer names are undisclosed.
- No logging, IP or account-metadata policy found in the architecture docs.
- Whether model weights are measured into the attestation (the docs mention workloads only).

---

## Q4. Confident Security (CONFSEC / OpenPCC)

### Takeaway
Confident Security is an Apple-PCC-style enterprise layer: Oblivious HTTP through a third-party relay (so the compute provider cannot link requests to users), GPU attestation, stateless processing and transparency logs. Since Nov 2025 it ships as the open standard OpenPCC (Apache 2.0 / FSL). It serves open-weight models through an OpenAI-compatible API. Of the startups here, it is the only one designed for unlinkability at the network layer.

### Cited Findings
- Came out of stealth July 17, 2025 with $4.2M, pitched as "the Signal for AI". It wraps foundation models so prompts and metadata stay private, even from model providers, and is modeled on Apple PCC — [TechCrunch](https://techcrunch.com/2025/07/17/confident-security-the-signal-for-ai-comes-out-of-stealth-with-4-2m/). Conflict: the Nov 2025 press release cites a "$5 million seed round from Decibel, Ex/Ante, South Park Commons, Halcyon, and SAIF" — [Business Wire, Nov 5 2025](https://www.businesswire.com/news/home/20251105013372/en/Confident-Security-Launches-OpenPCC-an-Open-Source-Standard-that-Protects-Data-Shared-with-AI-Models)
- OpenPCC (Nov 5, 2025): the release includes the spec and SDKs (Apache 2.0), a compliant inference server and reference deployment, "Two-Way" encrypted client↔AI streaming, go-nvtrust (GPU attestation), and Go implementations of BHTTP and OHTTP. It uses OHTTP with a third-party relay. Built by ex-Databricks and Apple engineers. An independent foundation will steward it — [Business Wire](https://www.businesswire.com/news/home/20251105013372/en/Confident-Security-Launches-OpenPCC-an-Open-Source-Standard-that-Protects-Data-Shared-with-AI-Models); [Axios](https://www.axios.com/2025/11/05/openpcc-encryption-ai-mcp-data); [AI Journal](https://aijourn.com/confident-security-launches-openpcc-an-open-source-standard-that-protects-data-shared-with-ai-models/)
- Site claims: confidential computing (TEEs), "anonymized encrypted pathways", stateless processing, remotely verifiable attestation and transparency logs. Models listed: Mistral, Gemma, Llama, Phi, Qwen, DeepSeek, plus custom model hosting, through an OpenAI-compatible API/SDK. Pricing is "usage-based fees pinned to market rates per model". Targets GDPR/CCPA/HIPAA enterprises. Members of NVIDIA Inception, CSA and the Confidential Computing Consortium — [confident.security](https://confident.security/)
- Backed by South Park Commons — [SPC](https://www.southparkcommons.com/companies/confident-security/)

### Inferences
- OHTTP plus a relay is a real network-metadata defense (the operator sees requests but not client IPs, and the relay sees IPs but not content). This is the most important structural difference from Tinfoil, Privatemode and Confer. Account and billing linkage for the enterprise customer still exists by design (B2B).
- "Access to leading LLMs" on the site is ambiguous. The named models are all open-weight, and I found no evidence of GPT, Claude or Gemini served inside CONFSEC.

### Gaps
- No 2026 funding, customers, revenue or price sheet found. Founder names not verified in fetched pages.
- Whether the OHTTP relay operator is truly independent in production deployments.

---

## Q5. Maple AI / OpenSecret

### Takeaway
Maple is a consumer and team E2EE assistant on OpenSecret's encrypted backend. It runs open-weight models in TEEs and has an OpenAI-compatible "Maple Proxy" API. It is the only startup here offering anonymous signup with no email plus Bitcoin payment, which makes it the closest to identity anonymity. Funding is small and partly unconfirmed.

### Cited Findings
- Launched Jan 28, 2025 as "Maple: Secure and Private AI for Work and Personal Use". OpenSecret is "the encrypted backend" (developer platform). Joined NVIDIA Inception May 21, 2025. Team includes Anthony Ronning and "Marks" (Mark Suman) — [OpenSecret blog](https://blog.opensecret.cloud/); [Maple launch post](https://blog.opensecret.cloud/maple-private-ai-for-work-and-personal/)
- Maple Proxy (announced Sept 3, 2025; updated Oct 4, 2026) is an OpenAI-compatible endpoint with inference in a TEE ("prompts and responses never leave the enclave") and user-run attestation. Models: gpt-oss-120b, llama3-3-70b, gemma4-31b, qwen3-vl-30b, kimi-k2-6, glm-5-1, deepseek-v4-pro (800k context). API price range is $0.90–$3.00 per 1M input tokens and $2.00–$10.50 per 1M output, with credits in $10 increments. It requires a $20+/mo plan — [Maple Proxy post](https://www.trymaple.ai/blog/introducing-maple-proxy-the-maple-ai-api-that-brings-encrypted-llms-to-your-openai-apps)
- DeepSeek V4 Flash (284B MoE) went to paid customers in limited beta — [RuntimeWire](https://runtimewire.com/article/maple-deepseek-v4-flash-paid-customers-limited-beta) (secondary)
- Plans: Free (25 messages/week), Pro $20/mo, Max $100/mo, Team $30/user/mo. Bitcoin via Zaprite with 10% off annual Pro/Max — [bitcoinproducts review](https://www.bitcoinproducts.com/blog/maple-ai-review) (secondary, "current as of Sept 2026"); [GetApp](https://www.getapp.com/business-intelligence-analytics-software/a/maple/) (secondary). The trymaple.ai/pricing page returned 403.
- Anonymous sign-up "doesn't ask for an email" (Jan 8, 2026), and co-founder Marks confirmed it is "quite popular" (Jan 20, 2026). Monero is "on our list, but low". Marks: "Confidential computing let us build e2ee AI on top of full size open models"; "Projects" coming — [Privacy Guides forum](https://discuss.privacyguides.net/t/privacy-using-maple-ai/34503)
- Bitcoin, Lightning and ecash payments — [search summary of Maple privacy materials](https://discuss.privacyguides.net/t/privacy-using-maple-ai/34503) (the thread itself mentions Bitcoin. Lightning and ecash come from other unverified snippets.)
- Investor: a search snippet quotes someone saying "Ten31, where I'm a managing partner, is an investor in OpenSecret" — [Typefully thread](https://typefully.com/teemupleb/opensecret-and-maple-ai-private-ai-that-cant-spy-9SVCqww) (secondary; exact source page uncertain)

### Inferences
- Maple goes furthest on account and payment anonymity (no-email accounts plus Bitcoin). It still sees IP addresses unless the user brings Tor or a VPN, and I found no relay or OHTTP.
- Maple is open-weight only and appears to be a privacy UX layer over enclave inference, not a GPU-infrastructure company.

### Gaps
- Which TEE/GPU provider Maple's inference runs on (own hardware vs a partner) was not confirmed in fetched sources.
- Funding amount and rounds; user counts; IP-logging policy.

---

## Q6. Other players in the category (brief)

### Takeaway
The rest of the field is mostly enterprise or infrastructure: Opaque (a $24M Series B at a $300M valuation, Feb 2026), Fortanix Armet AI (turnkey agentic AI on Intel CC and NVIDIA CC GPUs), Lucid Computing (attested inference location, "AI Passports"), Caution (YC S26 attested hosting), Super Protocol and Phala (marketplace/crypto-adjacent GPU TEE clouds). None is a consumer anonymity product, and none serves closed frontier models.

### Cited Findings
- **Opaque Systems**: $24M Series B at a $300M valuation (Feb 12, 2026), led by Walden Catalyst with Intel Capital, Race Capital, Storm Ventures, Thomvest and ATRC. $55.5M raised in total. Founded 2021. A confidential AI platform for enterprise data, model protection and policy enforcement — [SiliconANGLE](https://siliconangle.com/2026/02/12/opaque-raises-24m-300m-valuation-confidential-ai-platform/); [Intel Capital](https://www.intelcapital.com/opaque-raises-24m-series-b-at-300m-valuation-to-advance-confidential-ai-for-the-enterprise/)
- **Fortanix Armet AI**: launched Apr 2025 on Intel Confidential Computing and Tiber Trust Authority — [Fortanix PR](https://www.fortanix.com/company/pr/2025/04/fortanix-armet-ai-enables-enterprises-to-create-secure-and-compliant-custom-gen-ai-applications-to-mitigate-data-exposure-risk). Extended to NVIDIA CC GPUs for agentic AI (Oct 28, 2025) — [Business Wire](https://www.businesswire.com/news/home/20251028147323/en/Fortanix-Brings-Secure-and-Trusted-Agentic-AI-to-Cutting-Edge-NVIDIA-Confidential-Computing-GPUs). Partnered with HPE and NVIDIA on "AI factories" (Dec 2025) — [Fortanix PR](https://www.fortanix.com/company/pr/2025/12/fortanix-teams-with-hpe-and-nvidia-to-embed-confidential-computing-in-ai-factories). Showcased at GTC 2026 — [Business Wire](https://www.businesswire.com/news/home/20260304380475/en/Fortanix-Showcases-Confidential-AI-Innovation-at-NVIDIA-GTC-2026)
- **Lucid Computing** (founded 2025, SF): TEE clusters (Intel TDX, NVIDIA H100 CC) plus latency-based location proofs. Products are "AI Passports" (proof of where and how a model ran), compliance modules (GDPR/HIPAA/EU AI Act/ITAR) and "Digital Embassies". Accelerator-stage investors include Lionheart, Halcyon, Seldon Lab, Juniper and Safe AI Fund — [Long-term Wiki](https://www.longtermwiki.com/organizations/lucid-computing/facts); [MATS](https://www.matsprogram.org/stream/lucid-11-ebc72) (secondary)
- **Caution (YC S26)**, George Town, Cayman Islands: an "open, verifiable platform" proving what software runs on a server, with encryption keys bound to attestation so "the host sees ciphertext". Targets fintech, blockchain, private AI and healthcare. CEO Anton Livaja (ex-Distrust); team from BitGo, Turnkey, Unit 410 and Ledn — [YC privacy companies](https://www.ycombinator.com/companies/industry/privacy); [Dealroom](https://app.dealroom.co/companies/caution); [LinkedIn](https://ky.linkedin.com/in/alivaja) (secondary)
- **Super Protocol**: confidential AI cloud and marketplace. Marketplace 2.0 (first public release Nov 27, 2024) uses Intel TDX and NVIDIA H100 CC with blockchain orchestration and a trusted loader that publishes attestation reports — [Super Protocol docs](https://docs.superprotocol.com/marketplace/)
- **Phala Cloud** (brief; crypto, covered elsewhere): GPU TEE launched July 2025 on H100/H200 (B200 later). OpenAI-compatible confidential AI API with per-response attestation. Claims "up to 99% efficiency" in TEE mode — [Phala docs](https://docs.phala.com/phala-cloud/confidential-ai/overview); [Phala launch post](https://phala.com/posts/gpu-tee-is-launched-on-phala-cloud-for-confidential-ai). TEE.fail showed that dstack (the confidential-app stack Phala uses) could have attestation forged by a malicious provider with physical access — [tee.fail](https://tee.fail/)
- **Anjuna**: no 2025-2026 confidential-AI product information found.

### Inferences
- Enterprise money (Opaque, Fortanix) is flowing to "confidential AI for your own data or agents" more than to consumer private chat. The consumer pure-plays (Tinfoil, Confer, Maple) appear seed-scale.

### Gaps
- Anjuna's AI offering; Lucid's and Caution's round sizes; Super Protocol's 2026 status.

---

## Q7. What exactly is attested, and to whom (weights, serving stack, logging)?

### Takeaway
Attestation scope varies a lot. Tinfoil and Confer measure the full boot chain and verify it client-side against public Sigstore logs, and Tinfoil also binds the model weights through dm-verity. Privatemode attests workloads through its Contrast coordinator and a client proxy. CONFSEC adds transparency logs and OHTTP. No vendor attests the absence of account, billing or IP logging, because those happen outside the enclave.

### Cited Findings
- Tinfoil: firmware, kernel, initrd, config hash and model weights (modelwrap plus dm-verity). TLS key bound to the attestation. Verified by the client SDK against Sigstore and GitHub logs and AMD root certs — [Tinfoil attestation](https://docs.tinfoil.sh/verification/attestation-architecture)
- Confer: whole root filesystem through dm-verity, reproducible Nix/mkosi builds, Sigstore log, attestation bound into the Noise handshake. Workers are verified by Confer's inference proxy, with host-key pinning — [Private inference](https://confer.to/blog/2026/01/private-inference/); [Confidential workers](https://confer.to/blog/2026/09/confidential-workers-for-private-ai/)
- Privatemode: the Contrast Coordinator attests inference instances and the Secret Service, and privatemode-proxy verifies on the client. The docs do not detail weight measurement — [Privatemode architecture](https://docs.privatemode.ai/architecture/overview)
- CONFSEC: "remotely verifiable attestation", transparency logs and go-nvtrust GPU attestation — [confident.security](https://confident.security/); [Business Wire](https://www.businesswire.com/news/home/20251105013372/en/Confident-Security-Launches-OpenPCC-an-Open-Source-Standard-that-Protects-Data-Shared-with-AI-Models)
- Tinfoil's own privacy policy lists IP and request logs (via Clerk) and usage metrics. These are collected at the edge, outside what the enclave attests — [Tinfoil privacy](https://tinfoil.sh/privacy)

### Inferences
- "Verifiable privacy" means the content path is verifiable. Metadata paths (auth provider, billing, CDN or edge logs, analytics) are policy promises, not attested.
- In Tinfoil and Privatemode the web chat verifies in a client the operator also ships. Users rarely check attestation independently, and that is a UX gap.

### Gaps
- Whether any vendor has had a third-party audit of its attestation pipeline in 2026 (none found).

---

## Q8. Can any serve closed frontier models (GPT, Claude, Gemini) in an enclave? Any frontier-lab partnerships?

### Takeaway
No. Every startup profiled serves open-weight models only, and Tinfoil says so explicitly. The only TEE-protected frontier closed-model serving is first-party: Google's Private AI Compute for Gemini (Nov 2025), Apple PCC for Apple's models, and Meta AI adopting Confer's technology (Mar 2026). Anthropic has published confidential-inference research, and OpenAI has a "Private Safety Processing" preview, but neither runs on a third-party TEE startup and neither is confirmed TEE-based.

### Cited Findings
- Tinfoil: "All our hosted models are open-weight" (Sept 2026) — [Tinfoil](https://tinfoil.sh/blog/2026-09-14-safety-without-compromising-privacy). At launch, an HN commenter said "everyone wants... Gemini, OpenAI", and the founders positioned Tinfoil as infrastructure rather than a competitor to frontier providers — [Launch HN](https://news.ycombinator.com/item?id=43996555)
- Tinfoil Containers supports "proprietary models" in attested enclaves (the closest technical path), but no lab is named — [Tinfoil Containers](https://tinfoil.sh/blog/2026-03-10-tinfoil-containers)
- Google Private AI Compute (announced Nov 2025): Gemini cloud models on Trillium TPUs with Titanium Intelligence Enclaves (TIE), binary authorization, VM isolation, and "IP blinding relays operated by third-parties". First uses were Pixel 10 Magic Cue and Recorder — [The Hacker News](https://thehackernews.com/2025/11/google-launches-private-ai-compute.html)
- Anthropic, with Pattern Labs (now Irregular), published "Confidential Inference via Trusted Virtual Machines", which covers protecting both model weights and user data — [Anthropic research](https://www.anthropic.com/research/confidential-inference-trusted-vms); [Anthropic paper PDF](https://assets.anthropic.com/m/c52125297b85a42/original/Confidential_Inference_Paper.pdf); [Irregular](https://www.irregular.com/research/confidential-inference-systems)
- Aug 19, 2026: OpenAI previewed "Private Safety Processing" ("no OpenAI personnel access", customer-controlled keys, safety flags send only risk-type signals, a CSAM exception). Anthropic added a self-custody option for its 30-day mandatory retention on its newest models (named "Mythos and Fable" in the source). The author finds no evidence of TEE deployment by either: "no evidence yet" that Anthropic's confidential-inference work is implemented — [Barczentewicz](https://barczentewicz.com/post/openai-and-anthropic-beef-up-customer-data-confidentiality-for-frontier-models-but-details-lacking/) (secondary analysis)
- Meta AI will integrate Confer's technology, and Confer stays independent — [Confer](https://confer.to/blog/2026/03/encrypted-meta/)
- Apple PCC is the reference design that CONFSEC explicitly copies — [TechCrunch](https://techcrunch.com/2025/07/17/confident-security-the-signal-for-ai-comes-out-of-stealth-with-4-2m/); [Apple PCC security research](https://security.apple.com/blog/pcc-security-research/)

### Inferences
- The market is split. Startups have verifiable privacy on second-tier open models. Frontier labs have the best models with policy-based or first-party-only enclave privacy. Labs appear to prefer building it themselves (Google, Apple) or acqui-partnering (Meta and Confer) over licensing weights to a third-party enclave operator.
- Tinfoil's weight-confidential Containers and clean-room evals are the most credible technical bridge if a lab ever agrees to ship weights to a neutral enclave.

### Gaps
- No evidence of OpenAI, Anthropic or Google weights deployed on any startup's TEE. OpenAI's promised September 2026 white paper was not located.
- Whether Azure's confidential GPU offerings serve Azure OpenAI models under attestation in 2026 (not researched in depth).

---

## Q9. Identity, account, payment and network address: anonymous to the operator, or content-only?

### Takeaway
Almost everyone is content-only. The best partial exceptions: Maple (no-email accounts plus Bitcoin), CONFSEC (OHTTP relays hide client IPs from compute), and Google PAIC (third-party IP-blinding relays, first-party). No startup combines anonymous accounts, anonymous payment and IP unlinkability with attested inference.

### Cited Findings
- Tinfoil: email/OAuth via Clerk, Stripe/Apple/Google billing, IP and device data, timestamps and token usage, all retained — [Tinfoil privacy](https://tinfoil.sh/privacy); [pricing](https://tinfoil.sh/pricing)
- Confer: passkey-derived encryption with a $35/mo paid tier. No anonymity or IP statements found — [TechCrunch](https://techcrunch.com/2026/01/18/moxie-marlinspike-has-a-privacy-conscious-alternative-to-chatgpt)
- Maple: anonymous no-email signup and Bitcoin payments, with Monero requested but not planned soon — [Privacy Guides](https://discuss.privacyguides.net/t/privacy-using-maple-ai/34503); Zaprite Bitcoin discount — [bitcoinproducts](https://www.bitcoinproducts.com/blog/maple-ai-review) (secondary)
- CONFSEC/OpenPCC: OHTTP with a third-party relay and "unlinkable requests" — [Business Wire](https://www.businesswire.com/news/home/20251105013372/en/Confident-Security-Launches-OpenPCC-an-Open-Source-Standard-that-Protects-Data-Shared-with-AI-Models); [Axios](https://www.axios.com/2025/11/05/openpcc-encryption-ai-mcp-data)
- Privatemode: account plus API key, free tier "no credit card required", and SSO for enterprise. No IP policy found — [Privatemode pricing](https://www.privatemode.ai/pricing)
- Google PAIC: third-party IP blinding relays — [The Hacker News](https://thehackernews.com/2025/11/google-launches-private-ai-compute.html)

### Inferences
- The operator can usually still link "user X (email, card, IP) sent N tokens to model M at time T", even when it cannot read the prompt. For many threat models (subpoena, profiling, breach of the billing database) that metadata is the sensitive part.

### Gaps
- No vendor publishes an attested "no IP logging" property. Blind-signature or token-based anonymous credits (Privacy Pass style) were not found at any startup.

---

## Q10. Known weaknesses: TEE attacks (2025-2026), attestation UX, performance overhead

### Takeaway
Physical memory-bus interposers (Battering RAM, WireTap, TEE.fail, all late 2025) broke SGX, SEV-SNP and TDX guarantees for an attacker with physical access to the host. TEE.fail showed that stolen CPU attestation keys can forge NVIDIA GPU CC trust, because GPU attestations are not bound to a specific CVM. Intel and AMD treat physical attacks as out of scope. GPU CC overhead can reach 20-118% on latency for naive stacks, falling to about 1% with CC-aware runtimes.

### Cited Findings
- Battering RAM (KU Leuven and University of Birmingham, Oct 2025): a ~$50 interposer that passes boot checks and is then switched to redirect protected addresses, letting an attacker corrupt or replay encrypted memory. It breaks SGX and SEV-SNP on DDR4, and the design is open source — [The Hacker News](https://thehackernews.com/2025/10/50-battering-ram-attack-breaks-intel.html); [Dark Reading](https://www.darkreading.com/cloud-security/50-battering-ram-bust-confidential-computing)
- WireTap: a DDR4 interposition attack on SGX servers, released weeks before TEE.fail — [Hacken](https://hacken.io/insights/wiretap-and-battering-ram-risks/); [SecurityWeek](https://www.securityweek.com/new-attack-targets-ddr5-memory-to-steal-keys-from-intel-and-amd-tees/amp/)
- TEE.fail (Georgia Tech and Purdue; IEEE S&P 2026): a DDR5 interposer for under $1,000 that exploits deterministic AES-XTS. It extracted Intel PCE ECDSA attestation keys (forged TDX quotes verify as "UpToDate"), extracted SEV-SNP signing keys even with Ciphertext Hiding, and enables "borrowing" NVIDIA GPU attestations. Case studies cover BuilderNet, Secret Network and dstack. Intel and AMD do not plan firmware fixes and recommend physical security — [tee.fail](https://tee.fail/); [BleepingComputer](https://bleepingcomputer.com/news/security/teefail-attack-breaks-confidential-computing-on-intel-amd-nvidia-cpus); [The Hacker News](https://thehackernews.com/2025/10/new-teefail-side-channel-attack.html)
- Performance (Tinfoil, June 23, 2026): vLLM inter-token latency under CC was +118% for a single request on multi-GPU Blackwell and +49% at 32 requests. Single-GPU Gemma overhead was ~1% with TRT-LLM/SGLang versus 21-26% with vLLM. Speculative decoding raised overhead to ~70%. Pinned-memory PCIe bandwidth fell to ~20% of plaintext. Kimi K2.6 kept 0.59× throughput at TP=4 and 0.46× at TP=8. Blackwell overhead is worse than Hopper because NVLink encryption is on and multicast is disabled. Training loss ran 18-32%. TEE-I/O/TDISP is named as the fix — [Tinfoil benchmarks](https://tinfoil.sh/blog/2026-06-23-confidential-computing-overhead)
- Phala claims "up to 99% efficiency" on H100/H200 in TEE mode — [Phala docs](https://docs.phala.com/phala-cloud/confidential-ai/overview) (vendor claim, conflicts with Tinfoil's multi-GPU numbers)

### Inferences
- All the startups' guarantees reduce to "trust the CPU and GPU vendor, plus the datacenter's physical security". The 2025 attacks make the hosting provider's physical access a live threat, which matters because most of these vendors rent bare metal from third parties (for example Scaleway and Lyceum for Privatemode).
- The biggest frontier-scale MoE models (multi-GPU, tensor parallel) pay the highest CC tax, which works against serving frontier-size models privately.

### Gaps
- No startup publicly documented mitigations for TEE.fail (for example datacenter vetting or binding GPU attestation to the CVM). No 2026 follow-up attacks were found in this pass.

---

## Q11. Cross-company comparison and gaps none of them close

### Takeaway
Every startup verifies content and runs only open-weight models. Identity anonymity is rare (Maple), IP unlinkability is rare (CONFSEC), and nobody serves GPT, Claude or Gemini. The open lane is a product that pairs attested inference with anonymous accounts and payment and network unlinkability, and that gets frontier closed models inside the same trust boundary.

### Cited Findings (comparison table; sources as cited in Q1-Q10)

| | Tinfoil | Confer | Privatemode | CONFSEC | Maple |
|---|---|---|---|---|---|
| Segment | Chat + API + Containers | Consumer chat + agents | EU API/chat, gov/regulated | Enterprise SDK/API, open standard | Consumer/team chat + API |
| TEE | SEV-SNP (+TDX for Containers) + NVIDIA CC H100/H200/B200 | Confidential VM (vendor unstated) | NVIDIA H100/B200 CCE via Contrast | TEEs + NVIDIA (go-nvtrust) | TEE (provider unstated) |
| Attests weights? | Yes (dm-verity/modelwrap) | Whole rootfs (dm-verity) | Not documented | Not documented | Not documented |
| Public transparency log | Sigstore | Sigstore | Not documented | Yes | Not documented |
| Closed frontier models | No (explicit) | No (open-weight) | No | No | No |
| Anonymous account | No (email/OAuth) | Passkey; no anon payment found | No | B2B | Yes (no-email) |
| Anonymous payment | No (Stripe/app stores) | Not found | No | B2B | Bitcoin |
| IP hidden from operator | No (IPs collected) | Not found | Not found | Yes (OHTTP relay) | No |
| Price | $20/mo; API PAYG | Free 20 msg/day; $35/mo | Free 1M/mo; from €0.65/M out; GLM-5.3 €1.55/€5.74 | Usage-based "market rates" | Free; $20/$100/mo; Team $30; API $0.90-3 in / $2-10.50 out |
| Funding | YC + undisclosed (uncertain) | Not disclosed | €1.45M + $5M (2023) | $4.2M or $5M seed | Not confirmed (Ten31, secondary) |

### Inferences
- Gaps none close:
  1. No closed frontier models inside a third-party enclave. Labs keep privacy first-party (Google PAIC, Apple PCC, Meta + Confer).
  2. The metadata layer (accounts, billing, IP, timing) is outside attestation everywhere. Only partial fixes exist (Maple anonymous accounts; CONFSEC OHTTP).
  3. Physical-attack exposure (TEE.fail, Battering RAM) is unmitigated in vendor docs, and GPU attestation is not bound to the CVM.
  4. Attestation is verified by vendor-shipped clients, with no independent, user-friendly verifier or third-party audit found.
  5. CC performance overhead is largest exactly where frontier-scale multi-GPU models live.
- The direction of travel for 2026-2027 is agents and tools inside TEEs (Confer Workers, Tinfoil Containers, Fortanix agentic AI), enterprise and sovereignty (Privatemode, Opaque, Lucid), and big-platform adoption (Meta and Confer). Consumer pure-plays remain seed-scale.

### Gaps
- Revenue and user traction for every startup are effectively undisclosed. No reliable numbers were found.
