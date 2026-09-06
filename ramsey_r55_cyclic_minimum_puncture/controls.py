#!/usr/bin/env python3
import copy
import itertools as it
import json
from pathlib import Path
from check import enumerate_models, verify, need
from verify_graph import check_text


def run():
    possible = [(a,0) for a in range(1,8)]+[(0,a) for a in range(1,8)]
    for choice in range(1 << 14):
        clauses = [c for i,c in enumerate(possible) if choice >> i & 1]
        expected = [s for s in range(8) if all(a&s or b&(7^s) for a,b in clauses)]
        actual,_ = enumerate_models(clauses,3)
        need(actual == expected,'small complete DPLL comparison')
    certificate = json.loads(Path(__file__).with_name('certificate.json').read_text())
    physical = []
    for rec in certificate['records']:
        g = rec['maximal_witness']
        text = f"{g['n']} {len(g['red_edges'])}\n"+''.join(f'{u} {v}\n' for u,v in g['red_edges'])
        result = check_text(text)
        need(result['ramsey_5_5'],'physical sharpness witness')
        physical.append(result)
    # Each mutation attacks a different claim boundary, not a byte hash.
    mutations = []
    def change(fn):
        c = copy.deepcopy(certificate)
        fn(c)
        mutations.append(c)
    change(lambda c:c.update(minimum_deletions=8))
    change(lambda c:c['records'][0]['stars'].pop())
    change(lambda c:c['records'][0]['stars'].__setitem__(0,True))
    change(lambda c:c['records'][0].update(pair_cap=4,maximum_added=4))
    change(lambda c:c['records'][1]['terminal'].pop())
    change(lambda c:c['records'][1]['terminal'][0]['five'].update(color=1-c['records'][1]['terminal'][0]['five']['color']))
    rejected = 0
    for c in mutations:
        try:
            verify(c)
        except (ValueError,TypeError,KeyError):
            rejected += 1
        else:
            raise ValueError('bad certificate accepted')
    malformed = ['', '43 1\n0 43\n', '3 2\n0 1\n0 1\n', '3 1\n1 0\n']
    for text in malformed:
        try:
            check_text(text)
        except ValueError:
            pass
        else:
            raise ValueError('bad physical graph accepted')
    return {'status':'VERIFIED_MINIMUM_PUNCTURE_CONTROLS','complete_small_formulas':1 << 14,
            'sharp_physical_witnesses':physical,'rejected_certificates':rejected,
            'rejected_physical_inputs':len(malformed)}


if __name__ == '__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
