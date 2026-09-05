#!/usr/bin/env python3
"""Rebuild the exact block and check a complete forbidden-signature proof.

Without --proof this checks inputs, geometry, encoding and degree peeling only.
It does not certify the universal boundary restriction without a DRAT proof.
"""
import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import subprocess
import tempfile
from engine import HERE, REPO, build, direct_cnf, load, require


def verify(args):
    data = build()
    expected = json.loads((HERE / 'expected.json').read_text())
    cert = json.loads((HERE / 'certificate.json').read_text())
    require(data['facts'] == expected, 'ambient preflight changed')
    labels = cert['selected']
    selected = set(labels)
    require(labels == sorted(selected) and selected <= set(data['vertices']), 'selected domain')
    require(set(data['interface']) <= selected, 'mandatory interface missing')
    require(cert['seed_omission'] == data['omit'] == 40 and 40 not in selected, 'seed omission')
    raw, vertices, edges = direct_cnf(data, selected)
    require(len(vertices) == cert['final_vertices'] == 870, 'final order')
    require(len(edges) == cert['final_edges'] == 4715, 'final edge count')
    require(sha256(raw).hexdigest() == cert['final_cnf_sha256'], 'final CNF digest')
    # A second published arithmetic routine checks the final listed edges.
    # Parsing and ambient enumeration are shared with engine.py; this is not
    # claimed to be a new independently authored audit of the whole package.
    other = load(REPO / 'hadwiger_nelson_parts509_point613_closure_review1/independent_check.py')
    unit = (288 * 288,) + (0,) * 7
    require(all(other.squared_distance(data['points'][u], data['points'][v]) == unit
                for u, v in edges), 'second arithmetic edge check')
    require(len({data['points'][v] for v in selected}) == 870, 'final coordinate collision')
    for row in cert['peeling']:
        v = row['v']
        require(v in selected and v not in data['interface'], 'peel domain')
        neighbours = sorted(data['adj'][v] & selected)
        require(neighbours == row['neighbors'] and len(neighbours) <= 3, 'peel degree')
        selected.remove(v)
    peeled_edges = [(u, v) for u, v in edges if u in selected and v in selected]
    require(len(selected) == cert['peeled_vertices'] == 869, 'peeled order')
    require(len(peeled_edges) == cert['peeled_edges'] == 4712, 'peeled edges')
    # Check only the geometric side of the imported S135 composition theorem.
    # The twenty blocking UNSAT certificates are an explicit external premise.
    interface = json.loads((REPO / 'hadwiger_nelson_parts509_interface_lemma/interface_L.json').read_text())
    S = set(range(374, 509))
    require(S.isdisjoint(selected), 'S label collision')
    require({data['points'][v] for v in S}.isdisjoint({data['points'][v] for v in selected}),
            'S coordinate collision')
    cross = interface['cross_edges_L_S']
    require(len(cross) == 30 and {u for u, v in cross} == set(data['interface']), 'cross interface')
    require(all(u in selected and v in S and other.squared_distance(data['points'][u], data['points'][v]) == unit
                for u, v in cross), 'original cross edges')
    S_edges = sum(other.squared_distance(data['points'][u], data['points'][v]) == unit
                  for u, v in combinations(sorted(S), 2))
    require(S_edges == interface['S_edges'] == 552, 'S geometry')
    result = dict(status='GEOMETRY AND ENCODING CHECKED; SIGNATURE PROOF NOT CHECKED',
                  ambient_vertices=976, ambient_edges=6406, final_vertices=870,
                  final_edges=4715, second_arithmetic_unit_edge_checks=len(edges),
                  peeled_vertices=869, peeled_edges=4712,
                  original_vertices_retained=sum(v < 374 for v in selected),
                  completion_vertices_retained=sum(v >= 509 for v in selected),
                  final_cnf_variables=4 * len(vertices),
                  final_cnf_clauses=len(raw.splitlines()) - 1,
                  final_cnf_sha256=sha256(raw).hexdigest(),
                  original_S_vertices=135, original_S_edges=S_edges, original_cross_edges=30,
                  imported_S_blocking_theorem_reproved_here=False,
                  target_block_budget=373, target_reached=False,
                  record_improvement=False, minimality_claimed=False,
                  complete_signature_proof_checked=False)
    if args.cnf:
        args.cnf.write_bytes(raw)
    if args.proof:
        with tempfile.TemporaryDirectory(prefix='hn-rigid-verify-') as name:
            cnf = Path(name) / 'block.cnf'
            cnf.write_bytes(raw)
            checked = subprocess.run([str(args.drat_trim.resolve()), str(cnf), str(args.proof.resolve())],
                                     capture_output=True, text=True)
            require(checked.returncode == 0 and 's VERIFIED' in checked.stdout,
                    ('complete DRAT check failed', checked.returncode, checked.stdout[-2000:], checked.stderr[-2000:]))
        digest = sha256(args.proof.read_bytes()).hexdigest()
        result.update(status='BLOCK SIGNATURE AND DEGREE-PEELED SIGNATURE VERIFIED',
                      complete_signature_proof_checked=True, drat_trim_exit=checked.returncode,
                      proof_sha256=digest, proof_bytes=args.proof.stat().st_size,
                      original_run_proof_hash_matches=digest == cert['final_proof_sha256'],
                      drat_trim_binary_sha256=sha256(args.drat_trim.read_bytes()).hexdigest())
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cnf', type=Path, help='write the deterministic 870-vertex CNF')
    parser.add_argument('--proof', type=Path, help='complete DRAT refutation of that CNF')
    parser.add_argument('--drat-trim', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    if bool(args.proof) != bool(args.drat_trim):
        parser.error('--proof and --drat-trim are required together')
    result = json.dumps(verify(args), indent=2, sort_keys=True) + '\n'
    if args.report:
        args.report.write_text(result)
    print(result, end='')


if __name__ == '__main__':
    main()
