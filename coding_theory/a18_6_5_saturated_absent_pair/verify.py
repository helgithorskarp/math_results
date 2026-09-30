#!/usr/bin/env python3
"""Separate set/orthogonal-parallel-class verification of the full theorem.

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


def validate_case(case,plane):
    design = frozenset(map(decode,case['second_plane']))
    if len(case['second_plane']) != len(design):
        raise ValueError('duplicate second-plane line')
    check_plane(design)
    if any(len(a&b)>2 for a in plane for b in design):
        raise ValueError('planes are not orthogoval')
    common = [decode(a) for a in case['common_five_arcs']]
    if len(set(common)) != len(common) or any(len(a)!=5 for a in common):
        raise ValueError('invalid common-five-arc list')
    if any(len(a&b)>2 for a in common for b in plane|design):
        raise ValueError('invalid claimed common arc')
    witness = [decode(a) for a in case['attaining_words']]
    if (type(case['maximum']) is not int or case['maximum'] != len(witness)
        or len(set(witness)) != len(witness) or not set(witness) <= set(common)
        or any(len(a&b)>2 for a,b in itertools.combinations(witness,2))):
        raise ValueError('invalid residual lower-bound witness')
    return design


def check_witness(data):
    words = data['words']
    if (len(words) != len(set(words)) or len(words) != 56
        or any(type(b) is not int or not 0<=b<(1<<18) or b.bit_count()!=5 for b in words)
        or any((a&b).bit_count()>2 for a,b in itertools.combinations(words,2))):
        raise ValueError('invalid fifty-six-word witness')
    absent_pair = data['absent_pair']
    if absent_pair != [16,17] or any(b>>16&1 and b>>17&1 for b in words):
        raise ValueError('witness lacks specified absent pair')
    degrees = [sum(b>>p&1 for b in words) for p in range(18)]
    if degrees != data['degrees'] or degrees[16:] != [20,20]:
        raise ValueError('witness point-degree mismatch')
    return degrees


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


def cliques_of_size(neighbors,target,node_cap=2_000_000):
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


def maximum_clique(neighbors,node_cap=2_000_000):
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest',type=Path,default=BASE/'expected.json')
    parser.add_argument('--witness',type=Path,default=BASE/'witness56.json')
    parser.add_argument('--output',type=Path,help='optional compact operational result')
    parser.add_argument('--progress',type=Path,help='optional incomplete per-orbit checkpoint')
    args = parser.parse_args()
    start = time.monotonic()
    expected = json.loads(args.manifest.read_text())
    if expected['schema'] != 1:
        raise ValueError('unsupported manifest schema')
    plane = field_plane()
    if sorted(map(encode,plane)) != expected['normalization']['first_plane']:
        raise ValueError('first plane input mismatch')
    check_plane(plane)
    latin_count,latin_triples = check_normalization(expected['normalization'])
    witness_degrees = check_witness(json.loads(args.witness.read_text()))
    cases = {validate_case(c,plane):c for c in expected['cases']}
    if len(cases) != len(expected['cases']):
        raise ValueError('duplicate manifest case')
    if len(expected['rows']) != len(expected['first_class_orbits']):
        raise ValueError('incomplete first-class rows')
    arcs4 = [frozenset(p) for p in itertools.combinations(range(16),4)
             if all(len(frozenset(p)&line)<=2 for line in plane)]
    perms = group(plane)
    partitions,nodes = all_arc_partitions(arcs4)
    if len(partitions) != expected['partition_count']:
        raise ValueError('first class coverage count mismatch')
    covered = set()
    for row in expected['first_class_orbits']:
        representative = frozenset(map(decode,row['representative']))
        orbit = {frozenset(frozenset(g[p] for p in b) for b in representative) for g in perms}
        if len(orbit) != row['size'] or not orbit <= partitions or orbit & covered:
            raise ValueError('invalid representative orbit coverage')
        covered.update(orbit)
    if covered != partitions:
        raise ValueError('missing first-class orbit')
    print(json.dumps({'stage':'independent-orbit-cover','partitions':len(partitions),
                      'orbits':len(expected['first_class_orbits']),
                      'seconds':round(time.monotonic()-start,3)}),flush=True)
    all_fives = [frozenset(p) for p in itertools.combinations(range(16),5)]
    all_planes = set()
    output_rows = []
    for index, orbit_row in enumerate(expected['first_class_orbits']):
        first = frozenset(map(decode,orbit_row['representative']))
        classes, partition_nodes = transverse_classes(first,arcs4)
        expected_row = expected['rows'][index]
        if len(classes) != expected_row['second_classes']:
            raise ValueError('transverse class count mismatch')
        designs,edges,clique_nodes = orthogonal_completions(first,classes)
        # Entry-level comparison with the generator's overall list, localized
        # by the exact first class. No aggregate-only classification comparison.
        old = {d for d in cases if first <= d}
        if designs != old:
            raise ValueError('second-plane entry mismatch')
        all_planes.update(designs)
        row = {'index':index,'parallel_classes':len(classes),'orthogonality_edges':edges,
               'four_clique_nodes':clique_nodes,'complete_planes':len(designs)}
        output_rows.append(row)
        if args.progress:
            args.progress.write_text(json.dumps({'status':'INCOMPLETE',
                'completed_orbits':len(output_rows),'total_orbits':len(expected['rows']),
                'rows':output_rows},indent=2)+'\n')
        print(json.dumps({'stage':'independent-plane-completion',**row,
                          'seconds':round(time.monotonic()-start,3)}),flush=True)
    if all_planes != set(cases):
        raise ValueError('complete plane list mismatch')
    common_histogram = {}
    clique_histogram = {}
    residual_nodes = 0
    for design in sorted(cases,key=lambda d:tuple(sorted(map(encode,d)))):
        case = cases[design]
        common = [a for a in all_fives if all(len(a&b)<=2 for b in plane|design)]
        if set(common) != set(map(decode,case['common_five_arcs'])):
            raise ValueError('incomplete common-five-arc input')
        neighbors = [{j for j,b in enumerate(common) if i!=j and len(a&b)<=2}
                     for i,a in enumerate(common)]
        maximum,nodes = maximum_clique(neighbors)
        residual_nodes += nodes
        if len(maximum) != case['maximum']:
            raise ValueError('residual maximum mismatch')
        common_histogram[len(common)] = common_histogram.get(len(common),0)+1
        clique_histogram[len(maximum)] = clique_histogram.get(len(maximum),0)+1
    if ({str(k):v for k,v in common_histogram.items()} != expected['common_five_arc_histogram']
        or {str(k):v for k,v in clique_histogram.items()} != expected['residual_maximum_histogram']
        or max(common_histogram) != expected['max_common_five_arcs']
        or max(clique_histogram) != expected['max_residual_code']
        or 40+max(clique_histogram) != expected['restricted_code_maximum']
        or expected['restricted_code_maximum'] != 56):
        raise ValueError('final theorem summary mismatch')
    result = {'agent':'six-code-3','role':'researcher',
              'status':'COMPLETE; separate exact verification, no peer review or formalization',
              'normalized_latin_squares':latin_count,'orthogonal_latin_triples':latin_triples,
              'first_class_partitions':len(partitions),'symmetries':len(perms),
              'representative_planes':len(all_planes),'rows':output_rows,
              'maximum_common_five_arcs':max(common_histogram),
              'maximum_residual_code':max(clique_histogram),'restricted_code_maximum':56,
              'residual_maximal_clique_nodes':residual_nodes,'witness56_degrees':witness_degrees,
              'seconds':round(time.monotonic()-start,4),
              'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    if args.output:
        args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'}),flush=True)


if __name__=='__main__':
    main()
