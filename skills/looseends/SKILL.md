---
name: looseends
metadata:
  family: check
description: Find what was left unfinished in this chat, across the whole project, or around one ADR or topic - questions never answered, promises not kept, things waiting on the user's ruling, work never landed - check each is still open, list them by who acts, and offer to tie them off. Use when the user types "looseends", "looseends chat", "looseends session", "looseends project", "looseends decisions" or "adrorphans" (past decisions no ADR covers), or "looseends" followed by an ADR or a topic, or "treslooseends" followed by the projects to check (every project named, each by name), or "looseendsreally" (ties off its own share without asking), or asks "any loose ends?", "tie up the loose ends" or "what loose ends are left". Plainer asks such as "what's left hanging?", "what did we leave open?" or "what's still open?" also load it, and it first asks "Check for loose ends? This chat, the project, or a topic?"
---

# looseends: find what was left unfinished, and offer to tie it off

Decided by pitmaster ADR-019.
"treslooseends" and "looseendsreally": ADR-023.
The decisions scope ("looseends decisions", "adrorphans"): ADR-038.

Sibling of `goforit` (a settled plan that was never built), `dealers-choice` (takes the bigger work that is the
agent's), `makeadr` (an unratified ADR, one with asks left open, an ADR candidate left open, or a past decision
no ADR covers) and `bbq` and `talk-through` (their records' Owed lists, ADR candidates, calls open to veto and
open questions are loose ends this skill reads). `catchmeup` looks at what changed inside a window and sends the
older items still waiting on the user here.

## Config

Edit these lines here, or put the same lines in a `pitmaster.md` at your project root, which wins. Every line is
optional.

```
name: the user                   # who the skill speaks to; "name: Alex" makes it say "Alex"
looseends_dir: docs/looseends    # where a chat's loose ends are written: <looseends_dir>/<date>-<topic>.md
looseends_markers: default       # what the scan looks for: default, or a file in the scan's marker format
looseends_decisions_markers: default  # the decisions scope's: default (references/decisions-markers.txt), or a file
land: commit                     # commit (branch only) | pr (branch + PR) | file (just the file) (step 6)
```

## Steps

1. **Which scope.** The word after the opener sets it: `chat` or `session` (two words for one thing: this
   conversation), `project` (the whole repository), `decisions` (past decisions no ADR covers; "adrorphans" says
   the same in one word, see *looseends decisions* below), or anything else as a topic (an ADR number, a skill, a
   subject). Plain `project` never runs the decisions sweep. A plain "looseends", or a plainer ask that loaded this
   skill, asks one question first: "Check for loose ends? This chat, the project, or a topic?" Stop on a no.
2. **Gather, inside the scope only.** Four kinds:
   - **Questions never answered**, asked by either side.
   - **Promises not kept**: "I'll do X next", next steps, action items, owed work.
   - **Waiting on the user's ruling**: a decision, a ratification, an approval, a call left open to veto.
   - **Work never landed**: uncommitted files, a stash, a branch never pushed, an open PR, a red check.

   Where to look:
   - **chat**: this conversation from its start, and the work it did (its branches, commits, files and PRs, and
     any workers it started). Nothing outside it.
   - **project**: fetch, then run `scripts/looseends-scan.py` (with `--markers <file>` when `looseends_markers`
     names one). It lists each marker the project's records use,
     with `file:line`: the status file's waiting section, the debt list, records' Owed lists and calls open to
     veto, ADRs' open asks and unratified ADRs, open proposals' questions, commented publish lines, unticked items
     in earlier looseends records, and git's unlanded work. Add what it cannot see: open PRs, their checks,
     review comments waiting for an answer, and records' *ADR candidates* lists (ADR-036): a candidate neither
     picked for an ADR nor marked "not an ADR, by the user". Without the script, read the same places by hand.
   - **topic**: the project's sources narrowed to that subject (`--topic`), plus anything said about it in this
     chat.
   - **decisions**: not the four kinds but decisions already made, with no ADR. It gathers, checks, lists and
     offers by its own steps, in *looseends decisions* below, in place of steps 2 to 6.
3. **Check each is still open** before listing it: a cheap look for the answer, the commit, the merged PR or the
   ruling (search the main branch, read the file it cites). Drop what is closed. Mark anything you could not check
   *unverified*.
4. **List them by who acts**, each in one line with where it came from (`file:line`, a PR, or the point in the
   chat):
   - **Yours**: what only the user can answer or rule.
   - **Mine**: what the agent can tie off.
   - **Waiting on someone else**: a reviewer, a check, another person.

   Many of one kind from one place make one line ("14 calls open to veto in last week's planning record"). End with
   the counts.
5. **Offer to tie them off.** Act only on the user's yes:
   - **Mine, small** (a commit, a push, a status line, a question the files answer): tie it off here and say what
     was done.
   - **Mine, bigger**: a settled plan never built goes to `goforit`; other work to `dealers-choice`.
   - **An unratified ADR or its open asks**, or **an ADR candidate left open**: offer `makeadr`.
   - **Yours**: ask them as a numbered list, the recommended answer first, ready to answer in one reply. Write each
     answer where its item lives (the status line, the record, or an ADR amendment through `makeadr`).
6. **Write it down, for a chat only.** A chat's loose ends exist nowhere else, so write them to
   `<looseends_dir>/<date>-<topic>.md`: one checkbox each, grouped as in step 4, ticked as each is tied off. Land
   it by `land`: `commit` (the default; on a branch, never the main branch), `pr`, or `file`. A project or topic
   list stays in the chat, since every item already has a home; offer once to save it.

## looseends decisions: past decisions no ADR covers

"looseends decisions" and "adrorphans" (orphaned decisions, the owner's word) start the same sweep (ADR-038). It
finds decisions already made that no ADR covers and no record listed as an ADR candidate, and offers `makeadr` for
the ones the user picks. It runs only for those words: plain "looseends project" never runs it, and nothing offers
it.

1. **The window.** Since the last sweep: the stamp in the ledger, `<looseends_dir>/adrorphans.md` (step 7). With
   no ledger yet, ask for a start date first. A date after the word overrides the stamp for this run ("adrorphans
   since 2026-10-01"). A record is in the window when the date in its name is on or after the start; a file with
   no date in its name (the status log, a proposal) when `git blame` dates the line on or after it.
2. **Gather.** Fetch, then run `scripts/looseends-scan.py --markers <file> --no-git`, where the file is
   `references/decisions-markers.txt` unless `looseends_decisions_markers` names another. It lists the likely
   spots with `file:line`: bbq records' answers, rows marked agreed in talk-through and townhall records,
   Defaulted rows, and the status log's rulings. Add the bodies of PRs merged in the window (`gh pr list --state
   merged --search "merged:>=<date>"`, then `gh pr view`), and the ledger's *Waiting* list. Read commit messages
   only when the user asks for them ("adrorphans with commits"). In a project with no records of this kind, read
   merged PRs only, and say so. Without the script, read the same places by hand.
3. **Judge each find** against this test, makeadr's, and keep only the ones that pass:

   <!-- adr-sized:begin (a checked copy of makeadr's test, ADR-036: change it there first) -->
   **Is it ADR-sized?** An answer or a call is ADR-sized when it will still bind a later session **and** at least one
   of these holds: (1) it chose between two or more options that each had merit; (2) it fixes something other work
   will build on (a file format, a folder layout, a dependency, where data lives, a name others will call); (3) it
   sets a standing rule ("from now on", "always", "never"); (4) it overrules the recommendation; (5) it touches,
   narrows or reverses an existing ADR. Not ADR-sized: a mechanism with one plain answer; a choice that only shapes
   this run (its order, its budget, who leads).
   <!-- adr-sized:end -->

   The session's own model judges. A big first sweep may go to workers (`tier-select` picks them); the lead
   re-judges every find they send back.
4. **Drop what is covered**: an ADR cites its record or question, or plainly says the same thing; a record already
   lists it as an ADR candidate (an open one is the project scope's to find, ADR-036) or marks it "not an ADR, by
   the user"; or the ledger lists it as skipped. A skipped find is never offered again.
5. **Strongest first, about 10.** Those that touch an existing ADR (sign 5) first, then those with the most signs.
   List each under **Yours**, in one line: where it came from (`file:line` or the PR), what was decided, and the
   signs it showed. Count the rest by record ("23 more: 9 in the stew bbq, 14 in the status log"); they wait for
   the next run (step 7).
6. **Offer once.** Offer `makeadr` once, for the ones the user picks; each takes makeadr's light route, written
   from its cited source. A find the user turns down is skipped; one left unanswered goes back on *Waiting*. Never
   write or draft an ADR unasked.
7. **The ledger**, `<looseends_dir>/adrorphans.md`, one file, landed by `land` as step 6 lands a chat's record:
   - **The stamp**, `Swept to: <date>`. A run whose window started at or before the stamp moves it to today; one
     that started after it (a later date given) leaves it where it was, so no stretch is skipped.
   - **Skipped**: every find the user skipped, with its source and "not an ADR, by the user".
   - **Waiting**: the finds that passed the test but were past the run's ten or left unanswered, each with its
     source, so a moved stamp does not lose them. The next run reads them first and takes each off once it is shown.

   Plain lines, never `- [ ]` boxes, so the project scope does not read them as open. Old records and merged PRs
   are never edited.

## treslooseends: across the projects named

The project scope, run in each project named with the word ("treslooseends pitmaster and maplesyrup os"). It
widens where the skill looks, never what it may do (ADR-023 rules 7 and 8).

1. **Resolve the names** to folders (a `projects:` line in `pitmaster.md`, otherwise the folders the user keeps
   projects in and their git remotes) and say each in one line; a name that matches none, or two, is asked.
   **None named:** list the projects you would check and wait for one yes. **One project:** it is `looseends
   project`.
2. **Gather and check** in each project as steps 2 and 3 do, reading each project's own markers and config.
3. **List them under each project**, then by who acts within it, with the counts per project and in all.
4. **Tie off** as step 5 does, in the project each item lives in, under that project's own rules. A project not
   named is never touched; one that turns out to matter is asked first.

## looseendsreally: tie off its own share

"-really" means all the way through (ADR-023 rule 11). Never past a safety stop: ratify, taste, public acts, pushing to main, deleting work. After the list (step 4), tie off every item under
**Mine** without asking: the small ones here, a settled plan through `goforit`, and merge each PR it opens once the
checks are green. **Yours** are still asked, as step 5 asks them. It works with any scope, and with tres-
("treslooseendsreally" across the projects named). In the decisions scope it never writes an ADR: it lists and
offers, as plain looseends does (ADR-038).

**Only when asked.** This skill never offers itself, and plain `looseends project` never runs the decisions
sweep.

**Never** answer or rule for the user (taste, naming, direction, ratifying); edit ruled ADR text; delete a branch,
close a PR, drop a stash or throw away work; mark anything done without evidence; push to the main branch.

## Platform notes

- **Claude Code:** step 1's question and step 5's list for the user go through `AskUserQuestion` (up to four at a
  time). git finds unlanded work; `gh`, or the GitHub tools in a cloud session, finds open PRs, checks and review
  threads. `scripts/looseends-scan.py` needs Python 3.8 or later.
- **Cowork / claude.ai:** usually no git or shell. A chat works fully; a project or topic reads the files the user
  attached or a connected repository, and says what it could not see. The decisions scope reads the records it
  is given and says it could not see merged PRs. A chat's record is given as a file to save.
- **Codex:** ask as a numbered list in one message (or with a question tool, if your Codex has one). git and `gh`
  as in Claude Code.
- **Other tools:** ask as a numbered list in one message. Without git, a chat and whatever files can be read; say
  which sources were missing.
