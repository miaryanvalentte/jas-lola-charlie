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
  html = html.replace(/\{%\s*if\s+customer\.first_name\s*%\}[\s\S]*?\{%\s*else\s*%\}([\s\S]*?)\{%\s*endif\s*%\}/g, (_, b) => b);
  if (/\{%/.test(html)) throw new Error('unresolved jinja');
  if (mode === 'both') html = html.replace(/(<a\s[^>]*href="([^"]*)"[^>]*>)\s*<\/a>/g, (_, open, href) =>
    `${open}<div style="font:600 12px/1.4 Arial,sans-serif;color:#595959;background:#f7f7f7;border:1px dashed #b0b0b0;padding:14px;text-align:center">Banner image missing from saved design<br>${href.replace(/^https?:\/\/[^/]+/, '')}</div></a>`);
  return html.replace(/\{\{[^}]*\}\}/g, '#');
}

const STOPS = [[0,'#fff6cc'],[.12,'#fde1bf'],[.21,'#fcd0b6'],[.30,'#fbbfac'],[.67,'#f67d87'],[1,'#f24567']];
function color(t) {
  const hex = (h) => [1,3,5].map(i => parseInt(h.slice(i, i + 2), 16));
  for (let i = 1; i < STOPS.length; i++) if (t <= STOPS[i][0]) {
    const [t0, c0] = STOPS[i - 1], [t1, c1] = STOPS[i], f = (t - t0) / (t1 - t0);
    const a = hex(c0), b = hex(c1);
    return '#' + a.map((v, k) => Math.round(v + (b[k] - v) * f).toString(16).padStart(2, '0')).join('');
  }
  return STOPS.at(-1)[1];
}

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const page = await browser.newPage({ viewport: { width: 640, height: 900 }, deviceScaleFactor: 2 });
const xpathOf = () => [...document.querySelectorAll('a[data-aid]')].map(a => {
  const parts = [];
  for (let el = a; el && el.tagName !== 'BODY'; el = el.parentElement) {
    const tag = el.tagName.toLowerCase();
    if (tag === 'tbody') continue;
    const sibs = [...el.parentElement.children].filter(s => s.tagName === el.tagName);
    parts.unshift(sibs.length > 1 ? `${tag}[${sibs.indexOf(el) + 1}]` : tag);
  }
  return { aid: a.dataset.aid, xpath: '//body/' + parts.join('/'), href: a.getAttribute('href') };
});

for (const name of names) {
  let n = 0;
  const src = fs.readFileSync(`${srcDir}/${name}.html`, 'utf8').replace(/<a\s/g, () => `<a data-aid="${n++}" `);
  const data = JSON.parse(fs.readFileSync(`${dataDir}/${name}.json`, 'utf8'));
  const norm = (x) => x.replace(/\/tbody/g, '');
  const rows = data.rows.map(([x, url, v]) => ({ xpath: norm(data.P + x), url, v, aids: new Set() }));
  for (const mode of ['pass', 'nopass']) {
    await page.setContent(resolve(src, mode), { waitUntil: 'domcontentloaded' });
    for (const { aid, xpath, href } of await page.evaluate(xpathOf)) {
      const cands = rows.filter(r => r.xpath === xpath);
      const row = cands.find(r => r.url === href) || cands.find(r => r.url === '*');
      if (row) row.aids.add(aid);
    }
  }
  const counts = {}, unmatched = [];
  for (const r of rows) {
    if (!r.aids.size) { unmatched.push(r); continue; }
    if (r.aids.size > 1) console.warn('  row maps to several links', r.xpath, [...r.aids]);
    const aid = [...r.aids][0]; counts[aid] = (counts[aid] || 0) + r.v;
  }
  const max = Math.max(...Object.values(counts));
  await page.setContent(resolve(src, 'both'), { waitUntil: 'networkidle', timeout: 60000 });
  const hidden = await page.evaluate(({ counts, max, colors }) => {
    const hidden = [];
    for (const a of document.querySelectorAll('a[data-aid]')) {
      const v = counts[a.dataset.aid] || 0;
      const r = a.getBoundingClientRect();
      if (r.width < 2 || r.height < 2) { if (v) hidden.push([a.getAttribute('href'), v]); continue; }
      const c = v ? colors[a.dataset.aid] : '#8695b2';
      const box = document.createElement('div');
      Object.assign(box.style, { position: 'absolute', left: r.left + scrollX - 2 + 'px', top: r.top + scrollY - 2 + 'px', width: r.width + 4 + 'px', height: r.height + 4 + 'px',
        border: `2px solid ${c}`, background: c + (v ? '55' : '22'), boxSizing: 'border-box', pointerEvents: 'none', zIndex: 9998 });
      const tag = document.createElement('div');
      tag.textContent = v.toLocaleString('en-GB');
      Object.assign(tag.style, { position: 'absolute', left: '-2px', top: '-17px', background: c, color: (!v || v / max >= 0.5) ? '#fff' : '#1a1a1a',
        font: '600 11px/1 Arial,sans-serif', padding: '2px 5px', borderRadius: '2px', whiteSpace: 'nowrap' });
      box.appendChild(tag); document.body.appendChild(box);
    }
    return hidden;
  }, { counts, max, colors: Object.fromEntries(Object.entries(counts).map(([k, v]) => [k, color(v / max)])) });
  await page.screenshot({ path: `${outDir}/${name}.png`, fullPage: true });
  const total = Object.values(counts).reduce((a, b) => a + b, 0);
  console.log(name, '| links with clicks:', Object.keys(counts).length, '| clicks placed:', total, '| unmatched rows:', JSON.stringify(unmatched.map(r => [r.xpath, r.v])), '| hidden:', JSON.stringify(hidden));
}
await browser.close();
