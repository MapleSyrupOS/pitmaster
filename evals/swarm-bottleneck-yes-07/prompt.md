---
name: swarm-bottleneck-yes-07
tags: [trigger, swarm-bottleneck, should-trigger]
runs: 3
max_turns: 2
timeout_seconds: 180
allowed_tools: [Skill, Read, Glob, Grep]
---
Why is this slow? We have eight workers running and the lead has been waiting on them for an hour.
