"""Literal physical phases and binary unions; standard library only."""
from copy import deepcopy
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
N,B,C,b,Q = 43200,64,675,16,720


def need(condition,message):
    if not condition:
        raise ValueError(message)


def evaluate(data):
    need(all(type(data[k]) is int and data[k]==v for k,v in
             [('N',N),('B',B),('C',C),('b',b),('Q',Q)]),'Unexpected implemented parameters')
    need(data['axes']==[16,9,5] and data['cluster']==[3,5],'Unexpected axes or cluster')
    known = tuple(tuple(p) for p in data['known'])
    need(all(len(p)==2 and all(type(v) is int for v in p) for p in known),'Malformed known class')
    need(len({m for m,a in known})==len(known),'Repeated known modulus')
    need(all(m>=8 and N%m==0 and 0<=a<m for m,a in known),'Invalid known divisor or phase')
    resources = [n for n in range(8,N+1) if N%n==0 and n not in dict(known)]
    top = {B*d for d in range(1,C+1) if C%d==0}
    need(top<=set(resources),'All top resources must remain eligible and unplaced')
    boxes = data['boxes']
    need(all(len(box)==4 and all(type(v) is int for v in box) and box[3]>0 and
             all(0<mask<1<<axis for mask,axis in zip(box[:3],data['axes'])) for box in boxes),
         'Malformed positive literal box')
    base = []
    for x in range(Q):
        hits = [box[3] for box in boxes if all(mask>>(x%axis)&1
                                              for mask,axis in zip(box[:3],data['axes']))]
        need(len(hits)<=1,'Overlapping boxes')
        base.append(hits[0] if hits else 0)
    need(any(base),'Zero certificate')
    vector = base*(N//Q)
    need(all(not w or all(x%m!=a for m,a in known) for x,w in enumerate(vector)),
         'Weight on a prescribed physical class')
    nonzero = [(x,w) for x,w in enumerate(vector) if w]
    capacities,H = {},{}
    phase_hash = sha256()
    for n in resources:
        populations = [0]*n
        for x,w in nonzero:
            populations[x%n] += w
        capacities[n] = max(populations)
        phase_hash.update(json.dumps([n,populations],separators=(',',':')).encode()+b'\n')
        if n in top and n!=B:
            H[n//B] = [max(populations[t::b]) for t in range(b)]
    M = {d:capacities[B*d] for d in H}
    label_totals = []
    cluster_totals = []
    pair_comparison = []
    case_hash = sha256()
    for t in range(b):
        # This ordinary progression is the opposite point of the binary block.
        points = [(x,vector[x]) for x in range(t+B//2,N,B) if vector[x]]
        values = []
        for a,r in product(range(-1,3),range(-1,5)):
            inside = [(d,s) for d,s in [(3,a),(5,r)] if s>=0]
            outside = [d for d,s in [(3,a),(5,r)] if s<0]
            union_mass = sum(w for x,w in points if any(x%d==s for d,s in inside))
            value = 2*union_mass+sum(M[d] for d in outside)
            case_hash.update(json.dumps([t,[a,r],value],separators=(',',':')).encode()+b'\n')
            values.append(value)
        cluster_totals.append(max(values))
        other = sum(max(M[d],2*H[d][t]) for d in H if d not in (3,5))
        label_totals.append(max(values)+other)
        both = max(sum(w*(2*(x%3==a)+2*(x%5==r)-((x%3==a) and (x%5==r)))
                       for x,w in points) for a in range(3) for r in range(5))
        pair_comparison.append(max(M[3]+M[5],2*H[3][t]+M[5],M[3]+2*H[5][t],both)+other)
    outside_total = sum(capacities[n] for n in resources if n not in top)
    ordinary = sum(capacities.values())
    old_G = max(sum(max(M[d],2*H[d][t]) for d in H) for t in range(b))
    total = outside_total+max(label_totals)
    return {'N':N,'Q':Q,'known_classes':len(known),'boxes':len(boxes),
            'actual_resources':len(resources),'outside_resources':len(resources)-len(top),
            'actual_phases_evaluated':sum(resources),'cluster_union_cases':b*4*6,
            'physical_demand':sum(vector),'outside_capacity':outside_total,
            'binary_union_top_budget':max(label_totals),'total_capacity':total,
            'strict_gap':sum(vector)-total,'ordinary_capacity':ordinary,
            'old_fibre_capacity':ordinary-capacities[1728]+capacities[8640]+capacities[N],
            'old_coarsest_G_capacity':outside_total+old_G,
            'reviewer_pair_capacity':outside_total+max(pair_comparison),
            'label_totals':label_totals,'cluster_label_totals':cluster_totals,
            'all_physical_phase_values_sha256':phase_hash.hexdigest(),
            'cluster_case_values_sha256':case_hash.hexdigest(),
            'base_weight_sha256':sha256(json.dumps(base,separators=(',',':')).encode()).hexdigest()}


def positive_control():
    # A small real cover, minimum2. This is not a target construction.
    classes = [(2,0),(3,0),(6,1),(4,1),(12,11)]
    need(all(any(x%m==a for m,a in classes) for x in range(12)),'Control is not a cover')
    w = [int(x%6==5) for x in range(12)]
    need(all(not v or all(x%m!=a for m,a in classes[:3]) for x,v in enumerate(w)),
         'Control weight has wrong support')
    populations = [sum(w[x] for x in range(a,12,12)) for a in range(12)]
    H = [max(populations[t::2]) for t in range(2)]
    G = max(max(max(populations),2*h) for h in H)
    need(sum(w)==G==2,'Small binary budget equation fails')
    return {'ambient_N':12,'minimum_modulus':2,'literal_cover':True,'demand':2,'top_upper_budget':2}


def malformed_controls(data):
    variants = []
    for edit in ('zero_mask','negative_weight','duplicate_box','duplicate_modulus','known_top',
                 'bad_block_period','known_weight','nondivisor','bad_phase','float_weight','zero_vector'):
        invalid = deepcopy(data)
        if edit=='zero_mask':invalid['boxes'][0][0]=0
        elif edit=='negative_weight':invalid['boxes'][0][3]=-1
        elif edit=='duplicate_box':invalid['boxes'].append(invalid['boxes'][0])
        elif edit=='duplicate_modulus':invalid['known'].append(invalid['known'][0])
        elif edit=='known_top':invalid['known'].append([64,0])
        elif edit=='bad_block_period':invalid['b']=3
        elif edit=='known_weight':invalid['boxes'].append([1,1,1,1])
        elif edit=='nondivisor':invalid['known'].append([7,0])
        elif edit=='bad_phase':invalid['known'][0][1]=8
        elif edit=='float_weight':invalid['boxes'][0][3]=0.5
        elif edit=='zero_vector':invalid['boxes']=[]
        try:evaluate(invalid)
        except ValueError:variants.append(edit)
        else:raise ValueError('Invalid input accepted: '+edit)
    return variants


def main():
    data = json.loads((HERE/'input.json').read_text())
    result = evaluate(data)
    need(result['strict_gap']>0,'No strict conditional exclusion')
    output = {'actual_author':'six-covering-3','role':'researcher','all_passed':True,
              'certificate':result,'positive_control':positive_control(),
              'malformed_rejections':malformed_controls(data),
              'input_sha256':sha256((HERE/'input.json').read_bytes()).hexdigest(),
              'independent_review_claimed':False,'full43200_exclusion':False,
              'numerical_L_min8_bound_changed':False}
    expected = json.loads((HERE/'expected.json').read_text())
    need(output==expected,'Exact results differ from pinned expected evidence')
    print(json.dumps(output,indent=2))


if __name__=='__main__':main()
