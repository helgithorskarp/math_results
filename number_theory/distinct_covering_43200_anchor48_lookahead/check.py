"""All48 raw phases for either stated parent; literal integers, no solver."""
import argparse
from copy import deepcopy
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
from time import monotonic

HERE=Path(__file__).resolve().parent
N,Q,B,C,b=43200,3600,64,675,16
ORDER=(8,9,10,12,15,16,18,20,24,25,30,36,40,45)
COMMON=(0,0,5,10,1,4,3,17,2,1,13,6,27)


def need(condition,message):
    if not condition:
        raise ValueError(message)


def validate(data):
    need(all(type(data[k]) is int and data[k]==v for k,v in
             [('N',N),('Q',Q),('B',B),('C',C),('b',b),('extra_modulus',48)]),
         'Unexpected implemented parameters')
    need(data['axes']==[16,9,25] and data['cluster']==[3,5] and
         all(type(v) is int for v in data['axes']+data['cluster']),'Unexpected axes or cluster')
    need(data['parent_moduli']==list(ORDER) and data['common_residues']==list(COMMON) and
         all(type(v) is int for v in data['parent_moduli']+data['common_residues']),
         'Unexpected conditional parent classes')
    need([p['phase45'] for p in data['parents']]==[33,38] and
         all(type(p['phase45']) is int for p in data['parents']),'Missing or different parent')
    for parent in data['parents']:
        phases=[r['phase48'] for r in parent['exceptions']]
        need(len(phases)==len(set(phases)) and all(type(a) is int and 0<=a<48 for a in phases),
             'Invalid or duplicate exceptional phase')


def weight(data,known,boxes):
    if boxes is None:
        return [int(all(x%m!=a for m,a in known)) for x in range(Q)]
    need(all(len(box)==4 and all(type(v) is int for v in box) and box[3]>0 and
             all(0<mask<1<<axis for mask,axis in zip(box[:3],data['axes'])) for box in boxes),
         'Malformed positive literal box')
    base=[]
    for x in range(Q):
        hits=[box[3] for box in boxes if all(mask>>(x%axis)&1
                                            for mask,axis in zip(box[:3],data['axes']))]
        need(len(hits)<=1,'Overlapping boxes')
        base.append(hits[0] if hits else 0)
    need(any(base),'Zero certificate')
    need(all(not w or all(x%m!=a for m,a in known) for x,w in enumerate(base)),
         'Positive weight on a prescribed class')
    return base


def evaluate(data,parent,a):
    need(type(a) is int and 0<=a<48,'Invalid raw phase')
    known=tuple(zip(ORDER,COMMON+(parent['phase45'],)))+((48,a),)
    exceptions={r['phase48']:r['boxes'] for r in parent['exceptions']}
    base=weight(data,known,exceptions.get(a))
    need(any(base),'An indicator weight must also be nonzero')
    vector=base*(N//Q)
    resources=[n for n in range(8,N+1) if N%n==0 and n not in dict(known)]
    top={B*d for d in range(1,C+1) if C%d==0}
    need(top<=set(resources),'Every top resource must be eligible and unplaced')
    nonzero=[(x,w) for x,w in enumerate(vector) if w]
    capacities,H={},{}
    phase_hash=sha256()
    for n in resources:
        populations=[0]*n
        for x,w in nonzero:
            populations[x%n]+=w
        capacities[n]=max(populations)
        phase_hash.update(json.dumps([n,populations],separators=(',',':')).encode()+b'\n')
        if n in top and n!=B:
            H[n//B]=[max(populations[t::b]) for t in range(b)]
    M={d:capacities[B*d] for d in H}
    labels=[]
    case_hash=sha256()
    for t in range(b):
        points=[(x,vector[x]) for x in range(t+B//2,N,B) if vector[x]]
        values=[]
        for s,r in product(range(-1,3),range(-1,5)):
            inside=[(d,v) for d,v in [(3,s),(5,r)] if v>=0]
            outside=[d for d,v in [(3,s),(5,r)] if v<0]
            mass=sum(w for x,w in points if any(x%d==v for d,v in inside))
            value=2*mass+sum(M[d] for d in outside)
            case_hash.update(json.dumps([t,[s,r],value],separators=(',',':')).encode()+b'\n')
            values.append(value)
        labels.append(max(values)+sum(max(M[d],2*H[d][t]) for d in H if d not in (3,5)))
    outside_total=sum(capacities[n] for n in resources if n not in top)
    total=outside_total+max(labels)
    result={'phase48':a,'demand':sum(vector),'outside_capacity':outside_total,
            'top_budget':max(labels),'total_capacity':total,'strict_gap':sum(vector)-total,
            'resource_phase_values_sha256':phase_hash.hexdigest(),
            'union_case_values_sha256':case_hash.hexdigest(),
            'base_weight_sha256':sha256(json.dumps(base,separators=(',',':')).encode()).hexdigest()}
    need(result['strict_gap']>0,'This phase has no strict integer exclusion')
    return result


def controls(data):
    rejected=[]
    for edit in ['bad_period','duplicate_exception','bad_exception_phase','zero_weight',
                 'negative_weight','overlapping_boxes','weight_on_known_class']:
        invalid=deepcopy(data)
        parent=invalid['parents'][0]
        if edit=='bad_period':invalid['b']=3
        elif edit=='duplicate_exception':parent['exceptions'].append(parent['exceptions'][0])
        elif edit=='bad_exception_phase':parent['exceptions'][0]['phase48']=48
        elif edit=='zero_weight':parent['exceptions'][0]['boxes']=[]
        elif edit=='negative_weight':parent['exceptions'][0]['boxes'][0][3]=-1
        elif edit=='overlapping_boxes':parent['exceptions'][0]['boxes'].append(parent['exceptions'][0]['boxes'][0])
        elif edit=='weight_on_known_class':parent['exceptions'][0]['boxes']=[[1,1,1,1]]
        try:
            validate(invalid)
            evaluate(invalid,parent,parent['exceptions'][0]['phase48'])
        except ValueError:
            rejected.append(edit)
        else:
            raise ValueError('Malformed certificate accepted: '+edit)
    return rejected


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--parent',type=int,choices=(33,38),required=True)
    parser.add_argument('--phase',type=int)
    parser.add_argument('--controls',action='store_true')
    args=parser.parse_args()
    data=json.loads((HERE/'input.json').read_text())
    validate(data)
    parent=next(p for p in data['parents'] if p['phase45']==args.parent)
    if args.phase is not None:
        print(json.dumps({'parent45':args.parent,'single_phase_only':True,
                          'parent_exclusion':False,'phase':evaluate(data,parent,args.phase)},indent=2))
        return
    start=monotonic()
    rows=[]
    for a in range(48):
        if monotonic()-start>=20:
            raise RuntimeError('Incomplete exact check at the20s cap; no parent exclusion')
        rows.append(evaluate(data,parent,a))
    resources=[n for n in range(8,N+1) if N%n==0 and n not in ORDER+(48,)]
    result={'parent45':args.parent,'raw_phases_checked':len(rows),'parent_exclusion':True,
            'minimum_physical_gap':min(r['strict_gap'] for r in rows),
            'resources_per_phase':len(resources),'actual_resources_checked':48*len(resources),
            'actual_phases_evaluated':48*sum(resources),'union_cases_evaluated':48*b*4*6,
            'exception_phases':[r['phase48'] for r in parent['exceptions']],
            'all_phase_results_sha256':sha256(json.dumps(rows,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
            'input_sha256':sha256((HERE/'input.json').read_bytes()).hexdigest(),
            'actual_author':'six-covering-3','role':'researcher','independent_review_claimed':False,
            'full43200_exclusion':False,'numerical_L_min8_bound_changed':False}
    expected=json.loads((HERE/'expected.json').read_text())
    need(result==expected[str(args.parent)],'Exact result differs from the separately pinned evidence')
    if args.controls:
        result={'certificate':result,'malformed_rejections':controls(data)}
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
