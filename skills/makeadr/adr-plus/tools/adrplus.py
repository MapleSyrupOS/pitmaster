#!/usr/bin/env python3
"""adrplus.py -- the one reader for an ADR's ADR+ header (ADR+ release 0.1.0).

An ADR carries its header as a YAML block at the top of the file (SPEC.md 1.3) or,
in files not yet converted, as the bold lines `**Status:**`, `**Built:**`,
`**Kind:**` and `**Supersedes:** ... **Amends:** ...`. Every tool that needs a
header value asks here, so a caller sees one shape whichever the file holds:

  front_matter(text, name)  (the parsed YAML block, index of the first line after
                            its closing `---`); (None, 0) when the file has none.
                            A block that never closes, or that the flat parser
                            refuses, is a HeaderError naming `name`; there is no
                            fallback to the bold lines.
  header(text, name)        the header as a dict of field name to value. A YAML ADR
                            gives its YAML values. A bold-line ADR gives the same
                            keys, derived by the converter in adr-yaml.py.
                            A bold-line header the converter refuses is a
                            HeaderError.
  is_yaml(text)             whether the file opens with a `---` line.
  status_wording(h)         the old `**Status:**` wording that `status` and
                            `status-note` say together (without the label).
  built_rest(h)             the text that followed `LANDED — ` on the old Built line:
                            `proof`, then `; owed: ` and `owed` when present.
  s2_status(word)           the status word a verdict maps to under the seven-word
                            rule, or None when the word is not a verdict.

The module also holds the parts every reader of the YAML shares: the field list in
schema order, the seven status words and the older verdicts that map onto them, the
parser for the flat YAML subset the converter writes, the emitter's quoting rules,
and a validator for the part of JSON Schema that schema/adr-plus.schema.json uses.
Project settings (the owner, the decisions folder, the archive folder, the schema)
come from `settings()`: the project's decisions README, then command-line values
passed to `configure()`. Standard library only; Python 3.8 or later.
"""
from __future__ import annotations

import datetime
import importlib.util
import json
import pathlib
import re
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple, cast

TOOLS = pathlib.Path(__file__).resolve().parent
PACKAGE = TOOLS.parent
SHIPPED_SCHEMA = PACKAGE / "schema" / "adr-plus.schema.json"
# Folders a project may keep its ADRs in, in the order they are tried.
DECISION_DIRS: Tuple[str, ...] = ("docs/decisions", "docs/adr", "docs/adrs", "doc/adr", "doc/decisions",
                                  "adr", "decisions")
ADR_FILE = re.compile(r"^ADR-\d+-.+\.md$")

FIELD_ORDER: Tuple[str, ...] = (
    "status", "status-note", "ratified-by", "ratified-on", "owner", "kind",
    "built", "proof", "owed", "supersedes", "amends", "consulted",
    "confirmed-by", "revisit-when",
)
KINDS: Tuple[str, ...] = ("architecture", "design", "process")
# The seven status words the schema allows, and the older verdicts that map onto them.
STATUS_WORDS: Tuple[str, ...] = (
    "proposed", "provisional", "accepted", "partially accepted", "superseded",
    "withdrawn", "rejected")
VERDICT_MAP: Dict[str, str] = {
    "ratified": "accepted", "adopted": "accepted", "ruled": "accepted", "landed": "accepted",
    "deprecated": "withdrawn", "retired": "withdrawn", "closed": "withdrawn",
    "nixed": "rejected",
    "draft": "proposed", "awaiting": "proposed",
}
PREFIX_TOKEN = re.compile(r"\*\*|(?:⚑{1,2}|✅) ")
# A setting is a row of the decisions README's settings table: `| Owner | Alex |`. The
# value runs to the end of the cell or to a ` — ` that starts an explanation.
SETTING_ROW = re.compile(r"^\|\s*([A-Za-z][A-Za-z ]*?)\s*\|\s*(.*?)\s*(?:\s—\s.*)?\|?\s*$")


class YamlError(Exception):
    """A header line the flat parser will not read."""


class HeaderError(Exception):
    """A header that cannot be read: a malformed YAML block, or a bold-line
    header the converter refuses. The message names the file."""


# ------------------------------------------------------------ YAML scalars

_BOOL = re.compile(r"^(?:yes|Yes|YES|no|No|NO|true|True|TRUE|false|False|FALSE|on|On|ON|off|Off|OFF)$")
_NULL = re.compile(r"^(?:~|null|Null|NULL|)$")
_INT = re.compile(
    r"^(?:[-+]?0b[0-1_]+|[-+]?0[0-7_]+|[-+]?(?:0|[1-9][0-9_]*)|[-+]?0x[0-9a-fA-F_]+"
    r"|[-+]?[1-9][0-9_]*(?::[0-5]?[0-9])+)$")
_FLOAT = re.compile(
    r"^(?:[-+]?(?:[0-9][0-9_]*)\.[0-9_]*(?:[eE][-+][0-9]+)?"
    r"|\.[0-9][0-9_]*(?:[eE][-+][0-9]+)?"
    r"|[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+\.[0-9_]*"
    r"|[-+]?\.(?:inf|Inf|INF)|\.(?:nan|NaN|NAN))$")
_DATE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
_STAMP = re.compile(
    r"^[0-9]{4}-[0-9][0-9]?-[0-9][0-9]?(?:[Tt]|[ \t]+)[0-9][0-9]?:[0-9][0-9]:[0-9][0-9]"
    r"(?:\.[0-9]*)?(?:[ \t]*(?:Z|[-+][0-9][0-9]?(?::[0-9][0-9])?))?$")


def resolve_plain(text: str) -> object:
    """The value YAML 1.1 gives an unquoted scalar: what PyYAML would load."""
    if _BOOL.match(text):
        return text.lower() in ("yes", "true", "on")
    if _NULL.match(text):
        return None
    if _DATE.match(text):
        try:
            return datetime.date(int(text[:4]), int(text[5:7]), int(text[8:10]))
        except ValueError:
            return text
    if _STAMP.match(text):
        return datetime.datetime(1970, 1, 1)
    if _INT.match(text):
        return 0
    if _FLOAT.match(text):
        return 0.0
    if text in ("<<", "="):
        return text
    return text


def type_name(value: object) -> str:
    if isinstance(value, bool):
        return "a boolean"
    if value is None:
        return "null"
    if isinstance(value, datetime.datetime):
        return "a timestamp"
    if isinstance(value, datetime.date):
        return "a date"
    if isinstance(value, int):
        return "a number"
    if isinstance(value, float):
        return "a number"
    if isinstance(value, str):
        return "a string"
    if isinstance(value, dict):
        return "a mapping"
    return "a list"


_START_UNSAFE = set("-?:,[]{}#&*!|>'\"%@`~=<")


def needs_quotes(value: str) -> bool:
    """Whether `value` cannot be written as a plain YAML scalar and still load
    as the same string."""
    if value == "":
        return True
    if value != value.strip():
        return True
    if value[0] in _START_UNSAFE:
        return True
    if ": " in value or " #" in value or value.endswith(":"):
        return True
    for ch in value:
        if not ch.isprintable():
            return True
    if value in ("---", "..."):
        return True
    return not isinstance(resolve_plain(value), str)


def quote(value: str) -> str:
    out: List[str] = ['"']
    for ch in value:
        if ch == "\\":
            out.append("\\\\")
        elif ch == '"':
            out.append('\\"')
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\t":
            out.append("\\t")
        elif ch == "\r":
            out.append("\\r")
        elif ch.isprintable():
            out.append(ch)
        elif ord(ch) <= 0xFF:
            out.append(f"\\x{ord(ch):02x}")
        elif ord(ch) <= 0xFFFF:
            out.append(f"\\u{ord(ch):04x}")
        else:
            out.append(f"\\U{ord(ch):08x}")
    out.append('"')
    return "".join(out)


def scalar(value: str) -> str:
    return quote(value) if needs_quotes(value) else value


def render_header(fields: Dict[str, str]) -> str:
    """`---`, the fields in schema order, `---`, one line each."""
    rows = ["---"]
    for name in FIELD_ORDER:
        if name in fields:
            rows.append(f"{name}: {scalar(fields[name])}")
    rows.append("---")
    return "\n".join(rows) + "\n"


_ESCAPES = {"0": "\0", "a": "\a", "b": "\b", "t": "\t", "\t": "\t", "n": "\n",
            "v": "\v", "f": "\f", "r": "\r", "e": "\x1b", " ": " ", '"': '"',
            "/": "/", "\\": "\\", "N": "\x85", "_": "\xa0", "L": "\u2028",
            "P": "\u2029"}
_KEY_LINE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):(?: (.*))?$")


def _parse_double(text: str) -> str:
    out: List[str] = []
    i = 1
    while i < len(text):
        ch = text[i]
        if ch == '"':
            if text[i + 1:].strip() != "":
                raise YamlError(f"text after the closing quote: {text[i + 1:]!r}")
            return "".join(out)
        if ch != "\\":
            out.append(ch)
            i += 1
            continue
        i += 1
        if i >= len(text):
            break
        esc = text[i]
        if esc in _ESCAPES:
            out.append(_ESCAPES[esc])
            i += 1
        elif esc in "xuU":
            width = {"x": 2, "u": 4, "U": 8}[esc]
            digits = text[i + 1:i + 1 + width]
            if len(digits) != width or not re.match(r"^[0-9a-fA-F]+$", digits):
                raise YamlError(f"bad \\{esc} escape")
            out.append(chr(int(digits, 16)))
            i += 1 + width
        else:
            raise YamlError(f"unknown escape \\{esc}")
    raise YamlError("unterminated double-quoted value")


def _parse_single(text: str) -> str:
    out: List[str] = []
    i = 1
    while i < len(text):
        ch = text[i]
        if ch == "'":
            if text[i + 1:i + 2] == "'":
                out.append("'")
                i += 2
                continue
            if text[i + 1:].strip() != "":
                raise YamlError(f"text after the closing quote: {text[i + 1:]!r}")
            return "".join(out)
        out.append(ch)
        i += 1
    raise YamlError("unterminated single-quoted value")


@dataclass
class Entry:
    key: str
    text: str
    value: object


def parse_flat(lines: Sequence[str]) -> List[Entry]:
    """The flat subset the converter writes: `key: value`, plain or quoted, one
    line each. A plain value takes the type YAML 1.1 would give it. Anything
    else (a nested block, a list, a flow collection, a duplicate key) is a
    YamlError."""
    entries: List[Entry] = []
    seen = set()
    for raw in lines:
        if raw.strip() == "":
            continue
        m = _KEY_LINE.match(raw)
        if m is None:
            raise YamlError(f"not a `key: value` line: {raw!r}")
        key, rest = m.group(1), m.group(2)
        if key in seen:
            raise YamlError(f"duplicate key {key!r}")
        seen.add(key)
        if rest is None or rest.strip() == "":
            entries.append(Entry(key, "", None))
            continue
        if rest[0] == '"':
            text = _parse_double(rest)
            entries.append(Entry(key, text, text))
        elif rest[0] == "'":
            text = _parse_single(rest)
            entries.append(Entry(key, text, text))
        else:
            if rest[0] in "[]{}|>&*!%@`,#?:" or rest.startswith("- "):
                raise YamlError(f"{key}: a value starting with {rest[0]!r} is outside the flat subset")
            text = rest
            cut = text.find(" #")
            if cut != -1:
                text = text[:cut]
            text = text.strip()
            if ": " in text or text.endswith(":"):
                raise YamlError(f"{key}: a plain value cannot hold ': '")
            entries.append(Entry(key, text, resolve_plain(text)))
    return entries


def split_header(text: str) -> Optional[Tuple[List[str], int]]:
    """(the lines between the leading `---` and the next `---`, the index of the
    line after the closing fence), or None when the file has no such block."""
    lines = text.split("\n")
    if not lines or lines[0] != "---":
        return None
    for j in range(1, len(lines)):
        if lines[j] == "---":
            return lines[1:j], j + 1
    return None


def parse_header(text: str) -> Dict[str, object]:
    block = split_header(text)
    if block is None:
        raise YamlError("no `---` header block at the top of the file")
    return {e.key: e.value for e in parse_flat(block[0])}


# --------------------------------------------------------- JSON Schema subset

_ANNOTATIONS = frozenset(("$schema", "$id", "$comment", "title", "description",
                          "default", "examples"))
_KEYWORDS = frozenset(("type", "properties", "required", "additionalProperties",
                       "enum", "const", "pattern", "minLength", "allOf", "if",
                       "then", "else", "not"))


def _is_type(value: object, name: str) -> bool:
    if name == "string":
        return isinstance(value, str)
    if name == "object":
        return isinstance(value, dict)
    if name == "array":
        return isinstance(value, list)
    if name == "boolean":
        return isinstance(value, bool)
    if name == "null":
        return value is None
    if name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if name == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    raise ValueError(f"unknown JSON Schema type {name!r}")


def as_dict(o: object) -> Dict[str, object]:
    if not isinstance(o, dict):
        raise ValueError("schema node is not an object")
    return cast(Dict[str, object], o)


def _check(inst: object, sch: object, path: str, errs: List[str]) -> None:
    """Validate `inst` against `sch`, appending `path: message` lines. Knows only
    the keywords in _KEYWORDS and refuses any other, so the schema cannot start
    using one this validator would silently skip."""
    if sch is True:
        return
    if sch is False:
        errs.append(f"{path}: not allowed here")
        return
    node = as_dict(sch)
    for key in node:
        if key not in _KEYWORDS and key not in _ANNOTATIONS:
            raise ValueError(f"schema keyword {key!r} is not implemented by adrplus.py")
    where = path or "(header)"
    if "type" in node:
        want = str(node["type"])
        if not _is_type(inst, want):
            hint = ""
            if want == "string" and not isinstance(inst, (dict, list)):
                hint = "; write the value in double quotes"
            errs.append(f"{where}: expected {want}, found {type_name(inst)}{hint}")
            return
    if "const" in node and inst != node["const"]:
        errs.append(f"{where}: must be {node['const']!r}")
    if "enum" in node:
        options = cast(List[object], node["enum"])
        if inst not in options:
            errs.append(f"{where}: {inst!r} is not one of {', '.join(str(o) for o in options)}")
    if "pattern" in node and isinstance(inst, str):
        if re.search(str(node["pattern"]), inst) is None:
            errs.append(f"{where}: {inst!r} does not match {node['pattern']}")
    if "minLength" in node and isinstance(inst, str):
        if len(inst) < int(cast(int, node["minLength"])):
            errs.append(f"{where}: must not be empty")
    if isinstance(inst, dict):
        data = cast(Dict[str, object], inst)
        for req in cast(List[str], node.get("required", [])):
            if req not in data:
                errs.append(f"{req}: required field is missing")
        props = as_dict(node["properties"]) if "properties" in node else {}
        for name, sub in props.items():
            if name in data:
                _check(data[name], sub, name, errs)
        if node.get("additionalProperties") is False:
            for name in data:
                if name not in props:
                    errs.append(f"{name}: unknown field")
    for sub in cast(List[object], node.get("allOf", [])):
        _check(inst, sub, path, errs)
    if "not" in node:
        inner: List[str] = []
        _check(inst, node["not"], path, inner)
        if not inner:
            errs.append(f"{where}: matches a pattern that is not allowed")
    if "if" in node:
        cond: List[str] = []
        _check(inst, node["if"], path, cond)
        branch = "then" if not cond else "else"
        if branch in node:
            sub_errs: List[str] = []
            _check(inst, node[branch], path, sub_errs)
            why = str(node.get("description", "")).strip()
            for e in sub_errs:
                errs.append(f"{e} ({why})" if why else e)


def validate(inst: object, schema: Dict[str, object]) -> List[str]:
    errs: List[str] = []
    _check(inst, schema, "", errs)
    return errs


# ------------------------------------------------------------ settings


@dataclass
class Settings:
    """What a project fills in (SPEC.md 4.2) for these tools. `decisions` and
    `archive` are relative to `root`; `schema` is a path."""
    root: pathlib.Path
    decisions: pathlib.Path
    archive: Optional[pathlib.Path]
    owner: Optional[str]
    schema: pathlib.Path


_OVERRIDES: Dict[str, str] = {}


def configure(decisions: Optional[str] = None, archive: Optional[str] = None,
              owner: Optional[str] = None, schema: Optional[str] = None) -> None:
    """Set the values that win over the decisions README, as the command line
    gives them. Calling it with no arguments clears them. `archive` of `none`
    means the project has no archive folder."""
    _OVERRIDES.clear()
    for key, value in (("decisions", decisions), ("archive", archive), ("owner", owner), ("schema", schema)):
        if value is not None:
            _OVERRIDES[key] = value


def find_decisions_dir(root: pathlib.Path) -> pathlib.Path:
    """The decisions folder relative to `root`: the configured one, else the first
    of DECISION_DIRS that exists, else the first of them."""
    if "decisions" in _OVERRIDES:
        return pathlib.Path(_OVERRIDES["decisions"])
    for rel in DECISION_DIRS:
        if (root / rel).is_dir():
            return pathlib.Path(rel)
    return pathlib.Path(DECISION_DIRS[0])


def readme_settings(folder: pathlib.Path) -> Dict[str, str]:
    """The rows of the settings table in `folder`/README.md, name (lowercase) to
    value. A missing README holds none."""
    path = folder / "README.md"
    if not path.exists():
        return {}
    rows: Dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").split("\n"):
        m = SETTING_ROW.match(line)
        if m is not None and m.group(2) != "" and set(m.group(1)) != {"-"}:
            rows.setdefault(m.group(1).strip().lower(), m.group(2))
    return rows


def settings(root: pathlib.Path) -> Settings:
    decisions = find_decisions_dir(root)
    rows = readme_settings(root / decisions)
    archive_text = _OVERRIDES.get("archive", rows.get("archive folder", "none"))
    archive = None if archive_text.strip().lower() in ("none", "") else pathlib.Path(archive_text.strip())
    owner = _OVERRIDES.get("owner", rows.get("owner"))
    if "schema" in _OVERRIDES:
        schema = pathlib.Path(_OVERRIDES["schema"])
    elif (root / decisions / "adr-plus.schema.json").exists():
        schema = root / decisions / "adr-plus.schema.json"
    else:
        schema = SHIPPED_SCHEMA
    return Settings(root, decisions, archive, owner, schema)


def settings_owner(root: pathlib.Path) -> Optional[str]:
    return settings(root).owner


def adr_paths(root: pathlib.Path) -> Tuple[List[pathlib.Path], List[pathlib.Path]]:
    """(the ADR files in the decisions folder, those in the archive folder), each
    sorted. A file counts when it is named like `ADR-012-some-title.md`."""
    cfg = settings(root)

    def listing(rel: Optional[pathlib.Path]) -> List[pathlib.Path]:
        if rel is None or not (root / rel).is_dir():
            return []
        return sorted(p for p in (root / rel).iterdir() if p.is_file() and ADR_FILE.match(p.name))

    return listing(cfg.decisions), listing(cfg.archive)


def load_schema(root: pathlib.Path) -> Dict[str, object]:
    return as_dict(json.loads(settings(root).schema.read_text(encoding="utf-8")))


# ------------------------------------------------------------ status codec


def consume_prefix(text: str) -> Tuple[str, str]:
    """(the leading glyph and bold tokens, the rest)."""
    pos = 0
    while True:
        m = PREFIX_TOKEN.match(text, pos)
        if m is None:
            return text[:pos], text[pos:]
        pos = m.end()


def word_regex(words: Sequence[str]) -> "re.Pattern[str]":
    ordered = sorted(words, key=len, reverse=True)
    return re.compile("(" + "|".join(re.escape(w) for w in ordered) + r")(?![A-Za-z])",
                      re.IGNORECASE)


def mapped_lead(rest: str) -> Optional[str]:
    """The older verdict word that `rest` begins with, as written, when it is
    one the S2 map rewrites; None otherwise."""
    m = word_regex(list(VERDICT_MAP)).match(rest)
    return m.group(1) if m is not None else None


def decode_status(verdict: str, note: str) -> str:
    """The Status wording (without `**Status:** `) the YAML says."""
    prefix, rest = consume_prefix(note)
    if mapped_lead(rest) is not None:
        return note
    if rest == "":
        tail = ""
    elif rest.startswith("— "):
        tail = " " + rest
    elif rest[0].isspace():
        tail = rest
    elif rest[0] == "\\":
        tail = rest[1:]
    else:
        tail = " — " + rest
    return prefix + verdict.upper() + tail


# ------------------------------------------------------------ the shared reader


def is_yaml(text: str) -> bool:
    """Whether the file opens with a `---` line, the start of a YAML header."""
    return text.split("\n", 1)[0] == "---"


def front_matter(text: str, name: str = "") -> Tuple[Optional[Dict[str, object]], int]:
    """(the parsed YAML block, the index of the first line after its closing
    `---`), or (None, 0) when the file does not open with `---`. Values keep the
    type YAML 1.1 would give a plain scalar, so a retyped value is visible to the
    schema. A block that never closes, or that the flat parser refuses, raises
    HeaderError naming `name`."""
    if not is_yaml(text):
        return None, 0
    where = name or "(text)"
    block = split_header(text)
    if block is None:
        raise HeaderError(f"{where}: the file opens with --- but the YAML block never closes")
    try:
        entries = parse_flat(block[0])
    except YamlError as exc:
        raise HeaderError(f"{where}: {exc}") from exc
    return {e.key: e.value for e in entries}, block[1]


def _converter() -> Any:
    """The module adr-yaml.py, loaded by path on first use. It imports this
    module, so it cannot be imported at the top of this one."""
    main = sys.modules.get("__main__")
    if main is not None and pathlib.Path(str(getattr(main, "__file__", ""))).name == "adr-yaml.py":
        return main
    cached = sys.modules.get("adr_yaml")
    if cached is not None:
        return cached
    spec = importlib.util.spec_from_file_location("adr_yaml", TOOLS / "adr-yaml.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load adr-yaml.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["adr_yaml"] = mod
    spec.loader.exec_module(mod)
    return mod


def header(text: str, name: str = "", owner: Optional[str] = None) -> Dict[str, object]:
    """The ADR's header as field name to value. A YAML ADR gives its YAML block.
    A bold-line ADR gives the keys the converter derives from its bold lines;
    `owner` stands in for the settings table's owner there (default: empty, since
    the owner is not read from the file). A malformed YAML block or a bold-line
    header the converter refuses raises HeaderError naming `name`."""
    data, _ = front_matter(text, name)
    if data is not None:
        return data
    who = owner if owner is not None else ""
    conv = _converter().convert_text(text, who, name)
    if conv.unparseable:
        raise HeaderError(f"{name or '(text)'}: {conv.unparseable}")
    return {str(k): str(v) for k, v in conv.fields.items()}


def text_field(h: Dict[str, object], key: str) -> str:
    """The string value of `key`, or "" when it is absent or not a string."""
    value = h.get(key)
    return value if isinstance(value, str) else ""


def status_wording(h: Dict[str, object]) -> str:
    """The Status wording `status` and `status-note` say together: the text that
    followed `**Status:** ` on the bold line."""
    return decode_status(text_field(h, "status"), text_field(h, "status-note"))


def built_rest(h: Dict[str, object]) -> str:
    """The text that followed `LANDED — ` on the bold Built line."""
    proof = text_field(h, "proof")
    owed = text_field(h, "owed")
    return f"{proof}; owed: {owed}" if owed else proof


def s2_status(word: str) -> Optional[str]:
    """The status word `word` stands for under the seven-word rule: one of the
    seven itself, or an older verdict mapped onto one; None for any other word."""
    low = word.strip().lower()
    if low in STATUS_WORDS:
        return low
    return VERDICT_MAP.get(low)
