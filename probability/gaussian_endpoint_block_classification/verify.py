#!/usr/bin/env python3
"""Compact exact controls, not Gaussian quadrature or a proof of the conjecture."""
import argparse
import copy
from fractions import Fraction as F
import itertools
import json
from pathlib import Path

import certificate as producer
import check_certificate as consumer


def wire(p, q):
    return {'source': [[str(F(x)) for x in row] for row in p],
            'target': [[str(F(x)) for x in row] for row in q]}


def layers(m):
    core = [(2,2,2), (3,2,2), (2,3,2), (2,2,3)]
    p, q = core[:], core[:]
    rays = [(F(1,3),F(2,3),F(2,3)), (F(2,3),F(1,3),F(2,3)),
            (F(6,7),F(2,7),F(3,7))]
    for k in range(m):
        scale = 8**k
        for i in range(3):
            p.append(tuple(-scale if j == i else 0 for j in range(3)))
            q.append(tuple(F(3,4)*scale*x for x in rays[i]))
    return wire(p, q)


def ordered_partitions(labels):
    if not labels:
        yield []
        return
    for partition in ordered_partitions(labels[:-1]):
        v = labels[-1]
        for j in range(len(partition)):
            out = [block[:] for block in partition]
            out[j].append(v)
            yield out
        for j in range(len(partition)+1):
            yield partition[:j]+[[v]]+partition[j:]


def direct_admissible(p, q, partition):
    state = p[:]
    for block in partition:
        new = state[:]
        for i in block:
            new[i] = q[i]
        for i in range(len(p)):
            for j in range(i):
                if consumer.square_distance(new[i], new[j]) > consumer.square_distance(state[i], state[j]):
                    return False
        state = new
    return state == q


def rejected(call):
    try:
        call()
    except (ValueError, TypeError, KeyError, ZeroDivisionError):
        return 1
    raise RuntimeError('Invalid input or certificate was accepted')


def audit():
    # Different formulation: exhaustive weak orders, without SCC reachability.
    arcs = [(i,j) for i in range(4) for j in range(4) if i != j]
    partitions = list(ordered_partitions(list(range(4))))
    tests = []
    for part in partitions:
        time = {v:k for k,block in enumerate(part) for v in block}
        forbidden = sum(1<<k for k,(u,v) in enumerate(arcs) if time[u] > time[v])
        tests.append((forbidden,max(map(len,part))))
    histogram = {str(k):0 for k in range(1,5)}
    for mask in range(1<<len(arcs)):
        edges = {i:set() for i in range(4)}
        for k,(u,v) in enumerate(arcs):
            if mask>>k & 1:
                edges[u].add(v)
        groups = producer.components(list(range(4)), edges)
        predicted = max(map(len, groups))
        truth = min(width for forbidden,width in tests if not mask & forbidden)
        if predicted != truth:
            raise RuntimeError('SCC/weak-order mismatch')
        positions = {v:k for k,block in enumerate(groups) for v in block}
        if any(positions[u] > positions[v] for u in edges for v in edges[u]):
            raise RuntimeError('Topological order violated')
        histogram[str(truth)] += 1

    fixtures = [layers(k) for k in range(1,5)]
    core = [(0,0,0),(1,0,0),(0,1,0),(0,0,1)]
    planar = wire(core+[(-3,0,0),(-5,0,0),(0,-3,0)],
                  core+[(-2,0,0),(-3,0,0),(0,-2,0)])
    fixtures.append(planar)
    # Globally positive similarity, intentionally NOT_COVERED in these frames.
    tetra = [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]
    outside = wire(tetra,[tuple(-F(3,4)*v for v in row) for row in tetra])
    fixtures.append(outside)
    fixtures.append(wire(core,core))
    fixtures.append(wire(core,[tuple(F(v)+F(1,3) for v in row) for row in core]))
    fixtures.append(wire([(0,0,0),(1,0,0),(2,0,0)],[(0,0,0)]*3))
    records = []
    geometric_orders = 0
    for data in fixtures:
        p,q = producer.read_input(data)
        cert = producer.produce(data)
        if cert['status'] == 'CERTIFIED':
            checked = consumer.check(data,cert)
        else:
            checked = {'status':'NOT_COVERED_IS_NOT_A_COUNTEREXAMPLE'}
        moved = [i for i in range(len(p)) if p[i] != q[i]]
        if len(moved) <= 4:
            possible = []
            for part in ordered_partitions(moved):
                geometric_orders += 1
                if direct_admissible(p,q,part):
                    possible.append(max(map(len,part),default=0))
            if min(possible) != cert['minimum_maximum_switch_batch']:
                raise RuntimeError('Direct metric path disagrees with graph')
        record = dict(labels=len(p),movers=len(moved),status=cert['status'],
                      component_sizes=[len(b['indices']) for b in cert['blocks']],
                      primitive_kinds=[b['kind'] for b in cert['blocks']],
                      whole_map=producer.block_certificate(p,q,moved) if moved else {'kind':'IDENTITY'},
                      checked=checked)
        records.append(record)
    for m,record in enumerate(records[:4],1):
        if record['component_sizes'] != [3]*m:
            raise RuntimeError('Layer family has wrong exact components')
        if record['primitive_kinds'] != ['COMMON_ANCHOR']*m:
            raise RuntimeError('Missing three-mover anchor primitive')
        if m>=2 and record['whole_map']['kind'] != 'NOT_COVERED':
            raise RuntimeError('Whole-map separation control failed')
    pp,qq=producer.read_input(planar)
    low=producer.block_certificate(pp,qq,[4,5,6])
    augmented=[list(producer.sub(qq[i],pp[i]))+[(producer.dot(qq[i],qq[i])-producer.dot(pp[i],pp[i]))/2]
               for i in [4,5,6]]
    if low['rank'] != 2 or producer.rank(augmented,4) != 3:
        raise RuntimeError('Unanchored planar-displacement control failed')
    # A manually coarsened positive stage checks a normal certificate as well.
    manual={'status':'CERTIFIED','blocks':[low]}
    consumer.check(planar,manual)

    data=layers(2)
    cert=producer.produce(data)
    failures=0
    damaged=copy.deepcopy(cert);damaged['blocks'][0]['anchor'][0]='0'
    failures+=rejected(lambda:consumer.check(data,damaged))
    damaged=copy.deepcopy(cert);damaged['blocks'].reverse()
    failures+=rejected(lambda:consumer.check(data,damaged))
    damaged=copy.deepcopy(cert);damaged['blocks'].pop()
    failures+=rejected(lambda:consumer.check(data,damaged))
    damaged=copy.deepcopy(cert);damaged['blocks'].append(damaged['blocks'][0])
    failures+=rejected(lambda:consumer.check(data,damaged))
    bad=copy.deepcopy(data);bad['source'][0][0]=0.25
    failures+=rejected(lambda:producer.produce(bad))
    bad=copy.deepcopy(data);bad['source'][0][0]=True
    failures+=rejected(lambda:producer.produce(bad))
    bad=copy.deepcopy(data);bad['target'][0][0]='100000'
    failures+=rejected(lambda:producer.produce(bad))
    bad=copy.deepcopy(data);bad['source'].append(bad['source'][0]);bad['target'].append(bad['target'][0])
    failures+=rejected(lambda:producer.produce(bad))
    bad=copy.deepcopy(manual);bad['blocks'][0]['normal']=['0','0','0']
    failures+=rejected(lambda:consumer.check(planar,bad))
    failures+=rejected(lambda:consumer.check(outside,producer.produce(outside)))

    # Common Euclidean frame and label changes preserve every edge and stage.
    p,q=producer.read_input(data)
    def frame(row):
        return (2*row[2]+3,-2*row[0]+F(1,7),2*row[1]-4)
    transformed=wire(list(map(frame,p)),list(map(frame,q)))
    fc=producer.produce(transformed)
    if [b['indices'] for b in fc['blocks']] != [b['indices'] for b in cert['blocks']]:
        raise RuntimeError('Shared frame/scaling changed the components')
    consumer.check(transformed,fc)
    permutation=list(reversed(range(len(p))))
    permuted=wire([p[i] for i in permutation],[q[i] for i in permutation])
    consumer.check(permuted,producer.produce(permuted))
    # Fixed tetrahedron plus each triple has paired affine rank six.
    subset=list(range(4))+[4,5,6]
    paired=[list(p[i])+list(q[i]) for i in subset]
    paired_rank=producer.rank([[v-w for v,w in zip(row,paired[0])] for row in paired[1:]],6)
    if paired_rank != 6:
        raise RuntimeError('Rank-six control failed')
    # Check the exact loss telescope on actual labelled geometric stages.
    weights=[F(i+1,len(p)*(len(p)+1)//2) for i in range(len(p))]
    def loss(x,y):
        return sum(weights[i]*weights[j]*(consumer.square_distance(x[i],x[j])
                   -consumer.square_distance(y[i],y[j]))
                   for i in range(len(x)) for j in range(len(x)))
    total_loss=loss(p,q)
    stage_losses=[]
    current=p[:]
    for block in cert['blocks']:
        following=current[:]
        for i in block['indices']:
            following[i]=q[i]
        stage_losses.append(loss(current,following))
        current=following
    if any(v<0 for v in stage_losses) or sum(stage_losses)!=total_loss:
        raise RuntimeError('Ordered-loss telescope failed')
    # Independent permutation expansion for every displayed four-row minor.
    minors=0
    for data in fixtures:
        pp,qq=producer.read_input(data)
        moved=[i for i in range(len(pp)) if pp[i]!=qq[i]]
        if not moved:
            continue
        result=producer.block_certificate(pp,qq,moved)
        if result['kind']!='NOT_COVERED':
            continue
        matrix=[list(producer.sub(qq[i],pp[i]))+
                [(sum(v*v for v in qq[i])-sum(v*v for v in pp[i]))/2]
                for i in result['minor_indices']]
        det=F(0)
        for permutation in itertools.permutations(range(4)):
            term=F((-1)**sum(permutation[i]>permutation[j] for i in range(4) for j in range(i+1,4)))
            for i in range(4):
                term*=matrix[i][permutation[i]]
            det+=term
        if det!=F(result['augmented_minor']) or not det:
            raise RuntimeError('Augmented minor expansion failed')
        minors+=1
    return dict(status='ENDPOINT_BLOCK_CLASSIFICATION_CONTROLS_PASS',
                directed_graphs=4096,weak_orders_per_graph=len(partitions),
                exact_minimum_batch_histogram=histogram,
                direct_geometric_order_checks=geometric_orders,
                three_mover_paired_rank=paired_rank,
                unanchored_displacement_plane_rank=low['rank'],
                unanchored_displacement_plane_augmented_rank=3,
                ordered_loss=str(total_loss),stage_ordered_losses=list(map(str,stage_losses)),
                independently_expanded_inconsistency_minors=minors,
                rejected_controls=failures,fixtures=records,
                gaussian_integrals_evaluated=False,old_motion_checkers_replayed=False)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit',action='store_true')
    a=parser.parse_args()
    record=audit()
    if not a.emit:
        expected=json.loads(Path(__file__).with_name('EXPECTED.json').read_text())
        if record != expected:
            raise RuntimeError('Exact expected record mismatch')
    print(json.dumps(record,indent=2))


if __name__=='__main__':
    main()
