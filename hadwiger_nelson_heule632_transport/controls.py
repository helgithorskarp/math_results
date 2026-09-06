#!/usr/bin/env python3
"""Complete small-instance checks of optional vertices and all list sizes."""
import argparse
from itertools import product
import json
from pathlib import Path
import time
import oracle
import independent


def main(out):
    start = time.monotonic()
    fixtures = [('path4', 4, [(0,1),(1,2),(2,3)], (), range(-1,16)),
                ('cycle4', 4, [(0,1),(1,2),(2,3),(3,0)], (0,1,2,3), range(-1,16)),
                ('cycle4_two_branches', 6, [(2,3),(3,4),(4,5),(5,2),(2,1),(1,0)], (2,3,4,5), range(-1,4))]
    records = []
    for name, n, edges, cycle, states in fixtures:
        vertices = list(range(n)); adjacency = oracle.graph(vertices, edges)
        count = positive = 0
        for word in product(states, repeat=n):
            masks = {v: m for v, m in enumerate(word) if m >= 0}
            a = oracle.extend(adjacency, masks, cycle)
            b = independent.solve(vertices, edges, masks, cycle)
            c = independent.brute(vertices, edges, masks)
            if (a is None) != (c is None) or (b is None) != (c is None):
                raise ValueError(('oracle disagreement', name, word))
            if a is not None:
                oracle.check_answer(adjacency, masks, a)
                oracle.check_answer(adjacency, masks, b)
                positive += 1
            count += 1
        records.append({'fixture': name, 'cases': count, 'colourable': positive})
    # A triangle with two identical colours on each vertex must fail even
    # though every vertex has two available colours; only the even-cycle
    # incidence theorem supplies two-choosability of the target fresh graph.
    triangle = [(0,1),(1,2),(0,2)]
    adj = oracle.graph([0,1,2], triangle)
    if oracle.extend(adj, {0:3,1:3,2:3}, (0,1,2)) is not None:
        raise ValueError('odd-cycle control')
    rejected = 0
    for lists in ({0:16}, {4:1}):
        try:
            oracle.extend(adj, lists, (0,1,2))
        except ValueError:
            rejected += 1
        else:
            raise ValueError('malformed list input accepted')
    try:
        oracle.extend(oracle.graph([0,1,2,3], [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]), {v:15 for v in range(4)}, (0,1,2))
    except ValueError:
        rejected += 1
    else:
        raise ValueError('non-pseudoforest accepted')
    result = {'status':'EXHAUSTIVE ORACLE CONTROLS PASSED', 'fixtures':records,
              'cases':sum(r['cases'] for r in records), 'odd_cycle_rejected':True,
              'malformed_inputs_rejected':rejected, 'seconds':time.monotonic()-start}
    out.mkdir(parents=True, exist_ok=True)
    (out/'controls.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True)
    main(ap.parse_args().out)
