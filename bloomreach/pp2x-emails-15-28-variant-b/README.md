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

- `shell/` holds the standard Valentte header/nav and footer, taken unchanged from the Email 8–14 Test B nodes.
  Only the preheader and the refer-a-friend `situation=Bloomreach-Emails-PP2x-E{n}-TestB` code change per email.
- `emails.py` transcribes each Figma frame section by section using the helpers in `lib.py`
  (live text in Cormorant Garamond / Mulish, orange CTAs, 2x images).
- Hero banners (photo + scrim + overlay copy), product photos, icons and the Email 28 gift tag
  were cropped from 2x Figma exports and hosted on Higgsfield; `urls.json` maps each crop to its URL.
- Subject lines and preview text come from each email's "Label B" card in Figma.
- `html/` is the exact HTML stored in each scenario node (verified byte-for-byte after upload).

Rebuild: `python3 -c "import emails; emails.build_all()"` from this folder.

## Notes for review

- Email 20's "Write My Review" goes to `/about-us/customer-reviews/`. The live review flow uses event-bound
  `{{ review_link }}` / `{{ item.url }}`, which a now-trigger test send can't populate.
- Email 18/22 free-gift links go to `/free-gifts/`; Bundle & Save CTAs go to `/bundle-save/`.
- The Figma Global Header/Footer instances are replaced by the live Bloomreach header/footer, as in Emails 8–14.
