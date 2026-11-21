#!/usr/bin/env python3
"""Soul linter for the Muse Setup Kit (module 11).

Deterministic and read-only. It checks only what can be checked
mechanically about a SOUL.md; everything else about a persona is
judgment, and judgment lives in the module's failure-mode
checklist, not here. Six checks:

  A. Word count against the cap (default ~1,200 words, the
     template's governance default; --cap overrides). A file
     past its cap is a file becoming a patch log. The count is
     of whitespace-separated tokens containing at least one
     letter or digit: markup-only tokens (table pipes, heading
     hashes, blockquote markers, rules) are not words and are
     not counted.
  B. An examples block is present and filled. An exchange
     counts as a whole blockquote block: at least two non-empty
     lines, and no line in the block still carrying a
     placeholder. Four filled exchanges are required outside
     the anti-example subsection, and at least one filled block
     inside it. Lines are never counted — a single exchange
     wrapped over eight lines is one exchange, not four.
  C. A priority order is present: a heading naming the priority
     order (or "what wins when things collide"), with at least
     three filled numbered items. An item is filled when its
     text is non-empty and carries no placeholder anywhere in
     it (a bolded placeholder is still a placeholder).
  D. A governance footer is present and filled: a heading
     naming governance or how the file changes, and a body
     holding at least one filled line — non-empty, no
     placeholder — that names who owns the file or how a
     change is approved. A bare heading is not governance.
  E. Inherited boilerplate, as warnings: stock template lines
     kept because they sound right. Patterns are matched
     against whitespace-collapsed text, so a phrase wrapped
     across lines is still caught; the line number reported is
     where the match starts. A warning is not a finding; it
     never affects the exit code. Keep a flagged line only if
     it changes a behavior you can name.
  F. No placeholder tokens remain anywhere in the file (the
     module's VERIFY check 1). A placeholder is an
     angle-bracket span in the template's slot shapes: its
     content carries an uppercase letter, a space, or a bare
     number, and never an "@" or a "://" — an angle-bracketed
     address, URL, or markup tag is not a slot.

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
ANGLE = re.compile(r"<[^>\n]+>")

# Words that name ownership or approval in a governance line.
GOVERN_WORDS = ("approv", "owner", "staged", "propos")

# Stock lines from the inherited template tradition. Matched
# against normalized, whitespace-collapsed text (curly quotes
# straightened, case folded). These are detection patterns, not
# persona text.
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


def is_placeholder(span):
    """Whether an angle-bracket span is a template slot: slot
    shapes carry an uppercase letter, a space, or a bare
    number; addresses, URLs, and markup tags are not slots."""
    content = span[1:-1]
    if "@" in content or "://" in content:
        return False
    if any(c.isupper() for c in content):
        return True
    if " " in content:
        return True
    return content.strip("0123456789,./ ") == "" and content != ""


def placeholder_in(text):
    return any(is_placeholder(m.group(0))
               for m in ANGLE.finditer(text))


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
    n = sum(1 for tok in text.split()
            if any(c.isalnum() for c in tok))
    if n > cap:
        return [f"A: {n} words, over the cap of {cap}: past the "
                f"cap, something comes out before anything goes in"]
    return []


def _blocks(lines):
    """Yield each blockquote block: a run of consecutive lines
    starting with '>'."""
    block = []
    for ln in lines:
        if ln.lstrip().startswith(">"):
            block.append(ln)
        else:
            if block:
                yield block
            block = []
    if block:
        yield block


def _filled(block):
    """A block is filled when it holds at least two non-empty
    lines and no line in it carries a placeholder: a wrapped
    slot's clean continuation line is not a filled exchange."""
    content = [ln.lstrip(">").strip() for ln in block]
    content = [ln for ln in content if ln]
    return len(content) >= 2 \
        and not any(placeholder_in(ln) for ln in content)


def check_examples(secs):
    body = section_body(secs, re.compile(r"example", re.I))
    if body is None:
        return ["B: no examples block: the file's strongest "
                "steering is missing"]
    anti_at = None
    for i, ln in enumerate(body):
        if ln.startswith("#") and "anti-example" in ln.lower():
            anti_at = i
            break
    if anti_at is None:
        return ["B: no anti-example in the examples block: "
                "the failure needs a shape too"]
    exchanges = sum(1 for b in _blocks(body[:anti_at])
                    if _filled(b))
    anti = sum(1 for b in _blocks(body[anti_at:])
               if _filled(b))
    findings = []
    if exchanges < 4:
        findings.append(
            f"B: examples block holds {exchanges} filled "
            f"exchanges; four are required — an exchange counts "
            f"only as a whole blockquote block of at least two "
            f"lines with no placeholder left in it")
    if anti < 1:
        findings.append(
            "B: the anti-example is unfilled: its block is "
            "missing, under two lines, or still carries a "
            "placeholder — the failure needs a filled shape too")
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
                and not placeholder_in(m.group(1)):
            filled.append(ln)
    if len(filled) < 3:
        return [f"C: priority order holds {len(filled)} filled "
                f"items; a ranking needs at least 3"]
    return []


def check_governance(secs):
    body = section_body(
        secs, re.compile(r"governance|how this file changes",
                         re.I))
    if body is None:
        return ["D: no governance footer: the file's own edit "
                "rules are the main defense against drift, and "
                "they are missing"]
    for ln in body:
        if ln.startswith("#") or not ln.strip():
            continue
        if placeholder_in(ln):
            continue
        low = ln.lower()
        if any(w in low for w in GOVERN_WORDS):
            return []
    return ["D: governance footer has a heading but no filled "
            "line naming who owns the file or how a change is "
            "approved: an empty footer is not governance"]


def check_boilerplate(text):
    warnings = []
    starts = []
    parts = []
    offset = 0
    for i, line in enumerate(text.splitlines(), 1):
        norm = normalize(line)
        starts.append((offset, i))
        parts.append(norm)
        offset += len(norm) + 1
    collapsed = " ".join(parts)
    for pattern, why in BOILERPLATE:
        m = pattern.search(collapsed)
        if m:
            lineno = max(ln for off, ln in starts
                         if off <= m.start())
            warnings.append(
                f"E: line {lineno}: inherited boilerplate "
                f"({why}): {collapsed[m.start():m.start() + 60]!r}")
    return warnings


def check_placeholders(text):
    hits = [i for i, line in enumerate(text.splitlines(), 1)
            if placeholder_in(line)]
    if hits:
        return [f"F: {len(hits)} line(s) still carry a "
                f"placeholder (first at line {hits[0]}): a slot "
                f"left in the file is read as instruction — "
                f"fill it, or cut the section"]
    return []


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
    findings += check_placeholders(text)
    warnings = check_boilerplate(text)

    for msg in findings:
        print(f"- [finding] {msg}")
    for msg in warnings:
        print(f"- [warning] {msg}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
