# ADR-009 — spend-ledger: what a session spent, beside what it landed

**Status:** ACCEPTED — ratified by the owner 2026-10-20
**Built:** LANDED — `skills/spend-ledger/SKILL.md`, `skills/spend-ledger/scripts/spend-ledger.py`, `skills/spend-ledger/scripts/prices.tsv`
**Public copy:** approved by the owner 2026-10-21; the private ADR is the record.

## Decision

pitmaster gains a skill, **spend-ledger**, that records what each session actually spent beside what it landed,
one row per session in an append-only ledger in the project, and reports spend per landing over a window. It is
the after-the-fact twin of `budget-select`: that skill sets a share before a run, this one measures it afterwards.
It has two jobs, **close** (one session) and **report** (a window). Its script reads token counts straight from
Claude Code and Codex transcripts, so spend is measured, not remembered. It keeps three figures apart: tokens
(measured), the meter (read before and after) and the points this session moved, which it estimates when other
sessions shared the meter.

## The rules

1. **Triggers:** `spend-ledger`, `log the spend`, `what did this run cost`, `what did we get for the points`,
   `cost per PR`, and session close in a project that keeps a ledger. Near-misses go to their owners: a budget
   before a run to `budget-select`, a model choice to `tier-select`, a live token breakdown to the platform.
2. **The row:** date, session, platform, lead, window, tokens by kind (fresh, cached, written, out), workers'
   share, model mix, list price (a proxy), meter (start and end, alone or shared, estimated points), landed (a
   count, then links), note.
3. **Measured, read, estimated:** tokens come from the transcript; the meter is read, never guessed (otherwise
   `not read`); points are the whole movement only when no other session on the machine overlapped, and an
   estimated share by list-price weight when one did.
4. **Landed:** PRs merged or opened, branches pushed with work, ADRs ratified, records committed. A zero is
   allowed and carries a note saying what the session produced instead.
5. **Append-only:** a correction is a new row for the same session; the report keeps the latest.
6. **One measurement, two records:** when `budget-select`'s calibration row is due, its token columns take this
   skill's figures. The points-spent lines of carte-blanche and dealers-choice take the meter figure.
7. **Privacy:** the ledger holds numbers and links only, never prompt text or file contents. Other projects'
   transcripts are read for the overlap count alone.
8. **The proxy:** list prices from a dated `prices.tsv` beside the script. A model with no row shows a dash and is
   shared by output tokens. The proxy is never called a bill or the meter.
9. **When it runs:** on ask, and at session close wherever the project already has a ledger file. No hook yet.

## Alternatives

- **A separate skill with its own ledger** (chosen). Every session gets a row, not only those that dispatched
  workers, and landings sit beside spend. Cost: a second table beside `budget-select`'s calibration log, so rule 6
  must keep them from disagreeing.
- **Fold it into budget-select as a last step** (not chosen). That skill loads only when workers are dispatched,
  so most sessions would never reach the step.
- **Report only, from transcripts, with no ledger** (not chosen). Nothing to keep in step, but landings are not in
  transcripts, transcripts age out, and cloud sessions never reach this machine.
- **Carry an older single-project usage script over unchanged** (not chosen). One project and one platform only.

## Consequences

- Every session's cost sits beside what it landed, readable by any later session; on Codex the meter is measured
  with no asking, since its transcripts carry the reading.
- The points estimate leans on list prices, which are not the meter's weights, and chats this machine cannot see
  still move the meter, so `alone here` can overstate a session's points.
- Commits us to keeping `prices.tsv` dated and the row's columns in step with the script's parser.

## History

- 2026-10-20: proposed.
- 2026-10-20: ratified by the owner.
