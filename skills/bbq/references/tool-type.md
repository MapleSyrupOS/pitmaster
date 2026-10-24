# The Tool type

The Tool type grills the user about a tool a person can run without an agent, writes its record, and carries it to
its ADR; the build is offered after that (ADR-026). "maketool" opens bbq straight in it; "tool bbq" names it too.

## First, the line

A script that is only useful inside a skill's steps is a skill script, not a tool: offer the Skill type instead. A
tool is one a person can run on its own, from a terminal, with no agent (in pitmaster, ADR-012's rule 1).

## Where tools live

The config's `tools_home` says where: a folder in this project (such as `tools/`) or a repository of its own. On
`ask`, the default, ask once and suggest saving the answer in `pitmaster.md` (`tools_home: tools/`). Pins are part of
the build only where the project pins its tools into skills.

## What the questions must cover

Ten things, within the bbq's count:

- what the tool is for, in one sentence;
- how a person runs it with no agent: the command, its options, its defaults;
- what it reads and what it writes;
- its output and exit codes;
- what it must never do;
- who uses it and how it reaches them: which skills pin it, how a skill hands off to it, how a person installs it,
  and how a fix reaches every copy (the version, the tag, the re-pin);
- the platforms it runs on, and whether it stays in the language's standard library, or why not;
- network and secrets: what it reaches, and where any key comes from (never a file in the repository);
- its self-test, and the deliberate break that proves the test can fail;
- its name and where it lives in the tools home. The name is taste: ask it, never choose it.

## What it writes

1. **The record**, each rule tagged with the question that set it, as every bbq writes. No draft folder: a tool's
   code is written where it lives, in the tools home.
2. **The ADR.** Offer `makeadr`. What the bbq settled with citations it writes from the record; it asks only what
   is still open.

## The life cycle

1. **The record**, then **the ADR** through makeadr.
2. **The owner's ratification.** Only the owner's own "ratify" counts; an agent never ratifies.
3. **The build, offered.** After the ratification, offer the build; on a yes, or "goforit", do it:
   - the tool in the tools home, with its self-test and its deliberate break, in a PR there;
   - once that PR is checked, the pinned copies in each skill that uses the tool, in one PR here, with the plugin's
     patch bump and a CHANGELOG line where the project has them.
   Then stop: merging is the owner's, unless a grant says otherwise.
