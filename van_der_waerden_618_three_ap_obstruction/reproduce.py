"""Reconstruct compact AP proofs and check the forbidden-domain orbit."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import resource
import sys
import tempfile
import time

from check_direct_phase_core import check
from phase_core_symmetry import analyze
from rup_controls import controls as rup_controls

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def controls(builddir):
    original = json.loads((ROOT / 'certificate.json').read_text())
    variants = []
    def mutation(name, mutate):
        d = copy.deepcopy(original)
        mutate(d)
        # Hashes bind reference bytes, while these controls exercise semantics.
        d.pop('CNF_sha256', None)
        d.pop('RUP_proof_sha256', None)
        variants.append((name, d))
    mutation('zero difference', lambda d: d['rows'][0]['AP'].update(difference=0))
    mutation('outside prefix', lambda d: d['rows'][0]['AP'].update(start=3704))
    mutation('different AP', lambda d: d['rows'][0]['AP'].update(start=306))
    mutation('wrong projected unit', lambda d: d['rows'][0].update(projected_clause=[-272]))
    mutation('omitted constrained residue', lambda d: d['frozen_residues'].remove(2))
    mutation('unused constrained residue', lambda d: d['frozen_residues'].insert(0, 0))
    mutation('bad RUP hint', lambda d: d.update(RUP_proof_text='4 0 1 2 99 0\n'))
    mutation('unsupported RAT hint', lambda d: d.update(RUP_proof_text='4 0 1 2 -3 0\n'))
    mutation('missing empty conclusion', lambda d: d.update(RUP_proof_text='4 272 0 1 0\n'))
    mutation('insufficient conflict hints', lambda d: d.update(RUP_proof_text='4 0 1 2 0\n'))
    rejected = []
    for number, (name, data) in enumerate(variants):
        path = builddir / f'negative-{number}.json'
        path.write_text(json.dumps(data) + '\n')
        try:
            check(path, builddir / f'negative-{number}')
        except (ValueError, KeyError, IndexError, TypeError):
            rejected.append(name)
        else:
            raise RuntimeError(f'Invalid certificate accepted: {name}')
    return {'invalid_direct_certificates_rejected': len(rejected), 'cases': rejected}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--builddir', type=Path, default=ROOT / 'build')
    args = ap.parse_args()
    began = time.monotonic()
    require(__debug__, 'Run Python with assertions enabled')
    for key in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS']:
        os.environ[key] = '1'
    args.builddir.mkdir(parents=True, exist_ok=True)
    tempfile.tempdir = str(args.builddir)
    primary = check(ROOT / 'certificate.json', args.builddir / 'primary')
    secondary = check(ROOT / 'secondary.json', args.builddir / 'secondary')
    orbit = analyze(primary['allowed_phase_sets'])
    checks = controls(args.builddir)
    proof_controls = rup_controls()
    expected = json.loads((ROOT / 'expected.json').read_text())
    for label, result in [('primary', primary), ('secondary', secondary)]:
        wanted = expected[label]
        for key in ['frozen_columns', 'arbitrary_phase_columns', 'AP_premises', 'direct_seven_term_truth_cases']:
            require(result[key] == wanted[key], f'{label}: different {key}')
        for key in ['cnf_sha256', 'proof_sha256', 'checked_additions', 'propagation_hints_checked']:
            require(result['RUP_verdict'][key] == wanted[key], f'{label}: different {key}')
    require(all(len(p) == 3 for p in primary['allowed_phase_sets'].values()), 'different permissive domain sizes')
    require(primary['excluded_phase_family_size'] == 3 ** 16 * 6 ** 87, 'different primary family size')
    require(orbit['distinct_transformed_domains'] == expected['orbit']['distinct_transformed_domains'], 'different orbit size')
    require(orbit['canonical_orbit_stream_sha256'] == expected['orbit']['canonical_orbit_stream_sha256'], 'different complete orbit stream')
    result = {'agent': 'six-vdw-1', 'role': 'researcher', 'status': 'VERIFIED_THREE_AP_OBSTRUCTION_AND_ORBIT',
        'Python': sys.version, 'primary': primary, 'secondary': secondary, 'orbit': orbit,
        'negative_controls': checks, 'RUP_controls': proof_controls, 'threads': 1,
        'simultaneous_CPU_jobs': 1, 'seconds': time.monotonic() - began,
        'maxrss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'no_length3704_witness': True, 'no_new_W_bound': True,
        'source_hashes': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.iterdir()
                          if p.is_file() and p.suffix in ['.py', '.json', '.md']}}
    require(result['seconds'] < 30, 'Reproduction time budget exceeded')
    (args.builddir / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ['primary', 'secondary', 'source_hashes']}, indent=2))


if __name__ == '__main__':
    main()
