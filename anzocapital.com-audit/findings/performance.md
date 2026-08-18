# Core Web Vitals / Page Performance — anzocapital.com

Audit date: 2026-08-17
Canonical rendered URL tested: https://www.anzocapital.com/en

## Data-Source Limitation (read first)

**No Google API credentials are configured in this environment** (`GOOGLE_API_KEY` unset). `pagespeed_check.py` was invoked and returned `"PSI rate limit exceeded (240 QPM / 25,000 QPD)"` for both mobile and desktop strategies, and `crux: null` — **no live PageSpeed Insights (Lighthouse) run and no CrUX field data were obtainable for this audit.** `npx`/`node`/`lighthouse` are also not installed in this environment, so a local Lighthouse CLI run was not possible either.

All findings below are therefore derived from:
- Direct `curl` timing against the origin (TTFB, transfer size) using a Googlebot UA
- Playwright-based rendering via `render_page.py` (`render_engine: playwright-chromium`), which reports wall-clock render time (`render_ms`) as a **proxy for time-to-fully-rendered-content**, not a certified LCP/INP/CLS trace
- Manual diffing of raw (`--mode never`) vs. rendered (`--mode always`) HTML to assess the SSR/CSR gap

**No LCP, INP, or CLS value in this report is a lab-certified Lighthouse metric or CrUX field percentile.** They are reasoned estimates from the above signals. Treat the 0-100 score at the end as directional only. Recommend re-running this audit with a configured `GOOGLE_API_KEY` (PSI v5 + CrUX) or a working Lighthouse CLI to obtain certified LCP/INP/CLS/TBT numbers before making binding go/no-go decisions.

## Pages Tested

| Page | Type | URL |
|---|---|---|
| Homepage | Landing | https://www.anzocapital.com/en |
| Blog post | Content | https://www.anzocapital.com/en/blog/forex-risk-management |
| ECN account | Conversion | https://www.anzocapital.com/en/ecn-account |

## Measured Data

### TTFB (server response, via curl, Googlebot UA, uncached-safe headers)

| Page | TTFB | HTTP status | Rating |
|---|---|---|---|
| Homepage | 244 ms | 200 | Good (<800ms) |
| Blog post | 138 ms | 200 | Good |
| ECN account | 135 ms | 200 | Good |

TTFB is not a bottleneck. Cloudflare edge (`cf-cache-status: DYNAMIC`, `server-timing: cfEdge;dur=8, cfOrigin;dur=51`) is responding quickly; origin compute (`cfOrigin;dur=51`) is ~51ms. This part of the stack is healthy and not a priority.

### Render/hydration time proxy (Playwright, unthrottled desktop Chromium, repeated runs)

| Page | render_ms (run 1) | render_ms (run 2) |
|---|---|---|
| Homepage | 4240.7 ms (prior capture) | 2657.4 ms / 1865 ms (this session, 2 additional runs) |
| Blog post | 1966.7 ms | — |
| ECN account | 1958.5 ms | — |

The homepage render time varies 1.9x–2.3x run-to-run (1865ms–4240ms) under identical **unthrottled** conditions, which is itself a signal of an unstable, hydration-heavy critical path (large JS bundle + ~20 third-party scripts racing on the main thread). Real-world mobile users on throttled CPU/network (which is what Lighthouse mobile and most real visitors experience) will see meaningfully worse numbers than any of these unthrottled figures — this is a **floor**, not a worst case.

### Critical finding: fully client-rendered above-fold content (SSR/CSR gap)

This is a Next.js App Router site using React Server Components streaming, but the **visible page body is not server-rendered**. Raw HTML (`--mode never`, pre-JS) inspection of all three URLs shows an identical pattern:

```html
<body class="overflow-x-hidden font-jeko relative">
  <div hidden=""><!--$?--><template id="B:0"></template><!--/$--></div>
  <script>requestAnimationFrame(...)</script>
  <script src="/_next/static/chunks/webpack-....js" ...></script>
  <script>self.__next_f.push([0])</script>
  <script>self.__next_f.push([1,"...RSC flight payload as JSON..."])</script>
  ...
```

- **0** `<img>` tags, **0** `<h1>` tags, and no visible text in the raw `<body>` on any of the 3 pages tested — the entire body is a hidden Suspense boundary plus 32 `<script>` tags (16 unique first-party JS chunks) that must download, parse and execute before anything paints.
- The homepage hero heading ("Elevate Your Trades") does not appear anywhere in the raw HTML string at all — it only exists inside the client bundle / RSC flight data, deserialized at runtime.
- `<title>` and meta description **are** present in the initial `<head>` for all 3 pages (SSR'd via Next.js Metadata API — good for baseline crawlability/snippets), and one JSON-LD block (Organization/WebSite/ContactPoint, 3,967 bytes) is present. So metadata is fine, but **all visible LCP-candidate content (hero image, headline, CTA) is 100% dependent on JS execution.**

**Why this matters for CWV:** LCP cannot occur until the JS bundle (16 first-party chunks + polyfills) downloads, parses, executes, and React hydrates/paints the Suspense boundary. There is no server-rendered fallback content to paint early. This directly explains why homepage render time is both slow (1.9-4.2s) and volatile — LCP is gated behind the full hydration chain rather than a static HTML paint. This is the single largest lever available to improve LCP on this site.

### Third-party script load (homepage, post-hydration DOM snapshot)

24 distinct third-party script/pixel requests were identified firing on the homepage after hydration (via GTM container `GTM-P7QDGNXM`), in addition to ~16 first-party Next.js JS chunks:

| Category | Vendor(s) |
|---|---|
| Tag manager | Google Tag Manager (`gtm.js`) |
| Analytics | Google Analytics 4 (`gtag/js?id=G-2HZ6J1ZZE7`), Cloudflare Web Analytics beacon |
| Ads/conversion | Google Ads (`AW-17682708814` + DoubleClick viewthrough conversion pixel), Microsoft Bing Ads (`bat.bing.com` x2), Meta/Facebook Pixel (`connect.facebook.net` config + `fbevents.js`), Twitter/X Ads (`static.ads-twitter.com`), Reddit Ads pixel, AdRoll (3 scripts + ~10 separate 1x1 tracking-pixel `<img>` beacons to `d.adroll.com/cm/*`) |
| Session recording / heatmaps | Microsoft Clarity (**loaded twice** — `www.clarity.ms/tag/uet/97195997` and `scripts.clarity.ms/0.8.69/clarity.js` + a third GTM-triggered variant `clarity.ms/tag/t7gew2o0j7`), Hotjar (`script.hotjar.com` + `static.hotjar.com`) |
| Social insight | LinkedIn Insight Tag (**loaded twice** — `insight.old.min.js` and `insight.min.js` from `snap.licdn.com`) |
| Support widget | Zendesk (`static.zdassets.com/ekr/snippet.js`) |
| Misc | `cdnjs.cloudflare.com/.../crypto-js/4.2.0/crypto-js.min.js` (loaded eagerly, non-deferred, `<script type="text/javascript" src=...>` with no async/defer) |

**Severity: High.** This is an unusually large third-party footprint for a single landing page — effectively 3 separate session-recording tools (2x Clarity + Hotjar), 2x duplicate LinkedIn Insight Tag, and 5+ ad-pixel platforms (Google Ads, Bing, Meta, Twitter, Reddit, AdRoll) all firing concurrently. None of this blocks the initial paint (all are `async` and GTM-deferred), but collectively it:
1. Adds sustained main-thread contention in the seconds after load — directly at risk for elevated **INP** on first user interactions (tapping a nav item, opening a form) while these scripts are still initializing/attaching listeners.
2. Duplicates (2x Clarity, 2x LinkedIn Insight) are pure waste — no performance or measurement benefit, only added parsing/execution cost.
3. `crypto-js.min.js` loaded synchronously with no `async`/`defer` from a third-party CDN (`cdnjs.cloudflare.com`) is an anti-pattern — if used only for a form or later-in-page feature, it should be lazy-loaded on interaction, not on every pageview.

### DOM size

Rendered homepage DOM: ~440 open tags found (rough grep proxy, includes script/style tags — true element count is somewhat lower). Well under the 1,500-element concern threshold. **Not a CLS/INP risk factor** in itself.

### Page weight

- Initial HTML document (brotli-compressed over the wire, `content-encoding: br`): homepage 194 KB, blog 196 KB, ECN 198 KB as measured by curl — this is inflated by an inline RSC flight-data payload embedded in `<script>` tags (serialized component tree), not by markup or images (0 `<img>` tags in raw HTML).
- Could not capture full transferred resource weight (images, JS bundle KB after minification/compression, video) because no network-trace-capable tool (Lighthouse, WebPageTest, or a CDP network listener) was available in this environment. **This is a gap — recommend a proper Lighthouse/WebPageTest run to get exact JS/image KB and a resource waterfall.**

## Core Web Vitals Assessment (estimated, not lab-certified)

| Metric | Estimate | Rating | Confidence |
|---|---|---|---|
| LCP | ~2.0s–4.2s+ unthrottled desktop (homepage), likely worse on throttled mobile | **Needs Improvement to Poor** | Medium — reasoned from render_ms + zero-SSR-content finding, not a direct LCP trace |
| INP | Not measured (no interaction trace captured) | **At risk** — flagged High due to 24 concurrent third-party scripts + hydration-heavy SPA | Low — no interaction was simulated |
| CLS | Not measured (no layout-shift trace captured) | **Unverified** — flagged as elevated risk because content pops in post-hydration behind a Suspense boundary with no visible pre-hydration placeholder dimensions confirmed | Low |
| TTFB | 135–244 ms across all 3 pages | **Good** | High — directly measured |

Given no CrUX field data is retrievable (no API key; the account/site may also be below CrUX's minimum-traffic threshold for public reporting — unconfirmed), **75th-percentile pass/fail against real users cannot be certified in this report.** The lab signals above indicate meaningful LCP and INP risk.

## Prioritized Recommendations

1. **[High impact / High severity] Ship server-rendered (or static) above-fold content.** The homepage/blog/conversion pages currently render an empty `<body>` behind a Suspense boundary with zero visible markup pre-hydration. Since this is Next.js App Router, use server components / static generation for the hero section, headline, and primary CTA so they paint from the initial HTML response instead of waiting on full client hydration. This is the single biggest lever to reduce LCP and reduce run-to-run render volatility (1.9s–4.2s observed).
2. **[High impact / High severity] Deduplicate and defer third-party tracking scripts.** Remove the duplicate Microsoft Clarity load (2-3 concurrent instances) and duplicate LinkedIn Insight Tag load (2 instances) — pick one implementation each. Move the eagerly-loaded `crypto-js.min.js` off the critical path (dynamic `import()` on the feature that needs it, not global). Consolidate ad-pixel/analytics loading through GTM's built-in triggers (e.g., load on user consent/interaction rather than all-at-once on page load) to reduce concurrent main-thread contention that drives up INP.
3. **[Medium impact] Preload the LCP resource once it's server-rendered.** After addressing #1, add `<link rel="preload">`/`fetchpriority="high"` for the actual hero image/font so the browser doesn't discover it late in a client-rendered tree.
4. **[Medium impact] Reduce first-party JS chunk count on initial route.** 16 separate Next.js chunks are requested for the homepage shell alone; review code-splitting boundaries to ensure non-critical UI (below-fold sections, modals) is not part of the initial chunk graph.
5. **[Verification / Medium] Re-run this audit with real tooling.** Configure `GOOGLE_API_KEY` for PSI v5 + CrUX, or get a working Lighthouse CLI in this environment, to obtain certified LCP/INP/CLS values, a Lighthouse performance score, TBT, and a full resource-weight breakdown (JS/image/font KB). Until then, treat all CWV figures in this report as directional lab estimates, not ranking-relevant field data.
6. **[Low, hygiene] Audit whether all 24 third-party integrations (2x session recording, 5 ad pixels, chat widget, 2x social insight tag) are still in active use.** Even deferred/async scripts consume battery, memory, and background CPU on mobile, and each is a potential INP contributor on the first tap.

## Score Estimate

**Estimated Performance Score: ~40-50 / 100** (mobile, lab-heuristic — not a certified Lighthouse score, since no PSI/Lighthouse run was obtainable in this environment)

Basis: TTFB is strong (+), DOM size is reasonable (+), but a 100%-client-rendered above-fold experience with volatile 1.9-4.2s render/hydration time and a 24-script third-party footprint firing concurrently on load are both classic drivers of "Needs Improvement"-to-"Poor" LCP and elevated INP risk. Recommend re-scoring with live PSI/CrUX or Lighthouse once available — this estimate should not be treated as authoritative for reporting to stakeholders as a final CWV pass/fail number.
