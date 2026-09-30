#!/usr/bin/env python3
"""SymPy1.14 generator with independent Q(t) patch/residual derivation.

The generator reads no certificate, expected output, scratch input or network.
Four small extension seeds and two parameter intervals are checked by check.py.
"""
import json
import sympy as s
from sympy.polys.fields import field
from field import Field
from patches import models,unfolding,dot,sign_open,t
from geometry import branch_rat,branch_field
from polynomial import need,primitive
from check import CONTINUUM,nonedges
import parametric

SEEDS={
    (1,6,1):('small_cap',[0,1,2,7],[2,3,4]),
    (5,32,-1):('small_cap',[0,1,3,9],[3,4,5]),
    (7,31,-1):('single_unit_vertex',[0,1,2,11],None),
    (7,31,1):('small_cap',[0,1,3,7],[3,4,5]),
}


def generate():
    all_models=models();K,z=field('t',s.QQ);symbol=K.symbols[0]
    def casdot(x,y):
        return sum((x[i]*y[j]*(K.one if i==j else z) for i in range(3) for j in range(3)),K.zero)
    def from_coeff(p):
        return sum((K(c)*z**i for i,c in enumerate(p)),K.zero)
    def coords(edges,n):
        anchors,steps=unfolding(edges,n)
        points={v:[K.one if j==k else K.zero for j in range(3)] for k,v in enumerate(anchors)}
        for new,i,j,old in steps:
            points[new]=[2*z/(1+z)*(x+y)-w for x,y,w in zip(points[i],points[j],points[old])]
        return points
    active_polys={};mapping={};zeros=[]
    for m,model in enumerate(all_models):
        a=coords(model['A']['edges'],7);b=coords(model['B']['edges'],6)
        p,q=model['B']['ears'];kappa=casdot(b[p],b[q])
        need(kappa==from_coeff(model['B']['kappa'].n)/from_coeff(model['B']['kappa'].d),'independent B-ear Gram')
        forced={}
        for i,j,old in model['A']['candidates']:
            w=casdot(a[i],a[j])
            forced[(i,j,old)]=[2*z/(1+w)*(x+y)-v for x,y,v in zip(a[i],a[j],a[old])]
        for c,case in enumerate(model['cases']):
            u,v=forced[case['p']],forced[case['q']]
            residual=casdot(u,v)-kappa
            need(residual==from_coeff(case['residual'].n)/from_coeff(case['residual'].d),'independent CAS residual comparison')
            if not residual:
                zeros.append((m,c));continue
            polynomial=s.Poly(residual.numer.as_expr(),symbol,domain=s.QQ);relevant=[]
            for factor,multiplicity in s.factor_list(polynomial)[1]:
                factor=factor.clear_denoms()[1].primitive()[1]
                coeff=primitive(tuple(int(x) for x in reversed(factor.all_coeffs())))
                q=s.Poly.from_list(list(reversed(coeff)),symbol,domain=s.QQ)
                intervals=q.intervals(eps=s.Rational(1,10**30),inf=s.Rational(1,2),sup=s.Rational(3,5))
                intervals=[item for item in intervals if not (item[0][0]==item[0][1] and item[0][0] in (s.Rational(1,2),s.Rational(3,5)))]
                if intervals:
                    need(len(intervals)==1,'CAS factor root coverage')
                    (lo,hi),multiplicity=intervals[0]
                    active_polys[coeff]={'polynomial':list(coeff),'bracket':[[int(lo.p),int(lo.q)],[int(hi.p),int(hi.q)]]}
                    relevant.append(coeff)
            if relevant:
                need(len(relevant)==1,'multiple relevant factors')
                mapping[(m,c)]=relevant[0]
    coefficients=sorted(active_polys);indices={p:i for i,p in enumerate(coefficients)}
    result={'roots':[active_polys[p] for p in coefficients],
            'active':[[m,c,indices[p]] for (m,c),p in sorted(mapping.items())],
            'zero_witnesses':[],'root_witnesses':[],'extensions':[],'parametric':None}
    for m,c in zeros:
        model=all_models[m];case=model['cases'][c]
        for orientation in (-1,1):
            points=branch_rat(model,case,orientation)
            if (m,c,orientation)==CONTINUUM:
                result['parametric']=parametric.make_tables(points);continue
            pair=next((p for p in nonedges(case) if sign_open(dot(points[p[0]],points[p[1]])-t)==1),None)
            need(pair is not None,'zero branch lacks uniform witness')
            result['zero_witnesses'].append([m,c,orientation,list(pair)])
    for (m,c),factor in sorted(mapping.items()):
        entry=active_polys[factor];f=Field(factor,entry['bracket']);model=all_models[m];case=model['cases'][c]
        for orientation in (-1,1):
            points=branch_field(model,case,orientation,f)
            pair=next((p for p in nonedges(case) if f.sign(f.sub(f.dot(points[p[0]],points[p[1]]),f.t))>0),None)
            if pair is not None:
                result['root_witnesses'].append([m,c,orientation,list(pair)]);continue
            mode,tetra,normal=SEEDS[(m,c,orientation)]
            extension={'model':m,'case':c,'orientation':orientation,'mode':mode,'tetrahedron':tetra}
            if normal is not None:extension.update(normal_triple=normal,threshold=[4,3])
            result['extensions'].append(extension)
    need(len(coefficients)==5 and len(mapping)==12 and len(zeros)==13,'CAS scalar cover counts')
    need(len(result['zero_witnesses'])==25 and len(result['root_witnesses'])==20 and len(result['extensions'])==4 and result['parametric'] is not None,'branch cover counts')
    return result


if __name__=='__main__':
    print(json.dumps(generate(),indent=2,sort_keys=True))
