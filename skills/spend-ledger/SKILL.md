---
name: spend-ledger
metadata:
  family: usage
description: Record what a session actually spent (tokens read from its own transcript, the usage meter's movement, a list-price proxy) beside what it landed (merged, opened and committed counted apart), as one row in the project's spend ledger, and report spend per landing over a window. The after-the-fact twin of budget-select. Use when the user types "spend-ledger", says "log the spend", "record what this session cost", "what did this comrun cost" (a comrun is also written com-run, com run, commission run or commissioned run), "what did we get for the points", "cost per PR", "where did the week's usage go" or "which sessions spent and landed nothing", and at the close of a session in a project that keeps a ledger. Reads Claude Code and Codex transcripts with its script; on any other platform it asks the user for the meter reading and writes the row by hand.
---

# spend-ledger: what a session spent, beside what it landed

Decided by pitmaster ADR-009.

Sibling of `budget-select` (its calibration row takes this skill's token figures), `tier-select` (the report shows
each lead model's cost per landing), `carte-blanche` and `dealers-choice` (their end summary's "points spent"
comes from step 5), `swarm-bottleneck` (which may read the ledger when spend is the constraint) and `setfree` (which
adds a row at the close of release day; not shipped yet).

**A usage meter is shared** by every session on the plan, including chats this machine never sees (claude.ai, the
phone, a cloud container, another computer). So the ledger keeps three figures apart: **tokens**, measured from
the session's own transcript; the **meter**, read before and after; and the **points** this session is estimated
to have moved, which is the whole movement only when nothing else ran beside it.

To close one session, run step 2's script with `--lead` and `--landed` and append its row; a meter reading, step
5's line and the report are extras.

## Config

Edit these lines here, or put the same lines in a `pitmaster.md` at your project root, which wins. Every line is
optional.

```
name: the user                 # whose plan it is. "name: Alex" makes this skill say "Alex".
ledger: auto                   # auto = docs/spend-ledger.md if docs/ exists, else spend-ledger.md at the root
on_close: when-ledger-exists   # when-ledger-exists | always | never: write a row at session close unasked
prices: scripts/prices.tsv     # the dated list prices behind the proxy
```

## Steps

1. **Which job.** **Close** records one session, usually this one, when it ends or when the user asks ("log the
   spend"). **Report** reads the ledger over a window ("what did this week cost"). Asked for both, close first.
2. **Close: measure.** From the session's working folder, run `scripts/spend-ledger.py measure --lead "<model>,
   <effort>"`. It reads the session's most recent transcript (or `--session <id>`) and prints one ledger row:
   tokens by kind, the workers' share, the model mix, the list-price proxy and the meter.
   - **The meter.** Where the transcript carries it, the row has it. Otherwise pass `--meter START END`: a
     reading taken now, and the start reading from the Budget block, the session's first log line, or a reading
     taken when it began. With no start reading, the cell says "not read". Never guess one.
   - **Shared or alone.** The script counts the other sessions on this machine active in the same window. Alone,
     the meter's movement is this session's own ("alone here"). Shared, the row gives this session's share of the
     movement, weighted by list price and marked "est", never the whole movement.
   - **No script for this platform:** ask the user for the meter's start and end readings (and token counts, if
     their tool shows them), and write the row by hand in the same columns, with "given" in the note.
3. **Close: what landed.** `--landed` takes a count per kind, such as `--landed "2 merged, 1 opened, 1 committed"`:
   - **merged:** a PR merged.
   - **opened:** a PR open and not merged.
   - **ratified:** an ADR ratified.
   - **committed:** a record, a doc or work on a branch, committed and pushed with no PR of its own.

   Count each landing once, under the furthest it got; a local commit never pushed does not count. Links may
   follow ("2 merged, 1 opened: #18, #19, #21"). A session that landed nothing writes `0` and says in `--note`
   what it produced instead (an answer, research, a parked question), so the report can tell useful zero-landing
   sessions from waste. Old rows (a bare number, or "2: #18, #19") read as "not split".
4. **Close: append the row**, creating the ledger with its header if it is missing. **Never edit a row already
   written:** a correction is a new row for the same session, its note starting "corrects", and the report keeps
   the latest row per session.
5. **Close: hand the numbers on in one line.** "Spent: $3.69 list-price proxy, ~0.4 pts (shared with 2), landed 1
   merged: #20." If `budget-select`'s calibration row is due (the session dispatched workers), its token columns
   take these figures: one measurement, written in two places. A `carte-blanche` or `dealers-choice` end summary
   takes this row's meter figure as its points spent.
6. **Report.** Run `scripts/spend-ledger.py report --ledger <ledger> --since <date> --until <date>` and say in a
   few lines: the totals; the cost per landing, and per merged landing where rows have a split; the sessions that
   spent and landed nothing, with their notes; spend by lead model; and the largest three. Add at most one
   observation ("Opus-led sessions cost three times as much per landing this week"). It is not a ruling: changing
   a share or a tier goes through `budget-select` or `tier-select`, and the user.
7. **Never:**
   - put anything from a transcript but counts into the ledger (no prompt text, file contents or secrets). It
     holds numbers and links only.
   - call the list-price proxy a bill or the plan's meter. It puts models on one scale, nothing more.
   - read another project's transcripts for anything but the overlap count, which uses token counts only.
   - import another tool's usage data (ccusage and the like). The ledger holds only what this script measured or
     the user gave.

## Platform notes

- **Claude Code:** the script reads `~/.claude/projects/`, with each session's `subagents/` folder as its workers.
  The desktop app's usage tool gives the readings for `--meter`; `gh pr list --author @me --state all` lists the
  landings. A cloud session runs the script inside its container before it ends, since its transcript never
  reaches this machine.
- **Cowork / claude.ai:** no shell and no transcript on disk. Ask for the weekly percentage from Settings → Usage
  at the start and the end; tokens are "not read".
- **Codex:** the script reads `~/.codex/sessions/`, taking the meter's start and end, the model and the effort
  from the transcript. Workers started with `codex exec` are separate sessions: measure them with `--all` over
  the comrun's window and add their rows.
- **Other tools:** write the row by hand. If the tool keeps token counts in a file, a reader is one function in
  `scripts/spend-ledger.py`; propose it upstream.
