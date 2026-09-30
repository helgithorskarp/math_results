"""Independent scalar/inverse-fiber audit; six-sorting-2, researcher.

No generator imports. Rebuilds full thirteen-wire marked-pair depths, explicitly
enumerates every effective word, and constructs every ten-class quota graph.
Pairings are enumerated by permutations, dependencies by root producers.
Python3.11+ standard library; integers only; no cutoffs or solver assumptions.
"""
from collections import Counter, defaultdict, deque
from functools import lru_cache
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import resource
import time

HERE = Path(__file__).resolve().parent
PAIRS13 = tuple(itertools.combinations(range(13), 2))
GATES = tuple(itertools.combinations(range(11), 2))


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode('ascii')).hexdigest()


def scalar(values, word):
    values = list(values)
    for a, b in word:
        if values[a] > values[b]: values[a], values[b] = values[b], values[a]
    return values


def marked(pair, word, maximum):
    values = list(range(2, 15))
    values[pair[0]], values[pair[1]] = (20, 21) if maximum else (-2, -1)
    depth = 0
    for a, b in word:
        depth += int(any((values[p] > 15 if maximum else values[p] < 0) for p in (a, b)))
        if values[a] > values[b]: values[a], values[b] = values[b], values[a]
    positions = tuple(p for p, v in enumerate(values) if (v > 15 if maximum else v < 0))
    assert len(positions) == 2
    return positions, depth


def canonical(state):
    vectors = []
    for profile, held in ((state[0], 0), (state[1], 12)):
        weights = [0] * 11
        for pair, depth in profile:
            assert held in pair and depth >= 5
            p = next(v for v in pair if v != held) - 1
            assert 0 <= p < 11
            weights[p] = 2 ** (depth - 5)
        vectors.append(tuple(weights))
    return *vectors, state[2]


def decode(code):
    code = int(code); digits = []
    for k in range(55): code, digit = divmod(code, 4); digits.append(digit)
    assert code == 0 and max(digits) <= 2
    return digits


def independent_profiles(fixture):
    initial_profiles = []; fibers = []
    for maximum in (False, True):
        depths = {}
        for pair in PAIRS13:
            after, depth = marked(pair, fixture['prefix22'], maximum)
            depths[after] = max(depths.get(after, -1), depth)
        initial_profiles.append(tuple(sorted(depths.items())))
        inverse = {}
        for gate in GATES:
            buckets = defaultdict(list)
            for pair in PAIRS13:
                after, charge = marked(pair, [(gate[0] + 1, gate[1] + 1)], maximum)
                buckets[after].append((pair, charge))
            assert all(len(v) <= 2 for v in buckets.values())
            assert all(d == 1 for v in buckets.values() if len(v) == 2 for pair, d in v)
            inverse[gate] = buckets
        fibers.append(inverse)
    @lru_cache(None)
    def transport(profile, gate, mode):
        old = dict(profile); new = {}
        for after, preimages in fibers[mode][gate].items():
            depths = [old[pair] + charge for pair, charge in preimages if pair in old]
            if depths: new[after] = max(depths)
        return tuple(sorted(new.items()))
    mass = lambda profile: sum(2 ** depth for pair, depth in profile)
    initial = *initial_profiles, False
    assert mass(initial[0]) == mass(initial[1]) == 480
    nodes = {initial}; todo = [initial]; outgoing = {}; edge_set = set()
    def potential(s):
        return 2 * (len(s[0]) + len(s[1])) + 32 - (mass(s[0]) + mass(s[1])) // 32
    while todo:
        s = todo.pop(); outgoing[s] = {}
        assert (5, 12) not in dict(s[1]) and (11, 12) in dict(s[1])
        for gate in GATES:
            if not s[2] and gate[1] == 10 and gate[0] in (0, 7, 9): continue
            d = transport(s[0], gate, 0), transport(s[1], gate, 1), s[2] or gate[1] == 10
            if mass(d[0]) > 512 or mass(d[1]) > 512: continue
            outgoing[s][gate] = d
            edge_set.add((canonical(s), gate, canonical(d)))
            if gate == (4, 10): assert not s[2] and d[2]
            if d != s: assert potential(d) < potential(s)
            if d not in nodes: nodes.add(d); todo.append(d)
    target = (((0, 1), 9),), (((11, 12), 9),), True
    assert target in nodes
    return initial, target, nodes, outgoing, edge_set


def enumerate_words(initial, target, outgoing):
    transitions = {s: [(GATES.index(g), d, g == (4, 10) and (0, 5) in dict(s[0]))
                       for g, d in choices.items() if s != d] for s, choices in outgoing.items()}
    old, new = Counter(), Counter(); degrees = {}; counts = [0] * 55
    units = [4 ** k for k in range(55)]
    def walk(s, code, length, rejected):
        if s == target:
            old[code] += 1
            if not rejected: new[code] += 1
            if code in degrees: assert degrees[code] == length
            else: degrees[code] = length
            return
        for k, d, bad in transitions[s]:
            counts[k] += 1
            assert counts[k] <= 2
            walk(d, code + units[k], length + 1, rejected or bad)
            counts[k] -= 1
    walk(initial, 0, 0, False)
    for code in old:
        digits = decode(code)
        assert sum(digits) == degrees[code] and degrees[code] in (10, 11)
        assert digits.count(2) <= 1 and (degrees[code] != 10 or not digits.count(2))
    return old, new


def pairings(ports):
    ports = tuple(ports)
    assert len(ports) == 4 and len(set(ports)) == 4
    return sorted({tuple(sorted((tuple(sorted(v[:2])), tuple(sorted(v[2:])))))
                   for v in itertools.permutations(ports)})


def independent_factors():
    records = []
    for p in (1, 2, 3, 4, 6):
        for bottom in pairings(set((1, 2, 3, 4, 6)) - {p}):
            roots = (0, p, *[g[0] for g in bottom])
            for middle in pairings(roots):
                x = next(g for g in middle if 0 in g); y = next(g for g in middle if 0 not in g)
                kind = 'I' if p in x else 'II'
                low_pairs = list(bottom)
                if kind == 'II': low_pairs.sort(key=lambda g: g[0] != x[1])
                b1, b2 = low_pairs
                z = tuple(sorted(g[0] for g in middle))
                for high in pairings((5, 8, 9, 10)):
                    A = next(g for g in high if 10 not in g)
                    B = next(g for g in high if 10 in g)
                    F = tuple(sorted(g[1] for g in high))
                    labels = ((p, 10), b1, b2, x, y, z, (7, 10), A, B, F)
                    assert len(set(labels)) == 10
                    # Derive dependencies from the events producing each root.
                    producer = {p: 0, b1[0]: 1, b2[0]: 2}
                    pred = [0] * 10
                    for j in (3, 4):
                        pred[j] = sum(1 << producer[v] for v in labels[j] if v in producer)
                    pred[5] = (1 << 3) + (1 << 4)
                    pred[6] = 1 << 0
                    pred[8] = 1 << 6
                    pred[9] = (1 << 7) + (1 << 8)
                    code = sum(4 ** GATES.index(g) for g in labels)
                    records.append(dict(code=str(code), first10_partner=p, kind=kind,
                                        labels=labels, predecessor_masks=tuple(pred)))
    assert len(records) == len({r['code'] for r in records}) == 135
    return sorted(records, key=lambda r: int(r['code']))


def audit_class(record, initial, target, outgoing):
    labels = record['labels']; required = record['predecessor_masks']
    ideals = {m for m in range(1024)
              if all(not (m >> j & 1) or m & need == need for j, need in enumerate(required))}
    profiles = {}
    for m in ideals:
        s = initial; used = 0
        # Choose the greatest ready event, unlike the generator's index order.
        while used != m:
            ready = [j for j, need in enumerate(required)
                     if m >> j & 1 and not (used >> j & 1) and used & need == need]
            assert ready
            gate = labels[max(ready)]; d = outgoing[s].get(gate)
            assert d is not None and d != s
            s = d; used |= 1 << max(ready)
        profiles[m] = s
    expected = set()
    for m, s in profiles.items():
        loops = {g for g, d in outgoing[s].items() if d == s}
        occupied = {v - 1 for profile, held in ((s[0], 0), (s[1], 12))
                    for pair, depth in profile for v in pair if v != held}
        empty = set(range(11)) - occupied
        assert len(empty) == m.bit_count() - int(bool(m & 1))
        assert loops == set(itertools.combinations(sorted(empty), 2))
        expected.update((m, gate, m) for gate in loops)
        for j, need in enumerate(required):
            if not (m >> j & 1) and m & need == need:
                dest = m | (1 << j)
                assert outgoing[s].get(labels[j]) == profiles[dest]
                expected.add((m, labels[j], dest))
    @lru_cache(None)
    def count_orders(m):
        if m == 1023: return 1
        return sum(count_orders(m | (1 << j)) for j, need in enumerate(required)
                   if not (m >> j & 1) and m & need == need)
    all_labels = frozenset(labels)
    root = initial, frozenset()
    nodes = {root}; todo = [root]; qedges = {}; incoming = defaultdict(set)
    while todo:
        q = todo.pop(); s, used = q; qedges[q] = {}
        for gate, d in outgoing[s].items():
            if s == d: next_q = q
            elif gate in all_labels and gate not in used: next_q = d, used | {gate}
            else: continue
            qedges[q][gate] = next_q; incoming[next_q].add(q)
            if next_q not in nodes: nodes.add(next_q); todo.append(next_q)
    terms = {q for q in nodes if q == (target, all_labels)}
    assert len(terms) == 1
    core = set(terms); todo = list(terms)
    while todo:
        d = todo.pop()
        for q in incoming[d]:
            if q not in core: core.add(q); todo.append(q)
    def mask_of(q):
        s, used = q
        m = sum(1 << j for j, gate in enumerate(labels) if gate in used)
        assert m in profiles and profiles[m] == s and len(used) == m.bit_count()
        return m
    assert root in core and len(core) == len(ideals) and {mask_of(q) for q in core} == ideals
    actual = {(mask_of(q), gate, mask_of(d)) for q in core
              for gate, d in qedges[q].items() if d in core}
    assert actual == expected
    profile_list = sorted((m, canonical(s)) for m, s in profiles.items())
    edge_list = sorted(expected); effective = sum(m != d for m, g, d in expected)
    summary = [record['code'], record['first10_partner'], record['kind'], len(ideals), effective,
               len(expected) - effective, count_orders(0), len(nodes), len(nodes - core),
               digest(profile_list), digest(edge_list)]
    catalogue = dict(record=record, profiles=profile_list, edges=edge_list,
                     all_reachable=len(nodes), dead_states=len(nodes - core))
    return summary, catalogue


def audit_controls(fixture):
    P = fixture['prefix22']; tail = fixture['B11_known23_control']
    assert len(P) == 22 and len(tail) == 23
    full = P + [[a + 1, b + 1] for a, b in tail]
    image = set()
    for row in range(8192):
        values = [row >> j & 1 for j in range(13)]
        output = scalar(values, P)
        image.add(sum(output[j + 1] << j for j in range(11)))
        assert output[0] == int(row == 8191) and output[12] == int(row != 0)
        assert scalar(values, full) == sorted(values)
    assert sorted(image) == fixture['B11_states'] and len(image) == 158
    return dict(original_boolean_inputs=8192, B11_rows=len(image), full45_control='SORTS_ALL8192')


def audit(fixture, certificate, private_catalogue=None):
    controls = audit_controls(fixture)
    initial, target, nodes, outgoing, edge_set = independent_profiles(fixture)
    old, new = enumerate_words(initial, target, outgoing)
    old_table = [[str(c), sum(decode(c)), n] for c, n in sorted(old.items())]
    new_table = [[str(c), sum(decode(c)), n] for c, n in sorted(new.items())]
    dropped = sorted(set(old) - set(new)); slot = GATES.index((4, 10))
    assert dropped == sorted(c for c in old if sum(decode(c)) == 10 and decode(c)[slot])
    assert len(dropped) == 27 and all(new[c] == old[c] for c in new)
    assert len(old) == 480 and len(new) == 453
    assert sum(old.values()) == 3018600 and sum(new.values()) == 2868210
    shapes = Counter((sum(decode(c)), decode(c).count(2)) for c in new)
    assert shapes == {(10, 0): 108, (11, 0): 297, (11, 1): 48}
    factors = independent_factors()
    assert {int(r['code']) for r in factors} == {c for c in old if sum(decode(c)) == 10}
    assert {int(r['code']) for r in factors if r['first10_partner'] != 4} == {c for c in new if sum(decode(c)) == 10}
    summaries = []; catalogue = []; bytype = defaultdict(list)
    for r in factors:
        summary, data = audit_class(r, initial, target, outgoing)
        assert summary[6] == old[int(r['code'])]
        summaries.append(summary); catalogue.append(data); bytype[r['kind']].append(summary)
    types = {}
    for kind, rows in sorted(bytype.items()):
        assert len({tuple(r[3:7]) for r in rows}) == 1
        r = next(x for x in factors if x['kind'] == kind)
        types[kind] = dict(predecessor_masks=r['predecessor_masks'],
                           classes_before_cut=len(rows), classes_after_cut=sum(x[1] != 4 for x in rows),
                           ideal_states=rows[0][3], effective_edges=rows[0][4],
                           profile_loops=rows[0][5], words_per_class=rows[0][6])
    state_list = sorted(map(canonical, nodes)); edge_list = sorted(edge_set)
    result = dict(schema='sorting13-ten-event-matching-dags-v1', agent='six-sorting-2', role='researcher',
                  codec='Base4 digits on lexicographic combinations(range(11),2); decimal strings.',
                  parent_profile_states=len(nodes), parent_profile_edges=len(edge_set),
                  parent_state_sha256=digest(state_list), parent_edge_sha256=digest(edge_list),
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
    result = json.loads(json.dumps(result))
    assert result == certificate, 'Independent certificate mismatch'
    if private_catalogue is not None:
        reconstructed = dict(parent_states=state_list, parent_edges=edge_list,
                             parent_class_table=old_table, filtered_table=new_table, ten_graphs=catalogue)
        assert json.loads(json.dumps(reconstructed)) == private_catalogue, 'Entrywise catalogue mismatch'
    return dict(status='INDEPENDENT_ALL_WORDS_AND_ALL135_ACCEPTING_GRAPHS_VERIFIED',
                classes=453, effective_words_enumerated=3018600, retained_words=2868210,
                controls=controls, types=types, entrywise_private_catalogue_checked=private_catalogue is not None,
                filtered_table_sha256=result['filtered_table_sha256'])


def main():
    assert __debug__, 'Run without -O'
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    parser.add_argument('--catalogue', type=Path, help='Optional private forward catalogue for entrywise checking')
    args = parser.parse_args(); start = time.monotonic()
    fixture = json.loads((HERE / 'fixture.json').read_text())
    certificate = json.loads(args.certificate.read_text())
    catalogue = json.loads(args.catalogue.read_text()) if args.catalogue else None
    result = audit(fixture, certificate, catalogue)
    result.update(agent='six-sorting-2', role='researcher', seconds=time.monotonic() - start,
                  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__': main()
