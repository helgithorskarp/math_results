"""Complete tiny physical truth inputs, field-column census, and semantic damages."""
import argparse
import copy
import importlib.util
import json
from pathlib import Path


def load(name):
    spec=importlib.util.spec_from_file_location('h3_'+name,Path(__file__).resolve().parent/(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


build=load('model').build;audit=load('check_model').audit;check_word=load('check_partial').check_word


def require(ok,message):
    if not ok:raise ValueError(message)


def physical(d,raw):
    q,m=d['field_prime'],d['row_half'];H=d['subgroup'];n=2*q*m
    representatives=sorted({min(r*h%q for h in H) for r in range(1,q)})
    word=[]
    for x in range(n):
        if x%q==0:word.append(None);continue
        g=representatives.index(min(x%q*h%q for h in H));s=x%(2*m)
        word.append(((raw//2**(m*g+s%m))%2+s//m)%2)
    return word


def small(q,m,k,H,fixed=None,palette=False,only_fixed_cylinder=False):
    d=build(q,m,k,H,fixed,palette);a=audit(d);n=d['period'];nv=d['variables']
    supports=set();regular=0
    for first in range(n):
        for second in range(n):
            if first==second:continue
            positions={(first+j*(second-first))%n for j in range(k)}
            if any(x%q==0 for x in positions):continue
            regular+=1;supports.add(sum(2**x for x in positions))
    inputs=range(2**nv) if not only_fixed_cylinder else [fixed+2**m*other for other in range(2**(nv-m))]
    positive=identities=0;certificates=[]
    for raw in inputs:
        word=physical(d,raw);ones=sum(2**x for x,v in enumerate(word) if v==1)
        actual=all(ones&s not in [0,s] for s in supports)
        if fixed is not None:actual &= raw%(2**m)==fixed
        if palette:actual &= raw%2==0
        encoded=all(any(((raw//2**(abs(v)-1))%2)==int(v>0) for v in c) for c in d['clauses'])
        require(actual==encoded,'whole small physical/model truth equivalence')
        for x,v in enumerate(d['point_literals']):
            if v is None:require(word[x] is None,'actual pole mask')
            else:
                require(word[x]==((raw//2**(abs(v)-1))%2+int(v<0))%2,'all actual small point identities');identities+=1
        if actual:
            assignment=[v if(raw>>(v-1))&1 else -v for v in range(1,nv+1)]
            check_word(d,assignment,word)
            certificates.append((assignment,word));positive+=1
    return d,certificates,{'q':q,'half':m,'length':k,'subgroup':H,'fixed_row':fixed,'palette':palette,
                           'variables':nv,'inputs':len(inputs),'positives':positive,'regular_pairs':regular,
                           'point_identities':identities,'coverage':'ALL_FIXED_ROW_CYLINDER_INPUTS' if only_fixed_cylinder else 'ALL_ORIGINAL_POINT_INPUTS_INCLUDING_WRONG_FIXED_ROWS',
                           'definition_audit':a['status']}


def field_census(data):
    H={1,5,25}
    classes=sorted({tuple(r for r in range(1,31) if r*pow(a,-1,31)%31 in H) for a in range(1,31)},key=lambda c:c[0])
    supports=set();regular=0
    for a in range(31):
        for b in range(31):
            if a==b:continue
            positions=[(a+j*(b-a))%31 for j in range(7)]
            if 0 in positions:continue
            regular+=1;supports.add(sum(2**i for i,c in enumerate(classes) if any(r in c for r in positions)))
    admissible=[m for m in range(1024) if all(m&s not in [0,s] for s in supports)]
    require(data['cosets']==[list(c) for c in classes] and data['admissible_masks']==admissible and data['admissible_count']==len(admissible)==262,'whole independent fixed-phase census')
    require(data['actual_regular_field_APs']==regular==720 and data['distinct_unsigned_supports']==len(supports)==110,'whole field AP/support inventory')
    excluded=data['excluded_actual_field_AP_witnesses']
    require([r[0] for r in excluded]==[m for m in range(1024) if m not in admissible] and len(excluded)==data['excluded_count']==762,'complete excluded input cover')
    for mask,a,d,color in excluded:
        require(0<=a<31 and 1<=d<31 and color in [0,1],'actual field witness bounds')
        positions=[(a+j*d)%31 for j in range(7)]
        require(all(positions) and all((mask//2**next(i for i,c in enumerate(classes) if r in c))%2==color for r in positions),'actual excluded field AP colors')
    return {'all_input_masks':1024,'admissible_masks':262,'actual_regular_field_APs':720,'distinct_unsigned_supports':110,'actual_negative_witnesses':762}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('production',type=Path);p.add_argument('field_census',type=Path);a=p.parse_args()
    results=[];tiny=[];positive_sets=[]
    for q,m,k,H in [(3,2,3,[1]),(3,4,7,[1]),(5,1,3,[1]),(5,1,3,[1,4]),(7,2,3,[1]),(7,2,3,[1,2,4])]:
        for palette in [False,True]:
            d,c,r=small(q,m,k,H,palette=palette);tiny.append(d);positive_sets.append(c);results.append(r)
    for spec in [(7,1,7,[1,2,4],None,False),(3,4,7,[1],1,False),(3,10,7,[1],16,True)]:
        q,m,k,H,fixed,cylinder=spec;d,c,r=small(q,m,k,H,fixed=fixed,only_fixed_cylinder=cylinder)
        tiny.append(d);positive_sets.append(c);results.append(r)
    cross_index=next(i for i,r in enumerate(results) if(r['q'],r['half'],r['length'],r['subgroup'],r['palette'])==(5,1,3,[1,4],False))
    require(results[cross_index]['positives']==2 and results[cross_index]['inputs']==4,'genuine cross-field nontrivial-subgroup positives/negatives')
    production=json.loads(a.production.read_text());damages=[]
    seed=tiny[cross_index]
    for key,value in [('variables',True),('free_point_inputs_before_AP',0),('period',11),('subgroup',[1,2]),('cosets',list(reversed(seed['cosets']))),
                      ('membership_clauses',[[1]]),('palette',True),('fixed_first_coset_row',0),('scope','closed transport'),('base_row_mask',72)]:
        x=copy.deepcopy(seed);x[key]=value;damages.append((x,False))
    for key in ['point_literals','clauses','cosets']:
        x=copy.deepcopy(seed);x[key].pop();damages.append((x,False))
    x=copy.deepcopy(seed);i=next(i for i,v in enumerate(x['point_literals']) if v is not None);x['point_literals'][i]=-x['point_literals'][i];damages.append((x,False))
    x=copy.deepcopy(seed);x['point_literals'][0]=1;damages.append((x,False))
    x=copy.deepcopy(seed);x['clauses'].append([1]);damages.append((x,False))
    x=copy.deepcopy(seed);x['palette_clauses']=[[-1]];damages.append((x,False))
    x=copy.deepcopy(production);x['point_literals'][1]=-x['point_literals'][1];damages.append((x,True))
    x=copy.deepcopy(production);x['fixed_row_clauses']=[[-1],[-2],[-3],[4],[5],[-6],[7],[-8],[-9],[-10]];damages.append((x,True))
    x=copy.deepcopy(production);i=next(i for i,c in enumerate(x['clauses']) if len(c)>1);x['clauses'].pop(i);x['distinct_AP_clauses']-=1;damages.append((x,True))
    x=copy.deepcopy(production);x['clauses'].append([11]);x['clauses'].sort();damages.append((x,True))
    for damaged,target in damages:
        try:audit(damaged,target)
        except (ValueError,KeyError,TypeError,StopIteration):pass
        else:raise ValueError('semantic model damage accepted')
    assignment,word=positive_sets[cross_index][0];core_damages=[]
    x=assignment.copy();x.pop();core_damages.append((seed,x,word))
    x=assignment.copy();x[0]=True;core_damages.append((seed,x,word))
    x=assignment.copy();x[1]=x[0];core_damages.append((seed,x,word))
    x=assignment.copy();x[0]=-x[0];core_damages.append((seed,x,word))
    x=word.copy();i=next(i for i,v in enumerate(x) if v is not None);x[i]^=1;core_damages.append((seed,assignment,x))
    x=word.copy();x[0]=0;core_damages.append((seed,assignment,x))
    x=word.copy();x.pop();core_damages.append((seed,assignment,x))
    x=copy.deepcopy(seed);x['fixed_first_coset_row']=1-(abs(assignment[0]) in {v for v in assignment if v>0});core_damages.append((x,assignment,word))
    bad_assignment=[-v for v in range(1,seed['variables']+1)];bad_word=physical(seed,0);core_damages.append((seed,bad_assignment,bad_word))
    for d,assign,w in core_damages:
        try:check_word(d,assign,w)
        except (ValueError,KeyError,TypeError,StopIteration):pass
        else:raise ValueError('bad raw-core certificate accepted')
    census=field_census(json.loads(a.field_census.read_text()))
    print(json.dumps({'author':'six-vdw-1','role':'researcher','status':'COMPLETE_ARBITRARY_SUBGROUP_PHYSICAL_CONTROLS',
                      'models':len(results),'inputs':sum(r['inputs'] for r in results),'positive_inputs':sum(r['positives'] for r in results),
                      'point_identities':sum(r['point_identities'] for r in results),'damaged_models_rejected':len(damages),
                      'production_definition_damages_rejected':sum(t for _,t in damages),'damaged_actual_cores_rejected':len(core_damages),
                      'field_census':census,'case_results':results,
                      'scope':'Whole listed tiny physical truth domains/meaningful production damages; no field31 regular core or W witness.'},sort_keys=True),flush=True)
