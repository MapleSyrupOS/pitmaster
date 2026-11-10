---
name: goforit
metadata:
  family: run
description: Carry a plan straight on into the build once its planning skill ends. Typed at the end of a message that starts bbq, makeadr or talk-through (or on its own after one has finished), it takes that skill's closing offers, has the build done here or by a worker, and stops at "ratify" and at "merge"; "goforitreally" also builds what the plan pulls in and merges on green, so the only stop is the user's "ratify"; it is the rung below carte blanche. Use when the user types "goforit" or "goforitreally". A plain "go for it", "yes, do it" or "ok" in answer to a question does not load this skill.
---

# goforit: once the plan is set, light the pit

Decided by pitmaster ADR-017.
The grant ladder: ADR-023, revisited by ADR-025.

Sibling of `bbq`, `makeadr` and `talk-through` (the planning skills it follows and acts on; makeadr owns the *Is it
ADR-sized?* test step 9 carries a checked copy of), `tier-select` (picks who builds) and `carte-blanche` (the rung
above "goforitreally", which allows everything goforitreally does).
`looseends` hands it a settled plan that was never built. `napkin` offers it when the napkins leave nothing open.
Built by a Skill bbq whose question record is kept in
pitmaster's private repository.

**The smallest comrun** is steps 1 to 6, stopping for **ratify** and for **merge**.

## Config

Edit these lines here, or put the same lines in a `pitmaster.md` at your project root, which wins. Every line is
optional.

```
name: the user          # who rules. "name: Alex" makes this skill say "Alex".
prompt_at: 50           # context used (%) at which the build goes to a fresh session's prompt instead
warn_at: 5 points, 1 PR, 2 workers   # both words warn above any of these (step 8)
```

## Steps

1. **Wait for the plan.** The planning skill runs as usual, and the user answers every question it asks until
   they answer one with **goforit**.
   - **Typed** in any free-text answer, anywhere, "goforit" means "we've talked enough": take the recommended
     option for that question and every one left, write each into the record as taken on goforit, and go to
     step 2.
   - **As an option.** Where the planning skill asks how many questions to have, or whether to go on, offer
     "goforit" too, but only when every question still to come can be answered **with a citation**: a question
     number in a record, an ADR, or the user's own words in this session. If any one cannot, offer no goforit and
     ask the questions. The option says what it rests on ("rests on the bbq's Q15–Q29"), and each answer taken is
     written with its citation (ADR-017, amendment of 2026-10-22). Never offer it on ordinary questions.
   - **No second interview.** When a bbq has already settled, with citations, what its ADR needs, write the ADR
     from the record and ask only what is still open.
   - **Taste.** List any taste answer (a name, a look, a direction) taken on goforit for the user's OK before
     anything that depends on it lands.
   - goforit says yes only to the planning skill's closing offers, such as makeadr after a Skill bbq, or "run it
     here".
2. **Find the record.** Typed alone after a planning skill ended, goforit acts on the most recent record from this
   session. With none, ask which; never guess across sessions.
3. **Name the build** in one line: what gets made, and the record it comes from.
4. **Pick who builds** by `tier-select`'s tier, and say the route in one line ("Building here: top tier, 18 %
   context"):
   - top or large judgement work runs **here**, if this session is on that model and effort; otherwise write a
     fresh session's prompt and stop;
   - mid or small work goes to **a worker** at that tier, and this session reviews its diff before anything lands;
   - at `prompt_at` context used or above, write a fresh session's prompt instead, and stop.
   - both words start as many subagents as their estimate allows (step 8). Neither starts a fresh session or a
     swarm, works outside the plan's repository, or pushes to another live session's branch.
5. **Build, then stop at ratify.** Build everything the record asks that needs no ratified ADR, run the project's
   checks and open a PR. A new judgement call that comes up while building is parked and asked, not taken; so is a
   fix outside the plan, even one the plan can't land without. Then ask for the one word that is always the user's:
   **ratify**, typed or dictated.
6. **After "ratify"**, record it with `makeadr`, then follow the ratified ADR's own build steps, whatever the work
   (for a new skill, bbq's Skill type holds them). Run the checks, update the PR, and ask to **merge**.
7. **goforitreally** runs the same steps all the way through, the middle rung of the ladder (goforit,
   goforitreally, carteblanche, trescarteblanche; ADR-023). It builds the plan plus any fix the plan can't land
   without (its checks fail until it is made), inside the plan's own PR; anything else it finds is written down (the
   debt list, or its end summary) and left, since fixing that is carte blanche's (ADR-025). It takes the
   recommended option on a new call mid-build and writes a `veto:` line for it, asks nothing before "ratify", and
   after it merges its own PR once the checks are green. It never picks unrelated work: that is carte blanche.
8. **Size it first (both words, ADR-025).** Estimate the points (`budget-select`'s unit, by default 1 % of the
   weekly limit), the PRs and the workers; the sizecheck skill will do this once it exists. At or under
   `warn_at`, start without a word, and the estimate is the budget; a number the user gives is its ceiling. Above
   it, say "This looks big: about N points, M PRs, K workers" and offer **go**, **trim** (say what to drop) or
   **back out** (goforitreally drops to plain goforit, stopping at each gate; plain goforit writes a fresh session's
   prompt and stops).
9. **ADR candidates (both words, ADR-036).** Hold each call made or parked while building to this test, makeadr's;
   one that passes goes on the *ADR candidates* list in the PR body and the end summary, with the call and the
   signs it showed:

   <!-- adr-sized:begin (a checked copy of makeadr's test, ADR-036: change it there first) -->
   **Is it ADR-sized?** An answer or a call is ADR-sized when it will still bind a later session **and** at least one
   of these holds: (1) it chose between two or more options that each had merit; (2) it fixes something other work
   will build on (a file format, a folder layout, a dependency, where data lives, a name others will call); (3) it
   sets a standing rule ("from now on", "always", "never"); (4) it overrules the recommendation; (5) it touches,
   narrows or reverses an existing ADR. Not ADR-sized: a mechanism with one plain answer; a choice that only shapes
   this run (its order, its budget, who leads).
   <!-- adr-sized:end -->

   At the close, only when a candidate is left, offer `makeadr` once: the user picks which become ADRs, and each
   skipped one is marked "not an ADR, by the user" and never offered again. Never write or draft one on your own,
   and never offer makeadr mid-build.

**Never:** ratify, or count any word but "ratify" as ratifying; answer a taste question for the user; skip a
planning skill's questions; merge without "goforitreally" or a plain yes to merge (a project rule that allows
merging grants nothing by itself); push to the main branch.

## Platform notes

- **Claude Code:** workers are subagents with `model:` and `effort:` pinned from tier-select's roster; `/context`
  gives context used; `gh` opens and merges the PR. Ask for ratify and merge with `AskUserQuestion`, everything
  needed to answer in the question itself, and send anything made for the user as a file.
- **Cowork / claude.ai:** no subagents, usually no git: build here or write a fresh session's prompt (step 4 asks
  which), and end with the files and the record instead of a PR.
- **Codex:** a worker where your Codex can start one, otherwise build here. Codex shows no context percentage, so
  step 4 asks before a long build. Skills live in `.agents/skills/` or `~/.codex/skills/`.
- **Other tools:** no workers: build here or write the prompt, asking which as a numbered list.
