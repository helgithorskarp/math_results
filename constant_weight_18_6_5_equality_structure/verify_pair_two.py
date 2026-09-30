#!/usr/bin/env python3
"""Rebuild the carrier by point partitions and replay literal no-cover trees.

The rebuild uses neither the primary group-closure generator nor its
bitset search. The ordinary coverage bridges are in NO_DEFICIT_THREE.md.
This is same-author verification, not independent peer review.
"""
import argparse
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from math import factorial
from pathlib import Path

HERE = Path(__file__).resolve().parent
A, B, V, U = 14, 15, 16, 17
O = frozenset(range(8))
IDENTITY = tuple(range(18))


def need(condition, message):
    if not condition:
        raise ValueError(message)


def encode(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'))+'\n').encode('ascii')


def edges(q):
    return frozenset(combinations(sorted(q), 2))


def transport(family, p):
    return tuple(sorted(tuple(sorted(p[x] for x in q)) for q in family))


def first_cases():
    result = []
    coverage = []
    for kind in ('middle', 'end', 'triangle'):
        if kind == 'middle':
            high = ((V,A),(V,B))
            leaves = ((V,tuple(range(8))), (A,(8,9,10)), (B,(11,12,13)))
            groups = ((8,9,10),(11,12,13))
            extra = ()
        elif kind == 'end':
            high = ((V,A),(A,B))
            leaves = ((V,tuple(range(9))), (A,(9,10)), (B,(11,12,13)))
            groups = ((9,10),(11,12,13))
            extra = ()
        else:
            high = ((V,A),(V,B),(A,B))
            leaves = ((V,tuple(range(8))), (A,(8,9)), (B,(10,11)))
            groups = ((8,9),(10,11),(12,13))
            extra = ((12,13),)
        leave = {tuple(sorted(e)) for e in high+extra}
        leave.update(tuple(sorted((x,y))) for x,ys in leaves for y in ys)
        degree = Counter(x for e in leave for x in e)
        need(len(leave) == 16 and all(degree[x] ==
             (10 if x == V else 4 if x in (A,B) else 1) for x in range(17)),
             'wrong first leave degrees')
        maps = set()
        for choices in product(*(permutations(g) for g in groups)):
            p = list(IDENTITY)
            for group, choice in zip(groups, choices):
                for x,y in zip(group,choice):
                    p[x] = y
            maps.add(tuple(p))
            if kind != 'end':
                swap = {A:B,B:A,**dict(zip(groups[0],groups[1])),
                        **dict(zip(groups[1],groups[0]))}
                maps.add(tuple(swap.get(y,y) for y in p))
        for p in maps:
            need(len(set(p)) == 18 and transport(leave,p) == tuple(sorted(leave)),
                 'tail map is not an actual leave permutation')
        available = tuple(x for x in range(16) if tuple(sorted((V,x))) not in leave)
        raw = {tuple(sorted((t,tuple(x for x in available if x not in t))))
               for t in combinations(available,3)}
        need(len(raw) == 10, 'wrong six-point partition universe')
        valid = {part for part in raw if all(not (edges(t)&leave) for t in part)}
        todo = set(valid)
        count = 0
        while todo:
            rep = min(todo)
            orbit = {transport(rep,p) for p in maps}
            need(orbit <= todo, 'first tail orbit does not partition its domain')
            todo -= orbit
            count += 1
            fixed = tuple(tuple(sorted(t+(V,))) for t in rep)
            result.append({'index':len(result),'kind':kind,'leave':leave,
                           'representative':rep,'fixed':fixed,
                           'small_maps':tuple(sorted(p for p in maps if p[A] == A and p[B] == B
                                                       and transport(rep,p) == rep))})
        coverage.append([len(valid),len(maps),count])
    need(coverage == [[10,72,2],[1,12,1],[6,16,2]], 'five-case carrier mismatch')
    need([c['representative'] for c in result] == [
        ((8,9,10),(11,12,13)), ((8,9,11),(10,12,13)),
        ((9,10,15),(11,12,13)), ((8,9,12),(10,11,13)),
        ((8,10,12),(9,11,13))], 'first representatives disagree')
    return result


def point_partitions(points, allowed):
    """All allowed triple partitions, branching on the largest free point."""
    points = frozenset(points)
    if not points:
        yield ()
        return
    pivot = max(points)
    for pair in combinations(sorted(points-{pivot}),2):
        triple = tuple(sorted(pair+(pivot,)))
        if triple not in allowed:
            continue
        for rest in point_partitions(points-frozenset(triple),allowed):
            yield tuple(sorted((triple,)+rest))


def a_types(case):
    neighbors = set(range(16))-{A}
    neighbors -= {y if x == A else x for x,y in case['leave'] if A in (x,y)}
    need(len(neighbors) == 12 and O <= neighbors, 'wrong A neighbors')
    special = neighbors-O
    used = set().union(*(edges(q) for q in case['fixed']))
    allowed_pairs = edges(range(17))-case['leave']-used
    allowed = {t for t in combinations(sorted(neighbors),3) if edges((A,)+t) <= allowed_pairs}
    histogram = Counter()
    compatible = set(point_partitions(neighbors,allowed))
    for part in compatible:
        pattern = tuple(sorted(tuple(x for x in t if x in special) for t in part))
        histogram[pattern] += 1
    need(len(compatible) == (8120 if case['index'] == 4 else 5880), 'wrong direct A domain')
    need(len(histogram) == (5 if case['index'] == 4 else 3), 'wrong special pattern domain')
    todo = set(histogram)
    records = []
    while todo:
        rep = min(todo)
        orbit = {transport(rep,p) for p in case['small_maps']}
        need(orbit <= todo, 'A pattern orbits overlap or leave the domain')
        todo -= orbit
        denominator = factorial(sum(not t for t in rep))
        for block in rep:
            denominator *= factorial(3-len(block))
        fillings = factorial(8)//denominator
        need(all(histogram[p] == fillings for p in orbit), 'A ordinary filling fibers disagree')
        offset = 0
        quads = []
        for t in rep:
            number = 3-len(t)
            quads.append(tuple(sorted((A,)+t+tuple(range(offset,offset+number)))))
            offset += number
        need(offset == 8, 'wrong canonical ordinary filling')
        records.append({'pattern':rep,'quads':tuple(sorted(quads))})
    checks = {'partitions_checked':factorial(12)//(factorial(4)*factorial(3)**4),
              'compatible_labeled_quartets':len(compatible),'special_patterns':len(histogram),
              'A_quartet_orbits':len(records)}
    return records,checks


def direct_stabilizer(case,a_record):
    """Enumerate maps by their four A-word images and ordinary bijections."""
    tails = [tuple(x for x in q if x != A) for q in a_record['quads']]
    special = [tuple(x for x in t if x not in O) for t in tails]
    ordinary = [tuple(x for x in t if x in O) for t in tails]
    group = set()
    for small in case['small_maps']:
        for word_images in permutations(range(4)):
            if any(tuple(sorted(small[x] for x in special[i])) != special[word_images[i]]
                   for i in range(4)):
                continue
            for choices in product(*(permutations(ordinary[j]) for j in word_images)):
                p = list(small)
                for i, choice in enumerate(choices):
                    for x,y in zip(ordinary[i],choice):
                        p[x] = y
                group.add(tuple(p))
    need(IDENTITY in group, 'stabilizer omits identity')
    for p in group:
        need(len(set(p)) == 18 and all(p[x] == x for x in (A,B,U,V)), 'not a fixed-anchor bijection')
        need(transport(case['leave'],p) == tuple(sorted(case['leave'])), 'stabilizer changes leave')
        need(transport(case['fixed'],p) == tuple(sorted(case['fixed'])), 'stabilizer changes shared words')
        need(transport(a_record['quads'],p) == a_record['quads'], 'stabilizer changes A words')
    need(all(tuple(p[q[x]] for x in range(18)) in group for p in group for q in group),
         'direct stabilizer is not closed')
    return tuple(sorted(group))


def rebuild(compare_primary=False):
    entries = []
    summaries = []
    for case in first_cases():
        if case['index'] not in (1,3,4):
            continue
        a_records,a_check = a_types(case)
        for ai,a_record in enumerate(a_records):
            prefix = tuple(sorted(case['fixed']+a_record['quads']))
            counts = Counter(e for q in prefix for e in edges(q))
            need(set(counts.values()) == {1}, 'prefix repeats a pair')
            rows = edges(range(17))-case['leave']-set(counts)
            free = {y if x == B else x for x,y in rows if B in (x,y)}
            fixed_b = sum(B in q for q in prefix)
            need(fixed_b == (1 if case['kind'] == 'middle' else 0), 'wrong fixed B count')
            need(len(free) == (9 if fixed_b else 12), 'wrong remaining B neighbors')
            allowed = {t for t in combinations(sorted(free),3) if edges((B,)+t) <= rows}
            groups = {tuple(sorted(tuple(sorted((B,)+t)) for t in part))
                      for part in point_partitions(free,allowed)}
            group = direct_stabilizer(case,a_record)
            todo = set(groups)
            bi = 0
            while todo:
                rep = min(todo)
                orbit = {transport(rep,p) for p in group}
                need(orbit <= todo, 'B group orbit leaves domain or overlaps another orbit')
                todo -= orbit
                fixed = tuple(sorted(prefix+rep))
                counts = Counter(e for q in fixed for e in edges(q))
                need(set(counts.values()) == {1}, 'fixed anchor groups repeat a pair')
                need(sum(A in q for q in fixed) == sum(B in q for q in fixed) == 4
                     and sum(V in q for q in fixed) == 2, 'wrong anchor replications')
                residual = tuple(sorted(edges(range(17))-case['leave']-set(counts)))
                need(len(residual) == (66 if fixed_b else 60), 'wrong residual size')
                # Directly inspect all 2,380 quadruples on seventeen points.
                residual_set = frozenset(residual)
                columns = tuple(q for q in combinations(range(17),4) if edges(q) <= residual_set)
                need(all(not (set(q)&{A,B,V}) for q in columns), 'residual column uses a saturated anchor')
                entries.append({'index':len(entries),'first_case':case['index'],
                                'a_case':ai,'b_case':bi,'orbit_size':len(orbit),
                                'fixed_quads':fixed,'rows':residual,'columns':columns,
                                'input_sha256':sha256(encode([residual,columns])).hexdigest()})
                bi += 1
            summaries.append({'first_case':case['index'],'a_case':ai,
                              'a_pattern':a_record['pattern'],'a_quads':a_record['quads'],
                              'A_coverage':a_check,
                              'B_coverage':{'partitions_checked':factorial(len(free))//
                                  (factorial(len(free)//3)*factorial(3)**(len(free)//3)),
                                  'compatible_labeled_B_groups':len(groups),
                                  'checked_A_stabilizer_size':len(group),'B_group_orbits':bi}})
    need(len(entries) == 198, 'rebuild did not cover all 198 residual cases')
    if compare_primary:
        from check_pair_two import generate,a_stabilizer,cases,anchor_a_patterns
        primary = generate()
        need(encode(summaries) == encode(primary['summary']), 'entrywise carrier summary mismatch')
        fields = ('index','first_case','a_case','b_case','orbit_size','fixed_quads','rows','columns','input_sha256')
        need(encode([{k:e[k] for k in fields} for e in entries]) ==
             encode([{k:e[k] for k in fields} for e in primary['cases']]), 'entrywise primary matrices mismatch')
        for case in cases():
            if case['index'] in (1,3,4):
                roots,_ = anchor_a_patterns(case)
                reference = next(c for c in first_cases() if c['index'] == case['index'])
                for root in roots:
                    need(a_stabilizer(case,root) == direct_stabilizer(reference,root),
                         'actual A stabilizer permutation sets disagree')
    return entries,summaries


def replay_tree(rows,columns,tree):
    """Every branch is checked literally against all compatible columns."""
    row_list = tuple(rows)
    column_edges = tuple(edges(q) for q in columns)
    need(len(set(row_list)) == len(row_list), 'duplicate input pair')
    need(all(len(e) == 6 and e <= set(row_list) for e in column_edges), 'malformed input column')
    nodes = 0

    def visit(left,node):
        nonlocal nodes
        nodes += 1
        need(bool(left), 'a complete cover cannot have a rejection certificate')
        need(type(node) is list and len(node) == 2, 'malformed tree node')
        pivot,branches = node
        need(type(pivot) is int and 0 <= pivot < len(row_list) and row_list[pivot] in left,
             'pivot is not an uncovered pair')
        need(type(branches) is list, 'malformed branch list')
        options = [i for i,e in enumerate(column_edges) if row_list[pivot] in e and e <= left]
        need(all(type(b) is list and len(b) == 2 and type(b[0]) is int for b in branches),
             'malformed branch')
        need([b[0] for b in branches] == options, 'omitted, extra, duplicate or reordered branch')
        for i,subtree in branches:
            visit(left-column_edges[i],subtree)

    visit(frozenset(row_list),tree)
    return nodes


def negative_controls(entries,certificate):
    rejected = 0

    def reject(fn):
        nonlocal rejected
        try:
            fn()
        except ValueError:
            rejected += 1
        else:
            raise ValueError('invalid rejection certificate accepted')

    first = next(i for i,c in enumerate(certificate['cases']) if c['tree'][1])
    bad = deepcopy(certificate['cases'][first]['tree'])
    bad[1].pop()
    reject(lambda: replay_tree(entries[first]['rows'],entries[first]['columns'],bad))
    bad = deepcopy(certificate['cases'][first]['tree'])
    bad[0] = len(entries[first]['rows'])
    reject(lambda: replay_tree(entries[first]['rows'],entries[first]['columns'],bad))
    bad = deepcopy(certificate['cases'][first]['tree'])
    bad[1].append(deepcopy(bad[1][0]))
    reject(lambda: replay_tree(entries[first]['rows'],entries[first]['columns'],bad))
    reject(lambda: replay_tree([],[],[0,[]]))
    reject(lambda: replay_tree([(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)],
                               [(0,1,2,3)],[0,[]]))
    return rejected


def positive_controls():
    # Rebuild the field plane as verticals plus the graphs of even permutations.
    lines = [tuple(range(4*x,4*x+4)) for x in range(4)]
    for p in permutations(range(4)):
        inversions = sum(p[i] > p[j] for i in range(4) for j in range(i+1,4))
        if inversions % 2 == 0:
            lines.append(tuple(4*x+p[x] for x in range(4)))
    lines += [tuple(4*x+y for x in range(4)) for y in range(4)]
    count = Counter(e for q in lines for e in edges(q))
    need(len(lines) == len(set(lines)) == 20 and len(count) == 120
         and set(count.values()) == {1}, 'even-permutation plane is invalid')
    labels = {0:A,4:B,1:8,2:9,3:10,5:11,6:12,7:13,
              **{x:x-8 for x in range(8,16)}}
    quads = [tuple(sorted(labels[x] for x in q)) for q in lines if q not in ((0,1,2,3),(4,5,6,7))]
    quads += [(8,9,10,V),(11,12,13,V)]
    leave = edges(range(17))-set().union(*(edges(q) for q in quads))
    need(len(quads) == 20 and len(leave) == 16 and
         all(len(set(x)&set(y)) <= 1 for x,y in combinations(quads,2)), 'positive split fixture invalid')
    fixed = tuple(q for q in quads if set(q)&{A,B,V})
    remaining = tuple(q for q in quads if not set(q)&{A,B,V})
    rows = edges(range(17))-leave-set().union(*(edges(q) for q in fixed))
    columns = tuple(q for q in combinations(range(17),4) if edges(q) <= rows)
    used = Counter(e for q in remaining for e in edges(q))
    need(len(fixed) == 9 and len(remaining) == 11 and len(rows) == 66
         and set(used) == rows and set(used.values()) == {1}
         and all(q in columns for q in remaining), 'positive residual exact cover rejected')
    # The primary kernel must also detect this exact positive cover and its guard.
    from check_pair_two import no_cover_tree,CoverFound
    try:
        no_cover_tree(tuple(sorted(rows)),columns)
    except CoverFound:
        pass
    else:
        raise ValueError('primary no-cover generator rejects a genuine positive cover')
    try:
        no_cover_tree(tuple(sorted(rows)),columns,node_limit=0)
    except RuntimeError as exc:
        need(str(exc).startswith('INCOMPLETE'), 'guard lost its incomplete status')
    else:
        raise ValueError('zero-node guard was ignored')
    return {'fixture':'pure_middle_even_permutation_plane','fixed_quads':9,
            'residual_quads':11,'residual_pairs':66,'positive_kernel_accepted':True,
            'zero_node_guard_incomplete':True}


def baseline_checks():
    words = [frozenset(i for i,c in enumerate(line) if c == '1')
             for line in (HERE/'baseline69.txt').read_text().splitlines()]
    need(len(words) == len(set(words)) == 69 and all(len(w) == 5 for w in words), 'invalid baseline words')
    need(all(len(x&y) <= 2 for x,y in combinations(words,2)), 'invalid baseline distance')
    replication = Counter(x for w in words for x in w)
    instances = []
    for u in range(18):
        if replication[u] != 20:
            continue
        for v in range(18):
            if v == u:
                continue
            shared = [w-{u,v} for w in words if {u,v} <= w]
            if len(shared) != 2:
                continue
            d = set(range(18))-{u,v}
            rest = [w-{u} for w in words if u in w and v not in w]
            leave = edges(d)-set().union(*(edges(q) for q in rest))
            cliques = [q for q in combinations(sorted(d),4) if edges(q) <= leave]
            completions = [(x,y) for x,y in combinations(cliques,2)
                           if not (edges(x)&edges(y)) and edges(x)|edges(y) == leave]
            need(len(leave) == 12 and len(completions) == 1, 'baseline pair-two completion failed')
            need(all(any(t <= set(q) for q in completions[0]) for t in shared), 'tail containment failed')
            instances.append({'u':u,'v':v,'other_replication':replication[v],
                              'completion':completions[0]})
    need(len(instances) == 7 and all(e['other_replication'] == 12 for e in instances),
         'baseline completion carrier changed')
    return {'valid_words':69,'oriented_replication20_pair2_cases':7,
            'all_have_unique_completion':True,'other_endpoint_replications':[12],
            'case_stream_sha256':sha256(encode(instances)).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compare-primary',action='store_true')
    parser.add_argument('--write-expected',action='store_true')
    args = parser.parse_args()
    entries,summaries = rebuild(args.compare_primary)
    raw = (HERE/'pair_two_certificate.json').read_bytes()
    certificate = json.loads(raw)
    need(certificate['schema'] == 'pair-two-completion-v1', 'unsupported certificate schema')
    need(encode(summaries) == encode(certificate['carrier_summary']), 'certificate carrier summary disagrees')
    need(len(certificate['cases']) == len(entries), 'certificate omits or adds a case')
    nodes = []
    for entry,cert in zip(entries,certificate['cases']):
        for key in ('index','first_case','a_case','b_case','orbit_size','fixed_quads','input_sha256'):
            need(encode(cert[key]) == encode(entry[key]), 'certificate input mismatch: '+key)
        nodes.append(replay_tree(entry['rows'],entry['columns'],cert['tree']))
    report = {'agent':'six-code-1','role':'researcher','status':'COMPLETE_LITERAL_REPLAY',
              'residual_cases':len(entries),'nodes':sum(nodes),'maximum_nodes_per_case':max(nodes),
              'direct_A_stabilizer_sizes':[s['B_coverage']['checked_A_stabilizer_size'] for s in summaries],
              'input_stream_sha256':sha256(encode([
                  [c['first_case'],c['a_case'],c['b_case'],c['fixed_quads'],c['rows'],c['columns']]
                  for c in entries])).hexdigest(),
              'certificate_sha256':sha256(raw).hexdigest(),
              'invalid_certificate_controls_rejected':negative_controls(entries,certificate),
              'positive_control':positive_controls(),'baseline':baseline_checks(),
              'global_72_word_exclusion':False,'independent_peer_review':False}
    path = HERE/'pair_two_expected.json'
    expected = json.loads(path.read_text())
    if args.write_expected:
        expected['replay'] = report
        path.write_text(json.dumps(expected,indent=2,sort_keys=True)+'\n')
    else:
        need(expected['replay'] == report, 'literal replay manifest differs')
    print(json.dumps(report,indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
