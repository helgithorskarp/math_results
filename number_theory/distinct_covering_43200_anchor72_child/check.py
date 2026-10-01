"""Twenty literal integer weights and the complete42-orbit missing72 split.

Standard library only. No numerical solver, private forest, graph or cache
is a mathematical input. Exceptions remain active under python -O.
"""
import argparse
from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
from time import monotonic
import orbits
import check_orbits

HERE=Path(__file__).resolve().parent
N,Q,B,C,b=43200,10800,64,675,16
ORDER=orbits.BASE
PARENT=orbits.PARENTS[0]
AXES=(16,27,25)
PROTOTYPES=(0,1,4,6,11,12,15,19,20,28,31,33,38,42,47,49,51,55,65,67)


def need(condition,message):
    if not condition:raise ValueError(message)


def validate(data):
    need(all(type(data[k]) is int and data[k]==v for k,v in
             [('N',N),('Q',Q),('B',B),('C',C),('b',b),('extra_modulus',72)]),'Wrong periods')
    need(data['axes']==list(AXES) and data['cluster']==[3,5,9]
         and all(type(v) is int for v in data['axes']+data['cluster']),'Wrong axes/cluster')
    need(data['parent_moduli']==list(ORDER) and data['parent_residues']==list(PARENT)
         and all(type(v) is int for v in data['parent_moduli']+data['parent_residues']),'Different19-parent')
    basis=data['box_basis']
    need(bool(basis) and all(len(mask)==3 and all(type(v) is int for v in mask)
         and all(0<m<1<<axis for m,axis in zip(mask,AXES)) for mask in basis),'Invalid masks')
    need(len({tuple(mask) for mask in basis})==len(basis),'Duplicate basis mask')
    rows=data['certificate_vectors']
    need(tuple(r['phase72'] for r in rows)==PROTOTYPES
         and all(type(r['phase72']) is int for r in rows),'Missing/duplicate certificate vector')
    for row in rows:
        terms=row['weights']
        need(bool(terms) and all(len(term)==2 and all(type(v) is int for v in term)
             and 0<=term[0]<len(basis) and term[1]>0 for term in terms),'Invalid positive integer terms')
        need(len({term[0] for term in terms})==len(terms),'Repeated vector term')
    mapping=data['representative_vector_phases']
    need(tuple(pair[0] for pair in mapping)==orbits.REPRESENTATIVES
         and all(len(pair)==2 and all(type(v) is int for v in pair)
                 and pair[1] in PROTOTYPES for pair in mapping),'Incomplete42-child assignment')
    need(all(pair[1]==(pair[0] if pair[0] in PROTOTYPES else 0) for pair in mapping),
         'Unexpected prototype assignment')


@lru_cache(None)
def coordinates():
    lookup={tuple(x%axis for axis in AXES):x for x in range(Q)}
    need(len(lookup)==Q,'Ordinary remainder axes are not bijective')
    return lookup


def decode(data,phase):
    row=next(r for r in data['certificate_vectors'] if r['phase72']==phase)
    base=[0]*Q
    for index,value in row['weights']:
        masks=data['box_basis'][index]
        leaves=[[a for a in range(axis) if mask>>a&1] for mask,axis in zip(masks,AXES)]
        for key in product(*leaves):
            x=coordinates()[key];need(not base[x],'Overlapping boxes');base[x]=value
    need(any(base),'Zero certificate')
    return base


def weight(data,a):
    need(type(a) is int and 0<=a<72,'Raw phase outside72')
    representative=orbits.representative(a)
    prototype=dict(data['representative_vector_phases'])[representative]
    base=decode(data,prototype)
    if a!=representative:
        base=[base[orbits.transport(Q,x,a)] for x in range(Q)]
    known=tuple(zip(ORDER,PARENT))+((72,a),)
    need(all(not w or all(x%m!=phase for m,phase in known) for x,w in enumerate(base)),
         'Positive weight on a prescribed class')
    return base


def evaluate(data,a):
    base=weight(data,a);vector=base*(N//Q)
    resources=[n for n in range(8,N+1) if N%n==0 and n not in ORDER+(72,)]
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
    result={'prototype_phase72':a,'demand':sum(vector),'outside_capacity':outside,
            'top_budget':max(labels),'total_capacity':total,'strict_gap':sum(vector)-total,
            'resource_phase_values_sha256':phase_hash.hexdigest(),
            'union_case_values_sha256':case_hash.hexdigest(),
            'base_weight_sha256':sha256(json.dumps(base,separators=(',',':')).encode()).hexdigest()}
    need(result['strict_gap']>0,'No strict physical inequality')
    return result


def certificate(data,details=None):
    validate(data);start=monotonic();action=check_orbits.verify()
    answers=[]
    for a in PROTOTYPES:
        need(monotonic()-start<20,'Incomplete prototype check under20s cap')
        answers.append(evaluate(data,a))
    # Same modulus resource set; a zero-phase support check extends its weight
    # certificate to each assigned representative without repeating budgets.
    for a in orbits.REPRESENTATIVES:
        need(monotonic()-start<20,'Incomplete representative check under20s cap')
        weight(data,a)
    if details is not None:details.extend(answers)
    events=''.join(json.dumps(row,separators=(',',':'),sort_keys=True)+'\n' for row in answers).encode()
    resources=[n for n in range(8,N+1) if N%n==0 and n not in ORDER+(72,)]
    return {'N':N,'Q':Q,'extra_modulus':72,'parent_moduli':list(ORDER),'parent_residues':list(PARENT),
            'stored_integer_vectors':len(PROTOTYPES),'literal_box_basis_count':len(data['box_basis']),
            'sparse_integer_terms':sum(len(r['weights']) for r in data['certificate_vectors']),
            'representative_children_excluded':len(orbits.REPRESENTATIVES),'raw72_phases_accounted':72,
            'smallest_prototype_physical_gap':min(r['strict_gap'] for r in answers),
            'actual_resources_checked':len(PROTOTYPES)*len(resources),
            'actual_phases_evaluated':len(PROTOTYPES)*sum(resources),
            'cluster_union_cases':len(PROTOTYPES)*b*240,
            'ordered_prototype_results_sha256':sha256(events).hexdigest(),
            'physical_action_event_sha256':action['physical_map_event_sha256'],
            'physical_generator_points':action['physical_generator_points'],
            'raw72_class_transport_points':action['raw72_class_transport_points'],
            'structural_invalid_controls_rejected':action['invalid_controls_rejected'],
            'actual_LCM_preserved':True,'parent_exclusion':True,'whole_period_exclusion':False}


def controls(data):
    edits=('bad_period','missing_vector','duplicate_vector','missing_representative','bad_basis_index',
           'zero_weight','negative_weight','duplicate_weight_term','oversized_mask','overlap',
           'weight_on_parent','different_parent')
    for edit in edits:
        invalid=deepcopy(data);row=invalid['certificate_vectors'][0]
        if edit=='bad_period':invalid['Q']=3600
        elif edit=='missing_vector':invalid['certificate_vectors'].pop()
        elif edit=='duplicate_vector':invalid['certificate_vectors'].append(deepcopy(row))
        elif edit=='missing_representative':invalid['representative_vector_phases'].pop()
        elif edit=='bad_basis_index':row['weights'][0][0]=len(invalid['box_basis'])
        elif edit=='zero_weight':row['weights'][0][1]=0
        elif edit=='negative_weight':row['weights'][0][1]=-1
        elif edit=='duplicate_weight_term':row['weights'].append(deepcopy(row['weights'][0]))
        elif edit=='oversized_mask':invalid['box_basis'][0][1]=1<<27
        elif edit=='overlap':
            index=len(invalid['box_basis']);invalid['box_basis'].append([(1<<axis)-1 for axis in AXES]);row['weights'].append([index,1])
        elif edit=='weight_on_parent':
            index=len(invalid['box_basis']);invalid['box_basis'].append([1,1,1]);row['weights']=[[index,1]]
        elif edit=='different_parent':invalid['parent_residues'][-1]=59
        try:validate(invalid);weight(invalid,0)
        except ValueError:continue
        raise ValueError('Malformed fixture accepted: '+edit)
    return list(edits)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--phase',type=int);parser.add_argument('--controls',action='store_true');args=parser.parse_args()
    raw=(HERE/'input.json').read_bytes();data=json.loads(raw);start=monotonic()
    if args.phase is None:
        result=certificate(data);result['input_sha256']=sha256(raw).hexdigest()
        need(result==json.loads((HERE/'expected.json').read_text()),'Exact result differs from expected')
    else:
        validate(data);result={'phase_result':evaluate(data,args.phase),'parent_exclusion':False,'whole_period_exclusion':False}
    rejected=controls(data) if args.controls else []
    print(json.dumps({'certificate':result,'rejected_controls':rejected,'elapsed_seconds':monotonic()-start,
                      'whole_cap_seconds':20,'independent_review':False},indent=2))
