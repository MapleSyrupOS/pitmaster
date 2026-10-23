---
status: accepted
status-note: — ratified by the owner 2026-10-18
owner: the owner
kind: process
built: landed
proof: "`templates/skill/SKILL.md`, `scripts/build-variants.py`"
supersedes: nothing
amends: nothing
---
# ADR-004 — How a pitmaster skill is made: an ADR first, then one house shape

This is the public copy of a decision I made. I've left out a few internal notes.

## Decision

Every new pitmaster skill is decided by an ADR before it is built, and every skill is built in one house shape. A
skill can be drafted in a drafts folder without an ADR. It needs one before it moves into `skills/`. The five
skills that shipped before this ADR get theirs the next time each is substantially revised, starting with
makeadr (ADR-005). The house shape is written out as a fill-in template, `templates/skill/SKILL.md`. bbq's Skill
type holds a new skill's whole life cycle: the draft, its ADR through `makeadr`, the owner's ratification, then the
move into `skills/` with the sibling pointer lines, the plugin's patch bump and a CHANGELOG line (amended
2026-10-22). It copies the template, and the skill check fails a shipped skill that is missing a part the check can
see. bbq's description carries the trigger word **makeskill**, which opens bbq in the Skill type; there is no
separate skill for it (amended 2026-10-22). goforit's skill file does not carry these steps: it carries any plan
into the build and stops at "ratify" and at merge (ADR-017).

## Context

The owner asked to revise makeadr so that skills would all follow the same format for being made. That meant two
things: one written shape for a skill, and a decision recorded before each one is built.

The five shipped skills already share most of a shape, though nothing wrote it down: frontmatter with only a
name and a description, a title that names the skill and its job, an optional Config block that `pitmaster.md`
can override, numbered steps in plain words, and a tagged Platform notes section at the end. ADR-001 already rules
on the last part, and `scripts/build-variants.py --check` enforces it.

Drivers:
- New skills should come out the same way every time, whoever drafts them.
- An outside reader should be able to trace any skill to the decision behind it.
- No backfill work for skills that already work.
- Reading comes first: a skill and its ADR must read as plain sentences to a non-programmer.

## The house shape

1. Frontmatter holds `name` and `description` (ADR-001), and one more field, a `metadata:` map with one key,
   `family:` (amended 2026-10-22; see *Families* below). The description says what the skill does and when to use
   it, with the phrases that should load it.
2. The title is `# <name>: <what it does>`.
3. Directly below it comes one line, `Decided by pitmaster ADR-NNN.`, in plain text so it still reads in an
   installed copy.
4. A sibling line, when the skill calls or defers to other skills. When a new skill's ADR names a sibling skill,
   the build adds the matching pointer to that sibling in the same PR: the sibling's *Sibling of* line names the
   new skill, and where the two hand something over, one clause in the step where it happens (amended 2026-10-20).
5. A `## Config` block, when the skill has settings. Every line is optional, and a `pitmaster.md` at the project
   root wins.
6. Numbered steps in plain words, with no tool names that only one platform has (ADR-001).
7. `## Platform notes` comes last, with the four tagged bullets (ADR-001).

The check enforces 1, 2, 3, 6 and 7. Parts 4 and 5 depend on the skill, so a reviewer checks those.

### The sibling pointer (amended 2026-10-20)

The pointer in part 4 is a default of the build, not a question for the owner: the new skill's ADR has already
ruled the relationship, and the pointer only says it exists. It applies to the grandfathered skills too. A pointer
line is not a substantial revision, so it does not bring forward their own ADR. This was ruled when spend-ledger
(ADR-009) named `budget-select` as its sibling and the pointer back was first parked as a question. The sibling
line's note is in `templates/skill/SKILL.md`, and the step is in bbq's Skill type.

### Families (amended 2026-10-22)

Besides `name` and `description`, a skill's frontmatter holds a `metadata:` map with one key, `family:`, set to one
of six families: `plan`, `run`, `usage`, `check`, `records`, `craft`. `metadata` is the Agent Skills
specification's own field for extra properties (agentskills.io/specification), so this is not Claude-only
frontmatter and ADR-001 still holds. "Family" is Apache Magpie's word for the same label; Magpie puts it at the top
level, outside the specification, so pitmaster keeps the word and the specification's place for it. The owner chose
`metadata:` over the top level, and six families over four, after seeing every skill placed in one.

The families:
- plan: bbq, makeadr, talk-through
- run: goforit, dealers-choice, carte-blanche, tier-select
- usage: budget-select, spend-ledger, swarm-bottleneck
- check: tastetest
- records: project-prep
- craft: none yet

A new skill's ADR names its family. Adding a family is an amendment here. The spec check in
`scripts/build-variants.py` allows `metadata.family` from the list and fails any other key; the template gains the
field, and bbq's Skill type writes it.

### The Skill type (amended 2026-10-22)

The Skill type behaved like a skill of its own, and goforit carried its steps, so goforit was not general. Moving
the whole life cycle into bbq's Skill type fixes that. The owner chose a trigger word over a separate skill because
bbq's description had room, and a new skill would add one more always-loaded description.

## Alternatives

### ADR, template and check (chosen: the shape holds without anyone remembering it)
- Good: a missing part fails the check, as ADR-001's rules already do
- Good: bbq's Skill type starts every new skill from the same file
- Bad: one more template to keep in step with the shipped skills

### ADR and template, no check
- Good: less to build
- Bad: drift is caught only when someone notices

### ADR only
- Good: lightest
- Bad: every drafter rebuilds the shape from prose

### Backfill an ADR for all five shipped skills now
- Good: a complete trail at once
- Bad: five ADRs that only describe what already works; each skill gets one anyway at its next revision

## Consequences

- Good: every skill made from now on can be traced to the decision behind it.
- Good: a drafter (person, agent or local model) starts from one file and one check.
- Bad: shipping a draft now takes an ADR first, which is slower for a small skill.
- Bad: until the five shipped skills are revised, the check carries a list of skills it exempts.
- Commits us to: removing each skill from that list once it gets its ADR, and keeping the template in step
  when the shape changes (that change is itself an amendment to this ADR).

## History

- 2026-10-18: proposed.
- 2026-10-18: ratified by the owner.
- 2026-10-20: amended by the owner.
- 2026-10-22: amended by the owner.
- 2026-10-22: amended by the owner.
