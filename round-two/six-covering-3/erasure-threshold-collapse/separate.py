"""Complete12/13-point rainbow diagnostics, each sufficient for noncompletion.

Passing both necessary tests does not establish tail feasibility. The search
visits every increasing tuple; symmetry is only the order of its own points.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
from model import BASE, PREFIX, capacities, hitting_clause, need


def rainbow(points, k, mixed3=False):
    H = sorted(set(points))
    need(type(k) is int and k in (3, 4) and all(type(y) is int and 0 <= y < 315 for y in H),
         "invalid rainbow tuple domain")
    masks = {d: [sum(1 << y for y in range(a, 315, d)) for a in range(d)] for d in (5, 7, 9)}
    def visit(chosen, remaining):
        if len(chosen) == k:
            return chosen if not mixed3 or len({y % 3 for y in chosen}) >= 2 else None
        if remaining.bit_count() < k - len(chosen):
            return None
        while remaining:
            bit = remaining & -remaining
            y = bit.bit_length() - 1
            remaining -= bit
            forbidden = masks[5][y % 5] | masks[7][y % 7] | masks[9][y % 9]
            result = visit(chosen + [y], remaining & ~forbidden)
            if result is not None:
                return result
        return None
    return visit([], sum(1 << y for y in H))


def separate(phases):
    need(isinstance(phases, list) and len(phases) == len(BASE) and all(
        isinstance(row, list) and len(row) == 2 and type(row[0]) is int and
        type(row[1]) is int and 0 <= row[1] < row[0] for row in phases) and
        sorted(n for n, a in phases) == list(BASE), "invalid original BASE inventory")
    H = [[] for _ in range(7)]
    for x in range(2520):
        if all(x % n != a for n, a in (*PREFIX, *phases)):
            need(x % 8 != 0, "unexpected eighth parent")
            H[x % 8 - 1].append(x % 315)
    parents = (2, 4, 6, 7)
    kernel = [[] for _ in range(7)]
    for r in parents:
        triple = rainbow(H[r-1], 3, mixed3=True)
        if triple is None:
            break
        kernel[r-1] = triple
    else:
        return obstruction(kernel, phases, "CREDITED12_POINT_KERNEL")
    triples = {r: rainbow(H[r-1], 3) for r in parents}
    if all(triples.values()):
        for large in parents:
            quad = rainbow(H[large-1], 4)
            if quad is not None:
                kernel = [[] for _ in range(7)]
                for r in parents:
                    kernel[r-1] = quad if r == large else triples[r]
                return obstruction(kernel, phases, "THIRTEEN_POINT_KERNEL")
    return {"status": "NECESSARY12_AND13_TESTS_PASS", "tail_feasibility_asserted": False}


def obstruction(kernel, phases, kind):
    total = 4*sum(map(len, kernel)); budget = sum(c for n, c in capacities(kernel))
    need(budget < total, "separator returned no exact strict obstruction")
    terms = hitting_clause(kernel)
    need(not any(row in terms for row in phases), "emitted clause is not violated")
    return {"status": kind, "kernel": kernel, "physical_points": total,
            "tail_capacity_budget": budget, "clause": terms,
            "clause_sha256": sha256(json.dumps(terms, separators=(",", ":")).encode()).hexdigest(),
            "scope": "This BASE stage is nonextendible; owned P remains open."}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--base-json', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    result = separate(json.loads(args.base_json.read_text()))
    args.out.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'clause'}, sort_keys=True))
