#!/usr/bin/env python3
"""seeded-fixture.py: a small project with four planted flaws, and a scorer that says whether an audit found them.

This is how tastetest is shown to work (ADR-016, A3). Make the fixture, run tastetest on it, then score the report:
every planted flaw must be named, and the verdict must be NOT READY.

The planted flaws, each scored by name:
  leak         docs/setup.md holds a home-folder path
  dead-link    README.md links to docs/missing.md, which does not exist
  placeholder  README.md still has placeholder text
  false-count  README.md promises three tools; tools/ holds two
A report finds a flaw when it names the flaw's file and one of its words (see FLAWS below). The verdict must read
NOT READY.

The fixture is made on demand, not kept in the repository, so its planted home path never trips a leak check.

Usage:
  python3 scripts/seeded-fixture.py --make DIR      write the fixture into DIR (new or empty) as a git repository
  python3 scripts/seeded-fixture.py --score REPORT  score an audit report against the planted flaws
  python3 scripts/seeded-fixture.py --self-test [--break score]

The self-test scores a report that finds everything (it must pass) and, as red arms, reports that each miss one
flaw or say READY (each must fail by name). --break score makes the scorer pass anything, and the self-test then
reports FAIL by name.

Exit status: 0 clean, 1 findings, 2 usage error. Python 3.8+, standard library only.
"""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys
import tempfile
from typing import Dict, List, Tuple

HOME = "/" + "Users" + "/someone"  # built from parts so this file holds no home path itself

FILES: Dict[str, str] = {
    "README.md": (
        "# Gauge\n\n"
        "Gauge ships three tools for checking a project's health.\n\n"
        "Lorem ipsum dolor sit amet. TODO: write the real introduction.\n\n"
        "Start with the [setup guide](docs/setup.md), then read [the tour](docs/missing.md).\n"
    ),
    "docs/setup.md": f"# Setup\n\nClone the repository into {HOME}/projects/gauge and run `python3 tools/size.py`.\n",
    "tools/size.py": "print('size')\n",
    "tools/age.py": "print('age')\n",
    "LICENSE": "Apache License 2.0\n",
}

# flaw: (file the report must name, words of which one must appear)
FLAWS: Dict[str, Tuple[str, List[str]]] = {
    "leak": ("docs/setup.md", ["home", "/users/", "private path", "personal path", "leak"]),
    "dead-link": ("docs/missing.md", ["dead", "broken", "missing", "does not exist", "404"]),
    "placeholder": ("README.md", ["lorem", "placeholder", "todo"]),
    "false-count": ("README.md", ["three", "two tools", "count"]),
}
SCORER_ON = True


def make(dest: pathlib.Path) -> int:
    if dest.exists() and any(dest.iterdir()):
        print(f"seeded-fixture: {dest} is not empty", file=sys.stderr)
        return 2
    for rel, text in FILES.items():
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        (dest / rel).write_text(text, encoding="utf-8")
    git = ["git", "-C", str(dest), "-c", "user.name=fixture", "-c", "user.email=test@example.com"]
    subprocess.run(["git", "init", "-q", str(dest)], check=True)
    subprocess.run(git + ["add", "."], check=True)
    subprocess.run(git + ["commit", "-qm", "fixture"], check=True)
    print(f"seeded-fixture: made {dest}")
    return 0


def score(report: str) -> List[str]:
    """The flaws the report missed, plus 'verdict' if it does not say NOT READY. Empty means the audit passed."""
    if not SCORER_ON:
        return []
    text = report.lower()
    missed = []
    for name, (path, words) in FLAWS.items():
        found = any(path.lower() in line and any(w in line for w in words) for line in text.splitlines())
        if not found:
            missed.append(name)
    if not re.search(r"\bnot ready\b", text):
        missed.append("verdict")
    return missed


GOOD_REPORT = """NOT READY
## Blocks
- docs/setup.md:3 — a home folder path is published (leak).
- README.md:5 — links to docs/missing.md, which does not exist (dead link).
## Should fix
- README.md:5 — Lorem ipsum placeholder text and a TODO.
- README.md:3 — says three tools; tools/ has two (count is wrong).
"""


def self_test(broken: str) -> int:
    global SCORER_ON
    if broken:
        if broken != "score":
            print("seeded-fixture: --break takes score", file=sys.stderr)
            return 2
        SCORER_ON = False
    failed: List[str] = []

    def check(label: str, ok: bool) -> None:
        print(f"{'ok  ' if ok else 'FAIL'} {label}")
        if not ok:
            failed.append(label)

    with tempfile.TemporaryDirectory() as tmp:
        fx = pathlib.Path(tmp) / "fixture"
        check("green: the fixture is made as a git repository", make(fx) == 0 and (fx / ".git").exists())
        check("green: the fixture holds its planted home path", HOME in (fx / "docs/setup.md").read_text())
    check("green: a report that finds everything passes", score(GOOD_REPORT) == [])
    lines = GOOD_REPORT.splitlines()
    for name, (path, words) in FLAWS.items():
        missing = "\n".join(l for l in lines if not (path.lower() in l.lower() and any(w in l.lower() for w in words)))
        check(f"red arm {name}: a report that misses it fails", name in score(missing))
    check("red arm verdict: a report that says READY fails", "verdict" in score(GOOD_REPORT.replace("NOT READY", "READY")))

    if failed:
        print(f"seeded-fixture: self-test FAILED: {', '.join(failed)}")
        return 1
    print("seeded-fixture: self-test passed")
    return 0


def main(argv: List[str]) -> int:
    if argv[:1] == ["--self-test"]:
        if len(argv) == 1:
            return self_test("")
        if len(argv) == 3 and argv[1] == "--break":
            return self_test(argv[2])
    elif len(argv) == 2 and argv[0] == "--make":
        return make(pathlib.Path(argv[1]))
    elif len(argv) == 2 and argv[0] == "--score":
        missed = score(pathlib.Path(argv[1]).read_text(encoding="utf-8"))
        for name in missed:
            print(f"missed: {name}")
        print("seeded-fixture: the audit found every planted flaw" if not missed else
              f"seeded-fixture: {len(missed)} missed")
        return 1 if missed else 0
    print("usage: seeded-fixture.py --make DIR | --score REPORT | --self-test [--break score]", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
