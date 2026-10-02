"""Entrywise finite calibration and controls; ordinary proof is in PROOF.md."""
import argparse
from collections import Counter
import hashlib
import itertools as it
import json
from pathlib import Path
import producer
import oracle

ROOT = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def reject(operation):
    try:
        operation()
    except ValueError:
        return
    raise ValueError('semantic damage accepted')


def relabel(record, order):
    n = record['n']
    roles = [record['roles'][old] for old in order]
    original = dict(zip(it.combinations(range(n),2),record['colors']))
    colors = [original[tuple(sorted((order[i],order[j])))] for i,j in it.combinations(range(n),2)]
    return roles,colors


def run():
    first, second = producer.records(), oracle.records()
    need(first == second, 'every role/colored-pair/certificate entry agrees')
    transports, active, fan = 0, 0, 0
    by_n = Counter()
    for record in first:
        by_n[record['n']] += 1
        cert = record['certificate']
        active += cert['active']
        fan += bool(cert['active'] and cert['minimum_C_neighbors'] > 1)
        n = record['n']
        for order in [list(reversed(range(n))), list(range(1,n))+[0]]:
            roles,colors = relabel(record,order)
            left = producer.certificate(n,roles,colors)
            right = oracle.certificate(n,roles,colors)
            need(left == right, 'every transported physical colored graph agrees')
            invariant = dict(left); invariant.pop('roots')
            previous = dict(cert); previous.pop('roots')
            need(invariant == previous, 'bound is invariant under physical point bijections')
            need(left['roots'] == sorted(order.index(old) for old in cert['roots']),
                 'actual root labels transport')
            transports += 1
    controls = []
    for name,n,roles,colors,expected in [
        ('heavy_support_path',3,[0,2,3],[1,0,2],(1,1,2)),
        ('eligible_unit_consumes_separate_endpoint',3,[0,1,2],[0,1,1],(1,2,2)),
        ('two_neighbor_fan',5,[0,2,2,3,3],[1,1,0,0,0,2,0,0,2,0],(2,2,4))]:
        cert = producer.certificate(n,roles,colors)
        need(cert == oracle.certificate(n,roles,colors) and cert['active'], name)
        need((cert['minimum_C_neighbors'],cert['required_color1'],cert['required_support']) == expected,
             'explicit positive graph has exact bound')
        controls.append(dict(name=name,certificate=cert))
    damage = 0
    for engine in (producer,oracle):
        for n,roles,colors in [
            (3,[0,2,3],[1,0,3]), (3,[0,2,3],[1,0]),
            (3,[0,4,3],[1,0,2]), (3,[0,2,3],[2,0,1]),
            (3,[0,2,3],[1,1,2]), (3,[0,2,3],[True,0,2])]:
            reject(lambda n=n,roles=roles,colors=colors,e=engine: e.certificate(n,roles,colors))
            damage += 1
    sample = controls[2]['certificate']
    for field in ['D_A','D_V','I_even','C1','C2','minimum_C_neighbors',
                  'required_color1','required_support','eligible_units','eligible_nonunits']:
        changed = dict(sample); changed[field] += 1
        reject(lambda changed=changed: need(changed == oracle.certificate(
            5,[0,2,2,3,3],[1,1,0,0,0,2,0,0,2,0]),'damaged whole certificate'))
        damage += 1
    # Exact formal coefficient identity. Variable order: P,N5,T,tau,constant.
    upper = (3,1,-1,-2,-94)
    lower = (0,4,0,0,13)
    difference = tuple(a-b for a,b in zip(upper,lower))
    factored = (3,-3,-1,-2,-107)
    need(difference == factored, 'exceptional penalty coefficient identity')
    for index in range(5):
        broken = list(factored); broken[index] += 1
        reject(lambda broken=broken: need(tuple(broken) == difference,'damaged algebra coefficient'))
        damage += 1
    need(active > 0 and fan > 0, 'nonvacuous root/fan calibration')
    record = dict(actual_agent='six-code-1',role='researcher',
                  status='COMPLETE_FINITE_CONTROLS_FOR_ORDINARY_LEMMAS',
                  graphs=len(first), graphs_by_order={str(n):count for n,count in sorted(by_n.items())},
                  active_radius_root_graphs=active, multiple_neighbor_fan_graphs=fan,
                  point_transports=transports, rejected_semantic_damages=damage,
                  positive_controls=controls, algebra_identity=list(difference),
                  finite_graphs_sha256=digest(first), finite_coverage='orders2..5 with A nonempty and V union B nonempty; all admissible colored graphs at canonical ordered roles; arbitrary role labels reduce by point permutation',
                  ordinary_proof_formalized=False, external_independent_review_claimed=False)
    record['whole_mathematical_sha256'] = digest(record)
    return record


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output',type=Path)
    p.add_argument('--no-expected',action='store_true')
    args = p.parse_args()
    record = run()
    if not args.no_expected:
        need(record == json.loads((ROOT/'EXPECTED.json').read_text()),'sealed complete mathematical record')
    if args.output:
        args.output.write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
    print(json.dumps(record,sort_keys=True,indent=2))


if __name__ == '__main__':
    main()
