#!/usr/bin/env python3
"""Optional SymPy1.14 generator, with independent Q(t) residual derivation.

No certificate, expected output, coordinates, scratch or network is read.
The stdlib checker certifies coverage, divisors, roots and witness signs.
"""
import json
import sympy as s
from sympy.polys.fields import field
from field import Field
from patches import models,unfolding,dot,sign_open,t
from geometry import branch_rat,branch_field
from polynomial import need,primitive
from check import nonedges


def generate():
    all_models=models();K,z=field('t',s.QQ);symbol=K.symbols[0]
    def casdot(x,y):
        return sum((x[i]*y[j]*(K.one if i==j else z) for i in range(3) for j in range(3)),K.zero)
    def from_coeff(p):
        return sum((K(c)*z**i for i,c in enumerate(p)),K.zero)
    def convert(r):return from_coeff(r.n)/from_coeff(r.d)
    def coords(edges,n):
        anchors,steps=unfolding(edges,n)
        points={v:[K.one if j==k else K.zero for j in range(3)] for k,v in enumerate(anchors)}
        for new,i,j,old in steps:
            points[new]=[2*z/(1+z)*(x+y)-w for x,y,w in zip(points[i],points[j],points[old])]
        return points
    active={};zeros=[];independent={}
    for m,model in enumerate(all_models):
        a=coords(model['A']['edges'],model['n']);b=coords(model['B']['edges'],5)
        p,q=model['B']['ears'];kappa=casdot(b[p],b[q])
        need(kappa==convert(model['B']['kappa']),'independent B-ear Gram')
        forced={}
        for i,j,old in model['A']['candidates']:
            w=casdot(a[i],a[j])
            forced[(i,j,old)]=[2*z/(1+w)*(x+y)-v for x,y,v in zip(a[i],a[j],a[old])]
        independent[m]=(a,b,forced,kappa)
        for c,case in enumerate(model['cases']):
            u,v=forced[case['p']],forced[case['q']]
            residual=casdot(u,v)-kappa
            need(residual==convert(case['residual']),'independent CAS residual comparison')
            if not residual:zeros.append((m,c));continue
            polynomial=s.Poly(residual.numer.as_expr(),symbol,domain=s.QQ);relevant=[]
            for factor,multiplicity in s.factor_list(polynomial)[1]:
                factor=factor.clear_denoms()[1].primitive()[1]
                coeff=primitive(tuple(int(x) for x in reversed(factor.all_coeffs())))
                qpoly=s.Poly.from_list(list(reversed(coeff)),symbol,domain=s.QQ)
                intervals=qpoly.intervals(inf=s.Rational(1,2),sup=s.Rational(3,5))
                intervals=[item for item in intervals if not (item[0][0]==item[0][1] and item[0][0] in (s.Rational(1,2),s.Rational(3,5)))]
                if intervals:
                    need(coeff==(-1,0,3) and len(intervals)==1,'CAS factor root coverage')
                    relevant.append(coeff)
            if relevant:
                need(len(relevant)==1,'multiple relevant factors');active[(m,c)]=0
    root={'polynomial':[-1,0,3],'bracket':[[57735,100000],[57736,100000]]}
    result={'roots':[root],'active':[[m,c,r] for (m,c),r in sorted(active.items())],
            'zero_witnesses':[],'root_witnesses':[]}

    # Independently compute the two frames in SymPy's rational function field.
    def casframe(m,c,orientation):
        model=all_models[m];case=model['cases'][c]
        a,b,forced,kappa=independent[m];u,v=forced[case['p']],forced[case['q']]
        p,q=model['B']['ears']
        def cross(x,y):return [x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],x[0]*y[1]-x[1]*y[0]]
        hi=[[((1/(1-z)) if i==j else K.zero)-z/((1-z)*(1+2*z)) for j in range(3)] for i in range(3)]
        raw=cross(u,v)
        normal=[sum((x*y for x,y in zip(row,raw)),K.zero) for row in hi]
        bnormal=cross(b[p],b[q]);den=1-kappa*kappa;points=dict(a)
        for j,x in b.items():
            d1,d2=casdot(x,b[p]),casdot(x,b[q])
            c1,c2=(d1-kappa*d2)/den,(d2-kappa*d1)/den
            magnitude=(1-z)**2*(1+2*z)*sum((x0*y0 for x0,y0 in zip(x,bnormal)),K.zero)/den
            points[j+model['n']]=[c1*x0+c2*y0+orientation*magnitude*n0 for x0,y0,n0 in zip(u,v,normal)]
        return points
    def reduce_root(r):
        modulus=s.Poly(3*symbol**2-1,symbol,domain=s.QQ)
        num=s.Poly(r.numer.as_expr(),symbol,domain=s.QQ).rem(modulus)
        den=s.Poly(r.denom.as_expr(),symbol,domain=s.QQ).rem(modulus)
        return (num*s.invert(den,modulus)).rem(modulus)
    for m,c in zeros:
        model=all_models[m];case=model['cases'][c]
        for orientation in (-1,1):
            points=branch_rat(model,case,orientation)
            pair=next((p for p in nonedges(case) if sign_open(dot(points[p[0]],points[p[1]])-t)==1),None)
            need(pair is not None,'zero branch lacks uniform witness')
            other=casframe(m,c,orientation)
            need(casdot(other[pair[0]],other[pair[1]])==convert(dot(points[pair[0]],points[pair[1]])),'independent zero witness Gram')
            result['zero_witnesses'].append([m,c,orientation,list(pair)])
    f=Field(root['polynomial'],root['bracket'])
    for m,c in sorted(active):
        model=all_models[m];case=model['cases'][c]
        for orientation in (-1,1):
            points=branch_field(model,case,orientation,f)
            pair=next((p for p in nonedges(case) if f.sign(f.sub(f.dot(points[p[0]],points[p[1]]),f.t))>0),None)
            need(pair is not None,'root branch lacks packing witness')
            other=casframe(m,c,orientation)
            gram=f.dot(points[pair[0]],points[pair[1]])
            expression=sum((s.Rational(x.numerator,x.denominator)*symbol**i for i,x in enumerate(gram)),s.Integer(0))
            need(reduce_root(casdot(other[pair[0]],other[pair[1]]))==s.Poly(expression,symbol,domain=s.QQ),'independent isolated witness Gram')
            result['root_witnesses'].append([m,c,orientation,list(pair)])
    need(len(active)==3 and len(zeros)==7 and len(result['zero_witnesses'])==14 and len(result['root_witnesses'])==6,'CAS cover counts')
    return result


if __name__=='__main__':
    print(json.dumps(generate(),indent=2,sort_keys=True))
