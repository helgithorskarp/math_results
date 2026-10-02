"""Independent universal Euclid/Newton audit of Lemma9398, stdlib only."""
from pathlib import Path
import hashlib
import importlib.util
import json
import signal
import sys
from fractions import Fraction as Q

spec = importlib.util.spec_from_file_location("own_exact_algebra", Path(__file__).with_name("algebra.py"))
alg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(alg)
P, vars, zero, mul, rem, trace, bernstein = alg.P, alg.vars, alg.zero, alg.mul, alg.rem, alg.trace, alg.bernstein


def cubic():
    a, b, c = vars(3)
    A, B, C = P(3, Q(-3, 8)), a/2, b/4
    r = [C, B, A, P(3, 1)]
    disc = A*A*B*B - 4*B**3 - 4*A**3*C - 27*C*C + 18*A*B*C
    # Explicit cubic Bezout inverse: r' V == disc (mod r).
    V = [A*A*B - 4*B*B + 3*A*C,
         2*A**3 - 7*A*B + 9*C, 2*A*A - 6*B]
    inverse = rem(mul([B, 2*A, P(3, 3)], V), r)
    for j, coef in enumerate(inverse):
        zero(coef - (disc if j == 0 else 0), "cubic derivative Bezout")
    # x^-1=-(x²+A x+B)/C, independently multiplied and checked.
    xv = rem(mul([B, A, P(3, 1)], V), r)
    invtest = rem(mul([P(3), B, 2*A, P(3, 3)], xv), r)
    for j, coef in enumerate(invtest):
        zero(coef + (C*disc if j == 0 else 0), "cubic x derivative Bezout")
    p = [c, b, a, P(3, Q(-1, 2)), P(3, 1)]
    massnum = [4*z for z in rem(mul(p, xv), r)]
    massden = C*disc
    squaredtrace = trace(rem(mul(massnum, massnum), r), r)
    numerator = 1024*c*c*massden**2 + 2*b*b*squaredtrace
    denominator = b*b*massden**2
    L = 256*a**3 - 18*a*a + 432*a*b + 864*b*b - 27*b
    H = 512*a**3 - 36*a*a + 736*a*b + 1344*b*b - 45*b
    U = 16*a*a-a+6*b
    W = 4096*a**4-512*a**3+7680*a*a*b+18*a*a-816*a*b+1440*b*b+27*b
    J = 8192*a**4-1024*a**3+13312*a*a*b+36*a*a-1376*a*b+2496*b*b+45*b
    V0 = 8192*a**4+13312*a*a*b-36*a*a+96*a*b+5184*b*b-45*b
    zero(disc + L/512, "cubic discriminant")
    expectednum = 1536*H*c*c-6144*U*b*b*c-W*b*b
    zero(numerator*(2*b*b*L)-expectednum*denominator, "entire cubic mass-square trace")
    zero(W*H+6144*b*b*U*U-L*J, "constant center elimination")
    zero(2*H+J-V0, "centered ratio numerator")
    F = 4*a*a+(15-112*a)*b
    G = 4*a*a*(64*a-5)+(208*a-15)*b
    zero(V0.diff(1)*H-V0*H.diff(1)-768*F*G, "complete b derivative factor")
    # Rational branch substitutions verified after homogeneous clearing.
    aa, = vars(1)
    def rational_sub(poly, bnum, bden):
        db = max((e[1] for e in poly.d), default=0)
        out = P(1)
        for (i,j,k), coeff in poly.d.items():
            if k:
                raise ValueError("branch unexpectedly depends on c")
            out += coeff*aa**i*bnum**j*bden**(db-j)
        return out, db
    bn, bd = -4*aa*aa, 15-112*aa
    vn, vd = rational_sub(V0, bn, bd)
    hn, hd = rational_sub(H, bn, bd)
    zero(-4*vn*bd**hd*(448*aa-45) + 4*(224*aa+15)*(32*aa-3)*hn*bd**vd,
         "F entire branch ratio")
    zero((-4*(224*aa+15)).diff(0)*(448*aa-45)-(-4*(224*aa+15))*448-67200,
         "F full moving branch derivative")
    gn, gd = -4*aa*aa*(64*aa-5), 208*aa-15
    ln, ld = rational_sub(L, gn, gd)
    T = 27648*aa*aa-4960*aa+225
    zero(-ln*256*gd**2+512*aa*aa*(32*aa-3)**2*T*gd**ld,
         "G cubic discriminant")
    zero(T-27648*(aa-Q(155,1728))**2-Q(275,108), "strict discriminant square")
    return {"mass_numerator": [z.record() for z in massnum], "mass_denominator":massden.record(),
            "Newton_squared_trace":squaredtrace.record(), "identity_terms":len(numerator.d),
            "derivative_factor_F":F.record(), "derivative_factor_G":G.record()}


def boundary():
    S,T = vars(2)
    A=-(3*S+2)/4;B=(S+2*T)/4
    q=[B,A,P(2,1)];disc=A*A-4*B
    # x q'(x) inverse follows from x^-1 and (q')²=disc.
    invnum=mul([A,P(2,1)],[A,P(2,2)])
    invtest=rem(mul([P(2),A,P(2,2)],invnum),q)
    for j,z in enumerate(invtest):zero(z+(B*disc if j==0 else 0),"quadratic Bezout")
    physicalnum=mul([P(2,-1),P(2,1)],[2*T-S,2-S])
    massnum=rem(mul(physicalnum,invnum),q);massden=B*disc
    squared=trace(rem(mul(massnum,massnum),q),q)
    etanum=1024*T*T*massden**2+2*(S+2*T)**2*squared
    etaden=(S+2*T)**2*massden**2
    s,w=vars(2);ts=s*s*(1-w)/4
    den=etaden.sub([s,ts]);num=etanum.sub([s,ts])
    K=(s-2)**2+8*s*s*w;V=(s-2)**2+2*s*s*w
    poly=(s-2)**4*(5*s*s-4*s+20)/4+s*(s-2)**2*(s+2)*(17*s*s+16*s-20)*w/2
    poly+=s*s*(21*s**4+816*s**3-744*s*s-1344*s+848)*w*w/4
    poly+=s**4*(-41*s*s-184*s+356)*w**3+26*s**6*w**4
    gapnum=(12*V-4*(s+2)**2)*den+num
    zero(gapnum*(s+2*ts)**2*K-2*s*s*poly*den,"complete boundary gap")
    cover=[(0,Q(1,2),0,1),(Q(1,2),1,0,Q(1,2)),(Q(1,2),1,Q(1,2),1),
           (1,Q(3,2),0,Q(1,4)),(1,Q(3,2),Q(1,4),Q(1,2)),
           (1,Q(3,2),Q(1,2),1),(Q(3,2),2,0,1)]
    u,v=vars(2)
    def certificates(p):
        rectangles=[]
        for lo,hi,left,right in cover:
            bs=bernstein(p.sub([lo+(hi-lo)*u,left+(right-left)*v]),(6,4))
            rectangles.append({"box":[str(z) for z in (lo,hi,left,right)],
                               "coefficients":[[list(k),str(z)] for k,z in bs.items()]})
        upper=p.sub([u+2,v]); upper_coeff=[]
        for j in range(5):
            bj=P(1)
            from math import comb
            for (i,k),z in upper.d.items():
                if k<=j:bj+=z*Q(comb(j,k),comb(4,k))*vars(1)[0]**i
            upper_coeff.append(bj)
        reconstructed=P(2)
        for j,bj in enumerate(upper_coeff):
            reconstructed+=bj.sub([u])*comb(4,j)*v**j*(1-v)**(4-j)
        zero(reconstructed-upper,"full upper Bernstein inverse")
        return rectangles,upper_coeff
    rectangles,upper=certificates(poly)
    if any(Q(z)<0 for r in rectangles for _,z in r['coefficients']):raise ValueError("negative original rectangle")
    if any(z<0 for p in upper for z in p.d.values()):raise ValueError("negative original upper coefficient")
    # Quantitative refinement: 24-C>delta iff 4P-delta Q>0.
    denominator_factor=(1+s*(1-w)/2)**2*V*K
    refinements=[]
    for delta in [Q(1,16),Q(1,8),Q(1,4),Q(1,2),Q(1),Q(2)]:
        refined=4*poly-delta*denominator_factor
        lower,ray=certificates(refined)
        all_lower=[Q(z) for r in lower for _,z in r['coefficients']]
        all_ray=[z for p in ray for z in p.d.values()]
        ok=min(all_lower)>=0 and min(all_ray)>=0
        refinements.append({"delta":str(delta),"certified_nonnegative":ok,
                            "lower_min":str(min(all_lower)),"upper_min":str(min(all_ray))})
        if ok:
            for r in lower[:6]:
                if min(Q(z) for _,z in r['coefficients'])<=0:raise ValueError("refinement strict first six")
            last=dict((tuple(k),Q(z)) for k,z in lower[-1]['coefficients'])
            if min(last[(0,0)],last[(0,4)])<=0:raise ValueError("refinement strict lower corners")
            if ray[0].d.get((6,),0)<=0 or ray[2].d.get((0,),0)<=0 or ray[4].d.get((0,),0)<=0:
                raise ValueError("refinement strict upper coverage")
            refinements[-1]['rectangles']=lower
            refinements[-1]['upper_polynomials']=[p.record() for p in ray]
    return {"mass_numerator":[z.record() for z in massnum],"mass_denominator":massden.record(),
            "Newton_squared_trace":squared.record(),"gap_polynomial":poly.record(),
            "rectangles":rectangles,"upper_polynomials":[p.record() for p in upper],
            "quantitative_refinements":refinements}


def run():
    return {"cubic":cubic(),"collision_boundary":boundary()}


def typed(expected, actual, where='root'):
    if type(expected) is not type(actual):
        raise ValueError('fixture type '+where)
    if isinstance(expected, dict):
        if set(expected)!=set(actual):raise ValueError('fixture fields '+where)
        for k in expected:typed(expected[k],actual[k],where+'.'+k)
    elif isinstance(expected,list):
        if len(expected)!=len(actual):raise ValueError('fixture length '+where)
        for j,(x,y) in enumerate(zip(expected,actual)):typed(x,y,where+'.'+str(j))
    elif expected!=actual:raise ValueError('fixture value '+where)


if __name__=='__main__':
    signal.alarm(45)
    rec=run()
    data=(json.dumps(rec,sort_keys=True,separators=(',',':'))+'\n').encode()
    if '--record' in sys.argv:
        sys.stdout.buffer.write(data)
    else:
        fp=Path(sys.argv[sys.argv.index('--expected')+1]) if '--expected' in sys.argv else Path(__file__).with_name('expected.json')
        fixture=json.loads(fp.read_text())
        typed(fixture,rec)
        print(json.dumps({'status':'PASS','bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
                          'refinements':[{k:v for k,v in x.items() if k not in ['rectangles','upper_polynomials']}
                                         for x in rec['collision_boundary']['quantitative_refinements']]}))
