---
status: accepted
status-note: — ratified by the owner 2026-10-22
owner: the owner
kind: process
built: partial
proof: "`skills/project-prep/rules/plain.md`"
owed: ADR-014's public copy still names defplz, and changes only on the user's approval (CHANGELOG keeps its history by design)
supersedes: ADR-013
amends: nothing
---
# ADR-018 — defplz is cut; its rules move to the opt-in rules catalogue

This is the published version of this decision. Some internal details have been left out.

## Decision

Supersedes ADR-013. pitmaster no longer ships **defplz** as a skill. What made it useful is three rules, and
three lines do that job better than a skill. Those rules, plus ADR-013's rule against running commands that
change anything, become the **Plain words** group of the opt-in rules catalogue: an agent explains a term
the way this project uses it first, in plain words, offers once to file it in the glossary and writes it only on
a yes, and never runs a command that changes anything while explaining. How rules reach a project is decided by
the rules ADR, ADR-022, which ships the group in project-prep's catalogue, `skills/project-prep/rules/plain.md`.

## The rules

1. **The skill goes**: `skills/defplz/` and its 11 eval cases are deleted; git keeps them.
2. **Its trigger words go**: `defplz` and `whatsthat` load nothing. Nothing replaces them.
3. **The siblings lose their pointer lines**: bbq, makeadr, talk-through and project-prep. project-prep still
   makes a glossary; its row says the agent files terms on a yes.
4. **Four rules carry on**, in the catalogue's Plain words group: the project's meaning first; plain words;
   offer once to file, write only on a yes; never run a command that changes anything while explaining a term.
   The length words (ADR-013 rule 2) end with the skill.
5. **The public copy is withdrawn**: ADR-013's `publish.txt` line is commented out, since it describes a
   skill the public never gets. This ADR gets no public copy until rules ship.

## Build steps

1. **The catalogue gains the command rule.** Test: the Plain words group has four rules, one from ADR-013 rule 5.
2. **The cut** (arc wave 2): delete the skill and its cases; remove the pointer lines (rule 3). Test: the spec check
   passes; `grep -rl defplz skills evals` finds nothing.
3. **The public copy is withdrawn** (rule 5). Test: `scripts/publish.py --dry-run` is clean and its output has no
   ADR-013.
4. **The front door** (arc wave 4): README.md, the starter guide, both manifests; the glossary's defplz line is
   marked as a former skill citing this ADR. Test: no file in the dry-run output names defplz.

**Confirmed by:** the steps' tests; whether the rules serve the user as well as the skill did is the user's
judgement once rules reach a project.
**Revisit when:** the rules ADR (G4) rules that rules cannot reach a project in a way that keeps the Plain words
group usable; then a smaller skill may be the better home.

## Alternatives

Each option is priced against the doctrine (function → ours → compatibility).

### Cut the skill; its rules join the opt-in catalogue (chosen: three lines do the job)
- Good: one fewer skill, trigger pair and set of pointer lines to learn and load
- Good: the habit still holds wherever a project switches on Plain words
- Bad: until the rules ADR lands, nothing loads the habit on its own
- Doctrine: function first; the catalogue is ours; plain lines in an agent-rules file are the common shape

### Keep defplz as written
- Good: nothing to change; the trigger words keep working
- Bad: the cost Codex named stays: 893 words and four pointer lines for three rules
- Doctrine: loses on function per word

### Keep it private, out of the public release
- Good: the user keeps the trigger word
- Bad: two versions of pitmaster to keep in step
- Doctrine: neutral on function; costs compatibility

## Consequences

- Good: the skill set shrinks to twelve; four siblings lose a pointer line each
- Bad: `defplz` and `whatsthat` stop working the day the cut lands
- Commits us to: the Plain words group in whatever the rules ADR rules; keeping the glossary A–Z by hand

## History

- 2026-10-22: proposed.
- 2026-10-22: ratified by the owner.
