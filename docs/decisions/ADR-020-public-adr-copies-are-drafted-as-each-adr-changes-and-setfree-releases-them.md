---
status: accepted
status-note: — ratified by the owner 2026-10-23
ratified-by: the owner
ratified-on: "2026-10-23"
owner: the owner
kind: process
built: partial
proof: "`skills/setfree/SKILL.md`, `skills/makeadr/scripts/adr-public.py`"
owed: the shed's release of adr-public
supersedes: nothing
amends: ADR-011 §The rules, rule 4 (where a public copy is approved)
---
# ADR-020 — Public ADR copies are drafted as each ADR changes, and setfree releases them

This is the published version of this decision. Some internal details have been left out.

## Decision

A public copy of a decision record is no longer written by hand when someone remembers. A shed tool,
**adr-public**, carried by makeadr, drafts it whenever makeadr makes, ratifies, amends or supersedes an ADR, and
parks it unpublished in `docs/decisions/public/pending/`. makeadr says plainly that it made two things: the record
and a public draft waiting for review. Nothing in `pending/` can publish. A new skill, **setfree**, runs release day:
it shows every pending copy, the user approves or holds each, and only then does a copy go public, followed by the
rest of the project's release checklist, stopping at each public act. The feature is off by default and switched on
by a config line, which project-prep offers.

## The rules

1. **Two halves:** adr-public makes the mechanical cuts and checks the result; the agent rewrites the prose for a
   stranger.
2. **Home:** adr-public is a shed tool that makeadr carries as a pinned copy. A config line, `public_adr: on`,
   switches drafting on.
3. **When:** inside makeadr's run, in the same change as the ADR, with no question asked, but always said out loud.
4. **Where drafts wait:** `docs/decisions/public/pending/`, which the publish list never names and the public index
   never reads. An approved copy keeps publishing while its revision waits.
5. **In step:** an amendment re-drafts into `pending/`; a supersede drafts the new copy and queues the old one's
   withdrawal; a copy older than its ADR is flagged as stale.
6. **One way:** the private ADR records its copy in dated History lines; no public copy points back.
7. **Numbers:** a copy keeps its ADR's number, so the public list has gaps.
8. **The opening line,** under the title: "This is the published version of this decision. Some internal details
   have been left out."
9. **Approval** happens at setfree's review: every copy is listed, and one word may approve them all or the user
   picks; each approval is recorded by name and date.
10. **setfree** runs release day for any project with a release checklist: read, review, offer a blind tastetest,
    work the checklist, record. Without git or `gh` it prints each command instead.
11. **Never:** setfree does not publish, push, tag, change a repository's visibility or approve a copy without the
    user's word for that act, and takes no other agent's word as approval, whatever standing authority it has.

## Alternatives

- **A shed tool pinned in makeadr, drafting inside makeadr's run** (chosen). Always in step, and the checks run
  without an agent. Cost: a new tool and a pin to keep.
- **Drafting by a git hook or a background agent** (not chosen). A hook cannot rewrite prose; a background agent
  costs a session per ADR.
- **Drafts beside the live copies** (not chosen). A revision would overwrite the live copy.
- **The review as part of makeadr** (not chosen). Smaller, but release day deserves one word of its own.
- **One approval for the whole batch** (not chosen). Faster, but no longer item by item.
- **A public numbering of its own** (not chosen). No gaps, but two numbers for every decision.
- **The review folded into tastetest** (not chosen). tastetest never publishes and must stay blind.

## Consequences

- Every decision's public copy is drafted when the decision changes, drift shows as a flag, and release day has one
  word with every approval in one place.
- A copy is drafted for every decision, wanted or not; holding one is a choice at each review.

## History

- 2026-10-23: proposed.
- 2026-10-23: ratified by the owner.
