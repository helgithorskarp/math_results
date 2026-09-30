#!/usr/bin/env python3
"""Exact stdlib checker for the 336-case seven/six reflection-family exclusion."""
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import copy
import json
import sys
from field import Field,selftest as field_controls
from patches import models,dot,sign_open,t,one
from geometry import branch_rat,branch_field,sum_field
from polynomial import need,primitive,pgcd,root_count,value
import parametric

CONTINUUM=(0,32,1)

def validate_root(entry):
    polynomial=tuple(entry['polynomial'])
    need(len(polynomial)>=2 and all(type(c) is int for c in polynomial),'integer root polynomial')
    need(primitive(polynomial)==polynomial,'primitive root polynomial')
    lo,hi=(Fraction(*x) for x in entry['bracket'])
    need(Fraction(1,2)<lo<hi<Fraction(3,5),'root bracket domain')
    need(value(polynomial,lo)*value(polynomial,hi)<0,'root bracket endpoint signs')
    need(root_count(polynomial)==root_count(polynomial,lo,hi)==1,'complete isolated-root count')
    return polynomial,lo,hi


def nonedges(case):
    return [p for p in combinations(range(13),2) if p not in case['edges']]


def validate_zero_frame(model,case,orientation):
    need(not case['residual'].n,'zero-case residual')
    points=branch_rat(model,case,orientation)
    need(all(dot(x,x)==one for x in points.values()),'zero-frame norms')
    need(all(dot(points[i],points[j])==t for i,j in case['edges']),'zero-frame contacts')
    p,q=model['B']['ears']
    need(points[p+7]==case['u'] and points[q+7]==case['v'],'zero-frame fixed ears')
    return points


def validate_zero(model,case,orientation,pair):
    need(tuple(pair) in nonedges(case),'zero-case witness prescribed/invalid')
    points=validate_zero_frame(model,case,orientation)
    need(sign_open(dot(points[pair[0]],points[pair[1]])-t)==1,'zero-case packing witness')


def validate_bad(points,f,case,pair):
    need(tuple(pair) in nonedges(case),'root-case witness prescribed/invalid')
    need(f.sign(f.sub(f.dot(points[pair[0]],points[pair[1]]),f.t))>0,'root-case packing witness')


def boundedness(f,points,labels):
    need(len(labels)==4 and len(set(labels))==4 and all(type(i) is int and 0<=i<13 for i in labels),'tetrahedron labels')
    chosen=[points[i] for i in labels]
    weights=[f.det3([chosen[j] for j in range(4) if j!=i]) for i in range(4)]
    weights=[f.neg(x) if i%2 else x for i,x in enumerate(weights)]
    total=sum_field(f,weights)
    weights=[f.div(x,total) for x in weights]
    need(all(f.sign(w)>0 for w in weights),'positive origin tetrahedron')
    need(sum_field(f,weights)==f.one,'tetrahedron weight sum')
    need(all(not sum_field(f,(f.mul(w,v[k]) for w,v in zip(weights,chosen))) for k in range(3)),'origin relation')


def linear_rows(f,points):
    return [[sum_field(f,(f.mul(x,f.one if i==j else f.t) for j,x in enumerate(p)))
             for i in range(3)] for p in points]


def polytope(f,points,bounds):
    rows=linear_rows(f,points);vertices={}
    for triple in combinations(range(len(points)),3):
        v=f.solve3([rows[i] for i in triple],[bounds[i] for i in triple])
        if v is None:continue
        if any(f.sign(f.sub(f.dot(p,v),b))>0 for p,b in zip(points,bounds)):continue
        vertices.setdefault(v,triple)
    need(vertices,'empty vertex enumeration of bounded full-dimensional polytope')
    return vertices


def validate_extension(points,f,case,entry):
    points=[points[i] for i in range(13)]
    need(all(f.dot(p,p)==f.one for p in points),'packing unit norms')
    need(all(f.dot(points[i],points[j])==f.t for i,j in case['edges']),'packing contacts')
    need(all(f.sign(f.sub(f.dot(points[i],points[j]),f.t))<=0 for i,j in nonedges(case)),'packing noncontacts')
    boundedness(f,points,entry['tetrahedron'])
    mode=entry['mode'];bounds=[f.t]*13
    if mode=='small_cap':
        triple=entry['normal_triple']
        need(len(triple)==3 and len(set(triple))==3 and all(0<=i<13 for i in triple),'cap normal triple')
        rows=linear_rows(f,[points[i] for i in triple])
        q=f.solve3(rows,[f.t]*3)
        need(q is not None,'cap normal singular')
        threshold=f.number(Fraction(*entry['threshold']))
        need(f.sign(threshold)>0,'cap threshold positive')
        norm=f.dot(q,q)
        need(norm==f.add(f.one,f.mul(f.number(2),f.t)),'cap normal norm identity')
        guard=f.sub(f.mul(f.number(2),f.mul(threshold,threshold)),f.mul(f.add(f.one,f.t),norm))
        need(f.sign(guard)>0,'cap diameter guard')
        points=points+[q];bounds=bounds+[threshold]
    else:
        need(mode in ('saturated','single_unit_vertex'),'extension proof mode')
    vertices=polytope(f,points,bounds)
    unit=0
    for v in vertices:
        sign=f.sign(f.sub(f.dot(v,v),f.one))
        if mode=='single_unit_vertex':
            need(sign<=0,'outside vertex in one-point proof')
            unit+=sign==0
        else:
            need(sign<0,'unit sphere intersects excluded polytope')
            bound=Fraction(9,10) if mode=='saturated' else Fraction(91,100)
            need(f.sign(f.sub(f.dot(v,v),f.number(bound)))<0,'compact norm bound')
    if mode=='single_unit_vertex':need(unit==1,'unique admissible unit vertex')
    return {'mode':mode,'vertices':len(vertices),'unit_vertices':unit,
            'additional_points_at_most':0 if mode=='saturated' else 1}


def verify(data):
    need(set(data)=={'roots','active','zero_witnesses','root_witnesses','extensions','parametric'},'certificate fields')
    roots=[validate_root(x) for x in data['roots']]
    need(len(roots)==5 and all(p!=q for i,(p,*_) in enumerate(roots) for q,*_ in roots[i+1:]),'distinct root table')
    active={(m,c):r for m,c,r in data['active']}
    zw={(m,c,s):pair for m,c,s,pair in data['zero_witnesses']}
    rw={(m,c,s):pair for m,c,s,pair in data['root_witnesses']}
    ex={(e['model'],e['case'],e['orientation']):e for e in data['extensions']}
    need(len(active)==len(data['active'])==12,'active case table')
    need(len(zw)==len(data['zero_witnesses'])==25 and len(rw)==len(data['root_witnesses'])==20 and len(ex)==len(data['extensions'])==4,'branch table duplicate/count')
    used_active=set();used_zero=set();used_bad=set();used_extension=set()
    used_continuum=False;extensions=[];continuous=None;zero_cases=0;rootless=0
    for m,model in enumerate(models()):
        for c,case in enumerate(model['cases']):
            numerator=primitive(case['residual'].n)
            if not numerator:
                zero_cases+=1
                need((m,c) not in active,'spurious zero-case active entry')
                for orientation in (-1,1):
                    key=(m,c,orientation)
                    if key==CONTINUUM:
                        need(key not in zw and not used_continuum,'continuous case duplication')
                        points=validate_zero_frame(model,case,orientation)
                        continuous=parametric.verify(points,data['parametric']);used_continuum=True
                    else:
                        need(key in zw,'zero branch omitted')
                        validate_zero(model,case,orientation,zw[key]);used_zero.add(key)
                continue
            count=root_count(numerator)
            if not count:
                need((m,c) not in active,'spurious active case');rootless+=1;continue
            need(count==1 and (m,c) in active,'uncovered residual root')
            used_active.add((m,c));index=active[(m,c)]
            need(type(index) is int and 0<=index<len(roots),'root table index')
            factor,lo,hi=roots[index]
            need(pgcd(numerator,factor)==factor,'residual/root factor identity')
            f=Field(factor,data['roots'][index]['bracket'])
            for orientation in (-1,1):
                key=(m,c,orientation)
                need((key in rw)!=(key in ex),'root branch omitted/duplicated')
                points=branch_field(model,case,orientation,f)
                need(all(f.dot(x,x)==f.one for x in points.values()),'root branch unit norms')
                need(all(f.dot(points[i],points[j])==f.t for i,j in case['edges']),'root branch contacts')
                if key in rw:
                    validate_bad(points,f,case,rw[key]);used_bad.add(key)
                else:
                    result=validate_extension(points,f,case,ex[key]);used_extension.add(key)
                    extensions.append({'model':m,'case':c,'orientation':orientation,**result})
    need(used_active==set(active) and used_zero==set(zw) and used_bad==set(rw) and used_extension==set(ex) and used_continuum,'unused or omitted certificate entry')
    need((zero_cases,rootless)==(13,311),'scalar partition counts')
    return {'status':'VERIFIED','A_triangulations':42,'A_degree_compatible':35,
            'A_patch_orbits':3,'B_triangulations':14,'B_marked_pairs':18,
            'B_marked_patch_orbits':3,'gluing_cases':336,'rootless_cases':rootless,
            'identically_zero_cases':zero_cases,'uniform_zero_branches_excluded':25,
            'root_cases':12,'root_polynomials':5,'root_packing_branches_excluded':20,
            'isolated_thirteen_point_branches':extensions,'continuous_branch':continuous,
            'fifteen_point_extensions':0,'global_Tammes15_bound_improved':False}


def selftest(data):
    field_controls()
    need(primitive((-3,))==(1,),'constant primitive normalization')
    need(root_count((-1,0,3))==1,'quadratic Sturm control')
    need(root_count((-1,2))==root_count((-3,5))==0,'open endpoint Sturm controls')
    need(root_count((1,-4,4),Fraction(0),Fraction(1))==1,'repeated-root Sturm control')
    p=(-57,100);square=parametric.mul(p,p);cube=parametric.mul(square,p)
    need(parametric.odd_part(square)==(1,),'even-factor reconstruction')
    need(parametric.sign_poly(square,*parametric.LOW)==1,'generic even-root sign')
    need(parametric.sign_poly(cube,*parametric.LOW) is None,'odd-root sign-change control')
    corrupted=copy.deepcopy(data['roots'][0]);corrupted['bracket']=[[1,2],[501,1000]]
    try:validate_root(corrupted)
    except ValueError:pass
    else:raise ValueError('false root bracket accepted')
    m,c,orientation,pair=data['zero_witnesses'][0]
    model=models()[m];case=model['cases'][c]
    try:validate_zero(model,case,orientation,list(sorted(case['edges'])[0]))
    except ValueError as error:need('witness' in str(error),'prescribed-witness rejection')
    else:raise ValueError('false packing witness accepted')
    m,c,orientation=CONTINUUM;model=models()[m];case=model['cases'][c]
    points=validate_zero_frame(model,case,orientation)
    try:parametric.prepare(points,Fraction(1,3))
    except ValueError as error:need('cap diameter' in str(error),'weak-cap rejection')
    else:raise ValueError('weak cap accepted')
    p,b,domain=parametric.prepare(points)[0]
    try:parametric.validate_cover(p,b,domain,data['parametric']['low'][:-1])
    except ValueError as error:need('cover length' in str(error),'omitted-triple rejection')
    else:raise ValueError('omitted active triple accepted')
    codes=copy.deepcopy(data['parametric']['low'])
    triples=tuple(combinations(range(13),3))
    index=next(i for i,code in enumerate(codes) if code is not None)
    codes[index]=[triples[index][0]]
    try:parametric.validate_cover(p,b,domain,codes)
    except ValueError as error:need('infeasibility witness' in str(error),'active-plane false-witness rejection')
    else:raise ValueError('zero-slack infeasibility witness accepted')


if __name__=='__main__':
    data=json.loads(Path(__file__).with_name('certificate.json').read_text())
    result=verify(data)
    if '--selftest' in sys.argv:
        selftest(data)
        result['controls']='field, primitive normalization, Sturm endpoint/multiplicity, odd/even signs, false root/witness/cap and omitted-triple controls passed'
    print(json.dumps(result,indent=2,sort_keys=True))
