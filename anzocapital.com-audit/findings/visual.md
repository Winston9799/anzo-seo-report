# Visual / Mobile UX Findings — anzocapital.com

**Rendered URL base:** https://www.anzocapital.com/en
**Pages captured:** Homepage (`/en`), Blog post (`/en/blog/forex-risk-management`), Conversion page (`/en/accounts-overview`)
**Viewports:** Desktop 1920×1080, Mobile 375×812 (device-scale-factor 2). Laptop (1366×768) and Tablet (768×1024) full-page captures also taken for the homepage.
**Tool:** Playwright/Chromium via `capture_screenshot.py`, `networkidle` + 1s settle delay.

**Score estimate: 78 / 100** (Good fundamentals — strong CTA visibility and above-fold trust stats — pulled down by persistent overlay-widget clutter on mobile and the absence of an above-the-fold regulatory trust badge on a YMYL financial site.)

---

## Screenshots

| Page | Desktop (viewport) | Desktop (full page) | Mobile (viewport) | Mobile (full page) |
|---|---|---|---|---|
| Homepage | `screenshots/homepage-desktop.png` | `screenshots/homepage-desktop-full.png` (+ `homepage-laptop-full.png`, `homepage-tablet-full.png`) | `screenshots/homepage-mobile.png` | `screenshots/homepage-mobile-full.png` |
| Blog post | `screenshots/blog-desktop.png` | `screenshots/blog-desktop-full.png` | `screenshots/blog-mobile.png` | `screenshots/blog-mobile-full.png` |
| Accounts overview | `screenshots/accounts-desktop.png` | `screenshots/accounts-desktop-full.png` | `screenshots/accounts-mobile.png` | `screenshots/accounts-mobile-full.png` |

All paths relative to `anzocapital.com-audit/`.

---

## 1. Above-the-fold content & CTA visibility

**Homepage — Desktop (`homepage-desktop.png`):** H1 "ELEVATE YOUR TRADES" and the primary red CTA "Open Live Account" render in the left third of the hero, fully visible without scrolling. The 4-stat strip (0.0 Pips / 1:1000 Max Leverage / $10 Low Deposit / <0.1 Sec Execution) and the trust-stat row (2015 Established / 80,000+ Global Clients / Official Partner of Phoenix Suns) are **also** visible above the fold at 1920×1080 — this is a strong result for a YMYL page. **Severity: none (pass).**

**Homepage — Mobile (`homepage-mobile.png`):** Heading and CTA are centered and prominent; CTA button is large (≈315×72 CSS px). The four quick stats and the "2015 Established / 80,000+ Global Clients / Official Partner of Phoenix Suns" trust row are all visible in the same 375×812 viewport, just above a "Welcome Deposit Bonus" promo banner docked at the bottom edge. **Severity: none (pass)** — but see overlay-clutter issue below.

**Accounts-overview (conversion page) — Desktop & Mobile (`accounts-desktop.png`, `accounts-mobile.png`):** H1 "ACCOUNTS OVERVIEW," a one-paragraph value prop, and the "Open Live Account" CTA are all visible above the fold on both viewports with good contrast (white text on near-black hero with red accent). **Severity: none (pass).**
- **Finding (Low):** Unlike the homepage, the accounts-overview hero does **not** repeat the "2015 Established / 80,000+ Global Clients" trust stats. On a conversion-critical page for a YMYL financial product, repeating a compact trust/credibility signal near the CTA (not just on the homepage) would reduce last-mile hesitation. Recommend adding a compact trust strip (regulator badge + established date + client count) directly under or beside the CTA on `/accounts-overview` and `/ecn-account`.

**Blog post (`blog-desktop.png`, `blog-mobile.png`):** No conversion CTA above the fold, which is acceptable/expected for editorial content, but there is also no visible author name/credential — only a publish date ("21 April 2026") and a category chip ("Risk Management"). Absent author E-E-A-T signals above the fold is a moderate weakness for YMYL content trust.
- **Severity: Medium** — Add a visible byline (author name + credential, e.g., "Reviewed by [name], licensed analyst") near the date/category row.

---

## 2. Mobile responsiveness & layout integrity

- Viewport meta tag (`width=device-width, initial-scale=1`) is correctly honored; no horizontal scrollbar or content overflow was observed on any of the three pages at 375px width (checked via full-page mobile captures).
- Navigation collapses correctly to a hamburger icon on mobile (top-right, `homepage-mobile.png`); primary nav items (Trading, Platforms, Education, Sponsorship, About Us) plus Sign in/Register are hidden behind it, which is standard practice.
- Full-page mobile renders (`homepage-mobile-full.png`, `blog-mobile-full.png`, `accounts-mobile-full.png`) show clean single-column stacking through pricing tables, FAQ accordions, and the footer — no broken grids, no text truncation from fixed-width containers, and images scale correctly.
- On `accounts-mobile-full.png`, the "STP / ECN / Copy Trading" account cards are laid out as a horizontally-scrollable row with the next card intentionally peeking in from the right edge — this reads as an intentional swipe affordance rather than a bug, but there is no explicit dot/arrow indicator signaling swipeability. **Severity: Low** — consider adding a scroll-position indicator (dots or gradient fade) so mobile users know more account types exist off-screen.
- **Severity: none** for general responsive layout integrity — pass across desktop/laptop/tablet/mobile breakpoints tested.

---

## 3. Overlay widget clutter / overlap (confirmed issue)

Two persistent floating elements — a live-chat bubble (bottom-right) and a "Welcome Deposit Bonus — Claim up to $2,000 USD" promo card — are present on every page tested, at every viewport.

- **Desktop:** These sit in the bottom-right corner without overlapping primary content; low impact.
- **Mobile — confirmed overlap (Medium-High severity):** In `blog-mobile.png`, the chat bubble icon visually overlaps the right edge of the dark "2026 Trader Guide" pull-quote text block, partially obscuring the sentence "...the real edge often comes from risk control..." In `blog-mobile.png` and `accounts-mobile.png`, the "Welcome Deposit Bonus" banner is docked at the very bottom of the viewport and consumes roughly 15–20% of the 812px-tall mobile viewport, pushing content up and creating a persistent below-the-fold obstruction that reappears on every scroll position (it is fixed/sticky).
- This is a genuine UX/readability defect on a content page (the blog) where paid-widget chrome is covering editorial text, and it eats a disproportionate share of mobile screen real estate on a small-viewport device.
- The banner's dismiss ("×") control is small — visually approximates ~24×24px, below the 48×48px recommended minimum touch target, making it harder to dismiss on mobile.

**Recommendation:** Reduce the vertical footprint of the mobile promo banner (collapse to a smaller pill/FAB that expands on tap), enlarge the close-button hit area to ≥48×48px, and ensure the chat-widget bubble's z-index/positioning never intersects body copy — reposition or shrink on scroll if a content block is under it.

---

## 4. Text readability / contrast

- Body copy (dark gray/black on white) throughout blog and accounts pages passes contrast comfortably.
- Hero headline text ("ELEVATE YOUR TRADES," "ACCOUNTS OVERVIEW") is white on a dark/black gradient — good contrast in both cases.
- **Low-severity note:** The homepage hero background is a busy collage of semi-transparent "copy trading" performance-card mockups (trader avatars, $ P&L figures, equity curves) layered behind the headline. On mobile in particular (`homepage-mobile.png`), a trader card ("ApexTrader92," "$19,383.3") sits directly behind the H1 text; the dark overlay keeps text legible, but the imagery itself (aggressive P&L/leverage stats: 1:1000, $16,761.50 profit, 3216.52% return) risks reading as "get-rich-quick" marketing rather than a regulated-broker aesthetic — a brand-trust consideration worth flagging for a YMYL forex site, independent of contrast/legibility (which is fine).
- No layout shift or flash-of-unstyled-content was observed after the 1s post-load settle window; fonts and hero imagery were fully painted in all captures.

---

## 5. Tap target sizing (mobile)

| Element | Approx. size (CSS px) | Verdict |
|---|---|---|
| "Open Live Account" CTA (homepage/accounts) | ~315×72 | Pass (well above 48×48) |
| Hamburger menu icon | ~24×24 icon, larger tappable padding assumed | Likely pass, not independently measured via DOM |
| Live-chat FAB bubble | ~62×62 | Pass |
| "Claim" button on promo banner | ~90×40 | Marginal — height 40px is under the 48px guideline |
| Promo banner "×" dismiss control | ~24×24 | **Fail** — below 48×48 recommended minimum |

**Severity: Low-Medium** for the two undersized controls on the promo banner; primary conversion CTAs are all correctly sized.

---

## 6. Trust signals (YMYL-critical)

- **Pass:** "2015 Established" and "80,000+ Global Clients" stats are visible above the fold on the homepage at both desktop and mobile viewports (confirmed in `homepage-desktop.png` and `homepage-mobile.png`).
- **Pass:** "Official Partner of Phoenix Suns" (sports sponsorship) also appears in the same above-fold trust row — a soft credibility signal.
- **Gap (Medium-High severity):** No regulator/license badge (e.g., FSC, FSA, CySEC-style badge/seal) is visible above the fold on any of the three pages captured. A "Regulation" link exists in the footer navigation (visible in `homepage-desktop-full.png`), but a regulatory credential is arguably the single most important trust signal for a forex/CFD broker and should not require scrolling to the footer to discover — especially on the homepage hero and the accounts/conversion pages where the buying decision is made.
- **Gap (Medium):** No author/reviewer credential visible on the blog post above the fold (see Section 1).

**Recommendation:** Add a compact regulator badge/seal (with license number) into the homepage hero stat row and into the accounts-overview/ECN-account hero, adjacent to the "2015 Established" stat, so the credibility signal a YMYL visitor is most likely to look for is available without scrolling.

---

## Summary of issues by severity

| Severity | Issue | Page(s) |
|---|---|---|
| Medium-High | No above-the-fold regulatory badge/license seal | Homepage, Accounts-overview |
| Medium-High | Chat widget overlaps editorial body text on mobile | Blog |
| Medium | Promo banner consumes ~15-20% of mobile viewport, fixed/persistent | All (mobile) |
| Medium | No visible author/reviewer byline above fold | Blog |
| Low-Medium | Promo banner close ("×") and "Claim" controls under 48px touch target | All (mobile) |
| Low | Trust stats not repeated on conversion page hero | Accounts-overview |
| Low | No swipe indicator on horizontally-scrolling account cards | Accounts-overview (mobile) |
| Low | Busy hero P&L-mockup imagery behind headline (brand-trust nuance, not a legibility bug) | Homepage |
| Pass | Primary CTA above-the-fold visibility (desktop & mobile) | Homepage, Accounts-overview |
| Pass | Viewport meta / no horizontal overflow / no broken grids | All |
| Pass | Nav collapses correctly to hamburger on mobile | All |
| Pass | Primary CTA tap-target sizing | All |

**Overall visual/mobile score: 78/100.**
