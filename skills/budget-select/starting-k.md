# The starting K, and where it came from

budget-select needs K, the finished workers' tokens per point of the weekly limit, before a project has measured its
own. It ships with **0.79M tokens per point** and a **ledger ratio of 1.5**. This note says where both came from,
so you can judge how far to trust them.

## Where they were measured

One owner's large project, run by many lead sessions with workers between 2026-10-13 and 2026-11-03, on Claude plans
with weekly limits. Each lead wrote a calibration row when it handed off: its start and end meter readings, and its
finished workers' tokens by model and effort.

- **K 0.79M.** The one night when the meter's movement could be set against everything that moved it: three leads in
  a row, about 24.4M finished worker tokens plus about 1.3M of the leads' own context, over 32 points of the weekly
  meter. Later rows on single leads gave 0.66M to 1.0M; none could be fitted alone, since other sessions shared
  the meter.
- **Ratio 1.5.** A week with five leads in parallel: their ledgers, at K 0.79M, added up to about 44 points while
  the meter moved 71. The leads' own re-reads, the owner's chats and the other sessions on the plan are not in a
  ledger, so the meter runs about 1.5 to 1.6 times ahead of it.
- **The mix.** Workers were mostly mid-tier at high or xhigh effort and large-tier at high or xhigh, with a little
  small-tier work. Leads were large-tier at high or xhigh, and ran up to about 500k of context each.

## What the same records showed about stop lines

- The lead's context, not its share, was the line that fired in most rows: a lead filled its context at about 7 to
  12 ledger points. A bigger share needs relay leads planned from the start.
- A share written as a meter percentage ("stop at 78 %") charged one lead for every other session's spend. When
  other sessions share the meter, the ledger is the share line and the meter is only the backstop.

## Why it is only a start

K moves with the plan (a point is a share of that plan's limit), the model mix and the effort, and caching. Your own
fit replaces it: take readings as you go (`spend-ledger.py reading`), then run `spend-ledger.py calibrate`. After
three pairs it trusts, use your own K with a ratio of 1 (the fit counts every session's tokens, so it already covers
what a ledger leaves out), and say so in each Budget block.
