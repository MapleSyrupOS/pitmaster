---
name: spend-ledger-yes-01
tags: [trigger, spend-ledger, should-trigger]
runs: 3
max_turns: 2
timeout_seconds: 180
allowed_tools: [Skill, Read, Glob, Grep]
---
spend-ledger: log what this session cost before we wrap up.
