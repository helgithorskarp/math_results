"""Exact pendant-only H completion; seed PSD is not required.

See AFFINE_PENDANT_COMPLETION.md for the ordinary all-order proof.  The
constructor stores O(N^2+p) rationals and evaluates entries on demand;
the deliberately bounded dense helper is for finite validation only.
"""
from fractions import Fraction as F
from math import ceil, isqrt


def require(condition, message):
    if not condition:
        raise ValueError(message)


def integer(x):
    return isinstance(x, int) and not isinstance(x, bool)


def geometry(family, center):
    """Validate a nontrivial bit-mask downset and a maximum coordinate."""
    require(isinstance(family, (list, tuple)) and len(family) >= 2,
            "Nontrivial finite family required")
    require(all(integer(a) and a >= 0 for a in family), "Bad set mask")
    require(list(family) == sorted(set(family)) and family[0] == 0,
            "Sorted distinct masks including empty required")
    present = set(family)
    for a in family:
        bits = a
        while bits:
            bit = bits & -bits
            require(a ^ bit in present, "Family is not a downset")
            bits ^= bit
    d = max(family).bit_length()
    require(integer(center) and 0 <= center < d, "Bad center")
    s = max(sum(bool(a >> i & 1) for a in family) for i in range(d))
    S = [a for a in family[1:] if a >> center & 1]
    B = [a for a in family[1:] if not a >> center & 1]
    require(len(S) == s and s >= 1, "Center does not attain maximum star")
    require(len(B) >= s - 1, "Downset injection bound failed")
    return s, S, B


def add_pendants(family, center, count):
    geometry(family, center)
    require(integer(count) and count >= 0, "Nonnegative integer count required")
    d = max(family).bit_length()
    singles = [1 << (d + j) for j in range(count)]
    return sorted(list(family) + singles + [a | (1 << center) for a in singles])


def validate_core(family, core, center):
    n, S, B = geometry(family, center)
    require(n >= 3, "Centered affine lemma requires star at least three")
    old = family[1:]
    m = len(old)
    require(len(core) == m and all(len(row) == m for row in core),
            "Core dimensions differ")
    require(all(integer(x) or isinstance(x, F) for row in core for x in row),
            "Exact integers or Fractions required; no floating input")
    C = [list(map(F, row)) for row in core]
    for i, a in enumerate(old):
        require(C[i][i] == n - 1 and sum(C[i]) == 0,
                "Core diagonal or centering differs")
        require(sum(C[i][j] for j, z in enumerate(old) if z in S) == 0,
                "Core does not kill chosen star")
        for j, z in enumerate(old):
            require(C[i][j] == C[j][i], "Nonsymmetric core")
            if i != j and a & z:
                require(C[i][j] == -1, "Intersection entry differs")
    return C, n, S, B


def centered_seed(family, center):
    """One preliminary pendant centers an affine seed by a disjoint pair tune."""
    s, S, B = geometry(family, center)
    require(s >= 3, "Preprocess star one/two before affine centering")
    old = family[1:]
    ix = {a: i for i, a in enumerate(old)}
    c = 1 << center
    b = len(B)
    singles = [a for a in B if a.bit_count() == 1]
    require(len(singles) >= 2, "Two outside singletons required")
    pair = tuple(singles[:2])
    A = [[F(s - 1) if a == z else F(-bool(a & z)) for z in old] for a in old]
    for z in B:
        A[ix[c]][ix[z]] = A[ix[z]][ix[c]] = F(sum(bool(a & z) for a in S))
    t0 = sum(map(sum, A))
    delta = (s - b - t0) / 2
    q, r = map(ix.get, pair)
    A[q][r] += delta
    A[r][q] += delta
    rows = list(map(sum, A))
    require(sum(rows) == s - b, "Pair tune total differs")
    p = 1 << max(family).bit_length()
    z = p | c
    E = add_pendants(family, center, 1)

    def entry(a, d):
        if a == d:
            return F(s)
        if a & d:
            return F(-1)
        if a == p or d == p:
            v = d if a == p else a
            return -rows[ix[v]] + int(v == c) if v in S else -rows[ix[v]] - 1
        if a == z or d == z:
            return F(1, b)
        ans = A[ix[a]][ix[d]]
        if (a == c and d in B) or (d == c and a in B):
            ans -= F(1, b)
        return ans

    C = [[entry(a, d) for d in E[1:]] for a in E[1:]]
    C, n, _, BB = validate_core(E, C, center)
    R = max(sum(abs(x) for x in row) for row in C)
    require(R <= 2 * len(old) ** 2 + 2, "Uniform seed row bound failed")
    return E, C, dict(initial_s=s, seed_s=n, seed_b=len(BB), row_bound=R,
                      pair=pair, delta=delta, tuned_total=s-b,
                      uniform_further_count=4*len(old)**2+s+5)


def compile_history(family, core, center, count):
    """Closed orthogonal-history entry formula, independent of step recurrence.

    This only constructs affine cores.  PSD follows from the proof when
    count>=ceil(2R+n), or from the sharper block-decay criterion below.
    Construction alone makes no PSD assertion for smaller counts.
    """
    C, n, S, B = validate_core(family, core, center)
    require(integer(count) and count >= 1, "Positive integer count required")
    b = len(B)
    old = family[1:]
    ix = {a: i for i, a in enumerate(old)}
    d = max(family).bit_length()
    singles = [1 << (d+j) for j in range(count)]
    spokes = [a | (1 << center) for a in singles]
    E = sorted(list(family) + singles + spokes)
    present = set(E[1:])
    ai = {a: j for j, a in enumerate(singles)}
    zi = {a: j for j, a in enumerate(spokes)}
    ap = [F(1)] * (count+1)
    bp = [F(1)] * (count+1)
    for j in range(count-1, -1, -1):
        ap[j] = ap[j+1] * (1-F(1, (n+j)*(b+j)))
        bp[j] = bp[j+1] * (1-F(1, b+j))
    nu = n + count

    def frame(a, j, star):
        if bool(a >> center & 1) != star:
            return F(0)
        table = zi if star else ai
        if a in ix or table[a] < j:
            return -F(1, (n if star else b)+j)
        return F(int(table[a] == j))

    planes = []
    for j in range(count):
        ds, db = 1+F(1, n+j), 1+F(1, b+j)
        planes.append((nu/ds, -ap[j+1],
                       (nu+bp[j+1]*(F(n+j, b+j)-1))/db))

    def entry(a, z):
        require(a in present and z in present, "Core vertex differs")
        value = F(0)
        if a in ix and z in ix:
            aa, zz = bool(a >> center & 1), bool(z >> center & 1)
            if aa and zz:
                value = nu*(int(a == z)-F(1, n))
            elif aa != zz:
                value = ap[0]*C[ix[a]][ix[z]]
            else:
                value = bp[0]*C[ix[a]][ix[z]] + (nu-n*bp[0])*(int(a == z)-F(1, b))
        for j, (h11, h12, h22) in enumerate(planes):
            ax, ay = frame(a, j, True), frame(a, j, False)
            zx, zy = frame(z, j, True), frame(z, j, False)
            value += h11*ax*zx + h12*(ax*zy+ay*zx) + h22*ay*zy
        return value

    R = max(sum(abs(x) for x in row) for row in C)
    data = dict(seed_s=n, seed_b=b, row_bound=R, further_pendants=count,
                sufficient_count=ceil(2*R+n), final_s=nu, final_b=b+count,
                alpha_product=ap[0], beta_product=bp[0], planes=planes)
    return E, entry, data


def block_decay_profile(family, core, center):
    """Exact operator norm bounds; centering/geometry are validated first.

    P bounds C_SB by sqrt(||X||_infinity ||X||_1), rounded upward to
    an integer and capped by the full-core row bound. T bounds the
    symmetric C_BB-n(I-J/b), capped by R+n. No eigenvalue estimates
    or positive-semidefinite seed assumption are used.
    """
    C, n, S, B = validate_core(family, core, center)
    ix = {a: i for i, a in enumerate(family[1:])}
    ss, bb = [ix[a] for a in S], [ix[a] for a in B]
    b = len(B)
    R = max(sum(abs(x) for x in row) for row in C)
    row = max(sum(abs(C[i][j]) for j in bb) for i in ss)
    col = max(sum(abs(C[i][j]) for i in ss) for j in bb)
    radicand = row*col
    rounded = isqrt(radicand.numerator//radicand.denominator)
    if F(rounded*rounded) < radicand:
        rounded += 1
    outside = max(sum(abs(C[i][j]-n*int(i == j)+F(n, b))
                      for j in bb) for i in bb)
    return dict(seed_s=n, seed_b=b, row_bound=R,
                cross_row_bound=row, cross_column_bound=col,
                cross_bound=min(R, F(rounded)),
                outside_row_bound=outside, outside_bound=min(R+n, outside),
                row_sufficient_count=ceil(2*R+n))


def block_decay_count(family, core, center):
    """First count satisfying the sufficient scalar test, not an optimal count.

    The test is monotone for all larger counts and is guaranteed by
    ceil(2R+n). Rejection below it does not assert H nonexistence.
    """
    profile = block_decay_profile(family, core, center)
    n, b = profile['seed_s'], profile['seed_b']
    P, T = profile['cross_bound'], profile['outside_bound']
    A = B = F(1)
    for u in range(1, profile['row_sufficient_count']+1):
        A *= 1-F(1, (n+u-1)*(b+u-1))
        B *= 1-F(1, b+u-1)
        determinant = u*(u-B*T)-(A*P)**2
        if u >= 2 and u >= B*T and determinant >= 0:
            return u, dict(profile, sufficient_count=u, alpha_product=A,
                           beta_product=B, determinant=determinant,
                           outside_margin=u-B*T)
    raise ValueError('Proven terminating block-decay criterion failed')


def completion(family, center, total_pendants=None, *, threshold='row'):
    """Rational H entry oracle for an arbitrary nontrivial finite downset.

    None selects the instance-specific proven sufficient count. The 'row'
    default retains the simple norm bound; 'decay' uses the sharper block
    criterion. An explicit smaller count is rejected without any
    nonexistence assertion. No seed certificate on the original family
    is assumed or concluded.
    """
    s, _, _ = geometry(family, center)
    preprocessing = max(0, 3-s)
    D = add_pendants(family, center, preprocessing)
    E0, C0, seed = centered_seed(D, center)
    require(threshold in ('row', 'decay'), 'Unknown sufficient-count criterion')
    if threshold == 'row':
        sufficient = ceil(2*seed['row_bound']+seed['seed_s'])
    else:
        sufficient, decay = block_decay_count(E0, C0, center)
    minimum = preprocessing + 1 + sufficient
    if total_pendants is None:
        total_pendants = minimum
    require(integer(total_pendants) and total_pendants >= minimum,
            "Count below this construction's sufficient threshold")
    u = total_pendants - preprocessing - 1
    E, raw, history = compile_history(E0, C0, center, u)
    n, b = history['final_s'], history['final_b']
    N = len(E)
    newest = 1 << (max(E).bit_length()-1)
    other = next(a for a in E0[1:] if not a >> center & 1 and a.bit_count() == 1)
    pair = (newest, other)
    eps = min(F(1, 2), F(seed['seed_s'], 2*(b+2)))
    present = set(E)

    def matrix_entry(a, z):
        require(a in present and z in present, "H vertex differs")
        if a == z == 0:
            return F(1+2*eps-n, N-n)
        if a == 0 or z == 0:
            return F(1-eps*int((z if a == 0 else a) in pair), N-n)
        trade = int((a, z) == pair or (z, a) == pair)
        return F(1+raw(a, z)+eps*trade-n*int(a == z), N-n)

    data = dict(original_N=len(family), original_s=s, preprocessing=preprocessing,
                total_pendants=total_pendants, sufficient_total=minimum,
                N=N, s=n, epsilon=eps, repair_pair=pair, seed=seed,
                history=history, raw_entry=raw)
    if threshold == 'decay':
        data['block_decay'] = decay
    require(N == len(family)+2*total_pendants and n == s+total_pendants,
            "Completion counts differ")
    return E, matrix_entry, data


def dense_entries(family, entry, limit=128):
    require(integer(limit) and limit >= 1 and len(family) <= limit,
            "Dense validation limit exceeded; use entry oracle")
    return [[entry(a, z) for z in family] for a in family]
