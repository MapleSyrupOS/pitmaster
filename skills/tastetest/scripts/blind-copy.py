#!/usr/bin/env python3
"""blind-copy.py: copy only what an outsider would see into a scratch folder, for tastetest's blind auditor.

The auditor reads this copy and nothing else, so it meets the project the way a stranger does: no git history, no
untracked notes, no files the project never published.

What goes in:
  - every file git tracks in SOURCE, or
  - with --list FILE, only the tracked files a line of FILE matches (a publish list, such as pitmaster's
    publish.txt). One path or glob per line, "#" starts a comment. "*", "?" and "[seq]" stay inside one folder;
    "**" as a whole segment matches any number of folders, a trailing one included ("examples/**"); a line naming a
    folder ("docs/" or "docs") takes everything under it. Files under docs/decisions/public/pending/ (makeadr's
    drafts of public ADR copies) are never copied: they wait for the release review. A line that matches no tracked file is a finding, so a typo cannot drop a file silently. An overlay line,
    "<pattern> -> <folder>/", copies each file its pattern matches to <folder>/ plus the file's own name instead of
    its own path, as pitmaster's scripts/publish.py publishes it; the folder ends in "/", and a line holds one "->".

Usage:
  python3 scripts/blind-copy.py SOURCE DEST [--list FILE]
  python3 scripts/blind-copy.py --self-test [--break tracked|outside|empty|list|history|overlay|glob|pending]

The guards, each named when it fails:
  tracked  untracked and ignored files never reach DEST
  outside  DEST is not inside SOURCE (the copy would end up in the project)
  empty    DEST is new or empty (old files would be audited as if they were published)
  list     every line of --list matches at least one tracked file
  history  DEST holds no .git folder, so the auditor cannot read the history
  overlay  an overlay line is well formed (one "->", a folder ending in "/" with no "." or ".."), and no two files
           are copied to the same path
  glob     lines match as publish.py matches them, so a trailing "**" takes everything under its folder
  pending  a list never copies a pending draft, and a line that names only pending drafts is a finding

The self-test builds a throwaway repository and proves each guard goes red on its own failure. --break NAME
switches that guard off (overlay reads the whole line as one glob again, and glob goes back to the old matcher,
the old behaviours), and the self-test then
reports FAIL by name.

This script does not push, does not use the network and changes nothing in SOURCE.
Exit status: 0 clean, 1 findings, 2 usage error. Python 3.8+, standard library only.
"""
from __future__ import annotations

import pathlib
import re
import fnmatch
import shutil
import subprocess
import sys
import tempfile
from typing import Dict, List, Optional, Tuple

GUARDS: Dict[str, bool] = {"tracked": True, "outside": True, "empty": True, "list": True, "history": True,
                           "overlay": True, "glob": True, "pending": True}
ARROW = "->"
PENDING_DIR = "docs/decisions/public/pending/"  # makeadr's drafts of public ADR copies, never published (ADR-020)


def tracked_files(source: pathlib.Path) -> List[str]:
    if not GUARDS["tracked"]:  # the self-test's broken arm: every file on disk, as if git were not asked
        return sorted(str(p.relative_to(source)) for p in source.rglob("*")
                      if p.is_file() and ".git" not in p.relative_to(source).parts)
    r = subprocess.run(["git", "-C", str(source), "ls-files", "-z"], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"blind-copy: {source} is not a git repository: {r.stderr.strip()}")
    return sorted(p for p in r.stdout.split("\0") if p)


def seg_match(pat: List[str], segs: List[str]) -> bool:
    """Pattern segments against path segments: "**" takes any number of segments, the rest one each, with fnmatch's
    "*", "?" and "[seq]". publish.py's rule, mirrored rather than imported, as parse_line's is."""
    if not pat:
        return not segs
    if pat[0] == "**":
        return any(seg_match(pat[1:], segs[i:]) for i in range(len(segs) + 1))
    return bool(segs) and fnmatch.fnmatchcase(segs[0], pat[0]) and seg_match(pat[1:], segs[1:])


def matches(rel: str, pattern: str) -> bool:
    """One list line against one path. A match on the path or on any folder above it counts (a folder line takes
    everything under it), so a trailing "**" takes the whole folder, as in publish.py."""
    if not GUARDS["glob"]:  # the self-test's broken arm: the old regex, where a trailing "**" matches nothing
        return bool(pattern_regex(pattern).match(rel))
    segs = rel.split("/")
    pat = pattern.strip().strip("/").split("/")
    return any(seg_match(pat, segs[:k]) for k in range(1, len(segs) + 1))


def pattern_regex(line: str) -> re.Pattern:
    """The old matcher, kept only for the self-test's broken glob arm: "*" and "?" never cross a "/"."""
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


def parse_line(line: str, findings: List[str]) -> Optional[Tuple[str, Optional[str]]]:
    """One list line as (pattern, folder), the folder None for a plain line. A malformed overlay line is a finding
    and gives None, so it copies nothing. The rule is publish.py's, mirrored rather than imported: this script runs
    in any project, and publish.py is pitmaster's own."""
    if ARROW not in line or not GUARDS["overlay"]:  # the self-test's broken arm: the whole line is one glob
        return line, None
    parts = [x.strip() for x in line.split(ARROW)]
    if len(parts) != 2:
        findings.append(f"overlay: '{line}' has more than one '{ARROW}'; an overlay line is '<pattern> {ARROW} <folder>/'")
        return None
    pattern, folder = parts
    if not pattern:
        findings.append(f"overlay: '{line}' has no pattern before '{ARROW}'")
        return None
    if not folder.endswith("/") or any(x in ("", ".", "..") for x in folder[:-1].split("/")):
        findings.append(f"overlay: '{line}': the destination '{folder}' is not a folder ending in '/'"
                        " (a relative path with no '.' or '..')")
        return None
    return pattern, folder


def select(files: List[str], list_file: Optional[pathlib.Path], findings: List[str]) -> List[Tuple[str, str]]:
    """The (source, destination) pairs to copy, both relative to SOURCE. A plain line copies a file to its own path;
    an overlay line copies it to its folder plus its file name."""
    if list_file is None:
        return [(f, f) for f in files]
    pairs = set()
    for raw in list_file.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        entry = parse_line(line, findings)
        if entry is None:
            continue
        pattern, folder = entry
        hits = [f for f in files if matches(f, pattern)]
        drafts = [f for f in hits if f.startswith(PENDING_DIR)] if GUARDS["pending"] else []
        hits = [f for f in hits if f not in drafts]  # pending drafts wait for the release review and never go out
        if drafts and not hits:
            findings.append(f"pending: '{line}' names only pending drafts ({drafts[0]}); they wait for the release review")
        elif not hits and GUARDS["list"]:
            findings.append(f"list: '{line}' matches no tracked file")
        pairs.update((f, f if folder is None else folder + f.rsplit("/", 1)[-1]) for f in hits)
    sources: Dict[str, List[str]] = {}
    for src, dst in pairs:
        sources.setdefault(dst, []).append(src)
    for dst in sorted(sources):
        if len(sources[dst]) > 1:
            findings.append(f"overlay: '{dst}' would be copied from more than one file: {', '.join(sorted(sources[dst]))}")
    return sorted(pairs)


def blind_copy(source: pathlib.Path, dest: pathlib.Path, list_file: Optional[pathlib.Path]) -> List[str]:
    source, dest = source.resolve(), dest.resolve()
    findings: List[str] = []
    if GUARDS["outside"] and (dest == source or source in dest.parents):
        return [f"outside: {dest} is inside {source}"]
    if GUARDS["empty"] and dest.exists() and any(dest.iterdir()):
        return [f"empty: {dest} is not empty"]
    pairs = select(tracked_files(source), list_file, findings)
    if findings:
        return findings
    dest.mkdir(parents=True, exist_ok=True)
    for src, dst in pairs:
        target = dest / dst
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / src, target)
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
        (src / "public").mkdir()
        (src / "README.md").write_text("hello\n")
        (src / "docs" / "guide.md").write_text("guide\n")
        (src / "public" / "guide.md").write_text("public guide\n")  # a public copy, published by an overlay line
        (src / "examples" / "deep").mkdir(parents=True)
        (src / "examples" / "deep" / "one.txt").write_text("one\n")
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

        def files_in(d: pathlib.Path) -> List[str]:  # .git left out, so only the history arm sees a broken history
            return sorted(p.relative_to(d).as_posix() for p in d.rglob("*")
                          if p.is_file() and ".git" not in p.relative_to(d).parts)

        lst = root / "list.txt"
        lst.write_text("docs/\n# comment\nREADME.md\n")
        f = blind_copy(src, root / "b", lst)
        check("green: a list copies only what it names",
              not f and files_in(root / "b") == ["README.md", "docs/guide.md"])
        lst.write_text("README.md\ndocs/typo.md\n")
        check("red arm list: a line that matches nothing is a finding",
              any(x.startswith("list") for x in blind_copy(src, root / "c", lst)))

        lst.write_text("examples/**\n")
        f = blind_copy(src, root / "h", lst)
        check("red arm glob: a trailing '**' takes everything under its folder",
              not f and files_in(root / "h") == ["examples/deep/one.txt"])
        pend = src / "docs" / "decisions" / "public" / "pending"
        pend.mkdir(parents=True)
        (pend / "ADR-001-x.md").write_text("draft\n")  # a public copy waiting for the release review
        subprocess.run(git + ["add", "docs/decisions"], check=True)
        subprocess.run(git + ["commit", "-qm", "a pending draft"], check=True)
        lst.write_text("docs/\n")
        f = blind_copy(src, root / "i", lst)
        check("red arm pending: a folder line leaves pending drafts out",
              not f and files_in(root / "i") == ["docs/guide.md"])
        lst.write_text("README.md\ndocs/decisions/public/pending/*.md\n")
        check("red arm pending: a line that names only pending drafts is a finding",
              any(x.startswith("pending") for x in blind_copy(src, root / "j", lst)))

        lst.write_text("README.md\npublic/guide.md -> docs/\n")
        f = blind_copy(src, root / "d", lst)
        check("red arm overlay: an overlay line copies its file to the folder it names, not to its own path",
              not f and files_in(root / "d") == ["README.md", "docs/guide.md"]
              and (root / "d" / "docs" / "guide.md").read_text() == "public guide\n")
        for tag, bad, label in (("e", "README.md -> docs/x", "an overlay folder with no trailing '/'"),
                                ("f", "README.md -> docs/ -> more/", "an overlay line with two '->'"),
                                ("g", "docs/guide.md\npublic/guide.md -> docs/", "two files copied to one path")):
            lst.write_text(bad + "\n")
            check(f"red arm overlay: {label} is a finding",
                  any(x.startswith("overlay") for x in blind_copy(src, root / tag, lst)))

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
