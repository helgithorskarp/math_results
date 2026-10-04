"""Regenerate ALL253 new positive minors, with no imported positive factors."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
from original import audit, build, canonical, require
from sparse import point_at
from check_original import audit_new, endpoint_form
from positive_elimination import eliminate


def check_proof(proof):
    require(proof.get('status') == 'positive_definite' and proof.get('dimension') == 253,
            'complete253 positive endpoint, no quotient or incomplete result')
    for key in ('original_leading_minors', 'normalized_pivots', 'positive_contents'):
        require(len(proof.get(key, [])) == 253 and all(int(x) > 0 for x in proof[key]),
                'EVERY original minor, pivot and positive scale')
    require(proof['symmetric_numerator_updates'] == 2699004 and
            proof['checked_content_divisions'] == 5430139, 'full original-coordinate update census')


def run(tau, record_path, full_path):
    base = build(json.loads(Path(__file__).with_name('COEFFICIENTS.json').read_bytes()))
    audit(base)
    _, T, L = point_at(base, tau, return_matrices=True)
    model = audit_new(base, tau, T, L)
    den, K = endpoint_form(T)
    require(den == (5505024 if tau == 0 else 27525120), 'fresh endpoint denominators')
    proof = eliminate(K)
    check_proof(proof)
    raw = canonical(proof)+b'\n'
    Path(full_path).write_bytes(raw)
    result = {'agent': 'six-downset-2', 'role': 'researcher', 'model': model,
              'fresh_T_floor': '1/1024', 'complete_original_leading_minors': 253,
              'complete_normalized_pivots': 253,
              'full_proof_sha256': hashlib.sha256(raw).hexdigest(),
              'no_seed_factors_minors_or_margins_as_input': True,
              'ordinary_real_affine_Sylvester_metric_bridges_unformalized': True,
              'independently_reviewed': False}
    Path(record_path).write_bytes(canonical(result)+b'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--tau', choices=('0', '1/128'), required=True)
    p.add_argument('--record', required=True); p.add_argument('--full-record', required=True)
    a = p.parse_args(); run(F(a.tau), a.record, a.full_record)
