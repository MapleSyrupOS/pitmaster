---
status: accepted
status-note: — ratified by the owner 2026-10-20
owner: the owner
kind: process
built: landed
proof: "`skills/project-prep/SKILL.md`, `skills/project-prep/templates/AGENTS.md.tmpl`, `skills/project-prep/scripts/status-check.py`, `evals/project-prep-yes-01/prompt.md`"
supersedes: nothing
amends: nothing
---
# ADR-010 — project-prep: get a project ready for agents, never overwriting a file

This is the published version of this decision. Some internal details have been left out.

## Decision

pitmaster gains a skill, **project-prep**, that gets a new or existing project ready for agents. It asks one round
of questions, then writes whatever is missing from a built-in set of starter files: one set of agent rules in
`AGENTS.md` with a `CLAUDE.md` that points to it, a `STATUS.md` whose claims cite files with its log, debt and
archive files, a glossary, a proposals folder, a decisions folder and a `pitmaster.md` config. It never overwrites
a file. It commits on a new branch and offers a pull request. It does not choose the decision format: it ends by
offering `makeadr`, which asks for the format with ADR+ first. It replaces an earlier `setup-project` skill, and
that name also loads it.

## The rules

> **Amended 2026-10-23 by ADR-023, ratified by the user:** project-prepreally (and prepworkreally) merges its
> set-up branch once its checks pass (rule 5).

1. **Questions first.** One round of four: the project, who owns it, an optional doctrine, and which pieces.
> **Amended 2026-10-23 by ADR-022 (its rule 5):** the round gains a fifth question, a checklist of the opt-in rule
> groups.
2. **Built-in templates**, in `skills/project-prep/templates/`, named `.tmpl` so no tool loads them as live agent
   rules. An optional `reference:` config line copies another repository's folder layout; the text still comes
   from the templates and the answers.
3. **One set of agent rules.** `AGENTS.md` holds them; `CLAUDE.md` is one line pointing to it. If either exists,
   neither is written, and the missing sections are shown as text to paste.
4. **Never overwrite.** An existing file is skipped and named in the summary.
> **Amended 2026-10-23 by ADR-022:** project-prep may add or change its own Rules section in an existing `AGENTS.md`,
> between its two marker lines, shown first and written on the user's yes; nothing else in the file is touched.
5. **Git.** Offer `git init` where there is none; commit on a new branch and offer a pull request; commit to
   main or push only when asked.
6. **No decision format chosen.** The decisions folder gets a README only; `makeadr` asks the format later.
7. **The ending.** Offer `makeadr` to record how the project was set up, then `bbq` for the first piece of work.
8. **The STATUS shape and its check.** Now, Next, Known debt, Log and how the file is kept, with an archive file
   beside the log and debt files. Every bullet under Now, Next and Known debt cites a file that exists;
   `skills/project-prep/scripts/status-check.py` checks that and a line ceiling (default 300), and reports an
   existing STATUS's findings without rewriting it.
9. **Still owed:** a checker that lists which pieces a repository lacks.

## Alternatives

- **Built-in templates with an optional reference** (chosen). Works anywhere, reference or not. Cost: the
  templates must be kept in step with the house layout.
- **Always copy from a reference repository** (not chosen). Exact match, but useless without a reference and it
  risks carrying names across.
- **project-prep asks the decision format itself** (not chosen). Two skills would ask one question; `makeadr`
  already owns it.
- **Keep `setup-project` as its own skill** (not chosen). Two skills for one job, with no `AGENTS.md` and no
  hand-off to `makeadr`.
- **CLAUDE.md only** (not chosen). Codex and other agents read `AGENTS.md`, so the rules would split.

## Consequences

- A new collaborator gets the same layout and ground rules in one run, with nothing overwritten; the first
  decision recorded is how the project was set up.
- The templates are a second copy of the house conventions and can drift from them.
- Commits us to the missing-pieces checker, and to updating the templates when the house layout changes.

## History

- 2026-10-20: proposed.
- 2026-10-20: ratified by the owner.
- 2026-10-20: amended.
- 2026-10-22: amended.
- 2026-10-23: amended.
- 2026-10-23: ratified by the owner.

## Amendment — 2026-10-22, the user

**What changed.** Rule 1's "which pieces" now defaults to the smallest set that works: the agent rules (`AGENTS.md`
with its `CLAUDE.md` pointer) and `STATUS.md`. The other pieces (the log, debt and archive files, the decisions
folder, the glossary, the proposals folder and the `pitmaster.md` config) are offered in the same question, one line
each, and "all of them" is one answer. If the decisions folder is left out, makeadr makes it when the project's
first ADR is written. The bare word "scaffold" no longer loads the skill, which says it sets a project up for
working with agents and is not for scaffolding an app, component or API.

**Why.** An outside review found the default file set heavy for an occasional user and "scaffold" too broad a
trigger; the user accepted both.

**Touches.** §The rules, rule 1, and the skill's triggers. The ruled text stands; this section governs where they
differ.
