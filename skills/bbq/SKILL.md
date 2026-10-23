---
name: bbq
metadata:
  family: plan
description: A Big Batch of Questions. Grill the user in numbered rounds to settle a plan before any work starts (a run, an overnight queue, a decision, a new skill), then write the record that becomes the prompt. Use when the user types "bbq" or "makeskill", or asks to "ask me N questions", "grill me before we start", "question me before you delegate", "hone this prompt", or "interview me about a skill I want". "makeskill" opens bbq straight in the Skill type, which writes a new skill folder from the answers. Other types are ADR, Overnight, Arc, Debt, Morning, Host, Week, PR and Cloud (a run led from a cloud container). Any type can run as a Batch ("batch skill bbq", "batch adr bbq"): many items at once, a builder per item. "multitask" also loads it, and it asks "Batch bbq?" first.
---

# bbq: a Big Batch of Questions, then the run or its prompt

A bbq asks every question a piece of work needs before it starts, in numbered rounds. Each answer becomes a rule
tagged with the question that set it, and the record the bbq ends with is the prompt for the run, whether this
session runs it or a fresh one does.

Siblings: `budget-select` (how much of the week the run may spend), `tier-select` (which model and effort lead it,
and which tier does each job) and `makeadr` (turns an ADR-type bbq into a decision record). `project-prep` offers a
bbq at the end of its run, and a `talk-through` plan that needs its questions settled starts one. `goforit`, typed at the end of the opener, takes the bbq's closing offers and carries
the record on into the work. A bbq never re-asks a question a sibling already settled.

## Config

Edit these lines here, or put the same lines in a `pitmaster.md` at your project root, which wins. Every line is
optional.

```
name: the user        # who is grilled; "the user" in the steps means this name ("name: Alex")
count: ask            # questions per bbq: ask (offer 8 / 12 / 20 / other) or a number
record_dir: docs/bbq  # where records go (step 5)
ending: auto          # auto | run-here | prompt | ask (step 6)
land: pr              # pr (branch + PR) | commit (branch only) | file (just the file) (step 7)
types: docs/bbq-types.md   # your own types, in your project (an update never overwrites it)
batch_usage: on       # a Batch bbq loads budget-select and spend-ledger: on | off
batch_format: ask     # a Batch bbq's format: ask (by size on top) | by-size | rounds | item-sheets | batch-sheet (no question)
batch_sheet: form     # a Batch bbq's worksheet: form (a file where no form can be drawn) | file
```

## Steps

A plain bbq is steps 1 to 7. A bigger run also reads a file from `references/`:

- `references/the-types.md`: the topic fits a named type, or the user wants a type of their own.
- `references/skill-type.md`: the Skill type, or the user typed "makeskill".
- `references/cloud-and-away.md`: a Cloud bbq, or the user will be away or on a poor link.
- `references/batch.md`: a Batch bbq.

1. **The first round: the count, the type, the lead.** One round of questions, before any reading.
   - **The count.** Use the number the user named ("ask me 20 questions"), else the config's `count`, else ask
     once: 8, 12, 20 or other. This round's questions are Q1… and count toward the number, so recommend a count
     that leaves room (12 or more for the Skill type, which has ten things to cover). Where every question can
     already be answered with a citation (a record's question, an ADR, the user's words here), offer `goforit`
     too, saying what it rests on: no rounds, each question takes its cited answer (ADR-017). If any cannot be
     cited, no goforit.
   - **The type**, unless the user named it or the topic makes it plain; an untyped bbq is fine. "makeskill"
     means the Skill type: do not ask.
   - **Who leads (model and effort)**, whenever the run needs a lead session (an Overnight, an Arc, a Host run,
     any run with workers). Never assume the biggest model; `tier-select` recommends. The answer goes into the
     record and the kickoff line.
   - **Will the user be reachable?** In a Cloud bbq, and whenever the user says they are away (ADR-006).
   - **Batch?** When the user says "batch" or names several items of one kind to build at once, the bbq runs in
     Batch mode (ADR-015). When the user says "multitask", ask "Batch bbq?" first.
2. **Ground before you grill.** Before the first round of real questions, read the status file, the newest log
   entry, the open queue it points at and the type's reading, so no question asks what the files already answer.
   Then load siblings, each only if the run needs it, in this order: `budget-select` if the run spends a share of
   the usage limit, then `tier-select` for who leads and who works.
3. **The rounds.** Up to four questions a round, numbered across rounds (Q1…QN) so answers can be cited. Put
   the recommended option first, marked *(Recommended)*, and give each option its benefit in one line. Ask the
   structural questions first (scope, who may land work, who executes), the mechanical ones last, and let earlier
   answers shape later ones. **The final question is always "Anything else to protect or avoid?"**
   - **The Owed list.** A question is *owed* when an answer opens it (adds a constraint, names something not yet
     settled, or asks for a comparison), when the type has something to cover that no question has settled, or
     when a premise check fails. Add each to the record's *Owed* list as it appears, and **end every round with
     one line: "Owed: N" and what they are**, so the user sees more questions coming.
   - **When the count is reached** with questions still owed, ask once: ask them now (say how many), or default
     them into the record's *Defaulted* list, each with a `veto:` line. `goforit` is a third option on step 1's
     terms: every owed question citable (ADR-017). If the questions run out first, stop. Never pad a round.
   - **Under carte blanche** for this session, ask no rounds: answer every question yourself into the *Defaulted*
     list with a `veto:` line each, keep the Owed list, and end with a summary the user can approve or change. A
     taste answer (a name, a look, a direction) is a proposal, flagged as taste (ADR-007, amendment of
     2026-10-20).
4. **Read answers literally.** An answer that is itself a question or a request ("can you reach the server?") is
   answered with evidence before the next round, and the original question is asked again if that changes it.
   Reachability, tools and state are measured, never assumed.
5. **Write the record** to `<record_dir>/<date>-<topic>.md` (in a project you may not write to, ask where):
   - a one-line header: the date, the type, the count, who leads;
   - the Budget block, if there is one;
   - each rule with the question that set it ("**Q7 Landing.** Merge on green.");
   - the *Owed* list (empty at the end, or each item moved to Defaulted);
   - the *Defaulted* list: anything the lead settled without asking, each with a `veto:` note;
   - any recommendation the user overruled, marked "overruled";
   - a kickoff paragraph (step 7).

   A Skill bbq also writes the skill folder.
6. **Route the run** by the config's `ending`: `run-here`, `prompt` and `ask` always do that. At `auto`, the
   default:
   - a typed bbq that names its own session (Overnight, Arc, Host, Cloud) always writes a prompt for a fresh
     session;
   - otherwise route by the lead's context used, where the platform can measure it, and say the number and the
     route in one line:

     | context used | route |
     |---|---|
     | under 33 % | **run it in this session**, starting now |
     | 33–49 % | **ask the user**: run here, or hand to a fresh session |
     | 50 % or more | **write it as a prompt** for a fresh session and stop |

   - where context cannot be measured, ask: run here, or write the prompt.
7. **End a prompt-writing bbq** by the config's `land` (default `pr`):
   - **`pr`**, in a git repository with `gh` signed in: commit the record on a branch, open a docs PR, and offer
     a **Merge** step. After the merge, give a one-line, paste-ready kickoff pointing at the record on the main
     branch.
   - **`commit`**, in a git repository: commit the record on a branch, with no PR. The kickoff points at the
     record on that branch.
   - **`file`**, or no repository (or, for `pr`, no signed-in `gh`): the record file and the kickoff line, ready
     to paste.
   - A Cloud bbq also offers to launch the lead.
   - The kickoff names the lead's model and effort and tells a session on another model or effort to stop and
     say so before doing anything.

## Platform notes

- **Claude Code:** ask each round with `AskUserQuestion` (up to four questions, the recommended option first),
  with everything needed to answer in the questions' own wording, since option previews may not reach the user.
  Anything you say you made for the user to look at (a table, an explainer, a file) is sent as a file or linked
  in the same message. `/context` measures step 6's context. The Skill type writes to `.claude/skills/` in a
  project, `~/.claude/skills/` for the user, or a plugin's `skills/`. A Cloud relay starts the successor with
  `create_session` (claude-code-remote) and hands off with `send_message`; in the desktop app, the Cloud launch
  offer is a `start_session` card with `target: "cloud"` that the user starts. A Batch worksheet form is
  `show_widget`'s elicitation shape: one choice group per question, the recommended option pre-selected, an
  *Other* box. Batch builders are sessions the user can open (`start_session` with a worktree, in the desktop
  app) or `Agent` subagents with worktree isolation.
- **Cowork / claude.ai:** ask with `AskUserQuestion` where it is offered. There is no `/context` and usually no
  git or `gh`, so step 6 asks the user and step 7 ends with the record file and the kickoff line. The user zips
  the Skill type's folder and uploads it in their skill settings. No session tool for a Cloud relay: write the
  hand-off and stop. A Batch bbq's records are prompts the user starts by hand.
- **Codex:** ask each round as a numbered list in one message (or with a question tool, if your Codex has one)
  and wait for the answers. Codex shows the skill no context percentage, so step 6 asks the user. The Skill type
  writes to `.agents/skills/` in a project or `~/.codex/skills/` for the user. No session tool for a Cloud relay:
  write the hand-off and stop. Batch builders are Codex subagents where your Codex has them; otherwise each
  item's record is a prompt the user starts.
- **Other tools:** ask each round as a numbered list in one message, the options lettered and the recommended
  one first, then wait for the answers. Step 6 asks the user unless the tool reports context used. The Skill type
  writes to the folder the tool documents for skills. A Cloud relay uses the tool's own session-start tool if it
  has one; otherwise write the hand-off and stop, and the user starts the next lead.
