---
status: accepted
status-note: ratified by the owner 2026-11-23
ratified-by: the owner
ratified-on: "2026-11-23"
owner: the owner
kind: architecture
built: partial
proof: "`skills/ripplecheck/scripts/keyed-merge.py`, `skills/ripplecheck/scripts/keyed-merge.pin`"
owed: the shed PR's merge and a shed tag for the pin (step 1); a first real run in a project with shared tables (step 4)
supersedes: nothing
amends: nothing
---
# ADR-047 — keyed-merge: a shed tool merges shared tables by key and stops only on a real conflict

This is the published version of this decision. Some internal details have been left out.

**Revisit when:** git or GitHub starts running repository-declared merge drivers on the server, or the reference
project adopts or declines the tool in place of its own writers

## Decision

A new pitmaster-shed tool, **keyed-merge**, merges the checked-in tables that many branches add to (censuses,
allowlists, ledgers, case lists) by key instead of by line. Where both sides only add or each change different rows,
it takes the union; it stops only on a real conflict.

1. **A shed tool, two ways in, one engine**. A git merge driver (`.gitattributes` names a file
   `merge=keyed-merge`) for merges, rebases and cherry-picks, and a command that merges three given versions or
   previews a branch pair. It lives in pitmaster-shed (ADR-012).
2. **The name**: **keyed-merge** is the folder, the command, the driver name and the config file
   (`.keyed-merge`). **tablemerge** is a second name: `install` also registers `merge=tablemerge`, and a `tablemerge`
   command runs the same tool.
3. **Formats, version 1**: a JSON object keyed by name; a JSON list of records keyed by a field or a tuple of
   fields; JSONL; TSV and CSV with a header and named key columns; a list of names, one a line; a Markdown table
   with key columns. YAML and TOML are out.
4. **The merge rule, per key.** Changed on one side only: that side. The same change on both: once. Added or
   changed differently on both, or deleted on one side and changed on the other: a conflict. A duplicate key in any
   input: refused. Row order comes from the config (sorted by key, or the order rows were added), never from
   either side.
5. **Conflicts**: every clean row is merged; only conflicted rows carry git's `<<<<<<<` / `=======` /
   `>>>>>>>` markers (for JSON, the whole record), and one report line per conflicted key.
6. **Generated tables**: the config can mark a table generated, with its regenerate command. The driver
   takes either side, runs the command after the merge and stops if it fails. It runs a command only if this
   clone's own git settings approve that exact command (`install` or `trust`); any other is refused, with how to
   approve it.
7. **The config**: one `.keyed-merge` file at the repository root, one line per table: path or glob, format,
   key, row order, generated or not.
8. **Output and exits**: plain lines for people, `--json` with the same content for agents. Separate exit
   codes for clean, conflicts, bad input (a duplicate key, an unreadable file) and refused (an unapproved command).
9. **The count lint**: `keyed-merge lint` reads the same config and the files beside it, flags bare counts and
   suggests a keyed list. It reports only, unless a project asks it to fail.
10. **Who carries it**: ripplecheck carries a pinned copy and names a keyed table both sides of a branch
    changed; project-prep's setup offers to install the driver in a project that has shared tables.
11. **Never**: write any file but the one being merged (and, for `install` and `trust`, this clone's git
    settings); drop or invent a row silently; run a regenerate command not approved locally; commit, push or change
    branches; reach the network.
12. **Platforms**: Python 3.8+, standard library only, CI on Ubuntu, macOS and Windows, as every shed tool.

## Context

Drivers:
- A silent wrong merge is worse than a conflict: union's failure must become a conflict.
- Every clean add should merge with no one asking, on every clone and agent worktree.
- A checked-in file must never be able to make a merge run a command nobody approved.
- The doctrine: function, then ours, then compatibility. Ours on the surface (one config, our report), compatible
  underneath (git's own driver interface and conflict markers).

## Alternatives

### Driver and command over one engine (chosen: merges happen unasked, and an agent can still preview or redo one)
- Good: everyday merges need no one; agents can explain a merge without running git.
- Bad: two entry points to test.

### Driver only, or command only
- Good: smaller.
- Bad: driver only gives agents no preview; command only leaves every merge of these files to someone remembering.

### Fewer formats in version 1
- Good: less to build.
- Bad: Markdown ledgers, the commonest shared table in pitmaster-style projects, would wait.

### Keep ours and write a separate report on a conflict; or leave the whole file to git
- Good: the file stays valid, or nothing new to learn.
- Bad: the first hides that theirs was dropped; the second loses every clean row's merge.

### Refuse generated tables and say "regenerate"; or merge their rows and warn
- Good: no command runs from a merge.
- Bad: the first leaves the gap open; the second merges what should be measured.

### Trust the checked-in config's command; or keep commands only in local settings
- Good: simpler, or safest.
- Bad: the first lets any branch run code at merge time; the second makes every clone set commands by hand.

### The config inside `.gitattributes`, or as JSON
- Good: one less file, or easy for tools.
- Bad: cramped lines, or hard for a person to edit.

### The lint later as its own tool, or never
- Good: a smaller version 1.
- Bad: counts keep being added while the tool that cures them waits.

## Consequences

- A project that names its shared tables in `.keyed-merge` stops getting conflicts on independent adds, and gets a
  named conflict, never a silent double row, when two branches change one key.
- Every clone and agent worktree needs `install` once. On GitHub a PR still shows a conflict that a local merge
  resolves.
- A union is a prediction: two branches right alone can be wrong together. The report says when both sides changed
  a table, and ripplecheck names the checks that read it.
- The shed gains a tool; ripplecheck and project-prep each gain a few lines and a pin.

**Steps to build:**
1. The tool in pitmaster-shed (backroom), Claude building and a blind Codex review checking, in a PR there. Test:
   `keyed-merge --self-test` with these arms (clean union; one key changed two ways; delete against edit; a
   duplicate key; reorder only; union's double row as a conflict; an unapproved command refused; the lint finding a
   count; a real git merge through the installed driver), every merge arm for all six formats, each run once against
   a deliberately broken tool; the shed's CI on all three systems.
2. Whether `git merge-tree`, rebase and cherry-pick call the driver, tried once and recorded (the record's
   Defaulted list). Test: the result in the shed PR.
3. The pinned copy in ripplecheck and project-prep's offer, in one PR here with the plugin's patch bump and a
   CHANGELOG line. Test: `scripts/check-pins.py`, check-all, `scripts/publish.py --dry-run`.
4. A first real run in a project with shared tables. Then `built: landed`.

## Asks left open

- None.

## History

- 2026-11-23: proposed.
- 2026-11-23: ratified by the owner.
- 2026-11-23: amended.

## Amendment — 2026-11-23

**What changed.** Rule 6's driver no longer runs the regenerate command itself. When both sides changed a generated
table, the driver keeps our side and stops the merge on that file with a message naming the table and its command.
Once the rest of the merge is in place, `keyed-merge regen` runs the locally approved command (the trust rule is
unchanged) and checks that the result parses in its format. This works the same for merge, rebase and cherry-pick.

**Why.** Git calls a merge driver before the merged files are written (tested with git 2.54.0), so a command run from
inside the driver would read the unmerged inputs and write a wrong table.

**Touches.** Decision, rule 6. Rule 11 is unchanged: the driver still writes only the merged file.
