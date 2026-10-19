# Valentte email production rules

## Logo: always use the "Aiden logo"

Whenever an email needs the Valentte logo or header, use the **Aiden logo** (the "Aiden Header" in the `valentte-email-production` skill). This applies to every future email, campaign and flow template. Don't rebuild the logo, and don't use any other logo variant.

- **Figma master**: frame `22470:6` "Aiden Header", page "Valentte PPF", file `3HcXPTDNPcYm2CohEsdFjm` (Flow Templates (Copy)). It's 600 × 86: VALENTTE above LONDON, both in Constantia. Clone this frame into the email; never retype it.
- **In Bloomreach**: ship it as one 2x PNG hosted via Higgsfield, never as live text, because Constantia doesn't render in most clients. Use alt text "Valentte London", link it to the homepage, and put `display:block` on the `<a>`.
- If the logo is needed at a different size or layout, ask before changing it. Constantia is a local-only font, so typography edits have to be made by hand in Figma.
