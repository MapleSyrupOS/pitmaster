# The Batch mode

A Batch bbq settles many items of one type at once (skills, ADRs, anything) and starts a builder for each
(ADR-015). It is a mode any type can carry: each item still gets its type's questions and its own record. This
session leads.

- **The batch round comes first, always in rounds.** Q1 is how many, in the type's own word ("How many skills?").
  Q2 is how many questions per item, in place of step 1's count: 4, 12, 20 or another number (recommend 12 for
  skills, which have ten things to cover). Then the items' names, and who lands. The batch round's own questions
  come on top.
- **Rounds or a worksheet**, asked after Q1 and Q2, since the count shapes the answer. At `batch_format: ask`, the
  default, every batch asks, with four options, each saying when its builders start; the top one is *By size*,
  naming its pick for this count ("By size: rounds, at 4 questions per item"). Any other `batch_format` is used
  without asking. The bbq never writes an answer into the config.
  - **By size** *(Recommended)*: rounds when an item has 8 questions or fewer, a worksheet per item at 9 or more.
  - **Rounds**: each item's questions up to four at a time, as step 3 asks them. Its builder starts the moment
    its last round ends, and each answer can shape the next question.
  - **A worksheet per item**: every question with its options and the recommended one already chosen. The user
    changes what they disagree with, at their own pace, and sends it. Its cost: the item's builder waits for the
    whole sheet, and the questions its answers open come after, as a short follow-up round.
  - **A worksheet for the batch**: the same, one form or file for every item
    (`<record_dir>/<date>-<topic>-sheet.md`). Its cost: no builder starts until the whole sheet and its follow-up
    round are done.
- **A worksheet is a form, unless the user wants a file.** No question is added for it. Where the platform can
  draw a form in the chat, the user clicks to change answers and sends it as one message (*Platform notes*).
  Elsewhere, or when the user asks for a file (the format question's *Other*, or `batch_sheet: file`), it is a
  file beside the record (`<record_dir>/<date>-<topic>-<item>-sheet.md`) that the user edits and says when it is
  done.
- **No two items may conflict.** Before any item's questions, check every pair: no two touch the same file (other
  than the shared files the lead lands), and no two decide the same thing. A clash among three or more items
  always shows in some pair, so pairs are enough. A pair that clashes becomes one item, or the second waits for
  the first to land; say which, and the user rules. A conflict found later stops the later item's builder until
  it is ruled.
- **The lead hands out anything numbered in sequence** (ADR numbers, ids) before the builders start, so no two
  take "the next one".
- **Usage is called out, never capped.** With `batch_usage: on`, the default, the
  batch loads `budget-select` for its share and stop lines, and before the first builder starts it says the
  expected usage: each item's estimate from `spend-ledger`'s past rows for work of that size and tier, the total,
  and the share of the week it takes. With no past rows, it says so, and the stop lines are the only guard. A
  builder not yet started when a stop line is reached waits. At the close, `spend-ledger` records the batch. The
  user turns this off in the batch round or with `batch_usage: off`; budget-select's hard stop still applies.
- **Then each item's questions, one item at a time**, all asked by the lead, never by a builder. As soon as an
  item's questions are done (its last round, or its sheet and follow-up round) and its record is written, its
  builder starts, while the user answers the next item's.
- **Each builder fits its item:** `tier-select` picks its model and effort for that item alone, never one tier for
  the whole batch.
- **Each builder gets its own worktree and branch**, its item's record as its prompt, and writes only its item's
  files. The shared changes it needs (a version bump, a changelog line, manifests, sibling pointer lines, counts
  in the README) go in a landing-notes file beside its work.
- **An answer that changes an earlier item** goes to that item's builder as a message, and into its record.
- **The lead lands it all, once:** it checks each builder's work, makes the shared changes from the landing notes
  in one pass, and opens one PR. Where an item needs a ruling first (a skill's ADR), the lead asks for it then.
- **When the batch feels slow**, `swarm-bottleneck` names what is holding it.
