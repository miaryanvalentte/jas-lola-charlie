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
- **Visitors** (Metrilo-style): `count first event session_start` where `.utm_campaign` = exact email name, send day only (BST).
  Some visits are tagged with `+` for spaces (`AM+Email+20/10/26+-+Title+Test+A`): count both spellings, and use
  `.utm_campaign is in [...]` with both spellings in the orders/revenue funnels.
- **Sanity check**: if a send's visitors are far below its clicks, check site activity by hour (`count event session_start`,
  `count event purchase` by hour vs the day before) – on 20/10 a ~7–11am gap meant almost no visits or orders were recorded.
- **Orders / revenue**: `funnel(session_start where .utm_campaign = X followed by purchase in last 3 days within 2 hours)`,
  purchases from send time to 23:00Z same day, sum `total_price`.

## 2. Miro board – https://miro.com/app/board/uXjVEYE5ouI=/

Layout (board units): day x = `-7400 + weekday * 2120` (Mon = 0); each day is 1880 wide; columns 600 wide with 40 gap.
Week rows: w/c 12 Oct y0 = -1064, w/c 19 Oct y0 = 1507, w/c 26 Oct y0 = 4157. Images go at y0 + 600.
Template text boxes already exist for 19–31 Oct: **update** them (stats box at y0+149, panel at y0+485) – don't create new ones.

Per send column:
- Label `Total – whole audience + tests`; stats = **totals** across whole audience + Test A + Test B
  (open rate weighted by delivered; CTR = clicks/delivered; conv = orders/visitors; AOV = revenue/orders). SL/P1 = whole-audience version.
- Grey panel: `Test A – OR% open · CTR% click rate: SL / P1`, same for Test B, then
  **`Winner on clicks: <variant> (x.xx% click rate vs whole audience y.yy%)`** – highest unique click rate (clicks ÷ delivered) wins.
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

Tab `Sheet1`. Columns: A `Day - dd/mm/yy AM|PM`, B `SL - P1` of the winner on clicks, C click rate (2 dp, no % sign), D open rate.

## 5. Daily write-up – Notion

Parent page: "Daily Campaign Email Analysis - Claude" (id `3fee99564794806886bff03d2cd79ea7`).
One child page per day, titled `<Weekday dd Month yyyy> – Email performance`, icon 📧, newest at the top
(after creating, `replace_content` on the parent with the `<page>` tags listed newest first – never drop a tag).
Sections: headline callout · headline figures table (per send + total) with vs day before / same day last week
from the daily sheet · things to know · subject-line tests (winner on click rate) · what did / didn't work
(click share per block from `links.mjs`: `node links.mjs <htmlDir> <clickJsonDir> <outDir> <names…>`).
Email the same summary to mia@valentte.com and ruby.h@valentte.com once an email connector is available.

## 6. Weekly meeting prep – Mondays ~7am (Europe/London)

New child page under the Notion page "Monday: Campaign Emails" (id `3ffe995647948074bdc4d975684a761e`, CRM Meetings – not
the daily analysis page), titled `Weekly meeting prep – <Weekday dd Month yyyy>`, icon 🗓️, placed directly under the
grey intro callout (keep the callout and every existing `<page>` tag, newest first). It covers the previous Mon–Sun and the week ahead, by **AM / PM / Evening**:

**Top of the page (written last; the routine prompt's wording wins on layout):**
- Two 50/50 columns: a blue 🗒️ "Meeting agenda · <date>" callout with an "In one line" summary, and a grey "At a glance" callout with AM / PM / Evening revenue and changes, ending with the total.
- One callout per send, AM orange, PM blue and Evening green, each with "Changes:" and "Good to know:" bullets.
  - "Changes" includes the team's comments on the Valentte Growth Goals sheet, email campaign rows 300–303.
  - Read them with the Google Drive `read_file_content` (file 1psCaYVSfIzDoKVA2guDLaBYFnaWhtEbV3j_Fwayj-a8, includeComments) and map each comment to its date via "Comment Anchors".
  - Never reply to or resolve those comments.
- "## 🔜 Upcoming planned changes" and "## 🚩 Anything else to flag" bullets.
- A divider, then *Everything below is the full detail, for reference if needed.*
- Plain words, rounded numbers, no tables or shorthand, and no separate "Agenda" list.

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
2. **Subject-line tests** – every test from the week (winner on click rate), and what styles won or lost.
3. **Content** – what did and didn't work, from the daily pages' click shares.
4. **Issues** – duplicate / unexpected sends (two actions to the same list, another day's email sending early),
   scenarios still in draft, high unsubscribe shares.
5. **This week's plan** – for each day's `dd/mm/yy Newsletter` scenario: status, trigger times and subject lines / tests
   (`search_scenarios` with designs → `python3 scenario_plan.py <saved result file>`). Add each email's status from the monday.com
   Emails board (id 1984717728, group "Daily Campaigns"). Finish with the decisions needed.
