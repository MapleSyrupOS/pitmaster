---
name: budget-select
metadata:
  family: usage
description: Choose the usage budget for a session that will run workers or a long job (a voyage, also called a runlap), in points of the plan's usage limit (by default 1 % of the weekly limit), set its stop lines, and write the Budget block its prompt carries. Use at the start of a session that will dispatch workers, before writing an overnight prompt, swarm kickoff or handoff, and when the user asks "how much budget", "what share should this get", "split the week between these", "which account", or "what should we spend the rest of the week on". Works with any platform's usage meter; where none can be read, it asks the user for the reading.
---

# budget-select: a share, its stop lines, and a measurement afterwards

Sibling of `tier-select` (model and effort for the lead and each worker), `bbq` (loads this skill first when a voyage
spends points) and `spend-ledger` (measures afterwards). This skill decides how much of the plan's limit a session
may spend.

**A usage meter is shared.** Every lead, every worker and the user's own chats on the same plan move the same
meter, so a lead cannot read its own spend off it while another lead runs beside it.

A session that will not dispatch workers or run long does only step 0; step 4 and the last two sections are for
bigger voyages.

## Config

Edit these lines here, or put the same lines in a `pitmaster.md` at your project root, which wins. Every line is
optional.

```
name: the user                 # whose plan it is. "name: Alex" makes this skill say "Alex".
point: 1% of the weekly limit  # the unit; any fixed share of any metered limit works
hard_stop: 75 / 80 / 85 / 93   # stop starting work at: >48 h to reset / 24-48 h / 12-24 h / <12 h
handoff_context: 500k          # hand off at about this much of the lead's own context
calibration: docs/budget-calibration.md   # the project's own log, one row per session; made from calibration.md
                                           # beside this file on first use, so an update never overwrites it
```

## Meters

A **meter** is one usage limit you can spend against: a plan's weekly limit, a separate model pool's limit, a
second account. **One budget per meter**, named by something the session can see, such as its reset day ("the
Tuesday meter"). A session finds its meter from the reading, its prompt, or by asking the user. With more than one
meter for the same work, one that resets later may spend more of its room early, since the other refreshes first
and covers the tail (the *Cover* line, step 3).

## Steps

0. **Will this session dispatch workers or run long?** Either way, take the reading (step 1's last bullet). If
   not, check the hard stop (step 3), warn the user in one line only if the meter is within 5 points of it, and
   stop: no questions, no Budget block, no calibration row.
1. **For a session that dispatches workers, settle four things every time.** Never default them, except as the
   first bullet says.
   - **An absolute allocation** ("you get 15 points") is the share: skip the ceiling, split and reserve, take the
     reading as usual, and cap the share at the hard stop minus the reading.
   - **The ceiling** for this session, or this set of sessions, in points.
   - **Leads in parallel on this meter** until its reset, and **the split ratio**, which the user names; never
     infer one from priority or model mix. A lead on another meter is not in the split.
   - **The reserve** the user keeps for their own use before the reset.
   - **The reading:** the meter's weekly percentage and reset time, and any short window's percentage and reset,
     from the platform's usage tool. **With none, ask the user** (their plan's usage page shows it) and say the
     reading was given, not measured.
2. **Work out the shares.** `room = min(ceiling, hard stop − reading) − reserve`, all on this meter. Split it by
   the ratio and round down to whole points. Example: a 35-point ceiling, no reserve, a hard stop more than 35
   points away and a 3:2 split give 21 and 14.
3. **Set the stop lines.** Each lead stops **starting** new work at the first of these. Work in flight finishes,
   with no cap on the overrun; the overrun goes in the calibration row.
   - **Its share:** the finished workers' tokens divided by K (worker tokens per point; see Calibration) reach the
     share. Alone on the meter, or with no K yet, use the reading minus the start reading.
   - **The combined backstop:** the meter reaches `start + the total of all shares on this meter`. It catches a
     wrong K.
   - **The hard stop**, by the time left to this meter's reset (the config's `hard_stop`):

     | time to reset | more than 48 h | 24–48 h | 12–24 h | under 12 h |
     |---|---|---|---|---|
     | hard stop | 75 % | 80 % | 85 % | 93 % |

     **Cover:** while another usable meter resets before this one,
     this meter's hard stop may rise to 90 %, if the user agrees once. The covered stretch ends more than 48 h
     before this meter's own reset, so the two rules never overlap.
   - **Context:** hand off at `handoff_context` of the lead's own context.

   A short rate window does not hold dispatches while the weekly share has room; if it fills, wait for its reset,
   note the wait, and go on. **No pacing:** spend as fast as the work allows, and let the lines govern.
4. **If the share is under 10 points, advise on tiers** in one line naming what a cheaper mix buys ("moving the
   reviewers down one tier buys about N more workers"); with no calibration rows yet, say N is unmeasured. Advise
   only: `tier-select` decides, and the user rules the lead.
5. **Write the Budget block** into the prompt, in this shape and no longer. It is portable: the meter, the start
   reading and the hard stop are read again on pickup, never carried over.

   ```
   ## Budget
   Share: NN points (1 point = <unit>) of a CC-point ceiling split R:R with <other lead>; reserve VV kept for the user.
   Room: HH points (the lower of the ceiling and the hard stop less the reading, less the reserve); split R:R gives NN and MM.
   Written when the <meter> meter read WW % (date, time); that reading is not yours. On pickup: take the reading
   (or ask the user for it), name your meter, note your start reading in the voyage's ledger, and cap the share at
   your hard stop minus your reading. Read the meter before each batch of dispatches; note a reading only at batch
   ends and when a stop line is within 5 points. Stop starting new work at the first of: your ledger's spend
   reaching NN points (K = <tokens>/point, or the meter alone if no K yet); the meter reaching your start + the
   shares on your meter; the hard stop (75 % beyond 48 h, 80 % at 24–48 h, 85 % at 12–24 h, 93 % under 12 h;
   90 % while another usable meter resets first, if agreed). In-flight work finishes. Hand off at ~<context> of
   your context. Before handoff, write your row in the calibration log.
   ```
6. **Close: before its handoff the lead writes one row in the calibration log**: the date, session, meter, lead's
   model and effort, share, start and end readings, finished workers' tokens by tier (`spend-ledger` measures
   them, and its row goes in the spend ledger too), which line fired and when, the overrun, and the sessions that
   overlapped. When work remains, the handoff ends with one factual line: the points left on this meter before its
   hard stop, and when the other meters reset.

## Calibration

K is the finished workers' tokens per point, fitted from the calibration log's rows, which come from real voyages.
**Until there are some, there is no K: every point estimate says it is unmeasured**, and the stop lines use the
meter alone. A lead's own context and the user's chats move the meter too, so a fitted K **overstates** a lead's
spend, the safe direction. A mix heavier in large models costs more per token; refit as rows come.

## No meter: a lead that cannot read the usage meter (bigger voyages)

A lead in a cloud container usually cannot read the meter or list the account's other sessions (see bbq's Cloud
type). Its prompt then carries:

- **An absolute share** in points (step 1's first bullet), and **the account** it is spent on, since the lead
  cannot work it out.
- **"You are not alone."** Other leads and the user's chats move the same meter.
- **The ledger as the only spend line** (step 3's share line). With no K yet, plan from the share and stop at the
  first of the prompt's hard stop or the context line.
- **Context as a stop line.** The lead's own context fills first on a large share (one large voyage saw
  about 10 of 35 points). At `handoff_context`: wait for in-flight workers, write the calibration row and hand off
  to a successor (bbq's Cloud type says how).

## 48 hours before a meter's reset: the use-it plan (bigger voyages)

From 48 hours before a meter's reset, **once per day per meter, whatever the headroom**, read it and work out the
points the hard stop leaves that the plans in hand will not use, and **propose** two or three ways to spend them,
each sized in points with its tier, for the user to pick, such as the oldest small debt items, reviews owed, re-runs
of checks that failed on a known flake, or the next step on a board's critical path. Record the
proposal on the calibration log's *Use-it* line for that meter; a session that finds today's date there proposes
nothing. Unspent share stays unspent: no lead takes another's leftover. Nothing starts without the user's word.

## Platform notes

- **Claude Code:** the desktop app's usage tool (where offered) gives the weekly and five-hour readings and reset
  times; `/context` gives the lead's context.
- **Cowork / claude.ai:** no usage tool. Ask for the weekly percentage and reset from Settings → Usage, and write
  the Budget block anyway.
- **Codex:** the reading is on the plan's usage page, or Codex's status view where it shows one. A ChatGPT plan's
  limit is its own meter.
- **Other tools:** a tool that meters model pools separately has one meter per pool.
