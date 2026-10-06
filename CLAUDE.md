# Valentte email production – standing preferences

## Product images must match the email's look and feel (always)

When building any email (e.g. the daily Evening emails in Figma file `3HcXPTDNPcYm2CohEsdFjm`),
never drop plain white-background studio cutouts into product cells. Always restyle every
product image so it belongs to the same scene, lighting and palette as that email's hero
and theme (e.g. a cosy candlelit evening, autumn, Christmas).

How:
- Source the real product photo from Dropbox (`/Valentte's shared workspace/x- temp email images/...`).
- Reference-edit it with Higgsfield `generate_image` (`gpt_image_2_5`, `image_references` role),
  prompting only for scene/lighting/props and forbidding any new or changed text/labels.
- Use a consistent scene prompt across all products in the email so the grid reads as one set.
- Zoom in on every output and check labels/wordmarks before using it; regenerate if any text is altered.
