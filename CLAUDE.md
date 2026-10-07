# Valentte email rules

## Every email imported, built or edited in Bloomreach

Before writing any email campaign's `jinja_html` back to Bloomreach (project "Valentte Prod",
`2e25bbd8-55a8-11f0-9f79-9aae66778e25`), run it through the product-grid fixer:

```
python3 tools/fix_product_grid.py in.html out.html
```

- It rebuilds 2-column product grids (image / title / Was-Now price / Shop Now button per cell)
  into one-row-per-part tables so prices and buttons line up on mobile no matter how many lines
  each product name wraps to, shrinks grid titles on phones, and stops "Shop Now →" wrapping.
- It also adds `box-sizing:border-box` to `.stack-col` rules that stack columns at 100% width,
  otherwise padded cells come out wider than the phone and the whole email pans sideways.
- It points every "Shop by scent" link (`valentte.com/shop-by-scent/`) at
  `https://valentte.com/all-scents/`.
- It only touches grids of that exact shape; zig-zag layouts that stack on mobile are left alone.
  It is safe to run more than once.
- If it prints the escaped-HTML warning, the Bloomreach visual editor has turned a block
  (usually the `has_delivery_pass` strip) into literal `&lt;tr&gt;` text that customers would
  see as raw code. Move the unescaped block back to its place inside the main `.wrap` table.

Follow the `valentte-email-production` skill's `update_email_campaign` safety steps: fetch with
`include_design=True`, diff before/after, re-fetch after writing and `cmp` the stored HTML.

Pre-change copies of edited campaigns live in `backups/`.
