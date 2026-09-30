"""Sparse exact third-branch closure: centroid geometry and bit-mask proofs.

six-heesch-2, researcher. Dense discovery inventories, native solvers and
DRAT are not reader inputs. Earlier geometry and interior-pair lemmas are
byte-pinned dependencies. The arbitrary-motion locking bridge is written.
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


def need(ok, message):
    if not ok:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text())


def context():
    for name, digest in read(BASE / 'dependency-pins.json').items():
        need(hashlib.sha256((PUB / name).read_bytes()).hexdigest() == digest, ('dependency bytes', name))
    path = PUB / 'heesch_polyiamond_original_second_closure/check.py'
    spec = importlib.util.spec_from_file_location('pinned_third_branch_parent', path)
    d = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(d)
    ctx = d.context()
    m, r, f, h, c, g, excluded, tables, dependencies, _ = ctx
    extra = read(BASE / 'extra-singles.json')
    checks = r.verify_patterns(f, h, c, g, extra)
    tables = [('single_surround_pattern', tables[0][1] + extra)] + tables[1:]
    patterns = read(PUB / 'heesch_polyiamond_original_second_closure/two-patterns.json')
    local_checks = {name: d.local(row, ctx) for name, row in sorted(patterns.items())}
    tables.append(('two_surround_original_fourth_pattern', list(patterns.values())))
    return d, (r, f, h, c, g, excluded, tables, dependencies), m, {
        'extra_single_checks': checks, 'imported_two_pattern_checks': local_checks,
        'old_geometric_dependencies': dependencies}


def scope(cert, kind, stages):
    need(cert['kind'] == kind and cert['tile'] == 'T214' and
         type(cert.get('future_surrounds_required', cert.get('surrounds'))) is int and
         cert.get('future_surrounds_required', cert.get('surrounds')) == stages,
         'wrong future-surround license')


def positive(c, g, r, fixture):
    need(fixture['tile'] == 'T214' and fixture['depth'] == 3, 'positive fixture scope')
    layers = [[r.pose(q) for q in fixture['placements'] if q['level'] == j] for j in range(4)]
    need([len(q) for q in layers] == [1, 5, 12, 33] and layers[0] == [c.IDENTITY], 'positive counts or root')
    fixed, previous_vertices, previous_layer, reports = [], set(), set(), []
    for depth, layer in enumerate(layers):
        fixed.extend(layer)
        occupied = g.union(fixed)
        mesh, vertices = c.mesh(occupied)
        need(mesh['chi'] == 1, 'positive union not a disc')
        if depth:
            need(all(set(c.star(v)) <= occupied for v in previous_vertices), 'positive old halo missing')
            need(all(previous_layer & {c.point(q, v) for v in g.vs} for q in layer), 'positive preceding-layer contact missing')
        reports.append(dict(mesh, depth=depth, new_copies=len(layer), cumulative_copies=len(fixed)))
        previous_vertices = vertices
        previous_layer = {c.point(q, v) for q in layer for v in g.vs}
    return layers, reports


def forcing(cert, layers, d, ctx, m):
    scope(cert, 'conditional_third_common_subset', 3)
    r, f, h, c, g, excluded, tables, _ = ctx
    fixed, providers = list(map(r.pose, cert['fixed_poses'])), list(map(tuple, cert['providers']))
    need(fixed == [q for layer in layers[:3] for q in layer] and len(fixed) == 18, 'different second prefix')
    r.valid_poses(g, fixed)
    r.valid_poses(g, providers)
    occupied = g.union(fixed)
    need(all(not g.footprint(q) & occupied for q in providers), 'provider overlaps fixed prefix')
    ids, covers = r.covers(f, c, g, fixed, providers, cert)
    counts = r.negative_clauses(h, c, g, fixed, providers, cert, ids, excluded, tables)
    yes, no = m.forward(cert)
    forced = [providers[i - 1] for i in cert['forced_provider_indices']]
    need(len(forced) == 29, 'different initial forced subset')
    known = fixed + forced
    g.union(known)
    old_vertices = {v for face in occupied for v in c.vertices(face)}
    completions = []
    for row in cert['terminal_targets']:
        provider, result = d.terminal(row, known, old_vertices,
                                     (m, r, f, h, c, g, excluded, tables, {}, []))
        need(provider not in known, 'duplicate terminal provider')
        known.append(provider)
        g.union(known)
        completions.append(result)
    need(len(completions) == 4 and set(known[len(fixed):]) == set(layers[3]), 'third subset differs from positive fixture')
    union = g.union(known)
    need(all(set(c.star(v)) <= union for v in old_vertices), 'forced third subset misses full old halo')
    return known, {'providers': len(providers), 'clauses': len(cert['clauses']),
                   'unit_steps': len(cert['steps']), 'true_units': yes.bit_count(), 'false_units': no.bit_count(),
                   'complete_covers': covers, 'clause_counts': counts, 'terminal_censuses': completions,
                   'forced_third_copies': len(forced) + len(completions), 'three_future_subset_verified': True}


def check(inputs=None, ctx_bundle=None):
    fixture, common, local = inputs if inputs is not None else [read(BASE / n) for n in ['witness.json', 'rigidity.json', 'local-pattern.json']]
    d, ctx, m, dependencies = ctx_bundle if ctx_bundle is not None else context()
    r, f, h, c, g, _, _, _ = ctx
    layers, positive_checks = positive(c, g, r, fixture)
    known, forcing_check = forcing(common, layers, d, ctx, m)
    scope(local, 'three_surround_obstruction', 3)
    local_check = m.check(local, ctx)
    motif = list(map(r.pose, local['poses']))
    keys = set(known)
    anchors = [q for q in known if all(c.compose(q, p) in keys for p in motif)]
    need(anchors, 'forced third subset misses the proved local obstruction')
    return {'agent': 'six-heesch-2', 'role': 'researcher', 'second_prefix_copies': 18,
            'positive_disc_coronas': positive_checks, 'prototype_automorphisms': d.automorphisms(c, g),
            'third_forcing': forcing_check, 'local_three_surround_obstruction': local_check,
            'local_obstruction_anchors': [list(q) for q in anchors],
            'dependencies_rechecked': dependencies, 'second_prefix_no_four_surrounds_verified': True,
            'scope': 'specified third18-copy second branch admits three disc coronas but no sixth corona under arbitrary real motions/topology; global height unchanged'}


def controls(inputs, bundle):
    d, ctx, m, _ = bundle
    r, _, _, c, g, _, _, _ = ctx
    for name in ['omitted_cover_provider', 'wrong_forcing_stage', 'wrong_local_stage',
                 'selected_only_terminal_point', 'shifted_terminal_provider', 'false_initial_rup',
                 'shifted_local_transport', 'deleted_fixed_premise']:
        bad = copy.deepcopy(inputs)
        if name == 'omitted_cover_provider':
            i = bad[1]['cover_targets'][0]['clause']
            bad[1]['clauses'][i].pop()
        elif name == 'wrong_forcing_stage':
            bad[1]['future_surrounds_required'] = 2
        elif name == 'wrong_local_stage':
            bad[2]['surrounds'] = 2
        elif name == 'selected_only_terminal_point':
            old = g.union(list(map(r.pose, bad[1]['fixed_poses'])))
            old_vertices = {v for face in old for v in c.vertices(face)}
            q = tuple(bad[1]['providers'][bad[1]['forced_provider_indices'][0] - 1])
            new_vertices = {c.point(q, v) for v in g.vs} - old_vertices
            need(new_vertices, 'control has no selected-only point')
            bad[1]['terminal_targets'][0]['vertex'] = list(min(new_vertices))
        elif name == 'shifted_terminal_provider':
            bad[1]['terminal_targets'][0]['provider'][4] += 3
        elif name == 'false_initial_rup':
            bad[2]['rup_lemmas'][0] = []
        elif name == 'shifted_local_transport':
            for row in bad[2]['poses']:
                row['translation'][0] += 300
        elif name == 'deleted_fixed_premise':
            bad[1]['fixed_poses'].pop()
        try:
            check(bad, bundle)
        except (ValueError, AssertionError):
            continue
        raise ValueError(('malformed control accepted', name))
    return ['omitted_cover_provider', 'wrong_forcing_stage', 'wrong_local_stage',
            'selected_only_terminal_point', 'shifted_terminal_provider', 'false_initial_rup',
            'shifted_local_transport', 'deleted_fixed_premise']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--controls', action='store_true')
    ap.add_argument('--expected', type=Path)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    start = time.monotonic()
    inputs = [read(BASE / n) for n in ['witness.json', 'rigidity.json', 'local-pattern.json']]
    bundle = context()
    report = check(inputs, bundle)
    if args.controls:
        report['rejected_controls'] = controls(inputs, bundle)
    if args.expected:
        need(report == read(args.expected), 'expected result differs')
    if args.output:
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, indent=2, sort_keys=True))
    print(json.dumps({'seconds': round(time.monotonic() - start, 3),
                      'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))


if __name__ == '__main__':
    main()
