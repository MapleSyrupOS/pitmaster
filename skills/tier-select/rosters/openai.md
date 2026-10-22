# Roster: OpenAI (Codex)

**Last checked: 2026-10-16** against the Codex model page (https://learn.chatgpt.com/docs/models), the Codex config
reference (https://learn.chatgpt.com/docs/config-file/config-reference) and the API model list
(https://developers.openai.com/api/docs/models/all). Flag it after about three months.

| tier | model | default effort | notes |
|---|---|---|---|
| small | `gpt-6-luna` | high | "most efficient"; summarising, extraction, focused coding. Efforts up to Max. The only model on the Free and Go plans |
| mid | `gpt-6.1-sol` | medium or high | "recommended for complex coding and agentic work"; Plus, Pro, Business, Enterprise and Edu (Enterprise and Edu need an admin to enable it) |
| large | `gpt-6.1-sol` | xhigh or max | the same model at a higher effort |
| top | `gpt-6-astra` | low first, raised as needed | "most capable"; the vendor suggests starting at its lowest effort |

The models share the ChatGPT plan's Codex limit, one meter per plan. An API key is a separate, pay-per-use meter.

## Effort

- **The names:** Codex's picker shows Light, Medium, High, Extra High, Max and Ultra. Light is `low` in the
  config; Extra High is taken to be `xhigh`. Ultra runs subagents in parallel; treat it as above `max`.
- **Where it is set:** `model` and `model_reasoning_effort` in `config.toml` (shared by the desktop app, the CLI
  and the IDE extension); a profile per tier (`<name>.config.toml`, chosen with `--profile <name>`); `-m <model>`
  on the command line; `/model` and then "More reasoning…" interactively.
- **What a session sees:** not documented.

## Not verified

- The plan availability of `gpt-6-astra`, and the efforts each model allows (the vendor's table did not render).
- That Extra High, Max and Ultra are `xhigh`, `max` and `ultra` in the config (only Light = `low` is stated).
- How `gpt-6-sol` differs from `gpt-6.1-sol` (both are listed).
- Codex's message limits per plan.
- Retired for ChatGPT sign-in as of this date: `gpt-5.5` (2026-10-14), `gpt-5.4`, `gpt-5.4-mini`, `gpt-5.3-codex-spark`;
  `gpt-5.2` and `gpt-5.3-codex` are deprecated.
