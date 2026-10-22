# Profile: repo

**Dated:** 2026-10-22. **Picked when:** the repository itself is about to be opened to people outside the
project (made public, or shared with invitees): someone will find it, read the README and try to use it.

The auditor is a stranger who has just found this repository, and checks everything below from the blind copy.
Rank each finding: **blocks** (a stranger cannot get to a first success, or something private is exposed),
**should fix** (a stranger gets there, but stumbles or is misled), **nice** (polish).

## The core checks (every profile)

1. **Fresh install works.** Follow the README's install steps exactly as written, in a scratch place, and reach
   the first success it promises. Every step that needed a guess, a missing tool or an unstated account is a
   finding. In read-only mode, read the steps and flag the ones that would need a guess.
2. **Readable to a newcomer.** A reader who is not a programmer can follow the README and the first guide. List
   every word used before it is explained, every step that assumes the reader already knows, and every "simply"
   or "just" that hides a hard step.
3. **Nothing private leaks.** Personal names that should not be there, home paths (`/Users/…`, `/home/…`), host
   names, internal IP addresses, keys or tokens, links to private repositories, chat quotes, internal process
   notes. Run the project's own leak check where it has one, and look anyway.
4. **Claims match reality.** Counts (skills, features, tests), version numbers, links, badges and promises in the
   README match what the copy actually holds. A dead link is a finding.

## Repo checks

5. **Licence.** A LICENSE file exists and the README names it. Any third-party code in the copy keeps its licence
   header, and a NOTICE credits it where its licence asks.
6. **Where to start.** The README's first screen says what this is, who it is for and the one command or step to
   try. A stranger never has to read internal docs to begin.
7. **How to get help or give back.** An issues link or contact, and what kind of feedback is wanted.
8. **No dead ends.** Every file the README points at exists in the copy, and nothing points at a file only the
   private side has.
