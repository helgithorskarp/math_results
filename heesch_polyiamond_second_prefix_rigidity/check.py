"""six-heesch-2: exact sparse unit proof and all-real terminal providers.

Standard-library replay. Reuses byte-pinned centroid primitives from the
independent earlier review; regenerates the complete corner inventory and
checks sparse clauses directly. No SAT, DRAT or dense formula is imported.
The 38 old interior-pair lemmas remain explicit mathematical premises.
"""
import argparse
from collections import Counter
import copy
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import resource
import time

BASE = Path(__file__).resolve().parent
PINS = {
    'heesch_polyiamond_deficit_review1/check.py': '9c96aa23e9bcc4d84d8cc222523d7db515887b09219c770838cd4b7073402eef',
    'heesch_polyiamond_deficit_review1/input.json': '158e3ad324a15e47c956813e9813600b3908c339649a4cafd826f0dc51cc7cc0',
    'heesch_polyiamond_fixed_fourth_extension/patterns.json': '4bb58e3394b97eca19d6ec76d9955b752144c7ae86820c7a65abf0e0b8e56124',
    'heesch_polyiamond_fixed_third_extension/hole.json': '2c1efa4d79ea1776bc55999d8470a28b6be90b81a6bb03a281f611d2087de10e',
}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(obj):
    return hashlib.sha256(json.dumps(obj, separators=(',', ':')).encode()).hexdigest()


def dependencies():
    for path, sha in PINS.items():
        need(hashlib.sha256((BASE.parent / path).read_bytes()).hexdigest() == sha, ('dependency bytes', path))
    path = BASE.parent / 'heesch_polyiamond_deficit_review1/check.py'
    spec = importlib.util.spec_from_file_location('prior_centroid_geometry', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pose(row):
    return tuple(row['matrix'] + row['translation'])


def cell(row):
    k, x, y = row
    need(k in (0, 1) and all(type(t) is int for t in row), 'cell coordinates')
    return (3 * x + k + 1, 3 * y + k + 1)


def pool(c, g, occupied, missing):
    # A centroid congruence enumerates every whole integral copy containing
    # any specified missing unit face. Small-gap locking supplies necessity.
    anchors = set()
    for matrix in g.ms:
        for face in g.fs:
            u, v = c.face(matrix + (0, 0), face)
            for x, y in missing:
                if (x - u) % 3 == 0 and (y - v) % 3 == 0:
                    anchors.add(matrix + ((x - u) // 3, (y - v) // 3))
    poses = sorted(q for q in anchors if not occupied & g.footprint(q))
    need(len(poses) <= 10000, 'incomplete inventory guard')
    return poses, len(anchors)


def providers(c, g, vertex, required, gap):
    out = {}
    for matrix in g.ms:
        for source in g.vs:
            if g.angles[source] not in (1, 2):
                continue
            x, y = c.point(matrix + (0, 0), source)
            q = matrix + (vertex[0] - x, vertex[1] - y)
            foot = g.footprint(q)
            incident = set(c.star(vertex)) & foot
            if required in foot and len(incident) in (1, 2) and incident <= gap:
                out[q] = foot
    return sorted(out), out


def validate_patterns(c, g, patterns):
    reports = []
    for row in patterns:
        fixed = list(map(pose, row['poses']))
        need(c.IDENTITY in fixed, 'normalized pattern anchor')
        occupied = g.union(fixed)
        if row['kind'] == 'small_hole':
            hole = set(map(cell, row['hole_cells']))
            need(0 < len(hole) < len(g.fs) and not hole & occupied, 'hole area')
            for face in hole:
                vs = c.vertices(face)
                for u, v in combinations(vs, 2):
                    w = next(t for t in vs if t not in (u, v))
                    across = c.triangle((u, v, (u[0] + v[0] - w[0], u[1] + v[1] - w[1])))
                    need(across in hole or across in occupied, 'unenclosed hole edge')
            reports.append({'kind': row['kind'], 'hole_faces': len(hole), 'copies': len(fixed)})
            continue
        targets = row['targets'] if row['kind'] == 'forced_clash' else [
            {'vertex': row['target'], 'cell': row['missing_cell']}]
        available, counts = [], []
        for target in targets:
            vertex, required = tuple(target['vertex']), cell(target['cell'])
            filled = set(c.star(vertex)) & occupied
            gap = set(c.star(vertex)) - occupied
            need(len(filled) in (4, 5) and required in gap, 'small corner gap')
            options, feet = providers(c, g, vertex, required, gap)
            available.append([q for q in options if not feet[q] & occupied])
            counts.append(len(options))
        if row['kind'] == 'empty_corner':
            need(len(available) == 1 and not available[0], 'fillable alleged empty corner')
        else:
            need(row['kind'] == 'forced_clash' and len(available) == 2 and all(available), 'clash targets')
            need(all(g.footprint(p) & g.footprint(q) for p in available[0] for q in available[1]), 'compatible clash providers')
        reports.append({'kind': row['kind'], 'provider_trials': counts, 'available_counts': list(map(len, available))})
    return reports


def pattern_clauses(c, fixed, poses, patterns):
    lookup = {q: 0 for q in fixed}
    lookup.update({q: i for i, q in enumerate(poses, 1)})
    result = set()
    for row in patterns:
        relative = list(map(pose, row['poses']))
        for anchor in fixed + poses:
            keys = [c.compose(anchor, q) for q in relative]
            if all(q in lookup for q in keys):
                clause = tuple(-i for i in sorted({lookup[q] for q in keys} - {0}))
                need(clause, 'impossible fixed pattern')
                result.add(clause)
    return result


def clauses_valid(c, g, certificate, fixed, poses, owners, excluded, patterns):
    allowed_covers = {tuple(js) for js in owners.values()}
    allowed_patterns = pattern_clauses(c, fixed, poses, patterns)
    count = Counter()
    for clause in certificate['clauses']:
        need(clause and len(set(clause)) == len(clause), 'empty/duplicate sparse clause')
        need(all(type(v) is int and 1 <= abs(v) <= len(poses) for v in clause), 'clause variable')
        if all(v > 0 for v in clause):
            need(tuple(clause) in allowed_covers, 'incomplete or false cover clause')
            count['complete_cover'] += 1
            continue
        need(all(v < 0 for v in clause), 'mixed unsupported sparse clause')
        ids = [-v for v in clause]
        if len(ids) == 1 and any(g.bad(poses[ids[0] - 1], q, excluded) for q in fixed):
            count['old_interior_pair_unit'] += 1
        elif len(ids) == 2 and g.footprint(poses[ids[0] - 1]) & g.footprint(poses[ids[1] - 1]):
            count['whole_overlap_pair'] += 1
        elif len(ids) == 2 and g.bad(poses[ids[0] - 1], poses[ids[1] - 1], excluded):
            count['old_interior_pair_binary'] += 1
        else:
            need(tuple(sorted(clause, key=abs)) in allowed_patterns, 'unsupported interior pattern')
            count['local_interior_pattern'] += 1
    return dict(sorted(count.items()))


def replay(certificate):
    assigned = {}
    for step in certificate['steps']:
        literal, reason = step['literal'], step['reason']
        need(type(literal) is int and abs(literal) not in assigned, 'repeated/invalid unit')
        need(type(reason) is int and 0 <= reason < len(certificate['clauses']), 'reason index')
        remaining = []
        for v in certificate['clauses'][reason]:
            if abs(v) not in assigned:
                remaining.append(v)
            else:
                need(assigned[abs(v)] != (v > 0), 'unit reason is already satisfied')
        need(remaining == [literal], 'unproved unit step')
        assigned[abs(literal)] = literal > 0
    need(all(assigned.get(i) is True for i in certificate['forced_third_indices']), 'missing forced copy')
    return assigned


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--expected', type=Path)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    start = time.monotonic()
    c = dependencies()
    data = json.loads((BASE.parent / 'heesch_polyiamond_deficit_review1/input.json').read_text())
    g = c.Geometry(c.shape(data['side_signs']))
    lower = c.lower(g.fs, data['placements'])
    fixed = [pose(q) for q in data['placements'] if q['level'] <= 2]
    original_third = [pose(q) for q in data['placements'] if q['level'] == 3]
    need(len(fixed) == 17 and len(original_third) == 23, 'fixed prefix counts')
    occupied = g.union(fixed)
    vertices = {v for f in occupied for v in c.vertices(f)}
    corners = sorted(v for v in vertices if len(set(c.star(v)) & occupied) in (4, 5))
    missing = set().union(*(set(c.star(v)) - occupied for v in corners))
    poses, trials = pool(c, g, occupied, missing)
    need(len(poses) == 1268 and digest(poses) == 'f2c9940c161efdebcc16082359ab6d7368fed386b6e9528938dff27bcd5e1193', 'complete pose census mismatch')
    need(len({g.footprint(q) for q in poses}) == len(poses), 'duplicate physical-copy poses')
    owners = {face: [] for face in sorted(missing)}
    for i, q in enumerate(poses, 1):
        for f in g.footprint(q) & owners.keys():
            owners[f].append(i)
    narrow, _, _ = g.anchor_pool(g.pockets)
    need(len(narrow) == 59, 'old attachment catalogue')
    retained = set(data['retained_indices'])
    excluded = {q for i, q in enumerate(narrow, 1) if i not in retained}
    need(len(excluded) == 38, 'old pair premises')
    patterns = json.loads((BASE.parent / 'heesch_polyiamond_fixed_fourth_extension/patterns.json').read_text())
    patterns.append(json.loads((BASE.parent / 'heesch_polyiamond_fixed_third_extension/hole.json').read_text()))
    pattern_reports = validate_patterns(c, g, patterns)
    certificate = json.loads((BASE / 'certificate.json').read_text())
    need(certificate['variables'] == len(poses), 'sparse variable census')
    expected_indices = sorted(i for i, q in enumerate(poses, 1) if q in original_third)
    need(len(expected_indices) == 21 and certificate['forced_third_indices'] == expected_indices, 'incorrect force targets')
    counts = clauses_valid(c, g, certificate, fixed, poses, owners, excluded, patterns)
    assigned = replay(certificate)
    need({i for i, value in assigned.items() if value} == set(expected_indices), 'unexpected core positive')
    forced = [poses[i - 1] for i in expected_indices]
    partial = g.union(fixed + forced)
    terminal_reports = []
    for row in certificate['terminal_corners']:
        vertex = tuple(row['vertex'])
        need(vertex in vertices, 'terminal target is not on second prefix')
        gap = set(c.star(vertex)) - partial
        need(len(gap) == 1, 'terminal gap is not isolated 60 degrees')
        options, feet = providers(c, g, vertex, next(iter(gap)), gap)
        allowed = [q for q in options if not feet[q] & partial]
        need(allowed == [tuple(row['provider'])], 'terminal provider not unique')
        terminal_reports.append({'vertex': list(vertex), 'sector_provider_trials': len(options),
                                 'unique_provider': list(allowed[0])})
    terminals = [tuple(row['provider']) for row in certificate['terminal_corners']]
    need(len(terminals) == 2 and set(forced + terminals) == set(original_third), 'third layer differs from fixture')
    whole = g.union(fixed + forced + terminals)
    halo = set().union(*(set(c.star(v)) - occupied for v in vertices))
    need(halo <= whole, 'second prefix is not strictly interior')
    mesh, _ = c.mesh(whole)
    rejected = []
    for label, mutation in [('flipped unit', lambda cert: cert['steps'][0].update(literal=-cert['steps'][0]['literal'])),
                            ('deleted first reason step', lambda cert: cert['steps'].pop(0))]:
        bad = copy.deepcopy(certificate)
        mutation(bad)
        try:
            replay(bad)
        except ValueError:
            rejected.append(label)
        else:
            raise ValueError(('mutation accepted', label))
    report = {'agent': 'six-heesch-2', 'role': 'researcher',
              'claim': 'arbitrary-motion third corona over the fixed second prefix is unique if a further real strict surround exists',
              'fixed_second_copies': len(fixed), 'fixed_second_faces': len(occupied),
              'reentrant_vertices': len(corners), 'necessary_faces': len(missing),
              'centroid_anchor_trials': trials, 'corner_candidates': len(poses), 'pool_sha256': digest(poses),
              'sparse_clauses': len(certificate['clauses']), 'unit_steps': len(certificate['steps']),
              'clause_types': counts, 'forced_corner_copies': len(forced),
              'terminal_corner_providers': terminal_reports, 'patterns_checked': pattern_reports,
              'complete_third_copies': len(original_third), 'third_total_copies': len(fixed) + len(original_third),
              'second_halo_faces': len(halo), 'final_mesh': mesh,
              'certificate_sha256': hashlib.sha256((BASE / 'certificate.json').read_bytes()).hexdigest(),
              'rejected_mutations': rejected,
              'unchanged_global_interval': [5, 385],
              'checked_fixture_prefix_meshes': lower}
    if args.expected:
        need(json.loads(json.dumps(report)) == json.loads(args.expected.read_text()), 'expected report mismatch')
    text = json.dumps(report, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text)
    print(json.dumps({'seconds': round(time.monotonic() - start, 3),
                      'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}), flush=True)


if __name__ == '__main__':
    main()
