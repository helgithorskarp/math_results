"""Independent scalar, finite-closure check for minimum preparations.

Author six-sorting-1, researcher. Imports no generator, SAT, or marker code.
For every Y20,7494 gives q1=2;7188 gives caps3/2/3. The new proposed
claim is that at leasttwo nonkernel events precede the final minimum merge.
Any reached terminal/operational cutoff fails the proposed exclusion.
"""
import argparse
from collections import deque
import hashlib
import itertools
import json
from pathlib import Path
import resource
import time

HERE = Path(__file__).resolve().parent
CAPACITIES = (3, 2, 3)


def scalar(values, word, marked_count=2):
    values = list(values)
    count = 0
    for a, b in word:
        count += values[a] < marked_count or values[b] < marked_count
        values[a], values[b] = sorted((values[a], values[b]))
    return values, count


def initial(fixture):
    profiles = []
    controls = 0
    for case in (1, 2):
        record = {}
        prefix = fixture['prefix21'] + fixture['tournaments'][str(case)]
        for a, b in itertools.combinations(range(13), 2):
            inputs = []
            middle = iter(range(2, 13))
            for i in range(13):
                inputs.append(0 if i == a else 1 if i == b else next(middle))
            values, deleted = scalar(inputs, prefix)
            mask = sum((v < 2) << i for i, v in enumerate(values))
            assert mask.bit_count() == 2 and mask < 512
            record[mask] = max(record.get(mask, deleted), deleted)
            checked, extra = scalar(values, fixture['known21_suffix'])
            assert checked == list(range(13)) and deleted + extra <= 10
            controls += 1
        profiles.append(tuple(sorted(record.items())))
    assert profiles[0] == profiles[1] == tuple(sorted(map(tuple, fixture['initial_two_minimum_profile'])))
    return profiles[0], controls


def single_minimum_controls(fixture):
    checked = 0
    for case in (1, 2):
        prefix = fixture['prefix21'] + fixture['tournaments'][str(case)]
        for leaf, mask in fixture['single_minimum_witnesses'].items():
            position = (8191 ^ mask).bit_length() - 1
            order = [position] + [i for i in range(13) if i != position]
            values = [0] * 13
            for rank, i in enumerate(order):
                values[i] = rank
            out, deleted = scalar(values, prefix, marked_count=1)
            assert out.index(0) == int(leaf)
            assert 44 - 39 - deleted == {0: 3, 1: 2, 5: 3}[int(leaf)]
            final, extra = scalar(out, fixture['known21_suffix'], marked_count=1)
            assert final == list(range(13)) and deleted + extra <= 6
            checked += 1
    return checked


def transitions(n, pairs):
    markers = list(itertools.combinations(range(n), 2))
    table = {}
    one = {}
    for gate in pairs:
        a, b = gate
        for p in range(n):
            bits = [1] * n
            bits[p] = 0
            hit = bits[a] == 0 or bits[b] == 0
            bits[a], bits[b] = sorted((bits[a], bits[b]))
            one[gate, p] = bits.index(0), int(hit)
        for u, v in markers:
            values = [2] * n
            values[u], values[v] = 0, 1
            hit = values[a] < 2 or values[b] < 2
            values[a], values[b] = sorted((values[a], values[b]))
            mask = sum((x < 2) << i for i, x in enumerate(values))
            table[gate, (1 << u) | (1 << v)] = mask, int(hit)
    return table, one


def change(rows, gate, table):
    fibers = {}
    for source, previous in rows:
        image, hit = table[gate, source]
        fibers.setdefault(image, []).append((source, previous, hit))
    result = []
    for image, inverse in fibers.items():
        assert 1 <= len(inverse) <= 2
        if len(inverse) == 2:
            assert all(hit == 1 for src, prev, hit in inverse)
        deletion = max(previous + hit for src, previous, hit in inverse)
        assert (1 << deletion) >= sum(1 << previous for src, previous, hit in inverse)
        result.append((image, deletion))
    return tuple(sorted(result))


def weight(rows):
    return sum(2 ** deleted for source, deleted in rows)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--n', type=int, choices=(10, 11), default=11)
    p.add_argument('--preparations', type=int, choices=(1, 2), default=2)
    a = p.parse_args()
    begun = time.monotonic()
    fixture = json.loads((HERE / 'fixture.json').read_text())
    assert fixture['conditional_minimum1_passages'] == 2
    assert fixture['minimum_route_caps'] == [3, 2, 3]
    assert fixture['maximum_two_minimum_weight'] == 512
    rows, controls = initial(fixture)
    pairs = list(itertools.combinations(range(a.n), 2))
    table, one = transitions(a.n, pairs)
    root = (0, (0, 1, 5), (0, 0, 0), rows)
    known = {root}
    queue = deque([root])
    edges = cuts = prep_cuts = route_cuts = 0
    complete = True
    terminal = None
    while queue:
        if len(known) >= 50000 or time.monotonic() - begun >= 45:
            complete = False
            break
        state = queue.popleft()
        nongates, positions, counts, profile = state
        if positions == (0, 0, 0):
            assert counts[1] == 2 and weight(profile) <= 512
            terminal = state
            complete = False
            break
        for gate in pairs:
            edges += 1
            moved = tuple(one[gate, p][0] for p in positions)
            charged = tuple(c + one[gate, pos][1] for pos, c in zip(positions, counts))
            non = nongates + (charged == counts)
            if non > a.preparations:
                prep_cuts += 1
                continue
            if any(c > cap for c, cap in zip(charged, CAPACITIES)):
                route_cuts += 1
                continue
            if len(set(moved)) > 1 and any(c >= cap for c, cap in zip(charged, CAPACITIES)):
                route_cuts += 1
                continue
            if moved == (0, 0, 0) and charged[1] != 2:
                route_cuts += 1
                continue
            updated = change(profile, gate, table)
            if weight(updated) > 512:
                cuts += 1
                continue
            new = non, moved, charged, updated
            if new not in known:
                known.add(new)
                queue.append(new)
    digest = hashlib.sha256()
    for state in sorted(known):
        digest.update(json.dumps(state, separators=(',', ':')).encode())
    pure = []
    for word in (((0, 1), (0, 5)), ((1, 5), (0, 1)), ((0, 5), (0, 1))):
        prof = rows
        for gate in word:
            prof = change(prof, gate, table)
        pure.append({'word':word,'profile':prof,'weight':weight(prof)})
    result = {'agent':'six-sorting-1','role':'researcher','n':a.n,'max_preparations':a.preparations,
              'status':'independent_complete_exclusion' if complete else
                       'accepting_relaxed_prefix' if terminal else 'operational_limit_incomplete',
              'states':len(known),'queue':len(queue),'edges':edges,'weight_cuts':cuts,
              'preparation_cuts':prep_cuts,'route_cuts':route_cuts,
              'state_sha256':digest.hexdigest(),'initial_profile':rows,'pure_binary':pure,
              'original_pair_controls':controls, 'single_minimum_controls':single_minimum_controls(fixture),
              'two_marker_fiber_controls':len(pairs)**2, 'single_zero_controls':len(pairs)*a.n,'seconds':time.monotonic()-begun,
              'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'terminal':terminal,'proof_status':'Independent scalar transition/domain audit; imports caps7188 and q1exact2 theorem7494',
              'scope':'No selected depth or kernel count; only the stated nongate-count class is excluded'}
    assert complete and terminal is None, 'Incomplete or accepting graph: no exclusion'
    if (a.n, a.preparations) == (11, 2):
        expected = json.loads((HERE / 'certificate.json').read_text())
        assert expected['fixture_sha256'] == hashlib.sha256((HERE / 'fixture.json').read_bytes()).hexdigest()
        for key in ('n','max_preparations','states','edges','weight_cuts','preparation_cuts','route_cuts','state_sha256','pure_binary'):
            actual = json.loads(json.dumps(result[key]))
            assert actual == expected[key], (key, actual, expected[key])
        result['certificate_matched'] = True
    print(json.dumps(result))


if __name__=='__main__':
    main()
