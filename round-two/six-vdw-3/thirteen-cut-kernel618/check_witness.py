#!/usr/bin/env python3
"""Check constructive irredundancy only for the weaker field-seven system."""
import argparse
import itertools
import json
from pathlib import Path


def require(condition,message):
    if not condition:
        raise ValueError(message)


def audit(record):
    q = 103
    lam = record['lambda']
    holes = {0,1,lam}
    outside = [x for x in range(q) if x not in holes]
    require(record.get('status') == 'SAT','No constructive witness')
    require(record['regular_point_order'] == outside,'Changed point order')
    word = record['orientation']
    require(len(word) == 100 and set(word) <= {'0','1'},'Malformed orientation')
    values = dict(zip(outside,map(int,word)))
    target = tuple(record['target_core'])
    require(len(target) == 10 and target == tuple(sorted(set(target))) and all(x in values for x in target), 'Bad target core')
    require(all(values[x] == 0 for x in target),'Target core is not all zero')
    endpoints = list(itertools.combinations(range(q),2))
    field_sevens = set()
    cores = set()
    for first,last in endpoints:
        step = (last-first)*pow(6,-1,q) % q
        seven = frozenset((first+j*step) % q for j in range(7))
        if not holes.intersection(seven):
            require(len({values[x] for x in seven}) == 2,'Witness has a constant field seven')
            field_sevens.add(seven)
        radius = (last-first)*pow(4,-1,q) % q
        center = (first+last)*pow(2,-1,q) % q
        seed = {(center+j*radius) % q for j in range(-2,3)}
        if holes.intersection(seed):
            continue
        neighborhood = {(center+j*radius) % q for j in range(-4,5)}
        neighborhood.update((center+j*radius*pow(2,-1,q)) % q for j in (-3,-1,1,3))
        cores.add(tuple(sorted(neighborhood-holes)))
    failures = sorted(core for core in cores if len({values[x] for x in core}) == 1)
    require(failures == [target],'Witness fails a different/additional eligible mixed-core cut')
    # Exhibit why this is not a partial XOR618 witness for the campaign target.
    colors = [None if t % q in holes else values[t % q] ^ int(t % 6 >= 3) for t in range(6*q)]
    bad = None
    for step in range(1,6*q):
        for start in range(6*q):
            residues = [(start+j*step) % (6*q) for j in range(7)]
            row = [colors[t] for t in residues]
            if None not in row and len(set(row)) == 1:
                bad = {'start':start,'step':step,'residues':residues,'color':row[0]}
                break
        if bad is not None:
            break
    require(bad is not None,'Unexpected outside-cyclic-AP-free witness; investigate separately')
    return {'status':'EXACT_FIELD_SEVEN_IRREDUNDANCY_WITNESS_VERIFIED',
            'lambda':lam,'target_core':list(target),'field_endpoint_pairs_checked':len(endpoints),
            'outside_field_seven_supports_checked':len(field_sevens),
            'eligible_regular_core_supports_checked':len(cores),'constant_cores':failures,
            'bad_outside_XOR618_cyclic_AP':bad,'outside_cyclic_avoidance_proved':False,
            'W_bound_improved':False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--witness',type=Path,required=True)
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    result = audit(json.loads(args.witness.read_text()))
    if args.output:
        args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
