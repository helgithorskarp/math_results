#!/usr/bin/env python3
"""Replay two exact enumerations and independently check all positive controls."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import subprocess
import tempfile

from model import build, decode, write_instance

HERE = Path(__file__).resolve().parent
CASES = [(71, 3, 0), (72, 0, 0), (72, 28, 0), (70, 1, 0), (70, 30, 32)]


def geometry():
    points = list(product(range(5), repeat=3))
    index = {p: i for i, p in enumerate(points)}
    directions = [d for d in points if any(d) and next(x for x in d if x) == 1]
    lines = sorted({
        tuple(sorted(index[tuple((x+t*y) % 5 for x, y in zip(a, d))]
                     for t in range(5)))
        for a in points for d in directions
    })
    planes = [[i for i, p in enumerate(points)
               if sum(x*y for x, y in zip(p, d)) % 5 == c]
              for d in directions for c in range(5)]
    if len(lines) != 775 or len(planes) != 155:
        raise ValueError("incorrect affine incidence structure")
    return points, lines, planes


def check_witness(witness, size, points, lines):
    chosen = set(witness)
    if len(chosen) != len(witness) or len(chosen) != size or not chosen <= set(range(125)):
        raise ValueError("invalid witness cardinality or coordinates")
    if any(all(p in chosen for p in line) for line in lines):
        raise ValueError("witness contains a full affine line")
    index = {p: i for i, p in enumerate(points)}
    image = {index[(x, -z % 5, (y-z) % 5)] for x, y, z in (points[p] for p in chosen)}
    if image != chosen:
        raise ValueError("witness is not rotation invariant")


def profile(witness, planes):
    chosen = set(witness)
    result = Counter(tuple(sorted(len(chosen.intersection(h)) for h in planes[i:i+5]))
                     for i in range(0, 155, 5))
    return [[list(p), n] for p, n in sorted(result.items())]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--sanitize", action="store_true")
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    out = args.out.resolve() if args.out else Path(tempfile.mkdtemp(prefix="linefree-odd-"))
    out.mkdir(parents=True, exist_ok=True)
    model = build()
    instance = out / "instance.txt"
    write_instance(instance, model)
    flags = ["-std=c++20", "-Wall", "-Wextra", "-Wconversion", "-Werror"]
    flags += ["-O1", "-g", "-fsanitize=address,undefined"] if args.sanitize else ["-O2"]
    binaries = []
    for name in ["enumerate_constraints", "enumerate_lines"]:
        binary = out / name
        subprocess.run(["g++", *flags, str(HERE / (name + ".cpp")), "-o", str(binary)], check=True)
        binaries.append(binary)
    points, lines, planes = geometry()
    records, witnesses = [], []
    for size, center, expected_count in CASES:
        first = json.loads(subprocess.check_output(
            [str(binaries[0]), str(instance), str(size), str(center)], text=True))
        second = json.loads(subprocess.check_output(
            [str(binaries[1]), str(size), str(center)], text=True))
        if first != second or first["solutions"] != expected_count:
            raise ValueError(("enumerations disagree or claimed theorem fails", first, second))
        if first["solutions"] != len(first["solution_masks"]):
            raise ValueError("incomplete positive control list")
        for masks in first["solution_masks"]:
            witness = decode(center, masks, model)
            check_witness(witness, size, points, lines)
            witnesses.append(witness)
        records.append(first)
    supplied = json.loads((HERE / "witness70.json").read_text())["points"]
    check_witness(supplied, 70, points, lines)
    if supplied not in witnesses:
        raise ValueError("supplied control was not enumerated")
    known = json.loads((HERE.parent / "known70.json").read_text())["points"]
    known_set = set(known)
    if len(known_set) != 70 or any(set(line) <= known_set for line in lines):
        raise ValueError("published control is malformed")
    new_profile, old_profile = profile(supplied, planes), profile(known, planes)
    if new_profile == old_profile:
        raise ValueError("claimed affine distinction not established")
    # The identity, fixed-point counts and fixed-set normalizations are exact.
    affine_maps = [(a, b) for a in range(1, 5) for b in range(5)]
    for count in [1, 2, 3, 4]:
        masks = [m for m in range(32) if m.bit_count() == count]
        representative = {1: 1, 2: 3, 3: 28, 4: 30}[count]
        orbit = {sum(1 << ((a*x+b) % 5) for x in range(5) if representative >> x & 1)
                 for a, b in affine_maps}
        if orbit != set(masks):
            raise ValueError("fixed-line normalization is incomplete")
    record_hash = sha256(json.dumps(records, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    result = {
        "status": "ODD_SYMMETRY_OBSTRUCTION_VERIFIED",
        "line_count": len(lines), "plane_count": len(planes),
        "orbit_lengths": [len(o) for o in model["orbits"]],
        "menu_spectra": [dict(sorted(Counter(m.bit_count() for m in menu).items()))
                         for menu in model["menus"]],
        "cross_line_patterns": len(model["constraints"]),
        "cases": records, "verified_70_controls": len(witnesses),
        "witness70_profile": new_profile, "published70_profile": old_profile,
        "record_sha256": record_hash,
    }
    # JSON makes integer-keyed dictionaries portable for exact comparison.
    result = json.loads(json.dumps(result))
    if args.check_expected and result != json.loads((HERE / "EXPECTED.json").read_text()):
        raise ValueError("expected-output mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
