# Post Purchase - Returning Customers: link fixes checklist

Scenario: https://uk1.eng.bloomreach.com/p/valentte-prod/campaigns/campaign-designs/6a181ffd0253fbf25716e701

## 1. One-off fixes (5 emails)

| Email | Change |
|---|---|
| 2x Email 4 (Test A) | "Why choose just 1… try 5" banner link: `https://valentte.com/organic/discovery-scent-set/` → `https://valentte.com/organic/mini-room-mists/` |
| 3x Email 4 (Test A) | same as above |
| 2x Email 24 (Test A) | "Spiced Vanilla & Leather Candle" image link: `https://valentte.com/organic/candle-spiced-vanilla-leather/` → `https://valentte.com/shop-by-scent/spiced-vanilla-leather/` |
| 3x Email 24 (Test A) | same as above |
| 3x Email 25 (Test A) | "Shop Pineapple & Mango" image: add link `https://valentte.com/shop-by-scent/pineapple-mango/` (currently empty) |

## 2. Footer fixes (same 3 edits in each email below)

In the footer of each email:

- Phone image link: `08000869311` → `tel:08000869311`
- Email image link: `support@valentte.com` → `mailto:support@valentte.com`
- Hidden link before "Unsubscribe" (`http://valentte.com/help/email-preference-center/?email={{ email }}`, a 404): change to `{{ email.unsubscribe }}` (in Beefree it's an empty link in the text "Click here to Unsubscribe")

Emails (82):

- [ ] Post Purchase 2x Purchase - Email 1 (Test A)
- [ ] Post Purchase 2x Purchase - Email 1 (Test B)
- [ ] Post Purchase 2x Purchase - Email 2 (Test A)
- [ ] Post Purchase 2x Purchase - Email 2 (Test B)
- [ ] Post Purchase 2x Purchase - Email 3 (Test A)
- [ ] Post Purchase 2x Purchase - Email 3 (Test B)
- [ ] Post Purchase 2x Purchase - Email 4 (Test A)
- [ ] Post Purchase 2x Purchase - Email 4 (Test B)
- [ ] Post Purchase 2x Purchase - Email 5 (Test A)
- [ ] Post Purchase 2x Purchase - Email 5 (Test B)
- [ ] Post Purchase 2x Purchase - Email 6 (Test A)
- [ ] Post Purchase 2x Purchase - Email 6 (Test B)
- [ ] Post Purchase 2x Purchase - Email 7 (Test A)
- [ ] Post Purchase 2x Purchase - Email 7 (Test B)
- [ ] Post Purchase 2x Purchase - Email 8 (Test A)
- [ ] Post Purchase 2x Purchase - Email 8 (Test B)
- [ ] Post Purchase 2x Purchase - Email 9 (Test A)
- [ ] Post Purchase 2x Purchase - Email 9 (Test B)
- [ ] Post Purchase 2x Purchase - Email 10 (Test A)
- [ ] Post Purchase 2x Purchase - Email 10 (Test B)
- [ ] Post Purchase 2x Purchase - Email 11 (Test A)
- [ ] Post Purchase 2x Purchase - Email 11 (Test B)
- [ ] Post Purchase 2x Purchase - Email 12 (Test A)
- [ ] Post Purchase 2x Purchase - Email 12 (Test B)
- [ ] [08.06] Post Purchase 2x Purchase - Email 13A
- [ ] Post Purchase 2x Purchase - Email 14 (Test A)
- [ ] Post Purchase 2x Purchase - Email 14 (Test B)
- [ ] Post Purchase 2x Purchase - Email 15 (Test A)
- [ ] Post Purchase 2x Purchase - Email 16 (Test A)
- [ ] Post Purchase 2x Purchase - Email 17 (Test A)
- [ ] Post Purchase 2x Purchase - Email 18 (Test A)
- [ ] Post Purchase 2x Purchase - Email 19 (Test A)
- [ ] [12.06] Post Purchase 2x Purchase - Email 20
- [ ] Post Purchase 2x Purchase - Email 21 (Test A)
- [ ] Post Purchase 2x Purchase - Email 22 (Test A)
- [ ] Post Purchase 2x Purchase - Email 23 (Test A)
- [ ] Post Purchase 2x Purchase - Email 24 (Test A)
- [ ] Post Purchase 2x Purchase - Email 25 (Test A)
- [ ] Post Purchase 2x Purchase - Email 26 (Test A)
- [ ] Post Purchase 2x Purchase - Email 27 (Test A)
- [ ] Post Purchase 2x Purchase - Email 28 (Test A)
- [ ] Post Purchase 3x Purchase - Email 1 (Test A)
- [ ] Post Purchase 3x Purchase - Email 1 (Test B)
- [ ] Post Purchase 3x Purchase - Email 2 (Test A)
- [ ] Post Purchase 3x Purchase - Email 2 (Test B)
- [ ] Post Purchase 3x Purchase - Email 3 (Test A)
- [ ] Post Purchase 3x Purchase - Email 3 (Test B)
- [ ] Post Purchase 3x Purchase - Email 4 (Test A)
- [ ] Post Purchase 3x Purchase - Email 4 (Test B)
- [ ] Post Purchase 3x Purchase - Email 5 (Test A)
- [ ] Post Purchase 3x Purchase - Email 5 (Test B)
- [ ] Post Purchase 3x Purchase - Email 6 (Test A)
- [ ] Post Purchase 3x Purchase - Email 6 (Test B)
- [ ] Post Purchase 3x Purchase - Email 7 (Test A)
- [ ] Post Purchase 3x Purchase - Email 7 (Test B)
- [ ] Post Purchase 3x Purchase - Email 8 (Test A)
- [ ] Post Purchase 3x Purchase - Email 8 (Test B)
- [ ] Post Purchase 3x Purchase - Email 9 (Test A)
- [ ] Post Purchase 3x Purchase - Email 9 (Test B)
- [ ] Post Purchase 3x Purchase - Email 10 (Test A)
- [ ] Post Purchase 3x Purchase - Email 10 (Test B)
- [ ] Post Purchase 3x Purchase - Email 11 (Test A)
- [ ] Post Purchase 3x Purchase - Email 11 (Test B)
- [ ] Post Purchase 3x Purchase - Email 12 (Test A)
- [ ] Post Purchase 3x Purchase - Email 12 (Test B)
- [ ] [08.06] Post Purchase 3x Purchase - Email 13A
- [ ] Post Purchase 3x Purchase - Email 14 (Test A)
- [ ] Post Purchase 3x Purchase - Email 14 (Test B)
- [ ] Post Purchase 3x Purchase - Email 15 (Test A)
- [ ] Post Purchase 3x Purchase - Email 16 (Test A)
- [ ] Post Purchase 3x Purchase - Email 17 (Test A)
- [ ] Post Purchase 3x Purchase - Email 18 (Test A)
- [ ] Post Purchase 3x Purchase - Email 19 (Test A)
- [ ] [12.06] Post Purchase 3x Purchase - Email 20
- [ ] Post Purchase 3x Purchase - Email 21 (Test A)
- [ ] Post Purchase 3x Purchase - Email 22 (Test A)
- [ ] Post Purchase 3x Purchase - Email 23 (Test A)
- [ ] Post Purchase 3x Purchase - Email 24 (Test A)
- [ ] Post Purchase 3x Purchase - Email 25 (Test A)
- [ ] Post Purchase 3x Purchase - Email 26 (Test A)
- [ ] Post Purchase 3x Purchase - Email 27 (Test A)
- [ ] Post Purchase 3x Purchase - Email 28 (Test A)

## 3. Referral tracking tag (3x Test B emails)

In every refer-a-friend link, change `situation=Bloomreach-Emails-PP2x-E` to `situation=Bloomreach-Emails-PP3x-E` (keep the email number). Easiest in the HTML editor with find & replace.

Emails (20):

- [ ] Post Purchase 3x Purchase - Email 8 (Test B)
- [ ] Post Purchase 3x Purchase - Email 9 (Test B)
- [ ] Post Purchase 3x Purchase - Email 10 (Test B)
- [ ] Post Purchase 3x Purchase - Email 11 (Test B)
- [ ] Post Purchase 3x Purchase - Email 12 (Test B)
- [ ] Post Purchase 3x Purchase - Email 14 (Test B)
- [ ] Post Purchase 3x Purchase - Email 15 (Test B)
- [ ] Post Purchase 3x Purchase - Email 16 (Test B)
- [ ] Post Purchase 3x Purchase - Email 17 (Test B)
- [ ] Post Purchase 3x Purchase - Email 18 (Test B)
- [ ] Post Purchase 3x Purchase - Email 19 (Test B)
- [ ] Post Purchase 3x Purchase - Email 20 (Test B)
- [ ] Post Purchase 3x Purchase - Email 21 (Test B)
- [ ] Post Purchase 3x Purchase - Email 22 (Test B)
- [ ] Post Purchase 3x Purchase - Email 23 (Test B)
- [ ] Post Purchase 3x Purchase - Email 24 (Test B)
- [ ] Post Purchase 3x Purchase - Email 25 (Test B)
- [ ] Post Purchase 3x Purchase - Email 26 (Test B)
- [ ] Post Purchase 3x Purchase - Email 27 (Test B)
- [ ] Post Purchase 3x Purchase - Email 28 (Test B)
