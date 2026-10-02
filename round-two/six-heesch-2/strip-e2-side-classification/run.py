"""Bounded search-free proof jobs; UV and axial engines are separate."""
from copy import deepcopy
from datetime import datetime, timezone
import argparse
import hashlib
import json
from pathlib import Path
import resource
import signal
import time

import deps
import strip_contact_reader as R
import strip_parametric_geometry as G
from strip_columns import require
import uv_cover as U
import repeated_cover as V
import axial_reader as A

HERE = Path(__file__).absolute().parent
I = ((1, 0, 0, 1), (0, 0), (0, 0))
SHIFT = ((1, 0, 0, 1), (0, 6), (-1, 3))
ARRAY = {'k': '2n+r', 'r': [0, 1], 'minimum_n': 3, 'matrix': [-1, 0, 0, -1],
         'u': '12+6j', 'v': '2n+r+6+2j', 'jlo': 0, 'jhi': 'n-2+r'}


def bind(data):
    require(data['agent'] == 'six-heesch-2' and data['role'] == 'researcher', 'Wrong author attribution')
    require(data['minimum_k'] == 6 and R.freeze(data['E2_fixed']) == (I, SHIFT), 'Wrong fixed E2 endpoint')
    require(len(data['E2_surround']) == 8, 'Wrong eight-copy E2 surround')
    require(data['repeated_array'] == ARRAY, 'Changed declared repeated-array bounds')
    cases = data['E1_cases']
    require(len(cases) == 11 and {x['name'] for x in cases} == {f'contact-{j:02d}' for j in range(1, 12)},
            'Missing or duplicated named E1 case')
    require(len({R.freeze(x['pose']) for x in cases}) == 11, 'Duplicated E1 target pose')
    for case in cases:
        require(R.freeze(case['fixed']) == (I, R.freeze(case['pose'])), 'E1 fixed target differs from its named pose')
        require(case['kind'] == ('repeated_angle' if case['name'] == 'contact-02' else 'finite_affine'),
                'Changed E1 witness kind')
    array = next(x for x in cases if x['name'] == 'contact-02')
    require(R.freeze(array['pose']) == ((-2, 3, -1, 1), (0, 5), (0, 3)), 'Wrong repeated-angle target')


def inventory(data, engine, guard, expected=None):
    types = [x['pose'] for x in data['E1_cases']] if expected is None else expected
    if engine == 'axial':
        return A.contact_types(data['E2_fixed'], data['E2_surround'], types, guard)
    poses = R.freeze((*data['E2_fixed'], *data['E2_surround']))
    rows = {(i, j): G.touching(G.relative(a, b))
            for j, b in enumerate(poses) for i, a in enumerate(poses[:j])}
    part = G.partition(list(rows.values()))
    require(part == R.splitter(list(rows.values())), 'UV contact partitions disagree')
    actual, pairs = set(), set()
    expected_types = set(R.freeze(types))
    for k in part['representatives']:
        guard()
        for (i, j), row in rows.items():
            if G.evaluate(row, k):
                rel = G.relative(poses[i], poses[j])
                canonical = min(rel, G.inverse(rel))
                require(canonical in expected_types, 'Unproved touching E1 type in E2 pattern')
                actual.add(canonical)
                pairs.add((i, j))
    require(actual == expected_types, 'Changed E1 contact inventory')
    return {'touching_pairs': sorted(pairs), 'types': sorted(actual), 'partition': part}


def constant(data, engine, guard):
    results = []
    checker = U.check if engine == 'uv' else A.check_constant
    for case in data['E1_cases']:
        if case['kind'] == 'finite_affine':
            row = checker(case['fixed'], case['surround'], guard)
            row['name'] = case['name']
            results.append(row)
    return {'E1_constant_cases': results,
            'outer_halo': checker(data['E2_fixed'], data['E2_surround'], guard),
            'contact_inventory': inventory(data, engine, guard)}


def repeated(data, engine, guard):
    case = next(x for x in data['E1_cases'] if x['kind'] == 'repeated_angle')
    return V.check(case, guard) if engine == 'uv' else A.check_array(case, guard)


def controls(data, engine, guard):
    checker = U.check if engine == 'uv' else A.check_constant
    array_checker = V.check if engine == 'uv' else A.check_array
    array = next(x for x in data['E1_cases'] if x['kind'] == 'repeated_angle')
    bad_array_first, bad_array_odd = deepcopy(array), deepcopy(array)
    del bad_array_first['even_caps'][0]
    del bad_array_odd['odd_caps'][-1]
    bad_schema, bad_binding = deepcopy(data), deepcopy(data)
    bad_schema['repeated_array']['jhi'] = 'n-3+r'
    bad_binding['E1_cases'][0]['fixed'][1][1][1] += 1
    tasks = [
        ('missing_outer_copy', lambda: checker(data['E2_fixed'], data['E2_surround'][1:], guard)),
        ('duplicate_outer_copy', lambda: checker(data['E2_fixed'], [data['E2_fixed'][0], *data['E2_surround'][1:]], guard)),
        ('missing_E1_contact_type', lambda: inventory(data, engine, guard,
            [x['pose'] for x in data['E1_cases'] if x['name'] != 'contact-02'])),
        ('missing_even_array_cap', lambda: array_checker(bad_array_first, guard)),
        ('missing_odd_array_cap', lambda: array_checker(bad_array_odd, guard)),
        ('changed_array_bound', lambda: bind(bad_schema)),
        ('changed_E1_target_binding', lambda: bind(bad_binding)),
    ]
    rejected = []
    for label, task in tasks:
        guard()
        try:
            task()
        except ValueError as error:
            rejected.append({'case': label, 'reason': str(error)})
        else:
            raise ValueError('Damaged positive witness was accepted: '+label)
    return {'rejected': rejected, 'count': len(rejected)}


def feet(g, k, tile):
    m, X, Y = A.axial(g)
    pose = m+(A.value(X, k), A.value(Y, k))
    require(pose == R.axial(R.freeze(g), k), 'AX/UV pose conversion differs')
    return set(R.E.affine(tile, pose))


def material_cover(fixed, surround, k, guard):
    guard()
    tile = R.literal(k)
    require(len(tile) == 4*k+3 and R.E.component(tile, min(tile)) == set(tile) and not R.E.holes(tile),
            'Literal prototype is not the claimed disc polyhex')
    copies = [feet(g, k, tile) for g in (*fixed, *surround)]
    occupied = set()
    for copy in copies:
        require(occupied.isdisjoint(copy), 'Unit-edge audit finds an overlap')
        occupied.update(copy)
    old = set().union(*copies[:len(fixed)])
    halo = R.E.halo(old)
    require(halo <= set().union(*copies[len(fixed):]), 'Unit-edge audit finds an uncovered original-halo cell')
    return {'surround_copies': len(surround), 'halo_cells': len(halo)}, copies


def audit(data, guard):
    results = []
    for k in (6, 7, 8, 9, 12, 40):
        rows = []
        for case in data['E1_cases']:
            if case['kind'] == 'finite_affine':
                surround = case['surround']
            else:
                n, residue = divmod(k, 2)
                caps = case['even_caps' if residue == 0 else 'odd_caps']
                array = [((-1, 0, 0, -1), (0, 12+6*j), (1, 6+2*j)) for j in range(n-1+residue)]
                surround = [*caps, *array]
            row, _ = material_cover(case['fixed'], surround, k, guard)
            rows.append({'name': case['name'], **row})
        outer, copies = material_cover(data['E2_fixed'], data['E2_surround'], k, guard)
        contact = [(i, j) for j, b in enumerate(copies) for i, a in enumerate(copies[:j]) if R.E.touching(a, b)]
        require(len(contact) == 19, 'Unit-edge contact inventory is not19')
        results.append({'k': k, 'E1_cases': rows, 'outer_halo': outer, 'touching_pairs': contact})
    return {'finite_material_controls': results, 'scope': 'Implementation audit; not the all-k proof'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--engine', choices=('uv', 'axial', 'joint'), required=True)
    parser.add_argument('--part', choices=('core', 'array', 'controls', 'audit'), required=True)
    args = parser.parse_args()
    require((args.engine == 'joint') == (args.part == 'audit'), 'Audit uses the joint engine only')
    start = time.monotonic()
    calls = 0
    def guard():
        nonlocal calls
        calls += 1
        if deps.paused() or time.monotonic()-start >= 43 or calls > 100000:
            raise RuntimeError('Operational/43s/100000-operation guard; unfinished proof job inconclusive')
    def alarm(a, b):
        raise RuntimeError('45s signal guard; unfinished proof job inconclusive')
    signal.signal(signal.SIGALRM, alarm)
    signal.alarm(45)
    data = json.loads((HERE/'inputs.json').read_text())
    bind(data)
    if args.part == 'core':
        math = constant(data, args.engine, guard)
    elif args.part == 'array':
        math = repeated(data, args.engine, guard)
    elif args.part == 'controls':
        math = controls(data, args.engine, guard)
    else:
        math = audit(data, guard)
    guard()
    mode = 'normal' if __debug__ else 'optimized'
    out = {'agent': 'six-heesch-2', 'role': 'researcher', 'complete': True, 'engine': args.engine,
           'part': args.part, 'evidence': math, 'mathematics_sha256': R.sha(math), 'guard_calls': calls,
           'mode': mode, 'seconds': round(time.monotonic()-start, 3),
           'max_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
           'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'checked_utc': datetime.now(timezone.utc).isoformat()}
    directory = HERE/'generated'
    directory.mkdir(exist_ok=True)
    (directory/f'{args.engine}-{args.part}-{mode}.json').write_text(json.dumps(out, indent=2)+'\n')
    signal.alarm(0)
    print(json.dumps({k: v for k, v in out.items() if k != 'evidence'}, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
