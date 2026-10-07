"""固定场景，用来复现题面里的锚点。"""

import json

from . import core


def _line(obj):
    print(json.dumps(obj, ensure_ascii=False))


def run(name):
    if name == "nested":
        root = core.parse("server {\n location /a {\n }\n}\n", {}, core.Counter())
        count = len(root.children[0].children) if root.children else 0
        _line({"locations": count})
        return 0
    if name == "inherit":
        text = "server {\n root /var/www;\n location /a {\n index a;\n }\n}\n"
        root = core.parse(text, {}, core.Counter())
        _line({"root": core.lookup(root, ["server", "location /a"], "root", core.Counter())})
        return 0
    if name == "last":
        text = "server {\n root /a;\n root /b;\n}\n"
        root = core.parse(text, {}, core.Counter())
        _line({"root": core.lookup(root, ["server"], "root", core.Counter())})
        return 0
    if name == "include":
        text = "include extra.conf;\n"
        files = {"extra.conf": "root /var/www;\n"}
        root = core.parse(text, files, core.Counter())
        _line({"root": core.lookup(root, [], "root", core.Counter())})
        return 0
    if name == "work":
        lines = []
        for i in range(800):
            lines.append("root /v%04d;" % i)
        root = core.parse("\n".join(lines) + "\n", {}, core.Counter())
        counter = core.Counter()
        for _ in range(800):
            core.lookup(root, [], "root", counter)
        _line({"lookups": 800, "scanned": counter.scanned})
        return 0
    raise SystemExit("未知场景：" + name)
