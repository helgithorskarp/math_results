"""Valid cluster upper relaxation for a prescribed binary top class.

This does not claim to exactly optimize the distinct-point budget.
Only the selected cofactor cluster has its union charged jointly.
"""
from itertools import product
from math import prod
from distinct_top_points import prepare, divisors


def cluster_bound(state, cluster=(3, 5, 7), phase_cap=100_000):
    B, C, N, T = state['B'], state['C'], state['N'], state['T']
    A, S, u, v = state['known'], state['S'], state['u'], state['v']
    if state['rho'] != 2 or set(A) & set(S) != {B}:
        raise ValueError('Exactly the binary coarsest top resource is prescribed')
    D = [d for d in divisors(C) if d > 1]
    if len(set(cluster)) != len(cluster) or any(d not in D for d in cluster):
        raise ValueError('Distinct eligible cofactor cluster')
    if prod(d + 1 for d in cluster) > phase_cap:
        raise ValueError('Complete cluster phase cap')
    alpha0 = A[B]
    alpha1 = (alpha0 + T) % B
    q0 = alpha0 % T
    inverse = pow(B, -1, C)
    U = []
    V = []
    for alpha in range(B):
        points = [alpha + B * (((z - alpha) * inverse) % C) for z in range(C)]
        U.append([u[x] for x in points])
        V.append([v[x % state['Q']] for x in points])
    outside, inside, inside_u = {}, {}, {}
    for d in D:
        outside[d] = max((sum(U[alpha][r::d]) + sum(V[alpha][r::d])
                          for alpha in range(B) if alpha % T != q0 for r in range(d)), default=0)
        inside_u[d] = [sum(U[alpha1][r::d]) for r in range(d)]
        inside[d] = max(inside_u[d][r] + 2 * sum(V[alpha1][r::d]) for r in range(d))
    cluster_cases = []
    for mask in range(1 << len(cluster)):
        selected = [d for i, d in enumerate(cluster) if mask >> i & 1]
        best = -1
        best_phases = None
        for phases in product(*(range(d) for d in selected)):
            value = sum(inside_u[d][r] for d, r in zip(selected, phases))
            value += 2 * sum(V[alpha1][z] for z in range(C)
                             if any(z % d == r for d, r in zip(selected, phases)))
            if value > best:
                best, best_phases = value, phases
        outside_value = sum(outside[d] for i, d in enumerate(cluster) if not mask >> i & 1)
        cluster_cases.append({'inside_mask': mask, 'inside_cofactors': selected,
                              'inside_phases': best_phases, 'inside_charge': best,
                              'outside_charge': outside_value, 'total': best + outside_value})
    selected_budget = max(r['total'] for r in cluster_cases)
    others = sum(max(outside[d], inside[d]) for d in D if d not in cluster)
    return {'top_upper_budget': selected_budget + others, 'cluster_budget': selected_budget,
            'other_top_budget': others, 'outside_top_maxima': outside, 'inside_top_maxima': inside,
            'cluster_cases': cluster_cases, 'q0': q0, 'known_alpha': alpha0,
            'opposite_alpha': alpha1, 'cluster': list(cluster)}


def evidence(state, cluster=(3, 5, 7)):
    bound = cluster_bound(state, cluster)
    N, Q, A, S = state['N'], state['Q'], state['known'], state['S']
    total = [state['u'][x] + state['v'][x % Q] for x in range(N)]
    known = {n: sum(state['v'][x % Q] for x in range(a, N, n))
             for n, a in A.items() if n not in S}
    R = [n for n in divisors(N) if n >= state['minimum'] and n not in A]
    capacities = {n: max(sum(total[a::n]) for a in range(n)) for n in R if n not in S}
    demand = sum(total) - sum(known.values())
    capacity = sum(capacities.values()) + bound['top_upper_budget']
    residual = [w if not any(x % n == a for n, a in A.items()) else 0 for x, w in enumerate(total)]
    residual_capacity = sum(max(sum(residual[a::n]) for a in range(n)) for n in R)
    return {'demand': demand, 'capacity': capacity, 'gap': demand - capacity,
            'top_bound': bound, 'outside_capacities': capacities,
            'known_outside_periodic_footprints': known,
            'ordinary_residual_demand': sum(residual), 'ordinary_residual_capacity': residual_capacity,
            'structural_cut_essential': demand > capacity and sum(residual) <= residual_capacity}
