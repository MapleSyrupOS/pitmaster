# Getting started with pitmaster — the starter guide (words only)

**Status:** draft words, 2026-10-21. The look is the owner's to design: layout, art, colours, type and format
(poster, zine, cards, a web page) are all open. Every panel below is a suggestion; cut, merge or rename freely.
Each panel has a headline, one line on what it's for, what you type, what happens, and a tip.

---

## Panel 0 — Cover

**Headline:** Getting started with pitmaster
**In a line:** Skills that make your agents ask before they build, stay on budget, and leave a record you can
check.
**Small print:** Works in Claude Code, Codex, Cowork, claude.ai and any tool that reads Agent Skills.

---

## Panel 1 — Install

**In a line:** Two commands and the skills are there.
**You type (Claude Code):**

```
/plugin marketplace add MapleSyrupOS/pitmaster
/plugin install pitmaster@pitmaster
```

**What happens:** twelve skills appear. You can call one by name, or just ask in plain words and Claude picks the
right one.
**Tip:** Codex has its own two lines (`codex plugin marketplace add …`, `codex plugin add …`); see the README.

---

## Panel 2 — bbq: grill me first

**In a line:** A Big Batch of Questions. Before any real work starts, it grills you.
**You type:** "bbq, ask me 8 questions before we start"
**What happens:** numbered rounds of questions, each with a recommended answer. When you're done, it writes the
plan down, and that record becomes the prompt for the work.
**Tip:** say "go with your picks" on any question you don't care about.

---

## Panel 3 — Write the decision down (makeadr)

**In a line:** Decisions get forgotten. Written ones don't.
**You type:** "makeadr: we're using Postgres, not SQLite"
**What happens:** a short, dated decision file: what was decided, why, what else was considered, and what's built.
**Tip:** you change a decision later with an amendment, never by rewriting it, so the history stays honest.

---

## Panel 4 — Budget and models (budget-select, tier-select)

**In a line:** Decide how much usage a run gets, and which model does what.
**You type:** "how much budget should this get?" and "which model should lead this?"
**What happens:** a share of your usage in points (1 point = 1 % of your weekly limit by default), stop lines, and
the right model for each job: a large one to plan, smaller ones to read and check.
**Tip:** the stop line is there so a long run ends with something left for tomorrow.

---

## Panel 5 — Let the agent pick (dealers-choice)

**In a line:** Not sure what to work on next? Let it choose.
**You type:** "dealer's choice"
**What happens:** four quick questions (is this carte blanche, how much usage and on which machines, anything
off-limits, who leads). Then it reads your status, debt list and open PRs, picks what unblocks the most, tells
you in one line, and starts.
**Tip:** redirect it any time. Your words win.

---

## Panel 6 — Go ahead without asking (carte-blanche)

**In a line:** Hand over the work, keep the final say.
**You type:** "carte blanche"
**What happens:** the agent works without asking, inside your project's rules and a set budget: it picks, pushes
its own branches and opens PRs. Taste (names, looks, direction) always comes back to you, and every call it made
for you gets a veto line.
**Tip:** merging is off unless you name it: "carte blanche, plus merge on green".

---

## Panel 7 — What did it cost? (spend-ledger, swarm-bottleneck)

**In a line:** See what a run spent, and what's slowing your agents down.
**You type:** "what did that cost?" or "what's the bottleneck?"
**What happens:** one row per session, what it spent beside what it landed. Or the one thing holding your agents
back right now, with the evidence and what to try.
**Tip:** "cost per PR" over a week shows which runs were worth it.

---

## Panel 8 — Set up a new project (project-prep)

**In a line:** Give agents what they need before the first task.
**You type:** "prep this project"
**What happens:** one round of questions, then the files agents need to work well (rules, a status file, a
glossary, folders for proposals and decisions), on a branch, never overwriting anything.
**Tip:** it ends by offering to write down your project's first decision.

---

## Panel 9 — Cheat sheet (back cover)

| say | it means |
|---|---|
| bbq | Grill me before we start: a Big Batch of Questions. |
| makeadr | Write this decision down properly. |
| budget-select | How much of my usage should this get? |
| tier-select | Which model should do this? |
| swarm-bottleneck | What's slowing my agents down? |
| spend-ledger | What did that cost, and what did we get? |
| dealers-choice | You pick what to work on. |
| carte-blanche | Go ahead without asking, inside these limits. |
| project-prep | Get this project ready for agents. |
| talk-through | Let's talk it through, then write down what we decided. |
| tastetest | Is this ready for strangers? Taste it blind and tell me. |
| goforit | We've talked enough: build it, and stop when you need my yes. |

**Sign-off:** Low and slow planning for fast agents.

---

## For the designer (open, the owner's call)

- Format: one poster, a folded zine, a card per skill, or a web page?
- A running character or mascot, or none?
- One panel per skill, or group panels 4 and 7 as they are here?
- Does the cheat sheet double as something to print?
