# GEO / AI Search Readiness Audit — anzocapital.com
Audit date: 2026-08-17 | Rendered site: https://www.anzocapital.com/en
Cross-reference: see `schema.md` for full structured-data validation detail (this file focuses on AI-crawler access, citability, and platform-visibility signals).

## GEO Health Score: 55 / 100

| Dimension | Weight | Score | Weighted |
|---|---|---|---|
| Citability | 25% | 65/100 | 16.3 |
| Structural Readability | 20% | 75/100 | 15.0 |
| Multi-Modal Content | 15% | 45/100 | 6.8 |
| Authority & Brand Signals | 20% | 55/100 | 11.0 |
| Technical Accessibility | 20% | 30/100 | 6.0 |
| **Total** | | | **55.0** |

**Headline finding:** the content itself (once JavaScript executes) is genuinely strong for GEO — clear definitional Q&A ("What is a margin call?", "What is a stop-out?"), comparison tables, FAQ blocks, and specific sourced statistics. But the site is **100% client-side rendered** with no server-rendered body content and no `<noscript>` fallback, which is a severe technical barrier for AI crawlers that don't execute JavaScript at scale (GPTBot, ClaudeBot, PerplexityBot). This single issue likely suppresses citation eligibility across the entire content library regardless of content quality.

---

## 1. AI Crawler Access (robots.txt) — Severity: Medium (informational gap, not a block)

```
User-agent: *
Allow: /en/
Disallow: /block
Disallow: /fr/
Disallow: /zh-Hans/
Disallow: /zh-Hant/
Host: www.anzocapital.com
Sitemap: https://www.anzocapital.com/sitemap.xml
```

- **No explicit AI-crawler rules** (GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, Google-Extended, CCBot, anthropic-ai) — everything falls through to the wildcard `User-agent: *` block.
- Under the wildcard rule, `/en/` is explicitly **Allowed** and only `/block`, `/fr/`, `/zh-Hans/`, `/zh-Hant/` are **Disallowed**. Since all the audited blog/market-analysis/regulation content lives under `/en/`, **AI crawlers are not blocked by robots.txt today** — this is a pass, not a gap.
- The `Disallow: /fr/`, `/zh-Hans/`, `/zh-Hant/` rules apply identically to every UA including AI crawlers (there's no AI-specific carve-out, but there's also no reason for one — locale-blocking is a deliberate, consistent policy here, not an accidental AI-crawler restriction). **Not flagged as a problem.**
- Worth flagging as **Info/Low**, not a gap to fix urgently: the *absence* of explicit `Allow`/`Disallow` blocks for GPTBot/ClaudeBot/PerplexityBot means the site has no way to differentiate AI-search crawlers (which the business likely wants for citation visibility) from pure AI-training crawlers (CCBot, anthropic-ai, Google-Extended) if the business ever wants to permit one and not the other. Currently everything is allowed by default, which is the correct posture if the goal is maximum AI visibility — but it's implicit, not intentional, and should be made explicit so a future robots.txt edit doesn't accidentally introduce a block.
- **Secondary finding (Low):** `sitemap.xml` lists `fr/`, `zh-Hans/`, `zh-Hant/` URLs that are simultaneously `Disallow`'d in robots.txt — a crawl-directive contradiction. Not AI-crawler-specific but worth a general SEO fix.

**Recommendation:** Add explicit `Allow` directives for GPTBot, OAI-SearchBot, ClaudeBot, and PerplexityBot (even though they're already implicitly allowed) to make the intent explicit and future-proof against accidental blocking. Effort: Low (5 min).

---

## 2. llms.txt — Severity: Low (per policy, optional/ignored by Google — not overweighted)

- `https://www.anzocapital.com/llms.txt` returns **HTTP 200**, but the response is **not a real llms.txt file** — it's the Next.js app's catch-all SPA shell rendering a client-side "not-found" page (confirmed via `not-found` chunk reference and page text). This is effectively a **soft-404**: content-type is `text/html`, not `text/plain` or `text/markdown`, and the body contains no llms.txt-formatted content.
- No RSL 1.0 licensing file found either.
- Per policy this is low priority (llms.txt is an emerging, non-standardized convention with no confirmed adoption by major AI crawlers, and Google Search ignores it). Given the site has 90+ blog posts and 25+ market-analysis posts, a curated llms.txt (linking canonical URLs for cornerstone definitional content like the margin-call and gold-vs-silver guides) would be a cheap, low-risk addition — but should not be treated as a blocking issue.

**Recommendation:** Optional — add a real `/llms.txt` (static file, bypassing the SPA router) listing top educational/regulatory pages. Effort: Low. Priority: Low.

---

## 3. Technical Accessibility for AI Crawlers — Severity: **Critical**

This is the most important finding in this audit.

Tested with `render_page.py --mode never` (raw HTTP fetch, no JS execution) across five page types:

| Page | Pre-JS body text (trafilatura/bs4) |
|---|---|
| `/en/` (homepage) | 47 chars — title only |
| `/en/blog/margin-call-guide` | 53 chars — title only |
| `/en/market-analysis/eur-usd-nfp-...` | 54 chars — title only |
| `/en/regulation` | 53 chars — title only |
| `/en/legal-documents` | 55 chars — title only |

In every case, the pre-JS HTML `<body>` contains **nothing but the page title text** — no article body, no FAQ content, no tables, no risk disclosures. The `<head>` is well-formed (title, meta description, canonical, OG tags are all server-rendered via Next.js metadata API — good), but all substantive content is injected client-side after hydration. There is no `<noscript>` fallback.

- `render_page.py`'s SPA auto-detection correctly flags `is_spa: True` on every sampled page and falls back to full Playwright rendering to retrieve content — meaning the full 8,000–13,000 character articles (definitions, FAQs, tables, stats) **only exist post-JavaScript-execution**.
- **GPTBot, ClaudeBot, and PerplexityBot are generally understood to not execute JavaScript at crawl scale** (unlike Googlebot, which renders via headless Chromium in a second indexing wave, and unlike Bing which has partial rendering capability). If that holds for this site's traffic, these crawlers see an effectively blank page for every blog post, market-analysis post, and the regulation/legal pages — independent of the permissive robots.txt.
- This explains a likely disconnect: robots.txt allows crawling, structured content is excellent when rendered, but the actual bytes delivered to a non-rendering bot are near-empty. **This is very plausibly the single highest-leverage fix on the site for AI answer-engine citation eligibility.**

**Recommendation:** Migrate blog/market-analysis/regulation/legal templates to SSR or static generation (Next.js supports this natively — this looks like a client-fetch/CSR-only implementation of an otherwise SSR-capable framework, so the fix is architectural but not a full rewrite). At minimum, ship server-rendered article body HTML matching what's currently only available post-hydration. Effort: **High** (engineering-owned, likely a Next.js rendering-strategy change). Priority: **Critical — do first.**

---

## 4. Passage-Level Citability of Blog/Market-Analysis Content — Severity: Medium (content is strong; markup coverage is inconsistent)

Once rendered, content quality is genuinely good for GEO:

- **`/en/blog/margin-call-guide`** (definitional): Clean, self-contained definitions — *"A margin call is a warning that your account equity is getting too close to the minimum required to keep your trades open... your margin level is falling toward the broker's required threshold..."* — followed immediately by a distinct, equally clean definition of "stop-out," then a direct comparison table (Margin Call vs Stop-Out). A 5-question FAQ block closes the article with short, extractable, self-contained answers (e.g., "Does a 50% bonus prevent margin calls? No, it does not prevent margin calls..."). Includes dated, sourced data points (2021 margin-call cascade, "$19 billion in leveraged positions wiped out in 25 minutes"). Ends with a full, explicit Risk Disclaimer paragraph. **This is exactly the kind of citable, definitional YMYL content AI Overviews/ChatGPT favor** — but **this specific page ships zero JSON-LD** (confirmed 0 structured-data blocks), so none of this excellent Q&A structure is machine-marked as `FAQPage`/`BlogPosting`. Machine-readability lags well behind prose quality here.
- **`/en/blog/gold-vs-silver`**: Strong comparison table (gold vs. silver drivers, volatility, liquidity), a clearly worked formula (`Gold–Silver Ratio = Gold Price / Silver Price`, with a numeric example), and a 5-question `FAQPage` block that **is** correctly marked up (`BlogPosting` + `FAQPage` + `BreadcrumbList` all present and valid). This is the standard the rest of the blog should match. One gap: specific stats ("$361B/day" liquidity, "219,890 tonnes" mined) are stated without inline source attribution/links, which reduces AI-engine confidence in citing the exact figures verbatim.
- **`/en/market-analysis/eur-usd-nfp-trade-setup-...`**: Concrete, dated, sourced statistics (NFP "-23,000 jobs vs. +80,000 expected," wage growth "3.2% YoY," unemployment "4.1%," 2-year yield "4.25% → 4.17%," DXY "99.50"), explicit data-source attribution ("Charts and market data shown are sourced from MetaTrader 4 (Anzo Capital)"), and a clear risk/informational disclaimer. `AnalysisNewsArticle` schema is present with `SpeakableSpecification` (a positive, underused signal for voice/AI-assistant excerpting) targeting `h1` and `h1 + p`. Gap: the market data is attributed only to the broker's own MT4 feed, not an independent/reputable third party (e.g., BLS for NFP) — AI systems may discount single-source, self-attributed statistics for market-moving numbers.
- **Coverage inconsistency (cross-referenced with `schema.md`):** confirmed across multiple spot-checks that structured data (`BlogPosting`/`AnalysisNewsArticle`/`FAQPage`) is present on some articles and completely absent on others of the same template (e.g., `margin-call-guide` has 0 JSON-LD blocks vs. `gold-vs-silver`'s full markup). Given the sitemap shows 80+ `/en/blog/*` and 20+ `/en/market-analysis/*` URLs, this pattern likely affects a large fraction of the content library, meaning citability is inconsistent article-to-article even though the best examples are excellent.

**Recommendation:** (1) Backfill `BlogPosting`/`AnalysisNewsArticle`/`FAQPage` schema on all articles missing it — the CMS clearly supports it, so this looks like a toggle/field not being populated consistently, not a template limitation. (2) Add inline source links for third-party statistics. Effort: Medium (content ops + one CMS field fix). Priority: High.

---

## 5. Authority & Brand Signals (Organization Schema / Entity Recognition) — Severity: Medium

Homepage `Organization` schema (`@id: https://www.anzocapital.com/en/#organization`) is reasonably complete:

- ✅ `legalName` ("Anzo Capital (SVG) LLC"), `alternateName`, `foundingDate` (2015), `identifier`/registration number, `address`, `logo`, `award` list (10 named industry awards), 3 `contactPoint` entries.
- ✅ `sameAs` covers 7 authoritative profiles: Google Maps/Business listing, LinkedIn, Instagram, Facebook, **YouTube**, Telegram, X — this hits the single strongest AI-citation-correlated signal in the brief (YouTube, ~0.737 correlation) and several of the other high-value platforms.
- ❌ **No Wikipedia entity** and **no Reddit presence** in `sameAs` or detected elsewhere in this audit (both flagged in the brief as high-correlation signals) — expected for a mid-size private broker, but worth noting as a ceiling on entity-recognition strength; not fixable via schema alone (requires actual third-party presence to exist first).
- ⚠️ **Address/sameAs mismatch** (full detail in `schema.md`): the declared `PostalAddress` is a St. Vincent & the Grenadines registered-agent address, but the first `sameAs` Google Maps link resolves to central London — a geographic contradiction on the same entity `@id`. For a YMYL financial entity this is a meaningful trust-signal inconsistency that AI systems cross-referencing entity data could flag as unreliable.
- ⚠️ **Authorship is not individually attributed**: blog posts credit `"Anzo Capital"` (Organization) as author; market-analysis posts credit a pseudonymous `"Anzo Capital - Senior Market Analyst"` (`Person` type, but no actual name, no bio page, no credentials, no `sameAs`). For YMYL financial content, AI systems increasingly weight named, credentialed authorship as an E-E-A-T signal — generic/pseudonymous bylines are a weaker signal than a named analyst with a linked author-bio page.

**Recommendation:** (1) Fix the address/Maps mismatch (data-integrity issue, not just SEO). (2) Add named author bios with credentials for market-analysis content, linked via `sameAs`/`author.url` to a real bio page. Effort: Medium. Priority: Medium-High.

---

## 6. YMYL Regulatory/Legal Content Structure (`/en/regulation`, `/en/legal-documents`) — Severity: High

This is the area where AI systems are most cautious about citing financial content, and it's currently the weakest content on the site from an extractability/specificity standpoint.

- `/en/regulation` extracted text uses only vague, unnamed language: *"operating under the oversight of multiple regulatory authorities,"* *"licensed by esteemed financial governing bodies across various jurisdictions"* — **no specific regulator name, license number, or verification link appears in the extractable text.** (Regulator badges/logos may exist visually on the page but were not captured as text — if they lack descriptive `alt` text, that content is invisible to both AI crawlers and citability scoring; worth a follow-up check.)
- The registered legal entity is explicitly **Anzo Capital (SVG) LLC** — a St. Vincent & the Grenadines International Business Company. SVG's Financial Services Authority is publicly on record as not licensing or regulating forex/CFD brokerage activity, which makes broad phrases like "licensed by esteemed financial governing bodies" harder for an AI system to verify or corroborate against a named regulator, and increases the chance that cautious AI Overviews/chat assistants simply decline to cite regulatory claims from this page at all.
- The `/en/regulation` page does carry `FAQPage` schema, but the 5 Q&A pairs are **account-opening FAQs** ("How do I open an account?", "Are there fees for deposits/withdrawals?"), not regulation-specific Q&A (e.g., "Which regulator licenses Anzo Capital?", "What is Anzo Capital's license number?"). This is a missed opportunity — the exact page most likely to be queried for regulatory verification doesn't answer the regulatory question directly and extractably.
- `/en/legal-documents` extracted text is essentially just the incorporation statement and a general risk-disclosure paragraph; the page's schema includes `DigitalDocument`/`ItemList` types suggesting individual policy documents (Privacy Policy, Terms, Risk Disclosure) exist, but their titles/dates/versions were not surfaced in the extracted text — reducing their extractability as individually citable, dated legal sources.
- On the positive side: risk-disclosure language **is** present and reasonably thorough where it does appear (both `/en/regulation` and the sampled blog/market-analysis articles close with clear, standard leveraged-trading risk disclaimers — "You may lose more than what you invest," "not suitable for everyone," "we recommend independent financial advice"). This is a genuine strength AI systems should reward.

**Recommendation:** Rewrite `/en/regulation` to name the specific regulator(s), license number(s), and a verification link/reference number for each, structured as direct Q&A ("Is Anzo Capital regulated? Anzo Capital [entity] is licensed by [named regulator] under license number [X], verifiable at [URL]"). Replace the generic account-opening FAQ on that page with regulation-specific Q&A. Effort: Medium (content + legal sign-off). Priority: **High** — this is the page most likely to be checked by a cautious AI system before citing anything else on the domain.

---

## 7. Multi-Modal Content — Severity: Medium

- Article schema references chart/screenshot images (`ImageObject`) consistently, and market-analysis content explicitly describes chart-based analysis (volume profile, market structure) — but no video content, embeds, or `VideoObject` schema were found on any of the 4 sampled article pages, despite the brand having an active YouTube channel (linked in `sameAs`). Given YouTube mentions are the single strongest AI-citation correlation signal cited in the brief, embedding or linking relevant YouTube videos into educational blog content (e.g., a video explainer alongside the margin-call article) is a clear, currently-unused opportunity.
- No downloadable/structured PDF or data-table exports observed for legal/regulatory documents.

**Recommendation:** Embed existing YouTube content into relevant educational articles with proper `VideoObject` schema. Effort: Low-Medium. Priority: Medium.

---

## Top 5 Highest-Impact Changes

| # | Change | Dimension | Effort | Priority |
|---|---|---|---|---|
| 1 | Move article body content (blog, market-analysis, regulation, legal) to server-side rendering — currently 100% CSR with no `<noscript>` fallback, meaning most non-JS AI crawlers see title-only pages | Technical Accessibility | High | **Critical** |
| 2 | Rewrite `/en/regulation` with named regulator(s), license number(s), verification links, and regulation-specific FAQ (replace generic account-opening FAQ) | Authority / YMYL | Medium | **High** |
| 3 | Backfill missing `BlogPosting`/`AnalysisNewsArticle`/`FAQPage` schema on articles that currently ship zero structured data (confirmed inconsistent, e.g. `margin-call-guide`) | Citability | Medium | High |
| 4 | Fix Organization `sameAs` Google Maps / `PostalAddress` geographic mismatch and add named author bios (with credentials) for market-analysis content | Authority | Medium | Medium-High |
| 5 | Add explicit AI-crawler `Allow` rules to robots.txt (GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot) to make current implicit-allow posture explicit; add real `/llms.txt` | Technical / Optional | Low | Low-Medium |

---

## Platform-Specific Estimated Scores (directional, not measured live — no DataForSEO/live-ChatGPT tooling was available in this run)

| Platform | Estimated readiness | Rationale |
|---|---|---|
| Google AI Overviews | 55/100 | Googlebot renders JS, so the CSR issue is largely mitigated for Google specifically; scored down for the vague regulatory language and inconsistent schema coverage. |
| ChatGPT / OAI-SearchBot | 30/100 | If GPTBot does not render JS, most article content is effectively invisible regardless of quality; homepage/head metadata alone is insufficient for citation. |
| Perplexity | 30/100 | Same CSR risk as ChatGPT; Perplexity is known to weight structured, sourced statistics highly, which this site has in places but inconsistently marked up. |
| Bing Copilot | 45/100 | Bing has partial JS-rendering capability, so likely a partial mitigation vs. ChatGPT/Perplexity, but still constrained by the regulatory-content vagueness. |

These are directional estimates based on documented crawler behavior patterns, not live-tested citations. Recommend re-running with DataForSEO's `ai_optimization_chat_gpt_scraper` / `ai_opt_llm_ment_search` tools (not available in this session) to confirm actual current citation status.
