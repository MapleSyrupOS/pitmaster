---
status: accepted
status-note: — ratified by the owner 2026-11-10
ratified-by: the owner
ratified-on: "2026-11-10"
owner: the owner
kind: process
built: partial
proof: "`skills/looseends/references/decisions-markers.txt`, `skills/looseends/SKILL.md`, `scripts/check-adr-sized.py`"
owed: "step 4: a first real run on this repository, judged by the owner"
supersedes: nothing
amends: "ADR-019 §The rules, rule 1 (Scope): a fourth scope, decisions"
---
# ADR-038 — looseends gains a decisions scope, "adrorphans", that finds past decisions no ADR covers

This is the published version of this decision. Some internal details have been left out.

## Decision

Amends ADR-019 rule 1: looseends gets a fourth scope beside chat, project and topic. It finds decisions already
made that no ADR covers and no record listed as an ADR candidate, and offers makeadr for the ones the user picks.
It is not a new skill.

1. **Two ways to start it**: "looseends decisions", and the user's word "adrorphans" (orphaned decisions
   with no ADR). Plain "looseends project" does not run it, and nothing offers it: ADR-019 rule 8 holds.
2. **Where it looks**: by default the project's records and its merged PRs: bbq records' answers,
   talk-through and townhall rows marked agreed, Defaulted rows, the status log, and the bodies of merged PRs
   (through `gh`). Commit messages only when asked for. In a project with no pitmaster-style records it reads
   merged PRs only, and says so.
3. **The scan, with a decisions markers file**: `looseends-scan.py` runs with a decisions markers file
   that ships with looseends, pointing it at the likely spots in the records. A project can swap in its own with a
   config line, as `looseends_markers` already allows. PR bodies are read by the agent, not the scan.
4. **How far back**: since the last sweep, from a dated stamp each run leaves; the first run asks for a
   start date. A date after the word overrides it for one run ("adrorphans since 2026-10-01"). A run whose window
   starts after the stamp leaves the stamp where it was, so no stretch is skipped; a run that starts at or before
   it moves the stamp to now.
5. **The judging**: each find is held to makeadr's *Is it ADR-sized?* test (ADR-036), which looseends
   carries as a checked copy. A find is covered, and dropped, when an ADR cites its record or question or plainly
   says it, or a record already lists it as an ADR candidate or as skipped. The session's model judges;
   tier-select may hand a large first sweep to workers, whose finds the lead re-judges.
6. **Strongest first**: about 10 finds a run, those that touch an existing ADR first, then those with the
   most signs. The rest are counted by record and wait for the next run.
7. **The offer, once** (ADR-036 rule 5): the finds are listed as *Yours*, each with its source and the signs it
   showed, and makeadr is offered once for the ones the user picks; each takes makeadr's light route from its
   cited source. "looseendsreally" never writes an ADR.
8. **The ledger**: one file, `docs/looseends/adrorphans.md` (under `looseends_dir`), holds the stamp and every
   find the user skipped, with its source and "not an ADR, by the user". A skipped find is never offered again.
   Old records and merged PRs stay as they were.

## Context

Drivers:
- Decisions made before ADR-036 get the same chance at an ADR as new ones.
- makeadr is still offered rarely: only when asked, once a run, about ten at a time.
- Reuse looseends' scan, list and offer instead of a new skill that repeats them.
- A "not an ADR" answer is final.

## Alternatives

### A looseends scope with a decisions markers file (chosen: no new skill, likely no new code, looseends already lists, checks, offers)
- Good: one more scope word, a markers file and a checked copy of the test; the scan, the list and the makeadr
  offer are reused.
- Bad: looseends' description and steps grow; its family (`check`) now also covers finding decisions.

### A new skill with its own gather script (the first recommendation; changed after P1 to P4)
- Good: its own name and steps, clear on its own.
- Bad: an 18th skill and description competing to load, a new shed tool, its own ADR and evals, and much of
  looseends repeated.

### A shed tool only
- Good: runs without an agent.
- Bad: it can list likely spots but cannot judge them against the test, so the user sorts many false hits.

### Records only, or everything with commits by default
- Good: records only is cheapest and works offline; commits by default is the most thorough.
- Bad: records only misses calls that only reached a PR; commit messages are noisy and mostly mechanism. Commits
  stay an option asked for by name.

### Everything every run, or a date each time
- Good: no stamp to keep; a date each time puts the window in the user's hands.
- Bad: rereading everything grows slower as the project grows; a date each time adds a question every run. The
  date stays as an override.

### Mark the skip in the source
- Good: the note sits beside the decision it is about.
- Bad: it cannot be done in a merged PR's body, and it edits old records.

### Run it in every "looseends project"
- Good: nothing slips, and no word to remember.
- Bad: every project sweep gets slower and may offer makeadr, which the user wants offered rarely.

## Consequences

- Easier: one word sweeps the backlog of decisions with no ADR, ten at a time, and never offers the same find
  twice.
- Harder: looseends carries the test's checked copy and a second markers file; a find's "covered" check depends on
  ADRs citing their records.
- Commits the project to: the decisions markers file and its test, the scope and the word in looseends, the
  ledger, a trigger case for "adrorphans" (and one that does not load it), the patch bump with
  `scripts/sync-manifests.py` and a CHANGELOG line, and this ADR's public copy. ADR-019's text is not changed; it
  gets a dated banner at rule 1 and a History line.

Steps, each with its test:
1. **The decisions markers file** in `skills/looseends/references/`, in the scan's format. Test: `looseends-scan.py
   --markers <it>` on this repository lists bbq answer lines, agreed rows and Defaulted rows with `file:line`; a
   red arm (a marker's pattern broken) shows its rows missing.
2. **looseends' scope and words**: the decisions scope in steps 1 and 2, the checked copy of the test, the
   strongest-first list, the ledger and the stamp rule; "adrorphans" and "looseends decisions" in its description.
   Test: `scripts/check-adr-sized.py` passes with looseends among the copies; read-through against rules 1 to 8.
3. **Trigger cases**: `looseends-yes` for "adrorphans", and a `looseends-no` near miss (for example, "what does
   orphaned mean in git?"). Test: `scripts/run-trigger-tests.py` on both.
4. **A first real run** on this repository, judged by the user. Test: the ledger exists with its stamp, and the
   list held about 10 finds, strongest first.
5. **The house steps**: patch bump, `scripts/sync-manifests.py`, CHANGELOG, `scripts/publish.py --dry-run`.

Confirmed by: the user's judgement of the first real run (step 4): the finds were real decisions, and none was
already covered by an ADR.

Revisit when: a first run shows mostly false hits, or ADRs stop citing their records, which the "covered" check
relies on.

## Asks left open

None.

## History

- 2026-11-10: proposed.
- 2026-11-10: ratified by the owner.
