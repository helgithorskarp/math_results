"""Literal author audit. Imports no production checker or coset-budget module."""
import json
from itertools import combinations, product
from pathlib import Path
from math import gcd, lcm

HERE = Path(__file__).resolve().parent


def require(test, message):
    if not test:
        raise ValueError(message)


def coset_pair(S, d, e):
    # Enumerate every actual phase; no selected-point two-branch oracle.
    for a in range(d):
        remaining = [x for x in S if x % d != a]
        for b in range(e):
            if all(x % e == b for x in remaining):
                return a, b
    return None


def local(S, E):
    A = [d for d in E if all(x % d == S[0] % d for x in S)]
    outside = [d for d in E if d not in A]
    cost = 3
    for d, e in combinations(outside, 2):
        if coset_pair(S, d, e) is not None:
            cost = 2; break
    return A, cost


def literal_capacity(period, targets, m):
    return max(sum(x in targets for x in range(a, period, m)) for a in range(m))


def run(check_expected=True):
    f = json.loads((HERE / 'fixture.json').read_text())
    N, Q, p, T = f['period'], f['core_period'], f['prime'], f['cofactor']
    core = f['core']; E = [d for d in range(1, T+1) if T % d == 0]
    require(len({m for a, m in core}) == len(core), 'duplicate modulus')
    require({m for a, m in core} == {m for m in range(8, Q+1) if Q % m == 0}, 'free core label')
    covered = bytearray(Q)
    for a, m in core:
        require(0 <= a < m, 'invalid phase')
        for x in range(a, Q, m):
            covered[x] = 1
    R = [x for x in range(Q) if not covered[x]]
    physical = {x for x in range(N) if not covered[x % Q]}
    points = []; A = []; costs = []; parents = []
    for row in f['groups']:
        S = row['points']; r = row['parent']
        require(all(0 <= x < Q and not covered[x] and x % 9 == r for x in S), 'bad target')
        choices, cost = local(S, E)
        require(cost == row['cost'], 'incorrect pair cost')
        A.append(choices); costs.append(cost); points.extend(S); parents.append(r)
    require(set(parents) == {x % 9 for x in R}, 'parent omitted')
    resource_v = {int(d): value for d, value in f['resource_potentials'].items()}
    require(set(resource_v) == set(E) and all(v >= 0 for v in resource_v.values()), 'bad resource potentials')
    for row, choices, cost in zip(f['groups'], A, costs):
        require(row['potential'] >= 0, 'negative parent potential')
        require(all(row['potential'] + resource_v[d] >= cost-1 for d in choices), 'uncovered credit edge')
    credit = p*sum(row['potential'] for row in f['groups']) + sum(resource_v.values())
    bound = p*sum(costs)-credit
    used_d = set(); used_f = set(); matched_credit = 0
    for r, j, d in f['matching']:
        i = parents.index(r)
        require(d in A[i] and 0 <= j < p and d not in used_d and (r,j) not in used_f, 'bad matching')
        used_d.add(d); used_f.add((r,j)); matched_credit += costs[i]-1
    require(matched_credit == credit, 'matching/credit inequality not sharp')
    physical_points = {x+j*Q for x in points for j in range(p)}
    require(len(physical_points) == p*len(points), 'repeated physical point')
    for row in f['groups']:
        for s in range(row['parent'], 27, 9):
            fibre = [x for x in physical_points if x % 27 == s]
            require(len(fibre) == len(row['points']), 'incompatible physical lifts')
    capacities = [literal_capacity(N, physical, 27*d) for d in E]
    point_capacity = sum(literal_capacity(N, physical_points, 27*d) for d in E)
    old_bound = 2*p*len(A)-len(f['matching'])
    require(len(set().union(*map(set,A))) == len(f['matching']), 'old matching upper bound')
    require(old_bound == 20 and sum(capacities) >= len(physical) and bound > len(E), 'fixture comparison changed')
    pair_phase_cases = 0
    S = f['groups'][0]['points']
    for d, e in combinations([d for d in E if d not in A[0]], 2):
        for a in range(d):
            remaining = [x for x in S if x % d != a]
            for b in range(e):
                pair_phase_cases += 1
                require(not all(x % e == b for x in remaining), 'two-class cover found')

    # Small exact controls vary the residual set and every possible selected
    # phase (including omission). Each successful literal completion must
    # satisfy every charge tested below. These are residual completions,
    # not asserted distinct integer covers with minimum eight.
    assignments = 0; successful = 0; residual_sets = 0; charge_checks = 0; assignment_residual_tests = 0
    for prime, exponent, t, max_size in [(2,1,3,3), (2,1,5,3), (3,1,2,3), (2,1,9,2)]:
        q = prime**exponent*t; n = prime*q
        resources = [d for d in range(1,t+1) if t % d == 0]
        residues = [list(c) for size in range(1, min(q,max_size)+1)
                    for c in combinations(range(q),size)]
        cases = []
        for residual in residues:
            groups = [local([x for x in residual if x % prime**exponent == r], resources)
                      for r in sorted({x % prime**exponent for x in residual})]
            bounds = []
            for u in product(*(range(cost) for a,cost in groups)):
                v = {d:max([0]+[cost-1-potential
                                for (a,cost),potential in zip(groups,u) if d in a])
                     for d in resources}
                bounds.append(prime*sum(cost for a,cost in groups)-prime*sum(u)-sum(v.values()))
            cases.append((set(x+j*q for x in residual for j in range(prime)), bounds))
        residual_sets += len(cases)
        for phases in product(*(range(-1,prime**(exponent+1)*d) for d in resources)):
            assignments += 1
            hits = set(); selected_count = 0
            for d,a in zip(resources,phases):
                if a >= 0:
                    selected_count += 1
                    hits.update(range(a,n,prime**(exponent+1)*d))
            for targets,bounds in cases:
                assignment_residual_tests += 1
                if targets <= hits:
                    successful += 1; charge_checks += len(bounds)
                    require(all(bound <= selected_count for bound in bounds), 'false exclusion of small completion')

    # A successful completion using one singleton and THREE classes on the
    # other fibre: this exercises the new cost3 term at equality.
    three_A, three_cost = local([0,1,2], [1,3,9,27])
    require(three_A == [1] and three_cost == 3, 'three-class control profile')
    three_bound = 2*three_cost - (three_cost-1)
    three_hits = set()
    for a,m in [(0,2),(3,6),(1,18),(29,54)]:
        three_hits.update(range(a,54,m))
    require({0,1,2,27,28,29} <= three_hits and three_bound == 4, 'three-class control completion')

    c = json.loads((HERE / 'control20160.json').read_text())
    rows, period = c['classes'], c['period']
    require(min(m for a,m in rows) == 8 and lcm(*(m for a,m in rows)) == period, 'invalid full-cover control')
    require(len({m for a,m in rows}) == len(rows), 'repeated control modulus')
    hit = bytearray(period)
    for a,m in rows:
        require(period % m == 0 and 0 <= a < m, 'bad control phase')
        for x in range(a,period,m):hit[x] = 1
    require(all(hit), 'full-cover control has a hole')
    q = period//2; core_hit = bytearray(q)
    for a,m in rows:
        if q % m == 0:
            for x in range(a,q,m):core_hit[x] = 1
    control_R = [x for x in range(q) if not core_hit[x]]
    control_E = [d for d in range(1,316) if 315 % d == 0]
    groups = [local([x for x in control_R if x % 32 == r],control_E)
              for r in sorted({x % 32 for x in control_R})]
    v = {d:max([0]+[cost-1 for a,cost in groups if d in a]) for d in control_E}
    control_bound = 2*sum(cost for a,cost in groups)-sum(v.values())
    require(control_bound <= len(control_E), 'false exclusion of known cover')
    checker = {'core_classes':len(core),'core_residual':len(R),'active_parents':parents,
               'local_costs':costs,'core_points':len(points),'physical_points':len(physical_points),
               'old_singleton_bound':old_bound,'full_uniform_demand':len(physical),
               'full_uniform_capacity':sum(capacities),'baseline':p*sum(costs),
               'maximum_singleton_credit':matched_credit,'new_resource_lower_bound':bound,
               'available_resources':len(E),'point_uniform_capacity':point_capacity,
               'positive_control_classes':len(rows),'positive_control_period':period,
               'positive_control_resource_bound':control_bound,
               'pair_oracle_cases':sum((2**t-1)*len(list(combinations(
                   [d for d in range(1,t+1) if t%d==0],2))) for t in range(1,11)),
               'four_pair_reduction_checks':4,
               'three_class_completion_control':True}
    audit = {'pair_phase_cases':pair_phase_cases,'small_assignments':assignments,
             'small_residual_sets':residual_sets,'successful_residual_completions':successful,
             'small_charge_checks':charge_checks,'fixture_verified':True,
             'assignment_residual_tests':assignment_residual_tests,
             'genuine_full_cover_verified':True}
    result = {'checker':checker,'audit':audit}
    if check_expected:
        require(result == json.loads((HERE/'expected.json').read_text()), 'expected audit output mismatch')
        print(json.dumps(audit,sort_keys=True))
    return result


if __name__ == '__main__':
    run()
