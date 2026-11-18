#!/usr/bin/env python3
"""Turn raw Bloomreach scenario JSON (flowmap/raw/<id>.json) into a compact
flow model (flowmap/model.json) used to draw the Miro board and diff weeks.

For every message node (email / SMS / WhatsApp) we work out:
  - live: reachable from an active trigger without passing through a 0% A/B branch
  - day:  shortest cumulative wait from the trigger (days, 1 decimal)
  - path: A/B variant names taken on the way (e.g. "Variant B")
  - lane: grouping key for a board row (node name with day/email numbers removed)
"""
import hashlib, heapq, json, re, sys, glob, os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
UNIT_H = {"seconds": 1 / 3600, "minutes": 1 / 60, "hours": 1, "days": 24, "weeks": 168}
MSG_TYPES = {"send-email-action": "Email", "send-sms-action": "SMS",
             "send-mobile-messaging-action": "WhatsApp"}


def wait_hours(n):
    if n["type"] == "wait-action":
        return n.get("count", 0) * UNIT_H.get(n.get("units", "hours"), 1)
    if n["type"] == "wait-action-dynamic":
        return 0  # depends on customer data; shown as-is
    return 0


def lane_key(name):
    s = name or ""
    s = re.sub(r"^\s*\[[^\]]*\]\s*", "", s)                 # [03.08] date prefixes
    s = re.sub(r"\(?\s*update[^)]*\)?", "", s, flags=re.I)
    s = re.sub(r"\b(day|email|sms|e|step)\s*\d+(\.\d+)?\b", "", s, flags=re.I)
    s = re.sub(r"\b\d+\s*(h|hr|hrs|hours?|days?|mins?|minutes?)\b", "", s, flags=re.I)
    s = re.sub(r"\((?:[^)]*\d[^)]*|\s*formerly[^)]*)\)", "", s, flags=re.I)   # (03/11), (formerly 1.2)
    s = re.sub(r"\b(\d+(st|nd|rd|th)?)\s*$", "", s)
    s = re.sub(r"\b([a-d])\s*$", "", s)                                  # trailing 2a / 3b suffix letters
    s = re.sub(r"[:\-–|]+", " - ", s)
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"(\s-\s)+", " - ", s).strip(" -")
    return s or "Main"


def track_norm(s):
    s = re.sub(r"\b(email|emails|flow)\b", "", (s or "").lower())
    return re.sub(r"[^a-z0-9]+", "", s)


def analyse(d):
    nodes = {n["id"]: n for n in d["nodes"]}
    out = defaultdict(list)
    for e in d["connections"]:
        out[e["source"]["node_id"]].append((e["source"]["connector_index"], e["destination"]["node_id"]))
    connected = {e["source"]["node_id"] for e in d["connections"]} | {e["destination"]["node_id"] for e in d["connections"]}

    triggers = [n for n in d["nodes"] if "trigger" in n["type"] and n.get("active", True) is not False]
    # Dijkstra on delay; state carries (live, path labels)
    best = {}
    pq = []
    for t in triggers:
        heapq.heappush(pq, (0.0, 0, t["id"], True, ()))
    seq = 1
    while pq:
        h, _, nid, live, path = heapq.heappop(pq)
        key = (nid, live)
        if key in best:
            continue
        best[key] = (h, path)
        n = nodes.get(nid)
        if not n:
            continue
        h2 = h + wait_hours(n)
        for ci, dst in out.get(nid, []):
            l2, p2 = live, path
            if n["type"] == "ab-split":
                vs = n.get("variants", [])
                v = vs[ci - 1] if 0 < ci <= len(vs) else None
                if v is not None:
                    if not v.get("percentage"):
                        l2 = False
                    p2 = path + (f"{n.get('name') or 'A/B'}: {v['name']} {v.get('percentage', 0)}%",)
            seq += 1
            heapq.heappush(pq, (h2, seq, dst, l2, p2))

    # ---- branch structure: which split outputs each message sits under
    def reach(start):
        seen, st = set(), [start]
        while st:
            x = st.pop()
            if x in seen:
                continue
            seen.add(x)
            st.extend(dst for _, dst in out.get(x, []))
        return seen
    msg_ids = {n["id"] for n in d["nodes"] if n["type"] in MSG_TYPES}
    decisions = defaultdict(list)  # msg id -> [(kind, label)]
    for b in d["nodes"]:
        if b["type"] not in ("ab-split", "condition", "segmentation-fork"):
            continue
        outs = defaultdict(set)
        for ci, dst in out.get(b["id"], []):
            outs[ci] |= reach(dst)
        with_msgs = {ci: r for ci, r in outs.items() if r & msg_ids}
        if len(with_msgs) < 2:
            continue
        excl = {ci: (r - set().union(*[o for c2, o in outs.items() if c2 != ci])) & msg_ids
                for ci, r in with_msgs.items()}
        # one message per branch = a single-email test (stack); longer branches = separate rows
        rejoin = sum(1 for e in excl.values() if len(e) >= 2) < 2
        depth = min((best[k][0] for k in ((b["id"], True), (b["id"], False)) if k in best), default=9e9)
        for ci, r in with_msgs.items():
            others = set().union(*[o for c2, o in outs.items() if c2 != ci])
            if b["type"] == "ab-split":
                vs = b.get("variants", [])
                v = vs[ci - 1] if 0 < ci <= len(vs) else {"name": f"Branch {ci}", "percentage": None}
                label = f"{v['name']} ({v.get('percentage')}%)"
            elif b["type"] == "condition":
                label = f"{(b.get('name') or 'Condition').strip()}: {'Yes' if ci == 1 else 'No'}"
            else:
                label = f"{(b.get('name') or 'Segment').strip()} #{ci}"
            for m in (r - others) & msg_ids:
                decisions[m].append(("test" if rejoin else "lane", label, depth))

    msgs = []
    for n in d["nodes"]:
        ch = MSG_TYPES.get(n["type"])
        if not ch:
            continue
        data = (n.get("design") or {}).get("data") or {}
        if (n["id"], True) in best:
            status, (h, path) = "live", best[(n["id"], True)]
        elif (n["id"], False) in best:
            status, (h, path) = "0% traffic", best[(n["id"], False)]
        elif n["id"] in connected:
            status, h, path = "unreachable", None, ()
        else:
            status, h, path = "not connected", None, ()
        html = data.get("jinja_html") or ""
        body = ""
        if ch == "SMS":
            body = re.sub(r"\s*Unsubscribe:.*$", "", (n.get("content") or {}).get("message", ""), flags=re.S)
        elif ch == "WhatsApp":
            tr = next(iter(((n.get("message") or {}).get("translations") or {}).values()), {})
            body = "Template: " + str(tr.get("id", "?"))
        msgs.append({
            "node_id": n["id"], "channel": ch, "name": (n.get("name") or "").strip(),
            "track": lane_key(n.get("name")),
            "lane": " / ".join(l for k, l, _ in sorted(decisions[n["id"]], key=lambda t: t[2]) if k == "lane") or "Main",
            "test": " / ".join(l for k, l, _ in decisions[n["id"]] if k == "test"),
            "status": status,
            "day": None if h is None else round(h / 24, 1),
            "path": list(path),
            "subject": (data.get("subject") or "").strip(),
            "preheader": (data.get("preheader") or "").strip(),
            "body": body.strip() if ch != "Email" else "",
            "html_hash": hashlib.sha1(html.encode()).hexdigest()[:16] if html else None,
        })
    from collections import Counter
    cnt = Counter((m["channel"], track_norm(m["track"])) for m in msgs if m["status"] == "live")
    names = defaultdict(Counter)
    for m in msgs:
        names[(m["channel"], track_norm(m["track"]))][m["track"]] += 1
    for m in msgs:
        k = (m["channel"], track_norm(m["track"]))
        if cnt[k] >= 3:
            m["row"] = names[k].most_common(1)[0][0]
        else:
            m["row"] = m["lane"] if m["lane"] != "Main" else f"{m['channel']} sequence"
    msgs.sort(key=lambda m: (m["lane"], m["day"] if m["day"] is not None else 9e9, m["name"]))

    trig_desc = []
    for t in [n for n in d["nodes"] if "trigger" in n["type"]]:
        if t["type"] == "on-event-trigger":
            trig_desc.append("On event: " + (t.get("event") or {}).get("type", "?"))
        elif t["type"] == "repeated-trigger":
            trig_desc.append("Repeating schedule")
        else:
            trig_desc.append(t["type"].replace("-", " "))
        if t.get("active") is False:
            trig_desc[-1] += " (off)"
    other = sorted({(n.get("name") or n["type"]).strip() for n in d["nodes"]
                     if n["type"] in ("batch-webhook-action", "per-customer-webhook-action", "set-property-action-raw")
                     and ((n["id"], True) in best)})
    return {
        "other_actions": other,
        "id": d["_id"], "name": d["name"].strip(), "status": d.get("status"),
        "edited": d.get("edited"), "edited_by": d.get("edited_by_display_name"),
        "triggers": sorted(set(trig_desc)),
        "ab_tests": sum(1 for n in d["nodes"] if n["type"] == "ab-split"),
        "messages": msgs,
    }


def main():
    raw = sorted(glob.glob(os.path.join(HERE, "raw", "*.json")))
    model = [analyse(json.load(open(f))) for f in raw]
    json.dump(model, open(os.path.join(HERE, "model.json"), "w"), indent=1, ensure_ascii=False)
    for f in model:
        from collections import Counter
        c = Counter(m["status"] for m in f["messages"])
        lanes = {m["lane"] for m in f["messages"] if m["status"] == "live"}
        print(f"{f['name'][:42]:42} {dict(c)} live lanes={len(lanes)}")


if __name__ == "__main__":
    main()
