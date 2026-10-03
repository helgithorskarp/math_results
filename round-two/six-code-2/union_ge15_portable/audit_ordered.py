"""Exact ordered physical K5 certificate. six-code-2, researcher.

Derived from the immutable four_empty_parents/audit_edge_certificate.py
SHA256 5e8dc8861756f786e8f66ff2ecfcc8d5d59e99163568cb528564b09291b91028.
Unchanged complete physical MRV/core, literal row reconstruction, packing
and damage checks. New ordered incidence kernel proves the recorded
ORDERED_GRAPH_BRIDGE, independently of the producer's clique DFS.
Original60-second/two-million-state guards, native1, existing1CPU/2GiB.
The old case76 guard failure is retained and supplies no absence premise.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time
from physical_helpers import cap_family, encoded, literal, point_set, require, check_packing, rejection, operations_guard


def check_row(actual, expected):
    require(actual == expected, 'complete physical graph row differs')


def check_boundary(words, old, holes, size):
    ps = check_packing(words, size)
    old_set = set(old)
    R = len(old_set - set(ps))
    caps = [word for word in ps if 17 not in word and word not in old_set]
    represented, noncontained = set(), []
    for word in ps:
        if 17 not in word:
            continue
        tail = word - {17}
        parents = [block for block in old if tail <= block]
        if not parents:
            noncontained.append(tail)
        else:
            require(len(parents) == 1 and parents[0] not in represented, 'unique physical parent reservation')
            represented.add(parents[0])
    require(not noncontained and R == len(represented) + 4 and len(caps) == size - 64 and
            old_set - set(ps) - represented == set(holes), 'positive four-empty-parent parameters differ')
    return {'size': size, 's': len(caps), 'a': len(represented), 't': 0, 'R': R,
            'pairs': size * (size - 1) // 2, 'distinct_triples': 10 * size}


def validate_simple_graph(neighbors):
    n = len(neighbors)
    require(all(isinstance(row, (set, frozenset)) and all(type(v) is int and 0 <= v < n for v in row)
                for row in neighbors), 'physical ordered graph vertex domain')
    require(all(i not in row for i, row in enumerate(neighbors)), 'physical ordered graph self edge')
    require(all(i in neighbors[j] for i, row in enumerate(neighbors) for j in row),
            'physical ordered graph symmetry')


def ordered_neighborhood_certificate(neighbors, guard, base_states=0, require_no_k5=True, trace=True):
    """Every increasing 5-clique once; also count triangles/K4 once.

    Each inner edge is visited even when its entire ordered third domain
    is empty. State units are unchanged: physical MRV + graph rows +
    actual outer edges + actual inner edges. The ordering removes repeated
    incidences; it does not enlarge a budget or discard a possible K5.
    Positive finite graphs can use require_no_k5=False for whole comparison.
    """
    validate_simple_graph(neighbors)
    n, triangles, fours, fives, outer, inner = len(neighbors), 0, 0, 0, 0, 0
    require(type(base_states) is int and base_states >= 0 and base_states + n <= 2_000_000,
            'INCOMPLETE original two-million ordered-neighborhood proof states')
    first_five = None
    digest = hashlib.sha256()
    for i, row in enumerate(neighbors):
        for j in sorted(v for v in row if v > i):
            outer += 1
            common = {v for v in row & neighbors[j] if v > j}
            triangles += len(common)
            entries = []
            for ell in sorted(common):
                for m in sorted(v for v in common & neighbors[ell] if v > ell):
                    inner += 1
                    third = {v for v in common & neighbors[ell] & neighbors[m] if v > m}
                    if third:
                        if first_five is None:
                            first_five = [i, j, ell, m, min(third)]
                        fives += len(third)
                        require(not require_no_k5, 'physical K5 refutes claimed upper4 caps')
                    if trace:
                        entries.append([ell, m, sorted(third)])
            fours += len(entries) if trace else 0
            if trace:
                digest.update(encoded([i, j, sorted(common), entries]))
            require(base_states + n + outer + inner <= 2_000_000,
                    'INCOMPLETE original two-million ordered-neighborhood proof states')
        if i % 128 == 0:
            guard('complete ordered actual-edge K5 certificate')
    # inner is already the exact K4 count, including trace=False runs.
    require(not trace or fours == inner, 'physical ordered K4 trace count')
    return {'vertices': n, 'triangles': triangles, 'four_cliques': inner,
            'five_cliques': fives, 'first_five': first_five,
            'outer_edge_tests': outer, 'actual_inner_edge_tests': inner,
            'proof_states': base_states + n + outer + inner,
            'ordered_edge_neighborhood_trace_sha256': digest.hexdigest() if trace else None}


def main():
    parser = argparse.ArgumentParser()
    for name in ['carrier', 'graph', 'producer-summary', 'witness-dir', 'baseline69', 'work']:
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    require(not args.work.exists(), 'fresh physical four-hole audit directory required')
    args.work.mkdir(parents=True)
    begin = time.monotonic()

    def guard(stage):
        operations_guard()
        require(time.monotonic() - begin < 60, 'INCOMPLETE original60s physical four-hole audit: ' + stage)

    raw = args.carrier.read_bytes()
    data = json.loads(raw)
    old = tuple(point_set(word, 5) for word in data['parent_words'])
    old_set = set(old)
    triples = [triple for word in old for triple in combinations(sorted(word), 3)]
    require(len(old) == len(old_set) == 68 and len(triples) == len(set(triples)) == 680 and
            set(triples) == set(combinations(range(17), 3)), 'whole physical Steiner partition')
    holes = {point_set(word, 5) for word in data['hole_words']}
    require(len(holes) == 4 and holes <= old_set, 'four distinct physical empty parents')
    hole_ids = {old.index(hole) for hole in holes}
    caps = tuple(frozenset(points) for points in combinations(range(17), 5)
                 if frozenset(points) not in old_set and
                 all(len(frozenset(points) & block) <= 3 for i, block in enumerate(old) if i not in hole_ids))
    require([entry['cap'] for entry in data['caps']] == [literal(cap) for cap in caps], 'whole physical cap order differs')
    cap_set = set(caps)
    actual, core_caps, core_tails = defaultdict(set), [], []
    for core in data['cores']:
        cap = point_set(core['cap'], 5)
        ids, tails = core['parents'], core['tails']
        require(cap in cap_set and len(ids) == len(set(ids)) == len(tails) and
                set(ids) == {i for i, block in enumerate(old) if i not in hole_ids and len(cap & block) >= 3},
                'physical exact required-parent carrier')
        ts = tuple(point_set(tail, 4) for tail in tails)
        require(all(tail <= old[i] and len(tail & cap) <= 2
                    for i, tail in zip(ids, ts)) and all(len(a & b) <= 1 for a, b in combinations(ts, 2)),
                'physical required-tail compatibility')
        key = tuple(sorted(zip(ids, tails)))
        require(key not in actual[cap], 'duplicate physical partial core')
        actual[cap].add(key)
        core_caps.append(cap)
        core_tails.append(ts)
    key_digest, mr_nodes, offset = hashlib.sha256(), 0, 0
    for cap, entry in zip(caps, data['caps']):
        expected, nodes = cap_family(cap, old, hole_ids, guard)
        mr_nodes += nodes
        require(mr_nodes <= 2_000_000, 'INCOMPLETE original two-million physical MRV states')
        require(actual[cap] == expected, 'complete physical core keys differ')
        count = len(expected)
        require(entry['first_core'] == offset and entry['core_count'] == count and
                all(core['cap'] == literal(cap) for core in data['cores'][offset:offset + count]),
                'complete zero/positive cap prefix differs')
        offset += count
        key_digest.update(encoded([literal(cap), sorted(expected)]))
        guard('full physical carrier')
    require(offset == len(data['cores']), 'full physical core prefix length')

    cap_occ, tail_occ = defaultdict(int), defaultdict(int)
    for i, (cap, tails) in enumerate(zip(core_caps, core_tails)):
        cap_occ[cap] |= 1 << i
        for tail in tails:
            tail_occ[tail] |= 1 << i
    cap3, tail3, tail2 = defaultdict(int), defaultdict(int), defaultdict(int)
    for cap, bits in cap_occ.items():
        for triple in combinations(sorted(cap), 3):
            cap3[triple] |= bits
    for tail, bits in tail_occ.items():
        for triple in combinations(sorted(tail), 3):
            tail3[triple] |= bits
        for pair in combinations(sorted(tail), 2):
            tail2[pair] |= bits
    cap_bad, tail_bad = {}, {}
    for cap in cap_occ:
        bad = 0
        for triple in combinations(sorted(cap), 3):
            bad |= cap3[triple] | tail3[triple]
        cap_bad[cap] = bad
    for tail in tail_occ:
        cb = pb = 0
        for triple in combinations(sorted(tail), 3):
            cb |= cap3[triple]
        for pair in combinations(sorted(tail), 2):
            pb |= tail2[pair]
        tail_bad[tail] = cb | (pb & ~tail_occ[tail])
    graph_raw = args.graph.read_bytes()
    graph = json.loads(graph_raw)
    n = len(core_caps)
    require(graph['vertices'] == len(graph['adjacency_hex']) == n and
            graph['core_carrier_sha256'] == hashlib.sha256(raw).hexdigest() and
            graph['hole_words'] == data['hole_words'],
            'physical graph scope differs')
    all_bits, row_digest, neighbors, degrees = (1 << n) - 1, hashlib.sha256(), [], Counter()
    for i, (cap, tails) in enumerate(zip(core_caps, core_tails)):
        bad = cap_bad[cap]
        for tail in tails:
            bad |= tail_bad[tail]
        row = all_bits & ~bad
        require(not row >> i & 1, 'physical self edge')
        check_row(int(graph['adjacency_hex'][i], 16), row)
        row_digest.update(encoded([i, format(row, 'x')]))
        degrees[row.bit_count()] += 1
        nb = set()
        while row:
            bit = row & -row
            row ^= bit
            nb.add(bit.bit_length() - 1)
        neighbors.append(nb)
        if i % 256 == 0:
            guard('entrywise physical rows')
    require(sum(degree * count for degree, count in degrees.items()) == 2 * graph['edges'] and
            all(i in neighbors[j] for i, row in enumerate(neighbors) for j in row), 'physical edge count/symmetry')

    ordered = ordered_neighborhood_certificate(neighbors, guard, base_states=mr_nodes, require_no_k5=True)
    outer_edge_tests, inner_edge_tests = ordered['outer_edge_tests'], ordered['actual_inner_edge_tests']
    tri_inc, four_inc = ordered['triangles'], ordered['four_cliques']
    require(outer_edge_tests == graph['edges'], 'physical ordered outer-edge count differs')
    summary_raw = args.producer_summary.read_bytes()
    summary = json.loads(summary_raw)
    require(summary['status'] == 'COMPLETE_FIXED_FOUR_HOLE_GRAPH_THROUGH_SIX_CLIQUES_SINGLE_PRODUCER_ONLY' and
            summary['all_counts_complete'] and summary['carrier_sha256'] == hashlib.sha256(raw).hexdigest() and
            summary['graph_sha256'] == hashlib.sha256(graph_raw).hexdigest() and
            summary['hole_words'] == data['hole_words'] and summary['vertices'] == n and
            summary['edges'] == outer_edge_tests and summary['triangles'] == tri_inc and
            summary['four_cliques'] == four_inc and summary['five_cliques'] == summary['six_cliques'] == 0,
            'complete producer carrier/graph/clique record differs')
    positives = []
    for size in range(64, 71):
        path = args.witness_dir / ('WITNESS' + str(size) + '.json')
        if path.exists():
            witness = json.loads(path.read_bytes())
            decoded = check_boundary(witness['words'], old, holes, size)
            positives.append(decoded)
    require(positives, 'at least one literal positive required')
    max_size = max(row['size'] for row in positives)
    words = json.loads((args.witness_dir / ('WITNESS' + str(max_size) + '.json')).read_bytes())['words']
    baseline_raw = args.baseline69.read_bytes()
    baseline_lines = baseline_raw.decode().splitlines()
    require(len(baseline_lines) == 69 and all(len(line) == 18 and set(line) <= {'0', '1'} for line in baseline_lines),
            'credited baseline binary domain')
    check_packing([int(line, 2) for line in baseline_lines], 69)
    target = next(cap for cap in caps if actual[cap])
    expected, _ = cap_family(target, old, hole_ids, guard)
    damaged = set(actual[target])
    damaged.pop()
    def check_keys(value):
        require(value == expected, 'complete physical core keys differ')
    controls = [rejection('omitted-valid-core', lambda: check_keys(damaged), 'complete physical core keys differ')]
    row = int(graph['adjacency_hex'][0], 16)
    controls.append(rejection('toggled-physical-graph-entry', lambda: check_row(row ^ 2, row),
                              'complete physical graph row differs'))
    wrong_holes = (holes - {next(iter(holes))}) | {next(block for block in old if block not in holes)}
    controls.append(rejection('wrong-empty-parent-declaration',
                              lambda: check_boundary(words, old, wrong_holes, max_size),
                              'positive four-empty-parent parameters differ'))
    duplicate = list(words[:-1]) + [words[0]]
    controls.append(rejection('duplicate-positive-word', lambda: check_packing(duplicate, max_size),
                              'positive distinct word count'))
    first = sorted(check_packing(words, max_size)[0])
    collision = next(literal(first[:4]) | (1 << p) for p in range(18) if p not in first and
                     (literal(first[:4]) | (1 << p)) not in words)
    collided = list(words[:-1]) + [collision]
    controls.append(rejection('distinct-weight-five-positive-collision', lambda: check_packing(collided, max_size),
                              'positive physical collision'))
    guard('complete audit')
    record = {'agent': 'six-code-2', 'role': 'researcher',
              'status': 'COMPLETE_PHYSICAL_FOUR_EMPTY_PARENT_CARRIER_GRAPH_ORDERED_NEIGHBORHOOD_K5_CERTIFICATE_AND_POSITIVES',
              'hole_words': data['hole_words'], 'physical_D_words': 68, 'physical_D_triples': 680,
              'prospective_caps': len(caps), 'zero_core_caps': sum(not actual[cap] for cap in caps),
              'cores': n, 'adaptive_MRV_nodes': mr_nodes, 'physical_core_key_sha256': key_digest.hexdigest(),
              'entrywise_physical_rows': n, 'physical_graph_row_sha256': row_digest.hexdigest(),
              'edges': graph['edges'], 'triangles': tri_inc, 'four_cliques': four_inc,
              'five_cliques': 0, 'six_cliques': 0,
              'outer_edge_tests': outer_edge_tests, 'actual_inner_edge_tests': inner_edge_tests,
              'ordered_edge_neighborhood_trace_sha256': ordered['ordered_edge_neighborhood_trace_sha256'],
              'counting_rule': 'Each triangle and K4 counted once by increasing physical core IDs.',
              'proof_states': mr_nodes + n + outer_edge_tests + inner_edge_tests,
              'producer_summary_sha256': hashlib.sha256(summary_raw).hexdigest(),
              'k5_method': 'For every edge i<j test every edge ell<m in N(i)&N(j)&{v>j}; every common third vertex>m is tested. Every K5 appears once by increasing order. No greedy-color inference.',
              'positive_packings': positives, 'max_positive_size': max_size,
              'baseline69_sha256': hashlib.sha256(baseline_raw).hexdigest(),
              'known_baseline69_pairs': 2346, 'known_baseline69_triples': 690,
              'semantic_controls': controls,
              'formalized': False, 'independent_person_review': 'pending', 'all_algorithms_same_author': True,
              'ordinary_scope': 'Specified literalD and four empty parents only; arbitrary t0/R=a+4 packing restricts to complete carrier. Optional restoration and all-four-parent normalization are separate ordinary bridges/coverage, no unrestricted endpoint.'}
    output = encoded(record)
    (args.work / 'EXACT_RESULT.json').write_bytes(output)
    execution = {'agent': 'six-code-2', 'role': 'researcher', 'seconds': time.monotonic() - begin,
                 'peak_RSS_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                 'initial_seconds': 60, 'initial_states': 2000000,
                 'exact_result_bytes': len(output), 'exact_result_sha256': hashlib.sha256(output).hexdigest()}
    (args.work / 'EXECUTION.json').write_bytes(encoded(execution))
    print(json.dumps(execution, sort_keys=True))


if __name__ == '__main__':
    main()
