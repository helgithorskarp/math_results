#!/usr/bin/env python3
"""six-reviewer-3: independent Newton/projector audit of triangle-majority8757.

No author imports. Written degree bounds and spectral proof are in REVIEW.md.
Published reviewer8682 supplies hash-pinned integer Bareiss PSD elimination.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, product
from math import lcm, factorial
from pathlib import Path
import importlib.util
import json

TYPES = ((0, 1), (0, 2), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0))
DEGREES = ((0, 0), (1, 0), (0, 1), (1, 1), (0, 2))


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(obj):
    return sha256(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def load_prior(path):
    need(sha256(path.read_bytes()).hexdigest() == '2382479d58813caf97b33f2b6cbc3fc318a4cd10e1c382aa9f6b4436108cd3c1', 'independent toolkit hash')
    spec = importlib.util.spec_from_file_location('independent8682', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def choose(n, k):
    if k < 0 or n < k:
        return F(0)
    result = F(1)
    for j in range(k):
        result *= F(n-j, j+1)
    return result


def generic_weights(q):
    need(type(q) is int and q >= 4, 'generic integer parameter')
    q, c = F(q), F(1, 2)
    s, k = 3*q+4, c/(3*q+5)
    one = (1-1/q, 1+1/q, 1+6/q)
    two = (1+2*k/(q*(q-1)), 1+2*(k+(q-1)**2/q)/((q-1)*(q-2)),
           1+6/q-6*k*(q+1)/(q*(q-1)))
    o, p, a, b, d, e, f = TYPES
    rows = [(o, o, (c-q-4+6/q)/(q-1)),
            (o, p, q*(q-3)/((q-1)*(q-2))),
            (p, p, (c+two[2]-1+2*q/(q-1)-s+q*(q-1)/2)/((q-2)*(q-3)/2))]
    for outside, (alpha, beta, gamma) in [(o, one), (p, two)]:
        rows += [(outside, a, alpha), (outside, d, alpha),
                 (outside, b, beta), (outside, e, beta), (outside, f, gamma)]
    t = 3+2/q
    rows += [(a, a, 0), (a, b, 0), (b, b, 0), (a, d, 2),
             (a, e, t), (b, d, t), (b, e, (s-t)/(q-1))]
    return {tuple(sorted((x, y))): F(v) for x, y, v in rows}


def delta(q):
    return 2*q*(q-1)*(q-2)*(q-3)*(3*q+5)


def sectors(q):
    weights, s = generic_weights(q), 3*q+4
    result = []
    for j, ell in DEGREES:
        levels = [t for t in TYPES if j <= t[0] <= 3-j and ell <= t[1] <= q-ell]
        norms = [choose(3-2*j, a-j)*choose(q-2*ell, b-ell) for a, b in levels]
        G = []
        for i, (a, b) in enumerate(levels):
            row = []
            for k, (c, d) in enumerate(levels):
                key = tuple(sorted(((a, b), (c, d))))
                incidence = (-1)**(j+ell)*choose(3-a-j, c-j)*choose(q-b-ell, d-ell)
                row.append(norms[i]*(s*(i == k)+weights.get(key, 0)*incidence)-
                           (norms[i]*norms[k] if j == ell == 0 else 0))
            G.append(row)
        need(G == list(map(list, zip(*G))), 'sector symmetry')
        result.append({'degree': (j, ell), 'levels': levels, 'D': norms, 'G': G})
    return result


def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p or [F(0)]


def add(a, b):
    return trim([(a[i] if i < len(a) else 0)+(b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))])


def mul(a, b):
    out = [F(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return trim(out)


def evaluate(p, u):
    out = F(0)
    for x in reversed(p):
        out = out*u+x
    return out


def interpolate(values):
    """Exact forward Newton differences on 0,...,d, not symbolic Leibniz."""
    out, basis, differences = [F(0)], [F(1)], list(map(F, values))
    for r in range(len(values)):
        out = add(out, [x*differences[0]/factorial(r) for x in basis])
        differences = [b-a for a, b in zip(differences, differences[1:])]
        basis = mul(basis, [F(-r), F(1)])
    return trim(out)


def determinant(matrix):
    """Rational Gaussian determinant at numeric interpolation nodes."""
    a = [list(map(F, row)) for row in matrix]
    out = F(1)
    for k in range(len(a)):
        pivot = next((i for i in range(k, len(a)) if a[i][k]), None)
        if pivot is None:
            return F(0)
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]; out = -out
        out *= a[k][k]
        for i in range(k+1, len(a)):
            ratio = a[i][k]/a[k][k]
            for j in range(k+1, len(a)):
                a[i][j] -= ratio*a[k][j]
    return out


def positive(p, strict=False):
    need(all(x >= 0 for x in p) and (not strict or p[0] > 0), 'coefficient-positive polynomial')


def reconstruct_signs(author):
    # Delta G has degree <=9. A k-minor has degree <=9k. Weighted
    # margins times Delta D_i q(2q+1) have degree <=12. See REVIEW.md.
    samples = [sectors(4+u) for u in range(10)]
    polynomials, records, reconstructed = [], [], []
    for index, (j, ell) in enumerate(DEGREES):
        sector = samples[0][index]; levels = sector['levels']; n = len(levels)
        P = [[interpolate([delta(4+u)*samples[u][index]['G'][i][k] for u in range(10)])
              for k in range(n)] for i in range(n)]
        signs = []
        for row in P:
            sr = []
            for p in row:
                sign = 1 if all(x >= 0 for x in p) else -1
                positive([sign*x for x in p]); sr.append(sign)
            signs.append(sr)
        kernels = [[a for a, b in levels], [int(a >= 2) for a, b in levels]] if index == 0 else \
                  [[1]*n] if index == 1 else []
        for v in kernels:
            for row in P:
                need(trim(sum((row[k][i]*v[k] if i < len(row[k]) else 0)
                              for k in range(n)) for i in range(10)) == [0], 'polynomial kernel identity')
        anchors = [(1, 0), (2, 0)] if index == 0 else [(1, 0)] if index == 1 else []
        keep = [i for i, level in enumerate(levels) if level not in anchors]
        if kernels:
            need(determinant([[v[levels.index(a)] for a in anchors] for v in kernels]) != 0, 'kernel anchor minor')
        for size in range(1, len(keep)+1):
            ids = keep[:size]
            values = [determinant([[evaluate(P[i][k], u) for k in ids] for i in ids])
                      for u in range(9*size+1)]
            coefficients = interpolate(values); positive(coefficients, True)
            expected = next(r for r in author['signs'] if r['kind'] == 'lower_leading_minor' and
                            r['sector'] == [j, ell] and r['size'] == size)
            need(coefficients == list(map(F, expected['coefficients'])), 'every lower coefficient')
            records.append({'kind': 'lower', 'sector': [j, ell], 'size': size,
                            'degree': len(coefficients)-1, 'coefficients': list(map(str, coefficients)),
                            'degree_bound': 9*size})
        for i in range(n):
            vals, dens = [], []
            for u in range(13):
                q = 4+u; data = sectors(q)[index]; D = data['D']; G = data['G']
                v = [F(4, 3*q) if a == 0 else F(2*q+1, q) if a == 3 else F(1)
                     for a, b in levels] if index == 0 else \
                    [F(1) if a == 0 else F(9, 10) for a, b in levels] if index == 2 else [F(1)]*n
                absolute = sum(signs[i][k]*G[i][k]*v[k]/(D[i]*v[i]) for k in range(n))
                denominator = delta(q)*D[i]*q*(2*q+1)
                vals.append(denominator*(2*(3*q+4)-absolute)); dens.append(denominator)
            numerator, denominator = interpolate(vals), interpolate(dens)
            positive(numerator); positive(denominator, True)
            expected = next(r for r in author['signs'] if r['kind'] == 'weighted_Gershgorin_margin' and
                            r['sector'] == [j, ell] and r['row'] == i)
            en, ed = list(map(F, expected['numerator'])), list(map(F, expected['denominator']))
            positive(en); positive(ed, True)
            need(mul(numerator, ed) == mul(en, denominator), 'every margin rational identity')
            records.append({'kind': 'margin', 'sector': [j, ell], 'row': i,
                            'numerator': list(map(str, numerator)), 'denominator': list(map(str, denominator)),
                            'degree_bound': 12})
        polynomials.append(P); reconstructed.append({'degree': [j, ell], 'levels': levels, 'scaled_G':
                                  [[list(map(str, p)) for p in row] for row in P]})
    # Independent complete constant identity from the interpolated trivial entries.
    for i, (a, b) in enumerate(TYPES):
        left = mul(add(add(add(add(add(add(polynomials[0][i][0], polynomials[0][i][1]),
                    polynomials[0][i][2]), polynomials[0][i][3]), polynomials[0][i][4]),
                    polynomials[0][i][5]), polynomials[0][i][6]), [17, 3])
        right = interpolate([delta(4+u)*samples[u][0]['D'][i]*F(1, 2)*
                ((3*(4+u)+5) if a == 0 else 1 if a < 3 else -3*((4+u)+1)) for u in range(10)])
        need(left == right, 'controlled constant polynomial identity')
    std_levels = samples[0][1]['levels']
    signed = [1 if a == 1 else -1 for a, b in std_levels]
    for i, row in enumerate(polynomials[1]):
        left = [sum((row[k][r] if r < len(row[k]) else 0)*signed[k]
                    for k in range(len(row))) for r in range(10)]
        right = interpolate([2*(3*(4+u)+4)*delta(4+u)*samples[u][1]['D'][i]*signed[i]
                             for u in range(10)])
        need(trim(left) == right, 'exact2s core-standard eigenmode polynomial identity')
    need(len(records) == 33, 'complete sign coverage')
    return {'records': records, 'entry_polynomials_sha256': digest(reconstructed),
            'lower_count': 15, 'margin_count': 18, 'author_coefficients_checked': author['coefficient_count'],
            'entry_degree_bound': 9, 'controlled_constant_identity': True,
            'exact_2s_eigenmode_identity': True}, polynomials


def boundary_weights(q, records):
    need(type(q) is int and q in [2, 3], 'boundary parameter')
    need(len(records) == 2 and [r['q'] for r in records] == [2, 3], 'boundary domain coverage')
    record = records[q-2]
    need(set(record) == {'q', 'keys', 'values'}, 'boundary fields')
    keys = [tuple(map(tuple, pair)) for pair in record['keys']]
    feasible = {tuple(sorted(pair)) for pair in combinations_with_replacement(TYPES, 2)
                if sum(t[0] for t in pair) <= 3 and sum(t[1] for t in pair) <= q}
    need(set(keys) == feasible and len(keys) == len(feasible) == len(record['values']), 'boundary orbit completeness')
    need(all(type(x) is str for x in record['values']), 'exact boundary strings')
    return {key: F(x) for key, x in zip(keys, record['values'])}


def domain(q):
    need(type(q) is int and q >= 2, 'literal integer parameter')
    need((q*q+13*q+16)//2 <= 80, 'literal order80 guard')
    return [mask for mask in range(1 << (q+3))
            if mask.bit_count() <= 2 or (mask.bit_count() == 3 and (mask & 7).bit_count() >= 2)]


def typ(mask):
    return (mask & 7).bit_count(), (mask >> 3).bit_count()


def family_list(members):
    return [[int(mask >> i & 1) for mask in members] for i in range(3)]+[
        [int(mask.bit_count() == 3 or (mask.bit_count() == 2 and mask & 7 == mask)) for mask in members]]


def literal(q, boundaries, prior):
    members, s = domain(q), 3*q+4
    weights = boundary_weights(q, boundaries) if q < 4 else generic_weights(q)
    N = len(members); m = N-1
    C = [[F(s-1) if a == b else F(-1) if a & b else weights[tuple(sorted((typ(a), typ(b))))]-1
          for b in members[1:]] for a in members[1:]]
    rows = list(map(sum, C))
    Q = [[sum(rows)]+[-x for x in rows]]+[
        [-rows[i]]+list(row) for i, row in enumerate(C)]
    L = [[x+1 for x in row] for row in Q]
    M = [[F(L[i][j]-s*(i == j), N-s) for j in range(N)] for i in range(N)]
    U = [[F(N*(i == j)-1)-C[i][j] for j in range(m)] for i in range(m)]
    observed = prior.checks(members, M, s, 4)
    need(prior.psd(C) == m-4 and prior.psd(U) == m, 'complete core ranks')
    families = family_list(members)
    need([sum(f) for f in families] == [s]*4, 'known family sizes')
    gram = [[sum((F(f[i])-F(s, N))*(F(g[i])-F(s, N)) for i in range(N))
             for g in families] for f in families]
    need(prior.psd(gram) == 4, 'four independent forced directions')
    den = lcm(*(x.denominator for row in M for x in row))
    numerators = [[int(x*den) for x in row] for row in M]
    result = {'q': q, 'N': N, 's': s, 'rank_L': observed['lower_rank'],
              'rank_upper': observed['upper_rank'], 'M_denominator': den,
              'M_numerators_sha256': digest(numerators), 'forced_Gram_sha256': prior.fingerprint(gram)}
    if q >= 4:
        alpha = F(q*(q+1), 2)+F(3*(q+1), 3*q+5)
        y = [F(1) if typ(mask)[0] == 0 else F(1, 3*q+5) if typ(mask)[0] < 3
             else F(-3*(q+1), 3*q+5) for mask in members[1:]]
        need(sum(y) == sum(x*x for x in y) == alpha, 'exact projected constant norm')
        need(rows == [x/2 for x in y], 'literal controlled constant')
        need([sum(C[i][j]*y[j] for j in range(m)) for i in range(m)] == [x/2 for x in y], 'literal projected constant eigenvector')
        v = [-alpha]+y
        controlled = (1+alpha)/2
        need([sum(Q[i][j]*v[j] for j in range(N)) for i in range(N)] == [controlled*x for x in v], 'exact lifted controlled eigenvalue')
        h = [1, -1, 0]
        z = [0]+[(1 if typ(mask)[0] == 1 else -1)*sum(h[i] for i in range(3) if mask >> i & 1)
                 if typ(mask)[0] in [1, 2] else 0 for mask in members[1:]]
        need(sum(z) == 0 and any(z), 'nonzero mean-zero core-standard eigenvector')
        need([sum(Q[i][j]*z[j] for j in range(N)) for i in range(N)] == [2*s*x for x in z], 'literal exact2s lifted eigenmode')
        lower_bound = F(1, 2)+F(m-alpha, 2*N-1)
        need(prior.psd([[x-lower_bound*(i == j) for j, x in enumerate(row)] for i, row in enumerate(U)]) == m,
             'improved strictly positive upper core gap')
        margin = min(F(N-2*s), N-controlled)
        prior.gap(M, s, margin)
        need(margin/F(N-s) >= F(5, 13), 'uniform nonunit M separation')
        result.update(alpha=str(alpha), lifted_controlled_eigenvalue=str(controlled),
                      core_gap_lower_bound=str(lower_bound), scaled_upper_gap=str(margin),
                      M_upper_gap=str(margin/F(N-s)), M_upper_gap_status='exact by complete spectral proof')
    return (members, M, s), C, result


def projector_actions(q, C, prior):
    """Overcomplete explicit projector columns, not the author's RREF basis."""
    members = domain(q)[1:]; m = len(members); data = sectors(q)
    edges = list(combinations(range(q), 2)); scale = 2*(q-1)*(q-2)
    edge_projector = [[scale*(e == f)-2*(q-1)*len(set(e) & set(f))+4 for f in edges] for e in edges]
    need(prior.psd(edge_projector) == q*(q-3)//2, 'harmonic projector rank')
    need(prior.mm(edge_projector, edge_projector) == [[scale*x for x in row] for row in edge_projector], 'harmonic projector identity')
    need(all(sum(row[k] for k, e in enumerate(edges) if point in e) == 0
             for row in edge_projector for point in range(q)), 'edge row-sum constraints')
    core_points = [[3*(i == k)-1 for i in range(3)] for k in range(3)]
    outside_points = [[q*(i == k)-1 for i in range(q)] for k in range(q)]
    bases_core = {0: [None], 1: core_points}
    bases_outside = {0: [None], 1: outside_points, 2: edge_projector}
    denominator = lcm(*(x.denominator for row in C for x in row))
    Ci = [[int(x*denominator) for x in row] for row in C]
    columns, records = [], []
    for sector in data:
        j, ell = sector['degree']; levels = sector['levels']; norms = sector['D']; G = sector['G']
        count = 0
        for cb, ob in product(bases_core[j], bases_outside[ell]):
            values = []
            for mask in members:
                cv = 1 if j == 0 else sum(cb[i] for i in range(3) if mask >> i & 1)
                selected = tuple(i for i in range(q) if mask >> (i+3) & 1)
                ov = 1 if ell == 0 else sum(ob[i] for i in selected) if ell == 1 else \
                     ob[edges.index(selected)] if len(selected) == 2 else 0
                values.append(cv*ov)
            for k, input_level in enumerate(levels):
                vector = [value if typ(mask) == input_level else 0 for mask, value in zip(members, values)]
                columns.append(vector)
                actual = [sum(x*y for x, y in zip(row, vector)) for row in Ci]
                expected = [F(0) if typ(mask) not in levels else
                            G[levels.index(typ(mask))][k]/norms[levels.index(typ(mask))]*values[i]
                            for i, mask in enumerate(members)]
                need(actual == [denominator*x for x in expected], 'literal projector-column sector action')
                count += 1
        records.append({'sector': list(sector['degree']), 'checked_columns': count})
    frame = [[sum(v[i]*v[k] for v in columns) for k in range(m)] for i in range(m)]
    need(prior.psd(frame) == m, 'complete overcomplete literal span')
    return {'q': q, 'dimension': m, 'checked_columns': len(columns), 'span_rank': m,
            'edge_harmonic_rank': q*(q-3)//2, 'sectors': records}


def equality_census(q):
    """All intersecting pair subfamilies, plus complete compatible triples."""
    members = domain(q); pairs = [a for a in members if a.bit_count() == 2]
    triples = [a for a in members if a.bit_count() == 3]; s = 3*q+4
    winners = {tuple(a for a in members if a >> i & 1) for i in range(3)}
    examined = 0
    def visit(chosen, candidates):
        nonlocal examined
        examined += 1
        compatible = [a for a in triples if all(a & b for b in chosen)]
        candidate = tuple(sorted(chosen+compatible))
        need(len(candidate) <= s, 'literal equality census upper bound')
        if len(candidate) == s:
            winners.add(candidate)
        for i, pair in enumerate(candidates):
            visit(chosen+[pair], [other for other in candidates[i+1:] if other & pair])
    visit([], pairs)
    expected = {tuple(mask for mask, x in zip(members, f) if x) for f in family_list(members)}
    need(winners == expected and len(winners) == 4, 'exact four-family census')
    return {'q': q, 'pair_subfamilies_examined': examined, 'maximum_size': s,
            'maximum_families': 4, 'family_sha256': digest(sorted(winners))}


def spectral_refinements():
    threshold = interpolate([3*(25+x)**3-64*(25+x)**2-199*(25+x)-144 for x in range(4)])
    need(threshold == [1756, 2226, 161, 3], 'complete large-q threshold polynomial')
    need(all(3*q**3-64*q*q-199*q-144 < 0 for q in range(4, 25)), 'complete lower-q mode split')
    rows = []
    for q in [4, 5, 6, 7, 24, 25, 32, 100, 1000]:
        N, s = (q*q+13*q+16)//2, 3*q+4
        alpha = F(q*(q+1), 2)+F(3*(q+1), 3*q+5)
        controlled = (1+alpha)/2
        det = N-controlled
        trace = F(N)+F(1, 2)
        need(det > 0 and F(1, 4)-trace/2+det == F(N-1-alpha, 2) > 0,
             'core smallest eigenvalue strictly above1/2')
        need(1-trace+det == -alpha/2 < 0, 'core smallest eigenvalue below1')
        need((1+alpha)*(N-F(1, 2)-alpha)-alpha*(N-1-alpha) == det,
             'exact two-dimensional core-cap determinant')
        if q >= 25:
            need(controlled > 2*s, 'controlled lifted mode is strictly largest')
        lower = F(1, 2)+F(N-1-alpha, 2*N-1)
        rows.append({'q': q, 'N': N, 's': s, 'alpha': str(alpha),
                     'core_cap_trace': str(trace), 'core_cap_determinant': str(det),
                     'core_gap_lower_bound': str(lower),
                     'M_gap_lower_bound': str(min(N-2*s, det)/F(N-s)),
                     'M_gap_exact': str(min(N-2*s, det)/F(N-s)),
                     'largest_lifted_mode': 'controlled constant' if q >= 25 else 'core-standard2s'})
    return {'threshold_at_q25_coefficients': threshold, 'cases': rows}


def product_forced_grams(parts, prior):
    records = []
    for parameters in [(2, 2), (2, 3), (4, 4), (2, 3, 2), (3, 5, 3)]:
        factors = [parts[q][0] for q in parameters]
        Nprod = 1
        for family, matrix, s in factors:
            Nprod *= len(family)
        lowest = min(parameters); eligible = [i for i, q in enumerate(parameters) if q == lowest]
        columns = [(i, f) for i in eligible for f in family_list(factors[i][0])]
        gram = []
        for i, f in columns:
            row = []
            for j, g in columns:
                if i != j:
                    row.append(F(0))
                else:
                    Nj, sj = len(factors[i][0]), factors[i][2]
                    row.append(Nprod*(F(sum(x*y for x, y in zip(f, g)), Nj)-F(sj, Nj)**2))
            gram.append(row)
        count = 4*len(eligible); need(prior.psd(gram) == count, 'independent product forced directions')
        Nmin, smin = len(parts[lowest][0][0]), parts[lowest][0][2]
        need((Nprod*smin) % Nmin == 0, 'integral product maximum size')
        records.append({'parameters': list(parameters), 'N': Nprod, 's': Nprod*smin//Nmin,
                        'forced_nullity': count, 'forced_Gram_sha256': prior.fingerprint(gram),
                        'status': 'forced-Gram check; full product PSD/equality proved analytically'})
    return records


def reject(callback):
    try:
        callback()
    except (ValueError, TypeError, KeyError, ZeroDivisionError):
        return
    raise ValueError('damaged control accepted')


def run(boundaries, signs, author_results, prior):
    certificate, _ = reconstruct_signs(signs)
    literal_rows, actions, parts = [], [], {}
    for q in range(2, 8):
        part, C, row = literal(q, boundaries, prior); parts[q] = part, C
        if q <= 4:
            old = next(r for r in author_results['literal_matrices'] if r['q'] == q)
            for key in ['N', 's', 'rank_L', 'rank_upper', 'M_denominator', 'M_numerators_sha256']:
                need(row[key] == old[key], 'every original matrix numerator/hash '+key)
        literal_rows.append(row)
        if q in [4, 5, 6]:
            actions.append(projector_actions(q, C, prior))
    census = [equality_census(q) for q in range(2, 8)]
    import copy
    bad = copy.deepcopy(boundaries); bad[0]['values'][0] = 0.5
    missing = copy.deepcopy(boundaries); missing[0]['keys'].pop()
    duplicate = copy.deepcopy(boundaries); duplicate[0]['keys'][0] = duplicate[0]['keys'][1]
    changed = copy.deepcopy(signs); changed['signs'][0]['coefficients'][0] = '0'
    matrix = [row[:] for row in parts[4][1]]; matrix[0][0] = -1
    controls = [lambda: domain(1), lambda: domain(True), lambda: domain(8), lambda: generic_weights(3),
                lambda: boundary_weights(2, bad), lambda: boundary_weights(2, missing),
                lambda: boundary_weights(2, duplicate), lambda: reconstruct_signs(changed),
                lambda: prior.psd(matrix), lambda: prior.psd([[0, 1], [1, 0]]),
                lambda: positive([1, -1]), lambda: prior.gap(parts[4][0][1], 16, F(100))]
    for callback in controls:
        reject(callback)
    refinements = spectral_refinements()
    refinements['threshold_at_q25_coefficients'] = list(map(str, refinements['threshold_at_q25_coefficients']))
    return {'actual_agent': 'six-reviewer-3', 'role': 'independent mathematical reviewer',
            'infinite_certificate': certificate, 'literal_matrices': literal_rows,
            'projector_column_actions': actions, 'complete_equality_census': census,
            'spectral_refinements': refinements, 'product_forced_grams': product_forced_grams(parts, prior),
            'rejected_controls': len(controls),
            'proof_status': 'Scoped ordinary unformalized all-q audit; complete Newton identity bounds and harmonic/action proof; exact q>=4 upper gap, sharp uniform5/13, exact core gap and controlled-mode threshold25. General H/I open.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--boundaries', type=Path, required=True)
    parser.add_argument('--signs', type=Path, required=True)
    parser.add_argument('--author-results', type=Path, required=True)
    parser.add_argument('--prior-audit', type=Path, default=Path(__file__).parent.parent/'three-petal-audit'/'audit.py')
    parser.add_argument('--write', type=Path)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    inputs = []
    for path, expected in [(args.boundaries, 'a105d39dd77b8cc1aa7264ab282a441aabdbb9752f497766d3fda9eba92dc836'),
                           (args.signs, '9566e6a225c3cd167af00e8c2addd0225c8bafec3074611e00e3c6e9c470fb37'),
                           (args.author_results, '3cc13a0c89e838dec859295809f21cd4a9c63e91fb8573d8f4bc596751f2988c')]:
        raw = path.read_bytes(); need(sha256(raw).hexdigest() == expected, 'public comparison/input hash')
        inputs.append(json.loads(raw))
    result = run(*inputs, load_prior(args.prior_audit))
    raw = (json.dumps(result, sort_keys=True, indent=2)+'\n').encode()
    if args.write:
        args.write.write_bytes(raw)
    if args.check:
        need(result == json.loads(args.check.read_bytes()), 'independent receipt mismatch')
    print(json.dumps({'ok': True, 'sign_records': 33, 'original_matrices': 3,
                      'literal_parameters': [2, 3, 4, 5, 6, 7],
                      'projector_columns_checked': sum(r['checked_columns'] for r in result['projector_column_actions']),
                      'equality_census_parameters': [2, 3, 4, 5, 6, 7],
                      'rejected_controls': result['rejected_controls'], 'expected_sha256': sha256(raw).hexdigest()}, sort_keys=True))


if __name__ == '__main__':
    main()
