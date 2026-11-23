# What to stop doing (a retire list)

Practices from the early agent era (peak roughly 2023 to early
2025) that the field has measured, tried at scale, and largely
abandoned. Run it against an existing setup the way you would
run `docs/governance-test.md`: each item names the practice,
what replaced it, and where that replacement lives in this
kit. An item you are still doing is not a scandal; it is a
finding with a date on it.

1. **Naive vector-only memory as the default** — embed every
   turn, retrieve top-k forever. Retrieved bulk actively harms:
   context-rot results (Chroma, Jul 2025) show performance
   degrading as retrieved volume grows, and a pile of similar
   chunks carries no provenance. Replaced by layered memory —
   transcripts, distilled notes with sources, a compiled layer,
   a small always-loaded index — with retrieval as one signal
   inside it. *Kit: module 01.*
2. **Fully autonomous swarms with shared writes** — many peer
   agents negotiating freely and editing the same artefacts.
   In CooperBench (Jan 2026), cooperating agents succeeded
   about half as often, relatively, as one agent doing both
   tasks, and communication did not rescue them; the failure
   was coordination, not collisions. Replaced by single-writer
   lanes on frozen contracts, with parallel reading and review.
   *Kit: modules 00 and 04.*
3. **Self-reflection loops as a completion gate** — the agent
   critiques its own work and declares it good. An ungrounded
   judge ratifies the assumptions that produced the work.
   Replaced by verifier-gated completion: an external check the
   agent cannot edit decides done. *Kit: modules 00 and 05.*
4. **LLM-as-judge as the sole eval or deployment gate** —
   measured false-positive rates of at least 45% and 22% for
   bundled benchmark judges against human gold labels (Rosset
   et al., Apr 2026); the same agent scored 74% under an
   official judge and 38% under a strict verifier. Judges are
   advisors for genuinely semantic criteria; deterministic
   checks and human adoption decide. *Kit: module 05.*
5. **Stuff-the-window preloading** — load everything the agent
   might need into context up front. Context is a budget;
   preloading spends it on the irrelevant and crowds out the
   relevant. Replaced by a small always-loaded layer plus
   just-in-time retrieval and progressive disclosure.
   *Kit: the wizard's reading budgets; module 01.*
6. **Loading all tool definitions up front** — retired at
   scale by deferred discovery (tool search) and code APIs:
   about 150,000 tokens of definitions became about 2,000 in
   Anthropic's worked example (Nov 2025). *Kit: module 06,
   protocol currency.*
7. **Prompt-hardening as the primary injection defense** —
   "ignore malicious instructions" and single classifiers,
   bypassed at over 90% under adaptive attack (*The Attacker
   Moves Second*, Oct 2025). No filter reliably separates
   instructions from data in one token channel. Replaced by
   structural design: the Rule of Two, least-privilege
   permissions, sandboxing. *Kit: module 06.*

Not retired, despite periodic obituaries: prompt chaining,
routing, and parallelisation as named workflow patterns;
few-shot examples; and retrieval itself — all survive as
components inside the stack above.
