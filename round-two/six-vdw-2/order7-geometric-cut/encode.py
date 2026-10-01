"""Exact longest-run cover of order-seven coset colorings of punctured F617.

The solver is absent from this generator. A variable i+1 is the color of
the multiplicative coset 3^i H, where H=<3^88> has order seven.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

P, M, ROOT = 617, 88, 3
LENGTHS = tuple(range(2, 33))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def field_edges():
    require(all(P % d for d in range(2, 25)), "617 must be prime")
    ids = [-1] * P
    for exponent in range(P-1):
        x = pow(ROOT, exponent, P)
        require(ids[x] == -1, "3 must be primitive")
        ids[x] = exponent % M
    require(ids[0] == -1 and all(x >= 0 for x in ids[1:]), "incomplete quotient")
    spacing_one = set()
    for a in range(P):
        terms = [(a+j) % P for j in range(7)]
        if 0 not in terms:
            spacing_one.add(tuple(sorted({ids[x] for x in terms})))
    # Scale a spacing-one progression by its nonzero difference.
    return sorted({tuple(sorted({(x+s) % M for x in edge}))
                   for edge in spacing_one for s in range(M)},
                  key=lambda edge: (len(edge), edge))


def encoding(length):
    require(length in LENGTHS, "length outside the complete 2..32 cover")
    edges = field_edges()
    clauses = []
    for edge in edges:
        variables = [x+1 for x in edge]
        clauses.extend((variables, [-x for x in variables]))
    # Every cyclic window of length L+1 has both colors.
    for start in range(M):
        window = [(start+j) % M+1 for j in range(length+1)]
        clauses.extend((window, [-x for x in window]))
    # Rotate a longest run to position zero and complement it to color zero.
    clauses.extend([[-i] for i in range(1, length+1)])
    clauses.extend(([length+1], [M]))
    metadata = {"p": P, "index": M, "subgroup_order": 7,
                "longest_run": length, "variables": M,
                "clauses": len(clauses), "field_edges": len(edges),
                "rank_histogram": dict(sorted(Counter(map(len, edges)).items())),
                "window_clauses": 2*M, "normalization_units": length+2}
    return clauses, metadata


def write_cnf(path, length):
    clauses, metadata = encoding(length)
    text = f"p cnf {M} {len(clauses)}\n"
    text += "".join(" ".join(map(str, c))+" 0\n" for c in clauses)
    path.write_text(text)
    metadata["cnf_sha256"] = hashlib.sha256(text.encode()).hexdigest()
    return metadata


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("output", type=Path)
    ap.add_argument("--length", type=int, required=True)
    args = ap.parse_args()
    print(json.dumps(write_cnf(args.output, args.length), sort_keys=True))


if __name__ == "__main__":
    main()
