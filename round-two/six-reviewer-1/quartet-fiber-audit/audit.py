"""Independent dense QQ derivation for LEMMA10200. No producer import.

CPython 3.12; SymPy 1.14.0. Exact Sturm counts, no numerical root search.
The surrounding compactness/IFT/root-count proof is in REVIEW.md.
"""
import argparse
import itertools
import json
import math
import sys
import sympy as sy

Z, S, T, U, A, B, d, t, s, a, b, x = sy.symbols("z S T U A B d t s a b x")
record = {"schema": "six-reviewer-1/quartet-fiber/1", "identities": {},
          "polynomials": {}, "bernstein": {}, "root_controls": {}}


def poly(p):
    vs = tuple(sorted(p.free_symbols, key=str))
    if not vs:
        vs = (Z,)
    q = sy.Poly(sy.expand(p), *vs, domain=sy.QQ)
    return {"variables": list(map(str, vs)), "terms": [
        {"powers": list(m), "coefficient": str(c)} for m, c in q.terms()]}


def eq(name, left, right):
    ln, ld = sy.cancel(left).as_numer_denom()
    rn, rd = sy.cancel(right).as_numer_denom()
    den = sy.lcm(ld, rd)
    l = sy.cancel(ln * den / ld)
    r = sy.cancel(rn * den / rd)
    if sy.expand(l - r) != 0:
        raise ValueError("identity failure: " + name)
    record["identities"][name] = {
        "left": poly(l), "right": poly(r), "clearing_denominator": poly(den)}


def moments(f, z, limit):
    cs = sy.Poly(f, z).all_coeffs()
    n = len(cs) - 1
    if cs[0] != 1:
        raise ValueError("Newton recurrence needs monic polynomial")
    p = [sy.Integer(n)]
    for j in range(1, limit + 1):
        val = sum(cs[i] * p[j-i] for i in range(1, min(j, n+1)))
        if j <= n:
            val += j * cs[j]
        p.append(sy.expand(-val))
    return p


def bernstein(name, p):
    q = sy.Poly(sy.expand(p.subs(x, x/4)), x, domain=sy.QQ)
    n = q.degree()
    vals = [sum(q.nth(j) * sy.Rational(math.comb(i,j), math.comb(n,j))
                for j in range(i+1)) for i in range(n+1)]
    if any(v <= 0 for v in vals):
        raise ValueError("closed Bernstein positivity: " + name)
    rebuilt = sum(vals[i]*math.comb(n,i)*x**i*(1-x)**(n-i)
                  for i in range(n+1))
    eq("Bernstein reconstruction " + name, rebuilt, q.as_expr())
    record["bernstein"][name] = {"interval": ["0", "1/4"],
        "polynomial": poly(p), "coefficients": list(map(str, vals))}


def variations(vals):
    signs = [sy.sign(v) for v in vals if v != 0]
    return sum(a != b for a,b in zip(signs, signs[1:]))


def root_control(name, f, intervals, expected_count):
    f = sy.Poly(f, Z, domain=sy.QQ)
    chain = sy.sturm(f.as_expr(), Z)
    if sy.degree(sy.gcd(f.as_expr(), f.diff().as_expr()), Z) != 0:
        raise ValueError("control roots are not all simple")
    vinf = variations([sy.LC(sy.Poly(p,Z)) for p in chain])
    vzero = variations([p.subs(Z,0) for p in chain])
    count = vzero - vinf
    if count != expected_count:
        raise ValueError("complete positive root count " + name)
    brackets = []
    for lo, hi in intervals:
        flo, fhi = f.eval(lo), f.eval(hi)
        v1 = variations([p.subs(Z,lo) for p in chain])
        v2 = variations([p.subs(Z,hi) for p in chain])
        if not (lo > 0 and hi > lo and flo*fhi < 0 and v1-v2 == 1):
            raise ValueError("exact isolated positive root " + name)
        brackets.append({"lo": str(lo), "hi": str(hi),
                         "values": [str(flo),str(fhi)], "root_count": v1-v2})
    record["root_controls"][name] = {"coefficients": list(map(str,f.all_coeffs())),
        "sturm_chain": [poly(p) for p in chain], "positive_root_count": count,
        "brackets": brackets, "moments_1_3_5": [str(moments(f.as_expr(),Z,5)[k])
                                                  for k in (1,3,5)]}


def build(damage=None):
    # Defining roots and elementary coefficients, not a producer certificate.
    roots = sy.symbols("a1 a2 a3 a4")
    es = [sy.Integer(1)] + [sum(sy.prod(v) for v in itertools.combinations(roots,j))
                            for j in range(1,5)]
    f = sy.prod(Z-r for r in roots)
    pm = moments(f,Z,5)
    for j in (1,3,5):
        eq("root Newton moment " + str(j), pm[j], sum(r**j for r in roots))
    for i,root in enumerate(roots):
        eq("root derivative product "+str(i),sy.diff(f,Z).subs(Z,root),
           sy.prod(root-other for j,other in enumerate(roots) if j!=i))
    pairprod = sy.prod(roots[i]+roots[j] for i in range(4) for j in range(i+1,4))
    eq("whole Orlando six-pair product", pairprod,
       es[1]*es[2]*es[3]-es[3]**2-es[1]**2*es[4])
    q = Z**2-S*Z-T/S
    R = -T**2-S**2*U
    g = Z**4-S*Z**3+A*Z**2-(S*A+T)*Z+U-T*A/S
    gm = moments(g,Z,5)
    for k,v in {1:S,3:S**3+3*T,5:S**5+5*S**2*T-5*S*U}.items():
        eq("pencil odd moment " + str(k), gm[k], v)
    eq("pencil factor decomposition",g,q*(Z**2+A+T/S)-R/S**2)
    eq("pencil invariant R",S*A*(S*A+T)-(S*A+T)**2-S**2*(U-T*A/S),R)
    K = S**3+3*T
    eq("direction discriminant", sy.discriminant(q,Z),(4*K-S**3)/(3*S))
    psi=R/(S**2*q)-Z**2-T/S
    eq("level polynomial",g,q*(A-psi))
    eq("level first derivative",sy.diff(psi,Z),R*(S-2*Z)/(S**2*q**2)-2*Z)
    H0=Z*q**2/(S-2*Z)
    N=-8*Z**3+9*S*Z**2-3*S**2*Z-T
    if damage=="critical-cubic":N+=Z
    eq("three-branch derivative",sy.diff(H0,Z),q*N/(S-2*Z)**2)
    eq("three-branch cubic derivative",sy.diff(N,Z),-3*(4*Z-S)*(2*Z-S))
    for label,at,v in [("zero",0,-T),("quarter",S/4,(S**3-16*K)/48),
                       ("half",S/2,(S**3-4*K)/12)]:
        eq("critical cubic " + label,N.subs(Z,at),v)
    record["polynomials"]["critical_cubic"]=poly(N)
    # Complete original octic, normalization and changing even coefficients.
    mid=S**2/2-sy.Rational(1,4)
    gb=g.subs(A,mid)
    octic=sy.expand((gb+d*q)*(gb.subs(Z,-Z)-d*q.subs(Z,-Z)))
    h=S*mid+T;v=U-T*mid/S
    J=d*R/(4*S)
    if damage=="odd-octic":J*=2
    E=(mid**2+2*v-2*S*h-d**2)/2
    G=(2*mid*v-h**2+d**2*(S**2+2*T/S))/4
    c=v**2-d**2*(T/S)**2
    expected=Z**8-Z**6/2+2*E*Z**4+4*G*Z**2+8*J*Z+c
    for i in range(9):
        eq("original octic coefficient " + str(i),
           sy.expand(octic).coeff(Z,i),sy.expand(expected).coeff(Z,i))
    om=moments(octic,Z,8)
    for i in (1,2,3,5):
        eq("full original moment " + str(i),om[i],int(i==2))
    eq("fourth-moment displacement",om[4]-om[4].subs(d,0),4*d**2)
    for i in range(9):record["polynomials"]["original_moment_"+str(i)]=poly(sy.cancel(om[i]*S**8))
    # Regular support multiplier/Hessian and dependent-support openings.
    lam=5*(a*a+b*b)/3;mu=-5*a*a*b*b
    eq("multiplier factor",5*x**4-3*lam*x*x-mu,5*(x*x-a*a)*(x*x-b*b))
    eq("constraint minor",3*b*b-3*a*a,3*(b*b-a*a))
    eq("lower Hessian",(20*x**3-6*lam*x).subs(x,a),10*a*(a*a-b*b))
    eq("upper Hessian",(20*x**3-6*lam*x).subs(x,b),10*b*(b*b-a*a))
    for k in (2,3):
        cen=1-x/k;delta=(k-k*cen**3-x**3)/(6*cen)
        if damage=="dependent-opening" and k==3:delta+=x*x
        cubic=k*cen**3+6*cen*delta+x**3
        fifth=k*cen**5+20*cen**3*delta+10*cen*delta**2+x**5
        eq(f"opening{k} first moment",k*cen+x,k)
        eq(f"opening{k} third moment",cubic,k)
        eq(f"opening{k} first fifth derivative",sy.diff(fifth,x).subs(x,0),5)
        vals={"delta2":delta/x,"positivity":cen**2-delta,"gain":(fifth-k)/x}
        for label,expr in vals.items():
            num,den=sy.cancel(expr).as_numer_denom()
            if den.subs(x,0)<0:num,den=-num,-den
            bernstein(f"opening{k} {label} numerator",num)
            bernstein(f"opening{k} {label} denominator",den)
    eq("triple Jensen gap",16*(3*t**3+s**3)-(3*t+s)**3,3*(s-t)**2*(5*s+7*t))
    eq("triple upper gap",(3*t+s)**3-(3*t**3+s**3),3*t*(8*t*t+9*t*s+3*s*s))
    eq("triple lower-branch boundary gap",(3*t+s)**3-9*(3*t**3+s**3),s*(27*t*t+9*t*s-8*s*s))
    # The indispensable fifth moment: exact quadratic field, never a decimal sign.
    v57=sy.Symbol("v57")
    aa=(47-3*v57)/32;bb=(-29+9*v57)/32
    reduce57=lambda p:sy.rem(sy.expand(p),v57**2-57,v57)
    for i in (1,3):eq("omitted fifth control moment "+str(i),
        reduce57(3*aa**i+bb**i),3+sy.Rational(1,2)**i)
    eq("omitted fifth control difference",reduce57(3+sy.Rational(1,2)**5-3*aa**5-bb**5),
       (14592015-1946835*v57)/262144)
    # Literal controls include the zero endpoint, double endpoints and singleton.
    base=sy.prod(Z-i for i in range(1,5));q0=Z*Z-10*Z+30
    for sign in (-1,1):root_control("distinct fiber "+str(sign),base+sign*q0/1000,
        [(sy.Rational(i)-sy.Rational(1,100),sy.Rational(i)+sy.Rational(1,100))for i in range(1,5)],4)
    zero=Z*(Z-1)*(Z-2)*(Z-3)+(Z*Z-6*Z+10)/1000
    root_control("excluded zero boundary",Z*(Z-1)*(Z-2)*(Z-3),
        [(sy.Rational(i)-sy.Rational(1,100),sy.Rational(i)+sy.Rational(1,100))for i in range(1,4)],3)
    # Explicit brackets for every root, including the formerly zero original.
    root_control("open zero boundary interior",zero,
        [(sy.Rational(1,10000),sy.Rational(1,100))]+
        [(sy.Rational(i)-sy.Rational(1,100),sy.Rational(i)+sy.Rational(1,100))for i in range(1,4)],4)
    dub=(Z-1)**2*(Z-2)**2;q2=Z*Z-6*Z+10
    root_control("two-double interior",dub-q2/1000,
        [(sy.Rational(9,10),sy.Rational(1)),(sy.Rational(1),sy.Rational(11,10)),
         (sy.Rational(19,10),sy.Rational(2)),(sy.Rational(2),sy.Rational(21,10))],4)
    root_control("outside two-double endpoint",dub+q2/1000,[],0)
    tri=(Z-1)**3*(Z-2);q3=Z*Z-5*Z+sy.Rational(38,5)
    for sign in (-1,1):root_control("outside triple singleton "+str(sign),tri+sign*q3/1000,[],2)
    # Only the inherited, relevant all-distinct Schur step, not a whole10105 verdict.
    EE,GG,JJ=sy.symbols("E G J")
    critical=Z**7-sy.Rational(3,8)*Z**5+EE*Z**3+GG*Z+JJ
    tr=moments(critical,Z,10)
    MA=sy.Matrix([[tr[i+j]for j in (0,2,4)]for i in (0,2,4)])
    MB=sy.Matrix([[tr[i+j]for j in (1,3,5)]for i in (1,3,5)])
    coupling=sy.Matrix([[tr[i+j]for j in (1,3,5)]for i in (0,2,4)])
    Umat=sy.Matrix([[0,0,0],[0,0,-7],[0,-7,-sy.Rational(27,8)]])
    for i in range(3):
        for j in range(3):
            eq(f"parity coupling {i}{j}",coupling[i,j],JJ*Umat[i,j])
            if sy.diff(MA[i,j],JJ)!=0 or sy.diff(MB[i,j],JJ)!=0:
                raise ValueError("even blocks depend on J")
    # w=0 gives y=( -5/7,8,0 ); the first two normal equations are impossible for D>0.
    y0=sy.Matrix([-sy.Rational(5,7),8,0])
    uvec=sy.Matrix([1,sy.Rational(3,8)-8*EE,sy.Rational(9,64)-4*EE-24*GG])
    eq("wzero first normal",(MA*y0-uvec)[0],0)
    eq("wzero second normal",(MA*y0-uvec)[1],sy.Rational(75,56)-24*EE)
    eq("wzero forced negative variance",sy.Rational(3,8)-8*sy.Rational(25,448),-sy.Rational(1,14))
    for i in range(11):record["polynomials"]["critical_trace_"+str(i)]=poly(tr[i])
    return record


def main():
    p=argparse.ArgumentParser();p.add_argument("--output");p.add_argument("--expected")
    p.add_argument("--damage",choices=["critical-cubic","odd-octic","dependent-opening"])
    args=p.parse_args();result=build(args.damage)
    raw=(json.dumps(result,sort_keys=True,separators=(",",":"))+"\n").encode()
    if args.expected:
        from pathlib import Path
        if Path(args.expected).read_bytes()!=raw:raise ValueError("entire record bytes mismatch")
    if args.output:
        from pathlib import Path
        Path(args.output).write_bytes(raw)
    import hashlib
    print(json.dumps({"sha256":hashlib.sha256(raw).hexdigest(),"bytes":len(raw),
        "identities":len(result["identities"]),"whole_polynomials":len(result["polynomials"]),
        "bernstein_vectors":len(result["bernstein"]),"root_controls":len(result["root_controls"]),
        "python":sys.version.split()[0],"sympy":sy.__version__},sort_keys=True))


if __name__=="__main__":main()
