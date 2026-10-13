# Project rules

## Permanent Rule – Dark Mode Compatibility

All emails must be designed and coded to keep their intended appearance in both Light Mode and Dark Mode, on desktop and mobile.

When a recipient has Dark Mode turned on, the email should keep the same colours and styling as closely as the email client allows. Dark Mode must not change, invert or distort the design.

Requirements:

- Text colours stay the same as the Light Mode design wherever the client supports it.
- Background colours stay the same and are never inverted by accident.
- Images, logos, banners and product images keep their original colours.
- Buttons and CTA text keep their intended colours and contrast.
- No text becomes invisible or hard to read because of automatic Dark Mode colour changes.
- Brand colours stay the same across Light and Dark Mode wherever the client allows.

### How to implement (apply to every email template)

1. **Declare a light-only colour scheme** in `<head>` so clients that respect it (Apple Mail, iOS Mail, some Outlook builds) don't apply their own dark palette:
   ```html
   <meta name="color-scheme" content="light only">
   <meta name="supported-color-schemes" content="light only">
   <style>
     :root { color-scheme: light only; supported-color-schemes: light only; }
   </style>
   ```
2. **Set colours explicitly on every element.** Set `bgcolor` and an inline `background-color` on every `<table>`/`<td>` that has a background, and an inline `color` on every text element and link. Never rely on inherited or default colours.
3. **Lock colours back in for clients that force Dark Mode:**
   ```css
   @media (prefers-color-scheme: dark) {
     .bg-brand { background-color: #XXXXXX !important; }
     .text-brand { color: #XXXXXX !important; }
   }
   /* Outlook.com / Outlook apps */
   [data-ogsc] .text-brand { color: #XXXXXX !important; }
   [data-ogsb] .bg-brand { background-color: #XXXXXX !important; }
   ```
   Repeat the Light Mode values here, not new dark values.
4. **Gmail (app and web) fully inverts colours and ignores the CSS above.** To protect key areas:
   - Use background images, or `linear-gradient(#hex,#hex)` backgrounds, on brand-coloured blocks. Gmail doesn't invert these.
   - Put critical branded text (headlines on coloured blocks, offer text) inside the image when exact colour matters, and keep the live text as alt text.
   - Avoid pure `#FFFFFF`/`#000000` where possible (for example `#FEFEFE`/`#111111`). Some clients only invert pure white or black.
5. **Images and logos:**
   - Export logos and icons as PNGs with a transparent background **plus** a thin light outline or glow (or a solid-colour background baked into the image) so they stay visible on both light and dark backgrounds.
   - Product images and banners should have their background colour baked in, not transparent.
   - Always set `alt` text, and give the containing cell an explicit background colour.
6. **Buttons and CTAs:** build them as bulletproof table buttons with `bgcolor` and inline `background-color` on the `<td>` and inline `color` on the `<a>`. Add the same values to the dark-mode lock classes. For CTAs where colour is critical, use an image button with live-text alt.
7. **QA before sending:** test every email in Light and Dark Mode in at least Apple Mail (iOS and macOS), Gmail (iOS, Android and web), and Outlook (Windows, Mac and Outlook.com), using Litmus/Email on Acid or real devices. Check that no text is invisible, no logo disappears, and brand colours match.
