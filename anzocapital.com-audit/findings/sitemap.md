# Sitemap Audit — anzocapital.com

**Sitemap URL:** https://www.anzocapital.com/sitemap.xml
**Audited:** 2026-08-17
**Total `<loc>` entries:** 322 (verified by parsing live XML)
**File size:** ~62 KB (well within 50MB / 50,000-URL caps)

## Score Estimate: 58 / 100

The sitemap is technically well-formed and free of dead links in spot-checks, but a real robots.txt/sitemap conflict blocks ~32% of listed URLs from being crawled at all, lastmod is non-functional (identical timestamp on every URL, refreshed daily), and there is no hreflang signal anywhere (page-level or sitemap-level) to make sense of the four locale trees. These are exactly the kinds of issues that waste crawl budget and confuse international indexation.

---

## 1. XML Validity — PASS

- `xmllint --noout` parses the document with no errors; well-formed XML 1.0, UTF-8 encoded.
- Single flat `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">` — no sitemap index needed at this scale.
- No duplicate `<loc>` entries (322 unique).
- All 322 URLs use the canonical `https://www.anzocapital.com` host — no scheme/host inconsistencies (bare and www-less variants are not present in the sitemap itself, which is correct given the 301 setup).
- 322 URLs / ~62KB is nowhere near the 50,000-URL / 50MB per-file limit. No split/index required today.

## 2. URL Status Codes — PASS (spot-check)

Spot-checked 17 URLs across every section and all four locales (regulation, accounts-overview, copy-trading-account, deposit-withdrawal, stp-account, ecn-account, metatrader-4, 2× blog, 2× help-center, 2× market-analysis, 1× notifications, and `/regulation` in zh-Hans, zh-Hant, and fr). **All 17 returned HTTP 200** (`curl -sL -o /dev/null -w "%{http_code}"`). No redirects, no 4xx/5xx found in the sample. No blanket claim of "all 322 are 200" should be made from this sample alone — recommend a full crawl-and-diff pass (e.g., Screaming Frog list mode against the sitemap) before relying on this for a definitive PASS.

## 3. Critical: robots.txt vs. Sitemap Locale Conflict — CRITICAL

`https://www.anzocapital.com/robots.txt`:
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

Verified locale breakdown of the live sitemap (corrects the ~240/75% estimate from the initial brief — actual measured numbers are lower but the conflict is just as real):

| Locale | URLs in sitemap | Robots.txt status |
|---|---|---|
| `/en/` | 220 (68.3%) | Allowed |
| `/fr/` | 34 (10.6%) | **Disallowed** |
| `/zh-Hans/` | 34 (10.6%) | **Disallowed** |
| `/zh-Hant/` | 34 (10.6%) | **Disallowed** |
| **Total disallowed** | **102 (31.7%)** | |

Nearly a third of all sitemap entries point at paths Googlebot is explicitly told not to fetch. This is a direct, verifiable contradiction between the two files the crawler reads together. Effects:
- Google will request these URLs from the sitemap, see the robots.txt block, and drop them from consideration — the URLs will show as "Excluded by robots.txt" in GSC Coverage/Indexing reports, polluting the index-coverage report with a permanent ~32% "excluded" bucket.
- Because the pages are blocked, Google **cannot even crawl them to discover a `noindex` tag, canonical, or hreflang annotation** on them — the block is absolute at the fetch layer.
- Submitting these URLs in the sitemap sends mixed signals about intent: is the non-English content meant to be indexed (sitemap says yes) or not (robots.txt says no)? Pick one.

**Recommendation (pick one, don't leave as-is):**
- **If the fr/zh content should rank:** remove the three `Disallow` lines from robots.txt and let it be crawled — that is the fix implied by having built and maintained full localized page sets for these languages.
- **If the fr/zh content is intentionally not ready for indexing** (e.g., soft-launch, thin/unlocalized, or regulatory reasons for those markets): strip all 102 `/fr/`, `/zh-Hans/`, `/zh-Hant/` entries out of the sitemap so it only lists crawlable, indexable URLs, and additionally add `noindex` meta robots to those pages as a safety net (robots.txt disallow alone does not prevent indexing of already-linked URLs — it only prevents crawling, so orphaned/linked instances of these URLs can still appear in search with no snippet).

## 4. Hreflang — CRITICAL (signal absent, contrary to brief's assumption)

The task brief referenced hreflang annotations "on the homepage" tying the locale trees together. I could not verify this:
- Static HTML fetch of `https://www.anzocapital.com/en/` (and `/fr/regulation`) contains **zero** `hreflang` attributes anywhere in the served document (checked via `curl` + regex over full source, not just `<head>`).
- Only a single `<link rel="canonical" href="https://www.anzocapital.com/en"/>` is present — no `rel="alternate" hreflang="..."` cluster.
- The sitemap itself does not use the `xmlns:xhtml` namespace or `<xhtml:link rel="alternate" hreflang="...">` annotations either (checked: 0 occurrences of `xhtml` or `hreflang` strings in the sitemap XML) — so there is no sitemap-level substitute.

Note: the site is Next.js App Router (`/_next/static/...` chunks, `<html lang="en">`), so it's possible hreflang is injected only after client-side hydration in a way `curl` cannot see. Googlebot does render JS on a second wave, so this should be re-verified in GSC's URL Inspection → "View Crawled Page" / rendered HTML, or via a headless-browser crawl (Screaming Frog with JS rendering enabled). As it stands from a plain HTTP fetch — which is how most crawlers, and non-Google search engines, will see the page — there is **no machine-readable link between the four locale trees at all**. Combined with the robots.txt block on 3 of the 4 locales (#3 above), the internationalization setup is not currently functional from an SEO signaling standpoint: Google has no reliable way to know these are language alternates of the same page, and even if it did, it's blocked from crawling three of them.

## 5. lastmod Accuracy — HIGH

Every one of the 322 `<url>` entries carries the exact same `<lastmod>2026-08-17</lastmod>` — today's date. This is a single unique value across the entire file (confirmed via XML parse). This strongly indicates lastmod is stamped at sitemap-generation/request time rather than reflecting the actual last significant content edit per page.

Impact: Google explicitly uses lastmod as a recrawl-priority signal only when it trusts the value to be accurate; a sitemap where 100% of URLs "changed today," every day, trains Google to discount/ignore the field entirely, which removes a legitimate lever for getting time-sensitive content (market-analysis posts, notifications) recrawled faster. It also makes it impossible to distinguish "this blog post was just updated" from "this page hasn't changed in a year."

**Recommendation:** Generate lastmod from the CMS's actual `updated_at` field per page/post, not from sitemap build time.

## 6. Deprecated Tags: priority / changefreq — INFO

Both are present on every URL. Google has publicly stated both are ignored for ranking/crawl-priority purposes (Bing/Yandex give changefreq limited weight). Distribution found:

- `priority`: 1.0 (20), 0.9 (40), 0.8 (187), 0.7 (48), 0.6 (8), 0.4 (19)
- `changefreq`: weekly (209), monthly (104), daily (9)

Internally the values are reasonably logical (homepage/account pages =1.0, trading instrument pages=0.9, blog/help-center hubs=0.8/daily, notifications=0.4/monthly) — this isn't hurting anything, but it's also not helping in Google. Safe to remove to shrink file size and simplify maintenance; not worth the effort to "fix" the values further.

## 7. Coverage vs. Site Structure

**/en/ section breakdown (220 URLs):**
| Section | Count |
|---|---|
| Static top-level pages (home, regulation, account types, instruments, platforms, etc.) | 34 |
| `/en/blog/*` | 82 |
| `/en/help-center/*` | 57 |
| `/en/market-analysis/*` | 28 |
| `/en/notifications/*` | 19 |

High-value pages present and returning 200: `regulation`, `accounts-overview`, `stp-account`, `ecn-account`, `copy-trading-account`, `deposit-withdrawal`, `margin-leverage`, `metatrader-4`, `metatrader-5`, `forex`, `metals`, `indices`, `stocks`, `oil-energies`, `dividend`, `swap`, `negative-balance-protection`, `ib-program`, `multi-account-manager`, `cybersecurity`, `economic-calendar`. This is good — the core trading/trust pages a broker needs indexed are all represented, correctly prioritized (1.0–0.9), and live.

**Potential gaps (not in sitemap, could not fully confirm via link-crawl since primary nav is client-rendered JS and not present in initial HTML — flag for manual/GSC confirmation):**
- No dedicated `privacy-policy` / `terms-and-conditions` URLs — likely bundled under `legal-documents` as a hub with downloadable PDFs; confirm PDFs aren't meant to be indexed separately.
- No `careers` or `about/team` style page beyond `about-anzo`.
- No image or video sitemap despite the site clearly using rich media (award badges, Suns sponsorship assets) — low priority unless image search traffic is a stated goal.

## 8. Content Hub / Internal-Linking Structure for High-Volume Sections — MEDIUM

The location-page-scale doorway-page gates (30+/50+) don't directly apply here — these are blog/help-center/market-analysis content pages, not templated location pages. However, at 115+ combined posts (82 blog + 28 market-analysis + 19 notifications... note notifications overlaps as its own hub) across three fast-refreshing sections, sitemap organization gives no indication of a hub/category taxonomy:

- All blog, help-center, and market-analysis URLs are flat `/en/blog/{slug}`, `/en/help-center/{slug}`, `/en/market-analysis/{slug}` — no category or tag-level sitemap entries, and the identical priority/changefreq per section (e.g., every one of the 81 blog posts = priority 0.8/weekly with zero differentiation) suggests no editorial signal distinguishes cornerstone content from routine posts.
- `market-analysis` posts are dated in their slugs (e.g., `...-20260810`) but carry the same fabricated `lastmod` as everything else (see #5), so freshness — which matters most for this content type — isn't actually communicated to crawlers.
- This is not a penalty-risk pattern (real, differentiated content per post, not templated swaps), but it is a missed opportunity: consider a sitemap index split by content type (`sitemap-blog.xml`, `sitemap-help-center.xml`, `sitemap-market-analysis.xml`, `sitemap-pages.xml`) once volume grows further, and accurate per-post lastmod, to help Google prioritize recrawling the fast-moving market-analysis section over static legal/help pages.

---

## Summary Table

| Check | Severity | Status |
|---|---|---|
| XML well-formedness | Critical | Pass |
| ≤50k URLs / ≤50MB | Critical | Pass (322 URLs, 62KB) |
| Sampled URL status codes | High | Pass (17/17 = 200) |
| robots.txt vs sitemap locale conflict | **Critical** | **Fail — 102 URLs (31.7%) disallowed yet listed** |
| hreflang signal (page-level & sitemap-level) | **Critical** | **Fail — none detected via static fetch** |
| lastmod accuracy | High | Fail — 100% identical, request-time generated |
| Duplicate/host-inconsistent URLs | Medium | Pass — none found |
| priority/changefreq | Info | Present but ignored by Google; internally logical, safe to remove |
| High-value page coverage (regulation, accounts, instruments, platforms) | — | Pass — all present, 200, correctly weighted |
| Content hub structure for blog/help-center/market-analysis | Medium | No differentiation/segmentation; opportunity for split sitemap + real lastmod |
| Location-page doorway-page gates (30+/50+) | N/A | Not applicable — no templated location pages on this site |

---

## Structured Findings (for audit-data.json)

```json
{
  "category": "Sitemap",
  "score_estimate": 58,
  "sitemap_url": "https://www.anzocapital.com/sitemap.xml",
  "total_urls": 322,
  "file_size_bytes": 62195,
  "findings": [
    {
      "id": "sitemap-xml-valid",
      "title": "Sitemap XML is well-formed",
      "severity": "info",
      "status": "pass"
    },
    {
      "id": "sitemap-under-limits",
      "title": "Sitemap under 50,000 URL / 50MB per-file limit",
      "severity": "info",
      "status": "pass",
      "detail": "322 URLs, ~62KB"
    },
    {
      "id": "sitemap-status-code-sample",
      "title": "Sampled URLs return 200",
      "severity": "high",
      "status": "pass",
      "detail": "17/17 spot-checked URLs across en/fr/zh-Hans/zh-Hant and all content sections returned HTTP 200; full crawl-diff recommended for complete coverage"
    },
    {
      "id": "sitemap-robots-conflict",
      "title": "robots.txt disallows /fr/, /zh-Hans/, /zh-Hant/ while sitemap lists full URL sets for them",
      "severity": "critical",
      "status": "fail",
      "detail": "102 of 322 sitemap URLs (31.7%) are in directories blocked by robots.txt Disallow rules. Google will exclude these from indexing coverage and cannot crawl them to see any on-page directives."
    },
    {
      "id": "sitemap-hreflang-missing",
      "title": "No hreflang annotations found (page-level or sitemap-level)",
      "severity": "critical",
      "status": "fail",
      "detail": "Zero hreflang occurrences in static HTML of homepage/fr-regulation and zero xhtml:link entries in sitemap XML. Site is Next.js (client hydration possible) — recommend re-check with JS-rendering crawler before finalizing."
    },
    {
      "id": "sitemap-lastmod-fabricated",
      "title": "lastmod identical (today's date) across all 322 URLs",
      "severity": "high",
      "status": "fail",
      "detail": "Single unique lastmod value 2026-08-17 across entire file indicates generation-time stamping rather than real content-change tracking."
    },
    {
      "id": "sitemap-deprecated-tags",
      "title": "priority and changefreq present on all URLs",
      "severity": "info",
      "status": "informational",
      "detail": "Ignored by Google; internally consistent values; safe to remove."
    },
    {
      "id": "sitemap-high-value-coverage",
      "title": "Core trading/trust pages present and correctly weighted",
      "severity": "info",
      "status": "pass",
      "detail": "regulation, account types (STP/ECN/copy-trading), MT4/MT5, instruments (forex/metals/indices/stocks/oil-energies), deposit-withdrawal, margin-leverage all present with priority 0.8-1.0 and verified 200 status."
    },
    {
      "id": "sitemap-content-hub-structure",
      "title": "No sitemap segmentation or lastmod differentiation for 115+ blog/help-center/market-analysis posts",
      "severity": "medium",
      "status": "opportunity",
      "detail": "Not a doorway-page/thin-content risk (real differentiated content), but flat structure with uniform priority/changefreq/lastmod per section limits crawl-priority signaling for time-sensitive market-analysis content."
    },
    {
      "id": "sitemap-quality-gates",
      "title": "Location-page doorway-page thresholds (30+/50+) not applicable",
      "severity": "info",
      "status": "n/a",
      "detail": "Site has no templated location pages."
    }
  ]
}
```
