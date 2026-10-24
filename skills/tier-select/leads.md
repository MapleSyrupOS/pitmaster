# tier-select: the lead table

**Last checked: 2026-10-16.** Flag this table when it is more than about three months old.

Each row answers: **what tier and effort should the lead (the session that dispatches, judges and lands) be for
this comrun?** Workers are part B of `SKILL.md`; the vendor's roster in `rosters/` turns a tier into a model.

**A lead is large only when it is itself the final judge of large-tier work** (untrusted input, memory safety,
security design); a lead that only reads verdicts and lands does a mid-shaped job. Effort is
`high` unless a row says otherwise: no record so far separates a `high` lead's outcome from an `xhigh` one's, and
`high` costs less per turn. **Context, not the model, is what usually ends a lead's comrun**: plan the handoff by
the lead's own context (`budget-select`) whichever row is chosen.

These rows are defaults, derived from one project's lead records (the pseudonymized
originals are kept in pitmaster's private repository). Rule them row by row for your own project: write "(ruled by <name>,
<date>)" after a row you confirm, and keep a row you change, struck through, beside the new one.

| # | comrun shape (what the lead judges) | recommend | cheaper option | why |
|---|---|---|---|---|
| L1 | **Overnight or swarm with large-tier streams**: the lead rules on parser, memory-safety or security verdicts, builds integration branches, and lands | **large, high** | mid, xhigh, with every large-tier verdict tie-broken by a large-tier worker | the lead is the final judge of large-tier work |
| L2 | **Debt night or queue drain**: spec'd fixes with tests; the lead checks file lists and verdicts and merges on green | **mid, high** | — | the lead's work is checking and merging |
| L3 | **Dispatch-only comrun**: the lead reads verdicts and lands; the judging is the workers' | **mid, high** | — | give it its closing steps as a checklist: a mid lead once skipped its digest |
| L4 | **Arc opening or design**: boards, ADRs, a plan with the user live | **mid, xhigh**; **large, high** when the design is security design | mid, high | open-ended, but the judging is shared with the user |
| L5 | **Prompt-writing session** (a bbq, a handoff, a kickoff) with no workers of its own | **mid, high** | — | it asks and writes; it dispatches nothing |
| L6 | **The top tier as lead** | only when the user names it | — | the top tier is kept for disputes and final passes |
