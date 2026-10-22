#!/usr/bin/env python3
"""run-trigger-tests.py: check that each skill loads for the prompts it should, and not for its near-misses.

The cases live in evals/<case>/prompt.md with one grader in evals/<case>/graders/, in the layout `claude plugin
eval` reads (use that harness where your account has it). This runner does the same check with headless Claude
Code, so it works without the harness:

  - each prompt runs in a fresh, empty folder with this repository loaded as a plugin (`--plugin-dir`);
  - the run is cut off after two turns; only the first decision matters;
  - a case passes when the Skill tool was called for its skill (skill-fired) or was not (skill-not-fired).

Usage:
  python3 scripts/run-trigger-tests.py                  every case, each case's `runs` times
  python3 scripts/run-trigger-tests.py --runs 1         override the run count
  python3 scripts/run-trigger-tests.py --case 'bbq-*'   only matching cases
  python3 scripts/run-trigger-tests.py --report FILE    also write a Markdown table of the results
  --jobs N (default 4)   --model NAME   --claude PATH (default: claude)

Each run is a real model call billed to the signed-in plan. Exit 2 means the runs could not start (for
example, Claude Code is not signed in), not that a skill failed. Python 3.9+, standard library only.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import fnmatch
import json
import pathlib
import re
import subprocess
import sys
import tempfile
from typing import Dict, List, Tuple

ROOT = pathlib.Path(__file__).resolve().parent.parent
EVALS = ROOT / "evals"


def parse_case(folder: pathlib.Path) -> Dict:
    text = (folder / "prompt.md").read_text(encoding="utf-8")
    _, front, body = text.split("---\n", 2)
    meta: Dict[str, str] = {}
    for line in front.splitlines():
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip()
    graders = list((folder / "graders").glob("*.md"))
    g = graders[0].read_text(encoding="utf-8")
    skill = re.search(r"\(\?:\[\\w-\]\+:\)\?([a-z0-9-]+)", g).group(1)
    expect = "max: 0" not in g
    return {"name": meta.get("name", folder.name), "prompt": body.strip(), "runs": int(meta.get("runs", "3")),
            "skill": skill, "expect": expect}


def skills_called(stream: str) -> List[str]:
    called = []
    for line in stream.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if event.get("type") != "assistant":
            continue
        for item in event.get("message", {}).get("content", []) or []:
            if item.get("type") == "tool_use" and item.get("name") == "Skill":
                called.append(str(item.get("input", {}).get("skill", "")))
    return called


def run_once(case: Dict, args) -> Tuple[bool, List[str], str]:
    cmd = [args.claude, "-p", case["prompt"], "--plugin-dir", str(ROOT), "--output-format", "stream-json",
           "--verbose", "--max-turns", "2", "--allowedTools", "Skill", "Read", "Glob", "Grep",
           "--strict-mcp-config", "--no-session-persistence"]
    if args.model:
        cmd += ["--model", args.model]
    with tempfile.TemporaryDirectory() as cwd:
        try:
            r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=240, stdin=subprocess.DEVNULL)
            out, err = r.stdout, r.stderr
        except subprocess.TimeoutExpired as e:
            out, err = (e.stdout or b"").decode() if isinstance(e.stdout, bytes) else (e.stdout or ""), "timeout"
    if "Failed to authenticate" in out or "Not logged in" in out or "Invalid API key" in out:
        raise RuntimeError("Claude Code is not signed in: run `claude auth login`, then try again")
    called = skills_called(out)
    fired = any(re.fullmatch(r"(?:[\w-]+:)?" + re.escape(case["skill"]), c) for c in called)
    note = "" if out.strip() else (err.strip().splitlines() or ["no output"])[-1][:120]
    return fired == case["expect"], called, note


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", type=int)
    ap.add_argument("--case", default="*")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--model")
    ap.add_argument("--claude", default="claude")
    ap.add_argument("--report")
    args = ap.parse_args()
    cases = [parse_case(d) for d in sorted(EVALS.iterdir())
             if (d / "prompt.md").is_file() and fnmatch.fnmatch(d.name, args.case)]
    jobs = [(c, i) for c in cases for i in range(args.runs or c["runs"])]
    results: Dict[str, List[Tuple[bool, List[str], str]]] = {c["name"]: [] for c in cases}
    with cf.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {pool.submit(run_once, c, args): c for c, _ in jobs}
        for f in cf.as_completed(futures):
            c = futures[f]
            try:
                results[c["name"]].append(f.result())
            except RuntimeError as e:
                print(f"run-trigger-tests: stopped: {e}", file=sys.stderr)
                pool.shutdown(wait=False, cancel_futures=True)
                return 2
            ok, called, note = results[c["name"]][-1]
            print(f"{'pass' if ok else 'FAIL'} {c['name']}: called {called or 'no skill'} {note}".rstrip(),
                  flush=True)
    rows = []
    failed = 0
    for c in cases:
        rs = results[c["name"]]
        passed = sum(ok for ok, _, _ in rs)
        failed += passed < len(rs)
        seen = sorted({s for _, called, _ in rs for s in called}) or ["none"]
        rows.append(f"| {c['name']} | {'should' if c['expect'] else 'should not'} | {passed}/{len(rs)} | "
                    f"{', '.join(seen)} | {c['prompt'][:70].replace('|', '/')} |")
    table = ["| case | load? | passed | skills called | prompt |", "|---|---|---|---|---|"] + rows
    print("\n".join(table))
    print(f"run-trigger-tests: {len(cases) - failed}/{len(cases)} cases passed every run")
    if args.report:
        pathlib.Path(args.report).write_text("\n".join(table) + "\n", encoding="utf-8")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
