# The neighbours doc

Your neighbours are the models other than the one you are talking to that a skill may call: other model families,
local models, other accounts. "neighbourhood" on a skill, and every townhall, uses only the names written here: it
is an allow list (Q6, Q7). One doc serves every project, because neighbours belong to your machines and accounts,
not to one repository.

**Where:** `~/.pitmaster/neighbours.md` (Q24). A project's `pitmaster.md` may add one line, only to change that:

```
neighbours: qwen, codex           # narrow: only these names, in this project
neighbours: docs/neighbours.md    # point elsewhere: a list kept with the project
```

## The shape

```markdown
# Neighbours

| name | how to reach it | family | cost | streams | live |
|---|---|---|---|---|---|
| qwen | LM Studio on alpha (port 1234) | Qwen | free | yes | yes |
| codex | `codex exec` on this machine | OpenAI | plan | no | yes |
| gemma | Ollama on alpha (port 11434) | Gemma | free | yes | no |

Seats: qwen, codex          <!-- written by the first townhall; the default line-up after that (Q34) -->

## Live
delivery: hybrid           <!-- all at once | streamed | hybrid (Q40) -->
filibuster: 1 sentence     <!-- how long a speaker may finish after you cut in (Q35) -->
```

- **name:** what you call it in an opener or a `neighbours:` line.
- **how to reach it:** the tool, server or command. Pitmaster ships no bridge to other models: name one you
  already have (a command-line tool, a local model's server, an MCP server of your own). A skill uses only what it
  can actually reach today and says which listed names did not answer.
- **family:** the model family. Two seats from one family agree sooner, so a townhall spreads seats across families
  where it can.
- **cost:** free, plan (counts against a usage limit) or paid (money per call). Anything not free makes the run load
  budget-select (Q17).
- **streams:** yes when its server sends words as they are produced; the live tool can cut it off mid-sentence.
- **live:** no keeps it out of the live tool's default line-up; a run may still seat it on purpose (Q34).

Notes per neighbour (what it is good at, when it is slow) can go under the table in plain sentences.

The values above are examples; `alpha` stands for one of your own machines. The streaming check behind
`streams: yes` for LM Studio was made on 2026-10-24 (port 1234).
