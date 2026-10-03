"""Source-only serial reproduction; expected records are checked afterward."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time

from controls import operations_allow
from run_preparations import ENV, need
from seal import source_rows, verify_and_seal

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'work'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--resume', action='store_true',
                        help='Reuse only completed local phases with the identical source seal.')
    args = parser.parse_args()
    operations_allow()
    expected_source = json.loads((ROOT/'SOURCE-MANIFEST.json').read_text())['files']
    need(source_rows() == expected_source, 'Source bytes differ from the complete source seal')
    manifest_sha = hashlib.sha256((ROOT/'SOURCE-MANIFEST.json').read_bytes()).hexdigest()
    state = WORK/'run-source.json'
    if args.resume:
        need(state.exists() and json.loads(state.read_text())['source_manifest_sha256'] == manifest_sha,
             'Resume requires exactly these previously recorded source bytes')
    else:
        need(not WORK.exists() or not any(WORK.iterdir()),
             'Cold execution requires empty work; preserve previous outputs or use --resume')
        prior_work = ROOT/'prior/work'
        need(not prior_work.exists() or not any(prior_work.iterdir()),
             'Cold execution requires empty prior/work; previous data are not an input')
        WORK.mkdir(exist_ok=True)
        prior_work.mkdir(exist_ok=True)
        state.write_text(json.dumps({'source_manifest_sha256': manifest_sha,
                                    'cache_free_start': True}, indent=2)+'\n')
    started = time.monotonic()
    receipts = []

    def driver(script, *arguments, optimized=False, guard=None):
        operations_allow()
        need(source_rows() == expected_source, 'Source changed during execution')
        arguments = list(map(str, arguments))
        command = [sys.executable]+(['-O'] if optimized else [])+[str(ROOT/script), *arguments]
        print(json.dumps({'start': script, 'arguments': arguments, 'optimized':optimized}), flush=True)
        t = time.monotonic()
        with (WORK/('runner-'+script+('-O' if optimized else '')+'.log')).open('w') as output:
            child = subprocess.Popen(command, env=ENV, stdout=output,
                                     stderr=subprocess.STDOUT, start_new_session=True)
            try:
                while child.poll() is None:
                    operations_allow()
                    need(guard is None or time.monotonic()-t < guard,
                         'Incomplete guarded mathematical stage; no exclusion')
                    time.sleep(.5)
            except BaseException:
                # This process group contains only this runner's own serial job.
                os.killpg(child.pid, signal.SIGTERM)
                try:
                    child.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(child.pid, signal.SIGKILL)
                    child.wait()
                raise
        receipt = {'script': script, 'arguments': arguments, 'optimized':optimized,
                   'returncode': child.returncode, 'seconds': time.monotonic()-t}
        receipts.append(receipt)
        (WORK/'runner-stages.json').write_text(json.dumps(receipts, indent=2)+'\n')
        need(child.returncode == 0, 'Incomplete mathematical stage: '+script+'; no exclusion')
        print(json.dumps({'completed': script, 'seconds': receipt['seconds']}), flush=True)

    if not args.resume or not (WORK/'preparation-phase-complete.json').exists():
        driver('run_preparations.py')
    if not args.resume or not (WORK/'preparation-bindings.json').exists():
        driver('make_bindings.py', guard=55)
    if not args.resume or not (WORK/'reserve-phase-complete.json').exists():
        driver('run_reserve.py')
    driver('run_all.py')
    for optimized in (False,True):
        name = 'transfer-checked'+('-O' if optimized else '')+'.json'
        if not args.resume or not (WORK/name).exists():
            driver('verify_transfer.py', optimized=optimized, guard=55)
    for script, result, folder in (
        ('check_controls.py', 'semantic-controls-complete.json', 'semantic-controls-scratch'),
        ('check_extended_controls.py', 'extended-semantic-controls-complete.json', 'extended-controls-scratch'),
        ('check_nested_controls.py', 'nested-semantic-controls-complete.json', 'nested-controls-scratch')):
        if not args.resume or not (WORK/result).exists():
            driver(script, WORK/folder)
    need(source_rows() == expected_source, 'Source changed before final mathematical binding')
    certificate = verify_and_seal()
    native_stages = []
    for path in sorted(WORK.glob('*stages*.json')):
        if path.name == 'runner-stages.json':
            continue
        for row in json.loads(path.read_text()):
            native_stages.append({'stage_file': path.name, **row})
    native_stages.extend({'stage_file':'runner-stages.json', **r} for r in receipts
                         if r['script']=='verify_transfer.py')
    need(all(row['returncode'] == 0 for row in native_stages), 'Unsuccessful retained mathematical child')
    rss = []
    for path in WORK.glob('*.json'):
        obj = json.loads(path.read_text())
        if isinstance(obj, dict) and 'maximum_rss_kib' in obj:
            rss.append(obj['maximum_rss_kib'])
    validation = {
        'agent': 'six-sorting-1', 'role': 'researcher',
        'status': 'COMPLETE_COLD_SOURCE_ONLY_EXECUTION' if not args.resume else 'COMPLETE_EXACT_SOURCE_RESUME',
        'command': 'python3 run.py'+(' --resume' if args.resume else ''),
        'python': sys.version, 'standard_library_only': True,
        'cache_free_this_execution': not args.resume,
        'source_manifest_sha256': manifest_sha,
        'certificate_finite_sha256': certificate['finite_sha256'],
        'wall_seconds': time.monotonic()-started,
        'top_level_serial_stages': receipts,
        'retained_actual_mathematical_stage_count': len(native_stages),
        'retained_actual_mathematical_stages': native_stages,
        'native_threads': 1, 'maximum_active_mathematical_children': 1,
        'actual_math_child_guard_seconds': 55,
        'internal_general_guard_seconds': 45,
        'preparation_guard_seconds': 5, 'preparation_guard_states': 20000,
        'maximum_top_result_self_RSS_kib': max(rss, default=0),
        'maximum_descendant_RSS_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
        'independent_person_review_claimed': False,
        'global_size44_exclusion_claimed': False}
    (WORK/'VALIDATION.json').write_text(json.dumps(validation, indent=2)+'\n')
    print(json.dumps({k:v for k,v in validation.items()
                      if k not in ('retained_actual_mathematical_stages','top_level_serial_stages')}), flush=True)


if __name__ == '__main__':
    main()
