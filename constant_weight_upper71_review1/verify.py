"""Independent literal-set verifier for complete color/branch exclusion trees."""
import argparse
import copy
import hashlib
import itertools
import json
import math
from pathlib import Path


def require(test, message):
    if not test:
        raise ValueError(message)


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def build(lengths):
    # The verifier explicitly traverses the alternating cycle components.
    absent = set()
    start = 0
    for size in lengths:
        for v in range(start, start + size):
            previous = start + (v - start - 1) % size
            absent.add((v, v))
            absent.add((previous, v))
        start += size
    cells = sorted(set(itertools.product(range(5), repeat=2)) - absent)
    require(len(cells) == 15, 'cell count')
    require(all(sum(r == i for r, c in cells) == 3 for i in range(5)), 'row degree')
    require(all(sum(c == i for r, c in cells) == 3 for i in range(5)), 'column degree')
    anchors = [frozenset([15] + [i for i, cell in enumerate(cells) if cell[0] == r]) for r in range(5)]
    anchors += [frozenset([16] + [i for i, cell in enumerate(cells) if cell[1] == c]) for c in range(5)]
    anchor_pairs = []
    for block in anchors:
        require(len(block) == 4, 'anchor cardinality')
        anchor_pairs.extend(frozenset(p) for p in itertools.combinations(block, 2))
    require(len(anchor_pairs) == len(set(anchor_pairs)) == 60, 'anchor pair repetition')
    forbidden = set(anchor_pairs)
    # Verifier tests every one of the 1365 literal four-subsets.
    columns = []
    pair_sets = []
    for block in itertools.combinations(range(15), 4):
        pairs = frozenset(frozenset(p) for p in itertools.combinations(block, 2))
        if pairs.isdisjoint(forbidden):
            columns.append(block)
            pair_sets.append(pairs)
    neighbors = {i: frozenset(j for j in range(len(columns))
                              if i != j and pair_sets[i].isdisjoint(pair_sets[j]))
                 for i in range(len(columns))}
    return cells, anchors, columns, neighbors


def check_tree(proof, neighbors, target, available=None, depth=0):
    if available is None:
        available = frozenset(neighbors)
    require(type(target) is int and target > 0, 'invalid target')
    require(depth < target, 'positive clique leaf cannot be refuted')
    require(type(proof) is list, 'node structure')
    remaining = set(available)
    nodes = 1
    for branch in proof:
        require(type(branch) is list and len(branch) == 2, 'branch structure')
        vertex, child = branch
        require(type(vertex) is int and vertex in remaining, 'branch vertex')
        nodes += check_tree(child, neighbors, target,
                            frozenset(remaining) & neighbors[vertex], depth + 1)
        remaining.remove(vertex)
    # Build a proper coloring with literal sets; no producer color is trusted.
    uncolored = set(remaining)
    groups = []
    while uncolored:
        group = []
        for vertex in sorted(uncolored):
            if all(vertex not in neighbors[u] for u in group):
                group.append(vertex)
        require(bool(group), 'color progress')
        uncolored.difference_update(group)
        groups.append(group)
    seen = set()
    for group in groups:
        require(type(group) is list and len(group) > 0, 'empty/malformed color class')
        require(all(type(v) is int and v in remaining for v in group), 'color vertex')
        require(len(group) == len(set(group)), 'repeated vertex in color')
        require(not seen.intersection(group), 'repeated color assignment')
        require(all(v not in neighbors[u] for u, v in itertools.combinations(group, 2)),
                'color class contains adjacent vertices')
        seen.update(group)
    require(seen == remaining, 'coloring must cover exactly the unbranched vertices')
    require(depth + len(groups) < target, 'insufficient color bound')
    return nodes


def packing(blocks, n=17):
    require(all(len(block) == 4 and all(type(x) is int and 0 <= x < n for x in block) for block in blocks),
            'invalid quadruple')
    pairs = [frozenset(p) for block in blocks for p in itertools.combinations(block, 2)]
    require(len(pairs) == len(set(pairs)), 'repeated pair')
    replication = [sum(x in block for block in blocks) for x in range(n)]
    require(max(replication) <= 5, 'point bound')
    high = {x for x, r in enumerate(replication) if r < 5}
    low = set(range(n)) - high
    leave = set(frozenset(p) for p in itertools.combinations(range(n), 2)) - set(pairs)
    e = sum(p <= high for p in leave)
    m = sum(p <= low for p in leave)
    return {'blocks': len(blocks), 'replication': replication,
            'positive_deficits': sorted(5 - replication[x] for x in high),
            'high_leave_edges': e, 'low_leave_edges': m, 'leave_edges': len(leave)}


def affine_examples():
    def multiply(a, b):
        result = 0
        for _ in range(2):
            if b & 1:
                result ^= a
            b >>= 1
            a <<= 1
            if a & 4:
                a ^= 7  # GF(4), irreducible polynomial x^2+x+1.
        return result
    require(all(multiply(x, y) == multiply(y, x) for x in range(4) for y in range(4)), 'field symmetry')
    blocks = [frozenset(4 * x + y for y in range(4)) for x in range(4)]
    blocks += [frozenset(4 * x + (multiply(slope, x) ^ b) for x in range(4))
               for slope in range(4) for b in range(4)]
    require(len(blocks) == len(set(blocks)) == 20, 'affine line count')
    examples = []
    for k in range(5):
        switched = [((block - {4 * i}) | {16}) if i < k else block
                    for i, block in enumerate(blocks)]
        row = packing(switched)
        require(row['blocks'] == 20 and row['high_leave_edges'] == k and row['low_leave_edges'] == 0,
                'parallel switches')
        examples.append(row)
    for switches in [[(0, 0), (4, 0)], [(0, 0), (4, 0), (8, 5)]]:
        changed = blocks.copy()
        for index, removed in switches:
            require(removed in changed[index], 'switch point')
            changed[index] = (changed[index] - {removed}) | {16}
        row = packing(changed)
        require(row['blocks'] == 20 and row['low_leave_edges'] == 0, 'marked switches')
        examples.append(row)
    partitions = sorted(row['positive_deficits'] for row in examples)
    require(partitions == [[1, 1, 1, 1, 1], [1, 1, 1, 2], [1, 1, 3], [1, 2, 2], [1, 4], [2, 3], [5]],
            'all seven deficit partitions')
    return examples


def baseline(data):
    lines = data.decode('ascii').splitlines()
    require(len(lines) == len(set(lines)) == 69, 'baseline69 distinct word count')
    require(all(len(word) == 18 and set(word) <= {'0', '1'} and word.count('1') == 5 for word in lines),
            'baseline word definition')
    words = [{i for i, bit in enumerate(word) if bit == '1'} for word in lines]
    maximum = max(len(a & b) for a, b in itertools.combinations(words, 2))
    require(maximum <= 2, 'baseline intersection')
    return {'words': len(words), 'maximum_intersection': maximum, 'minimum_distance': 10 - 2 * maximum,
            'sha256': hashlib.sha256(data).hexdigest()}


def bridge_controls():
    triples = []
    for edges in itertools.product([0, 1], repeat=3):
        degree = [edges[0] + edges[1], edges[0] + edges[2], edges[1] + edges[2]]
        homogeneous = sum(d in [0, 2] for d in degree)
        require(homogeneous >= 1, 'three-vertex homogeneous incidence')
        if min(degree) >= 1:
            require(edges.count(0) <= 1, 'no-isolated-vertex nondeficit pair bound')
        triples.append({'edges': list(edges), 'homogeneous_incidences': homogeneous,
                        'allowed_by_saturated_pair_lemma': min(degree) >= 1})
    result = {'three_vertex_graphs': triples,
              'twenty_point_deficit': 17 * 5 - 20 * 4,
              'twenty_leave_pairs': math.comb(17, 2) - 20 * math.comb(4, 2),
              'twenty_one_point_deficit': 17 * 5 - 21 * 4,
              'twenty_one_forced_saturated_leave_edges': (16 - 4) // 2,
              'seventy_two_total_point_occurrences': 72 * 5,
              'seventy_two_uncovered_triples': math.comb(18, 3) - 72 * math.comb(5, 3),
              'homogeneous_incidence_upper': 18 * (5 - 1),
              'nondeficit_pair_lower': math.comb(18, 2) - 18 * 5 // 2}
    require(result['twenty_point_deficit'] == 5 and result['twenty_leave_pairs'] == 16,
            'local incidence arithmetic')
    require(result['twenty_one_point_deficit'] == 1 and result['twenty_one_forced_saturated_leave_edges'] == 6,
            'classical bound arithmetic')
    require(result['seventy_two_total_point_occurrences'] == 18 * 20, 'point equality at72')
    require(result['seventy_two_uncovered_triples'] == 96 > result['homogeneous_incidence_upper'],
            'homogeneous contradiction arithmetic')
    require(result['nondeficit_pair_lower'] == 108 > result['seventy_two_uncovered_triples'],
            'alternative contradiction arithmetic')
    return result


def verify(record):
    require(type(record) is dict and set(record) == {'format', 'target', 'models'}, 'certificate fields')
    require(record['format'] == 'rebuild-color-branch-v1' and record['target'] == 10, 'format/target')
    require(len(record['models']) == 2, 'complete two-model coverage')
    output = []
    for model, lengths, count in zip(record['models'], [[5], [2, 3]], [95, 96]):
        require(set(model) == {'cycle_half_lengths', 'column_count', 'column_sha256', 'proof', 'proof_nodes', 'nine_clique'},
                'model fields')
        require(model['cycle_half_lengths'] == lengths, 'cycle coverage/order')
        cells, anchors, columns, neighbors = build(lengths)
        require(len(columns) == model['column_count'] == count, 'candidate count')
        digest = hashlib.sha256(canonical(columns)).hexdigest()
        require(digest == model['column_sha256'], 'full candidate stream')
        nodes = check_tree(model['proof'], neighbors, 10)
        require(nodes == model['proof_nodes'], 'node count')
        nine = model['nine_clique']
        require(type(nine) is list and len(nine) == len(set(nine)) == 9, 'nine-clique cardinality')
        require(all(type(v) is int and v in neighbors for v in nine), 'nine-clique vertex')
        require(all(v in neighbors[u] for u, v in itertools.combinations(nine, 2)), 'nine-clique adjacency')
        restored = packing(anchors + [frozenset(columns[i]) for i in nine])
        require(restored['blocks'] == 19 and restored['replication'][15:17] == [5, 5], 'nineteen-packing control')
        require(not any(15 in b and 16 in b for b in anchors + [columns[i] for i in nine]), 'uncovered anchor pair')
        output.append({'cycle_half_lengths': lengths, 'candidate_count': count,
                       'column_sha256': digest, 'proof_nodes': nodes, 'maximum_clique': 9,
                       'nineteen_packing': restored})
    return {'models': output, 'total_nodes': sum(row['proof_nodes'] for row in output),
            'certificate_sha256': hashlib.sha256(canonical(record)).hexdigest(),
            'affine_twenty_examples': affine_examples(),
            'bridge_controls': bridge_controls(),
            'proved_scope': 'Saturated points form a covered-pair clique in every20-quadruple pair packing on17 points; independent A(17,6,4)=20 and A(18,6,5)<=71 proofs use the written bridges.'}


def controls(record):
    failures = []
    def rejected(label, action):
        try:
            action()
        except (ValueError, TypeError, KeyError, IndexError):
            failures.append(label)
        else:
            raise ValueError('malformed control accepted: ' + label)
    bad = copy.deepcopy(record)
    bad['models'].pop()
    rejected('missing entire cycle model', lambda: verify(bad))
    bad = copy.deepcopy(record)
    bad['target'] = 11
    rejected('changed target', lambda: verify(bad))
    bad = copy.deepcopy(record)
    bad['models'][0]['column_sha256'] = '0' * 64
    rejected('wrong candidate stream', lambda: verify(bad))
    bad = copy.deepcopy(record)
    bad['models'][0]['nine_clique'][1] = bad['models'][0]['nine_clique'][0]
    rejected('repeated positive-witness vertex', lambda: verify(bad))
    _, _, _, graph = build([5])
    rejected('missing required branches', lambda: check_tree([], graph, 10))
    rejected('out-of-domain branch vertex', lambda: check_tree([[len(graph), []]], graph, 10))
    bad_tree = copy.deepcopy(record['models'][0]['proof'])
    require(bool(bad_tree), 'branch corruption control requires root branch')
    bad_tree.pop()
    rejected('missing branch without leaf coverage', lambda: check_tree(bad_tree, graph, 10))
    complete = {v: frozenset(range(10)) - {v} for v in range(10)}
    rejected('false K10 negative', lambda: check_tree([], complete, 10))
    rejected('positive leaf labeled negative', lambda: check_tree([], {}, 10, frozenset(), 10))
    rejected('repeated pair in a packing', lambda: packing([frozenset([0, 1, 2, 3])] * 2))
    empty_graph = {v: frozenset() for v in range(10)}
    require(check_tree([], empty_graph, 2) == 1, 'valid empty-edge graph control')
    require(check_tree([], {0: frozenset([1, 2]), 1: frozenset([0, 2]), 2: frozenset([0, 1])}, 4) == 1,
            'valid K3 bound control')
    return {'rejected': failures, 'valid_small_graph_controls': 2}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, required=True)
    parser.add_argument('--expected', type=Path)
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--controls', action='store_true')
    args = parser.parse_args()
    certificate = json.loads(args.certificate.read_text())
    output = verify(certificate)
    output['baseline69'] = baseline(args.baseline.read_bytes())
    if args.controls:
        output['controls'] = controls(certificate)
    serialized = canonical(output)
    if args.expected:
        require(serialized == args.expected.read_bytes(), 'complete expected output differs')
    print(serialized.decode(), end='')
