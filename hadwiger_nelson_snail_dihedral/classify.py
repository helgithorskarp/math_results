"""Optional reproducible exact-classification witness producer.

Solver UNSAT is used to propose lower subgraphs only. verify.py exhaustively
checks their non-three-colourability and never trusts these solver verdicts.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

import geometry as g
from produce import colouring,pack


def spindle(n,edges):
    neighbours = [set() for _ in range(n)]
    for a,b in edges:
        neighbours[a].add(b)
        neighbours[b].add(a)
    diamonds = [{} for _ in range(n)]
    for a,b in edges:
        common = sorted(neighbours[a]&neighbours[b])
        for x,y in itertools.combinations(common,2):
            if y not in neighbours[x]:
                diamonds[x][y] = (a,b)
                diamonds[y][x] = (a,b)
    for root,ds in enumerate(diamonds):
        for u in sorted(ds):
            for v in sorted(neighbours[u]&ds.keys()):
                vertices = [root,u,*ds[u],v,*ds[v]]
                if len(set(vertices))==7:
                    return vertices
    return None


def minimize(n,edges):
    keep = list(range(n))
    for v in list(keep):
        trial = [x for x in keep if x!=v]
        ids = {x:i for i,x in enumerate(trial)}
        retained = [(ids[a],ids[b]) for a,b in edges if a in ids and b in ids]
        if colouring(len(trial),retained,3)[0] is None:
            keep = trial
    return keep


def classify(directory,output):
    cert = json.loads((directory/'certificate.json').read_text())
    if cert['complete'] is not True or len(cert['cases'])!=812:
        raise ValueError('complete producer required')
    seed = g.seed()
    edges = g.edges_exact(seed,g.scale(g.ONE,g.D*g.D))
    seed_word,_ = colouring(29,edges,3)
    if seed_word is None:
        raise ValueError('seed three-colouring')
    cert['base_word'] = pack(seed_word)
    cert['seed_triangle'] = next(list(t) for t in itertools.combinations(range(29),3)
                                 if all(e in edges for e in itertools.combinations(t,2)))
    cert['version'] = 2
    counts = Counter()
    core_sizes = Counter()
    for row in cert['cases']:
        c,a = row[:2]
        graph = json.loads((directory/f'case_{c:02}_{a:02}.json').read_text())
        n,edges = len(graph['points']),graph['edges']
        lower = spindle(n,edges)
        word = None
        if lower is None:
            word,_ = colouring(n,edges,3)
            if word is None:
                lower = minimize(n,edges)
        if word is not None:
            chi = 3
            row[2] = pack([word[i] for i in graph['address_ids']])
            formal_core = []
        else:
            chi = 4
            formal_core = [graph['address_ids'].index(i) for i in lower]
            core_sizes[len(lower)] += 1
        row[:] = row[:3]+[chi,formal_core]
        counts[chi] += 1
    output.write_text(json.dumps(cert,separators=(',',':'),sort_keys=True)+'\n')
    return {'cases':812,'chromatic_counts':dict(counts),'lower_core_sizes':dict(core_sizes)}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--producer',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args = p.parse_args()
    print(json.dumps(classify(args.producer,args.output),indent=2))
