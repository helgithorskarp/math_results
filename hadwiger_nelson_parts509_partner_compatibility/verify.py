#!/usr/bin/env python3
"""Check all saved witnesses and, when supplied, every complete small proof."""
import argparse
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path
import subprocess
import tempfile
from data import HERE, build, composition, list_cnf, check_S, require


def verify(args):
    data = build()
    require(data['facts'] == json.loads((HERE / 'expected.json').read_text()), 'expected geometry/encoding')
    cert = json.loads((HERE / 'certificate.json').read_text())
    require(cert['cases'] == [{k: r[k] for k in ('kind', 'query', 'cnf_sha256')} for r in data['cases']], 'case provenance')
    instances = {r['cnf_sha256']: r['masks'] for r in data['cases']}
    require(set(instances) == set(cert['instances']), 'instance coverage')
    positives = proofs = zeros = hash_matches = 0
    for digest, masks in instances.items():
        row = cert['instances'][digest]
        cnf = list_cnf(masks, data['S_edges'])
        require(sha256(cnf).hexdigest() == digest, 'instance identity')
        if row['status'] == 'SAT_CHECKED':
            check_S(row['S_colouring'], masks, data['S_edges'])
            positives += 1
        elif row['status'] == 'EMPTY_LIST_CHECKED':
            require(masks[row['blocked_vertex'] - 374] == 0, 'zero list witness')
            zeros += 1
        elif row['status'] == 'UNSAT_DRAT_CHECKED':
            if args.proofs:
                proof = args.proofs / digest / 'proof.drat'
                with tempfile.TemporaryDirectory(prefix='hn-partner-check-') as name:
                    fresh = Path(name) / 'input.cnf'
                    fresh.write_bytes(cnf)
                    checked = subprocess.run([str(args.drat_trim.resolve()), str(fresh), str(proof.resolve())],
                                             capture_output=True, text=True)
                require(checked.returncode == 0 and 's VERIFIED' in checked.stdout, ('proof rejected', digest))
                proofs += 1
                hash_matches += sha256(proof.read_bytes()).hexdigest() == row['proof_sha256']
        else:
            require(row['status'] == 'UNKNOWN', 'unknown certificate status')
    # Decode the positives against graph edges, without relying on the list
    # decoder to establish the composition claim.
    fixed = {r['query']: r for r in data['witnesses']}
    full_extensions = interface_extensions = 0
    actual_extension_edge_checks = 0
    for case in data['cases']:
        witness = fixed[case['query']]
        labels = sorted(set(data['vertices']) - set(witness['omitted']))
        T = dict(zip(labels, map(int, witness['colouring'])))
        edges = data['old_cross'] if case['kind'] == 'interface' else data['cross']
        # Rebuild available sets using set subtraction, independently of masks.
        available = {v: set(range(4)) - {T[u] for u, s in edges if s == v and u in T} for v in data['S']}
        require([sum(1 << c for c in available[v]) for v in data['S']] == case['masks'], 'direct available set audit')
        row = cert['instances'][case['cnf_sha256']]
        if row['status'] != 'SAT_CHECKED':
            continue
        S = dict(zip(data['S'], map(int, row['S_colouring'])))
        require(all(S[u] != S[v] for u, v in data['S_edges']), 'direct S edge check')
        require(all(T[u] != S[v] for u, v in edges if u in T), 'direct cross edge check')
        if case['kind'] == 'full':
            joined = T | S
            for u, v in data['all_edges']:
                if u in joined and v in joined:
                    require(joined[u] != joined[v], 'full graph extension witness')
                    actual_extension_edge_checks += 1
            full_extensions += 1
        else:
            interface_extensions += 1
    blocked = sorted(c['query'] for c in data['cases'] if c['kind'] == 'interface' and
                     cert['instances'][c['cnf_sha256']]['status'] in ('UNSAT_DRAT_CHECKED', 'EMPTY_LIST_CHECKED'))
    require(blocked == cert['blocked_interface_queries'], 'blocked interface coverage')
    maps = [(0,) + p for p in permutations((1, 2, 3))]
    orbits = {tuple(p[c] for c in fixed[q]['pattern']) for q in blocked for p in maps}
    canonical = {min(tuple(p[c] for c in fixed[q]['pattern']) for p in maps) for q in blocked}
    require([list(p) for p in sorted(canonical)] == cert['new_blocked_orbit_representatives'], 'blocked colour orbit representatives')
    require(orbits.isdisjoint(data['allowed']) and len(canonical) == 11 and len(orbits) == 66, 'strict pattern enlargement')
    if args.composition_cnf:
        args.composition_cnf.write_bytes(composition(data))
    result = dict(status='GEOMETRY AND POSITIVE WITNESSES VERIFIED; NEGATIVE PROOFS NOT CHECKED',
                  exact_list_instances=len(instances), positive_instances_checked=positives,
                  zero_list_instances_checked=zeros, complete_DRAT_proofs_checked=proofs,
                  original_proof_hash_matches=hash_matches, interface_patterns_with_extension=interface_extensions,
                  full_saved_colourings_with_extension=full_extensions,
                  actual_extension_edge_checks=actual_extension_edge_checks,
                  new_blocked_orbits_certified_here=0, composition_formula_solved=False,
                  smaller_block_constructed=False, whole_family_closed=False, record_improvement=False)
    if args.proofs:
        require(proofs == 22 and positives == 66 and full_extensions == 38 and interface_extensions == 33,
                'complete outcome coverage')
        result.update(status='ALL 93 COMPATIBILITY CASES VERIFIED; 11 NEW BLOCKED COLOUR ORBITS',
                      new_blocked_orbits_certified_here=11, new_blocked_patterns_certified_here=66)
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--proofs', type=Path, help='fresh run.py output directory containing the complete proofs')
    ap.add_argument('--drat-trim', type=Path)
    ap.add_argument('--composition-cnf', type=Path)
    ap.add_argument('--report', type=Path)
    args = ap.parse_args()
    if bool(args.proofs) != bool(args.drat_trim):
        ap.error('--proofs and --drat-trim must be supplied together')
    text = json.dumps(verify(args), indent=2, sort_keys=True) + '\n'
    if args.report:
        args.report.write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
