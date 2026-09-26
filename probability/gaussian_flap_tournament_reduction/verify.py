"""Independent exact algebra/combinatorics audit; no imports from templates.py.

The analytic Gaussian implication remains a written proof, not a code result.
All checks survive python -O. Only standard-library integers/Fraction are used.
"""
from argparse import ArgumentParser
from collections import Counter
from copy import deepcopy
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, permutations
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def decode(mask):
    require(type(mask) is int and 0 <= mask < 64, "bad tournament mask")
    result, bit = set(), 1
    for lo in range(4):
        for hi in range(lo+1, 4):
            result.add((lo, hi) if mask & bit else (hi, lo))
            bit *= 2
    return result


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def add(a, b):
    return tuple(x+y for x, y in zip(a, b))


def sqdist(a, b):
    q = sub(a, b)
    return dot(q, q)


def rank(rows):
    a = [list(map(F, row)) for row in rows]
    r = 0
    for j in range(len(a[0])):
        p = next((i for i in range(r, len(a)) if a[i][j]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        scale = a[r][j]
        a[r] = [x/scale for x in a[r]]
        for i in range(r+1, len(a)):
            if a[i][j]:
                k = a[i][j]
                a[i] = [x-k*y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def gram_form(a, b):
    """Coefficients of h0,h1,h2,h3,c in a^T(diag(h)-c11^T)b."""
    return tuple(x*y for x, y in zip(a, b)) + (-sum(a)*sum(b),)


def vectors(v, arclist):
    x, y = list(v), list(v)
    for i, j in arclist:
        x.append(sub(v[j], v[i]))
        y.append(add(v[j], v[i]))
    return x, y


def polynomial_gram():
    """Formal bivariate polynomial arithmetic, variables (t,eta)."""
    def plus(*ps):
        out = Counter()
        for p in ps:
            for k, v in p.items():
                out[k] += v
        return {k: v for k, v in out.items() if v}
    def times(p, q):
        out = Counter()
        for (i, j), a in p.items():
            for (k, l), b in q.items():
                out[i+k, j+l] += a*b
        return {k: v for k, v in out.items() if v}
    one, t, h = {(0, 0): 1}, {(1, 0): 1}, {(0, 1): 1}
    neg = lambda p: {k: -v for k, v in p.items()}
    t2, h2 = times(t, t), times(h, h)
    den = plus(one, times(t, h))
    lhs1 = plus(times(plus(t, h), plus(t, h)),
                times(plus(one, neg(h2)), plus(one, neg(t2))),
                neg(times(den, den)))
    lhs2 = plus(times(t, plus(t, h)), one, neg(t2), neg(den))
    # Numerator of d/dt [(t+h)/(1+h*t)] equals 1-h^2.
    derivative = plus(den, neg(times(h, plus(t, h))), neg(one), h2)
    require(not lhs1 and not lhs2 and not derivative, "motion polynomial identity")
    return 3


def audit_algebra():
    e = [tuple(int(i == j) for i in range(4)) for j in range(4)]
    # A site is (origin coefficients, moving normal coefficients).
    zero = (0,)*4
    descriptors = [(e[i], zero) for i in range(4)]
    descriptors += [(e[j], e[i]) for i in range(4) for j in range(4) if i != j]
    checks = 0
    for (o, n), (p, m) in combinations(descriptors, 2):
        a, b = sub(o, p), sub(n, m)
        initial, final = sub(a, b), add(a, b)
        loss = sub(gram_form(initial, initial), gram_form(final, final))
        predicted = tuple(-4*x*y for x, y in zip(a, b))+(0,)
        require(loss == predicted, "formal distance-loss identity")
        require(all(x >= 0 for x in loss), "formal contraction coefficient")
        # Squared path distance is constant + sum_i lambda_i * 2*b_i*<a,vi>.
        derivative = tuple(2*x*y for x, y in zip(a, b))
        require(sum(a) == 0 and all(x <= 0 for x in derivative),
                "multi-origin motion coefficient")
        checks += 1
    return checks


def audit_mixture(units):
    total = sum(units)
    beta = {(i, j): F(units[4+i*3+j-(j>i)], total)
            for i in range(4) for j in range(4) if i != j}
    # Index formula above numbers outgoing heads in ascending order.
    all_arcs = [(i, j) for i in range(4) for j in range(4) if i != j]
    require([beta[e] for e in all_arcs] == [F(w, total) for w in units[4:]],
            "flap weight indexing")
    recovered = {e: F(0) for e in all_arcs}
    mass, remaining = F(0), F(0)
    for mask in range(64):
        chosen = decode(mask)
        probability = F(1)
        for i, j in chosen:
            q = beta[i, j]+beta[j, i]
            probability *= beta[i, j]/q if q else F(1, 2)
        mass += probability
        if len({i for i, j in chosen}) == 4:
            remaining += probability
        for i, j in chosen:
            recovered[i, j] += probability*(beta[i, j]+beta[j, i])
    require(mass == 1 and recovered == beta, "common-target convex mixture")
    sink_mass = F(0)
    for k in range(4):
        pk = F(1)
        for j in range(4):
            if j != k:
                q = beta[j, k]+beta[k, j]
                pk *= beta[j, k]/q if q else F(1, 2)
        sink_mass += pk
    require(remaining == 1-sink_mass and 0 <= remaining <= 1, "sinkless probability")
    return str(remaining)


def audit(data):
    require(data['schema'] == 'orthocentric_flap_selectors_v1', "schema")
    require(data['bit_edges'] == [[i, j] for i in range(4) for j in range(i+1, 4)],
            "bit edge ordering")
    require(data['bit_one'] == 'smaller_to_larger', "bit direction")
    require(data['relabelling_direction'] == 'old_vertex_to_new_vertex', "permutation direction")
    require(len(data['records']) == 64, "incomplete tournament certificate")
    seen, orbit_counts, score_counts, sink_count = set(), Counter(), Counter(), 0
    for mask, canonical, permutation in data['records']:
        require(mask not in seen, "duplicate tournament")
        seen.add(mask)
        require(sorted(permutation) == list(range(4)), "not a vertex permutation")
        actual, representative = decode(mask), decode(canonical)
        require({(permutation[i], permutation[j]) for i, j in actual} == representative,
                "invalid isomorphism certificate")
        # Minimality is checked via sets of arcs, not the producer's bit encoder.
        equivalent = []
        for candidate in range(canonical):
            target = decode(candidate)
            if any({(p[i], p[j]) for i, j in actual} == target
                   for p in permutations(range(4))):
                equivalent.append(candidate)
        require(not equivalent, "nonminimal orbit representative")
        degrees = tuple(sorted(sum(i == k for i, j in actual) for k in range(4)))
        score_counts[str(degrees)] += 1
        sink_count += degrees[0] == 0
        orbit_counts[str(canonical)] += 1
        require((degrees[0] > 0) == (canonical in (2, 4)), "sink pruning mismatch")
    require(seen == set(range(64)), "mask coverage")
    require(sink_count == 32 and orbit_counts['2'] == 8 and orbit_counts['4'] == 24,
            "wrong remaining counts")
    require(len(data['fixtures']) == 2, "need both template fixtures")
    fixture_masks, coordinate_checks, rank_checks = set(), 0, 0
    for fixture in data['fixtures']:
        require(fixture['status'] == 'INPUT_ONLY_NO_GAUSSIAN_SIGN', "fixture claim status")
        mask = fixture['mask']
        require(mask in (2, 4) and mask not in fixture_masks, "fixture template coverage")
        fixture_masks.add(mask)
        require(fixture['template'] == {2:'source_cycle', 4:'strong'}[mask], "template name")
        x = [tuple(map(F, p)) for p in fixture['input']]
        y = [tuple(map(F, p)) for p in fixture['output']]
        w = list(map(F, fixture['weights']))
        require(len(x) == len(y) == len(w) == 10, "fixture length")
        require(all(len(p) == 3 for p in x+y), "coordinate dimension")
        require(min(w) > 0 and sum(w) == 1 and F(fixture['variance']) > 0, "fixture weights")
        v = x[:4]
        require(v == y[:4] and len(set(x)) == len(set(y)) == 10, "distinct sites")
        a, b, d = map(F, fixture['shape_parameters'])
        require(min(a, b, d) > 0 and v[0] == (0,0,a) and v[1][:2] == (b,0)
                and v[2][1] == d, "shape gauge")
        require(all(dot(v[i],v[j]) == -1 for i,j in combinations(range(4),2)), "Gram products")
        require(rank([sub(p, v[0]) for p in v[1:]]) == 3, "tetrahedron degeneracy")
        h = [dot(p,p)+1 for p in v]
        require(sum(1/hi for hi in h) == 1 and
                all(sum(v[i][k]/h[i] for i in range(4)) == 0 for k in range(3)),
                "positive barycentric kernel")
        ordered = sorted(decode(mask), key=lambda e: sorted(e))
        xx, yy = vectors(v, ordered)
        require(x == xx and y == yy, "fixture endpoint decoding")
        expected_labels = ['anchor_'+str(i) for i in range(4)]
        expected_labels += [f'flap_{i}_{j}' for i,j in ordered]
        require(fixture['labels'] == expected_labels, "fixture labels")
        for m in range(64):
            chosen = decode(m)
            xx, yy = vectors(v, sorted(chosen))
            for i,j in combinations(range(10),2):
                require(sqdist(xx[i],xx[j]) >= sqdist(yy[i],yy[j]), "direct contraction")
                coordinate_checks += 1
            paired = [u+v for u,v in zip(xx,yy)]
            require(rank([sub(p,paired[0]) for p in paired[1:]]) == 6, "paired rank")
            rank_checks += 1
            tails = sorted({i for i,j in chosen})
            if len(tails) == 3:
                require(rank([v[i] for i in tails]) == 3, "sink basis independence")
    mixture_probabilities = [audit_mixture(u) for u in
                            [list(range(1,17)), list(range(16,0,-1)),
                             [1]*16, [1]*4+[0,2,0,0,0,3,1,0,4,0,2,0]]]
    require(mixture_probabilities[2] == '1/2', "balanced selector probability")
    return {"status":"ORTHOCENTRIC_TOURNAMENT_REDUCTION_EXACT_AUDIT_PASS",
            "tournaments":64, "sink_selectors":sink_count,
            "orbit_counts":dict(sorted(orbit_counts.items())),
            "score_counts":dict(sorted(score_counts.items())),
            "formal_pair_identities":audit_algebra(),
            "motion_polynomial_identities":polynomial_gram(),
            "direct_coordinate_pair_checks":coordinate_checks,
            "paired_rank_six_checks":rank_checks,
            "mixture_sinkless_probabilities":mixture_probabilities,
            "gaussian_signs_computed":0}


def run(path):
    data = json.loads(path.read_text())
    result = audit(data)
    bad = []
    p = deepcopy(data); p['records'].pop(); bad.append(p)
    p = deepcopy(data); p['records'][2][1] = 0; bad.append(p)
    p = deepcopy(data); p['fixtures'][0]['output'][4][0] = '123'; bad.append(p)
    p = deepcopy(data); p['fixtures'][1]['weights'][0] = '0'; bad.append(p)
    for damaged in bad:
        try:
            audit(damaged)
        except ValueError:
            continue
        raise ValueError('damaged certificate was accepted')
    result['rejected_corruptions'] = len(bad)
    result['certificate_sha256'] = sha256(path.read_bytes()).hexdigest()
    return result


def main():
    p = ArgumentParser(description=__doc__)
    p.add_argument('--certificate',type=Path,default=HERE/'CERTIFICATE.json')
    p.add_argument('--check',action='store_true')
    a = p.parse_args()
    result = run(a.certificate)
    if a.check:
        require(result == json.loads((HERE/'EXPECTED.json').read_text()), 'expected result mismatch')
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
