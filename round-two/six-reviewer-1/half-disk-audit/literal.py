"""Independent literal complex-polynomial and generic Newton bridges.

Exact Gaussian arithmetic uses pairs, distinct from any native target implementation.
Controls establish identities only, not original unit-disk feasibility.
"""
from fractions import Fraction as Q
from itertools import combinations
from exact import require, encode
import json

ZERO=(Q(0),Q(0)); ONE=(Q(1),Q(0))
def ga(x,y):return (x[0]+y[0],x[1]+y[1])
def gn(x):return (-x[0],-x[1])
def gm(x,y):return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def gs(x,c):return (x[0]*c,x[1]*c)
def gi(x):
    d=x[0]**2+x[1]**2;require(d>0,'nonzero reciprocal')
    return (x[0]/d,-x[1]/d)
def gp(x,n):
    r=ONE
    for _ in range(n):r=gm(r,x)
    return r
def padd(p,q):
    r=[ZERO]*max(len(p),len(q))
    for i,x in enumerate(p):r[i]=ga(r[i],x)
    for i,x in enumerate(q):r[i]=ga(r[i],x)
    return r
def pmul(p,q):
    r=[ZERO]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q):r[i+j]=ga(r[i+j],gm(x,y))
    return r
def peval(p,x):
    r=ZERO
    for c in reversed(p):r=ga(gm(r,x),c)
    return r
def pint(p):return [ZERO]+[gs(x,Q(1,i+1)) for i,x in enumerate(p)]
def integral(p):return peval(pint(p),ONE)
def coefficients(factors):
    p=[ONE]
    for f in factors:p=pmul(p,f)
    return p
def subset_coefficients(constants, slopes):
    out=[ZERO]*9
    for k in range(9):
        for selected in combinations(range(8),k):
            term=ONE
            for j in range(8):term=gm(term,slopes[j] if j in selected else constants[j])
            out[k]=ga(out[k],term)
    return out

def generic_newton():
    origin=(0,)*8
    elementary=[]
    for degree in range(9):
        m={}
        for indices in combinations(range(8),degree):
            e=tuple(int(j in indices) for j in range(8));m[e]=1
        elementary.append(m)
    records=[]
    for degree in range(1,9):
        rhs={}
        for k in range(1,degree+1):
            sign=1 if k%2 else -1
            for exp,c in elementary[degree-k].items():
                for j in range(8):
                    ee=list(exp);ee[j]+=k;ee=tuple(ee)
                    rhs[ee]=rhs.get(ee,0)+sign*c
        rhs={ee:c for ee,c in rhs.items() if c}
        lhs={ee:degree*c for ee,c in elementary[degree].items()}
        require(lhs==rhs,'complete eight-variable Newton identity')
        records.append(dict(degree=degree,lhs=sorted(lhs.items()),rhs=sorted(rhs.items())))
    require(len(records)==8,'all eight Newton degrees')
    return records

def one_control(a,q):
    require(len(q)==8,'all eight critical coordinates')
    aa=(a,Q(0)); b=1-a*a
    zs=[ga(aa,gn(gi(x))) for x in q]
    derivative=[gs(x,9) for x in coefficients([[gn(z),ONE] for z in zs])]
    p=pint(derivative);p[0]=gn(peval(p,aa))
    require(peval(p,aa)==ZERO,'actual marked root')
    # Literal long division by z-a: quotient degree8, not a sample evaluation.
    quotient=[ZERO]*9;quotient[8]=p[9]
    for i in range(7,-1,-1):quotient[i]=ga(p[i+1],gm(aa,quotient[i+1]))
    require(pmul([gn(aa),ONE],quotient)==p,'full original degree-nine polynomial')
    require(peval(quotient,aa)==peval(derivative,aa),'simple marked derivative')
    origin=coefficients([[ONE,gs(x,-a)] for x in q])
    origin2=subset_coefficients([ONE]*8,[gs(x,-a) for x in q])
    polar=coefficients([[aa,gs(x,b)] for x in q])
    polar2=subset_coefficients([aa]*8,[gs(x,b) for x in q])
    require(origin==origin2 and polar==polar2,'all nine integrated product coefficients')
    o=gs(integral(origin),9);j=integral(polar)
    require(o==gm(gs(quotient[0],9),gi(peval(quotient,aa))),'original origin communication')
    rhs=gm(gs(peval(quotient,(1/a,Q(0))),a**8),gi(peval(quotient,aa)))
    require(j==rhs,'original polar communication including a^8')
    mu=gs(sum_ga(q),Q(1,8));w=[ga(x,gn(mu)) for x in q]
    require(sum_ga(w)==ZERO,'all eight centered entries')
    centered=[ZERO]*9
    for ell in range(9):
        e=ZERO
        for indices in combinations(range(8),ell):
            term=ONE
            for index in indices:term=gm(term,w[index])
            e=ga(e,term)
        rest=coefficients([[ONE,gs(mu,-a)]]*(8-ell))
        term=[ZERO]*ell+[gm(gs(e,(-a)**ell),c) for c in rest]
        centered=padd(centered,term)
    require(centered==origin,'whole seven-order centered expansion')
    return dict(a=a,q=q,critical_points=zs,original_polynomial=p,
                derivative=derivative,original_quotient=quotient,
                origin_coefficients=origin,polar_coefficients=polar,
                O=o,J=j,mean=mu,centered_entries=w,
                centered_origin_coefficients=centered,
                original_disk_feasibility_claim=False)

def sum_ga(xs):
    result=ZERO
    for x in xs:result=ga(result,x)
    return result

def build():
    tuples=[[(Q(1),Q(0))]*8,
            [(Q(3,5),Q(4,5)),(Q(3,5),-Q(4,5)),(Q(5,13),Q(12,13)),
             (Q(5,13),-Q(12,13)),(Q(4,3),Q(1,2)),(Q(4,3),Q(1,2)),
             (-Q(2,3),Q(0)),(Q(7,8),Q(0))]]
    cases=[one_control(a,q) for a in (Q(2,5),Q(9,20),Q(1,2)) for q in tuples]
    return encode(dict(agent='six-reviewer-1',role='independent mathematical reviewer',
                       generic_newton=generic_newton(),all_six_controls=cases))

if __name__=='__main__':print(json.dumps(build(),sort_keys=True,separators=(',',':')))
