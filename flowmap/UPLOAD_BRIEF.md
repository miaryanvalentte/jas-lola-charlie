# Brief: placing email preview images on the Valentte flow board

Board: https://miro.com/app/board/uXjVEMAz3fI=/
Working dir: /home/user/jas-lola-charlie/flowmap
All layout is pre-computed. The work is mechanical; do not redesign anything.

Load these tool schemas first with ToolSearch:
`select:mcp__Miro__image_get_upload_url,mcp__Miro__image_create,mcp__Miro__canvas_create_from_svg`

## Creating a frame (only when your task says so)
1. Run `python3 slots.py status`. If the flow already has a frame id, skip creating it.
2. Read `out/<flow_id>.svg` and pass its full contents VERBATIM as `svg` to
   `mcp__Miro__canvas_create_from_svg` (miro_url = the board URL above). Never edit or shorten it.
3. Take the `data-miro-id` of the top-level `<g ... data-frame=...>` in the result and run
   `python3 slots.py frame <flow_id> <frame_id>`.

## Placing images for a flow
Run `python3 slots.py list <flow_id> [start] [end]`. Each output line is one pending slot:
`{"index", "hash", "miro_url", "x", "y", "width", "title"}`. For each slot, in order:

1. Call `mcp__Miro__image_get_upload_url` with `miro_url` = slot.miro_url (it already targets the
   frame), `content_type` = "image/jpeg", and x, y, width, title from the slot (copy them exactly).
2. Upload with: `python3 slots.py put <hash> '<upload_url>'` — paste the upload_url exactly,
   inside single quotes. It must print 200. URLs expire after 10 minutes, so upload straight away.
3. Call `mcp__Miro__image_create` with the same `miro_url` and `image_token` = the token from step 1.
   Pass nothing else.
4. Record it: `python3 slots.py done <flow_id> <index> <item_id>` using item_id from step 3.

To save turns, you may batch: request upload URLs for up to 5 slots in parallel, then run the
5 `put` commands in one Bash call (separated by `&&`), then 5 image_create calls in parallel, then
the 5 `done` commands in one Bash call.

Rules:
- Never place the same slot twice. `list` only shows slots not yet recorded as done, so re-run it if
  you lose track.
- If a put does not return 200, request a fresh upload URL for that slot and retry once.
- If image_create fails, report the error and move on.
- Only work on the flows and index ranges in your task; other agents handle the rest in parallel.

When finished, run `python3 slots.py status` and reply in at most 5 lines: what you placed, and any
failures (slot index + error). Do not paste upload URLs or tokens in your reply.
