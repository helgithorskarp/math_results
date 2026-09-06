"""Independent certificate audit: sparse-radical geometry, direct CNF, DRAT.

Imports no executable from this contribution's producer. Native solvers are
untrusted until their witnesses or proof traces have been checked.
"""
import argparse
import copy
import hashlib
import itertools
import json
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


def canonical(word):
    rename = {}
    return ''.join(str(rename.setdefault(c, len(rename))) for c in word)


def geometry():
    plan = json.loads((HERE / 'plan.json').read_text())
    for path, sha in plan['input_files'].items():
        need(digest((REPO / path).read_bytes()) == sha, ('input identity', path))
    points, host_edges, _ = I.geometry()
    boundary = json.loads((REPO / 'hadwiger_nelson_heule632_minimize/boundary.json').read_text())
    mandatory = set(boundary['mandatory_vertices'])
    optional = set(boundary['optional_vertices'])
    need(not mandatory & optional and len(mandatory) == 492 and len(optional) == 68, 'M/U partition')
    vertices = mandatory | optional
    parent = json.loads((REPO / 'hadwiger_nelson_heule632_minimize/certificate.json').read_text())
    need(vertices == set(parent['retained']), 'accepted support')
    edges = [(a, b) for a, b in host_edges if a in vertices and b in vertices]
    large = {v for v in vertices if all(all(r % 5 for r in axis) for axis in points[v])}
    small = vertices - large
    cross = [(a, b) if a in large else (b, a) for a, b in edges if (a in large) != (b in large)]
    separator = {a for a, b in cross}
    need(len(edges) == 2758 and len(cross) == 33, 'edge census')
    need(len(large) == 383 and len(small) == 177 and len(separator) == 19, 'field split')
    need(separator <= mandatory, 'mandatory separator')
    need(not any(a in separator and b in separator for a, b in edges), 'independent separator')
    return mandatory, optional, large, small, separator, edges, cross


def direct_formula(vertices, edges, separator, states):
    """One-hot colours and first-occurrence normal form; no triangle pins."""
    position = {v: i for i, v in enumerate(vertices)}
    var = lambda v, c: 4 * position[v] + c + 1
    clauses = []
    for v in vertices:
        clauses.append([var(v, c) for c in range(4)])
        for a in range(4):
            for b in range(a + 1, 4):
                clauses.append([-var(v, a), -var(v, b)])
    for u, v in edges:
        if u in position and v in position:
            for c in range(4):
                clauses.append([-var(u, c), -var(v, c)])
    for i, v in enumerate(separator):
        for c in range(1, 4):
            clauses.append([-var(v, c)] + [var(w, c - 1) for w in separator[:i]])
    base_count = len(clauses)
    for state in states:
        clauses.append([-var(v, int(c)) for v, c in zip(separator, state)])
    raw = (f'p cnf {4 * len(vertices)} {len(clauses)}\n' + ''.join(' '.join(map(str, c)) + ' 0\n' for c in clauses)).encode('ascii')
    return raw, base_count


def inspect(certificate, geo, manifest):
    mandatory, optional, large, small, separator, edges, cross = geo
    q = sorted(separator)
    need(certificate['separator'] == q, 'separator identity')
    need(certificate['optional_large'] == sorted(large & optional), 'nine optional vertices')
    matching = certificate['cross_matching']
    need(len(matching) == 19 and all(tuple(e) in cross for e in matching), 'matching edges')
    need(len({v for e in matching for v in e}) == 38, 'matching disjointness')
    need(certificate['record_improvement'] is False and certificate['whole560_family_closed'] is False, 'claim scope')
    formulas = {}
    state_sets = {}
    edge_checks = 0
    block_report = {}
    for name, support in [('mandatory', mandatory & large), ('full', large)]:
        block = certificate['blocks'][name]
        vs = sorted(support)
        need(block['vertices'] == vs, 'block support')
        es = [(a, b) for a, b in edges if a in support and b in support]
        words = []
        for row in block['states']:
            text = row['colouring']
            need(len(text) == len(vs) and set(text) <= set('0123'), 'colour string')
            colour = dict(zip(vs, text))
            need(all(colour[a] != colour[b] for a, b in es), 'proper unit edges')
            state = ''.join(colour[v] for v in q)
            need(state == row['state'] == canonical(state), 'canonical restriction')
            words.append(state)
            edge_checks += len(es)
        need(words == sorted(set(words)), 'ordered distinct states')
        state_sets[name] = set(words)
        raw, base_count = direct_formula(vs, edges, q, words)
        need(digest(raw) == manifest[name]['cnf_sha256'], 'completeness CNF identity')
        need(len(raw) == manifest[name]['cnf_bytes'], 'CNF size')
        formulas[name] = raw
        block_report[name] = {'vertices': len(vs), 'edges': len(es), 'states': len(words), 'variables': 4 * len(vs), 'base_clauses': base_count, 'complete_clauses': base_count + len(words), 'state_sha256': digest(('\n'.join(words) + '\n').encode()), 'cnf_sha256': digest(raw)}
    need(state_sets['full'] <= state_sets['mandatory'], 'restriction inclusion')
    right = small | separator
    report = {'separator': q, 'cross_edges': len(cross), 'minimum_cross_edge_endpoint_cover': 19,
              'host_pairs_checked': 199396, 'seed_vertices': 560, 'seed_edges': len(edges),
              'large_vertices': len(large), 'small_vertices': len(small),
              'right_block_vertices': len(right), 'right_block_edges': sum(a in right and b in right for a, b in edges),
              'mandatory_right_vertices': len(right & mandatory), 'mandatory_right_edges': sum(a in right & mandatory and b in right & mandatory for a, b in edges),
              'optional_large': sorted(optional & large), 'optional_right_count': len(optional & small),
              'positive_unit_edge_checks': edge_checks, 'blocks': block_report,
              'lost_states_when_all_nine_present': len(state_sets['mandatory'] - state_sets['full']),
              'unconstrained_palette_orbits': (4**19 + 6 * 2**19 + 8) // 24,
              'whole560_family_closed': False, 'record_improvement': False}
    return report, formulas


def controls(certificate, geo, manifest):
    # Exact finite normalization controls; the arbitrary-length argument is in README.
    normalization_cases = 0
    for n in range(1, 6):
        for word in itertools.product('0123', repeat=n):
            cnf_rule = all(int(c) == 0 or str(int(c) - 1) in word[:i] for i, c in enumerate(word))
            need(cnf_rule == (''.join(word) == canonical(word)), 'normalization control')
            normalization_cases += 1
    mutations = []
    x = copy.deepcopy(certificate); x['separator'].pop(); mutations.append(x)
    x = copy.deepcopy(certificate); x['cross_matching'][1] = x['cross_matching'][0]; mutations.append(x)
    x = copy.deepcopy(certificate); x['blocks']['mandatory']['states'].pop(); mutations.append(x)
    x = copy.deepcopy(certificate); x['blocks']['full']['states'][0]['colouring'] = '0' * 383; mutations.append(x)
    x = copy.deepcopy(certificate); x['blocks']['full']['vertices'].pop(); mutations.append(x)
    x = copy.deepcopy(certificate); x['record_improvement'] = True; mutations.append(x)
    for x in mutations:
        try:
            inspect(x, geo, manifest)
        except ValueError:
            continue
        raise ValueError('corrupt certificate accepted')
    return {'normalization_words_checked': normalization_cases, 'mutations_rejected': len(mutations)}


def limits():
    resource.setrlimit(resource.RLIMIT_AS, (4 * 1024**3, 4 * 1024**3))
    resource.setrlimit(resource.RLIMIT_FSIZE, (512 * 1024**2, 512 * 1024**2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument('--archive', type=Path)
    mode.add_argument('--prove', action='store_true')
    mode.add_argument('--positives-only', action='store_true')
    ap.add_argument('--kissat', default='/scratch/researcher3-kissat/build/kissat')
    ap.add_argument('--drat-trim', default='/scratch/drat-trim-package/usr/bin/drat-trim')
    args = ap.parse_args(); args.out.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    certificate = json.loads((HERE / 'certificate.json').read_text())
    manifest = json.loads((HERE / 'proof_manifest.json').read_text())
    geo = geometry()
    report, formulas = inspect(certificate, geo, manifest)
    report['controls'] = controls(certificate, geo, manifest)
    proof_checks = {}
    if not args.positives_only:
        for name, raw in formulas.items():
            cnf = args.out / (name + '_complete.cnf'); cnf.write_bytes(raw)
            if args.archive:
                need((args.archive / cnf.name).read_bytes() == raw, 'archived CNF byte comparison')
                proof = args.archive / (name + '_complete.drat')
                need(digest(proof.read_bytes()) == manifest[name]['proof_sha256'], 'archived proof identity')
            else:
                proof = args.out / (name + '_complete.drat')
                with (args.out / (name + '_kissat.log')).open('wb') as log:
                    result = subprocess.run([args.kissat, '--seed=0', '--conflicts=2000000', '--time=120', str(cnf), str(proof)], stdout=log, stderr=subprocess.STDOUT, timeout=135, preexec_fn=limits)
                need(result.returncode == 20, 'fresh proof solver UNSAT')
            log_path = args.out / (name + '_drat.log')
            with log_path.open('wb') as log:
                result = subprocess.run([args.drat_trim, str(cnf), str(proof)], stdout=log, stderr=subprocess.STDOUT, timeout=135, preexec_fn=limits)
            need(result.returncode == 0 and b's VERIFIED' in log_path.read_bytes().splitlines(), 'DRAT acceptance')
            proof_checks[name] = {'verified': True, 'proof_sha256': digest(proof.read_bytes()), 'proof_bytes': proof.stat().st_size}
    report['proof_checks'] = proof_checks
    report['complete_boundary_relations_verified'] = len(proof_checks) == 2
    report['seconds'] = time.monotonic() - started
    (args.out / 'result.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    main()
