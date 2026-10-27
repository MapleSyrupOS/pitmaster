# Getting started with Pitmaster — the starter guide (words only)

**Status:** draft words, 2026-10-23, reworded in the owner's words by the bbq in
`docs/bbq/2026-10-23-readme-starter-guide.md` (Q94–Q137). The look is the owner's to design: layout, art, colours,
type and format (poster, zine, cards, a web page) are all open. Each panel has four parts: a headline, what you type,
what happens, and a tip (Q94). A line marked *(from the README)* was filled in from the README's wording rather than
asked on its own; change it freely.

---

## Panel 0 — Cover

**Headline:** Getting started with Pitmaster
**In a line:** A plugin of skills, rules and tools that you and your AI agent can use to start new projects or manage
existing ones.
**Small print:** Works with Claude Code, Codex, Antigravity and any other agent that reads skills.

---

## Panel 1 — Install

**Headline:** Two commands and the skills are there.
**You type (Claude Code):**

```
/plugin marketplace add MapleSyrupOS/pitmaster
/plugin install pitmaster@pitmaster
```

**What happens:** Sixteen skills become available. Call one by name, or ask in plain words and your agent picks the
right one.
**Tip:** Use the README to figure out how to use Pitmaster in the way that works best for your setup.

---

## Panel 2 — bbq

**Headline:** bbq: ask me first
**You type:** "have a bbq", or "16q bbq user interface"
**What happens:** Before the agent builds anything, it reads your project and asks you rounds of questions, each with a
recommended answer. When you're done, it writes down what you settled, and that becomes the plan for the work.
**Tip:** Answer with a question if you need to. If something needs checking, it checks before going on.

---

## Panel 3 — makeadr

**Headline:** Decisions get forgotten. ADRs don't.
**You type:** "makeadr: we're using Postgres, not SQLite"
**What happens:** A short, dated decision file: what was decided, why, what else was considered, and what's built.
*(unchanged from the last draft)*
**Tip:** You can amend a decision, but the history stays, so you can always see how you got there.

---

## Panel 4 — talk-through

**Headline:** "Let's have a chat about this and you can distill the important parts of the conversation for me."
**You type:** "talk-through" *(from the README)*
**What happens:** A talk, not a build: go back and forth on a topic, and it will help make sure it's kept on record.
**Tip:** Say "wrap it up" or just tell the agent you're done with the session.

---

## Panel 5 — Budget and models (budget-select, tier-select)

**Headline:** Share out your weekly usage, and pick the right model for each part.
**You type:** "how much budget should this get?" and "which model should lead this?" *(from the README)*
**What happens:** You get a share of your weekly usage in points (by default, 1 point is 1 % of your weekly limit), a
stop line, and a model for each job: a big one to plan, smaller ones to read and check.
**Tip:** Set a stop line so a long comrun leaves room in your weekly and session usage.

---

## Panel 6 — Dealer's choice

**Headline:** Not sure what to work on next? Let it choose.
**You type:** "dealer's choice"
**What happens:** It asks four quick questions first (how much usage, anything off-limits, and so on), then keeps
picking until it reaches the budget you set. *(from the README)*
**Tip:** Give it a direction if you like: "dealer's choice docs". Or don't, and see what it picks.

---

## Panel 7 — How much can it do without asking? (goforit, goforitreally, carte-blanche, trescarteblanche)

**Headline:** How much can it do without asking?
**You type:** "goforit", "goforitreally", "carte blanche" or "trescarteblanche"
**What happens:** Each word allows everything the one before it does, and adds one thing.

| say | adds | still stops for you at |
|---|---|---|
| goforit | builds the plan you just settled | your approval and your merge |
| goforitreally | merges by itself once you've approved | your approval |
| carteblanche | any work, for the whole session | anything public, pushing to main, deleting work |
| trescarteblanche | every project you name | the same |

*(No tip: the table says it, Q137.)*

---

## Panel 8 — Where did the time and tokens go? (spend-ledger, swarm-bottleneck)

**Headline:** Where did the time and tokens go?
**You type:** "log the spend" or "what's the bottleneck?" *(from the README)*
**What happens:** spend-ledger writes one row per session: what it used, beside what got merged. swarm-bottleneck
names the one thing holding your agents back right now, with the evidence and what to try.
**Tip:** Check your cost per pull request across a week to see which comruns were good value and which cost too much.

---

## Panel 9 — project-prep

**Headline:** Organize this project for you and your agents.
**You type:** "prep this project"
**What happens:** One round of questions, then the files your agents need (a rules file, a status file, and more if
you want it), on a new branch, never overwriting anything.
**Tip:** It ends by offering to write down your project's first decision.

---

## Panel 10 — tastetest

**Headline:** An outsider's audit.
**You type:** "tastetest" or "is this ready to go public?" *(from the README)*
**What happens:** It starts a fresh agent that gets none of your notes, only what a stranger would see, has it try
your project, and gives you a plain READY or NOT READY.
**Tip:** Making an app? It has an App Store check too.

---

## Panel 11 — looseends

**Headline:** What did we leave unfinished?
**You type:** "looseends" *(from the README)*
**What happens:** It looks through the chat you're in, the whole project or one topic for anything left hanging,
checks each is still open, and offers to tie them off.
**Tip:** Point it somewhere: "looseends project", or "looseends" plus a topic.

---

## Panel 12 — setfree

**Headline:** Release day, on your word.
**You type:** "setfree" or "release day" *(from the README)*
**What happens:** It shows each decision waiting to go public so you can approve or hold it, offers a blind
tastetest, then works through your release checklist and stops for your word before every public step.
**Tip:** Nothing is published, tagged or made public until you say so.

---

## Panel 13 — Cheat sheet (back cover)

The README's "What to say" table, word for word, so the two always match (Q131):

| say | it means |
|---|---|
| bbq | Before you build anything, read where the project stands and ask me a Big Batch of Questions so we agree on the plan. |
| makeadr | Record this decision in a dated decision file, so later sessions know what we decided and why. |
| carte-blanche | Until this session ends, you don't need my OK to push branches, open pull requests or merge them once their checks pass. Stay inside the budget and the project's rules, and leave a veto line for every call you make. |
| tastetest | Audit from an agent that knows nothing about the project. |
| setfree | Get the release ready, show me exactly what goes out, and wait for my word before anything is published. |
| talk-through | Let's have a chat about this and you can distill the important parts of the conversation for me. |
| dealers-choice | You pick what to work on: look at what needs doing, ask me a few quick questions, and pick the most useful job. |
| goforit | This plan is settled. Build it now, and stop only for my approval and my merge. |
| goforitreally | Build the plan and merge it once the checks pass. Stop only for my approval. |
| looseends | What did we leave unfinished? |
| tier-select | Out of our available models, which model should handle this part of the work? |
| budget-select | Help me decide what share of my weekly usage goes to this, so one job doesn't take more than I want. |
| spend-ledger | What did the agents spend their time on, and how many tokens did it take? |
| swarm-bottleneck | Several agents are working at once and getting in each other's way: what's slowing the agents down? |
| project-prep | Organize this project for me and my agents. |

**Sign-off:** Stay organized in a way that helps you and your agents.

---

## For the designer (open, the owner's call)

- Format: one poster, a folded zine, a card per skill, or a web page?
- If it becomes a web page, panel 7 (the ladder) could be interactive: click a word and see what it adds (Q136).
- A running character or mascot, or none?
- One panel per skill, or grouped as panels 5, 7 and 8 are here?
- Does the cheat sheet double as something to print?
