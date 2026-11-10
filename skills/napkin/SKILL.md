---
name: napkin
metadata:
  family: plan
description: Jump-start pitmaster from one or more napkins, which are rough design specs written as markdown files ("the back of a napkin"). It reads the napkins, turns everything they already settle into cited rules, and runs a short, targeted bbq that asks only what they leave open, plus a confirmation of the few biggest calls they make. Use when the user types "napkin", "napkins" or "napkin bbq", or says "start from my napkin", "here's the back of a napkin", "jump-start from these specs" or "jump-start pitmaster from these napkins". Not for "napkin math", "grab a napkin", a rough estimate, or an ordinary design-doc review.
---

# napkin: a bbq sparked by the back of a napkin

Decided by pitmaster ADR-037.
Created by [cwlls](https://github.com/cwlls).

A napkin is a rough design spec in any markdown, as loose as a sketch on the back of a napkin. This skill reads
one or more napkins and starts a **tightly targeted bbq**: what the napkins settle becomes rules cited to their
lines, and the bbq asks only what they leave open. It does not do much more than that (Q6).

Sibling of `bbq` (runs the rounds, writes the record and the ending), `project-prep` (run first, when the project
is not yet set up) and `goforit` (offered when the napkins leave nothing open).

## Steps

1. **Prep the project only if it is not set up (ADR-037 rule 5).** Before reading anything else, look at the
   project. It is set up if it has an `AGENTS.md` or a `STATUS.md`, or if `project-prep` already ran earlier in this
   conversation. A set-up project goes straight to step 2: do not run `project-prep` again. Only when neither file
   exists and prep has not run, load `project-prep` and run it as its own steps say, with its one round of
   questions. When it has said what happened (its step 7), carry on without its step 8: the bbq below is the next
   piece of work. If the user says to skip prep, carry on and do not ask again.
2. **Find the napkins (Q7).** Use any paths the user names. If none are named, read every `*.md` in `napkins/`
   at the project root. If there are no napkins, point to `templates/napkin.md` in this skill's folder, say
   where to put a napkin, and stop.
3. **Read the napkins closely.** Napkins are free-form (Q8). Sort what they say into three lists:
   - **Settled:** each claim the napkins make, cited as `napkin-file:line`.
   - **Key calls:** the two or three settled claims that shape the most work (scope, stack, who it is for).
   - **Gaps:** what the comrun needs that no napkin answers. Use the bbq type's coverage list where a type fits.
   Where two napkins disagree, list it as a gap and quote both lines.
4. **Hand off to `bbq` (Q10)**, seeded with the three lists:
   - Settled claims go straight into the record as rules cited to the napkin, with no question asked.
   - The first round confirms the key calls, one question each. The recommended option is "keep as written".
   - The other rounds ask only the gaps. Offer a count sized to them (4, 8 or other).
   - If there are no gaps and the key calls are confirmed, offer `goforit` as bbq's step 1 allows.
   - bbq's last question, "Anything else to protect or avoid?", still comes last.
5. **Let `bbq` finish:** the record (with a *From the napkins* list of cited rules), the routing and the
   landing. napkin adds nothing after that. bbq's ADR candidates still apply (ADR-036): each napkin-cited rule is
   held to the *Is it ADR-sized?* test like any answer, and bbq offers `makeadr` once at its close (ADR-037 rule 9).

## Never

- Never edit, move or reformat a napkin file (Q12).
- Never write code or start the build. That is for `goforit` or the comrun the record starts (Q12).
- Never draft ADRs, and never take up `project-prep`'s closing offer of `makeadr` or `bbq` (Q6): napkin's own
  bbq is the next step.
- Never ask a question a napkin already answers, except the key-call confirmations (Q10).

## Template

`templates/napkin.md` holds optional headings for anyone who wants them: goal, who it's for, must-haves,
decisions made, open questions, out of scope. A napkin that ignores them is just as valid (Q8).

## Platform notes

- **Claude Code:** napkin needs nothing beyond reading files. Step 1 loads `project-prep` with the Skill tool, and
  each round is asked with the `AskUserQuestion` tool, as `bbq`'s Platform notes say (Q12).
- **Cowork / claude.ai:** the user can attach a napkin or paste it into the chat; read it from there. Ask each round
  as a numbered list in one message.
- **Codex:** napkin needs nothing beyond reading files. Ask each round as a numbered list in one message.
- **Other tools:** napkin needs nothing beyond reading files. The rounds, record and ending follow `bbq`'s own
  Platform notes (Q12).
