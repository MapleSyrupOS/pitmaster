#!/usr/bin/env python3
"""turns.py: keep a guided townhall's turns, the user's notes and the prompt each speaker gets.

A guided townhall alternates: one debater speaks, then the user, then the next debater. This script keeps that
run's state in one folder, so the lead never rebuilds "the transcript so far" by hand and no note of the user's is
paraphrased or lost. Python 3.8+, standard library only. It never calls a model except through `send`, and only at
the address it is given.

Usage:
  turns.py init RUN --seats a,b,c --allow a,b,c,d --pack FILE [FILE ...] [--word-cap N]
  turns.py next RUN                      who speaks next (exit 3 when the round is done)
  turns.py prompt RUN SEAT --ask FILE [--inline]
                                         the full prompt for SEAT: the user's open notes (section 0, verbatim,
                                         numbered), a question asked of it, the word cap, the transcript so far,
                                         this round's ask; --inline also puts the pack's text in, for a seat that
                                         cannot open files
  turns.py add RUN SEAT FILE             record SEAT's turn (copied into RUN/turns/)
  turns.py check RUN TURN FILE           append the judge's check (FILE's text) to a recorded turn
  turns.py note RUN TEXT                 the user's note, kept verbatim as the next section-0 item
  turns.py ask RUN SEAT TEXT             the user's question for one seat, which speaks next
  turns.py pass RUN                      the user passed their turn
  turns.py seat RUN drop SEAT | add SEAT | swap OLD NEW
  turns.py advance RUN [--closing]       start the next round (or the closing round)
  turns.py log RUN                       the turn log as a Markdown table, for the record
  turns.py send RUN SEAT --url URL --model M --ask FILE --out FILE [--timeout S]
                                         post the --inline prompt to an OpenAI-wire server (a local model), write
                                         the reply to --out (any <think> block cut), and print the usage it reports
  turns.py --self-test

Exit status: 0 done, 1 refused (the reason is printed), 2 usage error, 3 the round is done (from `next`).
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import re
import pathlib
import shutil
import sys
import tempfile
import threading
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, List, Optional


class Refused(Exception):
    """A request the run's rules do not allow; printed, exit 1."""


# ---------------------------------------------------------------- state

def state_path(run: pathlib.Path) -> pathlib.Path:
    return run / "run.json"


def load(run: pathlib.Path) -> Dict[str, Any]:
    p = state_path(run)
    if not p.exists():
        raise Refused(f"no run at {run} (run init first)")
    return json.loads(p.read_text(encoding="utf-8"))


def save(run: pathlib.Path, st: Dict[str, Any]) -> None:
    tmp = state_path(run).with_suffix(".tmp")
    tmp.write_text(json.dumps(st, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(state_path(run))


def event(st: Dict[str, Any], **kw: Any) -> Dict[str, Any]:
    kw["n"] = len(st["events"]) + 1
    kw["round"] = st["round"]
    kw["label"] = round_label(st)
    st["events"].append(kw)
    return kw


def spoke_this_round(st: Dict[str, Any]) -> List[str]:
    return [e["seat"] for e in st["events"] if e["kind"] == "turn" and e["round"] == st["round"]]


def round_label(st: Dict[str, Any]) -> str:
    return "closing round" if st.get("closing") else f"round {st['round']}"


# ---------------------------------------------------------------- commands

def cmd_init(run: pathlib.Path, seats: List[str], allow: List[str], pack: List[str], word_cap: int) -> str:
    if state_path(run).exists():
        raise Refused(f"a run already exists at {run}")
    bad = [s for s in seats if s not in allow]
    if bad:
        raise Refused(f"not on the allow list: {', '.join(bad)}")
    if len(set(seats)) != len(seats):
        raise Refused("a seat is named twice")
    for f in pack:
        if not pathlib.Path(f).is_file():
            raise Refused(f"pack file not found: {f}")
    (run / "turns").mkdir(parents=True, exist_ok=True)
    st = {"seats": seats, "allow": allow, "pack": [str(pathlib.Path(f).resolve()) for f in pack],
          "word_cap": word_cap, "round": 1, "closing": False, "events": []}
    save(run, st)
    return f"run started: {len(seats)} seats, round 1"


def pending_ask(st: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    for e in st["events"]:
        if e["kind"] == "ask" and not e.get("answered") and e["seat"] in st["seats"]:
            return e
    return None


def cmd_next(st: Dict[str, Any]) -> Optional[str]:
    """The seat that speaks next, or None when every seat has spoken this round."""
    ask = pending_ask(st)
    if ask:
        return ask["seat"]
    done = spoke_this_round(st)
    for s in st["seats"]:
        if s not in done:
            return s
    return None


def open_notes(st: Dict[str, Any], seat: str) -> List[Dict[str, Any]]:
    """The user's notes this seat has not yet answered: each seat answers each note once, in its next turn."""
    return [e for e in st["events"] if e["kind"] == "note" and seat not in e["answered_by"]]


def transcript(run: pathlib.Path, st: Dict[str, Any]) -> str:
    out: List[str] = []
    for e in st["events"]:
        if e["kind"] == "turn":
            body = (run / e["file"]).read_text(encoding="utf-8").rstrip()
            out.append(f"----- {e['seat']}, {e.get('label', 'round ' + str(e['round']))} -----\n{body}")
        elif e["kind"] == "note":
            out.append(f"----- the user's note 0.{e['num']} -----\n{e['text']}")
        elif e["kind"] == "ask":
            out.append(f"----- the user asks {e['seat']} -----\n{e['text']}")
        elif e["kind"] == "seat":
            out.append(f"----- seats changed: {e['text']} -----")
    return "\n\n".join(out)


def cmd_prompt(run: pathlib.Path, st: Dict[str, Any], seat: str, ask_text: str, inline: bool) -> str:
    if seat not in st["seats"]:
        raise Refused(f"{seat} does not sit in this run")
    parts: List[str] = []
    notes = open_notes(st, seat)
    if notes:
        lines = ["## Section 0: the user's notes. Answer each first, by number, before anything else.", ""]
        for e in notes:
            lines.append(f"0.{e['num']}. \"{e['text']}\"")
        parts.append("\n".join(lines))
    ask = pending_ask(st)
    if ask and ask["seat"] == seat:
        parts.append("## The user asks you, and only you\n\n\"" + ask["text"] + "\"\n\nAnswer it before your turn.")
    parts.append(f"## This turn: {round_label(st)}\n\n{ask_text.rstrip()}")
    if st["word_cap"]:
        parts.append(f"Keep this turn under {st['word_cap']} words.")
    tx = transcript(run, st)
    parts.append("## The debate so far\n\n" + (tx if tx else "(you speak first)"))
    if inline:
        packs = [f"===== {p} =====\n{pathlib.Path(p).read_text(encoding='utf-8')}" for p in st["pack"]]
        parts.append("## The evidence pack (you cannot open files: everything you may cite is here)\n\n"
                     + "\n\n".join(packs))
    else:
        parts.append("## The evidence pack (read these files)\n\n" + "\n".join(f"- {p}" for p in st["pack"]))
    return "\n\n".join(parts) + "\n"


def cmd_add(run: pathlib.Path, st: Dict[str, Any], seat: str, src: str) -> str:
    if seat not in st["seats"]:
        raise Refused(f"{seat} does not sit in this run")
    nxt = cmd_next(st)
    if nxt is None:
        raise Refused(f"{round_label(st)} is done: advance first")
    if seat != nxt:
        raise Refused(f"{nxt} speaks next, not {seat}")
    n = len([e for e in st["events"] if e["kind"] == "turn"]) + 1
    name = f"turns/{n:02d}-r{st['round']}-{seat}.md" if not st.get("closing") else f"turns/{n:02d}-closing-{seat}.md"
    shutil.copyfile(src, run / name)
    for e in open_notes(st, seat):
        e["answered_by"].append(seat)
    ask = pending_ask(st)
    if ask and ask["seat"] == seat:
        ask["answered"] = True
    event(st, kind="turn", seat=seat, file=name)
    return name


def cmd_check(run: pathlib.Path, st: Dict[str, Any], turn: str, src: str) -> str:
    hits = [e for e in st["events"] if e["kind"] == "turn" and (e["file"] == turn or pathlib.Path(e["file"]).name == turn)]
    if not hits:
        raise Refused(f"no recorded turn {turn}")
    e = hits[-1]
    text = pathlib.Path(src).read_text(encoding="utf-8").rstrip()
    with (run / e["file"]).open("a", encoding="utf-8") as fh:
        fh.write(f"\n\n> **Judge's check:** {text}\n")
    e["checked"] = True
    return e["file"]


def cmd_seat(st: Dict[str, Any], op: str, args: List[str]) -> str:
    seats = st["seats"]
    if op == "drop" and len(args) == 1:
        if args[0] not in seats:
            raise Refused(f"{args[0]} does not sit in this run")
        if len(seats) == 1:
            raise Refused("the last seat cannot be dropped: stop the run instead")
        seats.remove(args[0])
        text = f"{args[0]} dropped"
    elif op == "add" and len(args) == 1:
        if args[0] not in st["allow"]:
            raise Refused(f"not on the allow list: {args[0]}")
        if args[0] in seats:
            raise Refused(f"{args[0]} already sits")
        seats.append(args[0])
        text = f"{args[0]} added"
    elif op == "swap" and len(args) == 2:
        old, new = args
        if old not in seats:
            raise Refused(f"{old} does not sit in this run")
        if new not in st["allow"]:
            raise Refused(f"not on the allow list: {new}")
        if new in seats:
            raise Refused(f"{new} already sits")
        seats[seats.index(old)] = new
        text = f"{old} swapped for {new}"
    else:
        raise Refused("seat takes: drop SEAT | add SEAT | swap OLD NEW")
    event(st, kind="seat", text=text)
    return text


def cmd_advance(st: Dict[str, Any], closing: bool) -> str:
    left = [s for s in st["seats"] if s not in spoke_this_round(st)]
    if left and not closing:
        raise Refused(f"{round_label(st)} is not done: {', '.join(left)} still to speak")
    if st.get("closing"):
        raise Refused("the closing round is the last one")
    st["round"] += 1
    st["closing"] = closing
    return round_label(st)


def cell(text: str) -> str:
    """Text safe inside one Markdown table cell: a pipe or a line break would split the row."""
    return text.replace("\\", "\\\\").replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def cmd_log(st: Dict[str, Any]) -> str:
    rows = ["| # | round | who | what | where |", "|---|---|---|---|---|"]
    for e in st["events"]:
        r = e.get("label", "round " + str(e["round"]))
        if e["kind"] == "turn":
            what = "turn" + (", judge's check appended" if e.get("checked") else "")
            rows.append(f"| {e['n']} | {r} | {e['seat']} | {what} | `{e['file']}` |")
        elif e["kind"] == "note":
            rows.append(f"| {e['n']} | {r} | the user | note 0.{e['num']}: \"{cell(e['text'])}\" | section 0 |")
        elif e["kind"] == "ask":
            rows.append(f"| {e['n']} | {r} | the user | asked {e['seat']}: \"{cell(e['text'])}\" | next turn |")
        elif e["kind"] == "pass":
            rows.append(f"| {e['n']} | {r} | the user | passed | |")
        elif e["kind"] == "seat":
            rows.append(f"| {e['n']} | {r} | the user | {e['text']} | |")
    return "\n".join(rows)


def strip_think(text: str) -> str:
    return text.split("</think>", 1)[1].strip() if "</think>" in text else text.strip()


def cmd_send(run: pathlib.Path, st: Dict[str, Any], seat: str, url: str, model: str, ask_text: str,
             out: str, timeout: float) -> str:
    prompt = cmd_prompt(run, st, seat, ask_text, inline=True)
    sysmsg = ("You are a debater in a townhall. You cannot open files: everything you may cite is in the message. "
              "Cite the inline document's name for every factual claim, mark estimates, and say when you could not "
              "check something.")
    body = {"model": model, "messages": [{"role": "system", "content": sysmsg}, {"role": "user", "content": prompt}]}
    req = urllib.request.Request(url.rstrip("/") + "/v1/chat/completions", json.dumps(body).encode(),
                                 {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        r = json.load(resp)
    text = strip_think(r["choices"][0]["message"].get("content") or "")
    pathlib.Path(out).write_text(text + "\n", encoding="utf-8")
    return f"{seat}: reply in {out}; usage {json.dumps(r.get('usage'))}"


# ---------------------------------------------------------------- CLI

def main(argv: List[str]) -> int:
    if argv[:1] == ["--self-test"]:
        return self_test()
    ap = argparse.ArgumentParser(prog="turns.py", description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init"); p.add_argument("run"); p.add_argument("--seats", required=True)
    p.add_argument("--allow", required=True); p.add_argument("--pack", nargs="+", required=True)
    p.add_argument("--word-cap", type=int, default=0)
    p = sub.add_parser("next"); p.add_argument("run")
    p = sub.add_parser("prompt"); p.add_argument("run"); p.add_argument("seat"); p.add_argument("--ask", required=True)
    p.add_argument("--inline", action="store_true")
    p = sub.add_parser("add"); p.add_argument("run"); p.add_argument("seat"); p.add_argument("file")
    p = sub.add_parser("check"); p.add_argument("run"); p.add_argument("turn"); p.add_argument("file")
    p = sub.add_parser("note"); p.add_argument("run"); p.add_argument("text")
    p = sub.add_parser("ask"); p.add_argument("run"); p.add_argument("seat"); p.add_argument("text")
    p = sub.add_parser("pass"); p.add_argument("run")
    p = sub.add_parser("seat"); p.add_argument("run"); p.add_argument("op"); p.add_argument("args", nargs="+")
    p = sub.add_parser("advance"); p.add_argument("run"); p.add_argument("--closing", action="store_true")
    p = sub.add_parser("log"); p.add_argument("run")
    p = sub.add_parser("send"); p.add_argument("run"); p.add_argument("seat"); p.add_argument("--url", required=True)
    p.add_argument("--model", required=True); p.add_argument("--ask", required=True); p.add_argument("--out", required=True)
    p.add_argument("--timeout", type=float, default=1500)
    a = ap.parse_args(argv)
    run = pathlib.Path(a.run)
    try:
        if a.cmd == "init":
            print(cmd_init(run, a.seats.split(","), a.allow.split(","), a.pack, a.word_cap))
            return 0
        st = load(run)
        if a.cmd == "next":
            nxt = cmd_next(st)
            if nxt is None:
                print(f"{round_label(st)} is done")
                return 3
            print(nxt)
            return 0
        if a.cmd == "prompt":
            sys.stdout.write(cmd_prompt(run, st, a.seat, pathlib.Path(a.ask).read_text(encoding="utf-8"), a.inline))
            return 0
        if a.cmd == "log":
            print(cmd_log(st))
            return 0
        if a.cmd == "send":
            print(cmd_send(run, st, a.seat, a.url, a.model, pathlib.Path(a.ask).read_text(encoding="utf-8"),
                           a.out, a.timeout))
            return 0
        if a.cmd == "add":
            msg = cmd_add(run, st, a.seat, a.file)
        elif a.cmd == "check":
            msg = cmd_check(run, st, a.turn, a.file)
        elif a.cmd == "note":
            num = len([e for e in st["events"] if e["kind"] == "note"]) + 1
            event(st, kind="note", num=num, text=a.text, answered_by=[])
            msg = f"note 0.{num} kept verbatim"
        elif a.cmd == "ask":
            if a.seat not in st["seats"]:
                raise Refused(f"{a.seat} does not sit in this run")
            if pending_ask(st):
                raise Refused("a question is already waiting for its answer")
            event(st, kind="ask", seat=a.seat, text=a.text, answered=False)
            msg = f"{a.seat} speaks next"
        elif a.cmd == "pass":
            event(st, kind="pass")
            msg = "passed"
        elif a.cmd == "seat":
            msg = cmd_seat(st, a.op, a.args)
        elif a.cmd == "advance":
            msg = cmd_advance(st, a.closing)
        else:  # pragma: no cover
            return 2
        save(run, st)
        print(msg)
        return 0
    except Refused as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 1


# ---------------------------------------------------------------- self-test

def self_test() -> int:
    fails: List[str] = []

    def expect(name: str, cond: bool) -> bool:
        if not cond:
            fails.append(name)
        return cond

    def refuses(name: str, fn: Any, *a: Any) -> None:
        try:
            fn(*a)
        except Refused:
            return
        fails.append(name + " (not refused)")

    # Red arms first: the instruments must be able to fail, or their greens mean nothing.
    before = len(fails)
    expect("red: expect", False)
    refuses("red: refuses", lambda: None)
    red_ok = len(fails) == before + 2
    del fails[before:]
    if not red_ok:
        print("self-test: FAIL (the red arms did not go red)")
        return 1

    tmp = pathlib.Path(tempfile.mkdtemp(prefix="turns-selftest-"))
    try:
        pack = tmp / "evidence.md"
        pack.write_text("EVIDENCE-LINE-42\n", encoding="utf-8")
        ask = "Make your opening case."
        run = tmp / "run"
        cmd_init(run, ["codex", "s35", "sonnet"], ["codex", "s35", "sonnet", "gemma"], [str(pack)], 600)
        refuses("init twice", cmd_init, run, ["codex"], ["codex"], [str(pack)], 0)
        refuses("init off-list", cmd_init, tmp / "r2", ["agy"], ["codex"], [str(pack)], 0)
        refuses("init missing pack", cmd_init, tmp / "r3", ["codex"], ["codex"], [str(tmp / "nope")], 0)
        st = load(run)
        expect("first speaker", cmd_next(st) == "codex")
        refuses("out of turn", cmd_add, run, st, "s35", str(pack))

        t = tmp / "t.md"
        t.write_text("Codex opening. Cites evidence.md line 1.\n", encoding="utf-8")
        cmd_add(run, st, "codex", str(t))
        expect("second speaker", cmd_next(st) == "s35")

        # The user's note: verbatim, numbered, owed by every seat once.
        note = "Maybe trying lower codex tiers | is the compromise?\nIsn't it?"
        event(st, kind="note", num=1, text=note, answered_by=[])
        p = cmd_prompt(run, st, "s35", ask, inline=True)
        expect("note verbatim", f'0.1. "{note}"' in p)
        expect("note before transcript", p.index("Section 0") < p.index("The debate so far"))
        expect("earlier turn visible", "Codex opening." in p)
        expect("inline pack text", "EVIDENCE-LINE-42" in p)
        expect("word cap", "under 600 words" in p)
        p2 = cmd_prompt(run, st, "sonnet", ask, inline=False)
        expect("pack by path only", "EVIDENCE-LINE-42" not in p2 and str(pack.resolve()) in p2)
        expect("codex owes note too", any(e["num"] == 1 for e in open_notes(st, "codex")))

        cmd_add(run, st, "s35", str(t))
        expect("note answered by s35", not open_notes(st, "s35"))
        expect("note still open for sonnet", bool(open_notes(st, "sonnet")))

        # Ask one seat: it jumps the order, even a seat that already spoke this round.
        event(st, kind="ask", seat="codex", text="Which pin did the sizing miss?", answered=False)
        expect("asked seat next", cmd_next(st) == "codex")
        pa = cmd_prompt(run, st, "codex", ask, inline=False)
        expect("question shown to asked seat", "only you" in pa and "Which pin" in pa)
        expect("question not shown as own to others", "only you" not in cmd_prompt(run, st, "sonnet", ask, False))
        cmd_add(run, st, "codex", str(t))
        expect("ask answered", pending_ask(st) is None and cmd_next(st) == "sonnet")

        refuses("advance early", cmd_advance, st, False)
        cmd_add(run, st, "sonnet", str(t))
        expect("round done", cmd_next(st) is None)
        refuses("add after round done", cmd_add, run, st, "codex", str(t))

        # Judge's check is appended to the turn and shown to later speakers.
        chk = tmp / "chk.md"
        chk.write_text("line 1 says otherwise (checked).", encoding="utf-8")
        f = cmd_check(run, st, "02-r1-s35.md", str(chk))
        expect("check appended", "Judge's check" in (run / f).read_text(encoding="utf-8"))
        refuses("check unknown turn", cmd_check, run, st, "99-r1-x.md", str(chk))

        # Seats: allow list only; never the last seat.
        refuses("add off-list", cmd_seat, st, "add", ["agy"])
        refuses("swap to off-list", cmd_seat, st, "swap", ["s35", "agy"])
        refuses("drop absent", cmd_seat, st, "drop", ["agy"])
        cmd_seat(st, "swap", ["s35", "gemma"])
        expect("swap kept order", st["seats"] == ["codex", "gemma", "sonnet"])
        # A seat swapped in mid-round has not been heard: it speaks this round, and owes the open notes.
        expect("newcomer speaks this round", cmd_next(st) == "gemma")
        expect("new seat owes the note", bool(open_notes(st, "gemma")))
        refuses("advance before newcomer", cmd_advance, st, False)
        cmd_add(run, st, "gemma", str(t))

        cmd_advance(st, False)
        expect("round 2", st["round"] == 2 and cmd_next(st) == "codex")
        cmd_add(run, st, "codex", str(t)); cmd_add(run, st, "gemma", str(t)); cmd_add(run, st, "sonnet", str(t))
        cmd_advance(st, True)
        expect("closing label", round_label(st) == "closing round")
        refuses("past closing", lambda: (cmd_add(run, st, "codex", str(t)), cmd_add(run, st, "gemma", str(t)),
                                         cmd_add(run, st, "sonnet", str(t)), cmd_advance(st, False)))
        lg = cmd_log(st)
        expect("log quotes note", 'note 0.1: "Maybe trying lower codex tiers \\| is the compromise? Isn\'t it?"' in lg)
        expect("log marks check", "judge's check appended" in lg)
        expect("log is a table", lg.splitlines()[1].startswith("|---"))
        expect("log rows keep 5 cells", all(len(re.split(r"(?<!\\)\|", ln)) == 7 for ln in lg.splitlines()))
        expect("log one round word", "| 1 |" not in lg.replace("| 1 | round", ""))
        save(run, st)
        expect("state round-trips", load(run)["seats"] == ["codex", "gemma", "sonnet"])

        # send: against a stub OpenAI-wire server; the <think> block is cut, the usage printed.
        got: Dict[str, Any] = {}

        class Stub(BaseHTTPRequestHandler):
            def do_POST(self) -> None:  # noqa: N802
                got["body"] = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                out = {"choices": [{"message": {"content": "<think>hidden</think>Visible turn."}}],
                       "usage": {"prompt_tokens": 7, "completion_tokens": 2}}
                data = json.dumps(out).encode()
                self.send_response(200); self.send_header("Content-Length", str(len(data))); self.end_headers()
                self.wfile.write(data)

            def log_message(self, *a: Any) -> None:
                pass

        srv = HTTPServer(("127.0.0.1", 0), Stub)
        th = threading.Thread(target=srv.handle_request, daemon=True); th.start()
        out = tmp / "reply.md"
        msg = cmd_send(run, st, "gemma", f"http://127.0.0.1:{srv.server_address[1]}", "m", ask, str(out), 10)
        th.join(5); srv.server_close()
        expect("send stripped think", out.read_text(encoding="utf-8") == "Visible turn.\n")
        expect("send printed usage", '"prompt_tokens": 7' in msg)
        expect("send was inline", "EVIDENCE-LINE-42" in got["body"]["messages"][1]["content"])

        # CLI: exit codes.
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            expect("cli next done -> 3", main(["next", str(run)]) == 3)
            expect("cli refusal -> 1", main(["seat", str(run), "add", "agy"]) == 1)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if fails:
        print("self-test: FAIL")
        for f in fails:
            print("  -", f)
        return 1
    print("self-test: PASS (2 red arms went red; all arms green)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
