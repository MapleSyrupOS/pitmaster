---
status: accepted
status-note: — ratified by the owner 2026-11-05
ratified-by: the owner
ratified-on: "2026-11-05"
owner: the owner
kind: process
built: partial
proof: "`scripts/check-all.py`, `scripts/check-pins.py`"
owed: the skill step in setfree and catchmeup (rule 1); the shed tag holding the tool, with the pin moved onto it; the public facts file and tool at the next release (rule 7)
supersedes: nothing
amends: nothing
---
# ADR-033 — stale-facts: a shed tool checks the facts living docs state against the repo, and check-all fails on a stale one

This is the published version of this decision. Some internal details have been left out.

## Decision

pitmaster-shed gains a tool, **`stale-facts`**, and check-all runs it. It reads a facts file that lists each fact a
project writes by hand in its docs (the skill count, the version, the repository path), how to work that fact out
from the repository itself, and the living docs that state it; it fails, naming the file and line, what the doc says
and what is true, wherever the two differ.

1. **A shed tool, then a skill step**. The tool lands first and check-all runs it. A skill step that runs the
   tool, explains what it found and, for a ruled ADR, offers the amendment through makeadr lands later in its own
   change, in setfree (release day) and catchmeup. A tool cannot write an amendment; the step is what does.
2. **A facts file says what a fact is**. A plain file in `docs/`: one fact a line, with its name, how to work it
   out (count the folders in `skills/`, read a key from `.claude-plugin/plugin.json`) and the pattern that states it
   in a doc. Numbers match as digits or as words. Nothing is guessed: a fact not in the file is not checked.
3. **Only listed living docs are read**. The facts file lists them: the README, `AGENTS.md`, the plugin and
   marketplace descriptions, `STATUS.md` without its *Landed* history, and each ADR's Access and Built lines. Dated
   records (bbq records, the log, field reports, the debt list's dated sections) describe the past and are never
   read.
4. **A stale fact fails check-all**.
5. **A ruled ADR is cleared by an amendment**. Ruled text is never edited, so an ADR line that states an old
   fact passes once a dated amendment section, newer than the ruled text, states the true value. The old line stays
   as history.
6. **`--fix` changes only the fact's own words**: "seventeen" becomes "eighteen" in the listed docs and nothing
   around it moves. It never touches an ADR; those it reports for an amendment.
7. **The public tree runs it too**. The facts file is published from the next release on, listing only the
   docs the public tree holds, and public CI runs the check on the public README.
8. **Pitmaster's copy lives in `scripts/`.** check-all is its first user, and no skill carries it yet, so the pinned
   copy (ADR-012 rule 2) sits at `scripts/stale-facts/` with its `.pin`, and `scripts/check-pins.py` checks pins
   under `scripts/` as well as `skills/`. The skill step (rule 1) carries its own copy when it lands.

Overtaken plans (a dated record still read as the plan after a later one replaced it) are out of this decision:
whether a plan is overtaken takes judgment, and they are filed as their own debt.

## Context

**Drivers:**
- It runs on every PR, with no agent and no points spent.
- It never edits ruled ADR text (CLAUDE.md, ADR-005).
- It never rewrites the user's sentences: only the fact's own words move.
- Another project can use it with nothing pitmaster-only in the code.

## Steps to build

1. **The tool** in `pitmaster-shed-backroom`: `stale-facts/` with the script (Python, standard library only), a
   README, fixtures and a self-test with a red arm (ADR-012 rules 4 and 8). Test: its self-test passes, and its red
   arm (a fixture README with a wrong count) fails naming the line.
2. **The pinned copy and check-pins.** `scripts/stale-facts/` and its `.pin`, the pin naming the shed PR's commit
   until the shed's next tag; `scripts/check-pins.py` reads pins under `scripts/` too. Test: `check-pins.py
   --self-test` gains a case for a pin under `scripts/`.
3. **The facts file and check-all.** The facts file, and a `stale-facts` line in `scripts/check-all.py`, not
   private-only. Test: `check-all` runs it and passes on main.
4. **Its first run is fixed in the same change.** Stale facts in non-ADR docs are fixed with `--fix`; each ruled ADR
   it flags gets an amendment through makeadr. Test: `check-all` green.
5. **Publishing it.** The facts file's line goes into `publish.txt` commented out; the next release uncomments it.
   Test: `publish.py --dry-run` clean.
6. **The skill step** (later, its own change): setfree and catchmeup run the tool and offer the amendments.

## Alternatives

### A shed tool in check-all, then a skill step (chosen: it runs on every PR and still gets amendments written)
- Good: CI catches a stale fact before it lands, with no agent.
- Good: the skill step covers what a tool cannot, the amendment.
- Bad: two changes, and a shed PR and pin before the first.

### A shed tool in check-all, with no skill step (not chosen)
- Good: one change.
- Bad: a stale ADR line fails and nothing offers the amendment; the debt line's "prompts an amendment" stays owed.

### A script in pitmaster's own `scripts/` (not chosen)
- Good: the fastest to build.
- Bad: no other project gets it, and ADR-012 rule 1 puts code usable without an agent in the shed.

### A skill only (not chosen)
- Good: an agent can notice facts no rule names.
- Bad: it spends points, and it never runs in CI.

### Built-in facts, or markers in the docs (not chosen)
- Good: built-in facts need no setup; markers are exact.
- Bad: built-in facts are pitmaster's alone; markers clutter the user's README with hidden tags.

### Warn only, or fail only on public docs (not chosen)
- Good: never blocks a PR.
- Bad: a warning is easy to ignore, and a stale private doc is still read as current by the next session.

### An ignore line per known-old ADR (not chosen)
- Good: quick.
- Bad: the ADR is never amended, so the stale line is still read as current.

### Report only, or `--fix` everywhere (not chosen)
- Good: report-only never edits; fix-everywhere does all the work.
- Bad: report-only leaves every count to be edited by hand; fixing ADR lines breaks the rule against editing ruled
  text.

### Private only (not chosen)
- Good: no facts file in the public tree.
- Bad: the doc outside readers see is the one left unchecked.

## Consequences

- Good: a PR that adds a skill and forgets the README's count fails until the count is right.
- Good: ADR-007's stale Access line, and any like it, gets its amendment.
- Bad: a new fact is only checked once someone adds it to the facts file.
- Bad: one more pin to move at each shed tag.
- Commits us to: a shed release that holds the tool and the pin moved onto its tag; the skill step in setfree and
  catchmeup; a debt line for overtaken plans.

**Revisit when:** the skill step lands, or a fact turns up that the facts file's ways of working one out cannot
express.

## History

- 2026-11-05: proposed.
- 2026-11-05: ratified by the owner.
