---
name: bbq-no-12
tags: [trigger, bbq, should-not-trigger]
runs: 3
max_turns: 2
timeout_seconds: 180
allowed_tools: [Skill, Read, Glob, Grep]
---
Run the build overnight and tell me in the morning if anything broke.
