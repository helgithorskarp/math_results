"""Independent physical row actions, before sufficient-comparison samples.

ALL original ordered pairs at (19,5),(24,6); one representative against
EVERY member at (74,15), with the original permutation symmetry bridge.
No counted disjoint multiplicities or original matrix-square shortcut.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json
import time
import residual
from literal import member, typ, table, require
from exact import digest


def amplitudes(a):
    return (F(1), F((a & 7) == 1 and (a >> 3).bit_count() == 1),
            F(bool(a & 6) and a not in (3, 5)))


def original(q, k, all_rows):
    x = sorted(sum(1 << j for j in points) for size in (1, 2, 3)
               for points in combinations(range(q+3), size)
               if member(q, k, sum(1 << j for j in points)))
    groups = {}
    for a in x:
        z = sum(bool(a & (1 << j)) for j in range(3, k+3))
        w = sum(bool(a & (1 << j)) for j in range(k+3, q+3))
        groups.setdefault((a & 7, z, w), []).append(a)
    keys = sorted(groups)
    sizes = [len(groups[key]) for key in keys]
    n, s = len(x)+1, 3*q+4
    tab = table(q)
    vectors = [amplitudes(a) for a in x]
    kinds = [typ(a) for a in x]
    labels = {a: i for i, key in enumerate(keys) for a in groups[key]}
    action_by_orbit, f_by_orbit = {}, {}
    positions = 0
    rows = x if all_rows else [groups[key][0] for key in keys]
    for a in rows:
        aa, fa = typ(a), amplitudes(a)
        action = [F(0)]*3
        for b, bb, fb in zip(x, kinds, vectors):
            positions += 1
            if a == b:
                value = F(n-s)
            elif a & b:
                value = F(0)
            else:
                value = -tab[tuple(sorted((aa, bb)))][0]
            if value:
                for j in range(3):
                    if fb[j]:
                        action[j] += value*fb[j]
        label = labels[a]
        if label in action_by_orbit:
            require(action_by_orbit[label] == action,
                    'every computed original row action constant on orbit')
        action_by_orbit[label] = action
        f_by_orbit[label] = list(fa)
    for key in keys:
        require(len({amplitudes(a) for a in groups[key]}) == 1,
                'every original vector amplitude constant on orbit')
    acts = [action_by_orbit[i] for i in range(len(keys))]
    fs = [f_by_orbit[i] for i in range(len(keys))]
    frame = [[sum(sizes[i]*fs[i][a]*fs[i][b] for i in range(len(keys)))
              for b in range(3)] for a in range(3)]
    first = [[sum(sizes[i]*fs[i][a]*acts[i][b] for i in range(len(keys)))
              for b in range(3)] for a in range(3)]
    second = [[sum(sizes[i]*acts[i][a]*acts[i][b] for i in range(len(keys)))
               for b in range(3)] for a in range(3)]
    data = residual.orbits.forms(q, k)
    counted = residual.moments(data)
    require(keys == data['keys'] and sizes == data['sizes'], 'independent original census')
    require(acts == counted['actions'] and fs == counted['amplitudes'],
            'every independently computed original row action and amplitude')
    for name, value in (('frame', frame), ('first', first), ('second', second)):
        require(value == counted[name], 'every original physical '+name+' entry')
    # Deliberately ignoring a residual action must change the second moment.
    damaged = [row[:] for row in acts]
    damaged[0][0] += 1
    bad_second = [[sum(sizes[i]*damaged[i][a]*damaged[i][b] for i in range(len(keys)))
                   for b in range(3)] for a in range(3)]
    require(bad_second != second, 'altered original action changes second moment')
    return {'q': q, 'k': k, 'N': n, 'original_rows': len(rows),
            'original_positions': positions, 'all_original_ordered_pairs': all_rows,
            'large_fixture_symmetry_bridge': not all_rows,
            'every_original_action_and_moment_matches': True,
            'original_moments': residual.encode({'frame': frame, 'first': first, 'second': second}),
            'original_actions_digest': digest(residual.encode(acts)),
            'semantic_damage_rejected': True}


def run():
    start = time.perf_counter()
    fixtures = [original(q, k, all_rows) for q, k, all_rows in
                ((19, 5, True), (24, 6, True), (74, 15, False))]
    result = {'agent': 'six-downset-3', 'role': 'researcher',
              'status': 'exact calibration; not new classification',
              'fixtures': fixtures}
    result['record_sha256'] = digest(result)
    Path(__file__).with_name('CALIBRATION.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'digest': result['record_sha256'], 'seconds': time.perf_counter()-start,
                      'positions': sum(x['original_positions'] for x in fixtures),
                      'all_three_frames_and_moments_match': True}))


if __name__ == '__main__':
    run()
