"""Check enumeration, affine coverage, geometry, and a positive lifting control."""
import argparse
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import subprocess

from pysat.solvers import Solver
from model import POINTS, decode_and_check, generate, geometry
from quotients import POINTS as PLANE_POINTS, classify, orbit, validate

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
            image = "".join(image)
            if sum(map(int, image[:5])) == 8 and sum(int(image[5*i]) for i in range(5)) == 8:
                validate(image)
                result.add(image)
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
        exe = out/name
        subprocess.run(["g++", "-std=c++20", "-Wall", "-Wextra", "-Wconversion", *flags,
                        str(HERE/f"{name}.cpp"), "-o", str(exe)], check=True)
        with (out/f"{name}.txt").open("w") as output:
            subprocess.run([str(exe)], stdout=output, check=True)
    first = (out/"deficit_enumeration.txt").read_text().splitlines()
    second = (out/"row_enumeration.txt").read_text().splitlines()
    if first != second or len(first) != 4442 or len(set(first)) != 4442:
        raise RuntimeError("entry-level enumeration disagreement")
    representatives = classify(first)
    if len(representatives) != 164:
        raise RuntimeError("unexpected number of affine classes")
    if representatives != json.loads((HERE/"orbits.json").read_text()):
        raise RuntimeError("published orbit catalogue disagrees")

    # Compare the selected-low-plane normalization with all 12,000 affine maps.
    samples = {}
    for word in first:
        count = sum(p.count(8) for p in validate(word))
        samples.setdefault(count, word)
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

    # Regenerate every proof input and compare with the checked production inputs.
    checked = json.loads((HERE/"certificates.json").read_text())["cases"]
    if len(checked) != 164 or [r["index"] for r in checked] != list(range(164)):
        raise RuntimeError("incomplete certificate manifest")
    for i, representative in enumerate(representatives):
        formula, gauge = generate(representative["weights"])
        path = out/f"case_{i:03d}.cnf"
        formula.to_file(str(path))
        if digest(path) != checked[i]["cnf_sha256"] or list(gauge) != checked[i]["gauge"]:
            raise RuntimeError(f"proof input mismatch in case {i}")
        if checked[i]["status"] is not False or not checked[i]["verified"]:
            raise RuntimeError("manifest contains an unchecked case")

    # This control uses the actual 70-point construction, with no expected UNSAT.
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
    result = {"status": "TWO_EIGHT_PLANE_REDUCTION_VERIFIED", "labeled_quotients": 4442,
              "affine_classes": 164, "catalogue_sha256": digest(out/"deficit_enumeration.txt"),
              "independent_enumeration": "entry-level equality", "affine_group_controls": len(samples),
              "lines": len(lines), "planes": len(planes), "positive_control_size": len(control),
              "cnf_hashes_matched": len(checked), "proofs_rechecked": False,
              "proof_replay": "Run replay.py with DRAT-trim to recheck the computer-assisted exclusion."}
    (out/"verification.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
