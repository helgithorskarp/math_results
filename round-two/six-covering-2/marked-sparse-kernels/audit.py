"""Physical-residue audit. No cofactor engine or solver is imported.

Only the CLI and static damaged-data factory are shared with check.py.
Every original tail phase is checked as a literal progression modulo10080.
"""
from fractions import Fraction
import hashlib
import json
from controls import cli


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def unpack(parents):
    need(isinstance(parents, dict) and parents, 'Empty or invalid parents')
    answer = {}
    for key, values in parents.items():
        need(key in tuple(map(str, range(8))), 'Invalid parent label')
        need(isinstance(values, list) and len(values) > 0, 'Empty points')
        need(all(type(x) is int and x in range(315) for x in values), 'Invalid point')
        need(len(values) == len(set(values)) and values == sorted(values), 'Duplicate/order')
        answer[int(key)] = set(values)
    return answer


def actual_kernel(parents):
    return {x for x in range(10080) if x % 315 in parents.get(x % 8, set())}


def actual_row(parents, base, tails, divisors):
    W = actual_kernel(parents)
    need(len(W) == 4 * sum(map(len, parents.values())), 'Wrong physical replication')
    populations, maxima, stream = {}, [], hashlib.sha256()
    for n in tails:
        # Visit all actual phases, including empty intersections and TOP phases.
        counts = [sum(x in W for x in range(a, 10080, n)) for a in range(n)]
        stream.update(json.dumps([n, counts], separators=(',', ':')).encode())
        populations[n] = counts
        maxima.append([n, max(counts)])
    M = {d:max(populations[32*d]) for d in divisors}
    for d in divisors[1:]:
        need(max(populations[16*d]) == 2*M[d], 'CRT capacity formula failed')
    cap = sum(c for _, c in maxima)
    clause = [[n, a] for n in base for a in sorted({x % n for x in W})]
    shortened = [p for p in clause if p[0] != 15]
    hits = sum(x % 15 == 2 for x in W)
    return {
        'parents': sorted(parents), 'parent_sizes': [len(parents[r]) for r in sorted(parents)],
        'cofactor_points': len(W)//4, 'physical_points': len(W), 'capacity':cap,
        'strict_gap':len(W)-cap, 'cofactor_maxima':[[d,M[d]] for d in divisors],
        'tail_maxima':maxima, 'all_phase_populations_sha256':stream.hexdigest(),
        'base_clause_terms':len(clause), 'base_clause_sha256':sha(clause),
        'original15_two_physical_hits':hits,
        'after_original15_two_clause_terms':len(shortened) if hits == 0 else None,
        'after_original15_two_clause_sha256':sha(shortened) if hits == 0 else None,
    }


def evaluate(cert):
    need(all(type(cert.get(k)) is int for k in ('schema','period','minimum')),
         'Integer domain required')
    need((cert['schema'], cert['period'], cert['minimum']) == (1,10080,8), 'Domain changed')
    prefixes = {
        'H': [[8,0],[9,0],[10,1],[14,0],[12,10],[16,1]],
        'P': [[8,0],[9,0],[10,1],[14,1],[12,10],[16,1]]}
    need(cert['prefixes'] == prefixes, 'Prescribed original class changed')
    need(all(type(n) is int and type(a) is int for p in cert['prefixes'].values() for n,a in p),
         'Boolean/noninteger original class')
    divisors = sorted({d for d in range(1,316) if 315//d*d == 315})
    first, last = cert['first_pool'], cert['last_pool']
    need(all(type(d) is int for d in first + last), 'Boolean/noninteger cofactor')
    need(first == divisors[1:] and last == divisors, 'Unequal inventory changed')
    tails = [16*d for d in first] + [32*d for d in last]
    base = sorted({n for n in range(8,2521) if 2520%n == 0} - {8,9,10,12,14})
    need(set(tails).isdisjoint(base) and len(tails) == len(set(tails)) == 23,
         'Original resource collision')
    need(sorted(base+tails+[8,9,10,12,14,16]) ==
         [n for n in range(8,10081) if 10080%n == 0], 'Missing original resource')
    available = set(range(315)) - set(range(0,315,9))
    buckets = [[d,len({x%d for x in available})] for d in first]
    harmonic = sum(Fraction(1,b) for _,b in buckets)
    need(harmonic == 1, 'Harmonic identity failed')
    thresholds = [(2,12),(3,11),(4,10),(5,9),(6,9)]
    rows = []
    for s, threshold in thresholds:
        for k in range(1,threshold):
            m = len(range(0,k,s))
            bound = 3*sum(len(range(0,m,d)) for d in first)+m
            need(bound >= 4*k, 'Universal endpoint failed')
            rows.append([s,k,m,bound,4*k])
    need([x['id'] for x in cert['kernels']] == ['two','three','four','five'],
         'Missing minimum witness')
    output, logical_masks = [], 0
    for item, (s, threshold) in zip(cert['kernels'], thresholds):
        need(item['at_most_parents'] == s, 'Wrong support cap')
        parents = unpack(item['parents'])
        need(len(parents) <= s, 'Too many parent fibres')
        W = actual_kernel(parents)
        for prefix in prefixes.values():
            for n,a in prefix:
                need(W.isdisjoint(range(a,10080,n)), 'Physical prescribed class hit')
        row = actual_row(parents,base,tails,divisors)
        need(row['cofactor_points'] == threshold and row['strict_gap'] > 0,
             'Minimum strict witness failed')
        row.update({'id':item['id'],'at_most_parents':s,'prefixes_avoided':['H','P']})
        output.append(row)
        logical_masks += len(parents)*sum(divisors)
    need(output[0]['parent_sizes'] == [6,6], 'Minimum two-parent profile changed')
    need(output[0]['cofactor_maxima'] ==
         [[d,6 if d==1 else 2 if d in (3,5) else 1] for d in divisors],
         'Complete two-parent minimum shape failed')
    need(cert['without_nine_control'] ==
         {'parent':4,'interval_start':0,'interval_size':180}, 'Wrong missing9 control')
    control = {4:set(range(180))}
    W = actual_kernel(control)
    for n,a in prefixes['P']:
        if n != 9:
            need(W.isdisjoint(range(a,10080,n)), 'Absent9 control hits another original class')
    sensitive = actual_row(control,sorted(base+[9]),tails,divisors)
    need((sensitive['physical_points'],sensitive['capacity'],sensitive['strict_gap']) ==
         (720,717,3), 'Hypothesis control failed')
    return {
        'agent':'six-covering-2','role':'researcher','period':10080,
        'certificate_sha256':sha(cert),'first_pool':first,'last_pool':last,
        'base_moduli':base,'tail_moduli':tails,'one_parent_bucket_counts':buckets,
        'one_parent_reciprocal_sum':[harmonic.numerator,harmonic.denominator],
        'one_parent_obstruction_exists':False,
        'minima_by_at_most_parents':[[s,k] for s,k in thresholds],
        'lower_bound_rows':rows,'kernels':output,'cofactor_phase_rows':logical_masks,
        'all_four_tail_phase_rows':4*sum(tails),
        'all_five_tail_phase_rows_including_hypothesis_control':5*sum(tails),
        'two_parent_minimum_shape':{'sizes':[6,6],'quotas':[[3,2],[5,2]],
                                    'rainbow_labels':[7,9,15]},
        'without_original9_control':sensitive,
        'simultaneous_capacity_attainment_claimed':False,
        'complete_BASE_realization_claimed':False,
        'global_L_min_8_improvement_claimed':False,'independent_reviewer':False,
    }


if __name__ == '__main__':
    cli(evaluate, 'physical')
