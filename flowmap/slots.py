#!/usr/bin/env python3
"""Helper for agents uploading email previews to Miro.

  python3 slots.py frame <flow_id> <frame_miro_id>     record the frame id for a flow
  python3 slots.py list <flow_id> [start] [end]         print pending image slots (not yet placed)
  python3 slots.py put <hash> '<upload_url>'            PUT images/<hash>.jpg to a Miro upload URL
  python3 slots.py done <flow_id> <index> <item_id>     record a placed image
  python3 slots.py status                               summary of frames and placed images
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "state.json")


LOG = os.path.join(HERE, "state_log.jsonl")   # append-only; safe with several agents


def load():
    s = json.load(open(STATE)) if os.path.exists(STATE) else {"board": "https://miro.com/app/board/uXjVEMAz3fI=/", "frames": {}, "images": {}}
    if os.path.exists(LOG):
        for line in open(LOG):
            if line.strip():
                e = json.loads(line)
                if e["kind"] == "frame":
                    s["frames"][e["flow"]] = e["id"]
                else:
                    s["images"][e["key"]] = e["val"]
    return s


def log(e):
    with open(LOG, "a") as fh:
        fh.write(json.dumps(e) + "\n")


def save(s):
    tmp = STATE + ".tmp"
    json.dump(s, open(tmp, "w"), indent=1)
    os.replace(tmp, STATE)


def layout():
    return {f["id"]: f for f in json.load(open(os.path.join(HERE, "out", "layout.json")))}


def main():
    cmd = sys.argv[1]
    if cmd == "frame":
        log({"kind": "frame", "flow": sys.argv[2], "id": sys.argv[3]}); print("ok")
    elif cmd == "list":
        fid = sys.argv[2]
        only = None
        if len(sys.argv) > 3 and sys.argv[3] == "--idx":
            only = {int(x) for x in sys.argv[4].split(",")}
            a, b = 0, 10**9
        else:
            a = int(sys.argv[3]) if len(sys.argv) > 3 else 0
            b = int(sys.argv[4]) if len(sys.argv) > 4 else 10**9
        s = load(); frame = s["frames"].get(fid)
        if not frame:
            sys.exit(f"no frame recorded for {fid}")
        imgs = layout()[fid]["images"]
        for i, im in enumerate(imgs):
            if a <= i < b and (only is None or i in only) and f"{fid}:{i}" not in s["images"]:
                print(json.dumps({"index": i, "hash": im["hash"], "miro_url": f"{s['board']}?moveToWidget={frame}",
                                  "x": im["x"], "y": im["y"], "width": im["w"], "title": im["title"]}, ensure_ascii=False))
    elif cmd == "put":
        h, url = sys.argv[2], sys.argv[3]
        r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-X", "PUT", "-H", "Content-Type: image/jpeg",
                            "--data-binary", "@" + os.path.join(HERE, "images", h + ".jpg"), url], capture_output=True, text=True)
        print(r.stdout)
    elif cmd == "done":
        fid, i, item = sys.argv[2], int(sys.argv[3]), sys.argv[4]
        im = layout()[fid]["images"][i]
        log({"kind": "image", "key": f"{fid}:{i}", "val": {"item_id": item, "hash": im["hash"], "node_ids": im["node_ids"]}})
        print("ok")
    elif cmd == "compact":
        s = load(); save(s); os.remove(LOG) if os.path.exists(LOG) else None; print("ok")
    elif cmd == "status":
        s = load(); L = layout()
        for fid, f in L.items():
            placed = sum(1 for k in s["images"] if k.startswith(fid + ":"))
            print(f"{f['title'][:45]:45} frame={s['frames'].get(fid, '-'):>20} images {placed}/{len(f['images'])}")


if __name__ == "__main__":
    main()
