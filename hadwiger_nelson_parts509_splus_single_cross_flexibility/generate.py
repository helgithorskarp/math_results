#!/usr/bin/env python3
"""Generate a positive colouring library for S+ one-cross-edge flexibility."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import sys
from pathlib import Path

from pysat.solvers import Solver


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PRIOR = ROOT / "hadwiger_nelson_parts509_two_overlap_reduction"
POINTS = ROOT / "hadwiger_nelson_parts509_completion_census_degree9" / "points.tsv"
POINTS_VTX = ROOT / "hadwiger_nelson_parts509_criticality" / "parts509.vtx"
FORMAT = "parts509-splus-single-cross-flexibility-v1"

sys.path.insert(0, str(PRIOR))
import generate_certificate as prior_generate  # noqa: E402
import verify as prior  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def unpack(text: str):
    raw = base64.b64decode(text, validate=True)
    if len(raw) != 34:
        raise ValueError("bad packed colouring length")
    return tuple((raw[index // 4] >> (2 * (index % 4))) & 3 for index in range(136))


def missing_requirements(witnesses):
    missing = []
    for q1 in range(136):
        for q2 in range(q1 + 1, 136):
            for equal in (True, False):
                subset = [colors for colors in witnesses if (colors[q1] == colors[q2]) == equal]
                if not subset:
                    continue
                for q3 in range(136):
                    if q3 in (q1, q2):
                        continue
                    for endpoint in (q1, q2):
                        if all(colors[q3] == colors[endpoint] for colors in subset):
                            missing.append((q1, q2, equal, q3, endpoint))
    return missing


def covers(colors, requirement):
    q1, q2, equal, q3, endpoint = requirement
    return (colors[q1] == colors[q2]) == equal and colors[q3] != colors[endpoint]


def generate(output: Path) -> None:
    prior_certificate = json.loads((PRIOR / "certificate.json").read_text(encoding="utf-8"))
    inherited = [unpack(text) for text in prior_certificate["s_colorings"]]
    missing = missing_requirements(inherited)
    if len(inherited) != 31 or len(missing) != 30_174:
        raise RuntimeError("inherited pair-flexibility library census mismatch")

    points = prior.read_points(POINTS)
    small = [points[0]] + points[374:]
    edges = prior.build_edges(small)
    formula = prior_generate.clauses(136, edges)
    selector = 4 * 136 + 1
    added = []
    with Solver(name="cadical195", bootstrap_with=formula) as solver:
        while missing:
            q1, q2, equal, q3, endpoint = missing[0]
            for color in range(4):
                x1 = 4 * q1 + color + 1
                x2 = 4 * q2 + color + 1
                x3 = 4 * q3 + color + 1
                xe = 4 * endpoint + color + 1
                if equal:
                    solver.add_clause([-selector, -x1, x2])
                    solver.add_clause([-selector, -x2, x1])
                else:
                    solver.add_clause([-selector, -x1, -x2])
                solver.add_clause([-selector, -x3, -xe])
            if not solver.solve(assumptions=[selector]):
                raise RuntimeError(f"unexpected missing flexibility requirement: {missing[0]}")
            colors = prior_generate.decode(solver.get_model())
            if not covers(colors, missing[0]):
                raise RuntimeError("decoded colouring does not cover its target")
            added.append(colors)
            selector += 1
            missing = [requirement for requirement in missing if not covers(colors, requirement)]
            print(f"added={len(added)};remaining={len(missing)}", flush=True)

    all_witnesses = inherited + added
    certificate = {
        "format": FORMAT,
        "source_sha256": {
            "points.tsv": sha256(POINTS),
            "parts509.vtx": sha256(POINTS_VTX),
            "pair_flexibility_certificate.json": sha256(PRIOR / "certificate.json"),
            "pair_flexibility_verify.py": sha256(PRIOR / "verify.py"),
        },
        "counts": {
            "vertices": 136,
            "strict_edges": len(edges),
            "inherited_pair_flexibility_witnesses": len(inherited),
            "initial_uncovered_requirements": 30_174,
            "added_witnesses": len(added),
            "total_witnesses": len(all_witnesses),
            "pair_relation_cases": 564 + 2 * 8_616,
            "triple_flexibility_requirements": (564 + 2 * 8_616) * 134 * 2,
        },
        "s_colorings": [prior.pack_coloring(list(colors)) for colors in all_witnesses],
    }
    output.write_text(json.dumps(certificate, separators=(",", ":")) + "\n", encoding="utf-8")
    print("certificate_written=" + str(output))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", nargs="?", type=Path, default=Path("certificate.json"))
    args = parser.parse_args()
    generate(args.output)


if __name__ == "__main__":
    main()
