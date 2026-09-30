"""Exact forward-mask/BFS exclusion of the Q20 unary-minimum branches.

six-sorting-2, researcher. Standard-library Python, assertions enabled.
There is no solver, depth restriction, or enumeration cutoff. Generated
complete profile catalogues belong in ignored scratch, not publication.
"""
import argparse
from collections import Counter, deque
import hashlib
import itertools
import json
from pathlib import Path
import resource
import time

HERE = Path(__file__).resolve().parent
PAIRS = tuple(itertools.combinations(range(12), 2))
PARTNERS = (2, 3, 4, 6, 7, 8, 9, 10, 11)


def digest(value):
    return hashlib.sha256((json.dumps(value, separators=(',', ':'))+'\n').encode()).hexdigest()


def boolean(row, word):
    for a, b in word:
        if row >> a & 1 and not row >> b & 1:
            row ^= (1 << a) | (1 << b)
    return row


def step(profile, gate):
    a, b = gate
    following = {}
    for mask, depth in profile:
        charged = bool(mask & ((1 << a) | (1 << b)))
        if mask >> b & 1 and not mask >> a & 1:
            mask ^= (1 << a) | (1 << b)
        following[mask] = max(following.get(mask, -1), depth+charged)
    return tuple(sorted(following.items()))


def weight(profile):
    return sum(1 << depth for _, depth in profile)


def mass(profile, port):
    return sum(1 << depth for mask, depth in profile if mask >> port & 1)


def admissible(profile, anchors):
    return weight(profile) <= 512 and all(
        (1 << remaining)*mass(profile, port) <= 512 for port, remaining in anchors)


def close(seeds, anchors):
    accepted = [profile for profile in seeds if admissible(profile, anchors)]
    seen = set(accepted)
    queue = deque(sorted(seen))
    occupied = {port for port, _ in anchors}
    nongates = [gate for gate in PAIRS if not occupied.intersection(gate)]
    while queue:
        profile = queue.popleft()
        for gate in nongates:
            following = step(profile, gate)
            if following not in seen and admissible(following, anchors):
                seen.add(following)
                queue.append(following)
    profiles = sorted(seen)
    summary = dict(profiles=len(profiles), accepted_seeds=len(accepted),
                   distinct_seeds=len(set(accepted)), nongates=len(nongates),
                   transitions=len(profiles)*len(nongates), sha256=digest(profiles))
    return profiles, summary


def reconstruct(fixture):
    P19 = fixture['prefix19']
    Q20 = P19+[fixture['maximum_merge']]
    assert len(P19) == 19 and fixture['maximum_merge'] == [10, 12]
    assert fixture['minimum_word'] == [[0, 5], [0, 1]]
    assert fixture['imported_sizes'] == {'11':35, '13_lower':44}
    assert fixture['full_budget'] == 44
    profiles = tuple(sorted(((1 << a) | (1 << b), 0)
                            for a, b in itertools.combinations(range(13), 2)))
    for gate in Q20:
        profiles = step(profiles, gate)
    assert all(mask < 4096 for mask, _ in profiles)
    anchors = [mass(profiles, p) for p in (0, 1, 5)]
    assert anchors == [72, 160, 48]
    caps = [(512//v).bit_length()-1 for v in anchors]
    assert caps == [2, 1, 3]
    qimage, bimage, minimum_ports = set(), set(), set()
    minword = fixture['minimum_word']
    full_control = Q20+fixture['Q20_known25_control']
    lifted_control = Q20+minword+[[a+1,b+1] for a,b in fixture['B11_known23_control']]
    assert len(full_control) == len(lifted_control) == 45
    assert all(0 <= a < b < 13 for a,b in full_control+lifted_control)
    assert all(b < 12 for a,b in fixture['Q20_known25_control'])
    assert len(fixture['Q20_known25_control']) == 25
    assert len(fixture['B11_known23_control']) == 23
    for x in range(8192):
        y = boolean(x, Q20)
        qimage.add(y & 4095)
        if x.bit_count() == 12:
            minimum_ports.add(next(p for p in range(13) if not(y >> p & 1)))
        b = boolean(y, minword)
        assert b & 1 == int(x == 8191) and b >> 12 == int(x != 0)
        bimage.add((b >> 1) & 2047)
        target = ((1 << x.bit_count())-1) << (13-x.bit_count())
        assert boolean(x, full_control) == target
        assert boolean(x, lifted_control) == target
    assert sorted(minimum_ports) == [0, 1, 5]
    assert len(qimage) == 174 and len(bimage) == 158
    return profiles, dict(Q20_states=174, Q20_sha256=digest(sorted(qimage)),
                          B11_states=158, B11_sha256=digest(sorted(bimage)),
                          original_inputs=8192, checked_full45_controls=2)


def reproduce(fixture):
    initial, images = reconstruct(fixture)
    pre, prestats = close([initial], [(0, 2), (1, 1), (5, 3)])
    catalogue = {'pre':pre}
    cases = []
    for a in PARTNERS:
        unary = tuple(sorted((5, a)))
        m = min(5, a)
        post, poststats = close([step(F, unary) for F in pre], [(0, 2), (1, 1), (m, 2)])
        joined, joinedstats = close([step(F, (0, m)) for F in post], [(0, 1), (1, 1)])
        terminal = sorted({step(F, (0, 1)) for F in joined})
        distribution = Counter(weight(F) for F in terminal)
        assert distribution and min(distribution) > 512
        cases.append(dict(partner=a, post=poststats, joined=joinedstats,
                          terminal_profiles=len(terminal), terminal_sha256=digest(terminal),
                          terminal_weight_histogram=sorted(distribution.items()),
                          minimum_terminal_weight=min(distribution), survivors=0))
        for phase, profiles in [('post',post), ('joined',joined), ('terminal',terminal)]:
            catalogue[f'a{a}/{phase}'] = profiles
    certificate = dict(schema=1, agent='six-sorting-2', role='researcher',
                       fixture_sha256=hashlib.sha256((HERE/'fixture.json').read_bytes()).hexdigest(),
                       ceiling=512, Q20_minimum_profile=initial, anchored_masses=[72,160,48],
                       minimum_ports=[0,1,5], minimum_passage_caps=[2,1,3],
                       minimum_unary_partners=PARTNERS, pre=prestats, cases=cases, images=images,
                       conclusion={'Q20_C24_minimum_event_word':[[0,5],[0,1]],
                                   'P19_full44_equivalent_target':'B11_C22',
                                   'B11_interval':[22,23], 'global_S13_interval':[44,45]})
    return json.loads(json.dumps(certificate)), json.loads(json.dumps(catalogue))


def main():
    if not __debug__:
        raise RuntimeError('Assertions must be enabled')
    started = time.monotonic()
    parser = argparse.ArgumentParser()
    parser.add_argument('--write-certificate', action='store_true')
    parser.add_argument('--export', type=Path)
    args = parser.parse_args()
    fixture = json.loads((HERE/'fixture.json').read_text())
    certificate, catalogue = reproduce(fixture)
    if args.write_certificate:
        (HERE/'certificate.json').write_text(json.dumps(certificate, indent=2)+'\n')
    else:
        assert certificate == json.loads((HERE/'certificate.json').read_text())
    if args.export:
        args.export.write_text(json.dumps(catalogue, separators=(',', ':'))+'\n')
    print(json.dumps(dict(status='GENERATOR_CHECKS_PASSED', preprofiles=certificate['pre']['profiles'],
                         unary_partners=len(PARTNERS), excluded_partners=len(PARTNERS),
                         minimum_terminal_weight=min(c['minimum_terminal_weight'] for c in certificate['cases']),
                         complete_profile_sets=len(catalogue),
                         seconds=time.monotonic()-started,
                         peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)),flush=True)


if __name__ == '__main__':
    main()
