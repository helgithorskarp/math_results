"""Independent scalar inverse-fiber/DFS audit of the finite closures.
Author: six-sorting-1, researcher. Imports no generator or SAT package.
"""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import resource
import time

HERE = Path(__file__).resolve().parent
PAIRS = tuple(itertools.combinations(range(11), 2))

def classification():
    result = [[(0, 5), (0, 1)]]
    free = (2, 3, 4, 6, 7, 8, 9, 10)
    for p in free:
        result += [[(0, p), (0, 5), (0, 1)],
                   [tuple(sorted((p, 5))), (0, min(p, 5)), (0, 1)]]
    for p in range(2, 11):
        result.append([(0, 5), (0, p), (0, 1)])
    for p, q in itertools.product(free, repeat=2):
        result.append([(0, p), tuple(sorted((q, 5))), (0, min(q, 5)), (0, 1)])
    for q in free:
        for p in range(2, 11):
            if p != min(q, 5):
                result.append([tuple(sorted((q, 5))), (0, p), (0, min(q, 5)), (0, 1)])
    result.sort()
    assert len(result) == len({tuple(word) for word in result}) == 154
    assert Counter(map(len, result)) == {2: 1, 3: 25, 4: 128}
    return result

def scalar(values, word, low_count=2):
    v = list(values)
    hits = 0
    for a, b in word:
        hits += v[a] < low_count or v[b] < low_count
        if v[a] > v[b]:
            v[a], v[b] = v[b], v[a]
    return v, hits

def initial_profiles(fixture):
    results = {}
    controls = 0
    for case in (1, 2):
        strongest = {}
        prefix = fixture['prefix21'] + fixture['tournaments'][str(case)]
        for a, b in itertools.combinations(range(13), 2):
            order = [a, b] + [i for i in range(13) if i not in (a, b)]
            values = [0] * 13
            for rank, position in enumerate(order):
                values[position] = rank
            out, D = scalar(values, prefix)
            positions = tuple(sorted((out.index(0), out.index(1))))
            assert positions in PAIRS and out[11:] == [11, 12]
            label = PAIRS.index(positions)
            strongest[label] = max(D, strongest.get(label, D))
            final, tail = scalar(out, fixture['known21_suffix'])
            assert final == list(range(13)) and D + tail <= 10
            controls += 1
        results[case] = tuple(sorted(strongest.items()))
    assert results[1] == results[2] and len(results[1]) == 8
    assert sum(2 ** D for label, D in results[1]) == 208
    return results, controls

def comparator_fibers():
    tables = {}
    checks = 0
    for gate in PAIRS:
        images = {}
        fibers = {}
        for label, marked in enumerate(PAIRS):
            values = [0] * 11
            order = list(marked) + [i for i in range(11) if i not in marked]
            for rank, position in enumerate(order):
                values[position] = rank
            out, hits = scalar(values, [gate])
            positions = tuple(sorted((out.index(0), out.index(1))))
            output = PAIRS.index(positions)
            images[label] = output
            fibers.setdefault(output, []).append((label, hits))
            checks += 1
        assert all(1 <= len(fiber) <= 2 for fiber in fibers.values())
        assert all(len(fiber) == 1 or all(hits == 1 for label, hits in fiber)
                   for fiber in fibers.values())
        tables[gate] = images, fibers
    return tables, checks

def inverse_step(state, gate, tables, maximum_weight=512):
    images, fibers = tables[gate]
    source = dict(state)
    outputs = {images[label] for label, D in state}
    new = []
    for output in sorted(outputs):
        deletion = max(source[label] + hits for label, hits in fibers[output] if label in source)
        new.append((output, deletion))
    assert sum(2 ** D for label, D in new) >= sum(2 ** D for label, D in state)
    if sum(2 ** D for label, D in new) > maximum_weight:
        return None
    return tuple(new)

def state_digest(known):
    digest = hashlib.sha256()
    for depth, states in enumerate(known):
        packed = []
        for state in states:
            packed.append(tuple(sorted((((1 << PAIRS[label][0]) | (1 << PAIRS[label][1])) << 4) | D
                                       for label, D in state)))
        for state in sorted(packed):
            digest.update(json.dumps([depth, state], separators=(',', ':')).encode())
    return digest.hexdigest()

def root_closure(initial, tables):
    allowed = [gate for gate in PAIRS if all(p not in gate for p in (0, 1, 5))]
    known = {initial}
    stack = [initial]
    edges = rejected = 0
    while stack:
        state = stack.pop()
        for gate in allowed:
            edges += 1
            new = inverse_step(state, gate, tables)
            if new is None:
                rejected += 1
            elif new not in known:
                known.add(new)
                stack.append(new)
    return frozenset(known), edges, rejected

def check_closure(report, word, initial, tables, root_data=None):
    assert report['complete'] and report['remaining_queue'] == 0 and not report['survivors']
    assert report['trie_nodes'] == len(word) + 1
    positions = [0, 1, 5]
    allowed = []
    for gate in word:
        allowed.append(tuple(pair for pair in PAIRS if all(p not in pair for p in positions)))
        positions = [gate[0] if p in gate else p for p in positions]
    assert positions == [0, 0, 0]
    known = [set() for depth in range(len(word) + 1)]
    if root_data is None:
        known[0].add(initial)
        stack = [(0, initial)]
        transitions = pruned = 0
    else:
        known[0], transitions, pruned = root_data
        assert initial in known[0]
        stack = []
        for state in known[0]:
            transitions += 1
            new = inverse_step(state, word[0], tables)
            if new is None:
                pruned += 1
            elif new not in known[1]:
                known[1].add(new)
                stack.append((1, new))
    while stack:
        depth, state = stack.pop()
        assert depth < len(word), 'A terminal passed the necessary deletion bound'
        events = [(depth, gate) for gate in allowed[depth]] + [(depth + 1, word[depth])]
        for child, gate in events:
            transitions += 1
            new = inverse_step(state, gate, tables)
            if new is None:
                pruned += 1
            elif new not in known[child]:
                known[child].add(new)
                stack.append((child, new))
    states = sum(map(len, known))
    assert states == report['unique_states'] == report['processed_states']
    assert transitions == report['transitions']
    assert pruned == report['pruned_deletion_weight_above512']
    assert {str(depth): len(rows) for depth, rows in enumerate(known) if rows} == report['coverage_by_kernel_depth']
    digest = state_digest(known)
    assert digest == report['state_digest_sha256']
    return {'kernel_index': report['kernel_index_selection'], 'states': states,
            'transitions': transitions, 'pruned': pruned, 'state_digest_sha256': digest}


def fixture_checks(fixture):
    boolean_inputs = positive_inputs = single_bounds = mixed_bounds = 0
    for case in (1, 2):
        prefix = fixture['prefix21'] + fixture['tournaments'][str(case)]
        assert len(prefix) == 24
        image = set()
        for mask in range(8192):
            values = [int(bool(mask & (1 << i))) for i in range(13)]
            out, _ = scalar(values, prefix)
            assert out[11:] == sorted(values)[-2:]
            image.add(sum(out[i] << i for i in range(11)))
            final, _ = scalar(out, fixture['known21_suffix'])
            assert final == sorted(values)
            boolean_inputs += 1
            positive_inputs += 1
        assert image == set(fixture['Y_states'][str(case)])
        assert len(image) == (146 if case == 1 else 145)
        assert {i for i in range(11) if 2047 ^ (1 << i) in image} == {0, 1, 5}
        assert all(mask == 2047 or any(not (mask >> i & 1) for i in (0, 1, 5)) for mask in image)
        assert all((mask >> 1 & 1) <= (mask >> 10 & 1) for mask in image)
        assert 1 << 9 in image and 1 << 10 in image
        for leaf, nonlow in fixture['single_minimum_witnesses'].items():
            low = [i for i in range(13) if not (nonlow >> i & 1)]
            assert len(low) == 1
            order = low + [i for i in range(13) if i not in low]
            ranks = [0] * 13
            for rank, position in enumerate(order):
                ranks[position] = rank
            out, D = scalar(ranks, prefix, 1)
            assert out.index(0) == int(leaf)
            assert 44 - 39 - D == (2 if int(leaf) == 1 else 3)
            single_bounds += 1
        witness = fixture['mixed_witness']
        high, low = witness['high_inputs'], witness['low_input']
        order = [low] + [i for i in range(13) if i not in high and i != low] + high
        ranks = [0] * 13
        for rank, position in enumerate(order):
            ranks[position] = rank
        D = 0
        for a, b in prefix:
            D += ranks[a] == 0 or ranks[b] == 0 or ranks[a] >= 10 or ranks[b] >= 10
            if ranks[a] > ranks[b]:
                ranks[a], ranks[b] = ranks[b], ranks[a]
        assert ranks[1] == 0 and ranks[10:] == [10, 11, 12]
        assert D == witness['prefix_deletions'] == 16
        assert 44 - witness['middle_size_lower_bound'] - D == 3
        mixed_bounds += 1
    return {'original_boolean_prefix_inputs': boolean_inputs,
            'known45_positive_boolean_inputs': positive_inputs,
            'single_minimum_rank_bounds': single_bounds, 'mixed_rank_bounds': mixed_bounds}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--index', type=int)
    p.add_argument('--out', type=Path)
    args = p.parse_args()
    start = time.monotonic()
    raw = (HERE / 'fixture.json').read_bytes()
    fixture = json.loads(raw)
    certificate = json.loads((HERE / 'certificate.json').read_text())
    assert certificate['fixture_sha256'] == hashlib.sha256(raw).hexdigest()
    assert fixture['known_sizes']['11'] == 35 and fixture['known_sizes']['12'] == 39
    assert fixture['known_sizes']['9'] == 25
    assert fixture['full_budget'] == 44 and fixture['Y_budget'] == 20
    controls = fixture_checks(fixture)
    words = classification()
    assert len(certificate['closures']) == 153
    assert [record['index'] for record in certificate['closures']] == [i for i, word in enumerate(words) if len(word) > 2]
    for record in certificate['closures']:
        assert record['word'] == [list(gate) for gate in words[record['index']]]
    initial, ranks_checked = initial_profiles(fixture)
    scalar_profile = [[(1 << PAIRS[label][0]) | (1 << PAIRS[label][1]), D] for label, D in initial[1]]
    assert sorted(scalar_profile) == sorted(fixture['initial_two_minimum_profile'])
    tables, fiber_rows = comparator_fibers()
    weight_steps = 0
    for case in (1, 2):
        state = initial[case]
        for gate in fixture['known21_suffix']:
            state = inverse_step(state, tuple(gate), tables, 1024)
            assert state is not None
            weight_steps += 1
        assert len(state) == 1 and PAIRS[state[0][0]] == (0, 1)
    assert inverse_step(((PAIRS.index((0, 1)), 10),), (2, 3), tables) is None
    assert inverse_step(((PAIRS.index((0, 1)), 10),), (2, 3), tables, 1024) is not None
    root_data = root_closure(initial[1], tables)
    audited = []
    for record in certificate['closures']:
        if args.index is not None and record['index'] != args.index:
            continue
        report = {'complete': True, 'remaining_queue': 0, 'survivors': [],
                  'trie_nodes': len(record['word']) + 1, 'unique_states': record['states'],
                  'processed_states': record['states'], 'transitions': record['edges'],
                  'pruned_deletion_weight_above512': record['rejected'],
                  'coverage_by_kernel_depth': record['depth_counts'],
                  'state_digest_sha256': record['state_sha256'],
                  'kernel_index_selection': record['index']}
        audited.append(check_closure(report, words[record['index']], initial[1], tables, root_data))
        if len(audited) % 25 == 0:
            print(json.dumps({'kernels_checked': len(audited)}), flush=True)
    assert audited
    if args.index is None:
        assert len(audited) == 153
        assert sum(record['states'] for record in audited) == certificate['total_states']
        assert sum(record['transitions'] for record in audited) == certificate['total_edges']
    result = {'agent': 'six-sorting-1', 'role': 'researcher',
              'fixture_sha256': hashlib.sha256(raw).hexdigest(),
              'kernel_closures_checked': len(audited), 'audited': audited,
              'initial_profiles_identical_across_Y': True,
              'initial_distinct_rank_controls': ranks_checked,
              'scalar_comparator_fiber_rows': fiber_rows,
              'known45_weight_control_steps': weight_steps,
              'weakened_budget_negative_controls': 2, **controls,
              'shared_initial_closure_states': len(root_data[0]),
              'shared_initial_closure_edges_checked_once': root_data[1],
              'transition_checks_with_shared_reuse': sum(record['transitions'] for record in audited) - (len(audited) - 1) * root_data[1],
              'elapsed_seconds': time.monotonic() - start,
              'peak_rss_kib_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'status': 'All selected closed graphs, transition cuts and absence of terminals independently verified.'}
    if args.out:
        args.out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: value for key, value in result.items() if key != 'audited'}))


if __name__ == '__main__':
    main()
