# Rules: the opt-in catalogue

Decided by pitmaster ADR-022. A rule is one line an agent follows every session: no trigger, no steps. A project
chooses whole groups. project-prep copies the chosen groups' lines, word for word, into a marked Rules section of
the project's `AGENTS.md`, and switches groups on and off later (its SKILL.md, "Switching rule groups").

Catalogue: 2026-10-23

| group | heading | rules | at setup |
|---|---|---|---|
| `plan` | Plan and decide | 6 | pre-ticked |
| `run` | Run and delegate | 6 | off |
| `check` | Check and review | 2 | pre-ticked |
| `records` | Records and repository | 5 | off |
| `plain` | Plain words | 4 | pre-ticked |
| `craft` | Engineering craft | 7 | off |

30 rules, 12 of them pre-ticked. All groups together stay within 35 lines, and no rule runs over 30 words.

**Lists.** Three rules keep a list the project holds in its `docs/rules/` folder, and each rule names its list's
path. When the group is switched on, project-prep writes any list that is missing from its starter in `templates/`
(a title, one line on what it is for, and an empty table), and never overwrites one; switching the group off leaves
the list (ADR-022, amendment of 2026-10-23).

| list | group | starter |
|---|---|---|
| `docs/rules/task-homes.md` | `run` | `templates/task-homes.md.tmpl` |
| `docs/rules/hot-files.md` | `records` | `templates/hot-files.md.tmpl` |
| `docs/rules/tool-traps.md` | `records` | `templates/tool-traps.md.tmpl` |

**Changing the catalogue.** Keep each rule to one line; a new rule that names a list in `docs/rules/` needs its
starter in `templates/`, named after the file. Move the Catalogue date whenever a rule is added, reworded or
dropped: project-prep compares it with the date in a project's Rules section and offers the difference.
