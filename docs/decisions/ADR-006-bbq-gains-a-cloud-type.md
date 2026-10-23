---
status: accepted
status-note: — ratified by the owner 2026-10-20
owner: the owner
kind: process
built: landed
proof: "`skills/bbq/SKILL.md`, `skills/budget-select/SKILL.md`, `evals/bbq-yes-08/prompt.md`"
supersedes: nothing
amends: nothing
---
# ADR-006 — bbq gains a Cloud type

This is the public copy of a decision I made. I've left out a few internal notes.

## Decision

bbq gains a **Cloud** type for a run led by a session in a cloud container. A Cloud bbq always writes a prompt for a
fresh session, and asks the questions a cloud lead needs: a fixed share in points and the account it starts on, the
relay of leads when the share outgrows one lead's context, how asks reach the owner without blocking, a *Capacity*
section written from the project's cloud rules, a cap on parallel builders in the one shared container, and the
repositories the run may touch. "Away" (the owner unreachable or on a poor link) is a mode, not a type. The
reachability question is asked in a Cloud bbq's first round, and in any bbq where the owner says they are away. It
is not added to every bbq. `budget-select` gains a *No meter* section, and the platform notes say how a successor
starts on each platform.

Four further rules were settled before ratification (amended 2026-10-20):

- **Unanswered asks.** A parked ask still unanswered at hand-off, or at the end of the run, takes its
  recommended option and goes into the hand-off's *Defaulted* list with a `veto:` line. The stream stays parked
  until then, and the user can overrule the default later.
- **Builder cap.** The bbq asks for the cap on parallel builders every time; 3 is the recommended answer.
- **Launch.** Where the platform can start a cloud session, a Cloud bbq offers to launch the lead once the
  record is merged. The user clicks it or pastes the kickoff; it never launches without their yes.
- **Relay length.** A relay has no cap on its number of leads. The share limits it: the chain ends when the
  ledger reaches the share, and each hand-off is logged.

## Context

A first "away cloud bbq" was run on a large project on 2026-10-19, and a Cloud type was ruled provisionally. A cloud
lead lacks things the other types assume: it cannot read the usage meter or list other sessions, its context fills
before a large share is spent, it has no `ssh`, LAN or local models, and it shares one container with its builders.

Drivers:
- Each gap needs a question the other types never ask.
- ADR-001: platform-agnostic, so the successor tool is a tagged note, not a step.
- Doctrine: function first, then ours, then compatibility. The type is original; it is compatible with Overnight's
  shape.

## Alternatives

### A Cloud type, away as a mode (chosen: each gap becomes a question, and away stays reusable)
- Good: one place to find the cloud rules
- Good: away runs of other types still work
- Bad: one more row in the table

### An Overnight run with a note
- Good: no new type
- Bad: the six gaps are left to a note nobody reads; the lead meets them mid-run

### "Away" as the type
- Good: names the owner's situation
- Bad: away runs are not always cloud runs; the name hides where the lead runs

### Ask the reachability question in every bbq (overruled by the owner)
- Good: no run starts without knowing how asks travel
- Bad: the owner ruled it only for Cloud and away runs; most bbqs have the owner present

## Consequences

Easier: a cloud run's prompt carries the same six things every time. Harder: bbq's table and Platform notes grow, and
`budget-select` grows a section. Next: a host-selection skill, when pitmaster gets one, may take over the *Capacity*
section.

## History

- 2026-10-19: proposed.
- 2026-10-20: amended by the owner.
- 2026-10-20: ratified by the owner.
