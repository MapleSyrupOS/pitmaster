---
name: dealers-choice
metadata:
  family: run
description: The agent picks what to work on, and starts. Use when the user says "dealer's choice" or "dealers choice", or either followed by a topic ("dealer's choice docs") ("tresdealers-choice": across the projects named), or leaves the choice of work to the agent and says to start, however it is worded and even when it names the repository: "you pick what to work on next and do it", "pick something worth doing and get going", "what's most worth doing? go". Load it first, before looking around or reading any file: its own steps do that reading. A plainer ask is checked with "Dealer's choice?". An ask only to recommend ("just tell me") does not load it. After four quick questions it reads the project's status, debt and open PRs, picks what unblocks the most and then what gives the most per point, and keeps picking until the budget stop or until nothing worthwhile is left. It picks the work only; what may be done without asking comes from carte-blanche or the rules of the voyage (also called a runlap).
---

# dealers-choice: the agent picks the work

Decided by pitmaster ADR-008.
"tresdealers-choice": ADR-023.

Sibling of `carte-blanche` (question 1 asks whether it is granted), `budget-select` (how much usage), `tier-select`
(who leads and who does each job) and `bbq` (which can run on the picked topic). `looseends` hands it the bigger
loose ends that are the agent's, and finds the ones waiting on the user's ruling, which step 4 leaves out.

**The smallest voyage** skips every question the user's words answered, picks, works and writes the end report. A
swarm (several workers at once) is for bigger voyages.

## Config

Edit these lines here, or put the same lines in a `pitmaster.md` at your project root, which wins. Every line is
optional.

```
name: the user      # who is asked. "name: Alex" makes this skill say "Alex".
questions: 4        # the starting questions (step 2)
status: auto        # the status file: auto finds STATUS.md or docs/STATUS.md
log: auto           # where the end report goes: auto finds docs/STATUS-log.md or STATUS-log.md
sources: auto       # extra places to look for work, comma-separated, added to the list in step 4
```

## Steps

1. **Confirm, if needed.** After "dealer's choice" (or "dealers choice"), go on. If a plainer ask loaded this
   skill, first ask "Dealer's choice? I pick what to work on." Stop on a no.
   - **A topic.** Words after the opener that are not an answer to step 2 (a budget, "carte blanche", a model)
     name a topic: "dealer's choice docs", "dealer's choice the build". Say it back in one line ("Picking within
     the docs"); step 4 then gathers only candidates about it.
2. **Four questions, in one round**, skipping any the user's words already answered (a skipped one does not
   count).
   1. **Is this carte blanche?** Options: *No*; *Yes* (it merges its own PRs on green); *Yes,
      trescarteblanche* (the same in the projects named); or other acts the user names. On a yes, load
      `carte-blanche`: this question settles its extra grants, and the next is its budget.
   2. **How much usage, is a swarm allowed, and on which machines?** `budget-select` gives the share in points;
      the options say with or without a swarm. For a swarm, also ask which build or test machines it may use and
      how many jobs each takes: on a long voyage the machines, not the points, often set the pace.
   3. **Anywhere off-limits?** Areas, files or topics to stay out of.
   4. **Who leads?** The model and effort, from `tier-select`. If that is not this session's, write the voyage as a
      prompt for a fresh session (as bbq's step 8 does) and stop.

   Ask more than four only when a voyage cannot start without the answer, or the user asks for more; say why.
3. **The kind of voyage** around the pick is one of these. The user's words choose; failing that, question 1 chooses
   between a plain session and carte blanche.
   - **A plain session:** the project's rules and the platform's usual defaults (ask before anything leaves the
     machine).
   - **With bbq:** pick the topic, then run a bbq on it with the user.
   - **With Cloud** (a voyage led from a cloud container): pick, then write a prompt with bbq's Cloud type.
   - **With carte blanche:** work under the grant.
4. **Gather the candidates.**
   - The status file's *next* and *in progress* sections.
   - The debt list.
   - Open PRs and review findings: a red check, a review waiting for an answer.
   - Queued next-session prompts and proposals. **Work taken from a proposal stays a draft**: it goes in the
     drafts folder, or is marked PROPOSED, and is never shipped.

   With a topic (step 1), keep only candidates about it; if none is left, say so and ask whether to widen to the
   whole project. Leave out anything off-limits, marked as the user's, or waiting on a ruling. With none of these sources, read
   the README, open issues, TODO and FIXME comments, failing checks and the recent history. Say which sources you
   had.

   **In a swarm voyage, a list too long to read whole goes to small readers:** cheap workers (`tier-select`'s small
   tier, or local models) each return one line per candidate in their slice: what it is, what it unblocks, its
   rough size. The lead ranks those lines, not the list.
5. **Rank them**: work that other work waits on first, then the most value per point. Visual work may be picked:
   build any taste call in it as two or three options side by side, and send frames (screenshots) to the user by
   the end of the session, as `carte-blanche` does.

   **Before a pick goes out, check it is still open**, not already paid, superseded or retired: a cheap look at
   the main branch (search for the fix, read the file it cites, run the check it names). Mark a closed entry so,
   and send out the next pick.
6. **Announce and start**, without waiting: "Picked X because Y; next up Z." The user can redirect at any time,
   and their words win.
7. **Keep picking** until the budget's stop line (`carte-blanche`'s `stop_margin` under a grant, `budget-select`'s
   stop lines otherwise) or until step 8 applies.
   - **A pick that needs a real decision** (more than the starting questions covered): park it, file its
     questions, and pick the next.
   - **A swarm**, if allowed: `tier-select` chooses who does each job, local models included. A worker never
     has more authority than the lead. Picks that touch the same files or check go to one worker, in order, so
     one landing does not leave its siblings each needing a merge.
8. **When nothing is worth doing, say so** rather than invent work, write the end report and stop. Do
   housekeeping (stale comments, tidy docs, checks that should pass) only if the user asked for it.
9. **The end report.** A dated entry in the log: what was picked and why, what landed, parked questions, drafts
   written and points spent. Update the status file. Give the user the short version in chat, or as a
   notification when they are away, with any taste frames listed by branch.

## tresdealers-choice: across the projects named

The same choosing, across each project named with the word ("tresdealers-choice pitmaster and maplesyrup os"). It
widens where the agent looks for work, never what it may do there (ADR-023 rules 7 and 8).

1. **Resolve the names** to folders (a `projects:` line in `pitmaster.md`, otherwise the folders the user keeps
   projects in and their git remotes) and say each in one line; a name that matches none, or two, is asked.
   **None named:** list the projects you would pick from and wait for one yes. **One project:** it is plain
   dealer's choice there.
2. **Gather** step 4's candidates in every project named, and **rank them together** by step 5, so the pick may be
   in any of them. Say the project with the pick: "Picked X in maplesyrup os because Y."
3. **Each project's own rules** are the ceiling inside it, read before the first change there. What may be done
   without asking still comes from question 1: `trescarteblanche` for the same projects, or the voyage's own rules.
4. **The end report** lists what landed under each project, in each project's own log.

## Platform notes

- **Claude Code:** ask steps 1 and 2 with `AskUserQuestion`. Workers start with the Agent tool, or go to local
  models through whatever local-model tooling is installed. When the user is away, send frames and the short
  report with `SendUserFile` or `PushNotification`. In a Cloud voyage, `create_session` starts a successor.
- **Cowork / claude.ai:** no git or status file is usually at hand; read what the user has shared, pick from it,
  and end with the report in chat.
- **Codex:** ask as a numbered list in one message and wait. Run workers where your Codex supports them,
  otherwise one pick at a time.
- **Other tools:** ask as a numbered list, the options lettered and the recommended one first, then wait. Work the
  picks one at a time unless the tool documents its own workers.
