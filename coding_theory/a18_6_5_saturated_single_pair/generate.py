#!/usr/bin/env python3
"""Complete one-exceptional-line plane census and exact residual bounds."""
import argparse
import hashlib
import itertools
import json
import resource
import time
from pathlib import Path

from geometry import automorphisms, image, normalization, points, word

FULL = (1 << 16)-1
FIRST_LINE = word([0,1,2,3])
TRIPLE = word([1,2,3])


def partitions(blocks, max_nodes=200_000, unused=FULL):
    by_point = [[b for b in blocks if b >> p & 1] for p in range(16)]
    output = []
    nodes = 0
    def visit(left, chosen):
        nonlocal nodes
        nodes += 1
        if nodes > max_nodes:
            raise RuntimeError('INCOMPLETE partition node cap')
        if not left:
            output.append(tuple(sorted(chosen)))
            return
        p = (left & -left).bit_length()-1
        for b in by_point[p]:
            if b & left == b:
                visit(left ^ b, chosen+(b,))
    visit(unused, ())
    if len(set(output)) != len(output):
        raise ValueError('duplicate partition')
    return sorted(output),nodes


def maximum_clique(neighbors, node_cap=200_000):
    """Complete increasing inclusion/deletion recursion with exact bit masks."""
    best = ()
    nodes = 0
    def visit(chosen, active):
        nonlocal best,nodes
        nodes += 1
        if nodes > node_cap:
            raise RuntimeError('INCOMPLETE residual clique cap')
        if len(chosen)+active.bit_count() <= len(best):
            return
        if not active:
            best = chosen
            return
        while active:
            bit = active & -active
            active ^= bit
            v = bit.bit_length()-1
            visit(chosen+(v,), active & neighbors[v])
            if len(chosen)+active.bit_count() <= len(best):
                break
    visit((),(1 << len(neighbors))-1)
    return best,nodes


def valid_code(words):
    return (len(words) == len(set(words))
            and all(type(b) is int and 0 <= b < (1 << 18) and b.bit_count() == 5 for b in words)
            and all((a&b).bit_count() <= 2 for a,b in itertools.combinations(words,2)))


def star_words(plane, second, anchor):
    exceptional = TRIPLE | (1 << anchor)
    return sorted([a | (1 << 17) for a in plane if a != FIRST_LINE]
                  + [a | (1 << 16) for a in second if a != exceptional]
                  + [TRIPLE | (1 << 16) | (1 << 17)])


def first_carriers(arcs, permutations):
    flags = {(g[0],image(FIRST_LINE,g)) for g in permutations}
    if len(flags) != 80:
        raise ValueError('incomplete point-line flag normalization')
    stabilizer = [g for g in permutations if g[0] == 0 and image(FIRST_LINE,g) == FIRST_LINE]
    if len(stabilizer) != 72:
        raise ValueError('first flag stabilizer mismatch')
    anchors = set(range(16))-set(points(TRIPLE))
    remaining = anchors.copy()
    anchor_orbits = []
    while remaining:
        representative = min(remaining)
        orbit = {g[representative] for g in stabilizer}
        if not orbit <= remaining:
            raise ValueError('invalid anchor orbit')
        remaining.difference_update(orbit)
        anchor_orbits.append(sorted(orbit))
    if anchor_orbits != [[0],list(range(4,16))]:
        raise ValueError('second anchor normalization mismatch')
    carriers = []
    groups = []
    for anchor in [0,4]:
        exceptional = TRIPLE | (1 << anchor)
        subgroup = [g for g in stabilizer if g[anchor] == anchor]
        complements,nodes = partitions([a for a in arcs if not a & exceptional],unused=FULL ^ exceptional)
        classes = {tuple(sorted((exceptional,)+c)) for c in complements}
        left = classes.copy()
        orbits = []
        while left:
            representative = min(left)
            orbit = {tuple(sorted(image(b,g) for b in representative)) for g in subgroup}
            if not orbit <= left:
                raise ValueError('first parallel-class orbit overlap')
            left.difference_update(orbit)
            row = {'representative':representative,'size':len(orbit)}
            orbits.append(row)
            carriers.append((anchor,row))
        groups.append({'anchor':anchor,'exceptional_line':exceptional,'stabilizer_order':len(subgroup),
                       'parallel_class_count':len(classes),'partition_nodes':nodes,'orbits':orbits})
    if [(g['stabilizer_order'],g['parallel_class_count'],len(g['orbits'])) for g in groups] != [(72,600,14),(6,537,92)]:
        raise ValueError('first carrier baseline mismatch')
    return groups,carriers


def run(progress):
    baseline = normalization()
    plane = baseline['first_plane']
    arcs = [word(a) for a in itertools.combinations(range(16),4)
            if all((word(a)&b).bit_count() <= 2 for b in plane)]
    residual = [word(a) for a in itertools.combinations(range(16),5)
                if (word(a)&TRIPLE).bit_count() <= 2
                and all((word(a)&b).bit_count() <= 2 for b in plane if b != FIRST_LINE)]
    if len(arcs) != 840 or len(residual) != 378:
        raise ValueError('first-plane candidate count mismatch')
    permutations = automorphisms(plane)
    groups,carriers = first_carriers(arcs,permutations)
    cases = {}
    rows = []
    for index,(anchor,orbit) in enumerate(carriers):
        first = orbit['representative']
        exceptional = TRIPLE | (1 << anchor)
        allowed = set(arcs) | {exceptional}
        transverse = [a for a in arcs if all((a&b).bit_count() == 1 for b in first)]
        second_classes,nodes = partitions(transverse)
        occurrences = {}
        for second in second_classes:
            mapping = [points(r&c)[0] for r in first for c in second]
            if len(set(mapping)) != 16:
                raise ValueError('invalid affine coordinate grid')
            for grid_plane in baseline['normalized_grid_planes']:
                design = tuple(sorted(image(a,mapping) for a in grid_plane))
                if exceptional in design and all(a in allowed for a in design):
                    occurrences[design] = occurrences.get(design,0)+1
        if any(n != 4 for n in occurrences.values()):
            raise ValueError('incomplete grid completion multiplicity')
        for design in sorted(occurrences):
            key = (anchor,design)
            if key in cases:
                continue
            stars = star_words(plane,design,anchor)
            if len(stars) != 39 or not valid_code(stars):
                raise ValueError('invalid two-star bridge')
            if [sum(b >> p & 1 for b in stars) for p in [16,17]] != [20,20]:
                raise ValueError('invalid two-star degrees')
            common = [a for a in residual if all((a&b).bit_count() <= 2 for b in design if b != exceptional)]
            if any((a&b).bit_count() > 2 for a in common for b in stars):
                raise ValueError('invalid residual bridge')
            neighbors = [sum(1 << j for j,b in enumerate(common) if i != j and (a&b).bit_count() <= 2)
                         for i,a in enumerate(common)]
            witness,clique_nodes = maximum_clique(neighbors)
            attaining = [common[i] for i in witness]
            if not valid_code(stars+attaining):
                raise ValueError('invalid attaining residual code')
            cases[key] = {'anchor':anchor,'second_plane':design,'common_five_arcs':common,
                          'maximum':len(witness),'attaining_words':attaining,'clique_nodes':clique_nodes}
        rows.append({'index':index,'anchor':anchor,'first_class':first,'orbit_size':orbit['size'],
                     'transverse_quadruples':len(transverse),'second_classes':len(second_classes),
                     'partition_nodes':nodes,'grid_completions':2*len(second_classes),
                     'compatible_planes':len(occurrences)})
        if progress:
            progress.write_text(json.dumps({'status':'INCOMPLETE','completed_carriers':len(rows),
                'total_carriers':len(carriers),'rows':rows},indent=2)+'\n')
    summaries = []
    for anchor in [0,4]:
        local = [case for (b,q),case in cases.items() if b == anchor]
        common_hist = {}
        maximum_hist = {}
        for case in local:
            n = len(case['common_five_arcs'])
            common_hist[n] = common_hist.get(n,0)+1
            maximum_hist[case['maximum']] = maximum_hist.get(case['maximum'],0)+1
        summaries.append({'anchor':anchor,'representative_planes':len(local),
                          'common_five_arc_histogram':common_hist,'residual_maximum_histogram':maximum_hist,
                          'max_residual_code':max(maximum_hist),'restricted_code_maximum':39+max(maximum_hist)})
    if [s['restricted_code_maximum'] for s in summaries] != [56,53]:
        raise ValueError('restricted theorem summary mismatch')
    return {'schema':1,'agent':'six-code-3','role':'researcher',
            'claim':'Exact maximum56 for (18,6,5) packings with d_x=d_y=20 and lambda_xy=1',
            'normalization':baseline,'first_plane_four_arcs':len(arcs),'first_star_residual_candidates':len(residual),
            'symmetries':len(permutations),'point_line_flags':80,'first_flag_stabilizer':72,
            'second_anchor_orbits':[[0],list(range(4,16))],'carrier_groups':groups,
            'rows':rows,'cases':[cases[key] for key in sorted(cases)],'anchor_summaries':summaries,
            'max_residual_code':17,'restricted_code_maximum':56}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--check',type=Path)
    parser.add_argument('--witness',type=Path,help='write an attaining fifty-six-word fixture')
    parser.add_argument('--progress',type=Path,help='optional INCOMPLETE per-carrier checkpoint')
    args = parser.parse_args()
    if not args.output and not args.check:
        parser.error('provide --output or --check')
    start = time.monotonic()
    result = run(args.progress)
    serialized = json.dumps(result,separators=(',',':'))+'\n'
    if args.check and json.loads(serialized) != json.loads(args.check.read_text()):
        raise ValueError('entry-level complete replay mismatch')
    if args.output:
        args.output.write_text(serialized)
    if args.witness:
        case = next(c for c in result['cases'] if c['maximum'] == 17)
        words = sorted(star_words(result['normalization']['first_plane'],case['second_plane'],case['anchor'])
                       + case['attaining_words'])
        fixture = {'agent':'six-code-3','role':'researcher','words':words,'specified_pair':[16,17],
                   'pair_degree':1,'degrees':[sum(b >> p & 1 for b in words) for p in range(18)]}
        args.witness.write_text(json.dumps(fixture,indent=2)+'\n')
    print(json.dumps({'status':'COMPLETE','carrier_count':len(result['rows']),'representative_planes':len(result['cases']),
        'anchor_summaries':result['anchor_summaries'],'restricted_code_maximum':result['restricted_code_maximum'],
        'manifest_sha256':hashlib.sha256(serialized.encode()).hexdigest(),'seconds':round(time.monotonic()-start,4),
        'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))


if __name__ == '__main__':
    main()
