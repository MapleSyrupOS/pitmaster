#!/usr/bin/env python3
"""adr-yaml.py -- the ADR+ YAML header: converter and lossless proof (ADR+ release 0.1.0).

SPEC.md 1.3 puts an ADR's header in a YAML block at the top of the file, checked
against `schema/adr-plus.schema.json`. This tool moves older headers into that
shape and proves that nothing was lost. It writes no ADR unless told to: it prints
a converted file, or converts all of them in memory and judges the result.

  --convert FILE   Print FILE converted to stdout, warnings to stderr.
  --dry-run [--report PATH]
                   Convert every ADR in the decisions and archive folders in
                   memory, prove each, and write a report (default
                   adr-yaml-dry-run.md in the root). Writes nothing else.
  --prove          Convert every ADR in memory and prove each lossless. Prints one
                   PASS line, or FAIL lines naming the ADR file and the value
                   lost; exit 1 on any failure.
  --validate FILE...
                   Check the YAML header of each file against the schema.
  --apply          Write the converted file over every bold-line ADR, in both
                   folders. Every conversion is proved first and nothing is
                   written unless all of them prove. A file that already has a
                   YAML header is left alone, so a second run changes nothing.
  --prove-against REV
                   For every ADR now holding a YAML header, take its old text from
                   `git show REV:<path>` and run the proof between the two. Exit 1
                   naming any ADR that fails, and any ADR still in bold lines.
  --check          The standing check once the tree is YAML: every ADR in both
                   folders has a YAML header that parses and passes the schema, and
                   no line beginning `**Status:**`, `**Built:**`, `**Kind:**` or
                   `**Supersedes:**` is left above the first `## ` heading.
  --self-test      The fixtures in tools/fixtures/adr-yaml/ (EXPECTED.md names the
                   verdict of each), the parser and emitter, the validator, the
                   shared reader, --apply, --check and --prove-against on a scratch
                   tree, and the red arms. One line per arm; exit 1 on any failure.

Settings. The tools read the project's values from the decisions folder's README.md,
a table with one setting per row (SPEC.md 4.2):

  | Owner          | Alex                  |   written into every converted ADR
  | Archive folder | docs/archive/adrs     |   `none` (the default) when there is no archive

and the command line wins over the README: `--root DIR` (default: the current
directory), `--dir PATH` (the decisions folder, relative to the root; default: the
first of docs/decisions, docs/adr, docs/adrs, doc/adr, doc/decisions, adr, decisions
that exists), `--archive PATH` (or `none`), `--owner NAME` and `--schema FILE`
(default: the schema shipped beside these tools, or `adr-plus.schema.json` in the
decisions folder when the project keeps its own copy).

What the converter reads. Three shapes, each moved without invention:
  * the bold-line ADR+ header: the lines that BEGIN with `**Status:**` (the whole
    paragraph, which ends at a blank line, at the next `**Word:**` field line or at a
    heading or rule), `**Built:**`, `**Kind:**` and the `**Supersedes:** ...
    **Amends:** ...` line move into YAML. Every other line stays where it is,
    including a later line that carries `**Status:**` after another field (reported
    as kept-in-body:status). The Status paragraph also ends at the first later line
    that begins with a bold `**Label:**` (a label ending in a colon, as in
    `**Amended 2026-10-12:**`). Such a line standing between two of the four moved
    lines (`**Owner:**` between Kind and Supersedes, a dated note between Status and
    Built) stays in the body, in the place the Status line was, and is reported as
    kept-in-body:label; the proof fails if a header line of that shape other than
    the four moved fields is missing from the body;
  * MADR 4.0 (front matter `status`, `date`, `decision-makers`, `consulted`,
    `informed`);
  * classic Nygard (a `## Status` section holding a word).
`owner` comes from the settings. A field the source does not hold is left out and
reported as a warning; nothing is guessed.

How a Status paragraph is split. `status` is one of seven words (proposed,
provisional, accepted, partially accepted, superseded, withdrawn, rejected).
`status-note` holds the rest of the wording, with the paragraph's line breaks
joined by one space:
  * an older verdict is mapped (ratified, adopted, ruled, landed -> accepted;
    deprecated, retired, closed -> withdrawn; nixed -> rejected; draft,
    awaiting -> proposed) and reported as verdict-mapped. The note then holds
    the whole wording from the old verdict on, exactly as written: the old word
    in its own case, then the separator and the rest, so a note that leads with
    one of those words is the Status wording verbatim and is rendered as it
    stands. When an unmapped verdict is followed by ` — ` and then by one of
    those words (`ACCEPTED — RATIFIED BY ALEX ...`), the note starts with the
    dash and a space (`— RATIFIED BY ALEX ...`) so the two readings differ;
  * a glyph or bold mark that stood before the verdict (`✅ `, `**`) is the
    start of the note, kept in front of the text, one space after a glyph;
  * the separator ` — ` after the verdict is not written; any other separator is
    kept: a note that begins with a space is the text exactly as it followed the
    verdict, and a note that begins with a backslash is that text without the
    backslash.
The proof re-renders the moved lines from the YAML alone and compares them with
the originals; an unmapped verdict is compared without case, everything else byte
for byte.

The red arm. ADRPLUS_PLANT=drop:<ADR-NNN>:<field> makes the converter drop that
field's value for that one ADR; --prove must then fail naming the file and the
field. Under --check the same variable drops the field from that ADR's parsed
header, and the schema names it missing.

The parser, the schema validator, the settings and the field list live in
adrplus.py, the one reader every tool uses; this file adds the converter and the
proof. Standard library only (Python 3.8 or later); PyYAML and jsonschema, when
importable, are a second instrument over the same headers.
"""
from __future__ import annotations

import argparse
import datetime
import importlib
import importlib.util
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, cast

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import adrplus  # noqa: E402
from adrplus import (  # noqa: E402
    FIELD_ORDER, KINDS, PREFIX_TOKEN, STATUS_WORDS, VERDICT_MAP, HeaderError, YamlError, adr_paths,
    as_dict, built_rest, configure, consume_prefix, decode_status, front_matter, header, is_yaml,
    load_schema, mapped_lead, needs_quotes, parse_flat, parse_header, render_header, s2_status,
    scalar, settings, settings_owner, split_header, status_wording, type_name, validate, word_regex)

TOOLS = pathlib.Path(__file__).resolve().parent
PACKAGE = TOOLS.parent
FIXTURES = TOOLS / "fixtures" / "adr-yaml"
REPORT_NAME = "adr-yaml-dry-run.md"

BUILT_WORDS: Tuple[str, ...] = ("NOT STARTED", "PARTIAL", "LANDED", "N/A")
# Statuses whose wording is expected to say who ratified and when.
EXPECT_RATIFIED = frozenset(("accepted", "partially accepted"))
# The suffix of a Built line that names what is still missing.
OWED_MARK = "; owed:"

STATUS_PREFIX = "**Status:** "
BUILT_PREFIX = "**Built:** "
KIND_PREFIX = "**Kind:** "
SUPERSEDES_PREFIX = "**Supersedes:** "
AMENDS_MARK = " **Amends:** "
ADR_TITLE = re.compile(r"^# (ADR-\d+)")
ADR_REF = re.compile(r"ADR-[0-9]+")
ADR_NAME = re.compile(r"^(ADR-\d+)")
_LATER_STATUS = re.compile(r"(?<![`\w])\*\*Status:\*\*")
RATIFIED_RE = re.compile(r"ratified by ([A-Za-z]+) (\d{4}-\d{2}-\d{2})", re.IGNORECASE)
CLASSIC_STATUS = re.compile(r"^## Status\s*$")


# ------------------------------------------------------------ header lines


def verdict_words() -> List[str]:
    """The verdicts the converter recognises: the seven status words and the older
    words the S2 map rewrites."""
    return list(STATUS_WORDS) + list(VERDICT_MAP)


# A Status paragraph ends at a blank line, or earlier at the next `**Word:**`
# field line (a single capitalised word before the colon, so a wrapped sentence
# that continues on a bold run is not mistaken for a field) or at a heading or
# horizontal rule.
FIELD_LINE = re.compile(r"^\*{0,2}[A-Z][A-Za-z]{2,15}:\*{0,2}(\s|$)")
NEW_BLOCK = re.compile(r"^(#|---)")


def status_paragraph_end(lines: List[str], status_idx: int) -> int:
    """Index of the last line of the `**Status:**` paragraph that starts at
    `status_idx`. `lines` must not contain the `**Built:**` line, which is itself
    a field line."""
    end = status_idx
    j = status_idx + 1
    while j < len(lines):
        line = lines[j]
        if not line.strip():
            break
        if FIELD_LINE.match(line) or NEW_BLOCK.match(line):
            break
        end = j
        j += 1
    return end


# A line that begins with a bold label ending in a colon (`**Amended <date>:**`,
# `**Date:**`) starts a new field, so it ends the Status paragraph for moving
# purposes even when FIELD_LINE (a plain word before the colon) does not see it as
# one. The module switch exists so the self-test can show the absorbing behaviour
# is caught.
LABEL_LINE = re.compile(r"^\*\*[^*]{1,80}:\*\*")
LABEL_ENDS_STATUS = True
MOVED_PREFIXES = (STATUS_PREFIX, BUILT_PREFIX, KIND_PREFIX, SUPERSEDES_PREFIX)


def status_last_line(lines: List[str], status_idx: int) -> int:
    """Index of the last line of the Status paragraph that starts at `status_idx`:
    where status_paragraph_end ends it, or just before the first later line that
    begins with a bold `**Label:**`."""
    e = status_paragraph_end(lines, status_idx)
    if LABEL_ENDS_STATUS:
        for i in range(status_idx + 1, e + 1):
            if LABEL_LINE.match(lines[i]):
                return i - 1
    return e


def split_owed(rest: str) -> Tuple[str, str, bool]:
    """(evidence half, owed half, whether `; owed:` was present)."""
    head, sep, tail = rest.partition(OWED_MARK)
    return head, tail, bool(sep)


def heading_indices(lines: Sequence[str]) -> List[int]:
    """Indices of `## ` headings that are not inside a code fence."""
    found: List[int] = []
    fenced = False
    for i, line in enumerate(lines):
        if line.startswith("```"):
            fenced = not fenced
        elif not fenced and line.startswith("## "):
            found.append(i)
    return found


def header_end(lines: Sequence[str]) -> int:
    """Index of the first `## ` heading outside a code fence: where the header block ends."""
    heads = heading_indices(lines)
    return heads[0] if heads else len(lines)


# ----------------------------------------------------------- data classes


@dataclass
class Warn:
    kind: str
    detail: str


@dataclass
class Conversion:
    adr: str
    shape: str
    fields: Dict[str, str] = field(default_factory=dict)
    out: str = ""
    warnings: List[Warn] = field(default_factory=list)
    span: Tuple[int, int] = (0, 0)
    kept: List[Tuple[int, int]] = field(default_factory=list)
    dropped_blank: bool = False
    inserted: List[str] = field(default_factory=list)
    unparseable: str = ""


@dataclass
class Failure:
    field: str
    message: str


def schema_drift(schema: Dict[str, object]) -> List[str]:
    """Where the schema disagrees with the tool: the verdict list, the field
    order and the required set."""
    problems: List[str] = []
    props = as_dict(schema["properties"])
    if list(props.keys()) != list(FIELD_ORDER):
        problems.append(f"schema field order {list(props.keys())} is not {list(FIELD_ORDER)}")
    status = as_dict(props["status"])
    got = [str(w) for w in cast(List[object], status["enum"])]
    if got != list(STATUS_WORDS):
        problems.append(f"schema status enum {got} is not the seven words {list(STATUS_WORDS)}")
    kind = as_dict(props["kind"])
    if list(cast(List[str], kind["enum"])) != list(KINDS):
        problems.append("schema kind enum differs from the three kinds")
    return problems


# ------------------------------------------------------------ the second instrument


def second_instrument() -> Optional[Tuple[Any, Any]]:
    """(yaml module, jsonschema module) when both import, else None."""
    try:
        return importlib.import_module("yaml"), importlib.import_module("jsonschema")
    except ImportError:
        return None


def second_check(header_text: str, ours: Dict[str, object], schema: Dict[str, object],
                 tools: Tuple[Any, Any]) -> List[Failure]:
    yaml, jsonschema = tools
    fails: List[Failure] = []
    try:
        theirs = yaml.safe_load(header_text)
    except Exception as exc:  # PyYAML raises its own family
        return [Failure("header", f"second instrument: PyYAML cannot load the header: {str(exc).splitlines()[0]}")]
    if not isinstance(theirs, dict):
        return [Failure("header", "second instrument: PyYAML did not load a mapping")]
    for k, v in theirs.items():
        if not isinstance(v, str):
            fails.append(Failure(str(k), f"second instrument: {k} loads as {type_name(v)}, not a string"))
    if not fails and theirs != ours:
        for k in sorted(set(theirs) | set(ours)):
            if theirs.get(k) != ours.get(k):
                fails.append(Failure(str(k), f"second instrument: {k} loads differently from the tool's own parse"))
    validator = jsonschema.Draft202012Validator(schema)
    for err in validator.iter_errors(theirs):
        loc = ".".join(str(p) for p in err.absolute_path) or "(header)"
        fails.append(Failure(loc, f"second instrument: jsonschema: {err.message}"))
    return fails


# ------------------------------------------------------------ settings, plant


def plant_spec() -> Optional[Tuple[str, str]]:
    """(ADR id, field) from ADRPLUS_PLANT=drop:<ADR-NNN>:<field>."""
    raw = os.environ.get("ADRPLUS_PLANT", "")
    if not raw:
        return None
    parts = raw.split(":")
    if len(parts) != 3 or parts[0] != "drop" or parts[2] not in FIELD_ORDER:
        raise SystemExit(f"ADRPLUS_PLANT must be drop:<ADR-NNN>:<field>, got {raw!r}")
    return parts[1], parts[2]


def adr_id(text: str, name: str = "") -> str:
    first = text.split("\n", 1)[0]
    m = ADR_TITLE.match(first)
    if m is not None:
        return m.group(1)
    m = ADR_NAME.match(name)
    if m is not None:
        return m.group(1)
    for line in text.split("\n"):
        m = ADR_TITLE.match(line)
        if m is not None:
            return m.group(1)
    return "ADR-???"


# ------------------------------------------------------------ status codec


def _verdict_regex() -> "re.Pattern[str]":
    """Every verdict the project has used, plus the older words the S2 map knows."""
    words = [w.lower() for w in verdict_words()] + list(STATUS_WORDS) + list(VERDICT_MAP)
    return word_regex(sorted(set(words)))


def encode_status(text: str) -> Optional[Tuple[str, str, List[Warn]]]:
    """(verdict lowercased, status-note, warnings) for the Status wording that
    follows `**Status:** `, or None when no verdict stands at its start."""
    prefix, rest = consume_prefix(text)
    m = _verdict_regex().match(rest)
    if m is None:
        return None
    word = m.group(1)
    verdict = word.lower()
    tail = rest[m.end():]
    warns: List[Warn] = []
    if "✅" in prefix or "⚑" in prefix:
        warns.append(Warn("glyph-before-verdict", f"`{prefix}` stands before the verdict; kept at the start of status-note"))
    if "**" in prefix:
        warns.append(Warn("bold-before-verdict", "a bold mark stands before the verdict; kept at the start of status-note"))
    if verdict in VERDICT_MAP:
        mapped = VERDICT_MAP[verdict]
        warns.append(Warn("verdict-mapped", f"{verdict} -> {mapped}; the original wording stays word for word at the start of status-note"))
        return mapped, prefix + word + tail, warns
    if tail == "":
        body = ""
    elif tail.startswith(" — ") and len(tail) > 3:
        r = tail[3:]
        if r[0].isspace() or r[0] == "\\" or r[0] == "—" or PREFIX_TOKEN.match(r) is not None:
            body = tail
            warns.append(Warn("separator-kept", "the text after the verdict is kept with its separator"))
        elif mapped_lead(r) is not None:
            body = "— " + r
        else:
            body = r
    elif tail[0].isspace():
        body = tail
        warns.append(Warn("separator-not-dash", f"the verdict is followed by {tail[:4]!r}, not ' — '; kept with its separator"))
    else:
        body = "\\" + tail
        warns.append(Warn("separator-not-dash", f"the verdict is followed by {tail[:4]!r}, not ' — '; kept with its separator"))
    return verdict, prefix + body, warns


# ------------------------------------------------------------ the converter


def _cut_blank_rule(rest: List[str], cut: int) -> Tuple[List[str], bool]:
    """`rest` is a file with its moved lines cut out at index `cut`. When that
    leaves two blank lines together, the second is dropped. The second value says
    whether one was."""
    if 0 < cut < len(rest) and rest[cut - 1] == "" and rest[cut] == "":
        return rest[:cut] + rest[cut + 1:], True
    return rest, False


def _next_moved(lines: List[str], start: int, end: int, accept: Callable[[str], bool]) -> Optional[int]:
    """Index of the first line at or after `start` that `accept` takes, when only
    bold label lines that are not moved fields (which stay in the body) stand
    before it inside the header block; None otherwise."""
    k = start
    while k < end and LABEL_LINE.match(lines[k]) and not lines[k].startswith(MOVED_PREFIXES):
        k += 1
    if k < len(lines) and accept(lines[k]):
        return k
    return None


def _lineage(line: str) -> Optional[Tuple[str, str]]:
    if not line.startswith(SUPERSEDES_PREFIX) or AMENDS_MARK not in line:
        return None
    cut = line.index(AMENDS_MARK)
    left = line[len(SUPERSEDES_PREFIX):cut]
    right = line[cut + len(AMENDS_MARK):]
    if not (left.endswith(".") and right.endswith(".")):
        return None
    return left[:-1], right[:-1]


def _finish(conv: Conversion, body_lines: List[str], plant: Optional[Tuple[str, str]]) -> Conversion:
    if plant is not None and plant[0] == conv.adr:
        conv.fields.pop(plant[1], None)
    ordered = {k: conv.fields[k] for k in FIELD_ORDER if k in conv.fields}
    conv.fields = ordered
    conv.out = render_header(ordered) + "\n".join(body_lines)
    return conv


def _missing_warnings(conv: Conversion) -> None:
    for name in ("kind", "built", "supersedes", "amends"):
        if name not in conv.fields:
            conv.warnings.append(Warn(f"missing:{name}", f"the source holds no {name} to move"))
    if conv.fields.get("built") in ("landed", "partial", "n/a") and "proof" not in conv.fields:
        conv.warnings.append(Warn("missing:proof", "the source names no proof"))
    if conv.fields.get("built") == "partial" and "owed" not in conv.fields:
        conv.warnings.append(Warn("missing:owed", "a partial decision names nothing owed"))


def _convert_bold(text: str, lines: List[str], owner: str, plant: Optional[Tuple[str, str]],
                  name: str) -> Conversion:
    conv = Conversion(adr_id(text, name), "bold")
    end = header_end(lines)
    status_at = [i for i in range(end) if lines[i].startswith("**Status:**")]
    if not status_at:
        conv.unparseable = "no **Status:** line in the header block"
        return conv
    s = status_at[0]
    if not lines[s].startswith(STATUS_PREFIX):
        conv.unparseable = "the **Status:** line has no single space after the bold label"
        return conv
    builts = [i for i in range(end) if lines[i].startswith("**Built:**")]
    if len(builts) > 1:
        conv.unparseable = "more than one **Built:** line in the header block"
        return conv
    if builts:
        b = builts[0]
        if b < s:
            conv.unparseable = "the **Built:** line stands above the **Status:** line"
            return conv
        e = status_last_line(lines[:b], s)
        if e != b - 1:
            mid = lines[e + 1:b]
            if not all(LABEL_LINE.match(l) and not l.startswith(MOVED_PREFIXES) for l in mid):
                conv.unparseable = "the **Built:** line is not directly below the Status paragraph"
                return conv
            conv.kept.append((e + 1, b))
        pos = b + 1
    else:
        e = status_last_line(lines, s)
        pos = e + 1
    joined = " ".join(lines[s:e + 1])
    enc = encode_status(joined[len(STATUS_PREFIX):])
    if enc is None:
        conv.unparseable = "no verdict word stands at the start of the Status wording"
        return conv
    verdict, note, warns = enc
    conv.warnings.extend(warns)
    fields = conv.fields
    fields["status"] = verdict
    if note != "":
        fields["status-note"] = note
    ratified = RATIFIED_RE.search(joined)
    if ratified is not None and verdict != "proposed":
        try:
            datetime.date.fromisoformat(ratified.group(2))
            fields["ratified-by"] = ratified.group(1)
            fields["ratified-on"] = ratified.group(2)
        except ValueError:
            ratified = None
    if "ratified-by" not in fields and verdict in EXPECT_RATIFIED:
        conv.warnings.append(Warn("unparsed:ratified", "the Status wording names no ratifier and date in a shape the converter recognises"))
    fields["owner"] = owner
    conv.warnings.append(Warn("owner-from-settings", f"owner {owner} comes from the settings table"))
    if builts:
        built_line = lines[b]
        if not built_line.startswith(BUILT_PREFIX):
            conv.unparseable = "the **Built:** line has no single space after the bold label"
            return conv
        value_text = built_line[len(BUILT_PREFIX):]
        word = next((w for w in BUILT_WORDS if value_text.startswith(w + " — ")), None)
        if word is None:
            conv.unparseable = "the **Built:** line is not `<VALUE> — <text>`"
            return conv
        body = value_text[len(word) + 3:]
        head, owed, had_owed = split_owed(body)
        fields["built"] = word.lower()
        if had_owed:
            if not owed.startswith(" ") or owed.startswith("  ") or owed.strip() == "" or head == "":
                conv.unparseable = "the `; owed:` clause is not `; owed: <text>` with text on both sides"
                return conv
            fields["proof"] = head
            fields["owed"] = owed[1:]
        elif body != "":
            fields["proof"] = body
        else:
            conv.unparseable = "the **Built:** line has no text after the value"
            return conv
    else:
        conv.warnings.append(Warn("missing:built", "no **Built:** line"))
    k = _next_moved(lines, pos, end, lambda l: l.startswith(KIND_PREFIX))
    if k is not None:
        if k > pos:
            conv.kept.append((pos, k))
        fields["kind"] = lines[k][len(KIND_PREFIX):]
        pos = k + 1
    k = _next_moved(lines, pos, end, lambda l: _lineage(l) is not None)
    if k is not None:
        lin = _lineage(lines[k])
        assert lin is not None
        if k > pos:
            conv.kept.append((pos, k))
        fields["supersedes"], fields["amends"] = lin
        pos = k + 1
    _missing_warnings(conv)
    for name in ("supersedes", "amends"):
        value = fields.get(name)
        if value is not None and value != "nothing" and ADR_REF.search(value) is None:
            conv.warnings.append(Warn("lineage-names-no-adr", f"{name} is neither `nothing` nor names an ADR-NNN"))
    for i in range(end):
        if s <= i < pos:
            continue
        if lines[i].startswith("**") and _LATER_STATUS.search(lines[i]):
            conv.warnings.append(Warn("kept-in-body:status", f"line {i + 1} carries `**Status:**` after another field and stays in the body"))
    kept_lines = [l for a, z in conv.kept for l in lines[a:z]]
    for l in kept_lines:
        conv.warnings.append(Warn("kept-in-body:label", f"`{l[:50]}` stands among the moved header lines and stays in the body"))
    body_lines, dropped = _cut_blank_rule(lines[:s] + kept_lines + lines[pos:], s + len(kept_lines))
    conv.span = (s, pos)
    conv.dropped_blank = dropped
    return _finish(conv, body_lines, plant)


MADR_KEYS = ("status", "date", "decision-makers", "consulted", "informed")
ADRPLUS_SECTIONS = ("Decision", "Context", "Alternatives", "Consequences")
MADR_HEADINGS = {
    "Decision": "Decision Outcome",
    "Context": "Context and Problem Statement",
    "Alternatives": "Considered Options",
}


def _section_warnings(conv: Conversion, lines: Sequence[str]) -> None:
    heads = [l[3:].strip() for l in lines if l.startswith("## ")]
    for sec in ADRPLUS_SECTIONS:
        if sec not in heads:
            alt = MADR_HEADINGS.get(sec, "")
            note = f"; the file has `{alt}`" if alt and alt in heads else ""
            conv.warnings.append(Warn(f"missing-section:{sec}", f"no `## {sec}` heading{note}"))


def _convert_madr(text: str, lines: List[str], owner: str, plant: Optional[Tuple[str, str]],
                  name: str) -> Conversion:
    conv = Conversion(adr_id(text, name), "madr")
    block = split_header(text)
    assert block is not None
    try:
        entries = parse_flat(block[0])
    except YamlError as exc:
        conv.unparseable = f"front matter: {exc}"
        return conv
    k = block[1]
    fields = conv.fields
    kept: List[str] = []
    for e in entries:
        if e.key == "status":
            enc = encode_status(e.text.strip())
            if enc is None:
                conv.warnings.append(Warn("unmapped:status", f"`{e.text}` is not one of the project's verdicts"))
                kept.append(f"**Status:** {e.text}")
                continue
            fields["status"] = enc[0]
            conv.warnings.extend(w for w in enc[2] if w.kind == "verdict-mapped")
            if mapped_lead(enc[1]) is not None:
                fields["status-note"] = enc[1]
            else:
                tail = e.text.strip()[len(enc[0]):].strip()
                if tail:
                    fields["status-note"] = tail
        elif e.key == "consulted":
            if e.text != "":
                fields["consulted"] = e.text
        elif e.key in ("date", "decision-makers", "informed") or e.key not in MADR_KEYS:
            label = "-".join(w.capitalize() for w in e.key.split("-"))
            kept.append(f"**{label}:** {e.text}")
            conv.warnings.append(Warn(f"kept-in-body:{e.key}", f"`{e.key}` has no ADR+ field; kept as a bold line under the title"))
    fields["owner"] = owner
    conv.warnings.append(Warn("owner-from-settings", f"owner {owner} comes from the settings table"))
    if fields.get("status") in EXPECT_RATIFIED:
        conv.warnings.append(Warn("unparsed:ratified", "MADR holds no ratifier and date the converter may take as ratification"))
    _missing_warnings(conv)
    body = lines[k:]
    _section_warnings(conv, body)
    if "status" not in fields:
        conv.warnings.append(Warn("missing:status", "the front matter holds no usable status"))
    if kept:
        title = next((i for i, l in enumerate(body) if l.startswith("# ")), None)
        if title is None:
            conv.unparseable = "front matter keys to keep, but no `# ` title line to put them under"
            return conv
        ins = [""] + kept
        conv.inserted = ins
        body = body[:title + 1] + ins + body[title + 1:]
    conv.span = (0, k)
    return _finish(conv, body, plant)


def _convert_classic(text: str, lines: List[str], owner: str, plant: Optional[Tuple[str, str]],
                     name: str) -> Conversion:
    conv = Conversion(adr_id(text, name), "classic")
    h = next((i for i, l in enumerate(lines) if CLASSIC_STATUS.match(l)), None)
    assert h is not None
    z = next((i for i in range(h + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    section = [l for l in lines[h + 1:z] if l.strip() != ""]
    fields = conv.fields
    enc = encode_status(" ".join(section)) if section else None
    if enc is None:
        conv.warnings.append(Warn("unmapped:status", "the `## Status` section holds no verdict the project uses"))
        conv.warnings.append(Warn("kept-in-body:status", "the `## Status` section stays in the body"))
        span = (0, 0)
    else:
        fields["status"] = enc[0]
        conv.warnings.extend(w for w in enc[2] if w.kind == "verdict-mapped")
        if mapped_lead(enc[1]) is not None:
            rest = enc[1]
        else:
            rest = " ".join(section)[len(enc[0]):].strip()
        if rest:
            fields["status-note"] = rest
        span = (h, z)
    fields["owner"] = owner
    conv.warnings.append(Warn("owner-from-settings", f"owner {owner} comes from the settings table"))
    if fields.get("status") in EXPECT_RATIFIED:
        conv.warnings.append(Warn("unparsed:ratified", "a classic Status section holds no ratifier and date"))
    if "status" not in fields:
        conv.warnings.append(Warn("missing:status", "no usable status"))
    _missing_warnings(conv)
    _section_warnings(conv, lines)
    conv.span = span
    body = lines[:span[0]] + lines[span[1]:]
    return _finish(conv, body, plant)


def convert_text(text: str, owner: str, name: str = "",
                 plant: Optional[Tuple[str, str]] = None) -> Conversion:
    """Convert one ADR's text. `owner` is the settings value; `name` the file
    name, used only when the title carries no ADR number."""
    if "\r" in text:
        return Conversion(adr_id(text, name), "?", unparseable="the file has carriage returns")
    lines = text.split("\n")
    if lines[0] == "---" and split_header(text) is not None:
        return _convert_madr(text, lines, owner, plant, name)
    end = header_end(lines)
    if any(lines[i].startswith("**Status:**") for i in range(end)):
        return _convert_bold(text, lines, owner, plant, name)
    if any(CLASSIC_STATUS.match(l) for l in lines):
        return _convert_classic(text, lines, owner, plant, name)
    return Conversion(adr_id(text, name), "?", unparseable="no recognisable header: no `**Status:**` line, no front matter, no `## Status` section")


# ------------------------------------------------------------ the proof


def _eq_modulo_verdict_case(orig: str, rend: str, at: int, width: int) -> bool:
    if len(orig) != len(rend) or orig[:at] != rend[:at] or orig[at + width:] != rend[at + width:]:
        return False
    return orig[at:at + width].casefold() == rend[at:at + width].casefold()


def _moved_roundtrip(src_lines: List[str], conv: Conversion, data: Dict[str, object]) -> List[Failure]:
    """Re-render the moved bold lines from the YAML alone and compare."""
    fails: List[Failure] = []
    a, z = conv.span
    moved = [l for i, l in enumerate(src_lines[a:z], start=a) if not any(k0 <= i < k1 for k0, k1 in conv.kept)]
    status_end = len(moved)
    for i, l in enumerate(moved):
        if l.startswith(BUILT_PREFIX) or l.startswith(KIND_PREFIX) or _lineage(l) is not None:
            status_end = i
            break
    # The Status paragraph is every moved line before the first of the others.
    if status_end == 0:
        return [Failure("status", "no Status lines were moved")]
    orig_status = " ".join(moved[:status_end])
    status = data.get("status")
    note = data.get("status-note", "")
    if not isinstance(status, str):
        fails.append(Failure("status", f"status is missing from the YAML; the original `{orig_status[:60]}` is not recoverable"))
    elif not isinstance(note, str):
        fails.append(Failure("status-note", "status-note is not a string"))
    else:
        rend = STATUS_PREFIX + decode_status(status, note)
        prefix, after = consume_prefix(note)
        lead = mapped_lead(after)
        at = len(STATUS_PREFIX) + len(prefix)
        if lead is not None:
            if VERDICT_MAP[lead.lower()] != status:
                fails.append(Failure("status", f"status is {status!r} but the note leads with {lead}, which maps to {VERDICT_MAP[lead.lower()]!r}"))
            ok_line = orig_status == rend
        else:
            ok_line = _eq_modulo_verdict_case(orig_status, rend, at, len(status))
        if not ok_line:
            fails.append(Failure("status-note",
                                 f"the Status wording does not round-trip: original `{orig_status[:70]}` rendered `{rend[:70]}`"))
    for line in moved[status_end:]:
        if line.startswith(BUILT_PREFIX):
            built, proof, owed = data.get("built"), data.get("proof"), data.get("owed")
            if not isinstance(built, str):
                fails.append(Failure("built", f"built is missing from the YAML; the original `{line[:60]}` is not recoverable"))
                continue
            if not isinstance(proof, str):
                fails.append(Failure("proof", f"proof is missing from the YAML; the original `{line[:60]}` is not recoverable"))
                continue
            rend = f"{BUILT_PREFIX}{built.upper()} — {proof}"
            if isinstance(owed, str):
                rend += f"; owed: {owed}"
            elif line.find("; owed:") != -1:
                fails.append(Failure("owed", f"owed is missing from the YAML; the original `{line[:60]}` is not recoverable"))
                continue
            if rend != line:
                fails.append(Failure("built", f"the Built line does not round-trip: original `{line[:70]}` rendered `{rend[:70]}`"))
        elif line.startswith(KIND_PREFIX):
            kind = data.get("kind")
            if not isinstance(kind, str):
                fails.append(Failure("kind", f"kind is missing from the YAML; the original `{line}` is not recoverable"))
            elif KIND_PREFIX + kind != line:
                fails.append(Failure("kind", f"the Kind line does not round-trip: original `{line}` rendered `{KIND_PREFIX + kind}`"))
        else:
            sup, amd = data.get("supersedes"), data.get("amends")
            if not isinstance(sup, str):
                fails.append(Failure("supersedes", f"supersedes is missing from the YAML; the original `{line[:60]}` is not recoverable"))
            elif not isinstance(amd, str):
                fails.append(Failure("amends", f"amends is missing from the YAML; the original `{line[:60]}` is not recoverable"))
            else:
                rend = f"{SUPERSEDES_PREFIX}{sup}.{AMENDS_MARK}{amd}."
                if rend != line:
                    fails.append(Failure("supersedes", f"the lineage line does not round-trip: original `{line[:70]}` rendered `{rend[:70]}`"))
    return fails


def _expected_body(src_lines: List[str], conv: Conversion) -> List[str]:
    a, z = conv.span
    if conv.shape == "bold":
        kept_lines = [l for k0, k1 in conv.kept for l in src_lines[k0:k1]]
        return _cut_blank_rule(src_lines[:a] + kept_lines + src_lines[z:], a + len(kept_lines))[0]
    return src_lines[:a] + src_lines[z:]


def prove(source: str, conv: Conversion, schema: Dict[str, object], owner: str,
          second: Optional[Tuple[Any, Any]], schema_leg: bool = True) -> List[Failure]:
    """Every way `conv` loses or invents something, as Failures naming the field.
    `schema_leg` False skips the schema and second-instrument legs, for a source
    that cannot hold every required field (a classic or MADR file)."""
    if conv.unparseable:
        return [Failure("header", f"cannot convert: {conv.unparseable}")]
    fails: List[Failure] = []
    block = split_header(conv.out)
    if block is None:
        return [Failure("header", "the converted file has no YAML block")]
    header_lines, body_at = block
    header_text = "\n".join(header_lines) + "\n"
    try:
        data = parse_header(conv.out)
    except YamlError as exc:
        return [Failure("header", f"the YAML does not parse: {exc}")]
    src_lines = source.split("\n")
    out_lines = conv.out.split("\n")
    body = out_lines[body_at:]
    # Round trip.
    if conv.shape == "bold":
        fails.extend(_moved_roundtrip(src_lines, conv, data))
    else:
        low = source.casefold()
        for k, v in data.items():
            if k == "owner":
                continue
            if k == "status" and mapped_lead(consume_prefix(str(data.get("status-note", "")))[1]) is not None:
                continue
            if isinstance(v, str) and v.casefold() not in low:
                fails.append(Failure(k, f"{k} holds text that is not in the source: `{v[:60]}`"))
    # Never invent: owner from the settings, ratifier and date from the wording.
    if data.get("owner") != owner:
        fails.append(Failure("owner", f"owner is {data.get('owner')!r}, the settings say {owner!r}"))
    for k in ("ratified-by", "ratified-on"):
        v = data.get(k)
        if isinstance(v, str) and v.casefold() not in source.casefold():
            fails.append(Failure(k, f"{k} `{v}` does not appear in the source"))
    # Body.
    want = _expected_body(src_lines, conv)
    if conv.inserted:
        t = next((i for i, l in enumerate(body) if l.startswith("# ")), -1)
        n = len(conv.inserted)
        if t < 0 or body[t + 1:t + 1 + n] != conv.inserted:
            fails.append(Failure("body", "the lines kept under the title are not where the converter says"))
        else:
            body = body[:t + 1] + body[t + 1 + n:]
    if body != want:
        first = next((i for i in range(min(len(body), len(want))) if body[i] != want[i]), min(len(body), len(want)))
        fails.append(Failure("body", f"the body differs from the source minus the moved lines, first at body line {first + 1}"))
    if conv.shape == "bold":
        # A bold `**Label:**` line of the old header block that is not one of the four
        # moved fields stays in the body, so the converted body must still hold it.
        have: Dict[str, int] = {}
        for l in body:
            have[l] = have.get(l, 0) + 1
        for l in src_lines[:header_end(src_lines)]:
            if LABEL_LINE.match(l) and not l.startswith(MOVED_PREFIXES):
                if have.get(l, 0) == 0:
                    fails.append(Failure("body", f"the header line `{l[:60]}` is not a moved field and is missing from the body"))
                else:
                    have[l] -= 1
    if not schema_leg:
        return fails
    # Schema, with the tool's own validator.
    fails.extend(schema_failures(validate(data, schema)))
    if second is not None:
        fails.extend(second_check(header_text, data, schema, second))
    return fails


# ------------------------------------------------------------ the corpus


@dataclass
class Corpus:
    paths: List[pathlib.Path]
    n_live: int
    n_arch: int
    conversions: Dict[pathlib.Path, Conversion]
    sources: Dict[pathlib.Path, str]
    failures: Dict[pathlib.Path, List[Failure]]
    second_ran: bool


def yaml_conversion(text: str, name: str) -> Conversion:
    """A Conversion standing for a file that already has a YAML header."""
    conv = Conversion(adr_id(text, name), "yaml", out=text)
    try:
        data, _ = front_matter(text, name)
    except HeaderError as exc:
        conv.unparseable = str(exc)
        return conv
    conv.fields = {k: v for k, v in (data or {}).items() if isinstance(v, str)}
    return conv


def require_owner(root: pathlib.Path) -> str:
    """The owner setting, or exit saying where to put it."""
    owner = settings_owner(root)
    if owner is None:
        raise SystemExit(f"adr-yaml: no owner setting: add a row `| Owner | <name> |` to "
                         f"{root / settings(root).decisions / 'README.md'} or pass --owner")
    return owner


def run_corpus(root: pathlib.Path) -> Corpus:
    owner = require_owner(root)
    schema = load_schema(root)
    plant = plant_spec()
    live, archived = adr_paths(root)
    second = second_instrument()
    conversions: Dict[pathlib.Path, Conversion] = {}
    sources: Dict[pathlib.Path, str] = {}
    failures: Dict[pathlib.Path, List[Failure]] = {}
    for path in live + archived:
        text = path.read_text(encoding="utf-8")
        if is_yaml(text):
            # Already migrated: there is no bold-line source to prove against, so
            # the header is judged by the schema alone.
            conversions[path] = yaml_conversion(text, path.name)
            sources[path] = text
            failures[path] = check_header_text(text, path.name, schema, second, plant)
            continue
        conv = convert_text(text, owner, path.name, plant)
        conversions[path] = conv
        sources[path] = text
        failures[path] = prove(text, conv, schema, owner, second)
    return Corpus(live + archived, len(live), len(archived), conversions, sources,
                  failures, second is not None)


def do_prove(root: pathlib.Path) -> int:
    corpus = run_corpus(root)
    if not corpus.paths:
        print(f"adr-yaml: FAIL -- INSTRUMENT BLIND: no ADR-*.md files found under {root}")
        return 1
    drift = schema_drift(load_schema(root))
    bad = [(p, f) for p, fl in corpus.failures.items() for f in fl]
    for problem in drift:
        print(f"FAIL schema: {problem}")
    for path, f in bad:
        rel = relative(path, root)
        print(f"FAIL {rel}: {f.field}: {f.message}")
    second = "ran" if corpus.second_ran else "absent"
    print(f"second instrument: {second}")
    n_bad = len({p for p, _ in bad})
    if bad or drift:
        print(f"adr-yaml: FAIL -- {n_bad} of {corpus.n_live} + {corpus.n_arch} ADRs "
              f"lose or invent a header value ({len(bad)} findings, {len(drift)} schema drift)")
        return 1
    print(f"adr-yaml: PASS -- {corpus.n_live} + {corpus.n_arch} ADRs, every header "
          f"moves to YAML and proves lossless (second instrument: {second})")
    return 0


# ------------------------------------------------------------ the dry-run report


def _adr_num(conv: Conversion) -> str:
    return conv.adr.replace("ADR-", "")


def ranges(nums: Sequence[str]) -> str:
    """ADR numbers as text, consecutive runs collapsed: `181-196, 202`."""
    vals = sorted({int(n) for n in nums})
    parts: List[str] = []
    i = 0
    while i < len(vals):
        j = i
        while j + 1 < len(vals) and vals[j + 1] == vals[j] + 1:
            j += 1
        parts.append(f"{vals[i]:03d}" if i == j else f"{vals[i]:03d}-{vals[j]:03d}")
        i = j + 1
    return ", ".join(parts)


def build_report(root: pathlib.Path, corpus: Corpus) -> str:
    total = len(corpus.paths)
    clean: List[str] = []
    warned: List[str] = []
    unparsed: List[Tuple[str, str]] = []
    kinds: Dict[str, List[str]] = {}
    shapes: Dict[str, int] = {}
    for path in corpus.paths:
        conv = corpus.conversions[path]
        shapes[conv.shape] = shapes.get(conv.shape, 0) + 1
        if conv.unparseable:
            unparsed.append((path.name, conv.unparseable))
            continue
        extra = [w for w in conv.warnings if w.kind != "owner-from-settings"]
        (warned if extra else clean).append(conv.adr)
        seen = set()
        for w in conv.warnings:
            if w.kind in seen:
                continue
            seen.add(w.kind)
            kinds.setdefault(w.kind, []).append(_adr_num(conv))
    proof_bad = {p for p, fl in corpus.failures.items() if fl}
    out: List[str] = []
    out.append("# Dry run: the ADR header converter over every ADR\n")
    cfg = settings(root)
    folders = f"`{cfg.decisions.as_posix()}/`" + (f" and `{cfg.archive.as_posix()}/`" if cfg.archive else "")
    out.append(f"Written by `python3 adr-yaml.py --dry-run`. It converted every ADR in {folders} in memory and "
               "proved each. No ADR file was changed.\n")
    out.append("## Headline\n")
    out.append(f"- ADRs converted: {total} ({corpus.n_live} in the decisions folder, {corpus.n_arch} in the "
               f"archive folder).")
    out.append(f"- Convert and prove cleanly (no warning except `owner-from-settings`): {len(clean)}.")
    out.append(f"- Convert, with other warnings: {len(warned)}.")
    out.append(f"- Cannot be parsed: {len(unparsed)}.")
    out.append(f"- Proof failures (a value lost, a body changed or a schema error): {len(proof_bad)}.")
    second = ("ran: PyYAML and jsonschema also loaded and checked every header"
              if corpus.second_ran else "absent: PyYAML or jsonschema was not importable on this host")
    out.append(f"- Second instrument: {second}.\n")
    out.append("## What a warning means\n")
    out.append("The converter never invents a value. When the source does not say something in a shape it "
               "recognises, the field is left out and the ADR is listed under a warning kind. `owner-from-settings` "
               "is on every ADR by design: the owner comes from the settings table, not from the file.\n")
    if unparsed:
        out.append("## ADRs that cannot be parsed\n")
        for name, why in unparsed:
            out.append(f"- `{name}`: {why}")
        out.append("")
    if proof_bad:
        out.append("## Proof failures\n")
        out.append("A schema failure here means the old line holds a value the schema as written refuses; "
                   "the conversion itself lost nothing. These need a ruling before the migration.\n")
        for path in corpus.paths:
            for f in corpus.failures[path]:
                out.append(f"- `{path.name}`: {f.field}: {f.message}")
        out.append("")
    mapped: Dict[str, List[str]] = {}
    for path in corpus.paths:
        conv = corpus.conversions[path]
        for w in conv.warnings:
            if w.kind == "verdict-mapped":
                mapped.setdefault(w.detail.split(" ->")[0], []).append(_adr_num(conv))
    out.append("## Verdicts mapped to the seven status words\n")
    if mapped:
        out.append("| Old word | Becomes | ADRs | Which |")
        out.append("|---|---|---|---|")
        for word in sorted(mapped, key=lambda k: (-len(mapped[k]), k)):
            out.append(f"| `{word}` | `{VERDICT_MAP[word]}` | {len(mapped[word])} | {ranges(mapped[word])} |")
    else:
        out.append("No ADR carries an older verdict.")
    out.append("")
    out.append("## Warnings by kind\n")
    out.append("| Kind | ADRs | Which |")
    out.append("|---|---|---|")
    for kind in sorted(kinds, key=lambda k: (-len(kinds[k]), k)):
        nums = kinds[kind]
        which = "every ADR" if len(nums) == total - len(unparsed) and kind == "owner-from-settings" else ranges(nums)
        out.append(f"| `{kind}` | {len(nums)} | {which} |")
    out.append("")
    out.append("## Three headers as they would look\n")
    picks = [corpus.paths[i] for i in sorted({0, len(corpus.paths) // 2, len(corpus.paths) - 1})]
    for sample in picks:
        conv = corpus.conversions[sample]
        out.append(f"### {conv.adr}\n")
        out.append("```yaml")
        out.append(render_header(conv.fields).rstrip("\n"))
        out.append("```\n")
        interesting = [w for w in conv.warnings if w.kind != "owner-from-settings"]
        if interesting:
            out.append("Warnings: " + "; ".join(f"`{w.kind}`" for w in interesting) + ".\n")
    out.append("## How the proof works\n")
    out.append("For each ADR the proof re-renders the moved lines from the YAML alone and compares them with the "
               "originals (the verdict is compared without case, everything else byte for byte, with the Status "
               "paragraph's line breaks counted as single spaces). It checks that the file minus its YAML block "
               "equals the old file minus the moved lines, apart from one blank line dropped where the cut left "
               "two together. It parses the YAML and checks it against the schema with the tool's own parser and "
               "validator, and, where importable, with PyYAML and jsonschema. The red arm "
               "`ADRPLUS_PLANT=drop:<ADR-NNN>:<field>` drops one value and the proof must fail naming it.\n")
    return "\n".join(out) + "\n"


def do_dry_run(root: pathlib.Path, report: Optional[pathlib.Path]) -> int:
    corpus = run_corpus(root)
    if not corpus.paths:
        print("adr-yaml --dry-run: no ADR files found")
        return 1
    text = build_report(root, corpus)
    dest = report if report is not None else root / REPORT_NAME
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8")
    clean = sum(1 for p in corpus.paths
                if not corpus.conversions[p].unparseable
                and all(w.kind == "owner-from-settings" for w in corpus.conversions[p].warnings))
    unp = sum(1 for p in corpus.paths if corpus.conversions[p].unparseable)
    bad = sum(1 for p in corpus.paths if corpus.failures[p])
    print(f"adr-yaml --dry-run: {len(corpus.paths)} ADRs, {clean} clean, "
          f"{len(corpus.paths) - clean - unp} with warnings, {unp} unparseable, "
          f"{bad} with proof failures; report at {dest}")
    return 0


# ------------------------------------------------------------ --convert, --validate


def do_convert(path: pathlib.Path, root: pathlib.Path) -> int:
    owner = require_owner(root)
    text = path.read_text(encoding="utf-8")
    conv = convert_text(text, owner, path.name, plant_spec())
    for w in conv.warnings:
        print(f"warning: {conv.adr} {w.kind}: {w.detail}", file=sys.stderr)
    if conv.unparseable:
        print(f"adr-yaml: {path}: cannot convert: {conv.unparseable}", file=sys.stderr)
        return 2
    sys.stdout.write(conv.out)
    return 0


def header_errors(conv: Conversion, schema: Dict[str, object]) -> List[str]:
    if conv.unparseable:
        return [f"(header): cannot convert: {conv.unparseable}"]
    return validate_text(conv.out, schema)


def validate_text(text: str, schema: Dict[str, object]) -> List[str]:
    try:
        data = parse_header(text)
    except YamlError as exc:
        return [f"(header): {exc}"]
    return validate(data, schema)


def do_validate(paths: Sequence[str], root: pathlib.Path) -> int:
    schema = load_schema(root)
    bad = 0
    for p in paths:
        errs = validate_text(pathlib.Path(p).read_text(encoding="utf-8"), schema)
        if errs:
            bad += 1
            for e in errs:
                print(f"{p}: {e}")
        else:
            print(f"{p}: ok")
    return 1 if bad else 0


# ------------------------------------------------------------ --apply, --check, --prove-against

# Header lines that belong in the YAML block. A line that begins with one of these
# above the first `## ` heading is a header the migration left behind.
LEFT_BOLD: Tuple[str, ...] = ("**Status:**", "**Built:**", "**Kind:**", "**Supersedes:**")


def relative(path: pathlib.Path, root: pathlib.Path) -> pathlib.Path:
    """`path` relative to `root` when it lies under it, else `path`."""
    try:
        return path.relative_to(root)
    except ValueError:
        return path


def read_adr(path: pathlib.Path) -> str:
    """The file's text with its line endings untouched, so a carriage return
    reaches the converter, which refuses it."""
    return path.read_bytes().decode("utf-8")


def rel_path(path: pathlib.Path, root: pathlib.Path) -> str:
    return relative(path, root).as_posix()


FIELD_NAME = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")


def schema_failures(errors: Sequence[str]) -> List[Failure]:
    """One Failure per schema error, naming the field the error starts with. An
    unknown field is named too (`date: unknown field`), so the failure does not
    depend on the second instrument being importable; an error about the header as
    a whole starts with `(header)` and is named that way."""
    out: List[Failure] = []
    for err in errors:
        name = err.split(":", 1)[0]
        out.append(Failure(name if FIELD_NAME.match(name) else "header", f"schema: {err}"))
    return out


def check_header_text(text: str, name: str, schema: Dict[str, object],
                      second: Optional[Tuple[Any, Any]],
                      plant: Optional[Tuple[str, str]]) -> List[Failure]:
    """Every way the file's YAML header fails the standing check: no YAML block,
    a block the parser refuses, a schema error, a header line left in bold above
    the first `## ` heading. `plant` drops one field from the parsed header, the
    red arm of ADRPLUS_PLANT."""
    try:
        data, body_at = front_matter(text, name)
    except HeaderError as exc:
        return [Failure("header", str(exc))]
    if data is None:
        return [Failure("header", "no YAML header: the file does not open with ---")]
    planted = plant is not None and plant[0] == adr_id(text, name)
    if plant is not None and planted:
        data.pop(plant[1], None)
    fails = schema_failures(validate(data, schema))
    block = split_header(text)
    if second is not None and not planted and block is not None:
        fails.extend(second_check("\n".join(block[0]) + "\n", data, schema, second))
    lines = text.split("\n")
    for i in range(body_at, header_end(lines)):
        if lines[i].startswith(LEFT_BOLD):
            fails.append(Failure("bold-line", f"line {i + 1} `{lines[i][:50]}` is a header line left "
                                              f"in bold above the first ## heading"))
    return fails


def check_root(root: pathlib.Path, plant: Optional[Tuple[str, str]]
               ) -> Tuple[int, int, List[Tuple[str, Failure]], bool]:
    """(live count, archived count, (file, failure) pairs, whether the second
    instrument ran) for every ADR under `root`."""
    schema = load_schema(root)
    live, archived = adr_paths(root)
    second = second_instrument()
    bad: List[Tuple[str, Failure]] = []
    for path in live + archived:
        for f in check_header_text(read_adr(path), path.name, schema, second, plant):
            bad.append((rel_path(path, root), f))
    return len(live), len(archived), bad, second is not None


def do_check(root: pathlib.Path) -> int:
    n_live, n_arch, bad, ran = check_root(root, plant_spec())
    if n_live + n_arch == 0:
        print(f"adr-yaml: FAIL -- INSTRUMENT BLIND: no ADR-*.md files found under {root}")
        return 1
    drift = schema_drift(load_schema(root))
    for problem in drift:
        print(f"FAIL schema: {problem}")
    for rel, f in bad:
        print(f"FAIL {rel}: {f.field}: {f.message}")
    second = "ran" if ran else "absent"
    print(f"second instrument: {second}")
    if bad or drift:
        n_files = len({rel for rel, _ in bad})
        print(f"adr-yaml: FAIL -- {n_files} of {n_live} + {n_arch} ADRs have a YAML header "
              f"that is missing, malformed or off the schema ({len(bad)} findings, "
              f"{len(drift)} schema drift)")
        return 1
    print(f"adr-yaml: PASS -- {n_live} + {n_arch} ADRs, every header is YAML and passes "
          f"the schema (second instrument: {second})")
    return 0


def apply_root(root: pathlib.Path, write: bool) -> Tuple[int, int, List[Tuple[str, Failure]]]:
    """Convert every bold-line ADR under `root` to a YAML header. Returns
    (converted, already YAML, failures). Nothing is written unless every
    conversion proves lossless and `write` is true."""
    owner = require_owner(root)
    schema = load_schema(root)
    second = second_instrument()
    live, archived = adr_paths(root)
    pending: List[Tuple[pathlib.Path, str]] = []
    already = 0
    bad: List[Tuple[str, Failure]] = []
    for path in live + archived:
        text = read_adr(path)
        if is_yaml(text):
            already += 1
            continue
        conv = convert_text(text, owner, path.name)
        fails = prove(text, conv, schema, owner, second)
        if fails:
            bad.extend((rel_path(path, root), f) for f in fails)
        else:
            pending.append((path, conv.out))
    if not bad and write:
        for path, out in pending:
            path.write_bytes(out.encode("utf-8"))
    return len(pending), already, bad


def do_apply(root: pathlib.Path) -> int:
    live, archived = adr_paths(root)
    if not live and not archived:
        print(f"adr-yaml --apply: no ADR-*.md files found under {root}")
        return 1
    converted, already, bad = apply_root(root, True)
    if bad:
        for rel, f in bad:
            print(f"FAIL {rel}: {f.field}: {f.message}")
        print(f"adr-yaml --apply: FAIL -- {len({r for r, _ in bad})} ADRs would lose or invent a "
              f"header value; nothing was written")
        return 1
    print(f"adr-yaml --apply: converted {converted} ADRs to a YAML header, "
          f"left {already} that already have one ({len(live)} + {len(archived)} ADRs)")
    return 0


def prove_against(root: pathlib.Path, fetch_old: Callable[[str], Optional[str]]
                  ) -> Tuple[int, int, List[Tuple[str, Failure]]]:
    """Prove each ADR now under `root` against its old text, which `fetch_old`
    returns for a repository-relative path (None when the file is new). Returns
    (proved, new since, failures). An ADR that is not YAML is a failure: the
    migration missed it."""
    owner = require_owner(root)
    schema = load_schema(root)
    second = second_instrument()
    live, archived = adr_paths(root)
    proved = 0
    fresh = 0
    bad: List[Tuple[str, Failure]] = []
    for path in live + archived:
        rel = rel_path(path, root)
        new_text = read_adr(path)
        if not is_yaml(new_text):
            bad.append((rel, Failure("header", "still has bold header lines: the migration missed this ADR")))
            continue
        old = fetch_old(rel)
        if old is None or is_yaml(old):
            fresh += 1
            continue
        conv = convert_text(old, owner, path.name)
        if conv.unparseable:
            bad.append((rel, Failure("header", f"cannot convert the old text: {conv.unparseable}")))
            continue
        conv.out = new_text
        fails = prove(old, conv, schema, owner, second)
        if fails:
            bad.extend((rel, f) for f in fails)
        else:
            proved += 1
    return proved, fresh, bad


def git_fetcher(root: pathlib.Path, rev: str) -> Callable[[str], Optional[str]]:
    def fetch(rel: str) -> Optional[str]:
        res = subprocess.run(["git", "-C", str(root), "show", f"{rev}:{rel}"],
                             capture_output=True, check=False)
        return res.stdout.decode("utf-8") if res.returncode == 0 else None
    return fetch


def do_prove_against(root: pathlib.Path, rev: str) -> int:
    probe = subprocess.run(["git", "-C", str(root), "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}"],
                           capture_output=True, check=False)
    if probe.returncode != 0:
        print(f"adr-yaml --prove-against: {rev} is not a commit in {root}")
        return 2
    live, archived = adr_paths(root)
    if not live and not archived:
        print(f"adr-yaml --prove-against: no ADR-*.md files found under {root}")
        return 1
    proved, fresh, bad = prove_against(root, git_fetcher(root, rev))
    for rel, f in bad:
        print(f"FAIL {rel}: {f.field}: {f.message}")
    if bad:
        print(f"adr-yaml --prove-against {rev}: FAIL -- {len({r for r, _ in bad})} of "
              f"{len(live)} + {len(archived)} ADRs do not prove against {rev}")
        return 1
    print(f"adr-yaml --prove-against {rev}: PASS -- {proved} of {len(live)} + {len(archived)} ADRs prove "
          f"lossless against their text at {rev} ({fresh} are new since)")
    return 0


# ------------------------------------------------------------ --self-test


@dataclass
class FixtureRow:
    name: str
    verdict: str
    detail: str


def read_expected(directory: pathlib.Path) -> List[FixtureRow]:
    rows: List[FixtureRow] = []
    for line in (directory / "EXPECTED.md").read_text(encoding="utf-8").split("\n"):
        if not line.startswith("|"):
            continue
        cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
        if len(cells) < 3 or cells[0] in ("fixture", "") or set(cells[0]) <= set("-: "):
            continue
        rows.append(FixtureRow(cells[0], cells[1], cells[2]))
    return rows


def _detail_get(detail: str, key: str) -> Optional[str]:
    for part in detail.split(";"):
        part = part.strip()
        if part.startswith(key + "="):
            return part[len(key) + 1:].strip()
    return None


class Arms:
    def __init__(self) -> None:
        self.total = 0
        self.failed = 0

    def check(self, name: str, ok: bool, why: str = "") -> None:
        self.total += 1
        if not ok:
            self.failed += 1
        suffix = "" if ok else f" -- {why}"
        print(f"  {'ok  ' if ok else 'FAIL'} {name}{suffix}")


# The scratch trees of the self-test keep their ADRs where a project usually does.
SCRATCH_DECISIONS = pathlib.Path("docs/decisions")
SCRATCH_ARCHIVE = pathlib.Path("docs/archive/adrs")
SCRATCH_README = ("# Decisions\n\n| Setting | Value |\n|---|---|\n| Owner | Alex — the person answerable |\n"
                  "| Archive folder | docs/archive/adrs |\n")


def self_test() -> int:
    arms = Arms()
    configure()
    owner = "Alex"
    schema = load_schema(PACKAGE)
    second = second_instrument()
    print("adr-yaml --self-test")

    # The schema agrees with the tool.
    drift = schema_drift(schema)
    arms.check("schema: field order, verdict enum and kinds agree with the tool", not drift, "; ".join(drift))
    try:
        validate({"x": 1}, {"type": "object", "minimum": 3})
        arms.check("validator: refuses a schema keyword it does not implement", False, "accepted `minimum`")
    except ValueError:
        arms.check("validator: refuses a schema keyword it does not implement", True)

    # Scalars: what is plain, what is quoted, and that both load back as the same string.
    tricky = ["yes", "No", "on", "off", "true", "null", "~", "2026-09-10", "12:30", "1e3", "0x1f", "007", "3.5",
              "-5", "+5", ".inf", "<<", "=", "`SCAN_TEST=1` (the scan)", "@mention", "*bold*", "&anchor",
              "!tag", "|pipe", ">fold", "'single'", '"double"', "%percent", "[list]", "{map}", "#hash",
              "a: b", "a #b", "ends with:", "trailing space ", " leading", "tab\there", "back\\slash",
              'say "hi"', "line\nbreak", "✅ — glyph", "- dash", "? q", ", comma", "", "---", "plain words — fine"]
    ok = True
    why = ""
    for v in tricky:
        line = f"k: {scalar(v)}"
        try:
            got = parse_flat([line])[0].value
        except YamlError as exc:
            ok, why = False, f"{v!r}: {exc}"
            break
        if got != v:
            ok, why = False, f"{v!r} loaded as {got!r}"
            break
    arms.check("emitter: every tricky string loads back as itself with the tool's own parser", ok, why)
    plain_ok = all(not needs_quotes(v) for v in ("plain words", "n/a", "not started", "partially accepted",
                                                 "ADR-001 and ADR-002", "alex (the owner)"))
    arms.check("emitter: ordinary words stay plain", plain_ok)
    if second is not None:
        yaml = second[0]
        ok = True
        why = ""
        for v in tricky:
            try:
                got = yaml.safe_load(f"k: {scalar(v)}\n")["k"]
            except Exception as exc:  # PyYAML raises its own family
                ok, why = False, f"{v!r}: PyYAML {exc}"
                break
            if got != v:
                ok, why = False, f"{v!r} loaded by PyYAML as {got!r}"
                break
        arms.check("emitter: PyYAML loads every tricky string back as itself (second instrument)", ok, why)
    else:
        arms.check("emitter: second instrument absent, skipped", True)
    refused = 0
    for bad_line in ("k:\n  nested: 1", "k: [a, b]", "k: {a: 1}", "- item", "a: 1\na: 2", "k: a: b", "k: |"):
        try:
            parse_flat(bad_line.split("\n"))
        except YamlError:
            refused += 1
    arms.check("parser: refuses a nested block, a list, a flow collection, a duplicate key and `a: b`",
               refused == 7, f"refused {refused} of 7")

    # The status codec round trips.
    cases = ["ACCEPTED", "ACCEPTED — RATIFIED BY ALEX 2026-09-10", "✅ ACCEPTED — RATIFIED BY ALEX 2026-09-10 (x)",
             "**ACCEPTED — RATIFIED BY ALEX 2026-08-18, live", "**✅ ACCEPTED — RATIFIED:** tail",
             "PROPOSED (S4 sitting)", "RATIFIED BY DELEGATION — 2026-08-02", "ACCEPTED in design — ruled",
             "Accepted — mixed case", "PARTIALLY ACCEPTED — x", "ACCEPTED — ✅ glyph after the dash",
             "ACCEPTED —  two spaces", "ACCEPTED: colon", "ACCEPTED**: bold close", "✅ ACCEPTED", "ACCEPTED — ",
             "RATIFIED — by Alex 2026-09-10", "DRAFT", "✅ Awaiting (a glyph and a mapped word)",
             "ACCEPTED — ratified by Alex", "Closed: no separator dash", "**NIXED** — bold", "PROPOSED — draft of x"]
    ok = True
    why = ""
    for c in cases:
        enc = encode_status(c)
        if enc is None:
            ok, why = False, f"{c!r} found no verdict"
            break
        back = decode_status(enc[0], enc[1])
        if back.casefold() != c.casefold():
            ok, why = False, f"{c!r} came back as {back!r}"
            break
    arms.check(f"status codec: {len(cases)} wordings, mapped verdicts and collisions among them, come back as written", ok, why)

    # Fixtures.
    fixtures = FIXTURES
    try:
        rows = read_expected(fixtures)
    except OSError as exc:
        arms.check("fixtures: EXPECTED.md is readable", False, str(exc))
        rows = []
    present = sorted(p.name for p in fixtures.glob("*.md") if p.name != "EXPECTED.md") if fixtures.exists() else []
    arms.check("fixtures: EXPECTED.md names every fixture file and no other",
               sorted(r.name for r in rows) == present, f"table {sorted(r.name for r in rows)} files {present}")
    for row in rows:
        text = (fixtures / row.name).read_text(encoding="utf-8")
        if row.verdict in ("good", "warn"):
            conv = convert_text(text, owner, row.name)
            want_valid = _detail_get(row.detail, "schema") != "invalid"
            fails = prove(text, conv, schema, owner, second, schema_leg=want_valid)
            want = [k for k in (_detail_get(row.detail, "warnings") or "").split(",") if k]
            got = sorted({w.kind for w in conv.warnings})
            errs = header_errors(conv, schema)
            arms.check(f"fixture {row.name} ({row.verdict}): converts, proves lossless, warns {','.join(want) or 'nothing'}",
                       not fails and sorted(want) == got,
                       f"failures {[(f.field, f.message[:60]) for f in fails]}, warnings {got}")
            arms.check(f"fixture {row.name}: the converted header {'is valid against' if want_valid else 'is refused by'} the schema",
                       (not errs) == want_valid, "; ".join(errs) or "no schema error")
        else:
            errs = validate_text(text, schema)
            sub = _detail_get(row.detail, "refuses") or ""
            arms.check(f"fixture {row.name} (bad): the schema refuses it saying `{sub}`",
                       bool(errs) and any(sub in e for e in errs), f"errors {errs}")
            block = split_header(text)
            if second is not None and block is not None:
                try:
                    theirs = second[0].safe_load("\n".join(block[0]) + "\n")
                    n = len(list(second[1].Draft202012Validator(schema).iter_errors(theirs)))
                except Exception as exc:  # PyYAML raises its own family
                    n = 1
                    theirs = str(exc)
                arms.check(f"fixture {row.name}: jsonschema refuses it too (second instrument)", n > 0, f"{theirs!r}")

    # Blank-line rule and the cut, on a small file.
    sample = "# ADR-900 — t\n\n**Status:** ACCEPTED — RATIFIED BY ALEX 2026-01-02\n**Built:** N/A — a rule\n" \
             "**Kind:** process\n**Supersedes:** nothing. **Amends:** nothing.\n\n**Date:** 2026-01-01\n\n## Decision\n\nx\n"
    conv = convert_text(sample, owner)
    tail = conv.out.split("\n---\n", 1)[1]
    arms.check("cut: two blank lines meeting at the cut become one",
               conv.dropped_blank and tail == "# ADR-900 — t\n\n**Date:** 2026-01-01\n\n## Decision\n\nx\n", repr(tail))
    only_one = "# ADR-901 — t\n\n**Status:** ACCEPTED\n**Built:** N/A — a rule\n**Kind:** process\n" \
               "**Supersedes:** nothing. **Amends:** nothing.\n## Decision\n\nx\n"
    conv1 = convert_text(only_one, owner)
    arms.check("cut: no blank line is dropped when the cut leaves none together",
               not conv1.dropped_blank and not prove(only_one, conv1, schema, owner, second))

    # A dated label line between Status and Built ends the Status paragraph and stays in the body.
    atext = (FIXTURES / "good-amended-label.md").read_text(encoding="utf-8")
    aconv = convert_text(atext, owner, "ADR-905-amended.md")
    abody = aconv.out.split("\n---\n", 1)[-1]
    arms.check("label line: the Amended line stays in the body and out of status-note",
               "**Amended 2026-10-12:**" in abody and "Amended" not in aconv.fields.get("status-note", ""),
               repr(aconv.fields.get("status-note")))
    arms.check("label line: the converted copy proves clean", not prove(atext, aconv, schema, owner, second))
    global LABEL_ENDS_STATUS
    LABEL_ENDS_STATUS = False
    try:
        absorbed = convert_text(atext, owner, "ADR-905-amended.md")
    finally:
        LABEL_ENDS_STATUS = True
    afl = prove(atext, absorbed, schema, owner, second)
    arms.check("red arm: a converter that absorbs the Amended line into status-note is caught by the proof",
               "Amended" in absorbed.fields.get("status-note", "") and any(f.field == "body" and "Amended" in f.message for f in afl),
               f"failures {[(f.field, f.message[:50]) for f in afl]}")
    lost = convert_text(atext, owner)
    lost.out = lost.out.replace("**Amended 2026-10-12:** the context's \"16.4 MB\" mixes MB and MiB; the correction is in the Consequences.\n", "")
    lfl = prove(atext, lost, schema, owner, second)
    arms.check("red arm: a header label line missing from the body fails the proof naming it",
               any(f.field == "body" and "Amended" in f.message for f in lfl), f"failures {[(f.field, f.message[:50]) for f in lfl]}")

    # Label lines between Kind and the lineage line stay in the body; the lineage line still moves.
    ltext = (FIXTURES / "good-labels-between.md").read_text(encoding="utf-8")
    lconv = convert_text(ltext, owner, "ADR-926-labels.md")
    lbody = lconv.out.split("\n---\n", 1)[-1]
    arms.check("label lines: Owner and Consulted stay in the body, in the place the Status line stood",
               "**Owner:** Alex\n**Consulted:** a read-only survey\n" in lbody and "Owner" not in "".join(lconv.fields.values()),
               repr(lbody))
    arms.check("label lines: Supersedes and Amends are still moved after them",
               lconv.fields.get("supersedes") == "nothing" and lconv.fields.get("amends") == "nothing"
               and not prove(ltext, lconv, schema, owner, second),
               f"{lconv.fields!r}")
    lconv.out = lconv.out.replace("**Consulted:** a read-only survey\n", "")
    lfl2 = prove(ltext, lconv, schema, owner, second)
    arms.check("red arm: a Consulted line cut from the body fails the proof naming it",
               any(f.field == "body" and "Consulted" in f.message for f in lfl2),
               f"failures {[(f.field, f.message[:50]) for f in lfl2]}")

    # A planted copy: the red arm and its green twin.
    base = "# ADR-902 — planted\n\n**Status:** ACCEPTED — RATIFIED BY ALEX 2026-01-02\n**Built:** LANDED — `tools/adr-yaml.py`\n" \
           "**Kind:** process\n**Supersedes:** nothing. **Amends:** nothing.\n\n## Decision\n\nx\n"
    green = convert_text(base, owner)
    arms.check("red arm: with nothing planted a converted copy proves clean", not prove(base, green, schema, owner, second))
    for fld in ("kind", "status", "supersedes", "proof"):
        planted = convert_text(base, owner, plant=("ADR-902", fld))
        fl = prove(base, planted, schema, owner, second)
        arms.check(f"red arm: dropping `{fld}` fails the proof naming it", any(f.field == fld for f in fl),
                   f"failures {[(f.field) for f in fl]}")
    other = convert_text(base, owner, plant=("ADR-999", "kind"))
    arms.check("red arm: a plant aimed at another ADR changes nothing", other.fields == green.fields)

    # Every body line outside the moved ones survives a conversion of a demoted-style file.
    demoted = "# ADR-903 — demoted\n\n> **Demoted.** banner\n\n**Status:** ✅ ACCEPTED — RATIFIED BY ALEX 2026-01-02 (a\nwrapped paragraph)\n" \
              "**Built:** PARTIAL — `tools/adr-yaml.py`; owed: the rest\n**Kind:** process\n**Supersedes:** nothing. **Amends:** nothing.\n\nProse.\n"
    cd = convert_text(demoted, owner)
    arms.check("demoted shape: banner kept, wrapped Status paragraph and `; owed:` move and prove",
               not prove(demoted, cd, schema, owner, second) and cd.fields.get("owed") == "the rest",
               f"{[(f.field, f.message[:50]) for f in prove(demoted, cd, schema, owner, second)]}")

    # The shared reader (tools/adrplus.py).
    yaml_adr = render_header({"status": "accepted", "status-note": "RATIFIED BY ALEX 2026-09-10", "owner": owner,
                              "kind": "process", "built": "partial", "proof": "`FOO_TEST=1`",
                              "owed": "the rest", "supersedes": "nothing", "amends": "nothing"}) + \
        "# ADR-904 — y\n\n## Decision\n\nx\n"
    fm, at = front_matter(yaml_adr, "ADR-904.md")
    arms.check("reader: front_matter returns the YAML block and the line after its closing fence",
               fm is not None and fm.get("kind") == "process" and at == 11 and yaml_adr.split("\n")[at].startswith("# ADR-904"),
               f"{fm!r} {at}")
    arms.check("reader: front_matter of a bold-line file is (None, 0)",
               front_matter("# ADR-1 — t\n\n**Status:** ACCEPTED\n") == (None, 0))
    for label, text in (("a block that never closes", "---\nstatus: accepted\n# ADR-9 — t\n"),
                        ("a line the parser refuses", "---\nstatus accepted\n---\n# ADR-9 — t\n"),
                        ("a nested block", "---\nstatus:\n  x: 1\n---\n# ADR-9 — t\n")):
        try:
            front_matter(text, "ADR-9-x.md")
            arms.check(f"reader: {label} is a HeaderError naming the file", False, "no error")
        except HeaderError as exc:
            arms.check(f"reader: {label} is a HeaderError naming the file", "ADR-9-x.md" in str(exc), str(exc))
    arms.check("reader: header() of a YAML ADR is its YAML values", header(yaml_adr, "ADR-904.md")["owed"] == "the rest")
    bold_text = (fixtures / "good-bold.md").read_text(encoding="utf-8")
    bold_conv = convert_text(bold_text, owner, "good-bold.md")
    arms.check("reader: header() of a bold-line ADR is the converter's fields, the same keys a YAML ADR has",
               header(bold_text, "good-bold.md", owner) == dict(bold_conv.fields) and "status" in bold_conv.fields,
               f"{header(bold_text, 'good-bold.md', owner)!r}")
    bad_bold = "# ADR-1 — t\n\nno header lines here\n"
    try:
        header(bad_bold, "ADR-1-x.md", owner)
        arms.check("reader: a bold-line header the converter refuses is a HeaderError", False, "no error")
    except HeaderError as exc:
        arms.check("reader: a bold-line header the converter refuses is a HeaderError", "ADR-1-x.md" in str(exc), str(exc))
    hy = header(yaml_adr, "ADR-904.md")
    arms.check("reader: status_wording and built_rest rebuild the old line text",
               status_wording(hy) == "RATIFIED BY ALEX 2026-09-10" and built_rest(hy) == "`FOO_TEST=1`; owed: the rest",
               f"{status_wording(hy)!r} {built_rest(hy)!r}")
    arms.check("reader: s2_status maps ratified, closed, draft and nixed; passes the seven; refuses others",
               [s2_status(w) for w in ("RATIFIED", "closed", "Draft", "nixed", "partially accepted", "bogus")]
               == ["accepted", "withdrawn", "proposed", "rejected", "partially accepted", None])

    # --apply, --check and --prove-against on a scratch tree.
    with tempfile.TemporaryDirectory(prefix="adr-yaml-selftest-") as td:
        scratch = pathlib.Path(td) / "tree"
        (scratch / SCRATCH_DECISIONS).mkdir(parents=True)
        (scratch / SCRATCH_ARCHIVE).mkdir(parents=True)
        (scratch / SCRATCH_DECISIONS / "README.md").write_text(SCRATCH_README, encoding="utf-8")
        shutil.copy(PACKAGE / "schema" / "adr-plus.schema.json", scratch / SCRATCH_DECISIONS / "adr-plus.schema.json")
        layout = (("good-bold.md", SCRATCH_DECISIONS / "ADR-901-bold.md"),
                  ("good-partial.md", SCRATCH_DECISIONS / "ADR-902-partial.md"),
                  ("good-glyph-paragraph.md", SCRATCH_ARCHIVE / "ADR-903-glyph.md"))
        old: Dict[str, str] = {}
        for src, dest in layout:
            shutil.copy(fixtures / src, scratch / dest)
            old[dest.as_posix()] = (scratch / dest).read_text(encoding="utf-8")
        n_live, n_arch, bad, _ran = check_root(scratch, None)
        arms.check("--check: a tree of bold-line ADRs fails, naming each file",
                   len({r for r, _ in bad}) == 3 and all("no YAML header" in f.message for _, f in bad), f"{bad!r}")
        before = {d: (scratch / d).read_bytes() for d in old}
        conv_n, left_n, apply_bad = apply_root(scratch, False)
        arms.check("--apply: a dry run converts nothing and writes nothing",
                   (conv_n, left_n, apply_bad) == (3, 0, []) and all((scratch / d).read_bytes() == before[d] for d in old),
                   f"{conv_n} {left_n} {apply_bad!r}")
        conv_n, left_n, apply_bad = apply_root(scratch, True)
        arms.check("--apply: converts every bold-line ADR in both folders", (conv_n, left_n, apply_bad) == (3, 0, []),
                   f"{conv_n} {left_n} {apply_bad!r}")
        after = {d: (scratch / d).read_bytes() for d in old}
        conv_n, left_n, apply_bad = apply_root(scratch, True)
        arms.check("--apply: a second run changes nothing (idempotent)",
                   (conv_n, left_n, apply_bad) == (0, 3, []) and all((scratch / d).read_bytes() == after[d] for d in old))
        n_live, n_arch, bad, _ran = check_root(scratch, None)
        arms.check("--check: the converted tree passes", (n_live, n_arch, bad) == (2, 1, []), f"{bad!r}")
        proved, fresh, against = prove_against(scratch, lambda rel: old.get(rel))
        arms.check("--prove-against: every converted ADR proves against its old text", (proved, fresh, against) == (3, 0, []),
                   f"{proved} {fresh} {against!r}")
        proved, fresh, against = prove_against(scratch, lambda rel: None)
        arms.check("--prove-against: an ADR with no old text is counted as new, not proved", (proved, fresh, against) == (0, 3, []))

        # Red arms, each on a fresh copy of the converted tree.
        def tampered(label: str, edit: Callable[[str], str], rel: str) -> pathlib.Path:
            copy = pathlib.Path(td) / f"tree-{label}"
            shutil.copytree(scratch, copy)
            target = copy / rel
            target.write_text(edit(target.read_text(encoding="utf-8")), encoding="utf-8")
            return copy

        bold_rel = (SCRATCH_DECISIONS / "ADR-901-bold.md").as_posix()
        partial_rel = (SCRATCH_DECISIONS / "ADR-902-partial.md").as_posix()
        glyph_rel = (SCRATCH_ARCHIVE / "ADR-903-glyph.md").as_posix()
        red = tampered("body", lambda s: s.rstrip("\n") + "\n\nAn extra sentence.\n", bold_rel)
        _p, _f, against = prove_against(red, lambda rel: old.get(rel))
        arms.check("--prove-against red arm: a word added to a body fails naming the file and `body`",
                   any(r == bold_rel and f.field == "body" for r, f in against), f"{against!r}")
        red = tampered("proof", lambda s: s.replace("proof: ", "proof: x", 1), partial_rel)
        _p, _f, against = prove_against(red, lambda rel: old.get(rel))
        arms.check("--prove-against red arm: an altered proof fails naming the file and `built`",
                   any(r == partial_rel and f.field == "built" for r, f in against), f"{against!r}")
        red = tampered("status", lambda s: s.replace("status: ", "status: x", 1), glyph_rel)
        _n1, _n2, bad = check_root(red, None)[:3]
        arms.check("--check red arm: a status outside the seven fails naming the file",
                   any(r == glyph_rel and f.field == "status" for r, f in bad), f"{bad!r}")
        red = tampered("unknown", lambda s: s.replace("\nowner: ", "\ndate: 2026-01-01\nowner: ", 1), bold_rel)
        bad = check_root(red, None)[2]
        arms.check("--check red arm: an unknown field fails naming the file and the field",
                   any(r == bold_rel and f.field == "date" for r, f in bad), f"{bad!r}")
        red = tampered("left", lambda s: s.replace("\n---\n", "\n---\n**Kind:** process\n", 1), bold_rel)
        bad = check_root(red, None)[2]
        arms.check("--check red arm: a bold header line left above the first heading fails",
                   any(r == bold_rel and f.field == "bold-line" for r, f in bad), f"{bad!r}")
        red = tampered("unclosed", lambda s: s.replace("\n---\n", "\n", 1), partial_rel)
        bad = check_root(red, None)[2]
        arms.check("--check red arm: a block that never closes fails naming the file",
                   any(r == partial_rel and "never closes" in f.message for r, f in bad), f"{bad!r}")
        bad = check_root(scratch, ("ADR-902", "kind"))[2]
        arms.check("--check red arm: ADRPLUS_PLANT drops `kind` from one parsed header and the check names it",
                   any(r == partial_rel and f.field == "kind" for r, f in bad) and len(bad) >= 1, f"{bad!r}")
        bad = check_root(scratch, ("ADR-999", "kind"))[2]
        arms.check("--check: a plant aimed at another ADR changes nothing", bad == [], f"{bad!r}")

        # An ADR that cannot be proved stops the whole --apply.
        mixed = pathlib.Path(td) / "tree-mixed"
        (mixed / SCRATCH_DECISIONS).mkdir(parents=True)
        (mixed / SCRATCH_DECISIONS / "README.md").write_text(SCRATCH_README, encoding="utf-8")
        shutil.copy(fixtures / "good-bold.md", mixed / SCRATCH_DECISIONS / "ADR-901-bold.md")
        (mixed / SCRATCH_DECISIONS / "ADR-905-nothing.md").write_text("# ADR-905 — no header\n\nBody.\n", encoding="utf-8")
        was = (mixed / SCRATCH_DECISIONS / "ADR-901-bold.md").read_bytes()
        conv_n, left_n, apply_bad = apply_root(mixed, True)
        arms.check("--apply: one unconvertible ADR stops it, and nothing is written",
                   len(apply_bad) >= 1 and apply_bad[0][0].endswith("ADR-905-nothing.md")
                   and (mixed / SCRATCH_DECISIONS / "ADR-901-bold.md").read_bytes() == was, f"{apply_bad!r}")
        crlf = (mixed / SCRATCH_DECISIONS / "ADR-905-nothing.md")
        crlf.write_bytes(b"# ADR-905 \xe2\x80\x94 crlf\r\n\r\n**Status:** ACCEPTED\r\n")
        conv_n, left_n, apply_bad = apply_root(mixed, True)
        arms.check("--apply: a carriage return is refused rather than read away",
                   any("carriage" in f.message for _r, f in apply_bad), f"{apply_bad!r}")

    print(f"adr-yaml --self-test: {arms.total - arms.failed} of {arms.total} arms")
    return 1 if arms.failed else 0


# ------------------------------------------------------------ main


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0] if __doc__ else "")
    ap.add_argument("--convert", metavar="FILE")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--report", metavar="PATH", help="where --dry-run writes its report")
    ap.add_argument("--prove", action="store_true")
    ap.add_argument("--validate", nargs="+", metavar="FILE")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--prove-against", metavar="REV")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--root", default=".", metavar="DIR", help="the project root (default: the current directory)")
    ap.add_argument("--dir", default=None, metavar="PATH", help="the decisions folder, relative to the root")
    ap.add_argument("--archive", default=None, metavar="PATH", help="the archive folder, relative to the root, or none")
    ap.add_argument("--owner", default=None, metavar="NAME", help="the owner written into converted ADRs")
    ap.add_argument("--schema", default=None, metavar="FILE", help="the JSON Schema to check headers against")
    args = ap.parse_args(argv)
    root = pathlib.Path(args.root)
    if args.self_test:
        return self_test()
    configure(decisions=args.dir, archive=args.archive, owner=args.owner, schema=args.schema)
    if args.prove:
        return do_prove(root)
    if args.apply:
        return do_apply(root)
    if args.check:
        return do_check(root)
    if args.prove_against:
        return do_prove_against(root, args.prove_against)
    if args.dry_run:
        return do_dry_run(root, pathlib.Path(args.report) if args.report else None)
    if args.convert:
        return do_convert(pathlib.Path(args.convert), root)
    if args.validate:
        return do_validate(args.validate, root)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
