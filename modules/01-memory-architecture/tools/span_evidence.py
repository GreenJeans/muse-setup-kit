#!/usr/bin/env python3
"""
span_evidence.py — span-based evidence for memory claims.

Reference implementation from the Muse Setup Kit, Module 01 (Memory
Architecture). Distilled from a working installation where this gate runs
daily over machine-drafted memory pages.

Evidence is stored as a SPAN, not pasted text:
  {source, entry, start, end, entry_hash}
- source: path of the source document (relative to the memory workspace)
- entry: index of the entry (blank-line-delimited block) inside the source
- start/end: character offsets WITHIN the entry
- entry_hash: sha256 of the entry's full text at resolution time, recomputed
  on every verify — an edit to the entry breaks verification loudly (STALE).

Properties: a span cannot cross an entry boundary, so a quote stitched from
two entries is unrepresentable; a quote stitched from two fragments of one
entry does not resolve (the glued string does not exist contiguously).

Plus the token-containment check: every hard token in the claim — known
names, dates, amounts/numbers — must appear inside the span's text. It does
not judge whether the claim is a fair reading of the span (a sampled
fidelity check does that); it catches a claim quietly adding a fact its
evidence does not contain.

Normalization (shared by resolve + any string-match fallback): markdown
emphasis is stripped on both sides — **, __, and single * when it hugs a
word character on either side; whitespace runs collapse to one space.
"""
import hashlib, re

# ---------- normalization with an offset map ----------

def _strip_emphasis(s):
    """Remove emphasis markers, returning (clean, keep_mask over s)."""
    keep = [True] * len(s)
    i = 0
    while i < len(s):
        if s.startswith("**", i) or s.startswith("__", i):
            keep[i] = keep[i + 1] = False
            i += 2
            continue
        if s[i] == "*":
            prev = s[i - 1] if i > 0 else " "
            nxt = s[i + 1] if i + 1 < len(s) else " "
            if prev.isalnum() or nxt.isalnum():  # emphasis hugs a word char
                keep[i] = False
        i += 1
    return keep

def norm_with_map(s):
    """Normalize s (emphasis stripped, whitespace collapsed) and return
    (normalized, index_map) where index_map[j] is the raw offset in s of
    normalized character j."""
    keep = _strip_emphasis(s)
    out, idx = [], []
    i = 0
    while i < len(s):
        if not keep[i]:
            i += 1
            continue
        if s[i].isspace():
            j = i
            while j < len(s) and keep[j] and s[j].isspace():
                j += 1
            if out and (j < len(s)):
                out.append(" ")
                idx.append(i)
            i = j
            continue
        out.append(s[i])
        idx.append(i)
        i += 1
    return "".join(out), idx

def norm(s):
    return norm_with_map(s or "")[0]

# ---------- entries ----------

def segment_entries(text):
    """Split a source into entries: blank-line-delimited blocks.
    Returns [(start, end)] raw char ranges (entry text = text[start:end])."""
    entries, start = [], None
    pos = 0
    for line in text.splitlines(keepends=True):
        if line.strip() == "":
            if start is not None:
                entries.append((start, pos))
                start = None
        elif start is None:
            start = pos
        pos += len(line)
    if start is not None:
        entries.append((start, len(text)))
    return entries

def entry_hash(entry_text):
    return hashlib.sha256(entry_text.encode("utf-8")).hexdigest()

# ---------- span resolution & verification ----------

def resolve_span(source_rel, source_text, quote):
    """Locate quote in source_text and return (span, None) or (None, reason).
    Reasons: 'not_found', 'crosses_entry', 'empty_quote'."""
    if not quote or not norm(quote):
        return None, "empty_quote"
    nsrc, idx = norm_with_map(source_text)
    nq = norm(quote)
    at = nsrc.find(nq)
    if at == -1:
        return None, "not_found"
    raw_start = idx[at]
    raw_end = idx[at + len(nq) - 1] + 1
    for n, (es, ee) in enumerate(segment_entries(source_text)):
        if es <= raw_start and raw_end <= ee:
            entry_text = source_text[es:ee]
            return {
                "source": source_rel,
                "entry": n,
                "start": raw_start - es,
                "end": raw_end - es,
                "entry_hash": entry_hash(entry_text),
            }, None
        if es <= raw_start < ee or es < raw_end <= ee:
            return None, "crosses_entry"
    return None, "crosses_entry"

def verify_span(source_text, span):
    """Re-check a span against the (possibly edited) source.
    Returns (True, evidence_text) or (False, reason: 'stale'|'entry_gone'|'bad_range')."""
    entries = segment_entries(source_text)
    n = span.get("entry", -1)
    if n < 0 or n >= len(entries):
        return False, "entry_gone"
    es, ee = entries[n]
    entry_text = source_text[es:ee]
    if entry_hash(entry_text) != span.get("entry_hash"):
        return False, "stale"
    if not (0 <= span["start"] < span["end"] <= len(entry_text)):
        return False, "bad_range"
    return True, entry_text[span["start"]:span["end"]]

# ---------- token containment ----------

MONTHS = {m: i + 1 for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july",
     "august", "september", "october", "november", "december"])}
MONTHS.update({m[:3]: v for m, v in list(MONTHS.items())})
STOPWORDS = {"The", "This", "That", "These", "Those", "His", "Her", "Its",
             "Their", "Our", "Your", "When", "While", "After", "Before",
             "On", "In", "At", "By", "For", "With", "From", "Into", "Over",
             "Under", "Between", "Monday", "Tuesday", "Wednesday",
             "Thursday", "Friday", "Saturday", "Sunday"}

def _dates_in(text):
    """All recognizable dates in text, as (y, m, d) tuples (d may be None)."""
    out = set()
    for m in re.finditer(r"\b(\d{4})-(\d{2})-(\d{2})\b", text):
        out.add((int(m.group(1)), int(m.group(2)), int(m.group(3))))
    for m in re.finditer(r"\b([A-Za-z]+)\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})\b", text):
        mon = MONTHS.get(m.group(1).lower())
        if mon:
            out.add((int(m.group(3)), mon, int(m.group(2))))
    for m in re.finditer(r"\b(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]+)\.?,?\s+(\d{4})\b", text):
        mon = MONTHS.get(m.group(2).lower())
        if mon:
            out.add((int(m.group(3)), mon, int(m.group(1))))
    return out

def _numbers_in(text):
    """Digit-strings of every number in text, commas removed ('3472282')."""
    out = set()
    for m in re.finditer(r"\$?\d[\d,]*\.?\d*\s?%?", text):
        digits = re.sub(r"[^\d]", "", m.group(0).split(".")[0])
        if digits:
            out.add(digits)
        dec = m.group(0)
        if "." in dec:
            out.add(re.sub(r"[^\d]", "", dec))
    return out

def _names_in(claim, registry_names):
    """Hard name tokens in the claim: registry names present in it, plus
    capitalized multiword sequences that are not sentence furniture."""
    found = set()
    low = claim.lower()
    for name in registry_names:
        if name and name.lower() in low:
            found.add(name)
    for m in re.finditer(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b", claim):
        seq = m.group(1)
        if seq.split()[0] not in STOPWORDS:
            found.add(seq)
    return found

def token_containment(claim, evidence_text, registry_names=(), context_dates=()):
    """Return a list of hard tokens in the claim that do NOT appear inside
    the evidence text. Empty list = containment holds.

    context_dates: dates that count as contained without appearing in the
    span — deliberately narrow: the date of a dated daily log
    (memory/YYYY-MM-DD.md) is metadata printed on the evidence's face, so a
    claim dating an event to its own log's day adds nothing. Callers pass it
    ONLY for that source shape (refinement recorded 2026-11-23)."""
    missing = []
    ev_low = evidence_text.lower()
    ev_dates = _dates_in(evidence_text) | set(context_dates)
    ev_numbers = _numbers_in(evidence_text)
    for d in _dates_in(claim):
        if d not in ev_dates:
            missing.append(f"date {d[0]}-{d[1]:02d}" + (f"-{d[2]:02d}" if d[2] else ""))
    claim_numbers = _numbers_in(claim)
    # a number that is just a date component is already covered by the date check
    date_parts = set()
    for (y, m, dd) in _dates_in(claim):
        date_parts |= {str(y), str(m), f"{m:02d}", str(dd) if dd else "",
                       f"{dd:02d}" if dd else ""}
    for num in claim_numbers:
        if num in date_parts:
            continue
        if num not in ev_numbers:
            missing.append(f"number {num}")
    for name in _names_in(claim, registry_names):
        if name.lower() not in ev_low:
            missing.append(f"name {name}")
    return missing
