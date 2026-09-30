"""Independent original ranks/inverse graph and explicit all-word DFS.

Profile core adapted from the same author's independent checker65a48340.
Imports no generator or solver. Standard-library Python3.11+, no -O.
"""
from collections import Counter
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PAIRS13 = tuple(itertools.combinations(range(13), 2))
GATES = tuple(itertools.combinations(range(11), 2))

def witness(pair, maximum):
    other = iter(range(11) if maximum else range(2, 13))
    return [(11 if maximum else 0) + pair.index(i) if i in pair else next(other)
            for i in range(13)]

def scalar(values, gates, maximum=None):
    values = list(values)
    passages = 0
    for a, b in gates:
        if maximum is not None:
            passages += (values[a] >= 11 or values[b] >= 11) if maximum else (values[a] < 2 or values[b] < 2)
        if values[a] > values[b]: values[a], values[b] = values[b], values[a]
    if maximum is None: return values
    marked = tuple(i for i, v in enumerate(values) if (v >= 11 if maximum else v < 2))
    assert len(marked) == 2
    return marked, passages

def original_profile(prefix, maximum):
    result = {}
    for pair in PAIRS13:
        dest, d = scalar(witness(pair, maximum), prefix, maximum)
        result[dest] = max(result.get(dest, -1), d)
    return tuple(sorted(result.items()))

def inverse_fibers(maximum):
    result = {}
    for gate in GATES:
        fibers = {}
        for pair in PAIRS13:
            dest, d = scalar(witness(pair, maximum), [(gate[0] + 1, gate[1] + 1)], maximum)
            fibers.setdefault(dest, []).append((pair, d))
        assert all(len(pre) <= 2 for pre in fibers.values())
        assert all(d == 1 for pre in fibers.values() if len(pre) == 2 for pair, d in pre)
        result[gate] = fibers
    return result

def apply_inverse(profile, fibers):
    previous = dict(profile)
    out = {}
    for dest, pre in fibers.items():
        values = [previous[pair] + d for pair, d in pre if pair in previous]
        if values: out[dest] = max(values)
    return tuple(sorted(out.items()))

def total(profile): return sum(1 << d for pair, d in profile)

@lru_cache(None)
def canonical(state):
    low, high, flag = state
    vectors = []
    for profile, held in [(low, 0), (high, 12)]:
        weights = [0] * 11
        for pair, d in profile:
            assert held in pair and d >= 5
            active = next(p for p in pair if p != held) - 1
            assert 0 <= active < 11
            weights[active] = 1 << (d - 5)
        vectors.append(tuple(weights))
    return *vectors, flag


def main():
    assert sys.flags.optimize == 0, 'Run without -O'
    fixture = json.loads((HERE / 'fixture.json').read_text())
    certificate = json.loads((HERE / 'certificate.json').read_text())
    p20, minimum, prefix = fixture['prefix20'], fixture['minimum_word'], fixture['prefix22']
    assert p20[-1] == [8, 11] and minimum == [[0, 5], [0, 1]]
    assert prefix == p20[:-1] + [[10, 12]] + minimum and len(prefix) == 22
    rows = set()
    for x in range(8192):
        bits = [(x >> i) & 1 for i in range(13)]
        output = scalar(bits, prefix)
        assert output[0] == min(bits) and output[12] == max(bits)
        rows.add(sum(v << i for i, v in enumerate(output[1:12])))
    assert sorted(rows) == fixture['B11_states'] and len(rows) == 158
    known = fixture['B11_known23_control']
    assert len(known) == 23
    for row in rows:
        out = scalar([(row >> i) & 1 for i in range(11)], known)
        assert out == sorted(out)

    inverses = inverse_fibers(False), inverse_fibers(True)
    initial = original_profile(prefix, False), original_profile(prefix, True), False
    assert total(initial[0]) == total(initial[1]) == 480
    stack, seen, outgoing, edges = [initial], set(), {}, set()
    while stack:
        s = stack.pop()
        if s in seen: continue
        seen.add(s); low, high, touched = s; outgoing[s] = []
        for k, gate in enumerate(GATES):
            if not touched and gate[1] == 10 and gate[0] in (0, 7, 9): continue
            dl = apply_inverse(low, inverses[0][gate])
            dh = apply_inverse(high, inverses[1][gate])
            assert total(dl) >= total(low) and total(dh) >= total(high)
            if total(dl) > 512 or total(dh) > 512: continue
            dest = dl, dh, touched or gate[1] == 10
            outgoing[s].append((k, dest))
            edges.add((canonical(s), gate, canonical(dest)))
            if dest not in seen: stack.append(dest)
    target = (((0, 1), 9),), (((11, 12), 9),), True
    assert target in seen
    for s in seen:
        low, high, touched = canonical(s)
        if touched:
            assert sum(low) == sum(high) == 16
            assert not any(a and b for a, b in zip(low, high))

    # Enumerate every terminal effective word, not a DP of path counts.
    classes, lengths = Counter(), Counter()
    effective = {s: [(k, d) for k, d in outgoing[s] if d != s] for s in seen}

    def walk(s, code, length):
        if s == target:
            classes[code] += 1; lengths[length] += 1
            return
        assert length < 11, 'A non-loop path is too long or cyclic'
        for k, dest in effective[s]:
            assert ((code >> (2 * k)) & 3) < 2
            walk(dest, code + (1 << (2 * k)), length + 1)

    walk(initial, 0, 0)
    entries, event_lengths, shapes = [], Counter(), Counter()
    for code, words in sorted(classes.items()):
        digits = [(code >> (2 * k)) & 3 for k in range(55)]
        length, repeats = sum(digits), digits.count(2)
        assert code < (1 << 110) and max(digits) <= 2 and repeats <= 1
        assert length in (10, 11) and (length != 10 or repeats == 0)
        entries.append([str(code), length, words])
        event_lengths[length] += 1; shapes[(length, repeats)] += 1

    # Separately count distinct suffix multisets at all full13 states.
    visiting = set()

    @lru_cache(None)
    def suffix_classes(s):
        assert s not in visiting, 'Non-loop cycle'
        visiting.add(s)
        result = {0} if s == target else set()
        for k, dest in effective[s]:
            for code in suffix_classes(dest):
                assert ((code >> (2 * k)) & 3) < 2
                result.add(code + (1 << (2 * k)))
        visiting.remove(s)
        return frozenset(result)

    assert suffix_classes(initial) == classes.keys()
    cached_entries = sum(len(suffix_classes(s)) for s in seen)
    repeated_word = [tuple(g) for g in fixture['repeated_gate_profile_word']]
    cur, repeated_code = initial, 0
    for gate in repeated_word:
        k = GATES.index(gate)
        dests = [d for label, d in outgoing[cur] if label == k]
        assert len(dests) == 1 and dests[0] != cur
        cur = dests[0]; repeated_code += 1 << (2 * k)
    assert cur == target and repeated_code in classes
    repeats = [g for g, n in Counter(repeated_word).items() if n == 2]
    assert len(repeats) == 1
    split = next(i for i, g in enumerate(repeated_word) if g[1] == 10)
    positions = [i for i, g in enumerate(repeated_word) if g == repeats[0]]
    assert positions[0] < split < positions[1]

    # Independently reconstruct the quota graph on full13 inverse profiles.
    root = initial, 0; quota_seen = set(); stack = [root]; quota_edges = 0
    terminals = set()
    while stack:
        q = stack.pop()
        if q in quota_seen: continue
        quota_seen.add(q); s, used = q
        if s == target and used == repeated_code: terminals.add(q)
        for k, dest_profile in outgoing[s]:
            if dest_profile == s: dest = q
            else:
                if ((used >> (2 * k)) & 3) >= ((repeated_code >> (2 * k)) & 3): continue
                dest = dest_profile, used + (1 << (2 * k))
            quota_edges += 1
            if dest not in quota_seen: stack.append(dest)
    assert len(terminals) == 1
    digest = lambda x: hashlib.sha256(json.dumps(x, separators=(',', ':')).encode('ascii')).hexdigest()
    checked = {
        'schema': 'sorting13-multiset-quotient-v1', 'agent': 'six-sorting-1', 'role': 'researcher',
        'codec': 'Two bits per comparator in lexicographic combinations(range(11),2); decimal strings.',
        'classes': len(classes), 'counts_by_effective_events': {str(k): v for k, v in sorted(event_lengths.items())},
        'multiplicity_shapes': [[length, repeats, n] for (length, repeats), n in sorted(shapes.items())],
        'effective_word_counts': {str(k): v for k, v in sorted(lengths.items())},
        'total_effective_words': sum(classes.values()), 'total_cached_class_entries': cached_entries,
        'parent_reachable_states': len(seen), 'parent_edges_including_loops': len(edges),
        'parent_state_sha256': digest(sorted(map(canonical, seen))), 'parent_edge_sha256': digest(sorted(edges)),
        'class_table_sha256': digest(entries), 'class_table': entries,
        'repeated_word_class_code': str(repeated_code),
        'repeated_class_graph_states': len(quota_seen), 'repeated_class_graph_edges': quota_edges,
        'scope': 'Necessary B11/P19 profile partition, not a sorter or a nonexistence result.'}
    assert checked == certificate, 'Certificate mismatch'
    print(json.dumps({'status': 'independent_full13_multiset_certificate_verified',
                      'classes': len(classes), 'effective_words_enumerated': sum(classes.values()),
                      'original_boolean_inputs_checked': 8192, 'class_table_sha256': digest(entries)}))


if __name__ == '__main__': main()
