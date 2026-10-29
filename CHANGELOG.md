# Changelog

All notable changes to pitmaster are recorded here. The format follows Keep a Changelog
(https://keepachangelog.com/en/1.1.0/), and versions follow Semantic Versioning (https://semver.org/). pitmaster is
young: expect changes between minor versions until 1.0.

## [Unreleased]

## [0.4.31] — 2026-10-29

### Added
- project-prep also starts on "projectprep" (and "projectprepreally"), with a trigger eval.
- README: a section under the opening, "Use Pitmaster to start a project or help with an existing project", with
  the permissions note as a Warning box, "Is Pitmaster installed?", and the two ways in (projectprep or bbq).
- README: example prompts in "Your first five minutes" (renamed from "Start here (five minutes)"), sorted into
  project-prep first, could be either, and just a bbq.

### Changed
- README: the three skill lists ("What to say", "Start with these four", "The skills") are one list in five groups;
  each skill's plain-words sentence now heads its row.
- README, after a blind audit by Gemini 3.8 Flash and Codex: a bbq needs no extra tools; how to type a skill (word or
  `/pitmaster:` form); what "really" and "tres" add; restart and a "did it work?" check after installing; the folder
  projectprep works in; "comrun" links to its meaning; the shed's tools fold away by who they're for.
- README: the Warning box is one plain line, with the full paragraph moved to "How far each word lets the agent go";
  "Is Pitmaster installed?" says what to do next; "Where to start" is now "More ways to have a bbq", with its
  shorthand spelled out; the veto line says the agent does the undoing.
- README, after a second blind audit: merging needs your permission, given each time or ahead with a word; "install
  it first" goes to the friendly install routes; restart and "just ask" in Install; where Codex's terminal is; how to
  open your agent in a folder; "open source" beside Apache-2.0; Configure says every setting has a default.
- README: a copyable bbq example at the top; the shed paragraph moves below the two ways in; project-prep's row says
  to type `projectprep`; carte-blanche's notes let you ask for a call to be undone.
- README pictures in the beta banner's pixel style, light and dark, lettered in MapleSyrup OS's Maple UI faces
  (Terminus, OFL): the two cards for projectprep and bbq, the examples as three windows (stacked on narrow screens,
  with the same examples to copy beneath), a bbq chat, and the authority staircase, its steps coloured from teal to deep red by how much each word lets
  the agent do alone (`docs/assets/readme-*.svg`).

## [0.4.30] — 2026-10-29

### Changed
- makeadr says in one line when it chooses to amend an ADR the user did not ask to amend ("This amends ADR-14 to
  clarify its scope; say if it should be a new ADR instead."), then carries on without waiting (ADR-005, amendment
  of 2026-10-29).

## [0.4.29] — 2026-10-28

### Added
- A public-beta banner at the top of the README, a pixel window in light and dark versions
  (`docs/assets/beta-banner-light.svg`, `docs/assets/beta-banner-dark.svg`): "Under construction — public beta.
  Skills, names and commands may still change."

### Changed
- README: the "Where to start" paragraph (have a bbq) moves up, above Contents; Platform support lists each skill
  and where it has been tried, in place of grouped counts.
- setfree and bbq's Tool type say in short what the private ADR-011 and ADR-012 they cite decide.

## [0.4.28] — 2026-10-27

### Changed
- The README catches up with the sixteen skills and the shed's fifteen tools: the shed table adds `adr-public`,
  `looseends-scan`, `neighbour-check`, `neighbours` and `record-check`, and says which skill carries which tool;
  the Claude Code skill list adds townhall and neighbour-check. The starter guide's skill count reads sixteen.
- The plugin's description names townhall, and the Claude marketplace's names townhall, neighbour-check and
  setfree.

## [0.4.27] — 2026-10-27

### Changed
- neighbour-check's `neighbour-check` and townhall's `neighbours` copies are pinned to pitmaster-shed's `v0.3.0` tag,
  which holds the commit they were pinned to. The files are unchanged; only their pins move.

## [0.4.26] — 2026-10-27

### Added
- **neighbour-check** (ADR-029): before a session sends work to a neighbour on townhall's allow list, it
  reads what limits each one (Codex's 7-day meter, reset and burn; another Claude account's newest reading; Go's raw
  floor; Ollama's and OpenAI-wire servers' models; a project's lane queue; a guard over ssh) and whether it is busy,
  asks the user for the readings no file holds (agy, Go's weighted pool), and writes a Neighbours block. Every kind
  and setting is editable: the skill's Config, the neighbours doc's `## neighbour-check` section, `pitmaster.md`, or a
  flag. Its script is a pinned copy of pitmaster-shed's `neighbour-check`. "checkonneighbours" loads it too.

### Changed
- spend-ledger's close (step 5) leaves the closing usage reading in `~/.claude/meters.tsv` through neighbour-check's
  `record`, so the user's other accounts see how this one ended.
- budget-select, tier-select, townhall and spend-ledger name neighbour-check in their Sibling lines.
- townhall's `neighbours` copy is re-pinned to the same pitmaster-shed commit: the shed's file gained two
  marker lines around the doc reader neighbour-check shares, and nothing else changed.

## [0.4.25] — 2026-10-24

### Changed
- The five shed copies pinned to a commit (makeadr's `adr-public`, looseends' `looseends-scan`, townhall's
  `neighbours` and `record-check`, talk-through's `record-check`) are pinned to pitmaster-shed's `v0.2.0` tag. The
  files are unchanged; only their pins move.

## [0.4.24] — 2026-10-24

### Fixed
- A public ADR copy keeps its Context's **Drivers list** (makeadr's `adr-public`, re-pinned from pitmaster-shed #6).
  adr-check asks for that list wherever two or more options are weighed, and the copies had lost it, so 0.4.23's
  public CI failed on seven of them (ADR-014, 021 to 026).
- `scripts/publish.py` gains a **ci** check: the dry run and `--publish` run the copy's own `check-all.py`, the
  command the public repository's CI runs, so a tree that would go out red stops before it goes out.

## [0.4.23] — 2026-10-24

### Changed
- The noun "voyage" is now **comrun** (short for "commissioned run") in every skill, the README, the starter guide
  and the glossary, at the owner's ruling after three townhall rounds and trigger tests of five words. It counts
  only as comrun, com-run, com run, commission run or commissioned run; "voyage", "runlap" and "run-lap" are no
  longer named. budget-select, spend-ledger, swarm-bottleneck and tier-select name all five forms in their
  descriptions; bbq, carte-blanche and dealers-choice, which load on their own words, say "comrun". ADR-007, 008
  and 009 amended; their public copies re-drafted for the release review. Trigger cases: four now use the new
  forms, and `spend-ledger-yes-08`, `spend-ledger-no-06` and `budget-select-no-05` are new.
- `carte-blanche` and `dealers-choice`: the end summary and end report name the work a comrun ("Finished the
  comrun: …"), at the owner's word.

## [0.4.22] — 2026-10-24

### Changed
- `goforit`: plain goforit sizes itself like goforitreally (`warn_at`; go, trim or back out above it) and starts as
  many subagents as its estimate allows, not two. goforitreally fixes only what the plan can't land without, inside
  the plan's PR, and writes anything else down (ADR-025).
- `carte-blanche`: nearby fixes, needed by the plan or not, are carte blanche's (ADR-025).
- `dealers-choice`: tresdealers-choice asks first before reaching a project not named (ADR-025 rule 4).

## [0.4.21] — 2026-10-24

### Added
- `bbq` gains a **Tool** type for a tool a person runs without an agent ("tool bbq", "shedtool bbq", or the opener
  "maketool"): ten things to cover, a `tools_home` config line, and a life cycle of record, ADR, then the build
  offered (ADR-026). Three trigger cases.

### Changed
- `townhall`'s record ends with the usage where it is reported, in small print, for the record only (ADR-024,
  amendment of 2026-10-24).
- `bbq`'s Skill type offers the move into the shipped skills folder after ratification instead of making it
  (ADR-004, amended by ADR-026).

## [0.4.20] — 2026-10-24

### Changed
- `makeadr` makes the public ADR draft silently when `public_adr: on`: no chat notice; a supersede's queued
  withdrawal gets one short line in the PR body (ADR-020, amendment of 2026-10-24).

## [0.4.19] — 2026-10-24

### Added
- `townhall`, the fifteenth skill (ADR-024): agents argue a decision, a verdict or an attack-and-defend review in
  rounds while the lead, who never argues, judges and recommends; "familymeeting" seats subagents of the lead's own
  model family. Its scripts are pinned copies of two new pitmaster-shed tools: `neighbours` (reads
  `~/.pitmaster/neighbours.md` and says who answers) and `record-check` (checks a record's decisions tables).
  12 trigger cases in `evals/`.

### Changed
- `talk-through` carries a pinned `record-check` and runs it on its record at the wrap, where Python runs; how it
  writes is unchanged (ADR-014, amended by ADR-024).
- `makeadr`, `talk-through`, `budget-select` and `tier-select` no longer call `townhall` a draft.

## [0.4.18] — 2026-10-24

### Changed
- `makeadr`, `talk-through`, `budget-select` and `tier-select` name the `townhall` draft in their Sibling lines: agents
  argue a decision or a verdict in rounds and the lead, who never argues, judges (bbq record
  `docs/bbq/2026-10-24-skill-townhall.md`; the skill is a draft until its ADR is ratified).

## [0.4.17] — 2026-10-23

### Fixed
- `tastetest`'s `blind-copy.py` matches list lines the way `scripts/publish.py` does, so a trailing `**`
  (`examples/**`) takes everything under its folder instead of matching nothing, and `[seq]` classes work. A list's
  copy never includes makeadr's pending drafts of public ADR copies (`docs/decisions/public/pending/`), and a line
  that names only drafts is a finding. Its self-test's `--break history` now reddens only the history arm. Two new
  guards, `glob` and `pending`, each red by name.

## [0.4.16] — 2026-10-23

### Added
- `dealers-choice` takes a topic: "dealer's choice docs" picks only among candidates about the docs, says so in one
  line, and asks whether to widen to the whole project when nothing about the topic is left. A trigger case checks
  it.

## [0.4.15] — 2026-10-23

### Fixed
- `project-prep` writes a new project's `CLAUDE.md` as the one line `@AGENTS.md`, which Claude Code reads as an
  import, so the rules load at the start of every session. It used to write a sentence asking Claude to read
  `AGENTS.md` first, which reached the rules only if Claude followed it. pitmaster's own `CLAUDE.md` made the same
  change (#74).

## [0.4.14] — 2026-10-23

### Changed
- **The grant ladder.** goforit, goforitreally, carteblanche and trescarteblanche are one ladder, each word allowing
  everything the one before allows (ADR-023, proposed). `carte-blanche` now merges its own PRs once the checks are
  green, with no "merge on green" to name; it estimates its own budget and asks only above 10 points; it may close a
  stale PR with a comment and change a build host with the undo written down, in this project. `goforit`'s
  "goforitreally" is the middle rung: it builds the plan and what it pulls in and merges on green, but is no longer
  carte blanche. Plain goforit starts at most two subagents and parks new calls mid-build.
- `dealers-choice`'s first question drops "Yes, plus merge on green" and offers trescarteblanche.

### Added
- **tres- for the projects you name.** "trescarteblanche", "treslooseends" and "tresdealers-choice" do what
  carte-blanche, looseends and dealers-choice do, across every project named with the word ("trescarteblanche
  pitmaster and maplesyrup os"). Named projects start with no wait; reaching any other asks first; with none named
  the agent lists them and waits for one yes. tres- widens where the agent works, never what it may do. Each skill
  gains a tres section, and four trigger cases check the words.
- **-really: all the way through.** Run on to a skill's word, "really" finishes instead of stopping at a report or
  an offer, and merges its own PR once the checks are green; never past ratify, taste, public acts, pushing to main
  or deleting work. "tastetestreally" fixes the findings and re-audits until READY (at most three rounds);
  "looseendsreally" ties off its own share without asking; "project-prepreally" merges its set-up branch;
  "talk-throughreally" merges the record's PR after the wrap; the prompt-pack draft's "prompt-packreally" starts the
  session it wrote. goforitreally keeps it. Only the run-together word counts. Four more trigger cases.

## [0.4.13] — 2026-10-23

### Added
- **Three more rules, each with a list the project keeps.** `run` gains "give every scheduled task one home
  account", kept in `docs/rules/task-homes.md`; `records` gains "leave each hot file to its named writer"
  (`docs/rules/hot-files.md`) and "add each trap a tool sets to a list" (`docs/rules/tool-traps.md`). The catalogue
  holds 30 rules and none is held back. Switching on a group with one of these rules, at setup or later, writes its
  empty list from a starter in project-prep's `templates/` on the same yes; a list already there is never
  overwritten, and switching the group off leaves it. `scripts/check-rules.py` checks that every list a rule names
  has its starter (ADR-022, amendment of 2026-10-23).

## [0.4.12] — 2026-10-23

### Fixed
- `carte-blanche` and `dealers-choice` load again for plainer asks that also name the work, such as "full authority
  for this session: land what you can on the refactor" or "you pick what to work on next in this repo and do it".
  The agent used to look around the project first and never reach the skill; each description now says to load it
  first, before looking around or reading any file, even when the message names work not found yet or names the
  repository. They also say what does not load them: a "your call" on one choice, or an ask only to recommend.

## [0.4.11] — 2026-10-23

### Fixed
- tastetest's `scripts/blind-copy.py --list` reads overlay lines (`<pattern> -> <folder>/`) as pitmaster's
  `publish.py` does, copying each file a line matches to `<folder>/` plus its name. Before, each such line read as
  one glob that matched nothing, so a list with overlay lines stopped the copy. A malformed overlay line, or two
  files copied to one path, is a finding; the self-test gains an `overlay` arm.

## [0.4.10] — 2026-10-23

### Changed
- The skills say **voyage** where they said "run" for one stretch of work handed to agents, as the README does:
  "run" is an everyday verb in coding requests, so a description built around it could load a skill by accident.
  "Runlap" and "run-lap" mean the same, and the descriptions that name a voyage say so. Where "run" meant one use
  of a skill ("the smallest useful run"), it now says "use"; verbs, CI runs and dry runs are unchanged. New trigger
  cases check that everyday "run" ("run the tests") loads nothing and that "voyage", "runlap" and "run-lap" load
  the skill they name. The glossary defines voyage.
- ADR-007, ADR-008 and ADR-009, whose wording the carte-blanche, dealers-choice and spend-ledger descriptions
  carry, each gain a dated amendment for the new word (ADR-009's ruled trigger now reads "what did this voyage
  cost"). Their public copies are re-drafted into `pending/` for the next release review.

## [0.4.9] — 2026-10-23

### Changed
- tastetest's title is plain: "a blind readiness check before anything goes public".

## [0.4.8] — 2026-10-23

### Added
- **Rules.** `project-prep` now carries an opt-in catalogue of 27 one-line rules in six groups (`plan`, `run`,
  `check`, `records`, `plain`, `craft`) in its `rules/` folder. Setup asks which groups to switch on, with `plain`,
  `plan` and `check` ticked, and copies their lines into a marked Rules section of the project's `AGENTS.md`. Say
  "switch on the plain rules" or "which rules are on?" to change or see them later; project-prep touches nothing in
  `AGENTS.md` outside that section, and a project's rules change only on your yes (ADR-022).

### Changed
- The README is rewritten, mostly in the owner's own words: a new opening, an easier start ("have a bbq"), a section
  for readers new to agents, rules and skills, click-to-open install routes (including one for the shed's tools on
  their own), a plain line for what each skill means, and an About Pitmaster section in the author's voice in place of
  How it happened. The words section says which words come with AI agents, which are Git's and GitHub's, and which
  are Pitmaster's own. "Voyage" now names one stretch of work handed to agents, and the README no longer promises
  voice for talk-through.
- The starter guide's words are rewritten the same way, with new panels for talk-through, tastetest, looseends and
  setfree, and one panel that shows goforit, goforitreally, carte-blanche and trescarteblanche as a ladder.

## [0.4.7] — 2026-10-23

### Added
- **bbq's stew mode**, for thorough, back-and-forth sessions: say "stew bbq" ("stew skill bbq", "stew adr bbq";
  also "stewbbq", "stew-bbq", "bbq stew", "bbqstew", "bbq-stew") and the questions come in blocks sized to the
  count, each block re-planning the next. On a wording job, your own answers come back beside a light polish for
  you to pick, and the settled lines go into the document as you go (ADR-021, proposed). Under carte blanche a
  stew is answered by a subagent. "Let me stew on it" never starts one.

## [0.4.6] — 2026-10-23

### Changed
- `looseends`' scan is now a pinned copy of the shed's `looseends-scan` (ADR-012): its output is written as UTF-8,
  so a project's own text cannot crash a narrow console, and its self-test gains a case for Windows line endings.

## [0.4.5] — 2026-10-23

### Added
- **setfree**, the fourteenth skill: release day. It shows every public ADR copy waiting for review, so you approve
  or hold each, offers a blind tastetest, then works through your release checklist and stops at every public act
  for your word (ADR-020).
- makeadr carries **adr-public**, a pinned shed tool. With `public_adr: on`, each ADR made, ratified, amended or
  superseded also gets a public draft in `docs/decisions/public/pending/`, which never publishes until it is
  approved (step 5, part 5).
- project-prep offers a *public drafts* piece, which writes `public_adr: on`.

### Changed
- makeadr, tastetest and spend-ledger name setfree in their Sibling lines.

## [0.4.4] — 2026-10-23

### Added
- `looseends`: finds what was left unfinished in this chat, across the project, or around one ADR or topic
  (questions never answered, promises not kept, calls waiting on you, work never landed), checks each is still
  open, lists them by who acts and offers to tie them off. It runs only when asked. `scripts/looseends-scan.py`
  lists a project's markers with `file:line` and runs without an agent; check-all runs its self-test.

### Changed
- `bbq`, `dealers-choice`, `goforit`, `makeadr` and `talk-through` name `looseends` as a sibling.

## [0.4.3] — 2026-10-22

### Fixed
- `scripts/check-leaks.py` checks every file when run outside a git checkout (a downloaded ZIP), instead of
  reporting 0 files as clean, and exits 2 when it found nothing to check.
- Every built skill folder and release zip carries `LICENSE` and `NOTICE`, as Apache-2.0 asks of redistributed
  copies.
- `tastetest`'s example names a neutral project.

### Changed
- README: says where each command is typed (Claude Code's chat box or a terminal), how to sign `gh` in, that
  Python 3.8+ runs the optional scripts, and that `pitmaster.md` keys are shared across skills.
- CONTRIBUTING: a new skill is proposed with its ADR (`makeadr`), drafted in `drafts/`, and moves into `skills/`
  once a maintainer ratifies it; the sixth family, `craft`.
- check-all runs `spend-ledger`'s self-test; a `.gitignore` is published.

## [0.4.2] — 2026-10-22

The first public release.

### Skills

Twelve skills in five families, for Claude Code, Codex, Cowork and claude.ai, and any tool that reads the Agent
Skills format:

- **Plan the work:** `bbq` (a Big Batch of Questions before work starts), `makeadr` (decision records, with proof
  of what was built), `talk-through` (an open conversation, then one record of what was decided).
- **Run it:** `dealers-choice` (the agent picks the work), `carte-blanche` (standing authority for one session,
  with a veto line for every call), `goforit` (carries a settled plan into the build), `tier-select` (which model
  and effort for each job).
- **Watch the usage:** `budget-select` (a run's share of your usage, with stop lines), `spend-ledger` (what a
  session spent beside what it landed), `swarm-bottleneck` (what is slowing a multi-agent run).
- **Check it before it ships:** `tastetest` (a blind audit: READY or NOT READY).
- **Set the project up:** `project-prep` (agent rules and a STATUS file whose claims cite files).

### Changed, from the private versions before it

- `budget-select`'s calibration log, `bbq`'s own-types file and `tier-select`'s rosters for new vendors now live in
  your project (`docs/budget-calibration.md`, `docs/bbq-types.md`, `docs/tier-rosters/`), so an update never
  overwrites them. The calibration log ships empty.
- `talk-through` also loads for "chitchat".
- `makeadr` and `project-prep` carry pinned copies of `pitmaster-shed` 0.1.0 tools (`adr-index`, `adr-check`,
  `status-check`); `scripts/check-pins.py` fails if a copy drifts.
- The decisions behind the skills are published as public copies in `docs/decisions/`, with their index, and
  pass pitmaster's own ADR checks.
- A Code of Conduct (Contributor Covenant 2.1), a help and feedback section, and a plain warning that some skills
  push, open pull requests and merge.
