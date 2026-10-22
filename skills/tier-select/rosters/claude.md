# Roster: Claude (Anthropic)

**Last checked: 2026-10-16** against the model list Claude Code gave its own sessions that day (Anthropic's model
overview in its developer docs is the place to re-check). Flag it after about three months.

| tier | model | id | default effort | notes |
|---|---|---|---|---|
| small | Haiku 5.5 | `claude-haiku-5-5` | low | reading, counting, digests |
| mid | Sonnet 5.5 | `claude-sonnet-5-5` | high | the default builder and lead |
| large | Opus 5.5 | `claude-opus-5-5` | high | untrusted input, memory safety, security design |
| top | Fable 5.1 | `claude-fable-5-1` | max | disputes and final passes only |

All four share the plan's usage meter in Claude Code, Cowork and claude.ai; larger models use it faster.

## Effort

- **The names:** low, medium, high, xhigh and max, as written.
- **Where it is set:** for the session, the app's effort setting or `/model` in Claude Code. For a subagent, the
  `effort:` field of its definition; a `model:` override alone inherits the lead's effort.
- **What a session sees:** the name, in the `CLAUDE_EFFORT` environment variable (`echo "$CLAUDE_EFFORT"`), which
  Claude Code documents for hooks and the Bash tool and which matched the app's setting on 2026-10-16. The
  session's own context may carry a different form of the setting (that day, *high* showed up there as 15,
  *xhigh* and *ultracode* as 40, *max* as "max"): it is not the name, so never compare it with one. *Ultracode* is
  not an effort level but a mode on top of one.

## Not verified

- The numbers a session sees in its own context for each effort were observed in one session on one day; Anthropic
  documents only that the resolved effort is rendered into the prompt, not its form.
