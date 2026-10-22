---
name: project-prep
metadata:
  family: records
description: Set a project up with pitmaster's conventions for working with agents; it does not scaffold app code. Asks one round of questions, then writes the smallest set that works on a new branch, never overwriting a file - one set of agent rules (AGENTS.md, with a CLAUDE.md that points to it) and a STATUS.md whose every claim cites a file. The rest (log, debt and archive files, decisions folder, glossary, proposals folder, pitmaster.md config) is offered in the same question, or all of it at once. It ends by offering to put the project's first decision on record with makeadr, where the ADR+ format is offered first. Works on a new folder or an existing repository. Use when the user types "project-prep", "prepwork" or "setup-project", or says "prep this project", "set up this project for pitmaster", "init pitmaster", "prep a new project", "scaffold this project for agents", "set up this repo the pitmaster way" or "get this project ready for agents". Not for scaffolding an app, component or API.
---

# project-prep: set a project up with pitmaster's conventions for working with agents

Decided by pitmaster ADR-010.

Siblings: `makeadr` and `bbq` (offered at the end, step 8) and `talk-through` (suggests this skill when a talk was
about starting a project). Starter files are in `templates/`; the STATUS check is `scripts/status-check.py`.

## Config

Edit these lines here, or put the same lines in a `pitmaster.md` at your project root, which wins. Every line is
optional.

```
name: the user          # who the skill speaks to: read "the user" in the steps as this name
reference: none         # a repository whose folder layout to copy (a path or owner/name); none = the built-in one
pieces: rules, status   # the default pieces: all, or piece names from step 1 (core = rules, status, log, debt, archive, decisions)
branch: prep/<date>     # the branch it commits on
status_ceiling: 300     # the most lines STATUS.md may have; written into the new pitmaster.md
```

## Steps

1. **Ask one round first**, before writing anything. Four questions, the recommended answer first:
   - **The project**: its name (offer the folder's name) and one line on what it is.
   - **The owner**: who rules on taste, naming and decisions. Offer "the owner" as a neutral default.
   - **A doctrine** (optional): the project's rule for choosing between options, in a few words. "None yet" is a
     fine answer; the agent rules then say so instead of inventing one.
   - **Which pieces.** Put the table below in the question's own wording. Options: **the smallest set**, rules and
     status *(Recommended)*; **all of them**; or a typed list of piece names. Nothing else is assumed. A `pieces:`
     config line changes the recommended one.

   | piece | files | what it is for |
   |---|---|---|
   | rules *(default)* | `AGENTS.md`, `CLAUDE.md` | the rules every agent reads; `CLAUDE.md` is a one-line pointer to them |
   | status *(default)* | `STATUS.md` | where things stand now, every claim citing a file |
   | log | `docs/STATUS-log.md` | each session's work, dated, append-only |
   | debt | `docs/STATUS-debt.md` | known debt and owed work |
   | archive | `docs/STATUS-archive.md` | finished STATUS entries, moved word for word |
   | decisions | `docs/decisions/README.md` | decision records; no format chosen yet |
   | glossary | `docs/glossary.md` | terms the owner asks about, filed on a yes |
   | proposals | `docs/proposals/README.md`, `docs/proposals/INDEX.md` | explorations before a decision |
   | config | `pitmaster.md` | settings every pitmaster skill reads |
2. **Look at what is there.** List which of those files already exist. If the folder is not a git repository,
   offer to make it one; if the user declines, write the files and skip step 6. If `reference:` names a
   repository, copy its folder layout and file names from its file list; the text still comes from the templates
   and the answers.
3. **Write what is missing** for each chosen piece from its template in `templates/` (named after the file), with
   the answers and today's date. "Where
   things live" in the agent rules lists only the pieces that exist after this run. Every bullet under Now, Next
   and Known debt in a new `STATUS.md` cites a file that exists; the template's comments say what to change when a
   piece is left out.
4. **Never overwrite a file**; skip it. If `AGENTS.md` or `CLAUDE.md` already exists, write neither; show the
   sections it lacks as text the user can paste in, so the project keeps one set of agent rules.
5. **Run the STATUS check**: `scripts/status-check.py --root <project>`, for the line ceiling and the citations.
   Report what it finds, including in a `STATUS.md` that was already there; never rewrite an existing line to make
   it pass. Without Python, check by hand and say the script was not run.
6. **Commit on a new branch** (the config's `branch`) and offer a pull request. Commit to the main branch, or push,
   only when the user asks.
7. **Say what happened** in a short list: each file created, each file skipped and why, the pieces left out, and
   the check's result.
8. **"Let's put our first decision on record."** Setting a project up is itself a decision. Offer, in this order:
   - **Record it with `makeadr`** *(Recommended)*: the first ADR says how this project is set up and why. `makeadr`
     asks which format to use, ADR+ first, and writes it into `docs/decisions/README.md`, making the folder if
     needed.
   - **Plan the first piece of work with `bbq`.**
   - **Stop here.**

## Platform notes

- **Claude Code:** ask step 1 with the `AskUserQuestion` tool; the pieces question takes a typed list through
  "Other". `git` makes the branch and commit; `gh` opens the pull request when signed in. Step 8 loads `makeadr`
  or `bbq` with the Skill tool.
- **Cowork / claude.ai:** ask with `AskUserQuestion` where it is offered. Write into the connected folder; with no
  folder, show each file for the user to save. There is usually no git, so step 6 is skipped and the summary says
  so.
- **Codex:** ask step 1 as a numbered list in one message and wait for the answers. Codex reads `AGENTS.md` on its
  own, so the `CLAUDE.md` pointer is for the user's other tools. `git` and `gh` work where installed.
- **Other tools:** ask step 1 as for Codex, with the options lettered. Write with the tool's file
  access; use `git` if present, and skip step 6 if not.
