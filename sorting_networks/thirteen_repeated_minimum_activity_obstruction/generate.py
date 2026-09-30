"""Exact activity obstruction in one eleven-event B11 multiset class.

six-sorting-1, researcher. Profile/quota core adapts this author's source
bc1675c66ddeb936edbf38d09395420be06f551a. Activity domains/theorem are from
six-sorting-2 source1d55b42316153c7a6a213efb60016f71f3719262.
No solver, beam width, depth cutoff, or Boolean final-sorting assumption.
"""
from collections import deque
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
GATES = tuple(itertools.combinations(range(11), 2))


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode('ascii')).hexdigest()


def move(weights, gate, maximum):
    a, b = gate; result = list(weights)
    w = 2 * max(weights[a], weights[b])
    result[a], result[b] = (0, w) if maximum else (w, 0)
    return tuple(result)


def next_profile(profile, gate):
    low, high, touched = profile
    if not touched and gate[1] == 10 and gate[0] in (0, 7, 9): return None
    low_out, high_out = move(low, gate, False), move(high, gate, True)
    if sum(low_out) > 16 or sum(high_out) > 16: return None
    return low_out, high_out, touched or gate[1] == 10


def quota_graph(fixture):
    code = int(fixture['class_code'])
    digits = tuple((code >> (2 * k)) & 3 for k in range(55))
    assert sum(digits) == 11 and digits.count(2) == 1 and max(digits) == 2
    assert digits[GATES.index((0, 1))] == 2
    initial = (tuple(fixture['initial_low']), tuple(fixture['initial_high']), False), 0
    queue = deque([initial]); seen = {initial}; edges = {}
    while queue:
        node = queue.popleft(); profile, used = node; choices = {}
        for k, gate in enumerate(GATES):
            dest = next_profile(profile, gate)
            if dest is None: continue
            if dest == profile: child = node
            else:
                if ((used >> (2 * k)) & 3) >= digits[k]: continue
                child = dest, used + (1 << (2 * k))
            choices[k] = child
            if child not in seen: seen.add(child); queue.append(child)
        edges[node] = choices
    target = ((16,) + (0,) * 10, (0,) * 10 + (16,), True), code
    assert target in seen
    reverse = {q: set() for q in seen}
    for q, choices in edges.items():
        for child in choices.values(): reverse[child].add(q)
    live = {target}; queue = deque([target])
    while queue:
        for previous in reverse[queue.popleft()]:
            if previous not in live: live.add(previous); queue.append(previous)
    assert initial in live
    # The tiny minimum10 family is saturated because every completable
    # first10 event here is minimum-unary. This is checked, not assumed.
    first = []
    for q in live:
        if q[0][2]: continue
        for k, child in edges[q].items():
            if child not in live or GATES[k][1] != 10: continue
            assert q[0][0][GATES[k][0]] == 0 and q[0][0][10] > 0
            first.append(GATES[k][0])
    assert set(first) == {1}
    return initial, seen, edges, live, target


def reproduce(fixture):
    initial, quota_nodes, quota_edges, live, target = quota_graph(fixture)
    rows = fixture['B11_states']; assert len(rows) == 158
    families = fixture['families']; assert len(families) == 12
    row_index = {row: i for i, row in enumerate(rows)}
    domains = tuple(tuple(sum(1 << row_index[row] for row in domain) for domain in f['domains'])
                    for f in families)
    wires = tuple(sum(((row >> i) & 1) << j for j, row in enumerate(rows)) for i in range(11))
    root = initial, wires, tuple(f['partner'] for f in families)
    positions = {root: 0}; states = [root]; words = [[]]; records = []
    queue = deque([root]); rejected = 0; admitted = 0
    while queue:
        state = queue.popleft(); index = positions[state]
        q, wires, routes = state; outgoing = []; blocked = []
        assert q != target, 'Activity-obligations language reaches the quota target'
        for label, dest in quota_edges[q].items():
            if dest not in live: continue
            a, b = GATES[label]; swaps = wires[a] & ~wires[b]
            bad = None
            for j, (route, ds) in enumerate(zip(routes, domains)):
                if route in (a, b): continue
                for k, domain in enumerate(ds):
                    if not swaps & domain: bad = j, k; break
                if bad is not None: break
            if bad is not None:
                blocked.append([label, *bad]); rejected += 1; continue
            after = list(wires)
            after[a], after[b] = wires[a] & wires[b], wires[a] | wires[b]
            next_routes = tuple((b if f['mode'] == 'max' else a) if route in (a, b) else route
                                for route, f in zip(routes, families))
            child = dest, tuple(after), next_routes
            if child not in positions:
                positions[child] = len(states); states.append(child)
                words.append(words[index] + [label]); queue.append(child)
            outgoing.append([label, positions[child]]); admitted += 1
        assert index == len(records)
        records.append({'word': words[index], 'outgoing': outgoing, 'blocked': blocked})

    # Count all paths, not only shortest representative lengths, and expose
    # cycles if there were any. The empty next frontier is not a beam result.
    visiting = set()

    @lru_cache(None)
    def depth(index):
        assert index not in visiting, 'Activity graph contains a cycle'
        visiting.add(index)
        result = max((1 + depth(child) for label, child in records[index]['outgoing']), default=0)
        visiting.remove(index)
        return result

    longest = depth(0)
    levels = {d: sum(len(r['word']) == d for r in records)
              for d in sorted({len(r['word']) for r in records})}
    result = {
        'schema': 'sorting13-repeated-activity-obstruction-v1',
        'agent': 'six-sorting-1', 'role': 'researcher',
        'class_code': fixture['class_code'], 'parent_class_index_zero_based': 0,
        'effective_multiset': [[list(g), (int(fixture['class_code']) >> (2 * k)) & 3]
                               for k, g in enumerate(GATES) if (int(fixture['class_code']) >> (2 * k)) & 3],
        'quota_reachable_states': len(quota_nodes),
        'quota_edges_including_loops': sum(map(len, quota_edges.values())),
        'quota_coreachable_states': len(live),
        'quota_live_edges': sum(child in live for q in live for child in quota_edges[q].values()),
        'activity_domains': sum(map(len, domains)), 'activity_states': len(states),
        'admissible_edges': admitted, 'blocked_activity_edges': rejected,
        'shortest_word_length_counts': levels, 'longest_admissible_path': longest,
        'target_reached': False, 'fixture_sha256': digest(fixture),
        'records_sha256': digest(records), 'records': records,
        'scope': 'This one effective multiset cannot occur in a B11 size22 sorter. All comparator orders and arbitrarily placed profile self loops are covered; other classes remain open.'
    }
    return json.loads(json.dumps(result))


def main():
    assert sys.flags.optimize == 0, 'Run without -O'
    fixture = json.loads((HERE / 'fixture.json').read_text())
    result = reproduce(fixture)
    path = HERE / 'certificate.json'
    if path.exists(): assert result == json.loads(path.read_text()), 'Certificate mismatch'
    else: path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['class_code', 'activity_states', 'admissible_edges', 'blocked_activity_edges', 'longest_admissible_path', 'target_reached', 'records_sha256']}))


if __name__ == '__main__': main()
