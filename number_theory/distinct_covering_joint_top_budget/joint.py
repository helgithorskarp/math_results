"""Exact joint top-resource budget; six-covering-2, researcher.

The universal reduction is written separately. This routine implements
cofactors with at most four divisors and returns actual phase witnesses.
It never asserts that the maximizing phases form a covering.
"""
from itertools import product
from math import gcd,lcm


def require(condition, message):
    if not condition:
        raise ValueError(message)


def divisors(n):
    require(type(n) is int and n >= 1, "Positive integer required")
    return [d for d in range(1, n+1) if n % d == 0]


def radical(n):
    require(type(n) is int and n >= 2, "Base must be an integer at least two")
    result, p = 1, 2
    while p*p <= n:
        if n % p == 0:
            result *= p
            while n % p == 0:
                n //= p
        p += 1
    return result*n


def validate(B, C, b, u, base_v):
    require(all(type(x) is int for x in (B, C, b)), 'Integer parameters required')
    require(B >= 2 and C >= 2 and gcd(B, C) == 1, 'Coprime base/cofactor required')
    T = B // radical(B)
    require(b >= 1 and T % b == 0, 'Invalid block period')
    for w, size in [(u, B*C), (base_v, b*C)]:
        require(isinstance(w, (list, tuple)) and len(w) == size, 'Component domain')
        require(all(type(a) is int and a >= 0 for a in w), 'Nonnegative integer weights required')
    D = divisors(C)
    require(len(D) <= 4, 'General-size cofactor optimizer is not implemented')
    return T, D


def crt_phase(B, d, alpha, r):
    return alpha if d == 1 else (alpha + B*((r-alpha)*pow(B, -1, d) % d)) % (B*d)


def best_partition(costs, size):
    """First-element subset recurrence enumerates every unordered partition."""
    values, witnesses = {0: 0}, {0: ()}
    for mask in range(1, 1 << size):
        first = mask & -mask
        best, chosen = -1, None
        subset = mask
        while subset:
            if subset & first:
                candidate = costs[subset] + values[mask ^ subset]
                if candidate > best:
                    best, chosen = candidate, (subset,) + witnesses[mask ^ subset]
            subset = (subset-1) & mask
        values[mask], witnesses[mask] = best, chosen
    return values[(1 << size)-1], witnesses[(1 << size)-1]


def actual_score(B, C, b, u, base_v, phases):
    """Physical arithmetic progressions, not the subset/CRT maximization."""
    N, T = B*C, B//radical(B)
    counts, points, unrestricted = {}, [], 0
    require(len(phases) == len(divisors(C)), 'Missing top phases')
    require({n for n, a in phases} == {B*d for d in divisors(C)}, 'Wrong top resources')
    for n, a in phases:
        require(type(a) is int and 0 <= a < n, 'Invalid top phase')
        unrestricted += sum(u[a::n])
        for x in range(a, N, n):
            key = (x % B) % T, x % C
            counts[key] = counts.get(key, 0) + 1
            points.append((key, base_v[x % (b*C)]))
    useful = sum(w for key, w in points if counts[key] >= 2)
    return unrestricted + useful


def joint_budget(B, C, b, u, base_v):
    T, D = validate(B, C, b, u, base_v)
    N, rho = B*C, radical(B)
    urows = [[0]*C for _ in range(B)]
    vrows = [[0]*C for _ in range(b)]
    for x, w in enumerate(u):
        urows[x % B][x % C] = w
    for x, w in enumerate(base_v):
        vrows[x % b][x % C] = w
    vprofiles = list(map(tuple, vrows))
    A, attaining = {}, {}
    for d in D:
        A[d], attaining[d] = [], []
        for q in range(T):
            vals, args = [], []
            for r in range(d):
                candidates = [(sum(urows[q + T*j][r::d]), q + T*j) for j in range(rho)]
                value, alpha = max(candidates, key=lambda item: item[0])
                vals.append(value); args.append(alpha)
            A[d].append(vals); attaining[d].append(args)
    costs, vcosts, witnesses = {}, {}, {}
    patterns, label_rows = 0, 0
    for mask in range(1, 1 << len(D)):
        group = [d for i, d in enumerate(D) if mask & (1 << i)]
        best, vbest, chosen = -1, 0, None
        for phases in product(*(range(d) for d in group)):
            patterns += 1
            coefficients = [(z, k) for z in range(C)
                            if (k := sum(z % d == r for d, r in zip(group, phases))) >= 2]
            charge = {row: sum(k*row[z] for z, k in coefficients) for row in set(vprofiles)}
            vbest = max(vbest, max(charge.values()))
            for q in range(T):
                label_rows += 1
                value = sum(A[d][q][r] for d, r in zip(group, phases)) + charge[vprofiles[q % b]]
                if value > best:
                    best = value
                    chosen = {'q': q, 'cofactor_phases': list(phases), 'divisors': group,
                              'B_coordinates': [attaining[d][q][r] for d, r in zip(group, phases)]}
        costs[mask], vcosts[mask], witnesses[mask] = best, vbest, chosen
    budget, partition = best_partition(costs, len(D))
    F, _ = best_partition(vcosts, len(D))
    actual = []
    for mask in partition:
        w = witnesses[mask]
        for d, alpha, r in zip(w['divisors'], w['B_coordinates'], w['cofactor_phases']):
            actual.append((B*d, crt_phase(B, d, alpha, r)))
    actual.sort()
    score = actual_score(B, C, b, u, base_v, actual)
    require(score == budget, 'Joint budget witness does not attain the subset maximum')
    v = [base_v[x % (b*C)] for x in range(N)]
    total = [a+c for a, c in zip(u, v)]
    ordinary = sum(max(sum(total[a::n]) for a in range(n)) for n in [B*d for d in D])
    Cu = sum(max(sum(u[a::n]) for a in range(n)) for n in [B*d for d in D])
    require(budget <= min(ordinary, Cu+F), 'Joint upper comparison failed')
    if not any(base_v):require(budget == Cu, 'v=0 endpoint')
    if not any(u):require(budget == F, 'u=0 endpoint')
    return {'joint_budget': budget, 'periodic_budget': F, 'separate_top_budget': Cu+F,
            'ordinary_top_capacity': ordinary, 'u_top_capacities': Cu,
            'winning_partition': list(partition), 'actual_witness_phases': [list(a) for a in actual],
            'group_budgets': {str(mask): val for mask, val in costs.items()},
            'group_witnesses': {str(mask): val for mask, val in witnesses.items()},
            'group_phase_patterns': patterns, 'group_label_phase_rows': label_rows}


def literal_maximum(B, C, b, u, base_v):
    """All actual top phases, with literal physical points and grouped counts."""
    T, D = validate(B, C, b, u, base_v)
    N = B*C
    resources = [B*d for d in D]
    prepared = []
    for n in resources:
        classes = []
        for a in range(n):
            points = [( ((x % B) % T, x % C), base_v[x % (b*C)]) for x in range(a, N, n)]
            classes.append((sum(u[a::n]), points))
        prepared.append(classes)
    best, witness, checked = -1, None, 0
    for phases in product(*(range(n) for n in resources)):
        counts, points, score = {}, [], 0
        for classes, a in zip(prepared, phases):
            value, footprint = classes[a]
            score += value
            points.extend(footprint)
            for key, w in footprint:counts[key] = counts.get(key, 0)+1
        score += sum(w for key, w in points if counts[key] >= 2)
        checked += 1
        if score > best:best, witness = score, phases
    return {'maximum': best, 'actual_phase_tuples': checked,
            'attaining_phases': [list(pair) for pair in zip(resources, witness)]}


def periodic_known_footprint(N, base_v, n, a):
    """Exact CRT footprint formula; known classes retain multiplicity."""
    Q=len(base_v)
    require(all(type(x) is int for x in (N,n,a)), 'Integer footprint parameters')
    require(N>=1 and Q>=1 and N%Q==0 and n>=2 and N%n==0 and 0<=a<n, 'Footprint domain')
    require(all(type(w) is int and w>=0 for w in base_v), 'Invalid periodic weight')
    g=gcd(Q,n)
    return (N//lcm(Q,n))*sum(base_v[a%g::g])


def known_bound(B,C,b,anchors,u,base_v,minimum=8):
    """Affine necessary bound; all eligible actual unused divisors are allowed.

    Only u must vanish on known classes. The periodic component may be
    positive there. A strict gap excludes only the exact prescribed prefix.
    This function supports at most four top resources, as joint_budget does.
    """
    validate(B,C,b,u,base_v);N=B*C;Q=b*C
    require(type(minimum) is int and minimum>=2, 'Invalid minimum')
    require(isinstance(anchors,(list,tuple)) and
            all(isinstance(A,(list,tuple)) and len(A)==2 for A in anchors), 'Known class list')
    require(all(type(n) is int and type(a) is int and n>=minimum and N%n==0 and 0<=a<n
                for n,a in anchors), 'Invalid known class')
    require(len({n for n,a in anchors})==len(anchors), 'Distinct known moduli required')
    S={B*d for d in divisors(C)}
    require(min(S)>=minimum and not S.intersection(n for n,a in anchors), 'Top resources must be eligible and unplaced')
    covered=[any(x%n==a for n,a in anchors) for x in range(N)]
    require(all(not u[x] for x in range(N) if covered[x]), 'Unrestricted component support')
    J=joint_budget(B,C,b,u,base_v)
    total=[w+base_v[x%Q] for x,w in enumerate(u)]
    R=[n for n in divisors(N) if n>=minimum and n not in {m for m,a in anchors}]
    capacities={n:max(sum(total[a::n]) for a in range(n)) for n in R}
    known={n:periodic_known_footprint(N,base_v,n,a) for n,a in anchors}
    demand=sum(total)-sum(known.values())
    outside=sum(value for n,value in capacities.items() if n not in S)
    bound=outside+J['joint_budget']
    residual=[w if not covered[x] else 0 for x,w in enumerate(total)]
    ordinary_residual=sum(max(sum(residual[a::n]) for a in range(n)) for n in R)
    return {'N':N,'B':B,'C':C,'b':b,'Q':Q,'demand':demand,'total_demand':sum(total),
            'known_footprints':[[n,known[n]] for n,a in anchors],
            'outside_capacity':outside,'capacity':bound,'strict_gap':demand-bound,
            'ordinary_capacity':sum(capacities.values()),
            'separate_mixed_capacity':outside+J['separate_top_budget'],
            'ordinary_residual_demand':sum(residual),'ordinary_residual_capacity':ordinary_residual,
            'joint':J}
