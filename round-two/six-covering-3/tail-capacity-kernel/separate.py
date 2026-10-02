"""Exact four-fiber triple separator and original-base clause emission.

No triple means this necessary test passes, not that the tail is feasible.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
from check import BASE, PREFIX, hitting_clause, need, original_capacities


def admissible_triple(points):
    """Lexicographically first triple; complete pair scan with literal masks."""
    H = sorted(set(points))
    need(all(type(x) is int and 0 <= x < 315 for x in H), "invalid cofactor set")
    if len(H) < 3:
        return None
    masks = {d: [sum(1 << x for x in range(a, 315, d)) for a in range(d)]
             for d in (3, 5, 7, 9)}
    bits = sum(1 << x for x in H)
    for i, x in enumerate(H):
        for y in H[i+1:]:
            if any(x % d == y % d for d in (5, 7, 9)):
                continue
            forbidden = 0
            for d in (5, 7, 9):
                forbidden |= masks[d][x % d] | masks[d][y % d]
            if x % 3 == y % 3:
                forbidden |= masks[3][x % 3]
            eligible = bits & ~forbidden & ~((1 << (y+1))-1)
            if eligible:
                z = (eligible & -eligible).bit_length()-1
                return [x, y, z]
    return None


def separate(phases):
    need(isinstance(phases, list) and len(phases) == 36 and all(
        isinstance(row, list) and len(row) == 2 and type(row[0]) is int and
        type(row[1]) is int and 0 <= row[1] < row[0] for row in phases) and
        tuple(sorted(n for n, a in phases)) == BASE, "invalid original base inventory")
    holes = [[] for r in range(7)]
    for x in range(2520):
        if all(x % n != a for n, a in PREFIX+phases):
            need(x % 8 != 0, "unexpected eighth parent")
            holes[x % 8-1].append(x % 315)
    kernel = [[] for r in range(7)]
    for r in (2, 4, 6, 7):
        t = admissible_triple(holes[r-1])
        if t is None:
            return {"status": "NECESSARY TRIPLE TEST PASSES", "triple_free_parent": r,
                    "tail_feasibility_asserted": False}
        kernel[r-1] = t
    capacities = original_capacities(kernel)
    need(sum(c for n, c in capacities) == 45, "pattern does not give the promised45 budget")
    terms = hitting_clause(kernel)
    need(all([n, a] not in terms for n, a in phases), "separator clause is not violated")
    return {"status": "EXACT TAIL CAPACITY OBSTRUCTION", "kernel_cofactor_fibers": kernel,
            "physical_points": 48, "capacity_budget": 45, "base_clause": terms,
            "base_clause_canonical_sha256": sha256(json.dumps(terms, separators=(",", ":")).encode()).hexdigest(),
            "scope": "This original base stage cannot be completed by its24 remaining10080-divisor resources; P remains open."}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-json", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    result = separate(json.loads(args.base_json.read_text()))
    args.out.write_text(json.dumps(result, sort_keys=True, separators=(",", ":"))+"\n")
    print(json.dumps({k: v for k, v in result.items() if k != "base_clause"}, sort_keys=True))
