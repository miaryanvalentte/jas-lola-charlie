#!/usr/bin/env python3
"""Place image slots whose design is already on the board, by resource id (no upload needed).

  python3 dupes.py svg <flow_id>              -> out/dupes_<flow_id>.svg (+ out/dupes_<flow_id>.json slot order)
  python3 dupes.py record <flow_id> <file>    -> record item ids from the canvas_update_from_svg result
"""
import html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import slots  # noqa: E402


def make(fid):
    s = slots.load()
    lay = {f["id"]: f for f in json.load(open(os.path.join(HERE, "out", "layout.json")))}[fid]
    frame = s["frames"][fid]
    els, order, missing = [], [], []
    for i, im in enumerate(lay["images"]):
        if f"{fid}:{i}" in s["images"]:
            continue
        rid = s.get("resources", {}).get(im["hash"])
        if not rid:
            missing.append(i)
            continue
        order.append(i)
        els.append(f'<image id="d{i}" data-type="image" href="resource://{rid}" x="{im["left"]}" y="{im["top"]}" width="{im["w"]}" height="{im["h"]}" />')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg">\n<g data-miro-id="{frame}" data-frame="{html.escape(lay['title'], quote=True)}" transform="translate({lay["x"]},{lay["y"]})">\n'
           f'<rect data-type="frame" x="0" y="0" width="{lay["width"]}" height="{lay["height"]}" />\n' + "\n".join(els) + "\n</g>\n</svg>")
    open(os.path.join(HERE, "out", f"dupes_{fid}.svg"), "w").write(svg)
    print(f"{len(order)} to place, {len(missing)} without a known resource: {missing}")


def record(fid, path):
    txt = open(path).read()
    for m in re.finditer(r'id="d(\d+)"[^>]*?data-miro-id="(\d+)"|data-miro-id="(\d+)"[^>]*?id="d(\d+)"', txt):
        i = m.group(1) or m.group(4)
        item = m.group(2) or m.group(3)
        os.system(f"python3 {os.path.join(HERE, 'slots.py')} done {fid} {i} {item} >/dev/null")
    print("recorded")


if __name__ == "__main__":
    {"svg": lambda: make(sys.argv[2]), "record": lambda: record(sys.argv[2], sys.argv[3])}[sys.argv[1]]()
