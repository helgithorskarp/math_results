"""Independent physical-period and literal phase-union audit.

No cofactor checker, gcd classifier, CRT-count formula or solver is imported.
"""
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def shape_minima(fibers):
    labels = [n for n in range(1, 316) if 315 % n == 0]
    physical = {n: [sum(1 << x for x in range(a, 315, n)) for a in range(n)]
                for n in labels}
    abilities = []
    for points in fibers:
        bits = sum(1 << x for x in points)
        one = [1 << i for i, n in enumerate(labels)
               if any(bits & ~C == 0 for C in physical[n])]
        two = []
        for i, j in combinations(range(len(labels)), 2):
            if any(bits & ~(A | B) == 0 for A in physical[labels[i]]
                   for B in physical[labels[j]]):
                two.append((1 << i) | (1 << j))
        abilities.append((one, two))
    values = [[], []]
    for excluded in range(4096):
        counts = [0, 0]
        for points, (one, two) in zip(fibers, abilities):
            qualifies_one = not points or any(not (m & excluded) for m in one)
            qualifies_two = qualifies_one or any(not (m & excluded) for m in two)
            counts[0] += bool(qualifies_one)
            counts[1] += bool(qualifies_two)
        values[0].append(8*counts[0]+3*excluded.bit_count())
        values[1].append(24*counts[1]+10*excluded.bit_count())
    require(min(values[0]) >= 20 and min(values[1]) >= 72, "literal cuts reject fixture")
    return {"q2": min(values[0]), "q3": min(values[1])}


def capacities(points, inventory):
    result = []
    for n in inventory:
        all_phases = [0]*n
        for x in points:
            all_phases[x % n] += 1
        result.append([n, max(all_phases)])
    return result


def infinite_threshold_bridge(kernel):
    # Every nonempty fiber has exactly three points, and three fibers are empty.
    labels = [n for n in range(1, 316) if 315 % n == 0]
    witnesses = 0; small = 0
    for banned in range(4096):
        legal = [n for i, n in enumerate(labels) if not (banned >> i) & 1]
        b = 12-len(legal)
        if len(legal) < 3:
            small += 1
            # Worst Q is three empties; compare at q=4 and positive slope.
            at_four = 48+7*b-52
            increment = 12+2*b-16
        else:
            for H in kernel:
                if not H:
                    continue
                union = set()
                for n, point in zip(legal, H):
                    union.update(range(point % n, 315, n))
                require(set(H) <= union, "literal three-class union misses a point")
                witnesses += 1
            # Q is seven; compare at q=4 and its nonnegative increment.
            at_four = 112+7*b-52
            increment = 28+2*b-16
        require(at_four >= 0 and increment >= 0, "failed all-q affine certificate")
    return {"three_class_witnesses": witnesses, "small_pool_masks": small,
            "all_integer_q_at_least_4": True}


def small_size_bridge():
    count = 0
    for total in range(12):
        for a in range(total+1):
            for b in range(total-a+1):
                for c in range(total-a-b+1):
                    d = total-a-b-c
                    count += 1
                    if total == 0:
                        continue
                    largest = max(a, b, c, d)
                    thirds = max((a+1)//2, (b+2)//3, (c+1)//2, (d+2)//3)
                    require(4*total <= 3*(largest+thirds+10),
                            "failed small-cardinality lower budget")
    return count


def run(fixture):
    declared = [[8, 0], [9, 0], [10, 1], [14, 1], [12, 10]]
    require(fixture["prefix"] == declared and fixture["schema"] == 1 and
            fixture["agent"] == "six-covering-3" and fixture["role"] == "researcher",
            "wrong declared original scope")
    base = [n for n in range(8, 2521) if 2520 % n == 0 and n not in (8, 9, 10, 12, 14)]
    phases = fixture["base_phases"]
    require(isinstance(phases, list) and len(phases) == 36 and all(
        isinstance(row, list) and len(row) == 2 and type(row[0]) is int and
        type(row[1]) is int and 0 <= row[1] < row[0] for row in phases) and
        sorted(n for n, a in phases) == base, "invalid original base inventory")
    kernel = fixture["kernel_cofactor_fibers"]
    require(isinstance(kernel, list) and len(kernel) == 7 and all(
        isinstance(H, list) and H == sorted(set(H)) and all(
        type(x) is int and 0 <= x < 315 for x in H) for H in kernel), "invalid kernel")
    require([r for r in range(1, 8) if kernel[r-1]] == [2, 4, 6, 7] and
            all(len(H) == 3 for H in kernel if H), "wrong four-parent kernel")
    original = {n for n, a in declared+phases}
    inventory = [n for n in range(8, 10081) if 10080 % n == 0 and n not in original]
    require(len(original) == 41 and len(inventory) == 24 and
            original.isdisjoint(inventory), "original tail was cloned or consumed")
    uncovered = {x for x in range(10080) if all(x % n != a for n, a in declared+phases)}
    physical_kernel = {x for x in range(10080) if x % 8 != 0 and
                       x % 315 in kernel[x % 8-1]}
    require(physical_kernel <= uncovered and len(physical_kernel) == 48,
            "kernel is not a physical residual subset")
    fibers = []
    for r in range(1, 8):
        copies = [{x % 315 for x in uncovered if x % 32 == r+8*k} for k in range(4)]
        require(all(H == copies[0] for H in copies), "physical copies disagree")
        fibers.append(sorted(copies[0]))
    require(4*sum(map(len, fibers)) == len(uncovered) and
            [r for r in range(1, 8) if not fibers[r-1]] == [1, 3, 5],
            "wrong physical parent inventory")
    initial = [x for x in range(10080) if all(x % n != a for n, a in declared)]
    require(all(x % 3 != 1 for x in initial if x % 8 in (2, 6)),
            "actual original12 does not restrict the two claimed fibers")
    KC = capacities(physical_kernel, inventory); HC = capacities(uncovered, inventory)
    budget = sum(c for n, c in KC)
    require(budget == 45 and budget < len(physical_kernel), "no strict original capacity gap")
    lower_points = sorted({x % 2520 for x in physical_kernel})
    require(len(lower_points) == 12, "wrong lower-period replication")
    clause = [[n, a] for n in base for a in sorted({x % n for x in lower_points})]
    require(all([n, a] not in clause for n, a in phases), "stage hits the supposed residual kernel")
    return {"agent": "six-covering-3", "role": "researcher", "schema": 1,
            "kernel_sizes": list(map(len, kernel)), "kernel_physical_points": len(physical_kernel),
            "kernel_original_capacities": KC, "kernel_capacity_budget": budget,
            "kernel_deficit": len(physical_kernel)-budget,
            "kernel_cut_minima": shape_minima(kernel),
            "higher_thresholds": infinite_threshold_bridge(kernel),
            "minimality_count_vectors": small_size_bridge(), "stage_sizes": list(map(len, fibers)),
            "stage_physical_points": len(uncovered), "stage_original_capacities": HC,
            "stage_capacity_budget": sum(c for n, c in HC),
            "stage_cut_minima": shape_minima(fibers), "hitting_clause_terms": len(clause),
            "hitting_clause_sha256": sha256(json.dumps(clause, separators=(",", ":")).encode()).hexdigest()}


def verify(fixture, expected):
    result = run(fixture)
    require(result == expected, "frozen original evidence differs")
    return result


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    fixture = json.loads(Path(sys.argv[1] if len(sys.argv) > 1 else here / "fixture.json").read_text())
    expected = json.loads((here / "expected.json").read_text())
    print(json.dumps(verify(fixture, expected), sort_keys=True, separators=(",", ":")))
