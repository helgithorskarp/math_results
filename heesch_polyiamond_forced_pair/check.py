"""Centroid-join check of the three-copy T214 forced-filler obstruction.

six-heesch-2, researcher. No SAT/CNF, search pool, propagation extractor,
or author vertex-anchor generator is used. The old interior-pair lemmas
are mathematical premises; their attachment catalogue is regenerated here.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import time

BASE = Path(__file__).resolve().parent
PUB = BASE.parent
PINS = {
    'heesch_polyiamond_deficit_review1/check.py':
        '9c96aa23e9bcc4d84d8cc222523d7db515887b09219c770838cd4b7073402eef',
    'heesch_polyiamond_deficit_review1/input.json':
        '158e3ad324a15e47c956813e9813600b3908c339649a4cafd826f0dc51cc7cc0',
    'heesch_polyiamond_six_copy_obstruction/escape-witness.json':
        '121a768a90e9d8519168f0ee6488f997d9de45d6a12d8de71eaa4ca36019d60b',
    'heesch_polyiamond_six_copy_obstruction/pattern.json':
        '9a6bdd8df8484a7ffd28e32a2042325c66035564085c4e8c9b29e93782b35799',
    'heesch_polyiamond_forced_pair/escape-both-witness.json':
        'b949b4b8c4b0c738ccd54742356ddf803e82e63759683f138449221dc3daceae',
}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def geometry():
    for path, digest in PINS.items():
        need(hashlib.sha256((PUB / path).read_bytes()).hexdigest() == digest,
             ('pinned input', path))
    path = PUB / 'heesch_polyiamond_deficit_review1/check.py'
    spec = importlib.util.spec_from_file_location('centroid_geometry', path)
    c = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(c)
    data = json.loads((PUB / 'heesch_polyiamond_deficit_review1/input.json').read_text())
    g = c.Geometry(c.shape(data['side_signs']))
    need(len(g.fs) == 214, 'prototype face count')
    c.mesh(g.fs)
    return c, g, data


def pose(row):
    return tuple(row['matrix']) + tuple(row['translation'])


def check(pattern):
    c, g, data = geometry()
    need(pattern['kind'] == 'two_surround_obstruction' and pattern['tile'] == 'T214', 'scope')
    fixed = [pose(row) for row in pattern['poses']]
    providers = [tuple(q) for q in pattern['providers']]
    need(len(fixed) == len(set(fixed)) == 3 and fixed[0] == c.IDENTITY,
         'three distinct normalized copies')
    need(len(providers) == len(set(providers)) == 1, 'one certificate provider')
    need(all(len(q) == 6 and all(type(v) is int for v in q) and q[:4] in g.ms
             for q in fixed + providers), 'invalid pose')
    occupied = g.union(fixed)
    target = pattern['cover_targets'][0]
    need(len(pattern['cover_targets']) == 1 and target['clause'] == 0, 'one target')
    vertex, required = tuple(target['vertex']), tuple(target['required_centroid'])
    slots = c.star(vertex)
    present = [f in occupied for f in slots]
    need(sum(present) == 5 and required in set(slots) - occupied, 'one missing sector')
    need(sum(present[i] != present[(i + 1) % 6] for i in range(6)) == 2,
         'noncontiguous local sectors')
    # Join the required face to every prototype face under all twelve
    # integral linear isometries, rather than matching acute vertices.
    joins = set()
    for matrix in g.ms:
        for face in g.fs:
            x, y = c.face(matrix + (0, 0), face)
            if (required[0] - x) % 3 == (required[1] - y) % 3 == 0:
                joins.add(matrix + ((required[0] - x) // 3, (required[1] - y) // 3))
    raw, allowed, census = [], [], []
    for q in sorted(joins):
        foot = g.footprint(q)
        if set(slots) & foot != {required}:
            continue
        raw.append(q)
        blockers = []
        for index, p in enumerate(fixed, 1):
            overlap = foot & g.footprint(p)
            if overlap:
                blockers.append({'fixed': index, 'overlap_faces': len(overlap),
                                 'example_centroid': list(min(overlap))})
        if not blockers:
            allowed.append(q)
        census.append({'pose': list(q), 'blockers': blockers})
    need(len(raw) == target['raw_providers'] == 22, 'raw acute census')
    need(allowed == providers, 'incomplete or false sole provider')
    narrow, trials, gaps = g.anchor_pool(g.pockets)
    retained = set(data['retained_indices'])
    need(len(narrow) == 59 and len(retained) == 21 and
         all(type(i) is int and 1 <= i <= 59 for i in retained), 'old pair catalogue')
    old_pairs = []
    q = providers[0]
    # Check both relative directions explicitly; do not call Geometry.bad.
    for index, p in enumerate(fixed, 1):
        for direction, a, b in [('provider_to_fixed', q, p), ('fixed_to_provider', p, q)]:
            relative = c.compose(c.inverse(a), b)
            if relative in narrow:
                attachment = narrow.index(relative) + 1
                if attachment not in retained:
                    old_pairs.append({'fixed': index, 'direction': direction,
                                      'attachment': attachment, 'relative_pose': list(relative)})
    need(old_pairs, 'false old interior-pair unit')
    need(pattern['clauses'] == [[1], [-1]], 'certificate clauses')
    need(pattern['steps'] == [{'literal': 1, 'reason': 0}] and
         pattern['conflict_clause'] == 1, 'unit contradiction')
    return {'agent': 'six-heesch-2', 'role': 'researcher', 'tile_faces': len(g.fs),
            'fixed_copies': len(fixed), 'fixed_faces': len(occupied),
            'target_vertex': list(vertex), 'required_centroid': list(required),
            'filled_sectors': sum(present), 'centroid_joins': len(joins),
            'acute_provider_census': census, 'raw_providers': len(raw),
            'whole_disjoint_providers': [list(q) for q in allowed],
            'forbidden_interior_pairs': old_pairs,
            'old_pair_catalogue': {'raw': len(narrow), 'retained': len(retained),
                                   'forbidden': len(narrow) - len(retained),
                                   'centroid_trials': trials, 'target_faces': gaps},
            'clauses': 2, 'unit_steps': 1, 'unit_conflict_verified': True,
            'scope': 'no B,D containing this triple with target vertex interior in B and B strictly interior in D'}


def escape_control(pattern, avoid_both=False):
    c, g, _ = geometry()
    path = ('heesch_polyiamond_forced_pair/escape-both-witness.json' if avoid_both else
            'heesch_polyiamond_six_copy_obstruction/escape-witness.json')
    witness = json.loads((PUB / path).read_text())
    need(witness['tile'] == 'T214' and witness['depth'] == 4, 'positive scope')
    fixed = [pose(row) for row in witness['placements']]
    layers = [[] for _ in range(5)]
    for row, q in zip(witness['placements'], fixed):
        level = row['level']
        need(type(level) is int and 0 <= level <= 4 and q[:4] in g.ms and
             all(type(v) is int for v in q), 'escape control pose')
        layers[level].append(q)
    need(layers[0] == [c.IDENTITY] and list(map(len, layers)) == [1, 5, 12, 30, 41], 'escape layers')
    prefix, rows, previous_vertices, previous_layer = [], [], set(), set()
    for level, layer in enumerate(layers):
        prefix.extend(layer)
        occupied = g.union(prefix)
        mesh, vertices = c.mesh(occupied)
        if level:
            need(all(set(c.star(v)) <= occupied for v in previous_vertices), 'incomplete escape surround')
            need(all(previous_layer & {c.point(q, v) for v in g.vs} for q in layer), 'escape layer contact')
        mesh.update(level=level, layer_copies=len(layer), cumulative_copies=len(prefix))
        rows.append(mesh)
        previous_vertices = vertices
        previous_layer = {c.point(q, v) for q in layer for v in g.vs}
    relative = [pose(row) for row in pattern['poses']]
    lookup = {q: i for i, q in enumerate(fixed)}
    instances = []
    for anchor in fixed:
        keys = [c.compose(anchor, q) for q in relative]
        if all(q in lookup for q in keys):
            instances.append({'anchor': list(anchor), 'zero_based_witness_indices': [lookup[q] for q in keys],
                              'levels': [witness['placements'][lookup[q]]['level'] for q in keys]})
    report = {'disc_coronas': rows, 'displayed_pattern_instances': instances,
              'witness_sha256': PINS[path]}
    if not avoid_both:
        need(instances, 'no displayed occurrence in the escape control')
        return report
    # A geometric automorphism maps the six boundary directions and a
    # lattice boundary vertex into themselves. One-face joins enumerate
    # its resulting complete integral D12 list.
    target = min(g.fs)
    possible = set()
    for matrix in g.ms:
        for face in g.fs:
            x, y = c.face(matrix + (0, 0), face)
            if (target[0] - x) % 3 == (target[1] - y) % 3 == 0:
                possible.add(matrix + ((target[0] - x) // 3, (target[1] - y) // 3))
    symmetries = sorted(q for q in possible if g.footprint(q) == g.fs)
    need(symmetries == [c.IDENTITY], 'prototype symmetry census')
    need(not instances, 'new positive control contains the three-copy pattern')
    older = json.loads((PUB / 'heesch_polyiamond_six_copy_obstruction/pattern.json').read_text())
    six = [pose(row) for row in older['poses']]
    need(six[0] == c.IDENTITY, 'older normalized pattern')
    older_instances = [anchor for anchor in fixed if
                       all(c.compose(anchor, q) in lookup for q in six)]
    need(not older_instances, 'new positive control contains the six-copy pattern')
    report.update(tile_automorphisms=[list(q) for q in symmetries],
                  six_copy_pattern_instances=len(older_instances),
                  all_common_congruences_checked=True)
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pattern', type=Path, default=BASE / 'pattern.json')
    ap.add_argument('--output', type=Path)
    ap.add_argument('--expected', type=Path)
    ap.add_argument('--controls', action='store_true')
    args = ap.parse_args()
    start = time.monotonic()
    pattern = json.loads(args.pattern.read_text())
    report = check(pattern)
    report['escape_control'] = escape_control(pattern)
    report['escape_both_control'] = escape_control(pattern, avoid_both=True)
    if args.controls:
        for name in ['shifted_blocker', 'false_provider', 'flipped_unit']:
            bad = copy.deepcopy(pattern)
            if name == 'shifted_blocker':
                bad['poses'][1]['translation'][0] -= 40
            elif name == 'false_provider':
                bad['providers'][0][4] += 1
            else:
                bad['steps'][0]['literal'] *= -1
            try:
                check(bad)
            except ValueError:
                continue
            raise ValueError(('control accepted', name))
        report['rejected_controls'] = ['shifted_blocker', 'false_provider', 'flipped_unit']
    report['pattern_sha256'] = hashlib.sha256(args.pattern.read_bytes()).hexdigest()
    if args.expected:
        need(report == json.loads(args.expected.read_text()), 'expected output mismatch')
    text = json.dumps(report, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')
    print(json.dumps({'seconds': round(time.monotonic() - start, 3),
                      'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}), flush=True)


if __name__ == '__main__':
    main()
