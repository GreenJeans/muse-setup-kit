#!/usr/bin/env python3
"""Soul linter for the Muse Setup Kit (module 11).

Deterministic and read-only. It checks only what can be checked
mechanically about a SOUL.md; everything else about a persona is
judgment, and judgment lives in the module's failure-mode
checklist, not here. Five checks:

  A. Word count against the cap (default ~1,200 words, the
     template's governance default; --cap overrides). A file
     past its cap is a file becoming a patch log.
  B. An examples block is present and filled: a heading naming
     examples, at least eight filled exchange lines in the
     template's blockquote form (four exchanges, two lines
     each; lines still carrying a <PLACEHOLDER> do not count),
     and an anti-example.
  C. A priority order is present: a heading naming the priority
     order (or "what wins when things collide"), with at least
     three filled numbered items.
  D. A governance footer is present: a heading naming
     governance or how the file changes.
  E. Inherited boilerplate, as warnings: stock template lines
     kept because they sound right. A warning is not a finding;
     it never affects the exit code. Keep a flagged line only
     if it changes a behavior you can name.

Quiet by default: the tool prints findings and warnings only,
one per line, and nothing at all when the file is clean.

Usage:
  soul_lint.py [SOUL.md] [--cap 1200]
Exit code: 0 = no findings, 1 = findings, 2 = bad arguments.
"""

import argparse
import re
import sys

HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
NUMBERED = re.compile(r"^\s*\d+[.)]\s+(.*)$")
PLACEHOLDER = re.compile(r"<[^>\n]+>")

# Stock lines from the inherited template tradition. Matched
# against a normalized line (curly quotes straightened, case
# folded). These are detection patterns, not persona text.
BOILERPLATE = (
    (re.compile(r"not a chatbot.*becoming someone"),
     "the stock opener"),
    (re.compile(r"becoming someone"),
     "self-reflection bait: 'becoming someone' invites the "
     "agent to muse on its own nature, the conversation type "
     "most associated with drift"),
    (re.compile(r"yours to grow into"),
     "an unbounded self-edit invitation, with no approval gate"),
)


def normalize(line):
    for curly, straight in (("’", "'"), ("‘", "'"),
                            ("“", '"'), ("”", '"')):
        line = line.replace(curly, straight)
    return line.lower()


def sections(text):
    """Yield (level, title, [lines]) for each heading section."""
    out = []
    current = None
    for line in text.splitlines():
        m = HEADING.match(line)
        if m:
            current = (len(m.group(1)), m.group(2).strip(), [])
            out.append(current)
        elif current is not None:
            current[2].append(line)
    return out


def section_body(secs, title_pattern):
    """The lines under the first heading whose title matches,
    including any deeper subsections."""
    for i, (level, title, lines) in enumerate(secs):
        if title_pattern.search(title):
            body = list(lines)
            for level2, title2, lines2 in secs[i + 1:]:
                if level2 <= level:
                    break
                body.append("#" * level2 + " " + title2)
                body += lines2
            return body
    return None


def check_words(text, cap):
    n = len(text.split())
    if n > cap:
        return [f"A: {n} words, over the cap of {cap}: past the "
                f"cap, something comes out before anything goes in"]
    return []


def check_examples(secs):
    body = section_body(secs, re.compile(r"example", re.I))
    if body is None:
        return ["B: no examples block: the file's strongest "
                "steering is missing"]
    # Count filled exchange lines block by block: a blockquote
    # block (consecutive ">" lines) is filled only if no line
    # in it still carries a <PLACEHOLDER>: a wrapped slot's
    # clean continuation line is not a filled exchange.
    filled = 0
    block = []

    def flush(block):
        if block and not any(PLACEHOLDER.search(ln)
                             for ln in block):
            return sum(1 for ln in block
                       if ln.lstrip(">").strip())
        return 0

    for ln in body:
        if ln.lstrip().startswith(">"):
            block.append(ln)
        else:
            filled += flush(block)
            block = []
    filled += flush(block)
    findings = []
    if filled < 8:
        findings.append(
            f"B: examples block holds {filled} filled "
            f"exchange lines; four exchanges in the template's "
            f"blockquote form need at least 8")
    if not any("anti-example" in ln.lower() for ln in body):
        findings.append("B: no anti-example in the examples "
                        "block: the failure needs a shape too")
    return findings


def check_priority(secs):
    body = section_body(
        secs, re.compile(r"priorit|what wins when", re.I))
    if body is None:
        return ["C: no priority order: unranked values get "
                "picked per session by default pulls"]
    filled = []
    for ln in body:
        m = NUMBERED.match(ln)
        if m and m.group(1).strip() \
                and not m.group(1).strip().startswith("<"):
            filled.append(ln)
    if len(filled) < 3:
        return [f"C: priority order holds {len(filled)} filled "
                f"items; a ranking needs at least 3"]
    return []


def check_governance(secs):
    for _level, title, _lines in secs:
        if re.search(r"governance|how this file changes", title,
                     re.I):
            return []
    return ["D: no governance footer: the file's own edit "
            "rules are the main defense against drift, and "
            "they are missing"]


def check_boilerplate(text):
    warnings = []
    for i, line in enumerate(text.splitlines(), 1):
        norm = normalize(line)
        for pattern, why in BOILERPLATE:
            if pattern.search(norm):
                warnings.append(
                    f"E: line {i}: inherited boilerplate "
                    f"({why}): {line.strip()[:60]!r}")
                break
    return warnings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?", default="SOUL.md")
    ap.add_argument("--cap", type=int, default=1200)
    args = ap.parse_args()

    try:
        with open(args.path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError as exc:
        print(f"error: cannot read {args.path}: {exc}",
              file=sys.stderr)
        return 2

    secs = sections(text)
    findings = []
    findings += check_words(text, args.cap)
    findings += check_examples(secs)
    findings += check_priority(secs)
    findings += check_governance(secs)
    warnings = check_boilerplate(text)

    for msg in findings:
        print(f"- [finding] {msg}")
    for msg in warnings:
        print(f"- [warning] {msg}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
