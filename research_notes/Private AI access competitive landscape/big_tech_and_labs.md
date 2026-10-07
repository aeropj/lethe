# Big tech and frontier labs: private, unlinkable, or non-profiling access to AI (state as of 7 October 2026)

Scope: Apple, Google, Meta, Microsoft, Amazon, OpenAI, Anthropic, and the relay/token providers (Cloudflare, Fastly). Each section answers one key question. Status labels: **[SHIPPED]** means generally available or rolling out to real users. **[PREVIEW]** means a limited or phased rollout. **[ANNOUNCED]** means stated as coming, with no availability yet. **[REPORTED]** means it comes only from secondary press. **[OLDER]** marks information from before 2026 that may be stale.

---

## Q1. Does any incumbent already offer anonymous (account-unlinkable) access to a frontier model? To whom?

### Takeaway
Yes, but only inside a closed ecosystem and only for the incumbent's own device or app users. Apple is the clearest case: its Apple Intelligence ChatGPT extension gives OpenAI-model access without an Apple account link, with the IP address hidden and no storage by OpenAI. It also serves Gemini-based Apple Foundation Models through Private Cloud Compute (PCC), which uses blind-signed tokens and OHTTP. Google's Private AI Compute and Meta's Private Processing/Incognito Chat run the same pattern (anonymous tokens, third-party IP-blinding relay, TEEs) for their own models in their own apps. The 2026 WiSec paper found that Apple's shipped token scheme lets requests be linked to each other, contrary to the design.

None of these is sold as a general-purpose API or offered to third parties. The lab-direct enterprise products (OpenAI, Anthropic, Azure, Bedrock) offer *confidentiality from the provider* (ZDR, customer-held keys, TEEs) but are always *account-identified*. The only anonymous route to OpenAI and Anthropic frontier models outside Apple devices is a third-party intermediary, DuckDuckGo's Duck.ai, under bespoke agreements.

### Cited Findings

**Apple: Private Cloud Compute (architecture)**
- PCC's stated central claim is that it stores no user data and that "user input and user accounts are unlinkable" — [Dittmar et al., WiSec 2026 / arXiv 2605.24239](https://arxiv.org/html/2605.24239v1)
- Token flow, as documented by Apple and summarised by the WiSec authors:
  - A Token Granting Service issues a Token Granting Token (TGT) "per user and per device". Unlinkability between TGT issuance and redemption comes from RSA blind signatures, "similarly to Privacy Pass".
  - The device exchanges the TGT for batches of One-Time Tokens (OTTs) through a Token Granting Service that sits behind an OHTTP relay. Fraud detection happens at this step: TGTs can be blocklisted and OTT issuance is rate-limited.
  - Source: [arXiv 2605.24239](https://arxiv.org/html/2605.24239v1)
- Cloudflare says Apple PCC uses OHTTP "to disassociate AI inference requests from user identities". Cloudflare also lists Apple LiveCallerID as an OHTTP client — [Cloudflare blog, 2 Oct 2026](https://blog.cloudflare.com/announcing-cloudflare-ohttp-gateway/)
- PCC nodes are selected at random, which limits targetability — [arXiv 2605.24239](https://arxiv.org/html/2605.24239v1)

**Apple: the WiSec 2026 linkability finding (Dittmar, Stephan, Völkl, Hollick, Classen; WiSec '26, Saarbrücken, 30 June–3 July 2026; DOI 10.1145/3765613.3811691)**
- **OTT-to-TGT linkability.** Apple's OTT format adds a per-token salt that Privacy Pass does not have, and requires OTT.Nonce = SHA256(TGT || OTTSalt). The authors write that the OTT "can be linked to the TGT using the salt, allowing identification of which requests belong together". The source code implies the OTT is also forwarded to the PCC node — [arXiv 2605.24239](https://arxiv.org/html/2605.24239v1)
- **Server-side checks are weaker than documented:**
  - The PCC backend "skips the signature validation of TGT, even though this option exists in the source code".
  - The backend accepted modified Token Type, Nonce and Signature fields.
  - The researchers swapped TGTs and OTTs between devices and the backend accepted them.
  - They reused a "one-time" token 2–5 times and still got responses.
  - Source: [arXiv 2605.24239](https://arxiv.org/html/2605.24239v1)
- **Apple's response.** Apple "only made clarifications in the documentation and did not change the underlying protocol or checks" — [arXiv 2605.24239](https://arxiv.org/html/2605.24239v1)
- **Test setup.** iOS 26.2 on an iPhone 16 Security Research Device and macOS 15.5 on an M4 Mac mini, with experiments from December 2025 to early March 2026. PCC has no reproducible builds and its binaries ship without symbols. The authors also found the served model unchanged across that period, even though a new model was announced in January 2026 — [arXiv 2605.24239](https://arxiv.org/html/2605.24239v1)

**Apple: ChatGPT and Gemini integrations**
- **ChatGPT extension used without signing in:**
  - The user's IP address is obscured from ChatGPT.
  - OpenAI must process the request "solely for the purpose of fulfilling your request" and must not store it or the response, except where the law requires.
  - OpenAI receives no information tied to the Apple Account and must not train on the data.
  - Coarse metadata is still sent: time zone, country, device type, language, and the feature being used.
  - If the user signs in to a ChatGPT account, OpenAI's own policies apply, and OpenAI may log requests and train on them.
  - Source: [Apple Legal: ChatGPT Extension & Privacy](https://www.apple.com/legal/privacy/data/en/chatgpt-extension/) (from search extract; the page timed out on direct fetch). **[OLDER: terms date from the iOS 18.2 launch in Dec 2024 and appear unchanged]**
- **Apple–Google deal.** On 12 Jan 2026 Apple and Google announced a multi-year, non-exclusive deal that puts Gemini at the core of Apple Foundation Models. The ~$1B/year figure is **[REPORTED]** — [tech-insider](https://tech-insider.org/apple-google-gemini-siri-deal-1-billion-2026/); [Introl](https://introl.com/blog/apple-google-gemini-partnership-siri-ai-infrastructure-2026)
- **Gemini runs inside PCC.** On 29 Jan 2026 Tim Cook confirmed that Gemini-powered Siri will "continue to run on the device and run in Private Cloud Compute, and maintain our industry-leading privacy standards" — [9to5Mac](https://9to5mac.com/2026/01/29/apple-confirms-gemini-powered-siri-will-use-private-cloud-compute/). So the Gemini-derived models run inside Apple's PCC trust boundary, not as a call to Google's Gemini API.

**Apple: PCC moves onto Google Cloud (8 June 2026)** [PREVIEW]
- For the first time, Apple is deploying PCC outside its own data centres:
  - Hardware: NVIDIA Confidential Computing on NVIDIA GPUs, Intel CPUs with TDX, and Google's Titan chip.
  - Workloads: next-generation Apple Foundation Models built with Google using "technologies behind its Gemini family of models", for "agentic tool-use and complex reasoning".
  - Rollout: a gradual ramp "throughout the summer preview period".
  - Source: [Apple Security Research, "Expanding PCC"](https://security.apple.com/blog/expanding-pcc/)
- Transparency commitments:
  - All binaries will be published, with public research tooling and live PCC nodes for researchers through the Apple Security Bounty.
  - A "cryptographically verifiable, append-only ledger" will track Google Cloud hardware.
  - Software attestation will require "at least two separate roots of trust from independent vendors".
  - Source: [Apple](https://security.apple.com/blog/expanding-pcc/); [Help Net Security, 10 Jun 2026](https://www.helpnetsecurity.com/2026/06/10/apple-private-cloud-compute-google-cloud-expansion/)
- Apple's post says nothing about OHTTP, token granting, or unlinkability for the Google-hosted nodes. Coverage says Apple keeps "complete control over PCC software". It does not say explicitly that Google cannot see the data — [Apple](https://security.apple.com/blog/expanding-pcc/) (as extracted)

**Google: Private AI Compute** [SHIPPED for narrow Pixel features; memory ANNOUNCED]
- **Launch.** Announced 11 Nov 2025. First used for Magic Cue on Pixel 10 and for Recorder transcription summaries in more languages — [The Hacker News](https://thehackernews.com/2025/11/google-launches-private-ai-compute.html); [Droid Life](https://www.droid-life.com/2025/11/11/google-new-private-ai-compute-gemini/)
- **Architecture (technical brief, Sept 2026 version):**
  - Inference runs on "the latest Gemini models" on TPUs, using a hardened TPU platform (Titanium Intelligence Enclave). CPU workloads run in AMD SEV-SNP confidential VMs.
  - **IP-blinding relays "operated by third-parties"** tunnel all inbound traffic. The operator is not named.
  - **"Anonymous Tokens"** separate authentication from inference. A separate server handles device authentication and rate limiting and swaps device credentials for an "anonymous, cacheable token", so that "a user's identity never travels with their data on the inference path".
  - External audits: 2025 and 2026 report summaries were published (NCC Group did the 2025 assessment).
  - Source: [Google technical brief (PDF)](https://services.google.com/fh/files/misc/private_ai_compute_technical_brief.pdf)
- **Secure server-side memory** [ANNOUNCED, no rollout date]:
  - On 23 Sept 2026 Google added "secure server-side memory": a per-user "memory Oak Server" database inside a TEE, encrypted with "per-user keys" bound to the user, written in Rust, open source, and tied to deployed binaries through reproducible builds.
  - Source: [Google technical brief](https://services.google.com/fh/files/misc/private_ai_compute_technical_brief.pdf); [Help Net Security, 24 Sept 2026](https://www.helpnetsecurity.com/2026/09/24/google-private-ai-compute-server-side-memory/)
  - Note that the brief's non-targetability section is explicitly titled "for stateless inference". Memory is by design persistent and per-user — [brief](https://services.google.com/fh/files/misc/private_ai_compute_technical_brief.pdf)

**Meta: WhatsApp Private Processing and Incognito Chat** [SHIPPED / rolling out]
- **Timeline.** Private Processing was announced 29 Apr 2025 — [Meta Engineering](https://engineering.fb.com/2025/04/29/security/whatsapp-private-processing-ai-tools/). The technical whitepaper V1 was published 10 Jun 2025 and **V2 was updated 16 Mar 2026** — [Meta whitepaper](https://ai.meta.com/static-resource/private-processing-technical-whitepaper)
- **Authentication: ACS anonymous credentials.**
  - The client gets a credential from Meta's open-source Anonymous Credential Service. The credential "can be used a finite number of times" and lets Meta authenticate and rate-limit "without knowing who the user is".
  - The ACS token travels inside the OHTTP-encrypted inner request and is checked at Meta's OHTTP gateway. The gateway then picks a CVM.
  - Source: [whitepaper V2](https://ai.meta.com/static-resource/private-processing-technical-whitepaper)
- **Routing: third-party OHTTP relay (Fastly).**
  - Requests pass through a third-party OHTTP relay ("We have worked with Fastly to provide this infrastructure") that "strips out IP information".
  - Fastly also distributes the ACS and OHTTP key configs, which are signed with a Meta key hardcoded in the client. Meta says the point is to prevent it from serving per-user keys that could "allow de-anonymization".
  - Source: [whitepaper V2](https://ai.meta.com/static-resource/private-processing-technical-whitepaper)
- **Compute: confidential VMs.**
  - AMD EPYC SEV-SNP CVMs with NVIDIA H100 confidential-computing GPUs. NVLink encryption on Blackwell is also mentioned.
  - RA-TLS runs end to end from the device to the CVM.
  - Meta designed the system so it cannot observe classifier traffic sizes ("non-observability").
  - Source: [whitepaper V2](https://ai.meta.com/static-resource/private-processing-technical-whitepaper)
- **Transparency log (Cloudflare).** Cloudflare runs the third-party artifact transparency log. Meta notes it is "not a Merkle-tree based transparency ledger but a simple log maintained by a third-party" — [whitepaper V2](https://ai.meta.com/static-resource/private-processing-technical-whitepaper)
- **New in V2: web search.** The whitepaper adds a web-search section with these safeguards:
  - "Unlinked searches" (queries are not tied to the user).
  - Queries capped at 100 characters, with at most 5 queries per prompt.
  - Search terms shown in the in-app transparency report.
  - Source: [whitepaper V2](https://ai.meta.com/static-resource/private-processing-technical-whitepaper)
- **Independent assessment.** NCC Group assessed WhatsApp message summarisation (report dated 27 Aug 2025) — [NCC Group](https://www.nccgroup.com/media/ymskbe40/ncc_group_metaplatforms_whatsapp-message_summarization_report_2025-08-27_v10.pdf)
- **Incognito Chat (13 May 2026).**
  - Available on WhatsApp and in the Meta AI app, built on Private Processing.
  - Meta says "no one — not even Meta — can read your conversations". Chats are not saved and messages disappear by default.
  - It is rolling out "over the coming months". "Side Chat" is coming next.
  - The announcement does not name the model and does not address ads or training.
  - Source: [Meta Newsroom](https://about.fb.com/news/2026/05/incognito-chat-whatsapp-meta-ai/); [TechCrunch](https://techcrunch.com/2026/05/13/whatsapp-adds-an-incognito-mode-in-meta-ai-chats/)

**Microsoft (Azure / Foundry)**
- **Azure AI Confidential Inferencing preview.**
  - Covered the Azure OpenAI Whisper model, with TEEs, encrypted prompts, "user anonymity" and OHTTP.
  - Ran on confidential GPU VMs (AMD SEV-SNP + H100 CC mode).
  - Source: [Microsoft Tech Community, preview](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/azure-ai-confidential-inferencing-preview/4248181); [deep dive](https://techcommunity.microsoft.com/blog/azureconfidentialcomputingblog/azure-ai-confidential-inferencing-technical-deep-dive/4253150). **[OLDER: Sept 2024. I found no evidence it reached GA or extended to GPT-class frontier models by Oct 2026.]**
- Azure confidential VMs with H100 GPUs are GA — [Microsoft](https://techcommunity.microsoft.com/blog/azureconfidentialcomputingblog/general-availability-azure-confidential-vms-with-nvidia-h100-tensor-core-gpus/4242644) **[OLDER: 2024]**
- **Foundry data handling (doc dated 18 May 2026):**
  - Prompts and completions "are NOT available to OpenAI or other providers", and models "do NOT interact with any services operated by" OpenAI.
  - Abuse monitoring can store prompts for human review. "Managed customers" can apply for *modified abuse monitoring*, which turns off storage and human review, though automated review continues. Customers can verify the change through the `ContentLogging=false` setting.
  - Every request carries the customer's resource ID.
  - Source: [Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-foundry/responsible-ai/openai/data-privacy)

**Amazon Bedrock**
- Bedrock does not share prompts or outputs with model providers, and does not use them for training.
- Each model provider uploads its model to an "escrow account" that has no outbound access to Bedrock. Providers cannot see deployment accounts, service logs, prompts or completions.
- Source: [AWS re:Post knowledge center](https://repost.aws/knowledge-center/amazon-bedrock-model-data-use)
- For Anthropic covered models served through Bedrock, Google Cloud or Azure, the 30-day retention still applies. However, "retained data stays within each provider's environment" — [Claude Help Center](https://support.claude.com/en/articles/15425996-data-retention-practices-for-covered-models)

**OpenAI** [enterprise confidentiality; no anonymous product]
- **Private Safety Processing (PSP).**
  - Previewed 20 Aug 2026 to keep Zero Data Retention (ZDR) workable while detecting misuse across sessions.
  - Customer content sits either in customer infrastructure or in OpenAI storage under customer-held keys. OpenAI staff "never see the prompts or responses" and receive only narrowly defined alerts.
  - Early testers: Microsoft and Databricks. Consumer ChatGPT tiers (Free, Plus, Go, Pro) are excluded. The US CSAM reporting carve-out remains.
  - Source: [The Next Web](https://thenextweb.com/news/openai-zero-data-retention-private-safety-processing); [Security Boulevard](https://securityboulevard.com/2026/08/openai-unveils-private-safety-processing-to-detect-ai-misuse-without-storing-enterprise-data/). OpenAI's primary page returned 403: [openai.com](https://openai.com/index/offering-zero-data-retention-for-frontier-models/)
  - Phased rollout to eligible ZDR API customers began 22 Sept 2026 — [TokenPost](https://www.tokenpost.com/news/technology/25495)
- **"Private Intelligence" (DevDay, 29 Sept 2026).**
  - An umbrella name for (1) ZDR with PSP, available now, and (2) **"Private Inference"**, which combines "confidential computing with verifiable controls" and arrives as a **preview this fall**.
  - Safety review runs in a "hardware-attested safety runtime".
  - Retention for safety review is 30 days, in customer-controlled S3, Azure Blob or GCS storage.
  - It is aimed at enterprises.
  - Source: [VentureBeat](https://venturebeat.com/security/openais-new-private-intelligence-targets-a-growing-enterprise-concern-who-can-see-your-ai-data); [OpenAI DevDay 2026 recap](https://openai.com/index/devday-2026-recap/) (not fetched)

**Anthropic** [enterprise confidentiality; no anonymous product]
- **Covered-model retention (effective 9 June 2026).**
  - For Covered Models (Claude Fable 5, Fable 5.1, Mythos 5, Mythos 5.1), "prompts ... and outputs ... are retained for 30 days" to detect cross-request misuse.
  - It applies to *ZDR organisations* on the Console, Claude Code with ZDR in Enterprise, Bedrock, Google Cloud Agent Platform, and Azure Foundry.
  - No personnel can read the data by default. Human review happens only after automated flagging, and access is logged in tamper-proof records.
  - Source: [Claude Help Center](https://support.claude.com/en/articles/15425996-data-retention-practices-for-covered-models)
- **Enterprise Frontier Safeguards (EFS).**
  - Announced ~1–2 Sept 2026. Monitoring data is stored in the *customer's* S3, Azure Blob or GCS bucket under the customer's KMS keys. There is no Anthropic human review; automated systems scan a rolling window of traffic.
  - It is free; customers pay only cloud costs. It rolls out in phases "starting later this fall". Until then, eligible customers get ZDR on Fable 5/5.1.
  - Source: [Anthropic](https://www.anthropic.com/news/enterprise-frontier-safeguards); [Neomanex](https://neomanex.com/news/anthropic-enterprise-frontier-safeguards); [Quartz](https://qz.com/anthropic-enterprise-frontier-safeguards-data-retention-090226)
  - Neomanex says EFS was designed with 100+ customers, including Mastercard, Visa, Salesforce, Snowflake, Stripe, FIS, Cognition and Factory — [Neomanex](https://neomanex.com/news/anthropic-enterprise-frontier-safeguards)
- **Confidential inference research.** Anthropic published a confidential-inference system design (SEV-SNP/TDX plus H100/H200 CC mode, with weights released by a KMS after attestation) in a joint white paper with Irregular (formerly Pattern Labs). Whether it is commercially available "is not publicly documented" — [Sentora/Medium summary](https://medium.com/sentora/this-anthropic-research-about-secure-ai-inference-with-tees-can-be-very-relevant-to-web3-65107fa94657) **[OLDER: 2025; primary not fetched]**

**Third-party precedent: DuckDuckGo Duck.ai** (an intermediary, not an incumbent, but it shows the labs will contract for anonymous pooled access)
- Duck.ai strips IP addresses and other metadata, so requests to Anthropic, OpenAI, Mistral, Azure and Tinfoil "appear as though they are coming from DuckDuckGo".
- Models on the help page include OpenAI GPT-5.6 Sol and Terra and GPT-5.4 mini/nano, plus Anthropic Claude Opus 4.8, Sonnet 4.6 and Haiku 4.5. Advanced models sit behind the paid Privacy Pro plan.
- Every provider has agreed to ZDR ("delete your prompts and responses immediately after generating a reply"), no training, and no sharing with third parties. OpenAI and Anthropic keep exceptions for prompt caching (up to 1 hour, in memory) and for legal or malicious-use retention.
- Source: [DuckDuckGo Help: Duck.ai privacy](https://duckduckgo.com/duckduckgo-help-pages/duckai/ai-chat-privacy)
- **Conflict:** a DuckDuckGo help-page snippet surfaced in search says instead that providers "must delete your anonymized prompts within 30 days". This is probably an older version of the agreement — [DuckDuckGo Help: chat models](https://duckduckgo.com/duckduckgo-help-pages/duckai/chat-models)

### Inferences
- The *technical pattern* a privacy pool would use (blind or anonymous tokens for auth and rate limiting, a third-party OHTTP relay, TEE inference with attestation and a transparency log) is now standard practice at Apple, Google and Meta. These three companies run it at consumer scale, so the pattern itself is not a differentiator.
- The incumbents that already offer anonymous access do so only to users of their own hardware or apps (an Apple device plus TGT eligibility, a Pixel, WhatsApp or Meta AI), and mostly for their own or co-developed models. Apple's ChatGPT extension is the only case of anonymous access to a *rival lab's* model by an incumbent. It is a feature inside an OS, not an API, and the WiSec paper shows Apple's request-level unlinkability is weaker in practice than in its documentation.
- OpenAI and Anthropic are moving toward "confidential but identified" for frontier models. Both now *require* cross-session misuse detection for their top models (Anthropic: 30-day retention, then EFS; OpenAI: PSP). That needs a stable account or organisation identifier, which rules out per-user unlinkability at the lab boundary. A pool can only satisfy this by being the accountable "customer" itself.

### Gaps
- Which OpenAI model the Apple ChatGPT extension serves as of Oct 2026, and whether its no-store terms have changed. I could only reach the Apple legal page through a search extract.
- Whether PCC nodes on Google Cloud keep the same OHTTP and token path, and which relay operators Apple uses today. Apple's June 2026 post is silent on this.
- Who operates Google's "third-party" IP-blinding relays. The brief does not name them.
- Whether Incognito Chat interactions are excluded from Meta's ad personalisation. The announcement does not say.
- Whether Azure's 2024 confidential-inferencing preview (with OHTTP and "user anonymity") ever reached GA or covered GPT-class models. I found no 2025–2026 source.
- The OpenAI PSP white paper, the Private Inference technical details (TEE vendor, relay, whether users or only organisations get unlinkability), and OpenAI's primary pages. The openai.com pages returned 403.

---

## Q2. What business incentives (ads, memory, personalization) push against non-profiling access?

### Takeaway
Every consumer-facing incumbent except Apple monetises or personalises using AI-chat data. OpenAI selects ads using memory and past chats. Meta feeds AI chats into ad targeting. Google is building persistent per-user memory and Gmail/Photos-linked "Personal Intelligence", and is "open-minded" about putting ads in Gemini. For frontier labs the strongest force *against* anonymity is safety: per-account misuse detection. Anonymous access cuts against both revenue and safety, so incumbents' "private" modes are built as identified-but-sealed (Google memory, OpenAI PSP, Anthropic EFS) or as narrow opt-in modes (Meta Incognito).

### Cited Findings
- **OpenAI ads.**
  - Ad testing began 9 Feb 2026 in the US on the Free and Go plans — [OpenAI Help: Ads in ChatGPT](https://help.openai.com/en/articles/20001047-ads-in-chatgpt); [OpenAI: Testing ads in ChatGPT](https://openai.com/index/testing-ads-in-chatgpt/)
  - "If memory is on, ChatGPT may save and use memories and reference recent chats when selecting an ad". Advertisers get only aggregated performance data.
  - Free and Go users can opt out of ads in exchange for fewer messages. Paid tiers have no ads.
  - Source: [OpenAI Help](https://help.openai.com/en/articles/20001047-ads-in-chatgpt)
  - Expansion to the UK, Mexico, Brazil, Japan and South Korea, and to 31 European markets on 24 Aug 2026, is **[REPORTED]** in search summaries — [Proton blog](https://proton.me/blog/chatgpt-ads); [Segwise](https://segwise.ai/blog/chatgpt-ads-2026-guide)
- **Meta.**
  - From 16 Dec 2025 Meta uses text and voice interactions with Meta AI to personalise content and ads on Facebook and Instagram. Sensitive topics are excluded. There is no opt-out, except in the UK, EU and South Korea — [The Register, 1 Oct 2025](https://www.theregister.com/2025/10/01/meta_ai_use_informs_ads/); [Storyboard18](https://storyboard18.com/digital/meta-to-use-ai-chats-to-power-ads-starting-december-16-81924.htm)
  - Incognito Chat is therefore an *exception mode* layered on an ad-funded default — [Meta Newsroom](https://about.fb.com/news/2026/05/incognito-chat-whatsapp-meta-ai/)
- **Google.**
  - In Dec 2025 Google's ads VP Dan Taylor said "There are no ads in the Gemini app and there are no current plans to change that" — [Search Engine Land](https://searchengineland.com/google-corrects-report-claiming-ads-are-coming-to-gemini-in-2026-465856)
  - On the April 2026 earnings call, Alphabet CBO Philipp Schindler called Google "open-minded" and said a format that works in AI Mode "would transfer successfully to Gemini app" **[REPORTED via secondary]** — [ALM Corp](https://almcorp.com/blog/google-gemini-ads-not-ruled-out-advertiser-guide-2026/)
  - "Personal Intelligence" (beta, 14 Jan 2026, for US AI Pro/Ultra subscribers) links Gemini to Gmail, Photos, YouTube and Search history — [Fortune](https://fortune.com/2026/01/14/google-gemini-ai-personal-assistant-gmail-photos-youtube-history-personal-intelligence)
  - Private AI Compute's 2026 update exists to support "long-term context, cross-device or cross-platform context, and user preferences" — [Google brief](https://services.google.com/fh/files/misc/private_ai_compute_technical_brief.pdf)
- **Anthropic consumer.** Since the Sept 2025 consumer-terms change, Free, Pro, Max and Claude Code chats are used for training unless the user opts out, with retention of up to 5 years for those who allow training. Enterprise and API users are excluded — [Business Today](https://www.businesstoday.in/amp/technology/news/story/anthropic-to-use-claude-conversations-for-ai-training-unless-users-opt-out-by-september-28-491530-2025-08-29) **[OLDER: Aug 2025]**
- **Safety as an incentive against unlinkability.**
  - Anthropic retains covered-model traffic so it can identify misuse "that may only become apparent across multiple interactions" — [Claude Help Center](https://support.claude.com/en/articles/15425996-data-retention-practices-for-covered-models)
  - OpenAI's PSP exists to "identify behavioral trends across related interactions" — [Security Boulevard](https://securityboulevard.com/2026/08/openai-unveils-private-safety-processing-to-detect-ai-misuse-without-storing-enterprise-data/)
- **Apple's incentive runs the other way.** Apple's PCC is provided "free of charge" on its devices, and privacy is part of the product pitch — [arXiv 2605.24239](https://arxiv.org/html/2605.24239v1). That is consistent with Apple being the incumbent most willing to give anonymous access to third-party models.

### Inferences
- OpenAI, Meta and (prospectively) Google tie ads and personalisation to identity. For them, a general anonymous mode at scale would cannibalise ad inventory, memory lock-in and training data. Expect privacy features to stay opt-in, narrow, or limited to enterprise.
- The frontier labs' safety stance (cross-session linkability for top models) is a *non-commercial* barrier. It also applies to intermediaries: a pool reselling covered models will likely have to retain or monitor traffic in some EFS- or PSP-like form at the pool level.

### Gaps
- Whether ChatGPT memory or ads touch Apple-extension traffic. Under Apple's terms they should not, but I found no OpenAI statement.
- Microsoft Copilot's ad and personalisation use of chat data in 2026. Not researched for lack of budget.

---

## Q3. What do the terms say about intermediaries pooling users (reselling, approved partners)?

### Takeaway
Both OpenAI and Anthropic allow a customer to build an application that serves its own end users. That is legally the "pool" model, with the intermediary as the accountable customer. Both prohibit plain resale of access. OpenAI bans reselling or leasing account access and transferring API keys, and it places end-user enforcement and export-control know-your-customer (KYC) obligations on the customer. Anthropic bans reselling "except as expressly approved by Anthropic". DuckDuckGo shows the labs will sign bespoke ZDR agreements with an anonymising intermediary, and Anthropic says it is "working to support third-party offerings" for EFS.

### Cited Findings
- **OpenAI Services Agreement (online v.010126):**
  - §2.2 grants "the right to use OpenAI's API to integrate the Services into Customer Applications and to make Customer Applications available to End Users".
  - §3.1: "Customer may not resell or lease access to its Account or any End User Account."
  - §3.2: End User Accounts "may only be provisioned to, registered for, and used by, a single End User", and the Customer is responsible for all End User activity "including ... who access the Services through a Customer Application".
  - §3.3(g)–(i): no buying, selling or transferring of API keys; no circumventing rate limits, protective measures or "Usage Limits".
  - §8.1: OpenAI may ask the customer to suspend an End User and may do it itself if the customer does not.
  - §16.11 (Trade Controls): the customer warrants that it and its End Users are not in embargoed countries or on restricted-party lists, and that it will comply with export-control law, "including any 'know your customer' requirements or obligations applicable to Customer's End Users". §16.12 bars End Users from accessing the Services outside OpenAI's supported countries. Both are sanctions and export-control duties, not a general identity requirement.
  - §6.1: OpenAI also sells through resellers ("Customer will pay OpenAI or Customer's reseller").
  - Source: [OpenAI Services Agreement PDF](https://cdn.openai.com/osa/openai-services-agreement.pdf)
- **Anthropic Commercial Terms (effective 17 June 2025):**
  - §A.1 permits use "to power products and services Customer makes available to its own customers and end users".
  - §D.4 bars customers from building competing products or training competing models, or from "resell[ing] the Services except as expressly approved by Anthropic".
  - §D.5: "Customer is responsible for all activity under its account."
  - §B: "Anthropic may not train models on Customer Content from Services."
  - Source: [Anthropic Commercial Terms](https://www.anthropic.com/legal/commercial-terms)
- **EFS and third parties.** The EFS announcement says Anthropic is "working to support third-party offerings" for eligible customers. The context points to cloud and partner channels; it is not explicitly about privacy intermediaries — [Anthropic](https://www.anthropic.com/news/enterprise-frontier-safeguards)
- **Approved anonymising-intermediary precedent.** DuckDuckGo has "agreements in place with all model providers" (OpenAI, Anthropic, Mistral, Azure, Tinfoil) covering ZDR, no training and no third-party sharing for anonymised, pooled traffic — [DuckDuckGo Help](https://duckduckgo.com/duckduckgo-help-pages/duckai/ai-chat-privacy)
- **Hyperscaler channels.**
  - Anthropic covered models are sold through Bedrock, Google Cloud Agent Platform and Azure Foundry, under the same retention rules — [Claude Help Center](https://support.claude.com/en/articles/15425996-data-retention-practices-for-covered-models)
  - Azure-hosted OpenAI models never touch OpenAI's services — [Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-foundry/responsible-ai/openai/data-privacy)

### Inferences
- A pool that presents itself as one "Customer Application" whose members are its end users fits within OpenAI §2.2 and Anthropic §A.1. Selling raw access (shared keys or accounts) does not. The binding constraints are OpenAI's end-user suspension clause (§8.1), its export-control KYC and supported-country duties (§16.11–16.12, which an anonymous pool must still satisfy, e.g. through geo-checks) and both labs' misuse-monitoring requirements. These push the pool to keep a pseudonymous per-member handle it can suspend, even if it never reveals that handle upstream.
- Anthropic's "expressly approved" resale language and the DuckDuckGo agreements suggest the realistic path is a negotiated partner agreement, not reliance on standard terms.

### Gaps
- Whether OpenAI's or Anthropic's *usage policies* (as distinct from the agreements above) require per-end-user identifiers, such as OpenAI's `user`/safety identifier, for high-capability models in 2026. Not verified.
- The exact text of DuckDuckGo's provider contracts. They are not public.
- Google Gemini API / Vertex terms on resale and pooled end users. Not researched.

---

## Q4. What did each incumbent announce in 2025–2026, and what is on the roadmap?

### Takeaway
2025–2026 saw every major player converge on TEE-based "sealed cloud" inference. Apple took PCC onto Google Cloud with NVIDIA and TDX. Google launched Private AI Compute and added sealed memory. Meta shipped Private Processing v2 and Incognito Chat. OpenAI launched PSP and announced Private Inference. Anthropic launched EFS. The infrastructure vendors are commoditising the plumbing: Cloudflare launched its OHTTP Gateway, and Apple and Cloudflare are standardising ARC anonymous rate-limited credentials at the IETF. Anonymity (as opposed to confidentiality) appears only on consumer device/app surfaces, not in lab or cloud APIs.

### Cited Findings

| Date | Player | Item | Status | Source |
|---|---|---|---|---|
| 29 Apr 2025 | Meta | Private Processing announced | Shipped later in 2025 | [Meta Eng](https://engineering.fb.com/2025/04/29/security/whatsapp-private-processing-ai-tools/) |
| 11 Nov 2025 | Google | Private AI Compute (Magic Cue, Recorder) | SHIPPED (narrow) | [The Hacker News](https://thehackernews.com/2025/11/google-launches-private-ai-compute.html) |
| 16 Dec 2025 | Meta | AI chats used for ad personalisation | SHIPPED | [The Register](https://www.theregister.com/2025/10/01/meta_ai_use_informs_ads/) |
| 12–29 Jan 2026 | Apple/Google | Gemini at core of Apple Foundation Models; runs in PCC | Announced; Siri rollout | [9to5Mac](https://9to5mac.com/2026/01/29/apple-confirms-gemini-powered-siri-will-use-private-cloud-compute/) |
| 14 Jan 2026 | Google | Gemini Personal Intelligence (Gmail/Photos/YouTube/Search) | BETA (US paid) | [Fortune](https://fortune.com/2026/01/14/google-gemini-ai-personal-assistant-gmail-photos-youtube-history-personal-intelligence) |
| 9 Feb 2026 | OpenAI | Ads in ChatGPT Free/Go, using memory | SHIPPED, expanding | [OpenAI Help](https://help.openai.com/en/articles/20001047-ads-in-chatgpt) |
| 16 Mar 2026 | Meta | Private Processing whitepaper V2 (adds web search) | SHIPPED | [Meta whitepaper](https://ai.meta.com/static-resource/private-processing-technical-whitepaper) |
| Mar 2026 | Apple + Cloudflare | IETF ARC drafts (anonymous rate-limited credentials) | IETF draft | [draft-ietf-privacypass-arc-crypto-01](https://datatracker.ietf.org/doc/html/draft-ietf-privacypass-arc-crypto-01); [arc-protocol-01](https://datatracker.ietf.org/doc/html/draft-ietf-privacypass-arc-protocol-01) |
| 13 May 2026 | Meta | Incognito Chat (WhatsApp, Meta AI app) | ROLLING OUT | [Meta Newsroom](https://about.fb.com/news/2026/05/incognito-chat-whatsapp-meta-ai/) |
| 8 Jun 2026 | Apple | PCC on Google Cloud (NVIDIA CC + Intel TDX + Titan) | PREVIEW | [Apple](https://security.apple.com/blog/expanding-pcc/) |
| 9 Jun 2026 | Anthropic | 30-day retention for covered models, including for ZDR orgs | IN FORCE (interim ZDR for some) | [Claude Help Center](https://support.claude.com/en/articles/15425996-data-retention-practices-for-covered-models) |
| 30 Jun–3 Jul 2026 | Academia | WiSec PCC linkability paper | Published | [arXiv](https://arxiv.org/html/2605.24239v1) |
| 20 Aug / 22 Sept 2026 | OpenAI | Private Safety Processing preview, then phased rollout | PREVIEW, rolling out | [TNW](https://thenextweb.com/news/openai-zero-data-retention-private-safety-processing); [TokenPost](https://www.tokenpost.com/news/technology/25495) |
| ~1 Sept 2026 | Anthropic | Enterprise Frontier Safeguards | ANNOUNCED; phased fall 2026 | [Anthropic](https://www.anthropic.com/news/enterprise-frontier-safeguards) |
| 23 Sept 2026 | Google | Private AI Compute secure server-side memory | ANNOUNCED; no date | [Help Net Security](https://www.helpnetsecurity.com/2026/09/24/google-private-ai-compute-server-side-memory/) |
| 29 Sept 2026 | OpenAI | "Private Intelligence": Private Inference on confidential computing | ANNOUNCED; preview "this fall" | [VentureBeat](https://venturebeat.com/security/openais-new-private-intelligence-targets-a-growing-enterprise-concern-who-can-see-your-ai-data) |
| 2 Oct 2026 | Cloudflare | OHTTP Gateway (closed beta); Privacy Gateway renamed "OHTTP Relay" | CLOSED BETA | [Cloudflare](https://blog.cloudflare.com/announcing-cloudflare-ohttp-gateway/) |

- **Cloudflare.**
  - The OHTTP Gateway is a paid zone add-on that decapsulates OHTTP requests so origins see plain HTTP. Customers named: Flo Health (Anonymous Mode), Apple PCC, Apple LiveCallerID.
  - Cloudflare announced no AI-specific gateway — [Cloudflare](https://blog.cloudflare.com/announcing-cloudflare-ohttp-gateway/)
  - Cloudflare supports Privacy Pass (IETF) issuance and redemption — [Cloudflare Privacy Pass docs](https://developers.cloudflare.com/privacy-pass/)
- **Fastly.**
  - Sells an OHTTP Relay product — [Fastly docs](https://docs.fastly.com/products/oblivious-http-relay)
  - Relays Chrome Safe Browsing lookups for Google — [BusinessWire, Mar 2023](https://www.businesswire.com/news/home/20230315005302/en/Google-Selects-Fastly-Oblivious-HTTP-Relay-for-Privacy-Sandbox-Initiative-to-Enhance-Online-Privacy-for-Billions-of-Chrome-Users) **[OLDER]**
  - Is Meta's OHTTP relay and key-config distributor for Private Processing — [Meta whitepaper](https://ai.meta.com/static-resource/private-processing-technical-whitepaper)
- **ARC (IETF).**
  - ARC is a keyed-verification anonymous credential that can be presented a fixed number of times, with each presentation unlinkable. It is built for rate-limiting anonymous clients.
  - Authors: C. Yun and C. A. Wood (Apple) and A. Faz-Hernandez (Cloudflare). Drafts dated March 2026.
  - Source: [IETF draft](https://datatracker.ietf.org/doc/html/draft-ietf-privacypass-arc-crypto-01)
- **Frontier-lab partnerships with confidential-computing or anonymity providers:**
  - Apple–OpenAI: IP-obscured, no-store ChatGPT — [Apple Legal](https://www.apple.com/legal/privacy/data/en/chatgpt-extension/)
  - Apple–Google–NVIDIA: PCC on Google Cloud — [Apple](https://security.apple.com/blog/expanding-pcc/)
  - Meta–Fastly–Cloudflare: relay, key distribution and transparency log — [Meta whitepaper](https://ai.meta.com/static-resource/private-processing-technical-whitepaper)
  - OpenAI–Microsoft/Databricks: PSP early testers — [TNW](https://thenextweb.com/news/openai-zero-data-retention-private-safety-processing)
  - Anthropic–AWS/Google Cloud/Azure: EFS storage — [Anthropic](https://www.anthropic.com/news/enterprise-frontier-safeguards)
  - Anthropic–Irregular (Pattern Labs): confidential-inference design — [Medium summary](https://medium.com/sentora/this-anthropic-research-about-secure-ai-inference-with-tees-can-be-very-relevant-to-web3-65107fa94657)
  - DuckDuckGo with OpenAI, Anthropic and Tinfoil (TEE): anonymised proxy — [DuckDuckGo](https://duckduckgo.com/duckduckgo-help-pages/duckai/ai-chat-privacy)

### Inferences
- The roadmap direction is clear. TEEs plus attestation are becoming the default for "private" frontier inference: OpenAI Private Inference, Apple PCC on NVIDIA/TDX, Google TPU enclaves, Meta CVMs. The relay and token layer is turning into a commodity: Cloudflare's OHTTP Gateway and Relay, Fastly's relay, and IETF ARC. Within 12 months a lab could add OHTTP and anonymous tokens to its API at low engineering cost.
- What the labs are building, though, is *confidential from the provider, identified to the provider*. Their 2026 announcements (PSP, EFS, Private Inference) all keep an accountable customer for misuse detection.

### Gaps
- Microsoft's and AWS's 2025–2026 confidential-AI roadmaps for frontier models (for example, confidential GPUs for Azure OpenAI or Bedrock on Blackwell). I found no primary 2026 announcement.
- Whether OpenAI's "Private Inference" will include an OHTTP/anonymous-token option for end users. The VentureBeat article does not say.
- Whether Apple will offer Gemini (Google-branded) as a ChatGPT-style extension option. Not verified.

---

## Q5. Platform risk: could any incumbent ship anonymous, unlinkable access to its own or rivals' frontier models and undercut a third-party privacy pool?

### Takeaway
The technical capability exists today at Apple, Google and Meta. Commercial will and safety policy are the constraints. The highest risk is **Apple**: it already gives Apple-device users anonymous, no-store access to a rival's model (ChatGPT) and to Gemini-derived models inside PCC, at no charge, and it could add more providers. **Meta** and **Google** risk is mainly to the consumer "private chat with *their* model" segment. **OpenAI and Anthropic** are unlikely to offer per-user anonymous access to *their* frontier models in the near term, because 2026 safety policy explicitly requires cross-session linkability. **Microsoft and AWS** sell confidentiality to identified enterprise tenants. Cloudflare and Fastly are enablers (possible suppliers to a pool), not competitors.

### Cited Findings (evidence underlying the assessment)
- **Apple (high risk, confined to Apple devices):**
  - Anonymous, no-store, no-Apple-Account access to ChatGPT already ships — [Apple Legal](https://www.apple.com/legal/privacy/data/en/chatgpt-extension/)
  - Gemini-based models run in PCC — [9to5Mac](https://9to5mac.com/2026/01/29/apple-confirms-gemini-powered-siri-will-use-private-cloud-compute/)
  - PCC now scales on Google Cloud — [Apple](https://security.apple.com/blog/expanding-pcc/)
  - PCC is free on Apple devices — [arXiv 2605.24239](https://arxiv.org/html/2605.24239v1)
  - Limits: TGTs are issued "per user and per device" to eligible Apple devices. The interface is task-specific with "no general chat interface". The WiSec paper found request linkability through the OTT salt, and Apple did not change the protocol — [arXiv 2605.24239](https://arxiv.org/html/2605.24239v1)
- **Google (medium risk):**
  - The full stack exists: IP-blinding relays, anonymous tokens, TPU enclaves serving "the latest Gemini models" at "millions of user queries per second" — [Google brief](https://services.google.com/fh/files/misc/private_ai_compute_technical_brief.pdf)
  - Google's stated direction is identified, persistent memory and Personal Intelligence, with possible Gemini ads — [Google brief](https://services.google.com/fh/files/misc/private_ai_compute_technical_brief.pdf); [Fortune](https://fortune.com/2026/01/14/google-gemini-ai-personal-assistant-gmail-photos-youtube-history-personal-intelligence); [ALM Corp](https://almcorp.com/blog/google-gemini-ads-not-ruled-out-advertiser-guide-2026/)
- **Meta (medium risk for consumer chat, low for frontier-rival access):**
  - Incognito Chat gives anonymous-credential, OHTTP-relayed, TEE-processed access to Meta AI for WhatsApp and Meta AI app users — [Meta Newsroom](https://about.fb.com/news/2026/05/incognito-chat-whatsapp-meta-ai/); [whitepaper V2](https://ai.meta.com/static-resource/private-processing-technical-whitepaper)
  - Meta's default monetises AI chats through ads — [The Register](https://www.theregister.com/2025/10/01/meta_ai_use_informs_ads/)
- **OpenAI (low risk near term for anonymous; medium for "confidential"):**
  - Private Inference on confidential computing is aimed at enterprises — [VentureBeat](https://venturebeat.com/security/openais-new-private-intelligence-targets-a-growing-enterprise-concern-who-can-see-your-ai-data)
  - PSP keeps cross-interaction safety signals — [Security Boulevard](https://securityboulevard.com/2026/08/openai-unveils-private-safety-processing-to-detect-ai-misuse-without-storing-enterprise-data/)
  - Consumer ChatGPT is ad- and memory-driven — [OpenAI Help](https://help.openai.com/en/articles/20001047-ads-in-chatgpt)
  - Terms require customer accountability for end users, plus export-control KYC and supported-country duties — [OSA](https://cdn.openai.com/osa/openai-services-agreement.pdf)
- **Anthropic (low risk):**
  - 30-day retention on covered models, even for ZDR customers — [Claude Help Center](https://support.claude.com/en/articles/15425996-data-retention-practices-for-covered-models)
  - EFS keeps per-customer monitoring — [Anthropic](https://www.anthropic.com/news/enterprise-frontier-safeguards)
  - Consumer chats are trained on by default — [Business Today](https://www.businesstoday.in/amp/technology/news/story/anthropic-to-use-claude-conversations-for-ai-training-unless-users-opt-out-by-september-28-491530-2025-08-29)
- **Microsoft / AWS (low risk as competitors):**
  - Provider-blind hosting of rival models (Bedrock escrow accounts; Foundry's "NOT available to OpenAI"), but every request is tied to a customer resource ID — [AWS re:Post](https://repost.aws/knowledge-center/amazon-bedrock-model-data-use); [Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-foundry/responsible-ai/openai/data-privacy)
  - Azure did prototype OHTTP with "user anonymity" for Whisper in 2024 — [Microsoft](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/azure-ai-confidential-inferencing-preview/4248181)
- **Cloudflare / Fastly (enablers):**
  - Both sell OHTTP relays, and Cloudflare now also sells a gateway — [Cloudflare](https://blog.cloudflare.com/announcing-cloudflare-ohttp-gateway/); [Fastly](https://docs.fastly.com/products/oblivious-http-relay)
  - Cloudflare co-authors ARC — [IETF](https://datatracker.ietf.org/doc/html/draft-ietf-privacypass-arc-crypto-01)

### Inferences
- **Most plausible undercut:** Apple widening its extension model (more third-party models, or a general chat surface) for its installed base. Today the relationship is one partner model per OS feature with no API, and Apple's privacy guarantees for rival models rest on contract (OpenAI "must not store"), not on TEEs on the rival's side. A pool that offers cross-platform, multi-model, TEE-verifiable access, without needing an Apple device, stays differentiated. Apple could still shrink the iOS consumer addressable market.
- **Second most plausible:** an OpenAI or Google "incognito via OHTTP" consumer mode built on infrastructure that already exists. Their ad and memory incentives make this unlikely to be the default, and the safety-linkability requirement argues against it for top-tier models.
- **Least plausible:** a lab offering *rivals'* models anonymously. Only neutral platforms (Apple, Azure, Bedrock) host multiple labs' models. Azure and Bedrock show no sign of adding end-user anonymity.
- **Structural opening for a pool:** the labs now accept "customer-held" monitoring (EFS, PSP), meaning per-customer linkability stored outside the lab. A pool could be that customer, keeping misuse-detection logs or alerts inside its own TEE or under its own keys while presenting unlinkable members upstream. That is the pattern the labs have signalled they will accept from enterprises and from DuckDuckGo. The main platform risk is contractual (approval under Anthropic §D.4; end-user suspension and export-control KYC under OpenAI §8.1 and §16.11–16.12), not technical.

### Gaps
- No incumbent has publicly said it will, or will not, offer anonymous end-user API access. The assessment above is inference.
- Whether OpenAI's Private Inference preview, or the EFS "third-party offerings", will be open to intermediaries that pool many anonymous end users. Not stated.
- How DuckDuckGo-style agreements hold up under the 2026 covered-model retention rules. The Duck.ai model list includes Claude Opus 4.8 but not Fable/Mythos-class models, which suggests covered models may not be available to anonymous pools under ZDR. Not confirmed.
