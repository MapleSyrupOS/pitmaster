#!/usr/bin/env python3
"""open-items: the file fallback for the open-items page (stdlib only).

Items live in one Markdown file (default docs/open-items.md). Each item is a section:

    ## OI-003 · open · 2026-11-18T19:00Z · from lead-a
    **Pick a landing order**

    Which order should the two slices land in?

    Context: slice 2 needs slice 1's header.

    - [ ] (a) Slice 1 first (Recommended)
    - [ ] (b) Both in one PR
    - [ ] Other:

The user ticks one box ("- [x]") and may write after "Other:". The seat runs `answered` on each tick, passes
each answer on, then `close`s the item, which records the time the answer was read.

Commands:
    add --title T --question Q [--context C] [--from SEAT] [--kind K] --option TEXT [--option TEXT ...]
    list                 open items
    answered             open items the user has ticked (JSON lines)
    close ID             mark answered, with the time read
    --self-test          run the checks, deliberate failures included
Every command takes --file PATH.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import tempfile

DEFAULT = "docs/open-items.md"
HEAD = re.compile(r"^## (OI-\d{3,}) · (open|answered) · (\S+) · from (\S+)(?: · (\w+))?(?: · read (\S+))?$")
BOX = re.compile(r"^- \[( |x|X)\] (?:\((\w)\) )?(.*)$")
KINDS = ("question", "approval", "merge", "ratify", "look")


def now():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


def read(path):
    if not os.path.exists(path):
        return "# Open items\n\nTick one box per item. Write your own answer after \"Other:\".\n"
    with open(path, encoding="utf-8") as f:
        return f.read()


def parse(text):
    """Return a list of items: dict(id, status, opened, frm, kind, title, picks, other, start, end)."""
    lines = text.split("\n")
    items, cur = [], None
    for i, line in enumerate(lines):
        m = HEAD.match(line)
        if m:
            if cur:
                cur["end"] = i
            cur = {"id": m.group(1), "status": m.group(2), "opened": m.group(3), "frm": m.group(4),
                   "kind": m.group(5) or "question", "title": "", "picks": [], "other": "", "start": i, "end": None}
            items.append(cur)
            continue
        if not cur:
            continue
        if not cur["title"] and line.startswith("**") and line.endswith("**"):
            cur["title"] = line.strip("*")
        b = BOX.match(line)
        if b and b.group(1) in "xX":
            if b.group(2):
                cur["picks"].append(b.group(2))
            elif b.group(3).startswith("Other:"):
                cur["picks"].append("other")
                cur["other"] = b.group(3)[len("Other:"):].strip()
    if cur:
        cur["end"] = len(lines)
    return items


def next_id(items):
    n = max([int(i["id"][3:]) for i in items] or [0])
    return "OI-%03d" % (n + 1)


def add(path, title, question, options, context="", frm="lead", kind="question"):
    if kind not in KINDS:
        raise ValueError("kind must be one of " + ", ".join(KINDS))
    if not options:
        raise ValueError("an item needs at least one option")
    text = read(path)
    oid = next_id(parse(text))
    keys = "abcdefghijklmnopqrstuvwxyz"
    out = ["", "## %s · open · %s · from %s · %s" % (oid, now(), frm, kind), "**%s**" % title, "", question, ""]
    if context:
        out += ["Context: " + context, ""]
    for k, o in zip(keys, options):
        out.append("- [ ] (%s) %s%s" % (k, o, " (Recommended)" if k == "a" else ""))
    out.append("- [ ] Other:")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text.rstrip("\n") + "\n" + "\n".join(out) + "\n")
    return oid


def answered(path):
    """Open items with exactly one tick. Two or more ticks is not an answer; it is reported as a problem."""
    res = []
    for it in parse(read(path)):
        if it["status"] != "open" or not it["picks"]:
            continue
        if len(it["picks"]) > 1:
            res.append({"id": it["id"], "problem": "more than one box ticked", "picks": it["picks"]})
        elif it["picks"] == ["other"] and not it["other"]:
            res.append({"id": it["id"], "problem": "Other ticked with nothing written"})
        else:
            res.append({"id": it["id"], "from": it["frm"], "title": it["title"], "choice": it["picks"][0],
                        "other": it["other"]})
    return res


def close(path, oid):
    text = read(path)
    lines = text.split("\n")
    for it in parse(text):
        if it["id"] == oid:
            if it["status"] != "open":
                raise ValueError(oid + " is already answered")
            m = HEAD.match(lines[it["start"]])
            lines[it["start"]] = "## %s · answered · %s · from %s · %s · read %s" % (
                oid, m.group(3), m.group(4), m.group(5) or "question", now())
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            return
    raise ValueError("no item " + oid)


def tick(path, oid, key, other=""):
    """Test helper: tick a box the way the user would."""
    lines = read(path).split("\n")
    for it in parse("\n".join(lines)):
        if it["id"] != oid:
            continue
        for i in range(it["start"], it["end"]):
            b = BOX.match(lines[i])
            if not b:
                continue
            if (key == "other" and b.group(3).startswith("Other:")) or b.group(2) == key:
                lines[i] = lines[i].replace("- [ ]", "- [x]", 1)
                if key == "other":
                    lines[i] += " " + other
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def self_test():
    fails = []

    def check(name, cond):
        print(("ok   " if cond else "FAIL ") + name)
        if not cond:
            fails.append(name)

    def raises(fn):
        try:
            fn()
        except ValueError:
            return True
        return False

    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "open-items.md")
        a = add(p, "Landing order", "Which first?", ["Slice 1", "Both"], context="needs header", frm="lead-a")
        b = add(p, "Merge #12?", "Merge on green?", ["Yes", "No"], kind="merge")
        c = add(p, "Note", "Anything?", ["Nothing"])
        check("ids count up", (a, b, c) == ("OI-001", "OI-002", "OI-003"))
        check("first option marked Recommended", "(a) Slice 1 (Recommended)" in read(p))
        check("nothing ticked, nothing answered", answered(p) == [])
        tick(p, a, "a")
        tick(p, c, "other", "use the old order")
        got = {x["id"]: x for x in answered(p)}
        check("a tick is an answer", got.get(a, {}).get("choice") == "a" and got[a]["from"] == "lead-a")
        check("Other keeps the user's words", got.get(c, {}).get("other") == "use the old order")
        check("an unticked item stays out", b not in got)
        close(p, a)
        check("closed item leaves answered()", a not in {x["id"] for x in answered(p)})
        check("close records the time read", re.search(r"OI-001 · answered · .* · read \d{4}-", read(p)) is not None)
        # Deliberate failures: each must be refused or reported, never passed as an answer.
        tick(p, b, "a")
        tick(p, b, "b")
        two = [x for x in answered(p) if x["id"] == b]
        check("red: two ticks is a problem, not an answer", two and "problem" in two[0])
        e = add(p, "Empty other", "?", ["x"])
        tick(p, e, "other", "")
        emp = [x for x in answered(p) if x["id"] == e]
        check("red: empty Other is a problem", emp and "problem" in emp[0])
        check("red: closing twice is refused", raises(lambda: close(p, a)))
        check("red: unknown id is refused", raises(lambda: close(p, "OI-999")))
        check("red: an item with no options is refused", raises(lambda: add(p, "t", "q", [])))
        check("red: an unknown kind is refused", raises(lambda: add(p, "t", "q", ["x"], kind="todo")))
        check("no item was ever deleted", len(parse(read(p))) == 4)
    print("%d failed" % len(fails))
    return 1 if fails else 0


def main(argv):
    if "--self-test" in argv:
        return self_test()
    ap = argparse.ArgumentParser(description="open-items file fallback")
    ap.add_argument("--file", default=DEFAULT)
    sub = ap.add_subparsers(dest="cmd", required=True)
    pa = sub.add_parser("add")
    pa.add_argument("--title", required=True)
    pa.add_argument("--question", required=True)
    pa.add_argument("--context", default="")
    pa.add_argument("--from", dest="frm", default="lead")
    pa.add_argument("--kind", default="question", choices=KINDS)
    pa.add_argument("--option", action="append", default=[])
    sub.add_parser("list")
    sub.add_parser("answered")
    pc = sub.add_parser("close")
    pc.add_argument("id")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "add":
            print(add(args.file, args.title, args.question, args.option, args.context, args.frm, args.kind))
        elif args.cmd == "list":
            for it in parse(read(args.file)):
                if it["status"] == "open":
                    print("%s  %s  (%s, from %s)" % (it["id"], it["title"], it["kind"], it["frm"]))
        elif args.cmd == "answered":
            for x in answered(args.file):
                print(json.dumps(x))
        elif args.cmd == "close":
            close(args.file, args.id)
    except ValueError as e:
        print("open-items: " + str(e), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
