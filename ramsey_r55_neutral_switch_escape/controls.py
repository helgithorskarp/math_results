#!/usr/bin/env python3
"""Exhaust shared-vertex switch interactions and reject bad escape paths."""
import argparse
import copy
from itertools import combinations
import json
from pathlib import Path
import verify


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--report',type=Path,required=True)
    args = parser.parse_args()
    S,T = (1,2,0,3),(4,5,6,0)
    eS,eT = verify.support(S),verify.support(T)
    fixed = {(0,1):1,(2,3):1,(1,3):0,(0,2):0,
             (4,6):1,(0,5):1,(0,4):0,(5,6):0}
    free = [e for e in combinations(range(7),2) if e not in fixed]
    checked = 0
    nonzero = 0
    for mask in range(1 << len(free)):
        colors = dict(fixed)
        colors.update((e,mask >> bit & 1) for bit,e in enumerate(free))
        rows = [0]*7
        for (u,v),red in colors.items():
            if red:
                rows[u] |= 1 << v
                rows[v] |= 1 << u
        a = verify.flip(rows,eS)
        b = verify.flip(rows,eT)
        ab = verify.flip(a,eT)
        verify.require(ab == verify.flip(b,eS),'edge-disjoint switches did not commute')
        tt = [verify.literal_triangles(g) for g in (rows,a,b,ab)]
        literal = [d-b-c+a for a,b,c,d in zip(*tt)]
        formula = verify.interaction(rows,eS,eT)
        verify.require(literal == formula,'shared-vertex interaction mismatch')
        checked += 1
        nonzero += int(any(literal))
    verify.require(nonzero > 0,'vacuous interaction control')
    parent = verify.load_parent()
    checker = parent.load_audit()
    rows = checker.decode(json.loads((verify.PARENT/'GRAPH.json').read_text()))
    endpoint = checker.decode(json.loads((verify.HERE/'GRAPH.json').read_text()))
    path = json.loads((verify.HERE/'PATH.json').read_text())
    rejected = []
    for name in ('omit_neutral','reverse_order','wrong_score','wrong_endpoint'):
        mutant = copy.deepcopy(path)
        end = list(endpoint)
        if name == 'omit_neutral':
            mutant['moves'].pop(0)
        elif name == 'reverse_order':
            mutant['moves'].reverse()
        elif name == 'wrong_score':
            mutant['scores'][-1] += 1
        else:
            end[3] ^= 1 << 4
            end[4] ^= 1 << 3
        try:
            verify.square(rows,mutant,end)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('malformed escape accepted')
    try:
        verify.interaction([0]*7,eS,eS)
    except ValueError:
        rejected.append('invalid_overlap_domain')
    else:
        raise ValueError('invalid interaction domain accepted')
    report = {'free_edges':len(free),'all_seven_vertex_double_switch_completions':checked,
              'nonzero_triangle_interactions':nonzero,'negative_controls_rejected':rejected}
    args.report.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,sort_keys=True))


if __name__ == '__main__':
    main()
