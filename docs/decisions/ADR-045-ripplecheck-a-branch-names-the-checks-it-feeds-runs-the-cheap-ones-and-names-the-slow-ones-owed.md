---
status: accepted
status-note: ratified by the owner 2026-11-18
ratified-by: the owner
ratified-on: "2026-11-18"
owner: the owner
kind: process
built: partial
proof: "`skills/ripplecheck/SKILL.md`, `skills/ripplecheck/scripts/ripplecheck.py`, `skills/ripplecheck/scripts/ripplecheck.pin`"
owed: the trigger evals run (step 4); a first real run in the reference project (step 6)
supersedes: nothing
amends: nothing
---
# ADR-045 — ripplecheck: a branch names the checks it feeds, runs the cheap ones and names the slow ones OWED

This is the published version of this decision. Some internal details have been left out.

problem, the rules and the bar line format); this session (Opus 5.5), which built the draft and wrote this ADR
**Revisit when:** the reference project ratifies, amends or rejects its ADR-293, or a second project adopts the tool

## Decision

A new skill, **ripplecheck** (family `check`), says before a branch lands which of the project's checks the
branch's changes feed, from a map file the project keeps. It runs the cheap checks and names the slow ones OWED,
so no change lands having fed a check nobody ran.

1. **A new skill plus a shed tool**. The skill starts a project's map, reads the tool's exits, and adds a
   replay after a miss. The engine is a pitmaster-shed tool, and the skill carries a pinned copy (ADR-012).
2. **The name**: `ripplecheck` is the folder and the name other skills call. "ripplecheck", "knock-on" and
   "butterfly-effect" all load it.
3. **The engine moves to the shed now, diskcheck's way**: a shed PR holds the engine, and the draft carries a
   byte-for-byte copy pinned to that PR's commit, then to the next shed tag.
4. **The map**. Default path `tools/ripplecheck.list`; one config line names another. The engine reads
   two line formats, mixed freely in one map:
   - keyword lines: `row <ROW> cheap|slow|sweep-only [-- command]`, `feed <glob> <ROW> [-- targeted command]`,
     `always <ROW> [-- command]`, `strict <prefix> ...`, `sweep-only <ROW> ...`;
   - the reference project's ADR-293 bar lines: `glob | row | run|owed|always | command` (`-` for none).
   In either, `{files}` in a command stands for the changed paths that fired it.
5. **What it does with a diff.** The diff is `git diff --name-status -M <base>...HEAD`, from the merge base. Every
   matching rule fires, not just the first, and each fired check is printed with the file and map line. `always`
   rules carry the project's fixed fast gate. An unmapped changed file under a `strict` prefix is red; elsewhere it
   is one "N files unmapped" line. Coverage: every check the project lists is fed by a rule or declared sweep-only.
   Replays: a `*.replay` file holds a past diff and the check it must name, and goes red if the map stops naming it.
6. **Exits**: 0 green; 1 a run failed or a rule is broken; **2 OWED**, kept apart from red; 3 it could not run.
7. **OWED may merge if named**. Pitmaster's default: a branch with OWED checks may merge once every cheap check
   is green and each OWED check is named in the PR or landing record. A project rule may make OWED block.
8. **Callers**: `goforit` and `carte-blanche` run it before a merge, in a project that keeps a map, and name
   its OWED checks in the PR. Nothing else calls it.
9. **Never**: run a command the map does not name; edit the map to get a branch through without showing the
   owner the new line; call a branch green with OWED checks nobody named.

## Context

Drivers:
- A missed slow check costs hours, because a red batch stops everyone.
- A rule that lives only in notes stops being applied; the map must be checked by a tool.
- The doctrine: function, then ours, then compatibility. Ours on the surface (the name, the default path),
  compatible underneath (the engine reads the reference project's format as written).
- One source for the engine (ADR-012).

## Alternatives

### A new skill plus a shed tool (chosen: starting a map and adding a replay are agent steps, and the engine still runs with no agent)
- Good: agents get steps; CI and coordinators run the tool alone; goforit and carte-blanche call one thing.
- Bad: one more always-loaded description.

### A script inside goforit
- Good: no new skill.
- Bad: nothing teaches an agent to start a map or add a replay, and a hand run has no skill to load.

### A shed tool only
- Good: the lightest.
- Bad: no agent steps.

### One line format only
- Good: one reader to keep. Bar lines only would match the reference project; keyword lines only would be ours.
- Bad: bar only drops a row's class and full command stated once; keyword only makes the reference project rewrite
  its map or keep its own engine.

### Move the engine to the shed at the move into skills/
- Good: less work now.
- Bad: a draft that breaks ADR-012 until then.

### Default map path `tools/row-feeds.list`: the recommendation, withdrawn
- Good: the reference project needs no config line.
- Bad: puts compatibility before ours, against the doctrine's order when the options work alike. Withdrawn by the
  lead when the user asked "2 is probably better, isn't it?".

### OWED exits 1, like red
- Good: safest by default.
- Bad: a project that lets OWED merge must read the output to tell owed from red.

### OWED blocks by default
- Good: safer where no batch sweep stands behind the merge.
- Bad: stops every merge that touches a slow check until it runs.

## Consequences

- A project that keeps a map gets every check a branch feeds named before it lands, with the file and rule.
- The fixed fast gate becomes lines in one file.
- Each miss can become a replay that keeps the map honest.
- The reference project can use its ADR-293 map as written, with one config line for its path.
- The skill adds one always-loaded description; goforit and carte-blanche each gain a line.

**Steps to build:**
1. The draft under its working name, with the engine, a self-test (38 cases, 10 deliberate failures), a starter
   map, an illustration map in both formats with three replays, seven trigger evals, and the pointer lines — done
   before this decision was made. Test: the engine's `--self-test` in check-all.
2. Rename the draft to `ripplecheck`: folder, script, triggers ("ripplecheck", "knock-on", "butterfly-effect"),
   default map `tools/ripplecheck.list`, evals, pointer lines. Test: check-all; the self-test.
3. The shed PR with the engine, and the draft's copy pinned to its commit. Test: the shed's CI on ubuntu,
   macos and windows; `scripts/check-pins.py`.
4. Run the trigger evals, three runs each. Test: every case passes.
5. After ratify, the move into `skills/` (offered, not made; ADR-026), the patch bump and a CHANGELOG line; the pin
   moves to the shed's next tag. Test: check-all, and `publish.py --dry-run` once this ADR's public copy is
   approved.
6. A first real run in the reference project: a branch checked with its map, and a replay of one of the three
   pauses going red on the map from before the fix. Then `built: landed`. Test: the run's output in that project.

## Asks left open

None from the rounds. To veto, if any: the nine defaults in the record's *Defaulted* table (uncommitted work not
counted; renames, deletions and copies; commands through the shell; git's `:(glob)` rules; strict prefixes in the
map; exit 3; the replay format; the five readings where ADR-293 is silent; `kind: process`).

## History

- 2026-11-18: proposed.
- 2026-11-18: ratified by the owner.
