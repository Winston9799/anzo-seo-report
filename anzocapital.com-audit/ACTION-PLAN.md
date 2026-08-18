# Action Plan — anzocapital.com SEO Audit

Derived from `FULL-AUDIT-REPORT.md` (SEO Health Score: 54/100). Ordered by dependency — Phase 1 items unblock or de-risk items in later phases (e.g., the SSR migration in Phase 2 is easier to scope once the soft-404/routing fix in Phase 1 has already touched the same routing layer).

---

## Phase 1: Critical Fixes (Week 1)

1. **Fix robots.txt / sitemap / hreflang contradiction.** `Disallow: /fr/, /zh-Hans/, /zh-Hant/` blocks 102 of 322 sitemap URLs that hreflang headers and the sitemap declare as valid alternates. Decide: crawl-and-index these locales (remove the Disallow lines) or strip-and-noindex them (remove from sitemap/hreflang, add `noindex`). *Owner: SEO/Engineering. Effort: Low.*
2. **Fix sitewide soft-404.** Any invalid URL returns HTTP 200 with full page content. Ensure the Next.js catch-all route calls `notFound()`. *Owner: Engineering. Effort: Low.*
3. **Rewrite `/en/regulation`** with named regulator(s), license number(s), and direct verification links to each regulator's public register. This is the single most-cited trust gap across three independent audit passes (technical/schema, SXO, GEO). *Owner: Content + Legal/Compliance sign-off. Effort: Medium.*
4. **Add named, credentialed authorship** to blog and market-analysis content, starting with the highest-traffic articles. Replace the Organization-level byline and the pseudonymous "Senior Market Analyst" Person type with real names, bios, and credentials. *Owner: Content/Editorial. Effort: Medium.*
5. **Re-frame `margin-call-guide`** to lead with neutral, action-first risk guidance before any bonus-related content. Flag the broader "bonus as safety net" framing pattern for a compliance review outside SEO scope. *Owner: Content + Compliance. Effort: Low-Medium.*

**How we'll know these worked:** GSC Coverage report shows the fr/zh-Hans/zh-Hant "Excluded by robots.txt" bucket drop toward zero (or those URLs disappear from the sitemap, matching whichever path was chosen); a manual check of 10 random broken/typo URLs returns real 404s; `/en/regulation` reads as more specific than the top 3 third-party review results for "is Anzo Capital regulated" in a manual comparison.

---

## Phase 2: High-Impact Improvements (Weeks 2–4)

1. **Begin SSR/SSG migration** for blog, market-analysis, regulation, legal-documents, and help-center templates. This is the single highest-leverage fix identified across the technical, performance, and GEO audits — it simultaneously improves LCP, non-Google crawler discoverability, and AI-answer-engine citation eligibility. Likely multi-sprint; scope with engineering once Phase 1's routing-layer fixes have landed. *Owner: Engineering. Effort: High.*
2. **Add security headers** (CSP, X-Frame-Options, X-Content-Type-Options) sitewide — currently absent on a money-handling YMYL site. *Owner: Engineering. Effort: Low-Medium.*
3. **Backfill missing schema** (BlogPosting/AnalysisNewsArticle/QAPage) on article pages currently shipping zero structured data — confirmed to affect a meaningful share of the 110+ article-type URLs. Use generated JSON-LD examples in `findings/schema.md`. *Owner: Engineering + Content-ops. Effort: Medium.*
4. **Deduplicate third-party scripts**: remove the duplicate Microsoft Clarity and LinkedIn Insight Tag instances, lazy-load `crypto-js.min.js`, and consolidate ad-pixel loading through GTM triggers to reduce INP risk. *Owner: Marketing/Analytics + Engineering. Effort: Low-Medium.*
5. **Add an above-the-fold regulator trust badge** to the homepage hero and account/ECN page heroes — currently footer-only. *Owner: Design + Content. Effort: Low.*
6. **Fix the Organization schema address mismatch** (St. Vincent `PostalAddress` vs. London `sameAs` Google Maps link). *Owner: Engineering. Effort: Low.*
7. **Consolidate the Bonus/Promo content cluster** (11 posts → ~5-6): 301-redirect the 3 near-duplicate "50% deposit bonus" posts and the "maximize bonus credit" trio per `findings/cluster.md`. *Owner: Content/SEO. Effort: Medium.*

---

## Phase 3: Content & Authority (Month 2)

1. **Build 4 pillar/hub pages** for the highest-value content clusters (Gold/Metals, Macro/Central-Bank, MT4/MT5, Bonus/Promo) with mandatory bidirectional spoke-pillar internal linking. See `findings/cluster.md` for exact hub structure and slug groupings.
2. **Consolidate the MT4/MT5 alerts cluster** (5 posts → 2-3 posts).
3. **Add competitive differentiation to ECN/account pages**: name liquidity providers/infrastructure, add a spec-comparison table vs. 2-3 named competitors (IC Markets, Pepperstone).
4. **Standardize Organization `@type`** (Organization, not Corporation) across all pages referencing the shared `#organization` node.
5. **Fix sitemap `lastmod`** to reflect real CMS `updated_at` values instead of build-time stamping.
6. **Embed YouTube content** into educational articles with `VideoObject` schema — the brand has an active channel linked in `sameAs` but no video content embedded anywhere sampled.
7. **Add a free Moz API key** (2,500 rows/month, no cost) to unlock backlink DA/PA/spam-score/referring-domain analysis — currently a complete blind spot for toxic-link risk in a niche disproportionately targeted by affiliate/PBN schemes.
8. **Run a dedicated `/seo images` pass** for alt-text coverage and file-size optimization, not assessed in this audit.

---

## Phase 4: Monitoring & Iteration (Ongoing)

1. **Configure a Google API key** (PageSpeed Insights v5 + CrUX) or a working Lighthouse CLI to replace this audit's lab-estimate CWV figures with certified field/lab data.
2. **Implement IndexNow** given the site's active publishing cadence (dated market-analysis posts).
3. **Re-run the SXO and GEO analyses** after the SSR migration ships, to confirm it resolved the AI-crawler and Core Web Vitals impact identified in this audit.
4. **Establish a content-ops QA step** to prevent schema/authorship coverage from silently regressing on new articles — the inconsistency found in this audit (best-in-class templates existing but not consistently applied) suggests a CMS toggle/field issue rather than a template limitation.
5. **Capture a drift baseline** (`/seo drift baseline`) now that this audit is complete, to track regressions on future deploys.

---

*Full findings and evidence: `FULL-AUDIT-REPORT.md` and `findings/*.md`. Screenshots: `screenshots/`.*
