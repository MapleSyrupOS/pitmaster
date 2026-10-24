---
name: swarm-bottleneck
metadata:
  family: usage
description: Name the one constraint that is limiting a multi-agent voyage, also called a runlap (a swarm, an overnight queue, a lead with workers), right now, with the evidence and one to three moves that relieve it. Use when the user or a lead session asks "what's the bottleneck", "where are we stuck", "how's the swarm doing", "what are we waiting on", or when deciding what to start next while several jobs share the same limits, reviewers or machines. "Why is this slow" loads it only in a multi-agent voyage; one slow command, script, query or web page is an ordinary speed question. Read-only; it measures and reports, and starts nothing.
---

# swarm-bottleneck: measure, then name one constraint

You measure, the voyage's board says what matters, and you judge. The answer is **one binding constraint** (the one
thing holding the voyage back most), the evidence for it, and one to three moves that relieve it; never a tour of
everything that is slow.

The smallest use is steps 1 to 4 on the work in flight, the open pull requests and the last few CI runs;
hosts are only for voyages that use machines of their own.

## Config

Edit these lines here, or put the same lines in a `pitmaster.md` at your project root, which wins. Every line is
optional.

```
name: the user        # who owns the voyage's decisions. "name: Alex" makes this skill say "Alex".
board: auto           # the voyage's board: auto finds the newest voyage record or README with a streams table
hosts: none           # "none", or a file describing your machines (see "Your hosts")
```

## Steps

1. **Measure** each reading the platform allows:
   - **The work in flight:** the workers or jobs running now, how long each has run, when each last wrote
     anything, and any that stopped with an error.
   - **The review and merge queue:** open pull requests with their check state and age
     (`gh pr list --json number,title,mergeable,statusCheckRollup,createdAt` where `gh` is present).
   - **CI and tests:** runs queued and running, and how long the last few took (`gh run list --limit 20`).
   - **Usage:** the plan's usage meter and any rate-limit window, from the platform or the user (`budget-select`
     explains the reading).
   - **The lead's own context**, where the platform can say.
   - **Tool and connector health:** calls that failed or timed out in the last hour, and servers that are down.
   - **Your hosts**, if the config names a hosts file.

   Take a failed reading again once before believing the thing is down; a machine in the hosts file that does not
   answer counts as a failed reading.
2. **Read the critical path:** the chain of work that ends in the next landing, from the voyage's board (its record
   or README: the streams table, what has landed and what waits on what) and the newest handoff's order of work.
   A delay off it costs nothing.
3. **Name the constraint:** the one that, relieved, brings the next landing forward the most. If two would do so
   equally, the one that clears first is the constraint; name the other as next. If the readings do not decide
   it, say which reading would, and take it. The menu, and what points at each:

   | constraint | what points at it |
   |---|---|
   | **usage and rate limits** | the weekly meter near a stop line, a rate-limit window full, workers waiting on refusals while the work is ready |
   | **context** | the lead's own context near its handoff line, or workers ending early on context, while the work is ready |
   | **CI and test time** | runs queued behind each other, a suite slower than the work it checks, one slow job every change waits on |
   | **the review and merge queue** | pull requests green and mergeable but not merged (with their age), or reviews requested and not given |
   | **the human's attention** | questions waiting on the user, rulings asked for and not given, a merge only they may make |
   | **tool and connector failures** | the same call failing again and again, a connector signed out, a server down, a sandbox refusing a command |
   | **a builder on the critical path** | the next landing waits on one stream with no worker running and nothing pushed |
   | **a red to triage** | a failing test or check nobody has reproduced: nothing lands until it is understood |
   | **your hosts** (optional) | every slot full on every machine that can run the job while jobs pile up, or one long job holding a machine others need |

4. **Report** in this shape, no longer:
   - **Constraint:** one line.
   - **Evidence:** the readings' own lines (run ids, minutes, PR numbers, percentages), quoted.
   - **Moves:** one to three, each something the lead or the user can do now, with what it should change in the
     next reading (for example "merge #42 and #43: both green for six hours; the next landing waits on them").

## Rules

- **Measure, never guess.** Every claim cites a reading or a file you read; a count in prose is a guess.
- **A red that looks like the environment is re-run before it is believed.** A timing-sensitive test that failed
  while the machine was busy is re-run alone first.
- **Read-only.** This skill starts, stops and merges nothing and takes no lock; a moved job, a cancelled run or a
  merge is the lead's or the user's to order.
- **Say what was not measured**: readings that failed or that the platform could not take, machines the hosts
  file does not cover, and anything you had to ask for.

## Your hosts (optional)

If the voyage uses machines of its own (build servers, test boxes, a GPU machine), name a hosts file in the config,
with one block per machine: its name, how to reach it, how many jobs it runs at once, and the command that lists
what it is running. Step 1 then reads each machine's load and free slots, and the menu's *your hosts* row applies.

## Platform notes

- **Claude Code:** the session's task list and subagent results show the work in flight; `/context` gives the
  lead's context; a usage tool, where the app offers one, gives the meter.
- **Cowork / claude.ai:** there is usually no `gh` or shell: ask the user for the PR and CI state and the usage
  reading (Settings → Usage).
- **Codex:** `gh` and a shell are usually there, so PR, CI and host readings work. Codex shows the skill no
  context percentage or usage meter: ask the user for the usage reading.
- **Other tools:** take what the shell allows and ask the user for the rest.
