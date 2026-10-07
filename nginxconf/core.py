"""解析 nginx 风格配置块。"""


class Counter:
    """记录比较次数。"""

    def __init__(self):
        self.scanned = 0


class Block:
    def __init__(self, name):
        self.name = name
        self.directives = []
        self.children = []


def _split(text):
    out = []
    current = ""
    for line in text.splitlines():
        stripped = line.split("#", 1)[0].strip()
        if not stripped:
            continue
        current += " " + stripped
        out.append(current.strip())
        current = ""
    return out


def parse(text, files, counter):
    root = Block("")
    for statement in _split(text):
        counter.scanned += 1
        if statement.endswith("{"):
            root.children.append(Block(statement[:-1].strip()))
            continue
        if statement == "}":
            continue
        if statement.endswith(";"):
            parts = statement[:-1].split(None, 1)
            key = parts[0]
            value = parts[1] if len(parts) > 1 else ""
            root.directives.append((key, value))
    return root


def lookup(root, path, key, counter):
    block = root
    for name in path:
        found = None
        for child in block.children:
            counter.scanned += 1
            if child.name == name:
                found = child
        if found is None:
            return ""
        block = found
    value = ""
    for item in block.directives:
        counter.scanned += 1
        if item[0] == key:
            value = item[1]
    return value
