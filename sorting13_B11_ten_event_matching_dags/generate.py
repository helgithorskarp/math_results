"""Exact matching/ideal interface for B11; six-sorting-2, researcher.

The forward marker/profile kernel and base4 quotient adapt six-sorting-1's
bc1675c66ddeb936edbf38d09395420be06f551a source, credited in README.md.
Python3.11+ standard library; integers only; no search truncation.
"""
from collections import Counter, defaultdict, deque
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
GATES = tuple(itertools.combinations(range(11), 2))


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode('ascii')).hexdigest()


def marker_profile(prefix, maximum):
    profile = {}
    for pair in itertools.combinations(range(13), 2):
        marks = sum(1 << p for p in pair)
        depth = 0
        for a, b in prefix:
            A, B = 1 << a, 1 << b
            depth += bool(marks & (A | B))
            if maximum:
                if marks & A and not marks & B: marks ^= A | B
            elif marks & B and not marks & A: marks ^= A | B
        profile[marks] = max(depth, profile.get(marks, -1))
    return tuple(sorted(profile.items()))


def initial_state(fixture):
    vectors = []
    for maximum in (False, True):
        held = 12 if maximum else 0
        weights = [0] * 11
        for marks, depth in marker_profile(fixture['prefix22'], maximum):
            assert marks & (1 << held) and marks.bit_count() == 2 and depth >= 5
            partner = (marks ^ (1 << held)).bit_length() - 2
            assert 0 <= partner < 11
            weights[partner] = 2 ** (depth - 5)
        vectors.append(tuple(weights))
    return *vectors, False


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
    return state == ((16,) + (0,) * 10, (0,) * 10 + (16,), True)


def potential(state):
    low, high, _ = state
    return 2 * sum(bool(w) for w in low + high) + 32 - sum(low + high)


def closure(initial):
    nodes = {initial}
    queue = deque([initial])
    edges = set()
    while queue:
        s = queue.popleft()
        for gate in GATES:
            d = successor(s, gate)
            if d is None: continue
            edges.add((s, gate, d))
            if d != s: assert potential(d) < potential(s)
            if d not in nodes: nodes.add(d); queue.append(d)
    return nodes, edges


def multiset_counts(initial, nodes, edges, remove_first4_binary):
    outgoing = defaultdict(list)
    for s, gate, d in sorted(edges):
        if s == d: continue
        if remove_first4_binary and gate == (4, 10) and s[0][4]:
            assert not s[2] and d[2]
            continue
        outgoing[s].append((GATES.index(gate), d))
    tables = {}
    for s in sorted(nodes, key=potential):
        counts = Counter({0: 1}) if terminal(s) else Counter()
        for label, d in outgoing[s]:
            unit = 1 << (2 * label)
            for code, ways in tables[d].items():
                assert ((code >> (2 * label)) & 3) < 2
                counts[code + unit] += ways
        tables[s] = counts
    return tables[initial]


def decode(code):
    code = int(code)
    assert 0 <= code < (1 << 110)
    counts = tuple((code >> (2 * k)) & 3 for k in range(55))
    assert max(counts) <= 2 and sum(counts) in (10, 11)
    return counts


def class_table(counts):
    return [[str(c), sum(decode(c)), n] for c, n in sorted(counts.items())]


def matchings(ports):
    ports = tuple(sorted(ports))
    if not ports: return [()]
    a = ports[0]
    return [((a, b),) + rest for b in ports[1:]
            for rest in matchings(v for v in ports[1:] if v != b)]


def matching_candidates(include_removed=False):
    """All 108 surviving ten-event classes (or the 135 parent classes).

    Each record supplies actual comparator labels and dependency masks.
    These are effective profile events, not complete Boolean networks.
    """
    records = []
    for p in (1, 2, 3, 4, 6):
        if p == 4 and not include_removed: continue
        for bottom in matchings(set((1, 2, 3, 4, 6)) - {p}):
            roots = (0, p, *[a for a, b in bottom])
            for middle in matchings(roots):
                x, y = middle  # x contains 0 by canonical matching order.
                b1, b2 = bottom
                kind = 'I' if p in x else 'II'
                if kind == 'II' and b1[0] != x[1]: b1, b2 = b2, b1
                z = tuple(sorted(a for a, b in middle))
                for high in matchings((5, 8, 9, 10)):
                    A, B = high if 10 not in high[0] else high[::-1]
                    F = tuple(sorted(b for a, b in high))
                    labels = ((p, 10), b1, b2, x, y, z, (7, 10), A, B, F)
                    assert len(labels) == len(set(labels)) == 10
                    pred = ((0, 0, 0, 1, 6, 24, 1, 0, 64, 384) if kind == 'I'
                            else (0, 0, 0, 2, 5, 24, 1, 0, 64, 384))
                    code = sum(1 << (2 * GATES.index(g)) for g in labels)
                    records.append(dict(code=str(code), first10_partner=p,
                                        kind=kind, labels=labels, predecessor_masks=pred))
    assert len(records) == len({r['code'] for r in records}) == (135 if include_removed else 108)
    return sorted(records, key=lambda r: int(r['code']))


def ideal_graph(fixture, record):
    labels, pred = record['labels'], record['predecessor_masks']
    ideals = {m for m in range(1024)
              if all(not (m >> j & 1) or m & req == req for j, req in enumerate(pred))}
    profiles, choices = {}, {}
    ways = dict.fromkeys(ideals, 0); ways[0] = 1
    for m in sorted(ideals):
        s = initial_state(fixture)
        for j, gate in enumerate(labels):
            if m >> j & 1:
                d = successor(s, gate)
                assert d is not None and d != s
                s = d
        profiles[m] = s
        empty = [a for a in range(11) if not s[0][a] and not s[1][a]]
        assert len(empty) == m.bit_count() - bool(m & 1)
        choices[m] = {gate: m for gate in itertools.combinations(empty, 2)}
        for j, req in enumerate(pred):
            if not (m >> j & 1) and m & req == req:
                dest = m | (1 << j)
                assert dest in ideals and labels[j] not in choices[m]
                choices[m][labels[j]] = dest
                ways[dest] += ways[m]
    assert terminal(profiles[1023])
    return profiles, choices, ways[1023]


def ten_event_interface(fixture, code):
    """Return the complete accepting profile graph for one surviving class.

    Initial state is mask0, terminal is mask1023. A dictionary choice
    gate->same mask is an ordinary comparator that leaves both profiles
    fixed; it remains a real gate in any Boolean sorting search.
    """
    matches = [r for r in matching_candidates() if int(r['code']) == int(code)]
    assert len(matches) == 1, 'Not one of the 108 surviving ten-event classes'
    record = matches[0]
    profiles, choices, count = ideal_graph(fixture, record)
    return record, profiles, choices, count


def quota_graph(fixture, code):
    quota = decode(code)
    root = initial_state(fixture), 0
    nodes = {root}; queue = deque([root]); edges = {}
    while queue:
        q = queue.popleft(); s, used = q; edges[q] = {}
        for k, gate in enumerate(GATES):
            d = successor(s, gate)
            if d is None: continue
            if d == s: next_q = q
            else:
                if ((used >> (2 * k)) & 3) >= quota[k]: continue
                next_q = d, used + (1 << (2 * k))
            edges[q][gate] = next_q
            if next_q not in nodes: nodes.add(next_q); queue.append(next_q)
    terms = {q for q in nodes if q[1] == int(code) and terminal(q[0])}
    assert len(terms) == 1
    incoming = defaultdict(set)
    for q, choices in edges.items():
        for d in choices.values(): incoming[d].add(q)
    core = set(terms); queue = deque(core)
    while queue:
        d = queue.popleft()
        for q in incoming[d]:
            if q not in core: core.add(q); queue.append(q)
    assert root in core
    return nodes, edges, core


def reproduce(fixture):
    initial = initial_state(fixture)
    assert initial == ((4, 2, 2, 2, 2, 0, 2, 0, 0, 0, 1),
                       (0, 0, 0, 0, 0, 4, 0, 2, 4, 4, 1), False)
    nodes, edges = closure(initial)
    old = multiset_counts(initial, nodes, edges, False)
    new = multiset_counts(initial, nodes, edges, True)
    old_table, new_table = class_table(old), class_table(new)
    dropped = sorted(set(old) - set(new))
    slot = GATES.index((4, 10))
    assert dropped == sorted(c for c in old if sum(decode(c)) == 10 and decode(c)[slot])
    assert all(new[c] == old[c] for c in new)
    shapes = Counter((sum(decode(c)), decode(c).count(2)) for c in new)
    assert shapes == {(10, 0): 108, (11, 0): 297, (11, 1): 48}
    factor = matching_candidates(True)
    assert {int(r['code']) for r in factor} == {c for c in old if sum(decode(c)) == 10}
    assert {int(r['code']) for r in factor if r['first10_partner'] != 4} == {c for c in new if sum(decode(c)) == 10}
    summaries, catalogue, bytype = [], [], defaultdict(list)
    for r in factor:
        profiles, choices, ways = ideal_graph(fixture, r)
        all_nodes, quota_edges, core = quota_graph(fixture, r['code'])
        units = [1 << (2 * GATES.index(g)) for g in r['labels']]
        def projection(q):
            s, used = q
            m = sum(1 << j for j, unit in enumerate(units) if used // unit % 4)
            assert used == sum(unit for j, unit in enumerate(units) if m >> j & 1)
            assert m in profiles and s == profiles[m]
            return m
        assert {projection(q) for q in core} == set(profiles) and len(core) == len(profiles)
        actual = {(projection(q), gate, projection(d)) for q in core
                  for gate, d in quota_edges[q].items() if d in core}
        expected = {(m, gate, d) for m in choices for gate, d in choices[m].items()}
        assert actual == expected and ways == old[int(r['code'])]
        effective = sum(m != d for m, gate, d in expected)
        loops = len(expected) - effective
        profile_list = sorted(profiles.items()); edge_list = sorted(expected)
        row = [r['code'], r['first10_partner'], r['kind'], len(profiles), effective,
               loops, ways, len(all_nodes), len(all_nodes - core), digest(profile_list), digest(edge_list)]
        summaries.append(row); bytype[r['kind']].append(row)
        catalogue.append(dict(record=r, profiles=profile_list, edges=edge_list,
                              all_reachable=len(all_nodes), dead_states=len(all_nodes - core)))
    types = {}
    for kind, rows in sorted(bytype.items()):
        assert len({tuple(x[3:7]) for x in rows}) == 1
        r = next(x for x in factor if x['kind'] == kind)
        types[kind] = dict(predecessor_masks=r['predecessor_masks'],
                           classes_before_cut=len(rows), classes_after_cut=sum(x[1] != 4 for x in rows),
                           ideal_states=rows[0][3], effective_edges=rows[0][4],
                           profile_loops=rows[0][5], words_per_class=rows[0][6])
    result = dict(schema='sorting13-ten-event-matching-dags-v1', agent='six-sorting-2', role='researcher',
                  codec='Base4 digits on lexicographic combinations(range(11),2); decimal strings.',
                  parent_profile_states=len(nodes), parent_profile_edges=len(edges),
                  parent_state_sha256=digest(sorted(nodes)), parent_edge_sha256=digest(sorted(edges)),
                  parent_classes=len(old), parent_class_table_sha256=digest(old_table),
                  original_effective_words=sum(old.values()), remaining_classes=len(new),
                  remaining_effective_words=sum(new.values()),
                  remaining_shapes=[[n, repeats, count] for (n, repeats), count in sorted(shapes.items())],
                  filtered_table_sha256=digest(new_table), filtered_table=new_table,
                  dropped_ten_class_codes=list(map(str, dropped)), first_partner_choices=[1, 2, 3, 6],
                  matching_formula='4*3*3*3=108', ten_event_types=types,
                  all135_accepting_graph_summary_sha256=digest(summaries),
                  accepting_graphs_verified=135, repeated_classes_preserved=48,
                  scope='Necessary profile reduction for exact B11 C22/P19 full44; Boolean sorting and arbitrary-prefix coverage remain open.')
    export = dict(parent_states=sorted(nodes), parent_edges=sorted(edges),
                  parent_class_table=old_table, filtered_table=new_table, ten_graphs=catalogue)
    return json.loads(json.dumps(result)), json.loads(json.dumps(export))


def main():
    assert __debug__, 'Run without -O'
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-certificate', action='store_true')
    parser.add_argument('--export', type=Path, help='Private catalogue; never publish this output')
    args = parser.parse_args(); start = time.monotonic()
    fixture = json.loads((HERE / 'fixture.json').read_text())
    result, catalogue = reproduce(fixture)
    path = HERE / 'certificate.json'
    if args.write_certificate:
        assert not path.exists(), 'Certificate creation never overwrites an existing file'
        path.write_text(json.dumps(result, indent=2) + '\n')
    else: assert result == json.loads(path.read_text()), 'Certificate mismatch'
    if args.export:
        args.export.parent.mkdir(parents=True, exist_ok=True)
        args.export.write_text(json.dumps(catalogue, separators=(',', ':')) + '\n')
    print(json.dumps(dict(status='FORWARD_MATCHING_DAG_CERTIFICATE_VERIFIED',
                          classes=result['remaining_classes'], ten_classes=108,
                          accepting_graphs_checked=135, types=result['ten_event_types'],
                          filtered_table_sha256=result['filtered_table_sha256'],
                          seconds=time.monotonic() - start)))


if __name__ == '__main__': main()
