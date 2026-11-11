# Daily email report – 5:48am (Europe/London)

Each morning, report **yesterday's** three newsletter sends (AM 7am, PM 3pm, Evening 6pm).

## 1. Data (Bloomreach / Loomi)

- Project `2e25bbd8-55a8-11f0-9f79-9aae66778e25`. EQL is rate-limited: 1 query per ~3s, retry on 429.
- Campaign name: `dd/mm/yy Newsletter`. Action names: `AM Email dd/mm/yy`, `PM Email dd/mm/yy`, `Evening Email dd/mm/yy`;
  subject-line tests are `AM Email dd/mm/yy - Title Test A` / `- Title Test B` (on 15/10 they were `- Test A` / `- Test B`).
- **Delivered / opens / unique clicks**: per action name. Unique clicks = `count first event campaign where .status = "clicked"`
  (Bloomreach standard, no bot filter – this matches the team's "Winning Titles" sheet).
- **Click maps**: use reliable clicks (`.bot has no value`), counted per xpath × url, then render with `heatmap.mjs`.
- **Check for unexpected sends**: list every action that delivered yesterday (`count event campaign where .status="delivered"` grouped by action name),
  not just yesterday's own names. A send from another day's scenario (e.g. `Evening Email 21/10/26` going out on 19/10 because a
  planned trigger kept an old date) must be reported separately and flagged at the top of the write-up; keep it out of the day totals.
- **Visitors** (Metrilo-style): `count first event session_start` where `.utm_campaign` = exact email name, send day only (UK time).
  From 25 Oct 2026 the UK is on GMT: the day runs 00:00Z–24:00Z (Sun 25 was 23:00Z–24:00Z next day) and the
  orders/revenue funnel windows start at 07:00Z (AM), 15:00Z (PM) and 18:00Z (Evening) until 24:00Z.
  Some visits are tagged with `+` for spaces (`AM+Email+20/10/26+-+Title+Test+A`): count both spellings, and use
  `.utm_campaign is in [...]` with both spellings in the orders/revenue funnels.
  If an action name starts with a space (24/10/26 PM tests), the `+` spelling gets a leading `+`
  (`+PM+Email+24/10/26+-+Title+Test+A`): check the visitors query and add those spellings too.
- **Sanity check**: if a send's visitors are far below its clicks, check site activity by hour (`count event session_start`,
  `count event purchase` by hour vs the day before) – on 20/10 a ~7–11am gap meant almost no visits or orders were recorded.
- **Orders / revenue**: `funnel(session_start where .utm_campaign = X followed by purchase in last 3 days within 2 hours)`,
  purchases from send time to 23:00Z same day, sum `total_price`.

## 2. Miro board – https://miro.com/app/board/uXjVEYE5ouI=/

Layout (board units): day x = `-7400 + weekday * 2120` (Mon = 0); each day is 1880 wide; columns 600 wide with 40 gap.
Week rows: w/c 12 Oct y0 = -1064, w/c 19 Oct y0 = 1507, w/c 26 Oct y0 = 4157, w/c 2 Nov y0 = 6807, w/c 9 Nov y0 = 9457 (each new week +2650; grey divider at y0-129, "Week commencing" label at x=-8100). Images go at y0 + 600 up to w/c 2 Nov; **from w/c 9 Nov images go at y0 + 720** to make room for the hero-test panel (see below).
Template text boxes already exist for 19–31 Oct: **update** them (stats box at y0+149, panel at y0+485) – don't create new ones.

Per send column:
- Label `Total – whole audience + tests`; stats = **totals** across whole audience + Test A + Test B
  (open rate weighted by delivered; CTR = clicks/delivered; conv = orders/visitors; AOV = revenue/orders). SL/P1 = whole-audience version.
- Grey panel: `Test A – OR% open · CTR% click rate · N unique clicks: SL / P1`, same for Test B, then
  **`Winner on unique clicks: Test A|B (N vs M unique clicks; whole audience x.xx% click rate)`**.
  From 2 Nov 2026 the winner is the test version (A vs B, ~4,800 each) with more **unique clicks**; the whole-audience
  version (~245k) is shown for reference but is not in the contest. On a tie, the higher open rate wins; say "too close to call" if within 3 clicks.
- Evening: `Whole Audience` stats + "No subject line test on this send."
- Click map: one combined image (whole + tests) 180 wide at the column's left edge, y0 + 600.
  Images: create, then resize needs x, y, width + height in one call, then a second call with x, y only.
- `canvas_create_from_svg` auto-shifts batches that overlap existing items – send small batches and re-position by id if shifted.

## 3. Daily sheet – https://docs.google.com/spreadsheets/d/1Zj1U5HeRFIAcrgLJJiTkmshlRDWIclNkVjyZG2IVzsA

- Tab name: `'Daily totals'` (quote it in ranges). The team's `Weekly totals` tab is theirs – don't edit it.
- 16-column block per day; block start column (1-based) = `2 + 16 * (date − 24 Aug 2026 in days)`.
- To add a day: `appendDimension` 16 columns if needed, `copyPaste` the previous day's block (rows 1–11) to the new block,
  then write the header (row 1, e.g. `Monday 19th October 2026 `, trailing space) and inputs only:
  rows 4 Delivered, 5 Unique Clicks, 7 Visitors, 8 Orders, 10 Revenue, at block offsets 0 (AM), 4 (PM), 8 (Evening).
  Everything else is formulas. Values are totals incl. tests.

## 4. Winning titles sheet – https://docs.google.com/spreadsheets/d/1C8Ia61-CjHfehDDHZoB9-Xfzo6qSgctYwEmzN2crARE

Tab `Title Tests` (renamed from Sheet1 on 9 Nov). Columns: A `Day - dd/mm/yy AM|PM`, B `SL - P1` of the winner on unique clicks (Test A vs Test B), C click rate (2 dp, no % sign), D open rate.

Tab `Hero Tests` (from Tue 10 Nov). Columns: A `Date` as `Day - dd/mm/yy AM|PM`, B `Hero` = the winning hero version, described in plain words from its hero block (headline / image alt text, e.g. "Hero B – scratch card: 'Up to 44% off + FREE diffuser'"), C `CTR` = the winner's click rate (unique clicks ÷ delivered, 2 dp, no % sign). **Winner = Hero Test A vs Hero Test B on CTR** (Mia, 9 Nov). One row per send that has a hero test. Verify the write.

## 5. Daily write-up – Notion

Parent page: "Daily Campaign Email Analysis - Claude" (id `3fee99564794806886bff03d2cd79ea7`).
One child page per day, titled `<Weekday dd Month yyyy> – Email performance`, icon 📧, newest at the top
(after creating, `replace_content` on the parent with the `<page>` tags listed newest first – never drop a tag).
Sections: headline callout · headline figures table (per send + total) with vs day before / same day last week
from the daily sheet · things to know · subject-line tests (winner = Test A vs Test B on unique clicks; still show click rate and open rate) · what did / didn't work
(click share per block from `links.mjs`: `node links.mjs <htmlDir> <clickJsonDir> <outDir> <names…>`).
Email the same summary to mia@valentte.com and ruby.h@valentte.com once an email connector is available.

## 6. Weekly meeting prep – Mondays ~7am (Europe/London)

**From 2 Nov 2026 the routine prompt (trig_01DNg3jC9k9JhFqPDYjcpCzU) defines the layout and wins over this section:**
title is just the date ("2nd November 2026"); plain language modelled on the Wednesday page "28th October 2026"
(406e9956479481bbb042f6ae6fb42fea); "The headline" + 👍/👎 bullets; send boxes with "What we changed / What happened /
Subject-line test / Still a problem"; Content and Flags sections; optional "🔍 … explained"; all detail inside a
`<toggle heading="h2">Full analysis` block (no divider); never an "Upcoming planned changes" section.
The notes below still apply for data sources and like-for-like checks.


New child page under the Notion page "Monday: Campaign Emails" (id `3ffe995647948074bdc4d975684a761e`, CRM Meetings – not
the daily analysis page), titled `Weekly meeting prep – <Weekday dd Month yyyy>`, icon 🗓️, placed directly under the
bold underlined "Meeting Prep" heading, which sits below the grey intro callout (keep the callout, the heading and every existing `<page>` tag, newest first). It covers the previous Mon–Sun and the week ahead, by **AM / PM / Evening**:

**Top of the page (written last; the routine prompt's wording wins on layout):**
- Two 50/50 columns: a blue 🗒️ "Meeting agenda · <date>" callout with an "In one line" summary (revenue with its change vs the week before AND vs last month, from the Weekly totals tab's "vs. LM"), and a grey "At a glance" callout with AM / PM / Evening revenue and changes, ending with the total.
- One callout per send, AM orange, PM blue and Evening green, each with "Changes:" and "Good to know:" bullets.
  - "Changes" includes the team's comments on the Valentte Growth Goals sheet, email campaign rows 300–303.
  - Read them with the Google Drive `read_file_content` (file 1psCaYVSfIzDoKVA2guDLaBYFnaWhtEbV3j_Fwayj-a8, includeComments) and map each comment to its date via "Comment Anchors".
  - Never reply to or resolve those comments.
- "## 🎨 Content" (what worked / what didn't, short bullets with click shares) and "## 🚩 Anything else to flag" bullets. No "Upcoming planned changes" section (removed at the team's request, 26 Oct).
- A divider, then *Everything below is the full detail, for reference if needed.*
- Plain words, rounded numbers, no tables or shorthand, and no separate "Agenda" list.
- Every statement about a number moving or content working/not working gets a short, data-backed "why" (offer, deadline, audience, outage, counting change). The manager will ask.
- Like-for-like check: daily-sheet figures before Tue 20 Oct 2026 only counted space-tagged visits. When comparing against any week before 26 Oct, re-run that week's funnels per day/send with `.utm_campaign starts with "<AM|PM|Evening>" and .utm_campaign contains "dd/mm/yy"`, using `execution_time` = next day 05:50Z (matches the daily method exactly). 12–18 Oct like-for-like: AM £47,937.74 (1,019), PM £39,062.62 (842), Evening £20,693.72 (540); Mon 19: AM £5,983.48 (118), PM £3,697.79 (78), Evening £1,000.14 (29).

**Full detail below the divider:**
1. **Last week by send** – per-send weekly totals (delivered, open rate, clicks, CTR, visitors, orders, conv., AOV, revenue)
   vs the week before. Use the `'Daily totals'` sheet blocks (offsets 0/4/8 per day) for everything except opens; get opens from
   Bloomreach (`count first event campaign where .status="opened"` by `action_name`, grouping top 120, for the week).
   Check the week total matches the team's `Weekly totals` tab. The **revenue by day and send** grid comes from the
   Bloomreach dashboard "[JS] Email Performance" (69fb1e65c37a3b442ed279ce): `calculate_report` on report
   `69e722fb45db70c39cfceb9b` with an absolute date filter covering both weeks (Mon 00:00 BST, i.e. Sun 23:00Z). Use the "1. AM",
   "2. PM" and "3. Evening" columns, add week totals and the change vs the same day last week, and note that it uses last-email-visit
   attribution, so its totals are higher than the sheet's. Also add best/worst sends,
   and revenue per 1,000 emails sent.
2. **Subject-line tests** – every test from the week (winner = Test A vs Test B on unique clicks, with click and open rates), and what styles won or lost.
3. **Content** – what did and didn't work, from the daily pages' click shares.
4. **Issues** – duplicate / unexpected sends (two actions to the same list, another day's email sending early),
   scenarios still in draft, high unsubscribe shares.
5. **This week's plan** – for each day's `dd/mm/yy Newsletter` scenario: status, trigger times and subject lines / tests
   (`search_scenarios` with designs → `python3 scenario_plan.py <saved result file>`). Add each email's status from the monday.com
   Emails board (id 1984717728, group "Daily Campaigns"). Finish with the decisions needed.

## Hero tests (from Tue 10 Nov 2026)

Mia, 9 Nov: "we will also be doing hero tests alongside the title tests … select the winner based on click through rate".
- In each newsletter scenario, customers in the hero-test group (`hero_test = true`) go to a 50/50 "Hero test" A/B split; everyone
  else outside the title-test group gets the main email. The hero versions keep the main subject line; only the top banner differs.
- Find the hero-test send steps by action name (expect "… - Hero Test A/B"; check the day's delivered-by-action list and the
  scenario nodes – if two steps share a name, split by `action_id` as on 5–6 Nov).
- Per version: delivered, opens, unique clicks, **CTR = unique clicks ÷ delivered**, plus the hero block's share of that version's
  clicks (links.mjs on the version's own click data – prep.py keeps non-"Title Test" actions as separate sends, so hero versions
  get their own hm/main files). **Winner = higher CTR**, Hero A vs Hero B only; whole audience for reference. If CTRs are within
  0.05 points, call it too close to call (still log the higher one).
- **10 Nov gotcha:** the AM hero steps were named "PM Email 10/11/26 - Hero Test A/B" (action ids 49/51; PM ones 60/59). Always split
  hero actions by `action_id` and match each to its scenario node's subject. Their UTM tags also say PM: count hero visitors before
  15:00Z as AM, and add an AM-hero funnel (`.utm_campaign contains "Hero"`, purchases 07:00–15:00Z) to the AM orders/revenue.
  Hero A is not always the main email's hero (10 Nov PM: whole audience, Hero A and Hero B were three different heroes) – check the images.
- Totals in the stats box/daily sheet include the hero-test emails (like title tests). The combined click map stays
  whole audience + title tests; hero versions are reported in their own panel because their top block differs.
- Miro (from w/c 9 Nov): second grey panel under the title panel at y0+590 (x−4, w600, h110, fill #eef3f8), text at y0+601:
  `<b>Hero A – CTR% · N unique clicks · hero block NN% of clicks:</b> description<br/><b>Hero B – …</b><br/><b>Winner on CTR: Hero X (a% vs b%)</b>`.
  If a send has no hero test, write "No hero test on this send." there. Images start at y0+720.
- Notion daily page: add a "Hero tests (winner on CTR)" section after the subject-line tests.
- Sheets: add the winner to the `Hero Tests` tab (see section 4).

## Miro "what worked / didn't" notes (from 28 Oct 2026)

Under each click map, add 3–5 sticky notes per email next to the block they describe: light green = worked,
light pink = didn't work. Text: "<b>Worked – NN% of clicks</b><br>short why" (one sentence, plain words).
How: `node bbox.mjs <day>/main <day>/hm <day>/out AM_... PM_... Evening_...` writes `<name>.boxes.json`
(block positions in the 640px-wide render); write a notes JSON like `tools/notes_example.json`
(day, send, a text snippet to match the block, kind, why), set the day's column x and image top y in
`notes.py` (DAY dict), then `python3 notes.py notes.json > notes.svg` and send it with canvas_update_from_svg.
Notes sit 50px right of the image, stacked so they don't overlap, each with a short divider line to its block.
## Miro "💡 To watch" notes (from 4 Nov 2026)

Mia asked for these on 4 Nov, modelled on the team's own comments on https://miro.com/app/board/uXjVHDlFJCM=/
(their colours: light_pink, blue, orange – don't use those). Ours are **yellow** stickies starting "💡 <short title>".
- Only add one when it's something the team should know going forward: a pattern across days (e.g. a block low two
  days running, tests never beating the main line), a risk (same hero/offer/product repeated in one email or across
  sends, fatigue), a click vs conversion mismatch, or a concrete test idea. Never just restate a green/pink note.
- Check every number against the data (and the previous days' pages/sheet) before writing it. Zero notes is fine.
- Place next to the relevant block: AM/PM in the 160px gap right of the green/pink notes (x = column + 488, width 142),
  Evening and whole-day notes right of the Evening notes (x = Evening column + 510, width 250).
- canvas_create_from_svg often auto-shifts a batch ~1,900px down ("auto-placement moved this batch"): always move
  items back with canvas_update_from_svg using the returned ids, then read back to confirm.

Copies of all scripts (prep.py, heatmap.mjs, links.mjs, bbox.mjs, notes.py) are in daily-report/tools/.
