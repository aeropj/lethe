I have comprehensive data across all eight areas. Writing the report now.

---

# Lethe: Competitive Sweep, September 2026

**Method note.** YC findings come from the complete YC company dataset (6,232 companies, last updated 2026-09-18) at [yc-oss.github.io/api](https://github.com/yc-oss/api), filtered and verified locally — not from search. GitHub star counts were pulled live via the API on 2026-09-18. Where a number is an estimate or a secondary source, it says so. The session's web-search quota was exhausted mid-sweep; gaps are flagged at the end.

---

## 1. Master table — companies not already on your list

| Name | Stage / batch | Funding | What they do | Overlap | Status |
|---|---|---|---|---|---|
| **[LogosGuard](https://logosguard.com/)** | YC Fall 2025 | YC only | On-device redaction layer for ChatGPT/Claude/Gemini | **HIGH** — same consumer wedge, but **one-way redaction, not reversible** | Active, 2 people |
| **[Quilr](https://www.quilr.ai/)** | Seed, undisclosed | n/d | LLM gateway: inline PII redaction **+ per-agent scopes enforced at runtime** | **HIGHEST** — only company doing both halves of Lethe | Active; claims Vodafone, UiPath |
| **[Confident Security](https://confident.security/)** | Seed Jul 2025 | $4M (Maverick, Decibel) | CONFSEC: E2E encryption + **anonymized routing** + TEE attestation | **HIGH** — closest funded analogue to unlinkability | Active |
| **[1Privacy.ai](https://1privacy.ai/)** | Bootstrapped | none | Relay to 350+ models; strips ID/IP/session, rotates keys | **HIGH** — identical consumer pitch, operator-trust mechanism | Live, $25–100/mo |
| **[nullsink](https://nullsink.is/)** | Solo, anonymous | none | Account-less, crypto-paid proxy to 48 frontier models; no logs | **HIGH** — your consumer thesis, already shipping | Live; GitHub repo archived, moved to GitLab |
| **[Egoist Machines](https://ego.ist/)** | YC Summer 2026 | YC only | "AI Passport": portable personal context, **per-app scopes + audit receipts + revocation** | **HIGH** — your ledger/scopes model, inverted to personalization | Live, free for individuals |
| **[Skyflow](https://www.skyflow.com/)** | Series B+ | $100M total; last round Mar 2024 | Repositioned 2026 as "Runtime AI Data Control"; ships an **LLM Gateway that de-identifies and re-identifies** | **HIGHEST** — your exact mechanism, already funded | Active; secondary mark ~$295M ([Forge](https://forgeglobal.com/skyflow_stock/)) — flag as secondary-market, not a primary round |
| **[Multifactor](https://multifactor.com)** | YC Fall 2025 | YC only | Zero-trust authn/authz/audit for AI agents | HIGH (agent half) | Active, 6 people |
| **[Alter](https://alterauth.com)** | YC Summer 2025 | YC only | Parameter-level authz + ephemeral scoped credentials per tool call | HIGH (agent half) | Active |
| **[Clawvisor](https://clawvisor.com)** | YC Spring 2026 | YC only | "The Authorization Layer for AI Agents" | MED-HIGH | Active, 1 person |
| **[Inkbox](https://inkbox.ai)** | YC Summer 2026 | YC only | "Identity and communication layer for AI agents" | MED-HIGH | Active |
| **[Capacitive](https://capacitive.ai/)** | YC Spring 2025 | YC only | "The data gateway for agents" | MED-HIGH | Active |
| **[Unbound](https://getunbound.ai/)** | YC Summer 2024 | YC only | "Use AI tools without fear of data leakage" | MED-HIGH | Active, 7 people |
| **[Codag](https://codag.ai/)** | YC Summer 2026 | YC only | "AI gateway for cheaper, faster, permissioned agents" | MED | Active, 1 person |
| **[Omnifact](https://omnifact.ai)** | Germany, undisclosed | n/d | Enterprise multi-model platform, "Privacy Filter™" pseudonymization | MED-HIGH | Live; real logos (Aareal Bank, municipalities) |
| **[PrivacyScrubber](https://privacyscrubber.com/)** | Small, undisclosed | n/d | Reversible deterministic tokens, local map, Chrome ext + **PII MCP server** | HIGH on mechanism | Live; ⚠ unverified SOC2/patent claims |
| **[CamoCopy](https://www.camocopy.com/)** | EU, bootstrapped | n/d | Privacy ChatGPT alternative w/ in-browser anonymization, €14.90/mo | MED-HIGH | ⚠ Stale — still advertising Claude 3.5 in Sept 2026 |
| **[cymphony.io](https://cymphony.io/)** | Series A Sep 2026 | $25–30M (Sequoia, Fin) | Workforce security graph: identity + data + AI usage | MED | Active |
| **[Consus](https://www.consus.io)** | YC Fall 2024 | YC only | Cheapest way to use AI with ITAR/CUI data | MED | Active, 1 person |
| **[Tonic.ai](https://www.tonic.ai/)** | ~$35M (stale) | — | Commercial de-identification with a genuine `unredact()` | MED-HIGH | Most commercially serious reversible player |
| **[Opaque](https://opaque.co)** | $24M Feb 2026 @ ~$300M post | $55.5M | Confidential computing for enterprise AI | MED-LOW | Active |
| **[Evervault](https://evervault.com)** | $25M Mar 2026 | — | Encryption infra moving into AI | MED-LOW | Active (did **not** die) |
| **[VGS](https://www.verygoodsecurity.com/)** | Established | — | 5B tokens stored; pivoting into **agentic commerce** | MED | Healthy — not a failure |

Also live but lower-overlap: [Golf](https://golf.dev/), [Galini](https://www.galini.ai/), [truthsystems](https://www.truthsystems.ai), [Salus](https://www.usesalus.ai/), [Candor](https://candor.security/), [Inth](https://inth.com), [Tolmo](https://www.tolmo.com), [Harmonic](https://www.harmonic.security/), [Pomerium](https://www.pomerium.com/secure-agentic-access), [AIR Security](https://www.air.security/) ($50M A, Sequoia+Greenoaks, Sep 2026), [Mind](https://www.returnonsecurity.com/p/security-funded-260) ($72M B, Sep 2026).

---

## 2. Y Combinator: who is in, who died, what it implies

**The category is at an all-time high inside YC.** Filtering all 6,232 companies for AI-security/privacy/agent-governance language by batch:

| Batch | Companies in category | Batch size | % |
|---|---|---|---|
| W24 | 7 | 248 | 2.8% |
| S24 | 6 | 248 | 2.4% |
| F24 | 2 | 94 | 2.1% |
| W25 | 2 | 165 | 1.2% |
| X25 (Spring) | 7 | 143 | 4.9% |
| S25 | 8 | 166 | 4.8% |
| F25 | 6 | 146 | 4.1% |
| W26 | 8 | 199 | 4.0% |
| Spring 26 | 9 | 193 | 4.7% |
| **S26** | **15** | **232** | **6.5%** |

W25 was the trough (1.2%); S26 is the peak (6.5%) and the highest of any batch since W22. **YC is funding this category at an accelerating rate, and funded at least one company per recent batch that overlaps Lethe.**

**The four that matter most to your application:**

- **[LogosGuard](https://www.ycombinator.com/companies/logosguard)** (F25, 2 people) — "The sensitive data redaction layer for AI… redacts your private information before the prompt ever leaves your device." This is your consumer pitch, verbatim, already funded. **But it is one-way redaction, not reversible tokenization** — verified on their site. Your reversibility, cross-session bijection and per-provider surrogates are still genuinely differentiated. Do not pretend LogosGuard doesn't exist; name it and draw the line.
- **[Egoist Machines](https://www.ycombinator.com/companies/egoist-machines)** (S26) — per-app data scopes, audit receipts, revocation. Same primitives as your agent gateway and ledger, aimed at personalization rather than non-profiling. Free for individuals, which sets a price anchor you will have to fight.
- **[Tinfoil](https://www.ycombinator.com/companies/tinfoil)** (X25) — the only company in this space to get real developer traction: [146 points, 100 comments on HN](https://news.ycombinator.com/). $20/mo consumer, $2/1M tokens API. Positions explicitly *against* redaction.
- **[Multifactor](https://www.ycombinator.com/companies/multifactor)** (F25) and **[Alter](https://www.ycombinator.com/companies/alter)** (S25) — agent authz with ephemeral scoped credentials. Your agent-gateway half, twice.

**The YC graveyard in this space — the most valuable signal:**

| Company | Batch | Status | What it was |
|---|---|---|---|
| **[Blyss](https://www.ycombinator.com/companies/blyss)** | W23 | **Inactive** | "End-to-end encrypted AI." GPU secure enclaves. Explicitly: "make E2E encrypted AI a no-compromise option — just like Signal did for messaging." Team from Stanford/Apple/NVIDIA. **Died.** Tinfoil then raised on the same thesis two years later. |
| **[Sarus](https://www.ycombinator.com/companies/sarus)** | W22 | Acquired | Differential privacy for personal data in ML |
| **[Neosync](https://www.ycombinator.com/companies/neosync)** | S22 | Acquired | Open-source anonymization + synthetic data |
| **[JumpWire](https://www.ycombinator.com/companies/jumpwire)** | W22 | Acquired | Dynamic access controls for PII in databases |
| **[Tesseral](https://www.ycombinator.com/companies/tesseral)** | W24 | **Inactive** | Open-source identity platform |
| **[Mendral](https://www.ycombinator.com/companies/mendral)** | W26 | **Inactive** | Dead within months of the batch |
| **[Preclusio](https://www.ycombinator.com/companies/preclusio)** | S19 | Inactive | GDPR compliance automation |
| **[Chutney](https://www.ycombinator.com/companies/chutney-inc)** | W20 | Inactive | Pseudonymous social network |
| **[Zumo Labs](https://www.ycombinator.com/companies/zumo-labs)**, **[SBX](https://www.ycombinator.com/companies/sbx-robotics)** | W20/W21 | Inactive | Synthetic data |
| **[CodeStory](https://www.ycombinator.com/companies/codestory)** | S23 | Inactive | Privacy-first IDE |

**What this implies for your application.** YC has funded this thesis repeatedly and has watched the *pure privacy* versions die (Blyss, Chutney, Preclusio, Tesseral) while the *enterprise control* versions get acquired (Sarus, Neosync, JumpWire). Three of four exits were acquisitions, none large. The partner reading your application will have pattern-matched Blyss before finishing paragraph two. **Pre-empt it:** say why 2026 is different from 2023 (agent fan-out, MCP, the CJEU *EDPS v SRB* ruling), and why reversible tokenization beats encrypted inference commercially — it works with closed frontier models, which TEE approaches structurally cannot.

---

## 3. The Datavant analogue: verdict

**False analogue.** The mechanism rhymes; the business does not.

**What the tokens are.** PII is SHA-256 hashed with a **Datavant master salt**, then encrypted **AES-128 with a site-specific key**; a `transform-tokens` step re-encrypts for a specific sender/receiver pair ([Regenstrief/N3C packet, PDF](https://www.regenstrief.org/wp-content/uploads/2022/04/siteengagementpacket-pre-nda-v06.pdf)). Legal standing is HIPAA Expert Determination §164.514(b)(1).

**The finding that should change your architecture pitch:** Datavant's software is *not* self-custodial. The CLI must reach `sec.datavant.com` to retrieve encryption keys, and Datavant's certification exists specifically to protect "customer secrets (master salt/seed and customer encryption keys)." **Datavant holds the root secret. That central chokepoint *is* the business.** Lethe's local key custody deliberately deletes the exact asset Datavant monetizes.

**Scale:** 1 trillion records/year, 80,000+ hospitals, 75 of the top 100 health systems ([datavant.com](https://www.datavant.com/)). Revenue ~$1.9B is an **estimate** ([Owler](https://www.owler.com/company/datavant)); the last disclosed figure was ">$700M" at the $7B Ciox merger in 2021. Neuberger and KKR took a minority stake on 2026-09-17 at an **undisclosed** valuation ([HIT Consultant](https://hitconsultant.net/2026/09/17/datavant-secures-minority-investment-neuberger-kkr-new-mountain-capital-health-data-collaboration/)). At ~7,400 estimated staff, that is ~$258K revenue/employee: **services economics, not software.** Most of it is Ciox record-retrieval labour — **even Datavant does not primarily monetize the token.**

**No per-token or per-dataset price is public anywhere.** HealthVerity, the #2, is ~$40M revenue (estimate, [Growjo](https://growjo.com/company/HealthVerity)) against Datavant's ~$1.9B. The network winner takes essentially everything.

**The killer number is LiveRamp.** FY2026 revenue **$813M**, 71% GAAP gross margin, $545M ARR, 107% NRR ([FY26 results](https://www.globenewswire.com/news-release/2026/05/17/3296257/0/en/LiveRamp-Announces-Fourth-Quarter-and-Fiscal-Year-2026-Results.html)). Publicis is acquiring it for **$2.546B equity / $2.167B EV** — **~2.7x EV/revenue** ([Publicis](https://www.publicisgroupe.com/en/news/press-releases/publicis-to-acquire-liveramp-to-accelerate-data-co-creation-for-smarter-agents)). The canonical "make data linkable" business, profitable with 107% NRR, cleared 2.7x. Unlinkability has no ROI numerator at all.

**Four tests it fails:** (1) Datavant's buyer is a pharma enterprise with a budget line; yours is a consumer. (2) Datavant is genuinely two-sided — sender *and* receiver want the join; for Lethe the provider is the adversary, not a counterparty. (3) HIPAA is a forcing function that makes de-identification *unlock* otherwise-illegal value; there is no AI equivalent. (4) Datavant is **must-link-to-be-useful**; Lethe is **must-not-link** — pure subtraction, fighting the memory and personalization users demonstrably like.

And note: Datavant's own AI strategy is the *opposite* of yours — "proprietary clinical data… **ground frontier LLMs**," with the KKR capital earmarked for "clinical AI model training." They are selling linked data *into* AI.

**Use "LiveRamp in reverse," not "Datavant for AI."** The one transferable lesson: Datavant won by being neutral infrastructure that doesn't commercialize the data itself, and it solved cold-start with **single-player internal value first** ([Travis May's playbook](https://travismay.medium.com/a-playbook-for-building-a-b2b-network-business-90964781a516)). Your equivalent question — what does Lethe do for one user when zero providers cooperate? — needs a crisp answer.

---

## 4. Consumer privacy monetisation: the real numbers

| Company | Price | Scale | Revenue | Quality |
|---|---|---|---|---|
| **1Password** | ~$36/yr | 180,000 business customers | **$400M ARR (Oct 2025)**, >75% business, >90% gross retention | HARD ([CNBC](https://www.cnbc.com/2025/11/06/ryan-reynolds-backed-1password-tops-400-million-in-arr.html)) |
| **Venice.ai** | Pro tiers | 3M users | **$70M+ ARR, profitable**; $65M A at **$1B** | HARD ([TechCrunch](https://techcrunch.com/2026/07/01/venice-ai-becomes-a-unicorn-with-65m-series-a-as-its-privacy-first-ai-platform-takes-off/)) |
| **Mozilla** | Relay ~$0.99/mo | ~200M users | 2024: royalties $498.2M; **subscription + advertising combined only $66.4M**, +2.5% YoY | HARD — [audited](https://stateof.mozilla.org/) |
| **Brave** | VPN $59–199/yr | **101M MAU** | **~100,000 VPN subscribers** | HARD ([Brave](https://brave.com/blog/100m-mau/)) |
| **Mullvad** | Flat €5/mo | — | **314.8 MSEK (~$30M) 2024, +36%, profitable** | Swedish filings |
| **Proton** | $9.99/mo | 100M+ accounts | **Publishes nothing.** Estimates conflict ($64M–$97M) | WEAK |
| **DeleteMe** | **$129/yr** | — | ~$21M (aggregator guess) | Pricing HARD, revenue GUESS |
| **DuckDuckGo** | $9.99/mo | 0.71% global search | ">$100M" — **no primary source found** | WEAK |
| **Tinfoil** | $20/mo | — | not disclosed | — |

**Two numbers demolish the "privacy audience converts" thesis.** Brave: **101M MAU → ~100,000 VPN subscribers = 0.1% conversion**, from the most privacy-selected consumer audience on earth. Mozilla: **$66.4M of subscription-plus-advertising across ~200M users, growing 2.5%/yr**, against $498M of search royalties — and they won't even break subscription out from ads, which tells you it's unflattering.

**Churn.** RevenueCat's [State of Subscription Apps 2025](https://www.revenuecat.com/state-of-subscription-apps-2025/): annual plans retain **44.1% at year one (~56% churn)**; monthly retain **17.0%**; high-priced monthly is *worse* at 12.2%; ~30% of annual subs cancel in month one. Median realized Year-1 LTV is **$23/payer globally, $32 in North America**. Model Lethe at 50–60% annual churn and sub-$40 Year-1 LTV unless you have a structural reason to beat it.

**What actually makes people pay:** a functional product where privacy is framing, not purchase (1Password, VPNs). Ideology works but caps small — Mullvad is ~$30M, profitable, deliberately unscaled. Fear/harm sustains price ($129/yr DeleteMe vs $19.90/yr NextDNS for the same invisible outcome) but has no disclosed scale.

**The one genuinely encouraging datapoint is Venice.ai: $70M+ ARR, profitable, ~2 years old, on an explicit no-logging privacy pitch.** That is more than Mullvad, Brave's subscriptions and Mozilla's entire subscription line combined. The read: **paid AI privacy rides the $20/mo AI-subscription anchor, not the $5/mo privacy anchor.** Price against ChatGPT Plus, not against Mullvad. Note Venice's VVV token partly makes ARR reflexive — discount, don't dismiss.

---

## 5. Funding and M&A, 2025–2026

**The pattern: buyers pay for a control point, not ARR — 4–12x *capital raised*, clustering ~10x.**

| Acquirer | Target | Date | Price | Target raised | Mult |
|---|---|---|---|---|---|
| Cisco | Robust Intelligence | Aug 2024 | ~$400M (rep.) | $44M | ~9x |
| NVIDIA | Gretel | Mar 2025 | >$320M (rep.) | $65.5M | ~5x |
| Palo Alto | Protect AI | Apr 2025 | $650–700M (rep.) | $108.5M | ~6x |
| Tenable | Apex Security | May 2025 | >$105M (rep.) | $8.6M | **~12x** |
| SentinelOne | Prompt Security | Aug 2025 | ~$250M (rep.) | $23M | **~11x** |
| Cato | Aim Security | Sep 2025 | $300–350M (rep.) | $28M | **~12x** |
| CrowdStrike | Pangea | Sep 2025 | ~$260M (rep.) | — | — |
| Check Point | Lakera | Sep 2025 | ~$300M (rep.) | ~$30M | ~10x |
| F5 | CalypsoAI | Sep 2025 | **$180M (disclosed)** | — | — |
| **Veeam** | **Securiti AI** | Oct 2025 | **$1.725B (disclosed)** | — | — |
| Zscaler | SPLX | Nov 2025 | **$40.6M cash (disclosed)** | $9M | ~4.5x |
| Varonis | AllTrue.ai | Feb 2026 | ~$180M (rep.) | — | — |
| OpenAI | Promptfoo | Mar 2026 | undisclosed | $23M | — |
| Akamai | LayerX | May 2026 | **$205M (disclosed)** | — | — |
| **Palo Alto** | **Portkey** | May 2026 | **$117M (disclosed)** | seed | — |
| Cisco | Astrix | May 2026 | ~$400M (rep.) | — | — |
| **Cyera** | **Oasis Security** | Jul 2026 | **~$1.0B (rep.)** | — | — |
| Palo Alto | Console | Aug 2026 | ~$500M (rep.) | — | — |
| **Harvey** | **Guardrails AI** | Sep 2026 | undisclosed | $7.5M | quiet landing |
| Kiteworks | Bonfy.AI | Sep 2026 | undisclosed | $9.5M | quiet landing |
| Surfshark | Optery | Sep 2026 | undisclosed | $2.7M | consumer consolidation |

Big rounds 2026: **Cyera $600M at $12B**; Cylake $245M; Onyx $113M B (four months after a $40M A); HiddenLayer $100M B; AIR Security $50M A. AI-security startups raised **$855M across 150+ seed rounds in 2026 YTD**, an all-time high clustered at $5–10M ([Crunchbase](https://news.crunchbase.com/cybersecurity/seed-trends-ai-security-startup-funding-2026/)).

**Exit read.** The single most relevant comp is **Palo Alto/Portkey at $117M disclosed** — an AI gateway, the closest structural analogue to "privacy layer for LLM access." The honest distribution is a barbell: **~$250–400M** if you become a control point during a bidding window; **~$40–120M** if you're a good team with a feature. The modal deal is 18–36 months old, Series A, $8–30M raised. **A large Series B is an exit risk, not a milestone** — Onyx now needs $600M+ to be good for founders. And the 2025 land grab is over: every platform now owns an AI-security asset, shifting them from "buy the category" to "fill a gap cheaply."

---

## 6. Enterprise buying evidence

The category is real but the ACV is lower than your deck assumes.

- **Gartner: the market for securing AI reaches ~$4.8B in 2027, +68.7% over 2026** — the only accelerating segment in a $248.9B security forecast ([Gartner](https://www.gartner.com/en/newsroom/press-releases/2026-08-26-gartner-forecasts-the-market-for-securing-ai-will-reach-almost-5-billion-in-2027)). Enterprises still spend ~17x more on AI tools than on securing AI.
- **Nightfall: median $25,000/yr across 41 tracked purchases, range $12,000–$73,200**, average 19.8% off list ([Vendr](https://www.vendr.com/marketplace/nightfall)). By size: 10–50 users $8–20K; 50–250 users $25–60K; 250+ users $75–200K+.
- **Skyflow: ~$194,500 average annual cost** — but ([Vendr](https://www.vendr.com/buyer-guides/skyflow)) this is based on **one completed deal and one purchaser**. Treat as indicative, not a median.
- **Prompt Security (SentinelOne): $10,000 per 12-month contract** on AWS Marketplace. **HiddenLayer: $5,000,000** per platform unit. **Portkey: $49/month for 100K logs.** ([accuroai.co, Sep 2026](https://accuroai.co/blog/what-ai-security-actually-costs))
- Hyperscalers give the primitive away: **Google Model Armor $0.10/1M tokens after 2M free**; AWS Bedrock Guardrails $0.10–0.17/1K units.
- **73.6% of surveyed CISOs use no commercial GRC platform at all**; 51% of GRC teams are four people or fewer ([Return on Security](https://www.returnonsecurity.com/p/ai-era-grc-market)). Security budget growth slowed to **4% YoY in 2025**, with over half of CISOs flat or shrinking.

**Realistic ACV:** SMB $8–25K, mid-market $25–75K, enterprise $75–200K. Your **$75–150K enterprise gateway is defensible at the top of the market but is not the median** — the median for a comparable AI-DLP product is $25K. Your **$30/seat/month Teams tier implies ~$10,800/yr for a 30-seat team**, which is consistent with the SMB band and probably your most credible line. The buyer is the CISO or platform owner; budget comes out of DSPM/DLP, not a dedicated "AI governance" line, which mostly does not exist yet.

---

## 7. The graveyard

| Company | Died / pivoted | Raised | Cause |
|---|---|---|---|
| **[Crosshatch](https://www.crosshatch.io)** | **Shut down Jul 2025** | VC-backed | "Plaid for Personalized AI" — consumer data wallet with a **Proxy API letting apps use consumer context without handling the data**. Site now an archive: *"We shut down July 2025… should they be useful to anyone attempting a new identity layer for personalized AI."* **This is the closest funded attempt at your per-agent-data-scope thesis, and it died.** |
| **Blyss** (YC W23) | Inactive | YC | "End-to-end encrypted AI" via GPU enclaves. Right thesis, two years early. |
| **Piiano** | **Pivoted Jun 2025** | $9M (YL Ventures) | Vault discontinued after four years; became **MCPTotal**, an AI agent governance plane. A funded PII-vault company concluded the vault wasn't the business. |
| **TripleBlind** | Asset sale, ~2024 | $32.2M+ | Privacy Suite went to Selfii; team spun out as Ideem. Not a growth exit. |
| **Privitar** | Acquired 2023 | $150M+ | Last valued >$400M in 2020; Informatica price undisclosed — almost certainly a down exit ([TechCrunch](https://techcrunch.com/2023/06/14/informatica-acquires-privitar-once-valued-at-400m-to-expand-its-data-management-stack/)). |
| **Hazy** | IP-only sale to SAS, Nov 2024 | ~$13M+ | SAS bought "primary software capabilities," not the company. |
| **LLM Guard** | **Archived 2026-07-09** | Protect AI → Palo Alto | 3,207 stars, now read-only. The most-cited OSS competitor in your deck **no longer exists**. |
| **Guardrails AI** | Acquired by Harvey, Sep 2026 | $7.5M | Category pioneer, quiet landing. |
| **Tesseral** (YC W24), **Mendral** (YC W26) | Inactive | YC | Identity/devops; Mendral died within months of its batch. |
| **Rebuff**, **Vigil-LLM**, **gretel-synthetics**, **anonLLM**, **masquerade**, **Pebblo** | Archived/abandoned 2024–25 | OSS | The 2023 wave of LLM-security OSS is dead. |
| **Panda.chat**, **veil-api.com** | Dead (NXDOMAIN / HTTP 500) | — | Typical consumer-privacy-chat mortality. |
| **SafeKey Lab** | Pivoted | — | Was "PII redaction for LLM inputs" in Dec 2025; now drone/spacecraft security monitoring. |

**The causes, stated plainly.** (1) **No forcing function** — Preclusio, Privitar and Piiano all found that privacy tooling is a vitamin without a statute. (2) **The wrong half of the stack** — Piiano's pivot from vault to agent governance is the same move Skyflow made; everybody converges on the control plane because that's where the budget is. (3) **Consumer conversion doesn't happen** — Crosshatch, Blyss, Panda.chat. (4) **Commoditisation from above** — OpenAI shipped an **Apache-2.0 PII detector** (`openai/privacy-filter`, 1.5B params, 231k downloads); NVIDIA shipped [NeMo Anonymizer](https://github.com/NVIDIA-NeMo/Anonymizer); Presidio left Microsoft for a neutral foundation with 10,931 stars. **Detection is free.** Note carefully: **none of these are reversible.**

---

## 8. Open-source competition

The OSS field is much larger than "Anonproxy at 7 stars and DontFeedTheAI at 655." Verified live on 2026-09-18:

| Project | Stars | License | Reversible | Backer |
|---|---|---|---|---|
| [Presidio](https://github.com/data-privacy-stack/presidio) | 10,931 | MIT | No | **Left Microsoft** — now vendor-neutral |
| [LLM Guard](https://github.com/protectai/llm-guard) | 3,207 | MIT | Yes | ☠️ **ARCHIVED 2026-07-09** |
| [rizzo-pii](https://github.com/Rizzo-AI-Academy/rizzo-pii) | 1,000 | MIT/AGPL | **Yes** | Rizzo AI Academy (IT legal-tech) |
| [pasteguard](https://github.com/sgasser/pasteguard) | 753 | Apache-2.0 | **Yes** | Solo; [pasteguard.com](https://pasteguard.com), **free, no paid tier** |
| [dataiku/kiji-proxy](https://github.com/dataiku/kiji-proxy) | 430 | Apache-2.0 | **Yes** | **Dataiku — funded company, unmonetised OSS** |
| [thoughtbot/top_secret](https://github.com/thoughtbot/top_secret) | 417 | MIT | **Yes** | thoughtbot |
| [privacy-filter](https://github.com/packyme/privacy-filter) | 336 | MIT | No | PackyCode |
| [vigils](https://github.com/duncatzat/vigils) | 302 | Apache-2.0 | Partial | [vigils.ai](https://vigils.ai) — agent control plane + PII |
| [maskit](https://github.com/xiaYuTian11/maskit) | 246 | AGPL-3.0 | Yes | Solo |
| [promptmask](https://github.com/cxumol/promptmask) | 154 | MIT | Yes | Solo |
| [NeMo Anonymizer](https://github.com/NVIDIA-NeMo/Anonymizer) | 122 | Apache-2.0 | No | **NVIDIA** |
| [CosyRedactGateway](https://github.com/CassiopeiaCode/CosyRedactGateway) | 83 | Apache-2.0 | **Yes** | Solo |
| [datafog-python](https://github.com/DataFog/datafog-python) | 73 | MIT | No | **Open-core**, datafog.ai |
| [promptzero](https://github.com/openbashok/promptzero) | 69 | none | **Yes** | Direct Anonproxy analogue |
| [cloakpipe](https://github.com/rohansx/cloakpipe) | 42–48 | MIT | **Yes** | **Open-core — Cloud at $99–$499/mo** |
| [Anonproxy](https://github.com/jfreemansh/Anonproxy) | **7** | MIT | Yes | Solo |

Plus a long tail of ~40 projects at 0–13 stars, almost all created in 2026.

**Who is commercialising an OSS core:** CloakPipe (clearest open-core), CertaMesh/gaze (published open-core policy), Occludra, Arcjet, Hoop.dev, DataFog, Censgate (Apache + CLA — relicensing optionality), and inversely Tonic.ai and Enigma Vault, whose repos are demo shells around closed paid reversible tokenization. **Tonic is the most commercially serious reversible player.**

**The dangerous one is Dataiku's Kiji Proxy:** a well-funded company shipping a fully reversible privacy proxy as pure Apache-2.0 **with no paid tier**. Dangerous precisely *because* it is unmonetised.

**Demand signal from HN.** Every "Show HN" for a PII-redaction proxy since 2025 scored **1–7 points with 0–2 comments**: PromptMask (4), Claw Shield (1), Veil (2), Selixes (3), TensorWall (1), Prompt-scrub (4), SafeKey (4). The only things that got real traction were **Tinfoil (146 points, 100 comments)** and Credal (114). And **Skyflow, Protecto, WitnessAI and Wald.ai have literally zero HN story mentions.** Redaction proxies do not excite developers. Verifiable privacy does.

---

## 9. Where a new entrant could still win

Be skeptical of four things first.

**What's genuinely closed.** Reversible tokenization as a gateway is not white space — Skyflow ships an LLM Gateway that de-identifies and re-identifies, Kong restores, Wald and Protecto and WitnessAI all do it, Tonic has a real `unredact()`, and there are a dozen OSS implementations with more stars than Anonproxy. **Detection is free from OpenAI, NVIDIA and Presidio.** The detector cannot be the moat, and neither can reversibility alone.

**What the consumer evidence says.** 0.1% conversion at Brave. $66.4M at Mozilla across 200M users. Crosshatch dead. Blyss dead. Panda.chat dead. LogosGuard is free, PasteGuard is free, Kiji is free, Egoist is free for individuals, and nullsink already sells account-less frontier access for crypto. **A paid consumer privacy proxy is the single hardest business in this report.** Venice.ai is the one counter-example, and it wins by selling *AI* at an AI price with privacy as framing — not by selling privacy.

**What the enterprise evidence says.** Median ACV $25K, not $150K. 73.6% of CISOs buy no governance platform. Budget growth 4%. Portkey — the closest structural comp — sold for $117M.

So where is the opening?

**1. The agent gateway, not the prompt proxy.** Bedrock's PII filter [documented] does not evaluate `toolUse.input`, `toolResult`, or `toolSpec`. Cross-agent, cross-tool-call **bijective consistency** is the one thing no incumbent ships and no OSS project has solved — gaze publishes its own 20.7% byte-leak benchmark and is honest that it's unsolved. Quilr is the only company doing both halves, and it is early and undercapitalised. **This is your real wedge, and it is narrower and more technical than "privacy layer for AI."**

**2. Own the inline enforcement path.** Return on Security's analysis is that the agent-governance *dashboard* layer is commoditising (~49 venture-funded startups in three years) while the **data plane compounds**. Every large exit — Portkey, Genie, Oasis — sat in the access path and touched the data. A product that only inspects prompts is a feature Palo Alto, Cisco and Zscaler each already own three times.

**3. Sell the legal artifact, not the privacy.** The CJEU *EDPS v SRB* ruling (C-413/23 P, Sep 2025) assesses identifiability **from the recipient's perspective**. Local key custody is the strongest available claim that data leaving the device is not personal data *for the provider*. **That is a compliance unlock — the same structural move HIPAA Expert Determination gave Datavant.** It converts Lethe from a vitamin into a painkiller, and it is the only forcing function available to you. Build the evidence pack, the auditor relationship, and the expert determination analogue *before* the product polish.

**4. Be acquirable early and cheaply.** Keep total raised under ~$15M. The modal outcome is an $8–30M-raised Series A company selling for 4–12x capital to Palo Alto, Cisco, Check Point, Zscaler, F5, Cyera or a data platform. At $10M raised, a $150M exit is excellent. At $60M raised it is a wash. **Get a platform vendor as a design partner or investor early** — F5 invested in Prompt Security before buying CalypsoAI; Akamai led Hush's Series A.

**What I would drop.** "Datavant for AI" — a sophisticated investor will pull the thread and find that Datavant holds the master salt, that its revenue is chart-retrieval services, and that the linkable version of the business (LiveRamp) sold for 2.7x. The Mnemosyne Mark certification business is the weakest line; standards bodies are not seed-stage businesses, and nothing in this sweep suggests anyone will pay for a badge. And the $70M-ARR five-year model at $120K ACV assumes 5x the category median contract value — either defend that premium explicitly or reprice.

**The honest summary:** the mechanism is crowded, the consumer thesis has a graveyard, and the enterprise ACV is a third of what the deck assumes. What is genuinely unclaimed is **swarm-consistent reversible surrogates across agents and tool calls, held to a legal standard, sold to a platform owner** — a narrower, more defensible, and considerably less romantic company than "a privacy layer for the agentic era."

---

**Gaps to close:** DuckDuckGo revenue has no primary source. DeleteMe revenue and the "WhiteHat/PE" investment are unsubstantiated. Datavant's revenue, headcount and current valuation are all estimates. Skyflow's $295M Forge mark is a secondary-market quote, not a round. No VPN-specific churn figure is published anywhere. Latio, CSA, Menlo and Bessemer market maps were not fully mined — the web-search quota ran out. Arthur AI's GitHub repos now 404 and its status is unverified.
