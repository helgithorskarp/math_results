"""Generator-free scalar/full13-inverse check of every obstruction edge.

six-sorting-1, researcher. Inverse-profile core adapts this author's
sourcebc1675c66ddeb936edbf38d09395420be06f551a. Imports no generator,
bit-plane implementation, SAT solver, or private data. Python3.11+.
"""
from collections import Counter, deque
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
GATES = tuple(itertools.combinations(range(11), 2))
PAIRS13 = tuple(itertools.combinations(range(13), 2))


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode('ascii')).hexdigest()


def scalar(values, word):
    result = list(values)
    for a, b in word:
        if result[a] > result[b]: result[a], result[b] = result[b], result[a]
    return result


def witness(pair, maximum):
    others = iter(range(11) if maximum else range(2, 13))
    return [(11 if maximum else 0) + pair.index(i) if i in pair else next(others)
            for i in range(13)]


def marked_run(pair, maximum, word):
    values = witness(pair, maximum); passages = 0
    for a, b in word:
        passages += (values[a] >= 11 or values[b] >= 11) if maximum else (values[a] < 2 or values[b] < 2)
        if values[a] > values[b]: values[a], values[b] = values[b], values[a]
    positions = tuple(i for i, value in enumerate(values) if (value >= 11 if maximum else value < 2))
    return positions, passages, values


def prefix_profile(prefix, maximum):
    result = {}
    for pair in PAIRS13:
        dest, passages, values = marked_run(pair, maximum, prefix)
        result[dest] = max(result.get(dest, -1), passages)
    return tuple(sorted(result.items()))


def inverse_fibers(maximum):
    result = {}
    for gate in GATES:
        fibers = {}
        for pair in PAIRS13:
            dest, passages, values = marked_run(pair, maximum, [(gate[0] + 1, gate[1] + 1)])
            fibers.setdefault(dest, []).append((pair, passages))
        result[gate] = fibers
    return result


def pull_profile(profile, fibers):
    previous = dict(profile); out = {}
    for dest, preimages in fibers.items():
        values = [previous[pair] + passages for pair, passages in preimages if pair in previous]
        if values: out[dest] = max(values)
    return tuple(sorted(out.items()))


def canonical(profile):
    vectors = []
    for pairs, held in [(profile[0], 0), (profile[1], 12)]:
        weights = [0] * 11
        for pair, passages in pairs:
            assert held in pair and passages >= 5
            active = next(p for p in pair if p != held) - 1
            weights[active] = 1 << (passages - 5)
        vectors.append(tuple(weights))
    return *vectors, profile[2]


def rebuild_quota(fixture, entry, fibers):
    index, text_code, events, word_count = entry
    code = int(text_code)
    assert code & 3 == 2 and events == 11 and word_count == 2370
    counts = [(code >> (2 * k)) & 3 for k in range(55)]
    assert sum(counts) == 11 and counts.count(2) == 1 and max(counts) == 2
    prefix = fixture['prefix22']
    profile = prefix_profile(prefix, False), prefix_profile(prefix, True), False
    assert canonical(profile) == (tuple(fixture['initial_low']), tuple(fixture['initial_high']), False)
    root = profile, 0; stack = [root]; nodes = set(); edges = {}
    while stack:
        q = stack.pop()
        if q in nodes: continue
        nodes.add(q); profile, used = q; low, high, touched = profile; choices = {}
        for k, gate in enumerate(GATES):
            if not touched and gate[1] == 10 and gate[0] in (0, 7, 9): continue
            dl, dh = pull_profile(low, fibers[0][gate]), pull_profile(high, fibers[1][gate])
            if sum(1 << d for pair, d in dl) > 512 or sum(1 << d for pair, d in dh) > 512: continue
            dest = dl, dh, touched or gate[1] == 10
            if dest == profile: child = q
            else:
                if ((used >> (2 * k)) & 3) >= counts[k]: continue
                child = dest, used + (1 << (2 * k))
            choices[k] = child
            if child not in nodes: stack.append(child)
        edges[q] = choices
    target = (((((0, 1), 9),), (((11, 12), 9),), True), code)
    assert target in nodes
    # Independent fixed-point coreachability; self loops are never deleted
    # from the underlying graph and do not consume effective multiplicity.
    live = {target}
    while True:
        enlarged = live | {q for q in nodes if any(child in live for child in edges[q].values())}
        if enlarged == live: break
        live = enlarged
    assert root in live
    first_partners = set()
    for q in live:
        low, high, touched = canonical(q[0])
        if touched: continue
        for k, child in edges[q].items():
            if child in live and GATES[k][1] == 10:
                first_partners.add(GATES[k][0]); assert low[GATES[k][0]] == 0 and low[10] > 0
    assert first_partners == {1}

    @lru_cache(None)
    def effective_words(q):
        if q == target: return 1
        return sum(effective_words(child) for child in edges[q].values() if child in live and child != q)

    assert effective_words(root) == word_count == 2370
    return root, nodes, edges, live, target


def verify_fixture(fixture):
    prefix = fixture['prefix22']; assert len(prefix) == 22
    rows = set()
    for number in range(8192):
        values = [(number >> i) & 1 for i in range(13)]
        out = scalar(values, prefix)
        assert out[0] == min(values) and out[12] == max(values)
        rows.add(sum(bit << i for i, bit in enumerate(out[1:12])))
    assert sorted(rows) == fixture['B11_states'] and len(rows) == 158
    assert digest(sorted(rows)) == fixture['canonical_B11_sha256']
    control = fixture['B11_known23_control']; assert len(control) == 23
    for row in rows:
        values = [(row >> i) & 1 for i in range(11)]
        assert scalar(values, control) == sorted(values)
    full = prefix + [[a + 1, b + 1] for a, b in control]
    for number in range(8192):
        values = [(number >> i) & 1 for i in range(13)]
        assert scalar(values, full) == sorted(values)

    initial_ranks = []; assignments = 0
    for f in fixture['families']:
        maximum = f['mode'] == 'max'; held = 12 if maximum else 0
        assert len(f['domains']) == len(f['original_representatives'])
        for pair, domain in zip(f['original_representatives'], f['domains']):
            marked, depth, values = marked_run(pair, maximum, prefix)
            assert depth == f['prefix_D'] and marked == tuple(sorted([held, f['partner'] + 1]))
            other = [i for i in range(13) if i not in pair]; rebuilt = set()
            for assignment in range(2048):
                values = [0] * 13
                for i, position in enumerate(other): values[position] = (assignment >> i) & 1
                for position, v in zip(pair, [2, 3] if maximum else [-2, -1]): values[position] = v
                out = scalar(values, prefix)
                rebuilt.add(sum(int(v >= 1) << i for i, v in enumerate(out[1:12])))
            assignments += 2048
            assert sorted(rebuilt) == domain and all(row in rows for row in domain)
        initial_ranks.append(marked_run(f['original_representatives'][0], maximum, prefix)[2])
    assert len(initial_ranks) == 12 and sum(len(f['domains']) for f in fixture['families']) == 13
    return initial_ranks, assignments


def rebuild_parent_selection(fixture, fibers):
    """Full13 profiles and explicit DFS of all effective parent words.

    The structural six-by-three rule from the generator is not imported.
    This independent traversal checks that no repeated01 class is omitted.
    """
    prefix = fixture['prefix22']
    initial = prefix_profile(prefix, False), prefix_profile(prefix, True), False
    target = (((0, 1), 9),), (((11, 12), 9),), True
    stack = [initial]; nodes = set(); outgoing = {}; edge_count = 0
    while stack:
        state = stack.pop()
        if state in nodes: continue
        nodes.add(state); low, high, touched = state; choices = []
        for label, gate in enumerate(GATES):
            if not touched and gate[1] == 10 and gate[0] in (0, 7, 9): continue
            dl = pull_profile(low, fibers[0][gate])
            dh = pull_profile(high, fibers[1][gate])
            if sum(1 << d for pair, d in dl) > 512 or sum(1 << d for pair, d in dh) > 512: continue
            child = dl, dh, touched or gate[1] == 10
            edge_count += 1
            if child != state: choices.append((label, child))
            if child not in nodes: stack.append(child)
        outgoing[state] = choices
    assert len(nodes) == 2214 and edge_count == 22536 and target in nodes
    visiting = set()

    @lru_cache(None)
    def effective_height(state):
        assert state not in visiting, 'Cycle in the effective parent graph'
        visiting.add(state)
        height = max((1 + effective_height(child) for label, child in outgoing[state]), default=0)
        visiting.remove(state)
        return height

    assert effective_height(initial) == 11
    assert all(effective_height(state) <= 11 for state in nodes)
    classes = Counter(); lengths = Counter()

    def visit(state, used, length):
        if state == target:
            classes[used] += 1; lengths[length] += 1
            return
        for label, child in outgoing[state]:
            assert (used >> (2 * label)) & 3 < 2
            visit(child, used + (1 << (2 * label)), length + 1)

    visit(initial, 0, 0)
    assert len(classes) == 480 and dict(lengths) == {10: 751950, 11: 2266650}
    table = [[str(code), sum(code >> (2*k) & 3 for k in range(55)), count]
             for code, count in sorted(classes.items())]
    assert digest(table) == fixture['parent_class_table_sha256']
    selected = [[i, *row] for i, row in enumerate(table) if int(row[0]) & 3 == 2]
    assert selected == fixture['selected_parent_classes'] and len(selected) == 18
    assert sum(row[3] for row in selected) == 42660
    return {'states': len(nodes), 'edges_including_loops': edge_count,
            'max_effective_path': effective_height(initial),
            'effective_words': sum(classes.values()), 'classes': len(classes),
            'selected_classes': len(selected), 'class_table_sha256': digest(table)}


def check_class(fixture, entry, certificate, initial_ranks, fibers):
    index, code, events, word_count = entry
    root, quota_nodes, quota_edges, live, target = rebuild_quota(fixture, entry, fibers)
    rows = fixture['B11_states']; row_indices = {row: i for i, row in enumerate(rows)}
    families = fixture['families']; words = certificate['representative_words']

    def routes(ranks):
        result = []
        for values, f in zip(ranks, families):
            maximum = f['mode'] == 'max'; held = 12 if maximum else 0
            positions = [i for i, v in enumerate(values) if (v >= 11 if maximum else v < 2)]
            assert held in positions and len(positions) == 2
            result.append(next(i for i in positions if i != held) - 1)
        return tuple(result)

    def obstruction(values, positions, gate):
        a, b = gate
        for j, (p, f) in enumerate(zip(positions, families)):
            if p in (a, b): continue
            for k, domain in enumerate(f['domains']):
                if not any((values[row_indices[row]] >> a & 1) > (values[row_indices[row]] >> b & 1) for row in domain):
                    return j, k
        return None

    def boolean_step(values, gate):
        a, b = gate
        return tuple(value ^ ((1 << a) | (1 << b)) if (value >> a & 1) > (value >> b & 1) else value for value in values)

    def rank_step(ranks, gate):
        return [scalar(values, [[gate[0] + 1, gate[1] + 1]]) for values in ranks]

    states = []; rank_states = []
    for word in words:
        q = root; values = tuple(rows); ranks = initial_ranks
        for label in word:
            assert 0 <= label < 55 and quota_edges[q][label] in live
            gate = GATES[label]; assert obstruction(values, routes(ranks), gate) is None
            q = quota_edges[q][label]
            values, ranks = boolean_step(values, gate), rank_step(ranks, gate)
        states.append((q, values, routes(ranks))); rank_states.append(ranks)
        assert q != target, 'Activity closure reaches the quota target'
    assert words[0] == [] and len(set(states)) == len(states)
    indices = {state: i for i, state in enumerate(states)}
    admitted = rejected = preserving = 0; records = []
    for (q, values, positions), word, ranks in zip(states, words, rank_states):
        outgoing = []; blocked = []
        for label, child in quota_edges[q].items():
            if child not in live: continue
            gate = GATES[label]; bad = obstruction(values, positions, gate)
            if bad is not None:
                blocked.append([label, *bad]); rejected += 1; continue
            dest = child, boolean_step(values, gate), routes(rank_step(ranks, gate))
            assert dest in indices, 'A viable successor is absent from the certificate'
            outgoing.append([label, indices[dest]]); admitted += 1
            preserving += child == q
        records.append({'word': word, 'outgoing': outgoing, 'blocked': blocked})
    visited = set(); queue = deque([0]); shortest = {0: 0}
    while queue:
        node = queue.popleft()
        if node in visited: continue
        visited.add(node)
        for label, child in records[node]['outgoing']:
            if child not in shortest: shortest[child] = shortest[node] + 1
            if child not in visited: queue.append(child)
    assert visited == set(range(len(states)))
    assert all(len(word) == shortest[i] for i, word in enumerate(words))
    visiting = set()

    @lru_cache(None)
    def longest(node):
        assert node not in visiting, 'Cycle in the complete activity graph'
        visiting.add(node)
        length = max((1 + longest(child) for label, child in records[node]['outgoing']), default=0)
        visiting.remove(node)
        return length

    expected = {
        'schema': 'sorting13-repeated01-family-class-v1', 'agent': 'six-sorting-1', 'role': 'researcher',
        'class_code': code, 'parent_class_index_zero_based': index,
        'effective_events': events, 'effective_words': word_count,
        'effective_multiset': [[list(g), int(code) >> (2*k) & 3]
                               for k, g in enumerate(GATES) if int(code) >> (2*k) & 3],
        'quota_reachable_states': len(quota_nodes), 'quota_edges_including_loops': sum(map(len, quota_edges.values())),
        'quota_coreachable_states': len(live),
        'quota_live_edges': sum(child in live for q in live for child in quota_edges[q].values()),
        'activity_domains': sum(len(f['domains']) for f in families), 'activity_states': len(states),
        'admissible_edges': admitted, 'blocked_activity_edges': rejected,
        'shortest_word_length_counts': {str(d): sum(len(word) == d for word in words)
                                        for d in sorted({len(word) for word in words})},
        'longest_admissible_path': longest(0), 'target_reached': False,
        'fixture_sha256': digest(fixture), 'records_sha256': digest(records),
        'representative_words': words,
        'scope': 'Complete closure over every live quota edge, including profile self loops, at arbitrary depth.'
    }
    assert expected == certificate, 'Class certificate mismatch'
    assert longest(0) < 11 and preserving > 0
    return preserving


def main():
    assert sys.flags.optimize == 0, 'Run without -O'
    fixture = json.loads((HERE / 'fixture.json').read_text())
    certificate = json.loads((HERE / 'certificate.json').read_text())
    initial_ranks, assignments = verify_fixture(fixture)
    fibers = inverse_fibers(False), inverse_fibers(True)
    # Check coverage before the class certificates, including omitted or
    # added classes. Every parent word is visited; no beam or depth encoding.
    parent = rebuild_parent_selection(fixture, fibers)
    selected = fixture['selected_parent_classes']; classes = certificate['classes']
    assert len(classes) == len(selected) == 18
    preserving = sum(check_class(fixture, entry, c, initial_ranks, fibers)
                     for entry, c in zip(selected, classes))
    expected = {'schema': 'sorting13-repeated01-family-v1', 'agent': 'six-sorting-1', 'role': 'researcher',
                'fixture_sha256': digest(fixture), 'classes': classes,
                'excluded_parent_classes': 18, 'excluded_effective_words': 42660,
                'max_activity_path': max(c['longest_admissible_path'] for c in classes),
                'parent_class_table_sha256': parent['class_table_sha256'],
                'scope': 'No B11 size22 sorter repeats the internal comparator(0,1). Other classes remain open.'}
    assert expected == certificate, 'Family certificate mismatch'
    assert expected['max_activity_path'] == 8 < 11
    print(json.dumps({'status': 'INDEPENDENT_EIGHTEEN_CLASS_ACTIVITY_OBSTRUCTION_VERIFIED',
                      'classes': len(classes), 'parent': parent,
                      'clamped_assignments_checked': assignments, 'original_boolean_inputs_checked': 8192,
                      'known23_and_full45_control': True,
                      'activity_vertices': sum(c['activity_states'] for c in classes),
                      'admissible_edges': sum(c['admissible_edges'] for c in classes),
                      'blocked_edges': sum(c['blocked_activity_edges'] for c in classes),
                      'profile_preserving_admissible_edges': preserving,
                      'max_activity_path': expected['max_activity_path'],
                      'excluded_effective_words': 42660, 'certificate_sha256': digest(certificate)}))


if __name__ == '__main__': main()
