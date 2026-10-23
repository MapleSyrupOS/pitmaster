---
status: accepted
status-note: — ratified by the owner 2026-10-22
owner: the owner
kind: process
built: landed
proof: "`skills/bbq/SKILL.md`"
supersedes: nothing
amends: nothing
---
# ADR-015 — bbq gains a Batch mode

This is the public copy of a decision I made. I've left out a few internal notes.

## Decision

bbq gains **Batch**, a mode any type can carry, for many items of one type built at once: "batch skill bbq",
"batch adr bbq". The lead asks every item's own questions in one sitting, and each item's builder starts as soon as
that item's questions are done, while the user answers the next. The batch round first asks how many items, then how many questions each. Builders are not capped; the batch says its expected usage
first, by default. Each builder's model and effort fit its own item
(`tier-select`). Each builder gets its own worktree and only its own item's files, and the lead lands the shared
changes once, in one PR. The word "multitask" loads bbq, which asks "Batch bbq?" first.

## The rules

1. **A mode, not a type:** it rides on any type, as Away does. Each item still gets its type's own questions and
   its own record.
2. **No conflicts:** before any item's questions, every pair is checked. No two items touch the same file (other
   than the shared files the lead lands) or decide the same thing; a pair that does becomes one item, or the second
   waits for the first to land, and the user rules which. A clash among three items always shows in some pair.
3. **Taken in turn:** ADR numbers, ids and anything numbered in sequence are handed out by the lead before the
   builders start.
4. **Questions:** the batch round asks how many items first, then how many questions per item (4, 12, 20 or
   another number). A setting, `batch_format`, decides how questions come. At `ask`, the default,
   every batch asks: by size (rounds at 8 per item or
   fewer, a worksheet per item at 9 or more), in rounds of up to four (a builder starts the moment its last round
   ends), as one worksheet per item (a builder waits for its whole sheet), or as one worksheet for the batch (no
   builder starts until it is done). By size sits at the top, naming what it picks for this count. Set to one of
   the four, it is used without asking; the bbq never writes the setting itself. A worksheet is a form drawn in the chat where the platform can draw one, a file
   elsewhere or on request; no question is added for it. Then the lead asks every item's questions, item by
   item. No builder asks the user its questions.
5. **Builders:** one per item, started when its questions end, with no cap. By default the batch loads
   `budget-select` and says the expected usage first (per item from `spend-ledger`'s past rows, the total, the share
   of the week), and `spend-ledger` records it at the close. The user can turn this off.
6. **Tier:** each builder's model and effort come from `tier-select` for its own item, never one tier for the batch.
7. **Files:** a builder writes only its own item's files and lists the shared changes it needs (version,
   changelog, manifests, sibling lines) in a landing-notes file.
8. **Landing:** the lead adds the shared changes once and opens one PR.

## Alternatives

- **A mode on any type** (chosen). One batch shape for skills, ADRs or anything else. Cost: the type table no
  longer lists everything a bbq can be.
- **A Batch type of its own** (not chosen). A batch of skills still needs the Skill type's questions.
- **"Multitask" as the name** (not chosen). It reads as one person switching jobs; kept as a word that asks.
- **All questions first, then every builder** (not chosen). The first builder waits for the last item.
- **Builders ask their own questions** (not chosen). The user hops between waiting sessions.
- **A total question count** (not chosen). Items differ, so a total needs a split the user did not choose.
- **A builder cap** (not chosen). A cap stands in for usage; it is better to say the usage.
- **Each builder lands its own PR** (not chosen). Every merge conflicts on the version and the changelog.

## Consequences

- A batch's questions come in one sitting, and building starts with the first answer.
- The lead carries the landing for every item, and one PR is larger to review. An answer in a later item that
  changes an earlier one reaches a builder already at work.

## History

- 2026-10-22: proposed.
- 2026-10-22: ratified by the owner.
