# Monday refresh: Valentte Lifecycle Flows board

Board: https://miro.com/app/board/uXjVEMAz3fI=/
Bloomreach project "Valentte Prod": `2e25bbd8-55a8-11f0-9f79-9aae66778e25` (org `e3c412f4-f6e4-11f0-8497-6aa29e847a13`)
Code + state: branch `claude/cool-hamilton-12er2w`, folder `flowmap/`.

The board owner set this up and authorised this weekly job to: read Bloomreach scenarios, update the
board (including deleting and redrawing the items this tool created inside flow frames), and commit
`flowmap/state.json` back to the branch. Never edit Bloomreach. Never delete anything on the board that
is not listed in state.json (people may add their own notes). Never commit raw/, html/, images/, out/
or model.json (they hold email content and the repo is public; .gitignore covers them).

Context hygiene: large tool results are saved to files automatically. Process them with the scripts;
never read raw scenario JSON or long SVGs into your own context.

## 0. Setup
```
git fetch origin claude/cool-hamilton-12er2w && git checkout claude/cool-hamilton-12er2w
cd flowmap
```
Load tools with ToolSearch: `select:mcp__Loomi__search_scenarios,mcp__Miro__canvas_create_from_svg,mcp__Miro__canvas_update_from_svg,mcp__Miro__canvas_read_as_svg,mcp__Miro__image_get_upload_url,mcp__Miro__image_create`.

## 1. Which flows to fetch
- `search_scenarios(project_id, status="active")` (list mode, small).
- Tracked flows = keys of `state.json["flows"]`.
- A tracked flow missing from the active list is GONE: rename its frame title to start with
  "NOT ACTIVE - " (canvas_update_from_svg with `<g data-miro-id="FRAME" data-frame="NOT ACTIVE - ..."><rect data-type="frame" /></g>`),
  and drop its raw file so it is not re-analysed. Mention it in the summary.
- A NEW active scenario not tracked and not in `state.json["excluded"]` is added automatically
  unless its name matches (case-insensitive) `newsletter|test|do not stop|sync|tracking|audience|handler|transaction|key metrics|rfm|domain strip|temp segment`.
  Matching ones: add their id to `state.json["excluded"]` and mention them in the summary.

## 2. Fetch and analyse
For every tracked + new flow: `search_scenarios(project_id, scenario_id=ID, include_node_designs=true)`.
The result is saved to a file; run `python3 refresh.py ingest <that file>`. (If one comes back
inline because it is tiny, Write the JSON to `/tmp/scn_ID.json` and ingest that.)
Then: `python3 refresh.py diff` — prints the human-readable change list and writes out/changes.json.
If it says "No changes this week", skip to step 5.

## 3. Render email previews
`python3 extract_html.py && node render.js` (renders every live design; ~2 min).

## 4. Redraw changed and new flows (one flow at a time)
For a flow with kind "changed":
1. `python3 refresh.py rebuild <flow_id>`
2. `canvas_update_from_svg` with the contents of `out/rebuild_<flow_id>_delete.svg` (skip if it has no stubs).
3. `canvas_update_from_svg` with the contents of `out/rebuild_<flow_id>_create.svg` (send verbatim).
   Save the returned result_svg: if it was written to a file use that path, otherwise Write it to
   `out/result_<flow_id>.svg`. Run `python3 refresh.py harvest <path>`.
4. Upload the remaining new email images exactly as in `UPLOAD_BRIEF.md` ("Placing images"),
   using `python3 slots.py list <flow_id>`.
For a flow with kind "new": `python3 build_layout.py`, create the frame from `out/<flow_id>.svg` with
`canvas_create_from_svg`, record it with `python3 slots.py frame <flow_id> <frame_id>`, harvest the
result_svg as above, then upload images as in UPLOAD_BRIEF.md.

After any upload: `canvas_read_as_svg(widget_ids=[frame_id])` and `python3 refresh.py harvest <file>`
so the image resource ids are known for next week.

## 5. Re-stack frames and update the header
- `python3 refresh.py relayout` then `canvas_update_from_svg` with `out/relayout.svg`.
- `python3 refresh.py header` then `canvas_update_from_svg` with `out/header.svg` (it updates the
  existing header items in place; if state has no header ids, use canvas_create_from_svg and run
  `python3 refresh.py header-ids <result file>`).

## 6. Save state
```
python3 refresh.py commit
git add flowmap/state.json flowmap/*.py flowmap/*.js flowmap/*.md flowmap/.gitignore
git commit -m "Flow board refresh <date>"
git push -u origin claude/cool-hamilton-12er2w
```

## 7. Report
Finish with a short summary: flows changed, emails added/removed/changed, anything that failed,
and the board link.
