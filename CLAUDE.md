# Email template rules

## Delivery Pass strips (permanent rule)

When a reference email has strip headlines about the delivery pass (e.g. "You've got free delivery!" /
"Your Unlimited Delivery Pass is live", "Want free delivery?" / "Unlimited Delivery Pass"):

- Do NOT build a B&W wireframe version of those strips.
- Use the two real banner images from Dropbox, as-is, as the two strips:
  `/Valentte's shared workspace/Email Marketing/2026 Email Marketing/Annual Delivery Pass Banners`
  (https://www.dropbox.com/home/Valentte's%20shared%20workspace/Email%20Marketing/2026%20Email%20Marketing/Annual%20Delivery%20Pass%20Banners)
  - `3.png` = strip 1 ("You've got free delivery!"), `4.png` = strip 2 ("Want free delivery?"). Both 900×90, place at 600×60.
- Place them full-width (600px) in the same position and order as in the reference email.
- Applies to every new template and to existing B&W templates in Figma
  (file `3HcXPTDNPcYm2CohEsdFjm`, page "mia").

## "You May Also Like" section (permanent rule)

Every B&W template gets the real "You May Also Like" section, not a placeholder:

- Divider line, then heading "You May Also Like…" (Inter 22, centred).
- Three full-width image tiles (197×200 each, 4px gaps) using the real images from the
  reference email in Figma (file `3HcXPTDNPcYm2CohEsdFjm`, node `21418:3`, page "mia"):
  1. Reed diffuser with rosemary → label `OFFERS  ▶`
  2. Refill bottle with roses and reeds → label `REFILLS  ▶`
  3. Citrus (oranges, lemon, mint) → label `SHOP BY SCENT  ▶`
- Labels: Inter 11, #333333, centred under each tile.
- Quickest way to add it: copy the finished `You May Also Like` frame from an existing template
  (e.g. "Evening Email 2x2 – B&W Template") rather than re-cropping the images.
- If higher-resolution originals of these three photos turn up in Dropbox, swap them in.

## "Refer a friend" footer link (permanent rule)

In every email (new builds and existing ones, including anything that reuses the Zac Footer):

- The "refer a friend" link's href must be exactly `https://valentte.com/refer-a-friend/`
- No query parameters at all. Strip `email`, `firstname`, `surname`, `situation`, `locale`, `segment`,
  `utm_source`, `utm_campaign`, `utm_medium` and anything else. Every recipient lands on the same plain page.
- The canonical Zac Footer still carries the old personalised URL, so replace it every time the footer is pasted in.
