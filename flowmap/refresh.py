#!/usr/bin/env python3
"""Weekly refresh helper for the Valentte flow board. See RUNBOOK.md for the full procedure.

  python3 refresh.py ingest <file>...        copy Bloomreach scenario JSON (tool-result files or plain
                                            scenario JSON) into raw/<scenario_id>.json
  python3 refresh.py harvest <file>...       read canvas_read_as_svg output(s) of flow frames and record
                                            item ids + image resource ids in state.json
  python3 refresh.py diff                   analyse raw/, compare with state.json, write out/changes.json
                                            and out/changes.md (human summary)
  python3 refresh.py rebuild <flow_id>      write out/rebuild_<flow_id>_delete.svg and _create.svg and
                                            out/rebuild_<flow_id>_slots.json (images that still need upload)
  python3 refresh.py relayout               write out/relayout.svg: moves/resizes frames to the new stacking
  python3 refresh.py header                 write out/header.svg (title, index, what-changed panel)
  python3 refresh.py commit                 store the new fingerprints in state.json after a successful run

state.json holds ids and hashes only (no email copy), so it is safe to commit.
"""
import datetime, glob, hashlib, html, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import slots  # noqa: E402

BOARD = "https://miro.com/app/board/uXjVEMAz3fI=/"


def fp(m):
    keys = ("channel", "name", "subject", "preheader", "body", "html_hash", "day", "status", "row", "lane", "test")
    return hashlib.sha1(json.dumps([m.get(k) for k in keys], ensure_ascii=False).encode()).hexdigest()[:12]


def ingest(files):
    os.makedirs(os.path.join(HERE, "raw"), exist_ok=True)
    for f in files:
        d = json.load(open(f))
        if "result" in d:
            d = d["result"]
        if "data" in d:
            d = d["data"]
        json.dump(d, open(os.path.join(HERE, "raw", d["_id"] + ".json"), "w"))
        print("ingested", d["_id"], d["name"])


def harvest(files):
    s = slots.load()
    item_to_hash = {v["item_id"]: v["hash"] for v in s["images"].values()}
    frame_to_flow = {v: k for k, v in s["frames"].items()}
    s.setdefault("resources", {})
    s.setdefault("flow_items", {})
    for f in files:
        txt = open(f).read()
        try:
            j = json.loads(txt)
            txt = j.get("svg") or j.get("result", {}).get("svg") or txt
        except Exception:
            pass
        for g in re.finditer(r'<g[^>]*data-miro-id="(\d+)"[^>]*data-frame=[^>]*>(.*?)</g>', txt, re.S):
            flow = frame_to_flow.get(g.group(1))
            if not flow:
                continue
            ids = []
            for el in re.finditer(r'<(\w+)([^>]*?)data-miro-id="(\d+)"([^>]*)>', g.group(2)):
                tag, item = el.group(1), el.group(3)
                attrs = el.group(2) + el.group(4)
                if tag == "image":
                    r = re.search(r"resources/images/(\d+)", attrs) or re.search(r"resource://(\d+)", attrs)
                    if r and item in item_to_hash:
                        s["resources"][item_to_hash[item]] = r.group(1)
                ids.append(item)
            s["flow_items"][flow] = ids
            print(f"harvested {flow}: {len(ids)} items")
    slots.save(s)


def analyse_all():
    subprocess.run([sys.executable, os.path.join(HERE, "analyze.py")], check=True, stdout=subprocess.DEVNULL)
    return json.load(open(os.path.join(HERE, "model.json")))


def diff():
    s = slots.load()
    model = analyse_all()
    prev = s.get("flows", {})
    changes = {"date": datetime.date.today().isoformat(), "flows": {}}
    lines = []
    for f in model:
        old = prev.get(f["id"])
        cur = {str(m["node_id"]): m for m in f["messages"]}
        title = re.sub(r"\s*\((update|updated)[^)]*\)", "", f["name"], flags=re.I).strip()
        if not old:
            changes["flows"][f["id"]] = {"kind": "new", "title": title}
            lines.append(f"New flow on the board: {title}")
            continue
        oldm = old["messages"]
        added = [m for k, m in cur.items() if k not in oldm]
        removed = [v for k, v in oldm.items() if k not in cur]
        changed = [m for k, m in cur.items() if k in oldm and oldm[k]["fp"] != fp(m)]
        if not (added or removed or changed):
            continue
        changes["flows"][f["id"]] = {"kind": "changed", "title": title,
                                    "added": [m["node_id"] for m in added], "removed": [v["name"] for v in removed],
                                    "changed": [m["node_id"] for m in changed]}
        for m in added:
            lines.append(f"{title}: added {m['channel']} '{m['name']}' ({m['status']}). SL: {m['subject'] or m['body'][:60]}")
        for v in removed:
            lines.append(f"{title}: removed '{v['name']}'")
        for m in changed:
            o = oldm[str(m["node_id"])]
            what = []
            if o.get("status") != m["status"]:
                what.append(f"now {m['status']}")
            if o.get("subject_fp") != hashlib.sha1((m["subject"] + "|" + m["preheader"]).encode()).hexdigest()[:8]:
                what.append(f"new SL/P1: {m['subject']}")
            if o.get("html_hash") != m["html_hash"]:
                what.append("email design changed")
            if o.get("day") != m["day"]:
                what.append(f"timing now day {m['day']}")
            lines.append(f"{title}: '{m['name']}' {'; '.join(what) or 'branch/row changed'}")
    for fid, old in prev.items():
        if fid not in {f["id"] for f in model}:
            changes["flows"][fid] = {"kind": "gone", "title": old["name"]}
            lines.append(f"No longer tracked or no longer active: {old['name']}")
    changes["lines"] = lines
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    json.dump(changes, open(os.path.join(HERE, "out", "changes.json"), "w"), indent=1, ensure_ascii=False)
    open(os.path.join(HERE, "out", "changes.md"), "w").write("\n".join(lines) or "No changes this week.")
    print("\n".join(lines) or "No changes this week.")


def rebuild(fid):
    subprocess.run([sys.executable, os.path.join(HERE, "build_layout.py")], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    s = slots.load()
    frame = s["frames"][fid]
    svg_path = os.path.join(HERE, "out", fid + ".svg")
    src = open(svg_path).read()
    lay = {f["id"]: f for f in json.load(open(os.path.join(HERE, "out", "layout.json")))}[fid]
    # delete stubs for everything currently inside the frame
    ours = set(s.get("flow_items", {}).get(fid, []))
    ours |= {v["item_id"] for k, v in s["images"].items() if k.startswith(fid + ":") and v.get("item_id")}
    dels = "\n".join(f'<rect data-miro-id="{i}" data-deleted="true" />' for i in sorted(ours))
    open(os.path.join(HERE, "out", f"rebuild_{fid}_delete.svg"), "w").write(f'<svg xmlns="http://www.w3.org/2000/svg">\n{dels}\n</svg>')
    # new content inside the existing frame; images we already host go in as resource:// refs
    body = src.split("\n", 3)[3].rsplit("</g>", 1)[0]
    imgs, pending = [], []
    for i, im in enumerate(lay["images"]):
        rid = s.get("resources", {}).get(im["hash"])
        if rid:
            imgs.append(f'<image data-type="image" href="resource://{rid}" x="{im["left"]}" y="{im["top"]}" width="{im["w"]}" height="{im["h"]}" />')
        else:
            pending.append(i)
    g = re.search(r'<g id="f" transform="translate\(([-\d.]+),([-\d.]+)\)"', src)
    out = (f'<svg xmlns="http://www.w3.org/2000/svg">\n<g data-miro-id="{frame}" data-frame="{html.escape(lay['title'], quote=True)}" transform="translate({g.group(1)},{g.group(2)})">\n'
           f'<rect data-type="frame" x="0" y="0" width="{lay["width"]}" height="{lay["height"]}" />\n{body}\n' + "\n".join(imgs) + "\n</g>\n</svg>")
    open(os.path.join(HERE, "out", f"rebuild_{fid}_create.svg"), "w").write(out)
    json.dump(pending, open(os.path.join(HERE, "out", f"rebuild_{fid}_slots.json"), "w"))
    # forget old image records for this flow so `slots.py list` shows pending ones
    s["images"] = {k: v for k, v in s["images"].items() if not k.startswith(fid + ":") or int(k.split(":")[1]) not in pending}
    for i, im in enumerate(lay["images"]):
        if i not in pending:
            s["images"][f"{fid}:{i}"] = {"item_id": None, "hash": im["hash"], "node_ids": im["node_ids"]}
    slots.save(s)
    print(f"delete stubs: {dels.count('data-miro-id')}  create svg: {len(out)} chars  images reused: {len(imgs)}  to upload: {len(pending)}")


def relayout():
    subprocess.run([sys.executable, os.path.join(HERE, "build_layout.py")], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    s = slots.load()
    parts = []
    for f in json.load(open(os.path.join(HERE, "out", "layout.json"))):
        fr = s["frames"].get(f["id"])
        if fr:
            parts.append(f'<g data-miro-id="{fr}" data-frame="{html.escape(f["title"], quote=True)}" transform="translate({f["x"]},{f["y"]})"><rect data-type="frame" x="0" y="0" width="{f["width"]}" height="{f["height"]}" /></g>')
    open(os.path.join(HERE, "out", "relayout.svg"), "w").write('<svg xmlns="http://www.w3.org/2000/svg">\n' + "\n".join(parts) + "\n</svg>")
    print(len(parts), "frames")


def header():
    s = slots.load()
    lay = json.load(open(os.path.join(HERE, "out", "layout.json")))
    ch = json.load(open(os.path.join(HERE, "out", "changes.json"))) if os.path.exists(os.path.join(HERE, "out", "changes.json")) else {"lines": []}
    today = datetime.date.today().strftime("%-d %b %Y")
    e = lambda t: html.escape(t or "", quote=False)
    idx = "<br/>".join(f'<a href="{BOARD}?moveToWidget={s["frames"][f["id"]]}">{e(f["title"])}</a>'
                       for f in lay if f["id"] in s["frames"])
    lines = ch.get("lines") or ["No changes since the last refresh."]
    chg = "<br/>".join("- " + e(l) for l in lines[:40]) + (f"<br/>...and {len(lines) - 40} more" if len(lines) > 40 else "")
    ids = s.get("header", {})
    def el(key, tag_open, body):
        mid = f' data-miro-id="{ids[key]}"' if key in ids else ""
        return tag_open.replace("<textArea", f'<textArea id="{key}"{mid}', 1) + body + "</textArea>"
    svg = ['<svg xmlns="http://www.w3.org/2000/svg">',
           el("h_title", '<textArea x="0" y="-2200" width="5000" font-size="90" font-weight="bold" fill="#1a1a1a" font-family="noto_sans">', "Valentte Lifecycle Flows"),
           el("h_sub", '<textArea x="0" y="-2050" width="5000" font-size="33" fill="#595959" font-family="noto_sans">',
              f"Every live email, SMS and WhatsApp step in the 16 customer-facing Bloomreach flows. Refreshed automatically every Monday at 7:40am UK. Last refreshed {today}."),
           el("h_legend", '<textArea x="0" y="-1900" width="5000" font-size="22" fill="#595959" font-family="noto_sans">',
              "<b>How to read it:</b> each frame is one flow. Yellow pills are days since the trigger. Blue cards are emails (SL = subject line, P1 = preheader) with the email below; green cards are SMS or WhatsApp. Italic text on a card shows which branch or A/B variant gets it. Steps that get 0% traffic, cannot be reached or are not connected are listed at the bottom of each frame."),
           el("h_index", '<textArea x="0" y="-1650" width="1600" font-size="22" fill="#1a1a1a" font-family="noto_sans">', "<b>Flows</b><br/>" + idx),
           el("h_changes", '<textArea x="1800" y="-1650" width="3200" font-size="22" fill="#1a1a1a" font-family="noto_sans">',
              f"<b>What changed this week ({today})</b><br/>" + chg),
           "</svg>"]
    open(os.path.join(HERE, "out", "header.svg"), "w").write("\n".join(svg))
    print("header.svg written; after creating, record ids with: python3 refresh.py header-ids '<result_svg file>'")


def header_ids(path):
    s = slots.load()
    txt = open(path).read()
    s["header"] = {m.group(1): m.group(2) for m in re.finditer(r'id="(h_\w+)"[^>]*data-miro-id="(\d+)"', txt)}
    slots.save(s)
    print(s["header"])


def commit():
    s = slots.load()
    model = json.load(open(os.path.join(HERE, "model.json")))
    s["flows"] = {f["id"]: {"name": f["name"], "edited": f["edited"], "messages": {
        str(m["node_id"]): {"name": m["name"], "fp": fp(m), "status": m["status"], "day": m["day"],
                            "html_hash": m["html_hash"],
                            "subject_fp": hashlib.sha1((m["subject"] + "|" + m["preheader"]).encode()).hexdigest()[:8]}
        for m in f["messages"]}} for f in model}
    s["last_refresh"] = datetime.date.today().isoformat()
    slots.save(s)
    if os.path.exists(slots.LOG):
        os.remove(slots.LOG)
    print("state committed for", len(s["flows"]), "flows")


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    {"ingest": lambda: ingest(args), "harvest": lambda: harvest(args), "diff": diff,
     "rebuild": lambda: rebuild(args[0]), "relayout": relayout, "header": header,
     "header-ids": lambda: header_ids(args[0]), "commit": commit}[cmd]()
