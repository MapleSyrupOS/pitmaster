---
name: tastetest
metadata:
  family: check
description: Audit whether something is ready for the public, the way an end user would meet it. A blind auditor (one that knows nothing about the project) gets only what an outsider would see, tries it, and hands back a READY or NOT READY verdict with findings ranked blocks / should fix / nice. Profiles cover a repository going public and an app going to the App Store, whose dated checklist is compared with Apple's live guidelines each run. "tastetest readonly" only reads. Use when the user types "tastetest" or "tastetestreally" (which also fixes the findings and re-audits until READY), or asks "is this ready to go public?", "public readiness audit", "is it App Store ready?" or "audit this before launch". A code review, a security review, "is it done?" or a leak check on its own does not load this skill.
---

# tastetest: a blind readiness check before anything goes public

Decided by pitmaster ADR-016.
"tastetestreally": ADR-023.

Sibling of `tier-select` (step 4), `talk-through` (step 9), `neighbourhood` (step 1; not built yet) and `setfree` (which
offers this audit on release day, before anything goes out; not shipped yet). Built by a
Skill bbq; each rule names the question (Q-number) that set it, in a record kept in pitmaster's private repository.

**The smallest use:** type `tastetest`. Steps 1 and 3 are only for bigger audits.

## Config

Edit these lines here, or put the same lines in a `pitmaster.md` at your project root, which wins. Every line is
optional.

```
name: the user              # who gets the report. "name: Alex" makes this skill say "Alex".
report_dir: docs/audits     # where reports go (step 8); a project with reports/ may use that
publish_list: none          # what the public sees (pitmaster's is publish.txt); none = every tracked file
profiles: profiles          # the folder of profiles beside this file
project_profiles: none      # the project's own profiles, read beside the shipped ones
```

## Steps

1. **Read the opener.** After `tastetest`, the word `readonly` keeps the auditor to reading (step 7; Q8, Q21).
   The word `neighbourhood` (or `neighborhood`) asks that skill for auditors from other model families; while it
   is not installed, say so in one line and go on with one auditor (Q7, Q22). `tastetestreally`, one word, goes
   all the way through (§tastetestreally below).
2. **Pick the profile by reading the project** (Q5): `repo` when the repository itself is going out, `app-store`
   when it builds an App Store app. Both can apply, and so can a profile in `project_profiles` (A2). Say which in
   one line ("Profile: app-store, from app/Example.xcodeproj"). If none fits, ask. Each profile is a dated
   file in `profiles/`; the core checks in `repo.md` apply to all (Q3).
3. **Check the checklist against its source** (`app-store` only; Q6). Read Apple's current App Review Guidelines
   and note each rule new, changed or gone since the profile's date; these open the report as *checklist drift*.
   Without web access, say the live check was skipped.
4. **Pick the auditor's model and effort** with `tier-select` (Q13). The profile and the project's size set the
   tier.
5. **Make the blind copy** (Q2): `scripts/blind-copy.py <project> <scratch>/tastetest-<date>`, adding `--list
   <publish_list>` when the project has one. The copy holds only tracked files, never the history. App Store copy
   and screenshots come along if the repository keeps them.
6. **Route the audit** (Q2, Q14). Where the platform has subagents, a fresh subagent is the auditor. Its prompt
   is sealed: the copy, the profile files and the mode, and nothing an outsider could not see (never this
   session's suspicions or the project's private notes). With no subagents, always offer both routes; the context
   used changes only which is recommended:
   - under 33 %: **run it here in chat** (recommended), or write a prompt for a fresh session;
   - 33 % or more: **write a prompt for a fresh session** (recommended), or run it here;
   - 80 % or more: first say the context is very high, then offer the same two, the prompt recommended.

   Where context cannot be measured, ask which. An audit here is not blind, and the report says so (Q24).
7. **The auditor looks and tries** (Q8). It installs, builds and runs the tests and simulator, all inside the
   copy. In `readonly` mode, or with no shell, it only reads files, with no install or build.
8. **Write the report** (Q4, Q11, Q12) to `<report_dir>/<date>-<profile>.md`, on a branch, never on the main
   branch:
   - first line: **READY** or **NOT READY**. Any *blocks* finding means NOT READY. If the auditor knew the
     project, the next line says "Not a blind audit: the auditor knew the project."
   - the profile, its date and the checklist drift;
   - the findings, ranked **blocks**, **should fix**, **nice**, each cited to a file and line (or a screen), with
     what a stranger would hit and the smallest fix;
   - what was not checked, and why (read-only, no shell, no simulator, no web).
9. **Send the report to the user as a file**, then offer `talk-through` once, for an informal chat about next
   steps (Q13).

**Shown to work by** `scripts/seeded-fixture.py` (ADR-016, A3): `--make <dir>` builds a small project with four
planted flaws, tastetest audits it, and `--score <report>` lists the flaws the report missed. Run it after any
change to this skill.

## tastetestreally: fix, then audit again

"-really" means all the way through (ADR-023 rule 11). Never past a safety stop: ratify, taste, public acts, pushing to main, deleting work.

1. After the report (step 9), fix each finding that is not taste on a branch, never the main branch, and run the
   project's checks. Park each taste finding (a name, a look, a direction) as a question.
2. Audit again with a **fresh** blind copy and a fresh auditor, which never sees the earlier report.
3. Repeat until READY, at most three rounds. Still NOT READY after three: stop and report what is left.
4. Open the PR and merge it once the checks are green. The verdict still never decides that anything goes public.

**Never:** decide that something goes public (the verdict informs the user's word to go live; it never replaces
it); submit to App Store Connect, upload, publish or push; edit the project, except `tastetestreally`'s fixes on a branch.

## Platform notes

- **Claude Code:** the auditor is a subagent (the Agent tool); tier-select's roster pins its model. `/context`
  gives step 6's context used. The simulator steps use Xcode's command-line tools or the iOS Simulator tool where
  the session has one. Send the report with the file-sending tool. Step 6's question goes through
  `AskUserQuestion`, with everything needed to answer written into the question itself.
- **Cowork / claude.ai:** no subagents and no `/context`, so step 6 asks which route. With no shell, the user
  uploads the public files to make the blind copy by hand.
- **Codex:** use a subagent as the auditor where yours can start one; otherwise step 6 asks. Skills live in
  `.agents/skills/` in a project or `~/.codex/skills/` for the user.
- **Other tools:** step 6 asks which route, as a numbered list in one message.
