#!/usr/bin/env python3
"""Solver-free closure of every at-most508 subgraph of exact H517.

Public proof: recheck all positive witnesses, then directly cover all
binomial(21,9) omission sets left by 496 singleton witnesses. The earlier
39,453-case census is not a premise of this public closure check.
"""
import argparse
from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from math import comb
from pathlib import Path
import resource
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parent


def require(ok,message):
    if not ok: raise ValueError(message)


def load(path): return json.loads(path.read_text())


def module(name,path):
    spec = importlib.util.spec_from_file_location(name,path)
    result = importlib.util.module_from_spec(spec); spec.loader.exec_module(result); return result


def check(row,edges):
    c,D = row['colouring'],row['D']
    require(len(c) == 517 and set(c) <= set('.0123'), 'full colouring domain')
    require(D and D == [i for i,x in enumerate(c) if x == '.'], 'exact nonempty omissions')
    require(all(c[u] == '.' or c[v] == '.' or c[u] != c[v] for u,v in edges), 'unit edge inequality')
    return sum(c[u] != '.' and c[v] != '.' for u,v in edges)


def controls(row,edges):
    c = row['colouring']; u,v = next((u,v) for u,v in edges if c[u] != '.' and c[v] != '.')
    bad = c[:v]+c[u]+c[v+1:]
    for mutation in [dict(D=row['D'],colouring=bad),dict(D=[],colouring=c)]:
        try: check(mutation,edges)
        except ValueError: pass
        else: raise ValueError('malformed witness control was accepted')
    return 2


def verify(work=None):
    start = time.monotonic()
    for name,digest in load(HERE/'manifest.json').items():
        require(sha256((REPO/name).read_bytes()).hexdigest() == digest, ('input hash',name))
    R = module('reviewed_geometry_and_witnesses',REPO/'hadwiger_nelson_heule517_large4_review1/independent_check.py')
    old,labels,points,edges,L,S,edge_hash = R.reconstruct_graph(REPO)
    groups = R.witness_data(REPO,old,labels,L,S); inherited = R.verify_witnesses(groups,edges)
    old_cuts = {frozenset(row['D']) for rows in groups.values() for row,c in rows}
    new = load(HERE/'certificate.json')['rows']
    require(len(new) == 8 and len({r['native_index'] for r in new}) == 8, 'public row count and provenance')
    new_checks = sum(check(row,edges) for row in new); control_count = controls(new[0],edges)
    require(all(not set(a['D']) <= set(b['D']) for i,a in enumerate(new) for j,b in enumerate(new) if i != j), 'new antichain')
    all_cuts = old_cuts | {frozenset(row['D']) for row in new}
    minimal = {d for d in all_cuts if not any(e < d for e in all_cuts)}
    forced = set().union(*(d for d in minimal if len(d) == 1)); free = sorted(set(range(517))-forced)
    nonsingleton = sorted((d for d in minimal if len(d) > 1),key=lambda d:(len(d),sorted(d)))
    require((len(forced),len(forced & L),len(forced & S),len(free),len(minimal),len(nonsingleton)) == (496,367,129,21,538,42), 'combined forcing and antichain')
    require(all(d <= set(free) for d in nonsingleton), 'non-singleton support')
    cover_start = time.monotonic(); tested = 0
    for omitted in combinations(free,9):
        tested += 1; omitted = set(omitted)
        require(any(d <= omitted for d in nonsingleton), ('uncovered nine-subset',sorted(omitted)))
    require(tested == comb(21,9) == 293930, 'complete final cover')
    cover_seconds = time.monotonic()-cover_start
    native_count = native_checks = old_frontier_count = 0
    if work:
        # A separate recursion regenerates the OLD frontier for the optional
        # discovery audit. It is unnecessary for the direct final cover above.
        C = module('old_frontier_recursion',REPO/'hadwiger_nelson_heule517_whole_cover/verify.py')
        old_forced = set().union(*(d for d in old_cuts if len(d) == 1))
        old_free = tuple(sorted(set(range(517))-old_forced))
        old_nontrivial = {d for d in old_cuts if not d & old_forced}
        old_nontrivial = {d for d in old_nontrivial if not any(e < d for e in old_nontrivial)}
        frontier = list(C.independent_sets(old_free,old_nontrivial,9))
        old_frontier_count = len(frontier)
        raw = ''.join(','.join(map(str,t))+'\n' for t in frontier).encode('ascii')
        expected = load(REPO/'hadwiger_nelson_heule517_whole_cover/result.json')
        require(len(frontier) == expected['residual'] == 39453 and sha256(raw).hexdigest() == expected['frontier_sha256'], 'regenerated old frontier')
        buckets = {i:[] for i in range(5,10)}
        for t in frontier: buckets[len(set(t)&L)].append(t)
        require(load(work/'initial_counts.json') == {str(i):len(ts) for i,ts in buckets.items()}, 'initial bucket census')
        native = load(work/'native_witnesses.json'); native_count = len(native)
        native_checks = sum(check(row,edges) for row in native)
        require(native_count == 16 and all(any(set(r['D']) <= set(n['D']) for r in new) for n in native), 'native witness subsumption')
        for row in new:
            source = native[row['native_index']]
            require(row['D'] == source['D'] and row['colouring'] == source['colouring'], 'retained public row')
        result = load(work/'result.json'); history = result['history']; cursor = 5; remaining = len(frontier)
        require(result['status'] == 'WHOLE_H517_FAMILY_CLOSED' and result['proof'] is None and result['target'] is None, 'native closure status')
        require(len(history) == native_count == result['queries'] == result['positives'] <= 256, 'native query count')
        for turn,(record,row) in enumerate(zip(history,native)):
            while not buckets[cursor]: cursor = 5 if cursor == 9 else cursor+1
            bucket = cursor; O = buckets[bucket][0]; cursor = 5 if cursor == 9 else cursor+1
            require(record['turn'] == turn and record['bucket'] == bucket and record['omitted'] == list(O) and record['answer'] is True, 'round-robin query')
            require(set(row['D']) <= set(O) and row['D'] == record['D'], 'witness covers queried graph')
            for i in buckets: buckets[i] = [t for t in buckets[i] if not set(row['D']) <= set(t)]
            current = sum(map(len,buckets.values()))
            require(record['remaining'] == current and record['removed'] == remaining-current and record['remaining_by_large'] == {str(i):len(ts) for i,ts in buckets.items()}, 'every pruning step')
            remaining = current
        require(remaining == result['remaining_candidates'] == 0 and (work/'frontier.txt').read_bytes() == b'', 'empty final frontier')
        clauses = [[-2069-v]+[4*v+c+1 for c in range(4)] for v in range(517)]
        clauses.extend([-(4*u+c+1),-(4*v+c+1)] for u,v in edges for c in range(4)); clauses.append([-2069,1])
        cnf = ('p cnf 2585 '+str(len(clauses))+'\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode('ascii')
        require((work/'activation.cnf').read_bytes() == cnf and sha256(cnf).hexdigest() == result['activation_sha256'], 'actual full activation CNF')
    return dict(status='EVERY AT-MOST508 SUBGRAPH OF H517 IS FOUR-COLOURABLE',
                fixed_support_closed=True,record_improvement=False,unrestricted_at_most508_family_closed=True,
                exact_pair_checks=comb(517,2),unit_edges=len(edges),edge_stream_sha256=edge_hash,
                inherited_colourings=955,inherited_edge_checks=sum(v['retained_edge_checks'] for v in inherited.values() if isinstance(v,dict)),
                new_colourings=len(new),new_edge_checks=new_checks,final_antichain=len(minimal),
                forced_vertices=len(forced),forced_large=len(forced & L),forced_small=len(forced & S),
                free_vertices=free,non_singleton_cuts=len(nonsingleton),nine_sets_checked=tested,uncovered_nine_sets=0,
                old_family_theorem_required=False,old_census_theorem_required=False,
                witness_rejection_controls=control_count,old_frontier_regenerated=old_frontier_count,
                native_colourings_checked=native_count,native_edge_checks=native_checks,
                actual_cnf_and_transcript_checked=bool(work),negative_solver_proof_required=False,native_solver_used_by_checker=False,
                direct_cover_seconds=cover_seconds,seconds=time.monotonic()-start,
                peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--work',type=Path); parser.add_argument('--report',type=Path)
    args = parser.parse_args(); result = verify(args.work)
    if args.report: args.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))
