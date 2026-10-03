"""One complete <=128-preparation constant-first interval, serial bounded jobs.

Scalar replay covers every positive proposal; sufficient misses stay open.
Unchanged already verified full preparation data are read from the private pilot.
"""
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from controls import operations_allow
from bindings import selected_offsets

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work'
PILOT = ROOT.parent / 'disjoint_two_prior_56_710_pilot'
ENV = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
           MKL_NUM_THREADS='1', BLIS_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1',
           VECLIB_MAXIMUM_THREADS='1', PYTHONHASHSEED='0')
STAGES = []


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def read(name):
    return json.loads((WORK / name).read_text())


def progress(status, active=None):
    (ROOT / 'WORK_IN_PROGRESS.json').write_text(json.dumps({
        'agent': 'six-sorting-1', 'role': 'researcher', 'status': status,
        'retained_interval': [FIRST, LAST], 'current_serial_job': active,
        'stages': STAGES, 'whole_branch_exclusion_claimed': False,
        'new_source_publication': False, 'new_graph_submission': False,
    }, indent=2)+'\n')


def child(script, *args, optimized=False):
    operations_allow()
    label = f'{FIRST:05}-{LAST:05}-{len(STAGES):02}-'+script+('-O' if optimized else '')
    command = [sys.executable]+(['-O'] if optimized else [])+[str(ROOT/script), *map(str, args)]
    progress('ACTIVE_SERIAL_SLICE_CHILD', {'script': script, 'args': list(args), 'optimized': optimized})
    started = time.monotonic()
    result = subprocess.run(command, env=ENV, capture_output=True, text=True, timeout=55)
    (WORK / (label+'.log')).write_text(result.stdout+result.stderr)
    need(result.returncode == 0, 'Incomplete or failed child; no new exclusion: '+label)
    STAGES.append({'script': script, 'args': list(args), 'optimized': optimized,
                   'seconds': time.monotonic()-started, 'returncode': result.returncode})
    progress('SERIAL_SLICE_CHILD_COMPLETE')


def paired(base):
    n, o = read(base+'.json'), read(base+'-O.json')
    need(n['finite'] == o['finite'] and digest(n['finite']) ==
         n['finite_sha256'] == o['finite_sha256'], 'Normal/O complete finite mismatch: '+base)
    return n


def verified_inputs():
    from bindings import prerequisites
    from inputs import load
    prerequisites()
    return load('cuts')


def main():
    operations_allow()
    started = time.monotonic()
    need(0 <= FIRST < LAST and LAST-FIRST <= 128, 'Require explicit <=128 preparation interval')
    cuts = verified_inputs()
    offsets, previous, universal, universal_ref = selected_offsets(FIRST, LAST)
    try:
        child('fronts.py', 2, FIRST, LAST)
        child('verify_fronts.py', 2, FIRST, LAST)
        child('verify_fronts.py', 2, FIRST, LAST, optimized=True)
        front = read(f'fronts02-{FIRST:05}-{LAST:05}.json')
        check = paired(f'check02-{FIRST:05}-{LAST:05}')
        need(front['retained_function_ids'] == [cuts['retained_function_ids'][i] for i in offsets] ==
             check['finite']['retained_function_ids'] and check['finite']['producer_front_sha256'] ==
             front['finite_sha256'], 'Complete selected front binding differs')
        classifications = [{'front_index': i, 'prefix_sha256': row['prefix_sha256'],
                            'status': 'NO_IMPORTED_NEGATIVE_ASSUMED_DIRECT_CONSTANT_FIRST'}
                           for i, row in enumerate(front['survivors'])]
        kernel = {'agent': 'six-sorting-1', 'role': 'researcher',
                  'status': 'ALL_ACTUAL_FRONTS_PRESERVED_FOR_DIRECT_ORIGINAL_DOMAIN_BOUNDS',
                  'finite': {'producer_front_sha256': front['finite_sha256'],
                             'classifications_sha256': digest(classifications),
                             'imported_negative_count': 0}, 'classifications': classifications}
        (WORK / f'kernels02-{FIRST:05}-{LAST:05}.json').write_text(json.dumps(kernel, indent=2)+'\n')
        child('select_constant.py', 2, FIRST, LAST)
        proposal = read(f'constant02-{FIRST:05}-{LAST:05}.json')
        cases = proposal['cases']
        need([r['front_index'] for r in cases] == list(range(len(front['survivors']))) and
             digest(cases) == proposal['cases_sha256'], 'Entire actual front candidate partition differs')
        records, census, metrics = [], Counter(), Counter()
        positive = [r['front_index'] for r in cases if r['constant16_exceeds44']]
        misses = [r['front_index'] for r in cases if not r['constant16_exceeds44']]
        minimum = None
        for first in range(0, len(cases), 1000):
            last = min(first+1000, len(cases))
            child('verify_constant.py', 2, FIRST, LAST, first, last)
            child('verify_constant.py', 2, FIRST, LAST, first, last, optimized=True)
            checked = paired(f'constant-check02-{FIRST:05}-{LAST:05}-{first:05}-{last:05}')
            need(checked['finite']['case_slice'] == [first, last] and
                 checked['finite']['complete_case_certificate_sha256'] == proposal['cases_sha256'] and
                 checked['finite']['complete_front_cover_sha256'] == front['finite_sha256'],
                 'Positive scalar certificate slice not actually bound')
            census.update(checked['finite']['census'])
            metrics.update(checked['finite']['metrics'])
            m = checked['finite']['minimum_selected_mass']
            if m is not None:
                minimum = m if minimum is None else min(m, minimum)
            records.append({'case_interval': [first, last], 'finite_sha256': checked['finite_sha256']})
        need(census['independently_constant16_excluded_cases'] == len(positive) and
             census['inconclusive_preserved_open'] == len(misses) and
             (minimum is None or minimum > (1 << 44)), 'Incomplete actual negative/open partition')
        finite = {'branch_index': 2, 'HIGH_word': [[5, 6], [7, 10]],
                  'retained_interval': [FIRST, LAST], 'processed_previous_open_offsets': offsets,
                  'public_universal_graph_ref': universal_ref,
                  'retained_function_ids_sha256': digest(front['retained_function_ids']),
                  'front_census': front['census'], 'front_scalar_metrics_normal': check['finite']['metrics'],
                  'producer_front_finite_sha256': front['finite_sha256'],
                  'scalar_front_finite_sha256': check['finite_sha256'],
                  'complete_constant_cases_sha256': proposal['cases_sha256'],
                  'constant_scalar_slices': records, 'constant_scalar_census': dict(census),
                  'constant_scalar_metrics_normal': dict(metrics),
                  'minimum_positive_selected_mass': minimum,
                  'actual_negatives': len(positive), 'unresolved_sufficient_misses': len(misses),
                  'negative_front_indices_sha256': digest(positive),
                  'unresolved_front_indices': misses,
                  'remaining_gate_budgets': check['finite']['remaining_gate_budgets'],
                  'normal_O_entire_finite_records_equal': True,
                  'imported_negative_count': 0,
                  'entire_selected_original_open_function_interval_excluded': not misses}
        result = {'agent': 'six-sorting-1', 'role': 'researcher',
                  'status': 'COMPLETE_PRIVATE_CONSTANT_FIRST_NECESSARY_FRONT_SLICE',
                  'finite': finite, 'finite_sha256': digest(finite), 'stages': STAGES,
                  'seconds': time.monotonic()-started,
                  'maximum_recorded_child_rss_kib': max(check['maximum_rss_kib'], proposal['maximum_rss_kib']),
                  'external_person_review_claimed': False, 'cold_source_only_run_claimed': False,
                  'scope': 'Only this exact preparation interval; every sufficient miss remains open.'}
        (WORK/f'slice-complete02-{FIRST:05}-{LAST:05}.json').write_text(json.dumps(result, indent=2)+'\n')
        progress('SLICE_COMPLETE_IDLE_PRESERVING_ANY_MISSES')
        print(json.dumps({k: v for k, v in result.items() if k != 'stages'}), flush=True)
    except BaseException:
        progress('INCOMPLETE_SLICE_NO_NEW_NEGATIVE_CONCLUSION')
        raise


if __name__ == '__main__':
    FIRST, LAST = map(int, sys.argv[1:3])
    main()
