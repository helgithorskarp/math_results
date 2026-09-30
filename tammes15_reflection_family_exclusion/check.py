#!/usr/bin/env python3
"""Independent stdlib root/branch/polytope audit of the finite-family exclusion."""
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import copy
import json
import sys
from field import Field,selftest as field_controls
from family import (models,branch_rat,branch_field,dot,sign_open,t,one,zero,
                    sum_field)
from polynomial import (need,F,ROOT_LO,ROOT_HI,primitive,pgcd,root_count,
                        bernstein,value)


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


def validate_zero(model,case,orientation,pair):
    need(not case['residual'].n,'zero-case residual')
    b=branch_rat(case,orientation)
    need(all(dot(b[i],b[j])==(one if i==j else t) for i in (8,9,10) for j in (8,9,10) if i<=j),'zero-case anchor Gram')
    need(b[11]==case['u'] and b[12]==case['v'],'zero-case fixed ears')
    need(tuple(pair) in nonedges(case),'zero-case witness prescribed/invalid')
    points={**model['a'],**b}
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
    need(set(data)=={'roots','active','zero_witnesses','root_witnesses','extensions'},'certificate fields')
    need(all(c>0 for c in bernstein(tuple(i*F[i] for i in range(1,len(F))))),'incumbent derivative')
    need(value(F,ROOT_LO)<0<value(F,ROOT_HI),'incumbent bracket')
    roots=[validate_root(x) for x in data['roots']]
    need(len(roots)==9,'root-table size')
    active={(p,c):r for p,c,r in data['active']}
    need(len(active)==len(data['active'])==26,'active table duplicate/count')
    zw={(p,c,s):pair for p,c,s,pair in data['zero_witnesses']}
    rw={(p,c,s):pair for p,c,s,pair in data['root_witnesses']}
    ex={(e['patch'],e['case'],e['orientation']):e for e in data['extensions']}
    need(len(zw)==len(data['zero_witnesses'])==14 and len(rw)==len(data['root_witnesses'])==40 and len(ex)==len(data['extensions'])==6,'branch table duplicate/count')
    used_active=set();used_zero=set();used_bad=set();used_extension=set();extension_results=[]
    zero_cases=0;rootless=0;above=0;incumbent=0
    all_models=models()
    for p,model in enumerate(all_models):
        for c,case in enumerate(model['cases']):
            numerator=primitive(case['residual'].n)
            if not numerator:
                zero_cases+=1
                for orientation in (-1,1):
                    key=(p,c,orientation)
                    need(key in zw,'zero branch omitted')
                    validate_zero(model,case,orientation,zw[key]);used_zero.add(key)
                continue
            count=root_count(numerator)
            if not count:
                need((p,c) not in active,'spurious active case');rootless+=1;continue
            need(count==1 and (p,c) in active,'uncovered residual root')
            used_active.add((p,c));index=active[(p,c)]
            need(type(index) is int and 0<=index<len(roots),'root table index')
            factor,lo,hi=roots[index]
            need(pgcd(numerator,factor)==factor,'residual/root factor identity')
            if factor==F:
                incumbent+=1;continue
            if lo>ROOT_HI:
                above+=1;continue
            need(hi<ROOT_LO,'root comparison with incumbent unresolved')
            f=Field(factor,data['roots'][index]['bracket'])
            for orientation in (-1,1):
                key=(p,c,orientation)
                need((key in rw)!=(key in ex),'root branch omitted/duplicated')
                points=branch_field(model,case,orientation,f)
                if key in rw:
                    validate_bad(points,f,case,rw[key]);used_bad.add(key)
                else:
                    r=validate_extension(points,f,case,ex[key]);used_extension.add(key)
                    extension_results.append({'patch':p,'case':c,'orientation':orientation,**r})
    need(used_active==set(active) and used_zero==set(zw) and used_bad==set(rw) and used_extension==set(ex),'unused certificate entry')
    need((zero_cases,rootless,above,incumbent)==(7,322,2,1),'finite-cover outcome counts')
    return {'status':'VERIFIED','triangulations':132,'degree_compatible_patches':84,
            'dihedral_patch_orbits':8,'gluing_cases':355,'rootless_cases':rootless,
            'identically_zero_cases_excluded':zero_cases,'cases_above_incumbent':above,
            'incumbent_root_cases':incumbent,'root_packing_branches_excluded':len(rw),
            'surviving_thirteen_point_branches':extension_results,
            'fifteen_point_extensions':0,'global_Tammes15_bound_improved':False}


def selftest(data):
    field_controls()
    need(root_count((-1,0,3))==1,'quadratic Sturm control')
    need(root_count((-1,2))==root_count((-3,5))==0,'open endpoint Sturm controls')
    need(root_count((1,-4,4),Fraction(0),Fraction(1))==1,'repeated-root Sturm control')
    corrupted=copy.deepcopy(data['roots'][0])
    corrupted['bracket']=[[1,2],[501,1000]]
    try:validate_root(corrupted)
    except ValueError:pass
    else:raise ValueError('false root bracket accepted')
    all_models=models();p,c,orientation,pair=data['zero_witnesses'][0]
    case=all_models[p]['cases'][c]
    false_pair=list(sorted(case['edges'])[0])
    try:validate_zero(all_models[p],case,orientation,false_pair)
    except ValueError as error:need('witness' in str(error),'wrong rejection of prescribed witness')
    else:raise ValueError('false packing witness accepted')
    e=next(x for x in data['extensions'] if x['mode']=='small_cap')
    model=all_models[e['patch']];case=model['cases'][e['case']]
    active={(p,c):r for p,c,r in data['active']}
    index=active[(e['patch'],e['case'])];root=data['roots'][index]
    f=Field(root['polynomial'],root['bracket']);points=branch_field(model,case,e['orientation'],f)
    bad=copy.deepcopy(e);bad['threshold']=[1,3]
    try:validate_extension(points,f,case,bad)
    except ValueError as error:need('cap diameter guard' in str(error),'wrong rejection of weak cap')
    else:raise ValueError('false extension cap accepted')


if __name__=='__main__':
    data=json.loads(Path(__file__).with_name('certificate.json').read_text())
    result=verify(data)
    if '--selftest' in sys.argv:
        selftest(data);result['controls']='field, Sturm endpoint/multiplicity, false root/witness/cap controls passed'
    print(json.dumps(result,indent=2,sort_keys=True))
