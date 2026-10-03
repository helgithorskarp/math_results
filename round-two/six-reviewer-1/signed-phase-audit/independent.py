"""Fresh exact signed-phase reconstruction. CPython 3.12+, stdlib only.

Written target proof was exposed; native executable/data were unopened
when this primary file was written. No campaign executable kernel imported.
The universal analytic bridges are in PROOF.md, not certified by examples.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb, factorial
import argparse
import hashlib
import json


def need(ok, message):
    if not ok:
        raise ValueError(message)


def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(obj):
    return hashlib.sha256(canon(obj).encode()).hexdigest()


def integral_beta(n, m):
    # Integrate all coefficients of s^n(1-s)^m, rather than evaluate beta.
    return sum((Q((-1)**j * comb(m, j), n+j+1) for j in range(m+1)), Q(0))


def mul(a, b):
    out = [Q(0)] * (len(a)+len(b)-1)
    for j, x in enumerate(a):
        for k, y in enumerate(b):
            out[j+k] += x*y
    return out


def cmul(a, b):
    return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])


def cadd(a, b):
    return (a[0]+b[0], a[1]+b[1])


def coeffs_gaussian(z):
    # Full univariate eight-factor convolution, retaining all nine coefficients.
    p = [(Q(1), Q(0))]
    for w in z:
        new = [(Q(0), Q(0)) for _ in range(len(p)+1)]
        for j, v in enumerate(p):
            new[j] = cadd(new[j], v)
            new[j+1] = cadd(new[j+1], cmul(v, (-w[0], -w[1])))
        p = new
    # Separate subset-product route.
    subset = []
    for k in range(9):
        total = (Q(0), Q(0))
        for I in combinations(range(8), k):
            term = (Q((-1)**k), Q(0))
            for j in I:
                term = cmul(term, z[j])
            total = cadd(total, term)
        subset.append(total)
    need(p == subset, "complete Gaussian coefficient routes")
    O = tuple(9*sum((p[k][j]/Q(k+1) for k in range(9)), Q(0)) for j in range(2))
    return p, O


def endpoint(r, d, b, lam):
    sigma = r+d
    rms = {str(k): (8-k)*b[k]**2-sigma**2 for k in b}
    need(all(x >= 0 for x in rms.values()), "whole-path rms scale")
    g = Q(1,8)-sum((Q(j+1,8)*b[1]**j for j in range(1,8)), Q(0))
    h = sum((Q((j+1)*(j+2),56)*b[2]**j for j in range(1,7)), Q(0))
    c = Q(1,56)-Q(7,2)*h
    D4 = sum((Q(comb(j+4,4),70)*b[4]**j for j in range(5)), Q(0))
    D6 = sum((Q(comb(j+6,6),28)*b[6]**j for j in range(3)), Q(0))
    upper, lower = 2*(1+r), 2*(1-r)-d
    tail = Q(70,64)*D4*upper**2*d+Q(28,512)*D6*upper**3*d**2+upper**4*d**3/Q(4096)
    A = g+c*lower-tail
    need(g > 0 and c > 0 and lower > 0 and A > lam, "signed whole-degree endpoint")
    return {"rho": r, "delta": d, "scales": {str(k): v for k,v in b.items()},
            "lambda": lam, "rms_margins": rms, "g": g, "h": h, "c": c,
            "D4": D4, "D6": D6, "sminus": lower, "splus": upper,
            "tail": tail, "A": A, "gap": A-lam}


TABLES = [
    (Q(1,16),Q(1,1000),{1:Q(1,40),2:Q(13,500),4:Q(127,4000),6:Q(9,200)},Q(1,8)),
    (Q(1,40),Q(1,1000),{1:Q(1,100),2:Q(1,94),4:Q(13,1000),6:Q(19,1000)},Q(7,48)),
    (Q(1,16),Q(1,200),{1:Q(13,500),2:Q(7,250),4:Q(27,800),6:Q(6,125)},Q(1,8)),
    (Q(1,40),Q(1,200),{1:Q(23,2000),2:Q(1,80),4:Q(3,200),6:Q(11,500)},Q(7,48)),
]


def stringify(obj):
    if isinstance(obj, Q):
        return str(obj)
    if isinstance(obj, dict):
        return {str(k): stringify(v) for k,v in obj.items()}
    if isinstance(obj, (tuple, list)):
        return [stringify(v) for v in obj]
    return obj


def reconstruct(damage=None):
    general = {}
    shift = {}
    for k in range(9):
        shift[str(k)] = Q((-1)**k, comb(8,k))
        need(9*(-1)**k*integral_beta(k,8-k) == shift[str(k)], "all shifted coefficients")
        for n in range(k,9):
            # Direct c_k(a) integration versus expansion of all original subset terms.
            x = Q(9*(-1)**n*comb(8-k,n-k),n+1)
            y = Q(9*(-1)**n,n+1)*Q(comb(n,k)*comb(8,n),comb(8,k))
            if damage == "general-a" and (k,n)==(0,8):
                y += 1
            need(x==y, "all 45 general-a coefficients")
            general[f"{k},{n}"] = x
    majorants = {}
    for k in range(1,9):
        for j in range(9-k):
            left = Q(comb(8-k,j),comb(8,k+j))
            right = Q(factorial(k+j),factorial(k)*factorial(j)*comb(8,k))
            if damage == "majorant" and (k,j)==(1,7):
                right += 1
            need(left==right, "all 36 mixed-majorant coefficients")
            majorants[f"{k},{j}"] = left
    phase = {}
    order_counts = {str(k):0 for k in (2,4,6,8)}
    for choices in product(range(3), repeat=8):
        X = tuple(j for j,v in enumerate(choices) if v==1)
        I = tuple(j for j,v in enumerate(choices) if v==2)
        ell, n = len(I), len(X)+len(I)
        if ell not in (2,4,6,8):
            continue
        # Direct real part of eight-factor (1-s-sx-isy) integration.
        direct = -9*(-1)**n*(-1)**(ell//2)*integral_beta(n,8-n)
        # Independent distinct-derivative identity in shifted c_n polynomial.
        derivative = (-1)**(ell//2+1)*Q((-1)**n,comb(8,n))
        if damage == "phase-eight" and ell==8:
            derivative = -derivative
        if damage == "phase-four" and ell==4 and not X:
            derivative = -derivative
        need(direct==derivative, "entire signed even-phase map")
        key = f"{sum(1<<j for j in X)},{sum(1<<j for j in I)}"
        phase[key] = direct
        order_counts[str(ell)] += 1
    need(order_counts=={"2":1792,"4":1120,"6":112,"8":1} and len(phase)==3025,
         "complete ternary phase census")
    tables = []
    for index,(r,d,b,lam) in enumerate(TABLES):
        b = dict(b)
        if damage == "path-rms" and index==2:
            b[4] = Q(1,100)
        if damage == "endpoint" and index==3:
            lam = Q(1,6)
        tables.append(endpoint(r,d,b,lam))
    gaps = [
        Q(437216828764786061067429,57344000000000000000000000),
        Q(63390354751011315568145616079,18543699714785280000000000000000),
        Q(310956569766254566817161,57344000000000000000000000),
        Q(6821627179148116880351,5376000000000000000000000),
    ]
    need([t['gap'] for t in tables]==gaps, "all original and enlarged exact endpoint gaps")
    e = Q(1,12000)
    amin, H0 = 1-e, Q(1,320)
    f0 = amin-Q(7,125)
    tau, tstar = Q(1,50), Q(13,15)*e
    f1 = amin-tstar-tau
    h1 = 5+8*Q(169,225)*e
    Yfactor = (Q(8,3)+h1/f1)/amin**2
    actual = {
        "amin": amin, "f0":f0,"f1":f1,"h1":h1,"Yfactor":Yfactor,
        "broad_root_margin":Q(7,125)**2-H0,
        "broad_rms_margin":Q(1,16)**2-H0/f0**2,
        "phase_margin":Q(1,1000)-Q(17,2)*e,
        "zero_sum_radius_margin":tau**2-Q(7,8)*5*e,
        "fine_rms_margin":Q(1,40)**2-h1*e/f1**2,
        "imaginary_sum_margin":8-Yfactor,
        "conditional_phase_factor":Q(8,7)/Q(7,48),
    }
    need(all(actual[k]>0 for k in actual if k.endswith('margin')), "actual application margins")
    need(f0==Q(11327,12000) and f1==Q(44093,45000) and h1==Q(1687669,337500), "actual denominators")
    need(Yfactor==Q(49334956800000,6348333812093) and actual['conditional_phase_factor']==Q(384,49), "entire reciprocal remainder and conditional division")
    # Direct bivariate expansion of ((1-s)^2+2ds)^4; retain the full s polynomial at every d degree.
    paired = {}
    base = {(0,0):Q(1),(1,0):Q(-2),(2,0):Q(1),(1,1):Q(2)}
    pol = {(0,0):Q(1)}
    for _ in range(4):
        new = {}
        for (j,k),x in pol.items():
            for (u,v),y in base.items():
                key = (j+u,k+v)
                new[key] = new.get(key,Q(0))+x*y
        pol = {key:v for key,v in new.items() if v}
    for (j,k),v in pol.items():
        paired[f"{j},{k}"] = v
    balanced = [sum((9*v/Q(j+1) for (j,k),v in pol.items() if k==degree),Q(0)) for degree in range(5)]
    need(balanced==[Q(1),Q(9,7),Q(72,35),Q(24,5),Q(144,5)], "entire balanced-family integrated polynomial")
    need(balanced[1]/8==Q(9,56), "limiting signed curvature")
    # A phase-cap deletion counterexample, with no claim of actual disk feasibility.
    bad = [(-Q(1),Q(0))]+[(Q(1),Q(0))]*7
    _, Obad = coeffs_gaussian(bad)
    need(Obad==(Q(5,4),Q(0)) and 1-Obad[0]>-Q(7,48)*2, "cap deletion refuted")
    return {"shift":shift,"general_a":general,"majorants":majorants,"phase":phase,
            "phase_order_counts":order_counts,"tables":tables,"actual":actual,
            "paired_product":paired,"balanced_integral":balanced,
            "curvature_barrier":Q(9,56),"cap_deletion":{"O":Obad,"Delta":Q(2),"Y":Q(0),"rho_squared":Q(0)}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--damage',choices=['general-a','majorant','phase-eight','phase-four','path-rms','endpoint'])
    ap.add_argument('--summary',action='store_true')
    args = ap.parse_args()
    r = stringify(reconstruct(args.damage))
    if args.summary:
        r = {"whole_record_sha256":digest(r),"whole_record_bytes":len(canon(r).encode()),
             "maps":{k:{"entries":len(r[k]),"sha256":digest(r[k])} for k in ('shift','general_a','majorants','phase','paired_product')},
             "phase_order_counts":r['phase_order_counts'],"tables":r['tables'],"actual":r['actual'],
             "balanced_integral":r['balanced_integral'],"curvature_barrier":r['curvature_barrier'],"cap_deletion":r['cap_deletion']}
    print(canon(r))


if __name__=='__main__':
    main()
