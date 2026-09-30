"""Exact four-resource budgets and physical mixed-weight capacity checks.

Author: six-covering-2, researcher. Python 3.10+, standard library only.
The universal covering inequality is proved in proof.md. The partition
oracle checks its finite budget definition, not existence of a covering.
"""
from itertools import product
from math import gcd, isqrt
import hashlib
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def prime(n):
    return type(n) is int and n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))


def divisors(n):
    require(type(n) is int and n >= 1, "Positive integer required")
    return [d for d in range(1, n + 1) if n % d == 0]


def radical(n):
    require(type(n) is int and n >= 2, "Base must be an integer at least two")
    answer, d = 1, 2
    while d * d <= n:
        if n % d == 0:
            answer *= d
            while n % d == 0:
                n //= d
        d += 1
    return answer * n


def validate_weights(weights, C):
    require(isinstance(weights, (list, tuple)) and len(weights) > 0, "Empty weight matrix")
    require(all(isinstance(row, (list, tuple)) and len(row) == C for row in weights), "Wrong weight domain")
    require(all(type(w) is int and w >= 0 for row in weights for w in row), "Nonnegative integer weights required")


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def crt_pair(p, q, r, s):
    return (r + p * (((s - r) * pow(p, -1, q)) % q)) % (p * q)


def pq_budget(p, q, weights, include_table=False):
    """Closed form for cofactor p*q, where p and q are distinct primes."""
    require(prime(p) and prime(q) and p != q, "Two distinct primes required")
    C = p * q
    validate_weights(weights, C)
    U = [[sum(row[r::p]) for r in range(p)] for row in weights]
    V = [[sum(row[s::q]) for s in range(q)] for row in weights]
    Mp, Mq, M = max(map(max, U)), max(map(max, V)), max(map(max, weights))
    H, events = 0, []
    for r, s, u in product(range(p), range(q), range(C)):
        i = crt_pair(p, q, r, s)
        c = 1 if u % p == r or u % q == s else 2
        values = [2 * U[t][r] + 2 * V[t][s] - row[i] + c * row[u]
                  for t, row in enumerate(weights)]
        H = max(H, max(values))
        events.append([r, s, u, values])
    pairs = 2 * max(Mp, Mq) + 2 * M
    result = {"budget": max(H, pairs), "all_one_group": H, "two_pairs": pairs,
              "phase_table_rows": len(events), "phase_table_sha256": digest(events)}
    if include_table:
        result["table"] = events
    return result


def p3_budget(p, weights, include_table=False):
    """Closed form for cofactor p**3, where p is prime."""
    require(prime(p), "Prime required")
    C = p ** 3
    validate_weights(weights, C)
    U = [[sum(row[r::p]) for r in range(p)] for row in weights]
    V = [[sum(row[s::(p*p)]) for s in range(p*p)] for row in weights]
    M1, M3 = max(map(max, U)), max(map(max, weights))
    H, events = 0, []
    for r, s, u in product(range(p), range(p*p), range(C)):
        a = 1 if s % p == r else 2
        c = 1 if u % p == r or u % (p*p) == s else 2
        values = [2 * U[t][r] + a * V[t][s] + c * row[u]
                  for t, row in enumerate(weights)]
        H = max(H, max(values))
        events.append([r, s, u, values])
    pairs = 2 * M1 + 2 * M3
    result = {"budget": max(H, pairs), "all_one_group": H, "two_pairs": pairs,
              "phase_table_rows": len(events), "phase_table_sha256": digest(events)}
    if include_table:
        result["table"] = events
    return result


def partitions4():
    """Restricted growth strings, rather than merging resource subsets."""
    answer = []
    for tail in product(range(4), repeat=3):
        labels = (0,) + tail
        if any(labels[j] > max(labels[:j]) + 1 for j in range(1, 4)):
            continue
        answer.append(tuple(tuple(i for i, k in enumerate(labels) if k == j)
                            for j in range(max(labels) + 1)))
    require(len(answer) == len(set(answer)) == 15, "Incomplete partition enumeration")
    return answer


def definition_budget(periods, weights, include_table=False):
    """Literal definition: every partition, phase tuple and base-label maximum.

    This routine covers four divisors, not a general-size cofactor search.
    It independently counts active indicators, without the closed formulas.
    """
    require(isinstance(periods, (tuple, list)) and len(periods) == 4, "Four periods required")
    require(all(type(d) is int and d >= 1 for d in periods), "Invalid periods")
    C = periods[-1]
    require(periods[0] == 1 and set(periods) == set(divisors(C)) and len(set(periods)) == 4,
            "Periods must be the four divisors of the cofactor")
    validate_weights(weights, C)
    parts = partitions4()
    cache, events = {}, []
    best, H, checked = 0, 0, 0
    for tail in product(*(range(d) for d in periods[1:])):
        phases = (0,) + tail

        def group_max(group):
            if len(group) < 2:
                return 0
            key = group, tuple(phases[j] for j in group)
            if key not in cache:
                counts = [sum(z % periods[j] == phases[j] for j in group) for z in range(C)]
                cache[key] = max(sum(k * row[z] for z, k in enumerate(counts) if k >= 2)
                                 for row in weights)
            return cache[key]

        counts = [sum(z % periods[j] == phases[j] for j in range(4)) for z in range(C)]
        values = [sum(k * row[z] for z, k in enumerate(counts) if k >= 2) for row in weights]
        H = max(H, max(values))
        events.append(list(tail) + [values])
        for part in parts:
            best = max(best, sum(group_max(group) for group in part))
            checked += 1
    result = {"budget": best, "all_one_group": H, "partitions": len(parts),
              "phase_partition_rows": checked, "phase_table_rows": len(events),
              "phase_table_sha256": digest(events)}
    if include_table:
        result["table"] = events
    return result


def covering_hypotheses(N, B, b, C, anchors, minimum=8):
    require(all(type(n) is int for n in (N, B, b, C, minimum)), "Integer parameters required")
    require(B >= 2 and C >= 2 and N == B * C and gcd(B, C) == 1, "Cofactor hypotheses")
    require(b >= 1 and (B // radical(B)) % b == 0, "Invalid block period")
    require(minimum >= 2, "Minimum modulus at least two required")
    require(isinstance(anchors, (list, tuple)), "Anchor list required")
    require(all(isinstance(A, (list, tuple)) and len(A) == 2 for A in anchors), "Invalid anchor shape")
    require(all(type(n) is int and type(a) is int and n >= minimum and N % n == 0 and 0 <= a < n
                for n, a in anchors), "Invalid actual anchor")
    require(len({n for n, a in anchors}) == len(anchors), "Repeated actual modulus")
    S = {B * d for d in divisors(C)}
    require(min(S) >= minimum and not S.intersection(n for n, a in anchors),
            "All top resources must be eligible and unplaced")
    return S


def physical_capacity(N, B, b, periods, anchors, u, base_v, minimum=8):
    """Literal actual-modulus maxima; v is a b*C-periodic lifted component."""
    require(isinstance(periods, (list, tuple)) and len(periods) == 4, "Four periods required")
    C = periods[-1]
    S = covering_hypotheses(N, B, b, C, anchors, minimum)
    Q = b * C
    for values, size in ((u, N), (base_v, Q)):
        require(isinstance(values, (list, tuple)) and len(values) == size, "Wrong component domain")
        require(all(type(w) is int and w >= 0 for w in values), "Invalid component weights")
    v = [base_v[x % Q] for x in range(N)]
    require(all(not (u[x] or v[x]) or not any(x % n == a for n, a in anchors) for x in range(N)),
            "Components fail support on prescribed classes")
    weights = [[0] * C for t in range(b)]
    for x, w in enumerate(base_v):
        weights[x % b][x % C] = w
    if prime(periods[1]) and prime(periods[2]) and periods[1] * periods[2] == C:
        closed = pq_budget(periods[1], periods[2], weights)
    elif prime(periods[1]) and tuple(periods) == (1, periods[1], periods[1]**2, periods[1]**3):
        closed = p3_budget(periods[1], weights)
    else:
        raise ValueError("Unsupported four-divisor cofactor")
    # Deduplication changes no maximum over base labels. The definition
    # already permits different groups to choose independent labels.
    literal = definition_budget(periods, sorted(set(map(tuple, weights))))
    require(closed["budget"] == literal["budget"], "Partition budget mismatch")
    total = [a + c for a, c in zip(u, v)]
    R = [n for n in divisors(N) if n >= minimum and n not in {m for m, a in anchors}]
    capacities = {n: max(sum(total[a::n]) for a in range(n)) for n in R}
    top_u = {n: max(sum(u[a::n]) for a in range(n)) for n in sorted(S)}
    hybrid = sum(c for n, c in capacities.items() if n not in S) + sum(top_u.values()) + closed["budget"]
    return {"N": N, "B": B, "b": b, "C": C, "Q": Q,
            "actual_unused_resources": len(R), "demand": sum(total),
            "component_demands": [sum(u), sum(v)], "ordinary_capacity": sum(capacities.values()),
            "mixed_capacity": hybrid, "capacity_saving": sum(capacities.values()) - hybrid,
            "gap": sum(total) - hybrid, "partition_budget": closed["budget"],
            "top_u_capacities": [[n, c] for n, c in top_u.items()],
            "actual_capacity_sha256": digest(sorted(capacities.items()))}
