#!/usr/bin/env python3
"""Complete grid enumeration and exact residual maximum-clique replay."""
import argparse
import hashlib
import itertools
import json
import resource
import time
from pathlib import Path

from geometry import automorphisms, image, normalization, points, word

FULL = (1 << 16) - 1


def partitions(blocks, max_nodes=2_000_000):
    by_point = [[b for b in blocks if b >> p & 1] for p in range(16)]
    result = []
    nodes = 0
    def visit(left, chosen):
        nonlocal nodes
        nodes += 1
        if nodes > max_nodes:
            raise RuntimeError('INCOMPLETE partition node cap')
        if not left:
            result.append(tuple(sorted(chosen)))
            return
        p = (left & -left).bit_length() - 1
        for b in by_point[p]:
            if left & b == b:
                visit(left ^ b, chosen + (b,))
    visit(FULL, ())
    if len(set(result)) != len(result):
        raise ValueError('duplicate partition')
    return sorted(result), nodes


def maximum_clique(neighbors, node_cap=2_000_000):
    """Complete increasing inclusion/deletion recursion, exact integer masks."""
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
            vertex = bit.bit_length()-1
            visit(chosen+(vertex,),active & neighbors[vertex])
            if len(chosen)+active.bit_count() <= len(best):
                break
    visit((),(1 << len(neighbors))-1)
    return best,nodes


def run(progress):
    baseline = normalization()
    plane = baseline['first_plane']
    grid_planes = baseline['normalized_grid_planes']
    arcs4 = [word(p) for p in itertools.combinations(range(16),4)
             if all((word(p)&line).bit_count() <= 2 for line in plane)]
    arcs5 = [word(p) for p in itertools.combinations(range(16),5)
             if all((word(p)&line).bit_count() <= 2 for line in plane)]
    if len(arcs4) != 840 or len(arcs5) != 288:
        raise ValueError('unexpected first-plane arc counts')
    classes,partition_nodes = partitions(arcs4)
    permutations = automorphisms(plane)
    remaining = set(classes)
    orbit_rows = []
    while remaining:
        representative = min(remaining)
        point_lists = [points(b) for b in representative]
        orbit = {tuple(sorted(word(g[p] for p in ps) for ps in point_lists)) for g in permutations}
        if not orbit <= remaining:
            raise ValueError('non-disjoint symmetry orbit')
        remaining.difference_update(orbit)
        orbit_rows.append({'representative':representative,'size':len(orbit)})
    allowed = set(arcs4)
    all_planes = set()
    rows = []
    for index,orbit_row in enumerate(orbit_rows):
        first = orbit_row['representative']
        transverse = [b for b in arcs4 if all((b&r).bit_count()==1 for r in first)]
        second_classes,nodes = partitions(transverse,200_000)
        accepted = set()
        occurrences = {}
        for second in second_classes:
            mapping = [points(r&c)[0] for r in first for c in second]
            if len(set(mapping)) != 16:
                raise ValueError('invalid coordinate grid')
            for design in grid_planes:
                candidate = tuple(sorted(image(b,mapping) for b in design))
                if all(b in allowed for b in candidate):
                    accepted.add(candidate)
                    occurrences[candidate] = occurrences.get(candidate,0)+1
        if any(n != 4 for n in occurrences.values()):
            raise ValueError('incomplete plane grid multiplicity')
        all_planes.update(accepted)
        row = {'index':index,'first_class':first,'orbit_size':orbit_row['size'],
               'transverse_quadruples':len(transverse),'second_classes':len(second_classes),
               'partition_nodes':nodes,'grid_completions':2*len(second_classes),
               'compatible_planes':len(accepted)}
        rows.append(row)
        if progress:
            Path(progress).write_text(json.dumps({'status':'INCOMPLETE','completed_orbits':len(rows),
                'total_orbits':len(orbit_rows),'rows':rows},indent=2)+'\n')
    cases = []
    common_histogram = {}
    clique_histogram = {}
    for design in sorted(all_planes):
        common = [a for a in arcs5 if all((a&b).bit_count()<=2 for b in design)]
        neighbors = [sum(1 << j for j,v in enumerate(common) if i!=j and (w&v).bit_count()<=2)
                     for i,w in enumerate(common)]
        witness,nodes = maximum_clique(neighbors)
        common_histogram[len(common)] = common_histogram.get(len(common),0)+1
        clique_histogram[len(witness)] = clique_histogram.get(len(witness),0)+1
        cases.append({'second_plane':design,'common_five_arcs':common,'maximum':len(witness),
                      'attaining_words':[common[i] for i in witness],'clique_nodes':nodes})
    return {'schema':1,'agent':'six-code-3','role':'researcher',
            'claim':'Exact maximum56 for (18,6,5) packings with d_x=d_y=20 and lambda_xy=0',
            'normalization':baseline,'first_plane_arc_counts':{'4':len(arcs4),'5':len(arcs5)},
            'partition_count':len(classes),'partition_nodes':partition_nodes,
            'symmetries':len(permutations),'first_class_orbits':orbit_rows,'rows':rows,
            'cases':cases,'common_five_arc_histogram':common_histogram,
            'residual_maximum_histogram':clique_histogram,
            'max_common_five_arcs':max(common_histogram),
            'max_residual_code':max(clique_histogram),'restricted_code_maximum':40+max(clique_histogram)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,help='write compact deterministic replay manifest')
    parser.add_argument('--check',type=Path,help='compare every output entry with an existing manifest')
    parser.add_argument('--progress',type=Path,help='optional local incomplete checkpoint after each orbit')
    args = parser.parse_args()
    if not args.output and not args.check:
        parser.error('provide --output or --check')
    start = time.monotonic()
    result = run(args.progress)
    serialized = json.dumps(result,separators=(',',':'))+'\n'
    if args.check and result != json.loads(args.check.read_text()):
        # JSON converts tuple arrays and integer object keys. Compare canonical
        # serialization semantics, rather than Python-only container types.
        if json.loads(serialized) != json.loads(args.check.read_text()):
            raise ValueError('complete replay manifest mismatch')
    if args.output:
        args.output.write_text(serialized)
    print(json.dumps({'status':'COMPLETE','cases':len(result['cases']),
        'partition_count':result['partition_count'],'first_class_orbits':len(result['first_class_orbits']),
        'maximum_common_five_arcs':result['max_common_five_arcs'],
        'maximum_residual_code':result['max_residual_code'],'restricted_code_maximum':result['restricted_code_maximum'],
        'manifest_sha256':hashlib.sha256(serialized.encode()).hexdigest(),
        'seconds':round(time.monotonic()-start,4),
        'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))


if __name__ == '__main__':
    main()
