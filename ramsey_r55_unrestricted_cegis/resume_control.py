#!/usr/bin/env python3
"""Exercise semantic checkpoint continuation without retaining scratch state."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import tempfile


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def result(output: str) -> dict[str, str]:
    rows = [line for line in output.splitlines() if line.startswith("RESULT ")]
    require(len(rows) == 1, "producer did not emit exactly one RESULT")
    return dict(token.split("=", 1) for token in rows[0].split()[1:])


def checkpoint_header(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="ascii").splitlines()
    require(lines and lines[0] == "R55_CEGIS_CHECKPOINT_V1",
            "wrong checkpoint header")
    fields: dict[str, str] = {}
    for line in lines[1:14]:
        key, value = line.split(" ", 1)
        fields[key] = value
    return fields


def invoke(executable: Path, rounds: int, checkpoint: Path) -> dict[str, str]:
    command = [str(executable), "43", "43018", str(rounds), "100", "2000",
               "18", "18", "24", str(checkpoint)]
    completed = subprocess.run(command, text=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, check=False)
    if completed.returncode != 0:
        raise RuntimeError(completed.stdout + completed.stderr)
    parsed = result(completed.stdout)
    require(parsed["status"] == "INCOMPLETE",
            "resume control unexpectedly reached a terminal target result")
    return parsed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("executable", type=Path)
    args = parser.parse_args()
    executable = args.executable.resolve()
    require(executable.is_file(), "producer executable not found")
    with tempfile.TemporaryDirectory(prefix="r55-cegis-resume-") as name:
        checkpoint = Path(name) / "state.checkpoint"
        first = invoke(executable, 2, checkpoint)
        first_clauses = int(first["clauses_added"])
        header = checkpoint_header(checkpoint)
        require(header["rounds_completed"] == "2", "first checkpoint round mismatch")
        require(int(header["clauses_added"]) == first_clauses,
                "first checkpoint clause mismatch")

        second = invoke(executable, 4, checkpoint)
        second_clauses = int(second["clauses_added"])
        header = checkpoint_header(checkpoint)
        require(second["rounds"] == "4", "continuation did not reach round four")
        require(header["rounds_completed"] == "4", "continued checkpoint mismatch")
        require(second_clauses > first_clauses,
                "continuation did not extend explicit clause set")
        require(int(header["clauses_added"]) == second_clauses,
                "continued checkpoint clause mismatch")
    print("RESUME_CONTROL status=PASS first_rounds=2 final_rounds=4 "
          f"first_clauses={first_clauses} final_clauses={second_clauses}")


if __name__ == "__main__":
    main()
