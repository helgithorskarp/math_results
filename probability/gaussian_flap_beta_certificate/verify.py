"""Separate author controls; no import of certificate.py or its bounds module."""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, product
from math import comb, factorial, isqrt
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
SCALE = 10**48
V = ((0,0,1), (2,0,-1), (-1,3,-1), (-1,-1,-1))
EDGES = tuple(combinations(range(4), 2))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rounded(lo, hi):
    return F((lo*SCALE).__floor__(), SCALE), F((hi*SCALE).__ceil__(), SCALE)


@lru_cache(None)
def exponential(x):
    """Enclose exp(-x) with an alternating series, then squaring; x>=0."""
    require(x >= 0, 'negative exponential argument')
    z, squares = F(x), 0
    while z > F(1, 2):
        z /= 2
        squares += 1
    term = total = F(1)
    for j in range(1, 61):
        term *= z/j
        total += (-1)**j * term
    # Degree 60 is the upper alternating partial sum, degree 61 the lower.
    lo, hi = rounded(total-term*z/61, total)
    for _ in range(squares):
        lo, hi = rounded(lo*lo, hi*hi)
    return lo, hi


def geometry():
    x, y, labels = list(V), list(V), ['anchor_'+str(i) for i in range(4)]
    for edge in EDGES:
        for a, b in (edge, edge[::-1]):
            x.append(tuple(V[b][k]-V[a][k] for k in range(3)))
            y.append(tuple(V[b][k]+V[a][k] for k in range(3)))
            labels.append(f'flap_{a}_{b}')
    return x, y, labels


def selectors():
    rows = {}
    for bits in product((0, 1), repeat=6):
        tails = [edge[0] if bit else edge[1] for edge, bit in zip(EDGES, bits)]
        if set(tails) == set(range(4)):
            mask = sum(bit*2**j for j, bit in enumerate(bits))
            rows[mask] = tuple(range(4))+tuple(5+2*j-bit for j, bit in enumerate(bits))
    return rows


def coverage():
    residual = {7: [], 8: [], 9: []}
    safe = total = 0
    for a in combinations_with_replacement(range(10), 9):
        total += 1
        counts = Counter(a)
        # Remove one occurrence of each of two *different* labels.
        unknown = any(len(counts)-(counts[i]==1)-(counts[j]==1) == 7
                      for i, j in combinations(counts, 2))
        if unknown:
            residual[len(counts)].append(a)
        else:
            safe += 1
    require(total == 48620 and safe == 45730, 'incorrect analytic-pruning coverage')
    require([len(residual[d]) for d in (7,8,9)] == [2520,360,10], 'residual counts')
    for d, rows in residual.items():
        pattern = {7:[1]*5+[2,2], 8:[1]*7+[2], 9:[1]*9}[d]
        require(all(sorted(Counter(a).values()) == pattern for a in rows), 'wrong pattern')
    return residual


def distance(points, i, j):
    return sum((a-b)**2 for a, b in zip(points[i], points[j]))


def independent_coefficient(alpha, x, y):
    """Use count subvectors and their multiplicities, not position subsets."""
    counts = Counter(alpha)
    labels = sorted(counts)
    lo = hi = F(0)
    used = 0
    for sub in product(*(range(counts[i]+1) for i in labels)):
        m = sum(sub)
        if m < 2:
            continue
        multiplicity = 1
        for i, r in zip(labels, sub):
            multiplicity *= comb(counts[i], r)
        pairs = [(labels[a], labels[b], sub[a]*sub[b])
                 for a, b in combinations(range(len(labels)), 2)]
        sx = sum(n*distance(x,i,j) for i,j,n in pairs)
        sy = sum(n*distance(y,i,j) for i,j,n in pairs)
        e = F(sum(n for i,j,n in pairs), 100)
        yl, yh = max(F(0),sy-e)/(2*m), (sy+e)/(2*m)
        xl, xh = max(F(0),sx-e)/(2*m), (sx+e)/(2*m)
        root = isqrt(m*SCALE*SCALE)
        rl, rh = F(root,SCALE), F(root+1,SCALE)
        if root*root == m*SCALE*SCALE:
            rh = rl
        kl = max(F(0), exponential(yh)[0]-exponential(xl)[1])/(m*rh)
        kh = max(F(0), exponential(yl)[1]-exponential(xh)[0])/(m*rl)
        if m % 2:
            lo -= multiplicity*kh/9
            hi -= multiplicity*kl/9
        else:
            lo += multiplicity*kl/9
            hi += multiplicity*kh/9
        used += multiplicity
    require(used == 502, 'lost a position-subset multiplicity')
    return lo, hi


def compositions(total, n):
    if n == 1:
        yield (total,)
        return
    for first in range(total+1):
        for tail in compositions(total-first, n-1):
            yield (first,)+tail


def multinomial(counts):
    out = factorial(sum(counts))
    for n in counts:
        out //= factorial(n)
    return out


def weight(counts, p):
    out = F(multinomial(counts))
    for n, w in zip(counts, p):
        out *= w**n
    return out


def toy_kernel(counts):
    return F(1+sum((i+2)*n*n for i,n in enumerate(counts)), 3+sum(counts))


def homogenization():
    checks = []
    for p in ((F(1,6),F(1,3),F(1,2)), (F(1),F(0),F(0)), (F(2,9),F(7,9),F(0))):
        direct = F(0)
        for m in range(2,10):
            moment = sum((weight(c,p)*toy_kernel(c) for c in compositions(m,3)), F(0))
            direct += F(8*(-1)**m*comb(7,m-2),m*(m-1))*moment
        polarized = F(0)
        for counts in compositions(9,3):
            coef = F(0)
            for sub in product(*(range(n+1) for n in counts)):
                m = sum(sub)
                if m >= 2:
                    multiplicity = 1
                    for n,r in zip(counts,sub):
                        multiplicity *= comb(n,r)
                    coef += F((-1)**m*multiplicity,9)*toy_kernel(sub)
            polarized += weight(counts,p)*coef
        require(direct == polarized, 'wrong weight homogenization')
        checks.append(str(direct))
    for m in range(2,10):
        require(F(8*comb(7,m-2),m*(m-1)*comb(9,m)) == F(1,9), 'coefficient factor')
        require(F(comb(9,m)*m*(m-1),72) == comb(7,m-2), 'energy curvature factor')
    return checks


def pattern_probabilities(residual):
    records = []
    for p in ((F(1,10),)*10, tuple(F(i,55) for i in range(1,11)), (F(1,7),)*7+(F(0),)*3):
        row = {}
        for d, tuples in residual.items():
            q = F(0)
            for a in tuples:
                c = Counter(a)
                q += weight(tuple(c.get(i,0) for i in range(10)),p)
            formula = F(0)
            for a in combinations(range(10),d):
                monomial = F(1)
                for i in a:
                    monomial *= p[i]
                if d == 7:
                    monomial *= factorial(9)//4 * sum((p[i]*p[j] for i,j in combinations(a,2)),F(0))
                elif d == 8:
                    monomial *= factorial(9)//2 * sum((p[i] for i in a),F(0))
                else:
                    monomial *= factorial(9)
                formula += monomial
            require(q == formula and 0 <= q <= 1, 'wrong pattern probability')
            row[d] = str(q)
        records.append(row)
    return records


def reject(action):
    try:
        action()
    except RuntimeError:
        return 1
    raise RuntimeError('corruption was not rejected')


def selector_cover(listed, actual):
    require(len(listed) == len(set(listed)) == 32 and set(listed) == set(actual),
            'incomplete asymmetric selector cover')


def run():
    inputs = json.loads((HERE/'INPUTS.json').read_text())['inputs']
    for entry in inputs:
        data = (HERE.parents[1]/entry['path']).read_bytes()
        require(sha256(data).hexdigest() == entry['sha256'], 'changed input: '+entry['path'])
    expected = json.loads((HERE/'EXPECTED.json').read_text())
    x,y,labels = geometry()
    geo = expected['geometry']
    require(geo == {'vertices':list(map(list,V)), 'source':list(map(list,x)),
                    'target':list(map(list,y)), 'labels':labels}, 'geometry mismatch')
    require(all(sum(a*b for a,b in zip(V[i],V[j])) == -1 for i,j in EDGES), 'wrong Gram matrix')
    require(all(distance(x,i,j) >= distance(y,i,j) for i,j in combinations(range(16),2)),
            'noncontracting fixture')
    require(max(distance(z,0,j) for z in (x,y) for j in range(16)) == 19, 'anchored radius')
    actual_selectors = selectors()
    shrink = F(19999,20000)
    strict_pairs = 0
    for chosen in actual_selectors.values():
        for i,j in combinations(chosen,2):
            dy = distance(y,i,j)
            require(dy > 0 and distance(x,i,j) > shrink**2*dy, 'strict rational control')
            require((1-shrink**2)*dy < F(1,100), 'strict control leaves cell')
            strict_pairs += 1
    listed = [r['mask'] for r in expected['selectors']]
    selector_cover(listed, actual_selectors)
    residual = coverage()
    unique = {tuple(actual_selectors[mask][i] for i in a)
              for mask in actual_selectors for rows in residual.values() for a in rows}
    require(len(unique) == expected['distinct_coefficients'] == 47936, 'coefficient coverage')
    critical = []
    for d in (7,8,9):
        mask, alpha = expected['first_minimizers'][str(d)]
        require(set(alpha) <= set(actual_selectors[mask]) and len(alpha) == 9, 'bad minimizer')
        lo,hi = independent_coefficient(tuple(alpha),x,y)
        require(lo > F(expected['margins'][str(d)]), 'independent critical bound failed')
        published = F(expected['minimum_lower_bounds'][str(d)])
        require(abs(lo-published) < F(1,10**20), 'lower endpoint disagreement')
        critical.append({'distinct_labels':d,'mask':mask,'lower_rounded_down':str(F((lo*10**20).__floor__(),10**20)),
                         'upper_rounded_up':str(F((hi*10**20).__ceil__(),10**20))})
    rejected = 0
    rejected += reject(lambda: selector_cover([2,4], actual_selectors))
    rejected += reject(lambda: selector_cover(listed[:-1], actual_selectors))
    rejected += reject(lambda: selector_cover(listed[:-1]+[listed[0]], actual_selectors))
    rejected += reject(lambda: exponential(F(-1)))
    return {'status':'FIRST_UNSIGNED_FLAP_CONTROLS_PASS', 'selector_count':32,
            'all_multisets_per_selector':48620, 'analytically_pruned_per_selector':45730,
            'residual_counts_per_selector':{d:len(a) for d,a in residual.items()},
            'distinct_exceptional_coefficients':len(unique),
            'independent_critical_intervals':critical,
            'homogenization_controls':homogenization(),
            'pattern_probability_controls':pattern_probabilities(residual),
            'rejected_corruptions':rejected,
            'pinned_inputs_verified':len(inputs),
            'strict_rational_control_pair_checks':strict_pairs,
            'exponential_method':'60/61 alternating partial sums, range reduction, outward rational squaring',
            'independent_fixed_point_digits':48}


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true')
    parser.add_argument('--check',action='store_true')
    args = parser.parse_args()
    require(not(args.check and args.write),'choose --check or --write')
    record = run()
    text = json.dumps(record,indent=2,sort_keys=True)+'\n'
    if args.write:
        (HERE/'AUDIT_EXPECTED.json').write_text(text)
    elif args.check:
        require(text == (HERE/'AUDIT_EXPECTED.json').read_text(),'audit expected record changed')
        print(json.dumps({'status':record['status'],'record_sha256':sha256(text.encode()).hexdigest()},indent=2))
    else:
        print(text,end='')
