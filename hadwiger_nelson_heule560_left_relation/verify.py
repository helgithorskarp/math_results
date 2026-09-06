"""Definition-level audit of all 72 x 512 cases and the combined DRAT proof.

Does not import this contribution's producer. Parent completeness of the
72-state interface is an explicit imported theorem, not silently rerun here.
"""
import argparse
from collections import Counter
import copy
import hashlib
from itertools import combinations
import json
from math import comb
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO / 'hadwiger_nelson_heule632_pair_pilot'))
import independent as I


def need(ok, why):
    if not ok:
        raise ValueError(why)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def prepare():
    plan = json.loads((HERE / 'plan.json').read_text())
    for path, sha in plan['input_files'].items():
        need(digest((REPO / path).read_bytes()) == sha, ('input identity', path))
    points, host_edges, _ = I.geometry()
    boundary = json.loads((REPO / 'hadwiger_nelson_heule632_minimize/boundary.json').read_text())
    mandatory, optional = set(boundary['mandatory_vertices']), set(boundary['optional_vertices'])
    vertices = mandatory | optional
    large = {v for v in vertices if all(all(rad % 5 for rad in axis) for axis in points[v])}
    small = vertices - large
    edges = [(a, b) for a, b in host_edges if a in vertices and b in vertices]
    cross = [(a, b) if a in large else (b, a) for a, b in edges if (a in large) != (b in large)]
    q = sorted({a for a, b in cross})
    need(set(q) <= mandatory and len(q) == 19 and len(cross) == 33, 'separator')
    parent = json.loads((REPO / 'hadwiger_nelson_heule560_separator/certificate.json').read_text())
    need(parent['separator'] == q and parent['blocks']['full']['vertices'] == sorted(large), 'parent field block')
    need(parent['blocks']['mandatory']['vertices'] == sorted(large & mandatory), 'parent mandatory block')
    w = sorted(large & optional)
    need(w == plan['optional_order'] and len(w) == 9, 'nine selectors')
    return {'host_edges': host_edges, 'edges': edges, 'mandatory': mandatory, 'optional': optional,
            'large': large, 'small': small, 'q': q, 'w': w, 'parent': parent}


def mask_set(mask, optional):
    need(type(mask) is int and 0 <= mask < (1 << len(optional)), 'mask domain')
    return {v for i, v in enumerate(optional) if (mask // (2**i)) % 2}


def proper(text, vs, support, edges, q, state):
    need(len(text) == len(vs) and set(text) <= set('0123.'), 'colour string')
    colour = {v: c for v, c in zip(vs, text) if c != '.'}
    need(set(colour) == support, 'colour support')
    need(''.join(colour[v] for v in q) == state, 'boundary word')
    count = 0
    for u, v in edges:
        if u in support and v in support:
            need(colour[u] != colour[v], 'unit edge inequality'); count += 1
    return count


def direct_cnf(geo, cases):
    vs = sorted(geo['large']); w = geo['w']; q = geo['q']
    index = {v: i for i, v in enumerate(vs)}
    selector = {v: 4 * len(vs) + i + 1 for i, v in enumerate(w)}
    x = lambda v, c: 4 * index[v] + c + 1
    clauses = []
    for v in vs:
        colours = [x(v, c) for c in range(4)]
        clauses.append(colours)
        clauses.extend([[-a, -b] for a, b in combinations(colours, 2)])
    for u, v in geo['edges']:
        if u not in index or v not in index:
            continue
        for c in range(4):
            clause = []
            if u in selector:
                clause.append(-selector[u])
            if v in selector:
                clause.append(-selector[v])
            clauses.append(clause + [-x(u, c), -x(v, c)])
    top = 4 * len(vs) + len(w)
    clauses.append([top + i + 1 for i in range(len(cases))])
    for i, (state, mask) in enumerate(cases):
        gate = top + i + 1
        for j, v in enumerate(q):
            clauses.append([-gate, x(v, int(state[j]))])
        chosen = mask_set(mask, w)
        for v in w:
            if v in chosen:
                clauses.append([-gate, selector[v]])
    raw = (f'p cnf {top + len(cases)} {len(clauses)}\n' + ''.join(' '.join(map(str, c)) + ' 0\n' for c in clauses)).encode('ascii')
    return raw, top + len(cases), len(clauses)


def inspect(cert, geo, manifest):
    parent = geo['parent']; vs = sorted(geo['large']); w = geo['w']; q = geo['q']
    need(cert['optional_order'] == w and cert['separator'] == q, 'certificate coordinates')
    need(cert['record_improvement'] is False and cert['whole560_family_closed'] is False, 'scope flags')
    original = [r['state'] for r in parent['blocks']['mandatory']['states']]
    full = {r['state']: r for r in parent['blocks']['full']['states']}
    need(original == sorted(set(original)) and len(original) == 72 and len(full) == 20, 'parent state domain')
    need([r['state'] for r in cert['rows']] == original, 'complete state rows')
    subsets = [mask_set(mask, w) for mask in range(512)]
    mandatory = geo['large'] & geo['mandatory']
    table = []; cases = []; cover_counts = []; positive_checks = 0
    witnesses = []; minimal_checks = maximal_checks = 0
    for row in cert['rows']:
        state = row['state']
        need(row['inherited_full'] is (state in full), 'inherited state identity')
        if row['inherited_full']:
            positive_checks += proper(full[state]['colouring'], vs, set(vs), geo['edges'], q, state)
            need('negative_masks' not in row and 'positive_covers' not in row, 'inherited schema')
            table.append([True] * 512); cover_counts.append(1); continue
        covers = row['positive_covers']; negatives = row['negative_masks']
        positive_masks = [r['mask'] for r in covers]
        need(positive_masks == sorted(set(positive_masks)) and negatives == sorted(set(negatives)), 'canonical antichains')
        good_sets = [mask_set(x, w) for x in positive_masks]
        bad_sets = [mask_set(x, w) for x in negatives]
        for a, b in combinations(good_sets, 2):
            need(not (a <= b or b <= a), 'positive antichain')
        for a, b in combinations(bad_sets, 2):
            need(not (a <= b or b <= a), 'negative antichain')
        for cover, subset in zip(covers, good_sets):
            count = proper(cover['colouring'], vs, mandatory | subset, geo['edges'], q, state)
            positive_checks += count; witnesses.append({'mask': cover['mask'], 'vertices': len(mandatory | subset), 'edges': count})
        truth = []
        for subset in subsets:
            good = any(subset <= cover for cover in good_sets)
            bad = any(forbidden <= subset for forbidden in bad_sets)
            need(good != bad, 'complete disjoint lattice partition')
            truth.append(good)
        for forbidden in bad_sets:
            for v in forbidden:
                need(any(forbidden - {v} <= cover for cover in good_sets), 'minimal forbidden set'); minimal_checks += 1
        for cover in good_sets:
            for v in set(w) - cover:
                need(any(forbidden <= cover | {v} for forbidden in bad_sets), 'maximal good set'); maximal_checks += 1
        cases.extend((state, mask) for mask in negatives)
        table.append(truth); cover_counts.append(len(covers))
    raw, nvars, nclauses = direct_cnf(geo, cases)
    need(digest(raw) == manifest['cnf_sha256'] and len(raw) == manifest['cnf_bytes'], 'combined formula identity')
    need(len(cases) == manifest['cases'] and nvars == manifest['variables'] and nclauses == manifest['clauses'], 'proof formula dimensions')
    # Determine selector dependence by complete truth-table comparison.
    relevant = []
    for bit, vertex in enumerate(w):
        if any(values[mask] != values[mask ^ (1 << bit)] for values in table for mask in range(512)):
            relevant.append(vertex)
    equivalent = {}
    for mask in range(512):
        state_word = ''.join('1' if values[mask] else '0' for values in table)
        equivalent.setdefault(state_word, []).append(mask)
    census = Counter(sum(values[mask] for values in table) for mask in range(512))
    need(relevant == [310], 'one-switch conclusion')
    for state, values in zip(original, table):
        need(all(values[mask] == (state in full or 310 not in subsets[mask]) for mask in range(512)), 'exact one-switch relation')
    erased = set(w) - set(relevant)
    retained = (geo['mandatory'] | geo['optional']) - erased
    seed_edges = [(a, b) for a, b in geo['edges'] if a in retained and b in retained]
    old = json.loads((REPO / 'hadwiger_nelson_heule632_minimize/certificate.json').read_text())
    upper = old['five_colouring']
    need(len(upper) == 632 and all(upper[v] in '01234' for v in retained), 'inherited five-colouring support')
    need(all(upper[a] != upper[b] for a, b in seed_edges), 'inherited five-colouring edges')
    canonical_stream = ''.join(''.join('1' if x else '0' for x in row) + '\n' for row in table).encode('ascii')
    report = {'states': 72, 'masks': 512, 'state_mask_pairs': 72 * 512,
              'true_pairs': sum(map(sum, table)), 'false_pairs': 72 * 512 - sum(map(sum, table)),
              'inherited_full_states': len(full), 'new_positive_covers': len(witnesses),
              'negative_cases': len(cases), 'positive_unit_edge_checks': positive_checks,
              'new_positive_supports': sorted({(r['vertices'], r['edges']) for r in witnesses}),
              'minimality_checks': minimal_checks, 'maximality_checks': maximal_checks,
              'table_sha256': digest(canonical_stream), 'relevant_optional_vertices': relevant,
              'irrelevant_optional_vertices': sorted(erased), 'distinct_boundary_relations': len(equivalent),
              'state_count_census': {str(k): v for k, v in sorted(census.items())},
              'equivalence_class_sizes': sorted(map(len, equivalent.values())),
              'negative_cnf_sha256': digest(raw), 'negative_cnf_variables': nvars, 'negative_cnf_clauses': nclauses,
              'reduced_support_vertices': len(retained), 'reduced_support_edges': len(seed_edges),
              'reduced_support_five_colour_edge_checks': len(seed_edges),
              'reduced_support_chromatic_number_from_inherited_theorem': 5,
              'mandatory_vertices': len(geo['mandatory']), 'remaining_optional_vertices': len(geo['optional'] - erased),
              'original_exact508_support_count': comb(68, 16), 'canonical_exact508_support_count': comb(60, 16),
              'without_310_exact508_support_count': comb(59, 16), 'with_310_exact508_support_count': comb(59, 15),
              'host_pairs_checked': 199396, 'whole560_family_closed': False, 'record_improvement': False}
    return report, raw


def controls(cert, geo, manifest):
    mutations = []
    x = copy.deepcopy(cert); x['rows'].pop(); mutations.append(x)
    at = next(i for i, r in enumerate(cert['rows']) if not r['inherited_full'])
    x = copy.deepcopy(cert); x['rows'][at]['negative_masks'] = [2]; mutations.append(x)
    x = copy.deepcopy(cert); x['rows'][at]['positive_covers'][0]['mask'] = 511; mutations.append(x)
    x = copy.deepcopy(cert); x['rows'][at]['positive_covers'][0]['colouring'] = '0' * 383; mutations.append(x)
    x = copy.deepcopy(cert); x['rows'][at]['inherited_full'] = True; mutations.append(x)
    x = copy.deepcopy(cert); x['optional_order'][0], x['optional_order'][1] = x['optional_order'][1], x['optional_order'][0]; mutations.append(x)
    x = copy.deepcopy(cert); x['record_improvement'] = True; mutations.append(x)
    for x in mutations:
        try:
            inspect(x, geo, manifest)
        except ValueError:
            continue
        raise ValueError('corruption accepted')
    return len(mutations)


def limits():
    resource.setrlimit(resource.RLIMIT_AS, (4 * 1024**3, 4 * 1024**3))
    resource.setrlimit(resource.RLIMIT_FSIZE, (512 * 1024**2, 512 * 1024**2))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', type=Path, required=True)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument('--archive', type=Path); mode.add_argument('--prove', action='store_true')
    mode.add_argument('--positives-only', action='store_true')
    ap.add_argument('--kissat', default='/scratch/researcher3-kissat/build/kissat')
    ap.add_argument('--drat-trim', default='/scratch/drat-trim-package/usr/bin/drat-trim')
    args = ap.parse_args(); args.out.mkdir(parents=True, exist_ok=False)
    t = time.monotonic(); geo = prepare()
    cert = json.loads((HERE / 'certificate.json').read_text())
    manifest = json.loads((HERE / 'proof_manifest.json').read_text())
    report, raw = inspect(cert, geo, manifest)
    report['mutations_rejected'] = controls(cert, geo, manifest)
    report['new_negative_proof_verified'] = False
    if not args.positives_only:
        cnf = args.out / 'negative.cnf'; cnf.write_bytes(raw)
        if args.archive:
            need(raw == (args.archive / 'negative.cnf').read_bytes(), 'archived CNF bytes')
            proof = args.archive / 'negative.drat'
            need(digest(proof.read_bytes()) == manifest['proof_sha256'], 'proof identity')
        else:
            proof = args.out / 'negative.drat'
            with (args.out / 'kissat.log').open('wb') as log:
                result = subprocess.run([args.kissat, '--seed=0', '--conflicts=2000000', '--time=120', str(cnf), str(proof)], stdout=log, stderr=subprocess.STDOUT, timeout=135, preexec_fn=limits)
            need(result.returncode == 20, 'fresh negative UNSAT')
        logpath = args.out / 'drat.log'
        with logpath.open('wb') as log:
            result = subprocess.run([args.drat_trim, str(cnf), str(proof)], stdout=log, stderr=subprocess.STDOUT, timeout=135, preexec_fn=limits)
        need(result.returncode == 0 and b's VERIFIED' in logpath.read_bytes().splitlines(), 'DRAT check')
        report.update({'new_negative_proof_verified': True, 'proof_sha256': digest(proof.read_bytes()), 'proof_bytes': proof.stat().st_size})
    report['seconds'] = time.monotonic() - t
    (args.out / 'result.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    main()
