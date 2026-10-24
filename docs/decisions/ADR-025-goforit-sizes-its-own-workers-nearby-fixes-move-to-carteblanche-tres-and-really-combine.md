---
status: accepted
status-note: — ratified by the owner 2026-10-24
ratified-by: the owner
ratified-on: "2026-10-24"
owner: the owner
kind: process
built: partial
proof: "`skills/goforit/SKILL.md`, `skills/carte-blanche/SKILL.md`, `skills/dealers-choice/SKILL.md`, `README.md`"
owed: "goforit's description reworded for rule 2 once its trigger tests are reliable"
supersedes: nothing
amends: ADR-023 §The rules, rules 1, 4, 5 and 11
---
# ADR-025 — goforit sizes its own workers, nearby fixes move up to carteblanche, and tres- and -really combine

This is the published version of this decision. Some internal details have been left out.

## Decision

The grant ladder keeps its four words and its order (ADR-023), with two permissions moved so each step adds about
the same. **Plain goforit sizes itself** the way goforitreally does, and may start as many workers as its estimate
allows, not just two. **Nearby fixes move up to carteblanche:** goforitreally fixes only what the plan can't land
without, inside the plan's own pull request, and writes anything else down for later; fixing whatever nearby
problem is worth doing is carteblanche's, because picking work is what carteblanche is for. Separately, **tres- and
-really were checked and both hold**; where one skill has both, they combine, tres- first and -really last, each
keeping its own meaning. Ratifying, taste and the other limits of ADR-023 are unchanged.

## Context

Drivers:
- Each word up the ladder should add about the same amount, so the steps are easy to remember (ADR-023's first
  driver).
- A build under -really never stalls on a fix it needs.
- Every -really word should mean the same thing: finish and merge, not "do more".
- Doctrine, function then ours then compatibility: the words and their order are kept; only what each allows moves.


## The rules

1. **goforit's size** (amends ADR-023 rules 4, 5). Plain goforit estimates points, PRs and workers as
   goforitreally does (`skills/goforit/SKILL.md` step 8): at or under `warn_at` it starts without a word and the
   estimate is the budget; above it, it says "This looks big" and offers go, trim or back out. It may start as many
   subagents as the estimate allows. It still never starts a fresh session or a swarm; those stay carteblanche's.
2. **What goforitreally works on** (amends ADR-023 rule 1). The plan, plus any fix the plan can't land
   without (its checks fail until it is made), inside the plan's own PR. Anything else it finds is written down
   (the debt list, or its end summary) and left. goforit stops and asks about the same blocking fix, as ADR-023
   rule 3 has it.
3. **What carteblanche works on** (amends ADR-023 rule 1). Any work in the project, nearby fixes included,
   blocking or not, each in a PR of its own where that reads better. trescarteblanche the same, in the projects
   named.
4. **tres- holds**. ADR-023 rules 7 and 8 stand. tresdealers-choice gains the line the other two tres sections
   already have: reaching past the named projects asks first.
5. **-really holds**. ADR-023 rule 11 stands. With rule 2 above, goforitreally is now exactly goforit plus
   -really: it finishes and merges, and widens nothing.
6. **tres- and -really combine** (adds to ADR-023 rule 11). Where a skill has both, one word carries both:
   tres + the skill's word + really ("treslooseendsreally"). tres- keeps its scope meaning and -really its
   all-the-way-through meaning; together they grant nothing either lacks alone.
7. **No new tres- or -really words now**. Each is added when a skill needs it (ADR-023 rule 11's last line).

**The ladder, as the README will show it:**

| the agent may… | goforit | goforitreally | carteblanche | trescarteblanche |
|---|:-:|:-:|:-:|:-:|
| build the plan you settled, with workers as its estimate allows | ● | ● | ● | ● |
| make a new choice itself and write it down, so you can veto it | | ● | ● | ● |
| merge its own pull requests without asking, once the checks pass | | ● | ● | ● |
| pick its own work, nearby fixes included | | | ● | ● |
| start new sessions and swarms | | | ● | ● |
| work in more than one project (the ones you name) | | | | ● |

## Build steps

After ratification, in one PR with a patch bump and a CHANGELOG line:

1. `skills/goforit/SKILL.md`: step 8 sizes plain goforit too (rule 1); step 4 drops the two-subagent cap for an
   estimate-sized one; step 7 says goforitreally fixes only what the plan can't land without and writes the rest
   down (rule 2); the description follows. Test: `scripts/run-trigger-tests.py` keeps every goforit case passing.
2. `skills/carte-blanche/SKILL.md`: the grant table names nearby fixes as carteblanche's (rule 3). Test: the
   carte-blanche cases still pass.
3. `skills/dealers-choice/SKILL.md` §tresdealers-choice: the "reaching past the list asks first" line (rule 4). Test:
   the dealers-choice cases still pass.
4. `README.md`: the dot chart of the four words becomes the table above.
5. The two tres- candidates, spend-ledger and swarm-bottleneck, are noted as owed work.
6. `scripts/check-all.py` and `scripts/publish.py --dry-run`.

**Confirmed by:** the user reading the first goforit voyage that starts more than two workers, and the first
goforitreally voyage that meets a problem outside its plan.
**Revisit when:** a goforit estimate starts more workers than the user meant, or a "blocking" fix under
goforitreally turns out to be wider than the plan needed.

## Alternatives

### Size goforit by estimate and move nearby fixes up, with the table regrouped (chosen: the user's direction)
- Good: goforitreally adds two things over goforit, carteblanche two over goforitreally; the ladder reads in even
  steps
- Good: goforitreally becomes the plain -really of goforit, the same as every other -really word
- Bad: plain goforit gains a sizing step it never had, so a small build says one more line
- Doctrine: function first; the words stay ours and in the order the user set

### Regroup the README table only (not chosen)
- Good: no rule changes; a README edit
- Bad: goforitreally would still widen scope, unlike every other -really, and the regrouping would hide that

### Fix nothing outside the plan under goforitreally (not chosen)
- Good: the strictest line between goforitreally and carteblanche
- Bad: a build whose checks need one nearby fix stalls until the user or carteblanche picks it up

### goforitreally asks about a nearby problem (not chosen)
- Good: the user sees every problem before anything outside the plan is touched
- Bad: -really would stop before ratify, against ADR-023 rule 11

### Keep goforit at two workers unless the user gives a number (not chosen)
- Good: closest to today
- Bad: one more thing the user must say for a build that needs three workers

### Eight-row README table, one row per permission (not chosen)
- Good: nothing grouped
- Bad: uneven steps (2, 2, 3, 1); a nearby fix and picking work read as two ideas when they are one

### Leave tres- and -really combining unruled (not chosen)
- Good: nothing to write until a second skill has both
- Bad: a later skill could order or read the two differently

## Consequences

- Good: the README's dot chart shows each word adding about the same
- Good: goforitreally, like every -really word, means finish and merge
- Bad: plain goforit can now start more workers than before, inside its estimate; `warn_at` is what stops a big
  one without a word
- Bad: "can't land without" is a judgement; a wide reading lets goforitreally drift toward carteblanche
- Commits us to: the build steps above, the README's table, and the two tres- candidates noted as owed work

## History

- 2026-10-24: proposed.
- 2026-10-24: ratified by the owner.
