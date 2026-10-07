# Anonymous / private access to AI models via proxies, relays and privacy-first chat apps (state as of 7 Oct 2026)

Scope note: research done 7 Oct 2026 with web search plus direct fetches of product sites, docs, GitHub READMEs and press. Several marketing pages (openanonymity.ai blog posts, X posts, GeekWire) were JS-rendered or blocked, so some details come from secondary sources and are flagged. "Crypto guarantee" means a property enforced by cryptography or hardware attestation. "Policy promise" means it holds only if the operator or provider behaves as stated.

## Q1. OpenAnonymity (The Open Anonymity Project): deep profile

### Takeaway
OpenAnonymity is an academic, open-source "unlinkable inference" stack. Users get anonymous tickets through Privacy Pass-style blind signatures. A ticket is redeemed at a "station", which hands out short-lived child API keys on a shared OpenRouter account, and the browser then calls OpenRouter directly with that key. Each session uses a fresh key, so the provider sees unrelated anonymous keys rather than a user. It does not hide prompt content, it does not mix or batch traffic, and on its own it does not guarantee network-level IP anonymity. It is university-funded, has no public pricing, served more than 15k prompts in its Stanford alpha, and on 1 Oct 2026 launched zkAPI (ZK-proof crypto payments) with the Ethereum Foundation.

### Cited Findings
**Team and organisation**
- Created by Ken Liu (CS PhD student, Stanford AI Lab, advised by Percy Liang and Sanmi Koyejo; previously at Google DeepMind, CMU, Meta, Apple, Amazon) and Erik Chi (CS PhD candidate, University of Michigan, advised by J. Alex Halderman; works on network security and anti-censorship; previously on content-moderation systems at ByteDance) — [Brave Technologist podcast e120](https://brave.com/podcast/e120/)
- GitHub org "The Open Anonymity Project" lists two public members, kenziyuliu and erikchi, and links openanonymity.ai — [GitHub org](https://github.com/OpenAnonymity)
- Ken Liu describes it as a "blind, *unlinkable inference* layer where ChatGPT/Claude/Gemini can't tell which call came from which users, like a 'VPN for AI inference'", and says it served ">15k prompts at Stanford so far". Post date not retrievable (X returned 402) — [Ken Liu on X](https://x.com/kenziyuliu/status/2027145028737663259)
- Funding: "currently university-funded". The team is exploring foundation grants, possible venture funding and nonprofit models. The Ethereum Foundation has "expressed interest and collaboration". Alpha users report daily use — [Brave podcast e120](https://brave.com/podcast/e120/)
- One repo is named `oa-chat-gates-foundation` (1 commit, AGPL-3.0, updated 12 Mar 2026). Its README does not explain the Gates Foundation link (grant, pilot deployment or fork) — [repo](https://github.com/OpenAnonymity/oa-chat-gates-foundation); [GitHub org](https://github.com/OpenAnonymity)

**Code (GitHub, as of 6 Oct 2026)**
- oa-chat (JavaScript, MIT, 41 stars, 7 forks, 1,089 commits, updated 6 Oct 2026). Browser chat client with no server backend; history stored in IndexedDB — [oa-chat](https://github.com/OpenAnonymity/oa-chat); [org page](https://github.com/OpenAnonymity)
- oa-verifier (Go, MIT, 9 stars, updated 4 Oct 2026). oa-station-reference (Python, MIT, 5 stars, 2 commits, updated 7 Apr 2026). oa-sdk (Python, AGPL-3.0). oa-android (Kotlin, AGPL-3.0). oa-desktop-builds. nanomem ("Personal memory you own, in files you can actually read", 49 stars, updated 11 Jul 2026) — [GitHub org](https://github.com/OpenAnonymity)
- A third-party fork exists: staccDOTsol/oa-chat — [fork](https://github.com/staccDOTsol/oa-chat)

**Architecture and request flow**
- Station request flow: (1) the user gets blind-signed "inference tickets" from a ticket issuer; (2) POSTs them to `/api/request_key`; (3) the station verifies the tickets without identifying the user; (4) the station issues a "short-lived ephemeral API key" through its configured provider; (5) the user makes inference requests directly with that key. The reference station needs "Your OpenRouter management API key" — [oa-station-reference](https://github.com/OpenAnonymity/oa-station-reference)
- Blinding is done client-side with Cloudflare's open-source `@cloudflare/privacypass-ts`, vendored at `chat/vendor/privacypass-ts/privacypass-ts.min.js` (Apache-2.0). This is a Privacy Pass implementation, not a custom scheme — [oa-chat README](https://github.com/OpenAnonymity/oa-chat); [PRIVACY_MODEL.md](https://github.com/OpenAnonymity/oa-chat/blob/main/docs/PRIVACY_MODEL.md)
- Stations get "separate verified, bounded child keys", and the client "sends both requests directly from the browser". Many users share one OpenRouter account per station, each on separate child keys — [PRIVACY_MODEL.md](https://github.com/OpenAnonymity/oa-chat/blob/main/docs/PRIVACY_MODEL.md)
- Verifier: runs in an AMD SEV-SNP enclave. It checks each OpenRouter station's "Privacy toggles, API key ownership, account binding". It audits for shadow accounts so a station cannot issue keys from an account with logging enabled. Its TLS cert is generated inside the enclave and bound to the attestation. Anyone can rebuild it with Nix and compare hashes. Its role is "station compliance enforcer, not prompt/response transport" — [oa-verifier](https://github.com/OpenAnonymity/oa-verifier); [PRIVACY_MODEL.md](https://github.com/OpenAnonymity/oa-chat/blob/main/docs/PRIVACY_MODEL.md)
- For Open WebUI and other OpenAI-compatible clients, the command-line daemon "has moved to zkapi-clientd" — [oa-chat README](https://github.com/OpenAnonymity/oa-chat)

**Threat model: who sees what (per OA's own docs)**
- Org/station: sees "invitation or billing credential plus blinded requests at issuance; finalized tickets + issued API keys at redemption". It cannot see prompts or responses. If optional Google or username sync is used, it also sees identity mappings and encrypted wallet metadata — [PRIVACY_MODEL.md](https://github.com/OpenAnonymity/oa-chat/blob/main/docs/PRIVACY_MODEL.md)
- Verifier: sees the raw ephemeral key briefly during `/submit_key`, plus a truncated key hash. It sees no content — [PRIVACY_MODEL.md](https://github.com/OpenAnonymity/oa-chat/blob/main/docs/PRIVACY_MODEL.md)
- Inference provider (OpenRouter): "sees prompts and responses from anonymous ephemeral keys" and cannot link them to a user or across sessions, except during the CLI's deliberate key-reuse window — [PRIVACY_MODEL.md](https://github.com/OpenAnonymity/oa-chat/blob/main/docs/PRIVACY_MODEL.md)
- Explicit non-claim: "OA does not claim that prompts are hidden from the inference provider ... The claim is that prompts are _unlinkable_ to your identity." Definition used: "The adversary observing requests cannot tell if 100 requests came from 100 people with 1 request each, or 1 person with 100 requests" — [oa-chat README](https://github.com/OpenAnonymity/oa-chat)
- Trust claim: "Users need not trust any OA-operated component (org, stations, verifier operators)." If all OA components collude, they still cannot read prompts, though they "may attempt to associate a Google identity or stable username with redemption through sync metadata" — [oa-chat README](https://github.com/OpenAnonymity/oa-chat); [PRIVACY_MODEL.md](https://github.com/OpenAnonymity/oa-chat/blob/main/docs/PRIVACY_MODEL.md)
- IP handling: the browser has a built-in proxy that hides the browser IP "from the org/station" for accountless flows. The CLI daemon "defaults to direct HTTPS and local DNS ... exposing the source IP"; an optional Wisp relay can be set. Billing issuance "intentionally exposes subscriber IP". Listed limitation: IP, browser fingerprinting and DNS "remain exposed without additional privacy infrastructure" — [PRIVACY_MODEL.md](https://github.com/OpenAnonymity/oa-chat/blob/main/docs/PRIVACY_MODEL.md)
- Other documented limits: the CLI's default "60-second fixed window shares one credential across eligible calls ... The provider can link those calls". Sync timing and size "remain correlatable metadata". A reused username can be tied to an outside identity — [PRIVACY_MODEL.md](https://github.com/OpenAnonymity/oa-chat/blob/main/docs/PRIVACY_MODEL.md)
- Prompt scrubber: an LLM-based rewriter that redacts PII, neutralises style markers and maps identifiers to stable placeholders. A UMass Amherst study (Pham, Sheils, Singh, Houmansadr; arXiv Sept 2026) tested it alongside StyleRemix and found "text-rewriting defenses still leave users largely vulnerable to re-identification". 50–75% of in-set SWE-Chat users and up to ≈10% of in-set WildChat users were re-identified in at least one conversation — [arXiv 2609.33903](https://arxiv.org/html/2609.33903v1)

**Payments and zkAPI**
- On pricing, the team said it is university-funded and will eventually "have to start setting up payments". This is a search-snippet paraphrase of the podcast — [Brave podcast e120](https://brave.com/podcast/e120/)
- zkAPI was launched 1 Oct 2026 on Ethereum mainnet by the Ethereum Foundation and the Open Anonymity Project. Users deposit ETH or USDC into a vault contract as a private note. A ZK proof on the device shows a request is funded "without revealing which note or deposit funds it". The server then issues a temporary, spend-limited API key. Nullifiers stop double-spends. The client exposes "standard OpenAI and Ollama APIs" locally. Stated limits: no network anonymity; sessions can be re-linked through prompt content; "experimental". The design ("ZK API Usage Credits") was co-authored by Vitalik Buterin and Davide Crapis and published 11 Feb 2026 — [The Block](https://www.theblock.co/news/defi/2026-10-01-ethereum-foundation-launches-zkapi-417504)

**Direction**
- Roadmap: a "secretary model", where a local agent holds personal data and passes only what is needed to remote models. Next stage covers memory management and selective disclosure — [Brave podcast e120](https://brave.com/podcast/e120/). The nanomem repo matches this direction — [GitHub org](https://github.com/OpenAnonymity)
- A blog post titled "Unlinkable Inference as a User Privacy Architecture" exists at [openanonymity.ai/blog/unlinkable-inference](https://openanonymity.ai/blog/unlinkable-inference/), and an apps post at [openanonymity.ai/blog/oa-apps](https://openanonymity.ai/blog/oa-apps/). Both are JS-rendered and could not be read.

### Inferences
- **Blind signatures / Privacy Pass: yes** (via privacypass-ts). **Oblivious HTTP: no evidence.** **Mixing/batching: no.** Unlinkability comes from ephemeral credentials on a shared account, not from traffic mixing. **TEE: only for the verifier**, which audits the station's OpenRouter settings. Inference itself runs in no enclave.
- OA pools users in two layers. Many users share one station's OpenRouter account, and OpenRouter pools all its customers at OpenAI, Anthropic and Google. The frontier providers therefore see OpenRouter, not OA. OpenRouter sees the station account plus per-session child keys.
- Contested point: the browser calls OpenRouter directly, and the docs only say the IP is hidden "from the org/station". OpenRouter may therefore see the user's IP unless a relay or VPN is used. If so, OpenRouter could re-link sessions by IP, and the unlinkability holds mainly against OA and the upstream labs. This needs confirming from code.
- Cryptographic: the ticket-issuance/redemption unlinkability. Hardware-attested: the verifier's code. Policy-dependent: OpenRouter's no-logging toggle (the verifier checks the toggle, not OpenRouter's actual behaviour) and the upstream labs' retention under OpenRouter's terms.
- Within one session the ephemeral key is stable, so a provider can link messages inside that session; the "unlinkable" scope is cross-session.

### Gaps
- Pricing per ticket or subscription, payment rails besides zkAPI (card or Stripe?), and the "invitation" mechanics: not found on any readable page.
- Exact Privacy Pass token type (Type 1 VOPRF vs Type 2 blind RSA, RFC 9578/9474): the docs only name privacypass-ts, which supports both.
- What OpenRouter sees for the browser IP in the default web flow; whether the "built-in proxy" also sits in the inference path.
- Size and terms of the Gates Foundation link, any EF grant amount, user counts beyond ">15k prompts", and whether OpenRouter has approved this use of child keys.
- Text of the two openanonymity.ai blog posts and any formal paper (no arXiv paper by Liu/Chi on OA was found).

## Q2. Profiles of the other products (flow, models, hidden vs promised, pricing, team)

### Takeaway
The field splits into four groups. (a) Big-brand relays (Duck.ai, Brave Leo, Kagi Assistant, Apple's ChatGPT extension) strip IP and account data and send frontier-model requests from the company's own provider accounts, under contracts. (b) Crypto-paid no-account API proxies (nullsink, PayPerQ, nadanada, NanoGPT, LLMTor, 1Privacy, AnonRouter) do the same with prepaid balances. (c) Open-weight or TEE apps (Proton Lumo, Maple, Confer, Venice "Private/TEE/E2EE" tiers) avoid frontier labs entirely. (d) Research systems (OpenAnonymity, zkAPI, ProxyGPT, LLMTor) add blind-signature or ZK unlinkability.

### Cited Findings
**nullsink (nullsink.is)**
- Prepaid API gateway; "no account or email"; one key for many providers; 54 models from Tinfoil, Anthropic and OpenAI — [nullsink.is](https://nullsink.is)
- Flow: nullsink "reads request content in process to validate and meter it, then sends it to the selected model provider". It "connects to the selected provider using its own credentials". Providers see nullsink's IP, but "Information you include in content, metadata, or custom headers may still reach the provider" — [nullsink.is](https://nullsink.is); [trust page](https://nullsink.is/trust/)
- Stored: a SHA-256 hash of the API key, the prepaid balance and temporary payment state. Not stored: accounts, access or request logs, prompts and responses, analytics — [nullsink.is](https://nullsink.is)
- Payment: Monero, on-chain Bitcoin, Lightning; final and non-refundable; model rates plus a service fee added at funding — [nullsink.is](https://nullsink.is); [trust page](https://nullsink.is/trust/)
- Source code is public at [gitlab.com/c99e/nullsink](https://gitlab.com/c99e/nullsink), but "source availability alone does not prove which code or configuration is running". Tinfoil models carry Tinfoil's enclave attestation — [trust page](https://nullsink.is/trust/)
- Team, jurisdiction and abuse policy are not disclosed on the pages read (contact: admin@nullsink.is) — [nullsink.is](https://nullsink.is)

**1Privacy.ai**
- Operated by 1Defender Inc., "subscription-funded", no ads. Products: AI Chat (live), AI Identity (beta soon), AI Cleanup (coming soon) — [1privacy.ai](https://1privacy.ai)
- Flow: TLS 1.3 to a private relay, which removes account ID, IP and session metadata before forwarding. It rotates "API keys frequently enough that traffic-pattern analysis can't cluster requests". The relay itself knows which customer sent each request — [1privacy.ai](https://1privacy.ai)
- 350+ models from 50+ providers (GPT, Claude, Gemini, Llama, Mistral, DeepSeek, Grok, Qwen); from $25/month; paid through the "1Defender Wallet"; recovery email only, no KYC; "0 User logs kept"; no audit or SOC2 yet; no blind tokens — [1privacy.ai](https://1privacy.ai)

**Duck.ai (DuckDuckGo)**
- "All metadata that contains personal information (for example, your IP address) is removed before sending Prompts to underlying model providers." Providers must delete data "at most within 30 days" (with safety and legal exceptions) and may not train on prompts or outputs — [Duck.ai privacy terms](https://duckduckgo.com/duckai/privacy-terms)
- Providers: OpenAI, Anthropic, Azure OpenAI, together.ai, Mistral, plus open-weight models (Gemma 4, GPT-OSS 120B). Chats are stored locally by default, with optional encrypted Sync & Backup — [Duck.ai privacy terms](https://duckduckgo.com/duckai/privacy-terms)
- Requests appear to come from DuckDuckGo, not the individual user. Free tier: GPT-5 mini. Subscribers: GPT-5.2 with a reasoning toggle — [Storyboard18](https://www.storyboard18.com/digital/duckduckgo-enhances-duckai-with-advanced-reasoning-and-privacy-features-ws-l-92523.htm)
- Plans: Plus $9.99/mo or $99.99/yr; Pro $19.99/mo or $199.99/yr with 2x limits and exclusive Claude Opus 4.6 — [Spread Privacy](https://spreadprivacy.com/pro-subscription/)

**Brave Leo**
- Launched 2 Nov 2023 (desktop, v1.60). It now hosts Qwen, Llama and Anthropic Claude (Haiku, Sonnet, Opus). "Requests are routed through a reverse proxy so that they cannot be linked to a user's IP address, and responses are discarded immediately after generation." Premium users get "unlinkable tokens so that payment details cannot be associated with usage". Premium costs $15/mo or $149.99/yr. BYOM and Skills were added Dec 2025 — [Wikipedia: Brave Leo](https://en.wikipedia.org/wiki/Brave_Leo)
- Brave says that since 30 Jun 2025 it hosts all models, including Claude, on its own infrastructure. Before that, most or all models ran on Amazon Bedrock, a fact the community found hard to discover — [Brave support (via search)](https://support.brave.app/hc/articles/26727364100493); [Privacy Guides forum](https://discuss.privacyguides.net/t/how-trustworthy-is-amazon-bedrock-and-brave-leo/33236)
- Nov 2025 (older): TEEs added through NEAR AI on Nvidia confidential computing. Brave checks the attestation and shows a "Verifiably Private with NEAR AI TEE" label. Launched in Nightly with DeepSeek V3.1 only — [Brave blog](https://brave.com/blog/browser-ai-tee/); [Privacy Guides](https://www.privacyguides.org/news/2025/11/20/brave-announces-verifiable-and-transparent-tee-support-in-leo/); [The Register](https://www.theregister.com/2025/11/22/brave_leo_trusted_execution_environment/)

**Kagi Assistant and Kagi Privacy Pass**
- Assistant "is available to all members. However, premium models are only available in our Ultimate plan." Models listed on the page as fetched: OpenAI (GPT 6 Astra, GPT 6.1 Sol, GPT 5.6 Terra and others), Anthropic (Claude 4.5 Haiku, Claude 5.5 Sonnet, Claude Opus 5.5, Claude Fable 5.1), Google Gemini 3.x and 2.5 Pro, and open-weight models from Qwen, DeepSeek, Meta, Mistral, MiniMax, Moonshot, Nous, xAI and Z.ai. "No account information is shared with the LLM providers". Threads are deleted after 24h of inactivity by default — [Kagi Assistant docs](https://help.kagi.com/kagi/ai/assistant.html)
- Privacy Pass covers **Kagi Search only**. Assistant, Maps, Translate and Summarize are "Soon to follow". Limit: 3,000 tokens/month, fetched 300 at a time. Requires Professional, Ultimate, Family or Team (not Starter). Tor is supported through a session link. Personalisation is disabled under Privacy Pass — [Kagi help: Privacy Pass](https://help.kagi.com/kagi/privacy/privacy-pass.html)
- Privacy Pass and a Tor onion service launched Feb 2025 (older) — [AlternativeTo](https://alternativeto.net/news/2025/2/kagi-search-introduces-privacy-pass-and-tor-onion-service-for-enhanced-privacy-and-anonymity); [Kagi blog](https://blog.kagi.com/kagi-privacy-pass)
- Kagi has floated buying tokens without an account (for example with Monero), but it is not shipped — [Kagi feedback thread (via search)](https://kagifeedback.org/d/653-completely-anonymous-searches-unlinked-to-the-account-blind-tokens/5); the [help page](https://help.kagi.com/kagi/privacy/privacy-pass.html) does not mention it
- One source says Assistant is unavailable under Privacy Pass because Kagi cannot check the user's plan without account data. This conflicts with older "Ultimate-only" framing; the current docs say Assistant is on all plans — [Kagi help](https://help.kagi.com/kagi/privacy/privacy-pass.html); [Kagi Assistant docs](https://help.kagi.com/kagi/ai/assistant.html)

**Proton Lumo**
- Uses zero-access encryption and keeps no server logs. Chats are not used for training. At its July 2025 launch (older) it ran open-weight models: Mistral Small 3, OLMo 2 32B, OpenHands 32B, behind a router — [TechRadar review](https://techradar.com/pro/lumo-ai-review); [UC Today](https://www.uctoday.com/unified-communications/proton-enters-ai-race-with-lumo-a-privacy-first-alternative-to-big-tech-chatbots/)
- Lumo 2.0 (30 Jun 2026) runs Qwen 3.5 and GLM 5.2 on Proton-controlled servers. It added thinking mode, image generation, memory and web search. Free use needs no Proton account. Lumo Plus is $12.99/mo; Lumo Professional is $14.99/user/mo — [MacRumors](https://macrumors.com/2026/06/30/proton-lumo-version-2-new-features); [Engadget](https://www.engadget.com/2204704/proton-lumo-2-0-image-generation/?rand=26687)

**Venice.ai**
- Series A of $65M at a $1B valuation (1 Jul 2026), led by Dragonfly, with North Island, Coinbase Ventures, F-Prime, Archetype, Morgan Creek, Liquid2 and Founders' Co-op. Metrics: 3.5M registered users, 1.3T tokens/month, profitable in Q1 2026, ~45 staff (15 a year earlier). CEO Erik Voorhees (ShapeShift); President/CTO Jesse Proudman (Blue Box, sold to IBM). Over 200 open and proprietary models. The money goes to owned data centres and GPUs — [SiliconANGLE](https://siliconangle.com/2026/07/01/venice-raises-65m-1b-valuation-private-uncensored-ai/)
- Revenue: ARR above $70M at the raise — [AI Weekly](https://aiweekly.co/alerts/venice-ai-raises-65m-at-1b-tops-70m-arr-on-privacy-pitch). Search aggregators also report about 1.7M API calls/day and 3M users in April 2026 — [Dealroom](https://dealroom.co/companies/venice-ai/), [Cryptonomist](https://en.cryptonomist.ch/2026/07/01/privacy-first-ai-platform-venice/) (unverified per-figure attribution)
- Privacy modes, per Venice's own page:
  - Anonymous: proxied GPT, Claude and Gemini; "your identity is obscured from the provider", but users should "assume the provider is storing your content".
  - Private: runs on Venice GPUs or zero-retention partners (including Grok).
  - TEE: NEAR AI Cloud and Phala.
  - E2EE: encrypted on the device and decrypted only inside a verified TEE.
  - Conversation history stays on the device, and requests are "relayed without being stored". TEE and E2EE need Pro.

  Source: [Venice privacy](https://venice.ai/privacy)
- Pricing: Free (10 text prompts/day); Pro $18/mo; Pro Plus $68/mo; Max $200/mo — [Venice pricing](https://venice.ai/pricing)
- Tokens: VVV is on Base. Staking it gives a pro-rata share of API capacity. DIEM is minted by locking staked VVV and pays $1/day of API credit. Emissions were cut from 8M to 6M VVV/yr on 10 Feb 2026 — [KuCoin blog](https://www.kucoin.com/blog/vn-why-did-vvv-price-surge-so-rapidly-in-2026); [Venice help: tokenomics](https://veniceai.featurebase.app/help/articles/8403626-what-are-the-tokenomics-of-the-venice-token-vvv) (both via search snippets, not fetched)

**AnonRouter (anonrouter.ai)**
- Run by "Northstar Labs". Exposes an OpenAI-compatible API at api.anonrouter.ai/v1 with 215+ models (Claude, OpenAI, Gemini, Grok, Qwen, DeepSeek and others). Four tiers: Anonymous, Private, TEE (Intel TDX), E2EE ("prompts are sealed in your browser and opened only inside the enclave"). Content plane is open source at github.com/anonrouter/confidential-content-plane. Fee 5% promo (8% regular, $0.75 minimum); credits from $1; no blind tokens — [anonrouter.ai](https://anonrouter.ai/)

**PayPerQ (ppq.ai)**
- Founded Feb 2024 by Matt Ahlborg (CTO Rafael Valverde). "No registration required. Pay-per-use. No subscriptions." Top-ups from 10 cents by crypto or card; average ~2 cents/query, ~$4/month. Models from OpenAI, Anthropic, Mistral and Gemini, plus TEE models where prompts are "encrypted in your browser — not even PayPerQ can see them" — [ppq.ai](https://ppq.ai/); [PayPerQ TEE blog](https://www.ppq.ai/blog/introducing-tee-models)

**Others in the long tail**
- nadanada: no account, no conversation logs; GPT, Claude, Grok, DeepSeek, Perplexity Sonar; pay with Lightning, Monero, ETH, SOL, USDT or USDC — [nadanada blog](https://nadanada.me/blog/free-anonymous-ai-chat-no-signup-no-logs)
- NanoGPT: frontier models without a subscription — [search listing](https://monerica.com/tagged/api-available/page/2)
- Veila strips identifying data before forwarding to OpenAI and stores chats end-to-end encrypted — [Product Hunt](https://www.producthunt.com/products/veila). AInonymous (iOS) acts as an "anonymous middle layer" — [App Store](https://apps.apple.com/py/app/ainonymous/id6736578072)
- LLMTor (Show HN): users buy credits and receive blind RSA tokens (RFC 9474), then redeem token plus prompt over Tor. The builder ("codemastercpp") admits that banning abusers needs "one permanent blind RSA token per user", which "technically increases the surface area". Whitepaper and GitHub at llmtor.com — [HN](https://news.ycombinator.com/item?id=47298201)
- ProxyGPT (UMass research, Jul 2024, revised Jun 2025; older): volunteer browser proxies submit queries through their own chatbot accounts. Uses Chaum blind-signature e-cash as an incentive, TLS-provenance web proofs for audits, and prompt guards — [arXiv 2407.08792](https://arxiv.org/abs/2407.08792)
- Maple AI (OpenSecret): end-to-end encrypted chat on open models in secure enclaves. Free (10 chats/week), Starter $5.99, Pro $20; card or Bitcoin — [Techlore discussion](https://discuss.techlore.tech/t/maple-ai-encrypted-ai-chat/12952); [Privacy Guides forum](https://discuss.privacyguides.net/t/privacy-using-maple-ai/34503)
- Confer (Moxie Marlinspike; launched Dec 2025): encryption keyed to WebAuthn passkeys, inference in a TEE with remote attestation — [TechCrunch](https://techcrunch.com/2026/01/18/moxie-marlinspike-has-a-privacy-conscious-alternative-to-chatgpt); [SC World](https://www.scworld.com/brief/signal-founder-launches-confer-an-encrypted-ai-chat-alternative)
- Apple Intelligence ChatGPT extension, signed out: Apple obscures the IP; OpenAI may not store requests or train on them; no Apple Account data is shared; approximate region is shared for fraud and legal reasons — [Apple legal: third-party AI](https://www.apple.com/legal/privacy/data/en/third-party-ai/); [BGR](https://bgr.com/business/apple-reveals-how-its-chatgpt-integration-works-on-iphone-and-mac/)

### Inferences
- Brave says Claude runs on "Brave's own infrastructure", but Anthropic does not release Claude weights. This most likely means a Brave-controlled cloud tenancy (for example a Bedrock or Vertex account), not self-hosted weights. Treat it as a policy and contract arrangement.
- In Lumo, Maple, Confer and the Venice TEE/E2EE tiers, "zero-access" or E2EE protects stored history or the transport. Plaintext still exists on the inference GPU, protected by policy (Lumo) or by attestation (TEE apps).
- AnonRouter's and PayPerQ's TEE/E2EE tiers can only cover open models in their own enclaves. For Claude, GPT and Gemini the prompt must leave the enclave in plaintext to the lab.

### Gaps
- 1Privacy: whether the "350+ models / 50+ providers" are reached through an aggregator such as OpenRouter; team names; traction.
- nullsink: operator identity and jurisdiction, upstream contract terms, abuse policy.
- Duck.ai, Brave Leo, Kagi Assistant: user numbers specific to the AI products (none found).
- Venice: a later aggregator figure (>4M users and >$100M run-rate by Sep 2026) could not be traced to a primary source. VVV market cap (~$1.5B in Sep 2026 per aggregators) is unverified.

## Q3. Which products pool many users behind shared upstream provider accounts?

### Takeaway
Pooling is already standard. Every big-brand relay and every no-account crypto proxy that offers closed frontier models sends user requests from the operator's own provider account, so the lab sees one customer. What separates them is whether the operator can tell users apart. Only OpenAnonymity, zkAPI, LLMTor and ProxyGPT make the operator itself cryptographically unable to link users.

### Cited Findings
- OpenAnonymity: many users share one OpenRouter account per station, each on ephemeral child keys — [PRIVACY_MODEL.md](https://github.com/OpenAnonymity/oa-chat/blob/main/docs/PRIVACY_MODEL.md); [oa-station-reference](https://github.com/OpenAnonymity/oa-station-reference)
- nullsink: "connects to the selected provider using its own credentials" — [trust page](https://nullsink.is/trust/)
- 1Privacy: a relay strips account, IP and session data and rotates API keys "frequently enough that traffic-pattern analysis can't cluster requests" — [1privacy.ai](https://1privacy.ai)
- Duck.ai: requests are "anonymous" and appear to come from DuckDuckGo — [Duck.ai privacy terms](https://duckduckgo.com/duckai/privacy-terms); [Storyboard18](https://www.storyboard18.com/digital/duckduckgo-enhances-duckai-with-advanced-reasoning-and-privacy-features-ws-l-92523.htm)
- Brave Leo: a reverse proxy hides the IP; models run on Brave's infrastructure — [Wikipedia](https://en.wikipedia.org/wiki/Brave_Leo)
- Kagi Assistant: "no account information is shared with the LLM providers" — [Kagi docs](https://help.kagi.com/kagi/ai/assistant.html)
- Venice "Anonymous" mode: "your identity is obscured from the provider" for GPT, Claude and Gemini — [Venice privacy](https://venice.ai/privacy)
- Apple's signed-out ChatGPT: IP obscured, no Apple Account data — [Apple](https://www.apple.com/legal/privacy/data/en/third-party-ai/)
- ProxyGPT: mixes users behind volunteers' consumer chatbot accounts — [arXiv](https://arxiv.org/abs/2407.08792)
- The UMass study groups ProxyGPT, OpenAnonymity, Brave Leo, AnonChatGPT, DuckAI, Venice and PayPerQ as anonymising proxies that "exchange content confidentiality for operational practicality" — [arXiv 2609.33903](https://arxiv.org/html/2609.33903v1)

### Inferences
- Full pooling list (frontier models from a shared operator account): OpenAnonymity (through OpenRouter), nullsink, 1Privacy, Duck.ai, Brave Leo, Kagi Assistant, Venice Anonymous mode, PayPerQ, nadanada, NanoGPT, AnonRouter (Anonymous tier), LLMTor, Apple–ChatGPT, ProxyGPT (consumer accounts). Pooling for PayPerQ, nadanada, NanoGPT and AnonRouter is inferred from their no-account model, not stated.
- Pooling only defeats provider-side identification. In every case except the blind-token systems, the operator holds a full user-to-prompt map in memory and is trusted not to log it.
- 1Privacy's key rotation targets traffic-pattern clustering at the provider, which other pooled relays do not claim. It is still policy, because 1Privacy chooses which user's requests go on which key.

### Gaps
- No product publishes how many users share each upstream key or account (the anonymity-set size), or whether providers have agreed to it in writing beyond Duck.ai's and Apple's contract summaries.

## Q4. Cryptographic unlinkability vs no-logging promises

### Takeaway
Cryptographic unlinkability between payment or identity and usage exists in only a few places: OpenAnonymity (Privacy Pass blind signatures), zkAPI (ZK proofs plus nullifiers), LLMTor (blind RSA over Tor), Kagi (Privacy Pass, Search only, not Assistant), Brave Leo Premium ("unlinkable tokens"), and ProxyGPT (blind e-cash, research only). TEE attestation is a second category of hardware-backed guarantee, used by Brave/NEAR, Venice, Maple, Confer, AnonRouter, PayPerQ and Tinfoil through nullsink. It protects content from the operator, but only for models running in enclaves, never for GPT, Claude or Gemini. Everything else rests on no-logging policy.

### Cited Findings
- OA: blinding via `@cloudflare/privacypass-ts` ensures "no party can link ticket issuance to ticket redemption". The verifier is SEV-SNP-attested. Station privacy toggles are checked through the provider's own APIs, which is trust-based — [PRIVACY_MODEL.md](https://github.com/OpenAnonymity/oa-chat/blob/main/docs/PRIVACY_MODEL.md)
- zkAPI: ZK proof of a funded note with nullifiers; "does not provide network anonymity" — [The Block](https://www.theblock.co/news/defi/2026-10-01-ethereum-foundation-launches-zkapi-417504)
- LLMTor: blind RSA (RFC 9474) plus Tor — [HN](https://news.ycombinator.com/item?id=47298201)
- Kagi Privacy Pass: Search only; Assistant "soon to follow" — [Kagi help](https://help.kagi.com/kagi/privacy/privacy-pass.html)
- Brave Leo Premium: "unlinkable tokens so that payment details cannot be associated with usage" — [Wikipedia](https://en.wikipedia.org/wiki/Brave_Leo)
- Policy-only examples: Duck.ai (removes IP, provider deletes within 30 days by contract) — [Duck.ai terms](https://duckduckgo.com/duckai/privacy-terms); nullsink (no logs; "You trust the nullsink operator") — [trust page](https://nullsink.is/trust/); 1Privacy ("0 User logs kept", no audit) — [1privacy.ai](https://1privacy.ai); Venice Anonymous mode — [Venice privacy](https://venice.ai/privacy)
- TEE examples: Brave/NEAR AI with attestation checked client-side — [Brave blog](https://brave.com/blog/browser-ai-tee/); Venice TEE/E2EE via NEAR AI and Phala — [Venice privacy](https://venice.ai/privacy); Confer — [TechCrunch](https://techcrunch.com/2026/01/18/moxie-marlinspike-has-a-privacy-conscious-alternative-to-chatgpt); AnonRouter Intel TDX — [anonrouter.ai](https://anonrouter.ai/)

### Inferences
- Even the blind-token systems only unlink payment from usage. Prompt content is still visible to the provider (and to OpenRouter for OA) and is policy-protected. The UMass result shows that content alone re-identifies many users.
- Brave's "unlinkable tokens" are a cryptographic claim, but the scheme is not documented in the sources read. Its IP-stripping reverse proxy is policy.
- No product found uses Oblivious HTTP (RFC 9458) for AI requests. The only network-layer anonymity tools seen are Tor (LLMTor, Kagi onion) and an optional Wisp relay (OA CLI).

### Gaps
- Brave's token scheme (possibly derived from Privacy Pass) and whether Leo free-tier rate limiting uses tokens: not sourced.
- Kagi's token type (VOPRF vs blind RSA): not stated on the help page.

## Q5. Payment rails, abuse handling and provider terms of service

### Takeaway
Crypto-first no-account services (nullsink: XMR/BTC/Lightning; nadanada: XMR, Lightning and stablecoins; PayPerQ: crypto or card; zkAPI: ETH/USDC with ZK) contrast with card subscriptions at the brands (Duck.ai, Brave, Kagi, Proton, Venice, 1Privacy). Abuse handling is mostly undocumented. The only explicit designs are LLMTor's permanent per-user ban token, ProxyGPT's prompt guards and Duck.ai's user reporting. Provider-ToS compliance is solved by contract at Duck.ai and Apple, delegated to OpenRouter at OA, and not addressed elsewhere.

### Cited Findings
- nullsink: Monero, on-chain BTC and Lightning; non-refundable; abuse policy not stated — [nullsink.is](https://nullsink.is); [trust page](https://nullsink.is/trust/)
- nadanada: Lightning, Monero, ETH, SOL, USDT, USDC — [nadanada](https://nadanada.me/blog/free-anonymous-ai-chat-no-signup-no-logs)
- PayPerQ: crypto or card from 10 cents; also sold as Bitrefill gift cards — [ppq.ai](https://ppq.ai/); [Bitrefill](https://cwstaging.bitrefill.com/lc/en/gift-cards/ppq-ai-international/)
- zkAPI: ETH or USDC deposited into a vault; double-spend attempts expose "the attempt and nothing else" — [The Block](https://www.theblock.co/news/defi/2026-10-01-ethereum-foundation-launches-zkapi-417504)
- OA billing issuance "intentionally exposes subscriber IP for identity-bound payment authorization" — [PRIVACY_MODEL.md](https://github.com/OpenAnonymity/oa-chat/blob/main/docs/PRIVACY_MODEL.md)
- Maple: card or Bitcoin — [Techlore](https://discuss.techlore.tech/t/maple-ai-encrypted-ai-chat/12952). 1Privacy: 1Defender Wallet, no crypto mentioned — [1privacy.ai](https://1privacy.ai). Venice: subscriptions plus VVV staking and DIEM API credit — [Venice pricing](https://venice.ai/pricing); [KuCoin](https://www.kucoin.com/blog/vn-why-did-vvv-price-surge-so-rapidly-in-2026)
- Abuse: LLMTor's ban token trade-off — [HN](https://news.ycombinator.com/item?id=47298201); ProxyGPT's prompt guards and TLS-provenance audits — [arXiv](https://arxiv.org/abs/2407.08792); Duck.ai's "Harmful or illegal" feedback and provider retention "for safety and legal compliance" — [Duck.ai terms](https://duckduckgo.com/duckai/privacy-terms)
- Provider terms: Duck.ai's providers agree to data-use limits — [Duck.ai terms](https://duckduckgo.com/duckai/privacy-terms). Apple's contract with OpenAI bars storage and training — [Apple](https://www.apple.com/legal/privacy/data/en/third-party-ai/). OA relies on OpenRouter account toggles — [oa-verifier](https://github.com/OpenAnonymity/oa-verifier). The LLMTor builder notes "LLM providers are required to break user privacy if needed" — [HN](https://news.ycombinator.com/item?id=47298201)

### Inferences
- Small crypto proxies probably resell under standard API terms. Abuse from anonymous users falls on the operator's shared key, which risks a ban for every user at once. None documents mitigation.
- OA's design avoids direct reselling to labs by using OpenRouter, but OpenRouter's own abuse controls then apply per station account.

### Gaps
- Whether Anthropic, OpenAI or Google has formally objected to, or approved, any of the small anonymous proxies; whether OpenRouter allows anonymous child-key distribution.

## Q6. Comparison and the gaps none of them close

### Takeaway
No product delivers all of: frontier closed models, cryptographic unlinkability from the operator, network-layer anonymity, a large published anonymity set, and abuse controls compatible with provider terms. OpenAnonymity plus zkAPI comes closest on cryptographic unlinkability. Duck.ai, Brave, Kagi and Apple come closest on scale and contracts. Venice comes closest on commercial traction.

### Cited Findings
- Content re-identification: 50–75% of in-set SWE-Chat users and up to about 10% of WildChat users were re-identified despite text defenses — [arXiv 2609.33903](https://arxiv.org/html/2609.33903v1)
- zkAPI itself lists network-level and content-level linkability as limits — [The Block](https://www.theblock.co/news/defi/2026-10-01-ethereum-foundation-launches-zkapi-417504)
- OA lists IP, fingerprinting and DNS exposure as limits — [PRIVACY_MODEL.md](https://github.com/OpenAnonymity/oa-chat/blob/main/docs/PRIVACY_MODEL.md)

### Inferences
Comparison table. It synthesises the cited facts above; see Q1–Q5 for sources. "Pool" means the provider sees the operator's account, not the user's. "Crypto-unlink" means the operator cannot link payment or identity to usage.

| Product | Frontier closed models | Open-weight / TEE | Pool at provider | Crypto-unlink from operator | Network anonymity | Payment | Pricing | Funding / traction |
|---|---|---|---|---|---|---|---|---|
| OpenAnonymity | Yes, via OpenRouter | Some open models via OpenRouter; verifier in SEV-SNP | Yes (station OpenRouter account → OpenRouter) | Yes (Privacy Pass blind sigs) | Partial (browser proxy hides IP from OA; CLI exposes IP) | Invitation or billing; zkAPI ETH/USDC | Not public | University-funded; >15k prompts; EF zkAPI partner |
| zkAPI (EF + OA) | Depends on server | n/a | Yes | Yes (ZK + nullifiers) | No | ETH/USDC | n/a | Launched 1 Oct 2026 |
| LLMTor | Yes | n/a | Yes | Yes (blind RSA) | Yes (Tor) | Credits (rails unknown) | Unknown | Solo dev |
| nullsink | Anthropic, OpenAI | Tinfoil TEE | Yes | No (policy) | No | XMR/BTC/LN | Model rate + fee | Unknown |
| 1Privacy | Yes (350+ models) | n/a | Yes, rotating keys | No (policy) | No | Wallet/subscription | From $25/mo | Unknown |
| AnonRouter | Yes (215+) | Intel TDX, E2EE | Yes (inferred) | No | No | Credits | 5–8% fee | Unknown |
| PayPerQ | Yes | TEE models | Yes (inferred) | No | No | Crypto, card | ~2¢/query | Founded Feb 2024 |
| Duck.ai | GPT-5.x, Claude Opus 4.6 | Gemma 4, GPT-OSS | Yes (contracted) | No | IP stripped (policy) | Card subscription | Free; $9.99 / $19.99 | DuckDuckGo |
| Brave Leo | Claude Haiku/Sonnet/Opus | Llama, Qwen; NEAR TEE (Nightly) | Yes | Premium tokens (scheme undocumented) | Reverse proxy (policy) | Subscription | Free; $15/mo | Brave |
| Kagi Assistant | GPT, Claude, Gemini | Many open models | Yes | Not for Assistant (Search only) | Tor onion for Search | Subscription | Ultimate for premium models | Kagi |
| Proton Lumo | No | Qwen 3.5, GLM 5.2 (Proton servers) | n/a | No | No | Subscription | Free; $12.99/mo | Proton |
| Venice | Anonymous mode (GPT/Claude/Gemini) | Private, TEE, E2EE | Yes | No | No | Card, VVV/DIEM | $18–$200/mo | $65M at $1B; >$70M ARR; 3.5M users |
| Maple / Confer | No | TEE + E2EE | n/a | No | No | Card/BTC (Maple) | Maple $5.99–$20 | Confer: Moxie |
| Apple–ChatGPT | ChatGPT | n/a | Yes (contracted) | No | IP obscured (policy) | Free | Free | Apple |

Gaps none of them close:
1. **Prompt-content linkability.** No product hides content from the frontier lab, and text scrubbing fails per the UMass study.
2. **The operator sees content in plaintext** (nullsink says so explicitly) for all frontier-model relays. TEEs cannot help because the lab needs plaintext.
3. **No published anonymity-set sizes** or traffic mixing, batching or timing padding. Pooling without mixing leaves timing and size correlation open to a lab–relay collusion.
4. **No OHTTP-style separation** of the network relay from the token or inference gateway for AI traffic. OA and zkAPI both leave IP exposure to the user.
5. **Abuse versus anonymity is unsolved.** LLMTor's permanent ban token re-introduces linkability; others are silent. Shared keys risk mass bans.
6. **No provider-sanctioned anonymous-access tier** outside contracted big-brand deals (Duck.ai, Apple).
7. **Kagi's Privacy Pass does not cover Assistant.** Brave's tokens are undocumented. No big brand combines cryptographic unlinkability with frontier models in production.

### Gaps
- Head-to-head anonymity-set size, latency overhead and upstream retention terms per product were not available from any source.
