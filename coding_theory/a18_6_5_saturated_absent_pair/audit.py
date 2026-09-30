#!/usr/bin/env python3
"""Small exhaustive engine audits and rejection tests, without full replay."""
import copy
import itertools
import json
import time
from pathlib import Path

import generate
import verify


def require(condition,message):
    if not condition:
        raise ValueError(message)


def rejected(function,*args):
    try:
        function(*args)
    except ValueError:
        return
    raise ValueError('malformed evidence was accepted')


def small_graphs():
    total = 0
    queries = 0
    for n in range(6):
        pairs = list(itertools.combinations(range(n),2))
        for code in range(1 << len(pairs)):
            neighbors = [set() for _ in range(n)]
            for i,(a,b) in enumerate(pairs):
                if code >> i & 1:
                    neighbors[a].add(b)
                    neighbors[b].add(a)
            true_cliques = {t for size in range(n+1) for t in itertools.combinations(range(n),size)
                            if all(b in neighbors[a] for a,b in itertools.combinations(t,2))}
            optimum = max(map(len,true_cliques))
            for mapping in [list(range(n)),list(reversed(range(n)))]:
                relabeled = [set() for _ in range(n)]
                for a in range(n):
                    relabeled[mapping[a]] = {mapping[b] for b in neighbors[a]}
                masks = [sum(1 << j for j in row) for row in relabeled]
                found,_ = generate.maximum_clique(masks)
                checked,_ = verify.maximum_clique(relabeled)
                require(len(found) == len(checked) == optimum,'maximum-clique audit failed')
                require(all(b in relabeled[a] for a,b in itertools.combinations(found,2)),
                        'generator maximum witness is not a clique')
                require(all(b in relabeled[a] for a,b in itertools.combinations(checked,2)),
                        'checker maximum witness is not a clique')
                for target in range(n+2):
                    expected = {tuple(sorted(mapping[v] for v in t)) for t in true_cliques if len(t)==target}
                    output,_ = verify.cliques_of_size(relabeled,target)
                    require(set(output)==expected and len(output)==len(expected),'fixed-size clique audit failed')
                    queries += 1
            total += 1
    return total,queries


def partitions(points,width):
    if not points:
        yield ()
        return
    anchor = min(points)
    for rest in itertools.combinations(sorted(points-{anchor}),width-1):
        block = frozenset((anchor,)+rest)
        for tail in partitions(points-block,width):
            yield (block,)+tail


def orthogonality():
    checks = 0
    for width in [2,3]:
        all_classes = list(partitions(frozenset(range(width*width)),width))
        labels = [tuple(next(i for i,b in enumerate(c) if p in b) for p in range(width*width))
                  for c in all_classes]
        for i,left in enumerate(all_classes):
            for j in range(i,len(all_classes)):
                direct = all(len(a&b)==1 for a in left for b in all_classes[j])
                require(verify.orthogonal_labels(labels[i],labels[j],width)==direct,
                        'orthogonality audit failed')
                checks += 1
    return checks


def main():
    start = time.monotonic()
    graphs,clique_queries = small_graphs()
    orthogonality_checks = orthogonality()
    base = Path(__file__).parent
    witness = json.loads((base/'witness56.json').read_text())
    verify.check_witness(witness)
    corrupt = copy.deepcopy(witness)
    corrupt['words'][1] = corrupt['words'][0]
    rejected(verify.check_witness,corrupt)
    corrupt = copy.deepcopy(witness)
    corrupt['absent_pair'] = [0,1]
    rejected(verify.check_witness,corrupt)
    manifest = json.loads((base/'expected.json').read_text())
    case = next(c for c in manifest['cases'] if c['maximum']>=2)
    corrupt = copy.deepcopy(case)
    corrupt['attaining_words'][1] = corrupt['attaining_words'][0]
    rejected(verify.validate_case,corrupt,verify.field_plane())
    corrupt = copy.deepcopy(case)
    corrupt['second_plane'][1] = corrupt['second_plane'][0]
    rejected(verify.validate_case,corrupt,verify.field_plane())
    rejected(verify.decode,-1)
    rejected(verify.decode,1<<16)
    print(json.dumps({'status':'PASS','all_simple_graphs_through_five_vertices':graphs,
        'labelings_per_graph':2,'fixed_size_clique_queries':clique_queries,
        'orthogonality_comparisons':orthogonality_checks,'malformed_inputs_rejected':6,
        'seconds':round(time.monotonic()-start,4)}))


if __name__ == '__main__':
    main()
