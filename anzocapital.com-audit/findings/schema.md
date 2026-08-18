# Schema.org Structured Data Audit — anzocapital.com
Audit date: 2026-08-17 | Rendered site: https://www.anzocapital.com/en

## Summary Score: 60 / 100

Breadth of implementation is genuinely strong for a broker site (Organization, WebSite, BlogPosting,
NewsArticle subtype, FinancialProduct, FinancialService, BreadcrumbList, AboutPage, Corporation are all
present and mostly well-formed). The score is held down by three systemic issues: (1) inconsistent
coverage — many individual blog/market-analysis/help-center articles ship **zero** JSON-LD while
sibling pages of the same template have full schema, (2) a factual mismatch between the Organization's
declared `PostalAddress` and the location referenced by its own `sameAs` Google Maps entry (material for
a regulated financial entity), and (3) inconsistent `@type` modeling of the same `@id` node
(`Organization` on some pages, `Corporation` on others) and heavy reliance on `FAQPage`, which no longer
has any Google SERP benefit (retired for all sites May 7, 2026).

---

## 1. Detection Results (by page/template)

| Page | Types found | Bytes | Valid JSON |
|---|---|---|---|
| Homepage `/en` | WebPage, WebSite+SearchAction, Organization, PostalAddress, ContactPoint(×3), ImageObject, PropertyValue | 3,967 | Yes |
| Blog post `/en/blog/forex-risk-management` | BlogPosting, Person(author), Organization(publisher), ImageObject, BreadcrumbList, FAQPage | 4,884 | Yes |
| Blog post `/en/blog/margin-call-guide` | **None found** (0 blocks, confirmed with `--mode always`) | 0 | N/A |
| Market analysis `/en/market-analysis/gold-forecast-ahead-of-us-cpi-20260713` | **None found** (0 blocks, confirmed with `--mode always`) | 0 | N/A |
| Market analysis `/en/market-analysis/eur-usd-nfp-trade-setup-market-profile-levels-20260810` | AnalysisNewsArticle (valid NewsArticle subtype), Person, BreadcrumbList, SpeakableSpecification, ImageObject | 2,575 | Yes |
| `/en/regulation` | AboutPage, Corporation, PostalAddress, FinancialService, PropertyValue, FAQPage, BreadcrumbList | 5,668 | Yes |
| `/en/about-anzo` | AboutPage, Corporation, PostalAddress, ImageObject, BreadcrumbList | 3,117 | Yes |
| `/en/help-center` (listing) | CollectionPage, DefinedTermSet/DefinedTerm, Corporation, PostalAddress, WebSite+SearchAction, BreadcrumbList | 3,430 | Yes |
| `/en/help-center/account-types` (article) | **None found** | 0 | N/A |
| `/en/ecn-account`, `/en/stp-account`, `/en/accounts-overview` | WebPage, FinancialProduct, Offer, PropertyValue(×11), FAQPage, BreadcrumbList, Corporation | 5,600–8,047 | Yes |

No Microdata or RDFa detected anywhere; site is 100% JSON-LD, correctly using `https://schema.org` (not http) and absolute URLs throughout — good baseline hygiene.

Sitemap volumes for context: 81 `/en/blog/*` URLs, 28 `/en/market-analysis/*` URLs, and a large `/en/help-center/*` article set — meaning the "zero schema" pattern found on 3 of 3 spot-checked article-level pages likely represents a substantial fraction of total indexed content, not an isolated bug.

## 2. Validation Results

### Homepage Organization block — mostly valid, one High-severity data-integrity issue
- ✅ `@context` = https://schema.org, `@type` = Organization, `logo` (ImageObject), `sameAs` (7 links: Maps, LinkedIn, Instagram, Facebook, YouTube, Telegram, X)
- ✅ `identifier`/PropertyValue carries registration number "308 LLC 2020"; `legalName` "Anzo Capital (SVG) LLC" present — good for E-E-A-T on a regulated entity
- ⚠️ **High — Address/sameAs mismatch**: `address.PostalAddress` = "Euro House, Richmond Hill Road, Kingstown, VC, PO Box 2897" (a Saint Vincent & the Grenadines registered-agent/virtual-office address), but the first `sameAs` entry is a Google Maps place link resolving to **51.5158°N, -0.0817°W — central London**, a different city and country from the declared PostalAddress. For a financial services Organization node, Google/LLMs consuming this graph will see two conflicting locations for the same `@id`. Recommend either (a) adding the London office as a second registered `location`/`department`, or (b) removing the mismatched Maps link from `sameAs` if it does not represent the legal entity.
- ⚠️ Medium — `contactType` values are all `"customer support"`; Google's recognized ContactPoint values include `"customer service"`, `"technical support"`, `"sales"`, etc. `"customer support"` is not one of the enumerated values Google's documentation lists, so switch to `"customer service"`.
- ℹ️ Low — `logo.ImageObject` is 172×32 (5.4:1 wordmark). Not a hard requirement for the JSON-LD logo property, but Google's Organization logo guidance favors a roughly square mark (≥112×112) for Knowledge Panel use; consider adding a square icon variant.
- ℹ️ Low — `PostalAddress` mixes `streetAddress` and `postOfficeBoxNumber` simultaneously; harmless syntactically but reads as a formulaic offshore-registration address rather than an operational office, which is a trust-signal (not schema-syntax) concern worth flagging to the business/legal team given YMYL scrutiny of forex brokers.

### Entity `@type` inconsistency across pages — Medium severity
The same node `@id: "https://www.anzocapital.com/en/#organization"` is typed **`Organization`** on the homepage but **`Corporation`** on `/en/regulation`, `/en/about-anzo`, `/en/help-center`, `/en/ecn-account`, `/en/stp-account`. Both are valid schema.org types (`Corporation` is a subtype of `Organization`), so nothing is broken, but mixing types for one canonical `@id` across a site is bad practice for entity consolidation in Google's Knowledge Graph and is easy to standardize.

### FAQPage usage — Info severity, not a defect but flag per policy
`FAQPage` blocks appear on the homepage-adjacent template family: blog posts, `/en/regulation`, `/en/ecn-account`, `/en/stp-account`, `/en/accounts-overview`. Per current policy, Google retired FAQ rich results for all sites (May 7, 2026), so these blocks now carry **no Google SERP benefit**. They are syntactically valid (Question/Answer pairs are well-formed) and pose no error risk, so leaving them is low-priority cleanup — flag as Info, not something requiring urgent removal. Any AI/answer-engine visibility value from this markup is unconfirmed.

### FinancialProduct blocks (ECN/STP/accounts-overview) — mostly valid, two minor type issues
- ✅ Correct, current schema.org type (`FinancialProduct` is not deprecated); rich `additionalProperty`/PropertyValue set (leverage, min deposit, lot size, margin call %, stop-out %, commission) is a genuinely good, detailed implementation.
- ⚠️ Medium — `feesAndCommissionsSpecification` is schema.org-typed as **URL**, but is populated with free text ("Transparent fixed commission per lot. No hidden fees."). Should either point to a URL with the fee schedule, or this property should be dropped in favor of the existing `PropertyValue: "Commission"` field, which is a text-safe container.
- ℹ️ Low — nested `Offer` has only a `description` string; no `price`/`priceCurrency`. Not required for validity and FinancialProduct isn't Google-rich-result-eligible, but adding structured `price`/`priceCurrency` (e.g., minimum deposit as price) would make the Offer machine-readable rather than just descriptive text.

### BlogPosting (`forex-risk-management`) — Passes validation
All required/recommended properties present: `headline`, `author` (Person + url), `datePublished`/`dateModified` (ISO 8601, correct), `image` (ImageObject), `publisher` with `logo`, `mainEntityOfPage`, `articleSection`. This is the implementation standard the rest of the blog/market-analysis templates should be brought up to.

### Zero-schema pages — Critical severity (coverage gap)
Spot-checked and confirmed with both `--mode auto` and `--mode always` (ruling out an SPA-hydration/render-timing false negative):
- `/en/blog/margin-call-guide` — no JSON-LD at all, despite `/en/blog/forex-risk-management` having full BlogPosting+BreadcrumbList+FAQPage.
- `/en/market-analysis/gold-forecast-ahead-of-us-cpi-20260713` — no JSON-LD at all, despite `/en/market-analysis/eur-usd-nfp-trade-setup-market-profile-levels-20260810` having full AnalysisNewsArticle+BreadcrumbList.
- `/en/help-center/account-types` — no JSON-LD at all; the `/en/help-center` listing page has CollectionPage/DefinedTermSet, but the article template itself appears to ship no schema.

This indicates the schema-injection logic is likely tied to a CMS field (e.g., a "structured data" toggle or a template variant) that isn't populated/enabled for all entries, rather than a systemic template bug — worth an engineering investigation into why coverage is inconsistent across otherwise-identical templates.

## 3. Missing Opportunities

1. **Help-center articles: QAPage** (not FAQPage). These are genuine single-question user-support pages, which is exactly the use case schema.org's `QAPage` was designed for (as opposed to `FAQPage`, intended for a page hosting several distinct topic FAQs). Since FAQPage no longer has SERP value anyway, don't backport FAQPage to help-center — go straight to QAPage as the semantically correct type, understanding there is no confirmed Google rich-result for QAPage either at present, but it is the correct machine-readable structure per schema.org guidance and may carry AI/GEO value.
2. **Article/NewsArticle-family schema parity** for all blog and market-analysis posts — extend the existing well-formed `BlogPosting`/`AnalysisNewsArticle` templates to the currently-blank posts.
3. **BreadcrumbList on help-center articles** — present on blog/market-analysis/account pages but absent on the sampled help-center article, despite the deep `/help-center/<slug>` URL structure being the best fit for breadcrumbs on the site.
4. Consolidate the Organization `@id` to a single consistent `@type` across all pages.
5. Fix the PostalAddress vs sameAs Google Maps location mismatch.

## 4. Generated JSON-LD Recommendations

### 4a. QAPage for help-center articles (e.g., `/en/help-center/account-types`)
```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "QAPage",
      "@id": "https://www.anzocapital.com/en/help-center/account-types#qapage",
      "url": "https://www.anzocapital.com/en/help-center/account-types",
      "name": "What account types does Anzo Capital offer?",
      "inLanguage": "en",
      "dateModified": "2026-08-17",
      "mainEntity": {
        "@type": "Question",
        "name": "What account types does Anzo Capital offer?",
        "text": "An overview of the ECN and STP live trading account types available at Anzo Capital.",
        "answerCount": 1,
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Anzo Capital offers two live account types: the ECN Account, which connects traders directly to liquidity providers with raw spreads from 0.0 pips plus a fixed commission per lot, and the STP Account, which routes orders straight to liquidity providers with no additional commission. Both support MT4 and MT5, a minimum deposit of USD 10, and leverage up to 1:1000.",
          "url": "https://www.anzocapital.com/en/help-center/account-types",
          "author": {
            "@type": "Organization",
            "name": "Anzo Capital"
          }
        }
      }
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.anzocapital.com/en" },
        { "@type": "ListItem", "position": 2, "name": "Help Center", "item": "https://www.anzocapital.com/en/help-center" },
        { "@type": "ListItem", "position": 3, "name": "Account Types", "item": "https://www.anzocapital.com/en/help-center/account-types" }
      ]
    }
  ]
}
```
Replace the placeholder answer text with the article's actual on-page copy per URL when templatizing; do not use HowTo for step-based help articles (deprecated Sept 2023) even where content reads as a how-to guide.

### 4b. NewsArticle/BlogPosting parity fix — apply the site's own working template to blank posts
Example for `/en/market-analysis/gold-forecast-ahead-of-us-cpi-20260713`, mirroring the structure already live and valid on the `eur-usd-nfp...` post:
```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "AnalysisNewsArticle",
      "headline": "Gold Forecast Ahead of US CPI",
      "description": "Macroeconomic and technical gold price forecast ahead of the US CPI release, featuring key interest rate yield analysis and market profile levels.",
      "url": "https://www.anzocapital.com/en/market-analysis/gold-forecast-ahead-of-us-cpi-20260713",
      "datePublished": "2026-07-14",
      "dateModified": "2026-07-14",
      "inLanguage": "en",
      "author": {
        "@type": "Person",
        "name": "Anzo Capital Content Team",
        "url": "https://www.anzocapital.com/en"
      },
      "publisher": {
        "@type": "Organization",
        "@id": "https://www.anzocapital.com/en/#organization",
        "name": "Anzo Capital",
        "logo": {
          "@type": "ImageObject",
          "url": "https://www.anzocapital.com/navbar-logo.png"
        }
      },
      "mainEntityOfPage": {
        "@type": "WebPage",
        "@id": "https://www.anzocapital.com/en/market-analysis/gold-forecast-ahead-of-us-cpi-20260713"
      },
      "image": {
        "@type": "ImageObject",
        "url": "<REPLACE_WITH_ACTUAL_ARTICLE_IMAGE_URL>"
      }
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.anzocapital.com/en" },
        { "@type": "ListItem", "position": 2, "name": "Market Analysis", "item": "https://www.anzocapital.com/en/market-analysis" },
        { "@type": "ListItem", "position": 3, "name": "Gold Forecast Ahead of US CPI", "item": "https://www.anzocapital.com/en/market-analysis/gold-forecast-ahead-of-us-cpi-20260713" }
      ]
    }
  ]
}
```
Use the actual publish date pulled from the CMS (page copy shows "14 July 2026") rather than a placeholder — do not leave `datePublished`/`dateModified` blank or defaulted to "today."

### 4c. Organization consistency + address fix (apply to the shared `#organization` node used site-wide)
```json
{
  "@type": "Organization",
  "@id": "https://www.anzocapital.com/en/#organization",
  "name": "Anzo Capital",
  "legalName": "Anzo Capital (SVG) LLC",
  "identifier": {
    "@type": "PropertyValue",
    "name": "Registration Number",
    "value": "308 LLC 2020"
  },
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Euro House, Richmond Hill Road",
    "addressLocality": "Kingstown",
    "addressCountry": "VC"
  },
  "location": {
    "@type": "Place",
    "name": "Anzo Capital Global — London Office",
    "address": {
      "@type": "PostalAddress",
      "addressLocality": "London",
      "addressCountry": "GB"
    }
  },
  "sameAs": [
    "https://www.linkedin.com/company/anzo-capital",
    "https://www.instagram.com/anzocapitalglobal",
    "https://www.facebook.com/Anzocapitalworldwide",
    "https://www.youtube.com/anzocapital",
    "https://t.me/anzocapitalglobal",
    "https://x.com/Anzo_Capital"
  ]
}
```
Use `Organization` (not `Corporation`) consistently for this `@id` across every page that references it (homepage currently does this correctly; regulation/about/help-center/account pages need to be changed to match). If the London Google Maps listing is a genuine second office, model it explicitly as shown above instead of only surfacing it via `sameAs`, so the two addresses aren't presented as conflicting claims about a single location.

## 5. Priority Summary

| Priority | Finding |
|---|---|
| Critical | Zero JSON-LD on sampled blog, market-analysis, and help-center article pages despite sibling pages having full schema — likely affects a large share of the ~110+ article-type URLs in the sitemap |
| High | Organization `PostalAddress` (St. Vincent registered-agent address) conflicts with the location referenced by its own `sameAs` Google Maps link (London) — material for a regulated financial entity |
| Medium | Same `@id` node typed inconsistently as `Organization` vs `Corporation` across pages |
| Medium | `feesAndCommissionsSpecification` populated with free text instead of required URL type on FinancialProduct blocks |
| Medium | ContactPoint `contactType` uses non-standard value `"customer support"` instead of Google-recognized `"customer service"` |
| Info | FAQPage present on several templates — valid markup, but no Google SERP benefit as of May 2026; low-priority cleanup, not urgent |
| Info | Missing QAPage on help-center articles and BreadcrumbList on help-center article template |
| Low | Homepage `logo` is a wide wordmark (172×32) rather than a square mark; consider adding a square icon variant |
