#!/usr/bin/env python3
"""build-variants.py: check every skill against the spec, and build per-platform variants and zips (ADR-001).

Every SKILL.md ends with a "## Platform notes" section of tagged bullets. A variant keeps the skill's body byte
for byte and filters that section to its platform's bullets:

  claude    **Claude Code:**, **Cowork / claude.ai:** and **Other tools:**
  codex     **Codex:** and **Other tools:**
  generic   **Other tools:** only

Usage:
  python3 scripts/build-variants.py --check     the spec check (CI): exit 1 on any problem
  python3 scripts/build-variants.py             write dist/<platform>/<skill>/
  python3 scripts/build-variants.py --zip       also write dist/zips/<skill>-<platform>.skill (a zip whose top
                                                 level is the skill folder, for Cowork / claude.ai upload)
  python3 scripts/build-variants.py --self-test

The spec check: the folder name is lowercase letters, digits and hyphens (at most 64) and equals the frontmatter
`name`; the frontmatter has only `name`, `description` and a `metadata:` map holding only `family:` from FAMILIES; the description is at most 1,024 characters; the title
starts '# <name>: '; unless grandfathered, a 'Decided by pitmaster ADR-NNN.' line sits before the first section
and names an ADR with a file in docs/decisions/ (ADR-004); the template templates/skill carries that line with
the literal NNN; the Platform notes section is last and has a bullet for every tag; and no Claude-only tool name
appears in the steps outside it. Python 3.8+, standard library only.
"""
from __future__ import annotations

import pathlib
import re
import shutil
import sys
import tempfile
import zipfile
from typing import Dict, List, Tuple

ROOT = pathlib.Path(__file__).resolve().parent.parent
TAGS = ("Claude Code", "Cowork / claude.ai", "Codex", "Other tools")
PLATFORMS: Dict[str, Tuple[str, ...]] = {
    "claude": ("Claude Code", "Cowork / claude.ai", "Other tools"),
    "codex": ("Codex", "Other tools"),
    "generic": ("Other tools",),
}
NAME_RX = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
# Shipped before ADR-004; each leaves this list when it gets its ADR.
GRANDFATHERED = ("bbq", "budget-select", "swarm-bottleneck", "tier-select")
DECIDED_RX = re.compile(r"^Decided by pitmaster ADR-(\d{3})\.$")
# Words that name one platform's tools. They may appear only inside Platform notes.
PLATFORM_ONLY = re.compile(
    r"AskUserQuestion|TodoWrite|\$\{?CLAUDE_SKILL_DIR\}?|/pitmaster:|(?<![\w`])/context\b|\bTask tool\b|\bAgent tool\b")
NOTES_HEAD = "## Platform notes"
FAMILIES = ("plan", "run", "usage", "check", "records", "craft")  # ADR-004, amendment of 2026-10-22
BULLET = re.compile(r"^- \*\*(.+?):\*\*")


def split_skill(text: str) -> Tuple[Dict[str, str], str, str, str]:
    """Return (frontmatter fields, the raw frontmatter block, the body before the notes, the notes section)."""
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with a '---' frontmatter line")
    end = text.index("\n---\n", 4)
    block = text[: end + 5]
    fields: Dict[str, str] = {}
    key = None
    for line in text[4:end].splitlines():
        m = re.match(r"^([A-Za-z0-9_-]+):\s?(.*)$", line)
        if m:
            key = m.group(1)
            fields[key] = m.group(2).strip()
        elif key and line.startswith((" ", "\t")):
            fields[key] += " " + line.strip()
    rest = text[end + 5:]
    i = rest.find("\n" + NOTES_HEAD + "\n")
    if i < 0:
        return fields, block, rest, ""
    return fields, block, rest[: i + 1], rest[i + 1:]


def notes_bullets(notes: str) -> List[Tuple[str, List[str]]]:
    """The notes section's bullets, each as (tag, its lines), in order."""
    bullets: List[Tuple[str, List[str]]] = []
    for line in notes.splitlines()[1:]:
        m = BULLET.match(line)
        if m:
            bullets.append((m.group(1), [line]))
        elif bullets and (line.startswith("  ") or not line.strip()):
            bullets[-1][1].append(line)
        elif line.strip():
            bullets.append(("", [line]))
    return bullets


def check_skill(folder: pathlib.Path, *, template: bool = False,
                decisions: pathlib.Path = ROOT / "docs" / "decisions") -> List[str]:
    rel = folder.relative_to(ROOT) if ROOT in folder.parents else folder
    p = folder / "SKILL.md"
    try:
        fields, _, body, notes = split_skill(p.read_text(encoding="utf-8"))
    except ValueError as e:
        return [f"{rel}: {e}"]
    problems = []
    name = folder.name
    if not NAME_RX.match(name) or len(name) > 64:
        problems.append(f"{rel}: folder name must be lowercase letters, digits and hyphens, at most 64")
    if fields.get("name") != name:
        problems.append(f"{rel}: frontmatter name {fields.get('name')!r} must equal the folder name")
    extra = sorted(set(fields) - {"name", "description", "metadata"})
    if extra:
        problems.append(f"{rel}: frontmatter may hold only name, description and metadata (found {', '.join(extra)})")
    if "metadata" in fields:
        fam = re.fullmatch(r"family: ([a-z]+)", fields["metadata"].strip())
        if not fam or fam.group(1) not in FAMILIES:
            problems.append(f"{rel}: metadata may hold only family: one of {', '.join(FAMILIES)} (ADR-004)")
    desc = fields.get("description", "")
    if not desc:
        problems.append(f"{rel}: description is missing")
    elif len(desc) > 1024:
        problems.append(f"{rel}: description is {len(desc)} characters (at most 1,024)")
    heading = next((l for l in body.splitlines() if l.startswith("# ")), "")
    if not heading.startswith(f"# {name}: "):
        problems.append(f"{rel}: the title must start '# {name}: '")
    head_lines = []
    for line in body.splitlines():
        if line.startswith("## ") and head_lines:
            break
        head_lines.append(line)
    decided = next((l for l in head_lines if DECIDED_RX.match(l)), None)
    if template:
        if "Decided by pitmaster ADR-NNN." not in head_lines:
            problems.append(f"{rel}: no 'Decided by pitmaster ADR-NNN.' line before the first section (ADR-004)")
    elif name not in GRANDFATHERED:
        if decided is None:
            problems.append(f"{rel}: no 'Decided by pitmaster ADR-NNN.' line before the first section (ADR-004)")
        else:
            n = DECIDED_RX.match(decided).group(1)
            if not list(decisions.glob(f"ADR-{n}-*.md")):
                problems.append(f"{rel}: ADR-{n} named in the Decided by line has no file in docs/decisions/")
    if not notes:
        problems.append(f"{rel}: no '{NOTES_HEAD}' section")
    else:
        if re.search(r"^## ", notes[len(NOTES_HEAD):], re.M):
            problems.append(f"{rel}: '{NOTES_HEAD}' must be the last section")
        tags = [t for t, _ in notes_bullets(notes)]
        for t in TAGS:
            if t not in tags:
                problems.append(f"{rel}: Platform notes has no **{t}:** bullet")
        for t in tags:
            if t not in TAGS:
                problems.append(f"{rel}: Platform notes has an untagged or unknown bullet ({t or 'no tag'})")
    for n, line in enumerate(body.splitlines(), start=1):
        m = PLATFORM_ONLY.search(line)
        if m:
            problems.append(f"{rel}: '{m.group(0)}' outside Platform notes (body line {n}); move it to the notes")
    return problems


def variant(text: str, platform: str) -> str:
    _, block, body, notes = split_skill(text)
    keep = PLATFORMS[platform]
    out = [NOTES_HEAD, ""]
    for tag, lines in notes_bullets(notes):
        if tag in keep:
            while lines and not lines[-1].strip():
                lines = lines[:-1]
            out.extend(lines)
    return block + body + "\n".join(out) + "\n"


def skill_folders() -> List[pathlib.Path]:
    return sorted(p.parent for p in (ROOT / "skills").glob("*/SKILL.md"))


def build(dist: pathlib.Path, make_zips: bool) -> None:
    if dist.exists():
        shutil.rmtree(dist)
    for platform in PLATFORMS:
        for folder in skill_folders():
            dest = dist / platform / folder.name
            shutil.copytree(folder, dest, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))
            (dest / "SKILL.md").write_text(variant((folder / "SKILL.md").read_text(encoding="utf-8"), platform),
                                           encoding="utf-8")
            if make_zips:
                zdir = dist / "zips"
                zdir.mkdir(parents=True, exist_ok=True)
                zpath = zdir / f"{folder.name}-{platform}.skill"
                with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
                    for f in sorted(dest.rglob("*")):
                        if f.is_file():
                            z.write(f, f.relative_to(dest.parent).as_posix())
    print(f"build-variants: wrote {dist.relative_to(ROOT)} for {', '.join(PLATFORMS)}"
          + (" with zips" if make_zips else ""))


def self_test() -> int:
    sample = ("---\nname: demo\ndescription: A demo skill. Use when testing.\n---\n\n# demo: a demo skill\n\n"
              "Decided by pitmaster ADR-999.\n\n1. Ask the user.\n\n"
              "## Platform notes\n\n- **Claude Code:** ask with AskUserQuestion.\n  Second line.\n"
              "- **Cowork / claude.ai:** the same.\n- **Codex:** a numbered list.\n- **Other tools:** a list.\n")
    v = variant(sample, "codex")
    assert "**Codex:**" in v and "**Other tools:**" in v, v
    assert "AskUserQuestion" not in v and "Second line" not in v and "Cowork" not in v.split("## Platform")[1], v
    assert v.split("## Platform notes")[0] == sample.split("## Platform notes")[0], "the body must be byte-identical"
    assert "Second line" in variant(sample, "claude")
    with tempfile.TemporaryDirectory() as tmp:
        t = pathlib.Path(tmp)
        dec = t / "decisions"
        dec.mkdir()
        (dec / "ADR-999-demo.md").write_text("# ADR-999: a demo ADR\n")
        d = t / "demo"
        d.mkdir()
        (d / "SKILL.md").write_text(sample)
        assert check_skill(d, decisions=dec) == [], check_skill(d, decisions=dec)
        (d / "SKILL.md").write_text(sample.replace("description:", "metadata:\n  family: plan\ndescription:"))
        assert check_skill(d, decisions=dec) == [], "a listed family must pass"
        (d / "SKILL.md").write_text(sample)
        reds = {
            "a platform-only word in the body": sample.replace("1. Ask the user.", "1. Call AskUserQuestion."),
            "a missing Codex bullet": sample.replace("- **Codex:** a numbered list.\n", ""),
            "extra frontmatter": sample.replace("description:", "model: x\ndescription:"),
            "a family not in the list": sample.replace("description:", "metadata:\n  family: misc\ndescription:"),
            "another metadata key": sample.replace("description:", "metadata:\n  author: x\ndescription:"),
            "a name that differs from the folder": sample.replace("name: demo", "name: other"),
            "a long description": sample.replace("A demo skill.", "x" * 1100),
            "notes not last": sample + "\n## After\n\ntext\n",
            "a title without the name": sample.replace("# demo: a demo skill", "# A demo"),
            "no Decided by line": sample.replace("Decided by pitmaster ADR-999.\n\n", ""),
            "a Decided by line naming a missing ADR": sample.replace("ADR-999.", "ADR-998."),
        }
        for why, text in reds.items():
            (d / "SKILL.md").write_text(text)
            assert check_skill(d, decisions=dec), f"red arm did not fail: {why}"
        g = t / "bbq"
        g.mkdir()
        grand = sample.replace("# demo: a demo skill", "# bbq: a Big Batch of Questions") \
                      .replace("name: demo", "name: bbq") \
                      .replace("Decided by pitmaster ADR-999.\n\n", "")
        (g / "SKILL.md").write_text(grand)
        assert check_skill(g, decisions=dec) == [], check_skill(g, decisions=dec)
        s = t / "skill"
        s.mkdir()
        templ = sample.replace("# demo: a demo skill", "# skill: a template") \
                      .replace("name: demo", "name: skill") \
                      .replace("ADR-999.", "ADR-NNN.")
        (s / "SKILL.md").write_text(templ)
        assert check_skill(s, template=True, decisions=dec) == [], check_skill(s, template=True, decisions=dec)
        assert check_skill(s, template=False, decisions=dec), "template arm failed with template=False"
    print("build-variants: self-test passed")
    return 0


def main(argv: List[str]) -> int:
    if "--self-test" in argv:
        return self_test()
    problems = [p for f in skill_folders() for p in check_skill(f)]
    tdir = ROOT / "templates" / "skill"
    if "--check" in argv and tdir.exists():
        problems += check_skill(tdir, template=True)
    if "--check" in argv:
        for p in problems:
            print(p, file=sys.stderr)
        print(f"build-variants: {len(skill_folders())} skills, {len(problems)} problem(s)")
        return 1 if problems else 0
    if problems:
        for p in problems:
            print(p, file=sys.stderr)
        return 1
    build(ROOT / "dist", "--zip" in argv)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
