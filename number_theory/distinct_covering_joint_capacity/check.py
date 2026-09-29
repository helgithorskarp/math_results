"""Definition-level exact check of the published grouped-weight certificate.

No solver, orbit classifier, CRT formula, or branch-search corpus is needed.
All congruences and all 7840 phase pairs are literal finite sets.
"""
import argparse
from hashlib import sha256
import json
from math import lcm
from pathlib import Path
from time import monotonic

L=10080
PERIODS=(32,9,5,7)
PREFIX=((8,0),(9,0),(10,5),(12,10),(14,7),(15,1),(16,4),(18,12),(20,17),
        (21,7),(24,2),(28,1),(30,23))
PAIRS=((40,42),(32,35),(45,56),(36,70))


def verify(payload,encoded=None):
    if payload['L']!=L or payload['minimum']!=8:
        raise ValueError('Wrong period or minimum')
    if tuple(map(tuple,payload['anchors']))!=PREFIX or tuple(map(tuple,payload['pairs']))!=PAIRS:
        raise ValueError('Wrong declared case')
    if len({m for m,a in PREFIX})!=len(PREFIX) or min(m for m,a in PREFIX)!=8:
        raise ValueError('Repeated modulus or wrong minimum')
    if any(L%m or not 0<=a<m for m,a in PREFIX): raise ValueError('Invalid anchor')
    boxes=payload['boxes']
    for box in boxes:
        if len(box)!=5 or type(box[-1]) is not int or box[-1]<=0:
            raise ValueError('Invalid positive integer box')
        if any(type(mask) is not int or not 0<mask<1<<P for P,mask in zip(PERIODS,box[:-1])):
            raise ValueError('Invalid axis mask')
    candidates=[[box for box in boxes if box[0]>>r&1] for r in range(32)]
    weights=[]; uncovered=[]
    for x in range(L):
        hits=[box[-1] for box in candidates[x%32]
              if all(box[i]>>(x%P)&1 for i,P in enumerate(PERIODS[1:],1))]
        if len(hits)>1: raise ValueError('Overlapping boxes')
        w=hits[0] if hits else 0
        free=all(x%m!=a for m,a in PREFIX)
        if w and not free: raise ValueError('Positive weight on a covered point')
        weights.append(w);uncovered.append(free)
    available=[m for m in range(8,L+1) if L%m==0 and m not in {n for n,a in PREFIX}]
    paired={m for pair in PAIRS for m in pair}
    if len(paired)!=2*len(PAIRS) or not paired.issubset(available):
        raise ValueError('Groups do not partition available resources')
    single={m:max(sum(weights[a::m]) for a in range(m)) for m in available}
    uniform=sum(max(sum(uncovered[a::m]) for a in range(m)) for m in available)
    capacities=[];events=[]
    for m,n in PAIRS:
        left=[set(range(a,L,m)) for a in range(m)]
        right=[set(range(b,L,n)) for b in range(n)]
        largest=0
        for a,A in enumerate(left):
            for b,B in enumerate(right):
                value=sum(weights[x] for x in A|B)
                events.append([m,n,a,b,value])
                largest=max(largest,value)
        capacities.append([m,n,largest])
    demand=sum(weights)
    individual=sum(single.values())
    joint=sum(v for m,v in single.items() if m not in paired)+sum(v for m,n,v in capacities)
    if (demand,joint,individual)!=(payload['demand'],payload['joint_capacity'],payload['individual_capacity']):
        raise ValueError('Recorded capacities differ from literal sets')
    if demand<=joint: raise ValueError('Not a strict nonextension certificate')
    result={'L':L,'minimum':8,'anchor_count':len(PREFIX),'anchor_lcm':lcm(*(m for m,a in PREFIX)),
            'remaining_moduli':len(available),'resource_groups':len(available)-len(PAIRS),
            'uncovered_points':sum(uncovered),'positive_weight_points':sum(w>0 for w in weights),
            'positive_boxes':len(boxes),'demand':demand,'individual_capacity':individual,
            'pair_capacities':capacities,'joint_capacity':joint,'strict_gap':demand-joint,
            'uniform_residual_capacity':uniform,'uniform_total_upper':L-sum(uncovered)+uniform,
            'literal_phase_pairs':len(events),
            'phase_events_sha256':sha256(json.dumps(events,separators=(',',':')).encode('ascii')).hexdigest()}
    if encoded is not None: result['certificate_sha256']=sha256(encoded).hexdigest()
    return result


if __name__=='__main__':
    root=Path(__file__).resolve().parent
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate',type=Path,default=root/'certificate.json')
    parser.add_argument('--expected',type=Path)
    parser.add_argument('--write-expected',type=Path)
    args=parser.parse_args();start=monotonic()
    encoded=args.certificate.read_bytes(); result=verify(json.loads(encoded),encoded)
    expected=args.expected
    if expected is None and args.certificate==root/'certificate.json' and not args.write_expected:
        expected=root/'expected.json'
    if expected is not None and result!=json.loads(expected.read_text()): raise ValueError('Manifest differs')
    if args.write_expected: args.write_expected.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'CHECK':'COMPLETE EXACT NONEXTENSION',**result,'seconds':monotonic()-start},indent=2))
