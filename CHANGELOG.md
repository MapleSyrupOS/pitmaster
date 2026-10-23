# Changelog

All notable changes to pitmaster are recorded here. The format follows Keep a Changelog
(https://keepachangelog.com/en/1.1.0/), and versions follow Semantic Versioning (https://semver.org/). pitmaster is
young: expect changes between minor versions until 1.0.

## [Unreleased]

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
