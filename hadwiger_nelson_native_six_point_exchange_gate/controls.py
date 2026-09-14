#!/usr/bin/env python3
"""Definition-level finite controls, including positive uncovered instances."""
from pathlib import Path
import argparse
import itertools
import json
import random
import subprocess
import time
import verify as v


def connected(t, adj):
    allowed = set(t)
    seen = {t[0]}
    todo = [t[0]]
    while todo:
        for u in adj[todo.pop()] & allowed - seen:
            seen.add(u)
            todo.append(u)
    return len(seen) == len(t)


def controls(work, sanitize=False):
    start = time.monotonic()
    work.mkdir(parents=True, exist_ok=True)
    v.compile_tools(work, sanitize)
    rng = random.Random(20260914056)
    parents = [[-1,0,0,0,0,0], [-1,0,1,2,3,4], [-1,0,1,0,0,0],
               [-1,0,0,0,1,1], [-1,0,1,2,0,0], [-1,0,1,0,3,0]]
    graph_cases = []
    for p in parents:
        graph_cases.append((6, [(i,p[i]) for i in range(1,6)], [4]*6, [1]*6, 1))
    for trial in range(14):
        n = 8 + trial % 3
        edges = [e for e in itertools.combinations(range(n), 2)
                 if rng.random() < (0.18,0.35,0.65)[trial % 3]]
        graph_cases.append((n, edges, [rng.randrange(5) for _ in range(n)],
                            [rng.randrange(1 << 5) for _ in range(n)], 5))
    positive_sets = 0
    for case, (n, edges, degrees, masks, width) in enumerate(graph_cases):
        adj = [set() for _ in range(n)]
        for a,b in edges:
            adj[a].add(b)
            adj[b].add(a)
        expected = {}
        for k in range(3,7):
            expected[k] = {t for t in itertools.combinations(range(n), k)
                           if connected(t, adj)
                           and all(degrees[a] + len(adj[a] & set(t)) >= 4 for a in t)}
        uncovered = {t for t in expected[6]
                     if v.group_mask(t, dict(enumerate(masks))) == (1 << width) - 1}
        positive_sets += len(uncovered)
        inp = work / 'control-graph.txt'
        v.write_graph(inp, n, list(range(n)), dict(enumerate(degrees)), adj,
                      dict(enumerate(masks)), width)
        r = v.run(work, 'tree_six', [inp], allowed=(0,10))
        observed = {tuple(sorted(map(int, row.split()))) for row in r.stderr.splitlines()
                    if len(row.split()) == 6 and all(x.isdigit() for x in row.split())}
        v.require(observed == uncovered, 'tree-six entry comparison ' + str(case))
        v.run(work, 'connected_six', [inp, work / 'esu'])
        observed = {tuple(map(int, row.split())) for row in (work / 'esu-6.txt').read_text().splitlines()}
        v.require(observed == uncovered, 'ESU entry comparison ' + str(case))
        v.run(work, 'smaller_trees', [inp, work / 'small'])
        for k in (3,4,5):
            observed = {tuple(map(int, row.split()))
                        for row in (work / f'small-{k}.txt').read_text().splitlines()}
            v.require(observed == expected[k], 'smaller-tree entry comparison')
    covers = positive_covers = 0
    for trial in range(90):
        width = (1,5,65,128,166,256)[trial % 6]
        # Repeat a small mask pattern across the width to exercise every block boundary.
        small_width = min(width, 5)
        small = [rng.randrange(1 << small_width) for _ in range(8)]
        masks = [sum(((m >> (i % small_width)) & 1) << i for i in range(width)) for m in small]
        costs = [1 if i < 4 else 2 for i in range(8)]
        budget = 6 if trial % 2 else trial % 7
        allbits = (1 << width) - 1
        expected = any(sum(costs[i] for i in t) <= budget
                       and v.group_mask(t, dict(enumerate(masks))) == allbits
                       for k in range(9) for t in itertools.combinations(range(8), k))
        blocks = (width+63)//64
        inp = work / 'weighted.txt'
        with inp.open('w') as out:
            out.write(f'{width} 8 {budget}\n')
            for c,m in zip(costs,masks):
                out.write(' '.join(map(str,[c,*[(m>>(64*j))&((1<<64)-1) for j in range(blocks)]]))+'\n')
        v.run(work,'cover_six',[inp,work/'weighted-out.txt'])
        observed = (work/'weighted-out.txt').read_text().splitlines()[0] == 'SAT'
        v.require(observed == expected, 'weighted brute-force comparison')
        if budget == 6:
            inp = work/'split.txt'
            with inp.open('w') as out:
                out.write(f'{width} 4 4\n')
                for m in masks:
                    out.write(' '.join(str((m>>(64*j))&((1<<64)-1)) for j in range(blocks))+'\n')
            r = v.run(work,'split_cover',[inp],allowed=(10,20))
            v.require((r.returncode == 10) == expected, 'pair-split brute-force comparison')
        covers += 1
        positive_covers += expected
    rejected = 0
    for words in [['0.'], ['00'], ['0x'], ['012']]:
        try:
            v.check_words(words, [(0,1)], {0,1}, 2)
        except ValueError:
            rejected += 1
    v.require(rejected == 4, 'malformed colour words rejected')
    result = {'status':'PASS', 'graph_cases':len(graph_cases), 'positive_uncovered_sets':positive_sets,
              'weighted_cover_cases':covers, 'positive_cover_cases':positive_covers,
              'rejected_malformed_words':rejected, 'sanitize':sanitize,
              'seconds':time.monotonic()-start}
    (work/'controls.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--sanitize',action='store_true')
    args = parser.parse_args()
    print(json.dumps(controls(args.work.resolve(),args.sanitize),indent=2))
