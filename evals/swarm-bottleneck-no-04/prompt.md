---
name: swarm-bottleneck-no-04
tags: [trigger, swarm-bottleneck, should-not-trigger]
runs: 3
max_turns: 2
timeout_seconds: 180
allowed_tools: [Skill, Read, Glob, Grep]
---
Optimize this SQL query: SELECT * FROM orders WHERE customer_id IN (SELECT id FROM customers).
