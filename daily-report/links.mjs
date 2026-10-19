import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs';
const [,, srcDir, dataDir, outDir, ...names] = process.argv;
const PASS = 'Annual Delivery Pass holders', NOPASS = 'everyone else';

// Resolve the Jinja branches: mode 'pass' | 'nopass' | 'both' (both = all branches shown with labels)
function resolve(html, mode) {
  const label = (who) => mode === 'both'
    ? `<tr><td style="font:700 11px/1.3 Arial,sans-serif;color:#305bab;background:#f0f5fd;border:1px dashed #659df2;padding:4px 8px 4px 48px;text-align:left">Dynamic content: shown to ${who}</td></tr>` : '';
  html = html.replace(/\{%\s*if\s+\(customer\.has_delivery_pass[^%]*%\}([\s\S]*?)\{%\s*else\s*%\}([\s\S]*?)\{%\s*endif\s*%\}/g,
    (_, a, b) => mode === 'pass' ? a : mode === 'nopass' ? b : label(PASS) + a + label(NOPASS) + b);
  html = html.replace(/\{%\s*if\s+segmentations\[[^\]]+\]\s*==\s*'(Yes|No)'\s*%\}([\s\S]*?)\{%\s*endif\s*%\}/g,
    (_, yn, body) => mode === 'both' ? label(yn === 'Yes' ? PASS : NOPASS) + body
      : ((yn === 'Yes') === (mode === 'pass') ? body : ''));
  if (/\{%/.test(html)) throw new Error('unresolved jinja');
  if (mode === 'both') html = html.replace(/(<a\s[^>]*href="([^"]*)"[^>]*>)\s*<\/a>/g, (_, open, href) =>
    `${open}<div style="font:600 12px/1.4 Arial,sans-serif;color:#595959;background:#f7f7f7;border:1px dashed #b0b0b0;padding:14px;text-align:center">Banner image missing from saved design<br>${href.replace(/^https?:\/\/[^/]+/, '')}</div></a>`);
  return html.replace(/\{\{[^}]*\}\}/g, '#');
}

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const page = await browser.newPage();
const info = () => [...document.querySelectorAll('a[data-aid]')].map((a, i) => {
  const parts = [];
  for (let el = a; el && el.tagName !== 'BODY'; el = el.parentElement) {
    const tag = el.tagName.toLowerCase(); if (tag === 'tbody') continue;
    const sibs = [...el.parentElement.children].filter(s => s.tagName === el.tagName);
    parts.unshift(sibs.length > 1 ? `${tag}[${sibs.indexOf(el) + 1}]` : tag);
  }
  const img = a.querySelector('img');
  return { aid: a.dataset.aid, order: i, xpath: '//body/' + parts.join('/'), href: a.getAttribute('href'),
    alt: img ? (img.getAttribute('alt') || '') : '', text: a.textContent.replace(/\s+/g, ' ').trim(), img: img ? img.getAttribute('src') : '' };
});
const out = {};
for (const name of names) {
  let n = 0;
  const src = fs.readFileSync(`${srcDir}/${name}.html`, 'utf8').replace(/<a\s/g, () => `<a data-aid="${n++}" `);
  const data = JSON.parse(fs.readFileSync(`${dataDir}/${name}.json`, 'utf8'));
  const rows = data.rows.map(([x, url, v]) => ({ xpath: (data.P + x).replace(/\/tbody/g, ''), url, v }));
  const links = {};
  for (const mode of ['pass', 'nopass']) {
    await page.setContent(resolve(src, mode), { waitUntil: 'domcontentloaded' });
    for (const l of await page.evaluate(info)) {
      const cands = rows.filter(r => r.xpath === l.xpath);
      const row = cands.find(r => r.url === l.href) || cands.find(r => r.url === '*');
      links[l.aid] = links[l.aid] || { ...l, v: 0, modes: [] };
      if (row && !row.used) { row.used = true; links[l.aid].v += row.v; }
      links[l.aid].modes.push(mode);
    }
  }
  out[name] = Object.values(links).sort((a, b) => a.order - b.order);
}
fs.writeFileSync(outDir + '/links.json', JSON.stringify(out, null, 1));
await browser.close();
