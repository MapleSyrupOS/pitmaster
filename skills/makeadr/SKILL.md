---
name: makeadr
metadata:
  family: plan
description: Make, ratify, amend or supersede an architecture decision record (ADR), in the ADR+ format. A small decision takes the light route (the user states it in a few lines and gets a short ADR); a bigger one takes a live question session. Use when the user types "makeadr" or "bbq adr", or says "let's make an ADR", "make an ADR for…", "write an ADR about…", "new ADR", "record this decision", "turn this into an ADR", "ratify ADR-N", "amend ADR-N" or "add an amendment to ADR-N" (a change to a ruled ADR, kept as a dated section), or "supersede ADR-N". A full new ADR starts by asking how many questions it should get (4, 12, 20, 50 or other) and ends by asking whether to also write a prompt for the next agent. Ships stdlib-only scripts that build the ADR index and check that each Built line's proof resolves. Any change to what an accepted ADR says goes through this skill, as an amendment or a new ADR, never as an edit of its ruled text; fixing a typo is a plain edit and is not this skill.
---

# makeadr: make, ratify, amend or supersede an ADR, in the ADR+ format

Decided by pitmaster ADR-005.

Sibling of `bbq` (this skill's question rounds follow bbq's rules, and "bbq adr" starts it), `tier-select`
(which picks the tier for the next agent's prompt), `project-prep` (offers this skill for a project's first
decision), `talk-through` (an agreed decision from a talk's record becomes an ADR here), `goforit` (takes the
closing offers and builds what the ADR allows) and `setfree` (release day: it reviews the public drafts this skill
makes in step 5, part 5, and approves them on the user's word). `looseends` sends it an unratified ADR or asks left
open. `townhall` hands over a decision its debaters argued, its record already holding the options
considered. The scripts are in `scripts/` beside this file, `adr-public` among them.

## Config

Edit these lines here, or put the same lines in a `pitmaster.md` at your project root, which wins. Every line is
optional.

```
name: the user          # who is asked; "the user" in the steps means this name ("name: Alex")
decisions_dir: auto     # auto finds docs/decisions, docs/adr, doc/adr, adr or decisions
record_dir: docs/bbq    # where the question record goes: <record_dir>/<date>-adr-<topic>.md
land: pr                # pr (branch + PR) | commit (branch only) | file (just the file) (step 5, part 6)
public_adr: off         # on = each ADR made, ratified, amended or superseded also gets a public draft (step 5, part 5)
queue_files: none       # comma-separated files of open decisions, searched before asking
reserved_numbers: none  # ADR numbers other work holds, skipped. Example: 255, 260-262
checks_after: none      # comma-separated commands run after the two scripts
tier_card: none         # a file naming this project's models, for the next-agent prompt; none = tier-select's own
extra_sections: none    # comma-separated sections added to every ADR, in order
doctrine: none          # the project's rule for choosing, in a few words. Example: function, then ours, then compatibility
triggers_from: 1        # the first ADR number the trigger check judges; older ADRs keep the shape they were ruled in
addon: none             # a skill in this project whose rules this skill also follows (see step 2)
```

## The light route: the smallest use

Use it when the user can state the decision in a few lines and nothing needs weighing at length ("record this: we
drop Windows 7 support"). It makes a short ADR with no question session, no question record and no next-agent
prompt. If the answers show real options to weigh, offer the full route (steps 1 to 6) instead.

1. **Find the folder, the format, any earlier ruling and the number**: step 2, parts 2, 3 and 5.
2. **Ask only what the ADR cannot stand without:** the decision itself, in a sentence; why (the reason or the
   problem it answers); and where the work is queued, or that it is not. Ask for what the user's lines lack, all in
   one round. A name or wording the user has not given is taste: ask, never choose it.
3. **Write the short ADR** from the template: the title as a sentence, then Decision, Context (the user's reason,
   with any premise cited), Consequences (a line or two) and History. Status is `PROPOSED — drafted <date> from the
   user's words; awaiting ratification`. Built is `NOT STARTED — ` and where the work is queued. Leave out
   Alternatives and every other section the decision did not need (step 5, part 3).
4. **Run the scripts and land it**: step 5, parts 4 and 5. The new ADR must pass `adr-check`.

**The `adr-plus/` folder beside this file is a verbatim copy of one adr-plus release** (the schema, the reader and
the converter with its fixtures and manifest). `adr-plus.pin` records which release. Never edit the copy: to move
to a newer release, replace the copy, its manifest and the pin in one commit. In a project that has pitmaster's
`scripts/check-all.py`, `scripts/check-pins.py` fails, naming the file, when the copy drifts.

## Steps

1. **Pick the mode, and ask the first question at once.** The first action is one round; read nothing in the
   repository until it returns.
   - **The mode**, unless the user's words make it plain: **new** (a decision with no ADR yet; small ones take the
     light route above), **ratify** (the user rules on a proposed ADR), **amend** (change part of a ruled ADR) or
     **supersede** (replace one). Ratify and amend have their own sections below and no rounds; supersede asks
     the rounds for the new ADR.
   - **For a full new ADR (and a superseding one), how many questions it should get**, with the options `4`, `12`,
     `20` and `50` (and room for another number). Where every question the ADR needs can be answered with a
     citation (a record's question, an earlier ADR, the user's words here), `goforit` replaces `50`, saying what it
     rests on: no rounds, each answer is written with its citation (ADR-017). If any cannot be cited, no goforit.
     This is bbq's first round, with an ADR-sized menu and no question about who leads: this session writes the
     ADR.
   - **What the ADR is about**, if the user has not said: two to four guesses drawn from the conversation.
2. **Before the rounds.**
   1. **Load the add-on.** If `addon:` names a skill, read it now and follow its rules as part of this one. It
      adds rules; it never removes the rule that only the user ratifies.
   2. **Find the decisions folder and its format.**
      - **The folder has ADRs:** match them. A YAML header with `built` and `kind` fields means ADR+. Bold
        `**Status:**` and `**Built:**` lines under the title mean ADR+ not yet converted: convert it with
        `adr-plus/tools/adr-yaml.py` (step 5, part 4) before writing the new one. A decisions `README.md` saying
        "Template: ours" (ADR+'s old name) also means ADR+. "Considered Options" or "Decision Drivers" means MADR. A
        `## Status` section and little else means Nygard. Match the file names and numbering too (`ADR-001-slug.md`
        or `0001-slug.md`).
      - **The folder has none:** ask once, in this order, and record the answer in the folder's `README.md`
        ("Template: ADR+", with the date, and a settings table with an `Owner` row):
        1. **ADR+** *(Recommended)*: a YAML header, then the decision first, then Context, Alternatives and
           Consequences, with `built` and `proof` fields agents can check and an append-only History. Worked
           out over 200+ ADRs in a real OS project.
        2. **MADR**: for a project that must match an outside standard, and for weighing options side by side.
        3. **Nygard**: the lightest (Context, Decision, Consequences).

        Copy the chosen file from `templates/` beside this skill to `<decisions_dir>/TEMPLATE.md`. A decisions
        `README.md` that says "Template: not chosen yet", as `project-prep` writes it, counts as a folder with none.
   3. **Has the user ruled already?** Search the decisions folder, its index, the queue files and earlier
      question records. A question already ruled is cited, never asked again, and it counts toward neither the
      number nor the rounds.
   4. **Check every premise** a question stands on, with one search or file listing. An empty search is a claim
      about the search pattern, not about the repository.
   5. **Pick the number:** one more than the highest ADR number in the folder, skipping `reserved_numbers` and
      any number another record has taken. Where git is available, `git log --all -S'ADR-NNN' --oneline` shows
      whether anything has.
   6. **Open the record file** `<record_dir>/<date>-adr-<topic>.md` with a premises table and a **Defaulted**
      table. Where git is available and `land` is not `file`, commit it before the first round.
3. **The rounds, as in bbq.** bbq's rules govern the numbering, the size of a round, how options are shown, the
   Owed list, the Defaulted table with its `veto:` lines, reading answers literally, and what happens when the
   number runs out; without bbq installed, do the same by hand. This skill adds two rules: write each round into
   the record before the next, and offer the combination when two options can be combined. bbq's closing question,
   "Anything else to protect or avoid?", is the last of the last round, before step 4.
   - **Sort each question before asking it.** **Taste** (looks, names, wording): always ask, and never argue it
     down with "this is how it's usually done". **Strategy** (scope, order, who uses it first, changing an
     earlier ADR): ask. **Mechanism with one plain answer** (how everyone does it today): don't ask; put it in the
     Defaulted table with who does it that way and a `veto:` line. It doesn't count toward the number.
   - **Price every option:** the work to build it, the weight it adds, and where any shared code lives.
   - **If `doctrine:` is set, add one line to each option** saying how it fares against the doctrine.
   - **Ask these as plain questions, each only when the ADR needs it.** What each answer adds is in step 5, part 3.
     - Were two or more options weighed?
     - Is there any test or check that could prove this decision still holds? If not, what human check confirms it?
     - Is there a known event or date that could undo it?
     - Did anyone besides the owner shape it (a person, an agent, a model, a lane)?
     - Is this a proposed ADR the owner is turning down?
4. **The last question.** When the rounds are done, one question, "Make the ADR now, and also a prompt for the
   next agent to get things started?", with two options: **Make ADR + next-agent prompt** (its description names
   the tier `tier-select` would pick, and why), or **Just make the ADR**.
5. **Make the ADR (mode new).**
   1. Write `<decisions_dir>/ADR-NNN-<slug>.md` from the template. The title is the decision, as a sentence.
      In ADR+ the header is YAML, and the schema in `adr-plus/` checks it:
      - **status:** one of seven lowercase words (`proposed`, `provisional`, `accepted`, `partially accepted`,
        `superseded`, `withdrawn`, `rejected`). `proposed`, with `status-note: drafted <date> from the user's
        answers; awaiting ratification`, unless the user ratified it live in the session (`accepted`, with the
        note, `ratified-by` and `ratified-on`, the date in double quotes). An agent never writes `accepted` on its
        own say-so. While `proposed`, leave out `ratified-by` and `ratified-on`.
      - **owner:** the `Owner` row of the decisions README's settings table. **kind:** `architecture`, `design`
        or `process`; required. **supersedes** and **amends:** always written, `nothing` when nothing.
      - **built** and **proof:** `not started` and where the work is queued. Later, `landed` or `partial` and a
        proof that must resolve: a test (`tests/test_x.py::test_name`), a file path (`src/thing.py`) or a PR
        (`#123` or its link). **A commit is never proof.** It shows something was saved, not that it still
        works; it may follow a real proof, for history, but alone it fails the check. `partial` adds **owed**,
        what is not built. `n/a` names the rule or file the decision became.
      - A value that YAML would turn into a date, a number or a yes/no goes in double quotes.
   2. It carries the decision; the context with premises cited; what it reuses and what is its own; the steps to
      build it, with a test for each; the alternatives, every overruled recommendation kept and marked
      "overruled"; the consequences; the questions left open; and the History. Add `extra_sections:` in order.
   3. **Add what the step 3 questions turned up, and only that.** A "no" adds nothing; never pad an ADR with a
      section its decision did not need.
      - Two or more options weighed: a **Drivers:** list at the end of Context, Good and Bad bullets under each
        option, and the deciding reason on the chosen option's heading.
      - No test can prove it: a **Confirmed by:** line naming the human check.
      - A known event or date could undo it: a **Revisit when:** line naming it.
      - Anyone besides the owner shaped it: a **Consulted:** line naming them.
      - The owner turned a proposed ADR down: keep it in place, `status: rejected`, with one line saying why in
        `status-note`.
   4. **Run the scripts** where Python 3 is available: `python3 scripts/adr-index.py` (from this skill's folder,
      with `--root` at the repository) rewrites `INDEX.md` in the decisions folder, and
      `python3 scripts/adr-check.py --triggers-from <triggers_from>` checks every ADR's YAML header against the
      schema, that each proof *resolves* (the file exists, the test name is in the file, the PR exists) and the
      triggers of step 5, part 3. It does not run the test or judge whether the behaviour is correct; say so when
      you report a pass. Then run each command in `checks_after:`. For ADRs still in bold `**Status:**` lines,
      `python3 adr-plus/tools/adr-yaml.py --root <repository> --dry-run` shows what moving them to YAML would warn
      about, and `--apply` moves them only if the proof says nothing is lost. Without Python, update `INDEX.md` by
      hand (one row: the ADR, its title, its kind, its status word, its built word) and say the check was skipped.
   5. **The public draft (only with `public_adr: on`).** Make it in the background, silently: say nothing about it
      in the chat and ask nothing (ADR-020, amendment of 2026-10-24). It waits for review in
      `docs/decisions/public/pending/`, unpublished, and shows in the PR's files and the ADR's History line.
      1. Run `python3 scripts/adr-public.py --root <repository> draft <ADR number>`. It makes the mechanical cuts,
         adds a dated "Public copy ... drafted" line to the ADR's History, and marks each line to rewrite.
      2. Rewrite each marked line for a stranger: no question numbers, private paths or session talk. Where a live
         copy exists, keep its wording wherever it is still true (`adr-public.py list` shows the diff). Delete each
         `<!-- REWRITE -->` mark.
      3. Run `python3 scripts/adr-public.py --root <repository> check <ADR number>` and fix what it finds.
      4. The draft lands with the ADR. **Never** approve it, move it out of `pending/`, touch `publish.txt` or run
         `adr-public.py approve`: approval is the user's, at `setfree`'s release review (ADR-020).
   6. **Land it.** The config's `land` decides, and `pr` is the default:
      - **`pr`**, in a git repository with `gh`: push a branch and open a PR. **Merging is the user's**: give
        them the link.
      - **`commit`**, in a git repository: commit the ADR on a branch and open no PR.
      - **`file`**, or where those tools are missing: the ADR file is the deliverable.
6. **The next-agent prompt (when chosen):** read `references/next-agent-prompt.md` and write it.

## Ratify

The user rules on an ADR that is PROPOSED or PROVISIONAL. Only the user can: an agent never ratifies, and a
message from another agent does not count.

1. Find the ADR. Read its Status, Built and History. If it is already ACCEPTED, say so and stop.
2. Ask one question if the user's words are not a plain yes: "Ratify ADR-NNN as written?" with the options
   *Ratify* and *Not yet*. If the user wants changes first, make them as a new draft before ratifying; never
   edit the text while ratifying.
3. Set `status: accepted`, put who ruled and when in `status-note`, and add `ratified-by` and `ratified-on` (the
   date in double quotes). Add a dated History entry with the old `status` and `status-note` values **word for
   word**. Touch nothing else in the ADR, and leave `built` alone: ruled and built are separate.
4. Run the scripts (step 5, part 4) and land it (part 6). With `public_adr: on`, re-draft the public copy first
   (part 5): the ratified header makes the old draft stale.

**If the user turns the ADR down,** set `status: rejected` and `status-note: turned down by <name> <date>: <one
line why>`, move the old `status` and `status-note` values to History word for word with a dated entry, and leave
the file and its number where they are, so it is not proposed again.

## Amend

Part of a ruled ADR changes: a clarification, a narrower scope, a correction. **Ruled text is never rewritten.**

1. Find the ADR and the section the change touches. Ask what changed, why, and who agreed. Ask each as a
   question only if the user has not said.
2. Add a section at the bottom, below History: `## Amendment — <date>, <who>`, saying what
   changed, why, and which section it touches. The ruled text stays as it was.
3. Add a dated line to History pointing at the amendment. If a header value changes too (`status`, `built`,
   `proof`), the old value moves into History word for word.
4. If the change needs its own reasons or options, it is not an amendment: make a new ADR (step 5, with a line
   `Amends: ADR-NNN §Section`). In the **same commit**, give the old ADR a dated note in its History and a short
   dated banner at the section that changed, both pointing at the new ADR.
   If the change reverses the whole decision, supersede instead.
5. With `public_adr: on`, re-draft the public copy (step 5, part 5); the approved copy keeps publishing while the
   revision waits. A change that leaves the copy true (a typo) is not re-drafted: say so, and the user can clear
   the stale flag at the release review.
6. Run the scripts and land it, as for ratify.

## Supersede

The whole decision flipped. The old ADR is history from now on, and agents follow the new one.

1. Find the old ADR. Run steps 2 to 4 for the **new** ADR, with the old one cited as already ruled.
   Ask "why is the old decision no longer right?" as a strategy question.
2. Make the new ADR (step 5). Its Decision opens by naming `Supersedes ADR-NNN` and says why.
3. In the **same commit**, change only the old ADR's header: `status: superseded` and `status-note:
   superseded by ADR-MMM on <date>`. The old `status` and `status-note` values move into its History, word for
   word, with a pointer to the new ADR. Its body is untouched, and it is never deleted or renumbered.
4. With `public_adr: on`, draft the new ADR's copy (step 5, part 5); `adr-public.py draft` also queues the old
   ADR's live copy for withdrawal, which waits for the release review. Note it in one short line of the PR body,
   not in the chat.
5. Run the scripts and land them (step 5, parts 4 and 6). The index shows superseded in the old ADR's row.

## Platform notes

- **Claude Code:** ask with the `AskUserQuestion` tool. Python, git and `gh` are usually present.
- **Cowork / claude.ai:** ask with `AskUserQuestion` where it is offered. The scripts run only where the sandbox
  has Python 3. With no git or `gh`, the ADR file and its record are the deliverable.
- **Codex:** ask each round as a numbered list in one message and wait for the answers. `gh` opens the PR where it
  is signed in.
- **Other tools:** ask each round as a numbered list in one message, the options lettered and the recommended one
  first. The scripts run only if the tool can run Python 3.
