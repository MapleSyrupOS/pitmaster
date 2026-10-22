#!/usr/bin/env python3
"""check-pins.py: verify that every pinned copy in a skill is byte-for-byte the release it names.

Two modes:
  files   each file: line says <sha256>  <local path>  <source path>; checks existence and hash.
  manifest: the folder beside the pin holds MANIFEST.sha256; checks hash, existence, extra files.

Usage:
  python3 scripts/check-pins.py                  check every .pin file under <root>/skills/
  python3 scripts/check-pins.py --against DIR    compare files-mode copies against DIR/<source path>
  python3 scripts/check-pins.py --self-test      build fixtures and verify internal logic
  python3 scripts/check-pins.py --root DIR       override the skills root

Exit status: 0 clean, 1 findings, 2 usage error. Python 3.8+, standard library only.
"""
from __future__ import annotations

import hashlib
import os
import pathlib
import re
import sys
import tempfile
from typing import Dict, List, Optional, Tuple


ROOT: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent

VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def find_pins(root: pathlib.Path) -> List[pathlib.Path]:
    pins: List[pathlib.Path] = []
    skills = root / "skills"
    if not skills.is_dir():
        return pins
    for p in sorted(skills.rglob("*.pin")):
        if p.is_file():
            pins.append(p)
    return pins


def _extract_keys(lines: List[str]) -> set:
    """Get all keys from a pin file."""
    keys: set = set()
    for l in lines:
        s = l.strip()
        if not s or s.startswith("#"):
            continue
        if ":" in s:
            k = s.split(":", 1)[0].strip()
            keys.add(k)
    return keys


def parse_pin(pin_path: pathlib.Path) -> Tuple[str, List[Tuple[str, str, str]], Optional[str], Dict[str, List[str]], List[Tuple[str, str]]]:
    """Parse a pin file. Returns (source, files_list, manifest_sha, extra_keys_map, findings)."""
    lines = pin_path.read_text(encoding="utf-8").splitlines()
    source: str = ""
    files_list: List[Tuple[str, str, str]] = []
    manifest_sha: Optional[str] = None
    extra_keys: Dict[str, List[str]] = {}
    findings: List[Tuple[str, str]] = []
    keys = _extract_keys(lines)

    for lineno, raw in enumerate(lines, start=1):
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            findings.append(("malformed", "line {}: no colon".format(lineno)))
            continue
        key, val = stripped.split(":", 1)
        key = key.strip()
        val = val.strip()

        if key == "source":
            if val:
                source = val
            else:
                findings.append(("malformed", "line {}: source is empty".format(lineno)))
        elif key == "version":
            if not VERSION_RE.match(val):
                findings.append(("malformed", "line {}: version '{}' does not match \\d+.\\d+.\\d+".format(lineno, val)))
        elif key == "ref-kind":
            if val not in ("commit", "tag"):
                findings.append(("malformed", "line {}: ref-kind must be 'commit' or 'tag'".format(lineno)))
        elif key == "ref":
            pass
        elif key == "file":
            parts = val.split()
            if len(parts) != 3:
                findings.append(("malformed", "line {}: file: expects 3 whitespace-separated fields".format(lineno)))
            else:
                h, local, src = parts[0], parts[1], parts[2]
                if not SHA256_RE.match(h):
                    findings.append(("malformed", "line {}: sha256 '{}' is invalid".format(lineno, h)))
                files_list.append((h, local, src))
        elif key == "manifest-sha256":
            manifest_sha = val
        else:
            extra_keys.setdefault(key, []).append(val)
            findings.append(("unknown key", "line {}: '{}' = '{}'".format(lineno, key, val)))

    # Post-parse required-key checks
    if not source:
        if "source" not in keys:
            findings.append(("malformed", "missing required key 'source'"))
    if "version" not in keys:
        findings.append(("malformed", "missing required key 'version'"))
    if "ref-kind" not in keys:
        findings.append(("malformed", "missing required key 'ref-kind'"))
    if "ref" not in keys:
        findings.append(("malformed", "missing required key 'ref'"))

    # ref validation
    ref_val = None
    ref_kind_val = None
    ver_val = None
    for l in lines:
        s = l.strip()
        if not s or s.startswith("#"):
            continue
        if ":" in s:
            k, v = s.split(":", 1)
            if k.strip() == "ref":
                ref_val = v.strip()
            elif k.strip() == "ref-kind":
                ref_kind_val = v.strip()
            elif k.strip() == "version":
                ver_val = v.strip()

    if ref_kind_val == "tag" and ref_val is not None and ver_val is not None:
        expected_tag = "v" + ver_val
        if ref_val != expected_tag:
            findings.append(("malformed", "tag ref '{}' must be v{} (derived from version)".format(ref_val, ver_val)))
    elif ref_kind_val == "commit" and ref_val is not None:
        if not COMMIT_RE.match(ref_val):
            findings.append(("malformed", "commit ref '{}' must be 40 hex chars".format(ref_val)))

    # Must have file lines or manifest-sha256, never both, never neither
    has_files = len(files_list) > 0
    has_manifest = manifest_sha is not None
    if has_files and has_manifest:
        findings.append(("malformed", "pin has both file: lines and manifest-sha256"))
    if not has_files and not has_manifest:
        findings.append(("malformed", "pin has neither file: lines nor manifest-sha256"))

    return source, files_list, manifest_sha, extra_keys, findings


def check_files_mode(
    pin_path: pathlib.Path,
    root: pathlib.Path,
    against: Optional[pathlib.Path],
) -> List[Tuple[pathlib.Path, str, str]]:
    findings: List[Tuple[pathlib.Path, str, str]] = []
    source, files_list, manifest_sha, extra_keys, parse_findings = parse_pin(pin_path)

    for reason, detail in parse_findings:
        if reason == "malformed":
            findings.append((pin_path, pin_path, "malformed: {}".format(detail)))
        else:
            findings.append((pin_path, pin_path, "{}: {}".format(reason, detail)))

    if parse_findings:
        return findings

    pin_dir = pin_path.parent
    for sha_expected, local_rel, source_path in files_list:
        local_path = pin_dir / local_rel

        if not local_path.is_file():
            findings.append((pin_path, local_path, "missing"))
            continue

        actual = sha256_bytes(local_path.read_bytes())
        if actual != sha_expected:
            findings.append((pin_path, local_path, "changed"))
            continue

        if against is not None:
            against_path = against / source_path
            if not against_path.is_file():
                findings.append((pin_path, local_path, "differs from source: {} is not in the source".format(source_path)))
            elif against_path.read_bytes() != local_path.read_bytes():
                findings.append((pin_path, local_path, "differs from source"))

    return findings


def check_manifest_mode(
    pin_path: pathlib.Path,
    root: pathlib.Path,
) -> List[Tuple[pathlib.Path, str, str]]:
    findings: List[Tuple[pathlib.Path, str, str]] = []
    source, files_list, manifest_sha, extra_keys, parse_findings = parse_pin(pin_path)

    for reason, detail in parse_findings:
        if reason == "malformed":
            findings.append((pin_path, pin_path, "malformed: {}".format(detail)))
        else:
            findings.append((pin_path, pin_path, "{}: {}".format(reason, detail)))

    if parse_findings:
        return findings

    stem = pin_path.stem
    manifest_folder = pin_path.parent / stem

    if manifest_sha is None:
        findings.append((pin_path, pin_path, "malformed: no manifest-sha256 in pin"))
        return findings

    manifest_path = manifest_folder / "MANIFEST.sha256"
    if not manifest_path.is_file():
        findings.append((pin_path, pin_path, "malformed: MANIFEST.sha256 not found"))
        return findings

    manifest_bytes = manifest_path.read_bytes()
    if sha256_bytes(manifest_bytes) != manifest_sha:
        findings.append((pin_path, pin_path, "manifest changed"))

    # Parse manifest lines: <sha256>  <relative path>
    manifest_text = manifest_bytes.decode("utf-8")
    manifest_lines = manifest_text.splitlines()
    listed: Dict[str, str] = {}
    for mline in manifest_lines:
        s = mline.strip()
        if not s or s.startswith("#"):
            continue
        # Two spaces separator: sha256<two spaces>path
        m = re.match(r"([0-9a-f]{64})\s{2}(.+)", s)
        if m:
            listed[m.group(2)] = m.group(1)

    # Check each listed file
    for rel_path, expected_sha in listed.items():
        fp = manifest_folder / rel_path
        if not fp.is_file():
            findings.append((pin_path, fp, "missing"))
            continue
        actual = sha256_bytes(fp.read_bytes())
        if actual != expected_sha:
            findings.append((pin_path, fp, "changed"))

    # Check for extra files (not in manifest, not MANIFEST.sha256, not __pycache__, not .pyc)
    if manifest_folder.is_dir():
        for p in sorted(manifest_folder.rglob("*")):
            if p.is_file():
                if p.name == "MANIFEST.sha256":
                    continue
                rel = p.relative_to(manifest_folder)
                if "__pycache__" in rel.parts or p.suffix == ".pyc":
                    continue
                if rel.as_posix() not in listed:
                    findings.append((pin_path, p, "extra"))

    # VERSION check
    version_path = manifest_folder / "VERSION"
    if version_path.is_file():
        ver_content = version_path.read_text(encoding="utf-8").strip()
        lines = pin_path.read_text(encoding="utf-8").splitlines()
        ver_from_pin = None
        for l in lines:
            s = l.strip()
            if not s or s.startswith("#"):
                continue
            if ":" in s:
                k, v = s.split(":", 1)
                if k.strip() == "version":
                    ver_from_pin = v.strip()
        if ver_from_pin and ver_content != ver_from_pin:
            findings.append((pin_path, version_path, "version disagrees"))

    return findings


def run_check(root: pathlib.Path, against: Optional[pathlib.Path]) -> int:
    pins = find_pins(root)
    all_findings: List[Tuple[pathlib.Path, str, str]] = []
    pin_count = 0
    file_count = 0

    for pin_path in pins:
        pin_count += 1
        try:
            source, files_list, manifest_sha, extra_keys, parse_findings = parse_pin(pin_path)
        except Exception as e:
            all_findings.append((pin_path, pin_path, "malformed: {}".format(e)))
            continue

        if manifest_sha is not None:
            m_findings = check_manifest_mode(pin_path, root)
            all_findings.extend(m_findings)
            # Count files from manifest listing
            listed_set = set()
            _mp = pin_path.parent / pin_path.stem / "MANIFEST.sha256"
            if not parse_findings and _mp.is_file():
                manifest_bytes = _mp.read_bytes()
                for mline in manifest_bytes.decode("utf-8").splitlines():
                    m = re.match(r"([0-9a-f]{64})\s{2}(.+)", mline.strip())
                    if m:
                        listed_set.add(m.group(2))
            file_count += len(listed_set)
        elif files_list:
            file_count += len(files_list)
            f_findings = check_files_mode(pin_path, root, against)
            all_findings.extend(f_findings)

    # Output
    for pin_path, file_path, reason in all_findings:
        try:
            rel_pin = pin_path.relative_to(root)
        except ValueError:
            rel_pin = pin_path
        try:
            rel_file = file_path.relative_to(root)
        except ValueError:
            rel_file = file_path
        pin_str = str(rel_pin).replace(os.sep, "/")
        file_str = str(rel_file).replace(os.sep, "/")
        print("check-pins: {}: {} -- {}".format(pin_str, file_str, reason))

    if all_findings:
        print("check-pins: FAIL -- {} problem(s) across {} pin(s)".format(len(all_findings), pin_count))
        return 1
    else:
        print("check-pins: PASS -- {} pin(s), {} file(s)".format(pin_count, file_count))
        return 0


def self_test() -> int:
    cases_passed = 0
    cases_total = 0

    def check_case(name, builder_fn, expected_exit, expected_reasons):
        nonlocal cases_passed, cases_total
        cases_total += 1
        tmp = tempfile.TemporaryDirectory()
        try:
            fake_root = pathlib.Path(tmp.name)
            builder_fn(fake_root)
            import io
            import contextlib

            old_stdout = sys.stdout
            stdout_capture = io.StringIO()
            try:
                with contextlib.redirect_stdout(stdout_capture):
                    rc = run_check(fake_root, None)
            except SystemExit as e:
                rc = e.code if e.code is not None else 1

            stdout_text = stdout_capture.getvalue()

            if rc != expected_exit:
                print("FAIL {}: expected exit {}, got {}".format(name, expected_exit, rc))
                return

            for reason_word in expected_reasons:
                if reason_word not in stdout_text:
                    print("FAIL {}: expected '{}' in output".format(name, reason_word))
                    return

            cases_passed += 1
            print("PASS {}".format(name))
        finally:
            tmp.cleanup()

    def make_pin(path: pathlib.Path, content: str) -> pathlib.Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def make_file(path: pathlib.Path, content: bytes) -> pathlib.Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return path

    def write_manifest(path: pathlib.Path, lines: List[str]) -> str:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return sha256_bytes(path.read_bytes())

    # --- clean-files ---
    def build_clean_files(root):
        skills = root / "skills"
        sha = sha256_bytes(b"hello")
        content = "source: example/pitmaster-shed\nversion: 0.1.0\nref-kind: commit\nref: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\nfile: {}  local.txt  src/local.txt\n".format(sha)
        make_pin(skills / "my-skill.pin", content)
        make_file(skills / "local.txt", b"hello")

    check_case("clean-files", build_clean_files, 0, [])

    # --- clean-manifest ---
    def build_clean_manifest(root):
        skills = root / "skills"
        manifest_dir = skills / "adr-plus"
        manifest_dir.mkdir(parents=True, exist_ok=True)
        listed_file = manifest_dir / "doc.txt"
        listed_file.write_bytes(b"doc content")
        (manifest_dir / "VERSION").write_text("0.1.0\n", encoding="utf-8")
        manifest_path = manifest_dir / "MANIFEST.sha256"
        manifest_sha = write_manifest(manifest_path, ["{}  {}".format(sha256_bytes((manifest_dir / n).read_bytes()), n)
                                                      for n in ("VERSION", "doc.txt")])
        pin_content = "source: example/adr-plus\nversion: 0.1.0\nref-kind: tag\nref: v0.1.0\nmanifest-sha256: {}\n".format(manifest_sha)
        make_pin(skills / "adr-plus.pin", pin_content)

    check_case("clean-manifest", build_clean_manifest, 0, [])

    # --- no-pins ---
    def build_no_pins(root):
        (root / "skills").mkdir(parents=True, exist_ok=True)

    check_case("no-pins", build_no_pins, 0, [])

    # --- changed-byte ---
    def build_changed_byte(root):
        skills = root / "skills"
        sha = sha256_bytes(b"hello")
        content = "source: example/test\nversion: 0.1.0\nref-kind: commit\nref: bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\nfile: {}  local.txt  src/local.txt\n".format(sha)
        make_pin(skills / "my-skill.pin", content)
        make_file(skills / "local.txt", b"world")

    check_case("changed-byte", build_changed_byte, 1, ["skills/local.txt -- changed"])

    # --- missing-file ---
    def build_missing_file(root):
        skills = root / "skills"
        sha = sha256_bytes(b"hello")
        content = "source: example/test\nversion: 0.1.0\nref-kind: commit\nref: bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\nfile: {}  local.txt  src/local.txt\n".format(sha)
        make_pin(skills / "my-skill.pin", content)
        # local.txt not created

    check_case("missing-file", build_missing_file, 1, ["skills/local.txt -- missing"])

    # --- extra-file ---
    def build_extra_file(root):
        skills = root / "skills"
        manifest_dir = skills / "my-skill"
        manifest_dir.mkdir(parents=True, exist_ok=True)
        listed_file = manifest_dir / "doc.txt"
        listed_file.write_bytes(b"doc content")
        (manifest_dir / "VERSION").write_text("0.1.0\n", encoding="utf-8")
        manifest_sha = write_manifest(manifest_dir / "MANIFEST.sha256",
                                      ["{}  {}".format(sha256_bytes((manifest_dir / n).read_bytes()), n)
                                       for n in ("VERSION", "doc.txt")])
        pin_content = "source: example/my-skill\nversion: 0.1.0\nref-kind: tag\nref: v0.1.0\nmanifest-sha256: {}\n".format(manifest_sha)
        make_pin(skills / "my-skill.pin", pin_content)
        (manifest_dir / "extra.txt").write_text("extra", encoding="utf-8")

    check_case("extra-file", build_extra_file, 1, ["skills/my-skill/extra.txt -- extra"])

    # --- version-disagrees ---
    def build_version_disagrees(root):
        skills = root / "skills"
        manifest_dir = skills / "my-skill"
        manifest_dir.mkdir(parents=True, exist_ok=True)
        listed_file = manifest_dir / "doc.txt"
        listed_file.write_bytes(b"doc content")
        (manifest_dir / "VERSION").write_text("0.1.1\n", encoding="utf-8")
        manifest_sha = write_manifest(manifest_dir / "MANIFEST.sha256",
                                      ["{}  {}".format(sha256_bytes((manifest_dir / n).read_bytes()), n)
                                       for n in ("VERSION", "doc.txt")])
        pin_content = "source: example/my-skill\nversion: 0.1.0\nref-kind: tag\nref: v0.1.0\nmanifest-sha256: {}\n".format(manifest_sha)
        make_pin(skills / "my-skill.pin", pin_content)

    check_case("version-disagrees", build_version_disagrees, 1, ["skills/my-skill/VERSION -- version disagrees"])

    # --- tag-disagrees ---
    def build_tag_disagrees(root):
        skills = root / "skills"
        manifest_dir = skills / "my-skill"
        manifest_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = manifest_dir / "MANIFEST.sha256"
        manifest_path.write_text("aaa  doc.txt\n", encoding="utf-8")
        pin_content = "source: example/my-skill\nversion: 0.1.0\nref-kind: tag\nref: v0.2.0\nmanifest-sha256: 0000000000000000000000000000000000000000000000000000000000000000\n"
        make_pin(skills / "my-skill.pin", pin_content)

    check_case("tag-disagrees", build_tag_disagrees, 1, ["malformed"])

    # --- manifest-changed ---
    def build_manifest_changed(root):
        skills = root / "skills"
        manifest_dir = skills / "my-skill"
        manifest_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = manifest_dir / "MANIFEST.sha256"
        manifest_path.write_text("aaa  doc.txt\nbbb  stuff.txt\n", encoding="utf-8")
        pin_content = "source: example/my-skill\nversion: 0.1.0\nref-kind: tag\nref: v0.1.0\nmanifest-sha256: 0000000000000000000000000000000000000000000000000000000000000000\n"
        make_pin(skills / "my-skill.pin", pin_content)
        (manifest_dir / "VERSION").write_text("0.1.0\n", encoding="utf-8")

    check_case("manifest-changed", build_manifest_changed, 1, ["manifest changed"])

    # --- unknown-key ---
    def build_unknown_key(root):
        skills = root / "skills"
        manifest_dir = skills / "my-skill"
        manifest_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = manifest_dir / "MANIFEST.sha256"
        manifest_path.write_text("aaa  doc.txt\n", encoding="utf-8")
        pin_content = "source: example/my-skill\nversion: 0.1.0\nref-kind: tag\nref: v0.1.0\ncolour: red\nmanifest-sha256: 0000000000000000000000000000000000000000000000000000000000000000\n"
        make_pin(skills / "my-skill.pin", pin_content)

    check_case("unknown-key", build_unknown_key, 1, ["skills/my-skill.pin -- unknown key"])

    # --- against-differs ---
    def build_against_differs(root):
        skills = root / "skills"
        local_content = b"hello world"
        sha = sha256_bytes(local_content)
        pin_content = "source: example/my-skill\nversion: 0.1.0\nref-kind: commit\nref: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\nfile: {}  local.txt  src/local.txt\n".format(sha)
        make_pin(skills / "my-skill.pin", pin_content)
        make_file(skills / "local.txt", local_content)

        against_dir = root / "against_checkout"
        src_dir = against_dir / "src"
        src_dir.mkdir(parents=True, exist_ok=True)
        make_file(src_dir / "local.txt", b"different content")

    # Run with --against
    cases_total += 1
    tmp = tempfile.TemporaryDirectory()
    try:
        fake_root = pathlib.Path(tmp.name)
        build_against_differs(fake_root)
        against = fake_root / "against_checkout"
        import io, contextlib
        stdout_capture = io.StringIO()
        with contextlib.redirect_stdout(stdout_capture):
            rc = run_check(fake_root, against)
        stdout_text = stdout_capture.getvalue()

        if rc == 1 and "differs from source" in stdout_text:
            cases_passed += 1
            print("PASS against-differs")
        else:
            print("FAIL against-differs: expected exit 1 with 'differs from source', got rc={} text={}".format(rc, repr(stdout_text[:200])))
    finally:
        tmp.cleanup()

    if cases_passed != cases_total:
        print("check-pins: self-test FAIL -- {} of {} cases failed".format(cases_total - cases_passed, cases_total))
        return 1
    print("check-pins: self-test PASS -- {} of {} cases passed".format(cases_passed, cases_total))
    return 0


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="check-pins.py: verify pinned copies match their releases")
    parser.add_argument("--root", type=pathlib.Path, default=None, help="Root directory for skills/")
    parser.add_argument("--against", type=str, default=None, help="Directory containing source checkout")
    parser.add_argument("--self-test", action="store_true", help="Run self-test suite")
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    root = args.root if args.root else ROOT
    against: Optional[pathlib.Path] = None
    if args.against is not None:
        against = pathlib.Path(args.against)
        if not against.is_dir():
            print("check-pins: usage error: --against '{}' is not a directory".format(args.against), file=sys.stderr)
            return 2

    return run_check(root, against)


if __name__ == "__main__":
    sys.exit(main())
