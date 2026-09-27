#!/usr/bin/env python3
"""Exact source-cluster bounds; no Gaussian hinge evaluation or exact-zero claim."""

import argparse
from copy import deepcopy
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, groupby, product
import json
from math import isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
CAP = F(7, 50)


def need(condition, message):
    if not condition:
        raise ValueError(message)


def rat(value):
    need(type(value) in (int, str), 'rational entries must be integers or strings')
    return F(value)


def ceilq(q):
    return -((-q.numerator)//q.denominator)


def distance2(x, y):
    return sum((a-b)**2 for a, b in zip(x, y))


def sqrt_bounds(q, bits):
    need(q >= 0, 'negative square-root input')
    scale = 1 << bits
    v = isqrt((q.numerator*scale*scale)//q.denominator)
    lo = F(v, scale)
    hi = lo if lo*lo == q else F(v+1, scale)
    need(lo*lo <= q <= hi*hi, 'square-root enclosure')
    return lo, hi


def radius_units(r2, bits):
    """Ceiling of the credited local bound in units 2**(-bits)."""
    Q = 1 << bits
    need(r2 >= 0, 'negative normalized radius')
    if not r2:
        return 0, None
    k = 1//(8*r2)
    if k < 2:
        return ceilq(CAP*Q), k
    numerator, shift = 16*k, 5*k-bits
    if shift <= 0:
        units = numerator << (-shift)
    elif shift >= numerator.bit_length():
        units = 1
    else:
        units = (numerator+(1 << shift)-1)//(1 << shift)
    return min(units, ceilq(CAP*Q)), k


def wrong_label_units(d2, radius_upper, bits, geometry_bits):
    """Upper bound for one wrong nearest-center choice; distances/noise normalized."""
    Q = 1 << bits
    distance_lower = sqrt_bounds(d2, geometry_bits)[0]
    if distance_lower == 0:
        return Q
    margin = distance_lower/2-radius_upper
    if margin < 0:
        return Q
    exponent = (margin*margin/2).__floor__()+1
    return 1 if exponent >= bits else 1 << (bits-exponent)


def read_instance(obj):
    need(isinstance(obj, dict), 'instance object required')
    need(set(obj) <= {'source','target','weights','variance'}, 'unknown instance field')
    clouds = []
    for field in ('source','target'):
        rows = obj.get(field)
        need(isinstance(rows,list) and rows, 'nonempty coordinate arrays required')
        need(all(isinstance(v,list) and len(v)==3 for v in rows), 'dimension three required')
        clouds.append([tuple(rat(a) for a in v) for v in rows])
    xs, ys = clouds
    need(isinstance(obj.get('weights'),list), 'weight list required')
    ws = [rat(w) for w in obj['weights']]
    need(len(xs)==len(ys)==len(ws), 'label counts')
    need(all(w>=0 for w in ws) and sum(ws)==1, 'probability weights')
    s = rat(obj.get('variance',1))
    need(s>0, 'positive variance required')
    for i,j in combinations(range(len(ws)),2):
        need(distance2(xs[i],xs[j])>=distance2(ys[i],ys[j]), 'input is not a contraction')
    groups = {}
    for x,y,w in zip(xs,ys,ws):
        if w:
            groups[x,y] = groups.get((x,y),F(0))+w
    xs = [xy[0] for xy in groups]
    ys = [xy[1] for xy in groups]
    ws = list(groups.values())
    return xs,ys,ws,s


def partitions(dist):
    """All single-linkage cuts; tied distances are processed together."""
    n=len(dist)
    parent=list(range(n))
    def find(i):
        while parent[i]!=i:
            parent[i]=parent[parent[i]]
            i=parent[i]
        return i
    def current():
        d={}
        for i in range(n):
            d.setdefault(find(i),[]).append(i)
        return sorted(d.values(),key=lambda row:row[0])
    yield current()
    edges=sorted((dist[i][j],i,j) for i,j in combinations(range(n),2))
    for _,group in groupby(edges,key=lambda edge:edge[0]):
        changed=False
        for _,i,j in group:
            a,b=find(i),find(j)
            if a!=b:
                parent[max(a,b)]=min(a,b);changed=True
        if changed:
            yield current()


def evaluate_partition(dist,weights,partition,bits=40,geometry_bits=16):
    n=len(dist);Q=1 << bits
    need(sorted(i for row in partition for i in row)==list(range(n)) and
         all(row for row in partition), 'partition must cover every active label once')
    rows=[]
    for members in partition:
        r2,anchor=min((max(dist[a][j] for j in members),a) for a in members)
        units,k=radius_units(r2,bits)
        rows.append({'members':members,'anchor':anchor,'r2':r2,
                     'radius_upper':sqrt_bounds(r2,geometry_bits)[1],
                     'mass':sum(weights[j] for j in members),
                     'local_units':units,'local_k':k})
    total=F(0);worst=0
    for i,row in enumerate(rows):
        wrong=sum(wrong_label_units(dist[row['anchor']][other['anchor']],
                                    row['radius_upper'],bits,geometry_bits)
                  for j,other in enumerate(rows) if j!=i)
        row['classification_units']=min(Q,wrong)
        cost=row['local_units']+row['classification_units']
        total+=row['mass']*cost;worst=max(worst,cost)
    result={'weighted_units_ceiling':ceilq(total),
            'defect_upper_bound':str(min(CAP,F(ceilq(total),Q))),
            'all_masses_upper_bound':str(min(CAP,F(worst,Q))),
            'all_masses_scope':'Certified active components only; discarded zero-weight sites are not added to the cover',
            'components':[]}
    for row in rows:
        result['components'].append({
            'members':row['members'],'source_anchor':row['anchor'],
            'mass':str(row['mass']),'radius_squared_over_variance':str(row['r2']),
            'normalized_radius_upper':str(row['radius_upper']),
            'local_error_units':row['local_units'],'local_radius_k':row['local_k'],
            'classification_error_units':row['classification_units']})
    return result


def certify(obj,bits=40,geometry_bits=16):
    need(type(bits) is int and 1<=bits<=4096,'output precision must be 1..4096 bits')
    need(type(geometry_bits) is int and 0<=geometry_bits<=4096,'geometry precision must be 0..4096 bits')
    xs,ys,ws,s=read_instance(obj)
    dist=[[distance2(x,y)/s for y in xs] for x in xs]
    best=None;counts=[]
    for part in partitions(dist):
        candidate=evaluate_partition(dist,ws,part,bits,geometry_bits)
        counts.append(len(part))
        if best is None or F(candidate['defect_upper_bound'])<F(best['defect_upper_bound']):
            best=candidate
    normalized={'source':[[str(v) for v in row] for row in xs],
                'target':[[str(v) for v in row] for row in ys],
                'weights':[str(w) for w in ws],'variance':str(s)}
    digest=sha256(json.dumps(normalized,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return {'status':'ALL_THRESHOLD_DEFECT_UPPER_BOUND','active_labels':len(ws),
            'bits':bits,'geometry_bits':geometry_bits,'variance':str(s),
            'normalized_input_sha256':digest,
            'candidate_component_counts':counts,'selected_component_count':len(best['components']),
            'certificate':best,'exact_majorisation_certified':F(best['defect_upper_bound'])==0,
            'scope':'Actual all-threshold upper bound; no exact sign is inferred from a positive bound'}


def pinned_inputs():
    obj=json.loads((HERE/'CLUSTER_INPUTS.json').read_text())
    need(obj.get('schema')==1 and obj.get('files'),'dependency manifest')
    for name,digest in obj['files'].items():
        need(sha256((HERE/name).read_bytes()).hexdigest()==digest,'changed dependency: '+name)
    return len(obj['files'])


def reject(fn):
    try:
        fn()
    except (ValueError,KeyError,TypeError,ZeroDivisionError):
        return
    raise ValueError('malformed control was accepted')


def controls():
    from paired_cubature import budget,check_grid
    from signed_endpoints import exact_rank
    dependencies=pinned_inputs()
    mixture=0
    for values in product((F(0),F(1,4),F(1),F(2)),repeat=3):
        for threshold in (F(0),F(1,3),F(1),F(3)):
            interaction=max(F(0),sum(values)-threshold)-sum(max(F(0),v-threshold) for v in values)
            for selected in range(3):
                need(0<=interaction<=sum(values)-values[selected],'source interaction inequality')
                mixture+=1
    roots=0
    for q in (F(0),F(1,64),F(2),F(1,7),F(3,1000000),F(256),F(257),F(1024)):
        for bits in range(13):
            lo,hi=sqrt_bounds(q,bits)
            need(lo*lo<=q<=hi*hi and hi-lo<=F(1,1<<bits),'root enclosure width')
            roots+=1
    rounding=0
    for k in range(2,129):
        exact=F(16*k,1 << (5*k))
        for bits in (8,16,40,128):
            units,seen=radius_units(F(1,8*k),bits)
            need(seen==k and exact<=F(units,1<<bits)<exact+F(1,1<<bits),'upward local error')
            rounding+=1
    huge=radius_units(F(1,8*10**12),40)
    need(huge==(1,10**12),'large exponent was not safely compressed')
    halfspaces=0
    for dx,dy,dz in product(range(-2,3),repeat=3):
        if not (dx or dy or dz):continue
        c=(F(dx),F(dy),F(dz));origin=(F(0),)*3
        for z in ((F(0),F(0),F(0)),(F(1),F(-2),F(3)),(F(-3),F(1),F(2))):
            lhs=distance2(z,c)-distance2(z,origin)
            rhs=distance2(c,origin)-2*sum(a*b for a,b in zip(c,z))
            need(lhs==rhs,'Voronoi half-space identity');halfspaces+=1
    schedules=0
    for bits in range(65):
        k=1+(bits+4)//4
        need(F(16*k,1 << (5*k))<=F(1,1 << (bits+1)),'local tolerance schedule')
        for count in (2,3,7,16,129):
            ell=(count-2).bit_length()
            need(F(count-1,1 << (bits+ell+1))<=F(1,1 << (bits+1)),'separation schedule')
            schedules+=1
    fixture=json.loads((HERE/'CLUSTER_FIXTURE.json').read_text())
    result=certify(fixture)
    xs,ys,ws,s=read_instance(fixture)
    b=budget(8);L,W=b['coordinate_denominator'],b['weight_denominator']
    grid=check_grid(8,[tuple(int(v*L) for v in row) for row in xs],
                    [tuple(int(v*L) for v in row) for row in ys],
                    [int(w*W) for w in ws])
    need(all(v*L==(v*L).__floor__() for row in xs+ys for v in row) and
         all(w*W==(w*W).__floor__() for w in ws),'fixture exact denominators')
    local_ranks=[]
    for start in range(0,49,7):
        rows=[tuple(a-b for a,b in zip(xs[i],xs[start]))+
              tuple(a-b for a,b in zip(ys[i],ys[start])) for i in range(start+1,start+7)]
        local_ranks.append(exact_rank(rows))
    need(local_ranks==[6]*7,'local paired ranks')
    need(result['selected_component_count']==7,'automatic partition did not find source balls')
    need(F(result['certificate']['all_masses_upper_bound'])<=F(13,1<<33),'complete source-region bound')
    need(F(result['certificate']['defect_upper_bound'])<=F(13,1<<33),'weighted source-region bound')
    # Transform before geometric rounding, so normalized distance matrices agree.
    shifted=deepcopy(fixture)
    for field,shift in [('source',(3,-4,2)),('target',(-5,1,6))]:
        shifted[field]=[[str(2*F(v)+shift[j]) for j,v in enumerate(row)] for row in fixture[field]]
    shifted['variance']=4
    moved=certify(shifted)
    need(moved['certificate']==result['certificate'] and moved['candidate_component_counts']==result['candidate_component_counts'],
         'translation and variance-scaled geometry')
    split=deepcopy(fixture)
    split['source'].append(split['source'][0][:]);split['target'].append(split['target'][0][:])
    half=F(split['weights'][0])/2
    split['weights'][0]=str(half);split['weights'].append(str(half))
    need(certify(split)==result,'duplicate source/image merge')
    zero=deepcopy(fixture)
    zero['source'].append(zero['source'][0][:]);zero['target'].append(zero['target'][0][:]);zero['weights'].append(0)
    need(certify(zero)==result,'zero masses')
    point=certify({'source':[[1,2,3]],'target':[[4,0,-1]],'weights':[1]})
    need(point['exact_majorisation_certified'],'point equality')
    collapse=deepcopy(fixture);collapse['target']=[[0,0,0] for _ in xs]
    need(certify(collapse)['certificate']==result['certificate'],'target merging changed source bound')
    bad=[]
    for weights in ([1,1],[-1,2],[0.5,0.5],[True,False]):
        bad.append({'source':[[0,0,0],[1,0,0]],'target':[[0,0,0],[0,0,0]],'weights':weights})
    bad.append({'source':[[0,0,0],[0,0,0]],'target':[[0,0,0],[1,0,0]],'weights':['1/2','1/2']})
    bad.append({'source':[[0,0,0],[1,0,0]],'target':[[0,0,0],[2,0,0]],'weights':['1/2','1/2']})
    bad.append({'source':[[0,0]],'target':[[0,0,0]],'weights':[1]})
    bad.append({'source':[[0,0,0]],'target':[[0,0,0]],'weights':[1],'variance':0})
    for obj in bad:reject(lambda obj=obj:certify(obj))
    reject(lambda:certify(fixture,bits=True))
    reject(lambda:evaluate_partition([[F(0),F(1)],[F(1),F(0)]],[F(1,2)]*2,[[0],[0]]))
    return {'status':'SOURCE_CLUSTER_DEFECT_CERTIFICATES_PASS','pinned_dependencies':dependencies,
            'mixture_controls':mixture,'root_controls':roots,'local_rounding_controls':rounding,
            'half_space_controls':halfspaces,'tolerance_controls':schedules,
            'malformed_controls_rejected':len(bad)+2,'symmetry_mass_target_controls':4,
            'huge_local_exponent_control':{'k':huge[1],'upward_units':huge[0],'bits':40},
            'uniform_seven_ball_bound':str(F(13,1<<33)),'fixture_grid':grid,
            'component_paired_ranks':local_ranks,'fixture_certificate':result,
            'point_certificate':point}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group()
    group.add_argument('--check',action='store_true')
    group.add_argument('--input',type=Path)
    parser.add_argument('--bits',type=int,default=40)
    parser.add_argument('--geometry-bits',type=int,default=16)
    parser.add_argument('--expected',type=Path,default=HERE/'CLUSTER_EXPECTED.json')
    args=parser.parse_args()
    if args.input:
        answer=certify(json.loads(args.input.read_text()),args.bits,args.geometry_bits)
    else:
        answer=controls()
        if args.check:
            need(answer==json.loads(args.expected.read_text()),'complete cluster certificate differs')
            print(answer['status']);return
    print(json.dumps(answer,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
