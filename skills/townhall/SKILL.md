---
name: townhall
metadata:
  family: plan
description: Put a decision or a verdict to several agents who argue it out in rounds under set rules, while the lead, who never argues, judges and recommends; then write one record of who argued what and offer makeadr. A townhall seats the neighbours on the user's allow list (other model families, local models, other accounts); a family meeting seats subagents of the lead's own model family. Use when the user types "townhall" or "town hall" as an opener ("townhall: SQLite or Postgres?"), or "familymeeting" or "family meeting". "townhall live" hands the run to the live tool, where the user can cut in. A company or civic town hall meeting, "let's talk it through", "debate this with me" or "play devil's advocate" does not load it.
---

# townhall: agents argue it out, the lead judges

Decided by pitmaster ADR-024.
Each rule below names the question of its bbq that set it (Q3…Q40).

Sibling of `makeadr` (a decision a townhall argued, its record already holding the options considered),
`talk-through` (an open decision from a talk can be put to a townhall; both skills' records pass the same checker),
`budget-select` (the stop line for a run that seats outside neighbours or passes its cost line) and `tier-select`
(the debaters' models).

**The smallest use:** "familymeeting: should X or Y?", one setup round, three rounds of argument, a recommendation
and a record.

## Config

Edit these lines here, or put the same lines in a `pitmaster.md` at your project root, which wins. Every line is
optional.

```
name: the user                          # who the skill speaks to; "name: Alex" makes it say "Alex"
record_dir: docs/townhall               # where a run's record goes: <record_dir>/<date>-<topic>.md (Q26)
neighbours: ~/.pitmaster/neighbours.md  # the allow list (Q7, Q24); a project may name a path or narrow it to names
rounds: 3                               # rounds before the closing round (Q13)
positions: assigned, concede at the end # or: assigned, held | free (Q9, Q11)
watch: full                             # full | short | record (Q37)
cost_line: 200k                         # tokens; an estimate above it loads budget-select (Q17)
debater_warning: 4                      # more debaters than this shows a warning; it never blocks (Q20)
```

The live tool's settings (`delivery`, `filibuster`) and the seats default sit in the neighbours doc, outside this
skill (Q38, Q40). Its shape is in `references/neighbours-doc.md`.

## Steps

1. **Which meeting.** "townhall" or "town hall" seats neighbours from the allow list. "familymeeting" or "family
   meeting" seats subagents of the lead's own model family (Q27). When a townhall finds no outside neighbour listed
   or reachable, say so and ask whether a family meeting on this one account is all right; on a no, stop. Where
   there are no subagents and no reachable neighbours, say a fair meeting cannot be held here and offer
   talk-through (Q32). "townhall live" goes to step 9.
2. **Read first** (Q30): the files the opener names, any ADR or proposal on the topic, the status file, the newest
   log entry, and for a townhall the neighbours doc. If an ADR already rules the question, say so and ask whether
   to argue an amendment instead; never re-argue ruled text as if it were open.
3. **The setup round.** One round of questions, each with its default first; words in the opener answer them ahead,
   and a full opener skips the round (Q10).
   - **Kind** (Q12, Q19): a *decision* (which option), a *verdict* on work or findings already in hand (is it real,
     is it worth fixing, ship or hold), or *attack and defend* (one side attacks the work, one defends, the judge
     rules point by point). Nothing is ticked: the user picks, because a townhall is called on purpose.
   - **Who sits** (Q6, Q34): for a townhall, the default is the line-up from the first run, read from the
     neighbours doc's *Seats* line (on the very first run, ask and write the pick there). The user may go wider or
     narrower, never past the allow list. One debater per option (Q20); above `debater_warning`, warn and go on.
   - **Positions** (Q9, Q11), **rounds** (Q13), **judge** (Q8: the lead, unless the user names another), and
     **watching** (Q37).
   - **Cost** (Q17): a rough estimate (debaters × rounds × about 4k tokens a turn, plus the brief). A townhall that
     seats an outside neighbour, or any run over `cost_line`, loads budget-select for a stop line first.
   - **Models** (Q18): tier-select picks the debaters; where the account has more than one model, give the
     debaters different ones, because different models agree with each other less.
4. **The brief** (Q21). Each debater gets the question, the options, its position and an evidence pack: the files
   the lead read in step 2, cited. Debaters may read more. Never the lead's own leaning.
5. **The rounds** (Q13): opening case, reply, rebuttal. Each speaker sees every earlier turn. Show each turn as
   `watch` says. When the user types during a run (Q16), read it before the next speaker and settle with the user:
   the debaters answer it, or the round resets with new settings.
6. **The guard** (Q31). If the sides converge before the closing round, note it for the record and ask each side
   once more for its strongest objection: one sharper round.
7. **The closing round** (Q11): each debater says what, if anything, moved it.
8. **Judge and record.** The judge distils each side's best points and recommends. A taste answer (a name, a look,
   a direction) comes out as a proposal for the user, never ruled (Q22). Write the record to
   `<record_dir>/<date>-<topic>.md` in talk-through's shape (Q14, Q25): a header (date, kind, who sat on which
   side, which models), the key points per side, what moved whom, a decisions table with each row marked agreed,
   proposed or open and cited to the turn it came from, and the recommendation; mark a family meeting as one. Last,
   in small print (`<sub>` in Markdown), the usage where it is reported: each seat's model and tokens, the judge's,
   and the total; anything not reported says so. It is for the record, never part of the argument. The chat
   summary ends with the total in one short line. Run `scripts/record-check.py` on it. For a decision, offer
   makeadr.
9. **townhall live** (Q5, Q33–Q36, Q38, Q40). Hand the settings to the live tool, which runs the loop in a
   terminal: speakers on servers that stream arrive word by word, and the user types to cut in; a speaker may
   finish its sentence (`filibuster`), then must answer. Not built yet: until it is, say so and offer a plain run.

## Never

- **Act on its own result** (Q22): no edits, pull requests or merges come from a run. makeadr, goforit or the user
  carries the recommendation out.
- **Rule taste** (Q22): names, looks and directions come out as proposals.
- **Seat an outside model unasked** (Q4, Q27): a family meeting seats subagents only, and a townhall seats only
  names on the allow list.
- **Let debaters change files** (Q22): they only read; the judge writes only the record.
- **Let the lead argue** (Q8): the judge never takes a side in the rounds.

## Platform notes

- **Claude Code:** the setup round is one `AskUserQuestion` with up to four questions, everything needed to answer
  in their own wording. Debaters are `Agent` subagents with the model tier-select picks, each kept going across
  rounds with `SendMessage`. Outside neighbours are reached with the tools the neighbours doc names (the `outside`
  server for Codex and OpenCode, `lanes` for the local models). `scripts/neighbours.py` prints the allow list and
  who answers right now (`--only` narrows it to the setup round's pick, `--json` for reading back);
  `scripts/record-check.py <record>` checks the record's decisions tables. Both are standard-library Python with a
  `--self-test`. Usage for the small print: a subagent's tokens come back with its result; an Ollama or LM Studio
  reply carries its token counts; lanes and `outside` replies may not, so say so.
- **Cowork / claude.ai:** no subagents, so no family meeting: a townhall runs only with neighbours the tool can
  reach, otherwise it offers talk-through (Q32). No scripts run: read the neighbours doc by hand and skip the
  record check.
- **Codex:** debaters are Codex subagents where your Codex has them; otherwise step 1's no-subagents rule. Ask the
  setup round as a numbered list in one message.
- **Other tools:** the setup round is a numbered list in one message, the default first. Use the tool's own
  subagents if it has them; otherwise step 1's no-subagents rule.
