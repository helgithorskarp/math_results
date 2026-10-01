"""Exact integer checks for the complete100/108 conditional completion tree.

All four parts are required: orbits100, orbits108, capacity100, capacity108.
Standard library only. No solver, private forest or generated cache is an input.
Explicit exceptions also run under python -O; each part has a20s loop cap.
"""
import argparse
from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
from time import monotonic
import orbits100 as first
import orbits108 as second
import check_orbits

HERE=Path(__file__).resolve().parent
N,Q,B,C,b=43200,10800,64,675,16
ORDER=(8,9,10,12,15,16,18,20,24,25,30,36,40,45,48,50,75,54,60,72)
PARENT=(0,0,5,10,1,4,3,17,2,3,11,30,27,19,14,33,13,33,29,42)
AXES=(16,27,25)
PARTS=('orbits100','orbits108','capacity100','capacity108')


def need(condition,message):
    if not condition:raise ValueError(message)


def validate(data):
    need(all(type(data[k]) is int and data[k]==v for k,v in
             [('N',N),('Q',Q),('B',B),('C',C),('b',b)]),'Wrong periods')
    need(data['axes']==list(AXES) and data['cluster']==[3,5,9]
         and all(type(v) is int for v in data['axes']+data['cluster']),'Wrong axes/cluster')
    need(data['parent_moduli']==list(ORDER) and data['parent_residues']==list(PARENT)
         and all(type(v) is int for v in data['parent_moduli']+data['parent_residues']),
         'Different twenty-class parent')
    need(first.BASE==ORDER and first.PARENTS[2]==PARENT
         and second.BASE==ORDER+(100,) and second.PARENTS==(PARENT+(43,),PARENT+(93,)),
         'Structural and numerical parents differ')
    basis=data['box_basis']
    need(bool(basis) and all(len(mask)==3 and all(type(v) is int for v in mask)
         and all(0<m<1<<axis for m,axis in zip(mask,AXES)) for mask in basis),'Invalid masks')
    need(len({tuple(mask) for mask in basis})==len(basis),'Duplicate basis mask')
    rows=data['certificate_vectors'];ids=[r['id'] for r in rows]
    need(bool(rows) and len(set(ids))==len(ids),'Missing/duplicate integer vector')
    for row in rows:
        stage,a,phase=row['stage'],row['parent100'],row['phase']
        need(type(stage) is int and type(phase) is int
             and ((stage==100 and a is None and phase in first.REPRESENTATIVES
                   and phase not in (43,93))
                  or (stage==108 and type(a) is int and a in (43,93)
                      and phase in second.REPRESENTATIVES)),'Invalid vector child')
        need(row['id']==f'{stage}-{a if a is not None else 0}-{phase}','Different vector identifier')
        terms=row['weights']
        need(bool(terms) and all(len(term)==2 and all(type(v) is int for v in term)
             and 0<=term[0]<len(basis) and term[1]>0 for term in terms),'Invalid positive integer terms')
        need(len({term[0] for term in terms})==len(terms),'Repeated vector term')
    vectors={r['id']:r for r in rows};used=set()
    tree=data['completion_tree']
    need(tuple(node['phase100'] for node in tree)==first.REPRESENTATIVES
         and all(type(node['phase100']) is int for node in tree),'Incomplete32-child100 split')
    for node in tree:
        a=node['phase100']
        if a in (43,93):
            need(set(node)=={'phase100','children108'},'Missing or extra108 split')
            children=node['children108']
            need(tuple(pair[0] for pair in children)==second.REPRESENTATIVES
                 and all(len(pair)==2 and type(pair[0]) is int for pair in children),
                 'Incomplete28-child108 split')
            for phase,identifier in children:
                need(identifier in vectors and vectors[identifier]['stage']==108,
                     'Unknown or wrong-stage108 vector')
                used.add(identifier)
        else:
            need(set(node)=={'phase100','weight'},'Missing or extra100 certificate')
            identifier=node['weight']
            need(identifier in vectors and vectors[identifier]['stage']==100,
                 'Unknown or wrong-stage100 vector')
            used.add(identifier)
    need(used==set(ids),'Unreferenced or missing stored vector')


@lru_cache(None)
def coordinates():
    lookup={tuple(x%axis for axis in AXES):x for x in range(Q)}
    need(len(lookup)==Q,'Ordinary remainder axes are not bijective')
    return lookup


def decode(data,row):
    base=[0]*Q
    for index,value in row['weights']:
        masks=data['box_basis'][index]
        leaves=[[a for a in range(axis) if mask>>a&1] for mask,axis in zip(masks,AXES)]
        for key in product(*leaves):
            x=coordinates()[key];need(not base[x],'Overlapping boxes in one vector');base[x]=value
    need(any(base),'Zero certificate')
    return base


def known(stage,a,phase):
    return tuple(zip(ORDER,PARENT))+(((100,phase),) if stage==100 else ((100,a),(108,phase)))


def support(base,classes):
    need(all(not w or all(x%m!=phase for m,phase in classes) for x,w in enumerate(base)),
         'Positive weight on a prescribed class')


def support_bindings(data,bases=None):
    vectors={r['id']:r for r in data['certificate_vectors']}
    if bases is None:bases={identifier:decode(data,row) for identifier,row in vectors.items()}
    for row in vectors.values():support(bases[row['id']],known(row['stage'],row['parent100'],row['phase']))
    count=0
    for node in data['completion_tree']:
        a=node['phase100']
        if 'weight' in node:support(bases[node['weight']],known(100,None,a));count+=1
        else:
            for phase,identifier in node['children108']:
                support(bases[identifier],known(108,a,phase));count+=1
    need(count==86,'Different completion tree leaf count')
    return bases


def evaluate(row,base):
    vector=base*(N//Q)
    placed=ORDER+(100,)+((108,) if row['stage']==108 else ())
    resources=[n for n in range(8,N+1) if N%n==0 and n not in placed]
    need((len(resources),sum(resources))==((57,156692) if row['stage']==100 else (56,156584)),
         'Different actual unused resources')
    top={B*d for d in range(1,C+1) if C%d==0}
    need(top<=set(resources),'A top resource is unavailable')
    nonzero=[(x,w) for x,w in enumerate(vector) if w]
    capacities,H={},{};phase_hash=sha256()
    for n in resources:
        populations=[0]*n
        for x,w in nonzero:populations[x%n]+=w
        capacities[n]=max(populations)
        phase_hash.update(json.dumps([n,populations],separators=(',',':')).encode()+b'\n')
        if n in top and n!=B:H[n//B]=[max(populations[t::b]) for t in range(b)]
    M={d:capacities[B*d] for d in H}
    labels=[];case_hash=sha256()
    for t in range(b):
        points=[(x,vector[x]) for x in range(t+B//2,N,B) if vector[x]]
        values=[]
        for phases in product(range(-1,3),range(-1,5),range(-1,9)):
            inside=[(d,a) for d,a in zip((3,5,9),phases) if a>=0]
            outside=[d for d,a in zip((3,5,9),phases) if a<0]
            value=2*sum(w for x,w in points if any(x%d==a for d,a in inside))+sum(M[d] for d in outside)
            case_hash.update(json.dumps([t,phases,value],separators=(',',':')).encode()+b'\n')
            values.append(value)
        labels.append(max(values)+sum(max(M[d],2*H[d][t]) for d in H if d not in (3,5,9)))
    outside=sum(capacities[n] for n in resources if n not in top);total=outside+max(labels)
    result={'id':row['id'],'stage':row['stage'],'parent100':row['parent100'],'phase':row['phase'],
            'demand':sum(vector),'outside_capacity':outside,'top_budget':max(labels),
            'total_capacity':total,'strict_gap':sum(vector)-total,
            'resource_phase_values_sha256':phase_hash.hexdigest(),
            'union_case_values_sha256':case_hash.hexdigest(),
            'base_weight_sha256':sha256(json.dumps(base,separators=(',',':')).encode()).hexdigest()}
    need(result['strict_gap']>0,'No strict physical inequality')
    return result


def certificate(data,part,details=None):
    validate(data);need(part in PARTS,'Unknown certificate part');start=monotonic()
    result={'part':part,'N':N,'Q':Q,'parent_moduli':list(ORDER),'parent_residues':list(PARENT),
            'completion_tree_leaves':86,'all_four_parts_required':True,
            'part_alone_excludes_parent':False,'whole_period_exclusion':False}
    if part.startswith('orbits'):
        action=check_orbits.verify100() if part=='orbits100' else check_orbits.verify108()
        modulus=100 if part=='orbits100' else 108
        result.update({'extra_modulus':modulus,'orbit_count':action['orbit_count'],
                       'physical_generator_points':action['physical_generator_points'],
                       'projection_points':action['projection_points'],
                       'full_prescribed_class_points':action['full_prescribed_class_points'],
                       'divisor_partition_checks':action['divisor_partition_checks'],
                       'raw_class_transport_points':action[f'raw{modulus}_class_transport_points'],
                       'invalid_controls_rejected':action['invalid_controls_rejected'],
                       'physical_action_event_sha256':action['physical_map_event_sha256'],
                       'actual_LCM_preserved':action['actual_LCM_preserved']})
    else:
        stage=int(part[8:]);bases=support_bindings(data);answers=[]
        for row in data['certificate_vectors']:
            if row['stage']!=stage:continue
            need(monotonic()-start<20,'Incomplete stored-vector check under20s cap')
            answers.append(evaluate(row,bases[row['id']]))
        need(bool(answers),'Missing numerical certificate stage')
        if details is not None:details.extend(answers)
        events=''.join(json.dumps(row,separators=(',',':'),sort_keys=True)+'\n' for row in answers).encode()
        placed=ORDER+(100,)+((108,) if stage==108 else ())
        resources=[n for n in range(8,N+1) if N%n==0 and n not in placed]
        result.update({'stage':stage,'stored_integer_vectors':len(answers),
                       'literal_box_basis_count':len(data['box_basis']),
                       'sparse_integer_terms':sum(len(r['weights']) for r in data['certificate_vectors'] if r['stage']==stage),
                       'representative_leaves_excluded':30 if stage==100 else 56,
                       'all86_representative_supports_checked':True,
                       'smallest_prototype_physical_gap':min(r['strict_gap'] for r in answers),
                       'actual_resources_checked':len(answers)*len(resources),
                       'actual_phases_evaluated':len(answers)*sum(resources),
                       'cluster_union_cases':len(answers)*b*240,
                       'ordered_prototype_results_sha256':sha256(events).hexdigest()})
    need(monotonic()-start<20,'Incomplete part under20s cap')
    return result


def controls(data):
    edits=('bad_period','missing_vector','duplicate_vector','missing100_child','missing108_child',
           'wrong_vector_stage','bad_basis_index','zero_weight','negative_weight','duplicate_weight_term',
           'oversized_mask','overlap','weight_on_parent','different_parent','boolean_phase','unknown_vector')
    for edit in edits:
        invalid=deepcopy(data);row=invalid['certificate_vectors'][0]
        if edit=='bad_period':invalid['Q']=3600
        elif edit=='missing_vector':invalid['certificate_vectors'].pop()
        elif edit=='duplicate_vector':invalid['certificate_vectors'].append(deepcopy(row))
        elif edit=='missing100_child':invalid['completion_tree'].pop()
        elif edit=='missing108_child':
            next(n for n in invalid['completion_tree'] if n['phase100']==43)['children108'].pop()
        elif edit=='wrong_vector_stage':row['stage']=108
        elif edit=='bad_basis_index':row['weights'][0][0]=len(invalid['box_basis'])
        elif edit=='zero_weight':row['weights'][0][1]=0
        elif edit=='negative_weight':row['weights'][0][1]=-1
        elif edit=='duplicate_weight_term':row['weights'].append(deepcopy(row['weights'][0]))
        elif edit=='oversized_mask':invalid['box_basis'][0][1]=1<<27
        elif edit=='overlap':
            index=len(invalid['box_basis']);invalid['box_basis'].append([(1<<axis)-1 for axis in AXES]);row['weights'].append([index,1])
        elif edit=='weight_on_parent':
            index=len(invalid['box_basis']);invalid['box_basis'].append([1,1,1]);row['weights']=[[index,1]]
        elif edit=='different_parent':invalid['parent_residues'][-1]=31
        elif edit=='boolean_phase':invalid['completion_tree'][0]['phase100']=False
        elif edit=='unknown_vector':invalid['completion_tree'][0]['weight']='unknown'
        try:validate(invalid);support_bindings(invalid)
        except ValueError:continue
        raise ValueError('Malformed fixture accepted: '+edit)
    return list(edits)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--part',choices=PARTS,required=True)
    parser.add_argument('--controls',action='store_true');args=parser.parse_args()
    raw=(HERE/'input.json').read_bytes();data=json.loads(raw);start=monotonic()
    result=certificate(data,args.part);result['input_sha256']=sha256(raw).hexdigest()
    need(result==json.loads((HERE/'expected.json').read_text())[args.part],'Exact part differs from expected')
    rejected=controls(data) if args.controls else []
    need(monotonic()-start<20,'Incomplete part and controls under20s cap')
    print(json.dumps({'certificate':result,'rejected_controls':rejected,'elapsed_seconds':monotonic()-start,
                      'whole_cap_seconds':20,'independent_review':False},indent=2))
