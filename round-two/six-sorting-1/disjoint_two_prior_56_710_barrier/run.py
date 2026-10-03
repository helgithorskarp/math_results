"""Serial source-only regeneration of the second scoped disjoint HIGH route.

No historical work arrays or negative corpus are read. Mathematical children
have unchanged55s guards; preparation enumeration keeps5s/20000 states.
Completed phases are resumable using exact source/input bindings. A failed
or limited phase remains incomplete, and never proves nonexistence.
"""
from collections import Counter
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from controls import operations_allow
from inputs import checked_finite, digest, need, static_sources

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work'
ENV = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
           MKL_NUM_THREADS='1', BLIS_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1',
           VECLIB_MAXIMUM_THREADS='1', PYTHONHASHSEED='0')
STAGES = []


def read(name):
    return json.loads((WORK / name).read_text())


def write(name, value):
    (WORK / name).write_text(json.dumps(value, indent=2) + '\n')


def pair(name):
    n, o = checked_finite(read(name + '.json')), checked_finite(read(name + '-O.json'))
    need(n['finite'] == o['finite'], 'Entire scalar normal/O records differ: ' + name)
    return n


def progress(status, job=None, **fields):
    value = {'agent': 'six-sorting-1', 'role': 'researcher', 'status': status,
             'current_serial_job': job, 'serial_stages': len(STAGES),
             'cached_external_arrays_read': False, 'negative_corpus_read': False,
             'new_graph_submission': False, 'new_source_publication': False, **fields}
    (ROOT / 'WORK_IN_PROGRESS.json').write_text(json.dumps(value, indent=2) + '\n')


def child(script, *args, optimized=False):
    operations_allow()
    static_sources()
    label = f'{len(STAGES):03}-' + script.replace('/', '-') + ('-O' if optimized else '')
    command = [sys.executable] + (['-O'] if optimized else []) + [str(ROOT / script), *map(str, args)]
    progress('ACTIVE_SERIAL_SOURCE_ONLY_CHILD', {'script': script, 'args': list(args), 'optimized': optimized})
    start = time.monotonic()
    result = subprocess.run(command, env=ENV, capture_output=True, text=True, timeout=55)
    (WORK / (label + '.log')).write_text(result.stdout + result.stderr)
    need(result.returncode == 0, 'Failed/incomplete child; inspect ' + label + '; no new negative conclusion')
    STAGES.append({'script': script, 'args': list(args), 'optimized': optimized,
                   'seconds': time.monotonic() - start, 'returncode': result.returncode})
    write('run-stages.json', STAGES)
    progress('SERIAL_SOURCE_ONLY_CHILD_COMPLETE')
    print(json.dumps({'stage': len(STAGES), **STAGES[-1]}), flush=True)
    return result.stdout


def file_binding(name):
    raw = (ROOT / name).read_bytes()
    return {'path': name, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def original_reserve(universal_already_complete=False):
    start = time.monotonic()
    if not universal_already_complete:
        child('universal/run.py')
    # The public runner writes work/result.json. Its distinct binding step
    # creates the certificate consumed by the standalone transport layer.
    child('universal/freeze.py')
    universal = checked_finite(json.loads((ROOT / 'universal/certificate.json').read_text()))
    need(universal['finite_sha256'] ==
         'a2faef8075c751886b467a5c2095ad79552e712b3b7ca29256715dd86fe6ed4e',
         'Cold conditional-maximum source certificate differs')
    child('prior/base.py')
    base_n = json.loads(child('prior/verify_base.py'))
    base_o = json.loads(child('prior/verify_base.py', optimized=True))
    need(base_n == base_o, 'Entire original base scalar records differ')
    write('base-checked.json', {'finite': base_n, 'finite_sha256': digest(base_n)})
    write('base-checked-O.json', {'finite': base_o, 'finite_sha256': digest(base_o)})
    child('cover.py')
    child('verify_original.py')
    child('verify_original.py', optimized=True)
    original = pair('original-checked')
    need(original['finite']['scalar_cache_sha256'] ==
         '105a51aade5e8409ba8c7487946c2fab80f819518d4e3758d2de503d6e90ae01', 'Cold whole original cache differs')
    child('preparations.py', 2, 3)
    child('verify_preparations.py', 2, 3)
    child('verify_preparations.py', 2, 3, optimized=True)
    preparation = pair('checked02')
    need(preparation['finite_sha256'] ==
         'b710f7d4ebfacf5b079d8f54774dd6c020342b831d831666342eb68d16dbd375',
         'Cold complete8351 full-function cover differs')
    child('screen_cuts.py', 2, 3)
    child('verify_cuts.py', 2, 3)
    child('verify_cuts.py', 2, 3, optimized=True)
    cuts = pair('free-cut-independent-02-03')
    need(cuts['finite_sha256'] ==
         'b9c6d75aa4df209fbec25646a7b0c27935b3210e8cb7fa9f4b677a882b8306ac',
         'Cold complete minimum/free-pivot cover differs')
    write('preparation-bindings.json', {
        'generated_evidence': [file_binding('work/branch02.json'), file_binding('work/cuts02.json')],
        'preparation_scalar_finite_sha256': preparation['finite_sha256'],
        'cut_scalar_finite_sha256': cuts['finite_sha256'], 'entire_normal_O_records_equal': True})
    child('reserve_seed.py')
    child('verify_reserve_seed.py')
    child('verify_reserve_seed.py', optimized=True)
    seed = pair('reserve-seed-checked')
    need(seed['finite_sha256'] ==
         '9db26a3bac45fb4e80eec99fd9eb4325cb9c011d705b1676b26dab05642fc99c',
         'Cold all78 original HIGH cubes/event reserve differs')
    child('reserve_prune.py')
    child('verify_reserve_preps.py')
    child('verify_reserve_preps.py', optimized=True)
    reserve = pair('reserve-preparations-checked')
    need(reserve['finite_sha256'] ==
         '7b415d3f7532e10282a980ce5c5f2635d284dbb93e900b93793a2e66acc67842',
         'Cold all2098 actual original reserve obstructions differ')
    names = {'preparations': 'work/branch02.json', 'cuts': 'work/cuts02.json',
             'preparation_scalar': 'work/checked02.json', 'preparation_scalar_O': 'work/checked02-O.json',
             'cuts_scalar': 'work/free-cut-independent-02-03.json',
             'cuts_scalar_O': 'work/free-cut-independent-02-03-O.json',
             'seed_scalar': 'work/reserve-seed-checked.json', 'seed_scalar_O': 'work/reserve-seed-checked-O.json',
             'reserve_scalar': 'work/reserve-preparations-checked.json',
             'reserve_scalar_O': 'work/reserve-preparations-checked-O.json',
             'reserve_classifications': 'work/reserve-preparation-classifications.json',
             'public_universal_fixture': 'universal/fixture.json',
             'public_universal_certificate': 'universal/certificate.json'}
    write('transport-inputs.json', {'agent': 'six-sorting-1', 'role': 'researcher',
                                  'inputs': {name: file_binding(path) for name, path in names.items()},
                                  'all_inputs_regenerated_locally_from_static_source': True})
    child('controls_reserve.py')
    finite = {'original_scalar_cache_sha256': original['finite']['scalar_cache_sha256'],
              'whole_preparation_scalar_finite_sha256': preparation['finite_sha256'],
              'whole_freecut_scalar_finite_sha256': cuts['finite_sha256'],
              'whole_original_HIGH_reserve_finite_sha256': seed['finite_sha256'],
              'reserve_preparation_scalar_finite_sha256': reserve['finite_sha256'],
              'public_universal_finite_sha256': universal['finite_sha256'],
              'full_preparation_functions': 8351, 'retained_functions': 5295,
              'reserve_excluded_functions': 2098, 'reserve_open_functions': 3197,
              'cold_all_sources_and_original_inputs': True, 'external_cached_arrays_used': False,
              'old_negative_corpus_used': False, 'normal_O_entire_records_equal': True}
    result = {'agent': 'six-sorting-1', 'role': 'researcher',
              'status': 'COMPLETE_COLD_ORIGINAL_PREPARATION_AND_RESERVE_PHASE',
              'finite': finite, 'finite_sha256': digest(finite), 'seconds': time.monotonic() - start}
    write('phase-original-reserve-complete.json', result)
    progress(result['status'], phase_finite_sha256=result['finite_sha256'])
    print(json.dumps(result), flush=True)


def fronts():
    prerequisite = checked_finite(read('phase-original-reserve-complete.json'))
    need(prerequisite['finite']['cold_all_sources_and_original_inputs'], 'Cold complete input phase required')
    spec = importlib.util.spec_from_file_location('standalone_serial_slice', ROOT / 'run_slice.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    intervals = []
    for first in range(0, 5295, 128):
        operations_allow()
        static_sources()
        last = min(first + 128, 5295)
        module.FIRST, module.LAST = first, last
        module.STAGES.clear()
        started = time.monotonic()
        # The slice driver runs actual mathematical children with55s guards;
        # it is not itself wrapped in a nested computational-job timeout.
        module.main()
        slice_result = checked_finite(read(f'slice-complete02-{first:05}-{last:05}.json'))
        STAGES.extend({'parent_interval': [first, last], **row} for row in module.STAGES)
        f = slice_result['finite']
        extension = None
        if f['unresolved_front_indices']:
            child('select_extended.py', first, last)
            child('verify_extended.py', first, last)
            child('verify_extended.py', first, last, optimized=True)
            extended = pair(f'extended-check-{first:05}-{last:05}')
            need(extended['finite']['remaining_open_indices'] == [] and
                 extended['finite']['independently_positive_cases'] == len(f['unresolved_front_indices']),
                 'Actual sufficient misses remain open; no complete route conclusion')
            extension = {'scalar_finite_sha256': extended['finite_sha256'],
                         'actual_indices': f['unresolved_front_indices']}
        intervals.append({'retained_interval': [first, last],
                          'functions': len(f['processed_previous_open_offsets']),
                          'slice_finite_sha256': slice_result['finite_sha256'],
                          'extension': extension, 'seconds': time.monotonic() - started})
        write('cold-front-progress.json', {'agent': 'six-sorting-1', 'role': 'researcher',
                                          'complete_intervals': intervals,
                                          'complete_functions': sum(r['functions'] for r in intervals),
                                          'remaining_functions': 3197 - sum(r['functions'] for r in intervals),
                                          'whole_route_complete': False})
        write('run-stages.json', STAGES)
        print(json.dumps({'complete_front_interval': [first, last], 'functions': intervals[-1]['functions'],
                          'seconds': intervals[-1]['seconds']}), flush=True)
    need(sum(r['functions'] for r in intervals) == 3197, 'Incomplete cold remaining function cover')
    child('check_controls.py', 0, 128)
    if any(r['retained_interval'] == [5120, 5248] and r['extension'] for r in intervals):
        child('check_extended_controls.py', 5120, 5248)
    finite = {'cold_input_phase_finite_sha256': prerequisite['finite_sha256'],
              'complete_front_intervals': [{k: v for k, v in row.items() if k != 'seconds'} for row in intervals],
              'complete_remaining_functions': 3197, 'reserve_excluded_functions': 2098,
              'all_retained_functions_excluded': 5295, 'remaining_open_functions': 0,
              'external_cached_arrays_used': False, 'old_negative_corpus_used': False,
              'normal_O_entire_records_equal': True, 'independent_person_review_claimed': False,
              'arbitrary_actual_preparation_length': True, 'arbitrary_suffix_depth': True}
    result = {'agent': 'six-sorting-1', 'role': 'researcher',
              'status': 'COMPLETE_COLD_REMAINING_FRONT_PHASE_PENDING_FINAL_SOURCE_FREEZE',
              'finite': finite, 'finite_sha256': digest(finite)}
    write('phase-fronts-complete.json', result)
    progress(result['status'], phase_finite_sha256=result['finite_sha256'])
    print(json.dumps({'complete_phase': result['status'], 'finite_sha256': result['finite_sha256']}), flush=True)


def main():
    operations_allow()
    static_sources()
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'
    need(mode in ('all', 'seed', 'seed-resume', 'fronts'), 'Use all, seed, seed-resume, or fronts')
    WORK.mkdir(exist_ok=True)
    if mode in ('all', 'seed'):
        need(not any(WORK.iterdir()) and not (ROOT / 'prior/work').exists() and
             not (ROOT / 'universal/work').exists(), 'Cold seed requires fresh work; preserve previous outputs')
        original_reserve()
    else:
        STAGES.extend(read('run-stages.json'))
        if mode == 'seed-resume':
            need(len(STAGES) == 1 and STAGES[0]['script'] == 'universal/run.py' and
                 STAGES[0]['returncode'] == 0 and not (ROOT / 'prior/work').exists(),
                 'Seed resume is only for the preserved completed universal subphase')
            completed = checked_finite(json.loads((ROOT / 'universal/work/result.json').read_text()))
            need(completed['finite_sha256'] ==
                 'a2faef8075c751886b467a5c2095ad79552e712b3b7ca29256715dd86fe6ed4e',
                 'Preserved actual universal replay differs')
            original_reserve(universal_already_complete=True)
    if mode in ('all', 'fronts'):
        fronts()


if __name__ == '__main__':
    main()
