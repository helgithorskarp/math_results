#!/usr/bin/env python3
"""Direct positive verification and exhaustive membership comparison.

Imports no producing graph, CNF or runner code. No solver is needed.
"""
import argparse
import copy
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'hadwiger_nelson_heule632_pair_pilot'))
import independent as I
spec = importlib.util.spec_from_file_location('kempe_checker', ROOT / 'hadwiger_nelson_heule560_kempe/verify.py')
K = importlib.util.module_from_spec(spec)
spec.loader.exec_module(K)


def inputs():
    plan = json.loads((HERE / 'plan.json').read_text())
    for name, digest in plan['input_files'].items():
        I.check(sha256((ROOT / name).read_bytes()).hexdigest() == digest, 'input identity: ' + name)
    boundary = json.loads((ROOT / 'hadwiger_nelson_heule632_minimize/boundary.json').read_text())
    previous = json.loads((ROOT / 'hadwiger_nelson_heule560_kempe/certificate.json').read_text())
    mandatory = boundary['mandatory_vertices']
    endpoints = sorted({v for row in previous['combined_minimal_nonextending_sets'] for v in row})
    retained = sorted(set(mandatory) | set(endpoints))
    I.check(len(mandatory) == 492 and len(endpoints) == 11 and len(retained) == 503, 'support construction')
    I.check(endpoints == plan['endpoint_vertices'] and retained == plan['retained'], 'frozen support identity')
    # This independent helper rebuilds geometry by sparse-radicand arithmetic
    # and all 246 component switch slots by union-find, giving 118 templates.
    data = K.prepare()
    I.check(data['mandatory'] == mandatory, 'same mandatory set')
    edges = data['edges']
    clauses, raw, vertices, triangle = I.formula(retained, edges, 4)
    I.check(sha256(raw).hexdigest() == plan['cnf_sha256'] and len(raw) == plan['cnf_bytes'], 'independent formula identity')
    I.check(len(clauses) == plan['cnf_clauses'] and 4 * len(vertices) == plan['cnf_variables'] and triangle == plan['triangle'], 'CNF domain')
    return plan, previous, data, endpoints, retained, clauses, raw


def check(certificate, info):
    plan, previous, data, endpoints, retained, clauses, raw = info
    I.check(certificate['status'] == 'SAT' and certificate['chromatic_number_upper_bound'] == 4, 'positive claim')
    I.check(certificate['retained'] == retained and certificate['endpoint_vertices'] == endpoints, 'certificate support')
    I.check(certificate['vertices'] == 503 and certificate['edges'] == plan['edges'] == 2453, 'positive graph size')
    I.check(certificate['four_cnf_sha256'] == sha256(raw).hexdigest(), 'certificate formula')
    text = certificate['four_colouring']
    omitted = sorted(set(range(632)) - set(retained))
    checks = I.colouring(text, omitted, data['edges'], 4)
    I.check(checks == certificate['four_colouring_edge_checks'] == 2453, 'all exact unit edges')
    normalized = K.canonical(text, data['mandatory'])
    I.check(normalized not in data['family'], 'new mandatory colouring escapes the complete one-pair family')
    restrictions = []
    for row in previous['combined_minimal_nonextending_sets']:
        support = set(data['mandatory']) | set(row)
        restricted = ''.join(c if v in support else '.' for v, c in enumerate(text))
        count = I.colouring(restricted, sorted(set(range(632)) - support), data['edges'], 4)
        restrictions.append({'optional_set': row, 'vertices': len(support), 'edges': count})
    # The complete E-subset family follows by restriction, without any new query.
    I.check(all(set(row) <= set(endpoints) for row in previous['combined_minimal_nonextending_sets']), 'all nine sets present')
    I.check(not certificate['record_improvement'] and not certificate['whole560_family_closed'], 'scope flags')
    return {'vertices': 503, 'unit_edges': checks, 'chromatic_number_upper_bound': 4,
            'endpoint_vertices': endpoints, 'all_endpoint_subset_supports_four_colourable': 2 ** len(endpoints),
            'restricted_obstruction_supports': restrictions,
            'restriction_edge_checks': sum(row['edges'] for row in restrictions),
            'four_cnf_variables': plan['cnf_variables'], 'four_cnf_clauses': len(clauses), 'four_cnf_bytes': len(raw),
            'four_cnf_sha256': sha256(raw).hexdigest(), 'triangle': plan['triangle'],
            'host_point_pair_checks': 199396, 'kempe_full_switch_slots': data['full_slots'],
            'kempe_distinct_templates': len(data['family']), 'kempe_template_stream_sha256': data['family_sha256'],
            'normalized_mandatory_colouring_sha256': sha256(normalized.encode('ascii')).hexdigest(),
            'outside_one_pair_family_modulo_palette': True,
            'whole560_family_closed': False, 'record_improvement': False,
            'size508_supports_newly_closed_by_this_503_witness': 0}


def archive_check(archive, info, expected):
    plan, previous, data, endpoints, vertices, clauses, raw = info
    I.check((archive / 'four.cnf').read_bytes() == raw, 'native CNF bytes')
    output = (archive / 'four.log').read_text()
    I.check('s SATISFIABLE' in output.splitlines(), 'native status')
    literals = [int(token) for line in output.splitlines() if line.startswith('v ') for token in line.split()[1:] if token != '0']
    truth = {abs(lit): lit > 0 for lit in literals}
    I.check(len(truth) == len(literals) == 2012 and set(truth) == set(range(1, 2013)), 'complete signed model')
    for clause in clauses:
        I.check(any(truth[abs(lit)] == (lit > 0) for lit in clause), 'every native clause')
    decoded = ['.'] * 632
    for index, v in enumerate(vertices):
        colours = [c for c in range(4) if truth[4 * index + c + 1]]
        I.check(len(colours) == 1, 'one-hot decode')
        decoded[v] = str(colours[0])
    I.check(''.join(decoded) == expected, 'independent native decode')
    return len(clauses)


def controls(cert, info):
    variants = []
    bad = copy.deepcopy(cert)
    bad['four_colouring'] = bad['four_colouring'][:-1]
    variants.append(('short_colour_string', bad))
    bad = copy.deepcopy(cert)
    text = list(bad['four_colouring'])
    text[310] = '.'
    bad['four_colouring'] = ''.join(text)
    variants.append(('missing_endpoint', bad))
    bad = copy.deepcopy(cert)
    text = list(bad['four_colouring'])
    text[143] = text[0]
    bad['four_colouring'] = ''.join(text)
    variants.append(('monochromatic_unit_edge', bad))
    bad = copy.deepcopy(cert)
    bad['endpoint_vertices'] = bad['endpoint_vertices'][:-1]
    variants.append(('wrong_endpoint_union', bad))
    bad = copy.deepcopy(cert)
    bad['record_improvement'] = True
    variants.append(('false_record_flag', bad))
    rejected = []
    for label, bad in variants:
        try:
            check(bad, info)
        except ValueError:
            rejected.append(label)
        else:
            raise ValueError('corrupt certificate accepted: ' + label)
    return rejected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    parser.add_argument('--archive', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    info = inputs()
    cert = json.loads(args.certificate.read_text())
    report = check(cert, info)
    report['malformed_certificates_rejected'] = controls(cert, info)
    report['native_model_clauses_checked'] = archive_check(args.archive, info, cert['four_colouring']) if args.archive else 0
    report['certificate_sha256'] = sha256(args.certificate.read_bytes()).hexdigest()
    report['elapsed_seconds'] = time.monotonic() - start
    (args.out / 'verification.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
