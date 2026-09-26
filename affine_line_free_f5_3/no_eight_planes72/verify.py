"""Check the mixed catalogue, affine coverage, geometry and every proof input.

This validates the reduction and proof-input hashes; use replay.py to regenerate
and independently check every UNSAT proof. Neither script substitutes for the
two-eight-plane and global low-plane dependencies cited in THEOREM.md.
"""
import argparse
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import subprocess
import sys

from pysat.solvers import Solver
from model import POINTS, decode_and_check, generate, geometry
from quotients import A, B, POINTS as PLANE_POINTS, classify, orbit, validate

HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def all_affine_images(word):
    result = set()
    for a, b, c, d in product(range(5), repeat=4):
        if (a*d-b*c) % 5 == 0:
            continue
        for u, v in PLANE_POINTS:
            image = [""]*25
            for i, (x, y) in enumerate(PLANE_POINTS):
                image[5*((a*x+b*y+u) % 5)+(c*x+d*y+v) % 5] = word[i]
            rows = tuple(sum(int(image[5*x+y]) for y in range(5)) for x in range(5))
            if rows != A:
                continue
            columns = tuple(sum(int(image[5*x+y]) for x in range(5)) for y in range(5))
            if columns != B:
                continue
            transformed = "".join(image)
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
    flags = ["-O1", "-g", "-fsanitize=address,undefined", "-fno-omit-frame-pointer"] if args.sanitize else ["-O3"]
    for name in ("deficit_enumeration", "row_enumeration"):
        executable = out/name
        subprocess.run(["g++", "-std=c++20", "-Wall", "-Wextra", "-Wconversion", *flags,
                        str(HERE/f"{name}.cpp"), "-o", str(executable)], check=True)
        with (out/f"{name}.txt").open("w") as output:
            subprocess.run([str(executable)], stdout=output, check=True)
    first = (out/"deficit_enumeration.txt").read_text().splitlines()
    second = (out/"row_enumeration.txt").read_text().splitlines()
    if first != second or len(first) != 5428 or len(set(first)) != 5428:
        raise RuntimeError("entry-level enumeration disagreement")
    catalogue_hash = digest(out/"deficit_enumeration.txt")
    if catalogue_hash != "765937a860439729986f457b6cad703d362aa87a71ae6b3cb30631fbe5038792":
        raise RuntimeError("catalogue hash disagreement")
    representatives, discarded = classify(first)
    if discarded != 144 or len(representatives) != 1252:
        raise RuntimeError("unexpected affine partition")
    if representatives != json.loads((HERE/"orbits.json").read_text()):
        raise RuntimeError("published orbit catalogue disagrees")

    # All 12,000 affine maps, with independently tested normalized margins.
    # Sample every occurring (number of nine-lines, normalized orbit size).
    samples = {}
    for representative in representatives:
        word = representative["weights"]
        nine_count = sum(profile.count(9) for profile in validate(word))
        samples.setdefault((nine_count, representative["orbit_size"]), word)
    for word in samples.values():
        if all_affine_images(word) != orbit(word):
            raise RuntimeError("full affine-group control disagrees")

    index = {p: i+1 for i, p in enumerate(POINTS)}
    pair_lines = set()
    for p, q in combinations(POINTS, 2):
        pair_lines.add(tuple(sorted(index[tuple((a+t*(b-a)) % 5 for a, b in zip(p, q))]
                                    for t in range(5))))
    lines, planes = geometry()
    if pair_lines != set(lines):
        raise RuntimeError("all-pairs line geometry disagrees")
    if any(sum(set(line) <= set(plane) for plane in planes) != 6 for line in lines):
        raise RuntimeError("incorrect plane pencils")

    checked = [json.loads(line) for line in (HERE/"certificates.jsonl").read_text().splitlines()]
    if [r["index"] for r in checked] != list(range(1252)):
        raise RuntimeError("incomplete certificate manifest")
    # Reuse one temporary path; large formulas are regenerated, not published.
    path = out/"regenerated.cnf"
    for i, representative in enumerate(representatives):
        formula, gauge = generate(representative["weights"])
        formula.to_file(str(path))
        if digest(path) != checked[i]["cnf_sha256"] or list(gauge) != checked[i]["gauge"]:
            raise RuntimeError(f"proof input mismatch in case {i}")
        if checked[i]["status"] != "UNSAT_DRAT_VERIFIED":
            raise RuntimeError("manifest contains an unchecked case")

    known = json.loads((HERE.parent/"known70.json").read_text())["points"]
    word = "".join(str(sum(p//5 == i for p in known)) for i in range(25))
    formula, _ = generate(word)
    with Solver(name="cadical195", bootstrap_with=formula.clauses) as solver:
        if not solver.solve():
            raise RuntimeError("known 70-point positive control rejected")
        control = decode_and_check(word, solver.get_model())
    if len(control) != 70:
        raise RuntimeError("incorrect positive-control cardinality")
    cap = out/"plane_caps"
    subprocess.run(["g++", "-O3", "-std=c++20", str(HERE.parent/"plane_caps.cpp"),
                    "-o", str(cap)], check=True)
    planar = json.loads(subprocess.check_output([str(cap)], text=True))
    if planar["subsets17"] != 1081575 or planar["max4_valid17"] != 0:
        raise RuntimeError("planar cap check failed")
    frame = json.loads(subprocess.check_output(
        [sys.executable, str(HERE.parent/"nine_plane_frame72/verify.py"),
         "--out", str(out/"nine-plane-frame")], text=True))
    if (frame["status"] != "NINE_PLANE_FRAME72_VERIFIED"
            or frame["weighted_integer_lower_bound"] != 11):
        raise RuntimeError("weighted incidence dependency check failed")
    result = {"status": "NO_EIGHT_PLANE_REDUCTION_VERIFIED",
              "labeled_mixed_quotients": 5428, "inherited_two_eight_exclusions": discarded,
              "remaining_mixed_quotients": 5284, "mixed_affine_classes": 1252,
              "catalogue_sha256": catalogue_hash,
              "independent_enumeration": "entry-level equality",
              "affine_group_controls": len(samples), "lines": len(lines), "planes": len(planes),
              "positive_control_size": len(control), "cnf_hashes_matched": len(checked),
              "proofs_rechecked": False,
              "nine_planes_if_no_eight": 11,
              "dependencies": ["two_eight_planes72", "low_planes72", "nine_plane_frame72"],
              "proof_replay": "Run replay.py with DRAT-trim; replay the cited dependencies separately."}
    (out/"verification.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
