---
status: accepted
status-note: — ratified by the owner 2026-10-20
owner: the owner
kind: process
built: landed
proof: "`skills/project-prep/SKILL.md`, `skills/project-prep/templates/AGENTS.md.tmpl`, `skills/project-prep/scripts/status-check.py`"
supersedes: nothing
amends: nothing
---
# ADR-010 — project-prep: get a project ready for agents, never overwriting a file

This is the public copy of a decision I made. I've left out a few internal notes.

## Decision

pitmaster gains a skill, **project-prep**, that gets a new or existing project ready for agents. It asks one round
of questions, then writes whatever is missing from a built-in set of starter files: one set of agent rules in
`AGENTS.md` with a `CLAUDE.md` that points to it, a `STATUS.md` whose claims cite files with its log, debt and
archive files, a glossary, a proposals folder, a decisions folder and a `pitmaster.md` config. It never overwrites
a file. It commits on a new branch and offers a pull request. It does not choose the decision format: it ends by
offering `makeadr`, which asks for the format with ADR+ first. It replaces an earlier `setup-project` skill, and
that name also loads it.

## The rules

1. **Questions first.** One round of four: the project, the owner, an optional doctrine, and which pieces.
2. **Built-in templates**, in `skills/project-prep/templates/`, named `.tmpl` so no tool loads them as live agent
   rules. An optional `reference:` config line copies another repository's folder layout; the text still comes
   from the templates and the answers.
3. **One set of agent rules.** `AGENTS.md` holds them; `CLAUDE.md` is one line pointing to it. If either exists,
   neither is written, and the missing sections are shown as text to paste.
4. **Never overwrite.** An existing file is skipped and named in the summary.
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
