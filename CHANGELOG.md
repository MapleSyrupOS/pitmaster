# Changelog

All notable changes to pitmaster are recorded here. The format follows Keep a Changelog
(https://keepachangelog.com/en/1.1.0/), and versions follow Semantic Versioning (https://semver.org/).

## [Unreleased]

## [0.4.1] — private

The audit-followup arc: what the Codex value audit found, acted on in one release.

### Removed
- `defplz` (ADR-018, superseding ADR-013). Its rules (the project's meaning first, plain words, offer once to file,
  never run a command that changes anything while explaining) move to the draft opt-in rules catalogue. `defplz` and
  `whatsthat` no longer load anything.

### Changed
- Every skill: rewritten for plain reading and cut where it said things twice; the twelve SKILL.md files fell from
  19,457 to 16,511 words with every rule kept. Each skill opens with its smallest useful run and carries a
  `metadata: family:` label (plan, run, usage, check, records; ADR-004 amended). One Config intro wording in all.
- `bbq`: the plain bbq is the main file; the types, the Skill type, Cloud and Away, and Batch moved to `references/`.
  "makeskill" opens it in the Skill type, which now holds a new skill's whole life cycle (ADR-004 amended).
- `bbq`, `makeadr`, `talk-through`: a `land:` setting, `pr` (the default), `commit` or `file`.
- `makeadr`: a light route for a small decision (ADR-005 amended); says plainly that `adr-check` checks a proof
  exists, not that it is right.
- `goforit`: its skill-building steps moved to bbq's Skill type; after "ratify" it follows the ratified ADR's own
  build steps (ADR-017 amended).
- `dealers-choice`: stops when nothing worthwhile is left, instead of inventing housekeeping.
- `project-prep`: by default writes only the agent rules and STATUS.md, the rest offered in the same question; the
  bare "scaffold" trigger is gone ("scaffold this project for agents"); not for scaffolding app code (ADR-010
  amended).
- `swarm-bottleneck`: one rule for naming the constraint; "why is this slow" only loads it in a multi-agent run.
- `spend-ledger`: counts merged, opened, ratified and committed landings apart; the report reads the split.
- `budget-select`: says plainly that point estimates stay unmeasured until real runs fill its calibration.
- `tastetest`: the App Store payment check follows Apple's guideline 3.1.1(a) storefront rules instead of banning
  every outside link.
- The spec check accepts `metadata.family`; `check-all.py` skips the publisher's checks in the public repository.
## [0.4.0] — private

The shed lands (ADR-012 steps 2–4 and 6): `MapleSyrupOS/pitmaster-shed` holds wave 1's ten tools, each green on
macOS, Linux and Windows, tagged v0.1.0.

### Changed
- `makeadr`'s `adr-index.py` and `adr-check.py`, and `project-prep`'s `status-check.py`, are pinned to the shed's
  `v0.1.0` tag (they were pinned to its commit in 0.3.13); `scripts/check-pins.py` checks them.

## [0.3.13] — private

### Changed
- `makeadr`'s `adr-index.py` and `adr-check.py`, and `project-prep`'s `status-check.py`, are now byte-for-byte
  copies of their `pitmaster-shed` tools, each with a `.pin` beside it that `scripts/check-pins.py` checks
  (ADR-012 step 4). Their flags and exit codes are unchanged; their self-tests print a line per case and a verdict
  line. `adr-check` and `adr-index` carry the code they shared (`adr_common.py`, `adr_triggers.py`, and adr-plus's
  reader) inside each script, so those two helper files are gone.
- `status-check` reads `status_sections` from `pitmaster.md` (or `--sections`): the STATUS sections whose bullets
  must each cite a file. The default is still Now, Next and Known debt.

## [0.3.12] — private

### Added
- `makeadr` carries a copy of the adr-plus 0.1.0 release (`skills/makeadr/adr-plus/`: the schema, the header reader,
  the converter with its lossless proof, fixtures and manifest), pinned to the `v0.1.0` tag of `MapleSyrupOS/adr-plus`
  in `skills/makeadr/adr-plus.pin`; `scripts/check-pins.py` (ADR-012 step 2) fails, naming the file, when the copy
  drifts (ADR+ spec S7, ADR-005 step B).
- The ADR+ trigger check in `adr-check.py`: two or more options weighed needs Drivers, Good and Bad bullets and a
  chosen reason; a Drivers list on a one-option ADR is padding (ADR-003). `--triggers-skip N,N` names ADRs whose ruled
  text predates the check.

### Changed
- ADR headers are YAML (ADR+ spec 1.3). `adr-check.py` checks them against the schema (the seven lowercase status
  words, a required Kind) and fails a bold-line header, naming the converter; `adr-index.py` reads them and adds a
  Kind column. pitmaster's own ADRs (001 to 017) moved to the YAML header, proved lossless. `templates/adr-plus.md`
  is the new shape.

## [0.3.11] — private

### Added
- `bbq`: a Batch mode (ADR-015). Any type can run as a batch ("batch skill bbq", "batch adr bbq"): the lead asks
  every item's questions in one sitting, and each item's builder starts as soon as its questions are done, in its
  own worktree and at the tier `tier-select` picks for that item. Builders are not capped: by default the batch
  loads `budget-select` and says its expected usage first, and `spend-ledger` records it (`batch_usage`). No two
  items may conflict; the lead hands out ADR numbers and lands the shared changes once, in one PR. The batch round
  opens with how many items, then how many questions per item; then, at the default `batch_format: ask`, every
  batch asks for by size (rounds at 8 per item or fewer, a worksheet at 9 or more; on top, naming its pick),
  rounds, a worksheet per item or one for the batch; set to one of them, it stops asking. A worksheet is a form in
  the chat where the app can draw one, a file otherwise or on request (`batch_sheet`). "multitask" loads bbq,
  which asks "Batch bbq?" first. Three trigger cases.

## [0.3.10] — private

### Changed
- `goforit`, `bbq`, `makeadr`: goforit is offered only when every question still to come can be answered with a
  citation (a record's question, an ADR, the user's words); the option says what it rests on, and each answer
  taken on goforit is recorded with its citation (ADR-017, amendment of 2026-10-22).

## [0.3.9] — private

### Added
- `goforit` (ADR-017): typed after bbq, makeadr or talk-through (or on its own after one), it carries the plan on
  into the build, here or by a worker, and stops for "ratify", then merge. "goforitreally" adds carte blanche with
  merge on green, so the only stop is "ratify", after a size check. Nine trigger cases.

### Changed
- `bbq`, `makeadr`: `goforit` is offered where the count is asked and where more questions are offered, only when
  the agent judges it already knows enough. Pointer lines in bbq, makeadr, talk-through, tier-select and
  carte-blanche no longer call goforit a draft.

## [0.3.8] — private

### Added
- `tastetest` (ADR-016): a blind auditor gets only what an outsider would see, tries it, and reports READY or NOT
  READY with findings ranked blocks / should fix / nice. Profiles `repo` and `app-store` (dated; checked against
  Apple's live guidelines each run). `scripts/blind-copy.py` and `scripts/seeded-fixture.py`, each with a
  self-test in `check-all`. Eleven trigger cases.

### Changed
- `bbq`: its Claude Code notes say to put everything needed to answer into the questions themselves (option
  previews may not reach the user), and that anything the session says it made for the user is sent as a file or
  linked in the same message.
- `bbq`, `makeadr`, `talk-through`, `tier-select`, `carte-blanche`: pointer lines to two drafts, `tastetest` (a
  blind public-readiness audit) and `goforit` (carries a plan on into the build, stopping at "ratify"), whose
  ADRs are still to come.

## [0.3.6] — private

### Added
- `talk-through` (ADR-014): an open conversation in voice or text that tracks decisions, open questions, action
  items and corrections, and on the user's word writes one record, each decision marked agreed, proposed or open
  and cited to where it came up. Eleven trigger cases.

### Changed
- `bbq`, `makeadr`, `project-prep`, `defplz`: pointer lines to `talk-through` (ADR-004's sibling rule); `defplz`'s
  line now names `talk-through` where it named `talk-it-through`.

## [0.3.5] — private

### Added
- `defplz` (ADR-013): defines a term in plain words, project first, at the length a word after the opener asks
  for ("defplz more ssh"), and offers once to file it in the glossary, in A–Z order. `whatsthat` also loads it.
  Eleven trigger cases.

### Changed
- `bbq`, `makeadr`, `project-prep`: pointer lines to `defplz` (ADR-004's sibling rule).

## [0.3.4] — private

### Changed
- `dealers-choice`: says "local models" where it said "the local lanes", the word `tier-select` uses; the
  `local-lanes` skill keeps its name.

## [0.3.3] — private

### Changed
- `carte-blanche`: a widened grant reaches workers only in a fresh brief quoting the user, never by relayed
  message (a narrowing goes by any route); no grant widens shared-machine safety (stop only your own process, by
  its id; remove only your own files; fast-forward only, never force), and the written grant says so; spend is
  counted from a ledger kept from the first worker, the shared meter only the hard stop; a lead short of context
  hands off with the grant and the ledger (ADR-007 amendment 2026-10-21).
- `dealers-choice`: question 2 asks which machines a swarm may use; long lists are gathered by small readers; a
  pick is checked still open on the main branch before it goes out; picks that touch the same files go to one
  worker (ADR-008 amendment 2026-10-21).
- Both from the first real run of the pair, the reference project's debt run
  (`docs/field-reports/2026-10-20-reference-project-debt-run.md`).

## [0.3.2] — private

### Added
- `project-prep`: gets a new or existing project ready for agents. One round of questions, then whatever is
  missing of the agent rules (`AGENTS.md`, with a `CLAUDE.md` pointer), a `STATUS.md` in the reference project's
  shape (Now, Next, Known debt, Log, How this file is kept) with its log, debt and archive files, a glossary,
  proposals and decisions folders and a `pitmaster.md`, from built-in templates. Never overwrites a file; commits
  on a branch. `scripts/status-check.py` checks the line ceiling and that every claim cites a file that exists.
  Ends by offering `makeadr` for the project's first decision, where ADR+ is offered first. It replaces the
  unmerged `setup-project` (PR #4) (ADR-010).
- Trigger evals for it, from the 16-question record `docs/bbq/2026-10-20-project-prep.md`.

### Changed
- `bbq` and `makeadr` name `project-prep` in their Sibling lines (ADR-004 amendment).
- The repository moved to `MapleSyrupOS/pitmaster`; install lines and manifests point there.

## [0.3.1] — private

### Changed
- `bbq`: the Skill type adds the pointer line back to each sibling the new skill names, in the same PR
  (ADR-004 amendment). The skill template carries the same note.
- From this version on, any change to a file under `skills/` bumps at least the patch version, so an installed
  plugin picks it up with a plain update.

## [0.3.0] — private

### Added
- `spend-ledger`: what a session spent beside what it landed, one append-only row per session; tokens read from
  Claude Code and Codex transcripts, the meter read before and after (on Codex, from the transcript), points
  estimated by list-price share when other sessions overlapped, and a report of cost per landing (ADR-009).

### Changed
- `budget-select`: points at `spend-ledger` for its calibration row's token figures; the use-it plan proposes
  daily whatever the headroom.
- `carte-blanche` and `bbq`: a bbq run under carte blanche answers its own questions, each with a `veto:` line
  (ADR-007 amendment).

## [0.2.0] — private

### Added
- `carte-blanche`: standing authority for one session, inside the project's rules and the platform's safety
  rules. Picks work, pushes branches, opens PRs and spends a set budget without asking; merging, main, deletes and
  outward-facing acts only by a named grant; taste, ratification and charters never. A line per landing and an end
  summary with veto lines (ADR-007).
- `dealers-choice`: the agent picks the work after four questions (carte blanche? usage and swarm? off-limits?
  who leads?), ranks by what unblocks, then value per point, and keeps picking until the stop (ADR-008).
- Trigger evals for both, from the 40-question record `docs/bbq/2026-10-20-carte-blanche.md`.

## [0.1.0] — private

### Added
- Five skills, each written for any Agent Skills tool with a tagged *Platform notes* section (ADR-001):
  - `bbq`: a Big Batch of Questions, with nine types including the new Skill type, a configurable ending, and a
    guide to adding your own type.
  - `makeadr`: ADRs from a question session; three templates (pitmaster's own, MADR, Nygard); stdlib scripts
    `adr-index.py` and `adr-check.py`.
  - `swarm-bottleneck`: one binding constraint from a generic menu, with an optional hosts section.
  - `budget-select`: a run's share in points (1 % of the weekly limit by default), one budget per meter.
  - `tier-select`: neutral tiers by job shape, a lead table, and dated rosters for Claude, OpenAI and Google.
- Native packages for Claude Code and Codex, generated from one manifest and checked for parity in CI.
- Pseudonymized examples: the original skills, the build's own question record, a run record, an ADR, and a
  demo-project walkthrough for each skill.
- A scrub guard: `scripts/check-leaks.py` with a private denylist, as a pre-commit hook and in CI.
- Release zips per skill and per platform, built by a GitHub Action on each tag.
- Trigger evals for every skill, and a guide from Cowork to Claude Code.
- `bbq` and `makeadr` keep an **Owed** list and report it after every round, so more questions are seen coming
  (found by the second-project run, `docs/bbq/2026-10-16-skill-local-lanes.md`).
- Platform smoke runs: every skill in Codex, Antigravity and OpenCode, 15 of 15 as specified
  (`docs/tests/2026-10-16-platform-smoke.md`).
- Drafts, not loaded by the plugin: `prompt-pack` (the bake-off winner, `docs/bake-off-2026-10-16.md`) and
  `local-lanes` with a small local-model runner.
- The readability quiz (`scripts/readability-quiz.py`, `docs/readability-quiz.md`).
