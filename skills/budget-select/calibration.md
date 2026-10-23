# budget-select calibration log

One row per session that dispatched workers, written by its lead before the handoff. K is finished workers'
tokens per point; `budget-select` refits it from these rows. Readings are the meter's weekly percentage, with the
time and time zone.

## Meters

One line per meter: its name, its reset (day and time), its unit if not the default, and who recorded it.

| meter | reset | unit | recorded |
|---|---|---|---|
| (example) Tuesday meter | Tuesday 14:00 UTC | 1 % of the weekly limit | first lead on it, date |

## Use-it (the 48-hour plan, once per day per meter)

(meter): none yet.

## Rows

| date | session | meter | lead (model, effort) | share | start → end | worker tokens (by tier) | line fired | overrun | overlap | K (tokens/point) |
|---|---|---|---|---|---|---|---|---|---|---|

## Field notes

One line each: the date, the session, what happened, and where the evidence is.
