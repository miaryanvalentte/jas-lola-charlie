// Screenshot every flowmap/html/<hash>.html to flowmap/images/<hash>.jpg (600px wide, full length).
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const HERE = __dirname;
const MAX_H = 6000;

(async () => {
  const files = fs.readdirSync(path.join(HERE, 'html')).filter(f => f.endsWith('.html'));
  fs.mkdirSync(path.join(HERE, 'images'), { recursive: true });
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 600, height: 900 }, deviceScaleFactor: 1 });
  let done = 0, failed = [];
  const queue = [...files];
  async function worker() {
    const page = await ctx.newPage();
    while (queue.length) {
      const f = queue.shift();
      const out = path.join(HERE, 'images', f.replace('.html', '.jpg'));
      try {
        await page.goto('file://' + path.join(HERE, 'html', f), { waitUntil: 'load', timeout: 45000 });
        await page.waitForTimeout(500);
        const h = await page.evaluate(() => { let m = Math.max(document.body ? document.body.scrollHeight : 0, document.documentElement.scrollHeight); for (const el of document.querySelectorAll('body *')) { const r = el.getBoundingClientRect(); if (r.bottom > m) m = r.bottom; } return Math.ceil(m); });
        await page.setViewportSize({ width: 600, height: Math.min(h, MAX_H) });
        await page.screenshot({ path: out, type: 'jpeg', quality: 72,
          fullPage: true });
        done++;
      } catch (e) { failed.push(f + ': ' + e.message.split('\n')[0]); }
    }
    await page.close();
  }
  await Promise.all(Array.from({ length: 6 }, worker));
  await browser.close();
  console.log('rendered', done, 'failed', failed.length);
  failed.forEach(x => console.log('  ', x));
})();
