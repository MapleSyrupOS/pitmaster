#!/usr/bin/env python3
"""sync-manifests.py: write every native package manifest from the one source (ADR-001, rule 4).

The source is .claude-plugin/plugin.json. From it this script writes:
  .codex-plugin/plugin.json           Codex's plugin manifest, pointing at ./skills/
  .agents/plugins/marketplace.json    Codex's marketplace, listing the plugin at the repository root
and checks .claude-plugin/marketplace.json, which is hand-written, against the source.

Usage:
  python3 scripts/sync-manifests.py           write the generated manifests
  python3 scripts/sync-manifests.py --check   exit 1 if any manifest has drifted (CI runs this)

Parity means: the same name, version, description, license and repository in every manifest, and every skill
folder under skills/ present (Codex reads the folder; Claude discovers it). Python 3.8+, standard library only.
"""
from __future__ import annotations

import json
import pathlib
import sys
from typing import Dict, List

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / ".claude-plugin" / "plugin.json"
CLAUDE_MARKET = ROOT / ".claude-plugin" / "marketplace.json"
CODEX_PLUGIN = ROOT / ".codex-plugin" / "plugin.json"
CODEX_MARKET = ROOT / ".agents" / "plugins" / "marketplace.json"

SHORT = "Grill the plan, record the decision, find the bottleneck, pick the budget and the models."
PROMPTS = [
    "bbq: ask me 12 questions before we start this refactor",
    "makeadr: let's make an ADR for how we version the API",
    "What's the bottleneck in this run right now?",
]


def dump(obj) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def skills() -> List[str]:
    return sorted(p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md"))


def codex_plugin(src: Dict) -> Dict:
    return {
        "name": src["name"],
        "version": src["version"],
        "description": src["description"],
        "author": src["author"],
        "homepage": src["homepage"],
        "repository": src["repository"],
        "license": src["license"],
        "keywords": src.get("keywords", []),
        "skills": "./skills/",
        "interface": {
            "displayName": src["name"],
            "shortDescription": SHORT,
            "longDescription": src["description"],
            "developerName": src["author"]["name"],
            "category": "Productivity",
            "capabilities": ["Read", "Write"],
            "websiteURL": src["homepage"],
            "defaultPrompt": PROMPTS,
        },
    }


def codex_market(src: Dict) -> Dict:
    return {
        "name": src["name"],
        "interface": {"displayName": src["name"]},
        "plugins": [{
            "name": src["name"],
            "source": {"source": "local", "path": "./"},
            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            "category": "Productivity",
        }],
    }


def check_claude_market(src: Dict) -> List[str]:
    problems = []
    market = json.loads(CLAUDE_MARKET.read_text(encoding="utf-8"))
    entries = [p for p in market.get("plugins", []) if p.get("name") == src["name"]]
    if len(entries) != 1:
        problems.append(f"{CLAUDE_MARKET.relative_to(ROOT)}: needs exactly one entry named {src['name']!r}")
    elif "version" in entries[0] and entries[0]["version"] != src["version"]:
        problems.append(f"{CLAUDE_MARKET.relative_to(ROOT)}: entry version differs from plugin.json")
    elif entries[0].get("source") not in ("./", "."):
        problems.append(f"{CLAUDE_MARKET.relative_to(ROOT)}: entry source must be the repository root")
    return problems


def main(argv: List[str]) -> int:
    src = json.loads(SOURCE.read_text(encoding="utf-8"))
    want = {CODEX_PLUGIN: dump(codex_plugin(src)), CODEX_MARKET: dump(codex_market(src))}
    problems = check_claude_market(src)
    if not skills():
        problems.append("skills/: no skill folders found")
    if "--check" in argv:
        for path, text in want.items():
            have = path.read_text(encoding="utf-8") if path.exists() else None
            if have != text:
                problems.append(f"{path.relative_to(ROOT)}: {'missing' if have is None else 'drifted'} "
                                "from .claude-plugin/plugin.json; run scripts/sync-manifests.py")
        for p in problems:
            print(p, file=sys.stderr)
        print(f"sync-manifests: {'FAIL' if problems else 'in step'} "
              f"({src['name']} {src['version']}, {len(skills())} skills)")
        return 1 if problems else 0
    for path, text in want.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        print(f"sync-manifests: wrote {path.relative_to(ROOT)}")
    for p in problems:
        print(p, file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
