"""Serial source/cold delivery checks, fixed45s children/60s driver.

Source checks precede all mathematical imports. Existing paid mathematical
records are compared in their entirety. No parent positive reader runs.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import resource
import shutil
import signal
import subprocess
import sys
import time
from reader_binding import check, require


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--out', required=True, type=Path)
    out = parser.parse_args().out.resolve(); out.mkdir(parents=True, exist_ok=True)
    root = Path(__file__).resolve().parent; source = check(root)
    env = os.environ.copy(); native = ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                                     'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS']
    for name in native:
        env[name] = '1'

    def alarm(signum, frame):
        raise TimeoutError('60-second delivery driver cutoff; incomplete verification')

    signal.signal(signal.SIGALRM, alarm); signal.alarm(60)
    started = time.monotonic(); rows = []; positives = []
    cold = out/'cold/q18-transport-weighted-radius'

    def copy_source(target):
        target.mkdir(parents=True, exist_ok=True)
        for row in source['defining_files']:
            shutil.copyfile(root/row['file'], target/row['file'])
        for name in ('SOURCE.json', 'SHA256SUMS'):
            shutil.copyfile(root/name, target/name)
        for row in source['defining_data_dependencies']:
            p = target/row['file']; p.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(root/row['file'], p)
        check(target)

    copy_source(cold)

    def child(target, flags, args, wanted):
        t = time.monotonic()
        p = subprocess.run([sys.executable, '-B', *flags, str(target/'read.py'), *args],
                           env=env, capture_output=True, timeout=45)
        require(p.returncode == wanted, 'unexpected child exit: '+p.stderr.decode())
        row = {'source': str(target), 'flags': flags, 'arguments': args, 'exit_code': p.returncode,
               'wall_seconds': time.monotonic()-t,
               'cumulative_peak_child_RSS_KiB': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
               'whole_stdout_bytes': len(p.stdout),
               'whole_stdout_SHA256': hashlib.sha256(p.stdout).hexdigest()}
        rows.append(row); return p

    for target, label in ((root, 'local'), (cold, 'cold')):
        for flags, mode in (([], 'normal'), (['-O'], 'optimized')):
            p = child(target, flags, [], 0); positives.append(p.stdout)
            (out/(label+'-'+mode+'.json')).write_bytes(p.stdout)
    require(all(raw == positives[0] for raw in positives), 'ENTIRE four local/cold normal/O results differ')
    semantic = []
    for suite, cases in (
        ('transport', ['domain', 'types', 'targets', 'radius', 'floor', 'row', 'multiplicity', 'column', 'energy']),
        ('subset', ['abc-fixed', 'negative-fixed', 'J-column', 'J-support']),
        ('weighted', ['original_triple_indicator_all81', 'all_original_edge_product_census',
                      'weighted_old_cap_lambda_coefficients', 'selected_lambda_affine',
                      'optimized_unnormalized_F_polynomial_low_to_high', 'weighted_root_strict_coarse_cage'])):
        for case in cases:
            for flags in ([], ['-O']):
                p = child(cold, flags, ['--semantic', suite+':'+case, '--scratch', str(out/'semantic')], 0)
                result = json.loads(p.stdout)
                require(result['rejected_exactly_at_designated_gate'], 'no designated semantic rejection')
                semantic.append(result|{'flags': flags})
    faults = []
    source_cases = ['census.py', 'weighted_radius.py', 'weighted_critical.py', 'TRANSPORT.json',
                    'EXPECTED.json', 'SOURCE.json', '../q18-schur-weight-radius/CANDIDATE.json',
                    '../q18-schur-weight-radius/COMPARISON.json']
    for index, name in enumerate(source_cases):
        target = out/('source-fault-'+str(index))/'q18-transport-weighted-radius'
        copy_source(target); path = target/name; path.write_bytes(path.read_bytes()+b'\n')
        marker = out/('marker-'+str(index))
        p = child(target, [], ['--math-import-marker', str(marker)], 1)
        require(p.stderr.decode().rstrip().endswith('ValueError: SOURCE_GATE:'+name)
                and not marker.exists(), 'source fault entered math or wrong gate')
        faults.append({'file': name, 'designated_source_gate': 'SOURCE_GATE:'+name,
                       'math_import_marker_absent': True, 'actual_designated_rejection': True})
    signal.alarm(0)
    receipt = {'actual_agent': 'six-downset-3', 'role': 'researcher', 'interpreter': sys.version,
               'status': 'SOURCE and isolated cold author delivery verification paid',
               'ENTIRE_four_local_cold_normal_optimized_equal': True,
               'whole_result_bytes': len(positives[0]),
               'whole_result_SHA256': hashlib.sha256(positives[0]).hexdigest(),
               'positive_children': 4, 'actual_designated_semantic_rejections': len(semantic),
               'actual_pre_math_source_rejections': len(faults), 'rows': rows,
               'semantic': semantic, 'source_faults': faults,
               'fixed_child_timeout_seconds': 45, 'driver_timeout_seconds': 60,
               'driver_SIGALRM_guard_configured': True, 'native_threads': {name: env[name] for name in native},
               'serial_children': 1, 'total_wall_seconds': time.monotonic()-started,
               'math_code_edits': False, 'independent_review_or_formalization': False,
               'parent_positive_factor_or_program_or_peer_math_executed': False,
               'source_commit': None, 'graph_ref': None}
    (out/'RECEIPT.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps({'whole_result_bytes': receipt['whole_result_bytes'],
                      'whole_result_SHA256': receipt['whole_result_SHA256'],
                      'positive_children': 4, 'semantic_rejections': len(semantic),
                      'pre_math_source_rejections': len(faults),
                      'max_child_seconds': max(row['wall_seconds'] for row in rows),
                      'max_child_RSS_KiB': max(row['cumulative_peak_child_RSS_KiB'] for row in rows),
                      'total_wall_seconds': receipt['total_wall_seconds']}, indent=2))


if __name__ == '__main__':
    main()
