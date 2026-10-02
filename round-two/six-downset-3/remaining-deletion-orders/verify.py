"""complete finite-k/universal-dual record with a frozen exact replay."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import argparse
import json
import time
import calibrate
import direct
import dual
import sample
import three_vectors
import orbits
from exact import schur_psd, polynomial_psd, digest
from literal import require

ROOT = Path(__file__).resolve().parent


def reject(function, label):
    try:
        function()
    except ValueError:
        return label
    raise ValueError('false certificate was accepted: '+label)


def controls():
    data = orbits.forms(35, 8)
    # These are false mathematical certificates checked by actual exact PSD.
    rejected = [reject(lambda: orbits.floor(data, F(0), F(0), F(1)),
                       'false positive unit cap floor'),
                reject(lambda: schur_psd(orbits.evaluate(data, F(-1, 4096), F(0))[0]),
                       'false lower PSD at negative kappa'),
                reject(lambda: orbits.forms(5, 4), 'missing small-group orbit census'),
                reject(lambda: three_vectors.scalars(5, 2), 'unproved q<3k orientation scope')]
    malformed = [row[:] for row in data['U0']]
    malformed[0][1] += 1
    rejected.append(reject(lambda: schur_psd(malformed), 'asymmetric weighted Gram'))
    return rejected


def run():
    validation = calibrate.run()
    finite = sample.run()
    exceptional = dual.probe(74, 15)
    mechanism = three_vectors.run()
    original_exception = direct.run()
    positive, negative, ranks = [], [], []
    for row in finite['records']:
        k, q = row['k'], row['q']
        data = orbits.forms(q, k)
        mechanism_record = three_vectors.check(data)
        row['three_vector_Q'] = mechanism_record['Q']
        row['three_vector_Delta'] = mechanism_record['Delta']
        if 'kappa' in row:
            positive.append(k)
            G, H = orbits.evaluate(data, F(row['kappa']), F(row['t']))
            # Separate exact characteristic algorithm by the same author.
            c, u = polynomial_psd(G), polynomial_psd(H)
            require((c[0], u[0]) == (22, 23), 'all positive characteristic ranks')
            ranks.append({'k': k, 'q': q, 'lower_rank': c[0], 'lower_polynomial_digest': c[1],
                          'upper_rank': u[0], 'upper_polynomial_digest': u[1]})
        elif k == 15:
            require(F(mechanism_record['Q']) < 0 < F(mechanism_record['Delta']),
                    'new universal mechanism resolves actual exception')
            row['status'] = 'NEW original three-vector all-real ansatz exclusion'
            row['compact_exceptional_original_dual'] = {key: exceptional[key]
                                                       for key in ('original_U0', 'original_Delta', 'original_R')}
            negative.append(k)
        else:
            require(F(row['Q0']) < 0 < F(row['credited_dual_Delta']), 'entire credited negative group')
            negative.append(k)
    require(positive == [8, 10, 13, 16, 18, 19, 21, 22, 24]
            and negative == [5, 6, 7, 9, 11, 12, 14, 15, 17, 20, 23],
            'complete finite-k boundary partition, no undecided k')
    imported = [orbits.SOURCE / name for name in ('variance-deletion-frontier/pins.py',
                'variance-deletion-frontier/variance.py', 'variance-deletion-frontier/point.py',
                'variance-deletion-frontier/algebra.py', 'small-deletion-boundary/literal.py',
                'triangle-majority/exact.py')]
    input_bytes = [{'path': str(p.relative_to(orbits.SOURCE)), 'sha256': sha256(p.read_bytes()).hexdigest()}
                   for p in imported]
    result = {'agent': 'six-downset-3', 'role': 'researcher',
              'status': 'exact author proof, unformalized, independently unreviewed, standalone verifier supplies no independent review or graph commitment',
              'complete_classification': {'k_domain': [5, 24], 'q_domain': 'ALL q>=max(4,k)',
                  'deletions': 'ALL Z subset W, sizek', 'positive_boundary_cutoff_b_minus5': positive,
                  'negative_boundary_cutoff_b_minus4': negative,
                  'imports': '9478 negative ALLq<=b-6 and9546 positive ALLq>=b-4',
                  'new_k_coverage': [7, 24], 'known_k5_k6_not_claimed_new': True,
                  'ansatz_only_not_arbitrary_H_exclusions': True},
              'calibration': validation, 'finite_boundary_cases': finite,
              'new_universal_necessary_mechanism': mechanism,
              'new_compact_original_exceptional_dual': exceptional,
              'independent_original_exception': original_exception,
              'separate_same_author_characteristic_checks': ranks,
              'semantic_false_certificates_rejected': controls(), 'complete_executable_inputs': input_bytes,
              'limits': {'native_threads': 1, 'math_jobs': 1, 'per_process_seconds': 60,
                         'scope': 'unchanged1CPU2GiB', 'old_inverse_method': 'PAUSED, not rerun'},
              'remaining_frontier': 'k>=25 general b-5 classification, no infinite converse from this finite partition'}
    result['record_sha256'] = digest(result)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--freeze', action='store_true')
    arguments = parser.parse_args()
    start = time.perf_counter()
    result = run()
    target = ROOT / 'EXPECTED.json'
    if arguments.freeze:
        require(not target.exists(), 'refuse to overwrite existing frozen proof record')
        target.write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    else:
        expected = json.loads(target.read_text())
        require(json.loads(json.dumps(result, sort_keys=True)) == expected,
                'ENTIRE canonically normalized exact frozen record differs')
    (ROOT / 'RESULTS.json').write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    print(json.dumps({'record_sha256': result['record_sha256'], 'seconds': time.perf_counter()-start,
                      'all_k_boundary_cases': len(result['finite_boundary_cases']['records']),
                      'positive_coefficients': 133, 'original_calibration_pairs': 291661,
                      'new_original_exception_representative_positions': 73853,
                      'status': result['status']}))
