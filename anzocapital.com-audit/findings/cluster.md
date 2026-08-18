# Content/Topic Cluster Architecture Audit — anzocapital.com (/en/blog + /en/market-analysis)

**Date:** 2026-08-17
**Scope:** 90+ evergreen `/en/blog/` posts, 28 dated `/en/market-analysis/` posts, and `/en/learning-library-guides`.
**Method note:** The site is a fully client-rendered Next.js/Strapi app — server HTML returns no body/article content (in-page internal links, related-article widgets, and category taxonomy are injected client-side after a browser-executed API call), so pairwise SERP-overlap crawling of every article body was not possible via automated fetch. Findings below combine (a) exhaustive sitemap slug inventory for both sections, (b) breadcrumb JSON-LD extracted from raw HTML confirming `Blog` and (inferred) `Market Analysis` are separate, disconnected breadcrumb parents, (c) targeted Google SERP checks for the highest-risk keyword collisions, and (d) semantic/topical clustering of all 118 slugs. Recommend a follow-up crawl with a headless-browser-capable tool to confirm exact in-content link counts once available.

---

## 1. Does `/en/learning-library-guides` function as a hub?

**No.** Its meta title/OG description ("Learning Library | Free PDF Trading Guides | Anzo Capital" — "Download free educational guides covering CFD trading, forex basics, charting, platform navigation, risk management, and your first trade") identify it as a **gated PDF lead-magnet page**, not a topical hub that links out to the 90+ blog posts or 25+ market-analysis posts. It is a distinct content type/funnel (downloadable guides) sitting parallel to, not on top of, the blog and market-analysis archives. Breadcrumb data confirms blog posts live under `Home > Blog > [Post]` with no intermediate hub/category node, and no cluster hub currently exists for either section. **This is a missed opportunity** — the site has zero true pillar/hub pages today; blog and market-analysis are flat, unstructured archives.

---

## 2. Do blog and market-analysis form coherent hub-and-spoke clusters today?

**No — they operate as two parallel, disconnected flat archives with significant unmanaged topical overlap, especially in Gold/Metals and Macro/Central-bank content.** Both sections independently accumulated posts on the same core topics (gold drivers, CPI, NFP, COT reports) without a shared taxonomy or cross-linking plan. Evergreen "blog" explainer content and dated "market-analysis" news-hook content on the *same underlying query* compete for the same SERP real estate instead of reinforcing each other via links.

---

## 3. Natural topic clusters identified (from full slug inventory)

### Cluster A — Gold & Metals Trading (14 posts — largest overlap risk)
Blog: `what-moves-gold-prices`, `what-moves-silver-prices`, `gold-vs-silver`, `xauusd-vs-xagusd`, `xau-usd-gold-trading-strategies`, `gold-price-forecast-2026-drivers`, `best-time-to-trade-gold-silver`, `mt5-beat-mt4-xau-usd`
Market-analysis: `gold-forecast-ahead-of-us-cpi-20260713`, `us-cpi-gold-price-forecast-20260811`, `why-bond-yields-drive-gold-not-dxy-20260623`, `gold-trading-post-us-inflation-strategy-20260716`, `why-wait-for-gold-pullback-retail-sentiment-20260813`, `why-gold-prices-are-sliding`

### Cluster B — Macro / Central-Bank Events & News Trading (20 posts)
Blog: `cpi-impact-forex-index-trading`, `cpi-vs-core-cpi-trading-strategy`, `central-bank-role-economy`, `monetary-vs-fiscal-policy`, `gdp-impact-on-currency-forex-explained`, `professionals-traders-prepare-cpi-ppi-nfp`, `news-traders-shield-nfp-cpi`, `weekly-fx-macro-calendar-events-trading-guide`, `us-unemployment-claims-forex-impact`
Market-analysis: `fed-rate-decision-us-2-year-yields-dollar-impact-20260730`, `ecb-rate-decision-eurusd-price-outlook-20260722`, `bank-of-canada-rate-decision-analysis-20260714`, `bank-of-england-preview-gbpusd-20260729`, `rbnz-interest-rate-trap-nzd-20260707`, `nfp-live-preview-us-dollar-trading-guide-20260806`, `how-to-read-cot-report-cftc-guide-20260727`, `commitment-of-traders-gbp-extreme-positioning-20260701`, `cot-report-hedge-fund-positioning-cad-euro-20260812`, `how-to-use-retail-sentiment-counter-indicator-20260709`, `why-good-economic-news-can-be-bad-for-price-20260708`

### Cluster C — Copy Trading (4 posts)
`copy-trading-mistakes`, `copy-trading-provider-transparency-track-record`, `how-to-choose-copy-trading-provider-2026`, `copy-trading-risk-controls`

### Cluster D — MT4/MT5 Platform, Alerts & Margin Mechanics (13 posts — second-largest overlap risk)
Platform choice: `mt4-vs-mt5-trading-platforms`, `mt5-beat-mt4-xau-usd`, `anzo-mt4-mt5-setup`, `best-mt4-mt5-indicators`
Alerts (5 near-duplicate posts): `mt4-mt5-alert-templates-breakout`, `mt4-mt5-alerts-automation-guide`, `how-to-set-price-alerts-on-mt5-mobile`, `why-trading-alerts-dont-trigger`, `how-to-avoid-false-trading-alerts`
Margin/equity: `margin-call-guide`, `margin-vs-equity`, `credit-equity-margin-metatrader`, `low-vs-high-leverage-forex`
Troubleshooting: `fix-for-invalid-account-connection-glitches`

### Cluster E — IB / Introducing-Broker Marketing (6 posts, B2B commercial)
`how-to-become-successful-forex-introducing-broker`, `ib-marketing-growth-engine`, `introducing-brokers-authority-building`, `how-to-build-trust-forex-introducing-broker-marketing-strategies`, `ib-visual-identity`, `dedicated-cx-teams-ib-client-retention-lifetime-value`

### Cluster F — Bonus / Promo Mechanics (11 posts — highest cannibalization density on the site)
`bonus-vs-rebate-vs-cashback`, `deposit-bonus-key-terms`, `claim-activate-50-percent-deposit-bonus`, `50-percent-deposit-bonus-margin-power`, `50-percent-bonus-equity-multipliers`, `finding-right-spread-bonus`, `bonus-risk-models-drawdown-protection`, `bonus-risk-explained-trading-credit`, `pros-prefer-non-loseable-credits`, `maximize-credit-bonus-capital`, `how-to-turn-small-deposit-into-large-trading-cushion`

### Cluster G — Regional/Geo (SEA) Trading Guides (11 posts, low overlap, good geo-targeting)
`forex-trading-in-vietnam-beginners-guide`, `vietnam-pmi-export-data-commodity-cfd-trading`, `vietnam-digital-economy-fx-trading`, `bank-indonesia-usd-idr-guide`, `indonesia-nickel-exports-global-commodity-prices-trading`, `malaysian-forex-trading-mistakes-how-to-avoid`, `hong-kong-vs-us-stock-cfds`, `psei-vs-sp500-performance`, `ph-stock-market-vs-global-indices`, `how-to-use-cfds-to-profit-from-dropping-psei`, `how-ofw-remittances-impact-usd-php-forex`

---

## 4. Cannibalization risk pairs (flagged by slug, ranked by severity)

| Severity | Slug A | Slug B | Slug C (if any) | Why |
|---|---|---|---|---|
| **Critical** | `claim-activate-50-percent-deposit-bonus` | `50-percent-deposit-bonus-margin-power` | `50-percent-bonus-equity-multipliers` | Three separate blog posts all target the same commercial query "Anzo Capital 50% deposit bonus." Confirmed via live Google search — all three compete alongside the static promo landing page. |
| **High** | `bonus-risk-models-drawdown-protection` | `bonus-risk-explained-trading-credit` | — | Both explain bonus/credit risk mechanics; near-identical topical scope. |
| **High** | `pros-prefer-non-loseable-credits` | `maximize-credit-bonus-capital` | `how-to-turn-small-deposit-into-large-trading-cushion` | All three pitch "use bonus credit to trade bigger" — same angle, different headlines. |
| **High** | `mt4-mt5-alert-templates-breakout` | `mt4-mt5-alerts-automation-guide` | `how-to-set-price-alerts-on-mt5-mobile` (+ `why-trading-alerts-dont-trigger`, `how-to-avoid-false-trading-alerts`) | Five posts on MT4/MT5 alerts; overlapping intent on "how to set up/fix trading alerts on MT4/MT5." |
| **High** | `how-to-become-successful-forex-introducing-broker` | `ib-marketing-growth-engine` | `introducing-brokers-authority-building`, `how-to-build-trust-forex-introducing-broker-marketing-strategies` | Four posts on IB marketing strategy/success/trust/authority — overlapping subtopics of one broader query. |
| **Medium** | `what-moves-gold-prices` (blog, evergreen) | `gold-forecast-ahead-of-us-cpi-20260713` / `us-cpi-gold-price-forecast-20260811` / `why-bond-yields-drive-gold-not-dxy-20260623` / `gold-trading-post-us-inflation-strategy-20260716` (market-analysis, dated) | — | Evergreen "what drives gold" content directly overlaps the recurring macro-driver angle of four dated gold posts. Risk is elevated because the evergreen post is never updated to interlink with the dated ones, so Google sees four+ competing "why does gold move" pages instead of one authority page + timely spokes. |
| **Medium** | `gold-price-forecast-2026-drivers` (blog) | `gold-forecast-ahead-of-us-cpi-20260713` / `us-cpi-gold-price-forecast-20260811` (market-analysis) | — | Both target "gold price forecast" intent. |
| **Medium** | `cpi-impact-forex-index-trading` | `professionals-traders-prepare-cpi-ppi-nfp` | `news-traders-shield-nfp-cpi` | Three blog posts on trading CPI/NFP news events with overlapping "how to trade the news" angle. |
| **Medium** | `professionals-traders-prepare-cpi-ppi-nfp` (blog) | `nfp-live-preview-us-dollar-trading-guide-20260806` (market-analysis) | — | Overlap on "how to trade NFP." |
| **Medium** | `how-to-read-cot-report-cftc-guide-20260727` (evergreen educational) | `commitment-of-traders-gbp-extreme-positioning-20260701` / `cot-report-hedge-fund-positioning-cad-euro-20260812` | — | Educational "how to read COT" competes on generic "COT report" query with two applied/dated posts; should instead be the pillar these two link *from*. |
| **Medium** | `copy-trading-mistakes` | `copy-trading-risk-controls` | — | Overlapping "risks/mistakes to avoid in copy trading" framing. |
| **Medium** | `copy-trading-provider-transparency-track-record` | `how-to-choose-copy-trading-provider-2026` | — | Both target "how to choose/evaluate a copy trading provider." |
| **Medium** | `mt4-vs-mt5-trading-platforms` | `mt5-beat-mt4-xau-usd` | — | Second post is a gold-specific angle on the same MT4-vs-MT5 comparison query; needs clear differentiation + canonical hierarchy. |
| **Low** | `margin-vs-equity` | `credit-equity-margin-metatrader` | `margin-call-guide` | Adjacent margin-mechanics topics; some overlap on "margin vs equity" definitions but distinct enough if properly scoped and interlinked. |
| **Low** | `psei-vs-sp500-performance` | `ph-stock-market-vs-global-indices` | `how-to-use-cfds-to-profit-from-dropping-psei` | Three PSEi-related posts; moderate overlap, lower risk since angles (index comparison, comparison, bearish-CFD strategy) are more distinct. |

---

## 5. Recommended hub + internal-link architecture (top 4 clusters)

### Hub 1: Gold & Metals Trading (highest priority — 14 pieces, no hub today)
- **New pillar page:** `/en/blog/gold-trading-hub` (or repurpose `xau-usd-gold-trading-strategies` as the pillar since it already has the broadest transactional+informational scope; target 2,500–3,500 words covering what moves gold/silver, XAU/XAG basics, strategy, and a "current gold forecast" module that dynamically pulls/links the latest dated market-analysis gold post).
- **Spokes (evergreen):** `what-moves-gold-prices`, `what-moves-silver-prices`, `gold-vs-silver`, `xauusd-vs-xagusd`, `best-time-to-trade-gold-silver`, `mt5-beat-mt4-xau-usd`.
- **Timely spokes (dated market-analysis, link up to pillar + most recent 2-3 only, older ones canonicalize/consolidate):** `gold-forecast-ahead-of-us-cpi-20260713`, `us-cpi-gold-price-forecast-20260811`, `why-bond-yields-drive-gold-not-dxy-20260623`, `gold-trading-post-us-inflation-strategy-20260716`, `why-wait-for-gold-pullback-retail-sentiment-20260813`, `why-gold-prices-are-sliding`.
- **Action:** Merge/canonicalize `gold-price-forecast-2026-drivers` into the pillar (it duplicates `what-moves-gold-prices`); 301 or noindex+canonicalize the weakest of the four "gold macro-driver" market-analysis posts once superseded by newer ones.

### Hub 2: Macro / Central-Bank Events (20 pieces)
- **Pillar:** `weekly-fx-macro-calendar-events-trading-guide` (already positioned as the evergreen calendar/overview post — ideal pillar) or a new `/en/blog/central-bank-macro-events-hub`.
- **Evergreen spokes:** `central-bank-role-economy`, `monetary-vs-fiscal-policy`, `gdp-impact-on-currency-forex-explained`, `cpi-impact-forex-index-trading`, `cpi-vs-core-cpi-trading-strategy`, `how-to-read-cot-report-cftc-guide-20260727` (move this COT explainer to evergreen spoke status feeding the two dated COT posts).
- **Consolidate:** merge `professionals-traders-prepare-cpi-ppi-nfp` + `news-traders-shield-nfp-cpi` into one canonical "how to trade CPI/NFP" spoke; redirect the other.
- **Dated spokes (rate decisions/NFP/COT, each links up to pillar and to the relevant evergreen explainer):** `fed-rate-decision-us-2-year-yields-dollar-impact-20260730`, `ecb-rate-decision-eurusd-price-outlook-20260722`, `bank-of-canada-rate-decision-analysis-20260714`, `bank-of-england-preview-gbpusd-20260729`, `rbnz-interest-rate-trap-nzd-20260707`, `nfp-live-preview-us-dollar-trading-guide-20260806`, `commitment-of-traders-gbp-extreme-positioning-20260701`, `cot-report-hedge-fund-positioning-cad-euro-20260812`.

### Hub 3: MT4/MT5 Platform & Trading Mechanics (13 pieces)
- **Pillar:** `mt4-vs-mt5-trading-platforms` (broadest, highest-volume comparison query — natural pillar).
- **Spokes — platform:** `anzo-mt4-mt5-setup`, `best-mt4-mt5-indicators`, `mt5-beat-mt4-xau-usd` (re-angle explicitly as a Gold-cluster crosslink rather than a second platform-comparison piece).
- **Spokes — alerts (consolidate 5→2-3):** merge `mt4-mt5-alert-templates-breakout` + `mt4-mt5-alerts-automation-guide` into one "MT4/MT5 alert setup & automation" spoke; keep `why-trading-alerts-dont-trigger` + `how-to-avoid-false-trading-alerts` merged into one troubleshooting spoke; keep `how-to-set-price-alerts-on-mt5-mobile` as a distinct mobile-specific spoke.
- **Spokes — margin:** `margin-call-guide`, `margin-vs-equity`, `credit-equity-margin-metatrader`, `low-vs-high-leverage-forex` (interlink tightly; these are legitimately distinct sub-intents).

### Hub 4: Bonus / Promo Mechanics (11 pieces — most urgent cleanup)
- **Pillar:** `deposit-bonus-key-terms` (most evergreen, broadest informational framing) or a new `/en/blog/trading-bonus-hub` if commercial intent should lead.
- **Action before building links:** consolidate the 3 "50% deposit bonus" posts into one canonical page (301 the other two into it — this is a direct duplicate-content/cannibalization fix, not just an interlink fix), and consolidate the "bonus risk" pair and "maximize credit" trio similarly (aim for ~5-6 posts total, not 11).
- **Resulting spokes:** `bonus-vs-rebate-vs-cashback`, `finding-right-spread-bonus`, consolidated "50% deposit bonus" page, consolidated "bonus risk & drawdown protection" page, consolidated "maximize bonus credit" page.

### Link matrix rules applied to all four hubs
- Mandatory: every spoke ↔ pillar (bidirectional).
- Recommended: spoke ↔ spoke within the same cluster (e.g., `margin-call-guide` ↔ `margin-vs-equity`).
- Optional/cross-cluster: e.g. `mt5-beat-mt4-xau-usd` ↔ Gold pillar; `cpi-impact-forex-index-trading` ↔ Macro pillar ↔ relevant dated Fed/CPI market-analysis posts.
- Dated market-analysis posts older than ~90 days that have been superseded by a newer post on the same event type should link *up* to the evergreen pillar/spoke as their primary internal-link target once they roll off "recent" status, rather than continuing to compete independently in search.

---

## 6. Summary of gaps
1. No hub pages exist today for any of the 6-7 natural clusters; blog and market-analysis are flat archives with no shared taxonomy.
2. `/en/learning-library-guides` is a PDF-download funnel, not a content hub — it does not solve the hub-and-spoke gap.
3. Bonus/Promo (11 posts) and MT4/MT5 Alerts (5 posts) show the densest near-duplicate content and should be consolidated (not just interlinked) before building hub architecture.
4. Gold/Metals and Macro/Central-bank clusters show the clearest blog-vs-market-analysis cannibalization pattern: evergreen "driver" explainers and dated "forecast ahead of [event]" posts are answering the same underlying query without any link relationship connecting them.
