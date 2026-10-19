import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs';
const [,, emailsDir, outDir] = process.argv;
const clicks = JSON.parse(fs.readFileSync(new URL('./clicks.json', import.meta.url)));
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const page = await browser.newPage({ viewport: { width: 640, height: 900 }, deviceScaleFactor: 2 });
for (const [name, map] of Object.entries(clicks)) {
  const html = fs.readFileSync(`${emailsDir}/${name}.html`, 'utf8').replace(/\{\{[^}]*\}\}/g, '#');
  await page.setContent(html, { waitUntil: 'networkidle', timeout: 60000 });
  const total = await page.evaluate((map) => {
    const key = (h) => { try { const u = new URL(h); if (u.hostname.includes('facebook')) return 'facebook'; if (u.hostname.includes('instagram')) return 'instagram'; if (u.hostname.includes('tiktok')) return 'tiktok'; if (u.hostname.endsWith('valentte.com')) return u.pathname; } catch {} return null; };
    const links = [...document.querySelectorAll('a[href]')].map(a => ({ a, k: key(a.href) })).filter(x => x.k && x.k in map);
    const counts = {}; links.forEach(x => counts[x.k] = (counts[x.k] || 0) + 1);
    const max = Math.max(...Object.values(map));
    document.body.style.position = 'relative';
    for (const { a, k } of links) {
      const r = a.getBoundingClientRect(); if (r.width < 2 || r.height < 2) continue;
      const v = map[k], t = v / max;
      const hue = 60 - 60 * t; // yellow -> red
      const box = document.createElement('div');
      Object.assign(box.style, { position: 'absolute', left: r.left + scrollX + 'px', top: r.top + scrollY + 'px', width: r.width + 'px', height: r.height + 'px', background: `hsla(${hue},95%,50%,${0.18 + 0.32 * t})`, outline: `2px solid hsl(${hue},95%,42%)`, pointerEvents: 'none', zIndex: 9998 });
      const b = document.createElement('div');
      b.textContent = v.toLocaleString('en-GB') + (counts[k] > 1 ? '*' : '');
      Object.assign(b.style, { position: 'absolute', right: '2px', top: '2px', background: `hsl(${hue},95%,38%)`, color: '#fff', font: '700 13px/1 Arial,sans-serif', padding: '4px 6px', borderRadius: '10px', boxShadow: '0 1px 3px rgba(0,0,0,.4)' });
      box.appendChild(b); document.body.appendChild(box);
    }
    return Object.keys(counts).length;
  }, map);
  await page.screenshot({ path: `${outDir}/${name}.png`, fullPage: true });
  console.log(name, 'links badged:', total);
}
await browser.close();
