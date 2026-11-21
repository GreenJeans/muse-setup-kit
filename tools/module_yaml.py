#!/usr/bin/env python3
"""module_yaml.py — the kit's strict parser for module.yaml files.

Authored metadata in the kit (module.yaml, advisories.yaml) uses a
strict flat subset of YAML, parsed here with no third-party
dependency. The subset is deliberately small:

  - top-level `key: value` scalars (bare, "double-quoted", or an
    integer; the literal `null` — that exact spelling, lowercase —
    means no value);
  - inline lists: `key: [a, b, c]` (and `key: []`);
  - block lists under a key, indented two spaces:
        key:
          - a scalar item
          - name: a map item
            extra: its second key (indented four spaces)
    A list item is a scalar or a one-level map whose values are
    scalars or inline lists of scalars. A list item may not
    itself be a list. Nothing nests deeper.

Everything outside the subset is an ERROR, never a silent misparse:
nested maps, anchors and aliases, block (multi-line) scalars, flow
maps, tabs, duplicate keys, inconsistent indentation, document
markers — and the scalar spellings full YAML would reinterpret:
inline comments (`value # note`), single-quoted scalars, tags
(`!!str x`), nested lists in either form, YAML's other null and
boolean spellings (`~`, `Null`, `true`, `false`, and the YAML 1.1
family `y`, `yes`, `n`, `no`, `on`, `off`, in any case), and
unescaped double quotes inside a bare scalar. A scalar that needs
one of those spellings gets double quotes and stays a string.
Every error names the file and the line. Generated files
(directory.json, advisories.json) are JSON instead; this parser is
only for files a human authors.

Usage:
    python3 tools/module_yaml.py FILE          print the parsed
                                               document as JSON
    python3 tools/module_yaml.py --parity DIR  check DIR/module.yaml
                                               against DIR/MODULE.md's
                                               header block (prose
                                               fields and class sets)

Exit code: 0 = ok, 1 = parse or parity failure, 2 = bad arguments.
"""
import json
import os
import re
import sys

KEY = re.compile(r"^([a-z][a-z0-9_]*):")
INT = re.compile(r"^-?\d+$")

# YAML spellings this subset refuses to reinterpret. Only the
# literal `null` is a null here; the rest are strings a full YAML
# parser would silently turn into booleans or nulls, so the subset
# rejects them outright — quote the value if the string is meant.
# The y/n/yes/no/on/off family is YAML 1.1's boolean spellings:
# the same silent reinterpretation, the same rejection.
YAML_SPELLINGS = ("~", "Null", "NULL", "True", "TRUE", "False",
                  "FALSE", "true", "false", ".nan", ".inf", "-.inf",
                  "+.inf",
                  "y", "Y", "yes", "Yes", "YES",
                  "n", "N", "no", "No", "NO",
                  "on", "On", "ON", "off", "Off", "OFF")

# The class vocabularies module.yaml declares and MODULE.md
# headers repeat (docs/library.md). kit_selfcheck imports these
# from here so the two tools cannot drift apart.
DATA_CLASSES = ("none", "personal", "financial", "health",
                "third-party")
ACTION_CLASSES = ("none", "send", "file", "spend", "delete",
                  "contact")


class ModuleYamlError(Exception):
    def __init__(self, path, line, message):
        super().__init__(f"{path}:{line}: {message}")
        self.path, self.line, self.message = path, line, message


def _fail(path, line, message):
    raise ModuleYamlError(path, line, message)


def _reject_comment(raw, path, lineno):
    """An inline comment (` #…`) outside double quotes is outside
    the subset: it is how a value like `null # pending` would
    otherwise be silently absorbed into the string."""
    in_q = False
    i = 0
    while i < len(raw):
        c = raw[i]
        if in_q:
            if c == "\\":
                i += 2
                continue
            if c == '"':
                in_q = False
        elif c == '"':
            in_q = True
        elif c == "#" and (i == 0 or raw[i - 1] in " \t"):
            _fail(path, lineno, "inline comments are outside the "
                                "subset (put the note on its own "
                                "line, starting with #)")
        i += 1


def _parse_scalar(raw, path, lineno):
    """Parse one scalar token (already stripped of outer spaces)."""
    if raw == "":
        _fail(path, lineno, "empty value (a key with no value must "
                            "introduce a block list)")
    _reject_comment(raw, path, lineno)
    if raw[0] in "&*":
        _fail(path, lineno, "anchors and aliases are outside the subset")
    if raw[0] in "|>":
        _fail(path, lineno, "block (multi-line) scalars are outside "
                            "the subset")
    if raw[0] == "{":
        _fail(path, lineno, "flow maps are outside the subset")
    if raw[0] == "!":
        _fail(path, lineno, "tags (e.g. !!str) are outside the subset")
    if raw[0] == "'":
        _fail(path, lineno, "single-quoted scalars are outside the "
                            "subset (use double quotes, or bare)")
    if raw[0] == "[":
        if not raw.endswith("]"):
            _fail(path, lineno, "unterminated inline list")
        inner = raw[1:-1].strip()
        if not inner:
            return []
        items = []
        for part in _split_list(inner, path, lineno):
            part = part.strip()
            if part.startswith("["):
                _fail(path, lineno, "nested lists are outside the "
                                    "subset")
            items.append(_parse_scalar(part, path, lineno))
        return items
    if raw[0] == '"':
        out, i = [], 1
        while i < len(raw):
            c = raw[i]
            if c == "\\":
                if i + 1 >= len(raw) or raw[i + 1] not in '"\\':
                    _fail(path, lineno, "unsupported escape in quoted "
                                        "scalar (only \\\" and \\\\)")
                out.append(raw[i + 1])
                i += 2
                continue
            if c == '"':
                if i != len(raw) - 1:
                    _fail(path, lineno, "content after the closing "
                                        "quote of a scalar")
                return "".join(out)
            out.append(c)
            i += 1
        _fail(path, lineno, "unterminated double-quoted scalar")
    if raw == "null":
        return None
    if raw in YAML_SPELLINGS:
        _fail(path, lineno, f"{raw!r} is a YAML null/boolean spelling "
                            f"outside the subset (only the literal "
                            f"'null' is a null; quote the value if "
                            f"the string is meant)")
    if '"' in raw:
        _fail(path, lineno, "a bare scalar may not contain double "
                            "quotes (quote the whole value)")
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
                if item_text.startswith("- ") or item_text == "-":
                    _fail(path, lineno2, "nested block sequences are "
                                         "outside the subset")
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
                    val = _parse_scalar(item_text, path, lineno2)
                    if isinstance(val, list):
                        _fail(path, lineno2, "a block-list item may "
                                             "not itself be a list — "
                                             "nested lists are outside "
                                             "the subset")
                    items.append(val)
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
PROSE_FIELDS = ("reads", "writes", "network", "jobs")
CLASS_FIELDS = ("data classes", "action classes")
COMPARED_LABELS = PROSE_FIELDS + CLASS_FIELDS


def header_fields(module_md_text):
    """Extract the compared header fields of a MODULE.md —
    Reads/Writes/Network/Jobs plus Data classes / Action classes —
    whitespace-normalized, as a dict of lowercase keys.

    A field's value runs to the next *compared* label, not the
    next bold label of any kind: an unrecognized bold label inside
    a value is part of that value, so inserting one cannot
    truncate what parity compares. A repeated compared label is
    recorded under '<name> (duplicate)' so check_parity can fail
    on it — last-wins would let a second label steer the check."""
    head_lines = []
    for line in module_md_text.splitlines():
        if line.startswith("## ") and head_lines:
            break
        head_lines.append(line)
    head = " ".join(head_lines)
    labels = [(m.start(), m.end(), m.group(1).strip().lower())
              for m in LABEL.finditer(head)]
    compared = [t for t in labels if t[2] in COMPARED_LABELS]
    fields = {}
    for idx, (start, end, name) in enumerate(compared):
        stop = compared[idx + 1][0] if idx + 1 < len(compared) \
            else len(head)
        value = head[end:stop].replace("**", " ")
        value = re.sub(r"\s+", " ", value).strip()
        if name in fields:
            fields[name + " (duplicate)"] = value
        else:
            fields[name] = value
    return fields


NEGATIONS = ("no", "not", "never", "without")


def _class_tokens(value, vocabulary):
    """The vocabulary tokens a header class line names, as a set.
    The line may carry prose around the tokens (module 02's line
    explains itself); parity binds the token set, not the prose.
    A token named only under an immediate negation — "no financial
    data is held" — does not count: the header there is denying
    the class, not declaring it, and a negation is not a
    declaration. (A class the header both declares and negates
    in different clauses counts as declared.)"""
    found = set()
    for token in vocabulary:
        for m in re.finditer(r"(?<![a-z-])" + re.escape(token) +
                             r"(?![a-z-])", value):
            before = value[:m.start()].rstrip()
            prev = before.rsplit(" ", 1)[-1].strip("—–-();,").lower() \
                if before else ""
            if prev in NEGATIONS:
                continue
            found.add(token)
            break
    return found


def check_parity(module_dir):
    """Return a list of parity problems between DIR/module.yaml and
    the header block of DIR/MODULE.md: the four prose fields must
    agree verbatim (whitespace-normalized), and the Data classes /
    Action classes lines must name the same class sets the
    module.yaml declares — those are the fields the risk-class
    gate acts on, so they bind as sets, not as decoration."""
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
    for name in COMPARED_LABELS:
        if name + " (duplicate)" in fields:
            problems.append(f"{md_path}: header repeats the "
                            f"{name} label — parity cannot bind a "
                            f"steered header")
    for name in PROSE_FIELDS:
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
    for name, vocab in (("data classes", DATA_CLASSES),
                        ("action classes", ACTION_CLASSES)):
        key = name.replace(" ", "_")
        if name not in fields:
            problems.append(f"{md_path}: header has no {name} field")
            continue
        yval = data.get(key)
        if not isinstance(yval, list) or \
                not all(isinstance(x, str) for x in yval):
            problems.append(f"{yaml_path}: {key} is missing or not a "
                            f"list of class names")
            continue
        header_set = _class_tokens(fields[name], vocab)
        if header_set != set(yval):
            problems.append(
                f"{module_dir}: {name} disagree — MODULE.md header "
                f"names {sorted(header_set)}, module.yaml declares "
                f"{sorted(set(yval))}")
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
