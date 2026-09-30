"""Solver-free literal certificate checker; no LP, orbit or CRT imports.

The universal proof is the published prescribed binary-cluster lemma7633.
Here all actual physical residues, resource phases and cluster unions are
enumerated. Box decoding uses residue predicates, not Cartesian CRT products.
"""
import json
from itertools import product
from math import gcd, prod
from pathlib import Path
from time import monotonic


def need(condition, message):
    if not condition:
        raise ValueError(message)


def prime_powers(n):
    result = []
    p = 2
    while p*p <= n:
        power = 1
        while n % p == 0:
            n //= p
            power *= p
        if power > 1:
            result.append(power)
        p += 1
    if n > 1:
        result.append(n)
    return result


def decode(length, boxes, values):
    periods = prime_powers(length)
    need(len(boxes) == len(values), 'Box/value length mismatch')
    weights = [0]*length
    occupied = [False]*length
    for axes, w in zip(boxes, values):
        need(type(w) is int and w >= 0 and len(axes) == len(periods), 'Integer weight or axes')
        sets = []
        for axis, P in zip(axes, periods):
            need(bool(axis) and len(set(axis)) == len(axis) and
                 all(type(x) is int and 0 <= x < P for x in axis), 'Axis domain')
            sets.append(set(axis))
        count = 0
        for x in range(length):
            if all(x % P in axis for P, axis in zip(periods, sets)):
                need(not occupied[x], 'Overlapping literal boxes')
                occupied[x] = True
                weights[x] = w
                count += 1
        need(count == prod(len(axis) for axis in axes), 'Physical box cardinality')
    return weights


def verify(c, require_strict=True):
    start = monotonic()
    N, B, C, b, minimum = (c[k] for k in ['N','B','C','b','minimum'])
    need(all(type(x) is int for x in [N,B,C,b,minimum]), 'Integer parameters')
    need(B >= 2 and C >= 2 and minimum >= 2 and B >= minimum and
         B*C == N and gcd(B,C) == 1 and B & (B-1) == 0, 'Binary coprime factorization')
    T = B//2
    need(b >= 1 and T % b == 0, 'Periodic block condition')
    Q = b*C
    A = c['prefix']
    need(len({n for n,a in A}) == len(A), 'Distinct known classes')
    need(all(type(n) is int and type(a) is int and n >= minimum and N % n == 0 and 0 <= a < n
             for n,a in A), 'Known class domain')
    D = [d for d in range(1,C+1) if C%d == 0]
    S = {B*d for d in D}
    need(set(dict(A)) & S == {B}, 'Exactly coarsest top class prescribed')
    P = c['cluster']
    need(len(set(P)) == len(P) and all(type(d) is int and d in D and d > 1 for d in P), 'Cluster domain')
    need(prod(1+d for d in P) <= 100_000, 'Complete certificate phase cap')
    u = decode(N,c['u_boxes'],c['u_values'])
    v = decode(Q,c['v_boxes'],c['v_values'])
    need(all(not u[x] for n,a in A for x in range(a,N,n)), 'u positive on a known class')
    periodic = [v[x%Q] for x in range(N)]
    total = [u[x]+periodic[x] for x in range(N)]
    known = {n:sum(periodic[a::n]) for n,a in A if n not in S}
    R = [n for n in range(minimum,N+1) if N%n == 0 and n not in dict(A)]
    capacities = {n:max(sum(total[a::n]) for a in range(n)) for n in R if n not in S}
    q0, alpha1 = dict(A)[B]%T, (dict(A)[B]+T)%B
    outside, inside = {}, {}
    for d in D:
        if d == 1:
            continue
        n = B*d
        outside[d] = max((sum(total[a::n]) for a in range(n) if a%B%T != q0), default=0)
        inside[d] = max(sum(u[a::n])+2*sum(periodic[a::n]) for a in range(alpha1,n,B))
    cosets = {d:{a:set(range(a,N,B*d)) for a in range(alpha1,B*d,B)} for d in P}
    u_sums = {d:{a:sum(u[x] for x in points) for a,points in cosets[d].items()} for d in P}
    cluster_budget = 0
    evaluated = 0
    for mask in range(1 << len(P)):
        selected = [d for i,d in enumerate(P) if mask >> i & 1]
        unselected_cost = sum(outside[d] for i,d in enumerate(P) if not mask >> i & 1)
        for phases in product(*(range(alpha1,B*d,B) for d in selected)):
            points = set()
            value = 0
            for d,a in zip(selected,phases):
                points.update(cosets[d][a])
                value += u_sums[d][a]
            value += 2*sum(periodic[x] for x in points)
            cluster_budget = max(cluster_budget,value+unselected_cost)
            evaluated += 1
    need(evaluated == prod(1+d for d in P), 'Incomplete cluster phase enumeration')
    top_budget = cluster_budget+sum(max(outside[d],inside[d]) for d in D if d > 1 and d not in P)
    demand = sum(total)-sum(known.values())
    capacity = sum(capacities.values())+top_budget
    residual = [w if all(x%n != a for n,a in A) else 0 for x,w in enumerate(total)]
    ordinary_capacity = sum(max(sum(residual[a::n]) for a in range(n)) for n in R)
    expected = c.get('evidence')
    result = {'demand':demand,'capacity':capacity,'gap':demand-capacity,
              'outside_capacity':sum(capacities.values()),'outside_resources':len(capacities),
              'outside_actual_phases':sum(capacities),'top_upper_budget':top_budget,
              'no_cluster_capacity':sum(capacities.values())+sum(max(outside[d],inside[d]) for d in D if d>1),
              'ordinary_residual_demand':sum(residual),'ordinary_residual_capacity':ordinary_capacity,
              'cluster_phase_cases':evaluated,
              'known_top_periodic_weight':sum(periodic[dict(A)[B]::B]),
              'known_outside_periodic_cost':sum(known.values())}
    if expected is not None:
        need(all(result[k] == expected[k] for k in ['demand','capacity','gap','ordinary_residual_demand','ordinary_residual_capacity']),
             'Advertised totals differ from literal verification')
        need(top_budget == expected['top_bound']['top_upper_budget'], 'Advertised top bound differs')
        need(capacities == {int(k):v for k,v in expected['outside_capacities'].items()}, 'Outside-resource entry mismatch')
        need(known == {int(k):v for k,v in expected['known_outside_periodic_footprints'].items()}, 'Known outside footprint mismatch')
    if require_strict:
        need(demand > capacity, 'Non-strict certificate')
    result['seconds'] = monotonic()-start
    result['all_literal_checks_passed'] = True
    return result
