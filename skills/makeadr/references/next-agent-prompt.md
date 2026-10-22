# The next-agent prompt

Write `<record_dir>/<date>-adr-<topic>-NEXT.md`, commit it with the ADR (unless `land` is `file`), and give the
user the text to paste. Choose the tier with `tier-select` (reading `tier_card:` when it is set): local or small
models for reading, the mid tier for building, the large tier only for its classes of work. The prompt names:

- the ADR and the record, both by path;
- the **first step only**, with its test, and a deliberate break the test must catch (a red arm);
- what it must not touch;
- the stop condition (a wrong premise, or a fix that spreads past a few files: stop and report);
- the Budget block from `budget-select`, if that skill is present;
- that a builder's work is checked by a different tier.

If the ADR's first step waits on other work, the prompt says so and gives the part that can start now, or the
user is told it cannot start yet.
