# SEO Audit — anzocapital.com

**Audit date:** 2026-08-17 | **Site:** https://anzocapital.com (renders to https://www.anzocapital.com/en) | **Business type:** Financial Services — Forex/CFD Broker (YMYL, hybrid SaaS-product + Publisher content model)

## SEO Health Score: 54 / 100

| Category | Weight | Score |
|---|---|---|
| Technical SEO | 22% | 58 |
| Content Quality | 23% | 52 |
| On-Page SEO | 20% | 48 |
| Schema / Structured Data | 10% | 60 |
| Performance (CWV) | 10% | 45 |
| AI Search Readiness | 10% | 55 |
| Images | 5% | 65 |

**Data-source note:** Google API credentials (PageSpeed Insights, CrUX, GSC, GA4) and paid backlink APIs (Moz, Bing Webmaster) are not configured in this environment. Performance figures are lab-estimates from source/render inspection, not certified Lighthouse/CrUX field data. Backlink analysis is Common Crawl domain-level only (no DA/PA, referring domains, or toxic-link data). See individual category sections and `findings/*.md` for full caveats.

---

## Executive Summary

Anzo Capital is a forex/CFD broker with a substantial, well-organized site (~200 English pages: 82 blog posts, 28 dated market-analysis posts, 57 help-center articles, and a full account/instrument page set) built on Next.js behind Cloudflare. The content itself is frequently good — genuinely deep educational articles, sourced macro statistics, and a detailed FinancialProduct schema implementation for account pages. But one architectural decision undermines nearly every other category simultaneously: **the entire site is 100% client-side rendered with no server-rendered content and no fallback.** Three independent audit passes (technical, performance, AI-search readiness) each converged on this same root cause from different angles — it's simultaneously an LCP/Core-Web-Vitals problem, a non-Google-crawler discoverability problem, and an AI-answer-engine citation problem. It is the single highest-leverage fix available on this site.

Layered on top of that architectural issue is a second recurring pattern: **trust and authority signals are inconsistently and, on the most important page, insufficiently disclosed.** The `/en/regulation` page — the one page a skeptical prospect or a cautious AI system would check before trusting anything else on the domain — names its regulators but discloses zero license numbers or verification links, while independent third-party review sites already publish more specific detail than Anzo's own trust page. No blog or market-analysis content carries named, credentialed authorship. And one high-depth educational article (the margin-call guide) reframes a leverage-increasing bonus as a safety mechanism, directly inverting the neutral, risk-first framing used by every ranking competitor for that query.

### Top 5 Critical Issues
1. **Sitewide CSR-only rendering** — raw HTML is title-only on every template; no `<a href>` links exist without JS execution. Suppresses non-Google AI crawler visibility and gates LCP behind full hydration.
2. **robots.txt / sitemap / hreflang contradiction** — 102 of 322 sitemap URLs (fr/zh-Hans/zh-Hant) are disallowed from crawling while hreflang headers and the sitemap list them as valid alternates.
3. **Sitewide soft-404** — any invalid URL returns HTTP 200 with full page content, no noindex.
4. **`/en/regulation` under-discloses regulatory detail** versus what third-party reviewers already publish about the same broker.
5. **Inconsistent schema/E-E-A-T coverage** — best-in-class article templates exist and work well, but sibling articles on identical templates ship zero structured data and no named authorship, likely across a large share of the 110+ article-type URLs.

### Top 5 Quick Wins
1. Change the root→`/en` redirect hop from 307 to 301.
2. Add explicit `Allow` rules for GPTBot/OAI-SearchBot/ClaudeBot/PerplexityBot to robots.txt.
3. Fix the Organization schema `PostalAddress` (St. Vincent) vs. `sameAs` Google Maps (London) location mismatch.
4. Remove the deprecated `Host:` directive and clarify/remove the vague `Disallow: /block` rule.
5. Generate sitemap `lastmod` from real CMS `updated_at` timestamps instead of stamping today's date on all 322 URLs.

---

## Technical SEO — 58/100

**What works:** valid, well-formed sitemap (322 URLs); HTTPS+HSTS enforced; clean locale-prefixed URLs; correct responsive viewport; self-referencing canonicals on `/en/*`; fast TTFB (135–244ms) — Cloudflare origin compute is healthy.

**Critical**
- **Zero body content / zero links in raw HTML sitewide.** Every template tested (homepage, blog, market-analysis, regulation, legal-documents) returns only the `<title>` element pre-JS. No `<noscript>` fallback. Full detail and fix in `findings/technical.md` §8.
- **robots.txt disallows the exact locale paths hreflang and the sitemap declare as valid alternates.** `Disallow: /fr/, /zh-Hans/, /zh-Hant/` blocks 102 of 322 sitemap URLs (31.7%) that are simultaneously referenced via `Link: rel="alternate" hreflang="..."` HTTP headers on every page. Google cannot crawl these to verify reciprocal hreflang or read on-page directives.
- **Sitewide soft-404.** `/en/this-page-definitely-does-not-exist-xyz123` returns HTTP 200 with full "Oops! You're Off the Map" content — no `noindex`, no canonical, no `X-Robots-Tag`. Likely a Next.js catch-all route not calling `notFound()`.

**High**
- No CSP / X-Frame-Options / X-Content-Type-Options headers anywhere — clickjacking/MIME risk on a money-handling YMYL site.
- Help-center template (60+ pages) ships zero structured data, inconsistent with the blog template.
- Sitemap `lastmod` is identical (today's date) across all 322 URLs — a fabricated freshness signal Google will learn to discount.

**Medium** — 307 (not 301) on the root→`/en` hop; overly aggressive `no-store` cache-control on static/evergreen pages; zh-Hans missing canonical; inconsistent `x-default` hreflang; vague `Disallow: /block`; deprecated `Host:` directive.

**Info** — no IndexNow implementation despite an active publish cadence; JSON-LD delivered via React Server Components streaming payload (resolves correctly for Googlebot/Bingbot but invisible to plain-text parsers).

Full detail: `findings/technical.md`

---

## Content Quality — 52/100

**What works:** genuine depth where sampled (2,898-word margin-call guide, sourced macro statistics, comparison tables, FAQ blocks); risk disclaimers present and reasonably thorough; strong H2/H3 structure on best-example articles.

**Critical**
- **No named, credentialed authorship anywhere.** Blog posts credit the Organization; market-analysis posts credit a pseudonymous "Senior Market Analyst" with no name, bio, or credentials.
- **`/en/regulation` under-discloses versus public record** — see On-Page/AI-Readiness sections below for the same finding from different angles.

**High**
- The margin-call-guide blog post reframes a 50%-deposit bonus as a margin-call "safety net" — the opposite framing of every ranking competitor (SEC, FINRA, Fidelity, Vanguard) for this query, and a compliance-adjacent concern independent of SEO.
- The Bonus/Promo content cluster (11 posts) has severe near-duplicate content: three separate posts target the identical "50% deposit bonus" query.

**Medium** — content-operations inconsistency (best templates not consistently applied); MT4/MT5 alerts cluster (5 posts) shows the same cannibalization pattern at smaller scale; homepage prose is thin (386 words) relative to the commercial queries its title tag targets; risk disclaimers are buried at the bottom of long articles rather than leading.

**Info** — FAQPage schema present on several templates carries no current Google SERP benefit (retired May 2026); not urgent to remove.

Full detail: `findings/content.md`, `findings/cluster.md`

---

## On-Page SEO — 48/100

**What works:** clean URL slugs; correct self-referencing canonicals; detailed, accurate FinancialProduct spec data on account pages.

**Critical**
- Homepage, ECN/account pages, and `/en/regulation` are structurally page-type-mismatched against what Google actually rewards for their target queries. SERP analysis found 75–100% of top results for "best forex broker," "ECN account forex," and "is Anzo Capital regulated" are independent comparison/review content — Anzo's own `/regulation` page doesn't appear in the sample of top results for its own core trust query.

**High**
- ECN/account pages lack competitive differentiation: no named liquidity providers, no data-center/latency claim, no comparison table against competitors, unlike IC Markets/Pepperstone equivalents.
- No above-the-fold regulatory trust badge on homepage or conversion pages — the single most important trust signal for a forex broker is footer-only.

**Medium** — no sitemap content-hub/category segmentation for 115+ blog/help-center/market-analysis posts.

Full detail: `findings/sxo.md`, `findings/sitemap.md`

---

## Schema / Structured Data — 60/100

**What works:** 100% JSON-LD (no Microdata/RDFa), correct context/absolute URLs; rich homepage Organization/WebSite schema; detailed FinancialProduct implementation on account pages; no deprecated types used.

**Critical**
- Zero JSON-LD on multiple sampled blog, market-analysis, and help-center article pages despite sibling pages on identical templates having full schema — likely spans a large share of the 110+ article-type URLs.

**High**
- Organization `PostalAddress` (St. Vincent registered-agent address) conflicts with its own `sameAs` Google Maps link, which resolves to central London — a geographic contradiction for a regulated financial entity.

**Medium** — same Organization `@id` inconsistently typed (`Organization` vs. `Corporation`) across pages; `feesAndCommissionsSpecification` populated with free text instead of the required URL type; non-standard `contactType` value; a generic untyped `Thing` node in market-analysis JSON-LD.

**Info** — FAQPage usage carries no current SERP benefit; missing QAPage/BreadcrumbList on help-center articles.

Generated JSON-LD fixes for the top gaps are included in `findings/schema.md`.

---

## Performance (Core Web Vitals) — 45/100 *(lab estimate — no certified field/Lighthouse data this run)*

**What works:** strong TTFB (135–244ms) sitewide; reasonable DOM size; no console errors detected.

**Critical**
- Zero server-rendered above-fold content. Raw HTML body is an empty hidden Suspense boundary on every page tested — 0 `<img>`, 0 `<h1>` pre-hydration. LCP is gated behind full JS parse/hydrate. Render-time proxy varied 1.9s–4.2s across repeated homepage runs, indicating an unstable critical path.

**High**
- 24 distinct third-party scripts fire post-load, including duplicated tracking (2x Microsoft Clarity + Hotjar, 2x LinkedIn Insight Tag) and an eagerly-loaded, non-deferred `crypto-js.min.js` — a real INP risk on first interaction.

**Medium** — 16 first-party JS chunks required for the initial homepage route.

No PSI/CrUX field data was obtainable this run (no API key configured, PSI rate-limited, no local Lighthouse CLI). Treat all figures as directional; re-run once a Google API key or working Lighthouse is available.

Full detail: `findings/performance.md`

---

## AI Search Readiness (GEO) — 55/100

**What works:** robots.txt does not block AI crawlers today; content is genuinely strong for GEO once rendered (clear definitional Q&A, comparison tables, sourced stats, `SpeakableSpecification` on some market-analysis posts); Organization schema includes YouTube in `sameAs` (the strongest AI-citation-correlated platform signal).

**Critical**
- Same CSR-only rendering issue as Technical/Performance, viewed through the AI-crawler lens: GPTBot/ClaudeBot/PerplexityBot generally don't execute JS at scale, so pre-JS pages are title-only. Estimated platform readiness: Google AI Overviews 55/100 (Googlebot renders JS, largely mitigating this), ChatGPT/OAI-SearchBot 30/100, Perplexity 30/100, Bing Copilot 45/100.

**High**
- `/en/regulation` lacks the specific, extractable regulatory detail (named regulator, license number, verification link) a cautious AI system needs before citing financial claims. Its FAQPage schema answers generic account-opening questions, not the regulatory question the page is most likely to be queried for.

**Medium** — no video content despite an active YouTube channel linked in `sameAs`.

**Low** — `llms.txt` returns a soft-404 (SPA shell, not real content) — optional per policy, not overweighted; no explicit AI-crawler `Allow` rules in robots.txt (currently implicitly allowed, worth making explicit).

Full detail: `findings/geo.md`

---

## Images — 65/100 *(not independently audited this run — estimate from visual-audit observations)*

Images render correctly and scale properly across all breakpoints tested; no broken or oversized images visually apparent. Alt-text coverage and file-optimization were not directly assessed — recommend a dedicated `/seo images` pass. One brand-trust nuance (not a technical SEO issue): the homepage hero uses a busy P&L-mockup collage with aggressive leverage/return statistics that may read as "get-rich-quick" marketing for a YMYL site.

---

## Visual & Mobile UX — 78/100 *(supplementary — not part of the weighted health score)*

Strong fundamentals: primary CTA and trust stats (2015 Established, 80,000+ Global Clients) are visible above the fold on both desktop and mobile for homepage and the accounts-overview conversion page; responsive layout is clean across all breakpoints with no overflow or broken grids.

**Issues found:** no above-the-fold regulatory badge anywhere (footer-only); a persistent live-chat bubble overlaps editorial body text on the mobile blog post; a "Welcome Deposit Bonus" promo banner consumes 15–20% of the mobile viewport on every page and its dismiss control is under the 48×48px touch-target guideline; no visible author/reviewer byline above the fold on blog content.

Screenshots: `screenshots/` (14 desktop/mobile/tablet/laptop captures across homepage, blog, and accounts-overview).

Full detail: `findings/visual.md`

---

## Backlink Profile *(Tier 0 — Common Crawl only, no numeric score reported)*

Moz and Bing Webmaster API keys are not configured; referring-domain count, quality distribution, anchor text, toxic-link ratio, and link velocity are all unavailable at this tier and no score is reported to avoid a misleading figure. Common Crawl confirms the domain is crawled and present in the web graph (PageRank rank ~5.0M, harmonic centrality rank ~17.0M — outside the web's upper tier but not flagged as a negative signal in itself). WHOIS shows ~10.8 years of continuous registration, a mild positive signal against expired-domain/PBN risk patterns common in this niche.

**Recommendation:** add a free Moz API key (2,500 rows/month, no cost) before the next audit cycle — moderately high priority given forex/CFD's disproportionate exposure to toxic affiliate/PBN link schemes, which cannot currently be ruled out.

Full detail: `findings/backlinks.md`

---

## Content Cluster & Internal Linking Architecture *(supplementary)*

Blog (82 posts) and market-analysis (28 posts) operate as two disconnected flat archives with no hub pages and no cross-linking taxonomy. `/en/learning-library-guides` is a gated PDF lead-magnet page, not a content hub. Seven natural clusters were identified from the full slug inventory (Gold/Metals, Macro/Central-Bank, Copy Trading, MT4/MT5, IB Marketing, Bonus/Promo, Regional/SEA). The Bonus/Promo cluster shows the most severe cannibalization (3 near-duplicate "50% deposit bonus" posts, confirmed competing in live search), followed by MT4/MT5 Alerts (5 overlapping posts) and a Gold/Metals blog-vs-market-analysis collision (evergreen "what drives gold" content directly overlapping 4 dated forecast posts with no link relationship).

Full detail: `findings/cluster.md`

---

## Search Experience Optimization (SXO) *(supplementary)*

Anzo's biggest SXO problem: for nearly every non-branded query tested, Google rewards independent third-party comparison/review content, not the broker's own promotional pages — and Anzo has nothing built to compete in that format. Site-wide SXO Gap Score average: ~49/100, with the Trust/E-E-A-T dimension weakest everywhere (7–12/25 across all persona/page combinations). The `/en/regulation` page is the single most severe finding in the entire audit: its own core trust query ("is Anzo Capital regulated") surfaces 100% third-party review/verification sites in the SERP, and third parties already publish more regulatory specificity than Anzo's own page.

Full detail: `findings/sxo.md`

---

## Methodology Notes & Limitations

- No Google API credentials configured (PageSpeed Insights, CrUX, Search Console, GA4) — performance and indexation figures are lab/source-based estimates, not certified field data.
- No Moz/Bing Webmaster API keys configured — backlink analysis limited to free Common Crawl domain-level signals.
- The dedicated content-quality subagent for this run was interrupted by a session-limit error before producing its report; `findings/content.md` was synthesized from cross-referenced evidence gathered independently by the technical, schema, GEO, SXO, and cluster subagents (each of which read and quoted actual page content) rather than from a fresh independent pass. A follow-up `/seo content` run is recommended for exhaustive per-article sampling.
- Image SEO (alt text, file optimization) was not independently audited — the Images category score is an estimate from visual-audit observations only.
- SERP-backwards analysis in the SXO audit used WebSearch (AI-summarized results), not a raw SERP scrape — exact ranking positions and PAA lists could not be directly captured.
- Regulatory license numbers cited from third-party sources (TradersUnion, FXEmpire) were not independently verified against the FCA/ASIC/CMA public registers by this audit — the finding is about Anzo's own disclosure gap, not a verified compliance determination.

---

*Generate a professional PDF version of this report with:*
```
"$HOME/.claude/skills/seo/bin/claude-seo" run google_report.py --type full --data anzocapital.com-audit/audit-data.json --domain anzocapital.com --output-dir anzocapital.com-audit/
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Built by agricidaniel — Join the AI Marketing Hub community
🆓 Free  → https://www.skool.com/ai-marketing-hub
⚡ Pro   → https://www.skool.com/ai-marketing-hub-pro
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
