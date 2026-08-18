# Technical SEO Audit — anzocapital.com

Audited: 2026-08-17
Scope: https://anzocapital.com / https://www.anzocapital.com (Next.js SPA behind Cloudflare, YMYL forex/CFD broker)
Field-data (CrUX API) unavailable for this run — Google API credentials not configured. Core Web Vitals assessed from lab/source signals only.

## Technical SEO Score: 58 / 100

Scoring rationale: the site has strong foundations (valid sitemap, working HTTPS/HSTS, rich Organization/Article/FAQPage structured data, correct mobile viewport, clean canonical URLs) but is undermined by two Critical defects — a robots.txt/hreflang/sitemap contradiction that blocks 34% of the sitemap's declared, hreflang-linked URLs from being crawled, and a sitewide soft-404 (any invalid path returns HTTP 200) — plus a High-severity finding that **zero page content or internal links exist in the raw (non-JS) HTML for every page type tested**, which is a serious risk for any crawler/AI agent that does not execute JavaScript. Missing security headers (CSP, X-Frame-Options, X-Content-Type-Options) on a money-handling YMYL site is also High severity.

---

## 1. Crawlability

### CRITICAL — robots.txt disallows the exact locale paths that hreflang and the sitemap declare as canonical alternates
- `https://www.anzocapital.com/robots.txt`:
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
- The sitemap (`https://www.anzocapital.com/sitemap.xml`, verified 200/valid `urlset` via `sitemap_discovery.py`) contains 322 URLs: 220 `/en/*`, and 34 each for `/fr/*`, `/zh-Hans/*`, `/zh-Hant/*` — i.e. 102 URLs (32% of the sitemap) are in locales that robots.txt explicitly disallows.
- Every page checked also emits `Link: rel="alternate" hreflang="..."` headers pointing at these same disallowed locale URLs (confirmed on homepage, `/en/regulation`, `/en/legal-documents`, blog and market-analysis posts).
- Net effect: Google/Bing are told via hreflang and sitemap "these are valid alternate-language pages," but robots.txt tells crawlers not to fetch them. Google's documented behavior is to keep already-indexed disallowed URLs in the index using only referring signals (anchor text, hreflang) with no ability to read `<title>`/`<meta description>`/canonical from the page itself — producing poor, uncontrolled snippets in the zh-Hans/zh-Hant/fr markets and broken hreflang reciprocity (Google cannot confirm the alternate's own hreflang back-references because it can't crawl it).
- Fix: remove the `Disallow: /fr/`, `/zh-Hans/`, `/zh-Hant/` lines (crawling ≠ indexing — use `noindex` if those locales are intentionally not ready) or, if they are genuinely not ready for search, strip them from the sitemap and hreflang set until the disallow is lifted. Also drop the non-standard `Host:` directive — Yandex deprecated it in 2018; it has no effect on Google/Bing and adds noise.

### CRITICAL — Sitewide soft-404: invalid URLs return HTTP 200 with full "not found" page content
- Tested `https://www.anzocapital.com/en/this-page-definitely-does-not-exist-xyz123`:
  - HTTP status: **200** (verified via `curl -D -` and via rendered fetch)
  - Rendered `extracted_text` begins: *"Oops! You're Off the Map... The page you're looking for has wandered off..."* — a real custom 404 UI, but served without a 404 status code, without `<meta name="robots" content="noindex">`, and without a canonical tag.
  - No `X-Robots-Tag` header either.
- Impact: Google and Bing will treat every mistyped, deleted, or malformed URL (broken external links, old campaign URLs, typos, scraper-generated paths) as a unique 200-status page eligible for indexing, wasting crawl budget across a 220+ URL site and creating large-scale duplicate/thin-content risk (all resolving to the same "Oops" copy under different URLs). This is a common Next.js App Router pitfall when a catch-all `[...slug]` route renders the not-found UI without calling `notFound()`/setting the response status.
- Fix: ensure the catch-all/locale route calls Next.js `notFound()` (or an equivalent middleware override) so unmatched paths return a true 404 (or 410 for removed content), and add `noindex` as a defense-in-depth measure on that template.

### Info — Sitemap discovery validated
- `sitemap_discovery.py --json` against `https://anzocapital.com`: declared sitemap in robots.txt (`https://www.anzocapital.com/sitemap.xml`) resolves 200, `kind: urlset`, `valid: true`. Also independently found via the common `/sitemap.xml` path check. Other common fallback paths tested (`/sitemap_index.xml`, `/sitemap-index.xml`, `/wp-sitemap.xml`) all returned Next.js's catch-all 200 HTML page (not real sitemaps — `DOCTYPE is not allowed in sitemap XML`), consistent with the soft-404 issue above rather than genuine sitemap alternates.
- No `Disallow: /` or blanket blocks; `/en/` is explicitly allowed.

### Medium — `Disallow: /block` is vague/undocumented
- No corresponding page structure identified for `/block`; if this is a legacy or placeholder rule it should be removed to reduce robots.txt ambiguity, or documented if intentional (e.g., blocking a staging/preview path).

---

## 2. Indexability

### Pass — Canonical tags present and self-referencing on all indexable `/en/*` pages checked
- Homepage: `<link rel="canonical" href="https://www.anzocapital.com/en"/>`
- `/en/regulation`: `href="https://www.anzocapital.com/en/regulation"`
- `/en/legal-documents`: `href="https://www.anzocapital.com/en/legal-documents"`
- Blog post (`/en/blog/forex-risk-management`), market-analysis post: both self-referencing and correct.
- No `meta name="robots"` tag found on any of these pages (default index,follow) — confirmed absent via full-HTML grep, not just a truncation artifact.

### Medium — zh-Hans locale page is missing a canonical tag entirely
- `https://www.anzocapital.com/zh-Hans` full `<link rel="...">` inventory: only `stylesheet` and `preconnect` links — **no `rel="canonical"`** present anywhere in the document, unlike every `/en/*` page tested. Combined with the robots.txt disallow on this path, this locale has no indexability control of its own; if Google ever does crawl it (e.g., via an external link ignoring robots.txt semantics for discovery purposes, or before the disallow was added), it has no self-referencing signal.
- Recommend auditing whether this is systemic across all fr/zh-Hans/zh-Hant pages or isolated to the locale root.

### Medium — inconsistent x-default hreflang handling
- Homepage `Link` header includes `x-default` → `https://www.anzocapital.com/` (root, not `/en`). That root URL itself 307-redirects to `/en` (see Section 4), so x-default sends crawlers through an extra redirect hop rather than directly to the canonical English page.
- Subpages (`/en/regulation`, `/en/legal-documents`, blog/market-analysis posts) **omit `x-default` entirely** from their hreflang sets — only `en`, `zh-Hans`, `zh-Hant`, `fr` are declared. Per Google's hreflang guidelines this is technically valid (x-default is optional) but the inconsistency (present on homepage only) suggests it wasn't a deliberate site-wide decision. Recommend adding `x-default` → the `/en/...` equivalent consistently, or removing it from the homepage for consistency.

### Info — JSON-LD is delivered via Next.js RSC streaming payload, not a static parseable `<script type="application/ld+json">` block
- In the raw (unrendered) HTML, the actual JSON-LD is embedded inside a `self.__next_f.push([1,"5:[\"$\",\"script\",null,{\"type\":\"application/ld+json\",\"dangerouslySetInnerHTML\":{\"__html\":\"$19\"}}]\n"])` React Server Components hydration payload — i.e., a plain-text HTML/structured-data parser (most third-party SEO crawlers, some AI agents, quick `curl | grep` audits) will not find a valid `<script type="application/ld+json">…</script>` block to parse. It only resolves into real, extractable JSON-LD after JS execution (confirmed via Playwright-rendered fetch: 1 valid block, `Organization`/`WebSite`/`WebPage`/`ContactPoint`/`PostalAddress`/`SearchAction`/`ImageObject`/`PropertyValue`/`EntryPoint`, 3,967 bytes, valid). Googlebot and Bingbot's renderers do handle this correctly, but this is a broader crawlability risk — see Section 8.

---

## 3. Security

### High — No CSP, X-Frame-Options, or X-Content-Type-Options headers on any page, on a financial/YMYL site
- Verified via full raw response header dumps on homepage, `/en/regulation`, `/en/legal-documents`, blog and market-analysis posts (both `curl -D -` and the render tool's captured headers): headers present are `strict-transport-security` (good), `access-control-allow-*` (permissive CORS, `Access-Control-Allow-Origin: *` combined with `Access-Control-Allow-Credentials: true` — see below), `cache-control`, `vary`, `server: cloudflare`, `x-powered-by: Next.js`. **No `Content-Security-Policy`, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, or `Permissions-Policy`** headers observed anywhere.
- For a forex/CFD broker handling account login, KYC uploads and deposits, the absence of `X-Frame-Options`/frame-ancestors CSP leaves login/account pages open to clickjacking; absence of `X-Content-Type-Options: nosniff` allows MIME-sniffing attacks. This is a trust/E-E-A-T-adjacent signal as well as a direct security gap — YMYL sites are expected to demonstrate rigorous security hygiene.
- Note: `x-powered-by: Next.js` also unnecessarily discloses stack details; recommend disabling (`poweredByHeader: false` in `next.config.js`).

### Medium — Overly permissive CORS combined with credentials
- `Access-Control-Allow-Origin: *` paired with `Access-Control-Allow-Credentials: true` is set on every HTML document response (not just API routes). Browsers will actually reject the credentialed combination with a wildcard origin per spec, so this may be inert in practice, but it indicates the CORS policy was copied onto document responses rather than scoped to API endpoints — worth a security review, outside pure SEO scope but flagged given YMYL context.

### Pass — HTTPS enforced with HSTS
- `Strict-Transport-Security: max-age=31536000; includeSubDomains` present on all responses checked. HTTP→HTTPS behavior: apex `http://anzocapital.com` was not separately tested in this pass, but all HTTPS responses correctly chain to the canonical host; no mixed-content indicators found in rendered output.

---

## 4. URL Structure & Redirects

### Medium — Homepage redirect chain uses a 307 on the locale-establishing hop; should be 301
- Verified chain via `curl -D -`:
  1. `https://anzocapital.com/` → **301** → `https://www.anzocapital.com/`
  2. `https://www.anzocapital.com/` → **307** → `https://www.anzocapital.com/en`
  3. `https://www.anzocapital.com/en` → **200**
- Two redirect hops before reaching the canonical, indexable URL. The second hop (root → `/en`) is a temporary (307) redirect, which signals to search engines that the locale root should still be treated as the canonical location long-term and can slow consolidation of ranking signals onto `/en`. Since `/en` is consistently the canonical target (self-referencing canonical on `/en` confirms this), this hop should be a permanent 301.
- Also increases latency for first-time/cold visits (2 extra round trips before the SPA shell even begins loading), compounding the CWV risk noted in Section 6.

### Pass — Clean, descriptive URL patterns
- Locale-prefixed, human-readable slugs throughout: `/en/blog/forex-risk-management`, `/en/market-analysis/eur-usd-nfp-trade-setup-market-profile-levels-20260810`, `/en/help-center/choose-platform`, `/en/regulation`, `/en/legal-documents`. No query-string pagination artifacts or session IDs observed in sitemap URLs. Market-analysis slugs embed a `YYYYMMDD` suffix, which is fine but means the human-readable portion of the slug is duplicated across dated re-analyses of the same pair (e.g. repeated `eur-usd-...` roots) — acceptable pattern, not an issue.

---

## 5. Mobile-Friendliness

### Pass — Correct responsive viewport, no scaling lock
- `<meta name="viewport" content="width=device-width, initial-scale=1"/>` present and consistent across all pages checked (homepage, regulation, legal-documents, blog, market-analysis, help-center). No `maximum-scale` or `user-scalable=no` restriction, which is good for accessibility/zoom.
- Single responsive CSS bundle (`/_next/static/css/57fc3f66bdea92b6.css`) shared across templates rather than separate mobile/desktop markup — consistent with a standard responsive Next.js build. Touch-target sizing and tap-spacing could not be fully verified without a live-rendered visual/accessibility-tree pass (the `accessibility_tree` field returned `null` in this run); recommend a follow-up Lighthouse mobile run if not already covered elsewhere in this audit.

---

## 6. Core Web Vitals (source/lab inspection — no CrUX field data available this run)

### Medium — LCP risk: fully client-rendered hero with no server-rendered content to paint against
- Raw (non-JS) HTML for every template tested contains **no body content at all** beyond the `<title>` tag (see Section 8 for full detail — homepage raw text = 47 chars, all of it just the title). The visible hero ("Elevate Your Trades", stat callouts, imagery) only exists after Playwright-rendered execution (2.0–2.8s `render_ms` observed across homepage/blog/market-analysis fetches in this tooling, which is a proxy for hydration cost, not a substitute for real-user LCP but directionally consistent with a render-blocked LCP path).
- Because there is no server-rendered/streamed HTML fallback for the hero content itself, LCP is gated behind JS parse + hydrate + data-fetch on every page, for every visit (compounded by `cache-control: private, no-cache, no-store, max-age=0, must-revalidate` on the HTML document itself — see below). This is a classic CSR-without-SSR-content LCP risk pattern; actual LCP timing should be confirmed with a real Lighthouse/PageSpeed Insights run once CrUX/PSI API access is available.

### Medium — `Cache-Control: private, no-cache, no-store, max-age=0, must-revalidate` on the HTML document
- Confirmed on every page tested (homepage, regulation, legal-documents, blog, market-analysis, help-center) — identical header value site-wide, including on evergreen content like `/en/legal-documents` and older blog posts that don't need per-request freshness.
- This forces the browser (and any CDN edge, despite Cloudflare fronting — `cf-cache-status: DYNAMIC` confirms Cloudflare is NOT caching the HTML) to fully re-fetch and re-validate the document on every navigation, including back/forward and repeat visits, which increases repeat-visit LCP and TTFB. For an account/session-bearing page (e.g., logged-in dashboard) `no-store` is appropriate; for static marketing/legal/editorial content it is unnecessarily aggressive and should at minimum allow `private, max-age=0, must-revalidate` (drop `no-store`, allow conditional GET/304s) or, better, serve marketing/blog/help-center pages with public, revalidatable caching (e.g., `s-maxage`) so Cloudflare can actually cache them at the edge.

### Info — CLS/INP not directly assessable from source without live interaction tracing
- No obvious CLS red flags in source (no unsized `<img>` without dimensions detected in the truncated samples reviewed; full image-dimension audit not performed for every asset). No long synchronous inline scripts blocking the main thread were flagged in `console_errors`/`render_diagnostics` (both empty across all renders). Recommend a live PSI/Lighthouse pass once available for authoritative LCP/INP/CLS numbers — this section is directional only.

---

## 7. Structured Data

### Pass — Homepage: valid, rich Organization/WebSite schema
- 1 JSON-LD block, valid, 3,967 bytes, types: `Organization`, `WebSite`, `WebPage`, `PostalAddress`, `ContactPoint`, `SearchAction`, `ImageObject`, `PropertyValue`, `EntryPoint`. Good foundation for brand entity and sitelinks search box eligibility.

### Pass — Blog posts carry BlogPosting + FAQPage + BreadcrumbList
- `/en/blog/forex-risk-management`: valid JSON-LD, types `BlogPosting`, `FAQPage`, `Question`, `Answer`, `BreadcrumbList`, `ListItem`, `Person`, `Organization`, `WebPage`, `ImageObject`. Strong markup for rich-result eligibility (article rich results, FAQ rich results, breadcrumb trail in SERP).

### Medium — Market-analysis template: valid but includes a generic/untyped `Thing` node
- `/en/market-analysis/eur-usd-nfp-trade-setup-market-profile-levels-20260810`: valid JSON-LD (2,575 bytes), types `AnalysisNewsArticle` (a legitimate schema.org `NewsArticle` subtype — appropriate for dated trade-setup analysis), `BreadcrumbList`, `ListItem`, `Organization`, `Person`, `ImageObject`, `SpeakableSpecification`, plus a bare **`Thing`** type. A generic `Thing` typically indicates a nested property (e.g., `about`, `mentions`, or a mis-typed sub-entity) that wasn't given a specific schema.org type — worth checking in Rich Results Test to confirm it isn't suppressing eligibility for a more specific rich result (e.g., if it's meant to be a `FinancialProduct`/`MonetaryAmount` for the currency pair being discussed).

### High — Help-center articles have zero structured data
- `/en/help-center/choose-platform`: `structured_data.block_count: 0` — confirmed no JSON-LD present at all (rendered check). Help-center content is naturally FAQ/HowTo-shaped ("Which Platform Should I Choose?"); with 60+ help-center articles in the sitemap, this is a sitewide missed opportunity for `FAQPage`/`HowTo`/`Article` rich results across an entire content pillar, and inconsistent with the blog template (which does implement FAQPage). Recommend applying the same structured-data component used on `/en/blog/*` to the `/en/help-center/*` template.

---

## 8. JavaScript Rendering (SPA / CSR risk)

### CRITICAL — Zero body content and zero `<a href>` links present in raw (non-JS-executed) HTML, sitewide
- Directly measured by stripping all tags/scripts/styles from the **raw HTTP response** (`curl`, no JS execution) and counting remaining visible text, across every template tested:

  | Page | Raw-HTML visible text length | Content |
  |---|---|---|
  | Homepage (`/en`) | 47 chars | Title only |
  | Blog post | 52 chars | Title only |
  | Market-analysis post | 54 chars | Title only |
  | `/en/regulation` | 57 chars | Title only |
  | `/en/legal-documents` | 59 chars | Title only |

  In every case the only text surviving tag-stripping is the `<title>` element — hero copy, article bodies, regulation/legal disclosures, navigation, and footer are **entirely absent** from the document a non-JS-executing fetch receives. `render_page.py --mode auto` correctly detects this and flags `is_spa: true`, escalating to a Playwright render; the rendered `extracted_text` then shows full content (e.g., homepage hero stats, full blog/market-analysis body copy).
- `<a href>` count in raw homepage HTML: **0**. There is no server-rendered link graph at all — a crawler that does not execute JavaScript cannot discover a single internal link from the homepage (or any other page tested), and can only find URLs via the XML sitemap.
- Impact: Googlebot and modern Bingbot do execute JS and will see the full rendered content (confirmed structured data and text extraction succeed under `--mode always`), so primary search indexing is likely functioning correctly today (fast render, ~1.9–2.8s, no console errors). However this is a **significant risk surface**, not just theoretical:
  - AI/agentic crawlers that this skill's own guidance tracks (GPTBot, ClaudeBot, PerplexityBot, CCBot, and most link-preview/social-card bots) generally do **not** execute JavaScript and will see a blank page + title only — meaning this YMYL broker's regulation/legal/trust content, blog, and market analysis are effectively invisible to AI answer engines and citation-based discovery, directly undermining AI-search visibility for a site that otherwise has the structured data and content depth to be citable.
  - Any regression in Googlebot's rendering budget/queue (rendering is a second, resource-constrained pass in Google's pipeline, distinct from crawling) delays indexing of new/updated content — this is a real, documented risk for CSR-only sites at scale (200+ URLs, dozens of new blog/market-analysis posts).
  - No `<noscript>` fallback content was found on any page as a safety net.
- Recommend: given the stack is already Next.js, migrate key money/trust/content pages (homepage, `/en/regulation`, `/en/legal-documents`, blog, market-analysis, help-center — i.e., everything except authenticated app/account screens) to server-side rendering or static generation so the initial HTML response contains real content and real `<a href>` links, with client-side hydration layered on top for interactivity. This is the single highest-leverage technical fix available on this site.

---

## 9. IndexNow Protocol

### Info — No evidence of IndexNow implementation found
- No dedicated IndexNow key-verification file was found at a distinct path; `/indexnow.txt` returns the site's generic SPA catch-all response (HTTP 200, `<html lang="indexnow.txt">` — the router is treating "indexnow.txt" as a dynamic locale-segment parameter, which is itself a byproduct of the soft-404 issue in Section 1) rather than a real IndexNow key file. No `indexnow` references found in checked response headers or HTML.
- With 322 sitemap URLs across 4 locales and an active blog/market-analysis cadence (dated posts as recent as 2026-08-11 seen in this run), IndexNow would let the site push Bing/Yandex/Naver near-real-time notification of new/updated market-analysis content instead of waiting on crawl scheduling — worth implementing given the site already has a sitemap and clear publish cadence to key off of.

---

## Prioritized Recommendations

| Priority | Issue | Section |
|---|---|---|
| Critical | Fix robots.txt Disallow on /fr/, /zh-Hans/, /zh-Hant/ contradicting sitemap + hreflang | 1 |
| Critical | Fix soft-404: unmatched routes must return real HTTP 404 (call Next.js `notFound()`) | 1 |
| Critical | Add SSR/SSG so real content + `<a href>` links exist in raw HTML (currently title-only) | 8 |
| High | Add CSP, X-Frame-Options, X-Content-Type-Options headers (YMYL clickjacking/MIME risk) | 3 |
| High | Add structured data (FAQPage/HowTo) to /en/help-center/* template (60+ pages, currently 0) | 7 |
| Medium | Change root→/en redirect from 307 to 301 | 4 |
| Medium | Loosen `no-store` cache-control on static marketing/legal/blog pages; allow edge caching | 6 |
| Medium | Add canonical tag to zh-Hans (and audit fr/zh-Hant) locale pages | 2 |
| Medium | Standardize x-default hreflang presence/target across all templates | 2 |
| Medium | Investigate generic `Thing` type in market-analysis JSON-LD | 7 |
| Medium | Remove/document vague `Disallow: /block` rule; drop deprecated `Host:` directive | 1 |
| Low | Disable `x-powered-by: Next.js` header disclosure | 3 |
| Info | Implement IndexNow for Bing/Yandex/Naver given active publishing cadence | 9 |

---

## Evidence Sources
- `sitemap_discovery.py --json` output against `https://anzocapital.com`
- `render_page.py --mode auto/always/never --json` against: `/en` (home), `/en/blog/forex-risk-management`, `/en/market-analysis/eur-usd-nfp-trade-setup-market-profile-levels-20260810`, `/en/help-center/choose-platform`, `/en/this-page-definitely-does-not-exist-xyz123`
- Direct `curl -s -D -` header/HTML captures for: `https://anzocapital.com/` (redirect chain), `https://www.anzocapital.com/robots.txt`, `https://anzocapital.com/robots.txt`, `https://www.anzocapital.com/sitemap.xml`, `/en/regulation`, `/en/legal-documents`, `/zh-Hans`, `/fr`, `/indexnow.txt`
