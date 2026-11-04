---
status: accepted
status-note: — ratified by the owner 2026-10-26
ratified-by: the owner
ratified-on: "2026-10-26"
owner: the owner
kind: process
built: partial
proof: "`skills/catchmeup/SKILL.md`, `skills/catchmeup/scripts/catchmeup-gather.py`, `evals/catchmeup-yes-01/prompt.md`"
owed: the script's shed copy and pin (ADR-012), its own PR in `pitmaster-shed`; the first real runs judged by the owner (A2)
supersedes: nothing
amends: nothing
---
# ADR-028 — catchmeup: tell the user what changed since they last looked

This is the published version of this decision. Some internal details have been left out.

verified the script; Codex (`gpt-6.1-sol`, high effort), which built the script from a written brief

## Decision

pitmaster gains a skill, **catchmeup**, family `records`, that tells the user what changed in a project since they
last looked. The window starts at the date they name, else at the stamp the skill left for them last time, else it
asks. The catch-up has four parts in a fixed order, with what waits on the user last. It reads and
reports; the stamp is its only write. "catchmeupreally" goes all the way through, and an unattended mode
lets a scheduled morning brief run it.

## Context

Drivers:
- Coming back to a project is the moment a person knows least and is asked most (the hand-made catch-up).
- A summary nobody can check is worse than none: every line needs its proof (the reference project's rule).
- One way of summarising, not two: the morning brief and an on-demand catch-up read the same sources.

## The rules

1. **The window**: the user's date wins ("catchmeup since the 22nd"; a bare date is the user's own day); else
   the stamp this skill left for this project and person; else ask once. Never all history. It ends now.
2. **Loading**: "catchmeup", "catchmeup since …", "trescatchmeup", "catchmeupreally" and "catch me up" start
   straight away. "What did I miss?", "what's changed since I last looked?" and "bring me up to speed" load it and
   ask "Catch you up since <date>?" first.
3. **Projects**: the plain word covers this project; "trescatchmeup" covers each project named, under its own
   heading (ADR-023 rules 7 and 8).
4. **The four parts, in order**: what landed, by day and by run, each line naming its commit or pull request;
   how the way of working changed; what is in flight; what waits on the user, last, each ask with its options as
   written. Older asks still open are counted and handed to `looseends project`.
5. **The script**: `scripts/catchmeup-gather.py`, standard-library Python, lists the main branch's
   first-parent commits, the pull requests (through `gh`, where present), the dated log entries as the branch has
   them, and the record files changed in the window; it reads and writes the stamp. A self-test with eight guards.
6. **The stamp**: in the user's home folder by default (`~/.pitmaster/catchmeup.json`, by project and
   person), moved without asking at the end of a catch-up; `stamp: commit` keeps it in
   `docs/catchup/stamps.md` instead, and then a plain run asks before moving it.
7. **Where it lands**: in the chat, with a one-line offer to make it a page.
8. **Unattended**: run by a scheduled task, it asks nothing, writes `<catchup_dir>/<date>.md` and lists what
   waits on the user for when they next look. The task's prompt adds its own checks, such as a build.
9. **-really** (ADR-023 rule 11): writes the catch-up, makes the page, lands the file and merges its own pull
   request on green, and moves the stamp, with no offer between. It stops at every safety stop.
10. **Never**: a line without its proof; acting on a plain catchmeup; answering the user's asks for them,
    under any word or unattended; reading past the window, except a line the window cites.

What it reuses: looseends' self-test pattern and its scope words, bbq's question tool for the one confirming
question, ADR-023's tres- and -really. What is its own: the window and the stamp, the four parts in that order,
and the hand-off of older asks to looseends.

## Alternatives

Each option is priced against the doctrine (function → ours → compatibility).

### Its own skill with a window, a stamp and four parts (chosen: one summary, checkable, wherever the user returns)
- Good: the user's asks arrive last and freshest, with their options, and are never decided for them
- Good: the same skill serves a person sitting down and a scheduled brief
- Bad: one more always-loaded description (705 characters)
- Bad: the stamp lives outside the repository by default, so a cloud session without it must ask
- Doctrine: function first; the window, the stamp and the four parts are ours; the SKILL.md shape is common

### A mode of looseends (not chosen)
- Good: no new description
- Bad: looseends works at any age and lists what is unfinished; a window of what changed is a different question,
  and mixing them breaks the rule that it never reads past the window

### Landed only, asks left to looseends (not chosen)
- Good: shorter
- Bad: the user's asks are the part they most need on coming back

### Always ask for the date, no stamp (not chosen)
- Good: nothing stored
- Bad: a bare "catchmeup" always costs a question; guessing from the user's last ruling can guess wrong (the third
  option, also not chosen)

### Always a page, or always a file in the repository (not chosen)
- Good: nicer to read, or a trace later sessions can see
- Bad: slower and dearer for a read the user often wants in the chat; a file is kept for the unattended and
  -really runs that need one

### A stamp committed by default (not chosen)
- Good: every session and cloud container sees it
- Bad: each catch-up makes a commit; kept as the `stamp: commit` line

### Leave the morning brief separate, or retire it (not chosen)
- Good: no change to a task that runs
- Bad: two summaries of the same sources drift apart; retiring it leaves nothing waiting in the morning

## Consequences

- Good: coming back to a project costs one word, and every line it says can be checked
- Good: a scheduled brief can shrink to "catchmeup since the last brief, unattended" plus its own checks
- Bad: a catch-up is only as good as the project's records; a project with no dated log gets commits and pull
  requests only
- Bad: the stamp in the home folder does not travel to a cloud session, which asks for the date instead
- Commits us to: the script's self-test in `check-all` once it ships; a public copy of this ADR; the shed copy
  (ADR-012)

## History

- 2026-10-26: proposed.
- 2026-10-26: ratified by the owner.
- 2026-11-04: amended.

## Amendment — 2026-11-04, the user

**What changed.** The catch-up grows from four parts to six, in every catchmeup:

1. **Where we left off**, first: a short reminder of what the seven days before the window landed and what was in
   flight when they ended, each line with its proof; and a re-check that it still holds (each pull request merged
   then is still on the main branch and not reverted, and the project's `recheck:` command passes when one is
   named). It reads and runs; it fixes nothing.
2. to 5. What landed, how the way of working changed, in flight, and waiting on the user, as ruled, except
   that waiting on the user is no longer last.
6. **Where to go next**, last: one recommended move with its reason and two runners-up, ranked as
   `dealers-choice` ranks. A pick may name one of the user's asks with its options, never answering it. It is only
   a recommendation: starting it is the user's word, handed to `dealers-choice`, `goforit` or `looseends`.

`catchmeup-gather.py` gains `--until`, so the stretch before the window can be gathered on its own.

**Why.** Coming back to a project needs more than a list of changes: the context of where things stood, a check
that it still holds, and a suggestion of where to start.

**Sections touched.** Decision (four parts become six; waiting on the user is no longer last), the rules (the
catch-up's parts, and the window rule, which now also lets the stretch before the window be read for the
reminder), and Never (it never starts the move it recommends, nor fixes what the re-check finds).
