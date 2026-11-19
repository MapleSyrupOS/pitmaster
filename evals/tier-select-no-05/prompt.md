---
name: tier-select-no-05
tags: [trigger, tier-select, should-not-trigger]
runs: 3
max_turns: 2
timeout_seconds: 180
allowed_tools: [Skill, Read, Glob, Grep]
---
call-escalator: the installer has hung twice on the same step, get a stronger model on this.
