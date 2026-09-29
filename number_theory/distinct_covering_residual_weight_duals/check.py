"""Exact solver-free check of a nonextendible 17-class prefix at L=10080.

Enumerates all 42 actual phases, with all 45 actual phases in branch 29.
Checks every remaining modulus and phase, and every weighted point.
No orbit classification or numerical solver is used in verification.
"""
import argparse
from hashlib import sha256
from itertools import product
import json
from math import gcd, prod
from pathlib import Path
from time import monotonic

L=10080
PERIODS=[32,9,5,7]
PREFIX=[(8,0),(9,0),(10,5),(12,10),(14,7),(15,1),(16,4),(18,12),(20,17),
        (21,15),(24,2),(28,23),(30,13),(32,12),(35,3),(36,6),(40,9)]
FIRST,SECOND,SECOND_PHASE=42,45,29


def normalize42(a):
    residue=a%7
    target=min(residue,4)
    phase=next(b for b in range(42) if b%6==a%6 and b%7==target)
    return phase,((3,4,residue) if residue>4 else None)


def normalize45(a):
    residue=a%9
    root=residue%3
    target=root if root in (1,2) else residue
    phase=next(b for b in range(45) if b%5==a%5 and b%9==target)
    return phase,((1,root,residue) if target!=residue else None)


def transported_boxes(boxes,swap):
    if swap is None: return boxes
    axis,a,b=swap
    result=[]
    for box in boxes:
        box=list(box); mask=box[axis]
        if ((mask>>a)^(mask>>b))&1: box[axis]^=(1<<a)|(1<<b)
        result.append(box)
    return result


def decode(boxes):
    """Explicit Cartesian boxes decoded by the integer CRT formula."""
    if prod(PERIODS)!=L or any(gcd(a,b)!=1 for i,a in enumerate(PERIODS) for b in PERIODS[i+1:]):
        raise ValueError('Invalid CRT axes')
    coefficients=[L//P*pow(L//P,-1,P) for P in PERIODS]
    weights=[0]*L
    for box in boxes:
        if len(box)!=len(PERIODS)+1: raise ValueError('Box length')
        if any(type(mask) is not int or not 0<mask<1<<P for mask,P in zip(box,PERIODS)):
            raise ValueError('Box mask')
        weight=box[-1]
        if type(weight) is not int or weight<=0: raise ValueError('Nonpositive integer weight')
        axes=[[a for a in range(P) if mask>>a&1] for mask,P in zip(box,PERIODS)]
        for coordinates in product(*axes):
            x=sum(a*c for a,c in zip(coordinates,coefficients))%L
            if weights[x]: raise ValueError('Overlapping boxes')
            weights[x]=weight
    return weights


def eligible_divisors():
    # A literal scan, separately implemented from the generator.
    return [m for m in range(8,L+1) if L%m==0]


def exact_check(anchors,weights):
    if len(weights)!=L or any(type(w) is not int or w<0 for w in weights): raise ValueError('Weight vector')
    if len({m for m,a in anchors})!=len(anchors): raise ValueError('Repeated anchor modulus')
    if any(L%m or m<8 or not 0<=a<m for m,a in anchors): raise ValueError('Anchor domain')
    support=[(x,w) for x,w in enumerate(weights) if w]
    if any(x%m==a for x,w in support for m,a in anchors): raise ValueError('Weight on a covered point')
    demand=sum(w for x,w in support)
    maxima=[]
    for m in eligible_divisors():
        if m in dict(anchors): continue
        phases=[0]*m
        for x,w in support: phases[x%m]+=w
        maxima.append((m,max(phases)))
    capacity=sum(c for m,c in maxima)
    if demand<=capacity: raise ValueError(f'Non-strict certificate: demand={demand}, capacity={capacity}')
    return demand,capacity


def verify(payload,decoder=decode,checker=exact_check):
    if payload['schema']!=1 or payload['L']!=L or payload['minimum']!=8 or payload['prime_power_axes']!=PERIODS:
        raise ValueError('Wrong certificate scope')
    if [tuple(pair) for pair in payload['prefix']]!=PREFIX: raise ValueError('Wrong prefix')
    first_expected={str(normalize42(a)[0]) for a in range(FIRST)}-{str(SECOND_PHASE)}
    second_expected={str(normalize45(a)[0]) for a in range(SECOND)}
    if set(payload['first'])!=first_expected or set(payload['second'])!=second_expected:
        raise ValueError('Incomplete certificate table')
    events=[]
    def visit(anchors,boxes,swap):
        weights=decoder(transported_boxes(boxes,swap))
        demand,capacity=checker(anchors,weights)
        events.append([anchors[len(PREFIX):],demand,capacity])
    for a in range(FIRST):
        if a==SECOND_PHASE:
            for b in range(SECOND):
                representative,swap=normalize45(b)
                boxes=payload['boxes'][payload['second'][str(representative)]]
                visit(PREFIX+[(FIRST,a),(SECOND,b)],boxes,swap)
        else:
            representative,swap=normalize42(a)
            boxes=payload['boxes'][payload['first'][str(representative)]]
            visit(PREFIX+[(FIRST,a)],boxes,swap)
    encoded=json.dumps(events,separators=(',',':')).encode('ascii')
    return {'claim':'The specified 17-class prefix has no distinct minimum-eight covering extension at LCM 10080.',
            'literal_terminal_branches':len(events),'representative_certificates':len(first_expected)+len(second_expected),
            'stored_box_vectors':len(payload['boxes']),'minimum_integer_gap':min(d-c for a,d,c in events),
            'events_sha256':sha256(encoded).hexdigest()}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate',type=Path,default=Path(__file__).with_name('certificates.json'))
    parser.add_argument('--check',type=Path)
    parser.add_argument('--write',type=Path)
    args=parser.parse_args(); start=monotonic()
    result=verify(json.loads(args.certificate.read_text()))
    if args.check and result!=json.loads(args.check.read_text()): raise ValueError('Manifest differs')
    if args.write: args.write.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    print(f'EXACT CHECK PASSED; 17-class prefix excluded. Seconds: {monotonic()-start:.3f}')
