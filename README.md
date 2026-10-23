# pitmaster

**Low and slow planning for fast agents.** Twelve skills that make Claude (and any agent that reads skills) ask
before it builds, write down what was decided, and keep a long run fed, on budget and on the right models. Beside
them sits **the shed**: small tools you can run with no agent at all.

They were distilled from months of daily use on one large project of about 1.5 million lines, run with fleets of
agents and local models.

> **Early, and still moving.** pitmaster is young: expect changes between versions, and read the
> [CHANGELOG](CHANGELOG.md) when you update. Some skills act on your repository: they push
> [branches](#new-to-github), open [pull requests](#new-to-github) and, if you allow it, [merge](#new-to-github) them. Each one says
> so before it does, and nothing merges unless you grant it.

pitmaster is a plugin for Claude Code and Codex, and a set of plain skill folders for Cowork, claude.ai and any
other tool that reads the [Agent Skills](https://agentskills.io) format. Apache-2.0.

## Where to go

| you want to… | go to |
|---|---|
| see what pitmaster is in five minutes | [Start here](#start-here-five-minutes), below |
| pick a skill for a job | [The skills](#the-skills) |
| run a tool without an agent | [The shed](#the-shed) |
| install it, or update it | [Install](#install) and [Update](#update) |
| ask a question, report a problem, give feedback | [Help and feedback](#help-and-feedback) |
| change a setting | [Configure](#configure) |
| see what changed in a release | [CHANGELOG.md](CHANGELOG.md) |
| read the decisions behind the skills | [docs/decisions/](docs/decisions/) |
| add a skill of your own | [CONTRIBUTING.md](CONTRIBUTING.md) |
| learn the GitHub words | [New to GitHub?](#new-to-github) |

## Start here (five minutes)

**Who it's for.** You hand real work to agents, often several at once, and you want them to ask the right
questions first, stay inside a budget, and leave a record you can check later. If you run one agent on one small
task at a time, you may only need `bbq`.

**What you need.** Claude Code or Codex (any paid plan works; the usage skills assume a plan with a weekly usage
limit), or Cowork or claude.ai for the skill zips. For the skills that open pull requests, `git` and GitHub's
`gh` signed in. Nothing else to install.

**Install** (Claude Code; every other way is under [Install](#install)):

```
/plugin marketplace add MapleSyrupOS/pitmaster
/plugin install pitmaster@pitmaster
```

**Three things to try first.**

1. Before your next piece of work, say **"bbq, ask me 8 questions"**. You answer in rounds; it writes the plan.
2. When you settle something worth remembering, say **"makeadr"**. You get a short, dated decision file.
3. When you have a backlog and an hour of usage to spare, say **"dealer's choice"**. It asks four questions, picks
   the most useful work and tells you what it picked.

**Words you'll meet.**

- **Skill:** a packaged set of instructions an agent loads when your request matches.
- **Agent:** the AI assistant doing the work (Claude Code, Codex and so on).
- **Plugin:** how the skills install in Claude Code and Codex, all twelve at once.
- **Points:** a share of your plan's usage limit; by default, 1 point is 1 % of the weekly limit.
- **Lead and workers:** the session that plans and lands the work, and the helper agents it starts.
- **Swarm:** several agents working at once on one run.
- **Record:** the file a skill leaves behind (a question record, an ADR, a ledger row), so the next session
  starts from it rather than from memory.
- **ADR:** a short, dated file for one decision and why; pitmaster's format for them is ADR+.
- **Ratify:** you approve a decision. After that its words are never edited, only added to.
- **Veto line:** a call the agent made for you, written down so you can reverse it with one word.
- **Taste:** naming, looks and direction. Always yours, whatever authority you give an agent.
- **The shed:** small tools you can run with no agent at all.

GitHub words (repository, branch, pull request, merge) are under [New to GitHub?](#new-to-github).

| say | it means |
|---|---|
| bbq | "Grill me before we start": a Big Batch of Questions. |
| makeadr | "Write this decision down properly." |
| carte-blanche | "Go ahead without asking, inside these limits." |
| tastetest | "Would a stranger say this is ready?" |
| talk-through | "Let's talk it through, then write down what we decided." |
| dealers-choice | "You pick what to work on." |
| goforit | "The plan is settled: build it, and stop only for my yes." |
| tier-select | "Which model should do this?" |
| budget-select | "How much of my usage should this get?" |
| spend-ledger | "What did that cost, and what did we get?" |
| swarm-bottleneck | "What's slowing my agents down?" |
| project-prep | "Get this project ready for agents." |

## The skills

**Start with these four.** Each row says what the skill does and the words that start it; Claude also loads a
skill on its own when your request matches.

| skill | what it does | start it with |
|---|---|---|
| **bbq** | A Big Batch of Questions: grills you in numbered rounds before a piece of work starts, and writes the record that becomes its prompt. Ten types, including **Skill**, which takes a new skill from draft to shipped. | "bbq", "makeskill", "ask me 12 questions before we start" |
| **makeadr** | Turns a question session into an architecture decision record, or a few lines into a short one (the light route). Three templates; scripts that build the index and check that each "Built" claim points at something that exists. | "makeadr", "let's make an ADR for…" |
| **carte-blanche** | Standing authority for one session: the agent picks, pushes branches, opens PRs and spends a set budget without asking, inside your project's rules, and leaves a veto line for every call. Taste always comes back to you. | "carte blanche" |
| **tastetest** | A blind taste test before the public gets a bite: an auditor that knows nothing about your project gets only what an outsider would see, tries it, and reports READY or NOT READY with ranked findings. Profiles for a repository going public and an app going to the App Store. | "tastetest", "is this ready to go public?" |

**The rest, for power users**, by what they are for:

**Plan the work**

| skill | what it does | start it with |
|---|---|---|
| **talk-through** | Talks a subject through as an open conversation, in voice or text, tracking decisions, open questions, action items and corrections; on your word it writes one record, each decision marked agreed, proposed or open and cited to where it came up. | "talk-through", "chitchat", "let's talk it through" |

**Run it**

| skill | what it does | start it with |
|---|---|---|
| **dealers-choice** | The agent picks what to work on: four quick questions, then it reads your status, debt list and PR queue, says what it picked and why, and keeps going until the budget stop. | "dealer's choice" |
| **goforit** | Once a plan is settled, carries it on into the build, here or by a worker, and stops only for your "ratify" and your merge. "goforitreally" hands off the merge too. Also an answer: "goforit" mid-questions means take the recommended answers and go. | "bbq … goforit", "goforitreally" |
| **tier-select** | Picks the model and effort for a run's lead and each worker, by the shape of the job, on any vendor. | "which model should lead this?" |

**Watch the usage**

| skill | what it does | start it with |
|---|---|---|
| **budget-select** | Gives a run its share of your plan's usage limit, in points, with stop lines and a Budget block for its prompt. | "how much budget should this get?" |
| **spend-ledger** | Records what a session actually spent (tokens from its own transcript, the usage meter, a list-price proxy) beside what it landed, one row per session, and reports the cost per landing over a week. | "log the spend", "what did we get for the points?" |
| **swarm-bottleneck** | Names the one constraint holding a multi-agent run back (limits, context, CI, the review queue, your attention, failing tools) with evidence and moves. | "what's the bottleneck?" |

**Set the project up**

| skill | what it does | start it with |
|---|---|---|
| **project-prep** | Sets a new or existing project up for agents (not app code): by default the agent rules and a STATUS file whose claims cite files; a log, debt list, decisions folder, glossary and more on request. On a branch, never overwriting a file. Ends by offering to put your first decision on record. | "project-prep", "prep this project" |

The skills work together: a `bbq` asks `budget-select` and `tier-select` for their recommendations, and hands an
ADR-type session to `makeadr`. `spend-ledger` measures afterwards what `budget-select` set beforehand. `dealers-choice` picks the work and asks whether the run has `carte-blanche`. `project-prep` sets a project up and hands its first decision to `makeadr`.

## The shed

[`pitmaster-shed`](https://github.com/MapleSyrupOS/pitmaster-shed) holds small tools a person can run without an
agent: one Python 3 script per tool (standard library only), each in its own folder with a README and a self-test,
on macOS, Linux and Windows. Copy a tool's folder into your project, or use the shed as a
[pre-commit](https://pre-commit.com) hook repository.

| tool | what it does |
|---|---|
| `adr-check` | Checks every ADR's header, that each proof resolves, and that the extra sections appear only when options were weighed. |
| `adr-index` | Writes the ADR index from the ADRs themselves; `--check` fails when it is stale. |
| `comment-only` | Proves an edit changed only comments, in C, C++ or assembly code. |
| `compact` | Moves a block of text into an append-only archive, verbatim, and proves from git that nothing else changed. |
| `elf-loaded` | Compares only the parts of two compiled programs that actually get loaded and run. |
| `fence-mark` | Runs a command and always leaves a one-line marker and the whole diff. |
| `modeguard` | Refuses a lost executable bit (or any file-mode change) unless it is on an allow list. |
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
section ([ADR-001](docs/decisions/ADR-001-platform-agnostic-skills.md)). The first five skills' first moves were tried in Codex,
Antigravity and OpenCode on 2026-10-16; the later seven have been used in Claude Code and Codex.

## Configure

Every skill has a short config block at its top. To change a setting without editing the installed copy, put the
same `key: value` lines in a `pitmaster.md` file at your project root. For example:

```
name: Alex
count: 12
record_dir: docs/plans
```

`name` makes the skills address you by name in place of "the user".

## Help and feedback

Questions, bug reports and ideas are all welcome as an [issue](https://github.com/MapleSyrupOS/pitmaster/issues).
Most useful: a skill that loaded when it should not have (or did not when it should), a step that needed a guess,
and a word that was not explained. For anything about conduct, see the [Code of Conduct](CODE_OF_CONDUCT.md).

## New to GitHub?

- **Repository (repo):** a project's folder of files, with its full history.
- **Branch:** a separate line of work, so changes can be made without touching the main copy.
- **Commit:** one saved change, with a note saying what it is.
- **Pull request (PR):** a proposed change from a branch, waiting to be reviewed and merged.
- **Merge:** the proposed change joins the main copy.
- **Merge on green:** merge only once the automatic checks pass.
- **Issue:** a question, a bug report or a request, filed on the project's page.

## More

- [CHANGELOG.md](CHANGELOG.md): what changed in each release.
- [CONTRIBUTING.md](CONTRIBUTING.md): how to add a skill (with `bbq`, of course).
- [docs/decisions/](docs/decisions/): the decisions behind the skills.
- [LICENSE](LICENSE) (Apache-2.0) and [NOTICE](NOTICE).

Copyright 2026 Writerblockade.
