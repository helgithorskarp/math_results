"""Verify the complete reduction and all proof inputs; replay.py checks proofs."""
import argparse
from collections import Counter
import csv
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import subprocess
import sys

from pysat.solvers import Solver
from model import POINTS, decode_and_check, fiber_clauses, generate, geometry
from quotients import A, B, PROFILES, POINTS as PLANE_POINTS, classify, orbit, validate

HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def all_affine_images(key):
    word = key[1]
    profile_type = {profiles:i for i,profiles in enumerate(PROFILES)}
    result = set()
    for a, b, c, d in product(range(5), repeat=4):
        if (a*d-b*c) % 5 == 0:
            continue
        for u, v in PLANE_POINTS:
            image = [""]*25
            for i, (x, y) in enumerate(PLANE_POINTS):
                image[5*((a*x+b*y+u) % 5)+(c*x+d*y+v) % 5] = word[i]
            rows = tuple(sum(int(image[5*x+y]) for y in range(5)) for x in range(5))
            if rows not in (A, B):
                continue
            columns = tuple(sum(int(image[5*x+y]) for x in range(5)) for y in range(5))
            kind = profile_type.get((rows, columns))
            if kind is None:
                continue
            transformed = (kind, "".join(image))
            validate(transformed)
            result.add(transformed)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--sanitize", action="store_true")
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    dependencies = json.loads((HERE/"dependencies.json").read_text())
    for name, expected_hash in dependencies["files_sha256"].items():
        if digest(HERE.parent/name) != expected_hash:
            raise RuntimeError(f"dependency source changed: {name}")
    flags = ["-O1", "-g", "-fsanitize=address,undefined", "-fno-omit-frame-pointer"] if args.sanitize else ["-O3"]
    for name in ("deficit_enumeration", "row_enumeration"):
        executable = out/name
        subprocess.run(["g++", "-std=c++20", "-Wall", "-Wextra", "-Wconversion", *flags,
                        str(HERE/f"{name}.cpp"), "-o", str(executable)], check=True)
        with (out/f"{name}.txt").open("w") as output:
            subprocess.run([str(executable)], stdout=output, check=True)
    first = (out/"deficit_enumeration.txt").read_text().splitlines()
    second = (out/"row_enumeration.txt").read_text().splitlines()
    if first != second or len(first) != 16192 or len(set(first)) != 16192:
        raise RuntimeError("entry-level enumeration disagreement")
    catalogue_hash = digest(out/"deficit_enumeration.txt")
    if catalogue_hash != "7ad44f1b9e1244da30d0ac28d29eb9f84e441323285b62cd21454827579fcb7f":
        raise RuntimeError("typed catalogue hash disagreement")
    keys = [(int(line.split()[0]), line.split()[1]) for line in first]
    labeled_counts = [sum(kind == i for kind, _ in keys) for i in range(3)]
    if labeled_counts != [4442, 5428, 6322]:
        raise RuntimeError("incorrect labeled profile counts")
    representatives = classify(keys)
    if representatives != json.loads((HERE/"orbits.json").read_text()):
        raise RuntimeError("published orbit catalogue disagrees")
    orbit_counts = [sum(r["type"] == i for r in representatives) for i in range(3)]
    if orbit_counts != [164, 1252, 2916]:
        raise RuntimeError("incorrect affine class counts")

    samples = {}
    for representative in representatives:
        key = (representative["type"], representative["weights"])
        profiles = validate(key)
        signature = (key[0], sum(p.count(8) for p in profiles),
                     sum(p.count(9) for p in profiles), representative["orbit_size"])
        samples.setdefault(signature, key)
    for key in samples.values():
        if all_affine_images(key) != orbit(key):
            raise RuntimeError("full affine-group control disagrees")

    index = {p:i+1 for i,p in enumerate(POINTS)}
    pair_lines = set()
    for p, q in combinations(POINTS, 2):
        pair_lines.add(tuple(sorted(index[tuple((a+t*(b-a)) % 5 for a,b in zip(p,q))]
                                    for t in range(5))))
    lines, planes = geometry()
    if pair_lines != set(lines):
        raise RuntimeError("all-pairs line geometry disagrees")
    if any(sum(set(line) <= set(plane) for plane in planes) != 6 for line in lines):
        raise RuntimeError("incorrect plane pencils")

    # Definition-level truth-table check, without a solver or auxiliary variables.
    for n in range(5):
        clauses = fiber_clauses(list(range(1,6)), n)
        for assignment in product((False, True), repeat=5):
            satisfies = all(any(assignment[abs(v)-1] == (v > 0) for v in clause)
                            for clause in clauses)
            if satisfies != (sum(assignment) == n):
                raise RuntimeError("direct fiber cardinality clauses are wrong")

    with (HERE/"certificates.csv").open(newline="") as manifest:
        checked = list(csv.DictReader(manifest))
    if [int(r["index"]) for r in checked] != list(range(4332)):
        raise RuntimeError("incomplete certificate manifest")
    path = out/"regenerated.cnf"
    for i, representative in enumerate(representatives):
        formula, _ = generate(representative["weights"])
        if formula.nv != 125:
            raise RuntimeError("unexpected auxiliary variable")
        formula.to_file(str(path))
        if digest(path) != checked[i]["cnf_sha256"]:
            raise RuntimeError(f"proof input mismatch in case {i}")

    controls = []
    for name in ("known70.json", "odd_symmetry/witness70.json"):
        known = json.loads((HERE.parent/name).read_text())["points"]
        word = "".join(str(sum(p//5 == i for p in known)) for i in range(25))
        direct = decode_and_check(word, [p+1 for p in known])
        if len(direct) != 70:
            raise RuntimeError("input is not a 70-point construction")
        formula, _ = generate(word)
        with Solver(name="cadical195", bootstrap_with=formula.clauses) as solver:
            if not solver.solve():
                raise RuntimeError("70-point positive control rejected")
            control = decode_and_check(word, solver.get_model())
        if len(control) != 70:
            raise RuntimeError("incorrect positive-control cardinality")
        controls.append({"source":name, "direct_size":len(direct), "lift_size":len(control)})

    cap = out/"plane_caps"
    subprocess.run(["g++", "-O3", "-std=c++20", str(HERE.parent/"plane_caps.cpp"),
                    "-o", str(cap)], check=True)
    planar = json.loads(subprocess.check_output([str(cap)], text=True))
    if planar["subsets17"] != 1081575 or planar["max4_valid17"] != 0:
        raise RuntimeError("planar cap check failed")
    low = json.loads(subprocess.check_output(
        [sys.executable, "-E", str(HERE.parent/"low_planes72/verify.py"),
         "--out", str(out/"low-plane-dependency")], text=True))
    if (low["status"] != "GLOBAL_72_LOW_PLANE_REDUCTION_VERIFIED"
            or low["incidence_bounds"][0]["integer_lower_bound"] != 5):
        raise RuntimeError("low-plane counting certificate failed")
    result = {"status":"UPPER_BOUND71_REDUCTION_VERIFIED", "typed_quotients":16192,
              "labeled_counts_AA_AB_BB":labeled_counts, "affine_classes":4332,
              "canonical_counts_AA_AB_BB":orbit_counts, "catalogue_sha256":catalogue_hash,
              "independent_enumeration":"entry-level equality",
              "full_affine_group_controls":len(samples), "lines":len(lines), "planes":len(planes),
              "fiber_truth_assignments":160, "point_variables_per_formula":125,
              "positive_controls":controls, "cnf_hashes_matched":len(checked),
              "low_plane_count_certificate_rechecked":True, "proofs_rechecked":False,
              "dependency_hashes_matched":len(dependencies["files_sha256"]),
              "proof_replay":"Run replay.py with DRAT-trim to check all 4332 lifting proofs.",
              "previous_SAT_lemmas_required":False, "claimed_interval":[70,71],
              "exact_value":"OPEN: 70 or 71"}
    (out/"verification.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
