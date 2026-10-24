---
status: accepted
status-note: — ratified by the owner 2026-10-23
ratified-by: the owner
ratified-on: "2026-10-23"
owner: the owner
kind: process
built: landed
proof: "`skills/bbq/references/stew.md`, `skills/bbq/SKILL.md`, `evals/bbq-yes-14/prompt.md`, `evals/bbq-yes-21/prompt.md`, `evals/bbq-no-09/prompt.md`, `evals/bbq-no-11/prompt.md`"
supersedes: nothing
amends: "ADR-007, amendment of 2026-10-20 (a bbq under the grant answers itself): a stew is answered by a subagent"
---
# ADR-021 — bbq gains a stew mode

This is the published version of this decision. Some internal details have been left out.

The first stew was run by hand, before it had a name: a 137-question bbq that reworded this project's README and
starter guide.

## Decision

bbq gains **stew**, a mode any type can carry, for thorough, back-and-forth sessions: the bbq is asked in blocks,
and after each block the lead re-plans the next one from the answers so far. It is switched on by its word, so a
short bbq stays light: "stew bbq" is the usual form, the mode word in front as in "batch skill bbq" ("stew skill bbq", "stew adr bbq"), and "stewbbq",
"stew-bbq", "bbq stew", "bbqstew" and "bbq-stew" work too, only with the two words side by side; the same
words turn it on mid-bbq, from the next block. Stew is the format and the way the questions are processed,
nothing more: it never calls outside models on its own, never starts or offers a talk-through, and adds
no plain bbq setting.

How it runs:
- **Setup.** After the count (offering 8, 20, 40 or 80), one round: the block size, picked from the count (8
  or fewer, blocks of 2; 9 to 20, blocks of 4; 21 to 40, blocks of 8; over 40, blocks of 20), and with it how a
  block is asked, in rounds, one or two at a time, or as a worksheet; and a soft cap (recommended:
  re-plans may add questions past the count) or a hard one (everything fits; the rest is defaulted with veto
  lines).
- **Each block.** On a wording job, options give the same idea at different lengths and registers; on any other
  type, different answers. On a wording job, an answer the user writes comes back in the next block with
  typos fixed beside a light polish with reasons, as an uncounted pick, the user's words winning when untouched.
On every stew, a fact that seems to change is flagged, never changed quietly.
- **Each checkpoint.** The rest is re-planned silently, nothing said in the chat, the plan for the rest kept in
  the record; on a wording job, the settled lines go into the target document.
- **Who answers.** Anyone: the user, or another agent or session. Under carte blanche, a subagent at
  least, kept going across the blocks, never the asking agent itself; a model on the user's neighbourhood allow
  list may answer instead once a neighbourhood skill ships; with no subagents, a plain carte-blanche bbq. This
  narrows ADR-007's amendment of 2026-10-20, under which a bbq under the grant answers itself.
- **Alongside.** With Batch, each item is stewed, its builder starting when its last block ends, and each block
  names its item. Away sends blocks as asks. Neighbours, when the user adds them, draft per block.
goforit is unchanged.

## Context

Drivers:
- Short bbqs must stay light.
- Stew is a way of handling questions, so it must not pull in other skills or outside models.
- The user writes much of a wording job in their own words, and those words must not be changed quietly.
- Doctrine: function first, then ours, then compatibility. The mode is the user's own, and it reuses bbq's mode
  pattern (ADR-006's Away, ADR-015's Batch) and Batch's worksheet rule.


## Alternatives

### A mode on any type (chosen: the user's word)
- Good: "stew adr bbq" and "stew skill bbq" work on the day it lands; short bbqs never meet it
- Bad: one more reference file to keep in step with bbq's steps

### Make re-planning and single-item worksheets plain bbq settings too (not chosen)
- Good: any long bbq could use them without the word
- Bad: two switches for one thing; plain bbq would grow

### Neighbour drafts and a talk-through as part of stew (the amendment's proposal, narrowed by the user)
- Good: matches the first stew as it ran
- Bad: stew would depend on outside models and on another skill; the user: neighbours are "separate from the stew"

### Mention the talk-through in the setup line (overruled by the user: "Separate, never mentioned")
- Good: long stews throw off side ideas, and the first stew's talk-through caught three of them
- Bad: an offer the user does not want in every stew

### The pick between the user's words and a polish on every stew (overruled by the user: wording jobs only)
- Good: one rule for every stew
- Bad: on an ADR or Skill stew, the user's own answer is a decision, not text to polish

### One line in the chat at each checkpoint saying what the re-plan changed (overruled by the user)
- Good: the user sees why the questions moved
- Bad: the user: "it just silently in the background shapes its remaining questions"

### Block size from a table by count (chosen)
- Good: matches the first stew (80 in blocks of 20) and the user's smaller examples (4, 2 or 1 at a time)
- Bad: a count at a table's edge may want the neighbouring size; the setup lets the user change it

### A quarter of the count, or no table (not chosen)
- Good: always four blocks, or nothing to learn
- Bad: odd sizes like 5 do not fit a round of four; no pick to start from

### Soft cap on top, asked at setup (chosen)
- Good: the first stew grew from 80 to 137 because the answers asked for it
- Bad: a soft stew can run longer than planned; the Owed line is the only sign

### Under carte blanche: anyone but the asker, else a plain carte-blanche bbq (overruled by the user)
- Good: no subagent cost
- Bad: the user wanted stew to work agent to agent, with "at minimum a subagent" when no person answers

### Under carte blanche: the asking agent answers itself (narrowed by the user)
- Good: cheapest
- Bad: each re-plan would learn only from answers the planner wrote itself

## Consequences

Easier: a thorough session, for wording or anything else, gets its shape from one word, and the shape scales from
eight questions to eighty. Harder: a soft-capped stew can run long, and a stew under carte blanche costs a
subagent. The trigger cases prove only that bbq loads for every form and not for the near-misses; that the stew
mode itself runs as written has no test.

**Confirmed by:** the user's first real stew after this lands, whose lessons go into a field report.

**Revisit when:** a neighbourhood skill ships, with its allow list.

Next: the first real stew, and the neighbourhood skill's own ADR, which should say how it drafts per block for a
stew.

## Asks left open

None. Every question was settled; each default the agent chose carries a line the user can veto.

## History

- 2026-10-23: proposed.
- 2026-10-23: ratified by the owner.
