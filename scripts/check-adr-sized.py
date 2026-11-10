#!/usr/bin/env python3
"""check-adr-sized.py: verify that every copy of makeadr's "Is it ADR-sized?" test equals the master.

makeadr's SKILL.md holds the master paragraph between two markers:

  <!-- adr-sized:begin ... -->
  ...
  <!-- adr-sized:end -->

Any other skills/<name>/SKILL.md that carries the markers holds a copy, and the copy must match the master line for
line. Leading and trailing spaces on each line are ignored, so a copy may sit indented inside a list item; every
other difference fails, naming the file and the first line that differs. A skill with no markers is not checked.
A begin marker without an end marker, or two blocks in one file, fails.

Usage:
  python3 scripts/check-adr-sized.py               check every skill under <root>/skills/
  python3 scripts/check-adr-sized.py --root DIR    check the skills under DIR/skills/
  python3 scripts/check-adr-sized.py --self-test   build fixtures and verify the checker

Exit codes: 0 all copies match (or none exist); 1 a copy differs or a block is malformed; 2 the master is missing.
Standard library only.
"""
import argparse
import sys
import tempfile
from pathlib import Path
from typing import List, Optional, Tuple

BEGIN = "<!-- adr-sized:begin"
END = "<!-- adr-sized:end -->"
MASTER = Path("skills") / "makeadr" / "SKILL.md"


def extract(text: str) -> Tuple[Optional[List[str]], Optional[str]]:
    """Return (block lines, error). (None, None) when the file has no begin marker."""
    lines = text.splitlines()
    begins = [i for i, line in enumerate(lines) if line.strip().startswith(BEGIN)]
    if not begins:
        return None, None
    if len(begins) > 1:
        return None, f"{len(begins)} begin markers; one block per file"
    start = begins[0]
    for j in range(start + 1, len(lines)):
        if lines[j].strip() == END:
            return [line.strip() for line in lines[start : j + 1]], None
        if lines[j].strip().startswith(BEGIN):
            break
    return None, f"line {start + 1}: begin marker with no end marker"


def check(root: Path) -> Tuple[int, List[str]]:
    out: List[str] = []
    master_path = root / MASTER
    if not master_path.is_file():
        return 2, [f"check-adr-sized: FAIL master missing: {MASTER}"]
    master, err = extract(master_path.read_text(encoding="utf-8"))
    if err or master is None:
        return 2, [f"check-adr-sized: FAIL master {MASTER}: {err or 'no adr-sized block'}"]
    failures = 0
    copies = 0
    for skill in sorted((root / "skills").glob("*/SKILL.md")):
        if skill.resolve() == master_path.resolve():
            continue
        block, err = extract(skill.read_text(encoding="utf-8"))
        rel = skill.relative_to(root)
        if err:
            failures += 1
            out.append(f"FAIL {rel}: {err}")
            continue
        if block is None:
            continue
        copies += 1
        if block != master:
            failures += 1
            for n, (a, b) in enumerate(zip(block, master)):
                if a != b:
                    out.append(f"FAIL {rel}: block line {n + 1} differs from {MASTER}\n  copy:   {a}\n  master: {b}")
                    break
            else:
                out.append(f"FAIL {rel}: block has {len(block)} lines, {MASTER} has {len(master)}")
    out.append(f"check-adr-sized: {copies} cop{'y' if copies == 1 else 'ies'} of {MASTER}, {failures} failure(s)")
    return (1 if failures else 0), out


def self_test() -> int:
    block = [
        "<!-- adr-sized:begin (copy) -->",
        "**Is it ADR-sized?** It binds a later session and shows a sign.",
        "Not ADR-sized: a mechanism with one plain answer.",
        "<!-- adr-sized:end -->",
    ]
    master = "# makeadr\n\n" + "\n".join(block) + "\n"

    def run(files: dict) -> int:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for rel, text in files.items():
                p = root / rel
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(text, encoding="utf-8")
            rc, _ = check(root)
            return rc

    indented = "# bbq\n\n3. Step:\n" + "\n".join("   " + line for line in block) + "\n"
    one_word = "# goforit\n" + "\n".join(block).replace("later session", "later run") + "\n"
    no_end = "# carte\n" + "\n".join(block[:-1]) + "\n"
    two = "# twice\n" + "\n".join(block) + "\n" + "\n".join(block) + "\n"
    cases = [
        ("an exact copy passes", {"skills/makeadr/SKILL.md": master, "skills/bbq/SKILL.md": master}, 0),
        ("an indented copy passes", {"skills/makeadr/SKILL.md": master, "skills/bbq/SKILL.md": indented}, 0),
        ("a skill with no markers is not checked", {"skills/makeadr/SKILL.md": master, "skills/x/SKILL.md": "# x\n"}, 0),
        ("a one-word change fails", {"skills/makeadr/SKILL.md": master, "skills/goforit/SKILL.md": one_word}, 1),
        ("a missing end marker fails", {"skills/makeadr/SKILL.md": master, "skills/carte/SKILL.md": no_end}, 1),
        ("two blocks in one file fail", {"skills/makeadr/SKILL.md": master, "skills/t/SKILL.md": two}, 1),
        ("a missing master fails", {"skills/bbq/SKILL.md": master}, 2),
    ]
    bad = 0
    for name, files, want in cases:
        got = run(files)
        ok = got == want
        bad += not ok
        print(f"{'PASS' if ok else 'FAIL'} {name} (exit {got}, want {want})")
    print(f"check-adr-sized self-test: {len(cases) - bad}/{len(cases)} passed")
    return 1 if bad else 0


def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    rc, out = check(Path(args.root))
    print("\n".join(out))
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
