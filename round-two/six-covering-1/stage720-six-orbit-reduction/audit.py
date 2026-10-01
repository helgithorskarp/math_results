"""Separate same-author physical-set replay; imports no production code."""
from functools import lru_cache
import json
from math import gcd
from pathlib import Path


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def undominated(options):
    options = set(options)
    return sorted(p for p in options if not any(
        q != p and q[0] >= p[0] and q[1] >= p[1] for q in options))


def main():
    c = json.loads(Path(__file__).with_name('certificate.json').read_text())
    labels = [m for m in range(8, 721) if 720 % m == 0]
    free = [m for m in labels if m not in (8, 9)]
    fixed = {x for x in range(720) if x % 8 == 5 or x % 9 == 6}
    require(labels == c['original_labels'] and len(labels) == 24, 'original label census')
    anchor_checks = 0
    for m, n in c['forced_anchor_pairs']:
        for a in range(m):
            for b in range(n):
                actual = sum(x % n == b for x in range(a, 720, m))
                require(actual == 720 // (m * n), 'literal forced intersection')
                anchor_checks += 1
    raw = sum(len(range(a, 720, m)) for m in labels for a in [0])
    loss = sum(720 // (m * n) for m, n in c['forced_anchor_pairs'])
    require(720 - raw + loss == 102, 'first-stage hole lower bound')

    def target(a, b):
        allowed = {x for x in range(720) if x % 18 == a or x % 6 == b}
        R = set(range(720)) - fixed - allowed
        O, E = {x for x in R if x % 2}, {x for x in R if not x % 2}
        phases = {m: [(O.intersection(range(a, 720, m)), E.intersection(range(a, 720, m)))
                       for a in range(m)] for m in free}
        return allowed - fixed, O, E, phases

    envelope_results = {}
    for claim in c['envelope_cases']:
        rep = tuple(claim['representative'])
        _, O, E, phases = target(*rep)
        single = {m: undominated((len(o), len(e)) for o, e in phases[m]) for m in free}
        low, high = free[:14], free[14:]
        pair_profiles = {}
        for i, m in enumerate(low):
            for n in low[i + 1:]:
                pair_profiles[m, n] = undominated((len(o | oo), len(e | ee))
                                                  for o, e in phases[m] for oo, ee in phases[n])
        high_states = {(0, 0)}
        for m in high:
            high_states = set(undominated((o + a, e + b) for o, e in high_states
                                         for a, b in single[m]))

        @lru_cache(None)
        def capacity(pool, need):
            if not pool:
                return max((e for o, e in high_states if o >= need), default=None)
            m, tail = pool[0], pool[1:]
            answers = []
            for n in tail:
                child_pool = tuple(k for k in tail if k != n)
                candidates = []
                for o, e in pair_profiles[m, n]:
                    child = capacity(child_pool, max(0, need - o))
                    if child is not None:
                        candidates.append(e + child)
                if not candidates:
                    return None
                answers.append(max(candidates))
            return min(answers)

        upper = capacity(tuple(low), len(O))
        require((len(O), len(E), upper) ==
                (claim['odd_demand'], claim['even_demand'], claim['even_upper']),
                'separate set/count recurrence disagrees')
        require(upper is None or upper < len(E), 'envelope is not strict')
        envelope_results[rep] = upper

    seen = set()
    scalar_combinations = 0
    for row in c['excluded_shapes']:
        shape = row['a18'], row['c6']
        require(shape not in seen, 'duplicate excluded target')
        seen.add(shape)
        if row['reason'] == 'count_envelope':
            rep, (u, t) = tuple(row['representative']), row['affine_map']
            require(rep in envelope_results and gcd(u, 720) == 1 and
                    (5 * u + t) % 8 == 5 and (6 * u + t) % 9 == 6 and
                    ((u * rep[0] + t) % 18, (u * rep[1] + t) % 6) == shape,
                    'affine envelope transfer fails')
            # Literal point images additionally check target and fixed sets.
            source_allowed = {x for x in range(720) if x % 18 == rep[0] or x % 6 == rep[1]}
            dest_allowed = {x for x in range(720) if x % 18 == shape[0] or x % 6 == shape[1]}
            require({(u * x + t) % 720 for x in source_allowed} == dest_allowed and
                    {(u * x + t) % 720 for x in fixed} == fixed, 'literal affine target/fixed image')
            continue
        allowed, O, E, phases = target(*shape)
        if row['reason'] == 'hole_count':
            require(len(allowed) == row['allowed_holes'] < 102, 'physical allowed-hole count')
            continue
        groups = c['resource_partitions'][row['partition_id']]
        require(sorted(m for group in groups for m in group) == free, 'original resource incidence')
        u, v = row['weights']
        total = 0
        for group in groups:
            if len(group) == 1:
                tuples = phases[group[0]]
            else:
                tuples = [(o | oo, e | ee) for o, e in phases[group[0]] for oo, ee in phases[group[1]]]
            scalar_combinations += len(tuples)
            total += max(u * len(o) + v * len(e) for o, e in tuples)
        demand = u * len(O) + v * len(E)
        require((demand, total) == (row['demand'], row['capacity']) and total < demand,
                'physical scalar partition comparison')
    remaining = {tuple(s) for s in c['remaining_shapes']}
    require(len(seen) == 96 and len(remaining) == 12 and not seen.intersection(remaining)
            and seen | remaining == {(a, b) for a in range(18) for b in range(6)},
            'physical complete108-case partition')
    print(json.dumps({'agent': 'six-covering-1', 'role': 'researcher', 'status': 'AUDITED',
                      'same_author': True, 'production_imported': False,
                      'literal_anchor_phase_pairs': anchor_checks,
                      'scalar_original_phase_combinations': scalar_combinations,
                      'strict_envelopes': [{'representative': list(k), 'upper': v}
                                           for k, v in envelope_results.items()],
                      'excluded_shapes': 96, 'remaining_shapes': 12,
                      'global_numerical_bound_changed': False}, sort_keys=True))


if __name__ == '__main__':
    main()
