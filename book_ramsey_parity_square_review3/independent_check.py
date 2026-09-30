#!/usr/bin/env python3
"""Independent exact checks by six-reviewer-3; stdlib only, no author imports.

Finite controls validate identities, not universal graph nonexistence. The
written proof uses named external graph classifications, not a local census.
"""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import random


def require(condition, message):
    if not condition:
        raise ValueError(message)


def mm(a, b):
    columns = list(zip(*b))
    return [[sum(x*y for x, y in zip(row, col)) for col in columns]
            for row in a]


def transpose(a):
    return [list(row) for row in zip(*a)]


def identity(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def charpoly(a):
    """Newton identities from exact power traces, descending coefficients.

    No determinant elimination or invariant-basis algorithm is used.
    Every division is explicitly checked, also under python -O.
    """
    n = len(a)
    require(all(len(row) == n for row in a), 'square charpoly input')
    powers = identity(n)
    traces = [0]
    coefficients = [1]
    for k in range(1, n+1):
        powers = mm(powers, a)
        traces.append(sum(powers[i][i] for i in range(n)))
        numerator = -sum(coefficients[k-j]*traces[j] for j in range(1, k+1))
        require(numerator % k == 0, 'Newton exact division')
        coefficients.append(numerator // k)
    return coefficients


def poly_mul(a, b):
    c = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return c


def poly_power(a, n):
    c = [1]
    for _ in range(n):
        c = poly_mul(c, a)
    return c


def det3(a):
    x, y, z = a
    return (x[0]*y[1]*z[2]+x[1]*y[2]*z[0]+x[2]*y[0]*z[1]
            -x[2]*y[1]*z[0]-x[1]*y[0]*z[2]-x[0]*y[2]*z[1])


def evaluate(poly, t):
    value = 0
    for x in poly:
        value = value*t+x
    return value


def root_multiplicity(poly, t):
    poly = poly[:]
    multiplicity = 0
    while len(poly) > 1 and evaluate(poly, t) == 0:
        quotient = [poly[0]]
        for x in poly[1:-1]:
            quotient.append(x+t*quotient[-1])
        require(poly[-1]+t*quotient[-1] == 0, 'synthetic division')
        poly = quotient
        multiplicity += 1
    return multiplicity


def graph_data(a):
    n = len(a)
    require(n == 22, 'literal controls have order22')
    require(all(len(row) == n for row in a), 'graph shape')
    require(all(a[i][j] in (0, 1) and a[i][j] == a[j][i]
                and (i != j or a[i][j] == 0)
                for i in range(n) for j in range(n)), 'simple graph')
    red = [{j for j in range(n) if a[i][j]} for i in range(n)]
    blue = [set(range(n))-{i}-red[i] for i in range(n)]
    d = [len(s) for s in red]
    f = [[0]*n for _ in range(n)]
    for i, j in itertools.combinations(range(n), 2):
        value = (3-len(red[i] & red[j]) if a[i][j]
                 else 6-len(blue[i] & blue[j]))
        f[i][j] = f[j][i] = value
    mono = 0
    incident = [0]*n
    for i, j, k in itertools.combinations(range(n), 3):
        if a[i][j] == a[i][k] == a[j][k]:
            mono += 1
            for v in (i, j, k):
                incident[v] += 1
    return d, f, mono, incident


def square_from_defects(d, f):
    y = [10-x for x in d]
    return [[25*int(i == j)+24-4*(y[i]+y[j])-4*f[i][j]
             + (4*(y[i]*y[i]-2*y[i]) if i == j else 0)
             for j in range(22)] for i in range(22)]


def square_from_pages(d, f):
    """Separate construction via forced A^2 pages and K diagonal entries."""
    result = []
    for i in range(22):
        row = []
        for j in range(22):
            if i == j:
                row.append(4*d[i]+(2*d[i]-17)**2)
            else:
                row.append(4*(d[i]+d[j]-14-f[i][j]))
        result.append(row)
    return result


def graph_controls():
    rng = random.Random(2026093027)
    controls = []
    for label in range(128):
        a = [[0]*22 for _ in range(22)]
        for i, j in itertools.combinations(range(22), 2):
            if label == 0:
                edge = False
            elif label == 1:
                edge = True
            elif label == 2:
                edge = (j-i in (1, 21))
            elif label == 3:
                edge = (i < 11 <= j)
            else:
                edge = rng.randrange(23) < (label % 23)
            a[i][j] = a[j][i] = int(edge)
        d, f, mono, incident = graph_data(a)
        k = [[2*a[i][j]+(2*d[i]-17 if i == j else 0)
              for j in range(22)] for i in range(22)]
        h = square_from_defects(d, f)
        require(mm(k, k) == h, 'literal universal matrix-square identity')
        require(square_from_pages(d, f) == h, 'page construction')
        aa = mm(a, a)
        for i in range(22):
            for j in range(22):
                predicted = (d[i]+d[j]-14+(14-d[i] if i == j else 0)
                             +(17-d[i]-d[j])*a[i][j]-f[i][j])
                require(aa[i][j] == predicted, 'literal A^2 identity')
        total = sum(f[i][j] for i, j in itertools.combinations(range(22), 2))
        require(2*total == 132-3*sum((x-10)**2 for x in d), 'global defect')
        require(2*mono == 2*math.comb(22, 3)-sum(x*(21-x) for x in d),
                'literal mono triangles')
        for i in range(22):
            require(sum(f[i]) == 3*d[i]+6*(21-d[i])-2*incident[i],
                    'incident triangle equation')
            require(sum(f[i]) % 2 == d[i] % 2, 'incident parity')
        controls.append([label, sum(d)//2, mono, total, sum(x*x for x in d)])
    return {'graphs': 128, 'spines': 128*231, 'matrix_entries': 128*484,
            'incident_equations': 128*22,
            'signed_invalid_controls_are_not_witnesses': True,
            'records_sha256': hashlib.sha256(json.dumps(controls).encode()).hexdigest()}


CASES = [(7, 12, 3), (9, 6, 7), (11, 0, 11)]


def forced_square(histogram):
    a, b, c = histogram
    d = [8]*a+[9]*b+[10]*c
    f = [[0]*22 for _ in range(22)]
    for i in range(a, a+b, 2):
        f[i][i+1] = f[i+1][i] = 1
    h = square_from_pages(d, f)
    require(h == square_from_defects(d, f), 'forced page/defect agreement')
    return h


def predicted_charpoly(histogram):
    a, b, c = histogram
    if b:
        m = b//2
        quotient = [[25+8*a, 12*b, 16*c],
                    [12*a, 17+16*b, 20*c],
                    [16*a, 20*b, 25+24*c]]
        factors = poly_mul(poly_power([1, -25], a+c+m-2),
                           poly_power([1, -17], m-1))
    else:
        quotient = [[25+8*a, 16*c], [16*a, 25+24*c]]
        factors = poly_power([1, -25], a+c-2)
    return poly_mul(factors, charpoly(quotient)), quotient


def validate_forced(histogram, h):
    expected, quotient = predicted_charpoly(histogram)
    actual = charpoly(h)
    require(actual == expected, 'entire forced characteristic polynomial')
    a, b, c = histogram
    groups = [list(range(a)), list(range(a, a+b)), list(range(a+b, 22))]
    groups = [g for g in groups if g]
    for i, rows in enumerate(groups):
        for j, columns in enumerate(groups):
            require(all(sum(h[v][w] for w in columns) == quotient[i][j]
                        for v in rows), 'quotient row sums')
    determinant = actual[-1]
    record = {'histogram': list(histogram), 'edges': (8*a+9*b+10*c)//2,
              'quotient': quotient, 'full_characteristic_polynomial': actual,
              'determinant': determinant,
              'eigenvalue17_multiplicity': root_multiplicity(actual, 17),
              'eigenvalue25_multiplicity': root_multiplicity(actual, 25),
              'integer_square': math.isqrt(determinant)**2 == determinant}
    if b:
        record['quotient_determinant'] = det3(quotient)
        require(record['quotient_determinant'] in (114177, 65681),
                'displayed quotient determinant')
        require(not record['integer_square'], 'determinant obstruction')
    if histogram == (7, 12, 3):
        shifted = [[quotient[i][j]-17*int(i == j) for j in range(3)]
                   for i in range(3)]
        require(det3(shifted) == -3072, 'no quotient eigenvalue17')
        require(record['eigenvalue17_multiplicity'] == 5, 'odd rational eigenspace')
        value, valuation = determinant, 0
        while value % 17 == 0:
            value //= 17
            valuation += 1
        require(valuation == 5, '17-adic valuation')
        record.update(det_quotient_minus17=-3072, valuation17=valuation)
    elif histogram == (9, 6, 7):
        require(256**2 < det3(quotient) < 257**2, 'nonsquare interval')
        record['quotient_isqrt'] = 256
    else:
        require(charpoly(quotient) == [1, -402, 1681], '99 H quotient')
        require(record['integer_square'], '99 determinant alone is inconclusive')
        kq = [[7, 8], [8, 15]]
        require(charpoly(kq) == [1, -22, 41], '99 K quotient')
        require(charpoly(mm(kq, kq)) == charpoly(quotient), '99 quotient-square spectra')
        record['necessary_K_characteristic_polynomial'] = poly_mul(
            poly_power([1, 0, -25], 10), [1, -22, 41])
        record['necessary_K_determinant'] = 41*5**20
    return record


def cyclic_four(offsets):
    return [[int(i != j and (j-i) % 11 in offsets) for j in range(11)]
            for i in range(11)]


def block_controls():
    rng = random.Random(2026093099)
    nonzero = 0
    transcript = []
    for number in range(64):
        steps = rng.sample(range(1, 6), 2)
        b = cyclic_four(set(steps+[-x % 11 for x in steps]))
        steps = rng.sample(range(1, 6), 2)
        ell = cyclic_four(set(steps+[-x % 11 for x in steps]))
        shifts = set(rng.sample(range(11), 4))
        rows = list(range(11))
        cols = list(range(11))
        rng.shuffle(rows)
        rng.shuffle(cols)
        m = [[int((cols[j]-rows[i]) % 11 in shifts) for j in range(11)]
             for i in range(11)]
        c = [[int(i != j)-ell[i][j] for j in range(11)] for i in range(11)]
        a = [b[i]+m[i] for i in range(11)]
        a += [transpose(m)[i]+c[i] for i in range(11)]
        d, f, mono, incident = graph_data(a)
        require(d == [8]*11+[10]*11, 'block degrees')
        bb, ll = mm(b, b), mm(ell, ell)
        mmt, mtm = mm(m, transpose(m)), mm(transpose(m), m)
        bm, ml = mm(b, m), mm(m, ell)
        rb = [[bb[i][j]-b[i][j]+mmt[i][j]-6*int(i == j)-2
               for j in range(11)] for i in range(11)]
        rl = [[ll[i][j]-ell[i][j]+mtm[i][j]-6*int(i == j)-2
               for j in range(11)] for i in range(11)]
        rx = [[bm[i][j]-ml[i][j] for j in range(11)] for i in range(11)]
        predicted = [[-x for x in rb[i]+rx[i]] for i in range(11)]
        predicted += [[-x for x in transpose(rx)[i]+rl[i]] for i in range(11)]
        require(predicted == f, 'literal defect/block residual equivalence')
        require(all(sum(row) == 0 for row in rb+rl+rx), 'regular residual row sums')
        count = sum(x != 0 for row in f for x in row)
        require(count > 0, 'control deliberately not a saturated witness')
        nonzero += count
        transcript.append([number, mono, count, sum(x*x for row in f for x in row)])
    return {'graphs': 64, 'literal_defect_entries': 64*484,
            'nonzero_signed_entries': nonzero,
            'records_sha256': hashlib.sha256(json.dumps(transcript).encode()).hexdigest(),
            'no_graph_enumeration_or_nonexistence_inference': True}


def histogram_and_classification_arithmetic():
    candidates = [(a, b, 22-a-b) for a in range(23) for b in range(23-a)
                  if b % 2 == 0]
    equality = [x for x in candidates if 3*x[0]+x[1] == 33]
    require(equality == CASES, 'all parity equality histograms')
    boundaries = {}
    for edges in (97, 98, 99):
        boundaries[str(edges)] = [list(x) for x in candidates
                                 if (8*x[0]+9*x[1]+10*x[2]) == 2*edges
                                 and 3*x[0]+x[1] <= 32]
    require(boundaries['97'] == [[4, 18, 0], [5, 16, 1], [6, 14, 2]],
            '97-edge corollary')
    require(boundaries['98'] == [[a, 24-2*a, a-2] for a in range(2, 9)],
            '98-edge corollary')
    require(boundaries['99'] == [[a, 22-2*a, a] for a in range(11)],
            '99-edge strengthened corollary')
    for a, b, c in candidates:
        require((132-3*(4*a+b))-b == 4*(33-3*a-b), 'strict integral gap')
    pairs = [(r, 6-r) for r in range(1, 6) if 11 % r == 0 and 11 % (6-r) == 0]
    require(not pairs and 22 % 3 != 0, 'all regular line-graph root cases')
    require(11 not in (12, 9, 8) and 11 != 6 and 11 != 5,
            'exceptional, cocktail-party, clique orders')
    return {'all_handshake_histograms': len(candidates),
            'parity_equality_candidates': [list(x) for x in equality],
            'necessary_boundaries_with_global_degree_dependency': boundaries,
            'classification_degree4_exceptional_layer_orders': [12, 9, 8],
            'line_graph_bipartite_root_degree_pairs': pairs,
            'external_classifications_are_accepted_not_recomputed': True}


def audit():
    return {'agent': 'six-reviewer-3', 'role': 'independent mathematical reviewer',
            'method': 'literal set/triple controls; full Newton characteristic polynomials; exact block residuals',
            'graph_controls': graph_controls(),
            'forced_square_cases': [validate_forced(x, forced_square(x)) for x in CASES],
            'block_controls': block_controls(),
            'arithmetic': histogram_and_classification_arithmetic(),
            'scope': 'Controls are arithmetic checks; universal conclusions use the written proof and named external classification theorems.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', type=Path)
    parser.add_argument('--expected', type=Path)
    args = parser.parse_args()
    result = audit()
    data = (json.dumps(result, sort_keys=True, indent=2)+'\n').encode()
    if args.expected:
        require(data == args.expected.read_bytes(), 'expected result bytes')
    if args.write:
        args.write.write_bytes(data)
    print(json.dumps({'status': 'complete', 'agent': 'six-reviewer-3',
                      'graphs': 128, 'block_controls': 64,
                      'full_characteristic_polynomials': 3,
                      'summary_sha256': hashlib.sha256(data).hexdigest()}, sort_keys=True))


if __name__ == '__main__':
    main()
