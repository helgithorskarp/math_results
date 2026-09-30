"""Independent scalar full13 ranks, inverse-fiber DFS, and recursive counting.

six-sorting-1, researcher. Imports no generator or solver. Python3.11+.
Run without -O. Parent P20 exclusion and S11=35 are mathematical imports.
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
    p20, minimum = fixture['prefix20'], fixture['minimum_word']
    prefix = fixture['prefix22']
    assert p20[-1] == [8, 11] and minimum == [[0, 5], [0, 1]]
    assert prefix == p20[:-1] + [[10, 12]] + minimum and len(prefix) == 22
    assert all(set([8, 11]).isdisjoint(g) for g in [[10, 12]] + minimum)
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
    low_inv, high_inv = inverse_fibers(False), inverse_fibers(True)
    initial = original_profile(prefix, False), original_profile(prefix, True), False
    assert total(initial[0]) == total(initial[1]) == 480
    stack, seen, edges = [initial], set(), set()
    outgoing = {}
    while stack:
        s = stack.pop()
        if s in seen: continue
        seen.add(s)
        low, high, flag = s
        outgoing[s] = []
        for gate in GATES:
            if not flag and gate[1] == 10 and gate[0] in (0, 7, 9): continue
            dl, dh = apply_inverse(low, low_inv[gate]), apply_inverse(high, high_inv[gate])
            assert total(dl) >= total(low) and total(dh) >= total(high)
            if total(dl) > 512 or total(dh) > 512: continue
            dest = dl, dh, flag or gate[1] == 10
            edges.add((canonical(s), gate, canonical(dest)))
            outgoing[s].append((gate, dest))
            if dest not in seen: stack.append(dest)
    cstates = sorted(map(canonical, seen))
    cedges = sorted(edges)
    first = [(s, g, d) for s, g, d in cedges if not s[2] and d[2]]
    for s in cstates:
        if s[2]:
            assert sum(s[0]) == sum(s[1]) == 16
            assert not any(a and b for a, b in zip(s[0], s[1]))
    for s, g, d in first:
        assert sum(d[0]) == sum(d[1]) == 16
        assert not any(a and b for a, b in zip(d[0], d[1]))
    terminal_profile = (((0, 1), 9),), (((11, 12), 9),), True
    assert terminal_profile in seen
    # Independent recursive counting uses full13 profiles and detects cycles.
    visiting = set()

    @lru_cache(None)
    def counts(s):
        assert s not in visiting, 'Non-loop cycle'
        visiting.add(s)
        result = Counter({0: 1}) if s == terminal_profile else Counter()
        for gate, dest in outgoing[s]:
            if dest == s: continue
            for degree, count in counts(dest).items(): result[degree + 1] += count
        visiting.remove(s)
        return result

    for s in seen: counts(s)
    assert set(counts(initial)) == {10, 11}
    word = [tuple(g) for g in certificate['terminal_shortest_profile_word']]
    cur = initial
    for gate in word:
        dests = [d for g, d in outgoing[cur] if g == gate]
        assert len(dests) == 1 and dests[0] != cur
        cur = dests[0]
    assert cur == terminal_profile and len(word) == min(counts(initial))
    digest = lambda x: hashlib.sha256(json.dumps(x, separators=(',', ':')).encode('ascii')).hexdigest()
    masks = lambda f: tuple(sorted(((1 << a) | (1 << b), d) for (a, b), d in f))
    checked = {
        'schema': 'sorting13-joint-extrema-v1', 'agent': 'six-sorting-1', 'role': 'researcher',
        'branch': 'B11_158_selected_binary_minimum_branch', 'units': 32,
        'ceiling_per_profile': 16, 'original_marked_pairs_each': 78,
        'initial_full13_profiles': [masks(initial[0]), masks(initial[1])],
        'initial_state': canonical(initial), 'reachable_states': len(seen),
        'edges_including_self_loops': len(edges), 'state_sha256': digest(cstates),
        'edge_sha256': digest(cedges),
        'pre_first_wire10_touch_states': sum(not s[2] for s in seen),
        'first_wire10_touch_edges': len(first),
        'first_partner_edge_counts': {str(p): sum(g[0] == p for s, g, d in first)
                                     for p in (1, 2, 3, 4, 5, 6, 8)},
        'first_split_edge_forms': dict(sorted(Counter('minimum_unary' if s[0][g[0]] == 0 else 'minimum_binary'
                                                    for s, g, d in first).items())),
        'post_split_saturated_disjoint': True,
        'terminal_states': sum(s == terminal_profile for s in seen),
        'terminal_coreachable_states': sum(bool(counts(s)) for s in seen),
        'terminal_effective_word_counts': {str(k): v for k, v in sorted(counts(initial).items())},
        'terminal_shortest_profile_word': word,
        'trust_scope': 'Necessary profile relaxation, not a Boolean sorter or a nonexistence proof.'}
    assert json.loads(json.dumps(checked)) == certificate, 'Certificate mismatch'
    print(json.dumps({'status': 'independent_inverse_certificate_verified', 'states': len(seen),
                      'edges': len(edges), 'original_boolean_inputs_checked': 8192,
                      'effective_word_counts': checked['terminal_effective_word_counts']}))


if __name__ == '__main__': main()
