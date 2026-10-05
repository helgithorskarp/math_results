"""Bounded local author verification of the NEW weighted certificate only.

Four positive children and six designated field damages in each of two
modes. Does not provide source-before-import, cold or independent review.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import os
import resource
import signal
import subprocess
import sys
import time


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True, type=Path)
    out = parser.parse_args().out.resolve(); out.mkdir(parents=True, exist_ok=True)
    root = Path(__file__).resolve().parent
    env = os.environ.copy()
    native = ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
              'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS']
    for name in native:
        env[name] = '1'

    def alarm(signum, frame):
        raise TimeoutError('60-second verification driver guard; incomplete verification')

    signal.signal(signal.SIGALRM, alarm); signal.alarm(60)
    started = time.monotonic(); rows = []; positives = []

    def child(flags, args, code):
        t = time.monotonic()
        p = subprocess.run([sys.executable, '-B', *flags, str(root/'weighted_radius.py'), *args],
                           env=env, capture_output=True, timeout=45)
        require(p.returncode == code, 'unexpected child result: '+p.stderr.decode())
        rows.append({'flags': flags, 'arguments': args, 'exit_code': p.returncode,
                     'wall_seconds': time.monotonic()-t,
                     'cumulative_peak_child_RSS_KiB': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                     'whole_stdout_bytes': len(p.stdout),
                     'whole_stdout_SHA256': hashlib.sha256(p.stdout).hexdigest()})
        return p

    for flags, name in (([], 'normal'), (['-O'], 'optimized')):
        p = child(flags, [], 0); positives.append(p.stdout)
        (out/(name+'.json')).write_bytes(p.stdout)
    require(positives[0] == positives[1] == (root/'WEIGHTED.json').read_bytes(),
            'ENTIRE new weighted normal/O and fixed defining certificate agree')
    for flags in ([], ['-O']):
        child(flags, ['--check', str(out/'normal.json')], 0)
    data = json.loads(positives[0]); controls = []
    for field, gate in (
        ('original_triple_indicator_all81', 'certificate original weights'),
        ('all_original_edge_product_census', 'certificate original edge products'),
        ('weighted_old_cap_lambda_coefficients', 'certificate original weighted comparison cap'),
        ('selected_lambda_affine', 'certificate concave lambda optimizer'),
        ('optimized_unnormalized_F_polynomial_low_to_high', 'certificate exact weighted polynomial'),
        ('weighted_root_strict_coarse_cage', 'certificate exact root cage')):
        bad = copy.deepcopy(data)
        if field == 'original_triple_indicator_all81':
            bad[field][0] = 1-bad[field][0]
        elif field == 'all_original_edge_product_census':
            bad[field]['(1+lambda)^2'] = 1
        else:
            bad[field][0] = '0'
        path = out/('damaged-'+field+'.json')
        path.write_text(json.dumps(bad, indent=2)+'\n')
        for flags in ([], ['-O']):
            p = child(flags, ['--check', str(path)], 1)
            require(p.stderr.decode().rstrip().endswith('ValueError: '+gate),
                    'wrong designated rejection gate')
            controls.append({'field': field, 'flags': flags, 'designated_gate': gate,
                             'actual_designated_rejection': True})
    signal.alarm(0)
    result = {'actual_agent': 'six-downset-3', 'role': 'researcher',
              'interpreter': sys.version, 'status': 'LOCAL author verification paid',
              'normal_optimized_whole_result_equal': True,
              'whole_record_bytes': len(positives[0]),
              'whole_record_SHA256': hashlib.sha256(positives[0]).hexdigest(),
              'positive_children': 4, 'new_actual_designated_semantic_rejections': len(controls),
              'rows': rows, 'controls': controls,
              'fixed_child_timeout_seconds': 45, 'driver_timeout_seconds': 60,
              'driver_SIGALRM_guard_configured': True,
              'native_threads': {name: env[name] for name in native},
              'serial_children': 1, 'batch_wall_seconds': time.monotonic()-started,
              'source_before_import_or_isolated_cold_or_remote_gates': 'UNPAID',
              'independent_algorithm_or_review_or_formal_proof': False,
              'source_commit': None, 'graph_ref': None}
    (out/'RECEIPT.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'whole_record_bytes': result['whole_record_bytes'],
                      'whole_record_SHA256': result['whole_record_SHA256'],
                      'positive_children': 4, 'semantic_rejections': len(controls),
                      'max_child_seconds': max(r['wall_seconds'] for r in rows),
                      'max_child_RSS_KiB': max(r['cumulative_peak_child_RSS_KiB'] for r in rows),
                      'batch_wall_seconds': result['batch_wall_seconds']}, indent=2))


if __name__ == '__main__':
    main()
