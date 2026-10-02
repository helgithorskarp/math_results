#!/usr/bin/env python3
"""Exact certificates for the all-distinct angular stationary restriction.

Actual author six-sendov-2, researcher. CPython3.11 standard library only.
The universal statements are ordinary proofs in PROOF.md, not formalized by
finite checks. Rational polynomial/Sturm/dual helpers are adapted from the
same author's published constant-term reduction. No predecessor is imported.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import resource
import time


def require(value, message):
    if not value:
        raise ValueError(message)

def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p

def add(p, q):
    out = [Q(0)] * max(len(p), len(q))
    for i, x in enumerate(p):
        out[i] += x
    for i, x in enumerate(q):
        out[i] += x
    return trim(out)

def scale(p, c):
    return trim([x * c for x in p])

def mul(p, q):
    out = [Q(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i + j] += x * y
    return trim(out)

def derivative(p):
    return trim([i * x for i, x in enumerate(p)][1:] or [Q(0)])

def evaluate(p, x):
    out = Q(0)
    for c in reversed(p):
        out = out * x + c
    return out

def divide(p, q):
    p, q = trim(p), trim(q)
    require(q != [0], "zero polynomial divisor")
    out = [Q(0)] * max(1, len(p) - len(q) + 1)
    while p != [0] and len(p) >= len(q):
        i, c = len(p) - len(q), p[-1] / q[-1]
        out[i] += c
        p = add(p, scale([Q(0)] * i + q, -c))
    return trim(out), p

def sturm(p):
    out = [p, derivative(p)]
    while out[-1] != [0]:
        nxt = scale(divide(out[-2], out[-1])[1], -1)
        if nxt == [0]:
            break
        out.append(nxt)
    return out

def variations(chain, x):
    signs = [1 if y > 0 else -1 for p in chain if (y := evaluate(p, x))]
    return sum(a != b for a, b in zip(signs, signs[1:]))

def interval_add(a, b):
    return a[0] + b[0], a[1] + b[1]

def interval_mul(a, b):
    values = [x * y for x in a for y in b]
    return min(values), max(values)

def interval_scale(a, c):
    return (a[0] * c, a[1] * c) if c >= 0 else (a[1] * c, a[0] * c)

def interval_div(a, b):
    require(b[0] > 0 or b[1] < 0, "interval division through zero")
    return interval_mul(a, (1 / b[1], 1 / b[0]))

def interval_poly(p, x):
    out = (Q(0), Q(0))
    for c in reversed(p):
        out = interval_add(interval_mul(out, x), (c, c))
    return out

def interval_square(a):
    if a[0] <= 0 <= a[1]:
        return Q(0), max(a[0] ** 2, a[1] ** 2)
    return min(x * x for x in a), max(x * x for x in a)

def outward_dyadic(a, bits=160):
    """Exact directed rounding, keeping portable witness fixtures compact."""
    denominator = 1 << bits
    lower = (a[0].numerator * denominator) // a[0].denominator
    upper = -((-a[1].numerator * denominator) // a[1].denominator)
    result = Q(lower, denominator), Q(upper, denominator)
    require(result[0] <= a[0] <= a[1] <= result[1],
            "directed dyadic enclosure")
    return result

def encoded(x):
    if isinstance(x, Q):
        return str(x)
    if isinstance(x, dict):
        return {str(k): encoded(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [encoded(v) for v in x]
    return x

def monic(p):
    return scale(p, 1 / p[-1])

def gcd(p, q):
    while q != [0]:
        p, q = q, divide(p, q)[1]
    return monic(p)

def rem(p, h):
    return divide(p, h)[1]

def qm(p, q, h):
    return rem(mul(p, q), h)

def inverse(p, h):
    first, second = h, rem(p, h)
    u, v = [Q(0)], [Q(1)]
    while second != [0]:
        quotient, nxt = divide(first, second)
        first, second = second, nxt
        u, v = v, add(u, scale(mul(quotient, v), -1))
    require(len(first) == 1 and first[0] != 0, "polynomial is not invertible")
    out = rem(scale(u, 1 / first[0]), h)
    require(qm(out, p, h) == [Q(1)], "entire quotient inverse")
    return out

def trace_powers(h, n):
    d = len(h) - 1
    out, c = [Q(d)], list(reversed(h))
    for k in range(1, n + 1):
        if k <= d:
            value = -sum(c[j] * out[k-j] for j in range(1, k)) - k*c[k]
        else:
            value = -sum(c[j] * out[k-j] for j in range(1, d+1))
        out.append(value)
    return out

def trace(p, h):
    p = rem(p, h)
    return sum(x*y for x, y in zip(p, trace_powers(h, len(p)-1)))

def original_polynomial(u):
    require(len(u) == 8 and sum(u) == 0, "balanced eight original roots")
    f = [Q(1)]
    for x in u:
        f = mul(f, [-x, Q(1)])
    return f

def real_count(p):
    require(gcd(p, derivative(p)) == [Q(1)], "simple-root count input")
    chain = sturm(p)
    bound = 1 + max(abs(x) for x in p[:-1])
    require(evaluate(p, -bound) and evaluate(p, bound), "Sturm endpoints")
    return variations(chain, -bound) - variations(chain, bound)

def critical_nodes(u, h):
    # Each distinct original gap has one critical; each double original root
    # supplies one additional, inactive critical at the root itself.
    levels = sorted(set(u))
    require(all(u.count(x) <= 2 for x in levels), "simple critical spectrum")
    roots = [(x, x) for x in levels if u.count(x) == 2]
    for lo, hi in zip(levels, levels[1:]):
        for _ in range(155):
            mid = (lo+hi)/2
            value = sum(1/(x-mid) for x in u)
            if value < 0:
                lo = mid
            elif value > 0:
                hi = mid
            else:
                lo = hi = mid
                break
        require(all(not lo <= x <= hi for x in u), "secular enclosure pole")
        if lo != hi:
            require(sum(1/(x-lo) for x in u) < 0 <
                    sum(1/(x-hi) for x in u), "secular enclosure signs")
        else:
            require(evaluate(h, lo) == 0, "exact critical root")
        roots.append((lo, hi))
    roots.sort()
    require(len(roots) == 7 and all(roots[i][1] < roots[i+1][0]
            for i in range(6)), "seven disjoint critical enclosures")
    chain = sturm(h)
    for lo, hi in roots:
        require((lo == hi and evaluate(h, lo) == 0) or
                (lo < hi and variations(chain, lo)-variations(chain, hi) == 1),
                "independent Sturm critical isolation")
    return roots

def direct_mass(u, node):
    if node[0] == node[1] and u.count(node[0]) == 2:
        return Q(0), Q(0)
    total = (Q(0), Q(0))
    for x in u:
        inv = interval_div((Q(1), Q(1)), (x-node[1], x-node[0]))
        total = interval_add(total, interval_square(inv))
    return interval_div((Q(64), Q(64)), total)

def overlaps(a, b):
    return max(a[0], b[0]) <= min(a[1], b[1])

def rejected(action, text):
    try:
        action()
    except ValueError as error:
        require(text in str(error), "unexpected negative-control failure")
        return str(error)
    raise ValueError("damaged mathematical control accepted")

class Dual:
    """Exact first-order algebra Q[epsilon]/(epsilon^2), no finite differences."""
    def __init__(self, value, slope=0):
        self.value, self.slope = Q(value), Q(slope)

    @staticmethod
    def coerce(x):
        return x if isinstance(x, Dual) else Dual(x)

    def __add__(self, other):
        x = self.coerce(other)
        return Dual(self.value+x.value, self.slope+x.slope)

    __radd__ = __add__

    def __neg__(self):
        return Dual(-self.value, -self.slope)

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) + (-self)

    def __mul__(self, other):
        x = self.coerce(other)
        return Dual(self.value*x.value,
                    self.slope*x.value+self.value*x.slope)

    __rmul__ = __mul__

    def __truediv__(self, other):
        x = self.coerce(other)
        require(x.value != 0, "dual unit divisor")
        return Dual(self.value/x.value,
                    (self.slope*x.value-self.value*x.slope)/x.value**2)

    def __rtruediv__(self, other):
        return self.coerce(other)/self

    def __eq__(self, other):
        x = self.coerce(other)
        return self.value == x.value and self.slope == x.slope

def dual_polynomial(p, q):
    return [Dual(p[i] if i < len(p) else 0, q[i] if i < len(q) else 0)
            for i in range(max(len(p),len(q)))]

def data(f):
    require(len(f)==9 and f[-1]==1 and f[-2]==0,"monic balanced octic")
    h=scale(derivative(f),Q(1,8))
    ih=inverse(derivative(h),h)
    m=scale(qm(f,ih,h),-8)
    eta=trace(qm(m,m,h),h)
    n=-2*f[6]
    d=Q(3,8)*n*n-4*f[4]
    s3=-3*f[5]
    require(n>0 and d>0,"positive norm and angular denominator")
    require(trace(m,h)==n and
            trace(qm(m,[0,1],h),h)==s3 and
            trace(qm(m,[0,0,1],h),h)==d,"first three spectral moments")
    a=qm(derivative(derivative(h)),ih,h)
    b=add(qm(a,a,h),scale(qm(derivative(derivative(derivative(h))),ih,h),-1))
    b1=add(qm([0,1],b,h),scale(a,-1))
    b2=add(add(qm([0,0,1],b,h),scale(qm([0,1],a,h),-2)),[Q(-2)])
    require([trace(qm(m,x,h),h) for x in [b,b1,b2]]
            ==[Q(336),Q(0),22*n],"all three universal heat trace identities")
    weighted=[trace(qm(qm(m,m,h),x,h),h) for x in [b,b1,b2]]
    return h,ih,m,eta,n,d,s3,(n*n-eta)/d,a,b,weighted


def dual_variation(f,q,base):
    h,ih,m,eta,n,d,s3,c,a,b,weighted=base
    hp=derivative(h)
    t,r=divide(mul(ih,hp),h)
    require(r==[Q(1)],"inverse Bezout quotient")
    h1=scale(derivative(q),Q(1,8))
    corr=scale(qm(ih,add(qm(ih,derivative(h1),h),
                       scale(qm(h1,t,h),-1)),h),-1)
    hd=dual_polynomial(h,h1)
    invd=dual_polynomial(ih,corr)
    require(qm(invd,derivative(hd),hd)==[Dual(1)],
            "moving dual inverse")
    fd=dual_polynomial(f,q)
    md=scale(qm(fd,invd,hd),-8)
    ed=Dual.coerce(trace(qm(md,md,hd),hd))
    nd=-2*fd[6]
    dd=Q(3,8)*nd*nd-4*fd[4]
    cd=(nd*nd-ed)/dd
    require((ed.value,nd.value,dd.value,cd.value)==(eta,n,d,c),
            "entire dual variation base values")
    return nd.slope,dd.slope,ed.slope,cd.slope


def heat_variations(f,base):
    h,ih,m,eta,n,d,s3,c,a,b,weighted=base
    radial=add([0]+derivative(f),scale(f,-8))
    records=[]
    for aa,bb,cc in [(Q(0),Q(0),Q(1)),(Q(0),Q(1),Q(0)),
                     (Q(1),Q(0),Q(0)),(Q(2),Q(-3),Q(5))]:
        w=[cc,bb,aa]
        q=add(add(mul(w,derivative(derivative(f))),scale(f,-56*aa)),
              scale(derivative(f),-7*bb))
        require(len(q)<=7,"balanced raw heat degree")
        nf=-26*aa*n-112*cc
        df=-44*aa*d-3*aa*n*n-20*bb*s3-24*cc*n
        ef=-128*(aa*d+bb*s3+cc*n)+2*sum(
            x*y for x,y in zip((cc,bb,aa),weighted))
        cf=(aa*((128+44*c)*d+(3*c-52)*n*n-2*weighted[2])
           +bb*((128+20*c)*s3-2*weighted[1])
           +cc*(24*n*(c-4)-2*weighted[0]))/d
        exact=dual_variation(f,q,base)
        require(exact==(nf,df,ef,cf),"entire dual versus moving heat formulas")
        qfixed=add(q,scale(radial,-(13*aa+56*cc/n)))
        require(len(qfixed)<=6,"fixed norm heat tangent degree")
        fixed=dual_variation(f,qfixed,base)
        require(fixed[0]==0 and fixed[3]==cf,
                "exact radial cancellation and scale invariant derivative")
        records.append({"w":w,"q_raw":q,"q_fixed_norm":qfixed,
                        "raw_N_D_eta_C_slopes":exact,
                        "fixed_N_D_eta_C_slopes":fixed})
    return records


def node_checks(u,base):
    h,ih,m,eta,n,d,s3,c,a,b,weighted=base
    nodes=critical_nodes(u,h)
    masses=[];curvatures=[]
    for j,node in enumerate(nodes):
        s1=(Q(0),Q(0));s2=(Q(0),Q(0))
        for k,other in enumerate(nodes):
            if k==j:continue
            inv=interval_div((Q(1),Q(1)),(node[0]-other[1],node[1]-other[0]))
            s1=interval_add(s1,inv)
            s2=interval_add(s2,interval_square(inv))
        direct_a=interval_scale(s1,2)
        direct_b=interval_add(interval_square(s1),interval_scale(s2,3))
        quotient_a=interval_poly(a,node)
        quotient_b=interval_poly(b,node)
        require(overlaps(direct_a,quotient_a) and overlaps(direct_b,quotient_b),
                "critical-curvature direct versus quotient enclosures")
        require(direct_b[0]>0 and quotient_b[0]>0,
                "positive critical heat curvature")
        ratio=interval_div(interval_square(direct_a),direct_b)
        require(ratio[1]<Q(8,3),"strict six-reciprocal Cauchy curvature bound")
        dm=direct_mass(u,node)
        require(dm[0]>0 and overlaps(dm,interval_poly(m,node)),
                "positive masses and independent original-pole enclosures")
        masses.append(outward_dyadic(dm))
        curvatures.append({"A_direct":outward_dyadic(direct_a),
                           "A_quotient":outward_dyadic(quotient_a),
                           "B_direct":outward_dyadic(direct_b),
                           "B_quotient":outward_dyadic(quotient_b),
                           "A_squared_over_B":outward_dyadic(ratio)})
    return nodes,masses,curvatures


def scalar_constants():
    threshold=Q(24531,1000);q0=Q(81,100)
    poly=lambda c,q:(768+208*c)*q*q-(768+48*c)*q-9*c*c+128*c
    require(poly(threshold,0)<0 and poly(threshold,q0)<0,
            "high stationarity exact mass threshold")
    require(288-18*threshold<0,"threshold polynomial monotonic in C")
    dmax=(1-q0*q0-(1-q0)**2/6)/threshold
    require(dmax==Q(20273,1471860) and dmax<Q(69,5000),
            "quartic variance bound")
    require(Q(7,8)*Q(69,5000)<Q(11,100)**2,
            "original squared magnitude bound")
    require(Q(3,200)>Q(3,25)**2 and Q(47,200)<Q(1,2)**2,
            "rational signed original boxes")
    require(Q(1,8)*Q(3,200)>Q(17,400)**2,
            "signed uniform denominator lower bound")
    require(Q(3,200)+Q(1,8)+2*Q(17,400)==Q(9,40),
            "uniform distance denominator")
    require(Q(69,5000)/Q(9,40)==Q(23,375)<Q(1,16),
            "sign-imbalance distance contradiction")
    require(Q(15)<Q(31,8)**2 and 2-Q(31,16)==Q(1,16),
            "four plus four sign count")
    require(Q(69,5000)/q0<Q(2,15)**2 and Q(2,15)-Q(3,25)==Q(1,75)
            and Q(1,75)<Q(9,80),"central dominant critical gap")
    require(q0/64==Q(9,80)**2,"original pole distance")
    return {"threshold":threshold,"max_mass_fraction_lower":q0,
            "P_at_threshold_and_zero":poly(threshold,0),
            "P_at_threshold_and_q0":poly(threshold,q0),
            "normalized_D_strict_upper":dmax}


def stationary_domain(u):
    require(len(u)==8 and sum(u)==0 and len(set(u))==8,
            "eight distinct original roots required for two-sided stationarity")


def verify():
    records={"scalar_constants":scalar_constants()}
    bases={};polys={}
    for name,values in [
        ("symmetric_distinct",(-7,-5,-3,-1,1,3,5,7)),
        ("asymmetric_distinct",(-8,-6,-3,-1,2,3,5,8)),
        ("high_nonstationary",(-856,-854,-852,-850,412,998,1000,1002))]:
        u=list(map(Q,values));stationary_domain(u)
        f=original_polynomial(u);base=data(f)
        bases[name]=base;polys[name]=f
        nodes,masses,curvatures=node_checks(u,base)
        hv=heat_variations(f,base)
        h,ih,m,eta,n,d,s3,c,a,b,weighted=base
        maximum_box=(max(x[0] for x in masses),max(x[1] for x in masses))
        bound_box=interval_add(interval_scale(maximum_box,Q(80,3)*n),
                               (-Q(14,3)*eta,-Q(14,3)*eta))
        require(weighted[2]<bound_box[0],
                "independent mass enclosure verifies universal M2 upper bound")
        record={"u":u,"N":n,"D":d,"C":c,"weighted_heat_traces":weighted,
                "critical_enclosures":nodes,"mass_enclosures":masses,
                "curvature_enclosures":curvatures,
                "M2_upper_bound_margin":outward_dyadic(interval_add(
                    bound_box,(-weighted[2],-weighted[2]))),
                "heat_variations":hv}
        if name=="high_nonstationary":
            require(c>Q(24531,1000) and maximum_box[1]<Q(81,100)*n,
                    "dropping stationarity is contradicted by a feasible high profile")
            require(any(r["raw_N_D_eta_C_slopes"][3]!=0 for r in hv),
                    "high false-stationarity profile exact gradient")
        records[name]=record
    u=list(map(Q,(-7,-5,-3,-1,1,3,5,7)))
    f=original_polynomial(u)
    centered=add(f,[-Q(1294848,280993)])
    require(real_count(centered)==8,"genuinely feasible centered polynomial")
    bc=data(centered)
    const=dual_variation(centered,[Q(1)],bc)
    require(const[3]==0,"genuinely centered exact constant derivative")
    hv=heat_variations(centered,bc)
    cf=hv[0]["fixed_N_D_eta_C_slopes"][3]
    require(cf>0,"centered polynomial heat derivative is positive")
    dt=Q(1,1000)
    step=add(centered,scale(hv[0]["q_fixed_norm"],dt))
    require(real_count(step)==8,"literal legal coefficient step")
    bs=data(step)
    require(bs[4]==bc[4]==168 and bs[7]>bc[7],
            "strict norm-preserving improvement")
    require(bc[7]==Q(2522064,280993),"centered benchmark exact C")
    records["centered_improving_step"]={
        "original_symmetric_roots":u,"constant_center":-Q(1294848,280993),
        "centered_polynomial":centered,"centered_C":bc[7],
        "constant_direction_slope":const[3],"heat_variations":hv,
        "signed_step":dt,"improved_polynomial":step,"norm_before_after":bs[4],
        "improved_C":bs[7],"exact_improvement":bs[7]-bc[7],
        "eight_distinct_real_originals_before_and_after":True}
    # A simple critical spectrum does not make these directions two-sided
    # feasible at original doubles. The literal positive heat step loses roots.
    doubles=list(map(Q,(-3,-3,-2,-1,1,2,3,3)))
    fd=original_polynomial(doubles);bd=data(fd)
    require(gcd(bd[0],derivative(bd[0]))==[Q(1)],
            "double-original control has seven simple critical roots")
    dh=heat_variations(fd,bd)
    dstep=add(fd,scale(dh[0]["q_fixed_norm"],Q(1,1000)))
    count=real_count(dstep)
    require(count<8,"positive heat step is not feasible at original doubles")
    records["original_double_domain_control"]={
        "u":doubles,"f":fd,"critical_polynomial":bd[0],
        "heat_variations":dh,"positive_step":Q(1,1000),
        "positive_step_real_root_count":count}
    alpha=(Q(-853410556973738,10**15),Q(-853410556973736,10**15))
    quartic=list(map(Q,(746,4737,11175,11695,4575)))
    require(evaluate(quartic,alpha[0])*evaluate(quartic,alpha[1])<0 and
            variations(sturm(quartic),alpha[0])-
            variations(sturm(quartic),alpha[1])==1,
            "credited algebraic three-level optimizer interval")
    n0=interval_poly([Q(12),Q(24),Q(20)],alpha)
    s4=interval_add(interval_add(interval_scale(
        interval_square(interval_square(alpha)),4),(Q(3),Q(3))),
        interval_square(interval_square(interval_poly([Q(-3),Q(-4)],alpha))))
    d0=interval_add(interval_div(s4,interval_square(n0)),(-Q(1,8),-Q(1,8)))
    require(d0[0]>Q(707,50000),"three-level orbit quartic gap")
    require(Q(707,50000)-Q(20273,1471860)>4*Q(1,11000),
            "strict interior stationary orbit separation")
    records["three_level_orbit_variance"]={
        "credited_alpha_interval":alpha,"normalized_D_enclosure":outward_dyadic(d0),
        "normalized_D_lower":Q(707,50000),
        "high_stationary_distance_strict_lower":Q(1,11000)}
    hb,ihb,mb,etab,nb,db,s3b,cb,ab,bb,wb=bc
    q=hv[0]["q_fixed_norm"]
    frozen_eta=(-16*trace(qm(qm(mb,q,hb),ihb,hb),hb)-
                Q(1,4)*trace(qm(qm(qm(mb,mb,hb),
                derivative(derivative(q)),hb),ihb,hb),hb))
    raw=add(mul([Q(1)],derivative(derivative(centered))),
            scale(add([0]+derivative(centered),scale(centered,-8)),-Q(7,nb)))
    high=records["high_nonstationary"]
    records["negative_controls"]={
        "wrong_residue_factor":rejected(lambda:require(
            trace(scale(mb,Q(1,8)),hb)==nb,"residue normalization"),
            "residue normalization"),
        "wrong_heat_curvature":rejected(lambda:require(
            trace(qm(mb,qm(ab,ab,hb),hb),hb)==336,
            "missing curvature term"),"missing curvature term"),
        "omit_critical_motion":rejected(lambda:require(
            dual_variation(centered,q,bc)[2]==frozen_eta,
            "critical-motion contribution"),"critical-motion contribution"),
        "wrong_fixed_norm_factor":rejected(lambda:require(
            len(raw)<=6,"fixed-norm tangent degree"),
            "fixed-norm tangent degree"),
        "critical_simple_is_not_original_simple":rejected(
            lambda:stationary_domain(doubles),"eight distinct original roots"),
        "drop_stationarity":rejected(lambda:require(
            max(Q(x[1]) for x in high["mass_enclosures"])>
            Q(81,100)*high["N"],"false mass concentration"),
            "false mass concentration")}
    return encoded(records)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--expected",type=Path)
    parser.add_argument("--write-fixture",type=Path)
    args=parser.parse_args()
    start=time.monotonic()
    records=verify()
    if args.expected:
        require(json.loads(args.expected.read_text())==records,
                "entire external fixture differs")
    if args.write_fixture:
        args.write_fixture.write_text(json.dumps(records,indent=2,sort_keys=True)+"\n")
    digest=hashlib.sha256(json.dumps(records,sort_keys=True,
                         separators=(",",":")).encode()).hexdigest()
    print(json.dumps({"status":"checked","records":len(records),
        "curvature_nodes_independently_enclosed":21,
        "heat_variations_dual_and_root_motion":40,
        "mathematical_negative_controls":6,"record_sha256":digest,
        "elapsed_seconds":time.monotonic()-start,
        "peak_rss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))


if __name__=="__main__":
    main()
