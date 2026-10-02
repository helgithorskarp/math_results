"""Exact S2 complement-pair reduction; six-downset-2, researcher.

Ordinary bridges are written in PROOF.md, unformalized and independently unreviewed.
The credited forced-star face is the one used in 7578/9017/9269.
No centered-core equation is imposed.  Stdlib only.
"""
from fractions import Fraction as Q
from math import comb


def require(ok, message):
    if not ok:
        raise ValueError(message)


def choose(n, k):
    return comb(n, k) if n >= 0 and 0 <= k <= n else 0


def parameters(n):
    require(type(n) is int and n >= 6, 'Domain n>=6')
    return 2**n-n-1, 2**(n-1)-n, 2**(n-1)-1


def complete(n, z, b):
    """All complement deficits z_2..z_floor(n/2), b_a=beta_2a, 2<=a<=n-3."""
    N, s, h = parameters(n)
    require(set(z) == set(range(2, n//2+1)), 'Every complement coordinate')
    require(set(b) == set(range(2, n-2)), 'Every proper-union two-set coordinate')
    require(all(type(v) is Q for v in list(z.values())+list(b.values())), 'Exact inputs')
    B = [[Q(0) for _ in range(n-1)] for _ in range(n-1)]
    for a in range(2, n-1):
        B[a][n-a] = Q(s)-z[min(a, n-a)]
    for a in range(2, n-2):
        B[2][a] = B[a][2] = b[a]
    for a in range(3, n-2):
        B[1][a] = B[a][1] = z[min(a, n-a)]-(n-a-1)*b[a]
    B[1][n-2] = B[n-2][1] = z[2]
    B[1][2] = B[2][1] = z[2]-(n-3)*b[2]-sum(
        b[a]*choose(n-3, a-1) for a in range(3, n-2))
    B[1][1] = Q(s)-sum(B[1][a]*choose(n-2, a-1) for a in range(2, n-1))
    check_stars(n, B)
    return B


def check_stars(n, B):
    N, s, h = parameters(n)
    require(all(type(v) is Q for row in B for v in row), 'Exact table')
    require(all(B[a][b] == B[b][a] for a in range(n-1) for b in range(n-1)), 'Symmetry')
    for a in range(1, n-1):
        require(sum(b*B[a][b]*choose(n-a, b) for b in range(1, n-1)) == (n-a)*s,
                'Original star equation')
    require(all(B[a][b] == 0 for a in range(1, n-1) for b in range(1, n-1)
                if a+b > n or (min(a,b) >= 3 and a+b < n)), 'Original S2 support')


def defect(n, B):
    N, s, h = parameters(n)
    v = {a: Q(s-N+1)+sum(B[a][b]*choose(n-a,b) for b in range(1,n-1))
         for a in range(1,n-1)}
    sigma = sum(comb(n,a)*v[a] for a in v)
    norm2 = sum(comb(n,a)*v[a]**2 for a in v)
    return v, sigma, norm2


def physical(n, B, j, upper=False):
    N, s, h = parameters(n)
    aa = list(range(max(1,j), min(n-2,n-j)+1))
    g = {a: comb(n-2*j,a-j) for a in aa}
    F = [[g[a]*(Q((h if upper else s)*int(a==b))
                    +(-1)**(j+int(upper))*B[a][b]*choose(n-a-j,b-j)
                    -(comb(n,b) if not upper and j==0 else 0))
          for b in aa] for a in aa]
    require(all(F[i][k] == F[k][i] for i in range(len(aa)) for k in range(len(aa))),
            'Physical sector symmetry')
    if not upper and j <= 1:
        kernel = [Q(a if j == 0 else 1) for a in aa]
        require(all(sum(v*x for v,x in zip(row,kernel))==0 for row in F), 'Forced lower kernel')
    return aa, g, F


def reduced_physical(n, B, j, upper=False):
    aa, g, F = physical(n,B,j,upper)
    keep = [i for i,a in enumerate(aa) if upper or j >= 2 or a != 1]
    return [aa[i] for i in keep], g, [[F[i][k] for k in keep] for i in keep]


def pairing(n, j, d, eps, B, u, v):
    """Physical D^+ pairing for row couplings g_a*u_a, with range checks.

    Complement sum/difference coefficients are rational; no square roots.
    Caller verifies all relevant u/v lie in the range before using a zero mode.
    """
    total = Q(0)
    nullity = 0
    for a in range(3, n//2+1):
        b = n-a
        g = comb(n-2*j,a-j)
        c = B[a][b]
        if a == b:
            den = d+eps*c
            require(den >= 0, 'Negative central bulk eigenvalue')
            if den:
                total += g*u[a]*v[a]/den
            else:
                require(u[a] == v[a] == 0, 'Central zero-mode range failure')
                nullity += 1
        else:
            for sign in [1,-1]:
                den = d+sign*eps*c
                require(den >= 0, 'Negative bulk pair eigenvalue')
                left = u[a]+sign*u[b]; right = v[a]+sign*v[b]
                if den:
                    total += Q(g,2)*left*right/den
                else:
                    require(left == right == 0, 'Pair zero-mode range failure')
                    nullity += 1
    return total, nullity


def root_reduction(n, B, j, upper=False):
    """Exact roots <=3, all complement and mean boundaries included.

    Lower degrees0/1 remove layer1 using the actual forced lower kernel.
    Lower degree0 handles -J by a denominator-safe rank-one criterion.
    """
    require(j in (0,1,2), 'Only the three low sectors')
    N,s,h = parameters(n)
    aa,g,F = reduced_physical(n,B,j,upper)
    roots = [a for a in aa if a in (1,2,n-2)]
    bulk = list(range(3,n-2))
    ids = {a:i for i,a in enumerate(aa)}
    d = Q(h if upper else s); eps = (-1)**(j+int(upper))
    rows = [{a:F[ids[r]][ids[a]]/g[a] for a in bulk} for r in roots]
    S = [[F[ids[r]][ids[t]] for t in roots] for r in roots]
    gram = [[pairing(n,j,d,eps,B,u,v)[0] for v in rows] for u in rows]
    S = [[v-q for v,q in zip(row,qrow)] for row,qrow in zip(S,gram)]
    out = {'degree':j,'upper':upper,'roots':roots,'schur':S,'gram':gram,
           'bulk_layers':bulk,'mean_gamma':None,'mean_range':None}
    if not upper and j == 0:
        one = {a:Q(1) for a in bulk}
        gamma = pairing(n,j,d,eps,B,one,one)[0]
        require(gamma <= 1, 'Negative lower bulk mean')
        z = [pairing(n,j,d,eps,B,u,one)[0] for u in rows]
        out['mean_gamma'] = gamma; out['mean_range'] = z
        if gamma < 1:
            S = [[v-z[i]*z[k]/(1-gamma) for k,v in enumerate(row)] for i,row in enumerate(S)]
        else:
            require(all(v == 0 for v in z), 'Saturated mean range failure')
        out['schur'] = S
    return out


def lower_energy_budget(n,B):
    N,s,h=parameters(n)
    a0=Q(s)-B[2][n-2]**2/s
    _,g1,F1=reduced_physical(n,B,1)
    _,g2,F2=reduced_physical(n,B,2)
    bulk=range(3,n-2)
    u1={a:Q(-(n-a-1))*B[2][a] for a in bulk}
    u2={a:B[2][a] for a in bulk}
    e1=pairing(n,1,Q(s),-1,B,u1,u1)[0]/(n-2)
    e2=pairing(n,2,Q(s),1,B,u2,u2)[0]
    diagonal=Q(0)
    for a in bulk:
        den=Q(s*s)-B[a][n-a]**2
        require(den>=0,'Diagonal budget complement domain')
        if den:
            diagonal+=choose(n-3,a-1)*B[2][a]**2/den
        else:
            require(B[2][a]==0,'Diagonal budget singular coupling')
    require(e1+(n-3)*e2==(n-2)*s*diagonal,'Complement cross terms cancel exactly')
    return {'A':a0,'E1_normalized':e1,'E2':e2,
            'y_lower':e2-a0,'y_upper':(a0-e1)/(n-3),
            'combined_cost':e1+(n-3)*e2,'combined_budget':(n-2)*a0,
            'diagonal_cost':diagonal,'diagonal_budget':Q(1)-B[2][n-2]**2/s**2}


def inverse(A):
    n=len(A);work=[[Q(v) for v in row]+[Q(i==k) for k in range(n)] for i,row in enumerate(A)]
    for k in range(n):
        hit=next((i for i in range(k,n) if work[i][k]),None)
        require(hit is not None,'Singular matrix inverse')
        work[k],work[hit]=work[hit],work[k];p=work[k][k]
        work[k]=[v/p for v in work[k]]
        for i in range(n):
            if i!=k:
                v=work[i][k]
                work[i]=[x-v*y for x,y in zip(work[i],work[k])]
    return [row[n:] for row in work]


def direct_schur(n,B,j,upper=False):
    """Independent ordinary dense Schur, for bounded arithmetic controls only."""
    require(n<=20,'Dense Schur guard n<=20')
    aa,g,F=reduced_physical(n,B,j,upper)
    ri=[i for i,a in enumerate(aa) if a in (1,2,n-2)]
    bi=[i for i,a in enumerate(aa) if a not in (1,2,n-2)]
    D=[[F[i][k] for k in bi] for i in bi];inv=inverse(D)
    R=[[F[i][k] for k in bi] for i in ri]
    return [[F[i][k]-sum(R[p][u]*inv[u][v]*R[q][v] for u in range(len(bi)) for v in range(len(bi)))
             for q,k in enumerate(ri)] for p,i in enumerate(ri)]
