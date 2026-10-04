"""Exact eleven-parameter critical profiles with two independent lower means with an explicit pair radical.

Same-author arithmetic; not independent review. Parameters are I1..I5,
R1..R5,t, the two lower real means mA,mB, and b=sqrt(H/2). The sixth coordinates
are minus the corresponding sum. Monomial carries are checked before
every multiplication, and b²=H/2 is reduced explicitly.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
import json, sys

HERE = Path(__file__).resolve().parent
DEPENDENCIES = json.loads((HERE/'DEPENDENCIES.json').read_text())
PARENT = (HERE/DEPENDENCIES['parent_directory']).resolve()
for name, digest in DEPENDENCIES['parent_files'].items():
    if sha256((PARENT/name).read_bytes()).hexdigest() != digest:
        raise RuntimeError('SOURCE whole pinned same-author parent source changed: '+name)
sys.path.insert(0, str(PARENT))
import cap as s
import arithmetic as ar

NAMES = tuple('I'+str(i) for i in range(1,6)) + tuple('R'+str(i) for i in range(1,6)) + ('t', 'b', 'mA', 'mB')
WIDTH = len(NAMES)
BASE = 16
RADICAL = BASE**11
HALF_H = ar.ns(s.fH, F(1,2))

@lru_cache(maxsize=16384)
def digits(i):
    out = []
    for _ in range(WIDTH):
        out.append(i % BASE)
        i //= BASE
    ar.need(i == 0, 'formal monomial width')
    return tuple(out)

def multiply(p,q):
    out = {}
    for i,a in p.items():
        di = digits(i)
        for j,b in q.items():
            dj = digits(j)
            ar.need(all(x+y<BASE for x,y in zip(di,dj)), 'NO monomial carry/collision')
            k = i+j
            coeff = ar.nm(a,b)
            power_b = di[11]+dj[11]
            if power_b >= 2:
                k -= (power_b//2)*2*RADICAL
                coeff = ar.nm(coeff, ar.np(HALF_H,power_b//2))
            out[k] = ar.na(out.get(k,ar.N0),coeff)
    return {i:a for i,a in out.items() if a != ar.N0}
s.nm = multiply

def var(i): return {BASE**i:ar.N1}
I = [var(i) for i in range(5)]
I.append(s.ns(s.na(*I),-1))
R = [var(i) for i in range(5,10)]
R.append(s.ns(s.na(*R),-1))
t, radical_b, mean_A, mean_B = var(10), var(11), var(12), var(13)
VI = s.na(*(s.np(x,2) for x in I))
VR = s.na(*(s.np(x,2) for x in R))
J = s.na(*(s.nm(x,y) for x,y in zip(I,R)))
TI = s.na(*(s.np(x,3) for x in I))

prior = json.loads((PARENT/'EXPECTED.json').read_text())
con = {k:s.decode(v) for k,v in prior['constants'].items()}

def retag(g):
    return tuple({i*BASE**10:a for i,a in p.items()} for p in g)
raw = s.shrinking_components(con['M4'],con['beta3'],con['nu4'],con['sigma4'],s.N1)
A0,B0,K0 = tuple({key:retag(g) for key,g in p.items()} for p in raw)

# Explicit formulas; no private checkpoint or generated pencil is loaded.
A3=s.ns(s.N1,F(3,2)); A4=s.na(s.N1,s.c)
b3=s.ns(s.H,F(3,14)); b4=s.ns(s.nm(s.H,s.na(s.ns(s.N1,2),s.ns(s.np(s.c,2),-2))),F(1,7))
q3=s.ns(s.H,F(3,40))
q4=s.nm(s.H,s.na(s.ns(s.rho,F(1,8)),s.ns(s.na(s.ns(s.np(s.c,2),2),s.ns(s.c,-1)),F(1,20))))
determinant=s.na(s.nm(A4,b3),s.ns(s.nm(A3,b4),-1))
mI=s.nm(s.na(s.nm(b3,q4),s.ns(s.nm(b4,q3),-1)),s.ni(determinant))
betaI=s.nm(s.na(s.nm(A3,q4),s.ns(s.nm(A4,q3),-1)),s.ni(determinant))
P=s.na(s.ns(s.nm(s.nm(t,VI),s.ni(s.H)),F(-2,3)),
       s.ns(s.nm(s.nm(s.H,s.rho),J),F(-3,2)),s.ns(TI,F(1,2)))
Q=s.ns(s.nm(s.H,J),F(-9,10))
o3=s.ns(s.nm(s.H,J),F(1,10))
o4=s.ns(s.na(s.nm(P,s.na(s.ns(s.np(s.c,2),4),s.ns(s.N1,-1))),
             s.nm(Q,s.na(s.ns(s.c,-2),s.ns(s.N1,-1)))),F(-1,9))
sigma=s.ns(s.nm(s.na(o4,s.ns(o3,-1)),s.ni(s.nm(s.H,s.na(s.ns(s.c,2),s.ns(s.N1,-1))))),7)
nu=s.na(s.ns(s.nm(s.H,sigma),F(1,7)),s.ns(o3,-1))
chi=s.ns(s.nm(s.C['alpha'],s.H),-1)
LOWER_THIRD_PAIR_FACTOR=F(-1,2)


def predicted_delta(paid):
    rows=[[s.G0]*10 for _ in range(10)]
    def add(order,degree,g):
        rows[order][degree]=s.ga(rows[order][degree],g)
        rows[order][0]=s.ga(rows[order][0],s.gs(g,-1))
    add(8,6,s.gf(s.ns(s.nm(s.nm(s.rho,s.H),VI),F(3,4))))
    add(8,5,s.gf(s.ns(s.nm(s.H,VI),F(9,20))))
    add(9,6,(s.N0,P));add(9,5,(s.N0,Q))
    if paid:
        add(8,8,s.gf(s.ns(s.nm(mI,VI),-9)))
        add(8,7,s.gf(s.ns(s.nm(s.nm(s.H,betaI),VI),F(9,7))))
        add(9,8,(s.N0,s.ns(nu,-9)))
        add(9,7,(s.N0,s.ns(s.nm(s.H,sigma),F(-9,7))))
    return rows

def conjugate(p): return {key:s.gc(g) for key,g in p.items()}

def family(paid=True,order=10,lower_centers=False,balanced_means=False):
    m = s.nm(mI,VI) if paid else s.N0
    b = s.nm(betaI,VI) if paid else s.N0
    n, sig = (nu,sigma) if paid else (s.N0,s.N0)
    common = {(8,0):s.gf(m),(9,0):(s.N0,n)}
    small = [s.pa(A0,{(3,0):(s.N0,x),(4,0):s.gf(y)},common) for x,y in zip(I,R)]
    B = s.pa(B0,common)
    if lower_centers:
        small=[s.pa(point,{(4,0):s.gf(mean_A)}) for point in small]
        other=s.ns(mean_A,-3) if balanced_means else mean_B
        B=s.pa(B,{(4,0):s.gf(other)})
    S2 = {(6,0):s.gf(s.ns(VI,-1)),(7,0):(s.N0,s.ns(J,2)),(8,0):s.gf(VR)}
    D2 = {(e+2,j):s.gm(s.gf(s.ns(s.H,F(1,2))),g)
          for (e,j),g in s.pp(K0,2,order-2).items()}
    D2 = s.pa(D2,s.ps(S2,F(-1,2)),
              {(8,0):s.gf(s.ns(s.nm(s.H,b),-1)),
               (9,0):(s.N0,s.nm(s.H,sig))})
    return small,B,D2

def literal_primitive(small,B,D2,order=9):
    ar.need(len(small)==6, 'CENSUS all6 small critical slots')
    factor = {(0,0):s.G1}
    for point in small:
        factor = s.pm(factor,s.pa({(0,1):s.G1},s.ps(point,-1)),order)
    lb = s.pa({(0,1):s.G1},s.ps(B,-1))
    derivative = s.ps(s.pm(factor,s.pa(s.pp(lb,2,order),s.ps(D2,-1)),order),9)
    return s.primitive(derivative,order,2)

def actual_moments(small,B,D2,order=9):
    from math import comb
    moments = [s.N0]
    for n in range(1,9):
        moments.append(s.pa(*(s.pp(point,n,order) for point in small),
            *(s.ps(s.pm(s.pp(B,n-j,order),s.pp(D2,j//2,order),order),2*comb(n,j))
              for j in range(0,n+1,2))))
    return moments

def newton_primitive(moments,order=9):
    elementary = [{(0,0):s.G1}]
    for n in range(1,9):
        elementary.append(s.ps(s.pa(*(s.ps(s.pm(elementary[n-j],moments[j],order),(-1)**(j-1))
                                      for j in range(1,n+1))),F(1,n)))
    derivative = {}
    for n,e in enumerate(elementary):
        derivative = s.pa(derivative,{(i,8-n):s.gs(g,9*(-1)**n) for (i,j),g in e.items()})
    return s.primitive(derivative,order,2)

def pair_square_root(D2,order=8):
    L = {(e-2,j):s.gm(s.gf(s.ns(s.ni(s.H),2)),g)
         for (e,j),g in D2.items() if 2<=e<=order+2}
    # Knew=i sqrt(-L), with leading i; no square-root sign fitted numerically.
    q = s.pa(s.ps(L,-1),{(0,0):s.gs(s.G1,-1)})
    ar.need(not q or min(e for e,j in q)>=2, 'complete normalized pair square-root scale')
    root = s.pa({(0,0):s.G1},s.ps(q,F(1,2)),s.ps(s.pp(q,2,order),F(-1,8)),
                s.ps(s.pp(q,3,order),F(1,16)),s.ps(s.pp(q,4,order),F(-5,128)))
    K = {key:s.gm((s.N0,s.N1),g) for key,g in root.items()}
    return K,L

def squared_distances(small,B,D2,order=9):
    anchor = {(0,0):s.G1,(2,0):s.gs(s.G1,-1)}
    K,L = pair_square_root(D2,order-1)
    D = {(e+1,j):s.gm(s.gf(radical_b),g) for (e,j),g in K.items() if e+1<=order}
    points = [*small,s.pa(B,D),s.pa(B,s.ps(D,-1))]
    distances = []
    for point in points:
        delta = s.pa(anchor,s.ps(point,-1))
        distances.append(s.pm(delta,conjugate(delta),order))
    return distances,K,L

def reciprocal_distance(v,order=9):
    q = s.pa(v,{(0,0):s.gs(s.G1,-1)})
    ar.need(not q or min(e for e,j in q)>=2,'complete actual squared-distance binomial scale')
    return s.pa({(0,0):s.G1},s.ps(q,F(-1,2)),s.ps(s.pp(q,2,order),F(3,8)),
                s.ps(s.pp(q,3,order),F(-5,16)),s.ps(s.pp(q,4,order),F(35,128)))

def encode_g(g):
    return [[[list(digits(i)),[str(x) for x in a]] for i,a in sorted(p.items())] for p in g]

def vector(p,order=9): return [p.get((e,0),s.G0) for e in range(order+1)]

def encode_poly(p):
    return [[list(key),encode_g(g)] for key,g in sorted(p.items())]

def eq(ids,name,lhs,rhs):
    ar.need(lhs==rhs,'WHOLE '+name)
    ids.append({'name':name,'whole_maps_compared':True,
                'sha256':sha256(ar.canonical([encode_g(g) for g in lhs])).hexdigest()})

def complete_record(name,record):
    record={k:v for k,v in record.items() if k not in ('seconds','peak_rss_kib')}
    record.update({'stage':name,'agent':'six-sendov-3','role':'researcher','parameter_names':NAMES,
        'monomial_base':BASE,'every_multiplication_carry_checked':True,
        'radical_relation':'b^2=H/2; positive analytic branch specified ordinarily',
        'same_author_arithmetic':True,'formalization':False,'independent_review':False,
        'scope':'displayed fixed-compact critical class and constructed11Dcap; no universal fourth rate',
        'parent_source_commit':DEPENDENCIES['parent_source_commit']})
    return record
