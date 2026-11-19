---
name: call-escalator-yes-01
tags: [trigger, call-escalator, should-trigger]
runs: 3
max_turns: 2
timeout_seconds: 180
allowed_tools: [Skill, Read, Glob, Grep]
---
call-escalator: the installer still hangs after two tries.
