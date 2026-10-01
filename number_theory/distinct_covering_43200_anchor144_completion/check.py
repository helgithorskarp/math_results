"""Exact three-stage conditional completion certificate.

All six parts are required. Standard library only, no numerical solver,
private forest, hidden normalization, or generated cache. Explicit checks
also run under python -O. Each part has a20s whole-loop cap.
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
import orbits144 as third
import check_orbits100
import check_orbits108
import check_orbits144

HERE=Path(__file__).resolve().parent
N,Q,B,C,b=43200,10800,64,675,16
ORDER=(8,9,10,12,15,16,18,20,24,25,30,36,40,45,48,50,75,54,60,72)
PARENT=(0,0,5,10,1,4,3,17,2,3,11,30,27,19,14,33,13,33,29,31)
AXES=(16,27,25)
PARTS=('orbits100','orbits108','orbits144','capacity100','capacity108','capacity144')
REPS={100:first.REPRESENTATIVES,108:second.REPRESENTATIVES,144:third.REPRESENTATIVES}
LEAVES={100:31,108:31,144:63}

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
    need(first.BASE==ORDER and first.PARENTS==(PARENT,)
         and second.BASE==ORDER+(100,) and second.PARENTS==(PARENT+(93,),)
         and third.BASE==ORDER+(100,108) and third.PARENT==PARENT+(93,6),
         'Structural and numerical parents differ')
    basis=data['box_basis']
    need(bool(basis) and all(len(mask)==3 and all(type(v) is int for v in mask)
         and all(0<m<1<<axis for m,axis in zip(mask,AXES)) for mask in basis),'Invalid masks')
    need(len({tuple(mask) for mask in basis})==len(basis),'Duplicate basis mask')
    rows=data['certificate_vectors'];ids=[r['id'] for r in rows]
    need(bool(rows) and len(set(ids))==len(ids),'Missing/duplicate integer vector')
    for row in rows:
        stage,phase=row['stage'],row['phase']
        need(type(stage) is int and type(phase) is int and stage in REPS
             and phase in REPS[stage] and not(stage==100 and phase==93)
             and not(stage==108 and phase==6),'Invalid vector child')
        need(row['id']==f'{stage}-{phase}','Different vector identifier')
        terms=row['weights']
        need(bool(terms) and all(len(term)==2 and all(type(v) is int for v in term)
             and 0<=term[0]<len(basis) and term[1]>0 for term in terms),'Invalid positive integer terms')
        need(len({term[0] for term in terms})==len(terms),'Repeated vector term')
    vectors={r['id']:r for r in rows};used=set()
    def binding(identifier,stage):
        need(identifier in vectors and vectors[identifier]['stage']==stage,'Unknown or wrong-stage vector')
        used.add(identifier)
    tree=data['completion_tree']
    need(tuple(n['phase100'] for n in tree)==REPS[100]
         and all(type(n['phase100']) is int for n in tree),'Incomplete32-child100 split')
    for node in tree:
        if node['phase100']!=93:
            need(set(node)=={'phase100','weight'},'Missing/extra100 certificate')
            binding(node['weight'],100);continue
        need(set(node)=={'phase100','children108'},'Missing/extra108 split')
        children=node['children108']
        need(tuple(n['phase108'] for n in children)==REPS[108]
             and all(type(n['phase108']) is int for n in children),'Incomplete32-child108 split')
        for child in children:
            if child['phase108']!=6:
                need(set(child)=={'phase108','weight'},'Missing/extra108 certificate')
                binding(child['weight'],108);continue
            need(set(child)=={'phase108','children144'},'Missing/extra144 split')
            pairs=child['children144']
            need(tuple(pair[0] for pair in pairs)==REPS[144]
                 and all(len(pair)==2 and type(pair[0]) is int for pair in pairs),
                 'Incomplete63-child144 split')
            for phase,identifier in pairs:binding(identifier,144)
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
    need(any(base),'Zero certificate');return base

def known(stage,phase):
    extra={100:((100,phase),),108:((100,93),(108,phase)),
           144:((100,93),(108,6),(144,phase))}
    return tuple(zip(ORDER,PARENT))+extra[stage]

def support(base,classes):
    need(all(not w or all(x%m!=phase for m,phase in classes) for x,w in enumerate(base)),
         'Positive weight on a prescribed class')

def support_bindings(data):
    vectors={r['id']:r for r in data['certificate_vectors']}
    bases={identifier:decode(data,row) for identifier,row in vectors.items()}
    for row in vectors.values():support(bases[row['id']],known(row['stage'],row['phase']))
    count=0
    for node in data['completion_tree']:
        if 'weight' in node:
            support(bases[node['weight']],known(100,node['phase100']));count+=1;continue
        for child in node['children108']:
            if 'weight' in child:
                support(bases[child['weight']],known(108,child['phase108']));count+=1;continue
            for phase,identifier in child['children144']:
                support(bases[identifier],known(144,phase));count+=1
    need(count==125,'Different completion tree leaf count');return bases

def placed(stage):
    return ORDER+{100:(100,),108:(100,108),144:(100,108,144)}[stage]

def evaluate(row,base):
    vector=base*(N//Q)
    resources=[n for n in range(8,N+1) if N%n==0 and n not in placed(row['stage'])]
    need((len(resources),sum(resources))=={100:(57,156692),108:(56,156584),144:(55,156440)}[row['stage']],
         'Different actual unused resources')
    top={B*d for d in range(1,C+1) if C%d==0};need(top<=set(resources),'A top resource is unavailable')
    nonzero=[(x,w) for x,w in enumerate(vector) if w]
    capacities,H={},{};phase_hash=sha256()
    for n in resources:
        populations=[0]*n
        for x,w in nonzero:populations[x%n]+=w
        capacities[n]=max(populations)
        phase_hash.update(json.dumps([n,populations],separators=(',',':')).encode()+b'\n')
        if n in top and n!=B:H[n//B]=[max(populations[t::b]) for t in range(b)]
    M={d:capacities[B*d] for d in H};labels=[];case_hash=sha256()
    for t in range(b):
        points=[(x,vector[x]) for x in range(t+B//2,N,B) if vector[x]];values=[]
        for phases in product(range(-1,3),range(-1,5),range(-1,9)):
            inside=[(d,a) for d,a in zip((3,5,9),phases) if a>=0]
            outside=[d for d,a in zip((3,5,9),phases) if a<0]
            value=2*sum(w for x,w in points if any(x%d==a for d,a in inside))+sum(M[d] for d in outside)
            case_hash.update(json.dumps([t,phases,value],separators=(',',':')).encode()+b'\n')
            values.append(value)
        labels.append(max(values)+sum(max(M[d],2*H[d][t]) for d in H if d not in (3,5,9)))
    outside=sum(capacities[n] for n in resources if n not in top);total=outside+max(labels)
    result={'id':row['id'],'stage':row['stage'],'phase':row['phase'],
        'demand':sum(vector),'outside_capacity':outside,'top_budget':max(labels),
        'total_capacity':total,'strict_gap':sum(vector)-total,
        'resource_phase_values_sha256':phase_hash.hexdigest(),'union_case_values_sha256':case_hash.hexdigest(),
        'base_weight_sha256':sha256(json.dumps(base,separators=(',',':')).encode()).hexdigest()}
    need(result['strict_gap']>0,'No strict physical inequality');return result

def certificate(data,part,details=None):
    start=monotonic();validate(data);need(part in PARTS,'Unknown certificate part')
    result={'part':part,'N':N,'Q':Q,'parent_moduli':list(ORDER),'parent_residues':list(PARENT),
        'completion_tree_leaves':125,'all_six_parts_required':True,
        'part_alone_excludes_parent':False,'whole_period_exclusion':False}
    if part.startswith('orbits'):
        modulus=int(part[6:])
        action={100:check_orbits100,108:check_orbits108,144:check_orbits144}[modulus].verify()
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
        need(bool(answers),'Missing numerical stage')
        if details is not None:details.extend(answers)
        events=''.join(json.dumps(row,separators=(',',':'),sort_keys=True)+'\n' for row in answers).encode()
        resources=[n for n in range(8,N+1) if N%n==0 and n not in placed(stage)]
        result.update({'stage':stage,'stored_integer_vectors':len(answers),
            'literal_box_basis_count':len(data['box_basis']),
            'sparse_integer_terms':sum(len(r['weights']) for r in data['certificate_vectors'] if r['stage']==stage),
            'representative_leaves_excluded':LEAVES[stage],'all125_representative_supports_checked':True,
            'smallest_prototype_physical_gap':min(r['strict_gap'] for r in answers),
            'actual_resources_checked':len(answers)*len(resources),
            'actual_phases_evaluated':len(answers)*sum(resources),'cluster_union_cases':len(answers)*b*240,
            'ordered_prototype_results_sha256':sha256(events).hexdigest()})
    need(monotonic()-start<20,'Incomplete certificate part under20s cap');return result

def controls(data):
    edits=('bad_period','missing_vector','duplicate_vector','missing100_child','missing108_child',
           'missing144_child','wrong_vector_stage','bad_basis_index','zero_weight','negative_weight',
           'duplicate_weight_term','oversized_mask','overlap','weight_on_parent','different_parent',
           'boolean_phase','unknown_vector')
    for edit in edits:
        invalid=deepcopy(data);row=invalid['certificate_vectors'][0]
        middle=next(n for n in invalid['completion_tree'] if n['phase100']==93)
        deep=next(n for n in middle['children108'] if n['phase108']==6)
        if edit=='bad_period':invalid['Q']=3600
        elif edit=='missing_vector':invalid['certificate_vectors'].pop()
        elif edit=='duplicate_vector':invalid['certificate_vectors'].append(deepcopy(row))
        elif edit=='missing100_child':invalid['completion_tree'].pop()
        elif edit=='missing108_child':middle['children108'].pop()
        elif edit=='missing144_child':deep['children144'].pop()
        elif edit=='wrong_vector_stage':row['stage']=108
        elif edit=='bad_basis_index':row['weights'][0][0]=len(invalid['box_basis'])
        elif edit=='zero_weight':row['weights'][0][1]=0
        elif edit=='negative_weight':row['weights'][0][1]=-1
        elif edit=='duplicate_weight_term':row['weights'].append(deepcopy(row['weights'][0]))
        elif edit=='oversized_mask':invalid['box_basis'][0][1]=1<<27
        elif edit=='overlap':
            i=len(invalid['box_basis']);invalid['box_basis'].append([(1<<axis)-1 for axis in AXES]);row['weights'].append([i,1])
        elif edit=='weight_on_parent':
            i=len(invalid['box_basis']);invalid['box_basis'].append([1,1,1]);row['weights']=[[i,1]]
        elif edit=='different_parent':invalid['parent_residues'][-1]=6
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
