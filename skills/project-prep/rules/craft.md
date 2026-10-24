# craft — Engineering craft

Off at setup. For code, build or hardware projects; some rules suit only compiled or hardware work.

- At the start of every session, prove the build on disk matches HEAD.
- Make tests read one structured line, not prose.
- When only comments change, check the built files are byte-identical.
- Turn a future danger into a build error wherever you can.
- Land a new feature switched off behind a flag, tested, until the owner approves how it looks.
- Name milestones as numbered rungs; reach each in the emulator before real hardware.
- Take hardware values and protocol rules from the datasheet or spec section, never from memory.
