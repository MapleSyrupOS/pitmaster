# pitmaster

**Low and slow planning for fast agents.** Twelve skills that make Claude (and any agent that reads skills) ask
before it builds, write down what was decided, and keep a long run fed, on budget and on the right models. Beside
them sits **the shed**: small tools you can run with no agent at all.

pitmaster is a plugin for Claude Code and Codex, and a set of plain skill folders for Cowork, claude.ai and any
other tool that reads the [Agent Skills](https://agentskills.io) format. Apache-2.0.

## Where to go

| you want to… | go to |
|---|---|
| see what pitmaster is in five minutes | [Start here](#start-here-five-minutes), below |
| pick a skill for a job | [The skills](#the-skills) |
| run a tool without an agent | [The shed](#the-shed) |
| install it, or update it | [Install](#install) and [Update](#update) |
| change a setting | [Configure](#configure) |
| see what changed in a release | [CHANGELOG.md](CHANGELOG.md) |
| read the decisions behind the skills | [docs/decisions/](docs/decisions/) |
| add a skill of your own | [CONTRIBUTING.md](CONTRIBUTING.md) |

## Start here (five minutes)

**Who it's for.** You hand real work to agents, often several at once, and you want them to ask the right
questions first, stay inside a budget, and leave a record you can check later. If you run one agent on one small
task at a time, you may only need `bbq`.

**What the names mean.** Each name stands for something plain:

| say | it means |
|---|---|
| bbq | "Grill me before we start": a Big Batch of Questions. |
| makeadr | "Write this decision down properly." |
| talk-through | "Let's talk it through, then write down what we decided." |
| dealers-choice | "You pick what to work on." |
| carte-blanche | "Go ahead without asking, inside these limits." |
| goforit | "The plan is settled: build it, and stop only for my yes." |
| tier-select | "Which model should do this?" |
| budget-select | "How much of my usage should this get?" |
| spend-ledger | "What did that cost, and what did we get?" |
| swarm-bottleneck | "What's slowing my agents down?" |
| tastetest | "Would a stranger say this is ready?" |
| project-prep | "Get this project ready for agents." |

**Three things to try first.**

1. Before your next piece of work, say **"bbq, ask me 8 questions"**. You answer in rounds; it writes the plan.
2. When you settle something worth remembering, say **"makeadr"**. You get a short, dated decision file.
3. When you have a backlog and an hour of usage to spare, say **"dealer's choice"**. It asks four questions, picks
   the most useful work and tells you what it picked.

**Words you'll meet.**

- **Points:** a share of your plan's usage limit; by default, 1 point is 1 % of the weekly limit.
- **Lead and workers:** the session that plans and lands the work, and the helper agents it starts.
- **Record:** the file a skill leaves behind (a question record, an ADR, a ledger row), so the next session
  starts from it rather than from memory.
- **ADR / ADR+:** a short, dated file for one decision and why; ADR+ is the format pitmaster uses for them.
- **Veto line:** a call the agent made for you, written down so you can reverse it with one word.
- **Pinned copy:** a shed tool copied byte for byte into a skill, with a `.pin` file saying which release it is.

## The skills

They come in five families. Each row says what the skill does and the words that start it; Claude also loads a
skill on its own when your request matches.

**Plan the work** (`plan`)

| skill | what it does | start it with |
|---|---|---|
| **bbq** | A Big Batch of Questions: grills you in numbered rounds before a piece of work starts, and writes the record that becomes its prompt. Ten types, including **Skill**, which takes a new skill from draft to shipped. | "bbq", "makeskill", "ask me 12 questions before we start" |
| **makeadr** | Turns a question session into an architecture decision record, or a few lines into a short one (the light route). Three templates; scripts that build the index and check that each "Built" claim points at something that exists. | "makeadr", "let's make an ADR for…" |
| **talk-through** | Talks a subject through as an open conversation, in voice or text, tracking decisions, open questions, action items and corrections; on your word it writes one record, each decision marked agreed, proposed or open and cited to where it came up. | "talk-through", "let's talk it through" |

**Run it** (`run`)

| skill | what it does | start it with |
|---|---|---|
| **dealers-choice** | The agent picks what to work on: four quick questions, then it reads your status, debt list and PR queue, says what it picked and why, and keeps going until the budget stop. | "dealer's choice" |
| **carte-blanche** | Standing authority for one session: the agent picks, pushes branches, opens PRs and spends a set budget without asking, inside your project's rules, and leaves a veto line for every call. Taste always comes back to you. | "carte blanche" |
| **goforit** | Once a plan is settled, carries it on into the build, here or by a worker, and stops only for your "ratify" and your merge. "goforitreally" hands off the merge too. Also an answer: "goforit" mid-questions means take the recommended answers and go. | "bbq … goforit", "goforitreally" |
| **tier-select** | Picks the model and effort for a run's lead and each worker, by the shape of the job, on any vendor. | "which model should lead this?" |

**Watch the usage** (`usage`)

| skill | what it does | start it with |
|---|---|---|
| **budget-select** | Gives a run its share of your plan's usage limit, in points, with stop lines and a Budget block for its prompt. | "how much budget should this get?" |
| **spend-ledger** | Records what a session actually spent (tokens from its own transcript, the usage meter, a list-price proxy) beside what it landed, one row per session, and reports the cost per landing over a week. | "log the spend", "what did we get for the points?" |
| **swarm-bottleneck** | Names the one constraint holding a multi-agent run back (limits, context, CI, the review queue, your attention, failing tools) with evidence and moves. | "what's the bottleneck?" |

**Check it before it ships** (`check`)

| skill | what it does | start it with |
|---|---|---|
| **tastetest** | A blind taste test before the public gets a bite: an auditor that knows nothing about your project gets only what an outsider would see, tries it, and reports READY or NOT READY with ranked findings. Profiles for a repository going public and an app going to the App Store. | "tastetest", "is this ready to go public?" |

**Set the project up** (`records`)

| skill | what it does | start it with |
|---|---|---|
| **project-prep** | Sets a new or existing project up for agents (not app code): by default the agent rules and a STATUS file whose claims cite files; a log, debt list, decisions folder, glossary and more on request. On a branch, never overwriting a file. Ends by offering to put your first decision on record. | "project-prep", "prep this project" |

The skills work together: a `bbq` asks `budget-select` and `tier-select` for their recommendations, and hands an
ADR-type session to `makeadr`. `spend-ledger` measures afterwards what `budget-select` set beforehand. `dealers-choice` picks the work and asks whether the run has `carte-blanche`. `project-prep` sets a project up and hands its first decision to `makeadr`.

## The shed

[`pitmaster-shed`](https://github.com/MapleSyrupOS/pitmaster-shed) holds small tools a person can run without an
agent: one Python 3 script per tool (standard library only), each in its own folder with a README and a self-test,
on macOS, Linux and Windows. Copy a tool's folder into your project, or use the shed as a
[pre-commit](https://pre-commit.com) hook repository. It is private for now, and goes public with pitmaster.

| tool | what it does |
|---|---|
| `adr-check` | Checks every ADR's header, that each proof resolves, and that the extra sections appear only when options were weighed. |
| `adr-index` | Writes the ADR index from the ADRs themselves; `--check` fails when it is stale. |
| `comment-only` | Proves an edit changed only comments (C/C++ and NASM). |
| `compact` | Moves a block of text into an append-only archive, verbatim, and proves from git that nothing else changed. |
| `elf-loaded` | Compares only the loaded sections of two ELF64 files. |
| `fence-mark` | Runs a command and always leaves a one-line marker and the whole diff. |
| `modeguard` | Refuses a lost executable bit (or any mode change) unless it is on an allow list. |
| `ratchet` | Fails when a listed file grows past its line-count limit. |
| `split-status-log` | Splits a newest-first dated log by month, byte for byte. |
| `status-check` | Checks a STATUS file's length and that every bullet cites a file that exists. |

**How the skills use it.** `makeadr` carries pinned copies of `adr-index` and `adr-check`, and `project-prep`
carries `status-check`, so every install works offline with nothing extra to fetch. A fix is made in the shed
first; each copy is then updated byte for byte, and `scripts/check-pins.py` fails, naming the file, if a copy
ever drifts from its pin.

**Rules** are the third layer, still a draft: short opt-in lines a project switches on by group.

## Install

**Claude Code**

```
/plugin marketplace add MapleSyrupOS/pitmaster
/plugin install pitmaster@pitmaster
```

The skills are then `/pitmaster:bbq`, `/pitmaster:makeadr`, `/pitmaster:swarm-bottleneck`,
`/pitmaster:budget-select`, `/pitmaster:tier-select`, `/pitmaster:spend-ledger`, `/pitmaster:dealers-choice`,
`/pitmaster:carte-blanche`, `/pitmaster:project-prep`, `/pitmaster:talk-through`,
`/pitmaster:tastetest` and `/pitmaster:goforit`. Claude
also loads them on its own when your request matches.

**Codex**

```
codex plugin marketplace add MapleSyrupOS/pitmaster
codex plugin add pitmaster@pitmaster
```

**Cowork and claude.ai**

Download a skill's zip from the [latest release](https://github.com/MapleSyrupOS/pitmaster/releases) (pick the
`claude` build) and upload it in Claude's skill settings. One zip per skill; each is a plain zip with a `.skill` name.

**Any other tool that reads skills**

Copy a folder from `skills/` into your tool's skills folder, or use the `generic` zips from the release. Each
skill's *Platform notes* section says what it does differently there.

## Update

An installed plugin does not change by itself. Refresh the marketplace, then update the plugin:

**Claude Code**

```
claude plugin marketplace update pitmaster
claude plugin update pitmaster@pitmaster
```

Restart Claude Code to load the new version. `claude plugin list` shows which one you have.

**Codex**

```
codex plugin marketplace upgrade pitmaster
codex plugin add pitmaster@pitmaster
```

**Cowork and claude.ai:** download the skill's zip from the newest release and upload it again in place of the
old one.

## Platform support

| platform | install | status |
|---|---|---|
| Claude Code | plugin | supported |
| Cowork, claude.ai | zip upload | supported |
| Codex | plugin | supported; smoke-tested 2026-10-16 |
| OpenCode | copy a folder | smoke-tested 2026-10-16 |
| Antigravity | copy a folder | smoke-tested 2026-10-16 |
| Other Agent Skills tools | copy a folder | expected to work; untested |

Every skill keeps its steps in plain words and puts anything platform-specific in one tagged *Platform notes*
section ([ADR-001](docs/decisions/ADR-001-platform-agnostic-skills.md)). Each skill's first move has been tried in Codex,
Antigravity and OpenCode.

## Configure

Every skill has a short config block at its top. To change a setting without editing the installed copy, put the
same `key: value` lines in a `pitmaster.md` file at your project root. For example:

```
name: Alex
count: 12
record_dir: docs/plans
```

`name` makes the skills address you by name in place of "the user".

## More

- [CHANGELOG.md](CHANGELOG.md): what changed in each release.
- [docs/starter-guide/](docs/starter-guide/words.md): the starter guide's words, a panel per step; its design is on the way.
- [CONTRIBUTING.md](CONTRIBUTING.md): how to add a skill (with `bbq`, of course).
- [docs/decisions/](docs/decisions/): the decisions behind the skills.
- [LICENSE](LICENSE) (Apache-2.0) and [NOTICE](NOTICE).

Copyright 2026 Writerblockade.
