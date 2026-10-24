---
name: bbq-yes-22
tags: [trigger, bbq, should-trigger]
runs: 3
max_turns: 2
timeout_seconds: 180
allowed_tools: [Skill, Read, Glob, Grep]
---
maketool: a script anyone can run that checks every link in our docs folder still resolves.
