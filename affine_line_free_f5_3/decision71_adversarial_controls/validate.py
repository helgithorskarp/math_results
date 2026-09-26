"""Small semantic and corrupted-fixture controls, also effective under Python -O."""
import argparse
from copy import deepcopy
from itertools import product
import json
from pathlib import Path

from verify import check_fixture, formula, load_fixtures, require


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    records, seeds = load_fixtures()
    for r in records:
        check_fixture(r, seeds)
    # Each cardinality block, including n=0, must have precisely its intended models.
    trials = 0
    for n in range(5):
        word = str(n)+'4'*24
        clauses = [c for c in formula(word)[775:-3] if all(abs(v) <= 5 for v in c)]
        for bits in product((False, True), repeat=5):
            actual = all(any(bits[abs(v)-1] == (v > 0) for v in c) for c in clauses)
            require(actual == (sum(bits) == n), 'five-point cardinality truth table failed')
            trials += 1
    damaged = []
    for label in ('duplicate_point', 'missing_point', 'wrong_weight', 'wrong_gauge',
                  'wrong_line', 'wrong_omission', 'singular_map', 'wrong_source_map',
                  'wrong_intersection', 'wrong_formula_hash'):
        r = deepcopy(records[0])
        if label == 'duplicate_point':
            r['points'][0] = r['points'][1]
        elif label == 'missing_point':
            r['points'].pop()
        elif label == 'wrong_weight':
            r['weights'] = '1'+r['weights'][1:]
        elif label == 'wrong_gauge':
            r['gauge'] = [0, 1, 2]
        elif label == 'wrong_line':
            r['full_lines'][0][0] = 124
        elif label == 'wrong_omission':
            r['removed_clause_indices'][0] = 0
        elif label == 'singular_map':
            r['affine_matrix'][2] = r['affine_matrix'][0][:]
        elif label == 'wrong_source_map':
            r['affine_offset'][0] = (r['affine_offset'][0]+1) % 5
        elif label == 'wrong_intersection':
            r['added_image'] = 124
        else:
            r['original_cnf_sha256'] = '0'*64
        try:
            check_fixture(r, seeds)
        except ValueError:
            damaged.append(label)
        else:
            raise ValueError('corrupted fixture accepted: '+label)
    result = {'status': 'ADVERSARIAL_FIXTURE_REJECTION_CONTROLS_PASSED',
              'cardinality_truth_assignments': trials,
              'corrupted_fixtures_rejected': damaged,
              'global_exact_proof_accepted': False}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
