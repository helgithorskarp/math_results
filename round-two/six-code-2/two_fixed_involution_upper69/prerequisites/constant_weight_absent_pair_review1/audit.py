#!/usr/bin/env python3
"""Independent pair-exact-cover audit. Author: six-reviewer-1, reviewer.

No campaign modules, solver, downloaded census or manifest inputs.
All guards are exceptions and survive -O. Optional author comparison is
after complete regeneration; a cap raises INCOMPLETE.
"""
import argparse
import hashlib
import itertools as it
import json
import resource
import time
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

FULL = (1 << 16) - 1
PAIRS = list(it.combinations(range(16), 2))
PAIR_INDEX = {p:i for i,p in enumerate(PAIRS)}
OMEGA = (0, 2, 3, 1)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length()-1
        mask ^= bit


def encode(points):
    return sum(1 << p for p in points)


def mul(a, b):
    return (a if b & 1 else 0) ^ (OMEGA[a] if b & 2 else 0)


def image(block, perm):
    return encode(perm[p] for p in bits(block))


def pair_mask(block):
    return sum(1 << PAIR_INDEX[p] for p in it.combinations(bits(block), 2))


def plane_check(lines):
    require(len(lines) == len(set(lines)) == 20, 'plane line count')
    seen = 0
    for b in lines:
        require(type(b) is int and 0 <= b <= FULL and b.bit_count() == 4,
                'plane line mask')
        row = pair_mask(b)
        require(not row & seen, 'plane repeats a pair')
        seen |= row
    require(seen == (1 << 120)-1, 'plane omits a pair')


def exact_cover(rows, target, cap=500_000):
    """All covers, every row used at most once, including the empty cover.

    State = uncovered pair mask and available column mask. Choose an
    uncovered pair with fewest available columns. Every complete cover
    has exactly one of those columns, giving disjoint exhaustive branches.
    Remove precisely the columns overlapping its covered pairs.
    """
    require(type(target) is int and target >= 0, 'negative exact-cover target')
    require(len(rows) == len(set(rows)), 'duplicate exact-cover column')
    require(all(type(r) is int and r > 0 and r & target == r for r in rows),
            'invalid exact-cover column')
    containing = [0]*target.bit_length()
    for j, r in enumerate(rows):
        for k in bits(r):
            containing[k] |= 1 << j
    conflicts = []
    for r in rows:
        c = 0
        for k in bits(r):
            c |= containing[k]
        conflicts.append(c)
    answer = []
    nodes = 0
    def visit(left, available, chosen):
        nonlocal nodes
        nodes += 1
        if nodes > cap:
            raise RuntimeError('INCOMPLETE pair-cover node cap')
        if not left:
            answer.append(tuple(sorted(chosen)))
            return
        options = None
        size = len(rows)+1
        for k in bits(left):
            candidates = available & containing[k]
            count = candidates.bit_count()
            if count < size:
                options, size = candidates, count
                if count <= 1:
                    break
        if not size:
            return
        for j in bits(options):
            require(rows[j] & left == rows[j], 'pair-cover availability invariant')
            visit(left ^ rows[j], available & ~conflicts[j], chosen+(j,))
    visit(target, (1 << len(rows))-1, ())
    require(len(answer) == len(set(answer)), 'duplicate exact cover')
    return sorted(answer), nodes


def independence(conflict, cap=500_000):
    """Maximum independent set by conflict-vertex include/exclude recurrence.

    Unlike either source clique engine, solve alpha(U) with memoization;
    removing all isolated vertices is exact. No supplied lower bound.
    """
    n = len(conflict)
    require(all(type(r) is int and 0 <= r < (1 << n) for r in conflict),
            'invalid conflict mask')
    require(all(not (r >> i & 1) for i,r in enumerate(conflict)), 'conflict loop')
    require(all((conflict[i] >> j & 1) == (conflict[j] >> i & 1)
                for i in range(n) for j in range(n)), 'asymmetric conflicts')
    nodes = 0
    @lru_cache(None)
    def solve(active):
        nonlocal nodes
        nodes += 1
        if nodes > cap:
            raise RuntimeError('INCOMPLETE independent-set node cap')
        isolated = encode(i for i in bits(active) if not conflict[i] & active)
        if isolated:
            return isolated | solve(active ^ isolated)
        if not active:
            return 0
        v = max(bits(active), key=lambda i:((conflict[i] & active).bit_count(),-i))
        left = active ^ (1 << v)
        exclude = solve(left)
        include = (1 << v) | solve(left & ~conflict[v])
        return include if include.bit_count() >= exclude.bit_count() else exclude
    witness = solve((1 << n)-1)
    require(all(not conflict[i] & witness for i in bits(witness)), 'false independent witness')
    return witness, nodes


def field_plane():
    lines = [encode(4*x+y for y in range(4)) for x in range(4)]
    lines += [encode(4*x+(mul(m,x)^c) for x in range(4))
              for m in range(4) for c in range(4)]
    plane_check(lines)
    return tuple(sorted(lines))


def normalization(plane):
    """Enumerate row permutations, all MOLS triples, and check explicit maps."""
    perm4 = list(it.permutations(range(4)))
    squares = []
    for tail in it.product(perm4, repeat=3):
        rows = (tuple(range(4)),)+tail
        if all(len({rows[r][c] for r in range(4)}) == 4 for c in range(4)):
            squares.append(tuple(v for row in rows for v in row))
    triples = [t for t in it.combinations(squares,3)
               if all(len(set(zip(a,b))) == 16 for a,b in it.combinations(t,2))]
    grid = [encode(4*r+c for c in range(4)) for r in range(4)]
    grid += [encode(4*r+c for r in range(4)) for c in range(4)]
    records = []
    for t in triples:
        design = tuple(sorted(grid+[encode(p for p in range(16) if s[p] == v)
                                    for s in t for v in range(4)]))
        plane_check(design)
        maps = []
        for rows,cols in it.product(perm4,repeat=2):
            g = tuple(4*rows[p//4]+cols[p%4] for p in range(16))
            if tuple(sorted(image(b,g) for b in design)) == plane:
                maps.append(g)
        require(maps, 'unnormalized grid plane')
        records.append({'plane':design,'map':min(maps),'map_count':len(maps)})
    require(len(squares)==24 and len(triples)==2, 'MOLS census mismatch')
    require(len({tuple(r['plane']) for r in records})==2, 'duplicate grid plane')
    return {'squares':len(squares),'triples':len(triples),'maps':records}


def symmetries(plane):
    """Parametrize images of an ordered noncollinear affine frame + conjugation."""
    found = set()
    for origin in range(16):
        ox,oy = divmod(origin,4)
        for u,v in it.permutations(range(1,16),2):
            ux,uy = divmod(u,4)
            vx,vy = divmod(v,4)
            if mul(ux,vy) == mul(uy,vx):
                continue
            for conjugate in range(2):
                g = []
                for p in range(16):
                    x,y = divmod(p,4)
                    if conjugate:
                        x,y = mul(x,x),mul(y,y)
                    g.append(4*(ox^mul(ux,x)^mul(vx,y))
                             +(oy^mul(uy,x)^mul(vy,y)))
                require(sorted(g)==list(range(16)), 'non-bijective frame map')
                require(tuple(sorted(image(b,g) for b in plane))==plane,
                        'frame map does not preserve plane')
                found.add(tuple(g))
    require(len(found)==5760, 'frame symmetry count')
    return sorted(found)


def arc_partitions(arcs):
    """Join disjoint arc pairs across complementary eight-point masks.

    Each four-block partition appears three times, once per 2+2 split;
    require multiplicity exactly three instead of assuming no omissions.
    """
    pairs = defaultdict(list)
    for a,b in it.combinations(arcs,2):
        if not a & b:
            pairs[a|b].append((a,b))
    classes = Counter()
    for half, choices in pairs.items():
        if half & 1:
            for left in choices:
                for right in pairs.get(FULL ^ half, ()):
                    classes[tuple(sorted(left+right))] += 1
    require(all(v==3 for v in classes.values()), 'arc-class 2+2 multiplicity')
    return set(classes)


def orbit_cover(classes, group):
    remaining = set(classes)
    records = []
    while remaining:
        rep = min(remaining)
        orbit = {tuple(sorted(image(b,g) for b in rep)) for g in group}
        require(orbit <= remaining, 'overlapping or invalid class orbit')
        remaining -= orbit
        records.append({'first_class':rep,'size':len(orbit)})
    require(sum(r['size'] for r in records)==len(classes), 'incomplete orbit cover')
    return records


def completions(first, arcs):
    allowed = [b for b in arcs if all((b & a).bit_count() == 1 for a in first)]
    target = (1 << 120)-1
    for b in first:
        target ^= pair_mask(b)
    require(target.bit_count()==96, 'first-class pair target')
    covers,nodes = exact_cover([pair_mask(b) for b in allowed], target)
    designs = []
    for cover in covers:
        require(len(cover)==16, 'residual line count')
        design = tuple(sorted(first+tuple(allowed[j] for j in cover)))
        plane_check(design)
        designs.append(design)
    return sorted(designs), len(allowed), nodes


def normalize_arbitrary(design, normal, plane):
    """Explicitly map any generated second plane to the first plane."""
    plane_check(design)
    classes = sorted({tuple(sorted(a for a in design if a == b or not a & b))
                      for b in design})
    require(len(classes)==5 and all(len(c)==4 for c in classes), 'parallel classes')
    require(all(sum(c)==FULL and len(set(c))==4
                and all(not a & b for a,b in it.combinations(c,2)) for c in classes),
            'parallel cover')
    rows,cols = classes[:2]
    intersections = [r & c for r in rows for c in cols]
    require(all(a.bit_count()==1 for a in intersections), 'affine grid intersection')
    coordinate = {next(bits(a)):i for i,a in enumerate(intersections)}
    require(len(coordinate)==16, 'affine grid bijection')
    pulled = tuple(sorted(encode(coordinate[p] for p in bits(b)) for b in design))
    match = [r for r in normal['maps'] if tuple(r['plane'])==pulled]
    require(len(match)==1, 'general normalization grid missing')
    g = tuple(match[0]['map'][coordinate[p]] for p in range(16))
    require(tuple(sorted(image(b,g) for b in design))==plane, 'general plane transport')
    return g


def controls():
    cover_tests = 0
    # All subsets of nonempty columns on at most three rows, not just samples.
    for width in range(4):
        columns = list(range(1,1 << width))
        for selection in range(1 << len(columns)):
            rows = [r for i,r in enumerate(columns) if selection >> i & 1]
            brute = []
            for chosen in range(1 << len(rows)):
                union = 0
                good = True
                for j in bits(chosen):
                    if union & rows[j]:
                        good = False
                    union |= rows[j]
                if good and union == (1 << width)-1:
                    brute.append(tuple(bits(chosen)))
            got,_ = exact_cover(rows, (1 << width)-1)
            require(got==sorted(brute), 'small exact-cover disagreement')
            cover_tests += 1
    graph_tests = 0
    for n in range(6):
        es = list(it.combinations(range(n),2))
        for mask in range(1 << len(es)):
            adj = [0]*n
            for j,(u,v) in enumerate(es):
                if mask >> j & 1:
                    adj[u] |= 1 << v
                    adj[v] |= 1 << u
            got,_ = independence(adj)
            want = max((s.bit_count() for s in range(1 << n)
                        if all(not adj[i] & s for i in bits(s))), default=0)
            require(got.bit_count()==want, 'small independent-set disagreement')
            graph_tests += 1
    negatives = [lambda:exact_cover([1,1],1),lambda:exact_cover([0],1),
                 lambda:exact_cover([2],1),lambda:independence([1]),
                 lambda:independence([2,0]),lambda:plane_check([15]*20),
                 lambda:exact_cover([1],1,cap=0),lambda:independence([],cap=0)]
    caught = 0
    for f in negatives:
        try:
            f()
        except (ValueError,RuntimeError):
            caught += 1
    require(caught==len(negatives), 'negative control accepted')
    return {'all_exact_cover_systems_through_three_rows':cover_tests,
            'all_simple_graphs_through_five_vertices':graph_tests,
            'rejected_bad_inputs_or_zero_caps':caught}


def run(progress=None, pilot=None):
    control = controls()
    plane = field_plane()
    normal = normalization(plane)
    group = symmetries(plane)
    arcs = {k:[encode(c) for c in it.combinations(range(16),k)
                if all((encode(c)&b).bit_count()<=2 for b in plane)] for k in [4,5]}
    classes = arc_partitions(arcs[4])
    orbits = orbit_cover(classes,group)
    require(len(classes)==119880 and len(orbits)==38, 'class census mismatch')
    designs = set()
    cover_rows = []
    for index,r in enumerate(orbits):
        qs,allowed,nodes = completions(r['first_class'],arcs[4])
        designs.update(qs)
        cover_rows.append({**r,'index':index,'allowed_lines':allowed,
                           'cover_nodes':nodes,'planes':qs})
        if progress:
            Path(progress).write_text(json.dumps({'status':'INCOMPLETE','done':index+1,
                'nodes':sum(x['cover_nodes'] for x in cover_rows),'rows':cover_rows},indent=2)+'\n')
        if pilot and index+1 == pilot:
            return {'status':'INCOMPLETE PILOT','rows':cover_rows}
    cases = []
    for q in sorted(designs):
        # Full 4368-subset enumeration, no source first-plane arc fixture.
        common = [encode(c) for c in it.combinations(range(16),5)
                  if all((encode(c)&b).bit_count()<=2 for b in plane+q)]
        conflict = [encode(j for j,b in enumerate(common) if j!=i and (a&b).bit_count()>2)
                    for i,a in enumerate(common)]
        witness,nodes = independence(conflict)
        chosen = [common[j] for j in bits(witness)]
        words = sorted([b|(1 << 16) for b in plane]+[b|(1 << 17) for b in q]+chosen)
        require(len(words)==len(set(words)), 'duplicate packing word')
        require(all(0<=w<(1<<18) and w.bit_count()==5 for w in words), 'packing word mask')
        require(all((a&b).bit_count()<=2 for a,b in it.combinations(words,2)),
                'invalid direct packing witness')
        cases.append({'second_plane':q,'common_five_arcs':common,
                      'maximum':len(chosen),'attaining_words':chosen,
                      'independence_nodes':nodes,
                      'degrees':[sum(w >> p & 1 for w in words) for p in range(18)]})
    # Bounded strengthening: classify the attaining restricted configurations.
    high = {tuple(c['second_plane']) for c in cases if c['maximum']==16}
    require(all(len(c['common_five_arcs'])==16 and c['degrees']==[15]*16+[20,20]
                for c in cases if c['maximum']==16), 'attaining-case rigidity failure')
    left = set(high)
    attaining_orbits = []
    full_orbits = []
    while left:
        rep = min(left)
        orbit = {tuple(sorted(image(b,g) for b in rep)) for g in group}
        covered = orbit & left
        require(rep in covered, 'attaining orbit misses representative')
        left -= covered
        attaining_orbits.append({'representative':rep,'full_labeled_plane_orbit_size':len(orbit),
                                'covered_normalized_planes':len(covered)})
        full_orbits.append(orbit)
    # Interchange the two distinguished coordinates, then normalize the new
    # first plane. Compare full orbit membership, including full word transport.
    swap_targets = []
    for r in attaining_orbits:
        q = r['representative']
        g = normalize_arbitrary(q, normal, plane)
        second = tuple(sorted(image(b,g) for b in plane))
        targets = [i for i,orbit in enumerate(full_orbits) if second in orbit]
        require(len(targets)==1, 'center swap misses attaining orbit')
        swap_targets.append(targets[0])
        old_arcs = [a for a in arcs[5] if all((a&b).bit_count()<=2 for b in q)]
        new_arcs = [a for a in arcs[5] if all((a&b).bit_count()<=2 for b in second)]
        old = [b|(1<<16) for b in plane]+[b|(1<<17) for b in q]+old_arcs
        new = [b|(1<<16) for b in plane]+[b|(1<<17) for b in second]+new_arcs
        extended = g+(17,16)
        require(sorted(image(b,extended) for b in old)==sorted(new), 'full center-swap transport')
    require(all(swap_targets[swap_targets[i]]==i for i in range(len(swap_targets))),
            'center-swap involution')
    unordered_types = len({tuple(sorted((i,j))) for i,j in enumerate(swap_targets)})
    for i,r in enumerate(attaining_orbits):
        require(5760 % r['full_labeled_plane_orbit_size']==0, 'orbit-stabilizer divisibility')
        r['ordered_center_stabilizer'] = 5760 // r['full_labeled_plane_orbit_size']
        r['full_code_automorphism_order'] = r['ordered_center_stabilizer'] * (2 if swap_targets[i]==i else 1)
    return {'status':'COMPLETE','agent':'six-reviewer-1','role':'independent mathematical reviewer',
            'controls':control,'normalization':normal,'plane':plane,'symmetries':len(group),
            'arc_counts':{k:len(v) for k,v in arcs.items()},'partitions':len(classes),
            'cover_rows':cover_rows,'cases':cases,
            'common_arc_histogram':dict(Counter(len(c['common_five_arcs']) for c in cases)),
            'residual_maximum_histogram':dict(Counter(c['maximum'] for c in cases)),
            'maximum_common_arcs':max(len(c['common_five_arcs']) for c in cases),
            'maximum_residual':max(c['maximum'] for c in cases),
            'restricted_maximum':40+max(c['maximum'] for c in cases),
            'attaining_configuration_orbits':attaining_orbits,
            'ordered_center_swap':swap_targets,
            'unordered_attaining_configuration_types':unordered_types}


def compare_author(result, path):
    d = json.loads(Path(path).read_text())
    # Independent entry-wise comparison, not author data used to enumerate.
    ours = {tuple(c['second_plane']):(tuple(c['common_five_arcs']),c['maximum'])
            for c in result['cases']}
    theirs = {tuple(c['second_plane']):(tuple(c['common_five_arcs']),c['maximum'])
              for c in d['cases']}
    require(ours == theirs, 'author full plane/arc/maximum comparison')
    require([(tuple(r['first_class']),r['size']) for r in result['cover_rows']]
            == [(tuple(r['representative']),r['size']) for r in d['first_class_orbits']],
            'author class-orbit comparison')
    require([len(r['planes']) for r in result['cover_rows']]
            == [r['compatible_planes'] for r in d['rows']], 'author per-branch plane comparison')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--check',type=Path)
    parser.add_argument('--compare-author',type=Path)
    parser.add_argument('--progress',type=Path)
    parser.add_argument('--pilot',type=int,choices=range(1,39))
    args = parser.parse_args()
    started = time.monotonic()
    result = run(args.progress,args.pilot)
    if args.compare_author:
        require(not args.pilot,'cannot compare incomplete pilot')
        compare_author(result,args.compare_author)
    payload = json.dumps(result,sort_keys=True,separators=(',',':'))+'\n'
    if args.check:
        require(not args.pilot,'cannot certify incomplete pilot')
        require(json.loads(payload)==json.loads(args.check.read_text()), 'full independent manifest mismatch')
    if args.output:
        args.output.write_text(payload)
    print(json.dumps({'status':result['status'],'seconds':time.monotonic()-started,
        'rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'sha256':hashlib.sha256(payload.encode()).hexdigest(),
        'planes':len(result.get('cases',[])),
        'total_cover_nodes':sum(r['cover_nodes'] for r in result.get('cover_rows',result.get('rows',[]))),
        'attaining_orbits':result.get('attaining_configuration_orbits')}))


if __name__ == '__main__':
    main()
