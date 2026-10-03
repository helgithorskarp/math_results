"""Exact original star-only near-cube face for the two rational certificates.

six-downset-2, researcher. The decoder, original lift, and harmonic formulas
are credited to published9365/9639. Here the saturated complement classes
force every incident proper nonempty coupling to vanish. No centering,
entrywise signs, strict deficit, or artificial parameter bounds are imposed.
"""
from fractions import Fraction as Q
from math import comb


def require(ok, message):
    if not ok:
        raise ValueError(message)


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def specification(n=12, active=(3, 4, 5)):
    require(type(n) is int and n >= 6 and n % 2 == 0, 'Even near-cube order')
    require(tuple(sorted(set(active))) == active and
            all(type(a) is int and 2 <= a < n//2 for a in active),
            'Distinct increasing noncentral active classes')
    r, N, s = n-2, 2**n-n-1, 2**(n-1)-n
    middle = n//2
    endpoints = set(active) | {n-a for a in active} | {middle}
    proper = [(a, b) for a in range(2, r+1) for b in range(a, r+1)
              if a+b < n and a in endpoints and b in endpoints]
    saturated = [a for a in range(2, middle) if a not in active]
    return dict(n=n, r=r, N=N, s=s, h=N-s, gap=N-2*s,
                active=list(active), middle=middle, proper=proper,
                saturated=saturated, endpoints=sorted(endpoints),
                names=['d'+str(a) for a in (*active, middle)] +
                      ['t'+str(a)+'_'+str(b) for a, b in proper],
                saturated_pairs=sum(comb(n, a) for a in saturated))


def table(spec, values):
    require(len(values) == len(spec['names']) and all(type(v) is Q for v in values),
            'Full exact real-affine rational coordinates')
    n, r, s = spec['n'], spec['r'], spec['s']
    B = [[Q(0) for _ in range(r+1)] for _ in range(r+1)]
    deficits = dict(zip([*spec['active'], spec['middle']], values))
    for a in range(2, n//2+1):
        B[a][n-a] = B[n-a][a] = s-deficits.get(a, Q(0))
    offset = len(deficits)
    for (a, b), v in zip(spec['proper'], values[offset:]):
        B[a][b] = B[b][a] = v
    for a in range(2, r+1):
        B[a][1] = B[1][a] = Q((n-a)*s-
            sum(b*B[a][b]*choose(n-a, b) for b in range(2, r+1)), n-a)
    B[1][1] = Q((n-1)*s-
            sum(b*B[1][b]*choose(n-1, b) for b in range(2, r+1)), n-1)
    check_table(spec, B)
    return B


def check_table(spec, B):
    n, r, s = spec['n'], spec['r'], spec['s']
    require(len(B) == r+1 and all(len(row) == r+1 for row in B), 'Shape')
    require(all(type(v) is Q for row in B for v in row), 'Exact rational entries')
    require(all(B[a][b] == B[b][a] for a in range(r+1) for b in range(r+1)), 'Symmetry')
    for a in range(1, r+1):
        require(sum(b*B[a][b]*choose(n-a, b) for b in range(1, r+1)) == (n-a)*s,
                'Every point-star equation')
        for b in range(1, r+1):
            if a+b > n or (a+b < n and
                (a in spec['saturated'] or n-a in spec['saturated'] or
                 b in spec['saturated'] or n-b in spec['saturated'])):
                require(B[a][b] == 0, 'Unsupported or saturated incident entry')


def empty_entries(spec, B):
    """Actual original L[empty,a] and L[empty,empty], without dense matrices."""
    n, r, N, s = spec['n'], spec['r'], spec['N'], spec['s']
    sums = [Q(s-(N-1)) + sum(B[a][b]*choose(n-a, b) for b in range(1, r+1))
            for a in range(1, r+1)]
    rows = [1-v for v in sums]
    loop = 1+sum(comb(n, a)*v for a, v in enumerate(sums, 1))
    require(loop+sum(comb(n, a)*v for a, v in enumerate(rows, 1)) == N,
            'Actual empty row sum')
    return dict(loop=loop, row=rows, core_row_sum=sums)


def sectors(spec, B):
    n, r, N, s = spec['n'], spec['r'], spec['N'], spec['s']
    out = []
    for j in range(n//2+1):
        aa = list(range(max(1, j), min(r, n-j)+1))
        g = [comb(n-2*j, a-j) for a in aa]
        K = [[Q(s*int(a == b)-int(j == 0)*comb(n, b)) +
              (-1)**j*B[a][b]*choose(n-a-j, b-j) for b in aa] for a in aa]
        U = [[Q(N*int(a == b)-int(j == 0)*comb(n, b))-K[i][k]
              for k, b in enumerate(aa)] for i, a in enumerate(aa)]
        lower = [[g[i]*v for v in row] for i, row in enumerate(K)]
        upper = [[g[i]*v for v in row] for i, row in enumerate(U)]
        require(all(M[i][k] == M[k][i] for M in (lower, upper)
                    for i in range(len(aa)) for k in range(len(aa))), 'Physical symmetry')
        multiplicity = comb(n, j)-(comb(n, j-1) if j else 0)
        out.append(dict(j=j, layers=aa, gram=g, K=K, U=U,
                        lower=lower, upper=upper, multiplicity=multiplicity))
    require(sum(len(b['layers'])*b['multiplicity'] for b in out) == N-1,
            'Every original nonempty direction included')
    return out


def lower_keep(spec, block):
    """Delete pivot coordinates of explicitly verified constant lower kernels.

    Principal reduction is reversible because the omitted coordinate images
    are linear combinations of the retained coordinates modulo these kernels.
    This is not a specified full-space eigenvalue-floor normalization.
    """
    aa, j, K = block['layers'], block['j'], block['K']
    kernels = []
    if j == 0:
        kernels.append([Q(a) for a in aa])
    elif j == 1:
        kernels.append([Q(1) for _ in aa])
    for a in spec['saturated']:
        if a in aa and spec['n']-a in aa:
            kernels.append([Q(int(b == a)-(-1)**j*int(b == spec['n']-a)) for b in aa])
    for v in kernels:
        require(all(sum(K[i][k]*v[k] for k in range(len(aa))) == 0
                    for i in range(len(aa))), 'Every removed kernel is exact')
    rows = [v[:] for v in kernels]
    pivots, position = [], 0
    for c in range(len(aa)):
        hit = next((i for i in range(position, len(rows)) if rows[i][c]), None)
        if hit is None:
            continue
        rows[position], rows[hit] = rows[hit], rows[position]
        p = rows[position][c]
        rows[position] = [v/p for v in rows[position]]
        for i in range(len(rows)):
            if i != position:
                f = rows[i][c]
                rows[i] = [v-f*w for v, w in zip(rows[i], rows[position])]
        pivots.append(c)
        position += 1
    require(len(pivots) == len(kernels), 'All explicitly known kernels independent')
    return [i for i in range(len(aa)) if i not in pivots], kernels


def affine_basis(spec):
    zero = [Q(0)]*len(spec['names'])
    base = table(spec, zero)
    directions = []
    for k in range(len(zero)):
        unit = zero[:]
        unit[k] = Q(1)
        B = table(spec, unit)
        directions.append([[B[i][j]-base[i][j] for j in range(len(B))]
                           for i in range(len(B))])
    return base, directions
