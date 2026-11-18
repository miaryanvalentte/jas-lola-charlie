#!/usr/bin/env python3
"""Write each live email's HTML (Jinja resolved leniently) to flowmap/html/<hash>.html
so render.js can screenshot it. Skips hashes that already have a PNG in images/."""
import glob, hashlib, json, os, re
import jinja2

HERE = os.path.dirname(os.path.abspath(__file__))


class Blank(jinja2.Undefined):
    """Undefined that tolerates attribute access, calls, iteration and filters."""
    def __getattr__(self, name):
        if name.startswith("__"):
            raise AttributeError(name)
        return Blank()
    __getitem__ = lambda self, k: Blank()
    __call__ = lambda self, *a, **k: Blank()
    __iter__ = lambda self: iter(())
    __str__ = lambda self: ""
    __bool__ = lambda self: False
    __len__ = lambda self: 0
    __int__ = lambda self: 0
    __float__ = lambda self: 0.0


class AnyFilters(dict):
    def __missing__(self, key):
        return lambda v=None, *a, **k: v if v is not None else ""


def render(src):
    env = jinja2.Environment(undefined=Blank, extensions=["jinja2.ext.do", "jinja2.ext.loopcontrols"])
    env.filters = AnyFilters(env.filters)
    env.tests = AnyFilters(env.tests)
    try:
        return env.from_string(src).render(customer={"first_name": ""})
    except Exception:
        s = re.sub(r"{%-?\s*(if|elif|else|endif|for|endfor|set|macro|endmacro|call|endcall)[^%]*-?%}", "", src)
        s = re.sub(r"{{.*?}}", "", s, flags=re.S)
        s = re.sub(r"{%.*?%}", "", s, flags=re.S)
        s = re.sub(r"{#.*?#}", "", s, flags=re.S)
        return s


def main():
    os.makedirs(os.path.join(HERE, "html"), exist_ok=True)
    model = json.load(open(os.path.join(HERE, "model.json")))
    wanted = {m["html_hash"] for f in model for m in f["messages"] if m["status"] == "live" and m["html_hash"]}
    n = 0
    for f in glob.glob(os.path.join(HERE, "raw", "*.json")):
        for node in json.load(open(f))["nodes"]:
            data = (node.get("design") or {}).get("data") or {}
            html = data.get("jinja_html")
            if not html:
                continue
            h = hashlib.sha1(html.encode()).hexdigest()[:16]
            if h not in wanted or os.path.exists(os.path.join(HERE, "images", h + ".jpg")):
                continue
            open(os.path.join(HERE, "html", h + ".html"), "w").write(render(html))
            wanted.discard(h)
            n += 1
    print("wrote", n, "html files")


if __name__ == "__main__":
    main()
