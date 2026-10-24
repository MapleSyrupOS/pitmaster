# The Cloud type, and Away

A Cloud bbq hones the prompt for a lead that runs in a cloud container (ADR-006). **Away** (the user unreachable
or on a poor link) is a mode any type can carry, not a type. When step 1's "Will the user be reachable?" gets "no"
or "spotty", settle how asks travel (below).

## What a cloud lead is missing

The bbq asks for each of these and writes the answer into the record:

- **The share.** The lead cannot read the usage meter, so the prompt gives a fixed number of points and names the
  account. `budget-select`'s *No meter* section writes the Budget block.
- **The relay.** If the share is more than one lead's context can spend, lead 1 starts lead 2 with the platform's
  session tool (SKILL.md's *Platform notes*) once its in-flight workers finish, since they end with its container.
  `budget-select` owns the context stop line that triggers it. The chain has no cap of its own: it ends when the
  ledger reaches the share, and each hand-off is logged so the chain's length shows.
- **How asks travel** when the user is away: an ask goes out as a notification and into the decisions queue, the
  stream that needs it parks while other work goes on, and an answer is applied whenever it arrives. An ask still
  unanswered at hand-off (or at the comrun's end) takes its recommended option and goes into the hand-off's
  *Defaulted* list with a `veto:` line.
- **Capacity.** In place of measuring hosts, a *Capacity* section from the project's cloud rules: no `ssh`, no
  LAN, no local models. A machine the container cannot reach goes through CI: allowlisted jobs, one queue that
  only the lead feeds, and refs the cloud cannot delete, listed in the hand-off. If the project later has a
  host-selection skill, it takes this over.
- **The shared container.** Builders share its CPU and scratch space, so the prompt caps how many run at once
  (ask; 3 is the recommended answer), gives each its own worktree, and says to name scratch files uniquely.
- **Other repositories.** Every repository the comrun may touch, the access each needs, and what stays the user's
  (merges, tags, releases).

## The ending

Where the platform can start a cloud session, offer to launch the lead once the record has landed; the user clicks
it or pastes the kickoff. Never launch without the user's yes.
