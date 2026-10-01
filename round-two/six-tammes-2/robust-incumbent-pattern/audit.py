"""Independent centered-Taylor interval audit of the new rational bounds.

No production or prerequisite arithmetic is imported. The primary checker
derives model-functions.json; this audit verifies its rational enclosures
and derivatives by a different exact method. Python standard library only.
"""
from fractions import Fraction as Q
from pathlib import Path
from math import comb
from functools import lru_cache
import hashlib
import json

HERE=Path(__file__).resolve().parent
LO,HI=Q(14,25),Q(593,1000)


def require(ok,message):
    if not ok: raise ValueError(message)


def trim(p):
    p=list(p)
    while p and p[-1]==0: p.pop()
    return tuple(p)


def mul(p,q):
    result=[Q(0)]*(len(p)+len(q)-1) if p and q else []
    for i,a in enumerate(p):
        for j,b in enumerate(q): result[i+j]+=a*b
    return trim(result)


def sub(p,q):
    return trim([(p[i] if i<len(p) else 0)-(q[i] if i<len(q) else 0)
                 for i in range(max(len(p),len(q)))])


def derivative(p):
    return trim([i*p[i] for i in range(1,len(p))])


def rational_derivative(f):
    n,d=f
    return sub(mul(derivative(n),d),mul(n,derivative(d))),mul(d,d)


@lru_cache(maxsize=None)
def centered_enclosure(p,left,right):
    """Translate to midpoint; bound the even and odd Taylor monomials."""
    middle=(left+right)/2
    radius=(right-left)/2
    translated=[sum(Q(p[j])*comb(j,k)*middle**(j-k) for j in range(k,len(p)))
                for k in range(len(p))]
    if not translated: return Q(0),Q(0)
    low=high=translated[0]
    for k,a in enumerate(translated[1:],1):
        size=a*radius**k
        if k%2:
            low-=abs(size);high+=abs(size)
        else:
            low+=min(Q(0),size);high+=max(Q(0),size)
    return low,high


def rational_enclosure(f,pieces):
    n,d=f
    require(bool(d),'nonzero denominator polynomial')
    lower=upper=None
    for i in range(pieces):
        left,right=LO+(HI-LO)*i/pieces,LO+(HI-LO)*(i+1)/pieces
        a,b=centered_enclosure(n,left,right)
        c,dhi=centered_enclosure(d,left,right)
        require(not c<=0<=dhi,'centered denominator sign')
        values=(a/c,a/dhi,b/c,b/dhi)
        lower=min(values) if lower is None else min(lower,*values)
        upper=max(values) if upper is None else max(upper,*values)
    return lower,upper


def abs_upper(interval): return max(abs(x) for x in interval)


def audit_bounds(raw,pieces):
    f={name:(tuple(Q(x) for x in obj['numerator']),tuple(Q(x) for x in obj['denominator']))
       for name,obj in raw.items()}
    ranges={name:rational_enclosure(fun,pieces) for name,fun in f.items()}
    for name,left,right in (
        ('w',Q(1,3),Q(2,5)),('height2',Q(49,100),Q(3,5)),
        ('kappa',Q(-3,10),Q(-1,5)),('gamma',Q(-1,2),Q(0)),
        ('q2',Q(0),Q(1)),('Fprime',Q(10),Q(14)),
        ('minus_gramdet',Q(1,4),Q(1)),('plus_gramdet',Q(1,4),Q(1))):
        a,b=ranges[name];require(left<=a<=b<=right,'centered scalar bound '+name)
    require(ranges['minus_det'][0]>=Q(1,10),'negative orientation gap')
    require(ranges['plus_det_over_F'][1]<=Q(-2,5),'positive orientation factor gap')
    for tag in ('minus','plus'):
        require(max(sum(abs_upper(ranges[f'{tag}_xi_{i}_{j}']) for j in range(3))
                    for i in range(3))<=5,'centered inverse row l1 '+tag)
    require(max(sum(abs_upper(ranges[f'ri_{j}_{i}']) for j in range(3))
                for i in range(3))<=3,'centered reflection inverse column l1')
    require(max(sum(abs_upper(ranges[f'A_{label}_{i}']) for i in range(3))
                for label in (0,5,11,6,7,9,14))<=3,'centered A coefficient l1')
    require(max(sum(abs_upper(ranges[f's_{label}_{i}']) for i in range(3))
                for label in range(15))<=3,'centered model coefficient l1')
    derivatives={f's_{label}_{i}':rational_enclosure(rational_derivative(f[f's_{label}_{i}']),pieces)
                 for label in range(15) for i in range(3)}
    require(max(sum(abs_upper(derivatives[f's_{label}_{i}']) for i in range(3))
                for label in range(15))<=18,'centered model derivative l1')
    return len(f),len(derivatives)


def audit_constants():
    e=Q(1,10**13)
    require(6*161<=1000,'common-neighbor error')
    require(Q(3,4)+2*161*e<Q(4,5),'normal amplitude bound')
    require(Q(9,10)-41*e>Q(4,5)>6*161*e,'wrong common-neighbor branch')
    require(3*5*(161+2*1000)<40000,'linear reconstruction')
    require(Q(3,2)*(40000+1000)<64000,'cross-product perturbation')
    require(80+3*3*64000<600000,'block reconstruction')
    require(40000*e<1 and 120000*e<Q(1,10),'norm and orientation perturbations')
    require(120000/Q(2,5)/10==30000,'mean-value parameter bound')
    require(600000+(18+6*3)*30000<2000000,'whole configuration bound')
    require(10*2000000*e<=Q(1,400000),'local radius bridge')


def verify(raw=None):
    raw=json.loads((HERE/'model-functions.json').read_text()) if raw is None else raw
    # An independently fixed partition. No refinement timeout is a proof.
    functions,derivatives=audit_bounds(raw,16)
    audit_constants()
    sha=hashlib.sha256(json.dumps(raw,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return {'status':'VERIFIED','method':'centered Taylor rational intervals',
            'closed_subintervals':16,'rational_functions':functions,
            'model_derivatives':derivatives,'bound_manifest_sha256':sha,
            'production_arithmetic_imported':False,
            'prior_core_and_stress_rederived':False}


if __name__=='__main__': print(json.dumps(verify(),sort_keys=True,indent=2))
