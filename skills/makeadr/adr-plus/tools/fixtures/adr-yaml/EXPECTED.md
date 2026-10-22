# tools/fixtures/adr-yaml: what each fixture must do

`python3 tools/adr-yaml.py --self-test` reads this table. A **good** or **warn** fixture is an ADR the converter
reads: it must convert, prove lossless, and raise exactly the warning kinds named. A **bad** fixture is a file that
already has a YAML header: the schema must refuse it with the words named. Each fixture has one expected verdict: good, warn or bad.

| fixture | verdict | detail | what it targets |
|---|---|---|---|
| `good-bold.md` | good | warnings=owner-from-settings | The bold-line header, every field present, a ratifier and a date the converter recognises |
| `good-glyph-paragraph.md` | good | warnings=glyph-before-verdict,owner-from-settings | A demoted record's shape: a demotion banner, a glyph before the verdict, a Status paragraph wrapped over two lines |
| `good-partial.md` | good | warnings=owner-from-settings | A PARTIAL Built line with `; owed:`, a Supersedes with a reference |
| `good-mapped-verdict.md` | good | warnings=owner-from-settings,verdict-mapped | `RATIFIED BY ALEX 2026-09-10 (live sitting)` becomes `status: accepted`; the whole old wording leads `status-note` and round-trips byte for byte; the ratifier and date are still recognised |
| `good-mapped-draft.md` | good | warnings=owner-from-settings,verdict-mapped | `DRAFT` becomes `proposed`, so no ratified-by or ratified-on is written and `unparsed:ratified` does not fire |
| `good-madr.md` | good | warnings=kept-in-body:date,kept-in-body:decision-makers,kept-in-body:informed,missing-section:Alternatives,missing-section:Consequences,missing-section:Context,missing-section:Decision,missing:amends,missing:built,missing:kind,missing:supersedes,owner-from-settings,unparsed:ratified; schema=invalid | MADR 4.0 front matter: status and consulted move, the rest stays as bold lines under the title, every missing ADR+ field and section is named |
| `good-classic.md` | good | warnings=missing-section:Alternatives,missing:amends,missing:built,missing:kind,missing:supersedes,owner-from-settings,unparsed:ratified; schema=invalid | Classic Nygard: the `## Status` section moves, nothing is invented |
| `good-amended-label.md` | good | warnings=kept-in-body:label,owner-from-settings,separator-not-dash,unparsed:ratified | A dated label's shape: a `**Amended YYYY-MM-DD:**` line stands between Status and Built; it ends the Status paragraph and stays in the body |
| `good-labels-between.md` | good | warnings=kept-in-body:label,owner-from-settings | `**Owner:**` and `**Consulted:**` stand between `**Kind:**` and the lineage line; they stay in the body and the lineage line still moves |
| `warn-missing-kind.md` | warn | warnings=missing:kind,owner-from-settings; schema=invalid | A bold-line header with no Kind line: `kind` is left out and named |
| `warn-inline-status.md` | warn | warnings=kept-in-body:status,owner-from-settings,unparsed:ratified | A second `**Status:**` after `**Date:**` stays in the body and is named |
| `warn-lineage-names-no-adr.md` | warn | warnings=lineage-names-no-adr,owner-from-settings | `amends` names a section of another document: the schema accepts any non-empty string, the converter reports it |
| `bad-unknown-field.md` | bad | refuses=date: unknown field | `additionalProperties: false` |
| `bad-retyped-date.md` | bad | refuses=found a date | A date written without quotes loads as a date, not a string |
| `bad-status-yes.md` | bad | refuses=found a boolean | `status: yes` loads as a boolean: the YAML 1.1 trap |
| `bad-proposed-ratified.md` | bad | refuses=ratified-on: not allowed here | A proposed decision carries no ratification date |
| `bad-status-ratified.md` | bad | refuses=is not one of | `ratified` is an older verdict; the schema allows only the seven status words |
| `bad-partial-no-owed.md` | bad | refuses=owed: required field is missing | A partial decision must say what is owed |
