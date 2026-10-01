# OpenRouter — the idea and the funding journey, and what Lethe should take

Checked 2026-10-02.

## What it is

One API in front of 500+ models from 80+ providers. Model usage passes through at the provider's list
price; OpenRouter charges a platform fee on credit purchases: **5.5%** standard, **8%** for the Business
tier launched September 2026 (inference locked to EU or US providers), and **5%** on bring-your-own-key
traffic above a free allowance.

## The journey

| When | What happened |
|---|---|
| Aug 2022 | Alex Atallah leaves OpenSea, which he co-founded and which peaked at ~$3B a month in volume |
| Apr 2023 | Ships **Window.ai**, an open-source Chrome extension letting any web app use any model |
| May 2023 | Founds OpenRouter with Louis Vichy (met while building Window.ai) |
| Oct 2024 | ~$10M annualised inference spend through the platform |
| May 2025 | $100M+ annualised inference spend; ~$400k monthly revenue |
| Jun 2025 | Announces **$40M** seed + Series A, a16z and Menlo, Sequoia participating, ~**$500M** valuation |
| Apr 2026 | ~$50M ARR; ~100 employees, only **two** account executives |
| May 2026 | **$113M** Series B at **$1.3B**, led by Alphabet's CapitalG; Nvidia, ServiceNow, Snowflake, Databricks, MongoDB in |
| Aug 2026 | Stripe reportedly agrees to acquire for **more than $7B**, mostly stock (Bloomberg, TechCrunch; Stripe did not comment) |

About three and a half years from first commit to exit. Note the difference between *inference spend*
(the money flowing through) and *revenue* (the ~5.5% fee on it); headlines often quote the first.
Revenue estimates conflict across sources and should be treated as approximate.

## How it grew

- **A public data asset was the growth engine.** The live rankings page, showing which models developers
  actually use, became the industry's reference and the main acquisition channel. Labs listed on
  OpenRouter to reach that audience; OpenAI tested GPT-4.1 on it under aliases before launch.
- **Product-led.** A hundred people, two salespeople.
- **Two-sided network effect.** More models attract developers; more developers attract models.

## The criticism

- **Thin and shrinking margin.** Revenue is a percentage of token spend, and token prices fall fast.
  Growth has to outrun deflation.
- **It erodes its own reason to exist.** Putting every model on one comparable shelf commoditises them;
  developers increasingly "just call the cheapest one", and high-volume customers can go direct to avoid
  the fee. Anthropic was 46% of platform revenue on 12% of traffic.
- **Neutrality under Stripe** is now an open question.

## Is it an inspiration?

**For the business model and the position: yes, strongly.**

1. **It proves the shape works.** Hold the provider relationships, pass usage through at cost, charge on
   top. That is exactly Lethe's per-query line. And the providers accepted it: they list on OpenRouter,
   and OpenAI launched a model there. That is the best evidence we have that providers will work with an
   intermediary pooling many users behind it, our biggest open constraint.
2. **It proves the position is worth billions.** Stripe paid more than $7B to own the layer in front of
   every model.
3. **It shows how to get distribution without salespeople.** A public data asset. Ours: the live size of
   the pool, which is also the security guarantee, and a public measure of what each provider can learn
   about you.
4. **It shows a practical launch path.** Lethe could launch as an OpenRouter customer behind its own
   relays, getting hundreds of models under one contract, then move to direct provider contracts.
   OpenRouter would see the pool's prompts but not who sent them. This needs a read of OpenRouter's own
   terms on pooled access before anyone relies on it.

**For the funding journey: only the milestones, not the path.** OpenRouter raised $40M at $500M on
the reputation of OpenSea's founder plus 10x growth in seven months. Without that pedigree, the
transferable part is the evidence it showed: a usage number growing fast enough to be undeniable. For
Lethe that number is pool size and firm members.

**Where Lethe is structurally better.**

- **You can bypass a router; you cannot bypass a pool.** Going direct to save OpenRouter's fee loses
  nothing important. Going direct to save Lethe's fee is exactly what identifies you.
- **The fee is priced on what it hides, not on tokens.** Membership does not deflate with token prices,
  which is OpenRouter's central weakness. Our per-query fee does, so weight the model toward membership.
- **Its network effect commoditises its suppliers; ours strengthens with every member.**

## The best line it gives us

OpenRouter is the opposite of Lethe on privacy. It is a single company that sees every user's account,
card and prompts across every provider, and it is now inside Stripe, which already knows who people are
financially. The most valuable seat in front of AI is now held by the company that holds your card.

> OpenRouter proved the seat in front of every model is worth billions. Lethe is the same seat, built so
> it cannot see you.

## Sources

- Contrary Research, OpenRouter: https://research.contrary.com/company/openrouter
- Series A announcement, June 2025: https://www.globenewswire.com/news-release/2025/06/25/3105125/0/en/OpenRouter-raises-40-million-to-scale-up-multi-model-inference-for-enterprise.html
- Series B, May 2026: https://www.trendingtopics.eu/openrouter-investment-capitalg-others/
- Stripe deal, Bloomberg: https://www.bloomberg.com/news/articles/2026-08-16/stripe-nears-deal-to-buy-ai-firm-openrouter-for-over-7-billion
- Stripe deal, TechCrunch: https://techcrunch.com/2026/08/16/stripe-will-reportedly-acquire-ai-gateway-startup-openrouter-for-7b/
- Pricing: https://www.aichatdaily.com/tools/openrouter ; https://aireiter.com/blog/openrouter-byok-fees-fallback-guide
- Critique: https://finance.biggo.com/news/L3-yh54B6tLPsnrZE-bl
- 20VC interview: https://www.thetwentyminutevc.com/alex-atallah
