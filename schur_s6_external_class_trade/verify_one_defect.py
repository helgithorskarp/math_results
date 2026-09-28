"""Certify that three seed classes cannot be traded to at most one defect."""

import argparse
import hashlib
import itertools
import json
import subprocess
import tempfile
from pathlib import Path

from pysat.solvers import Solver

from verify import HERE, N, load_seed, triples, var


def encode(old, group):
    free = {v for v in range(1, N + 1) if old[v] in group}
    clauses = []
    for v in sorted(free):
        clauses.append([var(v, c) for c in range(1, 7)])
        for c in range(1, 7):
            for d in range(c + 1, 7):
                clauses.append([-var(v, c), -var(v, d)])

    selectors = []
    top = 6 * N
    for edge in triples():
        fixed = {old[v] for v in edge if v not in free}
        if len(fixed) >= 2:
            continue
        top += 1
        selector = top
        selectors.append(selector)
        moving = [v for v in edge if v in free]
        if fixed:
            c = next(iter(fixed))
            clauses.append([selector] + [-var(v, c) for v in moving])
        else:
            for c in range(1, 7):
                clauses.append([selector] + [-var(v, c) for v in moving])

    # Sinz sequential at-most-one: prefix variable s_i records whether
    # a selector among t_0,...,t_i may be true.
    prefixes = []
    for _ in range(len(selectors) - 1):
        top += 1
        prefixes.append(top)
    for i, selector in enumerate(selectors):
        if i < len(prefixes):
            clauses.append([-selector, prefixes[i]])
        if i > 0:
            clauses.append([-selector, -prefixes[i - 1]])
        if 0 < i < len(prefixes):
            clauses.append([-prefixes[i - 1], prefixes[i]])
    return clauses, len(free), len(selectors), top


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def check_case(old, group, cadical, drat_trim):
    clauses, free, active_edges, variables = encode(old, {int(c) for c in group})
    with tempfile.TemporaryDirectory(prefix=f"schur-atmost1-{group}-") as temp:
        cnf = Path(temp) / "case.cnf"
        proof = Path(temp) / "case.drat"
        with cnf.open("w", encoding="ascii", newline="\n") as out:
            out.write(f"p cnf {variables} {len(clauses)}\n")
            for clause in clauses:
                out.write(" ".join(map(str, clause)) + " 0\n")

        if group == "124":
            solved = subprocess.run(
                [str(cadical), "-q", "--no-binary", str(cnf), str(proof)],
                text=True, capture_output=True, check=False,
            )
            if solved.returncode != 20 or "s UNSATISFIABLE" not in solved.stdout:
                raise RuntimeError(f"{group}: CaDiCaL did not prove UNSAT: {solved.stdout} {solved.stderr}")
            solver_name = "cadical-1.9.5-cli"
        else:
            with Solver(name="glucose3", bootstrap_with=clauses, with_proof=True) as solver:
                if solver.solve() is not False:
                    raise RuntimeError(f"{group}: Glucose3 did not prove UNSAT")
                proof_lines = solver.get_proof()
            with proof.open("w", encoding="ascii", newline="\n") as out:
                for line in proof_lines:
                    out.write(line + "\n")
            solver_name = "glucose3-pysat-1.9.dev15"

        checked = subprocess.run(
            [str(drat_trim), str(cnf), str(proof)],
            text=True, capture_output=True, check=False,
        )
        if checked.returncode != 0 or "s VERIFIED" not in checked.stdout:
            raise RuntimeError(f"{group}: DRAT-trim rejected proof: {checked.stdout} {checked.stderr}")
        return {
            "group": group,
            "free": free,
            "active_edges": active_edges,
            "variables": variables,
            "clauses": len(clauses),
            "solver": solver_name,
            "cnf_sha256": sha256(cnf),
            "proof_sha256": sha256(proof),
            "proof_bytes": proof.stat().st_size,
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cadical", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--group", action="append", help="check selected triple(s), default all ten")
    args = parser.parse_args()
    expected = {row["group"]: row for row in json.loads((HERE / "expected_one_defect.json").read_text())}
    groups = ["".join(map(str, triple)) for triple in itertools.combinations(range(1, 7), 3) if 4 in triple]
    assert set(groups) == set(expected)
    selected = args.group or groups
    if any(group not in expected for group in selected):
        parser.error("--group must be one of " + ",".join(groups))
    old = load_seed()
    for group in selected:
        result = check_case(old, group, args.cadical, args.drat_trim)
        assert result == expected[group], f"{group}: regenerated result differs from expected manifest"
        print(f"{group}: UNSAT, DRAT VERIFIED, active_edges={result['active_edges']}, proof_bytes={result['proof_bytes']}", flush=True)
    print(f"PASS at_most_one_defect_trades_unsat={len(selected)} drat_verified={len(selected)}")


if __name__ == "__main__":
    main()
