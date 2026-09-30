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


def incomplete(function,*args):
    try:
        function(*args)
    except RuntimeError as error:
        require(str(error).startswith('INCOMPLETE'), 'unrecognized resource failure')
        return
    raise ValueError('capped search reported completion')


def partition_audit():
    blocks = [generate.word(a) for a in itertools.combinations(range(8),4)]
    found,_ = generate.partitions(blocks,unused=(1 << 8)-1)
    direct = {tuple(sorted((a,b))) for a,b in itertools.combinations(blocks,2)
              if not a & b and a | b == (1 << 8)-1}
    require(set(found) == direct and len(found) == 35, 'small exact-cover audit failed')
    require(generate.partitions([],unused=0)[0] == [()], 'empty exact cover failed')
    require(generate.partitions([],unused=1)[0] == [], 'infeasible exact cover failed')
    incomplete(generate.partitions,blocks,0)
    incomplete(generate.maximum_clique,[0],0)
    incomplete(verify.maximum_clique,[set()],0)
    incomplete(verify.cliques_of_size,[set()],1,0)
    return len(direct),4


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


def degree_nineteen_bridges():
    # Six uncovered pairs with degrees divisible by three have <=4 active
    # points. Exhaust the complete reduced domain against the K4 conclusion.
    leaves = 0
    for n in range(5):
        pairs = list(itertools.combinations(range(n),2))
        for code in range(1 << len(pairs)):
            edges = [pair for i,pair in enumerate(pairs) if code >> i & 1]
            degrees = [sum(p in edge for edge in edges) for p in range(n)]
            if len(edges) == 6 and all(d % 3 == 0 for d in degrees):
                require(n == 4 and edges == pairs, 'degree-19 leave completion failed')
                leaves += 1
    require(leaves == 1, 'unexpected degree-19 leave domain')
    base = Path(__file__).parent
    manifest = json.loads((base/'expected.json').read_text())
    plane = verify.field_plane()
    first_line = frozenset([0,1,2,3])
    triple = frozenset([1,2,3])
    swaps = 0
    for case in manifest['cases']:
        design = frozenset(map(verify.decode,case['second_plane']))
        exceptional = triple | {case['anchor']}
        residual = [verify.decode(w) for w in case['attaining_words']
                    if all(len(verify.decode(w)&line) <= 2 for line in plane)]
        stars = [line | {17} for line in plane]
        stars += [line | {16} for line in design if line != exceptional]
        original = stars + residual
        verify.validate_code(list(map(verify.encode,original)))
        changed = [word for word in original if word != first_line | {17}]
        changed.append(triple | {16,17})
        verify.validate_code(list(map(verify.encode,changed)))
        require(len(original) == len(changed), 'nonarc swap lost cardinality')
        require([sum(p in w for w in changed) for p in [16,17]] == [20,20],
                'nonarc swap did not produce saturated stars')
        require(sum({16,17} <= w for w in changed) == 1, 'nonarc swap pair degree failed')
        swaps += 1
    # Known orthogoval planes from a fixed mask fixture, built without reading
    # another directory. The original absent-pair fixture has both stars.
    q_lines = [51, 197, 680, 1292, 2136, 2566, 4448, 5633, 8976, 9282, 14464, 16770, 19488, 20500, 24585, 33936, 35073, 36874, 40996, 49728]
    design = frozenset(map(verify.decode,q_lines))
    verify.check_plane(design)
    require(all(len(a&b) <= 2 for a in plane for b in design), 'arc branch lacks orthogoval planes')
    additions = 0
    for missing in design:
        original = [line | {17} for line in plane]
        original += [line | {16} for line in design if line != missing]
        verify.validate_code(list(map(verify.encode,original)))
        changed = original + [missing | {16}]
        verify.validate_code(list(map(verify.encode,changed)))
        require([sum(p in w for w in changed) for p in [16,17]] == [20,20],
                'arc augmentation failed saturation')
        additions += 1
    # Every mutually compatible family of triples of a four-set has <=4
    # members; a four-point intersection consumes every triple at once.
    intersections = [frozenset(a) for size in [3,4] for a in itertools.combinations(range(4),size)]
    for code in range(1 << len(intersections)):
        chosen = [a for i,a in enumerate(intersections) if code >> i & 1]
        if all(len(a&b) <= 2 for a,b in itertools.combinations(chosen,2)):
            require(len(chosen) <= 4, 'removed-word triple capacity failed')
    return leaves,swaps,additions

def main():
    start = time.monotonic()
    graphs,clique_queries = small_graphs()
    orthogonality_checks = orthogonality()
    partition_count, cap_checks = partition_audit()
    leave_cases, nonarc_swaps, arc_additions = degree_nineteen_bridges()
    base = Path(__file__).parent
    witness = json.loads((base/'witness56.json').read_text())
    verify.check_witness(witness)
    corrupt = copy.deepcopy(witness)
    corrupt['words'][1] = corrupt['words'][0]
    rejected(verify.check_witness,corrupt)
    corrupt = copy.deepcopy(witness)
    corrupt['specified_pair'] = [0,1]
    rejected(verify.check_witness,corrupt)
    corrupt = copy.deepcopy(witness)
    corrupt['pair_degree'] = 0
    rejected(verify.check_witness,corrupt)
    manifest = json.loads((base/'expected.json').read_text())
    case = next(c for c in manifest['cases'] if c['maximum']>=2)
    corrupt = copy.deepcopy(case)
    corrupt['attaining_words'][1] = corrupt['attaining_words'][0]
    rejected(verify.validate_case,corrupt,verify.field_plane())
    corrupt = copy.deepcopy(case)
    corrupt['anchor'] = 1
    rejected(verify.validate_case,corrupt,verify.field_plane())
    corrupt = copy.deepcopy(case)
    corrupt['second_plane'][1] = corrupt['second_plane'][0]
    rejected(verify.validate_case,corrupt,verify.field_plane())
    rejected(verify.decode,-1)
    rejected(verify.decode,1<<16)
    plane = verify.field_plane()
    arcs = [frozenset(a) for a in itertools.combinations(range(16),4)
            if all(len(frozenset(a)&b) <= 2 for b in plane)]
    permutations = verify.group(plane)
    corrupt = copy.deepcopy(manifest)
    corrupt['carrier_groups'][1]['orbits'].pop()
    rejected(verify.verify_carriers,corrupt,plane,arcs,permutations)
    corrupt = copy.deepcopy(manifest)
    corrupt['carrier_groups'][0]['orbits'].append(corrupt['carrier_groups'][0]['orbits'][0])
    rejected(verify.verify_carriers,corrupt,plane,arcs,permutations)
    corrupt = copy.deepcopy(manifest['normalization'])
    corrupt['normalized_grid_planes'].pop()
    rejected(verify.check_normalization,corrupt)
    print(json.dumps({'status':'PASS','all_simple_graphs_through_five_vertices':graphs,
        'labelings_per_graph':2,'fixed_size_clique_queries':clique_queries,
        'orthogonality_comparisons':orthogonality_checks,'eight_point_exact_covers':partition_count,
        'degree19_completed_leaves':leave_cases,'nonarc_star_swaps':nonarc_swaps,
        'arc_missing_line_additions':arc_additions,'incomplete_searches_rejected':cap_checks,'malformed_inputs_rejected':11,
        'seconds':round(time.monotonic()-start,4)}))


if __name__ == '__main__':
    main()
