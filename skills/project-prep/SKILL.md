---
name: project-prep
metadata:
  family: records
description: Set a project up with pitmaster's conventions for working with agents; it does not scaffold app code. Asks one round of questions, then writes the smallest set that works on a new branch, never overwriting a file: agent rules (AGENTS.md, with a CLAUDE.md pointing to it) and a STATUS.md whose every claim cites a file. The rest (log, debt, archive, decisions, glossary, proposals, pitmaster.md config) is offered in the same round, as are the opt-in rule groups, which it also switches on and off later. It ends by offering makeadr for the project's first decision. Use when the user types "project-prep", "prepwork" (either with "really" run on also merges its branch) or "setup-project", or says "prep this project", "set up this project for pitmaster", "init pitmaster", "scaffold this project for agents", "set up this repo the pitmaster way", "get this project ready for agents", "switch on the plain rules", "turn off a rule group" or "which rules are on?". Not for scaffolding an app, component or API.
---

# project-prep: set a project up with pitmaster's conventions for working with agents

Decided by pitmaster ADR-010.
"project-prepreally": ADR-023.

Siblings: `makeadr` and `bbq` (offered at the end, step 8) and `talk-through` (suggests this skill when a talk was
about starting a project). Starter files are in `templates/`; the STATUS check is `scripts/status-check.py`. The
opt-in rules catalogue is in `rules/`, one file per group, decided by pitmaster ADR-022.

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

1. **Ask one round first**, before writing anything. Five questions, the recommended answer first:
   - **The project**: its name (offer the folder's name) and one line on what it is.
   - **The owner**: who rules on taste, naming and decisions. Offer "the owner" as a neutral default.
   - **A doctrine** (optional): the project's rule for choosing between options, in a few words. "None yet" is a
     fine answer; the agent rules then say so instead of inventing one.
   - **Which pieces.** Put the table below in the question's own wording. Options: **the smallest set**, rules and
     status *(Recommended)*; **all of them**; or a typed list of piece names. Nothing else is assumed. A `pieces:`
     config line changes the recommended one.

   | piece | files | what it is for |
   |---|---|---|
   | rules *(default)* | `AGENTS.md`, `CLAUDE.md` | the rules every agent reads; `CLAUDE.md` is one line, `@AGENTS.md`, which loads them into Claude Code |
   | status *(default)* | `STATUS.md` | where things stand now, every claim citing a file |
   | log | `docs/STATUS-log.md` | each session's work, dated, append-only |
   | debt | `docs/STATUS-debt.md` | known debt and owed work |
   | archive | `docs/STATUS-archive.md` | finished STATUS entries, moved word for word |
   | decisions | `docs/decisions/README.md` | decision records; no format chosen yet |
   | glossary | `docs/glossary.md` | terms the owner asks about, filed on a yes |
   | proposals | `docs/proposals/README.md`, `docs/proposals/INDEX.md` | explorations before a decision |
   | config | `pitmaster.md` | settings every pitmaster skill reads |
   | public drafts | `public_adr: on` in `pitmaster.md` | for a project that will publish some decisions: `makeadr` drafts a public copy of each, held in `docs/decisions/public/pending/` until the user approves it at a release review; never published by itself (takes decisions and config) |
   - **Which rule groups**: a checklist (several may be picked) of the six groups in `rules/README.md`, with
     `plan`, `check` and `plain` ticked. A rule is one line every agent follows every session, so each line costs
     a little context; nothing is on unless the user keeps it ticked. Put each group's heading, size and one line
     on what its rules ask in the question's own wording, from its file in `rules/`, and name any list it writes. The answer is used only where
     `AGENTS.md` is written or already exists.
2. **Look at what is there.** List which of those files already exist. If the folder is not a git repository,
   offer to make it one; if the user declines, write the files and skip step 6. If `reference:` names a
   repository, copy its folder layout and file names from its file list; the text still comes from the templates
   and the answers.
3. **Write what is missing** for each chosen piece from its template in `templates/` (named after the file), with
   the answers and today's date. *public drafts* writes `public_adr: on` into the new `pitmaster.md` (into an
   existing one only as text to paste, step 4); `makeadr` makes the `pending/` folder on its first draft. "Where
   things live" in the agent rules lists only the pieces that exist after this setup. Every bullet under Now, Next
   and Known debt in a new `STATUS.md` cites a file that exists; the template's comments say what to change when a
   piece is left out. The chosen rule groups fill the template's `{{rules}}` slot as the Rules section (below); with
   none chosen, the slot and its comments go. A chosen group's lists are written too (below, "Lists").
4. **Never overwrite a file**; skip it. If `AGENTS.md` or `CLAUDE.md` already exists, write neither; show the
   sections it lacks as text the user can paste in, so the project keeps one set of agent rules. The one exception
   is the Rules section: project-prep may add it to an existing `AGENTS.md`, or change it there, as "Switching
   rule groups" says (ADR-022).
5. **Run the STATUS check**: `scripts/status-check.py --root <project>`, for the line ceiling and the citations.
   Report what it finds, including in a `STATUS.md` that was already there; never rewrite an existing line to make
   it pass. Without Python, check by hand and say the script was not run.
6. **Commit on a new branch** (the config's `branch`) and offer a pull request. Commit to the main branch, or push,
   only when the user asks. After "project-prepreally" (or "prepworkreally"), push the branch, open the pull
   request and merge it once its checks are green (ADR-023 rule 11); never past a safety stop.
7. **Say what happened** in a short list: each file created, each file skipped and why, the pieces left out, the
   rule groups switched on, and the check's result.
8. **"Let's put our first decision on record."** Setting a project up is itself a decision. Offer, in this order:
   - **Record it with `makeadr`** *(Recommended)*: the first ADR says how this project is set up and why. `makeadr`
     asks which format to use, ADR+ first, and writes it into `docs/decisions/README.md`, making the folder if
     needed.
   - **Plan the first piece of work with `bbq`.**
   - **Stop here.**

## The Rules section

The chosen groups' rules, copied word for word from their files in `rules/` (only the lines starting `- `), in the
catalogue's order (`plan`, `run`, `check`, `records`, `plain`, `craft`), each group under its heading. The opening
marker line is the only record of which groups are on and which catalogue date they were copied from.

```
<!-- pitmaster rules: plain, plan · catalogue 2026-10-23 · project-prep rewrites everything down to the end line -->
## Rules

### Plan and decide
- Say how big a job is before starting it; if it is weeks of sessions, say so.
- …

### Plain words
- …
<!-- pitmaster rules: end -->
```

**Lists.** A rule that names a file in `docs/rules/` keeps a list the project holds (`rules/README.md`, "Lists").
When its group is switched on, at setup or later, write that list from its starter in `templates/`, named after the
file (`docs/rules/task-homes.md` from `task-homes.md.tmpl`), with the project's name. Show it with the Rules change;
the same yes writes both. Write a list only where none exists: never overwrite one, and leave it in place when the
group is switched off. It is the project's own record.

## Switching rule groups

When the user asks to switch a rule group on or off, which rules are on, or to update the rules (ADR-022):

1. **Read the Rules section** of the project's `AGENTS.md`: the groups its opening line names, and its catalogue
   date. No section means none are on.
2. **"Which rules are on?"** is answered from that line, with the six groups and their sizes from
   `rules/README.md`. Stop there.
3. **Ask which groups**, unless the user's words already say: the same checklist as step 1, with the groups now on
   ticked.
4. **Offer any update.** If the Catalogue date in `rules/README.md` is newer than the section's, compare the
   section's lines with the group files and list each rule added, reworded or dropped in the groups that stay on,
   and any list an added rule keeps; ask whether to take them. A project's rules never change without the user's
   yes.
5. **Write only the section, and any missing list.** Rebuild the section as above and show the change, with any
   list a group switched on keeps ("Lists" above); write them on a yes. Touch nothing in `AGENTS.md` outside the
   two marker lines. An `AGENTS.md` with no section gets one at its end, shown and written the same way;
   switching every group off removes the section, marker lines included. With no `AGENTS.md`, offer this skill's
   rules piece instead.
6. **Commit** on a new branch, as step 6, and say which groups are now on and any list written.

## Platform notes

- **Claude Code:** ask step 1 with the `AskUserQuestion` tool; the pieces question takes a typed list through
  "Other". The tool takes four questions at a time, so the rule groups go in a second call straight after, with
  `multiSelect` on; skip it when the pieces answer leaves out rules and there is no `AGENTS.md`. Six groups are
  more than the tool's four options: offer the three pre-ticked groups as one option (recommended), each of the
  other three as its own, and take any other mix through "Other". Switching later asks the same way, with the
  groups now on as the first option. `git` makes the branch and commit; `gh` opens the pull request when signed
  in. Step 8 loads `makeadr` or `bbq` with the Skill tool.
- **Cowork / claude.ai:** ask with `AskUserQuestion` where it is offered. Write into the connected folder; with no
  folder, show each file for the user to save. There is usually no git, so step 6 is skipped and the summary says
  so.
- **Codex:** ask step 1 as a numbered list in one message and wait for the answers. Codex reads `AGENTS.md` on its
  own; the `CLAUDE.md` import is for Claude Code. `git` and `gh` work where installed.
- **Other tools:** ask step 1 as for Codex, with the options lettered. Write with the tool's file
  access; use `git` if present, and skip step 6 if not.
