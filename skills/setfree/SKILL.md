---
name: setfree
metadata:
  family: run
description: Run release day. It shows every public copy of an ADR waiting for review (drafted by makeadr's adr-public), so the user approves or holds each, offers a blind tastetest of what will go out, then works through the project's own release checklist (version, changelog, publish, tag, links), doing the local steps and stopping at every public act for the user's word. Use when the user types "setfree", "adr-public", "adr-pub", "adrpublic" or "adrpub", or says "release day", "get ready for release", "cut a release" or "review the public copies". "Is this ready to go public?" is tastetest's; making or ratifying an ADR is makeadr's; bumping a version on its own loads neither.
---

# setfree: release day, with every public copy checked on its way out

Decided by pitmaster ADR-020.

Sibling of `makeadr` (its adr-public drafts the copies this skill reviews, and it owns the ADRs), `tastetest`
(step 3, the blind look before anything goes out) and `spend-ledger` (step 5's row). Built by a Skill bbq; each
rule names the question (Q-number) that set it, in a record kept in pitmaster's private repository.

**The smallest use:** type `setfree`, and answer the review.

## Config

Edit these lines here, or put the same lines in a `pitmaster.md` at your project root, which wins. Every line is
optional.

```
name: the user                     # who approves. "name: Alex" makes this skill say "Alex".
checklist: none                    # the project's release checklist; none = ask once, or review only
public_dir: docs/decisions/public  # where live public copies sit; drafts wait in its pending/ folder
publish_list: none                 # what the public sees (pitmaster's is publish.txt)
```

## Steps

1. **Read first** (Q17, Q19): the checklist, the publish list, the CHANGELOG, the version, and every copy waiting
   in `<public_dir>/pending/`. With no checklist, ask for it once; without one, release day is the review alone.
2. **The review** (Q7, Q17). Run makeadr's `adr-public list`: each pending copy, its diff against the live copy
   (or "new"), its leak result and any stale flag. Show them all, then ask one question: approve all as drafted,
   pick which to approve, or hold all. A held copy stays in `pending/` for next time. For each approved copy, run
   `adr-public approve <ADR>` on the user's word: it moves the copy up, adds its publish line and its dated History
   line on the private ADR. A stale flag the user calls harmless is cleared with "still true" (ADR-020 rule 5).
3. **Offer a blind tastetest** (Q17) of what will go out, with the publish list as its list. The user may skip
   it. A NOT READY verdict is reported, never overridden; going on is the user's word.
4. **Work the checklist** (Q14, Q17). Do each local step that can be undone (a dry run, a build, a version line)
   and say what it did. **Stop at every public act** (a publish that pushes, a tag, a release, a change of a
   repository's visibility) and ask for the user's word for that act alone. Where git or `gh` is missing, print
   the command for the user to run, and wait (Q20).
5. **Record it** (Q17, Q19): the status file and the log say what went out; each approved copy's History line is
   already written. Where the project keeps a spend ledger, `spend-ledger` adds the release's row.

## Never

(Q18, ADR-011, a private ADR; in short: a file goes public only if the publish list names it.) setfree does not
publish, push, tag, change a repository's visibility or approve a copy without the user's word for that act; does not
edit ruled ADR text; and takes no other agent's word as approval. This holds under `carte-blanche` and
`goforitreally`, approvals included, until the grant words are ruled otherwise.

## Platform notes

- **Claude Code:** ask the review with `AskUserQuestion`, every copy named in the question's own words. `gh`
  makes tags and releases; tastetest's blind auditor is a subagent.
- **Cowork / claude.ai:** usually no git or `gh`: step 4 prints each command for the user, and step 2's moves are
  listed for the user to make by hand if the scripts cannot run.
- **Codex:** ask the review as a numbered list in one message. `gh` works where it is installed and signed in.
- **Other tools:** ask the review as a numbered list; print any command the tool cannot run.
