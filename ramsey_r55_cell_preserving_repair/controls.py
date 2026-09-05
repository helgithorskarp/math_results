#!/usr/bin/env python3
"""Exhaustive small controls and complete entry-level move-generator comparison."""
import argparse
from collections import Counter
import copy
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import search
import verify


def literal_mixed(rows, roots):
    for five in combinations(range(len(rows)),5):
        if not set(five)&roots:
            continue
        colors = {bool(rows[u] >> v & 1) for u,v in combinations(five,2)}
        if len(colors) == 1:
            return True
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--report',type=Path,required=True)
    args = parser.parse_args()
    move = (0,1,2,3)
    fixed = {(0,2):1,(1,3):1,(0,3):0,(1,2):0}
    free = [e for e in combinations(range(6),2) if e not in fixed]
    delta_count = 0
    for mask in range(1 << len(free)):
        edges = dict(fixed)
        edges.update((e,mask >> k & 1) for k,e in enumerate(free))
        rows = [0]*6
        for (u,v),red in edges.items():
            if red:
                rows[u] |= 1 << v
                rows[v] |= 1 << u
        before = verify.triangles(verify.neighbors(rows))
        changed = search.flip(rows,move)
        after = verify.triangles(verify.neighbors(changed))
        delta = search.triangle_delta(rows,move)
        verify.require(all(after[v]-before[v] == delta.get(v,0) for v in range(6)),'small exact triangle change')
        delta_count += 1

    # Seven vertices are necessary for a nonvacuous K5 switch control: each
    # K5 uses two switch vertices and all three outside vertices. On six
    # vertices every five-set contains three switch vertices, hence both
    # colors already. Test the full seventeen-free-bit seven-vertex domain.
    mixed_count = introduced = 0
    free = [e for e in combinations(range(7),2) if e not in fixed]
    for mask in range(1 << len(free)):
        edges = dict(fixed)
        edges.update((e,mask >> k & 1) for k,e in enumerate(free))
        rows = [0]*7
        for (u,v),red in edges.items():
            if red:
                rows[u] |= 1 << v
                rows[v] |= 1 << u
        if not literal_mixed(rows,{6}):
            changed = search.flip(rows,move)
            bad = literal_mixed(changed,{6})
            verify.require(search.mixed_after_switch(changed,move,64) == (not bad),'incremental mixed-clique gate')
            mixed_count += 1
            introduced += int(bad)
    verify.require(introduced > 0,'vacuous mixed-clique control')

    colorings = 0
    for a,b,c,d in product(range(4),repeat=4):
        old = Counter((tuple(sorted((a,c))),tuple(sorted((b,d)))))
        new = Counter((tuple(sorted((a,d))),tuple(sorted((b,c)))))
        verify.require((old==new) == (a==b or c==d),'quota-preserving switch characterization')
        colorings += 1

    document = json.loads((verify.HERE/'GRAPH.json').read_text())
    checker = verify.load_audit()
    rows = checker.decode(document)
    adj = verify.neighbors(rows)
    signatures = [tuple(sorted(row&{0,1,2})) for row in adj]
    literal = set(verify.matching_supports(adj,signatures))
    fast = set()
    for a,b,c,d in search.swaps(rows):
        fast.add(tuple(sorted(tuple(sorted(e)) for e in ((a,c),(b,d),(a,d),(b,c)))))
    verify.require(fast == literal,'complete endpoint move sets differ')
    digest = hashlib.sha256()
    for support in sorted(literal):
        digest.update((json.dumps(support,separators=(',',':'))+'\n').encode())

    original_rows = checker.decode(json.loads((verify.PARENT/'GRAPH.json').read_text()))
    path = json.loads((verify.HERE/'PATH.json').read_text())
    rejected = []
    for name in ('repeated_vertex','wrong_score','omitted_switch','wrong_endpoint'):
        mutant = copy.deepcopy(path)
        endpoint = list(rows)
        if name == 'repeated_vertex':
            mutant['steps'][0]['move'][1] = mutant['steps'][0]['move'][0]
        elif name == 'wrong_score':
            mutant['steps'][0]['after_score'] += 1
        elif name == 'omitted_switch':
            mutant['steps'].pop(0)
        else:
            endpoint[3] ^= 1 << 4
            endpoint[4] ^= 1 << 3
        try:
            verify.check_path(original_rows,endpoint,mutant)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('invalid path accepted')
    report = {'all_six_vertex_switch_completions':delta_count,
              'all_seven_vertex_switch_completions':1 << len(free),
              'mixed_free_seven_vertex_cases':mixed_count,'mixed_K5_introductions_detected':introduced,
              'all_four_label_assignments':colorings,
              'complete_endpoint_support_sets_equal':True,'endpoint_supports':len(literal),
              'canonical_supports_sha256':digest.hexdigest(),'negative_controls_rejected':rejected}
    args.report.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,sort_keys=True))


if __name__ == '__main__':
    main()
