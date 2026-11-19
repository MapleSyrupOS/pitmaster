---
name: open-items
metadata:
  family: run
description: Keep one living page per project of everything waiting on the user (questions with options, approvals, merges, ratifies, things to look at), so an unattended or long run posts there and keeps working instead of stopping on a question box. The coordinator posts items and passes each answer back to the seat that asked; with no coordinator, the lead does. A pick counts as the user's word and is recorded as a pick, with its time. Use when the user types "open-items", "openitems" or "open items", or says "asks page", "what's waiting on me?" or "put it on the page", and whenever an unattended or long run needs the user. Not for a to-do list in code, GitHub's open issues, or opening a file.
---

# open-items: one page of everything waiting on you

Decided by pitmaster ADR-044.
Each (Qn) below is the question that set the rule, in the bbq record `docs/bbq/2026-11-18-skill-open-items.md`.

Sibling of `carte-blanche` (a coordinator under *Listen to the coordinator*, ADR-042, posts items for its leads
and passes the answers down on its tick), `catchmeup` (shows the page's open count and link under what waits on the
user) and `looseends` (may post the items it finds that wait on the user onto the page) (Q10). `bbq` and `makeadr`
keep their own question rounds in a live chat; only an unattended or long run moves its questions here (Q2).

## Config

Edit these lines here, or put the same lines in a `pitmaster.md` at your project root, which wins. Every line is
optional.

```
name: the user                 # who the page is for ("name: Alex")
fallback_file: docs/open-items.md   # where items go when no live page can be made (Q8)
```

## What goes on the page

Anything waiting on the user (Q6), each as one **item**:

- a **question** with options, the recommended one first and marked so, and an *Other* box for the user's own
  words;
- an **approval**, a **merge** or a **ratify**, with the buttons that answer it;
- a **look**: something made for the user to see, with its link, and a "Seen" button.

Each item carries an id, a title, the question or ask in full, its context, which seat asked, when it opened, its
kind, its options and its status (open or answered). Everything needed to answer is in the item's own words.

## Steps

1. **Find the page, or make it (Q3, Q14).** One page per project, kept for good. Its link lives in `STATUS.md`
   under *Waiting on owner*, so every session finds it. Read the page's answered items before asking anything:
   never ask again what is already answered.
2. **Who posts (Q4).** In a comrun with a coordinator, seats send their items up to it and the coordinator posts
   them. With no coordinator, the lead posts. Workers never post directly.
3. **Post the item (Q14), and keep working.** Never wait on it. Work that needs the answer is parked; everything
   else carries on. In an unattended or long run, an item goes on the page and never into a question box (Q2,
   Q15). A plain live chat keeps its usual questions.
4. **No push (Q11).** Posting sends no notification. The seat names the page and its open count in its own
   reports and digests, and `catchmeup` shows the count (Q10).
5. **Read the answers on each tick or step (Q14).** Pass each new answer to the seat that asked, then mark the item
   answered.
6. **Record it (Q9, Q14).** A pick is the user's word: it counts like an answer in chat, for a merge or a ratify
   too. Write it as a pick with its time, never as the user's own words: "picked (a), open-items, 18:13Z". Only the
   text in the *Other* box is quoted as the user's words.

## Never

- Open a question box mid-run, in an unattended or long run (Q15).
- Re-ask an answered item. Reopening is the user's alone (Q15).
- Delete an item. Answered items stay, folded away, as the record (Q15).

## The file fallback

Where no live page with saved answers can be made, items go in the `fallback_file`, a Markdown file in the
repository, and the user ticks a box beside the option they pick (Q8). The seat reads it on each tick, as it would
the page. `scripts/open-items.py` adds, lists and closes items in that file (Q17):

```
python3 scripts/open-items.py add --title "..." --question "..." --from lead-a --option "..." --option "..."
python3 scripts/open-items.py answered      # items the user has ticked, not yet closed
python3 scripts/open-items.py close OI-003  # mark it answered, with the time it was read
```

`--self-test` runs its own checks, deliberate failures included.

## Platform notes

- **Claude Code:** in the desktop app, the page is an Artifact with the shared database (`db`) capability: collection
  `items` holds the items and `answers` holds `{choice, other, at}` per item id. Post and read with
  `ArtifactData`; the page saves the user's pick and its time. Load the artifact skills before writing the page.
  A coordinator relays an answer to a seat with `SendMessage`.
- **Cowork / claude.ai:** the same Artifact page where artifacts with a database are offered; otherwise the file
  fallback, or the items listed in one message at the end of each step.
- **Codex:** the file fallback; the user ticks boxes in the file, or answers in chat.
- **Other tools:** the file fallback.
