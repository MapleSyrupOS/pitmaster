# Contributing to pitmaster

Contributions are welcome: new skills, new bbq types, fixes, rosters for more vendors, and better examples.
Everyone taking part follows the [Code of Conduct](CODE_OF_CONDUCT.md).

## Add a skill: make it with bbq

1. Install pitmaster (see the README) and run **`/pitmaster:bbq`** (or "bbq" in any tool), choosing the **Skill**
   type. It asks about the skill you want, then writes the skill folder and its trigger prompts.
2. Put the folder in `skills/<name>/` and the question record in `docs/bbq/`.
3. Open a pull request with **the skill and its record together**. The record lets reviewers trace each rule to
   the question that set it.

## The shape every skill follows

- **Frontmatter:** `name`, `description` and `metadata: family:` (plan, run, usage, check or records). The name is lowercase letters, digits and hyphens, matches the
  folder, and is at most 64 characters. The description says what the skill does and when to use it, with the
  phrases that should trigger it, in at most 1,024 characters.
- **Steps in plain words.** Say what to do ("ask up to four questions per round"), not which tool to call. Name
  sibling skills by their bare name (`budget-select`), and scripts by their path in the skill folder.
- **A closing `## Platform notes` section** with one bullet per platform, each starting with its tag:
  `**Claude Code:**`, `**Cowork / claude.ai:**`, `**Codex:**`, `**Other tools:**`. Anything only one platform has
  goes here, never in the steps ([ADR-001](docs/decisions/ADR-001-platform-agnostic-skills.md)).
- **A config block** near the top for settings a user may change, with `pitmaster.md` at the project root as the
  override.
- **Scripts:** Python 3.8+ with the standard library only, and a `--self-test` that includes a deliberate failure
  the test must catch. The skill says what it does when Python is not there.
- **Trigger evals** in `evals/`: at least five prompts that should load the skill and three that should not
  (the bigger skills have more).

## Before you open a pull request

Install the leak check as a pre-commit hook once per clone:

```bash
git config core.hooksPath scripts/hooks
```

Then run what CI runs:

```bash
python3 scripts/check-all.py
```

It checks for personal details (home paths, emails, IP addresses, tokens), that every skill meets the spec and
has its platform notes, that the Claude and Codex manifests agree, that every pinned copy matches its pin, and
that pitmaster's published decisions pass its own ADR checks.

**Keep examples anonymous.** People in examples are Alex and Sam (they/them); machines are `alpha`, `bravo`,
`charlie`, `delta` and `gpu-box`. Never commit a real name, machine, account or home path. If you keep a private
list of your own names and hosts in `~/.config/pitmaster/denylist.txt` (one per line, outside the repository), the
leak check reads it too.

## Releases

Maintainers tag `vX.Y.Z` after updating `CHANGELOG.md` and the version in `.claude-plugin/plugin.json` (then
`python3 scripts/sync-manifests.py`). The release workflow builds one zip per skill per platform.

## License

By contributing, you agree that your contributions are licensed under the Apache License 2.0, as the rest of the
project is.
