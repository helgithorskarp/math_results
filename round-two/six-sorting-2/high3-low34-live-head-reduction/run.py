"""Regenerate and separately check the entire live-head reduction twice.

Each child is serial, native threads1, with an unchanged55-second guard.
Timeout/kill/incomplete execution is an operational stop, not an exclusion.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
RUNTIME = ('packed.py', 'numeric.py', 'fixture.json', 'positive45.json', 'generate.py', 'verify.py', 'run.py', '.gitignore')


def need(ok, why):
    if not ok:
        raise ValueError(why)


def main():
    started = time.monotonic()
    out = ROOT / 'generated'
    out.mkdir(exist_ok=True)
    env = dict(os.environ)
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS'):
        env[key] = '1'
    stages = []
    for mode, option in (('normal', []), ('optimized', ['-O'])):
        produced = out / (mode + '-produced.json')
        certificate = out / (mode + '-certificate.json')
        checked = out / (mode + '-checked.json')
        for tool, arguments in (
            ('generate.py', ['--output', str(produced), '--certificate', str(certificate)]),
            ('verify.py', ['--producer', str(produced), '--certificate', str(certificate), '--output', str(checked)]),
        ):
            print('START', mode, tool, flush=True)
            t = time.monotonic()
            result = subprocess.run([sys.executable, *option, str(ROOT / tool), *arguments],
                                    cwd=ROOT, env=env, text=True, capture_output=True, timeout=55)
            need(result.returncode == 0, f'{mode}/{tool} stopped: {result.stderr[-2000:]}')
            stages.append({'mode': mode, 'tool': tool, 'seconds': time.monotonic() - t})
            print('COMPLETE', mode, tool, result.stdout.strip(), flush=True)
    normal = json.loads((out / 'normal-produced.json').read_text())
    optimized = json.loads((out / 'optimized-produced.json').read_text())
    first = json.loads((out / 'normal-checked.json').read_text())
    second = json.loads((out / 'optimized-checked.json').read_text())
    need(normal['mathematical'] == optimized['mathematical'] and first['mathematical'] == second['mathematical'],
         'ENTIRE normal/optimized mathematical records differ')
    certificate = (out / 'normal-certificate.json').read_bytes()
    need(certificate == (out / 'optimized-certificate.json').read_bytes(), 'whole regenerated compact certificates differ')
    if (ROOT / 'certificate.json').exists():
        need(certificate == (ROOT / 'certificate.json').read_bytes(), 'regenerated certificate differs from public compact input')
    summary = {'agent': 'six-sorting-2', 'role': 'researcher', 'status': 'COMPLETE_COLD_CAPABLE_SOURCE_ONLY_REPRODUCTION',
               'python': sys.version.split()[0], 'native_threads': 1, 'mathematical_child_concurrency': 1,
               'per_child_guard_seconds': 55, 'runtime_source_files': {
                   f: hashlib.sha256((ROOT / f).read_bytes()).hexdigest() for f in RUNTIME},
               'entire_producer_mathematical_sha256': normal['entire_mathematical_record_sha256'],
               'entire_separate_checker_mathematical_sha256': first['entire_mathematical_record_sha256'],
               'entire_normal_optimized_records_equal': True,
               'compact_certificate_bytes': len(certificate), 'compact_certificate_sha256': hashlib.sha256(certificate).hexdigest(),
               'forest_counts': normal['mathematical']['forest_counts'], 'live_head_count': normal['mathematical']['live_head_count'],
               'live_head_proof_counts': normal['mathematical']['live_head_proof_counts'],
               'original_ground_assignments_per_mode': first['mathematical']['extra_original_numeric_checks']['numeric_ground_assignments'],
               'positive_sorter_Boolean_inputs_per_mode': 8192,
               'rejected_damages_per_mode': first['mathematical']['controls']['rejected_damage_count'],
               'whole_clamped_identity_assignments_per_mode': 2048, 'balanced_tree_original_replays_per_mode': 6,
               'maximum_child_rss_kib': max(x['maximum_rss_kib'] for x in (normal, optimized, first, second)),
               'stages': stages, 'seconds': time.monotonic() - started,
               'ordinary_bridges': 'written unformalized', 'independent_person_review': 'pending', 'global44_exclusion': False}
    (out / 'checks.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary), flush=True)


if __name__ == '__main__':
    main()
