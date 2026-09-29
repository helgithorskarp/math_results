#!/usr/bin/env python3
"""Independent literal checker. Imports neither the encoder nor a SAT solver."""
import argparse
import hashlib
import itertools
import json
import math
import subprocess
import tempfile
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024*1024), b""):
            h.update(block)
    return h.hexdigest()


def compact(data):
    p = data["modulus"]
    require(p == 109 and all(p % q for q in range(2, math.isqrt(p)+1)), "modulus")
    require(data["external_schur_number"] == {"colours": 4, "largest_endpoint": 44},
            "external S(4) convention")
    require(data["progression_length"] == 45, "progression length")
    cover = {int(d): u for d, u in data["progression_cover"].items()}
    require(len(cover) == len(data["progression_cover"]), "duplicate numeric ratios")
    residual = set(range(2, 55)) - set(cover)
    require(sorted(residual) == data["remaining_ratios"], "incomplete ratio cover")
    for d, u in cover.items():
        require(2 <= d <= 54 and isinstance(u, int) and 0 < u < p, "cover domain")
        progression = [(u*j) % p for j in range(1, 46)]
        require(len(set(progression)) == 45 and 0 not in progression, "injective progression")
        require(not set(progression) & {1, p-1, d, p-d}, f"bad progression for {d}")
    # Confirm that precisely these eight ratios escape every such progression.
    for d in residual:
        for u in range(1, p):
            require(any((u*j) % p in {1, p-1, d, p-d} for j in range(1, 46)),
                    "residual admits an unrecorded avoiding progression")
    orbits = sorted({tuple(sorted({d, min(pow(d, -1, p), p-pow(d, -1, p))}))
                     for d in residual})
    require(orbits == [tuple(x) for x in data["remaining_orbits"]], "inversion orbits")
    require(orbits == [(2, 54), (4, 27), (28, 35), (37, 53)], "residual cases")
    require([r["ratio"] for r in data["exclusions"]] == [4, 28, 37], "exclusion coverage")
    require(data["admissible_ratios"] == [2, 54], "claimed ratios")

    word = data["axis_word"]
    require(len(word) == p-1 and all(type(c) is int and 0 <= c < 6 for c in word),
            "axis word domain")
    colour = {q: word[q-1] for q in range(1, p)}
    for q in colour:
        require(colour[q] == colour[p-q], "reflection")
    require({q for q in colour if colour[q] == 0} == {1, p-1}, "first pair")
    require({q for q in colour if colour[q] == 1} == {2, p-2}, "second pair")
    equations = 0
    for x in colour:
        for y in colour:
            z = (x+y) % p
            if z:
                equations += 1
                require(not colour[x] == colour[y] == colour[z], f"monochromatic {x}+{y}={z}")
    sizes = [word.count(c) for c in range(6)]
    require(sizes == data["axis_class_sizes"], "class sizes")
    # No three reflected pairs can have all pairwise ratios in the allowed orbit.
    allowed = {2, 54}
    compatible = lambda a, b: min((a*pow(b, -1, p)) % p,
                                   (-a*pow(b, -1, p)) % p) in allowed
    require(not any(compatible(1, d) and compatible(1, e) and compatible(d, e)
                    for d, e in itertools.combinations(range(2, 55), 2)), "three-pair corollary")
    return {"progression_certificates": len(cover), "remaining_orbits": data["remaining_orbits"],
            "axis_class_sizes": sizes, "ordered_modular_equations_checked": equations,
            "doublings_checked": p-1, "at_most_two_size_two_classes": True}


def literal_model(ratio):
    """Build the full six-colour modular model with constants for both pairs.

    All ordered residue pairs and all six colours are used. In particular,
    fixed-pair constraints are evaluated rather than omitted by assumption.
    """
    p = 109
    halves = [q for q in range(1, 55) if q not in (1, ratio)]

    def positive_literal(x, c):
        q = min(x, p-x)
        if q == 1:
            return c == 0
        if q == ratio:
            return c == 1
        if c < 2:
            return False
        rank = q-1-int(q > 1)-int(q > ratio)
        return 4*rank+c-1

    expected = set()
    for q in halves:
        row = [positive_literal(q, c) for c in range(2, 6)]
        expected.add(tuple(sorted(row)))
        for v, w in itertools.combinations(row, 2):
            expected.add(tuple(sorted((-v, -w))))
    for x in range(1, p):
        for y in range(1, p):
            z = (x+y) % p
            if z == 0:
                continue
            for c in range(6):
                values = [positive_literal(q, c) for q in (x, y, z)]
                if any(v is False for v in values):
                    continue
                expected.add(tuple(sorted({-v for v in values if v is not True})))
    for q in halves:
        for c in range(3, 6):
            row = [-positive_literal(q, c)]
            row += [positive_literal(old, c-1) for old in halves if old < q]
            expected.add(tuple(sorted(row)))
    return expected


def check_formula(path, record):
    require(digest(path) == record["cnf_sha256"], "CNF hash mismatch")
    require(Path(path).stat().st_size == record["cnf_bytes"], "CNF size mismatch")
    lines = Path(path).read_text().splitlines()
    require(lines[0] == f'p cnf {record["variables"]} {record["clauses"]}', "CNF header")
    clauses = []
    for line in lines[1:]:
        values = list(map(int, line.split()))
        require(values and values[-1] == 0 and 0 not in values[:-1], "CNF terminator")
        require(all(1 <= abs(v) <= 208 for v in values[:-1]), "CNF literal domain")
        require(len(set(values[:-1])) == len(values[:-1]), "repeated literal")
        clauses.append(tuple(sorted(values[:-1])))
    require(record["variables"] == 208 and record["clauses"] == 4056, "model dimensions")
    require(len(clauses) == 4056 and len(set(clauses)) == 4056, "clause count")
    require(set(clauses) == literal_model(record["ratio"]), "literal semantic model mismatch")
    return {"ratio": record["ratio"], "variables": 208, "clauses": 4056,
            "cnf_sha256": record["cnf_sha256"], "literal_model_checked": True}


def audit(data, cnf_dir=None, proof_dir=None, drat_trim=None, ratios=(4, 28, 37), seconds=120):
    require(set(ratios) <= {4, 28, 37} and len(set(ratios)) == len(ratios), "ratios")
    require(not proof_dir or (cnf_dir and drat_trim), "proofs need CNFs and a checker")
    result = {"status": "COMPACT_WITNESS_AND_COVER_VERIFIED", **compact(data),
              "external_theorem_assumed": "S(4)=44, largest colourable endpoint",
              "proofs_checked": False, "exclusions": []}
    for record in data["exclusions"]:
        ratio = record["ratio"]
        if ratio not in ratios or cnf_dir is None:
            continue
        cnf = Path(cnf_dir) / f"ratio{ratio}.cnf"
        entry = check_formula(cnf, record)
        if proof_dir is not None:
            proof = Path(proof_dir) / f"ratio{ratio}.drat"
            with tempfile.TemporaryFile() as log:
                proc = subprocess.run([str(drat_trim), str(cnf), str(proof), "-i", "-t", str(seconds)],
                                      stdout=log, stderr=subprocess.STDOUT, timeout=seconds+10)
                log.seek(0)
                output = log.read().decode(errors="replace")
            require(proc.returncode == 0 and "s VERIFIED" in output.splitlines(),
                    f"DRAT verification failed for {ratio}: {output[-1000:]}")
            sha = digest(proof)
            entry.update(proof_checked=True, proof_sha256=sha, proof_bytes=proof.stat().st_size,
                         matches_reference_proof=(sha == record["proof_sha256"]))
        result["exclusions"].append(entry)
    if proof_dir:
        result["proofs_checked"] = True
        result["status"] = ("CLASSIFICATION_CERTIFICATES_VERIFIED" if set(ratios) == {4, 28, 37}
                            else "PARTIAL_EXCLUSION_CERTIFICATES_VERIFIED")
    elif cnf_dir:
        result["status"] = "LITERAL_MODELS_AND_COMPACT_DATA_VERIFIED"
    result["all_three_exclusion_proofs_checked"] = bool(proof_dir and set(ratios) == {4, 28, 37})
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path(__file__).with_name("data.json"))
    parser.add_argument("--cnf-dir", type=Path)
    parser.add_argument("--proof-dir", type=Path)
    parser.add_argument("--drat-trim", type=Path)
    parser.add_argument("--ratios", nargs="+", type=int, choices=(4, 28, 37), default=(4, 28, 37))
    parser.add_argument("--seconds", type=int, default=120)
    args = parser.parse_args()
    print(json.dumps(audit(json.loads(args.data.read_text()), args.cnf_dir, args.proof_dir,
                           args.drat_trim, args.ratios, args.seconds), indent=2))
