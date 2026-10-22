---
name: makeadr-no-02
tags: [trigger, makeadr, should-not-trigger]
runs: 3
max_turns: 2
timeout_seconds: 180
allowed_tools: [Skill, Read, Glob, Grep]
---
Summarize the three newest ADRs in docs/decisions for me.
