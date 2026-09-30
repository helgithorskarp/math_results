#!/usr/bin/env python3
"""Independent replay by a B-parallel class and residual pair cover."""

import argparse
from itertools import combinations, permutations
from collections import Counter
from pathlib import Path
import hashlib
import json
import time

HERE = Path(__file__).resolve().parent


def need(condition, message):
    if not condition:
        raise ValueError(message)


def mask(points):
    return sum(1 << x for x in points)


def plane_by_permutations():
    lines = [mask(4*x+y for y in range(4)) for x in range(4)]
    lines += [mask(4*x+y for x in range(4)) for y in range(4)]
    for p in permutations(range(4)):
        inversions = sum(p[i] > p[j] for i in range(4) for j in range(i+1,4))
        if inversions % 2 == 0:
            lines.append(mask(4*x+p[x] for x in range(4)))
    need(len(lines)==len(set(lines))==20, 'bad A4 plane')
    for x,y in combinations(range(16),2):
        need(sum((line>>x&1) and (line>>y&1) for line in lines)==1,
             'A4 plane does not cover a pair once')
    return lines


def run_case(chosen, seconds=15, node_limit=200000, compare_primary=False):
    a,b,z,u,c = 16,0,17,11,14
    axes = [mask([0,1,2,3]),mask([0,4,8,12])]
    words = [((line ^ 1) | (1<<a) | (1<<z)) if line in axes
             else line | (1<<z) for line in plane_by_permutations()]
    need(all(w.bit_count()==5 for w in words), 'wrong star words')
    leftover = sorted({2,3,8,12}-set(chosen))
    # Remaining rows are pairs among the sixteen points after the two z-quads.
    missing = {tuple(sorted(e)) for e in [(u,c),(u,1),(u,4),
                (c,chosen[0]),(c,chosen[1]),tuple(leftover)]}
    fixed_pairs = {p for axis in [(1,2,3),(4,8,12)] for p in combinations(axis,2)}
    if missing & fixed_pairs:
        if compare_primary:
            from check_support16 import case_instance
            ref = case_instance(chosen)
            need(set(ref['conflict']) == missing & fixed_pairs, 'fixed-conflict mismatch')
        return {'status':'FIXED_BLOCK_LEAVE_CONFLICT','case':list(chosen),
                'conflicting_pairs':sorted(map(list,missing & fixed_pairs))}
    rows = set(combinations(range(16),2))-missing-fixed_pairs
    columns = []
    edges = []
    for quad in combinations(range(16),4):
        pairs = frozenset(combinations(quad,2))
        if not pairs <= rows:
            continue
        word = mask(quad) | (1<<a)
        if any((word ^ other).bit_count() < 6 for other in words):
            continue
        columns.append(quad)
        edges.append(pairs)
    need(len(rows)==108, 'wrong remaining edge count')
    if compare_primary:
        from check_support16 import case_instance
        ref = case_instance(chosen)
        need(set(ref['rows']) == rows, 'full pair-row universe mismatch')
        need(ref['columns'] == columns, 'entry-level candidate universe mismatch')
    result = cover_by_parallel_class(rows,columns,seconds,node_limit)
    result['case'] = list(chosen)
    return result


def cover_by_parallel_class(rows,columns,seconds=15,node_limit=200000):
    b=0
    edges = [frozenset(combinations(q,2)) for q in columns]
    b_columns = [i for i,q in enumerate(columns) if b in q]
    ordinary = frozenset(i for i,q in enumerate(columns) if b not in q)
    covered_points = frozenset(y for x,y in rows if x==0)
    need(len(covered_points)==15,'B must cover exactly fifteen points')
    by_point = {p:[] for p in covered_points}
    b_triples = {}
    for i in b_columns:
        triple = frozenset(columns[i])-{b}
        b_triples[i] = triple
        for p in triple:
            by_point[p].append(i)
    row_options = {p:frozenset(i for i in ordinary if p in edges[i]) for p in rows}
    conflicts = {i:frozenset(j for j in ordinary if edges[i]&edges[j])
                 for i in ordinary}
    nodes = 0
    b_states = 0
    partitions = 0
    queries = 0
    leaf_hash = hashlib.sha256()
    start = time.monotonic()

    def budget():
        nonlocal nodes
        nodes += 1
        if nodes>node_limit or (nodes%128==0 and time.monotonic()-start>seconds):
            raise TimeoutError('INCOMPLETE')

    def residual(remaining, available):
        budget()
        if not remaining:
            return []
        options = None
        for p in sorted(remaining):
            here = row_options[p] & available
            if not here:
                return None
            if options is None or len(here)<len(options):
                options = here
        for i in sorted(options):
            need(edges[i] <= remaining, 'replay available column covers a used edge')
            result = residual(remaining-edges[i],available-conflicts[i])
            if result is not None:
                return [i]+result
        return None

    def parallel_class(remaining, chosen_columns, used_edges):
        nonlocal b_states,partitions,queries
        budget()
        b_states += 1
        if not remaining:
            need(len(chosen_columns)==5 and len(used_edges)==30, 'bad B parallel class')
            partitions += 1
            available = frozenset(i for i in ordinary if not (edges[i]&used_edges))
            queries += 1
            result = residual(frozenset(rows)-used_edges,available)
            leaf_hash.update((','.join(map(str,chosen_columns))+'\n').encode())
            return chosen_columns+result if result is not None else None
        first = min(remaining)
        for i in by_point[first]:
            if b_triples[i] <= remaining:
                need(not (edges[i]&used_edges), 'B parallel class repeats an edge')
                result = parallel_class(remaining-b_triples[i],chosen_columns+[i],
                                        used_edges | edges[i])
                if result is not None:
                    return result
        return None

    try:
        solution = parallel_class(covered_points,[],frozenset())
        status = 'WITNESS' if solution is not None else 'COMPLETE_NO_COVER'
    except TimeoutError:
        status,solution = 'INCOMPLETE',None
    report = {'status':status,'candidate_quads':len(columns),
              'B_quads':len(b_columns),'B_partition_states':b_states,
              'B_parallel_classes':partitions,'residual_queries':queries,'nodes':nodes,
              'class_stream_sha256':leaf_hash.hexdigest(),
              'candidate_quads_sha256':hashlib.sha256(
                  (json.dumps(columns,separators=(',',':'))+'\n').encode()).hexdigest(),
              'complete_negative':status=='COMPLETE_NO_COVER'}
    if solution is not None:
        all_edges = Counter(p for i in solution for p in edges[i])
        need(set(all_edges)==rows and set(all_edges.values())=={1},'replay witness invalid')
        report['quadruples']=[columns[i] for i in solution]
    return report


def positive_controls():
    cases = []
    rows = set(combinations(range(16),2))
    columns = list(combinations(range(16),4))
    result = cover_by_parallel_class(rows,columns)
    need(result['status']=='WITNESS' and len(result['quadruples'])==20,
         'parallel-class replay rejects known affine-plane positive fixture')
    cases.append({'fixture':'affine_plane_unused_point','quadruples':20,
                  'nodes':result['nodes']})
    blocks = [frozenset(i for i,b in enumerate(word) if b=='1')
              for word in (HERE/'baseline69.txt').read_text().splitlines()]
    star = [word-{0} for word in blocks if 0 in word]
    need(len(star)==20,'wrong actual incumbent star')
    b = next(y for y in range(1,18) if sum(y in q for q in star)==5)
    neighbors = sorted({y for q in star if b in q for y in q-{b}})
    need(len(neighbors)==15,'wrong actual B neighbors')
    last = (set(range(1,18))-{b}-set(neighbors)).pop()
    labels = {b:0,last:16,**{y:i+1 for i,y in enumerate(neighbors)}}
    quads = [tuple(sorted(labels[y] for y in q)) for q in star]
    counts = Counter(pair for quad in quads for pair in combinations(quad,2))
    need(len(counts)==120 and set(counts.values())=={1},'actual positive fixture invalid')
    rows = set(counts)
    columns = [q for q in combinations(range(17),4) if set(combinations(q,2))<=rows]
    result = cover_by_parallel_class(rows,columns)
    need(result['status']=='WITNESS' and len(result['quadruples'])==20,
         'parallel-class replay rejects actual incumbent positive fixture')
    cases.append({'fixture':'actual_incumbent_point_0','quadruples':20,
                  'nodes':result['nodes']})
    return cases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-expected',action='store_true')
    parser.add_argument('--compare-primary',action='store_true',
                        help='compare every independently generated row and column')
    args = parser.parse_args()
    results = []
    for chosen in combinations([2,3,8,12],2):
        result = run_case(chosen,compare_primary=args.compare_primary)
        need(result['status'] in ['COMPLETE_NO_COVER','FIXED_BLOCK_LEAVE_CONFLICT'],
             'Obstruction not verified: '+result['status'])
        results.append(result)
    report = {'cases':results,'weighted_cases_covered':6,
              'positive_controls':positive_controls(),
              'B_parallel_classes_exhausted':sum(r.get('B_parallel_classes',0) for r in results),
              'global_72_word_exclusion':False,'theorem_depends_on_computation':True,
              'independent_peer_review':False}
    path = HERE/'support16_expected.json'
    if args.write_expected:
        expected = json.loads(path.read_text()) if path.exists() else {}
        expected['replay'] = report
        path.write_text(json.dumps(expected,indent=2,sort_keys=True)+'\n')
    else:
        need(json.loads(path.read_text())['replay']==report,'replay expected report differs')
    print(json.dumps(report,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
