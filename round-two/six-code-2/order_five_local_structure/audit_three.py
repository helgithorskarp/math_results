"""Independent physical-triple / opposite-edge audit for radius-three repairs.

Every finite candidate carrier is regenerated. A K4 exists exactly when the
common neighborhood of some graph edge contains another edge. Python sets
and shared physical triples replace the producer's word and graph bitsets.
"""
import argparse
from collections import Counter
from itertools import combinations
import hashlib
import json
from pathlib import Path
import resource
import time


def require(ok, message):
    if not ok:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def opposite_edges(neighbors):
    """Return (K4 absent, examined edges) in a finite simple graph."""
    examined = 0
    for w in neighbors:
        for v in neighbors[w]:
            if v <= w:
                continue
            examined += 1
            common = neighbors[w] & neighbors[v]
            if any(not neighbors[u].isdisjoint(common) for u in common):
                return False, examined
    return True, examined


def finite_graph_control():
    graphs = 0
    for n in range(6):
        edges = list(combinations(range(n), 2))
        for bits in range(1 << len(edges)):
            neighbors = {i: set() for i in range(n)}
            for j, (a, b) in enumerate(edges):
                if bits & (1 << j):
                    neighbors[a].add(b)
                    neighbors[b].add(a)
            literal_absence = not any(all(b in neighbors[a] for a, b in combinations(q, 2))
                                      for q in combinations(range(n), 4))
            require(opposite_edges(neighbors)[0] == literal_absence, 'opposite-edge control fails')
            graphs += 1
    require(graphs == 1100, 'incomplete small-graph control carrier')
    return graphs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--classification', type=Path, required=True)
    parser.add_argument('--producer-summary', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists(), 'require a new audit output')
    start = time.monotonic()
    raw = args.classification.read_bytes()
    bases = json.loads(raw)['classes']
    summary_raw = args.producer_summary.read_bytes()
    supplied = json.loads(summary_raw)
    require(supplied['status'] == 'COMPLETE_EXACT_69_ABSENCE_PRODUCER' and supplied['radius'] == 3,
            'producer did not complete radius three')
    require(len(bases) == len(supplied['cases']) == 8, 'wrong carrier')
    physical = {}
    for ps in combinations(range(18), 5):
        physical[sum(1 << p for p in ps)] = frozenset(combinations(ps, 3))
    all_three = list(combinations(range(68), 3))
    require(len(physical) == 8568 and len(all_three) == 50116, 'wrong complete carriers')
    graph_controls = finite_graph_control()
    cases = []
    distinct_graph_tests = 0
    opposite_edge_tests = 0
    for ci, entry in enumerate(bases):
        require(entry['class_index'] == supplied['cases'][ci]['class_index'] == ci, 'class order differs')
        base = entry['representative_words']
        require(len(base) == len(set(base)) == 68 and all(w in physical for w in base), 'invalid literal base')
        owners = {}
        for i, w in enumerate(base):
            for t in physical[w]:
                require(t not in owners, 'base reuses a triple')
                owners[t] = i
        packets = {}
        for w, triples in physical.items():
            blockers = tuple(sorted({owners[t] for t in triples if t in owners}))
            if len(blockers) <= 3:
                packets.setdefault(blockers, []).append(w)
        vertices = sorted(w for bucket in packets.values() for w in bucket)
        compatible = {w: {v for v in vertices if v != w and physical[w].isdisjoint(physical[v])}
                      for w in vertices}
        hist = Counter()
        digest = hashlib.sha256()
        known_graphs = set()
        for ai, deleted in enumerate(all_three):
            if ai % 512 == 0:
                require(time.monotonic() - start < 60, 'INCOMPLETE initial 60-second audit guard')
            words = sorted(w for n in range(4) for subset in combinations(deleted, n)
                           for w in packets.get(subset, ()))
            require(all(base[i] in words for i in deleted), 'missing old-word reinsertion')
            domain = set(words)
            neighbors = {w: compatible[w] & domain for w in words}
            position = {w: j for j, w in enumerate(words)}
            pattern = tuple(tuple(sorted(position[v] for v in neighbors[w])) for w in words)
            if pattern not in known_graphs:
                distinct_graph_tests += 1
                absent, checked_edges = opposite_edges(neighbors)
                opposite_edge_tests += checked_edges
                require(absent, 'four-clique contradicts claimed 69-word absence')
                known_graphs.add(pattern)
            hist[len(words)] += 1
            digest.update(encoded([list(deleted), words, True]))
        case = {'class_index': ci, 'anchors': len(all_three),
                'eligible_outside_words': len(vertices) - 68,
                'domain_size_histogram': [list(p) for p in sorted(hist.items())],
                'ordered_anchor_domain_absence_sha256': digest.hexdigest()}
        require(case == supplied['cases'][ci], 'complete independently rebuilt case differs')
        cases.append(case)
    result = {'agent': 'six-code-2', 'role': 'researcher',
              'status': 'COMPLETE_INDEPENDENT_PHYSICAL_OPPOSITE_EDGE_AUDIT',
              'input_classification_sha256': hashlib.sha256(raw).hexdigest(),
              'input_producer_summary_sha256': hashlib.sha256(summary_raw).hexdigest(),
              'every_physical_word_per_base': 8568, 'all_anchors': 400928,
              'sharp_maximum_completion_size_for_every_anchor': 68,
              'distinct_ordered_graph_patterns_checked': distinct_graph_tests,
              'opposite_edge_checks': opposite_edge_tests, 'cases': cases,
              'every_simple_graph_at_most_five_vertices_checked_against_literal_subsets': graph_controls,
              'initial_whole_guard_seconds': 60, 'seconds': time.monotonic() - start,
              'peak_RSS_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'scope': 'Eight literal bases; arbitrary target repairs retaining at least 65 base words. Complete original graph transports are a separate premise.'}
    args.output.write_bytes(encoded(result))
    print(json.dumps({k: v for k, v in result.items() if k != 'cases'}, sort_keys=True))


if __name__ == '__main__':
    main()
