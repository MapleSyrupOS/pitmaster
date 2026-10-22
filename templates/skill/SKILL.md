---
name: skill
metadata:
  family: plan
description: What this skill does, in one sentence, then when to use it. Use when the user types "skill", or says "the phrases that should load it", "another phrase". Name the near-misses in the evals, not here. At most 1,024 characters.
---

# skill: what it does, in a few words

Decided by pitmaster ADR-NNN.

<!-- The house shape (ADR-004). Copy this folder to drafts/<name>/, rename `skill` in the folder, the
     frontmatter and the title, set `family` to one of plan, run, usage, check, records or craft (ADR-004), and fill
     in each part. A draft needs its ADR (made with makeadr) before it moves
     into skills/. Write for a reader who is not a programmer: plain sentences, one idea each. Delete this
     comment when done. -->

Sibling of `other-skill` (what it hands over or takes back). Delete this line if the skill calls no other skill.
In the same PR, name this skill in each sibling's own Sibling line (ADR-004, amendment of 2026-10-20).

## Config

Edit these lines here, or put the same lines in a `pitmaster.md` at your project root, which wins. Every line is
optional.

```
name: the user        # who the skill speaks to. "name: Alex" makes this skill say "Alex".
```

Delete this section if the skill has no settings.

## Steps

1. **The first thing it does.** In plain words: what to read, what to ask, what to write. Name sibling skills by
   their bare name and scripts by their path inside this folder. No tool names that only one platform has; those
   go in Platform notes.
2. **The next thing.**
3. **What it must never do**, if anything, as its own step or a short list at the end.

## Platform notes

- **Claude Code:** how a step is done here (the question tool, `gh`, the skills folder).
- **Cowork / claude.ai:** what changes without git or a shell.
- **Codex:** how to ask and where skills live.
- **Other tools:** the plain fallback: a numbered list in one message, and what is skipped.
