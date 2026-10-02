#!/usr/bin/env python3
"""Independent actual-cyclic derivation of the one-satellite input cover."""
import argparse
import itertools
import json
from pathlib import Path


def require(condition,message):
    if not condition:
        raise ValueError(message)


def audit(record):
    q = 103
    seed = set(range(5))
    local = frozenset((0,1,2,3,4,5,6,52,53,54,55,101,102))
    supported = []
    field_supports = set()
    for step in range(1,618):
        for start in range(618):
            residues = tuple((start+j*step)%618 for j in range(7))
            fields = tuple(t%q for t in residues)
            if not set(fields) <= local:
                continue
            phases = tuple(int(t%6 >= 3) for t in residues)
            supported.append((fields,phases))
            if len(set(fields)) == 1:
                require(len(set(phases)) == 2,'Wrong same-column phase row')
            else:
                require(len(set(fields)) == 7,'Wrong nonzero field support')
                field_supports.add(frozenset(fields))
    require(len(supported) == 822 and len(field_supports) == 6,'Unexpected exact local cyclic cover')
    exceptional = []
    raw_hole_triples = 0
    for h in itertools.combinations((x for x in range(q) if x not in seed),3):
        raw_hole_triples += 1
        if all(set(h).intersection(s) for s in field_supports):
            exceptional.append(h)
    stabilizer = []
    maps_checked = 0
    for multiplier in range(1,q):
        for shift in range(q):
            maps_checked += 1
            if {(multiplier*x+shift)%q for x in seed} == seed:
                stabilizer.append((multiplier,shift))
    require(stabilizer == [(1,0),(102,4)],'Seed stabilizer is not precisely two maps')
    raw_inputs = set()
    local_inputs = local_accepted = 0
    for h in exceptional:
        core = local-set(h)
        satellites = sorted(core-seed)
        require(len(core) == 10 and len(satellites) == 5,'Wrong exceptional core domain')
        for bits in itertools.product((0,1),repeat=len(satellites)):
            values = {x:0 for x in seed}
            values.update(zip(satellites,bits))
            local_inputs += 1
            accepted = True
            for fields,phases in supported:
                if any(x in h for x in fields):
                    continue
                colors = [values[x]^f for x,f in zip(fields,phases)]
                if len(set(colors)) == 1:
                    accepted = False
                    break
            require(accepted,'Unexpected remaining local cyclic restriction')
            local_accepted += 1
            if sum(bits) == 1:
                opposite = satellites[bits.index(1)]
                raw_inputs.add((h,opposite))
    owners = {}
    for h,opposite in raw_inputs:
        orbit = {(tuple(sorted((a*x+b)%q for x in h)),(a*opposite+b)%q) for a,b in stabilizer}
        require(orbit <= raw_inputs and len(orbit) == 2,'Bad input orbit')
        owners.setdefault(min(orbit),set()).update(orbit)
    expected = []
    for (h,opposite),members in sorted(owners.items()):
        core = sorted(local-set(h))
        expected.append({'holes':list(h),'unique_opposite_satellite':opposite,'regular_core':core,
                         'seed_color':0,'root':0,'fixed_core_bits':[[x,int(x==opposite)] for x in core],
                         'other_regular_bits_free':90,
                         'represented_inputs':[{'holes':list(hh),'opposite':x} for hh,x in sorted(members)]})
    require(record['q'] == q and record['seed'] == sorted(seed) and record['thirteen_pattern'] == sorted(local),'Altered local definition')
    require(record['cases'] == expected,'Complete one-opposite input rows disagree')
    require(record['normalized_raw_one_satellite_inputs'] == len(raw_inputs) == 30,'Incomplete raw input family')
    require(record['reflection_classes'] == len(owners) == 15,'Incomplete quotient family')
    require(record['reflection_invariance_imposed'] is False and record['higher_density_lemma_proved'] is False,'Wrong proof scope')
    return {'status':'EXACT_COMPLETE_ONE_SATELLITE_INPUT_COVER_VERIFIED',
            'all_actual_cyclic_pairs_checked':618*617,'local_supported_pairs':len(supported),
            'field_supports_in_local_pattern':len(field_supports),
            'seed_disjoint_hole_triples_checked':raw_hole_triples,
            'exceptional_hole_triples':[list(h) for h in exceptional],
            'seed_stabilizer_maps_checked':maps_checked,'seed_stabilizer':[list(x) for x in stabilizer],
            'local_binary_inputs':local_inputs,'local_accepted_inputs':local_accepted,
            'raw_one_opposite_inputs':len(raw_inputs),'case_classes':len(owners),
            'all_cases_other_regular_bits_free':90,'higher_density_lemma_proved':False}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cover',type=Path,required=True)
    p.add_argument('--output',type=Path)
    a = p.parse_args()
    result = audit(json.loads(a.cover.read_text()))
    if a.output:
        a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
