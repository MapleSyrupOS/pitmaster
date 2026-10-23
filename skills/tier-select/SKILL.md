---
name: tier-select
metadata:
  family: run
description: Decide the model and effort for a session's lead (the session that dispatches, judges and lands) and for each worker it spawns, by the shape of the job, on any vendor. It picks a neutral tier (small, mid, large, top) and an effort, then turns them into real models with a dated roster per vendor (Claude, OpenAI, Google, or one it writes with you). Use when a bbq or a prompt-writing session must say who leads a run, before writing an overnight prompt, swarm kickoff or handoff, before spawning subagents or workers, and when the user asks "which model for this", "who should lead", "can the small model do this" or "plan the workers".
---

# tier-select: who leads, and which tier does each job

The skill reasons in **neutral tiers** by the **shape** of the job. A **roster** (a dated list of one vendor's
models) then turns each tier into a real model.

| tier | what it is for |
|---|---|
| **small** | the cheapest, fastest model: reading, counting, classifying, summarising |
| **mid** | the default builder: spec'd work with a test, and most leads |
| **large** | the hardest reasoning: untrusted input, security, memory-safety, disputed findings |
| **top** | the vendor's best: the final word on a dispute, the last pass before a big landing |

Effort is one of **low, medium, high, xhigh, max**, or the nearest setting the platform has (the roster says).

Sibling of `budget-select` (how much the run may spend; it advises on tiers and this skill decides) and `bbq`
(which asks the user who leads, with this skill's recommendation). `tastetest` asks it for its auditor's model,
and `goforit` for who builds.

**The smallest run** is a worker's tier: the roster steps, then the table in part B. Part A is only for a run that
starts a lead.

## Config

Edit these lines here, or put the same lines in a `pitmaster.md` at your project root, which wins. Every line is
optional.

```
name: the user      # who rules on leads. "name: Alex" makes this skill say "Alex".
roster: auto        # auto picks rosters/<vendor>.md for the platform in use; or name one, or a mix
local_models: none  # "none", or where your local-model notes live (local models go first for small jobs)
```

## Before anything: the roster

1. **Pick the roster** from the project's `docs/tier-rosters/` if it has one for the vendor, else from `rosters/`
   beside this file (`claude.md`, `openai.md`, `google.md`); with `roster: auto`, the platform's vendor. A roster may name another vendor's models for a tier (some tools offer several
   vendors, each with its own quota), and the user may ask for a mix.
2. **Check its *Last checked* date.** **Over about three months old, say so** in one line before using it, and
   offer to re-check it against the vendor's model list.
3. **No roster for this platform?** Ask the user which models they can use, cheapest first, and how effort is set
   there. Write `docs/tier-rosters/<vendor>.md` in the project from `rosters/TEMPLATE.md` (beside this file) with
   today's date, and use it; a roster written beside the skill would be lost at the next update.

## A. The lead

**Never assume the biggest model.** Whenever a prompt will start a session that leads (an overnight, a swarm, an
arc, a debt night, a handoff):

1. **Name the run's shape** from `leads.md`: what the lead itself must judge, not what its workers do.
2. **Take the row's tier and effort**, and turn the tier into a model with the roster. With no matching row, take
   the cheaper of the two nearest and say it is unmeasured.
3. **Ask the user**, never default it: in a bbq, as round one's lead question; elsewhere, as one question with the
   recommendation first, marked *(Recommended)*, then one cheaper and one dearer option, each with its reason
   from `leads.md`.
4. **Write it into the kickoff** as the session's model and effort, with the stop rule: "If your session is on
   another model or effort, stop and say so before doing anything." Effort is set in the platform's own setting,
   not by the prompt, so the kickoff says which to pick. **The session checks its effort by name** where the
   platform shows one (see *Platform notes*), never by a number or hint in its own context; where no name can be
   read, it asks the user to confirm the setting rather than stop on a guess.
5. **Record it at close**: the lead's model and effort go in its `budget-select` calibration row, so `leads.md`
   can be refit from cost as well as outcome.

## B. The workers

Route each job by its shape, to the **smallest tier that does the job well**:

| job shape | tier | effort |
|---|---|---|
| read, count, classify, summarise, digest a log or a report | small | low |
| a census with several steps, or cross-checking two sources | small | medium |
| a scripted tool step, or a one-function fix with a check to run | small (or a local model) | medium |
| spec'd building: a feature or fix with a test harness, a read-only review with named checks | mid | high |
| open-ended work: a failure with no known cause, a fix whose shape is not given, an adversarial review of a large change | mid | xhigh |
| parsers of untrusted input, memory-safety or kernel code, security design | large | high (xhigh for the builder of a parser) |
| a tie-break between two reviews of the same change | one tier above the reviewers | high |
| a disputed security finding, or the last pass over a night's work before landing | top | max |

Rules:

1. **Local models first** for small-shaped jobs, if the config names your local-model notes and a local model is
   free. Fall back to the small tier after two real failures (not after "busy" or "offline").
2. **Every tier's output is checked by a different tier.** A disagreement goes up one tier, never to a vote of
   equals.
3. **A large or top spawn names its class** in the brief (`untrusted input`, `memory safety`, `security design`,
   `dispute`), so a reader can see why it was not a smaller tier.
4. **Set each worker's effort explicitly** where the platform allows it. Where a worker inherits the lead's effort
   (see the roster), say so in the plan.

## Platform notes

- **Claude Code:** spawn workers with subagent definitions that pin `model:` and `effort:` (a bare model override
  inherits the lead's effort). The lead's effort is set in the app or with `/model`. A session reads its own effort
  name with `echo "$CLAUDE_EFFORT"`; use that for step A.4's stop rule.
- **Cowork / claude.ai:** no subagents, so part B plans work for other sessions or tools, naming each one's model
  and effort for the user to pick. Part A works as written.
- **Codex:** set the model and effort per session in `config.toml` (`model`, `model_reasoning_effort`), with a
  profile per tier (`--profile`), or with `/model` interactively. `rosters/openai.md` has the names.
- **Other tools:** use the tool's model picker and its effort or thinking setting; if it has none, the effort
  column is advice for the prompt only.
