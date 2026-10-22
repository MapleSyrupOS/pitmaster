---
name: swarm-bottleneck-no-01
tags: [trigger, swarm-bottleneck, should-not-trigger]
runs: 3
max_turns: 2
timeout_seconds: 180
allowed_tools: [Skill, Read, Glob, Grep]
---
My Python script is slow when it reads a big CSV. How do I profile it?
