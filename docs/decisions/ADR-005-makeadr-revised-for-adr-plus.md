---
status: accepted
status-note: — ratified by the owner 2026-10-18
owner: the owner
kind: design
built: partial
proof: "`skills/makeadr/SKILL.md`, `skills/makeadr/scripts/adr-check.py`, `skills/makeadr/adr-plus.pin`, `scripts/check-pins.py`"
owed: other projects switching to the same shared copy
supersedes: nothing
amends: nothing (it changes the order in ADR-003's queued work; see Context)
---
# ADR-005 — makeadr revised: ADR+ first, bbq's rounds, four modes, one pinned schema

This is the public copy of a decision I made. I've left out a few internal notes.

## Decision

makeadr stays its own skill under the same name and is revised so that it writes the ADR+ format, can change an
ADR after it is ruled, and shares its question rules with bbq instead of repeating them.

## The rules

1. **ADR+ first.** makeadr offers ADR+ as the recommended format. It keeps MADR and Nygard for projects that must
   match an outside standard. The template once called `ours` is renamed ADR+.
2. **bbq's rounds.** The question rounds follow bbq's rules by reference, so they are written once. Both `bbq adr`
   and `makeadr` start the skill. makeadr keeps only what is about ADRs: sorting questions into taste, strategy
   and mechanism; pricing every option, with one line against the project's doctrine when it has one; the
   MADR-feature triggers of ADR-003; and writing the ADR.
3. **Four modes.** New; ratify (the old Status line moves into History word for word); amend (a dated, attributed
   section, ruled text untouched); supersede (a new ADR, where the old one changes only its status).
4. **A commit never counts as proof** that something is built. The lowercase status words and a required Kind
   field arrive with the YAML header (rule 5), so every header changes only once.
5. **The YAML header.** The schema, converter and lossless-conversion proof come into pitmaster. The schema's
   master copy is the adr-plus project's first release (v0.1.0). makeadr carries a copy, records the version it
   follows, and has a check that fails when the copy drifts. The converter is copied with project-specific paths
   and names moved into settings, keeping its self-test and red arm.
6. **Project settings.** New Config lines cover what a project changes: where question records go, which queue
   files to search, reserved numbers, checks to run after writing, its tier card and extra ADR sections. Rules
   that need prose go in a short add-on skill in that project.
7. **The house shape** of ADR-004, including the `Decided by pitmaster ADR-005.` line.

## Alternatives

- **Two skills, one door** (chosen). Outsiders find makeadr by name, and the round rules are written once. No ADR
  machinery loads on bbq runs that never touch an ADR. Cost: a reader opens bbq to see the round rules.
- **Merge makeadr into bbq as its ADR type** (not chosen). One skill, one rule set. But ratify, amend and
  supersede are not question sessions, and every bbq would carry the scripts and the converter.
- **Keep makeadr self-contained** (not chosen). Works where bbq is not installed, but the round rules would exist
  twice and drift apart.
- **Header rules now, YAML later** (overruled). Nothing is ported ahead of proof elsewhere, but pitmaster's own
  ADRs stay on bold-line headers for longer.
- **A smaller converter of pitmaster's own** (not chosen). Shaped to fit from the start, but more work and two
  converters to keep in step.

## Consequences

- makeadr writes the format the owner ratified and can ratify, amend and supersede in it.
- Every project that uses makeadr runs one schema, pinned to one adr-plus release.
- The YAML migration changes every ADR header, so line citations into old ADRs shift.
- Commits us to the pinned copy with its drift check, and to trigger evals for the modes and for `bbq adr`.

## History

- 2026-10-18: proposed.
- 2026-10-18: ratified by the owner.
- 2026-10-22: the YAML header and the pinned copy of the adr-plus schema built.
