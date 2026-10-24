# The Skill type

The Skill type grills the user about a skill they want, writes its folder as a draft, and carries it through to
the shipped skills folder (ADR-004, amendment of 2026-10-22).

## What the questions must cover

Ten things, within the bbq's count:

- what the skill is for, in one sentence;
- the phrases a user types that should load it, and near-misses that should not;
- what it reads first;
- its steps;
- what it must never do;
- the skills it calls or defers to;
- what it needs that only some platforms have (subagents, worktrees, a context meter, `gh`), and what it does
  without them;
- where the folder goes: a project's skills folder, the user's own, or a plugin's `skills/` (SKILL.md's *Platform
  notes* have the paths);
- whether it ships scripts;
- its family, where the project uses them: `plan`, `run`, `usage`, `check`, `records` or `craft`. A new skill's ADR
  names it.

## What it writes

1. **The draft.** Where the project has a skill template (`templates/skill/SKILL.md`, as pitmaster does under
   ADR-004), start from it and write the new folder into the project's `drafts/` folder. Otherwise write
   `<folder>/<name>/SKILL.md`.
   - The frontmatter holds `name`, `description` and, where the project uses families, a `metadata:` map with one
     key, `family:` (ADR-004, amendment of 2026-10-22). Nothing else.
   - The description says what the skill does and when to use it, with its trigger phrases, in under 1,024
     characters. The name is lowercase letters, digits and hyphens, and matches the folder.
   - The steps are plain words. Anything only one platform has goes in a closing *Platform notes* section, one
     tagged bullet per platform. Any scripts the answers asked for are named by their path inside the folder.
2. **The trigger prompts:** five to ten that should load the skill and three to five that should not. In a plugin
   with an `evals/` folder they go there as eval cases; otherwise they go in the record.
3. **The record keeps the questions and answers**, so each of the skill's rules traces to the question that set
   it. A contributor opens one PR with the skill and its record together.

## The life cycle

A draft needs no ADR. The move into the shipped skills folder needs one, ratified.

1. **The draft**, with its scripts and self-tests, its eval cases and the project's checks.
2. **The pointer lines.** Each sibling the new skill names gets it in its own *Sibling of* line, plus one clause
   where they hand something over, in the same PR. A default, never a question (ADR-004, amendment of 2026-10-20).
3. **The ADR.** Offer `makeadr`. What the bbq already settled with citations, it writes from the record; it asks
   only what is still open.
4. **The owner's ratification.** Only the owner's own "ratify" counts; an agent never ratifies. Stop and ask for it.
5. **The move, offered.** After the ratification, `makeadr` records it and the move is offered, not made
   (ADR-026); the draft can still change until then. On a yes, or "goforit", the folder moves from `drafts/` into
   the shipped skills folder, the plugin's patch version goes up by one (running its manifest-sync script, if the
   project has one), a CHANGELOG line is added, the project's checks run and the PR is updated. Then stop:
   merging is the owner's.
