#!/usr/bin/env python3
"""module_yaml.py — the kit's strict parser for module.yaml files.

Authored metadata in the kit (module.yaml, advisories.yaml) uses a
strict flat subset of YAML, parsed here with no third-party
dependency. The subset is deliberately small:

  - top-level `key: value` scalars (bare, "double-quoted", or an
    integer; the literal `null` means no value);
  - inline lists: `key: [a, b, c]` (and `key: []`);
  - block lists under a key, indented two spaces:
        key:
          - a scalar item
          - name: a map item
            extra: its second key (indented four spaces)
    A list item is a scalar or a one-level map of scalars. Nothing
    nests deeper.

Everything outside the subset is an ERROR, never a silent misparse:
nested maps, anchors and aliases, block (multi-line) scalars, flow
maps, tabs, duplicate keys, inconsistent indentation, document
markers. Every error names the file and the line. Generated files
(directory.json, advisories.json) are JSON instead; this parser is
only for files a human authors.

Usage:
    python3 tools/module_yaml.py FILE          print the parsed
                                               document as JSON
    python3 tools/module_yaml.py --parity DIR  check DIR/module.yaml
                                               against DIR/MODULE.md's
                                               Reads/Writes/Network/Jobs
                                               header block

Exit code: 0 = ok, 1 = parse or parity failure, 2 = bad arguments.
"""
import json
import os
import re
import sys

KEY = re.compile(r"^([a-z][a-z0-9_]*):")
INT = re.compile(r"^-?\d+$")


class ModuleYamlError(Exception):
    def __init__(self, path, line, message):
        super().__init__(f"{path}:{line}: {message}")
        self.path, self.line, self.message = path, line, message


def _fail(path, line, message):
    raise ModuleYamlError(path, line, message)


def _parse_scalar(raw, path, lineno):
    """Parse one scalar token (already stripped of outer spaces)."""
    if raw == "":
        _fail(path, lineno, "empty value (a key with no value must "
                            "introduce a block list)")
    if raw[0] in "&*":
        _fail(path, lineno, "anchors and aliases are outside the subset")
    if raw[0] in "|>":
        _fail(path, lineno, "block (multi-line) scalars are outside "
                            "the subset")
    if raw[0] == "{":
        _fail(path, lineno, "flow maps are outside the subset")
    if raw[0] == "[":
        if not raw.endswith("]"):
            _fail(path, lineno, "unterminated inline list")
        inner = raw[1:-1].strip()
        if not inner:
            return []
        return [_parse_scalar(part.strip(), path, lineno)
                for part in _split_list(inner, path, lineno)]
    if raw[0] == '"':
        if len(raw) < 2 or not raw.endswith('"'):
            _fail(path, lineno, "unterminated double-quoted scalar")
        body = raw[1:-1]
        out, i = [], 0
        while i < len(body):
            if body[i] == "\\":
                if i + 1 >= len(body) or body[i + 1] not in '"\\':
                    _fail(path, lineno, "unsupported escape in quoted "
                                        "scalar (only \\\" and \\\\)")
                out.append(body[i + 1])
                i += 2
            else:
                out.append(body[i])
                i += 1
        return "".join(out)
    if raw == "null":
        return None
    if ": " in raw or raw.endswith(":"):
        _fail(path, lineno, "a bare scalar may not contain ': ' "
                            "(quote the value, or this is a nested "
                            "map, which is outside the subset)")
    if INT.match(raw):
        return int(raw)
    return raw


def _split_list(inner, path, lineno):
    """Split an inline list body on commas outside double quotes."""
    parts, cur, in_q = [], [], False
    i = 0
    while i < len(inner):
        c = inner[i]
        if in_q:
            cur.append(c)
            if c == "\\" and i + 1 < len(inner):
                cur.append(inner[i + 1])
                i += 2
                continue
            if c == '"':
                in_q = False
        elif c == '"':
            in_q = True
            cur.append(c)
        elif c == ",":
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(c)
        i += 1
    if in_q:
        _fail(path, lineno, "unterminated quote in inline list")
    parts.append("".join(cur))
    return parts


def _parse_kv(text, path, lineno):
    """Parse `key: value` or bare `key:`; return (key, raw-or-None)."""
    m = KEY.match(text)
    if not m:
        _fail(path, lineno, f"expected 'key: value' with a key matching "
                            f"[a-z][a-z0-9_]*, got: {text!r}")
    rest = text[m.end():]
    if rest == "":
        return m.group(1), None
    if not rest.startswith(" "):
        _fail(path, lineno, "expected a space after the colon")
    return m.group(1), rest.strip()


def parse_text(text, path="<text>"):
    """Parse the strict subset; return a dict. Raises ModuleYamlError."""
    doc = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i]
        lineno = i + 1
        i += 1
        if "\t" in raw:
            _fail(path, lineno, "tabs are outside the subset")
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped in ("---", "..."):
            _fail(path, lineno, "document markers are outside the subset")
        if raw != raw.lstrip():
            _fail(path, lineno, "top-level keys are not indented "
                                "(indented content here means a nested "
                                "map, which is outside the subset)")
        key, value = _parse_kv(stripped, path, lineno)
        if key in doc:
            _fail(path, lineno, f"duplicate key: {key}")
        if value is not None:
            doc[key] = _parse_scalar(value, path, lineno)
            continue
        # Block list: items at indent 2, map continuations at indent 4.
        items = []
        while i < len(lines):
            raw2 = lines[i]
            lineno2 = i + 1
            if "\t" in raw2:
                _fail(path, lineno2, "tabs are outside the subset")
            s2 = raw2.strip()
            if not s2 or s2.startswith("#"):
                i += 1
                continue
            indent = len(raw2) - len(raw2.lstrip(" "))
            if indent == 0:
                break
            if indent == 2 and s2.startswith("- "):
                item_text = s2[2:]
                i += 1
                if KEY.match(item_text) and (
                        ": " in item_text or item_text.endswith(":")):
                    k2, v2 = _parse_kv(item_text, path, lineno2)
                    if v2 is None:
                        _fail(path, lineno2, "a list item's key with no "
                                             "value would nest deeper; "
                                             "outside the subset")
                    items.append({k2: _parse_scalar(v2, path, lineno2)})
                else:
                    items.append(_parse_scalar(item_text, path, lineno2))
                continue
            if indent == 4 and isinstance(items[-1] if items else None,
                                          dict):
                k2, v2 = _parse_kv(s2, path, lineno2)
                if v2 is None:
                    _fail(path, lineno2, "a list item's key with no value "
                                         "would nest deeper; outside "
                                         "the subset")
                if k2 in items[-1]:
                    _fail(path, lineno2, f"duplicate key in list item: {k2}")
                items[-1][k2] = _parse_scalar(v2, path, lineno2)
                i += 1
                continue
            _fail(path, lineno2, "indentation must be 0, 2 (list items), "
                                 "or 4 (list-item keys); anything else "
                                 "is a nested structure, outside the "
                                 "subset")
        if not items:
            _fail(path, lineno, f"key '{key}' has no value and no block "
                                f"list follows")
        doc[key] = items
    return doc


def parse_file(path):
    with open(path, encoding="utf-8") as fh:
        return parse_text(fh.read(), path)


LABEL = re.compile(r"\*\*([A-Za-z ]+):\*\*")


def header_fields(module_md_text):
    """Extract the Reads/Writes/Network/Jobs header block of a
    MODULE.md, whitespace-normalized, as a dict of lowercase keys.
    Any other bolded label in the block (module 10's Data classes
    line) terminates the preceding field's value."""
    head_lines = []
    for line in module_md_text.splitlines():
        if line.startswith("## ") and head_lines:
            break
        head_lines.append(line)
    head = " ".join(head_lines)
    fields = {}
    labels = list(LABEL.finditer(head))
    for idx, m in enumerate(labels):
        name = m.group(1).strip().lower()
        if name not in ("reads", "writes", "network", "jobs"):
            continue
        end = labels[idx + 1].start() if idx + 1 < len(labels) \
            else len(head)
        value = head[m.end():end].replace("**", " ")
        fields[name] = re.sub(r"\s+", " ", value).strip()
    return fields


def check_parity(module_dir):
    """Return a list of parity problems between DIR/module.yaml and
    the Reads/Writes/Network/Jobs header of DIR/MODULE.md."""
    problems = []
    yaml_path = os.path.join(module_dir, "module.yaml")
    md_path = os.path.join(module_dir, "MODULE.md")
    try:
        data = parse_file(yaml_path)
    except ModuleYamlError as exc:
        return [str(exc)]
    except OSError as exc:
        return [f"{yaml_path}: cannot read: {exc}"]
    if not os.path.isfile(md_path):
        return [f"{md_path}: missing"]
    with open(md_path, encoding="utf-8", errors="replace") as fh:
        fields = header_fields(fh.read())
    for name in ("reads", "writes", "network", "jobs"):
        if name not in fields:
            problems.append(f"{md_path}: header has no {name} field")
            continue
        yval = data.get(name)
        if not isinstance(yval, str):
            problems.append(f"{yaml_path}: {name} is missing or not a "
                            f"scalar")
        elif re.sub(r"\s+", " ", yval).strip() != fields[name]:
            problems.append(
                f"{module_dir}: {name} disagrees — MODULE.md header "
                f"says {fields[name]!r}, module.yaml says {yval!r}")
    return problems


def main(argv):
    if len(argv) == 2 and argv[0] == "--parity":
        problems = check_parity(argv[1])
        for p in problems:
            print(f"parity: {p}", file=sys.stderr)
        if problems:
            return 1
        print(f"parity ok: {argv[1]}")
        return 0
    if len(argv) == 1 and not argv[0].startswith("-"):
        try:
            data = parse_file(argv[0])
        except ModuleYamlError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        except OSError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        print(json.dumps(data, indent=2, sort_keys=True))
        return 0
    print(__doc__.strip().splitlines()[-6], file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
