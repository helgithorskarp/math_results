#!/usr/bin/env python3
"""Exact witnesses plus a distinct, set-valued deletion/contraction audit.

No producer module, native solver or prior family enumeration is imported.
The pinned independently reviewed geometry/witness decoder is reused.
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


def require(ok, message):
    if not ok: raise ValueError(message)


def load(path): return json.loads(path.read_text())


def independent_sets(vertices, forbidden, size, counters=None):
    """Inclusion first gives lexicographic tuples. Forbidden sets are residuals.

    Excluding v discards constraints containing v; including v removes v from
    every constraint. An empty constraint rejects the entire remaining cube.
    """
    stats = counters if counters is not None else Counter()

    def visit(available, edges, chosen, needed):
        stats['nodes'] += 1
        if needed > len(available):
            stats['too_short'] += 1
            return
        if frozenset() in edges:
            stats['forbidden_cubes'] += 1
            stats['covered_rank_sets'] += comb(len(available),needed)
            return
        if needed == 0:
            yield chosen
            return
        if not edges:
            stats['free_cubes'] += 1
            for suffix in combinations(available,needed): yield chosen+suffix
            return
        v, tail = available[0], available[1:]
        yield from visit(tail,frozenset(d-{v} for d in edges),chosen+(v,),needed-1)
        yield from visit(tail,frozenset(d for d in edges if v not in d),chosen,needed)

    require(size >= 0 and tuple(sorted(set(vertices))) == vertices, 'enumeration domain')
    require(all(d <= set(vertices) for d in forbidden), 'forbidden support')
    yield from visit(vertices,frozenset(forbidden),(),size)


def controls():
    # Exhaust every hypergraph on a three-point ground set, at every rank.
    vertices = (0,1,2)
    possible = [frozenset(d) for size in range(4) for d in combinations(vertices,size)]
    tested = 0
    for family_bits in range(1 << len(possible)):
        forbidden = [d for i,d in enumerate(possible) if family_bits & (1 << i)]
        for size in range(4):
            expected = [d for d in combinations(vertices,size) if not any(e <= set(d) for e in forbidden)]
            stats = Counter(); actual = list(independent_sets(vertices,forbidden,size,stats))
            require(actual == expected, 'control entrywise enumeration')
            require(len(actual)+stats['covered_rank_sets'] == comb(3,size), 'control cube accounting')
            tested += 1
    return tested


def verify(work=None):
    start = time.monotonic()
    for name,digest in load(HERE/'manifest.json').items():
        require(sha256((REPO/name).read_bytes()).hexdigest() == digest, ('input hash',name))
    spec = importlib.util.spec_from_file_location('reviewed_h517', REPO/'hadwiger_nelson_heule517_large4_review1/independent_check.py')
    R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
    old, labels, points, edges, large, small, edge_hash = R.reconstruct_graph(REPO)
    groups = R.witness_data(REPO,old,labels,large,small)
    witness_report = R.verify_witnesses(groups,edges)
    require(witness_report['witness_stream_sha256'] == 'c247f7f293616b94360737612585d6182d84119934b9fffe22737439e52d7bf9', 'reviewed witness stream')
    recipes = {(name,i):row for name,rows in groups.items() for i,(row,_) in enumerate(rows)}
    unique = {frozenset(row['D']) for row in recipes.values()}
    minimal = {d for d in unique if not any(e < d for e in unique)}
    forced = set().union(*(d for d in minimal if len(d) == 1))
    free = tuple(sorted(set(range(517))-forced))
    remaining = {d for d in minimal if len(d) > 1}
    require((len(recipes),len(minimal),len(forced),len(free),len(remaining)) == (955,555,490,27,65), 'derived hypergraph counts')
    data = load(HERE/'hypergraph.json')
    require(data['published_rows'] == 955 and data['antichain_rows'] == 555, 'hypergraph row counts')
    require(data['forced_vertices'] == sorted(forced) and data['free_vertices'] == list(free), 'entrywise support')
    require(data['free_large'] == sorted(set(free) & large), 'geometric L membership')
    require(len(data['cuts']) == len(remaining) and {frozenset(r['D']) for r in data['cuts']} == remaining, 'entrywise minimal cuts')
    for row in data['cuts']:
        require(recipes[row['source'],row['index']]['D'] == row['D'], 'cut provenance')
    control_count = controls()
    expected = load(HERE/'result.json')
    stats = Counter(); stream = sha256(); histogram = Counter(); examples = []; count = byte_count = 0
    actual_file = (work/'frontier.txt').open('rb') if work else None
    t = time.monotonic()
    try:
        for omitted in independent_sets(free,remaining,9,stats):
            # Direct set check validates each emitted tuple independently of
            # residual-constraint propagation; the recursion proves completeness.
            require(not any(d <= set(omitted) for d in remaining), 'uncovered tuple')
            raw = (','.join(map(str,omitted))+'\n').encode('ascii')
            if actual_file: require(actual_file.readline() == raw, ('frontier entry',count))
            stream.update(raw); byte_count += len(raw); count += 1
            histogram[sum(v in large for v in omitted)] += 1
            if len(examples) < 3: examples.append(list(omitted))
        if actual_file: require(actual_file.read(1) == b'', 'frontier trailing data')
    finally:
        if actual_file: actual_file.close()
    require(count+stats['covered_rank_sets'] == comb(27,9), 'all rank-nine sets accounted for')
    result = dict(status='LIBRARY_COVER_COMPLETE' if not count else 'EXACT_LIBRARY_RESIDUAL',
                  record_improvement=False,unrestricted_at_most508_family_closed=(count == 0),
                  total_nine_sets=comb(27,9),covered=stats['covered_rank_sets'],residual=count,
                  residual_by_large_omissions={str(k):v for k,v in sorted(histogram.items())},
                  frontier_sha256=stream.hexdigest(),frontier_bytes=byte_count,
                  first_residuals=examples,new_colouring_queries=0)
    require(result == expected, 'complete expected census')
    if work:
        native = load(work/'result.json')
        require(all(native[k] == v for k,v in result.items()), 'producer census')
        require(load(work/'hypergraph.json') == data, 'producer hypergraph')
    return dict(status='VERIFIED_EXACT_LIBRARY_RESIDUAL' if count else 'VERIFIED_FAMILY_CLOSURE',
                census=result,exact_pair_checks=comb(517,2),unit_edges=len(edges),
                edge_stream_sha256=edge_hash,published_colourings=len(recipes),
                retained_edge_checks=sum(x['retained_edge_checks'] for x in witness_report.values() if isinstance(x,dict)),
                witness_stream_sha256=witness_report['witness_stream_sha256'],
                forced_large=len(forced & large),forced_small=len(forced & small),
                forbidden_hyperedges=len(remaining),control_rank_families=control_count,
                recursion_counts=dict(stats),entrywise_native_frontier_compared=bool(work),
                native_solver_used=False,negative_proof_required=False,
                enumeration_seconds=time.monotonic()-t,seconds=time.monotonic()-start,
                peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--work',type=Path); parser.add_argument('--report',type=Path)
    args = parser.parse_args(); result = verify(args.work)
    if args.report: args.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))
