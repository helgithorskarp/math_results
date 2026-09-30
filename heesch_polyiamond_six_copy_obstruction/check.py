"""Exact centroid-join replay of a local two-surround certificate.

six-heesch-2, researcher. Does not load the 89-copy fixture, 2213-pose pool,
SAT formula or discovery propagation trace. Reuses pinned centroid geometry
and prior local-pattern helpers; the old pair lemmas are explicit premises.
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
PARENT_SHA = '5dc9416ca18a86e742667282b095652cd1661c4ceeddb8bc25f7a2ca04701a06'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def helpers():
    path = PUB / 'heesch_polyiamond_second_prefix_rigidity/check.py'
    need(hashlib.sha256(path.read_bytes()).hexdigest() == PARENT_SHA, 'pinned parent helpers')
    spec = importlib.util.spec_from_file_location('rigidity_helpers', path)
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)
    return r, r.dependencies()


def cover(c, g, occupied, vertex, required):
    # Join a target unit face to every prototype unit face. This differs
    # from discovery's convex-vertex anchors and needs no input candidate list.
    slots = c.star(vertex)
    present = [f in occupied for f in slots]
    need(sum(present) in (4, 5), 'not a 60/120-degree remaining gap')
    need(sum(present[j] != present[(j + 1) % 6] for j in range(6)) == 2, 'noncontiguous sectors')
    gap = set(slots) - occupied
    need(required in gap, 'required sector is occupied or not incident')
    joins = set()
    for matrix in g.ms:
        for face in g.fs:
            x, y = c.face(matrix + (0, 0), face)
            if (required[0] - x) % 3 == (required[1] - y) % 3 == 0:
                joins.add(matrix + ((required[0] - x) // 3, (required[1] - y) // 3))
    raw, allowed = [], []
    for q in sorted(joins):
        foot = g.footprint(q)
        incident = set(slots) & foot
        if len(incident) in (1, 2) and incident <= gap:
            raw.append(q)
            if not foot & occupied:
                allowed.append(q)
    return raw, allowed, len(joins), sum(present)


def logic(certificate):
    clauses = certificate['clauses']
    assigned = {}
    for step in certificate['steps']:
        literal, reason = step['literal'], step['reason']
        need(type(literal) is int and abs(literal) not in assigned, 'duplicate/invalid assignment')
        need(type(reason) is int and 0 <= reason < len(clauses), 'invalid reason')
        unresolved = []
        for v in clauses[reason]:
            if abs(v) not in assigned:
                unresolved.append(v)
            else:
                need(assigned[abs(v)] != (v > 0), 'satisfied unit reason')
        need(unresolved == [literal], 'unit not justified')
        assigned[abs(literal)] = literal > 0
    index = certificate['conflict_clause']
    need(type(index) is int and 0 <= index < len(clauses), 'invalid conflict index')
    need(all(abs(v) in assigned and assigned[abs(v)] != (v > 0) for v in clauses[index]), 'no contradiction')
    return len(assigned)


def check(pattern):
    r, c = helpers()
    data = json.loads((PUB / 'heesch_polyiamond_deficit_review1/input.json').read_text())
    g = c.Geometry(c.shape(data['side_signs']))
    need(pattern['tile'] == 'T214' and pattern['kind'] == 'two_surround_obstruction', 'pattern scope')
    fixed = [r.pose(q) for q in pattern['poses']]
    providers = [tuple(q) for q in pattern['providers']]
    need(len(fixed) == 6 and len(set(fixed)) == 6, 'six distinct fixed copies')
    need(len(providers) == 18 and len(set(providers)) == 18, 'eighteen distinct providers')
    need(all(all(type(v) is int for v in q) and q[:4] in g.ms for q in fixed + providers), 'invalid pose')
    occupied = g.union(fixed)
    need(all(not g.footprint(q) & occupied for q in providers), 'provider overlaps fixed pattern')
    lookup = {q: i for i, q in enumerate(providers, 1)}
    target_rows, cover_indices = [], set()
    for ev in pattern['cover_targets']:
        index = ev['clause']
        need(type(index) is int and 0 <= index < len(pattern['clauses']) and index not in cover_indices, 'cover reason index')
        raw, allowed, joins, sectors = cover(c, g, occupied, tuple(ev['vertex']), tuple(ev['required_centroid']))
        need(all(q in lookup for q in allowed), 'omitted geometric provider')
        ids = sorted(lookup[q] for q in allowed)
        need(ids == sorted(pattern['clauses'][index]) and ids, 'cover list is incomplete')
        need(len(raw) == ev['raw_providers'], 'raw provider count')
        cover_indices.add(index)
        target_rows.append({'vertex': ev['vertex'], 'required_centroid': ev['required_centroid'],
                            'filled_sectors': sectors, 'centroid_joins': joins,
                            'raw_providers': len(raw), 'allowed_provider_ids': ids})
    narrow, _, _ = g.anchor_pool(g.pockets)
    need(len(narrow) == 59 and len(data['retained_indices']) == 21, 'old pair catalogue')
    excluded = {q for i, q in enumerate(narrow, 1) if i not in data['retained_indices']}
    path = PUB / 'heesch_polyiamond_alternate_fourth/patterns.json'
    need(hashlib.sha256(path.read_bytes()).hexdigest() == pattern['imported_patterns_sha256'], 'imported pattern bytes')
    patterns = json.loads(path.read_text())
    checks = r.validate_patterns(c, g, patterns)
    matched = r.pattern_clauses(c, fixed, providers, patterns)
    counts = {'complete_cover': len(cover_indices), 'old_pair_unit': 0, 'old_pair_binary': 0, 'local_pattern': 0}
    for index, clause in enumerate(pattern['clauses']):
        need(clause and len(set(clause)) == len(clause) and
             all(type(v) is int and 1 <= abs(v) <= len(providers) for v in clause), 'clause encoding')
        if index in cover_indices:
            need(all(v > 0 for v in clause), 'mixed cover')
            continue
        need(all(v < 0 for v in clause), 'unsupported extra positive clause')
        ids = [-v for v in clause]
        if len(ids) == 1:
            need(any(g.bad(providers[ids[0] - 1], q, excluded) for q in fixed), 'false old pair unit')
            counts['old_pair_unit'] += 1
        elif len(ids) == 2 and g.bad(providers[ids[0] - 1], providers[ids[1] - 1], excluded):
            counts['old_pair_binary'] += 1
        else:
            need(tuple(sorted(clause, key=abs)) in matched, 'false local pattern instance')
            counts['local_pattern'] += 1
    steps = logic(pattern)
    return {'agent': 'six-heesch-2', 'role': 'researcher', 'tile_faces': len(g.fs),
            'fixed_copies': len(fixed), 'fixed_faces': len(occupied),
            'providers': len(providers), 'target_census': target_rows,
            'clause_counts': counts, 'clauses': len(pattern['clauses']), 'unit_steps': steps,
            'imported_pattern_checks': checks, 'unit_conflict_verified': True,
            'scope': 'the specified six-copy pattern has no two further strict real surrounds, with arbitrary topology'}


def positive():
    r, c = helpers()
    data = json.loads((PUB / 'heesch_polyiamond_deficit_review1/input.json').read_text())
    g = c.Geometry(c.shape(data['side_signs']))
    witness = json.loads((BASE / 'escape-witness.json').read_text())
    need(witness['tile'] == 'T214' and witness['depth'] == 4, 'positive scope')
    layers = [[] for _ in range(5)]
    for row in witness['placements']:
        level, q = row['level'], r.pose(row)
        need(type(level) is int and 0 <= level < 5 and q[:4] in g.ms and
             all(type(v) is int for v in q), 'positive pose')
        layers[level].append(q)
    need(layers[0] == [c.IDENTITY] and list(map(len, layers)) == [1, 5, 12, 30, 41], 'positive counts')
    fixed, rows, last_vertices, last_layer = [], [], set(), set()
    for level, layer in enumerate(layers):
        fixed.extend(layer)
        occupied = g.union(fixed)
        mesh, vertices = c.mesh(occupied)
        if level:
            need(all(set(c.star(v)) <= occupied for v in last_vertices), 'incomplete previous strict surround')
            need(all(last_layer & {c.point(q, v) for v in g.vs} for q in layer), 'no preceding-layer contact')
        mesh.update(level=level, layer_copies=len(layer), cumulative_copies=len(fixed))
        rows.append(mesh)
        last_vertices = vertices
        last_layer = {c.point(q, v) for q in layer for v in g.vs}
    # Every real tile automorphism is an integral D12 pose: it maps the
    # boundary directions to boundary directions and an integer vertex to
    # an integer vertex. A one-face join enumerates this complete finite set.
    target = min(g.fs)
    possible = set()
    for matrix in g.ms:
        for face in g.fs:
            x, y = c.face(matrix + (0, 0), face)
            if (target[0] - x) % 3 == (target[1] - y) % 3 == 0:
                possible.add(matrix + ((target[0] - x) // 3, (target[1] - y) // 3))
    symmetries = sorted(q for q in possible if g.footprint(q) == g.fs)
    need(c.IDENTITY in symmetries, 'tile identity absent')
    physical = {c.compose(q, s) for q in fixed for s in symmetries}
    pattern = json.loads((BASE / 'pattern.json').read_text())
    relative = [r.pose(q) for q in pattern['poses']]
    need(c.IDENTITY == relative[0], 'normalized first copy')
    instances = [a for a in sorted(physical) if all(c.compose(a, q) in physical for q in relative)]
    need(not instances, 'positive control contains the six-copy pattern')
    gap = json.loads((BASE / 'single-gap.json').read_text())
    gap_checks = r.validate_patterns(c, g, [gap])
    need(gap['kind'] == 'empty_corner' and len(gap['poses']) == 3, 'single-gap scope')
    return {'disc_coronas': rows, 'positive_witness_sha256': hashlib.sha256((BASE / 'escape-witness.json').read_bytes()).hexdigest(),
            'tile_automorphisms': [list(q) for q in symmetries], 'six_copy_pattern_instances': len(instances),
            'single_gap_check': gap_checks, 'single_gap_sha256': hashlib.sha256((BASE / 'single-gap.json').read_bytes()).hexdigest()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pattern', type=Path, default=BASE / 'pattern.json')
    ap.add_argument('--output', type=Path)
    ap.add_argument('--controls', action='store_true')
    ap.add_argument('--expected', type=Path)
    args = ap.parse_args()
    start = time.monotonic()
    pattern = json.loads(args.pattern.read_text())
    report = check(pattern)
    report['positive_control_and_single_gap'] = positive()
    if args.controls:
        for name in ['shifted_cap', 'false_provider', 'flipped_unit']:
            bad = copy.deepcopy(pattern)
            if name == 'shifted_cap':
                bad['poses'][-1]['translation'][0] += 1
            elif name == 'false_provider':
                bad['providers'][0][4] += 1
            else:
                bad['steps'][0]['literal'] *= -1
            try:
                check(bad)
            except ValueError:
                continue
            raise ValueError(('control accepted', name))
        report['rejected_controls'] = ['shifted_cap', 'false_provider', 'flipped_unit']
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
