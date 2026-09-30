"""Forward vector closure and multiset dynamic programming; six-sorting-1.

Profile core adapted from the same author's coupled-profile source65a48340.
Exact integers, standard-library Python3.11+, no operational truncation.
"""
from collections import Counter, deque
import hashlib
import itertools
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
GATES = tuple(itertools.combinations(range(11), 2))

def marker_profile(prefix, maximum):
    profile = {}
    for original in itertools.combinations(range(13), 2):
        marks = (1 << original[0]) | (1 << original[1])
        depth = 0
        for a, b in prefix:
            A, B = 1 << a, 1 << b
            depth += bool(marks & (A | B))
            if maximum:
                if marks & A and not marks & B: marks ^= A | B
            elif marks & B and not marks & A: marks ^= A | B
        profile[marks] = max(depth, profile.get(marks, -1))
    return tuple(sorted(profile.items()))

def reduce_profile(profile, maximum):
    weights = [0] * 11
    held = 12 if maximum else 0
    for marks, depth in profile:
        assert marks & (1 << held) and marks.bit_count() == 2
        partner = (marks ^ (1 << held)).bit_length() - 2
        assert 0 <= partner < 11 and depth >= 5
        weights[partner] = 2 ** (depth - 5)
    return tuple(weights)

def initial_state(fixture):
    profiles = [marker_profile(fixture['prefix22'], maximum) for maximum in (False, True)]
    return (*[reduce_profile(f, bool(i)) for i, f in enumerate(profiles)], False)

def move(weights, gate, maximum):
    a, b = gate
    result = list(weights)
    merged = 2 * max(weights[a], weights[b])
    result[a], result[b] = (0, merged) if maximum else (merged, 0)
    return tuple(result)

def successor(state, gate):
    low, high, touched = state
    if not touched and gate[1] == 10 and gate[0] in (0, 7, 9): return None
    low_out, high_out = move(low, gate, False), move(high, gate, True)
    if sum(low_out) > 16 or sum(high_out) > 16: return None
    return low_out, high_out, touched or gate[1] == 10

def terminal(state):
    low, high, touched = state
    return touched and low == (16,) + (0,) * 10 and high == (0,) * 10 + (16,)

def potential(state):
    low, high, _ = state
    return 2 * sum(bool(w) for w in low + high) + 32 - sum(low + high)

def closure(initial):
    seen = {initial: ()}
    queue = deque([initial])
    edges = set()
    while queue:
        state = queue.popleft()
        for gate in GATES:
            dest = successor(state, gate)
            if dest is None: continue
            edges.add((state, gate, dest))
            if dest != state: assert potential(dest) < potential(state)
            if dest not in seen:
                seen[dest] = seen[state] + (gate,)
                queue.append(dest)
    return seen, edges

def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode('ascii')).hexdigest()


def decode(code):
    code = int(code)
    assert 0 <= code < (1 << 110)
    counts = tuple((code >> (2 * k)) & 3 for k in range(55))
    assert max(counts) <= 2 and sum(counts) in (10, 11)
    return tuple((g, n) for g, n in zip(GATES, counts) if n)


def quotient(initial, seen, edges):
    outgoing = {s: [] for s in seen}
    labels = {g: k for k, g in enumerate(GATES)}
    for source, gate, dest in sorted(edges):
        if source != dest: outgoing[source].append((labels[gate], dest))
    tables = {}
    for s in sorted(seen, key=potential):
        counter = Counter({0: 1}) if terminal(s) else Counter()
        for label, dest in outgoing[s]:
            unit = 1 << (2 * label)
            for code, words in tables[dest].items():
                assert ((code >> (2 * label)) & 3) < 2
                counter[code + unit] += words
        tables[s] = counter
    return tables[initial], sum(map(len, tables.values()))


def build_class_graph(fixture, code):
    """Retain all event orders and arbitrary profile self loops for one class.

    Quotas are multiplicities, so a repeated effective comparator is counted
    twice. A comparison that changes neither profile never spends a quota.
    Boolean sorting constraints must be supplied separately by a caller.
    """
    code = int(code)
    decode(code)
    initial = initial_state(fixture), 0
    seen = {initial};queue = deque([initial]);edges = {}
    while queue:
        state = queue.popleft();profile, used = state;choices = {}
        for k, gate in enumerate(GATES):
            dest_profile = successor(profile, gate)
            if dest_profile is None: continue
            if dest_profile == profile: dest = state
            else:
                if ((used >> (2 * k)) & 3) >= ((code >> (2 * k)) & 3): continue
                dest = dest_profile, used + (1 << (2 * k))
            choices[k] = dest
            if dest not in seen: seen.add(dest);queue.append(dest)
        edges[state] = choices
    terms = {s for s in seen if s[1] == code and terminal(s[0])}
    assert len(terms) == 1, 'Not a terminal quotient class'
    return initial, seen, edges, terms


def reproduce(fixture):
    initial = initial_state(fixture)
    seen, edges = closure(initial)
    counter, cached = quotient(initial, seen, edges)
    entries = [];lengths = Counter();shapes = Counter();word_counts = Counter()
    for code, words in sorted(counter.items()):
        multiplicities = [n for gate, n in decode(code)]
        length = sum(multiplicities);repeats = multiplicities.count(2)
        assert repeats <= 1 and (length != 10 or repeats == 0)
        entries.append([str(code), length, words])
        lengths[length] += 1;shapes[(length, repeats)] += 1;word_counts[length] += words
    cur = initial;code = 0
    for gate in map(tuple, fixture['repeated_gate_profile_word']):
        dest = successor(cur, gate)
        assert dest is not None and dest != cur
        code += 1 << (2 * GATES.index(gate));cur = dest
    assert terminal(cur) and code in counter
    # Exercise the quota-aware helper on a class that repeats a comparator.
    _, nodes, transitions, terms = build_class_graph(fixture, code)
    assert len(terms) == 1
    result = {'schema': 'sorting13-multiset-quotient-v1', 'agent': 'six-sorting-1', 'role': 'researcher',
              'codec': 'Two bits per comparator in lexicographic combinations(range(11),2); decimal strings.',
              'classes': len(counter), 'counts_by_effective_events': {str(k): v for k, v in sorted(lengths.items())},
              'multiplicity_shapes': [[length, repeats, n] for (length, repeats), n in sorted(shapes.items())],
              'effective_word_counts': {str(k): v for k, v in sorted(word_counts.items())},
              'total_effective_words': sum(counter.values()), 'total_cached_class_entries': cached,
              'parent_reachable_states': len(seen), 'parent_edges_including_loops': len(edges),
              'parent_state_sha256': digest(sorted(seen)), 'parent_edge_sha256': digest(sorted(edges)),
              'class_table_sha256': digest(entries), 'class_table': entries,
              'repeated_word_class_code': str(code),
              'repeated_class_graph_states': len(nodes),
              'repeated_class_graph_edges': sum(map(len, transitions.values())),
              'scope': 'Necessary B11/P19 profile partition, not a sorter or a nonexistence result.'}
    return json.loads(json.dumps(result))


def main():
    assert sys.flags.optimize == 0, 'Run without -O'
    fixture = json.loads((HERE / 'fixture.json').read_text())
    result = reproduce(fixture)
    path = HERE / 'certificate.json'
    if path.exists(): assert result == json.loads(path.read_text()), 'Certificate mismatch'
    else: path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': 'forward_multiset_quotient_verified', 'classes': result['classes'],
                      'event_counts': result['counts_by_effective_events'],
                      'effective_words': result['total_effective_words'],
                      'class_table_sha256': result['class_table_sha256']}))


if __name__ == '__main__': main()
