# The stew mode

Slow-cooked questions.

A stew bbq is asked in blocks, and after each block the lead re-plans the next one from the answers so far
(ADR-021). It changes how the questions are handled, not what they are about, so it is a mode any type can carry
("stew skill bbq", "stew adr bbq"), like Batch and Away. It is for a thorough, back-and-forth session; a short bbq
stays plain.

## How it starts

- **The words.** "stew bbq" is the usual form, the mode word in front: "stew skill bbq", "stew adr bbq".
  "stewbbq", "stew-bbq", "bbq stew", "bbqstew" and "bbq-stew" work too. Only when "stew" and "bbq" sit next to
  each other: "let me stew on it" never turns it on, and neither does a message where the two words are apart (a
  plain bbq request with "stew" elsewhere runs as a plain bbq).
- **Mid-bbq.** In a running bbq, "stew bbq" or "make this a stew bbq" turns it on from the next block. The
  questions already asked keep their numbers. "Let me stew on it" in an answer never does.
- **The count**, as step 1 asks it, offering 8, 20, 40 or 80 (or another number), each with its block size from
  the table below.
- **The setup: one round, after the count**, with two questions:
  - **The block size**, the table's pick first, and with it how a block is asked. The question's wording also
    says, in one line, what else the stew takes as given: on a wording job, the document the answers go into,
    when the opener has not named it. The user changes it in Other.
  - **A soft or a hard cap.** Soft *(Recommended)*: a re-plan may add questions past the count, which shows only
    in each round's Owed line and in the question numbers. Hard: everything fits the count, and whatever does not
    goes into the Defaulted list with a `veto:` line.

  | count | block | how a block is asked |
  |---|---|---|
  | 8 or fewer | 2 | one or two at a time |
  | 9 to 20 | 4 | one round |
  | 21 to 40 | 8 | two rounds of four, or one worksheet |
  | over 40 | 20 | a worksheet |

## Each block

- **Asked as the setup said:** in rounds of up to four (step 3), one or two at a time, or as a worksheet: every
  question of the block with its options and the recommended one already picked, which the user changes and
  sends once. A worksheet is a form where the platform can draw one (*Platform notes*), otherwise a file beside
  the record (`<record_dir>/<date>-<topic>-sheet-<block>.md`) that the user edits and says when it is done, the
  same rule as Batch's.
- **The options.** On a wording job (the answers are finished text for a document), each question offers the same
  idea at different lengths and registers (shortest, medium, explanatory, warm), and Other is expected, not a
  fallback. On any other type, the options are different answers, as in any bbq.
- **Your words, then a pick (wording jobs only).** An answer the user writes in Other comes back as a first
  question of the next block, numbered by the question it settles ("Q12 pick"): the user's words with typos
  fixed, beside a light polish with a reason for each change. Picks never count toward the total, and left
  untouched, the user's words win. On any other type, the user's own answer is taken as written.
- **Facts are flagged, never changed quietly**, on every stew. When a polish, a draft or an answer seems to change
  a fact, say so beside it, and the user rules.

## Each checkpoint (the end of a block)

- **Re-plan the rest, silently.** Reshape the remaining questions around how the user is actually answering:
  drop what is settled, merge what repeats, add what an answer opened, and lean the options the way the user
  leans. Say nothing about it in the chat. The plan for the rest is kept in the record, so another session can
  pick the stew up where it stopped. Each round still ends with its Owed line, as in any bbq.
- **Write the block into the record.**
- **On a wording job, write the settled lines into the target document**, so the user can read them in place
  before the next block.

## Who answers

- **Usually the user, but any answerer works.** Stew also works agent to agent (a lead questioning a worker, one
  session questioning another about a hand-off): each re-plan learns from answers the asker did not write.
- **Under carte blanche**, where a plain bbq's agent answers its own questions, a stew is answered by a subagent
  at least: one that sees the record and the project's files but not the asking agent's own plan, kept going
  across the blocks. Its answers go into the Defaulted list with `veto:` lines, and a taste answer is a proposal,
  flagged as taste (ADR-007). Once a neighbourhood skill ships, a model on the user's neighbourhood allow list (the
  outside models the user allows) may answer instead. Where the platform has no subagents, the stew runs as a
  plain carte-blanche bbq and says so in one line.
- **Away** (the user reachable now and then): blocks travel as asks, the way `cloud-and-away.md` sends them; the
  next block is planned when its answers arrive, and anything still open at hand-off takes its recommended answer
  with a `veto:` line.

## Alongside

- **Batch.** Each item is stewed, with its own blocks and re-plans, and its builder starts when its last block
  ends. Items come one at a time, as Batch asks them, and each block's first question names the item and the
  block ("Skill 2 of 5, block 2 of 3"), so the user can follow.
- **Neighbours are not part of stew.** A stew never calls outside models on its own and needs none. When the user
  adds them (by hand, until a neighbourhood skill ships), they draft per block: before the first block, then at
  each checkpoint for the next, so their drafts follow the re-plan. Each option they draft names who drafted it.
- **talk-through is separate.** A stew neither starts nor offers one; the user adds it by saying talk-through.
- **goforit is unchanged.** Mid-stew it takes only answers that can be cited (ADR-017), and the last question is
  still "Anything else to protect or avoid?".
- **A plain bbq is unchanged.** Re-planning in blocks and worksheets for a single item come only with stew.
