"""Exact forward joint-profile closure; six-sorting-1, researcher.

Python3.11+ standard library, integer arithmetic, no operational truncation.
Import this file to obtain initial_state(), successor(), and closure().
The relaxation is necessary for the specified full44 branch, not sufficient.
"""
from collections import Counter, deque
import hashlib
import itertools
import json
from pathlib import Path

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


def summarize(fixture, seen, edges):
    states = sorted(seen)
    outgoing = {s: [] for s in states}
    for source, gate, dest in sorted(edges): outgoing[source].append((gate, dest))
    first = [(s, g, d) for s, g, d in edges if not s[2] and d[2]]
    # This stronger invariant is checked for every state and every entry edge.
    for s in states:
        if s[2]:
            assert sum(s[0]) == sum(s[1]) == 16
            assert not any(a and b for a, b in zip(s[0], s[1]))
    for s, g, d in first:
        assert sum(d[0]) == sum(d[1]) == 16
        assert not any(a and b for a, b in zip(d[0], d[1]))
    # Ignore profile self loops, while retaining every non-loop gate label.
    # Strict potential decrease makes the resulting graph acyclic.
    polynomials = {}
    for s in sorted(states, key=potential):
        poly = Counter({0: 1}) if terminal(s) else Counter()
        for gate, d in outgoing[s]:
            if d == s: continue
            for degree, count in polynomials[d].items(): poly[degree + 1] += count
        polynomials[s] = poly
    initial = initial_state(fixture)
    terms = [s for s in states if terminal(s)]
    split_cases = Counter('minimum_unary' if s[0][g[0]] == 0 else 'minimum_binary'
                          for s, g, d in first)
    profiles = [marker_profile(fixture['prefix22'], maximum) for maximum in (False, True)]
    result = {
        'schema': 'sorting13-joint-extrema-v1', 'agent': 'six-sorting-1', 'role': 'researcher',
        'branch': 'B11_158_selected_binary_minimum_branch', 'units': 32,
        'ceiling_per_profile': 16, 'original_marked_pairs_each': 78,
        'initial_full13_profiles': profiles, 'initial_state': initial,
        'reachable_states': len(states), 'edges_including_self_loops': len(edges),
        'state_sha256': digest(states), 'edge_sha256': digest(sorted(edges)),
        'pre_first_wire10_touch_states': sum(not s[2] for s in states),
        'first_wire10_touch_edges': len(first),
        'first_partner_edge_counts': {str(p): sum(g[0] == p for s, g, d in first)
                                     for p in (1, 2, 3, 4, 5, 6, 8)},
        'first_split_edge_forms': dict(sorted(split_cases.items())),
        'post_split_saturated_disjoint': True,
        'terminal_states': len(terms),
        'terminal_coreachable_states': sum(bool(poly) for poly in polynomials.values()),
        'terminal_effective_word_counts': {str(k): v for k, v in sorted(polynomials[initial].items())},
        'terminal_shortest_profile_word': seen[terms[0]],
        'trust_scope': 'Necessary profile relaxation, not a Boolean sorter or a nonexistence proof.'}
    assert set(polynomials[initial]) == {10, 11}
    return json.loads(json.dumps(result))


def main():
    fixture = json.loads((HERE / 'fixture.json').read_text())
    seen, edges = closure(initial_state(fixture))
    result = summarize(fixture, seen, edges)
    path = HERE / 'certificate.json'
    if path.exists():
        assert result == json.loads(path.read_text()), 'Certificate mismatch'
        print(json.dumps({'status': 'forward_certificate_matches', 'states': len(seen),
                          'edges': len(edges), 'effective_word_counts': result['terminal_effective_word_counts']}))
    else:
        path.write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps({'status': 'certificate_generated', 'states': len(seen), 'edges': len(edges)}))


if __name__ == '__main__': main()
