"""Literal actual-phase checks of a polynomial mixed upper relaxation."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
from time import monotonic

from budget import completion_bound, mixed_budget, parameters


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def literal_top(B, C, b, u, v):
    N, T, ds = parameters(B, C, b)
    top = [B*d for d in ds]
    u_pops, v_pops, w_pops, points = {}, {}, {}, {}
    block_weights = {}
    for x in range(N):
        key = (x % B % T, x % C)
        if key in block_weights:
            require(block_weights[key] == v[x], 'Periodic weight varies in primitive block')
        block_weights[key] = v[x]
    for n in top:
        points[n] = [tuple(range(a, N, n)) for a in range(n)]
        u_pops[n] = [sum(u[x] for x in row) for row in points[n]]
        v_pops[n] = [sum(v[x] for x in row) for row in points[n]]
        w_pops[n] = [sum(u[x]+v[x] for x in row) for row in points[n]]
    best = -1
    witness = None
    phase_count = 0
    for phases in product(*(range(n) for n in top)):
        frequency = Counter((x % B % T, x % C)
                            for n,a in zip(top, phases) for x in points[n][a])
        charge = sum(u_pops[n][a] for n,a in zip(top, phases))
        charge += sum(k*block_weights[key] for key,k in frequency.items() if k >= 2)
        if charge > best:
            best, witness = charge, phases
        phase_count += 1
    G = max(sum(max(max(v_pops[n]), 2*max(v_pops[n][t::b]))
                for n in top if n != B) for t in range(b))
    return {'J': best, 'witness': list(witness), 'phase_tuples': phase_count,
            'top_u_sum': sum(max(row) for row in u_pops.values()),
            'ordinary_top': sum(max(row) for row in w_pops.values()), 'G': G}


def large_cofactor_reproduction():
    path = Path(__file__).with_name('input.json')
    require(sha256(path.read_bytes()).hexdigest() ==
            'bf4d3deb56fa173a875a816aef6831a6aebff54b8bfdb441898137a5b96e1b96',
            'Attributed7516 input bytes changed')
    data = json.loads(path.read_text())
    B,C,b,N = (data[k] for k in ('B','C','b','N'))
    v = []
    for x in range(N):
        hits = [box[-1] for box in data['boxes']
                if all(mask >> (x % axis) & 1 for mask,axis in zip(box[:-1],data['axes']))]
        require(len(hits) <= 1, 'Copied box support overlaps')
        v.append(hits[0] if hits else 0)
    anchors = data['anchors']
    require(all(not v[x] or all(x%n != a for n,a in anchors) for x in range(N)),
            'Copied full-period prescribed support failed')
    resources = [n for n in range(8,N+1) if N%n == 0 and n not in dict(anchors)]
    formula = mixed_budget(B,C,b,[0]*N,v,(3,5))
    affine = completion_bound(B,C,b,[0]*N,v,resources,anchors,(3,5))
    literal_top_caps = {n:max(sum(v[a::n]) for a in range(n))
                        for n in formula['ordinary_top_capacities']}
    require(formula['ordinary_top_capacities'] == literal_top_caps,
            'Large-cofactor CRT footprints differ from physical classes')
    require(formula['G_mix'] == 23150 and formula['G_mix_pair'] == 22295 and
            affine['demand_after_known_footprints'] == 597000 and
            sum(affine['outside_capacities'].values()) == 573780 and
            affine['total_capacity'] == 596075 and affine['deficit'] == 925,
            'Reviewer-derived pair925 reproduction differs')
    return {'N':N,'top_resources':len(literal_top_caps),'unused_resources':len(resources),
            'original_G':23150,'pair_G':22295,'total_capacity':596075,'gap':925,
            'input_sha256':sha256(path.read_bytes()).hexdigest(),
            'status':'Attributed reproduction of six-reviewer-5 result; not a new exclusion'}


def run():
    rows, phase_count = [], 0
    cases = ((4,3,2,4), (8,3,2,6), (9,4,3,4), (6,5,1,4), (4,9,2,2))
    for B,C,b,seeds in cases:
        N = B*C
        for seed in range(seeds):
            u = [((x*x+7*x+seed*5) % 11) % 4 for x in range(N)]
            base = [((x*7+seed*3) % 9) % 4 for x in range(b*C)]
            v = base*(N//(b*C))
            result = mixed_budget(B,C,b,u,v)
            actual = literal_top(B,C,b,u,v)
            require(actual['J'] <= result['G_mix'] <= result['separate_top_bound'],
                    'Actual-phase charge or separate upper comparison failed')
            require(result['ordinary_top_total'] == actual['ordinary_top'] and
                    result['periodic_G'] == actual['G'] and
                    sum(result['top_u_capacities'].values()) == actual['top_u_sum'],
                    'Physical ordinary or pure capacities differ')
            require(mixed_budget(B,C,b,u,[0]*N)['G_mix'] == actual['top_u_sum'],
                    'v=0 endpoint failed')
            require(mixed_budget(B,C,b,[0]*N,v)['G_mix'] == actual['G'],
                    'u=0 endpoint failed')
            phase_count += actual['phase_tuples']
            rows.append({'B':B,'C':C,'b':b,'seed':seed,'J':actual['J'],
                         'G_mix':result['G_mix'],'separate':result['separate_top_bound'],
                         'ordinary':actual['ordinary_top'],
                         'phase_tuples':actual['phase_tuples']})
    B,C,b,N = 8,3,2,24
    u = [int(x in (0,16)) for x in range(N)]
    v = [x % 2 for x in range(N)]
    result = mixed_budget(B,C,b,u,v)
    actual = literal_top(B,C,b,u,v)
    strict = {k:result[k] for k in ('G_mix','ordinary_top_total','separate_top_bound')}
    strict['J'] = actual['J']
    strict['phase_tuples'] = actual['phase_tuples']
    require(strict == {'G_mix':3,'ordinary_top_total':4,'separate_top_bound':5,
                       'J':3,'phase_tuples':192}, 'Strict joint fixture changed')
    phase_count += actual['phase_tuples']
    W = ((2,0,0),(0,3,0),(2,0,0),(0,0,0))
    pure_v = [W[x % 4][x % 3] for x in range(36)]
    upper = mixed_budget(9,4,3,[0]*36,pure_v)
    lower = literal_top(9,4,3,[0]*36,pure_v)
    require((lower['J'],upper['G_mix']) == (10,12), 'Known nonattainment fixture changed')
    phase_count += lower['phase_tuples']
    pair_rows = []
    for seed in range(3):
        u = [((x*x+3*x+seed*7) % 13) % 4 for x in range(60)]
        v = [(x*7+seed*3) % 5 for x in range(30)]*2
        result = mixed_budget(4,15,2,u,v,(3,5))
        actual = literal_top(4,15,2,u,v)
        require(actual['J'] <= result['G_mix_pair'] <= result['G_mix'],
                'Pair-corrected mixed budget invalid')
        require(mixed_budget(4,15,2,u,[0]*60,(3,5))['G_mix_pair'] == actual['top_u_sum'],
                'Pair correction changed pure-u endpoint')
        phase_count += actual['phase_tuples']
        pair_rows.append([seed,actual['J'],result['G_mix_pair'],result['G_mix']])
    u = [int(x == 0) for x in range(60)]
    v = [x % 2 for x in range(60)]
    paired = mixed_budget(4,15,2,u,v,(3,5))
    paired_actual = literal_top(4,15,2,u,v)
    paired_component = {'J':paired_actual['J'],'G_mix_pair':paired['G_mix_pair'],
                        'G_mix':paired['G_mix'],'separate':paired['separate_top_bound'],
                        'ordinary':paired['ordinary_top_total']}
    require(paired_component == {'J':17,'G_mix_pair':17,'G_mix':18,
                                 'separate':22,'ordinary':24}, 'Mixed pair fixture changed')
    phase_count += paired_actual['phase_tuples']
    # Noncoprime designated divisors: empty intersections contribute zero.
    result = mixed_budget(4,9,2,[x % 3 for x in range(36)],
                          [x % 5 for x in range(18)]*2,(3,9))
    actual = literal_top(4,9,2,[x % 3 for x in range(36)],
                         [x % 5 for x in range(18)]*2)
    require(actual['J'] <= result['G_mix_pair'] <= result['G_mix'],
            'Noncoprime pair correction invalid')
    phase_count += actual['phase_tuples']
    cover = ((2,0),(3,0),(4,1),(6,1),(12,11))
    require(all(any(x%n == a for n,a in cover) for x in range(12)), 'Positive fixture not cover')
    subsets = ((), ((2,0),), ((3,0),), ((2,0),(3,0)),
               ((2,0),(6,1)), ((2,0),(3,0),(6,1)))
    positive_rows = []
    for seed in range(30):
        u = [(x*11+x*x+seed*3) % 5 for x in range(12)]
        v = [1+(x*7+seed) % 4 for x in range(6)]*2
        for prescribed in subsets:
            placed = {n for n,a in prescribed}
            resources = [n for n,a in cover if n not in placed]
            result = completion_bound(4,3,2,u,v,resources,prescribed)
            require(result['deficit'] <= 0, 'False exclusion of genuine covering')
            literal_known = [sum(u[x]+v[x] for x in range(a,12,n)) for n,a in prescribed]
            require(result['known_footprints_with_multiplicity'] == literal_known,
                    'Known footprint multiplicity changed')
            positive_rows.append([seed,list(map(list,prescribed)),result])
    for seed in range(15):
        u = [(x*x+seed*3) % 5 for x in range(12)]
        v = [1+(x*7+seed) % 4 for x in range(4)]*3
        for prescribed in ((), ((2,0),), ((4,1),), ((2,0),(4,1))):
            placed = {n for n,a in prescribed}
            resources = [n for n,a in cover if n not in placed]
            result = completion_bound(3,4,1,u,v,resources,prescribed,(2,4))
            require(result['deficit'] <= 0, 'Pair bound falsely excludes genuine cover')
            positive_rows.append(['pair',seed,list(map(list,prescribed)),result])
    bad = (
        lambda:mixed_budget(4,2,2,[0]*8,[0]*8),
        lambda:mixed_budget(4,3,3,[0]*12,[0]*12),
        lambda:mixed_budget(True,3,1,[0]*3,[0]*3),
        lambda:mixed_budget(4,3,2,[0]*11,[0]*12),
        lambda:mixed_budget(4,3,2,[-1]+[0]*11,[0]*12),
        lambda:mixed_budget(4,3,2,[True]+[0]*11,[0]*12),
        lambda:mixed_budget(4,3,2,[0]*12,[1]+[0]*11),
        lambda:completion_bound(4,3,2,[0]*12,[0]*12,[4,4,12],()),
        lambda:completion_bound(4,3,2,[0]*12,[0]*12,[4,6],()),
        lambda:completion_bound(4,3,2,[0]*12,[0]*12,[4,12],[(4,1)]),
        lambda:completion_bound(4,3,2,[0]*12,[0]*12,[4,12],[(2,2)]),
        lambda:completion_bound(4,3,2,[0]*12,[0]*12,[4,12],[(2,0),(2,1)]),
        lambda:mixed_budget(4,9,2,[0]*36,[0]*36,(3,3)),
        lambda:mixed_budget(4,9,2,[0]*36,[0]*36,(3,5)),
        lambda:mixed_budget(4,9,2,[0]*36,[0]*36,(1,3)),
    )
    for operation in bad:
        try:
            operation()
        except ValueError:
            continue
        raise ValueError('Malformed hypotheses accepted')
    zero = mixed_budget(4,3,2,[0]*12,[0]*12)
    require(zero['G_mix'] == zero['separate_top_bound'] == 0, 'Zero boundary failed')
    large = large_cofactor_reproduction()
    return {'actual_author':'six-covering-3','role':'researcher','all_passed':True,
            'weight_pairs':len(rows)+7,'complete_actual_phase_tuples':phase_count,
            'phase_rows_sha256':digest(rows), 'strict_component':strict,
            'nonattainment_component':{'J':10,'G_mix':12},
            'pair_rows_sha256':digest(pair_rows), 'mixed_pair_component':paired_component,
            'noncoprime_pair_control':True,
            'genuine_cover_affine_controls':len(positive_rows),
            'positive_controls_sha256':digest(positive_rows),
            'malformed_inputs_rejected':len(bad), 'zero_component_boundary':True,
            'large_cofactor_reproduction':large,
            'independent_review_claimed':False,'numerical_bound_improved':False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write-expected', action='store_true')
    args = parser.parse_args()
    start = monotonic()
    output = run()
    expected_path = Path(__file__).with_name('expected.json')
    if args.write_expected:
        expected_path.write_text(json.dumps(output,indent=2)+'\n')
    else:
        require(output == json.loads(expected_path.read_text()), 'Compact expected output differs')
    print(json.dumps(output | {'elapsed_seconds':monotonic()-start},indent=2))
