---
status: accepted
status-note: — ratified by the owner 2026-10-22
owner: the owner
kind: process
built: partial
proof: "`skills/tastetest/SKILL.md`"
owed: the first real runs
supersedes: nothing
amends: nothing
---
# ADR-016 — tastetest: a blind audit of whether a thing is ready for its end users

This is the public copy of a decision I made. I've left out a few internal notes.

## Decision

pitmaster gains a skill, **tastetest**, that audits whether something is ready for the public the way an end user
would meet it. A **blind auditor**, one that knows nothing about the project, gets a copy of only what an outsider
would see, tries it, and hands back a report: **READY** or **NOT READY** at the top, then findings ranked blocks,
should fix and nice, each cited. It checks that a fresh install works, that a newcomer can read it, that nothing
private leaks, that its claims match what ships, and, for an app, what Apple requires. The verdict informs the
user's word to go live and never replaces it.

## The rules

1. **Triggers:** `tastetest`, or a readiness ask: "is this ready to go public", "public readiness audit", "is it
   App Store ready", "audit this before launch". Near-misses: a code review, a security review, "is it done?", a
   leak check on its own.
2. **Profiles:** one per target, picked by reading the project and said in one line; `repo` and `app-store` ship
   now. A new profile is a dated checklist added by a plain change; a project may keep its own.
3. **Apple's rules:** the `app-store` profile is dated, and each run reads Apple's current guidelines and reports
   anything new, changed or gone as checklist drift.
4. **The blind copy:** `scripts/blind-copy.py` copies only the files git tracks, or only those a publish list
   names, with no history.
5. **The auditor:** a fresh subagent with a sealed prompt. Without subagents, both routes (here, or a prompt for
   a fresh session) are always offered, and context used changes only which is recommended.
6. **Hands:** look and try inside the copy; `tastetest readonly` reads only. It never edits the project,
   submits, uploads, publishes or pushes.
7. **Not blind:** a run in the same session may still say READY, labelled "Not a blind audit".
8. **The report** goes to `docs/audits/<date>-<profile>.md` on a branch, never the main branch; any *blocks*
   finding means NOT READY.
9. **Other families:** `tastetest neighbourhood` adds auditors from other model families once that skill exists.

## Alternatives

- **A blind auditor with profiles and a verdict the user weighs** (chosen). A stranger's eyes, and the user keeps
  the word. Cost: a fresh agent's context per run, and a live check to keep the App Store list true.
- **The working session audits by checklist** (not chosen). Cheapest, but it already knows the project; kept only
  as a labelled fallback.
- **A hard gate that stops publishing until READY** (not chosen). Going public would become a checklist's call.
- **One universal checklist** (not chosen). App Store checks are noise on a repository, and the reverse.
- **No READY without a blind auditor** (not chosen). A project with no subagents could never get one.

## Consequences

- A repository or an app gets the same stranger's-eye check before it goes out, with a record on a branch, and
  Apple's changes show up as drift.
- A blind run is the most expensive way to audit; the not-blind fallback is weaker and says so.

## History

- 2026-10-22: proposed.
- 2026-10-22: ratified by the owner.
