"""Regenerate and verify a complete full-coordinate endpoint proof from public data."""
import argparse
import json
from pathlib import Path

from original import audit, build, canonical, digest, require, shifted_form
from positive_elimination import eliminate


def check_proof(proof):
    require(proof['status'] == 'positive_definite' and proof['dimension'] == 253 and
            len(proof['normalized_pivots']) == len(proof['positive_contents']) ==
            len(proof['original_leading_minors']) == 253,
            'full original endpoint coverage, no necessary-type shortcut')
    require(all(int(x) > 0 for key in ('normalized_pivots', 'positive_contents', 'original_leading_minors')
                for x in proof[key]), 'every original endpoint sign')
    require(proof['symmetric_numerator_updates'] == 2699004 and
            proof['checked_content_divisions'] == sum(i * i for i in range(1, 254)),
            'entire full-coordinate update and division census')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--endpoint', choices=('lower', 'upper'), required=True)
    parser.add_argument('--coefficients', default=str(Path(__file__).with_name('COEFFICIENTS.json')))
    parser.add_argument('--record', required=True)
    parser.add_argument('--full-record')
    args = parser.parse_args()
    point = build(json.loads(Path(args.coefficients).read_bytes()))
    model = audit(point)
    matrix = shifted_form(point, args.endpoint)
    proof = eliminate(matrix)
    check_proof(proof)
    result = {'agent': 'six-downset-2', 'role': 'researcher', 'q': 17, 'k': 8,
              'N': 255, 's': 55, 'h': 200, 'endpoint': args.endpoint, 'margin': '1/1024',
              'whole_shifted_matrix_sha256': digest(matrix), 'whole_proof_sha256': digest(proof),
              'positive_original_leading_minors': 253, 'positive_normalized_pivots': 253,
              'symmetric_numerator_updates': proof['symmetric_numerator_updates'],
              'content_divisions': proof['checked_content_divisions'],
              'model': model, 'no_external_positive_factor_or_reference_minor_input': True,
              'ordinary_bridges_unformalized': True, 'independently_reviewed': False}
    Path(args.record).write_bytes(canonical(result) + b'\n')
    if args.full_record:
        Path(args.full_record).write_bytes(canonical(proof) + b'\n')
    print(json.dumps(result))
