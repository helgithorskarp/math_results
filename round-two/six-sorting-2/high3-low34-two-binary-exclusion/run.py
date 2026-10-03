"""Bounded serial source-only proof replay, Python standard library only."""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent


def need(ok, why):
    if not ok:
        raise ValueError(why)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=('normal', 'optimized', 'both'), default='both')
    args = parser.parse_args()
    env = dict(os.environ)
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS'):
        env[name] = '1'
    started = time.monotonic()
    generated = ROOT / 'generated'
    generated.mkdir(exist_ok=True)
    progress, outcomes = [], []

    def child(command, label):
        before = time.monotonic()
        try:
            result = subprocess.run(command, capture_output=True, text=True, env=env, timeout=45)
        except subprocess.TimeoutExpired:
            raise SystemExit('45s child guard: incomplete, no exclusion from this run')
        (generated / (label + '.stdout')).write_text(result.stdout)
        (generated / (label + '.stderr')).write_text(result.stderr)
        progress.append({'stage': label, 'exit_code': result.returncode, 'seconds': time.monotonic() - before})
        (generated / 'progress.json').write_text(json.dumps({'complete': False, 'stages': progress}, indent=2) + '\n')
        print(json.dumps(progress[-1]), flush=True)
        need(result.returncode == 0, 'failed child: preserve outputs, no exclusion from this run')

    modes = ('normal', 'optimized') if args.mode == 'both' else (args.mode,)
    ranges = [(a, a + 16) for a in range(0, 96, 16)] + [(96, 113)]
    for mode in modes:
        command = [sys.executable] + (['-O'] if mode == 'optimized' else [])
        child(command + [str(ROOT / 'cover.py')], 'cover-' + mode)
        cover = json.loads((generated / 'cover.json').read_text())
        slices = []
        for a, b in ranges:
            out = generated / f'proof-{mode}-{a}-{b}.json'
            child(command + [str(ROOT / 'verify.py'), '--offset', str(a), '--cases', str(b - a),
                             '--output', str(out)], f'proof-{mode}-{a}-{b}')
            slices.append(json.loads(out.read_text()))
        need([s['mathematical']['function_range'] for s in slices] == [list(r) for r in ranges],
             'complete113 slice union differs')
        counts, assignments, bindings, controls = Counter(), Counter(), [], []
        for s in slices:
            m = s['mathematical']
            counts.update(m['kind_counts'])
            assignments.update(m['numeric_assignment_counts'])
            bindings.extend(m['all_actual_negative_binding_records_and_rows'])
            controls.append([m['function_range'], m['intended_rejections']])
        need(len(bindings) == 1030 and sum(s['mathematical']['full_tail_alternatives'] for s in slices) == 2034,
             'whole negative obligation accounting differs')
        math = {'entire_cover': cover['mathematical'], 'all_slice_mathematical_records': [s['mathematical'] for s in slices],
                'entire_certificate_sha256': hashlib.sha256((ROOT / 'certificate.json').read_bytes()).hexdigest(),
                'functions': 113, 'actual_negative_bindings': len(bindings), 'full_tail_alternatives': 2034,
                'kind_counts': dict(counts), 'numeric_assignment_counts': dict(assignments),
                'intended_rejections_by_slice': controls, 'complete_scoped_two_binary_exclusion': True,
                'full_LOW34_branch_exclusion': False, 'global_size44_exclusion': False}
        result = {'agent': 'six-sorting-2', 'role': 'researcher', 'mode': mode, 'mathematical': math,
                  'entire_mathematical_record_sha256': digest(math),
                  'maximum_scalar_seconds': max(s['seconds'] for s in slices),
                  'maximum_scalar_rss_kib': max(s['maximum_rss_kib'] for s in slices),
                  'independent_person_review': 'pending', 'formalization': 'pending'}
        (generated / ('complete-' + mode + '.json')).write_text(json.dumps(result, separators=(',', ':')) + '\n')
        outcomes.append(result)
    if len(outcomes) == 2:
        need(outcomes[0]['mathematical'] == outcomes[1]['mathematical'], 'ENTIRE normal/O mathematical records differ')
    final = {'agent': 'six-sorting-2', 'role': 'researcher', 'complete': True, 'modes': list(modes),
             'functions': 113, 'negative_bindings': 1030, 'full_tail_alternatives': 2034,
             'entire_mathematical_record_sha256': outcomes[0]['entire_mathematical_record_sha256'],
             'whole_normal_optimized_record_equality': len(outcomes) == 2,
             'seconds': time.monotonic() - started, 'stages': progress,
             'scope': 'Only stipulated literal LOW34/no-HIGH3-singleton/exactly-two-binary route; arbitrary original preparation words/suffixdepth.'}
    (generated / 'progress.json').write_text(json.dumps(final, indent=2) + '\n')
    print(json.dumps({k: v for k, v in final.items() if k != 'stages'}), flush=True)


if __name__ == '__main__':
    main()
