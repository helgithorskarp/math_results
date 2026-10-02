"""Semantic damages, monotone-count truth tables, literal tiny tuple controls."""
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path
import audit
import check
from model import need, point_shapes
from separate import rainbow


def run():
    here=Path(__file__).resolve().parent
    fixture=json.loads((here/'fixture.json').read_text())
    expected=json.loads((here/'expected.json').read_text())
    for engine in (check.verify,audit.verify):engine(fixture,expected)
    damages=[]
    def damaged(edit):
        f=deepcopy(fixture);edit(f);damages.append(f)
    damaged(lambda f:f.update(agent='somebody_else'))
    damaged(lambda f:f.update(schema=2))
    damaged(lambda f:f['prefix'].__setitem__(0,[8,1]))
    damaged(lambda f:f['tail_pools'][0].remove(1))
    damaged(lambda f:f['base_phases'].__setitem__(0,f['base_phases'][1]))
    damaged(lambda f:f['base_phases'][-1].__setitem__(1,2520))
    damaged(lambda f:f['five_class_ability_witness'].update(classes=[[1,0]]))
    damaged(lambda f:f['five_class_ability_witness'].update(classes=[[3,0]]))
    damaged(lambda f:f['five_class_ability_witness'].update(classes=[[3,0],[3,2]]))
    damaged(lambda f:f['kernel'][3].pop())
    damaged(lambda f:f['kernel'][1].__setitem__(0,1))
    damaged(lambda f:f['kernel'][3].__setitem__(3,3))
    rejected=[]
    for engine in (check.verify,audit.verify):
        count=0
        for f in damages:
            try:engine(f,expected)
            except (ValueError,KeyError,TypeError):count+=1
            else:raise ValueError('fixture semantic damage accepted')
        rejected.append(count)
    expected_damages=[]
    for key,value in [('kernel_capacity_budget',52),('stage_capacity_budget',1744),
                      ('minimality_vectors_through12',1819)]:
        bad=deepcopy(expected);bad[key]=value;expected_damages.append(bad)
    bad=deepcopy(expected);bad['collapse']['finite_families'][-1][0]=7;expected_damages.append(bad)
    bad_counts=[]
    for engine in (check.verify,audit.verify):
        count=0
        for bad in expected_damages:
            try:engine(fixture,bad)
            except ValueError:count+=1
            else:raise ValueError('expected semantic damage accepted')
        bad_counts.append(count)
    domain=(1,2,3,4,8,14,37,44)
    cases=0
    for bits in range(1<<len(domain)):
        H=[y for i,y in enumerate(domain) if bits & (1<<i)]
        for size,mixed in ((3,False),(3,True),(4,False)):
            good=[list(t) for t in combinations(H,size) if all(len({y%d for y in t})==size for d in (5,7,9))
                  and (not mixed or len({y%3 for y in t})>=2)]
            need(rainbow(H,size,mixed)==(good[0] if good else None), 'literal tuple control differs')
            cases+=1
    # Point shapes are arbitrary monotone counts, not assumed realizable
    # coverings or independent resource allocations.
    truth_cases=point_shapes()
    need(rejected==[12,12] and bad_counts==[4,4] and cases==768 and truth_cases==9504,
         'controls incomplete')
    return {'agent':'six-covering-3','role':'researcher','fixture_damages_per_engine':rejected,
            'expected_damages_per_engine':bad_counts,'tiny_literal_tuple_cases':cases,
            'monotone_qualification_truth_cases':truth_cases}


if __name__=='__main__':print(json.dumps(run(),sort_keys=True))
