---
name: catchmeup
metadata:
  family: records
description: Tell the user what changed in a project since they last looked - where they left off (re-checked), what landed (by day and by run, each line citing its commit or PR), how the way of working changed, what is in flight, what waits on them, and last one recommended next move - from a date they name or the stamp it left last time. Use when the user types "catchmeup" or "catchmeup since" a date, "trescatchmeup" followed by the projects to cover, or "catchmeupreally" (also lands the catch-up and moves the stamp without asking), or says "catch me up". Plainer asks such as "what did I miss?", "what's changed since I last looked?" or "bring me up to speed" also load it, and it first asks "Catch you up since <date>?". A scheduled morning brief can run it unattended.
---

# catchmeup: what changed since you last looked

Decided by pitmaster ADR-028.
Its amendment of 2026-11-04 (A1–A4) adds where we left off, and where to go next.
Each (Qn) below is the question that settled the rule in the session ADR-028 was made from; each (An), the
amendment's.

Sibling of `looseends` (catchmeup looks at what changed inside a window; looseends looks for what was left
unfinished at any age, so the older items still waiting on the user are counted here and handed to
`looseends project`) and of `dealers-choice` (whose ranking picks the next move here; catchmeup only recommends it,
and never starts it).

## Config

Edit these lines here, or put the same lines in a `pitmaster.md` at your project root, which wins. Every line is
optional.

```
name: the user                 # who is caught up; also the stamp's key ("name: Alex")
stamp: home                    # home (~/.pitmaster/catchmeup.json) | commit (docs/catchup/stamps.md)
catchup_dir: docs/catchup      # where an unattended run and catchmeupreally write the catch-up
logs: docs/STATUS-log.md       # dated logs whose entries in the window are read
waiting: STATUS.md             # where the user's open asks are listed (a file, or several, comma-separated)
land: pr                       # pr (branch + PR) | commit (branch only) | file (just the file), for a written catch-up
recheck: none                  # a command that checks the project still holds (its tests or checks), run once for
                               # "where we left off"; none = only the merge check (step 3)
```

## Steps

1. **The window and the person.** The window starts at the date the user named ("catchmeup since the 22nd"). With
   none, it starts at the stamp this skill left for this project and this person last time. With neither, ask for
   a date once; never fall back to "all history" (Q3). The window ends now.
   - The opener word starts straight away. A plainer ask that loaded this skill asks one question first: "Catch
     you up since <the stamp's date>?" (or "since when?" with no stamp). Stop on a no (Q8).
   - "trescatchmeup" followed by projects covers each one named, under its own heading. Each name is resolved to
     a folder by looking (a `projects:` line in `pitmaster.md`, or the folders the user keeps projects in), said
     in one line; a name that matches none or two is asked (Q4; ADR-023 rules 7 and 8).
2. **Gather, inside the window only.** Run `scripts/catchmeup-gather.py gather` (with `--since` when the user named
   a date, and `--log` for each file in `logs:`). It lists the main branch's commits, the pull requests merged and
   the ones still open that moved, the log entries dated in the window, and the record files that changed. Then
   read, still inside the window: each listed log entry, the `waiting:` file, and each open pull request's first
   paragraph. A line from before the window is read only when a line inside it cites it (Q11), or for the
   stretch below.
   - **The stretch before the window** (A1): run the script again with `--since` seven days before the window's
     start and `--until` the start. These lines feed "Where we left off" only; they are never listed as landed.
3. **Write the catch-up**, in six parts, in this order (Q2; A1, A3):
   - **Where we left off** (A1): two parts, a few lines in all.
     - **A reminder**: what the stretch before the window landed and what was in flight when it ended, so the
       context comes back. Each line names its proof, as for what landed.
     - **A re-check** that it still holds: each pull request merged in that stretch is still on the main branch
       and no later commit reverts it; and, when `recheck:` names a command, that command passes (run once). Say
       "still holds" in one line, or list what does not, with its proof. It reads and runs; it fixes nothing.
   - **What landed**, grouped by day, and by run where the log names runs: one line each, plain words first, the
     commit or pull request at the end. Every line names its proof; a count comes from the script or a command,
     never from a summary (Q11).
   - **How the way of working changed**: rulings made, decisions ratified or amended, routing and tooling changes,
     new skills or rules. Only the ones dated in the window.
   - **In flight**: open pull requests and running work that moved in the window, one line each.
   - **Waiting on the user**, so it is fresh: each ask filed in the window, with its options as written, never
     decided for them (Q11). Older asks still open are not listed; give their count in one line and point at
     `looseends project`.
   - **Where to go next**, last (A2, A3): one recommended move with its reason, then two runners-up in a line
     each. Rank the candidates (the asks waiting on the user, the work in flight, the debt list, the status file's
     next steps, and anything the re-check found) as `dealers-choice` ranks: what unblocks the most first, then
     what gives the most for the effort. A pick may be one of the user's asks ("rule ADR-30 first: it unblocks
     #115 and #118"); name it with its options, and never answer it. Only recommend: starting it is the user's
     word, which hands it to `dealers-choice`, `goforit` or `looseends`.

   Short sentences, the user's project's own words, no padding. A heading per part; drop a part that is empty and
   say so in one line.
4. **Where it lands.** In the chat, and close with one line offering to make it a page (Q5). A written catch-up
   (step 6, or catchmeupreally) goes to `<catchup_dir>/<date>.md` and lands by `land:`.
5. **Move the stamp** to the window's end once the catch-up is given: `scripts/catchmeup-gather.py stamp --set now`.
   With `stamp: home` this is the skill's own bookkeeping outside the repository, and it is done without asking.
   With `stamp: commit` it is a commit, so ask "Move your stamp? (one line in docs/catchup/stamps.md)" (Q10).
6. **Unattended** (a scheduled task, such as a morning brief, with no one there): the window starts at the stamp of
   the person the task names (or the newest file in `catchup_dir`), nothing is asked, the catch-up is written to
   `<catchup_dir>/<date>.md` and given as the reply, and anything waiting on the user is listed with its options
   for the next time they look. It has all six parts; the next move stays a recommendation. The task's own prompt adds whatever else it checks, such as a build (Q7).
7. **catchmeupreally** goes all the way through (ADR-023 rule 11; Q6): it writes the catch-up to `catchup_dir`,
   makes the page, lands the file and merges its own pull request once the checks are green, and moves the stamp,
   with no offer in between. It still asks every question that is the user's, and stops at every safety stop.

## Never

- Claim a line without its proof: every "landed" line names its commit or pull request (Q11).
- Act on a plain catchmeup: it reads and reports, and the stamp is its only write. Merging, closing pull requests,
  draining lists and filing debt are not its work; catchmeupreally lands only its own catch-up (Q11).
- Answer the user's asks for them, under any word or in an unattended run (Q11; ADR-023 rule 10).
- Read past the window, except a line the window cites (Q11) and the stretch before it, for "Where we left off"
  (A1).
- Start the next move it recommends, or fix what the re-check finds (A2).

## The script

`scripts/catchmeup-gather.py` is a pinned copy of pitmaster-shed's `catchmeup-gather` tool
(`scripts/catchmeup-gather.pin`); never edit it here. A change goes to the tool in the shed and is copied back byte
for byte with a new pin. Standard library only, Python 3.8 or newer.

## Platform notes

- **Claude Code:** the plain ask's confirming question goes through the question tool. `gh` reads the pull
  requests; without it the script says so in one line and the catch-up says the pull requests were not read. A
  page is an artifact where the session can publish one. A scheduled task (the desktop app's or a cloud routine)
  runs step 6 with its prompt naming "catchmeup since the last brief, unattended".
- **Cowork / claude.ai:** usually no git, no shell and no home folder that lasts, so there is no script and no
  stamp: ask for the date, and gather from what the user pastes or names, the project's files in the session, and
  any connected source. Say which of the six parts could not be read.
- **Codex:** ask the confirming question as a plain line and wait. The script runs as it does in Claude Code; `gh`
  where it is signed in.
- **Other tools:** ask the confirming question as a plain line. Run the script where there is a shell and git;
  otherwise do as Cowork does.
