---
name: bbq-yes-23
tags: [trigger, bbq, should-trigger]
runs: 3
max_turns: 2
timeout_seconds: 180
allowed_tools: [Skill, Read, Glob, Grep]
---
tool bbq: a command-line tool that prunes merged git branches, safe to run by hand.
