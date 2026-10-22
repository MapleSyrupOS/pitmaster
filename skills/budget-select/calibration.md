# budget-select calibration log

One row per session that dispatched workers, written by its lead before the handoff. K is finished workers'
tokens per point; `budget-select` refits it from these rows. Readings are the meter's weekly percentage, with the
time and time zone.

## Meters

One line per meter: its name, its reset (day and time), its unit if not the default, and who recorded it.

| meter | reset | unit | recorded |
|---|---|---|---|
| (example) Tuesday meter | Tuesday 14:00 UTC | 1 % of the weekly limit | first lead on it, date |
| the owner's other account | Tuesday 14:00 UTC | 1 % of the weekly limit | the 0.4.0 swarm's lead, 2026-10-22 |

## Use-it (the 48-hour plan, once per day per meter)

(meter): none yet.

## Rows

| date | session | meter | lead (model, effort) | share | start → end | worker tokens (by tier) | line fired | overrun | overlap | K (tokens/point) |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-22 | swarm-0-4-0 [766ab5be] | the owner's other account (Tuesday) | Opus 5.5, high | up to the hard stop (75 %) | 4 → 7 | sonnet ≈1.1M (6 builders); local lane 1 job | none | none | shared with 2 sessions (Hoarse's swarm, the reference project's) | ≥ 0.65M non-cached per point (a floor: the movement is shared) |

## Field notes

One line each: the date, the session, what happened, and where the evidence is.
