---
name: guided-townhall
metadata:
  family: plan
description: A townhall that takes turns with the user. One debater speaks, then the user, then the next debater, who sees every earlier turn, the user's included; the user may pass, leave a note every later turn must answer, ask one seat a question, change the seats, or steer the run. The lead judges and never argues, and the run ends in a townhall record. Use when the user types "guided-townhall", "guided townhall" or "guidedtownhall", or asks for a townhall "where I get a turn after each speaker" or "that waits for me between speakers". A plain "townhall" or "familymeeting" loads townhall instead, and "townhall live" is the streaming tool, where the user cuts in mid-sentence.
---

# guided-townhall: a townhall that takes turns with you

Decided by pitmaster ADR-039.
Each rule below names the setup-round question that set it (G1…G4) in the ADR's setup record, or the run it came
from.

Sibling of `townhall`, which it follows for everything but the rounds: what to read, the setup round, the brief, the
judging and the record are townhall's steps 2 to 4 and 8, unchanged. It hands its record to `makeadr` as townhall
does, and reads seats from the same neighbours doc, with `neighbour-check` for what limits each one and
`tier-select` for the debaters' models.

**The smallest use:** "guided-townhall: should X or Y?", townhall's setup round plus the rails below, then one
debater, your turn, the next debater, and so on, three rounds and a closing round, a recommendation and a record.

## Config

Edit these lines here, or put the same lines in a `pitmaster.md` at your project root, which wins. Every line is
optional; townhall's own settings (`record_dir`, `neighbours`, `rounds`, `positions`, `cost_line`) apply as they
are.

```
name: the user          # who the skill speaks to; "name: Alex" makes it say "Alex"
citation_check: on      # on | off: the judge checks each turn's load-bearing citations before the next speaker (G3)
seat_fallback: on       # on | off: a stand-in named at setup takes a failed seat; off asks every time (G3)
inline_pack: auto       # auto | off: a seat that cannot open files gets the pack and the debate inline (G3)
word_cap: 0             # words per debater turn; 0 means no cap (G3)
plan_review: on         # on | offer | off: a blind review of the recommendation before the record (ADR-039)
```

The owner ruled the rails optional, 2026-11-12: *"A lot of these seem like they should be optional, including word cap"*
(G3). The setup round shows each with its setting, and any can be switched there.

## Steps

1. **Read first and set up**, as townhall's steps 2 and 3 say, with three additions to the setup round:
   - **The rails** (G3): show the five settings above with their values; the user may switch any.
   - **The stand-ins** (G3, seat_fallback on): for each seat, a stand-in that may take it if it fails mid-run: the
     same neighbour on another model (Antigravity's Flash for its default model), or another name on the allow
     list from a different family. No stand-in means the run asks at the user's next turn.
   - **The preflight** (G3): before round 1, prove each seat can be seated: it answers (`scripts/neighbours.py
     --only`), it has quota left (`neighbour-check`), and nothing on the platform refuses it (a hook or tier gate
     that vetoes a model by name). A refusal goes back to the user in the setup round, with the gate's own reason.
     **Never relabel a job to get past a gate**; the user picks another seat, or changes the gate themselves.
2. **The brief**, as townhall's step 4, plus: each seat speaks in turn, sees every earlier turn and the user's
   notes, answers the user's notes first, and (with `word_cap`) keeps under the cap. Start the run's folder with
   `scripts/turns.py init`, naming the seats, the allow list and the pack.
3. **A turn** (G1). `scripts/turns.py next` names who speaks; `scripts/turns.py prompt` builds that seat's whole
   message: the user's open notes as section 0, verbatim and numbered; a question the user asked it; this round's
   ask; the debate so far; the pack by path, or inline for a seat that cannot open files (`--inline`;
   `scripts/turns.py send` posts it to a local model's server). Seats speak **one after another, never in
   parallel**, so no seat repeats a point another has just withdrawn. Record the reply with `turns.py add`.
4. **The judge's check** (G3, citation_check on). Before the user's turn, the judge checks the turn's
   load-bearing citations (those a decision would rest on) against the files they cite, and appends what it found
   with `turns.py check`: *verified*, or what the file says instead. A seat with two false citations in a run has
   every citation checked from then on, and the record says so. The next speaker sees the check.
5. **Your turn** (G1, G2). Show the turn (as townhall's `watch` says) and its check, then wait. The user may:
   - **pass**: "go", or an empty reply. The next debater speaks at once. (`turns.py pass`)
   - **leave a note**: any other words. Kept verbatim as the next numbered section-0 item (0.1, 0.2…); every seat
     answers it first, by number, in its next turn, once. Never paraphrased: what the seats answer is what the
     user typed. (`turns.py note`)
   - **ask one seat**: "@codex: which pin did the sizing miss?" That seat speaks next, even out of order, and
     answers it before its turn. One question waits at a time. (`turns.py ask`)
   - **change the seats**: drop, swap or add a seat, allow list only, each new seat preflighted as in step 1. A
     seat swapped in mid-round speaks in that round. (`turns.py seat`)
   - **steer the run**: "close" goes to the closing round now; "one more round" adds a round; "reset" restarts the
     round with new settings (townhall's step 5); "stop" ends it without a recommendation, and the record says
     where it stopped.
   When it is unclear which the user meant, ask in one line; never guess a note into a steer.
6. **A seat fails** (G3). A seat that errors, runs out of quota or is refused mid-run: with `seat_fallback` on, its
   stand-in takes the seat (`turns.py seat swap`) and the user hears it at their next turn, with the error; with it
   off, or no stand-in, the lead asks at that turn. A refusal is never worked around (step 1).
7. **Rounds and the close.** When `turns.py next` says the round is done, start the next with `turns.py advance`.
   Townhall's guard (step 6) and closing round (step 7) apply; the closing round is `turns.py advance --closing`.
8. **The plan-review** (`plan_review`, from the 2026-11-12 run). Before the record, a reviewer who did not sit
   sees the evidence pack and the recommendation with its reasons, never the turns or anyone's leaning, and says
   what the plan gets wrong and what everyone missed. Debaters all read the judge's pack, so a premise wrong there
   is wrong in every turn; this pass is the one voice that did not inherit it. Its findings are hypotheses: the
   judge checks each load-bearing one against the file it cites, and only a checked one changes the
   recommendation. `offer` asks first; `off` skips it.
9. **Judge and record**, as townhall's step 8, with two more parts: **Your turns**, the table `turns.py log`
   prints (every pass, note verbatim, question and seat change, in order), and, when it ran, **the plan-review**,
   each finding with the judge's check. Run townhall's `scripts/record-check.py` on the record. For a decision,
   offer makeadr.

## Never

Everything in townhall's *Never* list, and:

- **Paraphrase the user's note** to a seat: it goes verbatim, numbered.
- **Run seats in parallel**: a guided round is in order, each seat seeing the last.
- **Get past a gate by relabelling the job**; a refused seat goes back to the user.
- **Let a check change a turn**: the judge's check is appended below it; the debater's words stay as said.

## Platform notes

- **Claude Code:** the setup round is one `AskUserQuestion`. The user's turn is an ordinary reply, not a question
  box: show the turn and its check, then end the reply and wait. Debaters are as in townhall (`Agent` subagents
  kept going with `SendMessage`; `outside` for Codex, OpenCode and Antigravity; `lanes` or `scripts/turns.py send`
  for a local model's server). A hook that refuses an `Agent` spawn by model or class is the gate step 1 means:
  read its rules for each seat's model and the class the brief will name, before round 1. Antigravity run headless needs
  `--add-dir` for each folder it should read, or it quietly refuses the reads. `scripts/turns.py` is
  standard-library Python with a `--self-test`.
- **Cowork / claude.ai:** no subagents and no scripts: seat only neighbours the tool can reach, keep the notes and
  turns in the chat by hand (each note quoted, numbered), and skip the record check. With nobody to seat, offer
  talk-through.
- **Codex:** debaters are Codex subagents where your Codex has them; ask the setup round as a numbered list; the
  user's turn is an ordinary reply.
- **Other tools:** the setup round is a numbered list in one message, the defaults first; the rest as above.
