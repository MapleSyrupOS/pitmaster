---
status: accepted
status-note: — ratified by the owner 2026-10-20
owner: the owner
kind: process
built: landed
proof: "`skills/carte-blanche/SKILL.md`"
supersedes: nothing
amends: nothing
---
# ADR-007 — carte-blanche: standing authority for one session, inside the project's rules

This is the published version of this decision. Some internal details have been left out.

## Decision

pitmaster gains a skill, **carte-blanche**, that gives one session standing authority for one comrun. Under it the
agent may pick and order its own work, commit and push its own branches, open PRs, and spend within a set budget,
starting workers or a swarm if it wants, without asking. It stops 5 points short of the budget (counted from the
lead's own ledger, not the shared meter) or when the work is done, whichever comes first, and the grant ends with
the session (amended 2026-10-21). If the lead's context runs short first, it hands off the written grant, the
ledger, the open strands and any running workers to a fresh lead (amended 2026-10-21). Merging, pushing to the
main branch, deleting work and outward-facing acts are off unless the user grants that specific act. Taste,
ratifying ADRs and editing charters are never covered. The project's own rules always win unless a specific grant
names the rule it overrides.

## The rules

> **Amended 2026-10-23 by ADR-023, ratified by the user:** the grant ladder. carte blanche merges its own PRs on
> green (rule 2), stays in this project while trescarteblanche adds the projects named (rule 4), and estimates its
> own budget, asking only above 10 points (rule 5).

1. **What it unlocks:** picking and ordering work; commits, pushes to its own branches and PRs; spend within the
   budget, workers and swarms included.
2. **What needs a named grant:** merging, pushing to main, deleting work, outward-facing acts.
3. **What is never covered:** the `never:` list, which starts as taste (naming, looks, direction), ratifying ADRs
   and editing charters. A project may add to it and never remove those three.
4. **Ceilings:** the project's rules, unless a grant explicitly names one to override; and the platform's safety
   rules and permission prompts, which no grant reaches. A project rule that already allows more stands as
   written. No grant widens how the comrun treats a shared machine: stop only a process you started, by its id, never
   by name or pattern; remove only files you made; push fast-forward only, never force (amended 2026-10-21).
5. **Starting:** the words `carte blanche` grant it. Another explicit phrase loads the skill, which asks first, so
   authority is never granted by accident. Then two questions: the budget, and whether anything extra is granted.
   A question session (a bbq, or makeadr's rounds) started under the grant is answered by the agent itself; each
   answer goes in the Defaulted list with a `veto:` line, and taste answers are flagged as proposals only
   (amended 2026-10-20). A bbq run as a stew is the exception: a subagent answers it at least, never the asking
   agent itself (amended 2026-10-23, ADR-021).
6. **Taste mid-comrun:** visual calls are built as two or three options on their own branches, with frames sent to
   the user as files and in the end summary; nothing visual lands on main until the user picks. Other taste calls
   are parked as questions.
7. **Workers:** carry the grant in a written block, never wider than the lead's. Only the lead merges, and only if
   merging was granted. A widening reaches workers only in the user's own words, added to the written grant and
   re-issued in a fresh brief, never relayed to a running worker by message (amended 2026-10-21).
8. **Failure:** stop that strand, file a one-line question, move on.
9. **Revocation:** the user's latest instruction wins at once; `stop` or `revoke` ends the grant. A narrowing
   reaches workers by any route, a message included (amended 2026-10-21).
10. **Trail:** one line per landing, marked as made under carte blanche, in the log and the PR body; an end summary
    with the Defaulted list and its veto lines.

Tools that load no plugin reach the skill through a pointer line in their global instruction file.

## Alternatives

- **A per-session declaration, written down only when it leaves the session** (chosen). Nothing to set up, and
  workers and hand-offs still carry it in writing. A solo comrun's grant lives only in its end summary.
- **A grant file in the project** (overruled). Any agent can read it, but a standing grant is a charter, which
  this skill never edits; the grant is meant to be per session.
- **Choose a provisional visual option and keep going** (overruled). Cheaper, but the user would see one choice
  rather than a real set.
- **Ask only the budget at the start** (overruled). One question, but named grants would have no place to be given.
- **Explicit phrases grant it directly** (overruled). Friendlier, but authority could be granted by accident.

## Consequences

- One phrase and two answers hand a whole comrun over, and the user can veto anything afterwards.
- Workers, swarms and hand-offs carry the same bounded grant in writing.
- Visual work costs more under a grant, since each taste call is built two or three times.
- Commits us to keeping the `never:` list in step with the project's ground rules, and to amending this ADR when
  a veto shows a rule was too loose.

## History

- 2026-10-20: proposed.
- 2026-10-20: ratified by the owner.
- 2026-10-20: amended.
- 2026-10-21: amended.
- 2026-10-23: amended.
- 2026-10-23: ratified by the owner.
- 2026-10-24: amended.
