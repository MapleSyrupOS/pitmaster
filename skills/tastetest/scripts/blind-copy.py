#!/usr/bin/env python3
"""blind-copy.py: copy only what an outsider would see into a scratch folder, for tastetest's blind auditor.

The auditor reads this copy and nothing else, so it meets the project the way a stranger does: no git history, no
untracked notes, no files the project never published.

What goes in:
  - every file git tracks in SOURCE, or
  - with --list FILE, only the tracked files a line of FILE matches (a publish list, such as pitmaster's
    publish.txt). One path or glob per line, "#" starts a comment. "*" and "?" stay inside one folder; "**" as a
    whole segment matches any number of folders; a line naming a folder ("docs/" or "docs") takes everything under
    it. A line that matches no tracked file is a finding, so a typo cannot drop a file silently.

Usage:
  python3 scripts/blind-copy.py SOURCE DEST [--list FILE]
  python3 scripts/blind-copy.py --self-test [--break tracked|outside|empty|list|history]

The guards, each named when it fails:
  tracked  untracked and ignored files never reach DEST
  outside  DEST is not inside SOURCE (the copy would end up in the project)
  empty    DEST is new or empty (old files would be audited as if they were published)
  list     every line of --list matches at least one tracked file
  history  DEST holds no .git folder, so the auditor cannot read the history

The self-test builds a throwaway repository and proves each guard goes red on its own failure. --break NAME
switches that guard off, and the self-test then reports FAIL by name.

This script does not push, does not use the network and changes nothing in SOURCE.
Exit status: 0 clean, 1 findings, 2 usage error. Python 3.8+, standard library only.
"""
from __future__ import annotations

import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Dict, List, Optional

GUARDS: Dict[str, bool] = {"tracked": True, "outside": True, "empty": True, "list": True, "history": True}


def tracked_files(source: pathlib.Path) -> List[str]:
    if not GUARDS["tracked"]:  # the self-test's broken arm: every file on disk, as if git were not asked
        return sorted(str(p.relative_to(source)) for p in source.rglob("*")
                      if p.is_file() and ".git" not in p.relative_to(source).parts)
    r = subprocess.run(["git", "-C", str(source), "ls-files", "-z"], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"blind-copy: {source} is not a git repository: {r.stderr.strip()}")
    return sorted(p for p in r.stdout.split("\0") if p)


def pattern_regex(line: str) -> re.Pattern:
    """One list line as a regex over a whole path; "*" and "?" never cross a "/"."""
    line = line.strip().rstrip("/")
    parts = []
    for seg in line.split("/"):
        if seg == "**":
            parts.append("(?:.*/)?")
            continue
        s = re.escape(seg).replace(r"\*", "[^/]*").replace(r"\?", "[^/]")
        parts.append(s + "/")
    body = "".join(parts).rstrip("/")
    body = body.replace("(?:.*/)?/", "(?:.*/)?")
    return re.compile("^" + body + "(?:/.*)?$")  # a folder line takes everything under it


def select(files: List[str], list_file: Optional[pathlib.Path], findings: List[str]) -> List[str]:
    if list_file is None:
        return files
    chosen = set()
    for raw in list_file.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        rx = pattern_regex(line)
        hits = [f for f in files if rx.match(f)]
        if not hits and GUARDS["list"]:
            findings.append(f"list: '{line}' matches no tracked file")
        chosen.update(hits)
    return sorted(chosen)


def blind_copy(source: pathlib.Path, dest: pathlib.Path, list_file: Optional[pathlib.Path]) -> List[str]:
    source, dest = source.resolve(), dest.resolve()
    findings: List[str] = []
    if GUARDS["outside"] and (dest == source or source in dest.parents):
        return [f"outside: {dest} is inside {source}"]
    if GUARDS["empty"] and dest.exists() and any(dest.iterdir()):
        return [f"empty: {dest} is not empty"]
    files = select(tracked_files(source), list_file, findings)
    if findings:
        return findings
    dest.mkdir(parents=True, exist_ok=True)
    for rel in files:
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / rel, target)
    if not GUARDS["history"]:  # the self-test's broken arm: the history comes along
        shutil.copytree(source / ".git", dest / ".git")
    elif (dest / ".git").exists():
        findings.append("history: the copy holds a .git folder")
    return findings


def self_test(broken: Optional[str]) -> int:
    if broken:
        if broken not in GUARDS:
            print(f"blind-copy: --break takes one of {', '.join(GUARDS)}", file=sys.stderr)
            return 2
        GUARDS[broken] = False
    failed: List[str] = []

    def check(label: str, ok: bool) -> None:
        print(f"{'ok  ' if ok else 'FAIL'} {label}")
        if not ok:
            failed.append(label)

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        src = root / "project"
        (src / "docs").mkdir(parents=True)
        (src / "README.md").write_text("hello\n")
        (src / "docs" / "guide.md").write_text("guide\n")
        (src / ".gitignore").write_text("secret.txt\n")
        git = ["git", "-C", str(src), "-c", "user.name=t", "-c", "user.email=test@example.com"]
        subprocess.run(["git", "init", "-q", str(src)], check=True)
        subprocess.run(git + ["add", "."], check=True)
        subprocess.run(git + ["commit", "-qm", "init"], check=True)
        (src / "notes.md").write_text("untracked private note\n")
        (src / "secret.txt").write_text("ignored\n")

        out = root / "a"
        f = blind_copy(src, out, None)
        check("green: a clean copy has no findings", not f)
        check("red arm tracked: untracked and ignored files stay out",
              not (out / "notes.md").exists() and not (out / "secret.txt").exists())
        check("red arm history: the copy has no .git", not (out / ".git").exists())
        check("red arm outside: a copy inside the project is refused",
              any(x.startswith("outside") for x in blind_copy(src, src / "audit", None)))
        check("red arm empty: a non-empty destination is refused",
              any(x.startswith("empty") for x in blind_copy(src, out, None)))

        lst = root / "list.txt"
        lst.write_text("docs/\n# comment\nREADME.md\n")
        f = blind_copy(src, root / "b", lst)
        check("green: a list copies only what it names",
              not f and sorted(str(p.relative_to(root / "b")) for p in (root / "b").rglob("*") if p.is_file())
              == ["README.md", "docs/guide.md"])
        lst.write_text("README.md\ndocs/typo.md\n")
        check("red arm list: a line that matches nothing is a finding",
              any(x.startswith("list") for x in blind_copy(src, root / "c", lst)))

    if failed:
        print(f"blind-copy: self-test FAILED: {', '.join(failed)}")
        return 1
    print("blind-copy: self-test passed")
    return 0


def main(argv: List[str]) -> int:
    if argv[:1] == ["--self-test"]:
        if len(argv) == 1:
            return self_test(None)
        if len(argv) == 3 and argv[1] == "--break":
            return self_test(argv[2])
        print("usage: blind-copy.py --self-test [--break " + "|".join(GUARDS) + "]", file=sys.stderr)
        return 2
    list_file = None
    if "--list" in argv:
        i = argv.index("--list")
        if i + 1 >= len(argv):
            print("blind-copy: --list needs a file", file=sys.stderr)
            return 2
        list_file = pathlib.Path(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    if len(argv) != 2:
        print("usage: blind-copy.py SOURCE DEST [--list FILE] | --self-test", file=sys.stderr)
        return 2
    findings = blind_copy(pathlib.Path(argv[0]), pathlib.Path(argv[1]), list_file)
    for line in findings:
        print(line)
    if not findings:
        print(f"blind-copy: copied to {pathlib.Path(argv[1]).resolve()}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
