"""Small valid certificates and targeted malformed/false certificate controls."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import resource
import sys
import time

from check_positive_lrat import InvalidProof, verify


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    if args.output_dir.exists():
        raise RuntimeError('Existing controls')
    began = time.monotonic()
    args.output_dir.mkdir(parents=True)
    cnf = 'p cnf 1 2\n1 0\n-1 0\n'
    proof = '3 0 1 2 0\n'
    fixtures = [
        ('positive_units', cnf, proof, None),
        ('positive_learned_clause', 'p cnf 2 4\n1 2 0\n1 -2 0\n-1 2 0\n-1 -2 0\n',
         '5 1 0 1 2 0\n6 0 5 3 4 0\n', None),
        ('false_empty_without_hints', cnf, '3 0 0\n', 'Mandatory positive RUP hints; RAT unsupported'),
        ('SAT_false_empty', 'p cnf 1 1\n1 0\n', '2 0 1 0\n', 'RUP hint chain has no actual contradiction'),
        ('missing_terminal_empty', cnf, '', 'No verified terminal empty clause'),
        ('negative_RAT_hint', cnf, '3 0 -1 2 0\n', 'Mandatory positive RUP hints; RAT unsupported'),
        ('deleted_hint', cnf, '2 d 1 0\n3 0 1 2 0\n', 'Unavailable proof hint'),
        ('delete_unavailable', cnf, '2 d 3 0\n', 'Deleting unavailable clause'),
        ('reused_identifier', cnf, '2 0 1 2 0\n', 'Fresh increasing proof clause identifiers'),
        ('satisfied_hint', cnf, '3 0 1 1 2 0\n', 'Satisfied hint cannot justify RUP propagation'),
        ('nonunit_hint', 'p cnf 2 1\n1 2 0\n', '2 0 1 0\n', 'Hint is not an actual unit or false clause'),
        ('extra_hints', cnf, '3 0 1 2 1 0\n', 'Hints extend beyond actual conflict'),
        ('outside_variable', cnf, '3 2 0 1 2 0\n', 'Actual variable domain'),
        ('duplicate_literal', cnf, '3 1 1 0 1 2 0\n', 'Non-tautological proof clause'),
        ('tautological_clause', cnf, '3 1 -1 0 1 2 0\n', 'Non-tautological proof clause'),
        ('missing_original_row', 'p cnf 1 3\n1 0\n-1 0\n', proof, 'Complete CNF row count'),
        ('content_after_empty', cnf, proof + '3 d 1 0\n', 'Proof content follows terminal empty clause'),
    ]
    records = []
    for name, original, trace, reason in fixtures:
        c, p = args.output_dir / (name + '.cnf'), args.output_dir / (name + '.lrat')
        c.write_text(original)
        p.write_text(trace)
        try:
            answer = verify(c, p)
        except InvalidProof as error:
            if reason is None or str(error) != reason:
                raise RuntimeError(f'Wrong rejection for {name}: {error}')
            records.append({'name': name, 'status': 'EXPECTED_EXACT_DEFECT_REJECTED', 'reason': str(error)})
        else:
            if reason is not None:
                raise RuntimeError(f'False proof accepted: {name}')
            records.append({'name': name, 'status': answer['status'], 'proof_obligation_cases': answer['proof_obligation_cases']})
    result = {'agent': 'six-vdw-1', 'role': 'researcher', 'checked_at': datetime.now(timezone.utc).isoformat(),
              'status': 'TWO_POSITIVE_CERTIFICATES_AND_FIFTEEN_EXACT_RUP_CORRUPTIONS_VERIFIED',
              'controls': records, 'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'checker_sha256': hashlib.sha256(Path(__file__).with_name('check_positive_lrat.py').read_bytes()).hexdigest(),
              'interpreter_optimization': sys.flags.optimize, 'seconds': time.monotonic() - began,
              'maxrss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, 'threads': 1, 'new_W_bound': None}
    (args.output_dir / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'controls'}, indent=2), flush=True)


if __name__ == '__main__':
    main()
