---
status: accepted
status-note: — ratified by the owner 2026-10-24
ratified-by: the owner
ratified-on: "2026-10-24"
owner: the owner
kind: process
built: landed
proof: "`skills/bbq/references/tool-type.md`, `skills/bbq/references/the-types.md`, `skills/bbq/references/skill-type.md`, `skills/bbq/SKILL.md`, `evals/bbq-yes-22/prompt.md`, `evals/bbq-yes-23/prompt.md`, `evals/bbq-no-13/prompt.md`"
supersedes: nothing
amends: "ADR-004 §Amendment — 2026-10-22, the owner: the Skill type"
---
# ADR-026 — bbq gains a Tool type, and both the Skill and Tool types offer the build after ratify

This is the published version of this decision. Some internal details have been left out.

## Decision

bbq gains a **Tool** type, the tool version of the Skill type, for a tool a person can run without an agent. It is
started by "tool bbq" ("shedtool bbq" also names it) or by the opener **maketool**, the way "makeskill" opens the
Skill type. A tool bbq covers ten things, writes its record, then offers makeadr for the tool's ADR; after
that ADR is ratified it **offers** the build: the code in the project's tools home with its self-test, then the pins
in each skill that uses it, in one PR here. The Skill type changes to match: after its ADR is ratified it
offers the move into the shipped skills folder instead of making it, which amends ADR-004's Skill type section.

## The rules

1. **Starting it**: "tool bbq", "shedtool bbq", or "maketool", which opens bbq straight in the Tool type.
   bbq's description gains "maketool"; to make room, its "(a voyage led from a cloud container)" bracket goes.
2. **The line first** (ADR-012 rule 1): a script useful only inside a skill's steps is a skill script, and the
   bbq offers the Skill type instead.
3. **The ten things**: what it is for, in one sentence; how a person runs it with no agent (the command, its
   options, its defaults); what it reads and what it writes; its output and exit codes; what it must never do; who
   uses it and how it reaches them (which skills pin it, how a skill hands off to it, how a person installs it, how a
   fix reaches every copy: the version, the tag, the re-pin); platforms, and standard-library Python or why not;
   network and secrets (what it reaches, where keys come from); its self-test and the deliberate break that proves
   it; its name and where it lives.
4. **The tools home**: bbq's config gains `tools_home: ask`. The type asks once where tools live (a folder such
   as `tools/`, or another repository) and suggests saving the answer in `pitmaster.md`; pitmaster's is
   `MapleSyrupOS/pitmaster-shed`. Pins are part of the build only where the project pins.
5. **What it writes and when**: the record; then makeadr for the tool's ADR; after ratification, an offer to
   build: the code and its self-test in the tools home, then, once that is checked, the pins in each skill that uses
   it, in one PR here. No draft folder here.
6. **The Skill type, in step**: a Skill bbq still writes its draft and trigger cases during the bbq; after its ADR
   is ratified, the move into the shipped skills folder, the patch bump and the CHANGELOG line are offered, not made.
   A draft can change at any time before the move; a change that contradicts a ratified ADR goes through makeadr.
   "goforit" already says yes to these offers.
7. **Like every type**: it runs as a Batch or a stew with no extra rule.

## Alternatives

Each option is priced against the doctrine (function → ours → compatibility).

### A built-in Tool type, ruled before its first use (chosen: every tool bbq covers the same ground, ruled before its first use)
- Good: every tool bbq covers the same ground, in any project that uses bbq
- Good: the Skill and Tool types share one life cycle
- Bad: one more reference file, and description room for "maketool"
- Doctrine: function first; the name, the checklist and the opener are ours

### Fold it into the townhall live bbq, two ADRs after (not chosen: the first recommendation)
- Good: the type proven on a real run before it is ruled
- Bad: the first tool bbq runs on an unruled checklist

### A project-local type in `docs/bbq-types.md` (not chosen)
- Good: no ADR, no change to the shipped bbq
- Bad: nobody else who uses bbq gets it

### "Shed tool" as the name, with no opener (not chosen)
- Good: the user's own word
- Bad: other projects' tools may not live in a "shed". The user's rule was this as the default unless "makeskill"
  was ours; it was

### Eleven items, with updates on their own (not chosen)
- Good: updates stand out
- Bad: the user preferred ten, with the update path folded into who the tool reaches

### A draft tool folder here first (not chosen)
- Good: matches the Skill type's draft
- Bad: ADR-012 turned down "written here, published out" as a standing way

### Offer the Skill draft too, not only the move (not chosen)
- Good: nothing is written until asked
- Bad: the draft is the cheap, changeable part, and the bbq's answers are freshest while it is written

### Pins as a separate later step (not chosen)
- Good: smaller PRs
- Bad: a tool built for a skill sits unused until someone remembers the pin

## Consequences

- Good: the next tool (townhall live first) gets a bbq that asks how it reaches its copies before it is built
- Good: neither type builds or ships anything after ratify without the user's word, or a "goforit"
- Bad: bbq's description loses the Cloud bracket, and a Skill or Tool bbq takes one more step after ratify
- Commits us to: the build in one PR on ratification; a public copy of this ADR; townhall live as the first use

## History

- 2026-10-24: proposed.
- 2026-10-24: ratified by the owner.
