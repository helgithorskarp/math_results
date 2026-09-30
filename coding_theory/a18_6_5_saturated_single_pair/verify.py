#!/usr/bin/env python3
"""Separate set/orthogonal-class verification of the single-pair theorem.

Imports no generator code. Uses a generated permutation closure, set partitions
and complete four-clique enumeration, rather than two Latin completions per grid.
"""
import argparse
import itertools
import json
import resource
import time
from pathlib import Path

BASE = Path(__file__).parent
MULT = ((0,0,0,0),(0,1,2,3),(0,2,3,1),(0,3,1,2))


def decode(mask):
    if type(mask) is not int or not 0 <= mask < (1 << 16):
        raise ValueError('invalid sixteen-point mask')
    return frozenset(i for i in range(16) if mask & (1 << i))


def encode(block):
    return sum(1 << i for i in block)


def field_plane():
    return frozenset([frozenset(4*x+y for y in range(4)) for x in range(4)]
        + [frozenset(4*x+(MULT[m][x]^b) for x in range(4))
           for m in range(4) for b in range(4)])


def check_plane(design):
    if (len(design) != 20 or any(len(b) != 4 for b in design)
        or any(sum(a in b and c in b for b in design) != 1
               for a,c in itertools.combinations(range(16),2))):
        raise ValueError('invalid affine plane')


def check_normalization(expected):
    """Cell-wise Latin enumeration; no generator or geometry import."""
    squares = []
    entries = list(range(4)) + [-1]*12
    row_used = [set(range(4)),set(),set(),set()]
    col_used = [{i} for i in range(4)]
    def visit(position):
        if position == 16:
            squares.append(tuple(entries))
            return
        r,c = divmod(position,4)
        for value in range(4):
            if value not in row_used[r] and value not in col_used[c]:
                entries[position] = value
                row_used[r].add(value)
                col_used[c].add(value)
                visit(position+1)
                row_used[r].remove(value)
                col_used[c].remove(value)
    visit(4)
    orthogonal = lambda a,b: len(set(zip(a,b))) == 16
    triples = [t for t in itertools.combinations(squares,3)
               if all(orthogonal(a,b) for a,b in itertools.combinations(t,2))]
    grid = frozenset([frozenset(4*r+c for c in range(4)) for r in range(4)]
                  + [frozenset(4*r+c for r in range(4)) for c in range(4)])
    planes = {grid | frozenset(frozenset(p for p in range(16) if s[p] == symbol)
                              for s in t for symbol in range(4)) for t in triples}
    if (len(squares) != expected['normalized_latin_squares'] or len(squares) != 24
        or len(triples) != expected['complete_orthogonal_triples'] or len(triples) != 2
        or planes != {frozenset(map(decode,d)) for d in expected['normalized_grid_planes']}):
        raise ValueError('incomplete first-plane normalization')
    original = field_plane()
    maps = expected['maps_to_first_plane']
    if len(maps) != len(expected['normalized_grid_planes']):
        raise ValueError('missing normalization map')
    for design,permutation in zip(expected['normalized_grid_planes'],maps):
        if set(permutation) != set(range(16)) or len(permutation) != 16:
            raise ValueError('invalid normalization map')
        if frozenset(frozenset(permutation[p] for p in decode(b)) for b in design) != original:
            raise ValueError('incorrect normalization map')
    return len(squares),len(triples)


def group(plane):
    transformations = [
        lambda x,y: (x^1,y), lambda x,y: (x^2,y),
        lambda x,y: (x,y^1), lambda x,y: (x,y^2),
        lambda x,y: (MULT[2][x],y), lambda x,y: (x,MULT[2][y]),
        lambda x,y: (y,x), lambda x,y: (x^y,y),
        lambda x,y: (MULT[x][x],MULT[y][y])]
    generators = [tuple(4*f(*divmod(p,4))[0]+f(*divmod(p,4))[1]
                        for p in range(16)) for f in transformations]
    identity = tuple(range(16))
    found = {identity}
    queue = [identity]
    for perm in queue:
        for generator in generators:
            new = tuple(generator[perm[p]] for p in range(16))
            if new not in found:
                if len(found) >= 6000:
                    raise RuntimeError('INCOMPLETE permutation closure cap')
                if set(new) != set(range(16)):
                    raise ValueError('non-permutation')
                if frozenset(frozenset(new[p] for p in b) for b in plane) != plane:
                    raise ValueError('invalid plane symmetry')
                found.add(new)
                queue.append(new)
    if len(found) != 5760:
        raise ValueError('group order mismatch')
    return sorted(found)


def all_arc_partitions(arcs):
    by_point = {p:[b for b in arcs if p in b] for p in range(16)}
    output = set()
    nodes = 0
    def visit(unused, blocks):
        nonlocal nodes
        nodes += 1
        if nodes > 2_000_000:
            raise RuntimeError('INCOMPLETE partition enumeration cap')
        if not unused:
            output.add(frozenset(blocks))
            return
        p = min(unused)
        for b in by_point[p]:
            if b <= unused:
                visit(unused-b, blocks+(b,))
    visit(frozenset(range(16)),())
    return output,nodes


def transverse_classes(first, arcs):
    rows = sorted(first, key=encode)
    anchors = sorted(rows[0])
    choices = {p:[] for p in anchors}
    for arc in arcs:
        if all(len(arc & row) == 1 for row in rows):
            choices[next(iter(arc & rows[0]))].append(arc)
    output = []
    nodes = 0
    def visit(depth, used, chosen):
        nonlocal nodes
        nodes += 1
        if nodes > 200_000:
            raise RuntimeError('INCOMPLETE transversal enumeration cap')
        if depth == 4:
            if used != frozenset(range(16)):
                raise ValueError('non-covering parallel class')
            output.append(frozenset(chosen))
            return
        for arc in choices[anchors[depth]]:
            if not arc & used:
                visit(depth+1, used | arc, chosen+(arc,))
    visit(0, frozenset(), ())
    if len(set(output)) != len(output):
        raise ValueError('duplicate transversal class')
    return sorted(output, key=lambda c:tuple(sorted(encode(b) for b in c))),nodes


def orthogonal_labels(left,right,width=4):
    if len(left) != width*width or len(right) != width*width:
        raise ValueError('invalid orthogonal-class label length')
    flags = 0
    for a,b in zip(left,right):
        if not 0<=a<width or not 0<=b<width:
            raise ValueError('invalid orthogonal-class label')
        flag = 1 << (width*a+b)
        if flags & flag:
            return False
        flags |= flag
    return True


def cliques_of_size(neighbors,target,node_cap=200_000):
    result = []
    nodes = 0
    def visit(chosen,candidates):
        nonlocal nodes
        nodes += 1
        if nodes > node_cap:
            raise RuntimeError('INCOMPLETE fixed-size clique cap')
        need = target-len(chosen)
        if need == 0:
            result.append(chosen)
            return
        active = sorted(candidates)
        for index,v in enumerate(active):
            if len(active)-index < need:
                break
            visit(chosen+(v,),set(active[index+1:]) & neighbors[v])
    visit((),set(range(len(neighbors))))
    return result,nodes


def maximum_clique(neighbors,node_cap=200_000):
    """Bron--Kerbosch maximal-clique enumeration; independent of generator."""
    best = ()
    nodes = 0
    def visit(chosen,possible,excluded):
        nonlocal best,nodes
        nodes += 1
        if nodes > node_cap:
            raise RuntimeError('INCOMPLETE maximal-clique cap')
        if not possible and not excluded:
            if len(chosen)>len(best):
                best = chosen
            return
        pivot = max(possible|excluded,key=lambda u:(len(possible&neighbors[u]),-u))
        for v in sorted(possible-neighbors[pivot]):
            visit(chosen+(v,),possible&neighbors[v],excluded&neighbors[v])
            possible.remove(v)
            excluded.add(v)
    visit((),set(range(len(neighbors))),set())
    return best,nodes


def orthogonal_completions(first, classes):
    # Class labels assigned through the anchor row. Orthogonality is injectivity
    # of the sixteen ordered class labels, checked without mask intersections.
    assignments = []
    for blocks in classes:
        ordered = sorted(blocks, key=encode)
        assignments.append(tuple(next(i for i,b in enumerate(ordered) if p in b)
                                 for p in range(16)))
    neighbors = [set() for _ in classes]
    for i, left in enumerate(assignments):
        for j in range(i+1,len(classes)):
            right = assignments[j]
            if orthogonal_labels(left,right):
                neighbors[i].add(j)
                neighbors[j].add(i)
    results = set()
    completions,nodes = cliques_of_size(neighbors,4)
    for chosen in completions:
        design = first | frozenset(b for i in chosen for b in classes[i])
        check_plane(design)
        if design in results:
            raise ValueError('duplicate five-class decomposition')
        results.add(design)
    return results, sum(map(len,neighbors))//2, nodes


def validate_code(words):
    if (len(words) != len(set(words))
        or any(type(b) is not int or not 0 <= b < (1 << 18) or b.bit_count() != 5 for b in words)
        or any((a&b).bit_count() > 2 for a,b in itertools.combinations(words,2))):
        raise ValueError('invalid constant-weight code')


def check_witness(data):
    words = data['words']
    validate_code(words)
    degrees = [sum(b >> p & 1 for b in words) for p in range(18)]
    pair_degree = sum((b >> 16 & 3) == 3 for b in words)
    if (len(words) != 56 or data['specified_pair'] != [16,17]
        or data['pair_degree'] != pair_degree or pair_degree != 1
        or data['degrees'] != degrees or degrees[16:] != [20,20]):
        raise ValueError('witness fails the specified two-star conditions')
    return degrees


def two_stars(plane, design, anchor):
    first_line = frozenset([0,1,2,3])
    triple = frozenset([1,2,3])
    exceptional = triple | {anchor}
    stars = [a | {17} for a in plane if a != first_line]
    stars += [a | {16} for a in design if a != exceptional]
    stars += [triple | {16,17}]
    validate_code(list(map(encode,stars)))
    if len(stars) != 39 or [sum(p in a for a in stars) for p in [16,17]] != [20,20]:
        raise ValueError('invalid complete two-star union')
    return stars


def validate_case(case, plane):
    anchor = case['anchor']
    if type(anchor) is not int or anchor not in [0,4]:
        raise ValueError('invalid second split anchor')
    design = frozenset(map(decode,case['second_plane']))
    if len(design) != len(case['second_plane']):
        raise ValueError('duplicate second-plane line')
    check_plane(design)
    exceptional = frozenset([1,2,3,anchor])
    first_line = frozenset([0,1,2,3])
    if (exceptional not in design
        or {(a,b) for a in plane for b in design if len(a&b) > 2} != {(first_line,exceptional)}):
        raise ValueError('planes lack the unique exceptional line pair')
    stars = two_stars(plane,design,anchor)
    common = [decode(a) for a in case['common_five_arcs']]
    if (len(common) != len(set(common)) or any(len(a) != 5 for a in common)
        or any(len(a&b) > 2 for a in common for b in stars)):
        raise ValueError('invalid common residual list')
    witness = [decode(a) for a in case['attaining_words']]
    if (type(case['maximum']) is not int or len(witness) != case['maximum']
        or len(witness) != len(set(witness)) or not set(witness) <= set(common)):
        raise ValueError('invalid residual lower-bound witness')
    validate_code(list(map(encode,stars+witness)))
    return anchor,design


def exceptional_classes(exceptional, arcs):
    """Set partitions of the twelve-point complement, with the line fixed."""
    choices = {p:[a for a in arcs if p in a and not a & exceptional] for p in range(16)}
    output = set()
    nodes = 0
    def visit(unused, chosen):
        nonlocal nodes
        nodes += 1
        if nodes > 200_000:
            raise RuntimeError('INCOMPLETE exceptional class cap')
        if not unused:
            output.add(frozenset((exceptional,)+chosen))
            return
        # Largest point contrasts with the generator's smallest-point masks.
        point = max(unused)
        for block in choices[point]:
            if block <= unused:
                visit(unused-block,chosen+(block,))
    visit(frozenset(range(16))-exceptional,())
    return output,nodes


def verify_carriers(expected, plane, arcs, permutations):
    first_line = frozenset([0,1,2,3])
    image = lambda a,g:frozenset(g[p] for p in a)
    if {(g[0],image(first_line,g)) for g in permutations} != {(p,line) for line in plane for p in line}:
        raise ValueError('missing point-line flag normalization')
    stabilizer = [g for g in permutations if g[0] == 0 and image(first_line,g) == first_line]
    if len(stabilizer) != 72 or expected['first_flag_stabilizer'] != 72 or expected['point_line_flags'] != 80:
        raise ValueError('flag stabilizer summary mismatch')
    anchor_orbits = [sorted({g[b] for g in stabilizer}) for b in [0,4]]
    if anchor_orbits != [[0],list(range(4,16))] or expected['second_anchor_orbits'] != anchor_orbits:
        raise ValueError('second anchor orbit cover mismatch')
    carriers = []
    if [g['anchor'] for g in expected['carrier_groups']] != [0,4]:
        raise ValueError('incomplete carrier anchor list')
    for group_row in expected['carrier_groups']:
        anchor = group_row['anchor']
        exceptional = frozenset([1,2,3,anchor])
        subgroup = [g for g in stabilizer if g[anchor] == anchor]
        classes,nodes = exceptional_classes(exceptional,arcs)
        if (group_row['exceptional_line'] != encode(exceptional)
            or len(subgroup) != group_row['stabilizer_order']
            or len(classes) != group_row['parallel_class_count']):
            raise ValueError('carrier baseline count mismatch')
        covered = set()
        for orbit_row in group_row['orbits']:
            representative = frozenset(map(decode,orbit_row['representative']))
            orbit = {frozenset(image(b,g) for b in representative) for g in subgroup}
            if len(orbit) != orbit_row['size'] or not orbit <= classes or orbit & covered:
                raise ValueError('invalid first parallel-class orbit cover')
            covered.update(orbit)
            carriers.append((anchor,representative,orbit_row['size']))
        if covered != classes:
            raise ValueError('incomplete first parallel-class orbit cover')
    if len(carriers) != 106 or len(expected['rows']) != 106:
        raise ValueError('incomplete carrier row list')
    return carriers


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    base = Path(__file__).parent
    parser.add_argument('--manifest',type=Path,default=base/'expected.json')
    parser.add_argument('--witness',type=Path,default=base/'witness56.json')
    parser.add_argument('--output',type=Path)
    parser.add_argument('--progress',type=Path,help='optional INCOMPLETE per-carrier checkpoint')
    args = parser.parse_args()
    start = time.monotonic()
    expected = json.loads(args.manifest.read_text())
    if expected['schema'] != 1:
        raise ValueError('unsupported manifest schema')
    plane = field_plane()
    check_plane(plane)
    if sorted(map(encode,plane)) != expected['normalization']['first_plane']:
        raise ValueError('first plane input mismatch')
    latin_count,latin_triples = check_normalization(expected['normalization'])
    witness_degrees = check_witness(json.loads(args.witness.read_text()))
    arcs = [frozenset(a) for a in itertools.combinations(range(16),4)
            if all(len(frozenset(a)&b) <= 2 for b in plane)]
    all_fives = [frozenset(a) for a in itertools.combinations(range(16),5)]
    first_candidates = [a for a in all_fives if len(a & {1,2,3}) <= 2
                        and all(len(a&b) <= 2 for b in plane if b != frozenset([0,1,2,3]))]
    if (len(arcs) != 840 or len(arcs) != expected['first_plane_four_arcs']
        or len(first_candidates) != 378 or len(first_candidates) != expected['first_star_residual_candidates']):
        raise ValueError('first-star candidate count mismatch')
    permutations = group(plane)
    if len(permutations) != expected['symmetries']:
        raise ValueError('symmetry summary mismatch')
    carriers = verify_carriers(expected,plane,arcs,permutations)
    cases = {validate_case(c,plane):c for c in expected['cases']}
    if len(cases) != len(expected['cases']):
        raise ValueError('duplicate manifest case')
    print(json.dumps({'stage':'independent first-carrier coverage','carriers':len(carriers),
                      'seconds':round(time.monotonic()-start,3)}),flush=True)
    all_designs = set()
    output_rows = []
    for index,(anchor,first,orbit_size) in enumerate(carriers):
        expected_row = expected['rows'][index]
        if (expected_row['index'] != index or expected_row['anchor'] != anchor
            or frozenset(map(decode,expected_row['first_class'])) != first
            or expected_row['orbit_size'] != orbit_size):
            raise ValueError('incorrect carrier row provenance')
        classes,nodes = transverse_classes(first,arcs)
        if len(classes) != expected_row['second_classes']:
            raise ValueError('incomplete transverse class list')
        designs,edges,clique_nodes = orthogonal_completions(first,classes)
        old = {q for b,q in cases if b == anchor and first <= q}
        if designs != old or len(designs) != expected_row['compatible_planes']:
            raise ValueError('second-plane entry-level coverage mismatch')
        all_designs.update((anchor,q) for q in designs)
        output_rows.append({'index':index,'anchor':anchor,'parallel_classes':len(classes),
                            'orthogonality_edges':edges,'four_clique_nodes':clique_nodes,'complete_planes':len(designs)})
        if args.progress:
            args.progress.write_text(json.dumps({'status':'INCOMPLETE','completed_carriers':len(output_rows),
                'total_carriers':len(carriers),'rows':output_rows},indent=2)+'\n')
        print(json.dumps({'stage':'independent plane completion',**output_rows[-1],
                          'seconds':round(time.monotonic()-start,3)}),flush=True)
    if all_designs != set(cases):
        raise ValueError('missing second-plane case')
    histograms = {b:({}, {}) for b in [0,4]}
    residual_nodes = 0
    for (anchor,design),case in cases.items():
        stars = two_stars(plane,design,anchor)
        # Complete direct residual scan, without the generator's first-star filter.
        common = [a for a in all_fives if all(len(a&b) <= 2 for b in stars)]
        if set(common) != set(map(decode,case['common_five_arcs'])):
            raise ValueError('incomplete common-five-word list')
        neighbors = [{j for j,b in enumerate(common) if i != j and len(a&b) <= 2}
                     for i,a in enumerate(common)]
        maximum,nodes = maximum_clique(neighbors)
        residual_nodes += nodes
        if len(maximum) != case['maximum']:
            raise ValueError('residual maximum mismatch')
        common_hist,maximum_hist = histograms[anchor]
        common_hist[len(common)] = common_hist.get(len(common),0)+1
        maximum_hist[len(maximum)] = maximum_hist.get(len(maximum),0)+1
    summaries = []
    for anchor in [0,4]:
        common_hist,maximum_hist = histograms[anchor]
        summaries.append({'anchor':anchor,'representative_planes':sum(b == anchor for b,q in cases),
            'common_five_arc_histogram':{str(k):v for k,v in common_hist.items()},
            'residual_maximum_histogram':{str(k):v for k,v in maximum_hist.items()},
            'max_residual_code':max(maximum_hist),'restricted_code_maximum':39+max(maximum_hist)})
    if (summaries != expected['anchor_summaries'] or expected['max_residual_code'] != 17
        or expected['restricted_code_maximum'] != 56 or [s['restricted_code_maximum'] for s in summaries] != [56,53]):
        raise ValueError('final theorem summary mismatch')
    result = {'agent':'six-code-3','role':'researcher',
        'status':'COMPLETE; separate exact verification, no peer review or formalization',
        'normalized_latin_squares':latin_count,'orthogonal_latin_triples':latin_triples,
        'first_carriers':len(carriers),'representative_planes':len(cases),'rows':output_rows,
        'anchor_summaries':summaries,'restricted_code_maximum':56,
        'residual_maximal_clique_nodes':residual_nodes,'witness56_degrees':witness_degrees,
        'seconds':round(time.monotonic()-start,4),'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    if args.output:
        args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'rows'}),flush=True)


if __name__ == '__main__':
    main()
