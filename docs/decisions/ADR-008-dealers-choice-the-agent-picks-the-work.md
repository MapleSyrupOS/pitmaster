---
status: accepted
status-note: — ratified by the owner 2026-10-20
owner: the owner
kind: process
built: landed
proof: "`skills/dealers-choice/SKILL.md`"
supersedes: nothing
amends: nothing
---
# ADR-008 — dealers-choice: the agent picks the work, after four questions

This is the public copy of a decision I made. I've left out a few internal notes.

## Decision

pitmaster gains a skill, **dealers-choice**, in which the agent picks what to work on with little more guidance
from the owner. It asks four questions and then starts: is this carte blanche; how much usage, whether a swarm is
allowed and on which machines (amended 2026-10-21); is anywhere off-limits; who leads. It asks more than four only
if it cannot start without the answer or the owner asks. It picks the work only. What may be done without asking
comes from carte-blanche (ADR-007) or the run's own rules, so it sits on top of a plain session, a bbq, a Cloud
run or a carte blanche run.

## The rules

1. **Triggers:** `dealer's choice` or `dealers choice` loads it. A plainer ask loads it and is confirmed first, so
   an offhand `you pick` cannot start a run.
2. **The four questions:** carte blanche (yes or no, plus any extra grants); usage, swarm and, for a swarm, which
   build or test machines it may use and how many jobs each takes (amended 2026-10-21); off-limits; who leads. A
   question the request already answered is skipped. If the lead named is not this session's model and
   effort, the run is written as a prompt for a fresh session.
3. **The kind of run:** a plain session, with bbq (it picks the topic, then bbq asks), with Cloud (it picks, then
   writes a Cloud-type prompt), or with carte blanche.
4. **Sources:** the status file's next and in-progress items, the debt list, open PRs and review findings, queued
   prompts and proposals (work taken from a proposal stays a draft). In a bare project: README, issues, TODO and
   FIXME, failing checks, git log. A list too long to read whole is split into slices for small, cheap readers,
   each returning one line per candidate; the lead ranks the lines (amended 2026-10-21).
5. **Ranking:** work that unblocks other work first, then value per point. Before a pick goes to a worker, a cheap
   look at the main branch confirms it is still open; an entry found paid, superseded or retired is marked so and
   the next pick goes out (amended 2026-10-21). Visual taste calls are handled as carte-blanche does.
6. **Running:** announce the pick in one line and start without waiting; keep picking; park any pick that needs a
   real decision and file its questions.
7. **Swarms:** `tier-select` decides who does each job, local models included, and no worker has more authority
   than the lead. Picks that touch the same files or the same check go to one worker, in order, so one landing
   does not leave its siblings each needing a merge (amended 2026-10-21).
8. **Nothing worth doing:** housekeeping, then a short draft proposal of what to do next.
9. **End report:** a dated log entry, the status file updated, the short version as a message or a notification, and
   any taste frames sent.

## Alternatives

- **Picks the work only; authority comes from the run** (chosen). One skill sits on top of any kind of run, and
  the authority rules live in one place. Cost: a plain run still asks before anything leaves the machine, which can
  stall an unattended run.
- **dealers-choice sets its own authority** (not chosen). One skill to remember, but two places would say what an
  agent may do.
- **Agent decides, owner vetoes, as the purpose** (overruled). It would settle open questions as well as pick work,
  but deciding with a veto is carte-blanche's trail, not this skill's job.
- **Stop and report when nothing is worth doing** (overruled). Spends nothing, but wastes a run meant to be
  useful; housekeeping and a draft proposal are cheap.
- **Local lanes first, then Claude** (overruled). Saves points by standing rule, but `tier-select` should choose
  each time, lanes included.
- **Plain asks load it with no confirmation** (overruled). One step fewer, but an offhand ask could start a run.

## Consequences

- A run starts with four answers and keeps itself fed, and it works in projects with none of pitmaster's files.
- The ranking is the agent's judgment, so a wrong pick costs points before the owner sees it.
- Commits us to keeping the source list in step with where pitmaster projects keep next work, and the starting
  questions at four.

## History

- 2026-10-20: proposed.
- 2026-10-20: ratified by the owner.
- 2026-10-21: amended by the owner.
