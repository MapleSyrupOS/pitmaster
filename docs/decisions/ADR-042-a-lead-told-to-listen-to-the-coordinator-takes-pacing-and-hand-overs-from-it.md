---
status: accepted
status-note: ratified by the owner 2026-11-13
ratified-by: the owner
ratified-on: "2026-11-13"
owner: the owner
kind: process
built: partial
proof: "`skills/carte-blanche/SKILL.md`, `skills/bbq/SKILL.md`, `skills/budget-select/SKILL.md`, `skills/call-escalator/SKILL.md`"
owed: baton's line (step 7, in baton's own change, which waits on ADR-040); the two field tests of step 9, judged by the user
supersedes: nothing
amends: ADR-007 §The rules, rules 5 and 7, and §Amendment — 2026-10-21, part 1 (a widening relayed by the coordinator); ADR-041 §Decision, rule 8 (a hand-over the coordinator orders)
---
# ADR-042 — A lead told to listen to the coordinator takes pacing and hand-overs from it

This is the published version of this decision. Some internal details have been left out.

**Confirmed by:** trigger tests on the two words: a message that only mentions a coordinator or a supervisor
in passing must not load carte-blanche, turn the tick on or be taken as an order, and a real grant with the tick
must. As field tests, each written up as a field report and judged by the user: a live test with one lead and one
coordinator session, and the first real coordinated comrun
**Revisit when:** the platform gives a session a way to check that a message carries the user's own words; baton
(ADR-040, proposed) is ratified or turned down; a raise relayed under the tick turns out to have carried a wrong
quote

## Decision

A lead's grant can carry one more tick, **"Listen to the coordinator"**. A lead that has it takes two things from
the session coordinating its comrun, without the user repeating them in the lead's own session: changes to its
pacing, and an order to hand a stuck problem to a reader. Nothing else can be passed down. There is no new skill:
the tick lives in carte-blanche, where grants already live.

1. **The tick.** carte-blanche's question "Anything extra to grant?" offers "Listen to the coordinator". It is
   off unless the user turns it on. Any lead with a written grant can be given it: a lead under carte blanche, and a lead whose
   authority is the rules of a bbq record; bbq asks the same question for a comrun that has a coordinator.
2. **What it covers is a closed list of two:** pacing, and hand-overs the coordinator orders. Pacing is how much and when, never what a lead may
   do: its stop lines, its caps (workers, outside-model seats), its slots, the order of its work and its share of
   the budget. Adding a third thing to the list takes an ADR.
3. **A raise needs the user's words.** The coordinator relays a raise only by quoting what the user told it,
   word for word, with when it was said. A lead refuses a raise that carries no quote. Narrowing, handing out slots
   and setting the order stay the coordinator's own call, as they are today.
4. **A ceiling is optional.** With the tick the user may name figures ("hard stop up to 90 %, outside-model
   cap up to 6"). A dial with a figure cannot be raised past it by relay: past it, the user says so in the lead's
   own session, as every widening needed before this ADR. A dial with no figure follows the quote.
5. **Hand-overs.** A coordinator whose own grant names hand-overs
   (ADR-041 rule 8) may tell a lead to hand a stuck problem to a reader, and a lead with the tick does so without
   asking the user. The hand-over is read-only: the coordinator cannot grant a place to test, which stays the
   user's. ADR-041's limits stand: two hand-overs at most on one problem without the user's word, and a `DESIGN:`
   verdict goes to the user. The hand-over is paid from the lead's share.
6. **The coordinator passes down only what it holds.** Never wider than its own grant. The `never:` list and every
   act that needs a named grant (merging, pushing to main, deleting work, outward-facing acts) cannot be passed
   down by any wording.
7. **Who the coordinator is.** The tick follows the role: when the coordinator changes, a lead listens
   to the new holder at once. Where baton is in use, the lead reads who holds the role from baton before it takes
   a relay, and takes it only from that session. Where baton is not in use, the grant names one session, and the
   tick cannot follow a change of coordinator. The role is written "coordinator"; "supervisor" means the same
   role.
8. **How the tick is given.** By the user's own answer in the lead's session, or quoted in the lead's
   starting brief with when it was given: the user ticks once, in the coordinator's session or the bbq, for the
   leads the comrun starts. An agent never ticks it for itself: not a bbq that answers itself under carte blanche,
   and not a brief that claims the tick without the user's quote.
9. **The trail.** The coordinator logs every use: each raise it relays and each hand-over it orders is one
   dated line in its own notes, with the user's quote. A lead that refuses a relay says why in one line to the
   coordinator: no quote, the wrong session, past the ceiling, or not covered.
10. **The ceilings above every grant still hold.** The project's rules and the platform's safety rules win, as
    ADR-007 rule 4 says. Where the platform refuses a relay the tick allows, the lead says so and the user's own
    word is needed.

**This amends ADR-007.** §Amendment — 2026-10-21, part 1 ("It is never relayed to a running worker by message")
gains one exception: a lead whose grant says "Listen to the coordinator" takes a raise to its pacing relayed by
the coordinator, as rules 3, 4 and 7 here say. §The rules, rule 5: the second question offers the tick. Rule 7: the
written block gains the tick's line.

**This amends ADR-041.** §Decision, rule 8 ("hands over without asking only when the grant names hand-overs")
gains a second route: or when the lead's grant has the tick and a coordinator whose own grant names hand-overs
orders it.

The line the written grant gains:

```
Listen to the coordinator: no | yes, given by <name> on <date> ("<their words>").
  Coordinator: whoever holds the baton | <session>. Covers pacing and hand-overs it orders, nothing else.
  Ceilings: none | <each dial, with its figure>
```

## Context

Drivers:
- The user's words stay the source of every raise.
- One sentence to the coordinator reaches the whole fleet, with no pasting.
- A wrong or false relay can cost usage and nothing else.
- Grants keep one home.

## Alternatives

### A tick in the lead's own grant (chosen: the user's answer in the lead's grant is what the rule already accepts)
- Good: the lead heard the permission from the user, so it trusts no relay for the authority, only for the
  figure.
- Good: it sits in a question carte-blanche already asks, beside ADR-041's hand-over tick.
- Bad: it rests on the coordinator quoting the user truthfully. The ceiling and the usage-only list limit what a
  wrong quote can do; nothing checks the quote itself.

### A new permissions skill
- Good: one place for everything about a coordinator. It was the user's opening question.
- Bad: grants would have two homes. ADR-023 kept "tres-" as a mode of an existing skill for the same reason.

### A range written into each lead's brief (the first recommendation; replaced by the tick)
- Good: a move inside the range is a pacing call, so the widening rule is never touched.
- Bad: the coordinator writes the brief, so the authority would sit in the coordinator's text. The tick puts it
  in the user's answer. The range survives as rule 4's optional ceiling.

### The tick covers everything carte blanche covers (not picked)
- Good: fewer pastes, merges included.
- Bad: a wrong relay could then push to main or delete work, which cannot be undone.

### The coordinator raises on its own judgment, under a ceiling (not picked)
- Good: the fewest interruptions.
- Bad: a coordinator's mistake could spend up to the ceiling before the user saw it. The user chose that every
  raise needs their words.

### The coordinator may grant a place to test (not picked)
- Good: a hand-over it orders could prove its finding.
- Bad: a failed test can cost a wiped disk or an hour of building, more than usage.

### A ruling file only the user writes, or one command that sends the user's words to every lead
- Good: no pasting.
- Bad: any session on the machine can write a file, and a command's output is still a message from another
  session. Both were suggested by the session that met the problem.

### Keep the pasting, made one line to copy
- Good: the strongest proof, since each lead hears the user directly.
- Bad: it is the cost this ADR removes. It stays the route for everything outside the tick.

## Steps to build

Each step with its check. `python3 scripts/check-all.py` and `python3 scripts/publish.py --dry-run` run after all
of them.

1. **carte-blanche**: the tick in step 2's second question; step 6's widening rule gains the exception; the
   written grant gains its line; the Claude Code note ("`SendMessage` may only narrow it") gains the same
   exception. Check: the trigger tests of step 6 below.
2. **bbq**: a comrun with a coordinator asks "Listen to the coordinator?" once, and the record carries the answer
   in the user's words.
3. **budget-select**: the Budget block says who may raise the hard stop and any ceiling named.
4. **call-escalator**: step 3 gains the coordinator's route beside "the grant names hand-overs".
5. **The word**: a glossary entry for "coordinator" that says "supervisor" means the same; the L7 row of
   `skills/tier-select/leads.md` gains the word.
6. **Trigger tests**: carte-blanche cases where "my supervisor at work said…" and "the coordinator is slow today"
   set nothing off, and one where a grant with the tick does.
7. **baton** (a draft skill, in its own change): the lead's rule gains "take a relay only from the id
   `who --id` prints".
8. The plugin's patch version, the CHANGELOG line and the public copies, as every `skills/` change needs.
9. **Field tests**, when a coordinated comrun next runs: the live two-session test and the first real comrun, each
   a field report.

## Consequences

- Good: a ruling for the whole comrun costs the user one sentence, to the coordinator.
- Good: a fleet no longer sits on mixed rules while the user pastes.
- Good: pitmaster writes down the coordinator role for the first time, in the glossary and in the grant.
- Bad: a lead cannot check the quote. A coordinator that mishears the user, or is fed false text, can move a
  dial as far as the ceiling, or as far as the quote says where there is none.
- Bad: baton's pointer can be written by any session on the machine. It shows who holds the role, never what the
  user allowed.
- Bad: whether the platform lets a relayed raise or hand-over through is untested. Rule 10 says what a lead does
  when it does not.
- Bad: carte-blanche's steps grow.
- Commits us to: the steps above; the field reports of step 9; one more line in the draft handoff skill's kickoff, so the tick's
  line travels with the grant.

## Asks left open

1. Ratify ADR-042 as written? The one "ratify" also covers its changes to ADR-007 and ADR-041.
2. After ratification: build steps 1 to 6 and 8? Step 7 belongs to baton's own change.

## History

- 2026-11-13: proposed.
- 2026-11-13: ratified by the owner.
