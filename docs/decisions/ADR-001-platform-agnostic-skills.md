---
status: accepted
status-note: — ratified by the owner 2026-10-16
owner: the owner
kind: architecture
built: landed
proof: "`scripts/build-variants.py`, `scripts/sync-manifests.py`, `skills/tier-select/rosters/openai.md`"
supersedes: nothing
amends: nothing
---
# ADR-001 — Platform-agnostic skills: one body, tagged platform notes, Claude and Codex native

This is the public copy of a decision I made. I've left out a few internal notes.

## Decision

pitmaster's skills work on **any tool that reads Agent Skills (`SKILL.md`)**, not only on Claude. Claude Code,
Cowork and claude.ai stay fully supported. A skill's steps say *what* to do in words every tool understands;
everything that only one platform has lives in one tagged **Platform notes** section at the bottom, which a build
script filters into per-platform variants. The repository carries **native packages for Claude and Codex**,
generated from one manifest and held in step by a CI parity check. `tier-select` reasons in **neutral tiers** that
per-vendor **rosters** turn into models, with Claude, OpenAI and Google rosters shipped and dated. Before
pitmaster goes public, every skill is smoke-run in every installed tool.

## Context

pitmaster's first release made the skills work in any project and covered Claude's surfaces. The owner asked for
the next step: work on any platform too. The premises, measured on 2026-10-16:

- The Agent Skills format is an open spec (agentskills.io, December 2025), read by Codex CLI, Gemini CLI,
  GitHub Copilot, Cursor and VS Code, among others.
- Codex CLI 0.162 reads `SKILL.md` and has its own plugin format, `.codex-plugin/plugin.json`, with the same
  core fields as Claude's plus `"skills": "./skills/"`, and a marketplace at `.agents/plugins/marketplace.json`.
- OpenCode 2.0 and Antigravity 1.3 were installed on the build machine; their skill support was unconfirmed.
- The first drafts leaned on Claude-only pieces: `AskUserQuestion`, `/context`, subagents, `gh`,
  `${CLAUDE_SKILL_DIR}`, the `/pitmaster:` namespace, Claude model names and Claude's weekly limit.

## The rules

1. **Capability words in the steps.** A step says "ask up to four questions per call, recommended option first",
   not "call AskUserQuestion". It names sibling skills by bare name (`budget-select`) and scripts by path relative
   to the skill folder. It uses no Claude-only frontmatter.
2. **One tagged Platform notes section.** The last section of every `SKILL.md` is `## Platform notes`, with one
   bullet per platform, each starting with its tag: `**Claude Code:**`, `**Cowork / claude.ai:**`, `**Codex:**`,
   `**Other tools:**`.
3. **Variants are filtered, never rewritten.** `scripts/build-variants.py` writes `dist/<platform>/<skill>/` with
   the body byte for byte and only that platform's bullet plus *Other tools*. `skills/` itself keeps every
   bullet. Its `--check` fails if a skill lacks a bullet for a listed platform.
4. **Native packages from one source.** `.claude-plugin/plugin.json` is the source of the name, version,
   description, license and skill list. `scripts/sync-manifests.py` writes `.codex-plugin/plugin.json` and
   `.agents/plugins/marketplace.json`; `--check` in CI fails on any drift. Both packages point at `skills/`.
5. **Neutral tiers, vendor rosters.** `tier-select` maps a job shape to a tier (small, mid, large, top) and an
   effort. `rosters/<vendor>.md` maps tiers to models and says where effort is set, with a "last checked" date
   that the skill flags after about three months. The first release ships `claude.md`, `openai.md` and
   `google.md` from official sources, plus `TEMPLATE.md`. With no roster for the platform in use, the skill asks
   the user which models they have and writes one. A tier may name a model from another vendor's pool.
6. **Budgets per meter.** `budget-select`'s point stays 1 % of the plan's weekly limit, read as *whatever limit
   the platform meters*, one budget per meter. Where no usage tool exists, it asks the user for the reading.
7. **Proof.** CI checks every skill against the spec (`name` matches its folder, lowercase and hyphens,
   ≤ 64 characters; `description` ≤ 1,024 characters) and fails on a Claude-only tool name in a step outside
   Platform notes. Before pitmaster goes public, each skill is run once in Codex, OpenCode and Antigravity; a tool
   that cannot load skills is recorded as unsupported in the README, not hidden.

## Alternatives

- **Capability words and fallbacks, unfiltered.** The same notes, with every platform reading every bullet.
  Simplest, no build step. Lost because the filter is a few lines and gives each platform a copy that reads
  natively.
- **A full rewrite per platform** (templated bodies). The most native reading and the most upkeep, with real
  drift risk between bodies. Kept as the **long-term goal**.
- **Every native format now** (Gemini CLI, Copilot, Cursor). None was installed to test against. Kept as the
  **long-term goal**, under the same parity check.
- **One tree and an install table** (Claude manifest only). Nothing to keep in step, but Codex users get a copy
  step instead of an install. Lost to native packages with a parity check.
- **A Claude roster only, or Claude-only skills.** Lost: tier selection should work on any platform too. The
  recommendation to ship only verified rosters and let other vendors' be filled on first use was **overruled** in
  favour of filling the OpenAI and Google rosters now.
- **A spec check plus Codex only, or a spec check only.** Lost to a smoke run in every installed tool.

## Consequences

- Every skill has a Platform notes section and no inline Claude tool names.
- The repository has `.codex-plugin/`, `.agents/plugins/`, `scripts/build-variants.py`,
  `scripts/sync-manifests.py`, a spec check in CI, and `skills/tier-select/rosters/`.
- The release build makes one zip per skill per platform from `dist/`, not one per skill.
- Three rosters need refreshing as vendors ship models; the "last checked" flag is what keeps them honest.
- Going public waits on the smoke runs as well.

## History

- 2026-10-16: proposed.
- 2026-10-16: ratified by the owner.
- 2026-10-16: built; the skills were smoke-run in Codex, Antigravity and OpenCode.
- 2026-10-22: public copy approved by the owner.
