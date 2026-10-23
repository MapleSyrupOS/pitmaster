---
name: talk-through
metadata:
  family: plan
description: Talk a subject through as an open conversation, in voice or text, while quietly tracking decisions, open questions, action items and corrections; then, on the user's word, write it all up as one record with each decision marked agreed, proposed or open and cited to where it came up. Use when the user types "talk-through", "talkitout", "talkitthrough", "chatabout", "chitchat" or "talk-it-through", or says "let's talk it through" or "let's just talk it through". Also offer it once when several decisions have piled up in a conversation that did not start with it.
---

# talk-through: talk a subject through, then write it up as one record

Decided by pitmaster ADR-014.

Sibling of `makeadr` (an agreed decision big enough for an ADR), `bbq` (a plan whose questions need settling
before work starts) and `project-prep` (named only when the talk was about starting a project). `tastetest` offers
a talk over a finished readiness report, and `goforit` typed after a talk carries its plan on into the work.

The smallest run: say "talk-through", talk, then say "let's wrap it up", and you get one record file (with
`land: file`, nothing else: no branch, no pull request).

## Config

Edit these lines here, or put the same lines in a `pitmaster.md` at your project root, which wins. Every line is
optional.

```
name: the user                    # who is talking; "name: Alex" makes this skill say "Alex"
record_dir: docs/proposals        # where the talk's one record goes: <record_dir>/talk-<date>-<topic>.md
index: docs/proposals/INDEX.md    # the list the wrap adds a row to; "none" to skip
mode: auto                        # auto | voice | text (see step 1)
land: pr                          # pr (branch + PR) | commit (branch only) | file (just the file) (step 6)
```

## Steps

1. **Start.** Say in one line that you are listening and that "let's wrap it up" writes it up. Pick the mode:
   a word after the opener sets it ("talkitout voice", "talk-through text"); otherwise the config's `mode`;
   on `auto`, voice when the app says the input is spoken, text otherwise.
2. **Talk.** The back-and-forth is the point. Do not steer toward a document.
   - Let it wander and follow the user's curiosity. Be a real partner: react, ask one follow-up at a time, give
     honest opinions and recommendations, and push back when something is wrong.
   - When a fact matters, check it in the project's files instead of guessing. Say when something is unverified.
   - **Voice:** short turns, about two sentences. No lists, tables or headings until the wrap.
   - **Text:** the same, though a one-paragraph running summary is fine if the talk runs long.
3. **Track, quietly.** Keep a running list, neither shown nor written down until a checkpoint or the wrap:
   - **Decisions**, each with a status: **agreed** (the user said yes), **proposed** (suggested, not ruled) or
     **open** (unresolved), and where it came up (the user's words, or the point in the talk). Never decide for
     the user: only the user moves an item to agreed, and if unsure, mark it open. Agreed in talk is not
     ratified; rulings happen the project's normal way.
   - **Key points**, **open questions**, **action items** (each small enough to hand over, with what done looks
     like) and **corrections** (facts that changed during the talk).
   - Keep the user's own words for names and ideas they coined.
4. **Checkpoint.** When the user asks ("save what we have"), or when the talk turns to something unrelated,
   write what is tracked so far into the talk's record (step 5's shape, marked *checkpoint*), say so in one line
   ("Checkpointed: 3 decisions, 2 open"), and go on talking. A checkpoint writes the file only; it commits nothing.
   The wrap completes the same record.
5. **Wrap, only on the user's word** ("let's wrap it up", "write that up"). Write one record,
   `<record_dir>/talk-<date>-<topic>.md`, status **open**:
   1. **Header:** the status line ("open: nothing here is ruled unless marked agreed"), the date, voice or text,
      who took part, and "Produced by talk-through".
   2. **Context:** what prompted the talk.
   3. **Key points,** in plain words.
   4. **Decisions:** a table of decision, status, and where it came up.
   5. **Open questions** for the user, numbered, each with a recommendation.
   6. **Action items,** each with what done looks like.
   7. **Corrections,** if any facts changed.
   8. **Possible next steps:** which sibling could pick each item up. Suggest; do not run them.

   Then add a row to the `index` list. If `record_dir` does not exist, offer two choices: create just that folder
   and its index, or run `project-prep`.
6. **Land it** by the config's `land` (default `pr`), never on the main branch:
   - **`pr`**: on a branch, commit the record and the index row, open a docs PR, and give the link. Merging stays
     the user's.
   - **`commit`**: the same commit on a branch, with no PR.
   - **`file`**: leave the record and the index row as files. Commit nothing.
7. **Later.** A follow-up to the same talk appends a dated *Amendment* section to its record. One record per talk;
   never rewrite it.

**If it was not started.** When decisions are piling up in a conversation that did not start with this skill,
offer once: "Want me to talk this through and write it up?" If the user declines, do not ask again in that
conversation.

**Never** edit an ADR or charter.

## Platform notes

- **Claude Code:** text unless "voice" follows the opener. `gh` opens step 6's PR when it is signed in;
  otherwise the wrap ends with the committed branch and says so.
- **Cowork / claude.ai:** voice mode in the Claude apps counts as voice. With no git or `gh`, the wrap gives the
  record as a file to save and skips step 6; a checkpoint shows the record so far in the chat.
- **Codex:** text. `gh` opens step 6's PR where it is signed in.
- **Other tools:** text. Write the record where the tool can write files; without `gh`, the record file is the
  result.
