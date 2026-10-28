# Post Purchase 2x – Emails 15–28 · Variant B (test build)

Coded HTML versions of the Figma frames **Email 15 · Variant B** to **Email 28 · Variant B**
(file `3HcXPTDNPcYm2CohEsdFjm`, page "Mia - Automations"), loaded into a Bloomreach test scenario.

## Bloomreach

- Project: Valentte Prod (`2e25bbd8-55a8-11f0-9f79-9aae66778e25`)
- Scenario: **TEST - Post Purchase 2x Purchase - Emails 15-28 (Test B)** (`6ae1cdf3c552bdebd2f2ab6f`), draft
- Flow: now-trigger → condition `email equals mia@valentte.com` → 14 send-email nodes
  (node 2 = Email 15 … node 15 = Email 28), all on `unlimited-policy`.
- Same structure as "TEST - Post Purchase 2x Purchase - Emails 8-14 (Test B)".

## How the HTML is built

- Header: the approved **Aiden Header** logo (Figma frame `22576:10`, exported 2x and hosted on Higgsfield),
  linked to the homepage, plus the live Offers / Home Fragrance / Best Sellers nav.
- Footer: "You may also like" tiles, then the **Zac Footer** from `shell/zac-footer.html`.
  The only change from the reference copy is null-safe, URL-encoded personalisation in the refer-a-friend link,
  e.g. `{{ (customer.first_name or '') | urlencode }}`. Without it, a customer with a null name gets `firstname=None`.
- `emails.py` transcribes each Figma frame section by section using the helpers in `lib.py`
  (live text in Cormorant Garamond / Mulish, orange CTAs, 2x images). Wide two-column rows stack on phones.
- Hero banners (photo, scrim and overlay copy), product photos, icons and the Email 28 gift tag
  were cropped from 2x Figma exports and hosted on Higgsfield. `urls.json` maps each crop to its URL.
- Subject lines and preview text come from each email's "Label B" card in Figma.
- `html/` holds the exact HTML stored in each scenario node, verified byte-for-byte after upload.

## Checks run before upload

- Every visible Figma text string (294) appears verbatim in the HTML.
- Jinja2 render with a normal, a null and a missing first name gives "Hi Mia," / "Hi there," and no `None` anywhere.
- Chromium renders at 640px and 375px show no horizontal overflow and no broken images.
- All 37 distinct web links open with a 200 and land on the intended page.

Rebuild: `python3 -c "import emails; emails.build_all()"` from this folder.

## Notes for review

- Email 20's "Write My Review" goes to `/about-us/customer-reviews/`. The live review flow uses event-bound
  `{{ review_link }}` / `{{ item.url }}`, which a now-trigger test send can't populate.
- Email 18 and 22 "free candle or diffuser over £60" boxes go to `/best-sellers/` (as requested); Bundle & Save CTAs go to `/bundle-save/`.
- Email 16: Patchouli & Eucalyptus replaces Spiced Vanilla & Leather (as requested). Notes and formats come from product knowledge and the live scent page. The card image is a generated ingredients-only flat-lay (no product or text); the Diffuser tile uses the real `dif_pe` photo from Figma.
- The Zac Footer refer link uses a plain situation code (`Bloomreach-Emails-PP2x-E{n}-TestB`). The reference footer's `{{ action['name'] }}` (spaces, brackets) stopped Mention Me's widget loading, so the page came up blank.
- Mobile: images use `max-width:100%` inline and side-by-side cards carry their background on the `<td>`. Both hold in Outlook for iOS, which ignored the descendant CSS rule.
- The Figma Global Header/Footer instances are replaced by the Aiden Header and Zac Footer (see above).
