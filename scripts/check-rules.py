#!/usr/bin/env python3
"""check-rules.py: check project-prep's opt-in rules catalogue against ADR-022.

  shape   each group file in skills/project-prep/rules/ opens "# <word> — <Heading>" and holds at least one rule,
          a line starting "- "; rules/README.md has a "Catalogue: YYYY-MM-DD" line and a table row per group whose
          count matches its file; the AGENTS.md template has the {{rules}} slot
  words   no rule runs over 30 words
  total   all groups together hold at most 35 rules
  repeat  no rule repeats one of the AGENTS.md template's ground rules (ADR-022 rule 11)
  lists   a rule that names a list in docs/rules/ has its starter in project-prep's templates/, named after the
          file (ADR-022, amendment of 2026-10-23)

Usage:
  python3 scripts/check-rules.py                  check the catalogue
  python3 scripts/check-rules.py --root DIR       check another checkout
  python3 scripts/check-rules.py --self-test      build fixtures and check each arm goes red when it should
  python3 scripts/check-rules.py --self-test --break shape|words|total|repeat|lists
                                                  switch one guard off, to watch its arm go red by name

Exit status: 0 clean, 1 findings, 2 usage error. Python 3.8+, standard library only.
"""
from __future__ import annotations

import pathlib
import re
import sys
import tempfile
from typing import Dict, List, Optional, Tuple

ROOT = pathlib.Path(__file__).resolve().parent.parent
RULES = pathlib.Path("skills/project-prep/rules")
TEMPLATES = pathlib.Path("skills/project-prep/templates")
TEMPLATE = TEMPLATES / "AGENTS.md.tmpl"
MAX_WORDS = 30
MAX_TOTAL = 35
ARMS = ("shape", "words", "total", "repeat", "lists")
GUARDS: Dict[str, bool] = {arm: True for arm in ARMS}
TITLE_RX = re.compile(r"^# ([a-z]+) — (\S.*)$")
DATE_RX = re.compile(r"^Catalogue: \d{4}-\d{2}-\d{2}$", re.M)
ROW_RX = re.compile(r"^\| `([a-z]+)` \| [^|]+ \| (\d+) \|", re.M)
LIST_RX = re.compile(r"docs/rules/([a-z0-9-]+\.md)")

Finding = Tuple[str, str]


def norm(line: str) -> str:
    """Lower case, letters and digits only, for comparing a rule with a ground rule."""
    return " ".join(re.findall(r"[a-z0-9]+", line.lower()))


def ground_rules(template: str) -> List[str]:
    """The template's '## Ground rules' bullets, each joined onto one line."""
    m = re.search(r"^## Ground rules\n(.*?)(?=^## |^\{\{|\Z)", template, re.M | re.S)
    if not m:
        return []
    rules: List[str] = []
    for line in m.group(1).splitlines():
        if line.startswith("- "):
            rules.append(line[2:].strip())
        elif line.startswith("  ") and rules:
            rules[-1] += " " + line.strip()
    return [r.replace("{{owner}}", "the owner") for r in rules]


def check(root: pathlib.Path) -> List[Finding]:
    findings: List[Finding] = []
    folder = root / RULES
    groups = sorted(p for p in folder.glob("*.md") if p.name != "README.md")
    if GUARDS["shape"] and not groups:
        findings.append(("shape", f"{RULES}: no group files"))
    counts: Dict[str, int] = {}
    every: List[Tuple[str, str]] = []
    for path in groups:
        lines = path.read_text(encoding="utf-8").splitlines()
        title = TITLE_RX.match(lines[0]) if lines else None
        rules = [l[2:].strip() for l in lines if l.startswith("- ")]
        if GUARDS["shape"]:
            if not title or title.group(1) != path.stem:
                findings.append(("shape", f"{path.name}: the first line must be '# {path.stem} — <Heading>'"))
            if not rules:
                findings.append(("shape", f"{path.name}: no rules (lines starting '- ')"))
        counts[path.stem] = len(rules)
        every += [(path.name, r) for r in rules]
    readme = folder / "README.md"
    text = readme.read_text(encoding="utf-8") if readme.is_file() else ""
    if GUARDS["shape"]:
        if not DATE_RX.search(text):
            findings.append(("shape", f"{RULES}/README.md: no 'Catalogue: YYYY-MM-DD' line"))
        rows = {w: int(n) for w, n in ROW_RX.findall(text)}
        for word, n in counts.items():
            if rows.get(word) != n:
                findings.append(("shape", f"{RULES}/README.md: the {word} row says {rows.get(word)}, "
                                          f"its file holds {n}"))
        for word in sorted(set(rows) - set(counts)):
            findings.append(("shape", f"{RULES}/README.md: a {word} row with no {word}.md"))
    tmpl_path = root / TEMPLATE
    tmpl = tmpl_path.read_text(encoding="utf-8") if tmpl_path.is_file() else ""
    if GUARDS["shape"] and "{{rules}}" not in tmpl:
        findings.append(("shape", f"{TEMPLATE}: no {{{{rules}}}} slot"))
    for name, rule in every:
        n = len(rule.split())
        if GUARDS["words"] and n > MAX_WORDS:
            findings.append(("words", f"{name}: {n} words, over {MAX_WORDS}: {rule[:60]}"))
    if GUARDS["total"] and len(every) > MAX_TOTAL:
        findings.append(("total", f"{RULES}: {len(every)} rules in all, over {MAX_TOTAL}"))
    grounds = [norm(g) for g in ground_rules(tmpl)]
    for name, rule in every:
        r = norm(rule)
        hit = next((g for g in grounds if g and (g in r or r in g)), None)
        if GUARDS["repeat"] and hit:
            findings.append(("repeat", f"{name}: repeats a ground rule of the AGENTS.md template: {rule[:60]}"))
    for name, rule in every:
        for listed in LIST_RX.findall(rule):
            if GUARDS["lists"] and not (root / TEMPLATES / f"{listed}.tmpl").is_file():
                findings.append(("lists", f"{name}: names docs/rules/{listed}, with no starter "
                                          f"{TEMPLATES}/{listed}.tmpl"))
    return findings


def make_fixture(base: pathlib.Path, name: str, plan_rules: List[str], rows: Optional[str] = None) -> pathlib.Path:
    root = base / name
    (root / RULES).mkdir(parents=True)
    (root / TEMPLATE).parent.mkdir(parents=True)
    (root / TEMPLATE).write_text(
        "# AGENTS.md\n\n## Ground rules\n- Work on a branch. Never push straight to the main branch without\n"
        "  {{owner}}'s approval.\n- Keep `docs/` tidy: no loose dated files at its top level.\n\n{{rules}}\n",
        encoding="utf-8")
    body = "".join(f"- {r}\n" for r in plan_rules)
    (root / RULES / "plan.md").write_text(f"# plan — Plan and decide\n\nPre-ticked.\n\n{body}", encoding="utf-8")
    table = rows if rows is not None else f"| `plan` | Plan and decide | {len(plan_rules)} | pre-ticked |\n"
    (root / RULES / "README.md").write_text(
        f"# Rules\n\nCatalogue: 2026-10-23\n\n| group | heading | rules | at setup |\n|---|---|---|---|\n{table}",
        encoding="utf-8")
    return root


def self_test(broken: Optional[str]) -> int:
    if broken is not None and broken not in ARMS:
        print(f"check-rules: --break takes one of {', '.join(ARMS)}", file=sys.stderr)
        return 2
    if broken:
        GUARDS[broken] = False
    failed: List[str] = []

    def expect(label: str, ok: bool) -> None:
        print(("ok   " if ok else "FAIL ") + label)
        if not ok:
            failed.append(label)

    def arm(label: str, kind: str, findings: List[Finding]) -> None:
        if any(f[0] == kind for f in findings):
            print(f"ok   red arm {label}: the {kind} check failed it, as it should")
        else:
            print(f"FAIL red arm {label}: the {kind} check let it through")
            failed.append(label)

    with tempfile.TemporaryDirectory() as tmp:
        base = pathlib.Path(tmp)
        good = ["Say how big a job is before starting it.", "Never delete advice you withdrew."]
        expect("green: a well-formed catalogue has no findings", check(make_fixture(base, "green", good)) == [])
        arm("shape", "shape", check(make_fixture(base, "shape", good, rows="| `plan` | Plan and decide | 3 | on |\n")))
        arm("words", "words", check(make_fixture(base, "words", good + [" ".join(["word"] * 31) + "."])))
        arm("total", "total", check(make_fixture(base, "total", [f"Rule number {i}." for i in range(36)])))
        arm("repeat", "repeat", check(make_fixture(
            base, "repeat", good + ["Keep docs/ tidy: no loose dated files at its top level."])))
        expect("green: a rule that only shares words with a ground rule is not a repeat", check(make_fixture(
            base, "near", good + ["Keep the docs short."])) == [])
        listed = good + ["Give every task one home, written in `docs/rules/task-homes.md`."]
        arm("lists", "lists", check(make_fixture(base, "lists", listed)))
        root = make_fixture(base, "listed", listed)
        (root / TEMPLATES / "task-homes.md.tmpl").write_text("# Task homes\n", encoding="utf-8")
        expect("green: a rule whose list has its starter has no findings", check(root) == [])
    print(f"check-rules self-test: {'FAIL' if failed else 'ok'} ({len(failed)} failed)")
    return 1 if failed else 0


def main(argv: List[str]) -> int:
    if argv[:1] == ["--self-test"]:
        rest = argv[1:]
        if rest and not (len(rest) == 2 and rest[0] == "--break"):
            print(f"usage: check-rules.py --self-test [--break {'|'.join(ARMS)}]", file=sys.stderr)
            return 2
        return self_test(rest[1] if rest else None)
    root = ROOT
    if argv[:1] == ["--root"] and len(argv) == 2:
        root = pathlib.Path(argv[1]).resolve()
    elif argv:
        print(__doc__, file=sys.stderr)
        return 2
    findings = check(root)
    for kind, msg in findings:
        print(f"{kind}: {msg}")
    total = sum(1 for _ in (root / RULES).glob("*.md")) - 1
    print(f"check-rules: {len(findings)} finding(s) over {max(total, 0)} group files")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
