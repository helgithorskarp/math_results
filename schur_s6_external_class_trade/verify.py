"""Regenerate and independently check ten Schur class-trade UNSAT proofs."""

import argparse
import hashlib
import itertools
import json
import subprocess
import tempfile
from pathlib import Path

from pysat.solvers import Solver


N = 537
HERE = Path(__file__).resolve().parent
SEED = HERE / "seed537.txt"
SEED_SHA256 = "58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3"


def var(v, c):
    return 6 * (v - 1) + c


def triples():
    for x in range(1, N + 1):
        for y in range(x, N + 1 - x):
            yield (x, x + y) if x == y else (x, y, x + y)


def load_seed():
    raw = SEED.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SEED_SHA256
    word = raw.decode("ascii").strip()
    assert len(word) == N and set(word) == set("123456")
    old = [0] + [int(c) for c in word]
    defects = []
    triple_count = 0
    for edge in triples():
        triple_count += 1
        if len({old[v] for v in edge}) == 1:
            defects.append(edge)
    assert triple_count == 72092
    assert defects == [(12, 24), (12, 24, 36)]
    assert [old[1:].count(c) for c in range(1, 7)] == [93, 163, 119, 35, 63, 64]
    return old


def encode(old, group):
    free = {v for v in range(1, N + 1) if old[v] in group}
    clauses = []
    for v in sorted(free):
        clauses.append([var(v, c) for c in range(1, 7)])
        for c in range(1, 7):
            for d in range(c + 1, 7):
                clauses.append([-var(v, c), -var(v, d)])
    for edge in triples():
        fixed_colours = {old[v] for v in edge if v not in free}
        if len(fixed_colours) >= 2:
            continue
        moving = [v for v in edge if v in free]
        if fixed_colours:
            c = next(iter(fixed_colours))
            clauses.append([-var(v, c) for v in moving])
        else:
            for c in range(1, 7):
                clauses.append([-var(v, c) for v in moving])
    return clauses, len(free)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_case(old, group, drat_trim, directory):
    clauses, free = encode(old, {int(c) for c in group})
    cnf = directory / f"{group}.cnf"
    proof = directory / f"{group}.drat"
    with cnf.open("w", encoding="ascii", newline="\n") as out:
        out.write(f"p cnf {6 * N} {len(clauses)}\n")
        for clause in clauses:
            out.write(" ".join(map(str, clause)) + " 0\n")
    with Solver(name="glucose3", bootstrap_with=clauses, with_proof=True) as solver:
        result = solver.solve()
        if result is not False:
            raise RuntimeError(f"group {group}: solver returned {result}, expected UNSAT")
        conflicts = solver.accum_stats()["conflicts"]
        lines = solver.get_proof()
    with proof.open("w", encoding="ascii", newline="\n") as out:
        for line in lines:
            out.write(line + "\n")
    checked = subprocess.run(
        [str(drat_trim), str(cnf), str(proof)],
        text=True, capture_output=True, check=False,
    )
    if checked.returncode != 0 or "s VERIFIED" not in checked.stdout:
        raise RuntimeError(f"group {group}: DRAT-trim failed: {checked.stdout} {checked.stderr}")
    return {
        "group": group,
        "free": free,
        "clauses": len(clauses),
        "conflicts": conflicts,
        "cnf_sha256": sha256(cnf),
        "proof_sha256": sha256(proof),
        "proof_bytes": proof.stat().st_size,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--record", type=Path, help="write a new manifest instead of comparing")
    args = parser.parse_args()
    old = load_seed()
    results = []
    groups = ["".join(map(str, group)) for group in itertools.combinations(range(1, 7), 3) if 4 in group]
    assert len(groups) == 10
    with tempfile.TemporaryDirectory(prefix="schur-s6-trades-") as temp:
        for group in groups:
            result = verify_case(old, group, args.drat_trim, Path(temp))
            results.append(result)
            print(f"{group}: UNSAT, DRAT VERIFIED, free={result['free']}, clauses={result['clauses']}")
    if args.record:
        args.record.write_text(json.dumps(results, indent=2) + "\n", encoding="ascii")
    else:
        expected = json.loads((HERE / "expected.json").read_text(encoding="ascii"))
        assert results == expected, "generated result differs from the committed manifest"
    print("PASS all_ten_three_class_trades_unsat=10 drat_verified=10")


if __name__ == "__main__":
    main()
