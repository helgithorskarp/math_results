"""Independent exact two-entry audit and chain-event count for best4.txt."""
from collections import Counter, defaultdict
from itertools import combinations
from math import perm
from pathlib import Path

SOURCE = Path(__file__).resolve().parent.parent / 'schur_s6_nonlocal_doubling_search'
word = (SOURCE / 'best4.txt').read_text().strip()
assert len(word) == 537 and set(word) == set('123456')
colour = [0] + [int(c) for c in word]

triples = []
incident = [[] for _ in range(538)]
shared = defaultdict(list)
all_bad = []
total_triples = 0
for z in range(2, 538):
    for x in range(1, z // 2 + 1):
        total_triples += 1
        y = z - x
        if colour[x] == colour[y] == colour[z]:
            all_bad.append((x, y, z))
        if x == y:
            continue
        index = len(triples)
        triples.append((x, y, z))
        for v in (x, y, z):
            incident[v].append(index)
        for a, b in combinations((x, y, z), 2):
            shared[a, b].append(index)
assert len(triples) == 71824
assert total_triples == 72092
assert set(all_bad) == {(2, 281, 283), (4, 146, 150),
                        (4, 260, 264), (4, 391, 395)}
assert all(colour[v] != colour[2 * v] for v in range(1, 269))
assert max(map(len, shared.values())) == 2


def bad_edge(index, changes=()):
    x, y, z = triples[index]
    values = (colour[x], colour[y], colour[z])
    for vertex, replacement in changes:
        values = tuple(replacement if v == vertex else c
                       for v, c in zip((x, y, z), values))
    return values[0] == values[1] == values[2]


base_bad = [bad_edge(i) for i in range(len(triples))]
assert sum(base_bad) == 4


def direct(v, d, w, e):
    assignment = colour.copy()
    assignment[v] = d
    assignment[w] = e
    assert all(assignment[t] != assignment[2 * t] for t in range(1, 269))
    return sum(assignment[x] == assignment[y] == assignment[z]
               for x, y, z in triples)


choices = []
delta = {}
for v in range(1, 538):
    for d in range(1, 7):
        if d == colour[v]:
            continue
        change = sum(bad_edge(index, ((v, d),)) - base_bad[index]
                     for index in incident[v])
        delta[v, d] = change
        if v % 2 == 0 and colour[v // 2] == d:
            continue
        if 2 * v <= 537 and colour[2 * v] == d:
            continue
        choices.append((v, d))
assert len(choices) == 2177
assert 4 + min(delta[m] for m in choices) == 4


def score(v, d, w, e):
    correction = 0
    for index in shared.get((v, w), ()):
        correction += (bad_edge(index, ((v, d), (w, e)))
                       - bad_edge(index, ((v, d),))
                       - bad_edge(index, ((w, e),))
                       + base_bad[index])
    return 4 + delta[v, d] + delta[w, e] + correction


# Exhaust every final-legal nonadjacent pair, without the source's score
# cutoff. For such pairs, individual legality is equivalent to final legality.
best = 4
nonadjacent = 0
hist = Counter()
audits = 0
within_source_cutoff = 0
omitted_minimum = 100
for i, (v, d) in enumerate(choices):
    for w, e in choices[i + 1:]:
        if v == w or 2 * v == w or 2 * w == v:
            continue
        a, b = sorted((v, w))
        da, db = (d, e) if a == v else (e, d)
        value = score(a, da, b, db)
        nonadjacent += 1
        hist[value] += 1
        if delta[a, da] + delta[b, db] <= 6:
            within_source_cutoff += 1
        else:
            omitted_minimum = min(omitted_minimum, value)
        if nonadjacent % 25000 == 0:
            assert direct(a, da, b, db) == value
            audits += 1
        if value < best:
            best = value

# Adjacent pairs can be final-legal even when an individual move is illegal.
adjacent = 0
source_adjacent_overlap = 0
for v in range(1, 269):
    w = 2 * v
    for d in range(1, 7):
        if d == colour[v] or (v % 2 == 0 and colour[v // 2] == d):
            continue
        for e in range(1, 7):
            if e == colour[w] or e == d or (2 * w <= 537 and colour[2 * w] == e):
                continue
            value = score(v, d, w, e)
            adjacent += 1
            if (d != colour[w] and e != colour[v]
                    and delta[v, d] + delta[w, e] <= 6):
                source_adjacent_overlap += 1
            hist[value] += 1
            if adjacent % 100 == 0:
                assert direct(v, d, w, e) == value
                audits += 1
            if value < best:
                best = value
assert adjacent == 4551
assert best == 4
assert within_source_cutoff + source_adjacent_overlap == 233367
assert omitted_minimum >= 7

# An observed chain using k colours admits P(6,k) distinct palette images.
# One is the identity image; sum and pair counts are independent of the C++.
events = []
for root in range(1, 538, 2):
    seen = set()
    v = root
    while v <= 537:
        seen.add(colour[v])
        v *= 2
    events.append(perm(6, len(seen)) - 1)
assert len(events) == 269 and sum(events) == 15841
pair_count = (sum(events) ** 2 - sum(x * x for x in events)) // 2
assert pair_count == 123114286

print('PASS defects=4 doubling_defects=0 legal_single_moves=2177')
print(f'all_final_legal_pairs={nonadjacent + adjacent} nonadjacent={nonadjacent} adjacent={adjacent} minimum={best} direct_audits={audits}')
print(f'within_source_cutoff={within_source_cutoff + source_adjacent_overlap} omitted_nonadjacent_minimum={omitted_minimum}')
print(f'chain_moves={sum(events)} distinct_chain_pairs={pair_count}')
