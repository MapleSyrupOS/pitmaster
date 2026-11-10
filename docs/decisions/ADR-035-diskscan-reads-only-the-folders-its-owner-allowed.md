---
status: accepted
status-note: — ratified by the owner 2026-11-09
ratified-by: the owner
ratified-on: "2026-11-09"
owner: the owner
kind: process
built: not started
proof: "queued: a diskscan allow-list release in pitmaster-shed, then the diskcheck skill pinned to it"
supersedes: nothing
amends: ADR-034 §Decision rules 1 to 4
---
# ADR-035 — diskscan reads only the folders its owner allowed, and reports the rest as one unread total

This is the published version of this decision. Some internal details have been left out.

## Decision

Amends ADR-034 §Decision, rules 1 to 4: the scope stops being "this root, minus these exclusions" and becomes a list
of folders the user allowed. Nothing else is read, whatever starts the scan.

1. **An allow list.** A scope line `allow <path> [depth N]` names a folder the scan may read, and sizes are reported
   N levels below it (default 1). Nothing outside an allow line is read. `exclude` still carves a folder out of an
   allowed one. The access lines become `allow`, `exclude`, `limit` and `ledger`; `approve` and the refusal of a
   changed scope work as before.
2. **Setup offers help choosing, in plain words, and starts with nothing allowed.** The first time someone sets it
   up, the skill (and `init`) offers to list the names of the folders in their home folder, names only, the way the
   file browser shows them, with no sizes and nothing inside read, or lets them type the folders themselves. Every
   folder starts unticked; the scope has no allow line until they pick one.
3. **Space outside the allow list is one total.** The scan reports the disk's used space less what it measured, as
   "outside what you allowed", and never breaks it down. With `--alert-growth SIZE` that total raises an
   `ALERT unread` line when it grows by SIZE or more, and the report says to choose a folder to allow if they want to
   know where.
4. **The consent guard, inside allowed folders.** The first scan after an approval records the folders the system
   refused. Later scans under the same approval leave those folders unread, as if excluded, and raise an
   `ALERT access` line naming them, until the user approves again. A scan never reads more than the first approved
   scan did, whether a scheduler or a person starts it, and whatever the system would allow.
5. **Growth compares like with like.** Each scan records in the ledger the folders it did not read, refused or
   excluded. A folder whose unread set changed since the earlier scan is listed as not compared instead of showing
   growth; a scan from before this change, which recorded nothing, is not compared.
6. **Scopes with `root` lines are refused.** The release that carries this refuses a scope that still has a `root`
   line, and says how to rewrite it as allow lines; the user approves the rewritten scope.
7. **`plan` says where the boundary is:** the allow list, not the system's permissions.

## Context

Drivers:
- Consent to what is read, given by name before anything is read
- A boundary that does not change with who or what starts the scan
- A new hog outside the chosen folders still gets noticed

## Alternatives

### An allow list, with the rest as one unread total (chosen: nothing is read that the user did not pick, and growth outside still shows)
- Good: the scope names exactly what is read; a scheduler or Full Disk Access cannot widen it.
- Good: the unread total catches a growing folder nobody allowed, without reading it.
- Bad: the total is rough: it also holds system files, snapshots and other accounts' files, so it says "something
  grew", not what.
- Bad: setup asks more of the person; the plain-words offer is there to carry that.

### Keep the root and exclusions; exclude every protected folder by default and add the consent guard
- Good: no change to the scope format; v0.6.0 scopes keep working.
- Bad: anything nobody listed is still read; the protected places differ by system version and by app, so the default
  list is always behind.

### An allow list with no unread total
- Good: the quietest report.
- Bad: a hog outside the list goes unnoticed, the case diskcheck exists for. Offered; the user chose the total.

### Setup reads nothing at all; the person types every folder
- Good: the strictest start.
- Bad: people would need to know their own folder names. Kept as the offer's second choice, not the default.

### Old `root` scopes keep working, flagged in every report
- Good: no one's scan stops on upgrade.
- Bad: a whole-home scan carries on that nobody chose again. Offered; the user chose refusal.

## Consequences

- Easier: the user can read the scope and know every folder the tool may open, and a scheduled scan reads only what
  the user picked folder by folder.
- Harder: a first setup takes a few choices, and someone who wants everything must allow the folders one by one.
- Commits the project to: a shed release (v0.7.0, since `root` scopes are refused) with self-test cases for the allow
  list, the unread total, the guard and like-with-like growth, each shown red under `--break`; the skill's setup
  steps rewritten, held back from release until it pins that version; ADR-034's public copy re-drafted with
  this one.

Steps, each with its test:
1. `allow` lines parsed, `root` refused with the rewrite advice: a self-test case that a folder beside an allowed one
   is never listed (`--break allow` reads it).
2. The unread total and `ALERT unread`: a case with a fake disk usage.
3. The guard: a folder refused in the first approved scan and readable in the next is not read, and `ALERT access`
   names it (`--break guard`).
4. Like-with-like growth: a folder whose unread set changed shows as not compared (`--break access`).
5. `init` lists names only when asked, writes no allow line, and `plan` states the boundary.

## Asks left open

1. The scope line's name: `allow`? (ADR-034 used `root`.)
2. The wording of the setup offer. Drafted: "To help you choose, I can list the names of the folders in your home
   folder: just their names, the way your file browser shows them. No sizes, and nothing inside them is read. Or you
   can type the folders you want checked yourself."

## History

- 2026-11-09: proposed.
- 2026-11-09: ratified by the owner.
