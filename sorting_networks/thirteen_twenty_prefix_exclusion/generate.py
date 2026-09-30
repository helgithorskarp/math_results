"""Forward masks and breadth-first exact profiles; six-sorting-1 researcher.

No solver, enumeration cutoff, or chosen depth. --write-certificate is for
source preparation; the ordinary public command checks a fixed certificate.
"""
import argparse
from collections import deque
import hashlib
import itertools
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PAIRS = tuple(itertools.combinations(range(13), 2))
NONGATES = tuple(g for g in PAIRS if 10 not in g and 12 not in g)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def boolean(mask, word):
    for a, b in word:
        if mask >> a & 1 and not mask >> b & 1:
            mask ^= (1 << a) | (1 << b)
    return mask


def transition(profile, gate):
    a, b = gate
    result = {}
    for mask, d in profile:
        charge = int(bool(mask & ((1 << a) | (1 << b))))
        if mask >> a & 1 and not mask >> b & 1:
            mask ^= (1 << a) | (1 << b)
        result[mask] = max(result.get(mask, -1), d + charge)
    return tuple(sorted(result.items()))


def profile(word):
    f = tuple(sorted(((1 << a) | (1 << b), 0) for a, b in PAIRS))
    for gate in word:
        f = transition(f, gate)
    return f


def mass(f, port):
    return sum(1 << d for mask, d in f if mask >> port & 1)


def weight(f):
    return sum(1 << d for mask, d in f)


def allowed(f, cap12):
    return weight(f) <= 512 and mass(f, 10) <= 256 and mass(f, 12) <= cap12


def close(seeds, cap12):
    seen = {f for f in seeds if allowed(f, cap12)}
    queue = deque(sorted(seen))
    while queue:
        f = queue.popleft()
        for gate in NONGATES:
            dest = transition(f, gate)
            if allowed(dest, cap12) and dest not in seen:
                seen.add(dest)
                queue.append(dest)
    return sorted(seen)


def maximum_ports(word):
    return sorted({boolean(1 << p, word).bit_length() - 1 for p in range(13)})


def images(fixture):
    p20 = fixture['prefix20']
    assert len(p20) == 20 and p20[-1] == [8, 11]
    p19 = p20[:-1]
    q20 = p19 + [[10, 12]]
    minword = fixture['minimum_word']
    control25 = fixture['known25_control']
    assert control25[0] == [10, 12] and len(control25) == 25
    qcontrol = [[8, 11]] + control25[1:]
    # Reordering just these disjoint gates preserves the known full45 control.
    assert set(p20[-1]).isdisjoint(control25[0])
    qports = (0, 1, 5)
    events, others = [], []
    for gate in qcontrol:
        a, b = gate
        if set(qports).intersection(gate):
            events.append(gate)
            qports = tuple(a if p == b else p for p in qports)
        else:
            others.append(gate)
    assert events == minword and len(others) == 23 and qports == (0, 0, 0)
    assert all(0 < a < b < 12 for a, b in others)
    assert [[a - 1, b - 1] for a, b in others] == fixture['B11_known23_control']
    zports = (0, 1, 5)
    zevents, zothers = [], []
    for gate in control25:
        a, b = gate
        if set(zports).intersection(gate):
            zevents.append(gate)
            zports = tuple(a if p == b else p for p in zports)
        else:
            zothers.append(gate)
    assert zevents == minword and len(zothers) == 23
    assert [[a - 1, b - 1] for a, b in zothers] == fixture['Z12_known23_control']
    sets = {'P19': set(), 'P20': set(), 'Z12': set(), 'Q20': set(), 'B11': set()}
    for x in range(8192):
        y19, y20 = boolean(x, p19), boolean(x, p20)
        q = boolean(x, q20)
        z, b = boolean(y20, minword), boolean(q, minword)
        sorted13 = ((1 << x.bit_count()) - 1) << (13 - x.bit_count())
        assert boolean(y20, control25) == sorted13
        assert boolean(q, qcontrol) == sorted13
        assert z & 1 == int(x == 8191)
        assert q >> 12 == int(x != 0)
        assert b & 1 == int(x == 8191) and b >> 12 == int(x != 0)
        zi, bi = z >> 1, (b >> 1) & 2047
        assert boolean(zi, fixture['Z12_known23_control']) == ((1 << zi.bit_count()) - 1) << (12 - zi.bit_count())
        assert boolean(bi, fixture['B11_known23_control']) == ((1 << bi.bit_count()) - 1) << (11 - bi.bit_count())
        assert boolean(y20, minword + zothers) == sorted13
        assert boolean(q, minword + others) == sorted13
        for name, row in [('P19', y19), ('P20', y20), ('Z12', zi), ('Q20', q & 4095), ('B11', bi)]:
            sets[name].add(row)
    return {name: {'states': sorted(rows), 'count': len(rows), 'sha256': digest(sorted(rows))} for name, rows in sets.items()}


def reproduce(fixture):
    assert fixture['full_budget'] == 44 and fixture['S11'] == 35
    ceiling = 1 << (fixture['full_budget'] - fixture['S11'])
    assert ceiling == 512 and len(NONGATES) == 55
    p19, p20 = fixture['prefix20'][:-1], fixture['prefix20']
    f19, f20 = profile(p19), profile(p20)
    assert maximum_ports(p19) == maximum_ports(p20) == [10, 12]
    a19 = [mass(f19, p) for p in (10, 12)]
    a20 = [mass(f20, p) for p in (10, 12)]
    assert a19 == [224, 128] and a20 == [256, 144]
    caps19 = [(ceiling // v).bit_length() - 1 for v in a19]
    caps20 = [(ceiling // v).bit_length() - 1 for v in a20]
    assert caps19 == [1, 2] and caps20 == [1, 1]
    pre = close([f19], 128)
    cases = []
    for p in list(range(10)) + [11]:
        seeds = [transition(f, (p, 12)) for f in pre]
        post = close(seeds, 256)
        terminals = [transition(f, (10, 12)) for f in post]
        assert all(weight(f) > ceiling for f in terminals)
        cases.append({'unary': [p, 12], 'accepted_seed_count': sum(allowed(f, 256) for f in seeds),
                      'post_profiles': post, 'terminal_profiles': terminals,
                      'terminal_weights': [weight(f) for f in terminals],
                      'survivor_count': 0})
    all_images = images(fixture)
    assert {k: v['count'] for k, v in all_images.items()} == {'P19': 179, 'P20': 166, 'Z12': 150, 'Q20': 174, 'B11': 158}
    return {'ceiling': ceiling, 'P19_profile': f19, 'P20_profile': f20,
            'P19_anchor_masses_10_12': a19, 'P20_anchor_masses_10_12': a20,
            'P19_route_caps_10_12': caps19, 'P20_route_caps_10_12': caps20,
            'nongate_count': len(NONGATES), 'pre_profiles': pre,
            'unary_cases': cases, 'images': all_images, 'original_Boolean_inputs': 8192,
            'conclusion': {'P20_minimum_suffix': 25, 'Z12_minimum': 23,
                           'P19_full44_maximum_kernel': [[10, 12]],
                           'Q20_interval': [24, 25], 'B11_interval': [22, 23],
                           'global_S13_interval': [44, 45]}}


def main():
    if sys.flags.optimize:
        raise RuntimeError('Run without -O: assertions are exact checks.')
    parser = argparse.ArgumentParser()
    parser.add_argument('--write-certificate', action='store_true')
    args = parser.parse_args()
    result = reproduce(json.loads((HERE / 'fixture.json').read_text()))
    encoded = json.dumps(result, indent=2) + '\n'
    if args.write_certificate:
        (HERE / 'certificate.json').write_text(encoded)
    expected = json.loads((HERE / 'certificate.json').read_text())
    assert json.loads(json.dumps(result)) == expected
    print(json.dumps({'agent': 'six-sorting-1', 'role': 'researcher',
                      'status': 'all_exact_checks_passed', 'algorithm': 'forward_masks_BFS',
                      'certificate_sha256': hashlib.sha256((HERE / 'certificate.json').read_bytes()).hexdigest(),
                      'image_counts': {k: v['count'] for k, v in result['images'].items()},
                      'pre_profile_count': len(result['pre_profiles']),
                      'post_profile_counts': [len(c['post_profiles']) for c in result['unary_cases']],
                      'conclusion': result['conclusion']}, indent=2))


if __name__ == '__main__':
    main()
