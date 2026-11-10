---
status: accepted
status-note: — ratified by the owner 2026-11-10
ratified-by: the owner
ratified-on: "2026-11-10"
owner: the owner
kind: process
built: landed
proof: "`skills/makeadr/SKILL.md`, `skills/bbq/SKILL.md`, `skills/goforit/SKILL.md`, `skills/carte-blanche/SKILL.md`, `skills/looseends/SKILL.md`, `scripts/check-adr-sized.py`, `evals/makeadr-no-06/prompt.md`"
supersedes: nothing
amends: nothing
---
# ADR-036 — bbq, goforit and carte blanche flag ADR-sized decisions, and makeadr is offered once, at the close

This is the published version of this decision. Some internal details have been left out.

## Decision

1. **makeadr owns one test: "Is it ADR-sized?"**. An answer or call is ADR-sized when it will still bind a
   later session **and** at least one of these holds:
   1. it chose between two or more options that each had merit;
   2. it fixes something other work will build on (a file format, a folder layout, a dependency, where data
      lives, a name others will call);
   3. it sets a standing rule ("from now on", "always", "never");
   4. it overrules the recommendation;
   5. it touches, narrows or reverses an existing ADR.

   Not ADR-sized: a mechanism with one plain answer; a choice that only shapes this run (its order, its budget, who
   leads).
2. **bbq, goforit and carte-blanche carry a checked copy of the test**. Each holds the same short paragraph;
   makeadr's section is the master, and `scripts/check-all.py` fails when a copy drifts from it. makeadr is loaded
   only when the user picks a candidate, so a run with none never opens it.
3. **Every bbq except the ADR type watches for candidates**: untyped, Overnight, Arc, Debt, Week and the
   rest, and Skill and Tool for side decisions their own ADR does not cover.
   - Grounding (step 2) also reads the decisions index's one-line rows (number, title, status), and nothing else
     until an answer touches an ADR. No scripts are loaded.
   - Each round's closing line names them beside the owed questions: "Owed: 2 (budget, landing) · ADR candidates:
     1".
   - The record keeps an **ADR candidates** list, each with the question that raised it and the signs it showed;
     with none, it says "ADR candidates: none".
4. **Decisions made while building are flagged the same way**. goforit, goforitreally and carte-blanche apply
   the test to the calls they park or take mid-build and list the ones that pass as ADR candidates in their end
   summary. They never write or ratify an ADR on their own; under a grant nothing is drafted, only listed.
5. **makeadr is offered once per run, at the close, and only when a candidate is left**, so it is loaded and
   offered as rarely as the work allows. Never mid-round. The user picks which candidates become ADRs.
   Each picked one goes through makeadr's light route, written from its cited answer, so nothing is asked twice.
   One the user skips stays listed as "not an ADR, by the user" and is never offered again.
6. **What a candidate becomes follows makeadr's own test**. A candidate that touches an existing ADR is an
   amendment, a new ADR with an `Amends:` line, or a supersede, by makeadr's rules, with ADR-005's one-line notice
   (amendment of 2026-10-29) when makeadr picks amend.
7. **looseends reads the ADR candidates list** the way it reads Owed lists, so a candidate neither picked nor
   skipped is a loose end. Batch and stew bbqs inherit the rule, each item or block keeping its own list.
   dealers-choice is not edited: its picks run under carte-blanche's rules.

## Context

Drivers:
- Decisions get recorded where they are made, not found later by a sweep.
- The user stays the filter: nothing becomes an ADR without the user's pick.
- makeadr is loaded and offered as rarely as the work allows.
- One wording of the test, so the skills cannot drift apart.

## Alternatives

### Where the test lives: makeadr, with checked copies (chosen: one master, and makeadr is not loaded every run)
- Good: the wording sits beside the rules for writing an ADR; the copies are checked, so they cannot drift.
- Bad: three copies of one paragraph to keep in step, carried by a check.

### bbq owns the test
- Good: next to the rounds where it is watched.
- Bad: goforit and carte-blanche would point into a planning skill for a building rule.

### bbq reads makeadr's section by path, with no copies
- Good: no copies.
- Bad: breaks where makeadr is not installed, or the path differs by platform.

### Load makeadr on every run
- Good: the simplest wiring.
- Bad: makeadr opens on every bbq, which the user ruled out.

### At the close: offer, the user picks (chosen: the user is the filter, nothing is asked twice)
- Good: skipped candidates are recorded and never raised again.
- Bad: one more question at the close, on runs that have a candidate.

### Draft every candidate as a proposed ADR
- Good: nothing slips.
- Bad: every candidate costs a ratify-or-reject, and weak ones arrive pre-written. The same went for drafting under
  a grant.

### List only, never offer
- Good: the quietest.
- Bad: the user has to remember to start makeadr; decisions made in ordinary runs are then found only by a later
  sweep.

### Mid-build calls in a later ADR
- Good: a smaller first change.
- Bad: decisions made while building, where most of them pile up, stay unflagged, and a second ADR re-explains
  the same test.

### A sweep for past decisions in this ADR
- Good: catches what was decided before this lands.
- Bad: a different job, finding old decisions rather than flagging new ones. The user moved it to its own tool or
  skill, next.

## Consequences

- Easier: a run that settles an ADR-sized decision says so as it happens, and the user picks at the close which
  ones become ADRs. A run with no candidates costs one line in its record and nothing else.
- Harder: three skills carry a paragraph they must not edit on their own; a change to the test is a change to
  makeadr's section, then the copies.
- Commits the project to: makeadr's new section, the copies and their rules in bbq, goforit and carte-blanche, a
  line in looseends, a copy check in `scripts/check-all.py`, a should-not-trigger eval case for makeadr, the patch
  bump with `scripts/sync-manifests.py` and a CHANGELOG line, and this ADR's public copy.

Steps, each with its test:
1. **makeadr's *Is it ADR-sized?* section**, the master. Test: the copy check reads it.
2. **The copy check**, in `scripts/` and listed in `scripts/check-all.py`: the paragraph between matching markers
   in bbq, goforit and carte-blanche equals makeadr's. Test: its `--self-test`, with a red arm (one changed word
   in a copy must fail it).
3. **bbq**: the copy; step 2 reads the index's rows; step 3's closing line names candidates; step 5's record keeps
   the list; step 7 makes the one offer. Test: the copy check passes; read-through against rules 3 and 5.
4. **goforit and carte-blanche**: the copy, and candidates listed in the end summary with one offer at the close.
   Test: the copy check passes; read-through against rules 4 and 5.
5. **looseends**: the candidates list is read as a loose end. Test: read-through against rule 7.
6. **A should-not-trigger eval case for makeadr**: a plain bbq opener ("bbq: tonight's overnight queue") does not
   load makeadr. Test: `scripts/run-trigger-tests.py` on it.
7. **The house steps**: patch bump, `scripts/sync-manifests.py`, CHANGELOG, `scripts/publish.py --dry-run`
   (failing only on this ADR's pending public copy is expected).

Confirmed by: the first non-ADR bbq record after the merge carries an ADR candidates line (even "none"), and its
rounds show the count beside Owed.

Revisit when: the orphaned-decisions tool or skill is decided, or a sweep after this lands still finds many
decisions that no record listed.

## Asks left open

None. A sweep for past decisions that no record listed is its own next piece of work, as a separate tool or
skill.

## History

- 2026-11-10: proposed.
- 2026-11-10: ratified by the owner.
