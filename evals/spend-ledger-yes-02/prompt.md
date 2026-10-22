---
name: spend-ledger-yes-02
tags: [trigger, spend-ledger, should-trigger]
runs: 3
max_turns: 2
timeout_seconds: 180
allowed_tools: [Skill, Read, Glob, Grep]
---
Log the spend for this session in the ledger, then we're done.
