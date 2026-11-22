---
name: ripplecheck
metadata:
  family: check
description: Before a branch lands, say which of the project's checks its changes feed, from a map file the project keeps; run the cheap ones and name the slow ones OWED with the command that runs them. Also starts a project's map. Use when the user types "ripplecheck", "knock-on", "knockon" or "butterfly-effect", or asks "which checks does this branch feed?", "what do I owe before merging?" or "why did the batch go red when nobody touched that?", and before a merge under goforit, goforitreally or carte-blanche in a project that keeps a map. Not for running a whole test suite, setting up CI, or knock-on effects outside code.
---

# ripplecheck: which checks this branch feeds

Decided by pitmaster ADR-045.
Built at the reference project's request (2026-11-18), after three batch pauses in
one day came from changes that fed a slow check nobody ran.

Sibling of `goforit` and `carte-blanche` (both run it before a merge, in a project that keeps a map) and
`open-items` (an unattended run posts its OWED rows there when it cannot name them itself). `bbq`'s PR type may
ask for the project's map when the run will land code.

The skill runs `scripts/ripplecheck.py`, a pinned copy of the pitmaster-shed tool (standard-library Python 3).
The script does the work; this page says
when to run it and what to do with what it prints.

## Words

- **row**: one check the project runs (a test suite, a census, a two-hour corpus run). The word is the project's;
  call it what the project calls it.
- **the map**: the project's file that says which changed paths feed which rows. Default `tools/ripplecheck.list`.
- **OWED**: a slow row the branch fed, not run here. Whoever lands the branch names it, then runs it or has the
  next batch run it.

## Config

Edit these lines here, or put the same lines in a `pitmaster.md` at your project root, which wins. Every line is
optional.

```
map: tools/ripplecheck.list     # the project's map
base: origin/main             # what a branch is diffed against
replays: tools/ripplecheck-replays    # past diffs that must name the row they missed; "none" for none
```

## Steps

1. **Find the map.** If the project has none, say so in one line and offer to start one (step 5). Never run with
   a made-up map.
2. **Run it:** `python3 scripts/ripplecheck.py --map <map> --base <base> --replay <replays>`, from the
   project root. It prints every row the diff feeds (`FED`, with file and map line), runs the cheap commands
   (`ok` or `RED`), and prints the slow rows as `OWED` with their commands.
3. **Read the exit.**
   - **0, green:** say so in one line and carry on.
   - **1, red:** stop the landing. Show the `RED` lines as they are. A failed run is fixed in the branch. A broken
     map (an unmapped file under a strict prefix, an undeclared row, a row nothing feeds) is fixed in the map,
     in the same branch, and the user sees the new map line in the PR.
   - **2, OWED:** the branch may land only if the project's rules allow OWED rows and the cheap parts were green.
     Name each OWED row and its command in the PR body or the landing record, then re-run with `--named ROW,...`
     to show it is clean. Never drop an OWED row silently, and never name one to get past a red.
4. **Report** in the PR body: the rows fed, the runs and their result, and each OWED row as named.
5. **Start a map** (on the user's yes). Copy `templates/ripplecheck.list` to the map path. List the project's
   checks as `row` lines (from CI, the Makefile, the test runner), mark each `cheap`, `slow` or `sweep-only`, and
   add `feed` lines for what you can see feeds each. Put the fast gate every change runs on `always` lines. Ask the
   user which folders are **strict** (where an unmapped change is red) and say why it matters: everywhere else an
   unmapped file is one quiet line. Run `--check-map` until it is clean, and land the map in its own PR.
6. **After a check went red that nobody ran** (a batch pause, a red main), add a replay: a `*.replay` file in the
   replays folder holding `expect <ROW>` and the diff that slipped (`git diff --name-status` lines). Run it once
   against the old map to see it fail, then add the feed line that makes it pass. That failing run is the proof
   the replay can catch the gap.

## The map's lines

```
row    <ROW> cheap|slow|sweep-only [-- <command>]
feed   <glob> <ROW> [-- <targeted command>]
always <ROW> [-- <command>]
strict <prefix> [<prefix> ...]
```

Every matching line fires, not the first. A feed with a targeted command runs that instead of the row's whole run,
so a slow row can have a cheap slice for the paths that feed it. Globs: `*` and `?` stay in one folder, `**`
crosses folders, a trailing `/` means everything below. `#` starts a comment only at the start of a line. A `strict` prefix is a folder; one ending
in `*` (`tools/gen*`) covers every path that starts with the text before the `*`.

The script also reads a second format, one rule a line with bars, `glob | row | run|owed|always | command`
(`-` for no command); the two can be mixed in one map. In it each rule says whether it runs or is owed, and
`sweep-only <ROW> ...` lines and `--rows <file>` (the project's own list of rows) feed the coverage check. In
either format `{files}` in a command stands for the changed paths that fired it. Use whichever the project already
has; for a new map, the keyword format above, which keeps each row's class and full command in one place.

`examples/batch-pauses/` holds one illustration map in both formats, with three replays.

## Never

- Run a command the map does not name, or run outside the project root.
- Edit the map to make a branch pass without showing the user the new line.
- Call a branch green while it has OWED rows nobody named.

## Platform notes

- **Claude Code:** run `scripts/ripplecheck.py` with the shell tool from the project root; under goforit or
  carte-blanche, run it before the merge and name any OWED rows in the PR.
- **Cowork / claude.ai:** where no shell runs, read the map by hand against the branch's changed files and list
  the rows it feeds, each marked run or OWED; run nothing.
- **Codex:** as Claude Code, with Codex's shell.
- **Other tools:** run the script where the tool has a shell; otherwise read the map by hand, as above.
