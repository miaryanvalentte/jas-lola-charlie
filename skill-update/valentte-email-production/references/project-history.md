# Project History & Current State — Valentte Email Production

This is the accumulated context from the session that built out this workflow, kept so a teammate (or a future session) doesn't have to rediscover it. Load this when you need to know *what already exists* rather than just *how to build*.

## 1. Daily/promotional email — "v4 test"

- **Bloomreach project**: "Valentte Prod", project id `2e25bbd8-55a8-11f0-9f79-9aae66778e25`.
- **Campaign**: name **"v4 test"**, id `6ab516748e342c33687f7c80`, status draft. This is a coded (live-HTML) reproduction of a real, already-sent Valentte campaign ("Cosy Just Got An Upgrade"), matching it section-for-section.
- Structure: header/nav → two 2-column image+text promo strips → two full-bleed baked-text hero banners (photo with headline/badge/CTA baked directly onto it, boolean-subtract wave at the bottom of each) → Pick & Mix section → wave divider → baked-text review/testimonial banner → baked-text "Offer of the Day" banner (black ribbon, price, badge) → wave divider → Christmas Hamper (2-col, untouched per explicit user sign-off) → wave dividers → "You may also like" → referral bar → checkout-trust image (real cloned/sourced payment + trust icons, not text) → footer.
- **Fonts**: Cardo (serif, headings) + Inter (sans, body) — confirmed from valentte.com's own live CSS, not guessed.
- **Known open item**: Clearpay has no dedicated icon in any free icon set found; the Afterpay mark (same parent company) was used as a stand-in and flagged as not exact.
- **Hard-won gotcha, already burned once**: when updating this campaign, the top-level `design` field is authoritative and the backend rebuilds `split` from it — a payload with a placeholder/stub value in `jinja_html` briefly wiped the live campaign body mid-session. Always re-verify the fetched-back content before considering an update done.

## 2. Post-purchase flow B&W wireframes

- **Figma file**: "Flow Templates (Copy)", file key `3HcXPTDNPcYm2CohEsdFjm`.
- **Page**: "Valentte PPF" (page id `21052:17`), created specifically for this work.
- Contents, left to right on that page:
  - A row of 21 real reference images (Valentte's actual post-purchase flow, sourced from `~/Downloads/Post purchase flow/`), each scaled to 350px wide, named `1`, `2`, `3`...`14b`.
  - Below that row: 21 B&W wireframe frames (`PPF-01-BW` through `PPF-14b-BW`), each positioned directly under its matching reference image, rebuilt structurally faithful to the real design (correct section order/proportions, real 3-row zigzag timelines with connector lines + node circles, image-placeholder-with-overlaid-text for any section where the original bakes text onto a photo).
  - Below that: **5 "ideal flow" templates** (`PPF-Ideal-1a`, `-1b`, `-1c`, `-1d`, `-2`), inspired by/partly cloned from a separate reference page in the same file (see below), each structurally distinct: 1a = welcome + product grid + "why it works", 1b = referral-emphasis + single product highlight, 1c = feature grid + numbered benefits + a social-proof stats row (real approved Valentte proof points: 1M+ happy customers, 350K+ 5-star reviews, 8x stronger scent), 1d = VIP perks checklist card + "how to redeem" card (no product grid), 2 = usage-instruction table cards (Reed Diffuser / Candle), cloned from a real dosage-table pattern found in the reference library.
- **Reference/source page** (same file): a page named "Post Purchase" (page id `14:32329`) — a strategy map + curated swipe library, NOT something to edit, only to read/clone from. Contains: a literal flowchart of canonical flow logic (`Trigger → 1a → split by purchase count → 1b/1c/1d → Email 2`), three "Great Examples" sections of real curated screenshots, a "Bonus Templates" section (all from one real brand, LivFresh/Livionex), and four industry-vertical example collages (CPG, Health & Beauty, General, Fashion & Apparel). The diagonal-cut hero shape and the real Facebook/Instagram icon vectors used in the 5 ideal templates were cloned directly from a B&W frame in this page's "Email 1 Great Examples" section (source frame id `238:237`).

## 3. Standing technique notes
See the sibling memory file / the main SKILL.md in this skill for the boolean-subtract wave-divider technique and the `update_email_campaign` safety checklist — those are written as durable rules, not just history, so they live in the main skill body rather than here.

## 4. Approved asset library — Dropbox (confirmed accessible)

Two Dropbox folders are the canonical source of real, approved Valentte product photography — confirmed directly browsable via the connected `dropbox` MCP account (not just a broken public share link):

- `/Valentte's shared workspace/Email Marketing/2026 Email Marketing/Templates/AI raw` — older, curated (~22 subfolders).
- `/Valentte's shared workspace/x- temp email images` — larger, fresher (~45 subfolders, most added the same day), organized by exact product name. Check here first for anything product-specific.

Use these as the default source for (a) any plain "get me a real photo of X" request, and (b) the reference image fed into Higgsfield for Tier-2 reference-edit generations — not whatever photo happens to already be sitting in a Figma frame from prior wireframe work. Full rule lives in the main SKILL.md's Higgsfield section.

## 5. Higgsfield AI generation — added this phase
The `valentte-email-production` skill was substantially rewritten to add a full Higgsfield AI-image-generation section, after three real content bugs surfaced this project (a fabricated scent-name line, a corrupted "VALENTTE LONDON" wordmark, a fabricated URL — all on reference-edited product photos, all only caught by eye, not by the prompt). Read that section in the main SKILL.md before generating anything — it has the three-tier content-risk rule (safe to blank-slate vs reference-edit-only vs never-generate) and the cost-tracking discipline (never diff shared `balance`).

## 6. Open/unresolved items as of this session
- The `valentte-email-production` skill itself is only local to Aiden's machine — needs distribution (shared repo `.claude/skills/` folder, or org skill sync) before teammates can use it.
- A leaner alternative 5-template structure was discussed (collapsing 1b/1c into one "repeat customer" email, freeing a slot for something closer to Valentte's real flow) but not built — flagged as a live design opinion, not yet actioned.

## 7. Cart-abandon flow — 4 MCP-built emails, audited and fixed

- **Bloomreach project**: "Valentte Prod", project id `2e25bbd8-55a8-11f0-9f79-9aae66778e25` (same project as everything else in this skill).
- **Live standalone campaigns** (each a full HTML template, all `status: draft`):
  - **Email 1** "Cart Abandon · Short", id `6abbada37f16fb593993072d` — uses the Zac Footer (see main SKILL.md).
  - **Email 2** "Cart Abandon · Email 2 · Founders (text)", id `6abcf1a00c332acb697d1ace` — plain-text style, no footer/nav/images at all.
  - **Email 3** "Cart Abandon · Email 3 · Mystery Gift", id `6abcfd78a9600d29ec1167fb` — uses the Zac Footer (this campaign's footer was the *source* of the Zac Footer fixes — its footer was already closer to correct and was copied into Email 1).
  - **Email 4** "Cart Abandon · Email 4 · Last Chance (text)", id `6abd18febbf6271037701a62` — plain-text style, no footer/nav/images at all.
- **Test scenario**: "Simple Test - All 4 Emails - Aiden Only", scenario id `6abfa8dc999aafa3dbd616f1` — a standalone 4-branch scenario (not the real production flow), built specifically to validate all 4 emails end-to-end with real event data. All 4 branches trigger off the real `cart_update` event (not a fabricated custom event type — see the "never trust manual test-send" rule in the main SKILL.md for why), each gated by an `email equals aiden@valentte.com` condition, each with `frequency_policy: unlimited-policy` so test sends never suppress each other via shared quota.
- **Real production flow** this work feeds into: scenario "LB - Abandoned Cart Email and SMS", id `6a29272afdb92a4736dde32f`, status active. The 4 finished send-email nodes were copied in as new nodes (ids 285–288) but **deliberately left disconnected** pending a manual decision on whether they replace the existing "Abandon Cart - Email 1/2a/.../4b" touch sequence (nodes 259, 260, etc.) or run in parallel. Copying only the send-email nodes (not the scoping condition) means they currently have **no audience scoping of their own** — whoever wires them in must either reuse the existing branch's upstream gating (if replacing in place) or add an explicit condition (if adding a new parallel path). Their `frequency_policy` was set to `"Abandoned Email Policy"` to match the existing touch-sequence convention (shared quota bucket — same pool as nodes 259/260 and ~10 other touches; confirmed by exact-name match, not assumed).
- **All issues found and fixed across these 4 emails** are written up as durable, generalized rules in the main SKILL.md's "Footer & link-integrity checklist" section — not just a changelog here. That section is the one to read before building or auditing any future footer.
- **Near-miss worth remembering**: mid-fix, a background agent briefly pushed the literal placeholder text `"FILE:/tmp/..."` into the live Email 1 campaign body instead of the real HTML (a file-path reference used as a shortcut instead of materializing the actual content). Caught immediately on the next re-fetch/diff and corrected. Reinforces the existing "sanity-check before send, re-fetch after" rule in the main SKILL.md — large payloads must have their real content read back into context before submission, never referenced by path.
