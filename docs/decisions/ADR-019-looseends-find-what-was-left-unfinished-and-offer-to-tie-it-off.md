---
status: accepted
status-note: — ratified by the owner 2026-10-23
owner: the owner
kind: process
built: partial
proof: "`skills/looseends/SKILL.md`"
owed: the first real runs
supersedes: nothing
amends: nothing
---
# ADR-019 — looseends: find what was left unfinished, and offer to tie it off

This is the published version of this decision. Some internal details have been left out.

## Decision

pitmaster gains a skill, **looseends**, that finds what was left unfinished and offers to tie it off. It looks in
one of three scopes: **this chat** ("chat" and "session" are two words for it), **the project**, or **one ADR or
topic**. In that scope only, it gathers four kinds of loose end: questions never answered, promises not kept,
things waiting on the user's ruling, and work never landed. It checks each is still open, lists them by who acts,
and on the user's yes ties off the small ones and hands the rest on. It runs only when asked.

## The rules

> **Amended 2026-10-23 by ADR-023, ratified by the user:** looseendsreally ties off the agent's own loose ends
> without asking; treslooseends checks the projects named (rule 6).

1. **Scope:** the word after the opener sets it: `chat` or `session`, `project`, or anything else as a topic. A
   plain "looseends", or a plainer ask ("what's left hanging?", "what did we leave open?", "what's still open?"),
   loads it and asks one question first: "Check for loose ends? This chat, the project, or a topic?" Words with
   "loose ends" in them ("any loose ends?", "tie up the loose ends") load it outright.
2. **The four kinds, inside the scope only:** questions never answered; promises not kept; things waiting on the
   user's ruling; work never landed.
3. **Where it looks:** a chat reads the conversation and the work it did. A project fetches, runs
   `scripts/looseends-scan.py`, and adds what the scan cannot see (open pull requests, their checks, review
   threads). A topic is the project narrowed to that subject, plus this chat.
4. **The scan:** standard-library Python that lists each marker with `file:line`, runs without an agent, and only
   reads. Its markers are plain text a project can replace. It carries a self-test.
5. **Still open:** each item is checked before it is listed; closed ones are dropped, unchecked ones marked
   *unverified*.
6. **The list and the offer:** grouped yours / mine / waiting on someone else, each with where it came from. On a
   yes: small agent items tied off here; a settled plan never built to `goforit`; other agent work to
   `dealers-choice`; an unratified ADR to `makeadr`; the user's items as a numbered list, recommended answer first.
7. **Where the list goes:** a chat's list is written to `docs/looseends/<date>-<topic>.md` as checkboxes, on a
   branch; a project or topic list stays in the chat with an offer to save, since every item already has a home.
8. **Only when asked:** it never offers itself. A nudge at a session's end is left to an opt-in rule, not to this
   skill.
9. **Never:** rule for the user, edit ruled ADR text, delete a branch, close a pull request, drop a stash, throw
   away work, mark anything done without evidence, or push to the main branch.

## Alternatives

- **Its own skill that finds, checks and offers** (chosen). The user's own loose ends, the ones waiting on a
  ruling, get a home at any size. Cost: one more description always loaded.
- **A mode of a future handoff skill** (not chosen). Nothing would ship now, and a sweep happens at moments other
  than a handoff.
- **List only, read-only** (not chosen). The user would tie off every item by hand, a push the agent could do
  included.
- **Always write a file** (not chosen). A dated copy of project items goes stale the day one is tied off.
- **Offer itself at a session's close** (not chosen). It would stack with other end-of-session offers, and "thanks"
  comes mid-conversation, so the trigger barely filters.

## Consequences

- The user can ask, at any size, what is still open, and get it sorted by who must act; a chat's loose ends reach
  a later session through `docs/looseends/`.
- A project run is only as good as its markers: the scan over-reports and leans on the still-open check.

## History

- 2026-10-23: proposed.
- 2026-10-23: ratified by the owner.
- 2026-10-23: amended.
