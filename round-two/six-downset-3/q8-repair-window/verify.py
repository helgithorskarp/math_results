"""Serial standard-library replay, fixed 60s per mathematical phase.

--record PATH saves the regenerable full record outside this source packet.
An incomplete phase never supplies a mathematical conclusion.
"""
from pathlib import Path
import os, json, sys, subprocess, argparse, hashlib
import inputs
from literal import require
from exact import digest
from geometry import window

PHASES = ('lower', 'upper', 'duals', 'radical', 'whole', 'controls')


def assemble(records):
    native = records['duals']; radical = records['radical']
    for embedding in radical['embeddings']:
        for name in ('U0_pairing', 'Delta_pairing', 'R_pairing', 'lower_slope',
                     'upper_slope', 'outside_Delta_action'):
            require(embedding[name] == native[name], 'original native/radical disagreement')
    require(native['kappa_strict_necessary_bound'] == radical['kappa_strict_necessary_bound'],
            'separate strict necessary bound disagreement')
    geometry = window(records['lower'], records['upper'])
    result = {'agent': 'six-downset-3', 'role': 'researcher',
              'claim_status': 'author-checked exact certificate and ordinary unformalized bridges; independent review pending',
              'phase_records': records, 'zero_kappa_geometry': geometry,
              'complete_repair_projection': 'closed [tau_minus,tau_plus] over every real kappa,t',
              'greatest_rank_repair_projection': 'open (tau_minus,tau_plus); every interior t has a positive-kappa interval',
              'endpoint_fibers': 'kappa=0 only; whole lower and upper ranks87,87',
              'negative_kappa_excluded': True, 'positive_kappa_dual_bands_strict': True,
              'both_arithmetic_representations_agree': True,
              'scope': 'q8,k3 declared affine table plus four-edge scalar repair only; H/I remain open'}
    result['record_sha256'] = digest(result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--record', type=Path)
    parser.add_argument('--make-expected', action='store_true',
                        help='create the initial compact expected phase hashes; refuses to overwrite')
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent
    env = dict(os.environ)
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        env[name] = '1'
    records = {}
    for phase in PHASES:
        cmd = [sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(directory/'task.py'), phase]
        try:
            completed = subprocess.run(cmd, cwd=directory, env=env, text=True,
                                       capture_output=True, timeout=60, check=True)
        except subprocess.TimeoutExpired:
            raise SystemExit('INCOMPLETE: fixed 60s phase limit; no mathematical nonexistence conclusion')
        if completed.stderr:
            raise ValueError('Unexpected replay stderr: '+completed.stderr)
        records[phase] = json.loads(completed.stdout)
    result = assemble(records)
    expected = {'record_sha256': result['record_sha256'],
                'phase_record_sha256': {name: value['record_sha256'] for name, value in records.items()},
                'whole_original_entry_count': 31684, 'damage_count': 14,
                'orbit_count': 17, 'N': 89, 'fixed_phase_seconds': 60}
    target = directory/'EXPECTED.json'
    if args.make_expected:
        if target.exists():
            raise ValueError('Expected evidence already exists: compare instead of overwriting')
        target.write_text(json.dumps(expected, sort_keys=True, indent=2)+'\n')
    require(json.loads(target.read_text()) == expected, 'entire expected mathematical record differs')
    if args.record:
        args.record.write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    print(json.dumps(expected, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
