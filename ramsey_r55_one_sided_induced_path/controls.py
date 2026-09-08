#!/usr/bin/env python3
"""Small exhaustive soundness check and deliberate certificate corruptions."""
import argparse
import itertools
import json
import subprocess
import sys
from pathlib import Path
from check_rup import Formula


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    root = Path(__file__).resolve().parent
    clauses = [[(i + 1) * sign for i, sign in enumerate(signs) if sign]
               for signs in itertools.product((-1, 0, 1), repeat=2)]
    assignments = list(itertools.product((False, True), repeat=2))

    def satisfied(clause, assignment):
        return any(assignment[abs(v) - 1] == (v > 0) for v in clause)

    trials = 0
    for word in range(1 << len(clauses)):
        chosen = [clause for bit, clause in enumerate(clauses) if word >> bit & 1]
        formula = Formula(2)
        for clause in chosen:
            formula.add(clause)
        models = [a for a in assignments if all(satisfied(c, a) for c in chosen)]
        for clause in clauses:
            if formula.rup(clause) and any(not satisfied(clause, model) for model in models):
                raise ValueError("RUP checker is unsound on a two-variable instance")
            trials += 1

    interpreter = [sys.executable] + (["-O"] if sys.flags.optimize else [])
    subprocess.run(interpreter + [str(root / "build.py"), "G2", "--out", str(args.out)], check=True,
                   stdout=subprocess.DEVNULL)
    original = args.out / "G2.cnf"
    lines = original.read_text().splitlines()
    header = lines[0].split()
    header[-1] = str(int(header[-1]) - 1)
    corrupted = args.out / "missing-clause.cnf"
    corrupted.write_text(" ".join(header) + "\n" + "\n".join(lines[2:]) + "\n")
    false_proof = args.out / "false.proof"
    false_proof.write_text("0\n")
    rejected = []
    for label, command in [
        ("missing physical constraint", ["audit.py", "G2", str(corrupted), "--out", str(args.out / "bad-audit.json")]),
        ("unjustified empty clause", ["check_rup.py", str(original), str(false_proof), "--out", str(args.out / "bad-proof.json")]),
    ]:
        completed = subprocess.run(interpreter + [str(root / command[0])] + command[1:],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if completed.returncode == 0:
            raise ValueError(f"Corruption unexpectedly accepted: {label}")
        (args.out / ("control-" + str(len(rejected)) + ".log")).write_text(completed.stdout + completed.stderr)
        rejected.append(label)
    result = {"two_variable_rup_soundness_checks": trials, "corruptions_rejected": rejected, "status": "PASS"}
    (args.out / "CONTROLS.json").write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
