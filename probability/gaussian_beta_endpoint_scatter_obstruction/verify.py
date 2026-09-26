"""Exact endpoint obstruction for b_(7,0), not a majorisation counterexample.

Two formulations of replica enumeration, integer square-root enclosures, and
an exact Gamma-concentration certificate. No numerical Gaussian integrals.
"""
from collections import defaultdict
from fractions import Fraction as F
from math import comb,isqrt
from pathlib import Path
import hashlib,json

ROOT=Path(__file__).resolve().parent


def require(ok,why):
    if not ok: raise ArithmeticError(why)


def reduce_root(m):
    a=1
    for k in range(1,isqrt(m)+1):
        if m%(k*k)==0:a=k
    return a,m//(a*a)


def add(out,key,value):
    out[key]=out.get(key,F(0))+value
    if not out[key]:del out[key]


def spectrum(ordered=False):
    """Exact coefficients in Q(sqrt2,sqrt3,sqrt5,sqrt7), before exp(-tau*a)."""
    ans={};work=0
    for m in range(2,10):
        a,d=reduce_root(m)
        c=F(8*(-1)**(m-2)*comb(7,m-2)*a,m**3*(m-1))
        # c*sqrt(d) equals 8(-1)^(m-2)binom(7,m-2)/(m(m-1))*m^(-3/2).
        target=ans.setdefault(F(0),{});add(target,d,c)
        if ordered:
            counts=defaultdict(int)
            for mask in range(1<<m):
                coords=[1 if mask>>i&1 else -1 for i in range(m)]
                scatter=F(sum((coords[i]-coords[j])**2 for i in range(m) for j in range(i)),2*m)
                counts[scatter]+=1;work+=1
        else:
            counts=defaultdict(int)
            for r in range(m+1):
                counts[F(2*r*(m-r),m)]+=comb(m,r);work+=1
        for t,n in counts.items():
            add(ans.setdefault(t,{}),d,-c*F(n,1<<m))
    return {t:v for t,v in ans.items() if v},work


def A_at(spec,t):
    out={}
    for rate,vec in spec.items():
        if rate<t:
            for d,c in vec.items():add(out,d,c*(t-rate))
    return out


def enclosure(vec,scale=10**12):
    lo=hi=F(0)
    for d,c in vec.items():
        q=isqrt(d*scale*scale)
        a,b=F(q,scale),F(q+1,scale)
        if q*q==d*scale*scale:b=a
        require(a*a<=d<=b*b,'root enclosure')
        lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
    return lo,hi


def encode(vec):
    return {str(d):str(c) for d,c in sorted(vec.items())}


def compute():
    spec,n1=spectrum(False);other,n2=spectrum(True)
    require(spec==other,'binomial versus ordered-replica spectrum')
    total={}
    for vec in spec.values():
        for d,c in vec.items():add(total,d,c)
    require(not total,'nonzero total scatter mass')
    explicit={1:F(31667,15552),2:F(1663,3072),3:F(-28,27),5:F(-7,10),6:F(217,648),7:F(-3,28)}
    require(A_at(spec,F(4,3))==explicit,'closed radical formula')
    knot_lo,knot_hi=enclosure(explicit)
    require(F(-23,1000)<knot_lo<=knot_hi<F(-22,1000),'closed radical sign bounds')
    points=[F(33,25),F(4,3),F(27,20)]
    internal=sorted(t for t in spec if points[0]<t<points[-1])
    require(internal==[F(4,3)],'unaccounted scatter knot in negative window')
    values=[]
    for t in points:
        v=A_at(spec,t);lo,hi=enclosure(v)
        require(hi<F(-1,125),'negative interval not certified')
        values.append({'t':str(t),'radical_coefficients':encode(v),'interval':[str(lo),str(hi)]})
    # Uniform bound |A(t)|<=sum |nu_a|a <=4 sum binom(7,m-2)/m^(5/2)<128.
    # Use sqrt(m)>=1: denominator m^(5/2)>=m^2>=4.
    upper=sum(F(4*comb(7,m-2),m*m) for m in range(2,10))
    require(upper<128,'global absolute bound')
    order=2**28;mean=F(267,200);radius=F(3,200)
    chebyshev=mean*mean/(radius*radius*(order+1))
    expectation_upper=F(-1,125)+(128+F(1,125))*chebyshev
    require(expectation_upper<0,'Gamma certificate fails')
    return {'schema':'endpoint_scatter_obstruction_v1','beta_N':7,'beta_j':0,
            'source':[[-1,0,0],[1,0,0]],'target':[[0,0,0],[0,0,0]],'weights':['1/2','1/2'],
            'variance_parameter':'s=1/tau, tau>0','binomial_terms':n1,'ordered_replica_terms':n2,
            'distinct_scatter_knots':len(spec),'total_scatter_mass':{},
            'negative_window':['33/25','27/20'],'A_upper_bound_on_window':'-1/125',
            'knot_certificates':values,'global_absolute_A_bound':'128',
            'rational_intermediate_absolute_bound':str(upper),
            'derivative_witness':{'function':'b_(7,0)(tau)/tau^2','order':order,
                'evaluation_tau':str(F(order+1,1)/mean),'gamma_mean':str(mean),
                'gamma_radius':str(radius),'outside_probability_upper':str(chebyshev),
                'normalized_derivative_upper':str(expectation_upper)},
            'actual_beta_sign':'strictly positive for every tau>0, by Jensen; not evaluated numerically'}


def check_record(cert):
    require(cert==compute(),'certificate mismatch')


def reject_record(cert):
    try:check_record(cert)
    except ArithmeticError:return
    raise ArithmeticError('damaged certificate accepted')


def controls(cert):
    bad=json.loads(json.dumps(cert));bad['knot_certificates'][1]['radical_coefficients']['2']='0'
    reject_record(bad)
    bad=json.loads(json.dumps(cert));bad['derivative_witness']['order']=0
    reject_record(bad)
    bad=json.loads(json.dumps(cert));bad['negative_window'][1]='2'
    reject_record(bad)
    for d in [2,3,5,6,7]:
        lo,hi=enclosure({d:F(1)});require(lo*lo<d<hi*hi,'irrational root bounds')
    return 3


if __name__=='__main__':
    expected=json.loads((ROOT/'CERTIFICATE.json').read_text())
    actual=compute();check_record(expected)
    n=controls(actual)
    out={'status':'ENDPOINT_SCATTER_OBSTRUCTION_EXACT_PASS','ordered_replica_terms':actual['ordered_replica_terms'],
         'binomial_terms':actual['binomial_terms'],'scatter_knots':actual['distinct_scatter_knots'],
         'negative_window':actual['negative_window'],'damage_controls':n,
         'certificate_sha256':hashlib.sha256((ROOT/'CERTIFICATE.json').read_bytes()).hexdigest()}
    reference=json.loads((ROOT/'EXPECTED.json').read_text());require(out==reference,'expected record mismatch')
    print(json.dumps(out,sort_keys=True,indent=2))
