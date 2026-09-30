"""Independent scalar-rank, inverse-fiber and DFS checker.

No generator code is imported. Complete phase sets can be compared entry
by entry to an exported generator catalogue, in addition to compact hashes.
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
PAIRS = tuple(itertools.combinations(range(12), 2))
PARTNERS = (2, 3, 4, 6, 7, 8, 9, 10, 11)


def scalar(values, word):
    values = list(values)
    for a, b in word:
        if values[a] > values[b]:
            values[a], values[b] = values[b], values[a]
    return values


def canonical(profile):
    return sorted([[(1 << a) | (1 << b), depth] for (a, b), depth in profile])


def canonical_set(profiles):
    return sorted(canonical(profile) for profile in profiles)


def digest(value):
    return hashlib.sha256((json.dumps(value, separators=(',', ':'))+'\n').encode()).hexdigest()


def inverse_fibers(wires):
    fibers = {}
    pairs = tuple(itertools.combinations(range(wires), 2))
    for gate in pairs:
        a, b = gate
        inv = {}
        forward = {}
        for marked in pairs:
            values = list(range(2, wires+2))
            values[marked[0]], values[marked[1]] = -2, -1
            charged = int(values[a] < 0 or values[b] < 0)
            after = scalar(values, [gate])
            destination = tuple(i for i, v in enumerate(after) if v < 0)
            assert len(destination) == 2
            inv.setdefault(destination, []).append((marked, charged))
            forward[marked] = (destination, charged)
        assert sum(map(len, inv.values())) == len(pairs)
        assert all(len(fiber) <= 2 for fiber in inv.values())
        assert all(all(charge == 1 for _, charge in fiber)
                   for fiber in inv.values() if len(fiber) == 2)
        # Restricted transport at every possible single-minimum anchor.
        for anchor in range(wires):
            one = [int(i != anchor) for i in range(wires)]
            new_anchor = scalar(one, [gate]).index(0)
            restricted = [forward[z] for z in pairs if anchor in z]
            assert all(new_anchor in dest for dest, _ in restricted)
            if anchor in gate:
                assert all(charge == 1 for _, charge in restricted)
                assert len({dest for dest, _ in restricted}) == len(restricted)
            else:
                assert all((anchor in z) == (anchor in forward[z][0]) for z in pairs)
        fibers[gate] = tuple((dst, tuple(src)) for dst, src in sorted(inv.items()))
    return fibers


def update(profile, gate, fibers):
    depths = dict(profile)
    answer = []
    for destination, predecessors in fibers[gate]:
        candidates = [depths[source]+charge for source, charge in predecessors if source in depths]
        if candidates:
            answer.append((destination, max(candidates)))
    return tuple(answer)


def weight(profile):
    return sum(2**d for _, d in profile)


def valid(profile, anchors):
    if weight(profile) > 512:
        return False
    for port, remaining in anchors:
        anchored = sum(2**d for pair, d in profile if port in pair)
        if anchored*2**remaining > 512:
            return False
    return True


def closure(seeds, anchors, fibers):
    admitted = [profile for profile in seeds if valid(profile, anchors)]
    seen = set(admitted)
    stack = list(seen)
    ports = {p for p, _ in anchors}
    gates = [gate for gate in PAIRS if all(p not in ports for p in gate)]
    while stack:
        profile = stack.pop()
        for gate in gates:
            following = update(profile, gate, fibers)
            if following not in seen and valid(following, anchors):
                seen.add(following)
                stack.append(following)
    encoded = canonical_set(seen)
    statistics = dict(profiles=len(seen), accepted_seeds=len(admitted),
                      distinct_seeds=len(set(admitted)), nongates=len(gates),
                      transitions=len(seen)*len(gates), sha256=digest(encoded))
    return seen, encoded, statistics


def reconstruct(fixture):
    P19 = fixture['prefix19']
    Q20 = P19+[fixture['maximum_merge']]
    assert len(P19) == 19 and fixture['maximum_merge'] == [10, 12]
    assert fixture['minimum_word'] == [[0, 5], [0, 1]]
    assert fixture['imported_sizes'] == {'11':35, '13_lower':44}
    assert fixture['full_budget'] == 44
    F = {}
    for marked in itertools.combinations(range(13), 2):
        values = list(range(2, 15))
        values[marked[0]], values[marked[1]] = -2, -1
        D = 0
        for a, b in Q20:
            D += int(values[a] < 0 or values[b] < 0)
            if values[a] > values[b]:
                values[a], values[b] = values[b], values[a]
        destination = tuple(i for i, v in enumerate(values) if v < 0)
        assert len(destination) == 2 and 12 not in destination
        F[destination] = max(F.get(destination, -1), D)
    initial = tuple(sorted(F.items()))
    masses = [sum(2**d for pair, d in initial if p in pair) for p in (0, 1, 5)]
    assert masses == [72, 160, 48]
    assert all(2**r*M <= 512 < 2**(r+1)*M for r,M in zip((2,1,3),masses))
    qrows, brows, minima = set(), set(), set()
    C25 = fixture['Q20_known25_control']
    C23 = fixture['B11_known23_control']
    assert len(C25) == 25 and len(C23) == 23
    assert all(0 <= a < b < 12 for a,b in C25)
    assert all(0 <= a < b < 11 for a,b in C23)
    assert all(0 <= a < b < 13 for a,b in Q20)
    for bits in itertools.product((0, 1), repeat=13):
        q = scalar(bits, Q20)
        qrows.add(sum(v << p for p,v in enumerate(q[:12])))
        if sum(bits) == 12:
            minima.add(q.index(0))
        b = scalar(q, fixture['minimum_word'])
        assert b[0] == min(bits) and b[12] == max(bits)
        brows.add(sum(v << p for p,v in enumerate(b[1:12])))
        assert scalar(q, C25) == sorted(bits)
        assert [b[0]]+scalar(b[1:12], C23)+[b[12]] == sorted(bits)
    assert len(qrows) == 174 and len(brows) == 158 and sorted(minima) == [0,1,5]
    images = dict(Q20_states=174, Q20_sha256=digest(sorted(qrows)),
                  B11_states=158, B11_sha256=digest(sorted(brows)),
                  original_inputs=8192, checked_full45_controls=2)
    return initial, images


def main():
    if not __debug__:
        raise RuntimeError('Assertions must be enabled')
    started = time.monotonic()
    parser = argparse.ArgumentParser()
    parser.add_argument('--catalogue', type=Path)
    args = parser.parse_args()
    fixture = json.loads((HERE/'fixture.json').read_text())
    certificate = json.loads((HERE/'certificate.json').read_text())
    assert hashlib.sha256((HERE/'fixture.json').read_bytes()).hexdigest() == certificate['fixture_sha256']
    assert certificate['schema'] == 1 and certificate['agent'] == 'six-sorting-2'
    assert certificate['role'] == 'researcher' and certificate['ceiling'] == 512
    # The 13-wire audit has 6084 scalar pair transitions and 1014 anchors.
    inverse_fibers(13)
    fibers = inverse_fibers(12)
    initial, images = reconstruct(fixture)
    assert canonical(initial) == certificate['Q20_minimum_profile']
    assert certificate['anchored_masses'] == [72,160,48]
    assert certificate['minimum_passage_caps'] == [2,1,3]
    assert certificate['minimum_ports'] == [0,1,5]
    assert certificate['minimum_unary_partners'] == list(PARTNERS)
    assert images == certificate['images']
    pre, encoded, statistics = closure([initial], [(0,2),(1,1),(5,3)], fibers)
    assert statistics == certificate['pre']
    catalogue = {'pre':encoded}
    for a, expected in zip(PARTNERS, certificate['cases']):
        m = min(a, 5)
        unary = tuple(sorted((a, 5)))
        post, ep, sp = closure([update(F,unary,fibers) for F in pre], [(0,2),(1,1),(m,2)], fibers)
        joined, ej, sj = closure([update(F,(0,m),fibers) for F in post], [(0,1),(1,1)], fibers)
        terminal = {update(F,(0,1),fibers) for F in joined}
        et = canonical_set(terminal)
        distribution = Counter(weight(F) for F in terminal)
        assert distribution and min(distribution) > 512
        actual = dict(partner=a, post=sp, joined=sj, terminal_profiles=len(terminal),
                      terminal_sha256=digest(et), terminal_weight_histogram=sorted(distribution.items()),
                      minimum_terminal_weight=min(distribution), survivors=0)
        assert json.loads(json.dumps(actual)) == expected
        catalogue.update({f'a{a}/post':ep, f'a{a}/joined':ej, f'a{a}/terminal':et})
    assert len(certificate['cases']) == len(PARTNERS)
    assert certificate['conclusion'] == dict(Q20_C24_minimum_event_word=[[0,5],[0,1]],
        P19_full44_equivalent_target='B11_C22', B11_interval=[22,23], global_S13_interval=[44,45])
    if args.catalogue:
        assert catalogue == json.loads(args.catalogue.read_text())
    print(json.dumps(dict(status='ALL_INDEPENDENT_CHECKS_PASSED', preprofiles=len(pre),
                         unary_partners=9, excluded_partners=9, original_inputs=8192,
                         scalar_pair_transitions=6084, scalar_anchor_configurations=1014,
                         complete_profile_sets=len(catalogue),
                         entrywise_catalogue_comparison=args.catalogue is not None,
                         minimum_terminal_weight=608, seconds=time.monotonic()-started,
                         peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)),flush=True)


if __name__ == '__main__':
    main()
