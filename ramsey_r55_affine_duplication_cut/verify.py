#!/usr/bin/env python3
"""Reaudit all branch formulas and actually check all 32 DRAT proofs."""
import argparse
import json
from pathlib import Path
import audit_formula
import audit_geometry
import project
import runtime


def verify_all(work, checker):
    work = runtime.external(work)
    checker = runtime.check_tool(checker, 'drat-trim')
    geometry = audit_geometry.run()
    cases = [(i, c, entry['representative']) for i, entry in enumerate(geometry['orbits']) for c in (0, 1)]
    # Require the entire mathematically derived list before trusting any run.
    for i, c, _ in cases:
        p = work/'runs'/f'o{i:02d}c{c}'
        if not (p/'input.cnf').is_file() or not (p/'proof.drat').is_file() or (p/'proof.drat').stat().st_size == 0:
            raise ValueError('incomplete physical proof family: '+str(p))
    logs = work/'verification_logs'
    logs.mkdir(exist_ok=True)
    audits = []
    verified = []
    for i, c, D in cases:
        name = f'o{i:02d}c{c}'
        p = work/'runs'/name
        body, _ = project.build(D, c)
        if (p/'input.cnf').read_bytes() != body.encode():
            raise ValueError('formula does not match complete branch '+name)
        audits.append(audit_formula.audit(p/'input.cnf', D, c))
        proof = runtime.proof_check(checker, p/'input.cnf', p/'proof.drat', logs/(name+'.log'))
        verified.append({'branch': name, **proof})
        print(name+' PHYSICAL_PROOF_VERIFIED', flush=True)
    actual = json.dumps({'geometry':geometry, 'formulas':audits}, sort_keys=True)+'\n'
    if actual != (runtime.SOURCE/'expected_audit.json').read_text():
        raise ValueError('independent coverage/audit mismatch')
    result = {'status':'COMPLETE_AFFINE_DUPLICATION_FAMILY_EXCLUDED',
              'canonical_branches':32, 'all_proofs_physically_checked':True,
              'saved_solver_statuses_trusted':False, 'proofs':verified,
              'good43_found':False, 'ramsey_bound_improved':False}
    (work/'verified_family.json').write_text(json.dumps(result, indent=2)+'\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('work')
    parser.add_argument('--drat-trim', required=True)
    args = parser.parse_args()
    print(json.dumps(verify_all(args.work, args.drat_trim), sort_keys=True))
