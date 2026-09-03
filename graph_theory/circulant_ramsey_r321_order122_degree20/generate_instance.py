#!/usr/bin/env python3
"""Validate learned-cut witnesses and generate the final UNSAT CNF instance."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from pysat.card import CardEnc, EncType

sys.path.insert(0, str(Path(__file__).parent))
from search import cut_orbit, maximality_clauses, triangle_clauses  # noqa: E402


def pair_distances(n: int, vertices: list[int]) -> set[int]:
    distances = set()
    for i, u in enumerate(vertices):
        for v in vertices[i + 1:]:
            delta = abs(u - v)
            distances.add(min(delta, n - delta))
    return distances


def validated_cuts(path: Path) -> tuple[int, int, int, list[list[int]]]:
    data = json.loads(path.read_text())
    n, target = data["n"], data["target"]
    cuts: set[tuple[int, ...]] = set()
    for index, record in enumerate(data["orbit_representatives"]):
        cut = record["cut"]
        vertices = record["vertices"]
        if cut != sorted(set(cut)) or not cut or cut[-1] > n // 2:
            raise ValueError(f"malformed cut {index}")
        if len(vertices) != target or len(set(vertices)) != target:
            raise ValueError(f"malformed vertex witness {index}")
        if min(vertices) < 0 or max(vertices) >= n:
            raise ValueError(f"vertex outside range in witness {index}")
        if not pair_distances(n, vertices) <= set(cut):
            raise ValueError(f"vertex witness does not validate cut {index}")
        orbit = cut_orbit(n, cut)
        if len(orbit) != record["orbit_size"]:
            raise ValueError(f"orbit-size mismatch {index}")
        cuts.update(tuple(image) for image in orbit)
    expected = data["input_cut_count"]
    if len(cuts) != expected or data["remaining_cut_count"] != 0:
        raise ValueError(f"cut coverage mismatch: {len(cuts)} != {expected}")
    return n, target, len(data["orbit_representatives"]), [list(cut) for cut in sorted(cuts)]


def build_formula(n: int, cuts: list[list[int]]) -> tuple[list[list[int]], int]:
    primary = n // 2
    clauses = triangle_clauses(n)
    clauses.extend([[1], [-primary]])
    card = CardEnc.equals(lits=list(range(1, primary + 1)), bound=10,
                          top_id=primary, encoding=EncType.seqcounter)
    clauses.extend(card.clauses)
    extra, top_id = maximality_clauses(n, card.nv)
    clauses.extend(extra)
    clauses.extend(cuts)
    return clauses, top_id


def write_dimacs(path: Path, clauses: list[list[int]], variables: int) -> str:
    digest = hashlib.sha256()
    with path.open("w") as handle:
        header = f"p cnf {variables} {len(clauses)}\n"
        handle.write(header)
        digest.update(header.encode())
        for clause in clauses:
            line = " ".join(map(str, clause)) + " 0\n"
            handle.write(line)
            digest.update(line.encode())
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--witnesses", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    n, target, orbit_count, cuts = validated_cuts(args.witnesses)
    if (n, target) != (122, 21):
        raise ValueError("this proof instance is specialized to (n,k)=(122,21)")
    clauses, variables = build_formula(n, cuts)
    sha256 = write_dimacs(args.output, clauses, variables)
    print(json.dumps({
        "variables": variables,
        "clauses": len(clauses),
        "validated_cut_orbits": orbit_count,
        "expanded_cuts": len(cuts),
        "sha256": sha256,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
