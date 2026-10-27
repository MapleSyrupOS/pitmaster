---
status: accepted
status-note: — ratified by the owner 2026-10-27
ratified-by: the owner
ratified-on: "2026-10-27"
owner: the owner
kind: process
built: partial
proof: "`skills/neighbour-check/SKILL.md`, `skills/neighbour-check/scripts/neighbour-check.pin`, `skills/townhall/scripts/neighbours.pin`, `skills/spend-ledger/SKILL.md`, `evals/neighbour-check-yes-01/prompt.md`, `evals/neighbour-check-no-01/prompt.md`"
owed: the first real runs beyond the one in its PR, judged by the owner
supersedes: nothing
amends: nothing
---
# ADR-029 — neighbour-check: what limits each neighbour, and whether it is busy, read live

This is the published version of this decision. Some internal details have been left out.

## Decision

pitmaster gains a skill, **neighbour-check**, in the usage family. Before a session sends work to a neighbour (a
model other than the one the user is talking to: another model family, a local model, another account), it reads
each neighbour on townhall's allow list for two things: **what limits it** (a usage meter or quota, its reset and
its burn rate, wherever one can be read) and **whether it is busy** (jobs running, lanes held, a box in use). It
writes one Neighbours block, which a prompt carries beside budget-select's Budget block, and the session routes by
it. Where a limit cannot be read, the block says so and asks the user for the reading; it never guesses one.

1. **The names.** The skill and its shed tool are both `neighbour-check`. "checkonneighbours", the reference
   project's word, still loads it (the user, 2026-10-27: "3 as default, checkonneighbours can still work,
   though").
2. **The list is townhall's.** The neighbours come from the neighbours doc (`~/.pitmaster/neighbours.md`, or the
   doc a project's `pitmaster.md` `neighbours:` line names or narrows), read by the same code townhall's
   `neighbours` tool uses, shared as a byte-identical block in the shed. It checks only names on that list.
3. **The kinds it ships with** (the user, 2026-10-27, picking all eight): Codex (its 7-day meter, reset and burn,
   read from its own session logs); Gemini through Antigravity's agy (not readable: ask the user); OpenCode Go (a
   raw local floor beside its limits: ask the user for the weighted pool); another Claude account (its newest
   reading in the shared readings file); Ollama; LM Studio and other servers that answer on the OpenAI wire; a
   project's lane queue, only where the project has one; and a remote guard, a read-only busy check over ssh whose
   host and command come from the settings, never from the code.
4. **Every kind and every setting is editable** (the user, 2026-10-27: "this needs to be editable in some sort of
   settings too"). The skill's Config block holds the defaults; the neighbours doc's own `## neighbour-check`
   section sets them for every project on the machine; a project's `pitmaster.md` sets them for one project; a
   flag sets one run. `probes:` names the kinds that run; `kind <name>:` overrides the guess for one neighbour;
   `burn: show` is the default and `burn: hide` keeps the burn in the verdicts but prints no burn numbers.
5. **One account sees the other's meter through a shared readings file**, `~/.claude/meters.tsv`, one appended
   line per reading, never edited. neighbour-check's first step writes this session's reading, and spend-ledger's
   close writes the closing one, so the other account's next run sees how this one ended (the user asked whether
   a wrap-up step could do this, 2026-10-27).
6. **The verdicts are provisional**: closed (at 95 % or a reached limit), tight (runs out before its reset at its
   recent pace), on pace, spare (ends its window under 80 % at its pace), unknown; and free, busy, up, down for the
   neighbours with no meter. The lines are the source's, for the user to rule.

## Consequences

- Good: a session sees, before it routes, that a neighbour that looks spare is burning fast, or that a box is in
  use, and asks for the readings no file holds.
- Good: the other Claude account's meter is visible without switching accounts, as long as both write readings.
- Bad: two meters stay unreadable (agy and Go's weighted pool), so the block asks the user for them.
- Bad: the shed's `neighbours` tool changes (two marker lines), so townhall's pin moves with this one.
- Commits us to: a shed release that holds the tool, and both pins on it.

## History

- 2026-10-27: proposed.
- 2026-10-27: ratified by the owner.
