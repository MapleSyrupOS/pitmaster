# The types

A type is a name, what to read first, and where the record goes.

| type | reads first | record goes to |
|---|---|---|
| **ADR** | the decisions index, any open decisions queue, past rulings | the record, then the ADR itself: `makeadr` owns it |
| **Overnight** | `budget-select` (the Budget block), the status file's *next* section, the last voyage's handoff and ledger | the voyage's record, which is the prompt |
| **Arc** | the arc's board (its README), its newest digest or rulings | the arc's own folder: a `<arc>-PROMPT-<date>.md` for the next lead |
| **Debt** | the debt list, any census a prior voyage left | the voyage's record. New debt is filed in the debt list by the lead only |
| **Morning** | the open decisions queue, the night's digest | `rulings-<date>.md` beside the voyage. Resolved queue entries move to the queue's archive |
| **Host** | the host's record and its runner script | the same host record, with each change and its undo |
| **Week** | `budget-select`'s *48 hours before the reset* section and its calibration file's use-it line | the voyage's record, plus the day's line in the calibration file |
| **PR** | the reviewer's report, the PR's file list against the main branch | `rulings-<date>.md`: each finding walked and ruled |
| **Cloud** (own session) | the project's rules for cloud sessions, its CI path to any host the container cannot reach, the last cloud voyage's record and hand-off | the voyage's record, which is the prompt (see `cloud-and-away.md`) |
| **Skill** | the skills folder the new skill will join, the skills it should call or avoid, an example of the job it does | the record, then the skill folder itself (see `skill-type.md`) |

These are the usual places; find the project's equivalents with `ls` and `grep`. A file that does not exist is
skipped, and the record says so. The table seeds step 2's reading; it does not limit the questions.

## Adding a type

Add rows in the same three columns to the file the config's `types` names (`docs/bbq-types.md` in your project by
default; make it on first use). They
join the table above, and a row with a built-in type's name replaces it. Add "(own session)" after the name of a
type that should always write a prompt for a fresh session.
