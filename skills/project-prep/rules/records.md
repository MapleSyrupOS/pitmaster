# records — Records and repository

Off at setup. The second and fourth rules each keep a list in `docs/rules/`, which project-prep writes when the
group is switched on.

- After any copy, sync or upload, prove the content arrived (a checksum, or one changed line found at the destination).
- Leave each file in `docs/rules/hot-files.md` to its named writer: check that list before editing, and leave that writer a note of what should change instead.
- Never merge a generated file; regenerate it last.
- When a tool sets a trap, add it, with what to do instead, to `docs/rules/tool-traps.md`; read that list once each session before using the tools.
- Before a session ends, say in one line if it left work uncommitted or unpushed, or one of the user's questions unanswered.
