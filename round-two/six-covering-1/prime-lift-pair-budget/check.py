"""Author checker of the conditional fixture and a genuine full-cover control."""
import json
from pathlib import Path
from math import lcm
from itertools import combinations
from budget import profile, charge, pair_cover, cost560_gcd1

HERE = Path(__file__).resolve().parent


def require(test, message):
    if not test:
        raise ValueError(message)


def main():
    f = json.loads((HERE / 'fixture.json').read_text())
    N, Q, p, T = f['period'], f['core_period'], f['prime'], f['cofactor']
    require((N, Q, p, T) == (15120, 5040, 3, 560), 'unexpected fixture parameters')
    E = [d for d in range(1, T + 1) if T % d == 0]
    core = f['core']
    labels = [m for a, m in core]
    require(len(set(labels)) == len(labels), 'duplicate core modulus')
    require(set(labels) == {m for m in range(8, Q + 1) if Q % m == 0}, 'core resources not exhausted')
    require(all(0 <= a < m for a, m in core) and lcm(*labels) == Q, 'invalid core')
    R = [x for x in range(Q) if all(x % m != a for a, m in core)]
    profiles = []; point_profiles = []; selected = []; parents = []; fast_checks = 0
    for row in f['groups']:
        r, points = row['parent'], row['points']
        S = [x for x in R if x % 9 == r]
        require(S and points and len(points) == len(set(points)), 'invalid point group')
        require(all(x in S for x in points), 'point outside core residual')
        g = profile(S, E, T); small = profile(points, E, T)
        require(g['singleton'] == small['singleton'], 'singleton profile changed')
        require(small['cost'] == row['cost'], 'local cost mismatch')
        for targets, prof in [(S,g), (points,small)]:
            if prof['gcd'] == 1:
                require(cost560_gcd1(targets) == prof['cost'], 'four-pair reduction mismatch')
                fast_checks += 1
        profiles.append(g); point_profiles.append(small)
        selected.extend(points); parents.append(r)
    require(set(parents) == {x % 9 for x in R}, 'missing active parent')
    q = f['groups'][0]['points']
    require(len(q) == 4 and {x % 4 for x in q} == set(range(4)), 'missing mod4 pattern')
    require(len({x % 5 for x in q}) == len({x % 7 for x in q}) == 4, 'missing odd-prime pattern')
    u = [row['potential'] for row in f['groups']]
    lower, v = charge(point_profiles, p, E, u)
    require(v == {int(d): w for d, w in f['resource_potentials'].items()}, 'credit mismatch')
    used_resources = set(); used_copies = set(); matching_credit = 0
    for r, j, d in f['matching']:
        i = parents.index(r)
        require(0 <= j < p and (r, j) not in used_copies and d not in used_resources, 'bad matching')
        require(d in point_profiles[i]['singleton'], 'incompatible matching edge')
        used_resources.add(d); used_copies.add((r, j))
        matching_credit += point_profiles[i]['cost'] - 1
    require(matching_credit == sum(v.values()), 'matching does not attain resource credit')
    full = [x for x in range(N) if x % Q in R]
    capacities = {27*d: max(sum(x % (27*d) == a for x in full)
                            for a in range(27*d)) for d in E}
    # Explicit compatible lifts, indexed by the actual residue modulo27.
    lifted = []
    for row in f['groups']:
        r = row['parent']
        for s in range(r, 27, 9):
            for x in row['points']:
                copies = [x+j*Q for j in range(p) if (x+j*Q) % 27 == s]
                require(len(copies) == 1, 'invalid compatible lift')
                lifted.extend(copies)
    require(len(set(lifted)) == p*len(selected), 'repeated lifted point')
    point_capacity = sum(max(sum(x % (27*d) == a for x in lifted)
                             for a in range(27*d)) for d in E)
    old_union = set().union(*(set(g['singleton']) for g in profiles))
    require(len(old_union) == len(f['matching']), 'old matching upper bound mismatch')
    old_bound = 2*p*len(profiles) - len(f['matching'])
    require(old_bound <= len(E) and sum(capacities.values()) >= len(full), 'cheap filter no longer passes')
    require(lower > len(E), 'pair-aware bound is not strict')
    control = json.loads((HERE / 'control20160.json').read_text())
    rows = control['classes']; period = control['period']
    require(min(m for a, m in rows) == 8 and lcm(*(m for a, m in rows)) == period, 'bad full-cover control')
    require(len({m for a, m in rows}) == len(rows), 'repeated full-cover modulus')
    require(all(0 <= a < m and period % m == 0 for a, m in rows), 'invalid full-cover class')
    require(all(any(x % m == a for a, m in rows) for x in range(period)), 'control has holes')
    control_core = [(a, m) for a, m in rows if (period//2) % m == 0]
    control_R = [x for x in range(period//2) if all(x % m != a for a, m in control_core)]
    control_E = [d for d in range(1, 316) if 315 % d == 0]
    gs = [profile([x for x in control_R if x % 32 == r], control_E, 315)
          for r in sorted({x % 32 for x in control_R})]
    control_bound, _ = charge(gs, 2, control_E, [0]*len(gs))
    require(control_bound <= len(control_E), 'false exclusion of genuine cover')
    oracle_cases = 0
    for t in range(1,11):
        divisors = [d for d in range(1,t+1) if t % d == 0]
        for mask in range(1,1<<t):
            S = [x for x in range(t) if mask>>x & 1]
            for d,e in combinations(divisors,2):
                phases = pair_cover(S,d,e)
                possible = any(all(x%d == a or x%e == b for x in S)
                               for a in range(d) for b in range(e))
                require((phases is not None) == possible, 'pair oracle existence mismatch')
                if phases is not None:
                    a,b = phases
                    require(all(x%d == a or x%e == b for x in S), 'pair oracle witness mismatch')
                oracle_cases += 1
    three_profile = profile([0,1,2], [1,3,9,27], 27)
    three_bound, _ = charge([three_profile],2,[1,3,9,27],[0])
    require(three_profile['cost'] == 3 and three_bound == 4, 'three-class control profile')
    require(all(any(x%m == a for a,m in [(0,2),(3,6),(1,18),(29,54)])
                for x in [0,1,2,27,28,29]), 'three-class control completion')
    result = {'core_classes': len(core), 'core_residual': len(R), 'active_parents': parents,
              'local_costs': [g['cost'] for g in point_profiles],
              'core_points': len(selected), 'physical_points': len(lifted),
              'old_singleton_bound': old_bound, 'full_uniform_demand': len(full),
              'full_uniform_capacity': sum(capacities.values()),
              'baseline': p*sum(g['cost'] for g in point_profiles),
              'maximum_singleton_credit': matching_credit,
              'new_resource_lower_bound': lower, 'available_resources': len(E),
              'point_uniform_capacity': point_capacity,
              'positive_control_classes': len(rows), 'positive_control_period': period,
              'positive_control_resource_bound': control_bound,
              'pair_oracle_cases': oracle_cases, 'four_pair_reduction_checks': fast_checks,
              'three_class_completion_control': True}
    expected = json.loads((HERE / 'expected.json').read_text())
    require(result == expected['checker'], 'expected checker result mismatch')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
