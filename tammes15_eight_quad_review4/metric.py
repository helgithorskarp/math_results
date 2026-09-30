"""Independent Q(c) metric audit using SymPy fields and exact Sturm signs."""
import json
from fractions import Fraction
import sympy as sp
from sympy.polys.fields import field
from sympy.polys.domains import QQ

K, c = field('c', QQ)
X = sp.Symbol('c')
L, H = sp.Rational(1, 2), sp.Rational(3, 5)
Z, ONE = K.zero, K.one
sign_records = {}
identities = 0
coordinate_checks = 0
coordinate_endpoint_zeros = 0


def require(ok, text):
    if not ok:
        raise ValueError(text)


def polynomial(a):
    return sp.Poly(sum(sp.Rational(str(v)) * X ** m[0] for m, v in a.items()), X, domain=sp.QQ)


def strict_polynomial(a, lo=L, hi=H):
    p = polynomial(a)
    require(not p.is_zero, 'zero sign polynomial')
    q = p
    endpoint_multiplicities = []
    for endpoint in (lo, hi):
        multiplicity = 0
        factor = sp.Poly(X-endpoint, X, domain=sp.QQ)
        while q.degree() and q.eval(endpoint) == 0:
            q, remainder = q.div(factor)
            require(remainder.is_zero, 'endpoint division')
            multiplicity += 1
        endpoint_multiplicities.append(multiplicity)
    seq = q.sturm()
    def variation(point):
        signs = [int(sp.sign(f.eval(point))) for f in seq]
        signs = [v for v in signs if v]
        return sum(a != b for a, b in zip(signs, signs[1:]))
    v0, v1 = variation(lo), variation(hi)
    require(v0 == v1, 'interior polynomial root')
    sign = int(sp.sign(p.eval((lo+hi)/2)))
    require(sign in (-1, 1), 'midpoint sign')
    return {'coefficients': [str(p.nth(i)) for i in range(p.degree()+1)],
            'sign': sign, 'Sturm_variations': [v0, v1],
            'endpoint_root_multiplicities': endpoint_multiplicities,
            'endpoint_signs': [int(sp.sign(p.eval(e))) for e in (lo, hi)]}


def certify(value, name, wanted=None, lo=L, hi=H):
    n, d = strict_polynomial(value.numer, lo, hi), strict_polynomial(value.denom, lo, hi)
    sign = n['sign']*d['sign']
    if wanted:
        require(sign == wanted, 'wrong strict rational sign: '+name)
    record = {'interval': [str(lo), str(hi)], 'sign': sign, 'numerator': n, 'denominator': d}
    sign_records[name] = record
    return record


def equal(a, b, text):
    global identities
    require(a == b, text)
    identities += 1


def dot(a, b):
    return (ONE-c)*sum((x*y for x, y in zip(a, b)), Z)+c*sum(a,Z)*sum(b,Z)


def unit(a):
    equal(dot(a, a), ONE, 'unit')


def reflect(a, b, old):
    for v in (a, b, old): unit(v)
    for x, y in ((a,b),(a,old),(b,old)):equal(dot(x,y),c,'reflection contacts')
    v = tuple(2*c/(ONE+c)*(x+y)-z for x,y,z in zip(a,b,old))
    unit(v)
    for x in (a,b):equal(dot(v,x),c,'new reflection contacts')
    return v


def opposite(f, a, b, name):
    for v in (f,a,b):unit(v)
    for x in (a,b):equal(dot(f,x),c,'old opposite contacts')
    divisor = ONE+dot(a,b)
    certify(divisor, name+'_construction_divisor', 1)
    v = tuple(2*c/divisor*(x+y)-z for x,y,z in zip(a,b,f))
    unit(v)
    for x in (a,b):equal(dot(v,x),c,'new opposite contacts')
    return v


def third(a,b,s):
    unit(a);unit(b);equal(dot(a,b),c,'third edge')
    u=(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
    total=sum(u,Z)
    v=tuple((c*(x+y)+s*((ONE+2*c)*z-c*total))/(ONE+c) for x,y,z in zip(a,b,u))
    unit(v)
    for x in (a,b):equal(dot(v,x),c,'third contacts')
    return v


def audit(coords, tag):
    global coordinate_checks, coordinate_endpoint_zeros
    for i,v in coords.items():
        unit(v)
        for j,a in enumerate(v):
            result = strict_polynomial(a.denom)
            coordinate_checks += 1
            coordinate_endpoint_zeros += sum(result['endpoint_root_multiplicities'])


def run():
    global identities, coordinate_checks, coordinate_endpoint_zeros
    identities = coordinate_checks = coordinate_endpoint_zeros = 0
    sign_records.clear()
    base={0:(ONE,Z,Z),1:(Z,ONE,Z),2:(Z,Z,ONE)}
    for new,a,b,old in [(3,0,2,1),(4,0,3,2),(5,0,4,3)]:
        base[new]=reflect(base[a],base[b],base[old])
    base[12]=opposite(base[0],base[1],base[5],'A_Q')
    audit(base,'base')
    leaves=[]
    for s in (-1,1):
        coords=dict(base);coords[14]=third(coords[1],coords[12],s);audit(coords,'R')
        if s==-1:
            gap=c-dot(coords[5],coords[14]);certify(gap,'R_negative_5_14',-1)
            certify(gap+K(1)/1000,'R_negative_margin_1_1000',-1)
            expected=(-4*c-12*c**2+12*c**3+28*c**4-24*c**5)/(1+c)**4
            equal(gap,expected,'first printed gap')
            leaves.append({'R_seed':s,'forbidden_pair':[5,14]});continue
        coords[6]=tuple(2*c*x-y for x,y in zip(coords[14],coords[1]))
        coords[13]=tuple(2*c*x-y for x,y in zip(coords[14],coords[12]))
        for i in (6,13):unit(coords[i]);equal(dot(coords[i],coords[14]),c,'halfturn edge')
        equal(dot(coords[6],coords[13]),c,'second free triangle')
        coords[8]=opposite(coords[14],coords[12],coords[6],'R_Q');audit(coords,'Bbase')
        for b in (-1,1):
            work=dict(coords);work[7]=third(work[6],work[8],b)
            if b==-1:
                gap=c-dot(work[7],work[12]);certify(gap,'B_negative_7_12',-1)
                certify(gap+K(1)/1000,'B_negative_margin_1_1000',-1)
                equal(gap,-(1-c)**2*(1+2*c)/(1+c),'second printed gap')
                pair=[7,12]
            else:
                work[9]=reflect(work[7],work[8],work[6]);work[10]=reflect(work[7],work[9],work[8])
                gap=c-dot(work[4],work[10]);certify(gap,'B_positive_4_10',-1)
                certify(gap+K(1)/1000,'B_positive_margin_1_1000',-1)
                n=1+7*c+8*c**2-52*c**3-158*c**4-90*c**5+160*c**6+416*c**7+661*c**8+315*c**9-128*c**10-340*c**11-800*c**12
                d=1+6*c+12*c**2+12*c**3+22*c**4+40*c**5+28*c**6+20*c**7+49*c**8+50*c**9+16*c**10
                equal(gap,n/d,'third printed gap');pair=[4,10]
            audit(work,'terminal');leaves.append({'R_seed':s,'B_seed':b,'forbidden_pair':pair})
    return {'agent':'six-reviewer-4','role':'independent mathematical reviewer','sympy_version':sp.__version__,
            'field':'Q(c), characteristic zero; exact rational polynomial normalization',
            'identities':identities,'coordinate_denominator_checks':coordinate_checks,
            'coordinate_endpoint_zeros':coordinate_endpoint_zeros,
            'leaves':leaves,'strict_Sturm_certificates':dict(sign_records)}


if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
