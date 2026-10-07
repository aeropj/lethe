# Decentralized and Crypto-Native Private AI Inference Networks (as of October 7, 2026)

Scope note: covers NEAR AI Cloud, Phala Cloud (plus RedPill), Secret Network / Secret AI, Nillion (nilAI), Atoma, Ritual, Fortytwo, Gensyn, Bittensor's Chutes (SN64) and Targon (SN4), and Venice (VVV) only where it touches private-inference economics. Also SayGm, a TEE-hosted AI gateway that showed up as a partner of both NEAR AI and Phala and is the closest direct analogue to "a privacy pool in front of GPT/Claude/Gemini". Token prices come from a live CoinGecko API pull on 2026-10-07 13:15 UTC (`api.coingecko.com/api/v3/simple/price` and `/coins/{id}`). Nearly every usage metric below is self-reported by the project. Treat them as marketing unless stated otherwise.

---

## 1. Network-by-network profiles (product, architecture, trust model, models, team, funding)

### Takeaway
In practice almost every "decentralized private inference" product in 2026 works the same way. Open-weight models run inside Intel TDX confidential VMs attached to NVIDIA H100/H200/B200-class GPUs in confidential-computing mode, and the provider hands back remote-attestation reports. MPC and FHE (Nillion's pitch, Secret's heritage) are not what serves LLM traffic: Nillion's own nilAI docs say nilAI runs in NVIDIA confidential-computing TEEs. The real differences are who operates the hardware (one company versus a set of node operators), whether attestation can be checked by the client or only by a gateway, and how the token is attached.

### Cited Findings

#### NEAR AI Cloud / NEAR AI Private Chat (NEAR Protocol; co-founder Illia Polosukhin)
- Launch: NEAR AI Cloud and Private Chat were announced on **December 3, 2025**. Prompts are encrypted locally, processed in a TEE built on Intel TDX plus NVIDIA Confidential Computing, and signed proofs can be checked at `/v1/attestation/report?model=...`. Claimed overhead is about 5-10% latency, scaling to 100 requests/sec per tenant. — [NEAR AI blog, Dec 3 2025](https://near.ai/blog/introducing-near-ai-cloud-private-chat)
- Launch customers were Brave Nightly, OpenMind (robotics OS) and Phala. NEAR cites a "combined reach" of more than 100 million users. That is a reach figure for the partners, not NEAR AI usage. — [NEAR AI blog](https://near.ai/blog/introducing-near-ai-cloud-private-chat)
- NEAR says the protection covers prompts, model weights and outputs, isolated "from infrastructure providers, model owners, and NEAR AI itself". — [NEAR AI blog: SayGm](https://near.ai/blog/nearai-cloud-on-saygm-verifiable-confidential-inference)
- Models listed in September 2026, all open-weight: DeepSeek V4 Flash / V4.1 Flash, GLM 5.3 Flash, Kimi K2.6 and K3, and Qwen 3.x including a vision-language model. The direct API also offers embeddings, rerankers, image generation and speech-to-text. — [NEAR AI blog: SayGm, Sep 18 2026](https://near.ai/blog/nearai-cloud-on-saygm-verifiable-confidential-inference); [NEAR AI blog: OpenRouter, Sep 28 2026](https://near.ai/blog/near-ai-cloud-on-openrouter)
- Pricing is pay-per-token with no subscriptions or seat licenses. Attestation reports are free and can be verified against Intel and NVIDIA. — [NEAR AI blog: OpenRouter](https://near.ai/blog/near-ai-cloud-on-openrouter)
- Intel Trust Authority was integrated for independent attestation on Aug 12, 2026. — [NEAR AI blog index](https://near.ai/blog); [Coinfomania](https://coinfomania.com/intel-reveals-near-ai-cloud-now-runs-confidential-inference/)
- Other 2026 launches from the blog index: IronClaw 1.0 agent (Jul 27); staking for NEAR AI (Jul 30); NEAR AI Private Inference in Corbits (Jul 15); private USDC payments via "Confidential Intents" (May 14); Government of Bermuda AI assistant (May 13); Abound (Times of India Group fintech) cross-border agentic payments (Apr 2); "Venice Is Now Verifiably Private With NEAR AI" (Mar 19); "Assume We're Lying: How to Verify Private Inference" (Oct 2). — [NEAR AI blog index](https://near.ai/blog)
- On Oct 1, 2026 NEAR released a VSCode extension that lets GitHub Copilot use models hosted on NEAR AI Cloud. — [CryptoBriefing](https://cryptobriefing.com/near-ai-private-inference-github-copilot/)
- Operator model: NEAR AI's own materials describe NEAR AI running the TEE fleet. I found no documentation of independent third-party node operators serving NEAR AI Cloud traffic. — [NEAR AI blog](https://near.ai/blog/introducing-near-ai-cloud-private-chat)

#### Phala Network / Phala Cloud (CEO Marvin Tong, CTO Hang Yin)
- Products: Confidential VM (CPU TEE), GPU TEE (H100/H200/B300), Confidential AI Models (LLM endpoints), a Model Catalog, and the dStack SDK. — [phala.com](https://phala.com/)
- GPU TEE pricing has two conflicting readings of Phala's own pages. One shows H100 from $3.08/hr, H200 $4.80/hr and B300 $6.50/hr. The homepage fetch showed H200 $3.20/hr and B300 $5.60/hr. — [phala.com/gpu-tee via search](https://phala.com/gpu-tee); [phala.com](https://phala.com/)
- Confidential AI model pricing runs from $0.07/M input tokens (NVIDIA Nemotron) to $3.00/M (Kimi K3). DeepSeek is about $0.44/M and Qwen variants $0.12-$0.32/M. — [Phala Confidential AI Models](https://phala.com/confidential-ai-models)
- Architecture is two-hop RA-TLS. The client's TLS connection terminates inside a dstack-gateway confidential VM whose certificate carries its TDX quote. A second hop terminates inside the model confidential VM (TDX+H100 quote). Phala says there is "no plaintext intermediary". Each response carries `x-phala-receipt-sig` and `x-phala-compose-hash`, which chain to the TDX root and an on-chain `DstackApp.sol` registry entry. — [Phala private AI inference page](https://phala.com/solutions/private-ai-inference); [Phala search snippet](https://phala.com/de/solutions/private-ai-inference)
- Single endpoint `https://inference.phala.com/v1`. Clients filter with `is_tee: true` to find models that are actually confidential. The docs warn that observability tools (e.g., Langfuse) "may store prompts, responses, metadata, or traces". — [Phala docs: migration and integrations](https://docs.phala.com/phala-cloud/confidential-ai/confidential-model/migration-and-integrations)
- Team: CEO Marvin Tong (ex-Tencent, Didi) and CTO Hang Yin (ex-Google, Bitcoin Gold founder). This comes from a price-page profile blurb, a weak source. — [CoinDesk PHA page](https://www.coindesk.com/price/pha)
- Chain: Phala's community voted to leave its Polkadot parachain and become an Ethereum L2, with a 1:1 ERC-20 migration. **This is October 2025 information.** — [FXStreet, Oct 10 2025](https://www.fxstreet.com/cryptocurrencies/news/ai-polkadot-parachain-phala-votes-to-fully-switch-to-ethereum-l2-202510100604)
- Funding: sources are poor and conflict. One says more than $10M raised by end of 2020; CB Insights shows "$1M over 2 rounds". Private-round investors included IOSG, SNZ, Alameda Research, Mask Network and others. **Old (2020-era) and unreliable.** — [CB Insights](https://www.cbinsights.com/company/phala-network/financials); [ICO Drops](https://icodrops.com/phala-network/)

#### RedPill (gateway built on Phala)
- RedPill markets more than 200 models, "all protected by a TEE proxy", including GPT, Claude and Gemini, plus Phala-GPU-TEE-hosted open models built with private-ml-sdk. Phala Cloud's LLM inference API historically connected through RedPill. — [Phala case study: RedPill](https://cloud.phala.network/cases/redpill); [Phala docs (older)](https://docs.phala.network/llm-in-gpu-tee/inference-api); [RedPill GitHub](https://github.com/redpill-ai)

#### Secret Network / Secret AI / SecretVM (Secret Labs)
- Secret AI is described as "a Decentralized Confidential Computing solution". It uses NVIDIA Confidential Computing on GPU workers paired with Intel TDX and AMD SEV confidential VMs. — [Secret docs: Secret AI intro](https://docs.scrt.network/secret-network-documentation/secret-ai/introduction); [Secret docs: architecture](https://docs.scrt.network/secret-network-documentation/secret-ai/architecture)
- Off-chain GPU workers register with a `WorkerManager` smart contract and are attested, with the attestation stored on-chain. Workers report input and output token counts to a `RewardsManager` contract, and user payments are split among worker operators by work done. Each "Service" has its own model set, pricing and access policy. — [Secret docs: architecture](https://docs.scrt.network/secret-network-documentation/secret-ai/architecture)
- In 2025 Secret built SecretAI/SecretVM with billing, a KMS, verifiable message signing and posting of attestations to third-party chains. The 2026 roadmap adds SecretVM on Azure (Intel/AMD), GCP (Intel/AMD) and AWS (AMD). The direct roadmap URL returned 404 and Medium returned 403, so this rests on the search snippet. — [Secret 2026 roadmap (X post)](https://x.com/SecretNetwork/status/2010859443257593969); [Medium roadmap post](https://medium.com/secret-network-ecosystem-and-technology/2026-secret-network-roadmap-update-ec340c9efceb)
- 2026 partnerships: AITECH Agent Forge (Aug 2026) and Morpheus (Aug 7, 2026) for TEE execution of AI models. — [Yahoo Finance](https://finance.yahoo.com/technology/ai/articles/aitech-cloud-network-secret-network-181100795.html); [BitcoinWorld](https://bitcoinworld.co.in/aitech-cloud-network-and-secret-network-partner-to-bring-confidential-ai-to-agent-forge/)

#### Nillion (nilAI, nilDB, nilCC; "Blind Computer")
- Marketing describes MPC + homomorphic encryption + TEEs in a modular "blind computer". — [Bex blog, Jan 2026](https://bex.co/blog/2026/01/13/nillion-blind-computing-privacy-execution-mpc-fhe-tee)
- **In practice, nilAI LLM inference runs in a TEE on NVIDIA Confidential Computing, not MPC.** Every chat completion is signed so it can be traced back to the attested environment. Documented models are `google/gemma-4-26B-A4B-it` and `Qwen/Qwen3.6-35B-A3B`. — [Nillion docs: LLMs overview](https://docs.nillion.com/blind-computer/build/llms/overview)
- Earlier materials: nilAI ran Llama 3B/8B/70B and DeepSeek in TEEs (nilCC), plus nada-AI for small MPC-style programmable inference and a Private RAG SDK. **Older material.** — [Binance Research: Nillion](https://www.binance.com/en/research/projects/nillion); [Nillion Phase 0, Jul 2025](https://nillion.com/news/phase-0-nillions-biggest-upgrade-is-now-live/)
- Chain: nilChain was sunset around March 23, 2026 and NIL moved from Cosmos to an Ethereum ERC-20. Blacklight, a decentralized verification network, launched in February 2026. Native smart contracts on Nillion's Ethereum L2 are slated for later in 2026. — [CoinMarketCap CMC-AI updates](https://coinmarketcap.com/cmc-ai/nillion/latest-updates/); [MEXC guide](https://blog.mexc.com/nillion-nil-guide-2026-what-is-the-blind-computer-how-to-buy-nil-on-mexc-and-how-to-earn-staking-rewards/)
- Funding: $52.7M raised across three rounds. — [Binance Research](https://www.binance.com/en/research/projects/nillion)

#### Atoma Network (Sui ecosystem; Lisbon)
- The alpha went live on Sui mainnet on Dec 12, 2024. Inference runs off-chain and settles on-chain, with TEEs for privacy. It previewed "Utopia", a private chat app. — [Decrypt](https://decrypt.co/296210/atoma-launches-private-decentralized-ai-on-sui?amp=1); [Sui blog](https://blog.sui.io/atoma-ai-artificial-intelligence-blockchain/)
- The GitHub repo `atoma-node` is described as "Core infrastructure for confidential computing AI inference". Atoma joined NVIDIA Inception in May 2025, partnered with Linera, and has an ERC-20 "ATOMA" token contract on Etherscan. — [GitHub](https://github.com/AtomaAI/atoma-node); [Crunchbase](https://www.crunchbase.com/organization/atoma-network); [Linera](https://linera.io/news/linera-x-atoma); [Etherscan](https://etherscan.io/token/0xc601f3c40a8de1f872ae056e7e21e255e740741a)

#### Ritual (founders Niraj Pant and Akilesh Potti, ex-Polychain)
- Raised $25M in November 2023 (**old**). — [Fortune](https://www.fortune.com/crypto/2023/11/08/two-former-polychain-partners-fundraise-25-million-ritual-decentralize-ai/)
- Infernet is live as an oracle-style network that lets EVM chains call off-chain models. Ritual Chain testnet launched November 2024 and a private testnet December 2024. — [The Block](https://www.theblock.co/post/327108/decentralized-ai-project-ritual-launches-testnet-to-bring-ai-onchain)
- Mainnet was targeted for 2025 and missed. There was no firm date as of February 2026. Privacy features are TEE enclaves plus ECIES-encrypted communication. — [DeSpread research](https://research.despread.io/ai-infra-projects/); [Ritual docs](https://docs.ritualfoundation.org/)

#### Fortytwo
- "Swarm inference": a network of small models on personal computers that generate and peer-rank each other's answers, with on-chain auditability and proof-of-capability Sybil resistance. It is not a confidentiality product. — [The Register, Nov 2 2025](https://theregister.com/2025/11/02/fortytwo_dcentralized_ai); [Decrypt, Oct 31 2025](https://decrypt.co/346986)
- Fortytwo claims to beat GPT-5, Gemini 2.5 Pro and Claude Opus 4.1 on GPQA Diamond, MATH-500, AIME 2024 and LiveCodeBench. **This is a self-reported benchmark.** — [Decrypt](https://decrypt.co/346986)
- Raised a $2.3M pre-seed in March 2025, led by Big Brain Holdings. — [Decrypt](https://decrypt.co/308928/fortytwo-secures-2-3m-in-pre-seed-funding-led-by-big-brain-holdings)

#### Gensyn
- Gensyn is a decentralized training network (Verde probabilistic proof-of-learning, RepOps). It is not a private-inference product. — [Gensyn litepaper](https://docs.gensyn.ai/litepaper)
- Its Delphi app launched on mainnet April 22, 2026. The token listed on five exchanges and fell about 45% within hours. — [CoinGabbar](https://www.coingabbar.com/en/price-prediction/gensyn-ai-listed-45percent-crashed-in-hours)

#### Bittensor: Chutes (SN64) and Targon (SN4), significant additions
- Chutes uses Intel TDX with NVIDIA confidential computing, measured boot, a LUKS-encrypted root filesystem that unlocks only after attestation, and cosign-signed images only. Optional E2EE encrypts prompts on the client and decrypts them only inside a verified TEE. E2EE is not the default. OpenAI-compatible API at `llm.chutes.ai/v1`. — [Chutes, May 7 2026](https://chutes.ai/news/private-ai-inference-verifiable-confidential-llm-serving)
- Chutes reportedly completed a full move onto TEEs in June 2026 and brought its first B200s online. This comes from a search snippet. — [A Bittensor Journey, Jun 2026](https://www.abittensorjourney.com/p/navigating-bittensor-june-2026)
- Targon (Manifold Labs, Austin, founded 2023; backers OSS Capital and DCG) runs OpenAI-compatible endpoints in Intel TDX + NVIDIA Hopper/Blackwell TEEs with continuous remote attestation. — [iq.wiki: Targon](https://iq.wiki/en/wiki/targon); [OpenTAO SN4](https://opentao.ai/beginner/subnets/4-targon/)

#### SayGm (TEE gateway, not a token network)
- SayGm is "an AI gateway that reaches dozens of frontier and open-weight models through a single API key". The gateway itself runs inside an Intel TDX enclave, and payment is prepaid credits. — [NEAR AI blog: SayGm, Sep 18 2026](https://near.ai/blog/nearai-cloud-on-saygm-verifiable-confidential-inference)
- Phala also lists SayGM as a customer. — [Phala x Venice post](https://phala.com/posts/venice-ai-phala-tee-verifiable-private-ai)

### Inferences
- The hardware layer has become a commodity: NEAR AI, Phala, Chutes, Targon, Nillion and Secret all run Intel TDX + NVIDIA CC. Their differences are in attestation UX, gateway design and token mechanics, not cryptography.
- "Decentralized" mostly means a decentralized settlement or registry layer (on-chain attestation in Secret's WorkerManager, Phala's DstackApp.sol). Inference itself is usually served by a small number of operators or the company's own fleet. NEAR AI is effectively a single-operator confidential cloud.
- Nillion's MPC/FHE story does not reach LLM serving. Anyone comparing "blind computation" with TEEs should know nilAI is TEE-based.

### Gaps
- Secret AI's current model list and per-token or subscription pricing: docs pages fetched did not list them.
- Nillion's founders and current team; Secret Labs' team and funding; Phala's total funding (sources are 2020-era and conflicting).
- Atoma: no 2026 activity, funding amount or usage found. CoinGecko search returns no "atoma" listing. Its status (active, dormant or pivoted) is unverified.
- Ritual: no 2026 mainnet confirmation found. CoinGecko returned no "ritual" token.
- Did not research Oasis (ROFL), iExec, Super Protocol, Lit, OpenGradient, Nesa or Akash/io.net TEE offerings. CoinGecko market caps on 2026-10-07: Oasis (ROSE) about $62.2M and iExec (RLC) about $64.4M. These are context only.

---

## 2. Which serve closed frontier models, and how (proxy vs hosted open weights)?

### Takeaway
None of these networks hosts closed frontier weights (GPT-5.x, Claude, Gemini) inside a TEE. Where closed models appear (SayGm's "Frontier tier", RedPill, Phala's catalog, Venice "Anonymous" mode), they are proxied to the lab's API. The gateway may run in a TEE, but the prompt arrives at OpenAI/Anthropic/Google in plaintext and that provider's data policy applies. The verifiable-privacy guarantee covers open-weight models only.

### Cited Findings
- SayGm's "Frontier tier" includes "closed-weight models like Claude or GPT", routed to upstream providers, and "that provider's policy governs your data". NEAR AI's confidential models on SayGm are all open-weight. — [NEAR AI blog: SayGm](https://near.ai/blog/nearai-cloud-on-saygm-verifiable-confidential-inference)
- NEAR AI's OpenRouter route serves only GLM 5.3 Flash and is **not confidential**: "Requests arriving through a router pass through infrastructure outside our confidential environment", and the gateway in front "is not attested". Only the direct API is confidential. — [NEAR AI blog: OpenRouter](https://near.ai/blog/near-ai-cloud-on-openrouter)
- Brave Leo's NEAR AI TEE deployment (Nov 20, 2025) covered only DeepSeek V3.1, only in Brave Nightly. The post does not say Leo's closed models are TEE-protected. — [Brave blog](https://brave.com/blog/browser-ai-tee/)
- Phala's model catalog page lists "Claude Sonnet 4.5" and "Gemini 2.5 Pro" next to open models but does not explain how they are served. Phala's confidential model list on its inference page (Qwen 3.8 27B, Nemotron 3.5 Lightning, GLM 5.3, Llama 3.1, DeepSeek V4 Flash, Muse Glimmer 30B, Gemma 4 31B) contains only open-weight models. — [Phala Confidential AI Models](https://phala.com/confidential-ai-models); [Phala private AI inference](https://phala.com/solutions/private-ai-inference)
- RedPill offers GPT, Claude and Gemini "protected by a TEE proxy". The proxy is in a TEE; the upstream lab is not. — [Phala case study: RedPill](https://cloud.phala.network/cases/redpill)
- Venice offers Claude, GPT-5, Gemini and Grok in "Anonymous" mode, where identity is stripped but the provider sees prompts. TEE/E2EE covers only 12 Venice-hosted open models out of 230+ (as of July 2026, per an aggregator). — [OwnYourMind (aggregator)](https://ownyourmind.ai/projects/venice/)
- Venice docs describe Anonymous mode as "Identity obscured from provider" and say TEE/E2EE are "currently available on text models only". E2EE turns off web search, memory, summaries and some tool flows. — [Venice docs: privacy](https://docs.venice.ai/overview/privacy.md)
- Nillion (Gemma 4, Qwen 3.6), Chutes and Targon (open-weight catalogs) list no closed models in a TEE. — [Nillion docs](https://docs.nillion.com/blind-computer/build/llms/overview); [Chutes](https://chutes.ai/news/private-ai-inference-verifiable-confidential-llm-serving)

### Inferences
- For closed frontier models, these networks offer exactly what a privacy pool in front of GPT/Claude/Gemini offers: identity stripping and a TEE-attested relay. The pool is no weaker here. A TEE-hosted relay does add a verifiable no-logging claim at the relay hop, which a plain proxy cannot prove.
- Real confidentiality from the model operator requires the operator to host the weights in a TEE. For closed models only the labs or their cloud partners could do that, and none of these networks has such a deal.

### Gaps
- Whether OpenAI, Anthropic or Google offer confidential-GPU hosting of their own models through Azure, GCP or AWS that a crypto network could resell was not researched here.
- Exactly how Phala serves "Claude Sonnet 4.5" and "Gemini 2.5 Pro" (pass-through proxy versus another arrangement) is undocumented on the pages fetched.

---

## 3. What privacy is actually provided for user identity, payment, and network metadata?

### Takeaway
TEEs protect prompt and response content from the hardware operator. They do nothing by default for identity, payment or network metadata. Accounts, API keys, card payments (Nillion via Stripe), public-wallet staking (NEAR) and IP addresses still connect usage to a person. Only Secret Network (encrypted contract state) and NEAR's "Confidential Intents" USDC payments try to hide the payment trail, and neither publishes metrics. None of the profiles documents IP-level anonymization (Tor, mixnet, OHTTP).

### Cited Findings
- Venice says it "does not store or log prompt and response content for normal inference". It does process "account identifiers, API key identifiers, timestamps, model selection, token counts, and IP addresses" for authentication, billing, abuse prevention and analytics. — [Venice docs: privacy](https://docs.venice.ai/overview/privacy.md)
- Venice's architecture uses a centralized proxy that strips identity before routing prompts to GPUs. Its "Private" mode relies on an unaudited no-storage claim; only the TEE and E2EE modes can be verified through hardware attestation. — [OwnYourMind (aggregator)](https://ownyourmind.ai/projects/venice/)
- The Block: Venice "encrypts user requests before routing them through an external proxy". — [The Block, Jul 1 2026](https://theblock.co/post/406934/venice-ai-funding-equity-valuation-dragonfly)
- NEAR AI staking: staked NEAR ÷ 100 = monthly dollar credit budget (500 NEAR gives $5/month). The principal stays put and the yield pays for inference. The minimum to activate an IronClaw agent is 50 NEAR. — [CryptoBriefing](https://cryptobriefing.com/near-ai-staking-confidential-inference/); [KuCoin blog](https://www.kucoin.com/blog/near-stake-to-compute-ai-payments)
- NEAR AI announced "private USDC payments" using Confidential Intents for agent transactions on May 14, 2026. — [NEAR AI blog index](https://near.ai/blog)
- Secret AI says it protects "conversation contents and usage metadata". User payments, model access and worker earnings are recorded in Secret Network smart contracts (SNIP-20 tokens) that external parties cannot read. — [Secret docs: Secret AI intro](https://docs.scrt.network/secret-network-documentation/secret-ai/introduction)
- Nillion nilAI takes Stripe payments as the entry point (NIL is consumed behind the scenes). nilDB and nilCC credits are bought with NIL in a developer portal that manages API keys. — [Nillion Phase 2, Apr 16 2026](https://nillion.com/news/nillions-phase-2-upgrade-is-live-introducing-a-unified-developer-portal/)
- Brave's Stage 1 TEE verification happens on Brave's servers, shown as a "verified green label". Client-side verification is on the roadmap. Users therefore trust Brave's check. — [Brave blog](https://brave.com/blog/browser-ai-tee/)
- Phala's docs warn that observability integrations may store prompts and metadata. — [Phala docs](https://docs.phala.com/phala-cloud/confidential-ai/confidential-model/migration-and-integrations)
- NEAR AI publishes a post titled "Assume We're Lying: How to Verify Private Inference" (Oct 2, 2026), which shows the trust model leans on attestation. — [NEAR AI blog index](https://near.ai/blog)
- Academic caution: a 2026 arXiv paper shows vulnerabilities in partial-TEE-shielded LLM inference schemes. — [arXiv 2602.11088](https://arxiv.org/pdf/2602.11088)

### Inferences
- Staking NEAR from a public account to pay for "private" inference leaves a permanent on-chain link between a wallet and an AI-usage account. Unless the wallet is fresh and unlinked, that is weaker identity privacy than a pooled, prepaid account.
- Card payments (Nillion/Stripe; Venice Pro subscriptions likely, unverified) identify the user to the vendor and the payment processor. Attestation only shows that the operator cannot read prompt content.
- A pool that aggregates many users behind shared upstream accounts gives k-anonymity toward the model provider. These networks don't offer that for open models, because the provider is the operator and already sees per-user API keys and IPs. That is a real gap in their privacy story.

### Gaps
- Phala's payment methods for Confidential AI (crypto, card, PHA) were not documented on the pages fetched.
- No network here publishes data on IP or network-metadata handling, such as whether gateways log client IPs or support Tor/OHTTP.
- Secret AI's payment privacy claims have no independent audit that I found.

---

## 4. Actual usage and revenue vs. market cap / fundraising

### Takeaway
Usage reporting is almost entirely self-reported and uneven. The only large published volumes are Venice (about 60B tokens/day per an aggregator, $65M Series A at a $1B valuation), Phala (a live counter of about 34B confidential tokens/day) and Chutes (about 120B tokens/day, most of it not confidential). NEAR AI publishes no usage at all. Its staking uptake (500k NEAR) works out to only about $5k/month of credits. Nillion's cumulative 1.4M inference calls are tiny next to its ~$47M market cap. SCRT's market cap has collapsed to about $5.9M.

### Cited Findings

Token market data (CoinGecko API, 2026-10-07 13:15 UTC):
- NEAR: $5.05, market cap about $6.61B. This is an L1 token whose value is not tied to AI usage. — [CoinGecko API](https://api.coingecko.com/api/v3/simple/price?ids=near&vs_currencies=usd&include_market_cap=true)
- VVV (Venice): $26.46, market cap about $1.28B. An aggregator puts FDV around $2.14B. — [CoinGecko API](https://api.coingecko.com/api/v3/simple/price?ids=venice-token&vs_currencies=usd&include_market_cap=true); [OwnYourMind](https://ownyourmind.ai/projects/venice/)
- PHA: $0.0629, market cap about $54.0M, FDV about $63.0M, down 38% over one year. — [CoinGecko API](https://api.coingecko.com/api/v3/coins/pha)
- NIL: $0.0926, market cap about $47.0M, FDV about $93.6M, all-time high $0.897 (about 90% below ATH). — [CoinGecko API](https://api.coingecko.com/api/v3/coins/nillion)
- SCRT: $0.00857, market cap about $5.86M, **down 96% over one year**, all-time high $10.38. This is extreme and worth re-checking against another data source. — [CoinGecko API](https://api.coingecko.com/api/v3/coins/secret)
- TAO: market cap about $3.29B. Chutes alpha token about $125.9M; Targon (SN4) about $88.7M. These are subnet alpha tokens; IDs are as listed on CoinGecko. — [CoinGecko API](https://api.coingecko.com/api/v3/simple/price?ids=bittensor,chutes,targon&vs_currencies=usd&include_market_cap=true)
- Gensyn: market cap about $26.4M. — [CoinGecko API](https://api.coingecko.com/api/v3/simple/price?ids=gensyn&vs_currencies=usd&include_market_cap=true)

Usage and revenue (self-reported unless noted):
- **Phala:** "33.7B daily tokens" from confidential models (timestamp 2026-10-06), 5,000+ users, 10 active models, 99.9% uptime SLA. A search snippet the same week showed 34.1B, so it is a live counter. The homepage case-study numbers ("300% increase in enterprise sales" etc.) are marketing. — [phala.com](https://phala.com/)
- **Phala/OpenRouter:** "18B+ tokens" processed through the OpenRouter enterprise confidential route. — [Phala private AI inference](https://phala.com/solutions/private-ai-inference)
- **NEAR AI:** none of the posts I reviewed discloses requests, tokens, users or revenue (OpenRouter, SayGm, staking, Private Chat launch). — [NEAR AI blog: OpenRouter](https://near.ai/blog/near-ai-cloud-on-openrouter); [CryptoBriefing staking](https://cryptobriefing.com/near-ai-staking-confidential-inference/)
- **NEAR AI staking:** more than 500,000 NEAR staked within about two weeks of the Jul 30, 2026 launch. — [CryptoBriefing](https://cryptobriefing.com/near-ai-staking-confidential-inference/)
- **Nillion:** as of Apr 16, 2026, 112,000+ users, 641M+ documents stored and **1.4M inferences** executed, all cumulative. — [Nillion Phase 2](https://nillion.com/news/nillions-phase-2-upgrade-is-live-introducing-a-unified-developer-portal/)
- **Venice:** about 3.0M total signups by mid-May 2026 and **about 60B+ daily LLM tokens** by May 2026 (about 20B in early February). These are aggregator figures, not audited. — [OwnYourMind](https://ownyourmind.ai/projects/venice/)
- **Venice revenue:** undisclosed. A third-party estimate puts ARR around $60M (attributed to Delphi, May 2026, via an aggregator) and is unverified. Buyback spend rose from about $65K/month (Dec 2025) to about $413K/month (Sep 2026). — [OwnYourMind](https://ownyourmind.ai/projects/venice/)
- **Venice funding:** $65M Series A at a $1B equity valuation (announced about Jul 1, 2026), led by Dragonfly with North Island, Coinbase Ventures, F-Prime, Archetype, Liquid2, Morgan Creek and others. It was Venice's first outside capital. Investors received 8.98% equity, a 1.5M VVV vesting grant and warrants for 5M VVV over eight years. — [The Block](https://theblock.co/post/406934/venice-ai-funding-equity-valuation-dragonfly)
- **Venice tokenomics:** 100M genesis VVV (no presale or VC allocation); about 33.89M burned by October 2026; emissions cut from 14M to 2M per year. DIEM gives $1/day of perpetual API credit, about 36.6k DIEM outstanding. — [OwnYourMind](https://ownyourmind.ai/projects/venice/)
- **Chutes:** $5.5M annualized revenue, of which 75% organic and 25% "sponsored" (subsidized). About 120B tokens/day after monetization (peaks of 160B), 34T+ lifetime, 696k+ users, top provider on OpenRouter. **The article is undated and probably from 2025.** — [TAO Media](https://www.tao.media/the-investors-guide-to-chutes-bittensors-inference-layer/). A search-engine summary separately claimed "$43M in Q1 2026 real AI revenue" for Chutes. I could not trace it to a primary source and it conflicts with the $5.5M figure. — [Top Bittensor subnets 2026](https://ourcryptotalk.com/blog/top-bittensor-subnets-2026) (unverified attribution)
- **Targon:** described as the "highest-revenue subnet for enterprise hardware-enforced AI workloads". No figure was found. — [OpenTAO SN4](https://opentao.ai/beginner/subnets/4-targon/)
- **Fortytwo:** "hundreds of nodes" (Nov 2025). — [The Register](https://theregister.com/2025/11/02/fortytwo_dcentralized_ai)
- **Atoma, Ritual, Secret AI:** no usage numbers found.

### Inferences
- NEAR AI's 500k staked NEAR is about $2.5M of locked principal at $5.05. Under the published 100:1 rule it generates only about **$5,000/month** of inference credits, which is a rounding error against a $6.6B token. The NEAR market cap reflects the L1, not NEAR AI.
- Nillion: 1.4M cumulative inferences against a ~$47M market cap ($52.7M raised) gives a market-cap-to-usage ratio far above Phala's, whose claimed volume is about 34B tokens per *day* against a ~$54M market cap. Taken at face value, Phala has the clearest usage-to-valuation case among the pure-token infrastructure plays.
- Venice is the only one where a cash business has demonstrably converted into equity at a high valuation (Dragonfly-led, $1B). Much of its privacy comes from proxying plus partner TEEs (NEAR AI, Phala), so its volume is partly Phala's and NEAR's volume. Adding Venice tokens to Phala tokens may double-count.
- Secret's roughly 96% one-year collapse to a $5.9M market cap, set against a "ready for prime time" Secret AI/SecretVM suite, suggests the market sees no traction.

### Gaps
- No network publishes audited revenue. Phala's token counter cannot be checked independently from the sources I reviewed (no on-chain receipts dashboard found).
- NEAR AI Cloud's real volume (requests, tokens, paying customers) is unknown.
- I could not reconcile Chutes' revenue claims ($5.5M ARR vs. $43M Q1 2026).
- Venice ARR is an estimate from an aggregator citing Delphi; I could not access the underlying report.

---

## 5. Partnerships with frontier labs, enterprises, and AI gateways

### Takeaway
I found **no partnership with a frontier lab** (OpenAI, Anthropic, Google DeepMind) anywhere in this set. Real distribution comes through AI gateways (OpenRouter for both Phala and NEAR AI; SayGm; RedPill), consumer apps (Venice, Brave Nightly), chip vendors (Intel Trust Authority, NVIDIA Inception) and one Chinese lab (Z.AI/Zhipu, listed by Phala). Enterprise and government deals are mostly pilots or small (Bermuda, Abound, Corbits, OODA AI).

### Cited Findings
- **OpenRouter–Phala:** Phala says "OpenRouter's enterprise tier receives confidential routing through Phala at price parity with standard routes". It lists OpenRouter, NEAR AI and OODA AI (NASDAQ-listed) as production deployments. **Self-reported; I found no OpenRouter-side confirmation.** — [Phala private AI inference](https://phala.com/solutions/private-ai-inference)
- **OpenRouter–NEAR AI:** NEAR AI became an OpenRouter provider on Sep 28, 2026 (provider slug `near-ai`, no markup). The route is not confidential end-to-end. — [NEAR AI blog](https://near.ai/blog/near-ai-cloud-on-openrouter)
- **Phala's partner logos:** NVIDIA, OpenRouter, Z.AI (Zhipu), Linux Foundation, Venice AI, Intel, NEAR Protocol, Uniswap, Flashbots, Crossmint. A logo wall is not proof of a commercial relationship. — [phala.com](https://phala.com/)
- **Venice–Phala and Venice–NEAR AI:** both announced Mar 19, 2026 to deliver Venice's TEE/E2EE modes. — [Phala x Venice](https://phala.com/posts/venice-ai-phala-tee-verifiable-private-ai); [NEAR AI blog index](https://near.ai/blog)
- **Phala's other named customers:** SayGM and OPPO. — [Phala x Venice](https://phala.com/posts/venice-ai-phala-tee-verifiable-private-ai)
- **Brave–NEAR AI:** Leo TEE inference (DeepSeek V3.1, Nightly only, Nov 2025). — [Brave blog](https://brave.com/blog/browser-ai-tee/)
- **NEAR AI enterprise and government:** Government of Bermuda (May 13, 2026), Abound / Times of India Group (Apr 2, 2026), Corbits (Jul 15, 2026), OpenMind (Dec 2025), Intel Trust Authority (Aug 12, 2026). — [NEAR AI blog index](https://near.ai/blog); [NEAR AI launch post](https://near.ai/blog/introducing-near-ai-cloud-private-chat)
- **Secret Network:** AITECH Agent Forge (Aug 2026) and Morpheus (Aug 7, 2026), both crypto-native partners. — [Yahoo Finance](https://finance.yahoo.com/technology/ai/articles/aitech-cloud-network-secret-network-181100795.html)
- **Atoma:** NVIDIA Inception (May 2025) and Linera. — [Crunchbase](https://www.crunchbase.com/organization/atoma-network); [Linera](https://linera.io/news/linera-x-atoma)
- **Fortytwo:** Acurast, to explore swarm inference on edge devices. — [Acurast](https://acurast.com/blog/announcements/acurast-and-fortytwo-to-explore-swarm-inference-on-edge-devices/)

### Inferences
- The gateway channel (OpenRouter, SayGm, RedPill) is where confidential inference actually reaches developers. A Lethe-style pool would compete with, or could sit on top of, these gateways. SayGm, a TDX-enclave gateway with a frontier tier that proxies Claude and GPT, is the most direct existing analogue.
- The lack of any frontier-lab deal means none of these networks can offer verifiable confidentiality for Claude, GPT or Gemini. It also means frontier labs can still see who calls them, unless a pool aggregates the calls.

### Gaps
- Commercial terms and volumes for any of these partnerships were not disclosed.
- OODA AI and OPPO deployment scope and status are unknown.

---

## 6. Direction for 2026-2027

### Takeaway
The direction is consistent across projects. They are moving away from "decentralized chain" framing toward enterprise confidential cloud and agent infrastructure. Concretely that means getting into gateways and IDEs, moving tokens to Ethereum (Phala, Nillion), running on hyperscaler TEEs (Secret), and binding token staking to compute credits (NEAR, Venice DIEM, Nillion). Agents with private payments are the shared next story.

### Cited Findings
- **NEAR AI:** staking-to-compute (Jul 30, 2026); IronClaw always-on agents; Confidential Intents private USDC for agent payments (May 2026); IDE distribution through the Copilot/VSCode extension (Oct 1, 2026); gateway distribution through OpenRouter and SayGm (Sep 2026). — [NEAR AI blog index](https://near.ai/blog); [CryptoBriefing Copilot](https://cryptobriefing.com/near-ai-private-inference-github-copilot/)
- **Brave/NEAR:** the stated next steps are to cut TEE performance overhead and add client-side attestation verification before a broader rollout. — [Brave blog](https://brave.com/blog/browser-ai-tee/)
- **Phala:** migrating to an Ethereum L2 to "ramp computation offerings to enterprise clients" (vote of Oct 2025). Product emphasis is on GPU TEE rental (H100 to B300) and an OpenAI-compatible confidential model API with verifiable receipts. — [FXStreet](https://www.fxstreet.com/cryptocurrencies/news/ai-polkadot-parachain-phala-votes-to-fully-switch-to-ethereum-l2-202510100604); [phala.com](https://phala.com/)
- **Nillion:** nilChain sunset in March 2026 and NIL moved to an ERC-20. An Ethereum L2 with native contracts for staking and direct access to nilAI/nilDB is slated for later in 2026. Blacklight verification layer. Credit-based billing. — [CMC-AI](https://coinmarketcap.com/cmc-ai/nillion/latest-updates/); [Nillion Phase 2](https://nillion.com/news/nillions-phase-2-upgrade-is-live-introducing-a-unified-developer-portal/)
- **Secret:** SecretVM to run on Azure, GCP and AWS confidential VMs in 2026. A Private RAG database is planned. — [Secret roadmap X post](https://x.com/SecretNetwork/status/2010859443257593969); [Secret docs: architecture](https://docs.scrt.network/secret-network-documentation/secret-ai/architecture)
- **Ritual:** mainnet still pending, with no firm date as of Feb 2026. — [DeSpread](https://research.despread.io/ai-infra-projects/)
- **Messari's 2026 theses** highlight decentralized compute for inference, mid-sized open-source models, and agent businesses with on-chain identity and payments. — [Messari 2026 summary (OneKey)](https://onekey.so/blog/ecosystem/messari-2026-research-trends-across-seven-crypto-sectors/); [Messari: Decentralized AI Coordination](https://messari.io/report/decentralized-ai-coordination-transforming-siloed-intelligence-into-collective-networks)

### Inferences
- Expect more convergence with mainstream confidential AI clouds (Azure and GCP confidential GPUs). The crypto layer would shrink to attestation registries, staking-for-credits and agent payments.
- The ongoing move onto hyperscaler TEEs (Secret) and the dependence on Intel and NVIDIA attestation (everyone) means trust ultimately rests on Intel and NVIDIA, not on decentralization.

### Gaps
- No public 2027 roadmaps were found for any of these networks.
- The CoinReporter October 2026 "year of shutdowns" round-up names no AI or privacy networks (Abstract, Blast, Lisk, Kadena and others instead). That is weak evidence the AI networks here are still operating, not proof of activity. — [CoinReporter](https://www.coinreporter.io/2026/10/the-year-of-shutdowns-which-networks-are-winding-down-in-2026/)

---

## 7. Honest assessment: real traction vs. token narrative, and what they do that a privacy pool in front of GPT/Claude/Gemini cannot

### Takeaway
**Real traction:** Venice (consumer scale, $1B equity round), Phala (largest claimed confidential-token volume, OpenRouter and Venice integrations, though self-reported), and Chutes (large but mostly non-confidential volume). **Credible product, unproven usage:** NEAR AI Cloud has strong distribution deals and real engineering but publishes no usage. **Mostly token narrative:** Nillion (tiny inference count against a ~$47M market cap), Secret (market cap collapsed), Atoma (no 2026 signal), Ritual (no mainnet), Fortytwo and Gensyn (not private-inference products). The one thing these networks can do that a pool in front of closed models cannot is attested confidentiality from the model operator, and it applies only to open-weight models. A pool can do something they cannot: hide user identity *from the frontier lab* by aggregating many users.

### Cited Findings
- Venice's $65M Series A at a $1B valuation is the strongest third-party validation in this set. — [The Block](https://theblock.co/post/406934/venice-ai-funding-equity-valuation-dragonfly)
- Venice's verifiable private modes run on partner TEEs (NEAR AI Cloud, Phala), while closed models use Anonymous mode, where the provider sees the prompt. — [OwnYourMind](https://ownyourmind.ai/projects/venice/); [Venice docs](https://docs.venice.ai/overview/privacy.md)
- Phala claims about 33.7B confidential tokens per day and an OpenRouter enterprise route, on a ~$54M market cap. — [phala.com](https://phala.com/); [Phala private AI inference](https://phala.com/solutions/private-ai-inference); [CoinGecko](https://api.coingecko.com/api/v3/coins/pha)
- NEAR AI publishes no usage data, and its OpenRouter route is explicitly non-confidential. — [NEAR AI blog: OpenRouter](https://near.ai/blog/near-ai-cloud-on-openrouter)
- Nillion has 1.4M cumulative inferences, $52.7M raised and a ~$47M market cap. — [Nillion Phase 2](https://nillion.com/news/nillions-phase-2-upgrade-is-live-introducing-a-unified-developer-portal/); [Binance Research](https://www.binance.com/en/research/projects/nillion); [CoinGecko](https://api.coingecko.com/api/v3/coins/nillion)
- SCRT is down 96% over one year to a ~$5.9M market cap. — [CoinGecko](https://api.coingecko.com/api/v3/coins/secret)
- On closed models, SayGm says the upstream "provider's policy governs your data". — [NEAR AI blog: SayGm](https://near.ai/blog/nearai-cloud-on-saygm-verifiable-confidential-inference)
- What TEEs uniquely provide is hardware-signed attestation that the operator cannot see prompts, weights or outputs, checked rather than taken on trust. — [NEAR AI blog: SayGm](https://near.ai/blog/nearai-cloud-on-saygm-verifiable-confidential-inference); [Chutes](https://chutes.ai/news/private-ai-inference-verifiable-confidential-llm-serving)
- TEEs "still require software validation and auditability around them" (Chutes' own caveat), and partial-TEE schemes have published attacks. — [Chutes](https://chutes.ai/news/private-ai-inference-verifiable-confidential-llm-serving); [arXiv 2602.11088](https://arxiv.org/pdf/2602.11088)

### Inferences

What these networks can do that a privacy pool in front of GPT/Claude/Gemini cannot:
1. **Content confidentiality from the inference operator, with proof.** For open-weight models in a TEE, nobody (operator, cloud host, the company) can read the prompt, and the client can verify that through remote attestation. A pool in front of closed APIs always hands plaintext to OpenAI, Anthropic or Google.
2. **Verifiable no-logging at the relay.** A TEE-hosted gateway (SayGm, Phala's dstack-gateway, RedPill) can attest that the relay runs code that doesn't log. A pool could adopt this itself by running its relay in a TDX enclave. It is a technique available to the pool, not something only crypto networks have.
3. **Model-weight confidentiality** for third-party model owners who deploy on someone else's GPUs. This doesn't matter to users of frontier closed models.
4. **Crypto-native payment rails** (staking-for-credits, DIEM, Confidential Intents USDC). These are useful for agents but, as shown above, usually weaken identity privacy unless paired with shielded payments.

What a pool can do that they mostly cannot:
- Hide which person or firm sent a query from the frontier lab by mixing many members behind shared upstream accounts. None of these networks does this for closed models beyond Venice's "Anonymous" identity stripping, which comes from a single centralized proxy and is the same idea as a pool.
- Give access to the best closed models. Every TEE network here serves open-weight models (DeepSeek V4, GLM 5.3, Kimi K3, Qwen 3.x, Gemma 4) for its verifiable tier.

Strategic implication for Lethe, offered as inference: the strongest position combines both. Run the pool's relay in an attested TEE, proxy closed frontier models with identity mixing, and offer a TEE open-weight tier (for example through Phala or NEAR AI Cloud as backends) for queries where content confidentiality matters more than frontier quality. SayGm already sells nearly this bundle minus the pooling and identity mixing, so it is the competitor to watch.

### Gaps
- None of the traction metrics is independently audited. The ranking above depends on self-reported figures (Phala's counter, Venice via aggregator, Chutes via TAO Media).
- I found no evidence on whether enterprise buyers (law firms, finance) actually choose these networks over mainstream confidential clouds, or over a pool in front of closed models.
