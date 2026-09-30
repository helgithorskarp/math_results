#!/usr/bin/env python3
"""Uniform rank-four exact certificates. CPython 3.11+, standard library only.

Author: six-downset-3, researcher. Rational-function arithmetic and exact
linear-algebra helpers reuse the credited rank-three source. SymPy is not
used by this checker. All infinite identities hold in Q(u).
"""
from __future__ import annotations
import argparse
from copy import deepcopy
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, permutations
import json
from math import comb, gcd, lcm
from pathlib import Path

def require(condition, message):
    if not condition:
        raise ValueError(message)


def trim(a):
    a = [Q(x) for x in a] or [Q(0)]
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return tuple(a)


def padd(a, b):
    return trim([(a[i] if i < len(a) else 0) +
                 (b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))])


def pscale(a, c):
    return trim([x * c for x in a])


def pmul(a, b):
    out = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return trim(out)


def pdivmod(a, b):
    a, b = list(trim(a)), trim(b)
    require(b != (Q(0),), 'zero polynomial divisor')
    out = [Q(0)] * max(1, len(a) - len(b) + 1)
    while trim(a) != (Q(0),) and len(a) >= len(b):
        k, c = len(a) - len(b), a[-1] / b[-1]
        out[k] += c
        for i, x in enumerate(b):
            a[i+k] -= c*x
        a = list(trim(a))
    return trim(out), trim(a)


def pgcd(a, b):
    a, b = trim(a), trim(b)
    while b != (Q(0),):
        a, b = b, pdivmod(a, b)[1]
    return pscale(a, 1/a[-1])


def pvalue(a, x):
    out = Q(0)
    for v in reversed(a):
        out = out*x + v
    return out


class RF:
    """Reduced exact element of Q(u), normalized to monic denominator."""
    def __init__(self, numerator=0, denominator=1):
        if isinstance(numerator, RF):
            require(denominator == 1, 'RF copy with denominator')
            self.p, self.q = numerator.p, numerator.q
            return
        p = trim(numerator if isinstance(numerator, (list, tuple)) else [numerator])
        q = trim(denominator if isinstance(denominator, (list, tuple)) else [denominator])
        require(q != (Q(0),), 'zero rational-function denominator')
        g = pgcd(p, q)
        p, rp = pdivmod(p, g)
        q, rq = pdivmod(q, g)
        require(rp == rq == (Q(0),), 'polynomial gcd division')
        self.p, self.q = pscale(p, 1/q[-1]), pscale(q, 1/q[-1])

    def __add__(self, other):
        b = RF(other)
        return RF(padd(pmul(self.p, b.q), pmul(b.p, self.q)), pmul(self.q, b.q))

    __radd__ = __add__

    def __neg__(self):
        return RF(pscale(self.p, -1), self.q)

    def __sub__(self, other):
        return self + (-RF(other))

    def __rsub__(self, other):
        return RF(other) + (-self)

    def __mul__(self, other):
        b = RF(other)
        return RF(pmul(self.p, b.p), pmul(self.q, b.q))

    __rmul__ = __mul__

    def __truediv__(self, other):
        b = RF(other)
        return RF(pmul(self.p, b.q), pmul(self.q, b.p))

    def __rtruediv__(self, other):
        return RF(other) / self

    def __pow__(self, k):
        require(type(k) is int and k >= 0, 'RF exponent')
        out = RF(1)
        for _ in range(k):
            out *= self
        return out

    def __eq__(self, other):
        b = RF(other)
        return pmul(self.p, b.q) == pmul(b.p, self.q)

    def value(self, u):
        d = pvalue(self.q, Q(u))
        require(d != 0, 'rational-function pole at specialization')
        return pvalue(self.p, Q(u)) / d


def choose(x, k):
    require(type(k) is int and k >= 0, 'binomial lower argument')
    out = 1
    for i in range(k):
        out = out * (x-i) / (i+1)
    return out


def determinant(a):
    n = len(a)
    require(all(len(row) == n for row in a), 'determinant shape')
    out = 0
    for p in permutations(range(n)):
        term = 1
        for i in range(n):
            term *= a[i][p[i]]
        if sum(p[i] > p[j] for i in range(n) for j in range(i+1, n)) % 2:
            term = -term
        out += term
    return out


def certify_margins(calculated, certificate):
    require(set(calculated) == set(certificate), 'positivity margin names')
    for name, value in calculated.items():
        entry = certificate[name]
        a, b = entry['numerator_ascending'], entry['denominator_ascending']
        require(type(a) is list and type(b) is list and a and b, 'coefficient arrays')
        require(all(type(x) is int and x >= 0 for x in a+b), 'nonnegative integer coefficients')
        require(a[0] > 0 and b[0] > 0 and a[-1] > 0 and b[-1] > 0,
                'strictly positive constants and nonzero leading terms')
        require(value == RF(a, b), 'wrong rational-function identity: '+name)
    return len(calculated)


def integer_matrix(a):
    require(a and all(len(row) == len(a) for row in a), 'matrix shape')
    d = 1
    for row in a:
        for x in row:
            d = lcm(d, Q(x).denominator)
    return [[int(Q(x)*d) for x in row] for row in a], d


def psd_rank(a):
    z, _ = integer_matrix(a)
    N = len(z)
    require(all(z[i][j] == z[j][i] for i in range(N) for j in range(N)), 'PSD asymmetry')
    previous = 1
    rank = 0
    for k in range(N):
        require(all(z[i][i] >= 0 for i in range(k, N)), 'negative Schur diagonal')
        piv = next((i for i in range(k, N) if z[i][i] > 0), None)
        if piv is None:
            require(all(z[i][j] == 0 for i in range(k, N) for j in range(k, N)),
                    'zero diagonal with nonzero residual')
            break
        if piv != k:
            z[k], z[piv] = z[piv], z[k]
            for row in z:
                row[k], row[piv] = row[piv], row[k]
        pivot = z[k][k]
        for i in range(k+1, N):
            for j in range(i, N):
                value = pivot*z[i][j] - z[i][k]*z[k][j]
                require(value % previous == 0, 'nonexact Bareiss division')
                z[i][j] = z[j][i] = value//previous
        for i in range(k+1, N):
            z[i][k] = z[k][i] = 0
        previous = pivot
        rank += 1
    return rank


def nullspace(a, width):
    """Integer basis, with no reduction modulo a prime."""
    z = [[Q(x) for x in row] for row in a]
    require(all(len(row) == width for row in z), 'nullspace shape')
    pivots = []
    r = 0
    for j in range(width):
        pivot = next((i for i in range(r, len(z)) if z[i][j]), None)
        if pivot is None:
            continue
        z[r], z[pivot] = z[pivot], z[r]
        p = z[r][j]
        z[r] = [x/p for x in z[r]]
        for i in range(len(z)):
            if i != r and z[i][j]:
                c = z[i][j]
                z[i] = [x-c*y for x, y in zip(z[i], z[r])]
        pivots.append(j)
        r += 1
        if r == len(z):
            break
    basis = []
    for f in range(width):
        if f in pivots:
            continue
        v = [Q(0)]*width
        v[f] = 1
        for i, j in enumerate(pivots):
            v[j] = -z[i][f]
        d = lcm(*(x.denominator for x in v))
        v = [int(x*d) for x in v]
        g = gcd(*v)
        basis.append([x//g for x in v])
    require(all(sum(x*y for x, y in zip(row, v)) == 0 for row in a for v in basis),
            'nullspace residual')
    return basis


def inner(a, b):
    return sum(x*y for x, y in zip(a, b))


def matvec(a, x):
    return [inner(row, x) for row in a]


def inverse(a):
    N = len(a)
    require(all(len(row) == N for row in a), 'inverse shape')
    z = [[Q(x) for x in row]+[Q(i == j) for j in range(N)] for i, row in enumerate(a)]
    for k in range(N):
        p = next((i for i in range(k, N) if z[i][k]), None)
        require(p is not None, 'singular inverse')
        z[k], z[p] = z[p], z[k]
        pivot = z[k][k]
        z[k] = [x/pivot for x in z[k]]
        for i in range(N):
            if i != k and z[i][k]:
                c = z[i][k]
                z[i] = [x-c*y for x, y in zip(z[i], z[k])]
    result = [row[N:] for row in z]
    require(all(sum(a[i][k]*result[k][j] for k in range(N)) == int(i == j)
                for i in range(N) for j in range(N)), 'inverse residual')
    return result


def matrix_hash(a):
    raw = json.dumps([[str(Q(x)) for x in row] for row in a], separators=(',', ':')).encode()
    return sha256(raw).hexdigest()


def weights(n):
    """Generic formula, used only for n>=8; Q(n), no pole specialization."""
    d = (n-4)*(n-3)*(n-2)
    b13 = -2*n*(n-5)/((n-3)*(n-2))
    b14 = n*(n*n+3*n-22)/d
    b23 = -n*(n*n-9*n+2)/d
    b24 = n*(n+1)*(n+2)/d
    b33 = 12*n*(n+3)/d
    b34 = n*(n**3-3*n*n-16*n-108)/((n-6)*d)
    b44 = n*(n**4-10*n**3+29*n*n-20*n+324)/((n-7)*(n-6)*d)
    return [[0,0,b13,b14], [0,0,b23,b24], [b13,b23,b33,b34], [b14,b24,b34,b44]]


def exact_weights(n):
    require(type(n) is int and n>=6, 'weights require integer n>=6')
    if n == 6:
        return [[Q(x) for x in row] for row in
                [[-2,0,2,4], [0,Q(4,3),0,22], [2,0,24,0], [4,22,0,0]]]
    if n == 7:
        return [[Q(x) for x in row] for row in
                [[0,Q(-8,5),1,4], [Q(-8,5),Q(2,5),3,6], [1,3,2,26], [4,6,26,0]]]
    return [[Q(x) for x in row] for row in weights(Q(n))]


def sectors(n, beta, finite_n=None):
    N = 1+sum(choose(n,a) for a in range(1,5))
    s = sum(choose(n-1,b-1) for b in range(1,5))
    last = 4 if finite_n is None else min(4,finite_n//2)
    result = []
    for j in range(last+1):
        top = 4 if finite_n is None else min(4,finite_n-j)
        layers = list(range(max(1,j),top+1))
        K = [[s*int(a==b)-(choose(n,b) if j==0 else 0)
              +(-1)**j*beta[a-1][b-1]*choose(n-a-j,b-j)
              for b in layers] for a in layers]
        G = [choose(n-2*j,a-j) for a in layers]
        if finite_n is not None:
            require(all(x>0 for x in G), 'positive harmonic metric on actual truncated range')
        result.append((K,G,layers))
    return N,s,result


def elementary(M):
    return [1]+[sum(determinant([[M[i][j] for j in ix] for i in ix])
                   for ix in combinations(range(len(M)),k))
                for k in range(1,len(M)+1)]


def margins(N, blocks):
    result = {}
    for j,(K,G,layers) in enumerate(blocks):
        d = len(layers)-(2 if j==0 else (1 if j==1 else 0))
        e = elementary(K)
        require(all(x==0 for x in e[d+1:]), 'prescribed characteristic zero coefficients')
        for k in range(1,d+1):
            result['C%d_shift_e%d'%(j,k)] = sum((-1)**(k-l)*comb(d-l,k-l)*e[l] for l in range(k+1))
            result['U%d_shift_e%d'%(j,k)] = sum((-1)**l*comb(d-l,k-l)*(N-1)**(k-l)*e[l] for l in range(k+1))
    return result


def linear_checks(n,beta,N,s):
    for a in range(1,5):
        require(sum(beta[a-1][b-1]*choose(n-a-1,b-1) for b in range(1,5))==s,
                'coordinate star equation')
        require(sum(beta[a-1][b-1]*choose(n-a,b) for b in range(1,5))==N-1-s,
                'centering equation')
    return 8


def symbolic_check(certificate):
    u = RF([0,1]); n = u+8
    beta = weights(n)
    N,s,blocks = sectors(n,beta)
    count = linear_checks(n,beta,N,s)
    require([len(x[0]) for x in blocks]==[4,4,3,2,1], 'stable sector sizes')
    for K,G,layers in blocks:
        for i in range(len(K)):
            for j in range(len(K)):
                require(G[i]*K[i][j]==G[j]*K[j][i], 'harmonic metric symmetry')
                count += 1
    for v in ([1]*4,[1,2,3,4]):
        for row in blocks[0][0]:
            require(inner(row,v)==0,'trivial sector kernel')
            count += 1
    for row in blocks[1][0]:
        require(sum(row)==0,'degree one sector kernel')
        count += 1
    mg = margins(N,blocks)
    gaps = certify_margins(mg,certificate['margins'])
    count += gaps+3 # e3(K0)=e4(K0)=e4(K1)=0, checked above.
    m=N-1; delta=n*(n-1)*(n-2)*(n-3)/4; B=3*(n-1)*(n-2)*(n-3)/2
    eps=1/(3*(n+1)*(n*n-3*n+14)*(n-1)*(n-2)*(n-3))
    require(eps==delta/(8*m*B*B),'rank trade epsilon identity')
    require(eps*B==1/(2*(n+1)*(n*n-3*n+14)),'trade norm identity')
    require(N-2*s==choose(n-1,4),'strict half density identity')
    count += 3
    n6=u+6
    def density(x):
        NN=1+sum(choose(x,a) for a in range(1,5))
        ss=sum(choose(x-1,b-1) for b in range(1,5))
        return ss/NN
    def f(x):
        return x**4-2*x**3+11*x*x+14*x+24
    require(density(n6)-density(n6+1)==
            4*(n6-1)*(n6-2)*(n6-3)*(n6**3+3*n6*n6+14*n6+24)/(f(n6)*f(n6+1)),
            'strict density decrease identity')
    count += 1
    q=(n6*n6-3*n6+4)/2
    ss=n6*(n6*n6-3*n6+8)/6
    mm=n6*(n6+1)*(n6*n6-3*n6+14)/24
    A=ss+(n6-1)*q
    g=4*n6**3-15*n6*n6+29*n6-12
    H=mm-n6*ss*ss/A
    require(A==g/6,'constant star Gram eigenvalue')
    require(H==n6*(n6-1)*(n6**4+4*n6**3+17*n6*n6-106*n6+168)/(24*g),
            'exact star projection residual norm')
    dd=n6*(n6-1)*(n6-2)*(n6-3)/4
    BB=3*(n6-1)*(n6-2)*(n6-3)/2
    tmax=dd/(2*BB*(BB*H+dd))
    require(tmax==4*g/(3*(n6-1)*(n6-2)*(n6-3)*(n6**5+3*n6**4+29*n6**3-183*n6*n6+390*n6-216)),
            'larger closed sufficient repair endpoint')
    count += 3
    return {'coefficient_domain':'Q(u)','substitution':'n=8+u,u>=0',
            'identities_checked':count,'positive_margins':gaps,
            'finite_specializations_used_to_prove_infinite_signs':0,
            'sector_sizes':[len(x[0]) for x in blocks], 'density_decreases_for_all_n_at_least':6}


def vertices(n):
    return [sum(1<<i for i in a) for k in range(5) for a in combinations(range(n),k)]


def harmonic_audit(n,beta,members):
    """Full exact bases and all lifts/actions at each finite test order."""
    level={a:[x for x in members if x.bit_count()==a] for a in range(5)}
    _,s,blocks=sectors(Q(n),beta,finite_n=n)
    all_lifts=[]; dimensions=[]; actions=0
    for j,(K,G,layers) in enumerate(blocks):
        basis=[[1]] if j==0 else nullspace(
            [[int(r&x==r) for x in level[j]] for r in level[j-1]],len(level[j]))
        target=comb(n,j)-(comb(n,j-1) if j else 0)
        require(len(basis)==target,'harmonic dimension')
        dimensions.append(target)
        hgram=[[inner(v,w) for w in basis] for v in basis]
        require(psd_rank(hgram)==target,'full harmonic basis independence')
        lifts={}
        for a in layers:
            lifts[a]=[[sum(h[i] for i,x in enumerate(level[j]) if x&A==x)
                       for A in level[a]] for h in basis]
            for i,v in enumerate(lifts[a]):
                if j: require(sum(v)==0,'nontrivial lift mean')
                for k,w in enumerate(lifts[a]):
                    require(inner(v,w)==comb(n-2*j,a-j)*hgram[i][k],'complete lift norm identity')
                full=[0]*len(members); index={x:i for i,x in enumerate(members)}
                for A,value in zip(level[a],v):full[index[A]]=value
                all_lifts.append((j,a,full))
        for b in layers:
            for a in range(1,5):
                D=[[int(A&B==0) for B in level[b]] for A in level[a]]
                for hidx,v in enumerate(lifts[b]):
                    image=matvec(D,v)
                    if a not in layers:
                        require(all(x==0 for x in image),'disjoint operator outside harmonic range')
                    else:
                        c=(-1)**j*comb(n-a-j,b-j) if n-a-j>=b-j>=0 else 0
                        require(image==[c*x for x in lifts[a][hidx]],'complete disjoint action')
                    core_image=[s*(v[i] if a==b else 0)-sum(v)+beta[a-1][b-1]*d
                                for i,d in enumerate(image)]
                    if a not in layers:
                        require(all(x==0 for x in core_image),'core outside harmonic range')
                    else:
                        entry=K[layers.index(a)][layers.index(b)]
                        require(core_image==[entry*x for x in lifts[a][hidx]],'complete core action')
                    actions += 1
    for i,(j,a,v) in enumerate(all_lifts):
        for k,b,w in all_lifts[:i]:
            if j!=k or a!=b:require(inner(v,w)==0,'orthogonality of full lifted basis')
    require(len(all_lifts)==len(members)-1,'complete nonempty decomposition')
    return {'harmonic_dimensions':dimensions,'complete_lifted_basis_size':len(all_lifts),
            'disjoint_basis_actions_checked':actions,'sector_sizes':[len(x[0]) for x in blocks]}


def core(n,members,beta):
    s=sum(comb(n-1,k) for k in range(4))
    return [[Q(s*int(A==B)-1)+(beta[A.bit_count()-1][B.bit_count()-1] if A&B==0 else 0)
             for B in members[1:]] for A in members[1:]]


def trade(n,members):
    table={(1,1):(n-2)*(n-3),(1,2):-(n-3),(2,2):1}
    return [[table.get(tuple(sorted((A.bit_count(),B.bit_count()))),0) if A!=B and A&B==0 else 0
             for B in members[1:]] for A in members[1:]]


def lift(C):
    r=[sum(row) for row in C]
    return [[1+sum(r)]+[1-x for x in r]]+[[1-r[i]]+[1+x for x in row] for i,row in enumerate(C)]


def definition_check(n,members,L,s):
    N=len(members)
    require(members[0]==0 and len(set(members))==N,'vertex ordering')
    require(all((A&~(1<<i)) in members for A in members for i in range(n) if A>>i&1),'downward closure')
    require(2*s<N,'strict half density')
    require(all(len(row)==N for row in L),'matrix shape')
    require(all(L[i][j]==L[j][i] for i in range(N) for j in range(N)),'matrix symmetry')
    require(all(sum(row)==N for row in L),'H row sums')
    require(all(L[i][j]==s*int(i==j) for i,A in enumerate(members) for j,B in enumerate(members) if A&B),
            'H support and diagonal')
    stars=[[int(A>>i&1) for A in members] for i in range(n)]
    require(all(sum(x)==s for x in stars),'actual equal star sizes')
    require(all(matvec(L,x)==[s]*N for x in stars),'full forced star kernel')
    return stars


def finite_case(n):
    members=vertices(n); N=len(members); m=N-1; s=sum(comb(n-1,k) for k in range(4))
    beta=exact_weights(n); NN,ss,blocks=sectors(Q(n),beta,finite_n=n)
    require((NN,ss)==(N,s),'size formulas')
    linear_checks(Q(n),beta,NN,ss)
    mg=margins(NN,blocks)
    require(all(x>0 for x in mg.values()),'finite spectral gap one')
    C=core(n,members,beta); require(all(sum(row)==0 for row in C),'centered core rows')
    U=[[N*int(i==j)-1-C[i][j] for j in range(m)] for i in range(m)]
    L=lift(C); stars=definition_check(n,members,L,s)
    require(psd_rank(C)==m-n-1 and psd_rank(U)==m,'centered full PSD cap rank')
    X=[[1]+[int(A>>i&1) for i in range(n)] for A in members[1:]]
    gram=[[sum(row[i]*row[j] for row in X) for j in range(n+1)] for i in range(n+1)]
    Ginv=inverse(gram)
    XGinv=[[inner(row,[Ginv[k][j] for k in range(n+1)]) for j in range(n+1)] for row in X]
    P=[[Q(i==j)-inner(XGinv[i],X[j]) for j in range(m)] for i in range(m)]
    require(psd_rank(P)==m-n-1,'exact orthogonal complement projector rank')
    require(all(matvec(P,[row[i] for row in X])==[0]*m for i in range(n+1)),'projector kernel')
    require(psd_rank([[C[i][j]-P[i][j] for j in range(m)] for i in range(m)])==m-n-1,'full lower gap one')
    require(psd_rank([[U[i][j]-int(i==j) for j in range(m)] for i in range(m)])==m-1,'full upper gap one')
    D=trade(n,members); delta=Q(n*(n-1)*(n-2)*(n-3),4); B=Q(3*(n-1)*(n-2)*(n-3),2)
    require(sum(map(sum,D))==delta,'trade total')
    require(max(sum(map(abs,row)) for row in D)==B,'trade absolute row norm')
    require(all(matvec(D,x[1:])==[0]*m for x in stars),'trade star kernel')
    eps=Q(1,3*(n+1)*(n*n-3*n+14)*(n-1)*(n-2)*(n-3))
    require(eps==delta/(8*m*B*B) and eps<=1 and eps*B<=Q(1,4),'repair parameter bounds')
    Cp=[[C[i][j]+eps*D[i][j] for j in range(m)] for i in range(m)]
    Up=[[U[i][j]-eps*D[i][j] for j in range(m)] for i in range(m)]
    Lp=lift(Cp); definition_check(n,members,Lp,s)
    require(psd_rank(Cp)==m-n and psd_rank(Up)==m,'repaired full core PSD cap rank')
    require(psd_rank(Lp)==N-n,'maximal full lower rank')
    cap=[[N*int(i==j)-Lp[i][j] for j in range(N)] for i in range(N)]
    require(psd_rank(cap)==N-1,'simple upper endpoint')
    q=sum(comb(n-2,k) for k in range(3))
    A=s+(n-1)*q
    h=[1-Q(s,A)*v.bit_count() for v in members[1:]]
    H=Q(m)-Q(n*s*s,A)
    require(inner(h,h)==H>0,'actual star projection residual norm')
    require(all(inner(h,x[1:])==0 for x in stars),'projection residual orthogonal to every star')
    tmax=delta/(2*B*(B*H+delta))
    require(tmax>eps and tmax*B<Q(1,2),'larger endpoint parameter bounds')
    # Entire compressed endpoint slacks, using literal table weights.
    table={(1,1):(n-2)*(n-3),(1,2):-(n-3),(2,2):1}
    for j,(K,G,layers) in enumerate(blocks):
        T=[[(-1)**j*table.get(tuple(sorted((a,b))),0)*choose(Q(n-a-j),b-j)
            for b in layers] for a in layers]
        endpoint=[[K[i][k]+tmax*T[i][k] for k in range(len(layers))] for i in range(len(layers))]
        slack=[[N*int(i==k)-(comb(n,layers[k]) if j==0 else 0)-endpoint[i][k]
                for k in range(len(layers))] for i in range(len(layers))]
        target=len(layers)-(1 if j in (0,1) else 0)
        require(psd_rank([[G[i]*x for x in row] for i,row in enumerate(endpoint)])==target,
                'larger endpoint full compressed PSD rank')
        require(psd_rank([[G[i]*(x-Q(1,2)*int(i==k)) for k,x in enumerate(row)]
                           for i,row in enumerate(slack)])==len(layers),
                'larger endpoint compressed upper buffer strictly above one half')
    out={'n':n,'N':N,'s':s,'beta':[[str(x) for x in row] for row in beta],
         'centered_core_rank':m-n-1,'centered_full_rank':N-n-1,
         'epsilon':str(eps),'repaired_core_rank':m-n,'repaired_full_rank':N-n,
         'upper_slack_rank':N-1,'maximum_families_by_kernel_proof':n,
         'full_core_gap_one_checks':True,'centered_core_sha256':matrix_hash(C),
         'repaired_full_L_sha256':matrix_hash(Lp),'gap_one_margins':{k:str(x) for k,x in mg.items()},
         'star_projection_residual_squared_norm':str(H),'larger_safe_parameter':str(tmax),
         'larger_endpoint_all_compressed_slacks_checked':True}
    out.update(harmonic_audit(n,beta,members))
    return out


def negative_controls(certificate):
    rejected=[]
    def reject(name,f):
        try: f()
        except (ValueError,ZeroDivisionError,KeyError):
            rejected.append(name); return
        raise ValueError('corrupt control accepted: '+name)
    broken=deepcopy(certificate); name=next(iter(broken['margins']))
    broken['margins'][name]['numerator_ascending'][0]+=1
    reject('wrong_positive_coefficient_identity',lambda:symbolic_check(broken))
    broken=deepcopy(certificate); broken['margins'][name]['denominator_ascending'][0]=0
    reject('zero_denominator_constant',lambda:certify_margins({name:RF(1)},{name:broken['margins'][name]}))
    beta=exact_weights(6); beta[0][1]=beta[1][0]=1
    reject('wrong_six_boundary_star_weights',lambda:linear_checks(Q(6),beta,57,26))
    beta=exact_weights(8); beta[1][2]=beta[2][1]=0
    reject('omitted_generic_cross_layer_weight',lambda:linear_checks(Q(8),beta,163,64))
    reject('generic_formula_at_six_pole',lambda:weights(Q(6)))
    reject('generic_formula_at_seven_pole',lambda:weights(Q(7)))
    beta=exact_weights(7); members=vertices(7); L=lift(core(7,members,beta))
    L[1][1]+=1
    reject('wrong_nonempty_diagonal',lambda:definition_check(7,members,L,42))
    return rejected


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--check',type=Path)
    args=parser.parse_args()
    certificate=json.loads(Path(__file__).with_name('POSITIVITY_CERTIFICATE.json').read_text())
    result={'agent':'six-downset-3','role':'researcher',
            'status':'Exact certificates plus written completeness, lift and equality proofs in PROOF.md; author-checked, unformalized.',
            'symbolic':symbolic_check(certificate),'finite':[finite_case(n) for n in (6,7,8)],
            'negative_controls':negative_controls(certificate)}
    if args.check: require(result==json.loads(args.check.read_text()),'expected result mismatch')
    if args.output: args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'ok':True,'symbolic_identities':result['symbolic']['identities_checked'],
                      'positive_margins':result['symbolic']['positive_margins'],
                      'finite_orders':[x['n'] for x in result['finite']],
                      'full_lower_ranks':[x['repaired_full_rank'] for x in result['finite']],
                      'negative_controls':len(result['negative_controls'])}))


if __name__=='__main__':main()
