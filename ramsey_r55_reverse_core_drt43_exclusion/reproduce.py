#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent


def run(command: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=check)


def main() -> None:
    expected_text = (HERE / "EXPECTED.txt").read_text(encoding="ascii")
    expected_json = json.loads((HERE / "EXPECTED.json").read_text(encoding="ascii"))
    source = str(HERE / "enumerate.cpp")
    core = str(HERE / "core.edges")
    verifier = str(HERE / "verify.py")
    with tempfile.TemporaryDirectory(prefix="r55-drt43-") as tmp:
        tmp_path = pathlib.Path(tmp)
        release = str(tmp_path / "enumerate")
        ubsan = str(tmp_path / "enumerate-ubsan")
        run(["g++", "-O3", "-std=c++20", "-Wall", "-Wextra", "-Werror",
             "-pedantic", source, "-o", release])
        result = run([release, core])
        if result.stdout != expected_text or result.stderr:
            raise RuntimeError("release transcript mismatch")
        run(["g++", "-O1", "-g", "-std=c++20", "-Wall", "-Wextra", "-Werror",
             "-pedantic", "-fsanitize=undefined", "-fno-omit-frame-pointer",
             source, "-o", ubsan])
        checked = run([ubsan, core])
        if checked.stdout != expected_text or checked.stderr:
            raise RuntimeError("UBSan transcript mismatch")

        py = run([sys.executable, "-B", verifier, core])
        if json.loads(py.stdout) != expected_json or py.stderr:
            raise RuntimeError("independent checker mismatch")
        py_opt = run([sys.executable, "-B", "-O", verifier, core])
        if json.loads(py_opt.stdout) != expected_json or py_opt.stderr:
            raise RuntimeError("optimized independent checker mismatch")

        original = (HERE / "core.edges").read_text(encoding="ascii").splitlines()
        controls = {
            "bad_header": ["21 97", *original[1:]],
            "duplicate": [original[0], original[1], original[1], *original[3:]],
            "truncated": original[:-1],
        }
        for name, lines in controls.items():
            damaged = tmp_path / f"{name}.edges"
            damaged.write_text("\n".join(lines) + "\n", encoding="ascii")
            for command in ([release, str(damaged)], [sys.executable, "-B", verifier, str(damaged)]):
                outcome = run(command, check=False)
                if outcome.returncode == 0:
                    raise RuntimeError(f"{name} control was accepted by {command[0]}")

    print("REPRODUCED_REVERSE_CORE_DRT43_EXCLUSION")


if __name__ == "__main__":
    main()
