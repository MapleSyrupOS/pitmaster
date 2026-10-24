---
status: accepted
status-note: — ratified by the owner 2026-10-23
ratified-by: the owner
ratified-on: "2026-10-23"
owner: the owner
kind: process
built: landed
proof: "`skills/project-prep/rules/README.md`, `skills/project-prep/SKILL.md`, `scripts/check-rules.py`, `evals/project-prep-yes-08/prompt.md`, `skills/project-prep/templates/task-homes.md.tmpl`, `skills/project-prep/templates/hot-files.md.tmpl`, `skills/project-prep/templates/tool-traps.md.tmpl`"
supersedes: nothing
amends: ADR-010 §The rules, rule 4 (never overwrite)
---
# ADR-022 — Opt-in rules ship in project-prep and reach a project through its AGENTS.md

This is the published version of this decision. Some internal details have been left out.

## Decision

pitmaster's rules (one-line standing instructions, no trigger, no steps) ship as a **catalogue of six groups**
inside project-prep's folder, `skills/project-prep/rules/`, one file per group. A project chooses whole groups,
and project-prep copies the chosen groups' lines **word for word into a marked Rules section of the project's
`AGENTS.md`**, the one file every agent reads. Setup asks with a checklist that comes with Plain words, Plan and
decide, and Check and review pre-ticked; nothing is on unless accepted. project-prep also switches groups on
and off later, touching nothing in `AGENTS.md` outside its own section (amending ADR-010 rule 4). A project's
copy changes only on the user's yes. All groups together stay within 35 lines, no rule over 30 words, and a
check enforces it.

## Context

Drivers:
- A rule is only always on if every tool reads it every session (ADR-001: any tool that reads `SKILL.md`).
- Every switched-on line costs context in every session, so the catalogue must stay small and nothing new should
  load for users who never switch a group on.
- The user rules what is in a project's rules; nothing may change under them.
- No bulk nobody asked for (the user's words: "won't add bulk").


## The rules

1. **What reaches a project**: the chosen groups' lines, in a marked Rules section of the project's
   `AGENTS.md`. Codex reads that file on its own; Claude Code reads it through the `CLAUDE.md` pointer. A plugin hook
   that adds the lines at session start stays open as a later option, as an extra, never instead of the section.
2. **Where the catalogue ships**: `skills/project-prep/rules/`, one file per group, and a `README.md` listing
   the groups, their sizes, the catalogue date and the held-back rules. The rules keep their own folder and this
   ADR; project-prep carries them and applies them.
3. **Six groups**. Each has a one-word name, typed and recorded, and a heading agents read: `plan` Plan
   and decide, `run` Run and delegate, `check` Check and review, `records` Records and repository, `plain` Plain
   words, `craft` Engineering craft.
4. **Twenty-seven rules**: the drafted catalogue with four changes. Three lenses (ways of weighing options) join
   `plan`; the three rules that need a list file the project keeps (task homes, hot files, tool traps) are held back
   until each ships with a starter list; "send what you made as a file or a link" is dropped; the datasheet rule
   moves to `craft`. Each rule is one line. A rule a hook could enforce stays a line.
5. **Setup**: project-prep's round gains a fifth question, a checklist of the six groups with `plain`,
   `plan` and `check` pre-ticked (12 lines). Every group stays opt-in.
6. **Switching later**: project-prep switches groups on and off and says which are on. The agent copies a
   group file's lines word for word; there is no script. If copies are found to drift, a script is the fix.
7. **The record of what is on** (as built): the section's opening marker line names the groups that are on and
   the catalogue date it was copied from. No other file records them.
8. **Updates**: a project's copy never changes by itself. When the catalogue's date is newer than the
   section's, project-prep shows the difference and writes it only on the user's yes.
9. **Editing an existing AGENTS.md** (amends ADR-010 rule 4): project-prep may change an existing
   `AGENTS.md` only between its own two marker lines, showing the change first and writing it on a yes. Where the
   file has no Rules section yet, it adds one at the end the same way. Nothing else in the file is touched.
10. **The cap**: all groups together at most 35 lines, no rule over 30 words. `scripts/check-rules.py` fails
    past either, and when a rule repeats one of the `AGENTS.md` template's ground rules.
11. **The template's ground rules** stay in the template, written for every project. They are not a group,
    and no rule repeats one: the rule on the user's calls keeps only its new half, "For a delegated landing, show
    every precondition met."

## Build steps

1. **The catalogue**: six group files and a `README.md` in `skills/project-prep/rules/`. Test:
   `scripts/check-rules.py` passes (27 lines, each within 30 words, no repeat of a ground rule), and its self-test
   goes red by name under `--break words|total|repeat|shape`.
2. **Setup and switching** in project-prep: step 1's fifth question, the section written in step 3, a "Switching
   rule groups" section, and a Rules slot in the `AGENTS.md` template. Test: `build-variants.py --check`; trigger
   cases `project-prep-yes-08` and `-09` (switch a group on; which rules are on) and `project-prep-no-07` (a rule
   that is not this kind).
3. **The records**: the catalogue proposal marked decided, ADR-010's History line, the patch version and a
   CHANGELOG line, ADR-022's public draft and ADR-018's. Test: `scripts/check-all.py` and
   `scripts/publish.py --dry-run` clean; nothing under `pending/` in the dry-run output.
4. **On ratification**: ADR-010 gets a dated banner at rule 4 pointing here. Test: `adr-check` clean.

**Confirmed by:** the checks prove the catalogue's shape and the triggers; whether the rules serve a project as
meant is the user's judgement once a project switches a group on (as for ADR-018).
**Revisit when:** a hook can reach Codex and Antigravity as well as Claude Code (rule 1's later option); copies are
found to drift; a held-back rule gets its starter list; or the platforms that install one skill folder
start installing whole plugins, which would let the catalogue leave project-prep.

## Alternatives

Each option is priced against the doctrine (function → ours → compatibility).

### AGENTS.md, from a catalogue in project-prep's folder (chosen: reaches every platform and adds no skill)
- Good: every tool reads `AGENTS.md`; nothing new loads for users who never switch a group on; one writer for the file
- Bad: project-prep grows a fifth setup question and a switching section; ADR-010's never-overwrite gains an exception
- Doctrine: function first; the catalogue is ours; plain lines in an agent-rules file are the common shape

### A RULES.md that AGENTS.md points to (not chosen)
- Good: `AGENTS.md` stays short
- Bad: an agent may skip the pointer, so "always on" becomes "usually"; Codex does not follow imports

### Injected by a plugin hook (kept open for later)
- Good: always current, nothing copied into the project
- Bad: only Claude Code has hooks, so Codex and Antigravity would get no rules (ADR-001)

### A rules skill of its own (not chosen)
- Good: its own trigger word; the most separate home
- Bad: a new description of about 100 words in every session for every user, a SKILL.md, trigger tests, manifest
  lines, and a second skill writing `AGENTS.md`

### A top-level rules/ folder (not chosen)
- Good: the easiest place to find in the repository
- Bad: missing on four of six platforms, which install one skill folder at a time

### A pinned shed script that does the copying (recommended in round 1, dropped)
- Good: an exact copy every time, and it runs without an agent
- Bad: a shed release and a pin for copying a few lines; the user asked for no added bulk

### The 28 rules as drafted (not chosen)
- Good: no change to the catalogue
- Bad: the lenses stay missing; three rules need list files nobody has written; "show it" repeats the user's own
  instructions; the datasheet rule keeps Check and review from being pre-ticked whole

## Consequences

- Good: the tagline's "rules" are real: a project can switch a group on, on every platform pitmaster supports
- Good: ADR-018's Plain words group and ADR-019's session-end nudge reach projects
- Bad: project-prep's setup round has five questions, so on Claude Code it takes two dialogs
- Bad: a hand edit inside the Rules section is lost at the next switch; own rules go under Ground rules
- Commits us to: `check-rules.py` in `check-all`; a catalogue date moved whenever a rule changes; starter lists for
  the three held-back rules before they ship

## History

- 2026-10-23: proposed.
- 2026-10-23: ratified by the owner.
- 2026-10-23: amended.

## Amendment — 2026-10-23: the held-back rules and their lists

**What changed.** The three rules that rule 4 held back join the catalogue, each with a starter list the project
keeps, which makes thirty rules and leaves none held back. The lines, word for word:

- `run`: "Give every scheduled task one home account, written in `docs/rules/task-homes.md`; check that list before
  making or moving one."
- `records`: "Leave each file in `docs/rules/hot-files.md` to its named writer: check that list before editing, and
  leave that writer a note of what should change instead."
- `records`: "When a tool sets a trap, add it, with what to do instead, to `docs/rules/tool-traps.md`; read that list
  once each session before using the tools."

Each joins the group the draft gave it. The lists live in the project's `docs/rules/` folder. Each starter holds a
title, one line saying what the list is for and which rule keeps it, and an empty table with its column headings:
task homes `task | home account | runs on | when`, hot files `file | its writer | why`, tool traps `tool | the
trap | do this instead | found`. The starters ship in project-prep's `templates/`, named after the file each makes.

When a group holding one of these rules is switched on, at setup or later, project-prep shows its list with the
Rules change and writes it on the same yes. It writes a list only where none exists and never overwrites one;
switching the group off leaves the list where it is. A list is a new file, so ADR-010 rule 4 still holds, and
rule 9's limit is untouched: each rule names its own list's path, so nothing is added to `AGENTS.md` outside the
Rules section. An update (rule 8) that brings one of these rules into a group already on offers its list in the
same change. The check of rule 10 gains a fifth arm, `lists`: a rule that names a file in `docs/rules/` must have a
starter of that name in `templates/`.

**Why.** Rule 4 held the three back until each ships with a starter list, and *Revisit when* named that event. The
user settled how they ship in a round of questions on 2026-10-23, taking the recommended option each time.

**Touches.** §The rules, rule 4 (twenty-seven rules become thirty; none held back), rules 5 and 6 (setup and
switching write a group's lists), and rule 10 (the check's `lists` arm). The ruled text stands; this section governs
where they differ. Rule 5's twelve pre-ticked lines are unchanged: `run` and `records` stay off at setup. Built in
`skills/project-prep/rules/run.md` and `records.md`, the three starters in `skills/project-prep/templates/`,
`skills/project-prep/SKILL.md`, `skills/project-prep/rules/README.md` and `scripts/check-rules.py`.
