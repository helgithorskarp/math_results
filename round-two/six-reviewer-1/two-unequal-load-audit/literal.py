"""Independent original-set Fraction Gram, full frame and rank audit.

The fraction-free PSD congruence is adapted from this reviewer's published
8927 checker. All family/load/vector construction here is new. Author helpers
are never imported. Families are sorted by cardinality and bit mask.
"""
from fractions import Fraction as F
from hashlib import sha256
from math import lcm
import json
from itertools import product

CHECKS = 0


class Failure(ValueError):
    pass


def need(ok, label):
    global CHECKS
    if not ok:
        raise Failure(label)
    CHECKS += 1


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), F())


def image(a, x):
    return [dot(row, x) for row in a]


def lin(*terms):
    return [sum((c * v[i] for c, v in terms), F()) for i in range(len(terms[0][1]))]


def unit(n, k):
    return [F(i == k) for i in range(n)]


def psd(a):
    """Pivoted fraction-free positive congruence, requiring a zero full residual."""
    n = len(a)
    need(n > 0 and all(len(row) == n for row in a), 'square PSD matrix')
    need(all(a[i][j] == a[j][i] for i in range(n) for j in range(n)), 'symmetric PSD matrix')
    denominator = 1
    for row in a:
        for x in row:
            denominator = lcm(denominator, F(x).denominator)
    b = [[int(x * denominator) for x in row] for row in a]
    rank, previous = 0, 1
    while b:
        size = len(b)
        need(all(b[i][i] >= 0 for i in range(size)), 'nonnegative congruence diagonal')
        k = max(range(size), key=lambda i: b[i][i])
        pivot = b[k][k]
        if not pivot:
            need(all(x == 0 for row in b for x in row), 'complete zero PSD residual')
            break
        idx = [i for i in range(size) if i != k]
        new = [[0] * len(idx) for _ in idx]
        for ii, i in enumerate(idx):
            for jj in range(ii, len(idx)):
                j = idx[jj]
                value, rem = divmod(pivot * b[i][j] - b[i][k] * b[k][j], previous)
                need(rem == 0, 'exact Bareiss congruence division')
                new[ii][jj] = new[jj][ii] = value
        rank += 1
        previous, b = pivot, new
    return rank


def kernel(a):
    a = [[F(x) for x in row] for row in a]
    width = len(a[0])
    pivots, r = [], 0
    for j in range(width):
        k = next((i for i in range(r, len(a)) if a[i][j]), None)
        if k is None:
            continue
        a[r], a[k] = a[k], a[r]
        a[r] = [x / a[r][j] for x in a[r]]
        for i in range(len(a)):
            if i != r:
                a[i] = [x - a[i][j] * y for x, y in zip(a[i], a[r])]
        pivots.append(j)
        r += 1
        if r == len(a):
            break
    out = []
    for j in range(width):
        if j in pivots:
            continue
        v = unit(width, j)
        for i, p in enumerate(pivots):
            v[p] = -a[i][j]
        out.append(v)
    return out


def lift(c):
    rows = [sum(row) for row in c]
    return [[sum(rows), *[-x for x in rows]], *[[-rows[i], *row] for i, row in enumerate(c)]]


def gram(base, coefficients, residual=None):
    imgs = [image(base, v) for v in coefficients]
    out = [[dot(v, img) for img in imgs] for v in coefficients]
    if residual is not None:
        out = [[x + residual[i][j] for j, x in enumerate(row)] for i, row in enumerate(out)]
    return out


def fingerprint(a):
    return sha256(json.dumps([[str(x) for x in row] for row in a], separators=(',', ':')).encode()).hexdigest()


def build(n, D, t, positions):
    need(type(n) is int and 2 <= n <= 6, 'literal cube guard')
    need(type(D) is int and type(t) is int and D > t >= 1, 'strict positive integer load domain')
    need(len(positions) == 2 and len(set(positions)) == 2 and
         all(type(x) is int and 0 <= x < n for x in positions), 'distinct literal marks')
    q, m = 1 << (n - 1), D + t
    N, s = 2 * q + 2 * m, q + D
    need(N <= 80, 'fixed original-index size guard')
    w, old = F(s - 1), list(range(1, 2 * q))
    oldn = len(old)
    oldC = [[F((q + D) * int(a == b) + (q - D) * int(a ^ b == 2 * q - 1) - 1)
             for b in old] for a in old]
    need(psd(oldC) == oldn, 'old cube PD')
    H = [[-F(bool(a & (1 << p))) for a in old] for p in positions]
    Himages = [image(oldC, x) for x in H]
    need([[dot(x, y) for y in Himages] for x in H] == [[q * D, 0], [0, q * D]], 'marked old Gram')
    labels = [0] * D + [1] * t
    coefficients = [unit(oldn, i) for i in range(oldn)]
    coefficients += [lin((F(1, D), H[k])) for k in labels]
    base = gram(oldC, coefficients)
    for i in range(m):
        for j in range(m):
            if labels[i] == labels[j]:
                base[oldn + i][oldn + j] += (q + D) * (int(i == j) - F(1, D))
    width = oldn + m
    S = [unit(width, oldn + j) for j in range(m)]
    K = [F(1)] * width
    cs = [F(m * (w - load - m - 1), m + 1) / ((m - 1) * w - 1 + load)
          for load in [D] * D + [t] * t]
    Csum = [F(0)] * oldn + cs
    U = [lin((-F(1, m + 1), K), (cs[j], S[j]), (-F(1, m), Csum)) for j in range(m)]
    eta = [w - dot(v, image(base, v)) for v in U]
    E = sum(eta)
    zeta = [F(m, m - 2) * (e - E / (m * (m - 1))) for e in eta]
    W = [[zeta[i] * int(i == j) - (zeta[i] + zeta[j]) / m + sum(zeta) / m ** 2
          for j in range(m)] for i in range(m)]
    need(all(x > 0 for x in zeta), 'positive W weights')
    need([W[i][i] for i in range(m)] == eta and all(sum(row) == 0 for row in W), 'all W diagonal/row identities')
    need(psd(W) == m - 1, 'W exact rank')
    canonical = [0, *old]
    seedco = [unit(width, i) for i in range(oldn)]
    rawco = [unit(width, i) for i in range(oldn)]
    singleton_indices, spoke_indices = [], []
    for j, label in enumerate(labels):
        fresh = 1 << (n + j)
        canonical.extend([fresh | (1 << positions[label]), fresh])  # spoke BEFORE leaf
        spoke_indices.append(len(seedco))
        singleton_indices.append(len(seedco) + 1)
        seedco.extend([S[j], U[j]])
        rawco.extend([S[j], lin((-1 / w, S[j]))])
    residual = [[F(0)] * (N - 1) for _ in range(N - 1)]
    rawresidual = [[F(0)] * (N - 1) for _ in range(N - 1)]
    for i, row in enumerate(W):
        for j, value in enumerate(row):
            residual[singleton_indices[i]][singleton_indices[j]] = value
        rawresidual[singleton_indices[i]][singleton_indices[i]] = w - 1 / w
    seed, raw = gram(base, seedco, residual), gram(base, rawco, rawresidual)
    B0 = w + m * (q + D) - D ** 2 - t ** 2 - 2 * m
    need(sum(map(sum, seed)) == B0 / (m + 1) ** 2, 'actual seed empty energy')
    rawB = w + (1 - 1 / w) ** 2 * (m * (q + D) - D ** 2 - t ** 2) - 2 * m * (1 - 1 / w) + m * (w - 1 / w)
    need(sum(map(sum, raw)) == rawB and rawB >= 0, 'actual raw empty energy')
    return {'n': n, 'q': q, 'D': D, 't': t, 'm': m, 'N': N, 's': s, 'w': w,
            'canonical': canonical, 'seed': seed, 'raw': raw, 'oldC': oldC,
            'H': H, 'Sindices': spoke_indices, 'Uindices': singleton_indices,
            'c': [cs[0], cs[-1]], 'zeta': [zeta[0], zeta[-1]],
            'B0': B0, 'rawB': rawB, 'raw_trace': (N - 1) * w + rawB}


def frame_audit(d):
    q, D, t, m, N = (d[k] for k in ('q', 'D', 't', 'm', 'N'))
    c, oldC = d['seed'], d['oldC']
    size, oldn = N - 1, 2 * q - 1
    G = [F(i < oldn) for i in range(size)]
    h0 = lin((-F(1, 2), G), (-F(1, 2), unit(size, oldn - 1)))
    gp = lin((1, G), (1, h0))
    H = [h + [F(0)] * (size - oldn) for h in d['H']]
    A = [lin((1, h), (-1, h0)) for h in H]
    for v, expect in [(gp, lin((q + 1, gp), (q - 1, h0))),
                      (h0, lin((D, gp), (D, h0))),
                      *[(v, lin((2 * D, v))) for v in A]]:
        need(image(oldC, v[:oldn]) == expect[:oldn], 'original old frame action')
    S = [unit(size, i) for i in d['Sindices']]
    U = [unit(size, i) for i in d['Uindices']]
    L2 = lin(*[(F(1, t), v) for v in S[D:]])
    Z = lin((1, L2), (-F(1, D), H[1]))
    K = lin((1, G), *[(1, v) for v in S])
    ch, cl = d['c']
    y = lin((F(t, m) * ch / D, H[0]), (-F(t, m) * cl, L2))
    Ws = lin(*[(F(1, D), v) for v in U[:D]], (F(1, m + 1), K), (-1, y))
    coords = [gp, h0, *A, Z, Ws]
    sectors = []
    for start, load, ci, zi in [(0, D, ch, d['zeta'][0]), (D, t, cl, d['zeta'][1])]:
        ts = [lin((1, S[j]), (-1, S[start])) for j in range(start + 1, start + load)]
        ww = [lin((1, U[j]), (-1, U[start]), (-ci, ts[j - start - 1]))
              for j in range(start + 1, start + load)]
        offset = len(coords)
        coords.extend(ts + ww)
        sectors.append((offset, load - 1, ci, zi))
    imgs = [image(c, v) for v in coords]
    metric = [[dot(v, img) for img in imgs] for v in coords]
    expected = [[F(0)] * len(coords) for _ in coords]
    expected[0][0], expected[1][1] = q - 1, D
    for i in (2, 3):
        for j in (2, 3):
            expected[i][j] = D * (q * int(i == j) - 1)
    expected[4][4] = (q + D) * (F(1, t) - F(1, D))
    expected[5][5] = F(t, D * m ** 2) * (t * d['zeta'][0] + D * d['zeta'][1])
    for offset, dim, ci, zi in sectors:
        for i in range(dim):
            for j in range(dim):
                expected[offset + i][offset + j] = (q + D) * (1 + int(i == j))
                expected[offset + dim + i][offset + dim + j] = zi * (1 + int(i == j))
    need(metric == expected, 'all changed-sector Gram entries')
    count = (6 if q >= 4 else 5) + 2 * (D - 1) + 2 * (t - 1)
    need(psd(metric) == count, 'changed rank including dependent q2 generators')
    # Compute literal FULL frame from the old matrix and actual empty vector.
    full = [[dot(x, y) + sum(x) * sum(y) for y in imgs] for x in imgs]
    predicted = [[F(0)] * len(coords) for _ in coords]
    update_images = [image(c, v) for v in [H[0], L2, K, lin((1, y), (1, Ws))]]
    products = [[dot(v, x) for x in update_images] for v in coords[:6]]
    weights = [F(1, D), F(t), F(1, m + 1), F(D * m, t)]
    for i in range(6):
        for j in range(6):
            predicted[i][j] = dot(imgs[i][:oldn], imgs[j][:oldn]) + sum(weights[k] * products[i][k] * products[j][k] for k in range(4))
    for offset, dim, ci, zi in sectors:
        for i in range(dim):
            for j in range(dim):
                b = 1 + int(i == j)
                predicted[offset + i][offset + j] = (q + D) ** 2 * (1 + ci ** 2) * b
                predicted[offset + i][offset + dim + j] = predicted[offset + dim + j][offset + i] = ci * (q + D) * zi * b
                predicted[offset + dim + i][offset + dim + j] = zi ** 2 * b
    need(full == predicted, 'all complete changed-frame entries including actual empty')
    need(any(sum(x) for x in imgs), 'actual empty contribution is nonzero')
    omitted = [[dot(x, y) for y in imgs] for x in imgs]
    need(omitted != predicted, 'omitting empty frame detected')
    mask = 2 * q - 1
    pairs = [(a, mask ^ a) for a in range(1, mask) if a < (mask ^ a)]
    plus = [lin((1, unit(size, a - 1)), (1, unit(size, b - 1))) for a, b in pairs]
    highs = [lin((1, v), (-1, plus[0])) for v in plus[1:]]
    minus = [lin((1, unit(size, a - 1)), (-1, unit(size, b - 1))) for a, b in pairs]
    constraints = [[dot(h, image(c, v)) for v in minus] for h in H]
    lows = [lin(*[(co, v) for co, v in zip(row, minus)]) for row in kernel(constraints)]
    for label, rows, eigen, number in [('high', highs, 2 * q, q - 2), ('low', lows, 2 * D, max(0, q - 3))]:
        need(len(rows) == number, 'complete untouched ' + label + ' count')
        for v in rows:
            cv = image(c, v)
            need(image(c, lin((1, cv), (sum(cv), [F(1)] * size))) == lin((eigen, cv)), 'full untouched ' + label + ' action')
            need(all(dot(x, cv) == 0 for x in coords), 'changed/untouched orthogonality')
    need(count + len(highs) + len(lows) == N - 3, 'complete full frame dimension')
    return {'changed_dimension': count, 'untouched_high': len(highs), 'untouched_low': len(lows),
            'frame_dimension': N - 3, 'checked_changed_frame_entries': len(coords) ** 2}


def validate(family, Q, s, lower_rank, margin):
    N = len(family)
    M = [[(Q[i][j] + 1 - s * int(i == j)) / (N - s) for j in range(N)] for i in range(N)]
    need(family[0] == 0 and len(set(family)) == N, 'actual empty and distinct family')
    need(all(sum(row) == 1 for row in M), 'all exact row sums')
    need(all(M[i][j] == M[j][i] and (not (a & b) or M[i][j] == 0)
             for i, a in enumerate(family) for j, b in enumerate(family)), 'all original set support/symmetry')
    need(psd([[x + 1 for x in row] for row in Q]) == lower_rank, 'full lower PSD rank')
    if margin is not None:
        need(psd([[(N - margin) * (int(i == j) - F(1, N)) - Q[i][j] for j in range(N)]
                  for i in range(N)]) == N - 1, 'full scaled upper cap and rank')
    index = sorted(range(N), key=lambda i: (family[i].bit_count(), family[i]))
    return {'lower_rank': lower_rank, 'upper_rank': N - 1 if margin is not None else None,
            'scaled_gap': str(margin), 'matrix_sha256': fingerprint([[M[i][j] for j in index] for i in index])}


def one(n, D, t, marks):
    d = build(n, D, t, marks)
    N, s = d['N'], d['s']
    frame = frame_audit(d)
    family, seed, raw, trace = d['canonical'], lift(d['seed']), lift(d['raw']), d['raw_trace']
    seedresult = validate(family, seed, s, N - 2, F(1))
    rawresult = validate(family, raw, s, N - 1, None)
    need(sum(raw[i][i] for i in range(N)) == trace, 'full raw trace including empty')
    eps = F(1, 2) / (1 + trace)
    loss = trace - N + 1
    epsnew = F(1, 2) / loss
    need(loss >= (d['w'] - 1) * (N - 1) >= 18 and 0 < eps < epsnew < 1, 'larger rational repair domain')
    beta = 1 - eps * loss
    mixed = [[(1 - eps) * seed[i][j] + eps * raw[i][j] for j in range(N)] for i in range(N)]
    improved = [[(1 - epsnew) * seed[i][j] + epsnew * raw[i][j] for j in range(N)] for i in range(N)]
    mixedresult = validate(family, mixed, s, N - 1, beta)
    newresult = validate(family, improved, s, N - 1, F(1, 2))
    need(F(1, 2) < beta < 1, 'published-matrix stronger trace gap')
    heavy = [int(bool(a & (1 << marks[0]))) for a in family]
    need(sum(heavy) == s and image([[x + 1 for x in row] for row in mixed], [F(x) - F(s, N) for x in heavy]) == [0] * N, 'forced heavy star lower kernel')
    originalset = set(family)
    for a in family:
        b = a
        while True:
            need(b in originalset, 'all literal subsets present')
            if not b:
                break
            b = (b - 1) & a
    bad = [row[:] for row in mixed]
    i, j = d['Uindices'][0] + 1, d['Sindices'][0] + 1
    bad[i][j] += 1
    bad[j][i] += 1
    try:
        validate(family, bad, s, N - 1, F(1, 2))
    except Failure:
        pass
    else:
        raise Failure('altered mandatory singleton-spoke entry accepted')
    bad = [row[:] for row in mixed]
    bad[0][0] += 1
    try:
        validate(family, bad, s, N - 1, F(1, 2))
    except Failure:
        pass
    else:
        raise Failure('altered empty loop accepted')
    # Transport this independently relocated pair of marks to the author's
    # named pair (0,1), then compare in the author's leaf-before-spoke order.
    relabel = {marks[0]: 0, marks[1]: 1}
    remaining = [j for j in range(n) if j not in marks]
    relabel.update(zip(remaining, range(2, n)))
    def transport(a):
        return sum(1 << (relabel.get(i, i)) for i in range(a.bit_length()) if a & (1 << i))
    transported = [transport(a) for a in family]
    authorfamily = [0, *range(1, 1 << n)]
    for j in range(D + t):
        fresh = 1 << (n + j)
        authorfamily.extend([fresh, fresh | (1 << int(j >= D))])
    order = [transported.index(a) for a in authorfamily]
    def author_hash(Q):
        M = [[(Q[i][j] + 1 - s * int(i == j)) / (N - s) for j in range(N)] for i in range(N)]
        return fingerprint([[M[i][j] for j in order] for i in order])
    return {'n': n, 'D': D, 't': t, 'marks': marks, 'N': N, 's': s, 'frame': frame,
            'seed': seedresult, 'raw': rawresult, 'published_mixture': mixedresult,
            'improved_mixture': newresult, 'raw_trace': str(trace), 'epsilon': str(eps),
            'epsilon_improved': str(epsnew), 'published_gap_beta': str(beta),
            'author_order_seed_sha256': author_hash(seed),
            'author_order_mixed_sha256': author_hash(mixed)}


def run():
    global CHECKS
    CHECKS = 0
    rows = [one(*args) for args in [(2, 2, 1, [1, 0]), (2, 8, 7, [0, 1]),
                                  (3, 3, 2, [2, 0]), (3, 8, 7, [1, 2]),
                                  (4, 5, 1, [3, 1]), (6, 2, 1, [5, 0])]]
    try:
        psd([[F(0), F(1)], [F(1), F(0)]])
    except Failure:
        pass
    else:
        raise Failure('indefinite zero-diagonal PSD residual accepted')
    rejected = 0
    for args in [(2, 1, 1, [0, 1]), (2, 2, 0, [0, 1]), (2, 2, 1, [0, 0]),
                 (2, True, 1, [0, 1]), (2, 2, 1, [0, 2])]:
        try:
            build(*args)
        except Failure:
            rejected += 1
        else:
            raise Failure('invalid literal domain accepted')
    return {'records': rows, 'exact_checks': CHECKS, 'literal_instances': len(rows),
            'full_frame_entries': sum(row['frame']['checked_changed_frame_entries'] for row in rows),
            'damage_controls': 3 * len(rows) + 1, 'invalid_domain_controls': rejected}


def products():
    """Small literal tensor controls; unbounded scope uses the written spectral proof."""
    start_checks = CHECKS
    rows = []
    for pair in [(2, 2), (2, 3)]:
        factors = [build(2, D, 1, [0, 1]) for D in pair]
        Ns, ss, Ms = [], [], []
        beta = []
        for d in factors:
            N, s = d['N'], d['s']
            seed, raw = lift(d['seed']), lift(d['raw'])
            trace = d['raw_trace']
            eps = F(1, 2) / (1 + trace)
            Q = [[(1 - eps) * seed[i][j] + eps * raw[i][j] for j in range(N)] for i in range(N)]
            Ms.append([[(Q[i][j] + 1 - s * int(i == j)) / (N - s) for j in range(N)] for i in range(N)])
            Ns.append(N)
            ss.append(s)
            beta.append(1 - eps * (trace - N + 1))
        N = Ns[0] * Ns[1]
        need(N <= 120, 'fixed product order guard')
        rho = max(F(s, n) for s, n in zip(ss, Ns))
        S = rho * N
        eligible = [i for i in range(2) if F(ss[i], Ns[i]) == rho]
        idx = list(product(*[range(n) for n in Ns]))
        M = [[Ms[0][i[0]][j[0]] * Ms[1][i[1]][j[1]] for j in idx] for i in idx]
        need(all(sum(row) == 1 for row in M), 'literal product row sums')
        fams = [d['canonical'] for d in factors]
        need(all(not any(fams[k][i[k]] & fams[k][j[k]] for k in range(2)) or M[a][b] == 0
                 for a, i in enumerate(idx) for b, j in enumerate(idx)), 'literal product support')
        lower = [[(N - S) * M[i][j] + S * int(i == j) for j in range(N)] for i in range(N)]
        need(psd(lower) == N - len(eligible), 'literal product greatest lower rank')
        a = max(max(F(s, n - s), 1 - gap / (n - s)) for s, n, gap in zip(ss, Ns, beta))
        gap = (N - S) * (1 - a)
        upper = [[(N - S) * (int(i == j) - M[i][j]) - gap * (int(i == j) - F(1, N))
                  for j in range(N)] for i in range(N)]
        # A proved non-strict gap can attain zero on a nonconstant direction.
        need(psd(upper) >= 0 and gap > 0, 'literal product quantified upper cap')
        for k in eligible:
            h = [F(bool(fams[k][i[k]] & 1)) - rho for i in idx]
            need(image(lower, h) == [0] * N, 'literal eligible heavy-cylinder kernel')
        rows.append({'loads': list(pair), 'N': N, 's': str(S), 'eligible': eligible,
                     'lower_rank': N - len(eligible), 'upper_rank': N - 1,
                     'scaled_gap': str(gap), 'matrix_sha256': fingerprint(M)})
    return {'records': rows, 'exact_checks': CHECKS - start_checks,
            'scope': 'two finite tensor controls; generic spectral argument remains ordinary mathematics'}
