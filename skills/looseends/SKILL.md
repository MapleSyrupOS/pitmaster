---
name: looseends
metadata:
  family: check
description: Find what was left unfinished in this chat, across the whole project, or around one ADR or topic - questions never answered, promises not kept, things waiting on the user's ruling, work never landed - check each is still open, list them by who acts, and offer to tie them off. Use when the user types "looseends", "looseends chat", "looseends session", "looseends project" or "looseends" followed by an ADR or a topic, or "treslooseends" followed by the projects to check (every project named, each by name), or "looseendsreally" (ties off its own share without asking), or asks "any loose ends?", "tie up the loose ends" or "what loose ends are left". Plainer asks such as "what's left hanging?", "what did we leave open?" or "what's still open?" also load it, and it first asks "Check for loose ends? This chat, the project, or a topic?"
---

# looseends: find what was left unfinished, and offer to tie it off

Decided by pitmaster ADR-019.
"treslooseends" and "looseendsreally": ADR-023.

Sibling of `goforit` (a settled plan that was never built), `dealers-choice` (takes the bigger work that is the
agent's), `makeadr` (an unratified ADR, or one with asks left open) and `bbq` and `talk-through` (their records'
Owed lists, calls open to veto and open questions are loose ends this skill reads).

## Config

Edit these lines here, or put the same lines in a `pitmaster.md` at your project root, which wins. Every line is
optional.

```
name: the user                   # who the skill speaks to; "name: Alex" makes it say "Alex"
looseends_dir: docs/looseends    # where a chat's loose ends are written: <looseends_dir>/<date>-<topic>.md
looseends_markers: default       # what the scan looks for: default, or a file in the scan's marker format
land: commit                     # commit (branch only) | pr (branch + PR) | file (just the file) (step 6)
```

## Steps

1. **Which scope.** The word after the opener sets it: `chat` or `session` (two words for one thing: this
   conversation), `project` (the whole repository), or anything else as a topic (an ADR number, a skill, a
   subject). A plain "looseends", or a plainer ask that loaded this skill, asks one question first: "Check for
   loose ends? This chat, the project, or a topic?" Stop on a no.
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
     in earlier looseends records, and git's unlanded work. Add what it cannot see: open PRs, their checks, and
     review comments waiting for an answer. Without the script, read the same places by hand.
   - **topic**: the project's sources narrowed to that subject (`--topic`), plus anything said about it in this
     chat.
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
   - **An unratified ADR or its open asks**: offer `makeadr`.
   - **Yours**: ask them as a numbered list, the recommended answer first, ready to answer in one reply. Write each
     answer where its item lives (the status line, the record, or an ADR amendment through `makeadr`).
6. **Write it down, for a chat only.** A chat's loose ends exist nowhere else, so write them to
   `<looseends_dir>/<date>-<topic>.md`: one checkbox each, grouped as in step 4, ticked as each is tied off. Land
   it by `land`: `commit` (the default; on a branch, never the main branch), `pr`, or `file`. A project or topic
   list stays in the chat, since every item already has a home; offer once to save it.

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
("treslooseendsreally" across the projects named).

**Only when asked.** This skill never offers itself.

**Never** answer or rule for the user (taste, naming, direction, ratifying); edit ruled ADR text; delete a branch,
close a PR, drop a stash or throw away work; mark anything done without evidence; push to the main branch.

## Platform notes

- **Claude Code:** step 1's question and step 5's list for the user go through `AskUserQuestion` (up to four at a
  time). git finds unlanded work; `gh`, or the GitHub tools in a cloud session, finds open PRs, checks and review
  threads. `scripts/looseends-scan.py` needs Python 3.8 or later.
- **Cowork / claude.ai:** usually no git or shell. A chat works fully; a project or topic reads the files the user
  attached or a connected repository, and says what it could not see. A chat's record is given as a file to save.
- **Codex:** ask as a numbered list in one message (or with a question tool, if your Codex has one). git and `gh`
  as in Claude Code.
- **Other tools:** ask as a numbered list in one message. Without git, a chat and whatever files can be read; say
  which sources were missing.
