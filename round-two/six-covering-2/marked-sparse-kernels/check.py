"""Cofactor proof arithmetic; no solver, physical producer or peer fixture."""
from fractions import Fraction
from hashlib import sha256
import json
from controls import cli

N = 10080
D = [d for d in range(1, 316) if 315 % d == 0]
E = D[1:]
KNOWN = {'H': [[8,0],[9,0],[10,1],[14,0],[12,10],[16,1]],
         'P': [[8,0],[9,0],[10,1],[14,1],[12,10],[16,1]]}
MINIMUM = {2:12, 3:11, 4:10, 5:9, 6:9}


def require(ok, text):
    if not ok:
        raise ValueError(text)


def digest(obj):
    return sha256(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def ceildiv(a, b):
    return (a + b - 1) // b


def decoded(data):
    require(isinstance(data, dict) and data, 'Nonempty parent dictionary required')
    answer = {}
    for key, points in data.items():
        require(key in [str(r) for r in range(8)], 'Noncanonical parent')
        r = int(key)
        require(isinstance(points, list) and points, 'Nonempty point list required')
        require(all(type(y) is int and 0 <= y < 315 for y in points), 'Noncanonical cofactor')
        require(points == sorted(set(points)), 'Unsorted or repeated cofactor')
        answer[r] = points
    return answer


def admissible(sets, a14, nine=True):
    for r, points in sets.items():
        require(r not in (0, 1), 'Placed original8/16 hit')
        for y in points:
            require(not nine or y % 9 != 0, 'Placed original9 hit')
            require(not (r % 2 == 1 and y % 5 == 1), 'Placed original10 hit')
            require(not (r % 2 == a14 % 2 and y % 7 == a14 % 7), 'Placed original14 hit')
            require(not (r % 4 == 2 and y % 3 == 1), 'Placed original12 hit')


def analyze(sets, base):
    buckets = {}
    for d in D:
        buckets[d] = {}
        for r, points in sets.items():
            row = [0] * d
            for y in points:
                row[y % d] += 1
            buckets[d][r] = row
    maxima = {d:max(max(row) for row in buckets[d].values()) for d in D}
    phase_stream = sha256()
    phases = []
    for factor, pool in ((16, E), (32, D)):
        for d in pool:
            m = factor * d
            zero = [0] * d
            pop = [(2 if factor == 16 else 1) *
                   buckets[d].get(a % 8, zero)[a % d] for a in range(m)]
            phase_stream.update(json.dumps([m, pop], separators=(',', ':')).encode())
            phases.append([m, max(pop)])
    points = sum(map(len, sets.values()))
    cap = 3 * sum(maxima[d] for d in E) + maxima[1]
    require(cap == sum(c for _, c in phases), 'Wrong original-pool capacity')
    representatives = [
        (y + 315 * (((r - y) * pow(315, -1, 8)) % 8)) % 2520
        for r, values in sets.items() for y in values]
    clause = [[m, a] for m in base for a in sorted({x % m for x in representatives})]
    after = [pair for pair in clause if pair[0] != 15]
    hits15 = 4 * sum(y % 15 == 2 for values in sets.values() for y in values)
    return {
        'parents': sorted(sets), 'parent_sizes': [len(sets[r]) for r in sorted(sets)],
        'cofactor_points': points, 'physical_points': 4 * points, 'capacity': cap,
        'strict_gap': 4 * points - cap,
        'cofactor_maxima': [[d, maxima[d]] for d in D], 'tail_maxima': phases,
        'all_phase_populations_sha256': phase_stream.hexdigest(),
        'base_clause_terms': len(clause), 'base_clause_sha256': digest(clause),
        'original15_two_physical_hits': hits15,
        'after_original15_two_clause_terms': len(after) if not hits15 else None,
        'after_original15_two_clause_sha256': digest(after) if not hits15 else None,
    }


def evaluate(cert):
    require(all(type(cert.get(k)) is int for k in ('schema','period','minimum')),
            'Integer schema and domain fields required')
    require(cert.get('schema') == 1 and cert.get('period') == N and cert.get('minimum') == 8,
            'Wrong exact domain')
    require(cert.get('prefixes') == KNOWN, 'Wrong ORIGINAL prefix')
    require(all(type(m) is int and type(a) is int
                for prefix in cert['prefixes'].values() for m,a in prefix),
            'Integer ORIGINAL classes required')
    require(all(type(d) is int for d in cert['first_pool'] + cert['last_pool']),
            'Integer cofactor labels required')
    require(cert.get('first_pool') == E and cert.get('last_pool') == D,
            'Spent16 and free32 inventories changed')
    tail = [16*d for d in E] + [32*d for d in D]
    base = [m for m in range(8, 2521) if 2520 % m == 0 and m not in (8,9,10,12,14)]
    require(sorted(tail + base + [8,9,10,12,14,16]) ==
            [m for m in range(8, N+1) if N % m == 0], 'Original-resource partition differs')
    buckets = [[d, len({y % d for y in range(315) if y % 9 != 0})] for d in E]
    require(all(b == (8*d//9 if d % 9 == 0 else d) for d, b in buckets),
            'Original9 bucket restriction differs')
    harmonic = sum(Fraction(1, b) for _, b in buckets)
    require(harmonic == 1, 'One-parent reciprocal identity differs')
    rows = []
    for s, threshold in MINIMUM.items():
        for k in range(1, threshold):
            m = ceildiv(k, s)
            bound = 3 * sum(ceildiv(m, d) for d in E) + m
            require(bound >= 4*k, 'A lower-bound endpoint fails')
            rows.append([s, k, m, bound, 4*k])
    require([k['id'] for k in cert['kernels']] == ['two','three','four','five'],
            'Four named upper witnesses required')
    output, masks = [], 0
    for item, s in zip(cert['kernels'], (2,3,4,5)):
        require(item['at_most_parents'] == s, 'Wrong support bound')
        sets = decoded(item['parents'])
        require(len(sets) <= s, 'Too many parents')
        admissible(sets, 0)
        admissible(sets, 1)
        row = analyze(sets, base)
        require(row['cofactor_points'] == MINIMUM[s] and row['strict_gap'] > 0,
                'Upper witness is not a minimum-size strict obstruction')
        row.update({'id': item['id'], 'at_most_parents': s, 'prefixes_avoided': ['H','P']})
        output.append(row)
        masks += len(sets) * sum(D)
    # Complete minimum-two shape: M=6 is forced; an extra cofactor
    # population raises capacity from45 to48, losing strictness.
    two = decoded(cert['kernels'][0]['parents'])
    require(all(len(S) == 6 for S in two.values()), 'Two-parent profile differs')
    for S in two.values():
        require(all(sum(y % d == a for y in S) <= 2 for d in (3,5) for a in range(d)),
                'Ternary or prime5 quota differs')
        require(all(len({y % d for y in S}) == 6 for d in (7,9,15)),
                'Rainbow7/9/15 condition differs')
    require(cert['without_nine_control'] == {'parent':4,'interval_start':0,'interval_size':180},
            'Wrong absent9 hypothesis control')
    control = {4:list(range(180))}
    admissible(control, 1, nine=False)
    sensitive = analyze(control, sorted(base + [9]))
    require((sensitive['physical_points'], sensitive['capacity'], sensitive['strict_gap'])
            == (720,717,3), 'Absent9 control differs')
    return {
        'agent':'six-covering-2', 'role':'researcher', 'period':N,
        'certificate_sha256':digest(cert), 'first_pool':E, 'last_pool':D,
        'base_moduli':base, 'tail_moduli':tail, 'one_parent_bucket_counts':buckets,
        'one_parent_reciprocal_sum':[harmonic.numerator, harmonic.denominator],
        'one_parent_obstruction_exists':False,
        'minima_by_at_most_parents':[[s,k] for s,k in MINIMUM.items()],
        'lower_bound_rows':rows, 'kernels':output,
        'cofactor_phase_rows':masks,
        'all_four_tail_phase_rows':4*sum(tail),
        'all_five_tail_phase_rows_including_hypothesis_control':5*sum(tail),
        'two_parent_minimum_shape':{'sizes':[6,6], 'quotas':[[3,2],[5,2]],
                                    'rainbow_labels':[7,9,15]},
        'without_original9_control':sensitive,
        'simultaneous_capacity_attainment_claimed':False,
        'complete_BASE_realization_claimed':False,
        'global_L_min_8_improvement_claimed':False,
        'independent_reviewer':False,
    }


if __name__ == '__main__':
    cli(evaluate, 'cofactor')
