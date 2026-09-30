#!/usr/bin/env python3
"""SymPy1.14 generator: independent Q(t) residuals, factors and root brackets.

The six short extension proof seeds specify tetrahedra and cap normals;
the checker proves their validity and exhaustively enumerates each polytope.
No certificate, coordinates, scratch output or network input is read.
"""
from fractions import Fraction
import json
import sympy as s
from sympy.polys.fields import field
from field import Field
from family import (models,branch_rat,branch_field,dot,sign_open,t,REF,
                    one,zero)
from polynomial import F,ROOT_LO,ROOT_HI,need,primitive
from check import nonedges

SEEDS={
    (0,7,-1):('saturated',[0,1,2,12],None),
    (0,24,1):('small_cap',[0,1,3,12],[2,3,4]),
    (4,5,1):('small_cap',[0,1,2,8],[1,2,3]),
    (4,7,-1):('single_unit_vertex',[0,1,3,8],None),
    (4,12,-1):('single_unit_vertex',[0,1,3,9],None),
    (6,7,1):('small_cap',[0,1,2,8],[0,5,6])}


def generate():
    all_models=models()
    K,z=field('t',s.QQ)
    symbol=K.symbols[0]
    def casdot(x,y):
        return sum((x[i]*y[j]*(K.one if i==j else z) for i in range(3) for j in range(3)),K.zero)
    def from_coeff(p):
        return sum((K(c)*z**i for i,c in enumerate(p)),K.zero)
    active_polys={};mapping={};zeros=[]
    for p,model in enumerate(all_models):
        record=model['record']
        a={v:[K.one if j==k else K.zero for j in range(3)] for k,v in enumerate(record['anchors'])}
        for new,i,j,old in record['steps']:
            a[new]=[2*z/(1+z)*(x+y)-w for x,y,w in zip(a[i],a[j],a[old])]
        forced={}
        for i,j,old in record['candidates']:
            w=casdot(a[i],a[j])
            forced[(i,j,old)]=[2*z/(1+w)*(x+y)-v for x,y,v in zip(a[i],a[j],a[old])]
        for c,case in enumerate(model['cases']):
            u,v=(forced[x] for x in case['gluing'])
            residual=casdot(u,v)-z*(9*z*z-2*z-3)/(1+z)**2
            need(residual==from_coeff(case['residual'].n)/from_coeff(case['residual'].d),'independent CAS residual comparison')
            if not residual:
                zeros.append((p,c));continue
            polynomial=s.Poly(residual.numer.as_expr(),symbol,domain=s.QQ)
            relevant=[]
            for factor,multiplicity in s.factor_list(polynomial)[1]:
                factor=factor.clear_denoms()[1].primitive()[1]
                coeff=primitive(tuple(int(x) for x in reversed(factor.all_coeffs())))
                q=s.Poly.from_list(list(reversed(coeff)),symbol,domain=s.QQ)
                if q.eval(s.Rational(1,2))==0 or q.eval(s.Rational(3,5))==0:continue
                roots=q.intervals(eps=s.Rational(1,10**30),inf=s.Rational(1,2),sup=s.Rational(3,5))
                if roots:
                    need(len(roots)==1,'CAS factor root multiplicity/coverage')
                    (lo,hi),m=roots[0]
                    active_polys[coeff]={'polynomial':list(coeff),'bracket':[[int(lo.p),int(lo.q)],[int(hi.p),int(hi.q)]]}
                    relevant.append(coeff)
            if relevant:
                need(len(relevant)==1,'CAS residual has multiple relevant factors')
                mapping[(p,c)]=relevant[0]
    coefficients=sorted(active_polys)
    roots=[active_polys[p] for p in coefficients]
    indices={p:i for i,p in enumerate(coefficients)}
    result={'roots':roots,'active':[[p,c,indices[f]] for (p,c),f in sorted(mapping.items())],
            'zero_witnesses':[],'root_witnesses':[],'extensions':[]}
    for p,c in zeros:
        model=all_models[p];case=model['cases'][c]
        for orientation in (-1,1):
            points={**model['a'],**branch_rat(case,orientation)}
            pair=next((pair for pair in nonedges(case) if sign_open(dot(points[pair[0]],points[pair[1]])-t)==1),None)
            need(pair is not None,'zero branch has no uniform witness')
            result['zero_witnesses'].append([p,c,orientation,list(pair)])
    for (p,c),factor in sorted(mapping.items()):
        entry=active_polys[factor]
        lo,hi=(Fraction(*x) for x in entry['bracket'])
        if factor==F or lo>ROOT_HI:continue
        need(hi<ROOT_LO,'CAS root relative to incumbent unresolved')
        f=Field(factor,entry['bracket']);model=all_models[p];case=model['cases'][c]
        for orientation in (-1,1):
            points=branch_field(model,case,orientation,f)
            pair=next((pair for pair in nonedges(case) if f.sign(f.sub(f.dot(points[pair[0]],points[pair[1]]),f.t))>0),None)
            if pair is not None:
                result['root_witnesses'].append([p,c,orientation,list(pair)]);continue
            mode,tetra,normal=SEEDS[(p,c,orientation)]
            extension={'patch':p,'case':c,'orientation':orientation,'mode':mode,'tetrahedron':tetra}
            if normal is not None:extension.update(normal_triple=normal,threshold=[4,3])
            result['extensions'].append(extension)
    need(len(roots)==9 and len(mapping)==26 and len(zeros)==7,'CAS cover counts')
    return result


if __name__=='__main__':
    print(json.dumps(generate(),indent=2,sort_keys=True))
