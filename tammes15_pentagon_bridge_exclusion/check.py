#!/usr/bin/env python3
"""Exact stdlib verifier for the ten/eleven-label, ninety-four-case forbidden family."""
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import copy
import json
import sys
from field import Field,selftest as field_controls
from patches import catalog,models,dot,sign_open,t,one
from geometry import branch_rat,branch_field
from polynomial import need,primitive,pgcd,root_count,value


def validate_root(entry):
    need(set(entry)=={'polynomial','bracket'},'root fields')
    polynomial=tuple(entry['polynomial'])
    need(polynomial==(-1,0,3),'root polynomial')
    lo,hi=(Fraction(*x) for x in entry['bracket'])
    need(Fraction(1,2)<lo<hi<Fraction(3,5),'root bracket domain')
    need(value(polynomial,lo)<0<value(polynomial,hi),'root bracket endpoint signs')
    need(root_count(polynomial)==root_count(polynomial,lo,hi)==1,'complete isolated-root count')
    return polynomial


def nonedges(case):
    return [p for p in combinations(range(case['n']+5),2) if p not in case['edges']]


def validate_zero(model,case,orientation,pair):
    need(orientation in (-1,1),'orientation')
    need(not case['residual'].n,'zero-case residual')
    need(tuple(pair) in nonedges(case),'zero-case witness prescribed/invalid')
    points=branch_rat(model,case,orientation)
    need(all(dot(x,x)==one for x in points.values()),'zero-frame norms')
    need(all(dot(points[i],points[j])==t for i,j in case['edges']),'zero-frame contacts')
    p,q=model['B']['ears']
    need(points[p+model['n']]==case['u'] and points[q+model['n']]==case['v'],'zero-frame fixed ears')
    gap=dot(points[pair[0]],points[pair[1]])-t
    need(sign_open(gap)==1,'zero-case packing witness')
    return {'num':list(gap.n),'den':list(gap.d)}


def validate_bad(model,case,orientation,pair,f):
    need(orientation in (-1,1),'orientation')
    need(tuple(pair) in nonedges(case),'root-case witness prescribed/invalid')
    points=branch_field(model,case,orientation,f)
    need(all(f.dot(x,x)==f.one for x in points.values()),'root-frame norms')
    need(all(f.dot(points[i],points[j])==f.t for i,j in case['edges']),'root-frame contacts')
    gram=f.dot(points[pair[0]],points[pair[1]])
    need(f.sign(f.sub(gram,f.t))>0,'root-case packing witness')
    return f.encode(gram)


def verify(data):
    need(set(data)=={'roots','active','zero_witnesses','root_witnesses'},'certificate fields')
    need(len(data['roots'])==1,'root table size')
    factor=validate_root(data['roots'][0]);f=Field(factor,data['roots'][0]['bracket'])
    active={(m,c):r for m,c,r in data['active']}
    zw={(m,c,s):pair for m,c,s,pair in data['zero_witnesses']}
    rw={(m,c,s):pair for m,c,s,pair in data['root_witnesses']}
    need(len(active)==len(data['active'])==3,'active duplicate/count')
    need(len(zw)==len(data['zero_witnesses'])==14,'zero witness duplicate/count')
    need(len(rw)==len(data['root_witnesses'])==6,'root witness duplicate/count')
    used_active=set();used_zero=set();used_bad=set();zero_details=[];root_details=[]
    zero_cases=0;rootless=0
    for m,model in enumerate(models()):
        for c,case in enumerate(model['cases']):
            numerator=primitive(case['residual'].n)
            if not numerator:
                zero_cases+=1
                for orientation in (-1,1):
                    key=(m,c,orientation)
                    need(key in zw,'zero branch omitted')
                    gap=validate_zero(model,case,orientation,zw[key]);used_zero.add(key)
                    zero_details.append({'model':m,'case':c,'orientation':orientation,'pair':zw[key],'gap':gap})
                continue
            count=root_count(numerator)
            if not count:
                need((m,c) not in active,'spurious active case');rootless+=1;continue
            need(count==1 and (m,c) in active and active[(m,c)]==0,'uncovered residual root')
            need(pgcd(numerator,factor)==factor,'residual/root factor identity')
            need(f.div(f.element(case['residual'].n),f.element(case['residual'].d))==f.zero,'residual at root')
            used_active.add((m,c))
            for orientation in (-1,1):
                key=(m,c,orientation)
                need(key in rw,'root branch omitted')
                gram=validate_bad(model,case,orientation,rw[key],f);used_bad.add(key)
                root_details.append({'model':m,'case':c,'orientation':orientation,'pair':rw[key],'gram':gram})
    need(used_active==set(active) and used_zero==set(zw) and used_bad==set(rw),'unused certificate entry')
    need((zero_cases,rootless)==(7,84),'finite-cover outcome counts')
    counts={str(n):catalog(n)[2] for n in (5,6)}
    return {'status':'VERIFIED','interval':'(1/2,3/5)','points_in_forbidden_schemas':[10,11],
            'prescribed_contacts':[18,20],'gluing_cases':94,'rootless_cases':rootless,
            'zero_cases':zero_cases,'isolated_root_cases':len(active),
            'packing_branches_remaining':0,'cover':counts,
            'zero_branch_witnesses':zero_details,'isolated_branch_witnesses':root_details,
            'global_Tammes15_bound_improved':False}


def selftest(data):
    field_controls()
    need(primitive((-1,))==(1,),'constant primitive normalization')
    need(root_count((-1,0,3))==1,'quadratic Sturm control')
    need(root_count((-1,2))==root_count((-3,5))==0,'open endpoint Sturm controls')
    need(root_count((1,-4,4),Fraction(0),Fraction(1))==1,'repeated-root Sturm control')
    rejected=0
    def reject(function,message):
        nonlocal rejected
        try:function()
        except ValueError as e:need(message in str(e),'wrong rejection reason');rejected+=1
        else:raise ValueError('false certificate accepted')
    bad=copy.deepcopy(data['roots'][0]);bad['bracket']=[[51,100],[52,100]]
    reject(lambda:validate_root(bad),'endpoint signs')
    m,c,s,p=data['zero_witnesses'][0];model=models()[m];case=model['cases'][c]
    reject(lambda:validate_zero(model,case,s,list(sorted(case['edges'])[0])),'witness')
    reject(lambda:validate_zero(model,case,0,p),'orientation')
    m,c,s,p=data['root_witnesses'][0];model=models()[m];case=model['cases'][c]
    f=Field(data['roots'][0]['polynomial'],data['roots'][0]['bracket'])
    reject(lambda:validate_bad(model,case,s,list(sorted(case['edges'])[0]),f),'witness')
    for key in ('active','zero_witnesses','root_witnesses'):
        bad=copy.deepcopy(data);bad[key]=bad[key][:-1]
        reject(lambda:verify(bad),'count')
    return {'rejected_false_certificates':rejected,'arithmetic_controls':'PASS'}


if __name__=='__main__':
    data=json.loads(Path(__file__).with_name('certificate.json').read_text())
    result=verify(data)
    if '--selftest' in sys.argv:result['controls']=selftest(data)
    print(json.dumps(result,indent=2,sort_keys=True))
