---
name: neighbour-check
metadata:
  family: usage
description: Check on the neighbours on the user's allow list (other model families such as Codex, Gemini through Antigravity's agy and OpenCode Go, local models on Ollama or LM Studio, a project's lanes, another Claude account), live and read-only, for what limits each one (its usage meter or quota, its reset and burn rate where one can be read; where none can, it asks the user for the reading) and whether it is busy (jobs running, lanes held, a box in use), and write the Neighbours block a prompt carries beside the Budget block. Use after budget-select and before tier-select in a session that will send work to a neighbour, before writing an overnight prompt, swarm kickoff or handoff that routes work to one, when the user types "neighbour-check", "neighbor-check" or "checkonneighbours", or asks "check on the neighbours", "how much Codex is left", "is Codex busy", "is the lane free", "can we use Gemini", "what's the other account at" or "who has room".
---

# neighbour-check: what limits each neighbour, and whether it is busy

Decided by pitmaster ADR-029.

Sibling of `budget-select` (how much of this account's limit a session may spend; this skill reads the neighbours'
limits), `tier-select` (which routes work only to neighbours this skill does not report closed or busy),
`townhall` (whose neighbours doc is this skill's list) and `spend-ledger` (whose close leaves the closing reading
that the other account's run of this skill reads).

"Neighbours" is townhall's word: the models other than the one you are talking to that a skill may call. This
skill checks only the names on the neighbours doc, which is an allow list. "Gemini" means Antigravity's `agy`;
Gemma is a separate local model.

**The smallest use:** "neighbour-check", one run of the script, and its block quoted back.

## Config

Edit these lines here, or put the same lines in the neighbours doc under a `## neighbour-check` heading (every
project on this machine), or in a `pitmaster.md` at your project root (this project only), which wins. Every
line is optional; the script prints which file each setting came from (`--json`).

```
name: the user                 # who is asked for the readings no file holds; "name: Alex" makes it say "Alex"
burn: show                     # show | hide: hide keeps burn in the verdicts but prints no burn numbers
probes: codex, agy, go, claude, ollama, openai, lanes, guard   # the kinds that run; leave one out to switch it off
meters: ~/.claude/meters.tsv   # the shared readings file (below)
now: ~/.claude/now.tsv         # the machine-wide now signal: which sessions are open, on which account
codex_home: ~/.codex           # where Codex keeps its session logs
codex_trees:                   # a folder of Codex dispatch jobs (open = a started file, no finished file); empty = off
agy_trees:                     # a folder of agy dispatch clones; empty = off
opencode:                      # the opencode binary; empty = on PATH, else ~/.opencode/bin/opencode
go_limits: 12, 30, 60          # OpenCode Go's dollars per 5 h, per week, per month
lane_status: lanes/queue/STATUS.json   # a project's lane queue, from its main checkout; none there = no lanes
lane_holds:                    # an extra folder of machine-wide HOLD files; empty = off
lane_switch:                   # a file whose LANES: line switches the lanes off; empty = off
```

Two more kinds of line take a neighbour's name, and belong in the neighbours doc's section, since they name
machines:

```
kind box-a: openai             # the kinds to check for one neighbour, when the guess gets it wrong; none = skip it
guard lane-a: user@box-a lane-check -q   # a read-only busy check over ssh: destination, then the command
```

## The kinds, and what can be read

The script guesses each neighbour's kinds from its row (name, how to reach it, family); one row may have several.

| kind | guessed from | what limits it | how it is read | busy signal | when it cannot be read |
|---|---|---|---|---|---|
| **codex** | "codex" in the name or reach | one 7-day window per account, shared by every Codex process | the newest reading in its session logs: used %, reset, plan; burn from that window's readings 24 h and 3 h back | `codex exec` jobs; open dispatch jobs; sessions written in 15 min, by project | no reading in 8 days: ask |
| **agy** | "agy", "antigravity", or a neighbour named gemini | Antigravity's quota | **not readable**: agy keeps it to itself | `agy` processes; clones touched in 30 min | always: ask |
| **go** | "opencode" | one weighted pool: per 5 h, per week (Monday 00:00 UTC), per month | only a floor: `opencode stats` is raw, unweighted spend | `opencode run` jobs | the weighted pool is on its console: ask |
| **claude** | family Claude or Anthropic | each account's weekly meter | the newest line for that account in the readings file | its open sessions in the now signal | no reading yet, or its reset passed since: ask |
| **ollama** | "ollama", or port 11434 | no meter (local) | its model list and what is loaded | what is loaded | no answer: down |
| **openai** | "lm studio", "openai", or any address in the row | no meter (local) | `/v1/models` at the row's address | none shown | no answer: down |
| **lanes** | "lanes" | no meter: held lanes, a busy queue, the switch | the project's lane queue status and HOLD files | the lane's state, holds, queue | the project has no queue: no verdict |
| **guard** | a `guard` line | a box that refuses work while in use | the `guard` command over ssh, read-only | its `VERDICT:` line, or its exit code | no answer: unreachable |

## Steps

0. **Will this session send work to a neighbour, or did the user ask?** If neither, say nothing; the steps end
   here.
1. **Leave this account's reading for the others.** Read the usage meter (Platform notes), then from this skill's
   folder run `python3 scripts/neighbour-check.py record --weekly <weekly %> --weekly-reset <its reset> --five
   <5-hour %> --five-reset <its reset> --session "<what this session is>" --config SKILL.md`. It appends one line
   to the readings file. Skip this step where no meter can be read.
2. **Run the probes**: `python3 scripts/neighbour-check.py --root <project> --config SKILL.md` (a few seconds, more when a guard's ssh is slow;
   `--only <names>` for a re-check, `--json` for the raw readings, `--burn hide` for one run). It prints the
   draft block. Quote it; never retype its numbers.
3. **Get the readings that cannot be read.** For each neighbour this session will send work to whose verdict is
   UNKNOWN, ask the user for the reading the block's *Ask* line names, in one round, with what each reading is
   for in the question's own wording. Write each answer into the block as `<reading> (<name>, HH:MM UTC)`. A
   prompt written for a later session keeps the Ask line instead: its lead asks.
4. **Write the Neighbours block** into the prompt after the Budget block, in this shape and no longer:

   ```
   ## Neighbours
   Measured HH:MM UTC by neighbour-check (verdicts PROVISIONAL). Burn: shown.
   <name> (<kinds>): <VERDICT>. <meter>. Burn: <+N points in H h; out in ~X at that pace>. Busy: <what it is doing>.
   …one line per neighbour, then the Lanes line, Not checked, and the readings the user gave…
   On pickup, run neighbour-check again: every line above is a reading, and readings go stale.
   ```

5. **Route by it.** The project's own route order stands; this block only moves a neighbour within it:
   - **closed:** send nothing new there.
   - **tight** (it runs out before its reset at its recent pace): send only work that nothing else on the route
     takes, and tell the user in one line, with the hours it has left.
   - **on pace:** route as the project says.
   - **spare** (it ends its window under 80 % at its pace): send it every job it can take, first.
   - **busy** (a lane held or in use, a guard refusing, another session's jobs in flight): queue behind it or take
     the next neighbour; never stop another session's work and never clear its hold.
   - **down**, or **unknown** with no reading given: take the next neighbour; ask first when the work is large.
6. **Re-check** with `--only <names>` before each batch that sends work to a neighbour, and at each batch's end. A
   Codex reading updates only when some Codex call runs, so the block prints its age.
7. **Close.** The closing reading goes in through `spend-ledger`'s close; in a project that keeps no ledger, run
   step 1 again before the session ends. A lead that hands off writes the newest block into its handoff.
8. **Never:**
   - check a name the neighbours doc does not list, or write a reading nobody read.
   - stop another session's job, clear a hold, or run anything on a neighbour but the read-only checks above.
   - call a verdict a ruling: the lines are provisional (ADR-029) until the user rules them.

## The readings file: how one account sees another's meter

`~/.claude/meters.tsv`, on this machine and outside every repository, one tab-separated line per reading: when, the
account's label, its name, weekly %, weekly reset, 5-hour %, 5-hour reset, and what the session was. The label is
the one the machine-wide now signal writes, so the two files join; an account's name is its weekly reset's weekday
("the Sat account"). **Who writes it:** step 1 and `spend-ledger`'s close, on any account. **Who reads it:** this
skill, for the accounts it is not running on. Lines are only appended. A reading is a fact about its moment: the
block prints its age, and a reading from before the account's reset is void.

## The script

`scripts/neighbour-check.py` is a pinned copy of pitmaster-shed's `neighbour-check` tool (`scripts/
neighbour-check.pin`); never edit it here. Standard library only, Python 3.8 or newer. Every probe reads a file,
lists processes, asks a local server for its model list, or runs a check its settings name as read-only; the only
write is `record`'s one appended line. A probe that fails reports its neighbour down; it is never skipped.
`--self-test` runs on fixtures only, and its last case plants a defect in the real Codex pace (an earlier window's
readings leak in) that must be caught; with `NEIGHBOUR_CHECK_BREAK=1` set from outside, `--self-test` exits 1.

## Platform notes

- **Claude Code:** in the desktop app, its usage tool gives step 1's readings (weekly and 5-hour, each with its
  reset); ask with the `AskUserQuestion` tool. The script runs from the skill's folder.
- **Cowork / claude.ai:** no shell. Read Settings → Usage for step 1 and write the block by hand from the user's
  readings, with every neighbour's line marked "given".
- **Codex:** `/status` shows Codex's own meter; the script runs wherever Python 3 does. Ask each round as a
  numbered list in one message.
- **Other tools:** ask the readings as a numbered list in one message, and write the block by hand where the
  script cannot run.
