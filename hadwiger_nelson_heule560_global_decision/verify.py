"""Definition-level witnesses and independent right-CNF reconstruction.

Imports only the earlier sparse-radical geometry checker, not this producer.
The exact left-selector equivalence is an explicitly imported theorem.
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

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO / 'hadwiger_nelson_heule632_pair_pilot'))
import independent as I


def need(ok, why):
    if not ok:
        raise ValueError(why)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def prepare():
    plan = json.loads((HERE / 'plan.json').read_text())
    for path, digest in plan['input_files'].items():
        need(sha((REPO / path).read_bytes()) == digest, ('input', path))
    points, host_edges, _ = I.geometry()
    boundary = json.loads((REPO / 'hadwiger_nelson_heule632_minimize/boundary.json').read_text())
    m, u = set(boundary['mandatory_vertices']), set(boundary['optional_vertices'])
    left = {v for v in m | u if all(all(rad % 5 for rad in axis) for axis in points[v])}
    small = (m | u) - left
    edges = [(a, b) for a, b in host_edges if a in m | u and b in m | u]
    cross = [(a, b) if a in left else (b, a) for a, b in edges if (a in left) != (b in left)]
    q = sorted({a for a, b in cross}); right = sorted(small | set(q))
    es = [(a, b) for a, b in edges if a in right and b in right]
    optional = sorted((small & u) | {310})
    p = json.loads((REPO / 'hadwiger_nelson_heule560_separator/certificate.json').read_text())
    need(q == p['separator'] and set(q) <= m, 'exact separator')
    need(sorted(left) == p['blocks']['full']['vertices'], 'exact field block')
    need(left & u == {310,510,512,513,520,521,523,524,535}, 'erased vertices')
    need(len(optional) == 60 and len(right) == 196 and len(es) == 806, 'block dimensions')
    states = [r['state'] for r in p['blocks']['mandatory']['states']]
    full = {r['state'] for r in p['blocks']['full']['states']}
    return {'m': m, 'u': u, 'left': left, 'right': right, 'q': q, 'es': es,
            'optional': optional, 'states': states, 'full': full, 'parent': p, 'edges': edges}


def selected(mask, optional):
    need(type(mask) is int and 0 <= mask < 2**len(optional), 'mask domain')
    return {v for i, v in enumerate(optional) if mask // 2**i % 2}


def direct_formula(g, negatives=()):
    right = g['right']; opt = g['optional']; q = g['q']
    position = {v: i for i, v in enumerate(right)}
    var = lambda v, c: 4 * position[v] + c + 1
    sel = {v: 4 * len(right) + i + 1 for i, v in enumerate(opt)}
    top0 = 4 * len(right) + len(opt)
    clauses = []
    for v in right:
        cs = [var(v, c) for c in range(4)]
        clauses.append(cs); clauses.extend([[-a, -b] for a, b in combinations(cs, 2)])
    for a, b in g['es']:
        for c in range(4):
            cl = []
            for v in (a, b):
                if v in sel:
                    cl.append(-sel[v])
            clauses.append(cl + [-var(a, c), -var(b, c)])
    clauses.append(list(range(top0 + 1, top0 + len(g['states']) + 1)))
    for i, state in enumerate(g['states']):
        gate = top0 + i + 1
        for j, v in enumerate(q):
            clauses.append([-gate, var(v, int(state[j]))])
        if state not in g['full']:
            clauses.append([-sel[310], -gate])
    top = top0 + len(g['states'])
    if negatives is not None:
        clauses.append(list(range(top + 1, top + len(negatives) + 1)))
        for i, row in enumerate(negatives):
            chosen = selected(row['mask'], opt)
            for v in opt:
                if v in chosen:
                    clauses.append([-(top + i + 1), sel[v]])
        top += len(negatives)
    raw = (f'p cnf {top} {len(clauses)}\n' + ''.join(' '.join(map(str, cl)) + ' 0\n' for cl in clauses)).encode('ascii')
    return raw, top, len(clauses)


def proper(row, g):
    chosen = selected(row['mask'], g['optional'])
    keep = (g['m'] | chosen) & set(g['right'])
    text = row['colouring']; state = row['state']
    need(type(text) is str and len(text) == len(g['right']) and set(text) <= set('0123.'), 'colour string')
    cs = {v: c for v, c in zip(g['right'], text) if c != '.'}
    need(set(cs) == keep, 'colour support')
    need(''.join(cs[v] for v in g['q']) == state, 'boundary word')
    need(state in (g['full'] if 310 in chosen else g['states']), 'allowed left relation')
    count = 0
    for a, b in g['es']:
        if a in keep and b in keep:
            need(cs[a] != cs[b], 'right edge'); count += 1
    # Paste the actual inherited left witness and check the whole selected graph.
    rows = g['parent']['blocks']['full' if 310 in chosen else 'mandatory']
    left_row = next(r for r in rows['states'] if r['state'] == state)
    lc = dict(zip(rows['vertices'], left_row['colouring']))
    support = g['m'] | chosen
    joined = {v: c for v, c in lc.items() if v in support}
    need(all(joined[v] == cs[v] for v in g['q']), 'gluing match')
    joined.update(cs)
    need(set(joined) == support, 'whole support')
    whole_count = 0
    for a, b in g['edges']:
        if a in support and b in support:
            need(joined[a] != joined[b], 'whole graph unit edge'); whole_count += 1
    return count, whole_count


def inspect(cert, g, manifest):
    need(cert['optional_order'] == g['optional'] and cert['right_vertices'] == g['right'] and cert['separator'] == g['q'], 'index orders')
    need(cert['record_improvement'] is False and cert['whole560_family_closed'] is False, 'scope')
    positives = cert['positive_covers']; negatives = cert['negative_cores']
    ps = [selected(r['mask'], g['optional']) for r in positives]
    ns = [selected(r['mask'], g['optional']) for r in negatives]
    need(len({r['mask'] for r in positives}) == len(positives), 'positive uniqueness')
    need(len({r['mask'] for r in negatives}) == len(negatives), 'negative uniqueness')
    for a, b in combinations(ps, 2):
        need(not (a <= b or b <= a), 'positive antichain')
    for a, b in combinations(ns, 2):
        need(not (a <= b or b <= a), 'negative antichain')
    need(not any(n <= p for n in ns for p in ps), 'disjoint positive and negative cones')
    right_checks = whole_checks = deletion_checks = minimality_cores = 0
    upper = json.loads((REPO / 'hadwiger_nelson_heule632_minimize/certificate.json').read_text())['five_colouring']
    need(len(upper) == 632 and set(upper) <= set('01234.'), 'inherited five-colouring')
    upper_checks = 0
    for row in positives:
        a, b = proper(row, g); right_checks += a; whole_checks += b
    for row, support in zip(negatives, ns):
        vertex_set = g['m'] | support
        need(all(upper[v] in '01234' for v in vertex_set), 'five-colour support')
        for a, b in g['edges']:
            if a in vertex_set and b in vertex_set:
                need(upper[a] != upper[b], 'five-colour edge'); upper_checks += 1
        if 'deletion_witnesses' not in row:
            continue
        minimality_cores += 1
        ds = row['deletion_witnesses']
        need([r['removed'] for r in ds] == sorted(support), 'complete single deletions')
        for d in ds:
            need(selected(d['mask'], g['optional']) == support - {d['removed']}, 'deletion mask')
            a, b = proper(d, g); right_checks += a; whole_checks += b; deletion_checks += 1
    raw, top, clauses = direct_formula(g, negatives)
    if manifest is not None:
        need(sha(raw) == manifest['cnf_sha256'] and len(raw) == manifest['cnf_bytes'], 'negative CNF identity')
        need(top == manifest['variables'] and clauses == manifest['clauses'] and len(ns) == manifest['cases'], 'negative CNF dimensions')
    oracle, ov, oc = direct_formula(g, None)
    forced = sorted(set().union(*(set(g['optional']) - p for p in ps if len(p) == 59)))
    if 'minimality_evidence_core_index' in cert:
        at = cert['minimality_evidence_core_index']
        need(type(at) is int and 0 <= at < len(ns), 'minimality index')
        need('deletion_witnesses' in negatives[at] and len(ns[at]) == min(map(len, ns)), 'smallest core minimality')
        need(minimality_cores == 1, 'compact evidence scope')
    return {'positive_covers': len(ps), 'negative_cores': len(ns), 'deletion_witnesses': deletion_checks,
            'minimality_cores_checked': minimality_cores,
            'positive_cover_sizes': dict(sorted(Counter(map(len, ps)).items())),
            'negative_core_sizes': dict(sorted(Counter(map(len, ns)).items())),
            'right_edge_checks': right_checks, 'whole_graph_edge_checks': whole_checks,
            'five_colouring_edge_checks': upper_checks,
            'new_forced_vertices_from_singleton_complements': forced,
            'whole_310_absent_case_closed_by_positive_witness': 310 in forced,
            'smallest_negative_support_vertices': 492 + min(map(len, ns)),
            'oracle_sha256': sha(oracle), 'oracle_variables': ov, 'oracle_clauses': oc,
            'negative_cnf_sha256': sha(raw), 'negative_cnf_variables': top, 'negative_cnf_clauses': clauses,
            'host_pairs_checked': 199396, 'whole560_family_closed': False, 'record_improvement': False}, raw


def limits():
    resource.setrlimit(resource.RLIMIT_AS, (4 * 1024**3, 4 * 1024**3))
    resource.setrlimit(resource.RLIMIT_FSIZE, (512 * 1024**2, 512 * 1024**2))


def controls(cert, g, manifest):
    mutations = []
    x = copy.deepcopy(cert); x['optional_order'].reverse(); mutations.append(x)
    x = copy.deepcopy(cert); x['positive_covers'][0]['colouring'] = '0' * len(g['right']); mutations.append(x)
    x = copy.deepcopy(cert); x['positive_covers'][0]['mask'] ^= 1; mutations.append(x)
    at = next(i for i, r in enumerate(cert['negative_cores']) if 'deletion_witnesses' in r)
    x = copy.deepcopy(cert); x['negative_cores'][at]['deletion_witnesses'].pop(); mutations.append(x)
    x = copy.deepcopy(cert); x['negative_cores'][0]['mask'] = 0; mutations.append(x)
    x = copy.deepcopy(cert); x['negative_cores'].pop(); mutations.append(x)
    x = copy.deepcopy(cert); x['record_improvement'] = True; mutations.append(x)
    for x in mutations:
        try:
            inspect(x, g, manifest)
        except ValueError:
            continue
        raise ValueError('corrupted certificate accepted')
    return len(mutations)


def residual_audit(residual, cert, g):
    path = REPO / residual['old_cover_file']
    need(sha(path.read_bytes()) == residual['old_cover_sha256'], 'old cover identity')
    old = json.loads(path.read_text())['maximal_extending_cover_colourings']
    f = residual['required_vertices']
    need(f == sorted(set(f)) and set(f) <= set(g['optional']), 'residual required set')
    need(residual['target_size'] == 16 and len(f) <= 16, 'residual cardinality')
    need(residual['cylinder_count'] == comb(60 - len(f), 16 - len(f)), 'residual binomial count')
    ps = [selected(r['mask'], g['optional']) for r in cert['positive_covers']]
    need(not any(set(f) <= p for p in ps), 'residual avoids every new cover')
    old_checks = 0; subsumed = 0
    for row in old:
        keep = g['m'] | (g['u'] - set(row['omitted_optional']))
        text = row['colouring']
        need(len(text) == 632 and set(text) <= set('0123.'), 'old colour string')
        cs = {v: text[v] for v in g['m'] | g['u'] if text[v] != '.'}
        need(set(cs) == keep, 'old colour support')
        for a, b in g['edges']:
            if a in keep and b in keep:
                need(cs[a] != cs[b], 'old cover edge'); old_checks += 1
        p = set(g['optional']) - set(row['omitted_optional'])
        need(not set(f) <= p, 'residual avoids old cover')
        subsumed += any(p <= new for new in ps)
    need(all(r['mask'].bit_count() > 16 for r in cert['negative_cores']), 'residual avoids negative cones by size')
    return {'residual_required_vertices': f, 'certified_unclassified_exact508_support_lower_bound': residual['cylinder_count'],
            'old_kempe_covers_checked': len(old), 'old_kempe_edge_checks': old_checks,
            'old_kempe_covers_subsumed_by_new_covers': subsumed}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    ap.add_argument('--manifest', type=Path, default=HERE / 'proof_manifest.json')
    modes = ap.add_mutually_exclusive_group(required=True)
    modes.add_argument('--archive', type=Path)
    modes.add_argument('--prove', action='store_true')
    modes.add_argument('--structure-only', action='store_true')
    ap.add_argument('--kissat', default='/scratch/researcher3-kissat/build/kissat')
    ap.add_argument('--drat-trim', default='/scratch/drat-trim-package/usr/bin/drat-trim')
    args = ap.parse_args(); args.out.mkdir(parents=True, exist_ok=False)
    g = prepare(); cert = json.loads(args.certificate.read_text()); manifest = json.loads(args.manifest.read_text())
    report, raw = inspect(cert, g, manifest)
    report['mutations_rejected'] = controls(cert, g, manifest)
    residual = json.loads((HERE / 'residual.json').read_text())
    report.update(residual_audit(residual, cert, g))
    bad = copy.deepcopy(residual); bad['cylinder_count'] += 1
    try:
        residual_audit(bad, cert, g)
    except ValueError:
        report['mutations_rejected'] += 1
    else:
        raise ValueError('bad residual count accepted')
    cnf = args.out / 'negative.cnf'; cnf.write_bytes(raw)
    report['negative_proof_verified'] = False
    if not args.structure_only:
        if args.prove:
            proof = args.out / 'negative.drat'
            with (args.out / 'kissat.log').open('wb') as log:
                result = subprocess.run([args.kissat, '--seed=0', '--conflicts=4000000', '--time=180', str(cnf), str(proof)], stdout=log, stderr=subprocess.STDOUT, timeout=200, preexec_fn=limits)
            need(result.returncode == 20, 'fresh negative proof')
        else:
            proof = args.archive / 'negative.drat'
            need(sha(proof.read_bytes()) == manifest['proof_sha256'], 'archived proof identity')
        with (args.out / 'drat.log').open('wb') as log:
            result = subprocess.run([args.drat_trim, str(cnf), str(proof)], stdout=log, stderr=subprocess.STDOUT, timeout=200, preexec_fn=limits)
        need(result.returncode == 0 and b's VERIFIED' in (args.out / 'drat.log').read_bytes().splitlines(), 'independent DRAT')
        report['negative_proof_verified'] = True
        report['proof_sha256'] = sha(proof.read_bytes())
        report['proof_bytes'] = proof.stat().st_size
    (args.out / 'result.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    main()
