#!/usr/bin/env python3
"""Lay out model.json as Miro frames.

Writes flowmap/out/<flow_id>.svg (frame + text + cards, one canvas_create_from_svg call each)
and flowmap/out/layout.json (frame boxes and the image slots to upload into each frame).
"""
import html, json, os, re, datetime
from collections import defaultdict, OrderedDict
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
BR = "https://uk1.eng.bloomreach.com/p/valentte-prod/campaigns/scenarios/"

ORDER = ["Welcome Flow", "SMS Welcome Programme", "LB - Abandoned Browse", "LB - Abandoned Site",
         "LB - Abandoned Cart", "LB - Abandoned Checkout", "Post Purchase - First Time",
         "Post Purchase - Returning", "First to Second Purchase", "Post-purchase: Review Request",
         "Review Confirmation", "MentionMe - Customer Who Received", "MentionMe - Customer Who Sent",
         "DM001 Win Back", "Double Order Offer", "Annual Delivery Pass"]

PAD, CW, GAP, VGAP, TEXT_H, SMS_H = 64, 420, 64, 20, 250, 300
INK, BODY = "#1a1a1a", "#595959"
CH_STYLE = {"Email": ("#f0f5fd", "#305bab"), "SMS": ("#eaf9ef", "#067429"), "WhatsApp": ("#eaf9ef", "#067429")}
FLOW_GAP = 320


def esc(s):
    return html.escape(s or "", quote=False)


def attr(s):
    return html.escape(s or "", quote=True)


def clean_title(name):
    return re.sub(r"\s*\((update|updated)[^)]*\)\s*", " ", name, flags=re.I).strip()


def day_label(d):
    if d is None:
        return "No timing"
    whole = int(d + 1e-9)
    hrs = round((d - whole) * 24)
    return f"Day {whole}" + (f" +{hrs}h" if hrs else "")


def img_h(h, w=CW):
    p = os.path.join(HERE, "images", h + ".jpg")
    if not os.path.exists(p):
        return 600
    iw, ih = Image.open(p).size
    return int(ih * w / iw)


def fmt_date(ts):
    return datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).strftime("%-d %b %Y") if ts else "?"


def flow_sort_key(f):
    for i, p in enumerate(ORDER):
        if f["name"].startswith(p):
            return i
    return 99


def build_flow(f):
    live = [m for m in f["messages"] if m["status"] == "live"]
    dead = [m for m in f["messages"] if m["status"] != "live"]

    # rows -> day -> merged cards
    rows = OrderedDict()
    for m in sorted(live, key=lambda m: (m["channel"] != "Email", m["day"], m["row"])):
        rows.setdefault((m["channel"], m["row"]), defaultdict(list))
    for m in live:
        cell = rows[(m["channel"], m["row"])][m["day"]]
        key = m["html_hash"] or (m["channel"], m["body"], m["subject"])
        for c in cell:
            if c["key"] == key:
                c["branches"].add(" / ".join(x for x in (m["lane"], m["test"]) if x and x != "Main"))
                c["node_ids"].append(m["node_id"])
                break
        else:
            cell.append({"key": key, "m": m, "node_ids": [m["node_id"]],
                         "branches": {" / ".join(x for x in (m["lane"], m["test"]) if x and x != "Main")}})
    days = sorted({m["day"] for m in live})
    colw = {d: max([len(r.get(d, [])) for r in rows.values()] + [1]) for d in days}
    colx, x = {}, PAD
    for d in days:
        colx[d] = x
        x += colw[d] * CW + (colw[d] - 1) * VGAP + GAP
    width = max(x - GAP + PAD, 3600)

    els, images = [], []
    title = clean_title(f["name"])
    n_email = sum(1 for m in live if m["channel"] == "Email")
    n_sms = sum(1 for m in live if m["channel"] != "Email")
    counts = ", ".join(p for p in (f"{n_email} live emails" if n_email else "",
                                   f"{n_sms} live SMS/WhatsApp" if n_sms else "") if p) or "No customer messages"
    meta = (f"<b>Trigger:</b> {esc('; '.join(f['triggers']) or 'none')}<br/>"
            f"<b>Live steps:</b> {esc(counts)}. {len(dead)} more not live.<br/>"
            f"<b>Last edited:</b> {fmt_date(f['edited'])} by {esc(f['edited_by'] or '?')}. "
            f"<a href=\"{BR}{f['id']}\">Open in Bloomreach</a>")
    els.append(f'<textArea x="{PAD}" y="{PAD}" width="{width - 2 * PAD}" font-size="67" font-weight="bold" fill="{INK}" font-family="noto_sans">{esc(title)}</textArea>')
    els.append(f'<textArea x="{PAD}" y="{PAD + 110}" width="2400" font-size="22" fill="{BODY}" font-family="noto_sans">{meta}</textArea>')
    y = PAD + 280

    if f.get("other_actions") and not live:
        lst = "<br/>".join("- " + esc(a) for a in f["other_actions"])
        els.append(f'<textArea x="{PAD}" y="{y}" width="2400" font-size="22" fill="{BODY}" font-family="noto_sans"><b>This flow does not send emails or SMS. It runs these actions:</b><br/>{lst}</textArea>')
        y += 120 + 34 * len(f["other_actions"])

    if live:
        # day header band
        for d in days:
            w = colw[d] * CW + (colw[d] - 1) * VGAP
            els.append(f'<rect x="{colx[d]}" y="{y}" width="{w}" height="64" rx="12" fill="#fff6b6" stroke="none" data-content="{attr("<b>" + day_label(d) + "</b>")}" data-font-size="22" data-text-color="#af7e04" data-font-family="noto_sans" />')
        y += 64 + 64
    for (ch, row), cells in rows.items():
        els.append(f'<textArea x="{PAD}" y="{y}" width="{width - 2 * PAD}" font-size="33" font-weight="bold" fill="{INK}" font-family="noto_sans">{esc(row)} · {esc(ch)}</textArea>')
        ty = y + 80
        row_h = 0
        for d, cell in cells.items():
            for i, c in enumerate(cell):
                m = c["m"]
                cx = colx[d] + i * (CW + VGAP)
                fill, dark = CH_STYLE[m["channel"]]
                br = "; ".join(sorted(b for b in c["branches"] if b))
                parts = [f"<b>{esc(day_label(d))} · {esc(m['channel'])}</b>", esc(m["name"])]
                if br:
                    parts.append(f"<i>{esc(br)}</i>")
                if m["channel"] == "Email":
                    parts.append(f"<b>SL:</b> {esc(m['subject'])}")
                    parts.append(f"<b>P1:</b> {esc(m['preheader'])}")
                    h = TEXT_H
                else:
                    parts.append(esc(m["body"]).replace("\n", "<br>"))
                    h = TEXT_H + SMS_H
                els.append(f'<rect x="{cx}" y="{ty}" width="{CW}" height="{h}" rx="12" fill="{fill}" stroke="none" data-content="{attr("<br>".join(parts))}" data-font-size="16" data-text-color="{INK}" data-text-align="left" data-text-align-vertical="top" data-font-family="noto_sans" />')
                ch_h = h
                if m["channel"] == "Email" and m["html_hash"]:
                    ih = img_h(m["html_hash"])
                    images.append({"hash": m["html_hash"], "x": cx + CW / 2, "y": ty + h + 20 + ih / 2,
                                   "w": CW, "h": ih, "left": cx, "top": ty + h + 20,
                                   "title": m["name"][:120], "node_ids": c["node_ids"]})
                    ch_h = h + 20 + ih
                row_h = max(row_h, ch_h)
        y = ty + row_h + 128

    if dead:
        els.append(f'<textArea x="{PAD}" y="{y}" width="{width - 2 * PAD}" font-size="33" font-weight="bold" fill="{INK}" font-family="noto_sans">Not live in this flow</textArea>')
        y += 80
        lines = [f"{esc(m['name'] or m['channel'])} <i>({esc(m['status'])})</i>" for m in dead]
        per = 12
        for i in range(0, len(lines), per):
            chunk = lines[i:i + per]
            els.append(f'<textArea x="{PAD + (i // per) * 1000}" y="{y}" width="940" font-size="18" fill="{BODY}" font-family="noto_sans">{"<br/>".join(chunk)}</textArea>')
        y += 30 * min(len(lines), per) + 80

    height = y + PAD
    return {"id": f["id"], "title": title, "width": width, "height": height, "els": els, "images": images}


def main():
    model = sorted(json.load(open(os.path.join(HERE, "model.json"))), key=flow_sort_key)
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    layout, fy = [], 0
    for f in model:
        b = build_flow(f)
        b["x"], b["y"] = 0, fy
        fy += b["height"] + FLOW_GAP
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg">\n<g id="f" transform="translate({b["x"]},{b["y"]})" data-frame="{attr(b["title"])}">\n'
               f'<rect data-type="frame" x="0" y="0" width="{b["width"]}" height="{b["height"]}" fill="#ffffff" data-title="{attr(b["title"])}" />\n'
               + "\n".join(b["els"]) + "\n</g>\n</svg>")
        open(os.path.join(HERE, "out", f["id"] + ".svg"), "w").write(svg)
        layout.append({k: b[k] for k in ("id", "title", "x", "y", "width", "height", "images")} | {"svg_len": len(svg)})
    json.dump(layout, open(os.path.join(HERE, "out", "layout.json"), "w"), indent=1)
    for l in layout:
        print(f"{l['title'][:45]:45} {l['width']:>6}x{l['height']:<6} images={len(l['images']):<3} svg={l['svg_len']}")
    print("total images", sum(len(l["images"]) for l in layout), "unique", len({i["hash"] for l in layout for i in l["images"]}))


if __name__ == "__main__":
    main()
