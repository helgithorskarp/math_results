#!/usr/bin/env python3
"""Regenerate exact annulus certificates; mandatory compact fixtures.

Author six-sendov-1, researcher. Standard-library arbitrary precision,
one process at a time. Hashes are regression metadata; the sign/inverse
checks and written coverage proof establish the certified inequalities.
"""
from pathlib import Path
from fractions import Fraction as F
from math import prod
import argparse, hashlib, json, os, resource, subprocess, sys, time

# Support isolated mode while importing only this contribution's source.
DIRECTORY = Path(__file__).resolve().parent
sys.path.insert(0, str(DIRECTORY))
import algebra as A
import certificate as C
import controls as V
import kernel as K
import stability as S

KEYS = ('E1', 'E2', 'E3', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6')
CASES = tuple(key+'-'+chart for chart in ('nearer', 'farther') for key in KEYS)
SCHEMA = 'six-sendov-1-equal-light-annulus-v1'
THREADS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
           'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS')


def compare(actual, expected, label):
    if actual != expected:
        raise ArithmeticError('Whole mandatory fixture mismatch: '+label)


def load_fixture(path):
    # Missing and malformed fixtures are errors, including under python -O.
    value = json.loads(path.read_text())
    K.require(isinstance(value, dict) and set(value) == {'schema', 'core', 'cases'},
              'Malformed fixture root')
    K.require(value['schema'] == SCHEMA, 'Unexpected fixture version')
    K.require(isinstance(value['cases'], dict) and set(value['cases']) == set(CASES),
              'Missing or unexpected certificate case')
    K.require(isinstance(value['core'], dict), 'Malformed core fixture')
    return value


def core_result(data, cases):
    result = {'kernel': {key: {'terms': [len(p) for p in data[key]],
        'degrees': [list(map(max, zip(*p))) for p in data[key]],
        'sha256': K.digest(data[key])} for key in ('E', 'O', 'G')},
        'definition_controls': V.definition_controls(data),
        'angular_controls': V.angular_controls(data),
        'reference_regression': V.reference_regression(data),
        'normalization_controls': V.normalization_controls(),
        'stability': S.derive(cases)}
    # Positive expected records must never replace exact validation.
    changed = json.loads(json.dumps(result))
    changed['normalization_controls']['scale_exponent'] = 18
    try:
        compare(result, changed, 'deliberately changed core')
    except ArithmeticError:
        pass
    else:
        raise ArithmeticError('Changed whole-fixture control accepted')
    missing = json.loads(json.dumps(result))
    del missing['kernel']
    try:
        compare(result, missing, 'deliberately missing core field')
    except ArithmeticError:
        pass
    else:
        raise ArithmeticError('Missing whole-fixture control accepted')
    result['whole_fixture_rejection_controls'] = 2
    return result


def case_result(data, name):
    key, chart = name.split('-')
    raw, removed = K.angular_control(data, key)
    mapped, factor, radius_degree = C.cube(raw, chart)
    controls = V.cube_controls(data, raw, removed, mapped, factor,
                               radius_degree, key, chart)
    values, denominator, degrees = C.bernstein(mapped)
    C.inverse_identity(values, denominator, degrees, mapped)
    K.require(len(values) == prod(d+1 for d in degrees), 'Incomplete dense tensor')
    K.require(denominator > 0 and factor > 0, 'Nonpositive scale or denominator')
    K.require(all(v >= 0 for v in values), 'Negative Bernstein certificate coefficient')
    shape = [d+1 for d in degrees]
    stride = [prod(shape[j+1:]) for j in range(4)]
    zeros = [tuple((index//stride[j]) % shape[j] for j in range(4))
             for index, value in enumerate(values) if value == 0]
    all_zeros_on_b1 = all(e[0] == degrees[0] for e in zeros)
    b0_positive = all(e[0] > 0 for e in zeros)
    if key == 'E3':
        K.require(all_zeros_on_b1, 'Even angular endpoint lost interior strictness')
    if key == 'G6':
        K.require(b0_positive, 'Gram angular endpoint lost its positive b0 slice')
        K.require(degrees[0] == 72 and min(e[0] for e in zeros) >= 71,
                  'Gram endpoint lost its quadratic-margin positive slices')
    record = {'key': key, 'chart': chart, 'interval': ['7/8', '1'],
        'count': len(values), 'negative': 0, 'zero': len(zeros),
        'positive': len(values)-len(zeros), 'all_zeros_on_b1': all_zeros_on_b1,
        'degrees': list(degrees), 'radius_clear': radius_degree,
        'positive_scale': str(factor), 'minimum': str(F(min(values), denominator)/factor),
        'minimum_positive': str(F(min(v for v in values if v > 0), denominator)/factor),
        'polynomial_hash': hashlib.sha256(json.dumps(
            [[list(e), str(v)] for e, v in sorted(mapped.items())], separators=(',', ':')).encode()).hexdigest(),
        'tensor_hash': hashlib.sha256(json.dumps(
            [str(F(v, denominator)) for v in values], separators=(',', ':')).encode()).hexdigest(),
        'zero_hash': hashlib.sha256(json.dumps(zeros, separators=(',', ':')).encode()).hexdigest()}
    if key == 'G6':
        record['minimum_zero_b_index'] = min((e[0] for e in zeros), default=degrees[0]+1)
        record['all_b0_coefficients_positive'] = b0_positive
    return {'certificate': record, 'cube_controls': controls}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--core-only', action='store_true')
    group.add_argument('--case', choices=CASES)
    parser.add_argument('--check', type=Path, default=DIRECTORY/'expected.json')
    parser.add_argument('--case-timeout', type=int, default=180,
                        help='sequential child timeout; incomplete runs prove nothing')
    args = parser.parse_args()
    K.require(args.case_timeout > 0, 'Nonpositive case timeout')
    for name in THREADS:
        os.environ[name] = '1'
    fixture = load_fixture(args.check)
    start = time.monotonic()
    data = K.build()
    if args.case:
        result = case_result(data, args.case)
        compare(result, fixture['cases'][args.case], args.case)
        output = {'verified': True, 'case': args.case, 'result': result}
    else:
        core = core_result(data, fixture['cases'])
        compare(core, fixture['core'], 'core')
        if args.core_only:
            output = {'verified': True, 'core': core}
        else:
            # Fresh child processes bound memory; never run cases concurrently.
            completed, signs, peak = [], 0, 0
            for name in CASES:
                command = [sys.executable, '-I', '-B']
                if sys.flags.optimize:
                    command.append('-O')
                command += [str(Path(__file__).resolve()), '--case', name,
                            '--check', str(args.check.resolve())]
                run = subprocess.run(command, capture_output=True, text=True,
                                     timeout=args.case_timeout, env=os.environ.copy())
                if run.returncode:
                    raise ArithmeticError('Incomplete/failed case '+name+': '+run.stderr[-2000:])
                row = json.loads(run.stdout)
                K.require(row.get('verified') is True and row.get('case') == name,
                          'Unexpected child result')
                compare(row['result'], fixture['cases'][name], 'whole child '+name)
                completed.append(name)
                signs += row['result']['certificate']['count']
                peak = max(peak, row['peak_rss_kib'])
                print('verified '+name, file=sys.stderr, flush=True)
            K.require(tuple(completed) == CASES and signs == 4884500, 'Incomplete case union')
            output = {'verified': True, 'complete_cases': len(completed),
                      'complete_tensor_signs': signs, 'full_inverse_identities': len(completed),
                      'case_fixture_sha256': V.digest(fixture['cases']),
                      'core_sha256': V.digest(core), 'maximum_child_peak_rss_kib': peak}
    output.update({'agent': 'six-sendov-1', 'role': 'researcher',
                   'python': sys.version.split()[0], 'threads': 1,
                   'elapsed_seconds': time.monotonic()-start,
                   'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})
    print(json.dumps(output, sort_keys=True))


if __name__ == '__main__':
    main()
