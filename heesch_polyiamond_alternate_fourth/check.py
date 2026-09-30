"""six-heesch-2: four disc coronas and an all-real two-surround obstruction.

Exact standard-library replay: regenerate every necessary corner provider,
validate 19 sparse clauses geometrically and replay 18 unit steps. No SAT,
dense CNF or DRAT input. Four old interior-pair exclusions are mathematical
premises. Earlier centroid primitives and sparse-clause helpers are pinned.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
PARENT_SHA = '5dc9416ca18a86e742667282b095652cd1661c4ceeddb8bc25f7a2ca04701a06'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def helpers():
    path = BASE.parent / 'heesch_polyiamond_second_prefix_rigidity/check.py'
    need(hashlib.sha256(path.read_bytes()).hexdigest() == PARENT_SHA, 'parent helper bytes')
    spec = importlib.util.spec_from_file_location('prior_rigidity_helpers', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, module.dependencies()


def positive(c, r, g, witness):
    need(witness['tile'] == 'T214' and witness['depth'] == 4, 'witness scope')
    layers = [[] for _ in range(5)]
    for row in witness['placements']:
        level, q = row['level'], r.pose(row)
        need(type(level) is int and 0 <= level <= 4, 'layer encoding')
        need(all(type(v) is int for v in q) and q[:4] in g.ms, 'pose encoding')
        layers[level].append(q)
    need(layers[0] == [c.IDENTITY] and [len(v) for v in layers] == [1, 5, 12, 30, 41], 'root/layer counts')
    g.union([q for layer in layers for q in layer])
    fixed, previous_vertices, previous_layer_vertices, rows = [], set(), set(), []
    for level, layer in enumerate(layers):
        fixed.extend(layer)
        occupied = g.union(fixed)
        mesh, vertices = c.mesh(occupied)
        if level:
            need(all(set(c.star(v)) <= occupied for v in previous_vertices), 'incomplete previous surround')
            need(all(previous_layer_vertices & {c.point(q, v) for v in g.vs} for q in layer), 'previous-layer contact')
        mesh.update({'level': level, 'layer_copies': len(layer), 'cumulative_copies': len(fixed)})
        rows.append(mesh)
        previous_vertices = vertices
        previous_layer_vertices = {c.point(q, v) for q in layer for v in g.vs}
    return fixed, occupied, previous_vertices, rows


def unit_conflict(r, certificate):
    assigned = r.replay(dict(certificate, forced_third_indices=[]))
    index = certificate['conflict_clause']
    need(type(index) is int and 0 <= index < len(certificate['clauses']), 'conflict index')
    need(all(abs(v) in assigned and assigned[abs(v)] != (v > 0)
             for v in certificate['clauses'][index]), 'conflict clause is not false')
    return len(assigned)


def run(controls=False):
    r, c = helpers()
    data = json.loads((BASE.parent / 'heesch_polyiamond_deficit_review1/input.json').read_text())
    g = c.Geometry(c.shape(data['side_signs']))
    witness = json.loads((BASE / 'witness.json').read_text())
    certificate = json.loads((BASE / 'certificate.json').read_text())
    need(hashlib.sha256((BASE / 'witness.json').read_bytes()).hexdigest() == certificate['witness_sha256'], 'witness bytes')
    fixed, occupied, vertices, lower_rows = positive(c, r, g, witness)
    targets = [v for v in vertices if len(set(c.star(v)) & occupied) in (4, 5)]
    missing = set().union(*(set(c.star(v)) - occupied for v in targets))
    poses, trials = r.pool(c, g, occupied, missing)
    need(r.digest(poses) == certificate['pool_sha256'], 'complete regenerated pose pool')
    owners = {f: [] for f in sorted(missing)}
    for i, q in enumerate(poses, 1):
        for f in g.footprint(q) & owners.keys():
            owners[f].append(i)
    raw, _, _ = g.anchor_pool(g.pockets)
    need(len(raw) == 59 and len(data['retained_indices']) == 21, 'old pair catalogue')
    excluded = {q for i, q in enumerate(raw, 1) if i not in data['retained_indices']}
    patterns = json.loads((BASE / 'patterns.json').read_text())
    need(len(patterns) == 2 and all(row['kind'] == 'empty_corner' and len(row['poses']) == 3 for row in patterns), 'new local patterns')
    pattern_checks = r.validate_patterns(c, g, patterns)
    clause_checks = r.clauses_valid(c, g, certificate, fixed, poses, owners, excluded, patterns)
    assignments = unit_conflict(r, certificate)
    if controls:
        flipped = copy.deepcopy(certificate)
        flipped['steps'][0]['literal'] *= -1
        truncated = copy.deepcopy(certificate)
        truncated['steps'].pop()
        for label, bad in [('flipped_unit', flipped), ('deleted_terminal_unit', truncated)]:
            try:
                unit_conflict(r, bad)
            except ValueError:
                continue
            raise ValueError(('malformed control accepted', label))
    return {'agent': 'six-heesch-2', 'role': 'researcher', 'tile_faces': len(g.fs),
            'positive_disc_coronas': lower_rows, 'witness_sha256': certificate['witness_sha256'],
            'fixed_copies': len(fixed), 'reentrant_vertices': len(targets),
            'required_faces': len(missing), 'centroid_join_trials': trials,
            'complete_necessary_pool': len(poses), 'pool_sha256': r.digest(poses),
            'local_pattern_checks': pattern_checks, 'sparse_clause_checks': clause_checks,
            'sparse_clauses': len(certificate['clauses']), 'unit_steps': len(certificate['steps']),
            'assigned_variables': assignments, 'unit_conflict_verified': True,
            'scope': 'specified four-corona prefix admits no fifth strict surround with a further sixth strict surround; arbitrary real motions and topology'}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--controls', action='store_true')
    ap.add_argument('--expected', type=Path)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    report = run(args.controls)
    if args.expected:
        need(report == json.loads(args.expected.read_text()), 'expected output mismatch')
    text = json.dumps(report, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')
