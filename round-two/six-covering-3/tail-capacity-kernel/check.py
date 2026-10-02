"""Exact cofactor checker; imports no literal audit, encoder or solver."""

from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from math import gcd
from pathlib import Path
import sys

PREFIX = [[8, 0], [9, 0], [10, 1], [14, 1], [12, 10]]
D = (1, 3, 5, 7, 9, 15, 21, 35, 45, 63, 105, 315)
BASE = tuple(n for n in range(8, 2521) if 2520 % n == 0 and
             n not in {n for n, a in PREFIX})


def need(condition, message):
    if not condition:
        raise ValueError(message)


def validate(fixture):
    need(fixture["agent"] == "six-covering-3" and fixture["role"] == "researcher" and
         fixture["schema"] == 1 and fixture["prefix"] == PREFIX, "wrong declared scope")
    phases = fixture["base_phases"]
    need(isinstance(phases, list) and len(phases) == len(BASE), "missing base resource")
    need(all(isinstance(row, list) and len(row) == 2 and type(row[0]) is int and
             type(row[1]) is int and 0 <= row[1] < row[0] for row in phases),
         "illegal original phase")
    need(tuple(sorted(n for n, a in phases)) == BASE, "wrong or repeated original label")
    kernel = fixture["kernel_cofactor_fibers"]
    need(isinstance(kernel, list) and len(kernel) == 7 and all(
        isinstance(H, list) and all(type(x) is int and 0 <= x < 315 for x in H) and
        H == sorted(set(H)) for H in kernel), "invalid labeled kernel")
    need([r for r, H in enumerate(kernel, 1) if H] == [2, 4, 6, 7] and
         all(len(H) == 3 for H in kernel if H), "wrong four-parent twelve-point domain")
    initial = [set() for r in range(7)]
    holes = [set() for r in range(7)]
    for x in range(2520):
        if all(x % n != a for n, a in PREFIX):
            need(x % 8 != 0, "unexpected eighth parent")
            initial[x % 8 - 1].add(x % 315)
            if all(x % n != a for n, a in phases):
                holes[x % 8 - 1].add(x % 315)
    need(all(set(K) <= H for K, H in zip(kernel, holes)),
         "kernel is not contained in the actual shared-base residual")
    need([r for r, H in enumerate(holes, 1) if not H] == [1, 3, 5],
         "wrong actual empty parents")
    need(all(x % 3 != 1 for r in (2, 6) for x in initial[r - 1]),
         "missing original12 ternary restriction")
    return phases, kernel, [sorted(H) for H in holes]


def cofactor_capacities(fibers):
    return [(d, max((max(Counter(x % d for x in H).values(), default=0)
                    for H in fibers), default=0)) for d in D]


def original_capacities(fibers):
    M = cofactor_capacities(fibers)
    # Each16d class occupies two of the four32 children; each32d class one.
    return sorted([[16*d, 2*c] for d, c in M] + [[32*d, c] for d, c in M])


def supports(fibers):
    singles = []; pairs = []
    for H in fibers:
        g = 315
        for x in H[1:]:
            g = gcd(g, x-H[0])
        singles.append([1 << i for i, d in enumerate(D) if not H or g % d == 0])
        two = []
        for i, j in combinations(range(len(D)), 2):
            d, e = D[i], D[j]
            for a in range(d):
                rest = [x for x in H if x % d != a]
                if not rest or all(x % e == rest[0] % e for x in rest):
                    two.append((1 << i) | (1 << j))
                    break
        pairs.append(two)
    return singles, pairs


def all_cut_minima(fibers):
    singles, pairs = supports(fibers)
    low2 = 10**9; low3 = 10**9
    for B in range(1 << len(D)):
        Q1 = sum(not H or any(s & B == 0 for s in S)
                 for H, S in zip(fibers, singles))
        Q2 = sum(not H or any(s & B == 0 for s in S) or any(t & B == 0 for t in T)
                 for H, S, T in zip(fibers, singles, pairs))
        low2 = min(low2, 8*Q1 + 3*B.bit_count())
        low3 = min(low3, 24*Q2 + 10*B.bit_count())
    need(low2 >= 20 and low3 >= 72, "credited q2/q3 cuts reject this fixture")
    return {"q2": low2, "q3": low3}


def all_higher_thresholds(kernel):
    need(sum(not H for H in kernel) == 3 and max(map(len, kernel)) == 3,
         "higher-threshold bridge requires three empties and at most three points")
    witnesses = 0; small_pools = 0
    for B in range(1 << len(D)):
        legal = [d for i, d in enumerate(D) if not B & (1 << i)]
        b = B.bit_count()
        if len(legal) >= 3:
            for H in kernel:
                if H:
                    classes = [(d, x % d) for d, x in zip(legal[:3], H)]
                    need(len({d for d, a in classes}) == 3 and all(
                        any(x % d == a for d, a in classes) for x in H),
                        "failed distinct-label three-class witness")
                    witnesses += 1
            # Q=7 gives difference (12+2b)q +12-b, positive for ALL q>=4.
            slope, constant = 12+2*b, 12-b
        else:
            small_pools += 1
            need(b >= 10, "invalid small-pool complement")
            # Q>=3 gives difference (2b-4)q +12-b, positive for ALL q>=4.
            slope, constant = 2*b-4, 12-b
        need(slope >= 0 and 4*slope + constant >= 0,
             "infinite affine threshold bridge failed")
    return {"three_class_witnesses": witnesses, "small_pool_masks": small_pools,
            "all_integer_q_at_least_4": True}


def minimality():
    vectors = 0
    for h in product(range(12), repeat=4):
        N = sum(h)
        if N > 11:
            continue
        vectors += 1
        if N == 0:
            continue
        hmax = max(h)
        M3 = max((h[0]+1)//2, (h[1]+2)//3, (h[2]+1)//2, (h[3]+2)//3)
        # Each of the ten labels other than1/3 has capacity at least one.
        need(3*(hmax+M3+10) >= 4*N, "eleven-point capacity lower bound failed")
    return vectors


def hitting_clause(kernel):
    K = [x for x in range(2520) if x % 8 != 0 and x % 315 in kernel[x % 8-1]]
    need(len(K) == 12, "wrong lower-period kernel size")
    return [[n, a] for n in BASE for a in sorted({x % n for x in K})]


def run(fixture):
    phases, kernel, holes = validate(fixture)
    KC = original_capacities(kernel); HC = original_capacities(holes)
    kernel_size = 4*sum(map(len, kernel)); budget = sum(c for n, c in KC)
    need(kernel_size == 48 and budget == 45 and budget < kernel_size,
         "no strict unit-weight kernel obstruction")
    clause = hitting_clause(kernel)
    need(not any([n, a] in clause for n, a in phases), "stage meets the kernel clause")
    return {"agent": "six-covering-3", "role": "researcher", "schema": 1,
            "kernel_sizes": list(map(len, kernel)), "kernel_physical_points": kernel_size,
            "kernel_original_capacities": KC, "kernel_capacity_budget": budget,
            "kernel_deficit": kernel_size-budget, "kernel_cut_minima": all_cut_minima(kernel),
            "higher_thresholds": all_higher_thresholds(kernel),
            "minimality_count_vectors": minimality(), "stage_sizes": list(map(len, holes)),
            "stage_physical_points": 4*sum(map(len, holes)),
            "stage_original_capacities": HC, "stage_capacity_budget": sum(c for n, c in HC),
            "stage_cut_minima": all_cut_minima(holes), "hitting_clause_terms": len(clause),
            "hitting_clause_sha256": sha256(json.dumps(clause, separators=(",", ":")).encode()).hexdigest()}


def verify(fixture, expected):
    result = run(fixture)
    need(result == expected, "frozen exact evidence differs")
    return result


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    fixture = json.loads(Path(sys.argv[1] if len(sys.argv) > 1 else here / "fixture.json").read_text())
    expected = json.loads((here / "expected.json").read_text())
    result = verify(fixture, expected)
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
