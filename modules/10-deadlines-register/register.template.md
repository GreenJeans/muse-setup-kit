# Deadlines & expiry register

<!-- Template from the Muse Setup Kit (module 10). One row per
document that expires. This file records what a document is, when
it expires, and where the original lives — never the document's
number: no passport, policy, licence, or ID numbers (procedures
§13). It is an accumulating file: it grows by design in ordinary
use and is inventoried in the install baseline, never diffed. -->

## Current

- <ITEM — passport / driving licence / insurance policy /
  warranty / certification> — expires <YYYY-MM-DD>, lead time
  <e.g. 6 months>, on expiry: renew. Source: <where the original
  lives>. State: current.
- <ITEM> — expires unknown, lead time <e.g. 1 month>, on expiry:
  renew. Source: <where the original lives>. State: undated.

<!-- An item whose date nobody has read yet is recorded as
unknown, never omitted. Its lead time is the provisional window
that applies the day the date is read. State is current,
expired, or undated — renewal is an event, not a state. Rows
that would read alike carry the holder's first name or a
user-chosen label, never a number or part of one. Surfacing,
when module 02 is installed: an item appears in the brief's
Today section on the first day today >= expiry − lead time, and
stays until renewed or dropped; an item past its expiry appears
in Failures until it is renewed or dropped — or, when its
on-expiry field says lapse, surfaces once and retires to
History as lapsed; an unknown item appears in Today as a
one-line chase item in every brief until it is dated or
dropped. Without a brief, this file is read by hand on the
cadence recorded in the plan. -->

## History

<!-- Renewals, drops, and lapses land here. When an item is
renewed, its row above updates in place — new expiry, state
current — and the old expiry moves here with the renewal date.
A dropped item records the drop date and the user's reason; a
lapsed item records the expiry it was not renewed past. Nothing
here is deleted. -->

- <ITEM> — old expiry <YYYY-MM-DD>, renewed <YYYY-MM-DD> (new
  expiry <YYYY-MM-DD>).
- <ITEM> — dropped <YYYY-MM-DD>: <the user's reason, in their
  words>.
- <ITEM> — lapsed <YYYY-MM-DD>: expired and not renewed (on
  expiry: lapse).
