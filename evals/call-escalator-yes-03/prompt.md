---
name: call-escalator-yes-03
tags: [trigger, call-escalator, should-trigger]
runs: 3
max_turns: 2
timeout_seconds: 180
allowed_tools: [Skill, Read, Glob, Grep]
---
second-opinion: why does the build break only on the Linux host?
