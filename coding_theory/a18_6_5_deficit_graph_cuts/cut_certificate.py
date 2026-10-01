"""Exact colored-triple certificate for the deficit-graph cut inequality."""
from pathlib import Path
from fractions import Fraction
import itertools
import json
import resource
import time

from paths import WORK
ROOT = WORK
PAIRS = ((0, 1), (0, 2), (1, 2))

def primary(graph, subset):
    # Compute directly from incidence masks, without a graph-class shortcut.
    degrees = [0, 0, 0]
    for i, (x, y) in enumerate(PAIRS):
        if graph >> i & 1:
            degrees[x] += 1; degrees[y] += 1
    a = sum(bool(graph >> i & 1) for i, p in enumerate(PAIRS) if all(subset >> x & 1 for x in p))
    b = sum(not bool(graph >> i & 1) for i, p in enumerate(PAIRS) if all(subset >> x & 1 for x in p))
    h = sum(degrees[x] == 2 for x in range(3) if subset >> x & 1)
    low = sum(degrees[x] == 0 for x in range(3) if not (subset >> x & 1))
    return a, b, h, low

def literal(graph, subset):
    edge_set = {frozenset(p) for i, p in enumerate(PAIRS) if graph >> i & 1}
    inside = {x for x in range(3) if subset >> x & 1}
    pairs_inside = {frozenset(p) for p in itertools.combinations(sorted(inside), 2)}
    high = 0
    low = 0
    for x in range(3):
        adjacent = {y for y in range(3) if y != x and frozenset((x, y)) in edge_set}
        if x in inside and len(adjacent) == 2:
            high += 1
        if x not in inside and not adjacent:
            low += 1
    return len(pairs_inside & edge_set), len(pairs_inside - edge_set), high, low

def equality_boundary(s, q):
    t = 18 - s
    edge_pairs = Fraction(5 * s - q, 2)
    nonedges = Fraction(s * (s - 6) + q, 2)
    a = 4 * edge_pairs
    b = nonedges
    slack_bound = 6 * s + 2 * t - (a - b)
    expected = Fraction(5 * q - (s - 6) * (12 - s), 2)
    if slack_bound != expected:
        raise RuntimeError("symbolic aggregate identity mismatch")
    return {"size": s, "cut": q, "slack_bound": str(slack_bound), "lower_rhs": (s - 6) * (12 - s)}

def main():
    start = time.monotonic()
    rows = []
    for graph in range(8):
        for subset in range(8):
            p = primary(graph, subset)
            r = literal(graph, subset)
            if p != r:
                raise RuntimeError("actual colored-triple coefficients disagree")
            a, b, h, low = p
            slack = h + low - a + b
            if slack < 0:
                raise RuntimeError("a literal triple violates the claimed certificate")
            rows.append({"graph": graph, "subset": subset, "a": a, "b": b,
                         "h": h, "low": low, "slack": slack})
    aggregates = [equality_boundary(s, q) for s in range(19) for q in range(91)]
    component_orders = []
    def partitions(total, minimum=6):
        if not total:
            yield ()
        for first in range(minimum, total + 1, 2):
            for tail in partitions(total - first, first):
                yield (first,) + tail
    for sizes in partitions(18):
        violated = [s for s in sizes if (s - 6) * (12 - s) > 0]
        component_orders.append({"orders": sizes, "cut_bound_excludes": bool(violated)})
    # The bridge boundary follows from parity and equality, not floating LP.
    bridge_sides = [s for s in range(1, 18) if s >= 6 and 18 - s >= 6 and s % 2 == 1
                    and (s - 6) * (12 - s) <= 5]
    if bridge_sides != [7, 11]:
        raise RuntimeError("bridge order derivation mismatch")
    k6_solutions = []
    for a in range(21):
        for b in range(61):
            c = 36 - b
            d = 96 - a - b - c
            if 3 * a + b == 60 and min(c, d) >= 0 and 3 * a <= 36 and b <= 24:
                k6_solutions.append([a, b, c, d])
    if k6_solutions != [[12, 24, 12, 48]]:
        raise RuntimeError("K6 exact integer boundary is not the expected singleton")
    word_solutions = []
    for n3 in range(21):
        for n2 in range(73):
            n1 = 120 - 3 * n3 - 2 * n2
            n0 = 72 - n1 - n2 - n3
            if min(n0, n1) >= 0 and 3 * n3 + n2 == 60 and n3 == 8:
                word_solutions.append([n0, n1, n2, n3, 0, 0])
    if word_solutions != [[4, 24, 36, 8, 0, 0]]:
        raise RuntimeError("K6 original-word composition bridge mismatch")
    record = {"agent": "six-code-3", "role": "researcher", "status": "COMPLETE",
              "literal_coefficients": rows, "literal_cases": len(rows), "aggregate_identity_cases": len(aggregates),
              "cut_inequality": "5q >= (s-6)(12-s)", "component_partitions": component_orders,
              "bridge_side_sizes": bridge_sides, "k6_uncovered_triple_composition": k6_solutions[0],
              "k6_original_word_composition": word_solutions[0],
              "seconds": round(time.monotonic() - start, 6), "maxrss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              "ordinary_bridges_formalized": False, "independent_peer_review": False}
    (ROOT / "cut_record.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({k: v for k, v in record.items() if k != "literal_coefficients"}))

if __name__ == "__main__":
    main()
