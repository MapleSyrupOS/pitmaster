# Roster: Google (Gemini, Antigravity)

**Last checked: 2026-10-16** against the Gemini API model list (https://ai.google.dev/gemini-api/docs/models), the
Gemini 3.8 Flash page (https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash), the latest-model page
(https://ai.google.dev/gemini-api/docs/latest-model), and Antigravity's models and plans pages
(https://antigravity.google/docs/models/, https://antigravity.google/docs/plans). Flag it after about three months.

| tier | model | default thinking | notes |
|---|---|---|---|
| small | `gemini-3.5-flash-lite` | low | API only; Antigravity's picker has no Flash-Lite, so use `gemini-3.8-flash` at Low there |
| mid | `gemini-3.8-flash` ("Gemini 3.8 Flash") | medium | "most intelligent Flash", for long software tasks and agents; every Antigravity plan |
| large | `gemini-3.8-flash` at High, or `gemini-3.1-pro-preview` | high | Pro is Enterprise-only in Antigravity |
| top | `gemini-4-argon` ("Gemini 4 Argon") | high | the flagship, 1M context; Antigravity on AI Pro (paid), Ultra and Enterprise |

Antigravity meters **two pools separately**: the Gemini pool and the third-party pool (Claude and GPT models),
each with a weekly limit and a five-hour limit, shown as remaining percent. Each pool is its own meter for
`budget-select`. Antigravity's picker also offers Claude Sonnet 5.5 and Opus 5.5 from the third-party pool; use
`rosters/claude.md` for those.

## Effort

- **The names:** the thinking level is low, medium or high. There is no xhigh or max: use high. `minimal` and a
  numeric thinking budget are refused by the newest models.
- **Where it is set:** the API's `thinking_level`; in Antigravity, the model picker under the prompt box (it
  persists for the conversation); in the Antigravity CLI (`agy`), the `/effort` command, with `/usage` for quota.
- **What a session sees:** not documented.
- "gemini-3.8-flash-high", "-medium" and "-low" are not model ids: they are the picker's thinking levels.

## Not verified

- Whether Gemini 4 Argon is on the AI Pro plan: Antigravity's pages say yes (paid), the API's latest-model page
  says it is not on AI Pro. This is probably API against Antigravity; check your plan.
- The Antigravity CLI's model flag and its `/effort` options are not documented in what was read.
- Gemini CLI: its successor for unpaid and Google One users is the Antigravity CLI from 2026-06-18, per
  geminicli.com (not an official Google domain); Gemini CLI's own model docs were out of date.
