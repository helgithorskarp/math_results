"""Serial cold reproduction of ONE arbitrary-depth conditional size44 exclusion.

Generated arrays and logs stay in ignored work/. Each mathematical child has
an unchanged55-second external guard. Any failure is incomplete work, never
mathematical nonexistence. Set RESEARCH_OPERATIONS_STATE in a monitored campaign.
"""
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

from controls import operations_allow

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work'
ENV = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
           MKL_NUM_THREADS='1', BLIS_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1',
           PYTHONHASHSEED='0')
STAGES = []


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def read(name):
    return json.loads((WORK / name).read_text())


def write(name, value):
    (WORK / name).write_text(json.dumps(value, indent=2)+'\n')


def paired(name):
    normal = read(name+'.json')
    optimized = read(name+'-O.json')
    need(normal['finite'] == optimized['finite'] and
         digest(normal['finite']) == normal['finite_sha256'] == optimized['finite_sha256'],
         'Normal/O entry-level finite binding differs: '+name)
    return normal


def child(script, *args, optimized=False):
    operations_allow()
    label = str(len(STAGES)).zfill(3)+'-'+script.replace('/', '-')+('-O' if optimized else '')
    command = [sys.executable]+(['-O'] if optimized else [])+[str(ROOT / script), *map(str, args)]
    start = time.monotonic()
    try:
        result = subprocess.run(command, env=ENV, capture_output=True, text=True, timeout=55)
    except subprocess.TimeoutExpired as error:
        raise ValueError('Incomplete55s child; no exclusion: '+label) from error
    (WORK / (label+'.log')).write_text(result.stdout+result.stderr)
    need(result.returncode == 0, 'Incomplete/failed child; inspect '+label+'.log; no exclusion')
    STAGES.append({'script':script, 'args':list(args), 'optimized':optimized,
                   'seconds':time.monotonic()-start, 'returncode':result.returncode})
    write('run-stages.json', STAGES)
    print(json.dumps({'child':len(STAGES), **STAGES[-1]}), flush=True)
    return result.stdout


def original_and_preparations():
    child('prior/base.py')
    child('prior/verify_base.py')
    child('prior/verify_base.py', optimized=True)
    child('cover.py')
    child('verify_original.py')
    child('verify_original.py', optimized=True)
    original = paired('original-checked')
    need(original['finite']['scalar_cache_sha256'] ==
         '105a51aade5e8409ba8c7487946c2fab80f819518d4e3758d2de503d6e90ae01',
         'Clean original-domain reconstruction differs')
    child('preparations.py', 1, 2)
    child('verify_preparations.py', 1, 2)
    child('verify_preparations.py', 1, 2, optimized=True)
    prep = paired('checked01')
    need(prep['finite']['full_functions'] == 6214, 'Incomplete selected preparation cover')
    for suffix in ('', '-O'):
        shutil.copyfile(WORK / ('checked01'+suffix+'.json'), WORK / ('fresh-prep-checked'+suffix+'.json'))
    child('screen_cuts.py', 1, 2)
    child('verify_cuts.py', 1, 2)
    child('verify_cuts.py', 1, 2, optimized=True)
    cuts = paired('free-cut-independent-01-02')
    need(cuts['finite']['census']['INHERITED_INDEPENDENTLY_CHECKED_MINIMUM_LOCK'] == 2339 and
         cuts['finite']['census']['NO_CUT_FOUND_RETAINED_WITHOUT_FEASIBILITY_ASSERTION'] == 3875,
         'Complete selected retained cover differs')
    for suffix in ('', '-O'):
        shutil.copyfile(WORK / ('free-cut-independent-01-02'+suffix+'.json'), WORK / ('fresh-cuts-checked'+suffix+'.json'))


def fronts_and_quotient():
    ids = read('cuts01.json')['retained_function_ids']
    rows = []
    for first in range(0, len(ids), 128):
        last = min(first+128, len(ids))
        child('fronts.py', 1, first, last)
        child('verify_fronts.py', 1, first, last)
        child('verify_fronts.py', 1, first, last, optimized=True)
        producer = read(f'fronts01-{first:05}-{last:05}.json')
        check = paired(f'check01-{first:05}-{last:05}')
        need(check['finite']['producer_front_sha256'] == producer['finite_sha256'] and
             producer['retained_function_ids'] == ids[first:last], 'Front partition differs')
        rows.append({'retained_interval':[first,last], 'front_finite_sha256':producer['finite_sha256'],
                     'check_finite_sha256':check['finite_sha256']})
    write('branch01-front-cover-summary.json', {'intervals':rows, 'retained_functions':len(ids)})
    child('catalogue.py', 'build')
    child('catalogue.py', 'check')
    child('catalogue.py', 'check', optimized=True)
    check = paired('branch01-catalogue-checked')
    need(check['finite']['source_targets_replayed'] == 41562 and
         check['finite']['representative_targets'] == 17682, 'Whole-image quotient incomplete')


def constant_partition():
    catalogue = read('branch01-catalogue.json')
    count = len(catalogue['representatives'])
    rows, inconclusive = [], []
    for first in range(0, count, 1000):
        last = min(first+1000, count)
        child('select_constant.py', 'catalogue', first, last)
        child('verify_constant.py', 'catalogue', first, last, 0, last-first)
        child('verify_constant.py', 'catalogue', first, last, 0, last-first, optimized=True)
        producer = read(f'constant-catalogue01-{first:05}-{last:05}.json')
        check = paired(f'constant-catalogue-check01-{first:05}-{last:05}-00000-{last-first:05}')
        need(check['finite']['complete_case_certificate_sha256'] == producer['cases_sha256'],
             'Constant slice not bound to all supplied original cases')
        inconclusive.extend(producer['finite']['inconclusive_front_indices'])
        rows.append({'catalogue_slice':[first,last], 'producer_finite_sha256':producer['finite_sha256'],
                     'check_finite_sha256':check['finite_sha256'], 'census':check['finite']['census'],
                     'metrics':check['finite']['metrics'], 'minimum_selected_mass':check['finite']['minimum_selected_mass']})
    write('branch01-constant-summary.json', {'agent':'six-sorting-1', 'role':'researcher',
          'representative_targets':count, 'catalogue_finite_sha256':catalogue['finite_sha256'],
          'slices':rows, 'inconclusive_catalogue_indices':inconclusive, 'normal_O_finite_equal':True})


def inner_partition():
    residual = read('branch01-constant-summary.json')['inconclusive_catalogue_indices']
    need(len(residual) == 108, 'Exact constant-bound complement differs')
    rows, inconclusive = [], []
    for first in range(0, len(residual), 32):
        last = min(first+32, len(residual))
        child('select_inner.py', first, last)
        child('verify_inner.py', first, last)
        child('verify_inner.py', first, last, optimized=True)
        producer = read(f'inner01-{first:05}-{last:05}.json')
        check = paired(f'inner-checked01-{first:05}-{last:05}')
        need(check['finite']['complete_producer_cases_sha256'] == producer['finite']['cases_sha256'],
             'Inner slice not bound to complete original records')
        inconclusive.extend(check['finite']['inconclusive_catalogue_indices'])
        rows.append({'residual_slice':[first,last], 'producer_finite_sha256':producer['finite_sha256'],
                     'check_finite_sha256':check['finite_sha256'], 'census':check['finite']['census'],
                     'metrics':check['finite']['metrics'], 'minimum_selected_mass':check['finite']['minimum_selected_mass']})
    need(not inconclusive, 'Inner residuals remain open; no whole-route exclusion')
    write('branch01-inner-summary.json', {'agent':'six-sorting-1', 'role':'researcher',
          'complete_residual_indices':residual, 'slices':rows,
          'inconclusive_catalogue_indices':inconclusive, 'normal_O_finite_equal':True})


def controls_and_freeze():
    # The first checked catalogue slice is also used for semantic damage.
    # No private pilot kernel-classification input is required.
    index = next(i for i, case in enumerate(read('constant-catalogue01-00000-01000.json')['cases'])
                 if case['constant16_exceeds44'])
    child('verify_constant.py', 'catalogue', 0, 1000, index, index+1)
    child('verify_constant.py', 'catalogue', 0, 1000, index, index+1, optimized=True)
    child('check_damage.py')
    child('freeze.py')
    normal = json.loads((ROOT / 'certificate.json').read_text())
    child('freeze.py', optimized=True)
    optimized = json.loads((ROOT / 'certificate.json').read_text())
    need(normal['finite'] == optimized['finite'] and
         digest(normal['finite']) == normal['finite_sha256'] == optimized['finite_sha256'],
         'Clean final finite certificate differs between modes')
    write('frozen-normal.json', normal)
    write('frozen-optimized.json', optimized)
    return optimized


def main():
    operations_allow()
    WORK.mkdir(exist_ok=True)
    need(not any(WORK.iterdir()), 'Cold replay requires a fresh work directory; preserve old output rather than deleting it')
    start = time.monotonic()
    phases = []
    for name, function in [('original_and_preparations', original_and_preparations),
                           ('fronts_and_quotient', fronts_and_quotient),
                           ('constant_partition', constant_partition),
                           ('inner_partition', inner_partition)]:
        began = time.monotonic()
        function()
        phases.append({'phase':name, 'seconds':time.monotonic()-began})
        print(json.dumps({'complete_phase':name, 'seconds':phases[-1]['seconds']}), flush=True)
    began = time.monotonic()
    certificate = controls_and_freeze()
    phases.append({'phase':'controls_and_freeze', 'seconds':time.monotonic()-began})
    checks = {'agent':'six-sorting-1', 'role':'researcher', 'status':'CLEAN_PORTABLE_ONE_ROUTE_REPRODUCTION_COMPLETE',
              'python':sys.version.split()[0], 'stdlib_only':True, 'serial_math_children':len(STAGES),
              'native_threads':1, 'process_scope':'unchanged1CPU/2GiB', 'child_external_guard_seconds':55,
              'preparation_internal_guard_seconds':5, 'preparation_state_guard':20000,
              'other_internal_guard_seconds':45, 'normal_optimized_finite_equal':True,
              'private_baseline_finite_sha256':certificate['private_baseline_finite_sha256'],
              'certificate_finite_sha256':certificate['finite_sha256'], 'seconds':time.monotonic()-start,
              'phases':phases, 'four_semantic_damages_normal_optimized_reject':True,
              'generated_arrays_published':False, 'external_person_review_claimed':False}
    (ROOT / 'checks.json').write_text(json.dumps(checks, indent=2)+'\n')
    print(json.dumps(checks, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
