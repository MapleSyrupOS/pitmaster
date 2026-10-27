#!/usr/bin/env python3
"""check-all.py: run every check CI runs, in order, and say which failed.

  1. the leak check over every tracked file (scripts/check-leaks.py)
  2. each script's own self-test, with its deliberate failures
  3. the skill spec and platform notes (scripts/build-variants.py --check)
  4. manifest parity between Claude and Codex (scripts/sync-manifests.py --check)
  5. every pinned copy under skills/ equals the release its .pin names (scripts/check-pins.py; makeadr's adr-plus
     copy among them), and adr-plus's own self-test passes
  6. pitmaster's own ADRs: every YAML header passes the schema, the index is current, every proof resolves and the
     triggers hold from ADR-003 on
  7. pitmaster's own STATUS.md (status-check, with the sections pitmaster.md names)
  8. project-prep's rules catalogue: its shape, 30 words a rule, 35 rules in all, no repeat of a ground rule
     (scripts/check-rules.py, ADR-022)

In the public repository (no publish.txt) the publish self-test and the STATUS check are skipped: the publisher and
STATUS.md live only in the private one. The ADR checks run on the public copies there.

Python 3.8+, standard library only. Exit 1 if any check fails.
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ADR = ROOT / "skills" / "makeadr" / "scripts"
ADR_PLUS = ROOT / "skills" / "makeadr" / "adr-plus"
PRIVATE_ONLY = {"publish self-test", "STATUS"}
PUBLIC = not (ROOT / "publish.txt").exists()
CHECKS = [
    ("leaks", ["scripts/check-leaks.py"]),
    ("leaks self-test", ["scripts/check-leaks.py", "--self-test"]),
    ("publish self-test", ["scripts/publish.py", "--self-test"]),
    ("variants self-test", ["scripts/build-variants.py", "--self-test"]),
    ("adr-index self-test", [str(ADR / "adr-index.py"), "--self-test"]),
    ("adr-check self-test", [str(ADR / "adr-check.py"), "--self-test"]),
    ("status-check self-test", [str(ROOT / "skills" / "project-prep" / "scripts" / "status-check.py"), "--self-test"]),
    ("blind-copy self-test", [str(ROOT / "skills" / "tastetest" / "scripts" / "blind-copy.py"), "--self-test"]),
    ("seeded-fixture self-test", [str(ROOT / "skills" / "tastetest" / "scripts" / "seeded-fixture.py"), "--self-test"]),
    ("looseends-scan self-test", [str(ROOT / "skills" / "looseends" / "scripts" / "looseends-scan.py"), "--self-test"]),
    ("neighbours self-test", [str(ROOT / "skills" / "townhall" / "scripts" / "neighbours.py"), "--self-test"]),
    ("neighbour-check self-test", [str(ROOT / "skills" / "neighbour-check" / "scripts" / "neighbour-check.py"), "--self-test"]),
    # talk-through carries the same pinned copy; check-pins keeps the two equal.
    ("record-check self-test", [str(ROOT / "skills" / "townhall" / "scripts" / "record-check.py"), "--self-test"]),
    ("skill spec", ["scripts/build-variants.py", "--check"]),
    ("manifest parity", ["scripts/sync-manifests.py", "--check"]),
    ("pins self-test", ["scripts/check-pins.py", "--self-test"]),
    ("pins", ["scripts/check-pins.py"]),
    ("adr-plus self-test", [str(ADR_PLUS / "tools" / "adr-yaml.py"), "--self-test"]),
    ("ADR headers", [str(ADR_PLUS / "tools" / "adr-yaml.py"), "--check"]),
    ("ADR index", [str(ADR / "adr-index.py"), "--check"]),
    # The trigger check starts at ADR-003, the rule that set it. ADR-009 and ADR-010 name their chosen option
    # "(chosen)" with no reason, and ADR-018 weighs three options with no Drivers list; their text was ratified
    # before the check existed, so they are skipped by name.
    ("ADR check", [str(ADR / "adr-check.py"), "--triggers-from", "3", "--triggers-skip", "9,10,18"]),
    # pitmaster's own STATUS.md: the sections pitmaster.md names, every bullet citing a file that exists.
    ("STATUS", [str(ROOT / "skills" / "project-prep" / "scripts" / "status-check.py"), "--root", str(ROOT)]),
    ("spend-ledger self-test", [str(ROOT / "skills" / "spend-ledger" / "scripts" / "spend-ledger.py"), "--self-test"]),
    ("rules self-test", ["scripts/check-rules.py", "--self-test"]),
    ("rules", ["scripts/check-rules.py"]),
]


def main() -> int:
    failed = []
    ran = 0
    for name, cmd in CHECKS:
        if PUBLIC and name in PRIVATE_ONLY:
            print(f"skip {name} (private repository only)")
            continue
        ran += 1
        r = subprocess.run([sys.executable, *cmd], cwd=ROOT, capture_output=True, text=True)
        status = "ok  " if r.returncode == 0 else "FAIL"
        print(f"{status} {name}")
        if r.returncode != 0:
            failed.append(name)
            print("     " + (r.stdout + r.stderr).strip().replace("\n", "\n     "))
    print(f"check-all: {ran - len(failed)}/{ran} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
