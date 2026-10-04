"""Full original downset model for bounded literal validation.

The mathematical reduction applies to all finite nontrivial downsets.
Literal construction here is guarded at n<=6; n28 uses exact counts and a credited seed,
never an enormous generated original matrix.
"""
from fractions import Fraction as Q
from math import comb
from linear import identity, multiply, require, transpose, zeros


def parameters(n):
    require(type(n) is int and n >= 4, 'Integer near-cube domain n>=4')
    N, s = 2**n-n-1, 2**(n-1)-n
    return N, s, N-s, s-1


def literal(n, saturated=()):
    parameters(n)
    require(n <= 6, 'Literal original matrix guard n<=6')
    higher = [b for b in range(1 << n) if 2 <= b.bit_count() <= n-2]
    members = [0]+[1 << i for i in range(n)]+higher
    N, s, h, k = parameters(n)
    require(len(members) == N and set(members) == {b for b in range(1 << n) if b.bit_count() <= n-2}, 'Entire original membership')
    data = downset(n, members, saturated)
    require((data['N'],data['s'],data['h'],data['k']) == (N,s,h,k), 'Literal near-cube parameters')
    data['name'] = 'near_cube'
    return data


def downset(n, members, saturated=()):
    require(type(n) is int and 2 <= n <= 6, 'Literal downset guard 2<=n<=6')
    full = (1 << n)-1
    require(len(members) == len(set(members)) and all(type(a) is int and 0 <= a <= full for a in members), 'Literal distinct subset vertices')
    universe = set(members)
    require(0 in universe and all((1 << i) in universe for i in range(n)), 'Actual empty and every active singleton')
    require(all((a ^ (1 << i)) in universe for a in members for i in range(n) if a & (1 << i)), 'Original downward closure')
    stars = [sum(bool(a & (1 << i)) for a in members) for i in range(n)]
    require(max(stars) >= 2, 'Maximum-star size at least two')
    s = max(stars)
    maxpoints = [i for i, size in enumerate(stars) if size == s]
    pivot_singletons = [1 << i for i in maxpoints]
    higher = sorted(universe-{0}-set(pivot_singletons))
    members = [0]+pivot_singletons+higher
    N = len(members)
    h, k = N-s, s-1
    sat = set()
    for pair in saturated:
        require(len(pair) == 2, 'Saturation pair shape')
        a, b = sorted(pair)
        require(a in higher and b in higher and not (a & b) and (a | b) == full,
                'Whole-ground complementary residual pair')
        require((a, b) not in sat, 'Distinct saturation pairs')
        sat.add((a, b))
    endpoints = {a for pair in sat for a in pair}
    remaining = [a for a in higher if a not in endpoints]
    edges = [(a, b) for i, a in enumerate(remaining) for b in remaining[i+1:] if not (a & b)]
    R = [[Q(bool(b & (1 << i))) for i in maxpoints] for b in higher]
    A = [[Q(sum(bool(b & (1 << i)) for i in maxpoints)-1) for b in higher]]+[[Q(-bool(b & (1 << i))) for b in higher] for i in maxpoints]+identity(len(higher))
    return dict(name='downset', n=n, p=len(maxpoints), maxpoints=maxpoints, star_sizes=stars,
                N=N, s=s, h=h, k=k, members=members, residual=higher,
                saturated=sorted(sat), remaining=remaining, edges=edges, R=R, A=A)


def cycle(n):
    require(type(n) is int and 4 <= n <= 6, 'Literal cycle guard 4<=n<=6')
    members = [0]+[1 << i for i in range(n)]+[(1 << i)|(1 << ((i+1) % n)) for i in range(n)]
    data = downset(n, members)
    require(data['p'] == n, 'Cycle is regular')
    data['name'] = 'cycle'
    return data


def path(saturated=()):
    data = downset(3, [0, 1, 2, 4, 3, 6], saturated)
    data['name'] = 'nonregular_path'
    require(data['maxpoints'] == [1] and data['star_sizes'] == [2, 3, 2], 'Nonregular literal star sizes')
    return data


def build_T(data, values):
    require(len(values) == len(data['edges']) and all(type(v) is Q for v in values),
            'All individual exact rational free coordinates')
    qs, k = data['residual'], data['k']
    T = [[Q(k if a == b else -1) for b in qs] for a in qs]
    pos = {b: i for i, b in enumerate(qs)}
    for (a, b), value in zip(data['edges'], values):
        T[pos[a]][pos[b]] = T[pos[b]][pos[a]] = value
    for a, b in data['saturated']:
        T[pos[a]][pos[b]] = T[pos[b]][pos[a]] = Q(k)
    validate_T(data, T)
    return T


def validate_T(data, T):
    qs, k = data['residual'], data['k']
    require(len(T) == len(qs) and all(len(row) == len(qs) for row in T), 'Entire T shape')
    require(all(type(v) is Q for row in T for v in row), 'Exact T entries')
    require(T == transpose(T), 'T symmetry')
    for i, a in enumerate(qs):
        for j, b in enumerate(qs):
            if a == b:
                require(T[i][j] == k, 'T fixed diagonal')
            elif a & b:
                require(T[i][j] == -1, 'T fixed intersection entry')
    for a, b in data['saturated']:
        i, j = qs.index(a), qs.index(b)
        require(T[i] == T[j], 'Entire saturated columns coincide')
        require(all(T[i][z] == (k if c in (a, b) else -1) for z, c in enumerate(qs)),
                'All saturated column entries')


def original(data, T):
    validate_T(data, T)
    A, s, h = data['A'], data['s'], data['h']
    lift = multiply(multiply(A, T), transpose(A))
    L = [[Q(1)+v for v in row] for row in lift]
    M = [[(v-s*(i == j))/h for j, v in enumerate(row)] for i, row in enumerate(L)]
    return L, M


def original_equations(data, M):
    members, n, N, s, h = data['members'], data['n'], data['N'], data['s'], data['h']
    require(len(M) == N and all(len(row) == N for row in M), 'Entire original matrix shape')
    require(all(type(v) is Q for row in M for v in row), 'Original exact entries')
    require(M == transpose(M), 'Original symmetry')
    for i, a in enumerate(members):
        require(sum(M[i]) == 1, 'Original row-one equation including empty')
        for j, b in enumerate(members):
            if a & b:
                require(M[i][j] == 0, 'All original intersecting support')
        for point in data['maxpoints']:
            action = sum(M[i][j] for j, b in enumerate(members) if b & (1 << point))
            require(action == Q(s, h)*(not bool(a & (1 << point))), 'Individual original point-star action')
        for a1, a2 in data['saturated']:
            x, y = members.index(a1), members.index(a2)
            require(M[i][x]-M[i][y] == Q(s, h)*((i == y)-(i == x)), 'Original saturated pair kernel action')


def counts(n, lo, hi):
    parameters(n)
    require(type(lo) is int and type(hi) is int and 2 <= lo <= hi <= n-2, 'Higher interval domain')
    ordered = sum(comb(n, a)*comb(n-a, b) for a in range(lo, hi+1) for b in range(lo, min(hi, n-a)+1))
    require(ordered % 2 == 0, 'Fixed-point-free edge swap')
    unused = sum(comb(n, c)*sum(comb(n-c, a) for a in range(lo, min(hi, n-c-lo)+1) if lo <= n-c-a <= hi)
                 for c in range(n-2*lo+1))
    require(unused == ordered, 'Independent unused-point count')
    orbit_pairs = [(a, b) for a in range(lo, hi+1) for b in range(a, hi+1) if a+b <= n]
    degree = sum(comb(n-lo, b) for b in range(lo, min(hi, n-lo)+1))
    N, s, h, k = parameters(n)
    gamma = n*(n-1)*(2**(n-2)-n+1)+2*(N-n-1)
    return dict(n=n, interval=[lo, hi], dimension=ordered//2, unused_count=unused//2,
                invariant_dimension=len(orbit_pairs), invariant_size_pairs=[list(pair) for pair in orbit_pairs],
                maximum_degree=degree, trace_G=gamma)
