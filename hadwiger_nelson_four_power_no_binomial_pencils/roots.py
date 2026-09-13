"""Two exact affine decompositions over Q; neither discards nonreal roots."""
import importlib.util
from interface import A,OLD
spec=importlib.util.spec_from_file_location('cubic_anchor_field_euclid',OLD/'verify.py')
V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)


def resultant(left,right,x,y,s):
    f,g=[A.expression(p,x,y) for p in (left,right)]
    R=A.sp.Poly(A.sp.resultant(f,g,y),x,domain=A.sp.QQ)
    A.need(not R.is_zero,'nonzero anchor resultant')
    out=[]
    for q0,_ in A.sp.factor_list(R)[1]:
        qx=A.primitive(q0,x)
        q=V.fmpq_poly([V.fmpq(v) for v in A.coefficients(qx)])
        h=V.outer_gcd(V.fiber(left,q),V.fiber(right,q),q)
        A.need(h,'unsupported whole vertical component')
        if len(h)==1:continue
        if qx.degree()==1:
            x0=-qx.nth(0)/qx.nth(1)
            hy=A.sp.Poly(sum(A.sp.Rational(str(a[0]))*y**j for j,a in enumerate(h)),y)
            for h0,_ in A.sp.factor_list(hy)[1]:
                qy=A.primitive(h0.as_expr().subs(y,s),s)
                out.append(A.encode(qy,A.sp.Poly(x0,s,domain=A.sp.QQ),A.sp.Poly(s,s,domain=A.sp.QQ),s))
        else:
            A.need(len(h)==2 and h[1]==V.fmpq_poly([1]),'unsupported nonlinear nonrational fiber')
            qq=A.sp.Poly(qx.as_expr().subs(x,s),s,domain=A.sp.QQ)
            yy=A.sp.Poly(sum(-A.sp.Rational(str(v))*s**i for i,v in enumerate(h[0].coeffs())),s,domain=A.sp.QQ)
            out.append(A.encode(qq,A.sp.Poly(s,s,domain=A.sp.QQ),yy,s))
    return sorted(out,key=A.digest)


def groebner(left,right,x,y,s):
    return sorted([A.encode(q,xx,yy,s) for q,xx,yy in A.groebner_components(A.expression(left,x,y),A.expression(right,x,y),x,y,s)],key=A.digest)


def nreal(field):
    s=A.sp.Symbol('s');q=A.sp.Poly(sum(A.sp.Rational(t)*s**i for i,t in enumerate(field['q'])),s)
    A.need(q.is_irreducible,'irreducible component field')
    return int(q.count_roots(-A.sp.oo,A.sp.oo))
