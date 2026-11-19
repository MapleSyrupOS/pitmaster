---
status: accepted
status-note: ratified by the owner 2026-11-18
ratified-by: the owner
ratified-on: "2026-11-18"
owner: the owner
kind: process
built: partial
proof: "`skills/open-items/SKILL.md`, `skills/open-items/scripts/open-items.py`, `evals/open-items-yes-01/prompt.md`"
owed: the trigger evals run (step 3); a first real run with a coordinator, judged by the owner (step 5)
supersedes: nothing
amends: nothing
---
# ADR-044 — open-items: one page per project holds everything waiting on the user, so a long run never stops on a question box

This is the published version of this decision. Some internal details have been left out.

(2026-11-17 to 2026-11-18); this session (Opus 5.5), which read the page, ran the skill bbq and wrote this ADR
**Confirmed by:** the skill's trigger evals (six that must load the skill, four that must
not), run three times each before the move; and, as a field test the user judges, the first coordinated comrun
that uses the page: no seat opens a question box, every answer reaches the seat that asked, and every record quotes
picks as picks
**Revisit when:** the platform's question box stops blocking a session that is left unattended (a timeout, or a
reply from another device); or Artifacts lose the shared database, which would leave only the file fallback

## Decision

A new skill, **open-items** (family `run`), keeps one living page per project of everything waiting on the user.
An unattended or long run posts its questions there and keeps working, instead of stopping on a question box.

1. **When**. Any unattended or long run (a comrun, a coordinator, a lead that must not stall on the user)
   puts what it needs from the user on the page, and never opens a question box mid-run. A plain live chat
   keeps its usual questions; bbq and makeadr rounds asked live are unchanged.
2. **One page per project, kept for good**. Its link lives in `STATUS.md` under *Waiting on owner*, so any
   session finds it.
3. **What goes on it: anything waiting on the user**: questions with options (the recommended one first,
   and an *Other* box), approvals, merges, ratifies, and things to look at. Each item says everything needed to
   answer it in its own words.
4. **Who posts**. The coordinator, when the comrun has one: seats send their items up, and the coordinator
   posts them and passes each answer back to the seat that asked, on its tick (ADR-042's coordinator). With no
   coordinator, the lead does both. Workers never post directly.
5. **A pick is the user's word**. It counts like an answer in chat, a merge and a ratify included, and is
   recorded as a pick with its time: "picked (a), open-items, 18:13Z". Only what the user writes in the *Other*
   box is quoted as the user's own words.
6. **No push** (overruled the recommendation). Posting sends no notification. The seat names the page and its
   open count in its own reports, and catchmeup shows the count.
7. **The page is the one list**. catchmeup shows its open count and link under what waits on the user;
   looseends may post the items it finds onto it.
8. **Never**: open a question box mid-run in an unattended or long run; ask again what the page already
   answers (reopening is the user's alone); delete an item (answered items stay, folded away, as the record).
9. **Where no live page can be made**: the items go in a file in the repository
   (`docs/open-items.md` by default), and the user ticks the box beside the option they pick. The skill ships
   `scripts/open-items.py`, which adds, lists, reads ticks and closes items there, with a self-test in check-all.
   No page template ships.

## Context

Drivers:
- A run left alone must never stall on the user.
- Every answer must reach the seat that asked, and be quoted honestly in the records.
- One place to look for everything waiting on the user.
- Works, more plainly, where no live page can be made.

## Alternatives

### Unattended or long runs use the page (chosen: stalls only hurt runs left alone, and live chats keep their boxes)
- Good: fixes the case that froze a coordinator; nothing changes for live chats or for bbq and makeadr rounds.
- Bad: two ways to ask, so a seat must know which kind of run it is in.

### Coordinators only
- Good: the smallest change; only ADR-042's tick uses it.
- Bad: a lead with no coordinator can still stall, as the reference project's leads could.

### Every pitmaster skill asks on the page
- Good: one way to ask, everywhere.
- Bad: a live chat answered in seconds would wait on a page instead; bbq's rounds would slow down for nothing.

### One page per comrun or per session
- Good: tidier pages.
- Bad: a new link every time, so the user hunts for where the questions are; the reference project kept one page
  across three coordinators.

### Every seat posts its own items
- Good: no relay to drop an answer.
- Bad: many writers on one page, and answers no one tracks back to the comrun's plan.

### Questions only
- Good: a simpler page, as the reference project's was.
- Bad: approvals, merges and things to look at stay scattered across chats.

### One push when an item opens, then batched: the recommendation, overruled
- Good: the user hears at once that something waits; the reference project's coordinators sent one.
- Bad: the user chose no push.

### A pick counts for all but ratify
- Good: ratifying stays a typed word in chat.
- Bad: a ratify would still stall a run left alone.

## Consequences

- A run left alone posts and keeps working; the user answers when they look, on a phone or a desktop.
- The user has one page per project to check, and no notification tells them to; catchmeup and the seats'
  reports carry the count.
- Records quote a pick as a pick, with its time; the user's own words come only from the *Other* box.
- The skill adds one always-loaded description (692 characters).
- Two ways to ask now exist; each skill's platform notes that name the question tool still hold for live chats.

**Steps to build:**
1. The draft, its script with a self-test (15 checks, deliberate failures included) and its ten trigger evals —
   done. Test: `python3 skills/open-items/scripts/open-items.py --self-test` in check-all.
2. The pointer lines in carte-blanche, catchmeup and looseends; done. Test: check-all's skill spec.
3. Run the trigger evals, three runs each. Test: ten of ten cases pass.
4. After ratify, the move into `skills/` (offered, not made; ADR-026), the patch bump and a CHANGELOG line. Test:
   check-all, and `publish.py --dry-run` once this ADR's public copy is approved.
5. A first coordinated comrun that uses the page, written up as a field report. Test: the user's judgement.

## Asks left open

None from the bbq. To veto, if any: the four defaults in the record's *Defaulted* list (the collections named
`items` and `answers`, a "Seen" button for looks, workers never posting, the pointer lines landing now), and the
default above that a ratify picked on the page counts when the ratifying session reads it from the page itself.

## History

- 2026-11-18: proposed.
- 2026-11-18: ratified by the owner.
