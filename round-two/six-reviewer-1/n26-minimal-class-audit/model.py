"""Adapted own earlier original-star linear system and inverse empty-coordinate metric."""
from math import comb
from fractions import Fraction as Q
from exact import need, solve


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def parameters(n):
    sizes = list(range(1, n-1))
    populations = [comb(n, a) for a in sizes]
    N = 1+sum(populations)
    s = sum(comb(n-1, a-1) for a in sizes)
    return sizes, populations, N, s


def expected_names(n, active):
    allowed = set(active)|{n-a for a in active}|{n//2}
    return ([f'd{a}' for a in active+[n//2]]+
            [f't{a}_{b}' for a in range(2, n-1) for b in range(a, n-1)
             if a+b < n and a in allowed and b in allowed])


def decode(n, active, names, values):
    need(n == 26 and active == [8, 9, 10, 11, 12], 'wrong finite domain')
    need(names == expected_names(n, active), 'missing/reordered/or duplicate coordinate')
    need(len(values) == len(names) and all(isinstance(x, str) for x in values), 'rational strings required')
    vals = dict(zip(names, map(Q, values)))
    sizes, populations, N, s = parameters(n)
    B = [[Q(0) for b in range(n-1)] for a in range(n-1)]
    for a in range(2, n//2+1):
        d = vals.get(f'd{a}', Q(0))
        need(d >= 0 and (a not in active+[n//2] or d > 0), 'nonpositive active deficit')
        B[a][n-a] = B[n-a][a] = s-d
    for key, v in vals.items():
        if key.startswith('t'):
            a, b = map(int, key[1:].split('_'))
            B[a][b] = B[b][a] = v
    # Entire excluding-point star system, with all singleton couplings unknown.
    A = [[Q(0) for b in sizes] for a in sizes]
    rhs = []
    for row, a in enumerate(sizes):
        fixed = Q(0)
        for b in sizes:
            coefficient = choose(n-a-1, b-1)
            if a == 1:
                A[row][b-1] += coefficient
            elif b == 1:
                A[row][a-1] += coefficient
            else:
                fixed += coefficient*B[a][b]
        rhs.append(s-fixed)
    singleton = solve(A, rhs)
    for a, v in zip(sizes, singleton):
        B[1][a] = B[a][1] = v
    empty = [Q(N-s)-sum((choose(n-a, b)*B[a][b] for b in sizes), Q(0)) for a in sizes]
    loop = Q(N)-sum((c*v for c, v in zip(populations, empty)), Q(0))
    for a in sizes:
        need(sum((choose(n-a-1, b-1)*B[a][b] for b in sizes), Q(0)) == s, 'original out-point star')
        need(s+sum((choose(n-a, b)*B[a][b] for b in sizes), Q(0))+empty[a-1] == N, 'original size row')
    need(sum((choose(n-1, a-1)*empty[a-1] for a in sizes), Q(0)) == s, 'actual empty star')
    need(loop+sum(c*v for c, v in zip(populations, empty)) == N, 'actual empty row')
    need(B == list(map(list, zip(*B))), 'table symmetry')
    return B, empty, loop


def sector(n, B, j):
    _, _, N, s = parameters(n)
    sizes = list(range(max(1, j), min(n-2, n-j)+1))
    g = [choose(n-2*j, a-j) for a in sizes]
    H = [[Q(g[i])*(s*(a == b)-(choose(n, b) if j == 0 else 0)
           +(-1)**j*B[a][b]*choose(n-a-j, b-j))
          for b in sizes] for i, a in enumerate(sizes)]
    # y=Pz coordinates. The TRUE original Euclidean metric is G-b b'/N.
    R = [[Q(g[i])*(a == b)-(Q(choose(n, a)*choose(n, b), N) if j == 0 else 0)
          for b in sizes] for i, a in enumerate(sizes)]
    V = [[N*R[i][k]-H[i][k] for k in range(len(sizes))] for i in range(len(sizes))]
    Z = []
    if j == 0:
        Z.append([Q(a) for a in sizes])
    elif j == 1:
        Z.append([Q(1) for a in sizes])
    for a in range(2, 8):
        if a in sizes:
            Z.append([Q((b == a)-(-1)**j*(b == n-a)) for b in sizes])
    return sizes, g, H, V, R, Z


def triangular_decode(w):
    """Separate weighted original-star elimination; compare every table/empty entry."""
    n=w['n'];sizes, counts, N, s=parameters(n)
    B=[[Q(0) for _ in range(n-1)] for _ in range(n-1)]
    vals=dict(zip(w['names'],map(Q,w['values'])))
    for a in range(2,n//2+1):B[a][n-a]=B[n-a][a]=s-vals.get('d'+str(a),Q(0))
    for name,x in vals.items():
        if name.startswith('t'):
            a,b=map(int,name[1:].split('_'));B[a][b]=B[b][a]=x
    for a in sizes[1:]:
        B[1][a]=B[a][1]=(Q((n-a)*s)-sum((b*choose(n-a,b)*B[a][b]for b in sizes[1:]),Q(0)))/(n-a)
    B[1][1]=(Q((n-1)*s)-sum((b*choose(n-1,b)*B[1][b]for b in sizes[1:]),Q(0)))/(n-1)
    # Independent lower lift C row sums, not the original row decoder.
    c=[Q(s-(N-1))+sum((choose(n-a,b)*B[a][b]for b in sizes),Q(0))for a in sizes]
    empty=[1-x for x in c];loop=1+sum(count*x for count,x in zip(counts,c))
    return B,empty,loop


def affine_decode_control(w):
    """Baseline and all36 coordinate directions: full affine equality, not samples."""
    import copy
    probes=[]
    for coordinate in [None]+list(range(len(w['names']))):
        point=copy.deepcopy(w)
        if coordinate is not None:point['values'][coordinate]=str(Q(point['values'][coordinate])+1)
        actual=decode(point['n'],point['active'],point['names'],point['values']);other=triangular_decode(point)
        need(actual==other,'all full affine decoder/empty entries')
        probes.append({'changed_coordinate':coordinate,'whole_table':actual[0],'all_empty_entries':actual[1],'empty_loop':actual[2]})
    return probes
