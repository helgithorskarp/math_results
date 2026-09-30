"""Exact sparse replay of the original T214 second-prefix closure.

six-heesch-2, researcher. Centroid joins regenerate complete local covers;
bit-mask logic checks the forward and RUP certificates. No discovery pool,
native solver, dense CNF, DRAT or extractor is an input. The written locking
bridge and byte-pinned prior geometry/interior-pair results remain explicit
dependencies. The original17-copy second-prefix rigidity is an imported lemma.
"""
import argparse
from collections import Counter
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
    pins = read(BASE / 'dependency-pins.json')
    for relative, digest in pins.items():
        need(hashlib.sha256((PUB / relative).read_bytes()).hexdigest() == digest, ('dependency bytes', relative))
    path = PUB / 'heesch_polyiamond_second_prefix_closure/check.py'
    spec = importlib.util.spec_from_file_location('pinned_sparse_geometry', path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    r, f, h, c, g, excluded, tables, dependencies = m.context()
    single = dict(tables)['single_surround_pattern'] + read(BASE / 'single-patterns.json')
    checks = r.verify_patterns(f, h, c, g, single)
    tables = [('single_surround_pattern', single)] + tables[1:]
    return m, r, f, h, c, g, excluded, tables, dependencies, checks


def automorphisms(c, g):
    target = min(g.fs)
    joined = set()
    for matrix in g.ms:
        for face in g.fs:
            x, y = c.face(matrix + (0, 0), face)
            if (target[0] - x) % 3 == (target[1] - y) % 3 == 0:
                joined.add(matrix + ((target[0] - x) // 3, (target[1] - y) // 3))
    found = sorted(q for q in joined if g.footprint(q) == g.fs)
    need(found == [c.IDENTITY], 'prototype has an unhandled automorphism')
    return [list(q) for q in found]


def scope(cert, kind, surrounds):
    need(cert['kind'] == kind and cert['tile'] == 'T214' and
         type(cert.get('future_surrounds_required', cert.get('surrounds'))) is int and
         cert.get('future_surrounds_required', cert.get('surrounds')) == surrounds,
         'wrong future-surround license')


def cover_encoding(cert):
    for row in cert['cover_targets']:
        need(len(row['vertex']) == len(row['required_centroid']) == 2 and
             all(type(v) is int for v in row['vertex'] + row['required_centroid']), 'integral cover coordinates')


def forward(m, cert):
    # The bit-mask implementation differs from discovery's dictionary trace.
    data = dict(cert, forced_provider_indices=cert.get('forced_provider_indices', []))
    yes, no = m.forward(data)
    if 'conflict_clause' in cert:
        index = cert['conflict_clause']
        need(type(index) is int and 0 <= index < len(cert['clauses']), 'conflict index')
        positive, negative = m.encode(cert['clauses'][index], len(cert['providers']))
        need(positive & no == positive and negative & yes == negative, 'no forward contradiction')
    return yes, no


def local(cert, ctx):
    scope(cert, 'two_surround_obstruction', 2)
    cover_encoding(cert)
    m, r, f, h, c, g, excluded, tables, _, _ = ctx
    fixed = list(map(r.pose, cert['poses']))
    providers = list(map(tuple, cert['providers']))
    r.valid_poses(g, fixed)
    r.valid_poses(g, providers)
    need(fixed and fixed[0] == c.IDENTITY, 'local normalization')
    occupied = g.union(fixed)
    need(all(not g.footprint(q) & occupied for q in providers), 'local provider overlaps fixed copy')
    cover_ids, census = r.covers(f, c, g, fixed, providers, cert)
    counts = r.negative_clauses(h, c, g, fixed, providers, cert, cover_ids, excluded, tables[:1])
    yes, no = forward(m, cert)
    return {'fixed_copies': len(fixed), 'providers': len(providers), 'clauses': len(cert['clauses']),
            'unit_steps': len(cert['steps']), 'true_units': yes.bit_count(), 'false_units': no.bit_count(),
            'complete_covers': census, 'clause_counts': counts, 'two_surround_contradiction_verified': True}


def terminal(row, known, old_vertices, ctx):
    _, r, f, _, c, g, _, _, _, _ = ctx
    vertex, required = tuple(row['vertex']), tuple(row['required_centroid'])
    need(len(vertex) == len(required) == 2 and all(type(v) is int for v in vertex + required), 'terminal coordinates')
    need(vertex in old_vertices, 'terminal point is not in the OLD third prefix')
    occupied = g.union(known)
    raw, allowed, joins, sectors = f.cover(c, g, occupied, vertex, required)
    provider = tuple(row['provider'])
    r.valid_poses(g, [provider])
    need(sectors == 5 and len(raw) == row['raw_providers'] == 22 and allowed == [provider], 'terminal is not complete and unique')
    return provider, {'vertex': list(vertex), 'required_centroid': list(required),
                      'centroid_joins': joins, 'raw_providers': len(raw), 'provider': list(provider)}


def common(cert, ctx):
    scope(cert, 'conditional_fourth_common_subset', 2)
    cover_encoding(cert)
    m, r, f, h, c, g, excluded, tables, _, _ = ctx
    data = read(PUB / 'heesch_polyiamond_deficit_review1/input.json')
    fixed = list(map(r.pose, cert['fixed_poses']))
    providers = list(map(tuple, cert['providers']))
    named = [r.pose(row) for row in data['placements'] if row['level'] <= 3]
    need(fixed == named and len(fixed) == 40, 'different third prefix')
    r.valid_poses(g, fixed)
    r.valid_poses(g, providers)
    occupied = g.union(fixed)
    need(all(not g.footprint(q) & occupied for q in providers), 'common provider overlaps OLD prefix')
    cover_ids, census = r.covers(f, c, g, fixed, providers, cert)
    counts = r.negative_clauses(h, c, g, fixed, providers, cert, cover_ids, excluded, tables[:1])
    yes, no = forward(m, cert)
    forced = [providers[i - 1] for i in cert['forced_provider_indices']]
    need(len(forced) == 32, 'different initial common subset')
    known = fixed + forced
    g.union(known)
    old_vertices = {v for face in occupied for v in c.vertices(face)}
    terminals, added = [], []
    for row in cert['terminal_targets']:
        provider, result = terminal(row, known, old_vertices, ctx)
        need(provider not in known, 'terminal copy already known')
        known.append(provider)
        g.union(known)
        added.append(provider)
        terminals.append(result)
    need(len(added) == 5, 'different terminal count')
    return fixed, forced, added, {'providers': len(providers), 'clauses': len(cert['clauses']),
        'unit_steps': len(cert['steps']), 'true_units': yes.bit_count(), 'false_units': no.bit_count(),
        'initial_forced': len(forced), 'terminal_forced': len(added), 'complete_covers': census,
        'clause_counts': counts, 'terminal_censuses': terminals, 'common_fourth_subset_verified': True}


def closure(cert, old, forced, added, patterns, ctx):
    scope(cert, 'conditional_fourth_subset_atlas', 3)
    cover_encoding(cert)
    m, r, f, h, c, g, excluded, tables, _, _ = ctx
    providers = list(map(tuple, cert['providers']))
    r.valid_poses(g, providers)
    need(list(map(tuple, cert['derived_fixed'])) == added, 'unproved derived constants')
    occupied = g.union(old)
    need(all(not g.footprint(q) & occupied for q in providers), 'closure provider overlaps OLD prefix')
    cover_ids, census = r.covers(f, c, g, old, providers, cert)
    selectors, selector_rows = set(), []
    for row in cert['selector_exclusions']:
        index, ids, name = row['clause'], row['provider_indices'], row['name']
        need(type(index) is int and 0 <= index < len(cert['clauses']) and index not in selectors, 'selector index')
        need(len(ids) == 2 and len(set(ids)) == 2 and all(type(i) is int and 1 <= i <= len(providers) for i in ids), 'selector provider indices')
        need(set(cert['clauses'][index]) == {-i for i in ids} and name in patterns, 'selector clause or proof missing')
        tails = [providers[i - 1] for i in ids]
        need(list(map(tuple, row['tail_poses'])) == tails, 'selector poses differ')
        whole = old + forced + added + tails
        union = g.union(whole)
        motif = list(map(r.pose, patterns[name]['poses']))
        keys = set(whole)
        anchors = [anchor for anchor in whole if all(c.compose(anchor, q) in keys for q in motif)]
        need(anchors, 'selector misses its proved two-surround obstruction')
        # This finite halo check identifies the old four grid cases; the
        # exclusion itself uses only motif containment and the known subset.
        old_vertices = {v for face in occupied for v in c.vertices(face)}
        need(all(set(c.star(v)) <= union for v in old_vertices), 'selector is not a complete fourth surround')
        mesh, _ = c.mesh(union)
        selector_rows.append({'name': name, 'tail_poses': [list(q) for q in tails],
                              'local_obstruction_anchors': [list(q) for q in anchors], 'mesh': mesh})
        selectors.add(index)
    need(len(selectors) == 4 and {row['name'] for row in selector_rows} == {'A', 'original', 'B', 'C'}, 'four selector proofs required')
    # Covers are protected only at OLD points. Derived constants are known
    # C4 copies, and may be used as blockers without assuming them interior C4.
    extra = g.union(added)
    overlap_units = {i for i, row in enumerate(cert['clauses']) if len(row) == 1 and row[0] < 0 and
                     g.footprint(providers[-row[0] - 1]) & extra}
    ordinary = [i for i in range(len(cert['clauses'])) if i not in selectors | overlap_units]
    remap = {old_index: i for i, old_index in enumerate(ordinary)}
    reduced = dict(cert, clauses=[cert['clauses'][i] for i in ordinary])
    reduced_covers = {remap[i] for i in cover_ids}
    counts = Counter(r.negative_clauses(h, c, g, old + added, providers, reduced,
                                       reduced_covers, excluded, tables[:1]))
    counts['derived_whole_overlap_unit'] = len(overlap_units)
    counts['proved_two_surround_selector'] = len(selectors)
    proof = m.rup(cert)
    return {'providers': len(providers), 'clauses': len(cert['clauses']), 'complete_covers': census,
            'clause_counts': dict(sorted(counts.items())), 'rup_lemmas': proof,
            'fourth_selectors': selector_rows, 'four_case_subset_reduction_future_surrounds': 2,
            'four_case_subset_reduction_verified': True,
            'all_three_surrounds_of_original_third_excluded': True}


def controls(common_cert, cert, patterns, old, forced, added, ctx):
    m, r, _, _, c, g, _, _, _, _ = ctx
    rejected = []

    def reject(name, call):
        try:
            call()
        except ValueError:
            rejected.append(name)
            return
        raise ValueError(('malformed control accepted', name))

    bad = copy.deepcopy(common_cert)
    bad['steps'][0]['literal'] *= -1
    reject('flipped_common_unit', lambda: forward(m, bad))
    old_vertices = {v for face in g.union(old) for v in c.vertices(face)}
    known = old + forced
    selected_vertex = next(v for face in g.union(forced) for v in c.vertices(face) if v not in old_vertices)
    bad_row = copy.deepcopy(common_cert['terminal_targets'][0])
    bad_row['vertex'] = list(selected_vertex)
    reject('selected_only_terminal_point', lambda: terminal(bad_row, known, old_vertices, ctx))
    bad = copy.deepcopy(common_cert['terminal_targets'][0])
    bad['provider'][4] += 60
    reject('false_terminal_provider', lambda: terminal(bad, known, old_vertices, ctx))
    small = patterns['A']
    bad = copy.deepcopy(small)
    bad['providers'].pop()
    reject('omitted_local_provider', lambda: local(bad, ctx))
    bad = copy.deepcopy(small)
    bad['clauses'][bad['cover_targets'][0]['clause']].pop()
    reject('truncated_local_cover', lambda: local(bad, ctx))
    bad = copy.deepcopy(small)
    bad['surrounds'] = 1
    reject('wrong_local_future_stage', lambda: local(bad, ctx))
    bad = copy.deepcopy(read(BASE / 'single-patterns.json'))
    bad[0]['poses'][0]['translation'][0] += 60
    reject('shifted_single_gap_blocker', lambda: r.verify_patterns(ctx[2], ctx[3], c, g, bad))
    bad = copy.deepcopy(cert)
    bad['selector_exclusions'][0]['name'] = 'original'
    reject('false_selector_transport', lambda: closure(bad, old, forced, added, patterns, ctx))
    bad = copy.deepcopy(cert)
    bad['rup_lemmas'][0] = [1]
    reject('false_rup_addition', lambda: m.rup(bad))
    bad = copy.deepcopy(cert)
    bad['future_surrounds_required'] = 2
    reject('wrong_closure_future_stage', lambda: scope(bad, 'conditional_fourth_subset_atlas', 3))
    return rejected


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--expected', type=Path)
    ap.add_argument('--output', type=Path)
    ap.add_argument('--controls', action='store_true')
    args = ap.parse_args()
    start = time.monotonic()
    ctx = context()
    _, r, _, _, c, g, _, _, dependencies, single_checks = ctx
    symmetry_check = automorphisms(c, g)
    patterns = read(BASE / 'two-patterns.json')
    need(set(patterns) == {'A', 'original', 'B', 'C'}, 'local pattern names')
    two_checks = {name: local(row, ctx) for name, row in patterns.items()}
    common_cert, cert = read(BASE / 'common.json'), read(BASE / 'closure.json')
    old, forced, added, common_report = common(common_cert, ctx)
    out = {'agent': 'six-heesch-2', 'role': 'researcher', 'tile': 'T214',
           'scope': 'original40-copy third prefix has no three strict real surrounds; original17-copy second-prefix consequence imports the earlier rigidity lemma',
           'dependencies_rechecked': dependencies, 'single_patterns_checked': single_checks,
           'prototype_automorphisms': symmetry_check,
           'two_surround_patterns': two_checks, 'common_fourth_subset': common_report,
           'original_third_closure': closure(cert, old, forced, added, patterns, ctx)}
    data = read(PUB / 'heesch_polyiamond_deficit_review1/input.json')
    out['known_five_disc_coronas'] = c.lower(g.fs, data['placements'])
    out['named_prefix_counts'] = [1, 5, 11, 23, 39, 52]
    out['original_second_subset_rigidity_is_imported'] = True
    out['unchanged_global_interval'] = [5, 385]
    if args.controls:
        out['rejected_controls'] = controls(common_cert, cert, patterns, old, forced, added, ctx)
    if args.expected:
        need(out == read(args.expected), 'expected report mismatch')
    text = json.dumps(out, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text)
    print(json.dumps({'seconds': round(time.monotonic() - start, 3),
                      'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))


if __name__ == '__main__':
    main()
