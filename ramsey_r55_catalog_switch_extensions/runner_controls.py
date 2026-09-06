#!/usr/bin/env python3
"""File-boundary controls; no solver executable exists in these tests."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from physical import catalog, require


def main():
    source = Path(__file__).resolve().parent
    record = catalog(source/"r55_42some.g6")[0]
    with tempfile.TemporaryDirectory(prefix="r55-runner-controls-") as directory:
        root = Path(directory)
        def invoke(name):
            folder = root/name
            command = [sys.executable, "-B", str(source/"parallel_batch.py"), str(folder)]
            for option in ["generator", "kissat", "drat-trim", "checker"]:
                command.extend(["--"+option, str(root/"intentionally-absent-executable")])
            return subprocess.run(command, capture_output=True, text=True, timeout=30)
        stopped = root/"stop"
        stopped.mkdir()
        (stopped/"STOP").write_text("Stop before any case.\n")
        result = invoke("stop")
        require(result.returncode == 0, result.stderr)
        require(json.loads((stopped/"parallel_stopped.json").read_text()) ==
                {"status": "STOPPED_DURING_PREFLIGHT", "parent": 0}, "Bad stop boundary")
        require(not (stopped/"parent000").exists(), "Stop started a case")
        for status in ["NO_CONCLUSION", "UNSAT_PROOF_PENDING", "STARTED"]:
            folder = root/status/"parent000"
            folder.mkdir(parents=True)
            text = json.dumps({"parent": 0, "seed": record, "status": status})
            (folder/"result.json").write_text(text)
            result = invoke(status)
            require(result.returncode != 0 and "Unresolved prior case; no retry" in result.stderr,
                    "Unresolved case not refused")
            require((folder/"result.json").read_text() == text and not (folder/"solver.log").exists(),
                    "Unresolved case mutated")
        interrupted = root/"interrupted"/"parent000"
        interrupted.mkdir(parents=True)
        (interrupted/"solver.log").write_text("Invocation already begun.\n")
        result = invoke("interrupted")
        require(result.returncode != 0 and "Interrupted prior solver; no retry" in result.stderr,
                "Interrupted solver not refused")
    print(json.dumps({"status": "PASS", "stop_before_parent0": True,
                      "unresolved_statuses_refused": 3, "interrupted_solver_refused": True,
                      "solver_invocations": 0}))


if __name__ == "__main__":
    main()
