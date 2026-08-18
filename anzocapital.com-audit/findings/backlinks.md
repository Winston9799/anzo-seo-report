# Backlink Profile — anzocapital.com

**Analysis tier: 0 (Common Crawl + local verification crawler only).**
Moz API and Bing Webmaster API keys are **not configured** for this run, so
Domain Authority (DA), Page Authority (PA), Spam Score, referring-domain
counts/lists, and anchor-text distribution are **unavailable**. No numbers
below should be read as DA/PA-equivalent — none were fabricated.

**To unlock Tier 1 (DA/PA, spam score, referring domains, anchor text) for
future runs**, add a Moz API key to:
`/Users/winstonting/.config/claude-seo/backlinks-api.json`
(free tier: 2,500 rows/month — https://moz.com/products/api). Bing Webmaster
data (Tier 2) is only usable for properties already registered to the
account running this skill, so it would not apply to arbitrary competitor
comparisons even if configured.

## Data sources used

| Source | Confidence | What it provides at this tier |
|---|---|---|
| Common Crawl domain web graph (`cc-main-2026-jan-feb-mar`) | 0.50 | Domain-level PageRank, harmonic centrality, crawl/ranking presence, host count. Quarterly snapshot. |
| WHOIS / domain heritage check | n/a (factual) | Registration age, registrar, expiry — used as a PBN/expired-domain risk signal only, not a backlink metric. |
| Backlink verification crawler | n/a | **Not run** — no known/candidate backlink list was available or supplied for this domain. See note below. |

## What could NOT be assessed (explicitly out of scope at this tier)

- **Referring domain count** — no source available (CC's public graph exposes
  aggregate PageRank/harmonic-centrality scores, not the underlying edge list
  of who links to a specific domain; Moz/DataForSEO required).
- **Domain quality distribution of linking sites** — no source available.
- **Anchor text patterns** — no source available. No anchor text data exists
  at Tier 0; none is claimed.
- **Toxic/spammy link ratio** (critical for a forex/YMYL site) — no source
  available. Cannot confirm or rule out PBN/affiliate spam links without
  Moz Spam Score or DataForSEO.
- **Link velocity trend** — free sources do not provide historical link
  acquisition data.
- **Follow/nofollow ratio** — no source available.
- **Geographic relevance of linking domains** — no source available.
- **Specific authoritative/notable linking domains** (e.g. finance
  publications, regulator directories, industry award sites) — cannot be
  identified without a referring-domain list from Moz/DataForSEO/Bing. No
  such list was found in this repository/audit and none was supplied by the
  user for verification, so `verify_backlinks.py` was not run.

Given 7/7 standard scoring factors (referring domains, quality distribution,
anchor text, toxic ratio, velocity, follow/nofollow, geo relevance) have
**zero** data sources at this tier, **no numeric Backlink Health Score is
reported.** Reporting a score here would be misleading.

## Common Crawl domain-level signals (confidence: 0.50)

Source: Common Crawl Web Graph, release `cc-main-2026-jan-feb-mar`
(quarterly snapshot; https://commoncrawl.org/web-graphs). Retrieved
2026-08-17.

| Metric | Value |
|---|---|
| In CC crawl | Yes |
| In CC domain rankings | Yes |
| PageRank (raw) | 1.063e-08 |
| PageRank rank | 4,998,024 |
| Harmonic centrality (raw) | 12,604,621 |
| Harmonic centrality rank | 17,049,737 |
| Distinct hosts under domain seen in crawl | 4 |

**Interpretation (with explicit caveats):**
- The domain is present in both the CC crawl and its computed rankings —
  it is not a brand-new or unindexed site, and CC has discovered inbound
  links to it from elsewhere in the crawled web. This should **not** be
  read as "low authority" (per CC-interpretation guidance, absence would
  mean that, presence with a rank is a different, weaker signal).
- However, a PageRank rank in the high single-digit millions and a harmonic
  centrality rank in the high tens of millions place anzocapital.com well
  outside the upper tier of the web graph — millions of domains rank ahead
  of it on both metrics. This is a coarse, domain-level directional signal
  only; CC's public dataset does not expose *why* (i.e., which domains
  link in), so it cannot be broken into "good" vs. "toxic" links.
- 4 distinct hosts under the domain were observed in the crawl (e.g.
  `www.`, apex, and/or regional subdomains) — a normal footprint, not
  indicative of subdomain-based link manipulation.
- **This is a domain-level (not URL-level) metric** and does not
  distinguish inbound backlink quality from general crawl connectivity.

## Domain heritage check (factual, not a backlink metric)

Source: WHOIS. Retrieved 2026-08-17.

| Field | Value |
|---|---|
| Registrar | GoDaddy Corporate Domains, LLC |
| Created | 2015-10-21 |
| Last updated | 2024-10-16 |
| Expires | 2026-10-21 |
| Age | ~10.8 years |
| Topical shift risk | Unknown (no baseline topic supplied — would require historical archive comparison, out of scope for this run) |

anzocapital.com has been continuously registered for nearly 11 years under
one registrar, which is a mild positive signal against the "recently
acquired/flipped expired domain repurposed as a forex PBN hub" risk pattern
common in this niche. This is a heritage/trust signal, not a measure of
inbound link quality, and does not substitute for an actual spam-link audit.

## Forex/YMYL-specific notes

For a regulated financial services brand, the composition of the backlink
profile (regulator directories, finance media, award/press citations) is
more important than raw link volume — but **this cannot be verified without
Moz or DataForSEO data**. In particular:
- No inbound links from finance publications, regulator directories, or
  industry award sites could be confirmed or ruled out at this tier.
- No affiliate/PBN spam links could be confirmed or ruled out at this tier.
- The site's own `/en/awards` page (referenced in the audit brief) was not
  independently verified as part of this backlink task — outbound content
  verification belongs to the content/technical audit tracks, not this
  backlink-profile task. Recommend cross-checking with `/seo content
  <url>` if not already covered.

## Recommendation: is upgrading to a paid tier worth it?

**Yes, moderately high priority for this specific site.** anzocapital.com
is a YMYL financial services property in a niche (retail forex/CFD
brokerage) that is disproportionately targeted by low-quality affiliate
and PBN link schemes, and where toxic-link exposure and anchor-text
over-optimization carry real regulatory/reputational and ranking risk.
At Tier 0 we cannot rule out (or confirm) either problem — the entire
"toxic link ratio," "referring domain quality," and "anchor text
naturalness" dimensions are blind spots. A Moz API key (free, 2,500
rows/month) would immediately unlock DA/PA, Spam Score, a referring-domain
list, and anchor text — enough to answer the single highest-priority
question here ("are there spammy/manipulative links pointing at this
domain, and does the anchor text look natural"). DataForSEO (Tier 3) would
add link velocity and geographic relevance, which are lower priority for
an initial pass. **Recommended next step: add the free Moz API key before
the next scheduled audit cycle**, rather than immediately purchasing
DataForSEO credits.

---
*Findings generated by the SEO backlink-profile skill, Tier 0
(Common Crawl + verification crawler only). Re-run this analysis after
adding a Moz API key for materially more complete results.*
