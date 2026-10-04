"""Preimport source and full coefficient-map verification; Python 3.12 stdlib."""
from pathlib import Path
import argparse
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
BASELINE_SHA = '345874798f0263debfed05d8add567f341aa66b584a00cdb09c2586be3530618'
SEALED_FILES = {'.gitignore', 'arithmetic.py', 'coercivity.py', 'verify.py',
                'validate.py', 'EXPECTED.json', 'PROOF.md', 'README.md',
                'DEPENDENCIES.json', 'LITERATURE.md', 'provenance.json',
                'VALIDATION.json'}


def unique(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError('duplicate JSON key')
        out[key] = value
    return out


def load_json(raw):
    return json.loads(raw, object_pairs_hook=unique,
                      parse_constant=lambda text: (_ for _ in ()).throw(ValueError(text)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline', type=Path,
                        default=HERE.parent/'third-boundary-optimum/EXPECTED.json')
    parser.add_argument('--damage', choices=['sixth_sign', 'missing_norm_payment',
                                           'quadratic_skew_sign', 'frozen_moving_phi'])
    parser.add_argument('--fixture-damage', choices=['normal_coefficient', 'dropped_phi_term',
                                                   'boolean_as_integer', 'sign_as_number'])
    args = parser.parse_args()
    manifest = {}
    for line in (HERE/'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ', 1)
        if (len(digest) != 64 or name in manifest or
                Path(name).name != name or name == 'SHA256SUMS'):
            raise ValueError('invalid source manifest')
        manifest[name] = digest
    if manifest.keys() != SEALED_FILES:
        raise ValueError('incomplete or excess preimport seal')
    if {p.name for p in HERE.iterdir() if p.is_file()} != SEALED_FILES | {'SHA256SUMS'}:
        raise ValueError('unlisted source-directory file')
    for name, digest in manifest.items():
        if hashlib.sha256((HERE/name).read_bytes()).hexdigest() != digest:
            raise ValueError('preimport source seal: '+name)
    baseline_raw = args.baseline.read_bytes()
    if hashlib.sha256(baseline_raw).hexdigest() != BASELINE_SHA:
        raise ValueError('whole credited10152 baseline pin')
    baseline = load_json(baseline_raw)
    expected = load_json((HERE/'EXPECTED.json').read_bytes())
    if args.fixture_damage == 'normal_coefficient':
        expected['moving_third_normals']['4'][0][0][1] = '1/999'
    elif args.fixture_damage == 'dropped_phi_term':
        expected['moving_phi_exact_sum_mean_norm'][0].pop()
    elif args.fixture_damage == 'boolean_as_integer':
        expected['independent_review'] = 0
    elif args.fixture_damage == 'sign_as_number':
        expected['rational_positive_signs'][0]['lower'] = 0.0
    # No mathematical module has been imported above this boundary.
    from coercivity import build
    from arithmetic import canonical, need
    actual = build(baseline, args.damage)
    need(canonical(actual) == canonical(expected), 'ENTIRE strict canonical expected record')
    payload = canonical(actual)
    print(json.dumps({'complete': True, 'agent': 'six-sendov-3', 'role': 'researcher',
                      'whole_identities': len(actual['whole_identities']),
                      'positive_rational_signs': len(actual['rational_positive_signs']),
                      'whole_record_bytes': len(payload),
                      'whole_record_sha256': hashlib.sha256(payload).hexdigest(),
                      'whole_baseline_sha256': BASELINE_SHA,
                      'analytic_bridges_unformalized': True,
                      'independent_review': False}, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, IndexError, TypeError, FileNotFoundError) as error:
        print('REJECT: '+str(error), file=sys.stderr)
        sys.exit(1)
