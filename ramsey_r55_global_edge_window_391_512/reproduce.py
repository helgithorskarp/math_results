#!/usr/bin/env python3
"""One-command replay of the 391..512 global edge-window theorem."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile


DIRECTORY = "ramsey_r55_global_edge_window_391_512"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def invoke(command, expect_success=True):
    completed = subprocess.run(command, text=True, capture_output=True)
    if expect_success:
        need(completed.returncode == 0,
             "command failed: " + " ".join(map(str, command)) + "\n" +
             completed.stdout + completed.stderr)
    else:
        need(completed.returncode != 0, "corrupt certificate was accepted")
    return completed.stdout.strip()


def check_manifest(source):
    manifest = source / "SHA256SUMS"
    names = []
    for line in manifest.read_text().splitlines():
        expected, name = line.split("  ", 1)
        need(Path(name).name == name and name not in names, "manifest path")
        need(digest(source / name) == expected, "source hash " + name)
        names.append(name)
    actual = {path.name for path in source.iterdir() if path.is_file()}
    need(set(names) == actual - {"SHA256SUMS"}, "manifest file set")


def reproduce(root):
    root = Path(root).resolve()
    source = root / DIRECTORY
    parent = root / "ramsey_r55_regular18_overlap_exclusion"
    need(source.is_dir() and parent.is_dir(), "source/parent directory")
    check_manifest(source)
    expected_output = (source / "EXPECTED_OUTPUT.txt").read_text().strip()

    with tempfile.TemporaryDirectory(prefix="ramsey391-") as temporary:
        temporary = Path(temporary)
        generated = temporary / "CERTIFICATE.json"
        invoke([sys.executable, "-B", str(source / "produce.py"),
                "--parent", str(parent), "--output", str(generated)])
        need(generated.read_bytes() == (source / "CERTIFICATE.json").read_bytes(),
             "producer/certificate byte comparison")

        normal = invoke([sys.executable, "-B", str(source / "verify.py"),
                         "--parent", str(parent),
                         "--certificate", str(generated)])
        optimized = invoke([sys.executable, "-O", "-B", str(source / "verify.py"),
                            "--parent", str(parent),
                            "--certificate", str(generated)])
        need(normal == optimized == expected_output, "independent output")

        certificate = json.loads(generated.read_text())
        corrupt_window = temporary / "corrupt-window.json"
        changed = dict(certificate)
        changed["strengthened_edge_window"] = [390, 512]
        corrupt_window.write_text(json.dumps(changed))
        invoke([sys.executable, "-B", str(source / "verify.py"),
                "--parent", str(parent), "--certificate", str(corrupt_window)],
               expect_success=False)

        corrupt_deficit = temporary / "corrupt-deficit.json"
        changed = json.loads(generated.read_text())
        changed["overlap"]["minimum_required_common_deficit"] = 3
        corrupt_deficit.write_text(json.dumps(changed))
        invoke([sys.executable, "-B", str(source / "verify.py"),
                "--parent", str(parent), "--certificate", str(corrupt_deficit)],
               expect_success=False)

    print(expected_output)
    print("REPRODUCED_GLOBAL_GOOD43_EDGE_WINDOW_391_512")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    arguments = parser.parse_args()
    reproduce(arguments.root)
