---
name: call-escalator
metadata:
  family: run
description: Hand one stuck problem to a fresh reader, with a brief that keeps what was seen apart from what is only suspected, then check the reader's verdict before acting on it. "call-escalator" hands it to a stronger model or a higher effort; "secondopinion" hands it blind to the same model and effort. Use when the user types "call-escalator", "secondopinion" or "second-opinion", or says "escalate this", "get a stronger model on this", "hand this to a bigger model", "fresh eyes on this" or "we're stuck, escalate". Also offer it once when two attempts at the same problem have failed, before a third is spent; machine faults never count. "Second opinion" as two plain words in passing, "escalate to my manager" and an escalator in a building do not load it. The reader is read-only unless the brief grants one safe place to test, and never lands work.
---

# call-escalator: hand a stuck problem to a fresh reader

Decided by pitmaster ADR-041.
Two opt-in rules make a session keep the count (project-prep's `run` and `check` groups).

Sibling of `tier-select` (recommends the reader's model and effort, and keeps the note when a model could not be
reached) and `carte-blanche` (whose grant covers a hand-over only when it names one, or when a coordinator the
lead listens to orders one).

The session that is stuck is "the stuck session". The agent that takes the problem is "the reader".

## Config

Edit these lines here, or put the same lines in a `pitmaster.md` at your project root, which wins. Every line is
optional.

```
name: the user        # who the skill speaks to
offer_at: 2           # failed attempts at one problem before the skill is offered
reader: ask           # where the reader runs: ask | subagent | session
```

## The two words

| typed | who reads | what the reader is told of the stuck session's theories |
|---|---|---|
| "call-escalator" | a stronger model, or the same model at a higher effort | they are passed on, under the heading "Suspected, unverified" |
| "secondopinion", "second-opinion" | the same model and effort | nothing; the reader is blind |

## Steps

1. **Keep the count.** A failed round is one attempt at the same problem that did not fix it. After each one, say
   one line: "Failed rounds on <the problem>: 1". A machine fault (a host offline, a timeout, a quota, a model not
   loaded) never counts. Where the run keeps a ledger, the line goes there too.
2. **At two, stop and offer.** Before a third attempt, offer this skill once, with both words. The user may also
   type either word at any count.
3. **Pick the reader, then ask once.** One round of questions:
   - **Who reads.** For "call-escalator", `tier-select` recommends one step up from the stuck session, a tier or
     an effort. For "secondopinion", the same model and effort. Say the recommendation and let the user change
     it.
   - **Where the reader runs** (config `reader`): a subagent, whose report comes straight back, or a separate
     session the user can open and steer, which reports back by message. Recommend the subagent unless the brief
     grants a place to test and the job will run long.
   - **Any safe place to test** the reader may use (step 4, part 2).

   Under `carte-blanche`, take the recommendation without asking only when the grant names hand-overs, or when
   the grant says *Listen to the coordinator* and a coordinator whose own grant names hand-overs orders this
   hand-over (ADR-042). A hand-over the coordinator orders is read-only: it grants no place to test. When neither
   holds, or when the user is away with no grant, write the brief, park the problem, say so in one line and move
   to other work.
4. **Write the brief.** Five parts, in this order. The reader starts fresh: it never runs in the stuck session's
   own context, and the brief is all it knows.
   1. **Seen.** What happened, one line per run or test, each with the command or file that shows it.
      "call-escalator" then adds **Suspected, unverified**: the stuck session's theories, each marked as not
      proven. "secondopinion" leaves them out.
   2. **Off limits, and the safe place.** What the reader must not touch, with one line on what a failed try
      costs (a power-cycle by hand, an hour of building, a wiped disk). The reader is read-only unless this part
      grants one named place to test: a folder, a test VM, a scratch branch.
   3. **Changed since it last worked.** Everything the stuck session changed or added after the last run that
      passed, diagnostics included.
   4. **Done when.** A numbered list that ends: "name the cause, with the evidence that shows it and the evidence
      that would refute it".
   5. **Who lands it.** The stuck session does. The reader never pushes, merges or lands work.

   Anything the user granted is quoted in the user's own words, never restated in the session's.
5. **If the model cannot be reached** (a gate refuses it, the agent list is out of date, a quota is spent), run
   the reader on the strongest model that can be reached, still fresh. Say in one line which model was wanted and
   which ran, and add a dated line to the project's `tier-select` roster beside that model: what was wanted, why
   it could not be reached, what ran. `tier-select` reads its roster, so the next pick knows.
6. **Read the verdict.** The reader's report opens with one line naming the kind:
   - `MECHANICAL:` a plain cause (a stale value, a wrong path);
   - `TOOLING:` a fault the stuck session's own changes made;
   - `DESIGN:` the design is wrong, and what it should be;
   - `NOT FOUND:` no cause named.

   Then the evidence, what would refute it, and every check the reader could not run, named.
7. **Check, then act.** The stuck session checks the evidence itself before it changes anything. A mechanical or
   tooling cause it then fixes. A `DESIGN:` verdict stops and goes to the user: changing a design is theirs to
   rule.
8. **If the hand-over fails** (`NOT FOUND:`, or its fix fails too): a secondopinion may go up once to
   call-escalator. A call-escalator that fails stops and goes to the user with everything tried so far. Never more
   than two hand-overs on one problem without the user's word.
9. **Close.** One line: who read it, the verdict's kind, and what was done.

## Never

- The reader never touches what the brief marks off limits.
- The reader never pushes, merges or lands work.
- A machine fault never counts as a failed round.
- A `DESIGN:` verdict never changes a design without the user.
- The hand-over never runs in the stuck session's own context.
- A grant is quoted in the user's words, never passed on in the session's.

## Platform notes

- **Claude Code:** ask step 3 with `AskUserQuestion`, everything needed in the questions' own wording. A subagent
  reader is an `Agent` call with the model `tier-select` named; a session reader is `start_session` with a fresh
  context, in the desktop app, and it reports back with `SendMessage`. A session the user detaches stops
  reporting on its own: ask it to message the stuck session when it is done.
- **Cowork / claude.ai:** no subagents or sessions to start. Write the brief as a file and give the user one line
  to paste into a new chat; the user brings the verdict back.
- **Codex:** ask step 3 as a numbered list. The reader is a Codex subagent where your Codex has them; otherwise
  the brief is a prompt the user starts.
- **Other tools:** ask step 3 as a numbered list in one message. Use the tool's own subagents if it has them;
  otherwise write the brief as a file and stop, and the user starts the reader.
