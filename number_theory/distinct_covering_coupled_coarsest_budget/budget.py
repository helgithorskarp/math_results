"""Exact mixed coarsest-resource upper relaxation, in physical residue units.

Actual author: six-covering-3, researcher. No exact-attainment assertion.
u is unrestricted; v is b*C-periodic. All arithmetic is Python integers.
"""
from math import gcd


def parameters(B, C, b):
    if any(type(n) is not int for n in (B, C, b)) or min(B, C) < 2 or b < 1:
        raise ValueError('Expected integer B,C>=2 and b>=1')
    if gcd(B, C) != 1:
        raise ValueError('B and C must be coprime')
    remaining, radical, prime = B, 1, 2
    while prime * prime <= remaining:
        if remaining % prime == 0:
            radical *= prime
            while remaining % prime == 0:
                remaining //= prime
        prime += 1
    if remaining > 1:
        radical *= remaining
    T = B // radical
    if T % b:
        raise ValueError('b must divide B/rad(B)')
    return B*C, T, tuple(d for d in range(1, C+1) if C % d == 0)


def checked_weights(B, C, b, u, v):
    N, T, divisors = parameters(B, C, b)
    if any(not isinstance(w, (list, tuple)) or len(w) != N
           or any(type(x) is not int or x < 0 for x in w)
           for w in (u, v)):
        raise ValueError('Weights must be nonnegative integer N-vectors')
    if any(v[x] != v[x % (b*C)] for x in range(N)):
        raise ValueError('v must be b*C-periodic')
    return N, T, divisors


def mixed_budget(B, C, b, u, v, pair=None):
    """Compute G_mix, preserving the coarsest block in every resource maximum.

    The written proof permits real weights; this implementation accepts integers.
    Output does not assert that a maximizing phase tuple realizes G_mix.
    """
    N, T, divisors = checked_weights(B, C, b, u, v)
    if pair is not None and (len(pair) != 2 or any(type(d) is not int or d <= 1
                                                or C % d for d in pair)
                             or pair[0] == pair[1]):
        raise ValueError('Designate two distinct noncoarsest cofactor divisors')
    inverse = pow(B, -1, C)
    inverse_b = pow(b, -1, C)
    rows_u = [[u[alpha+B*((z-alpha)*inverse % C)] for z in range(C)]
              for alpha in range(B)]
    rows_v = [[v[t+b*((z-t)*inverse_b % C)] for z in range(C)]
              for t in range(b)]
    A = [max(sum(rows_u[alpha]) for alpha in range(q, B, T)) for q in range(T)]
    ordinary_groups, inside_groups, outside_groups = {}, {}, {}
    top_u = {B: max(A)}
    ordinary_top = {B: max(sum(rows_u[alpha])+sum(rows_v[alpha % b])
                           for alpha in range(B))}
    H, M, u_profiles, v_profiles = {}, {}, {}, {}
    totals = A.copy()
    for d in divisors[1:]:
        v_phases = [[sum(row[r::d]) for r in range(d)] for row in rows_v]
        profile = [[0]*d for q in range(T)] if pair is not None and d in pair else None
        E, I = [0]*T, [0]*T
        largest_u = largest_w = 0
        for alpha, row in enumerate(rows_u):
            q, t = alpha % T, alpha % b
            u_phases = [sum(row[r::d]) for r in range(d)]
            if profile is not None:
                profile[q] = [max(x,y) for x,y in zip(profile[q],u_phases)]
            largest_u = max(largest_u, max(u_phases))
            largest_w = max(largest_w, max(x+y for x,y in zip(u_phases, v_phases[t])))
            E[q] = max(E[q], max(x+y for x,y in zip(u_phases, v_phases[t])))
            I[q] = max(I[q], max(x+2*y for x,y in zip(u_phases, v_phases[t])))
        O = [max((E[s] for s in range(T) if s != q), default=0) for q in range(T)]
        for q in range(T):
            totals[q] += max(O[q], I[q])
        ordinary_groups[d], inside_groups[d], outside_groups[d] = E, I, O
        if profile is not None:
            u_profiles[d], v_profiles[d] = profile, v_phases
        H[d] = [max(row) for row in v_phases]
        M[d] = max(H[d])
        top_u[B*d], ordinary_top[B*d] = largest_u, largest_w
    pure_label_totals = [sum(max(M[d], 2*H[d][t]) for d in divisors[1:])
                         for t in range(b)]
    G = max(pure_label_totals)
    result = {'N': N, 'B': B, 'C': C, 'b': b, 'T': T,
            'G_mix': max(totals), 'label_totals': totals,
            'maximizing_block': totals.index(max(totals)), 'coarsest_u': A,
            'once_profiles': ordinary_groups, 'twice_profiles': inside_groups,
            'outside_profiles': outside_groups, 'top_u_capacities': top_u,
            'ordinary_top_capacities': ordinary_top,
            'ordinary_top_total': sum(ordinary_top.values()),
            'periodic_G': G, 'separate_top_bound': sum(top_u.values())+G,
            'attainability_claimed': False}
    if pair is not None:
        p, d = pair
        intersections = [[[0]*d for r in range(p)] for t in range(b)]
        for t,row in enumerate(rows_v):
            for z,weight in enumerate(row):
                intersections[t][z % p][z % d] += weight
        cases = []
        pair_totals = []
        for q in range(T):
            t = q % b
            both = max(u_profiles[p][q][r]+u_profiles[d][q][s]
                       +2*v_profiles[p][t][r]+2*v_profiles[d][t][s]
                       -intersections[t][r][s]
                       for r in range(p) for s in range(d))
            alternatives = [outside_groups[p][q]+outside_groups[d][q],
                            inside_groups[p][q]+outside_groups[d][q],
                            outside_groups[p][q]+inside_groups[d][q], both]
            P = max(alternatives)
            pair_totals.append(A[q]+P+sum(max(outside_groups[e][q],inside_groups[e][q])
                                          for e in divisors[1:] if e not in pair))
            cases.append(alternatives)
        result.update({'pair':list(pair), 'pair_label_cases':cases,
                       'pair_label_totals':pair_totals,
                       'G_mix_pair':max(pair_totals)})
    return result


def completion_bound(B, C, b, u, v, resources, prescribed, pair=None):
    """Affine necessary inequality; known u+v footprints count with multiplicity."""
    result = mixed_budget(B, C, b, u, v, pair)
    N = result['N']
    resources = tuple(resources)
    prescribed = tuple(tuple(row) for row in prescribed)
    if any(type(n) is not int or n < 2 or N % n for n in resources):
        raise ValueError('Resources must be distinct divisors >=2 of N')
    if len(set(resources)) != len(resources):
        raise ValueError('Repeated unused modulus')
    if any(len(row) != 2 or any(type(x) is not int for x in row)
           or row[0] < 2 or N % row[0] or not 0 <= row[1] < row[0]
           for row in prescribed):
        raise ValueError('Malformed prescribed class')
    placed = {n for n,a in prescribed}
    if len(placed) != len(prescribed) or placed & set(resources):
        raise ValueError('Prescribed and unused moduli must be distinct and disjoint')
    top = set(result['top_u_capacities'])
    if not top <= set(resources):
        raise ValueError('Every top resource must be eligible and unplaced')
    w = [x+y for x,y in zip(u, v)]
    footprints = [sum(w[a::n]) for n,a in prescribed]
    outside = {n: max(sum(w[a::n]) for a in range(n))
               for n in resources if n not in top}
    demand = sum(w)-sum(footprints)
    budget = result.get('G_mix_pair',result['G_mix'])
    capacity = sum(outside.values())+budget
    return {'demand_after_known_footprints': demand,
            'known_footprints_with_multiplicity': footprints,
            'outside_capacities': outside, 'G_mix': result['G_mix'],
            'top_bound_used': budget, 'pair': None if pair is None else list(pair),
            'total_capacity': capacity, 'deficit': demand-capacity,
            'full_period_exclusion_claimed': False}
