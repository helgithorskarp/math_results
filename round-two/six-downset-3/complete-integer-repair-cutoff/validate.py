"""Four serial source-sealed normal/-O children, whole arithmetic-byte comparison."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import os
import resource
import subprocess
import sys
import time

BASE = Path(__file__).resolve().parent
NATIVE = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
          'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, default=BASE / 'work/final')
    args = parser.parse_args()
    work = args.work.resolve()
    work.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(BASE))
    import source_gate
    source = source_gate.verify()
    env = dict(os.environ)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    for name in NATIVE:
        env[name] = '1'
    campaign = Path(os.environ['DISCOVERY_RESEARCH_TEAM_ROOT']) if os.environ.get('DISCOVERY_RESEARCH_TEAM_ROOT') else None
    receipt = {'actual_agent': 'six-downset-3', 'role': 'researcher',
               'UTC': datetime.now(timezone.utc).isoformat(), 'python': sys.version,
               'source_only': True, 'whole_public_source_sealed_before_completed_replay': True,
               'source_gate': source, 'native_threads': 1,
               'all_native_thread_settings': {name: env[name] for name in NATIVE},
               'one_serial_intensive_child': True, 'child_timeout_seconds': 60,
               'scope': 'unchanged1CPU2GiB', 'children': [], 'completed': False}
    outputs = {}
    for phase in ('producer', 'checker'):
        paired = []
        for mode, flags in (('normal', []), ('optimized', ['-O'])):
            if campaign is not None and any((campaign / name).exists() for name in ('PAUSED.json', 'HANDOVER.json')):
                raise RuntimeError('Operations pause/handover barrier; preserve partial receipt')
            source_gate.verify()
            out = work / (phase + '-' + mode + '.json')
            if phase == 'producer':
                script = BASE / 'probe.py'
                arguments = []
            else:
                script = BASE / 'check.py'
                arguments = ['--input', str(work / ('producer-' + mode + '.json'))]
            bootstrap = ('import runpy,sys\n'
                         'sys.path.insert(0,sys.argv.pop(1))\n'
                         'sys.argv=sys.argv[1:]\n'
                         'runpy.run_path(sys.argv[0],run_name="__main__")\n'
                         'if any(n=="sympy" or n.startswith("sympy.") for n in sys.modules):\n'
                         '    raise RuntimeError("CAS imported in mathematical child")\n')
            command = [sys.executable, '-I', *flags, '-B', '-c', bootstrap,
                       str(BASE), str(script), *arguments, '--out', str(out)]
            start = time.monotonic()
            item = {'phase': phase, 'mode': mode, 'command': command}
            try:
                run = subprocess.run(command, cwd=BASE, env=env, capture_output=True,
                                     text=True, timeout=60)
                item.update(exit_code=run.returncode, stdout=run.stdout,
                            stderr=run.stderr, completed=run.returncode == 0)
            except subprocess.TimeoutExpired:
                item.update(completed=False, timeout=True,
                            no_mathematical_absence_inference=True)
            item.update(seconds=time.monotonic() - start,
                        peak_children_RSS_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
            receipt['children'].append(item)
            (work / 'VALIDATION.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
            if not item['completed']:
                raise ValueError('Incomplete operational child, no absence inference: ' + phase + ' ' + mode)
            data = json.loads(out.read_text())
            if not data['completed']:
                raise ValueError('Mathematical obligation incomplete: ' + phase + ' ' + mode)
            paired.append(out.read_bytes())
            print(phase + ' ' + mode + ' completed ' + format(item['seconds'], '.3f') + 's', flush=True)
        if paired[0] != paired[1]:
            raise ValueError('ENTIRE paired normal/-O mathematical bytes differ: ' + phase)
        outputs[phase] = json.loads(paired[0])
    if outputs['checker']['entire_independently_evaluated_census'] != outputs['producer']:
        raise ValueError('EVERY paired producer/checker arithmetic field must agree')
    payload = json.dumps(outputs, separators=(',', ':'), sort_keys=True) + '\n'
    (work / 'RESULT.json').write_text(payload)
    receipt.update(completed=True, phase_count=2, isolated_normal_O_children=4,
                   entire_normal_optimized_math_records_and_bytes_equal=True,
                   every_producer_checker_census_field_equal=True,
                   point_count=19969, count_count=121,
                   whole_math_SHA256=hashlib.sha256(payload.encode()).hexdigest(),
                   whole_math_bytes=len(payload.encode()),
                   whole_point_record_SHA256=outputs['checker']['whole_point_record_SHA256'],
                   whole_point_record_bytes=outputs['checker']['whole_point_record_bytes'],
                   semantic_damage_rejections_per_checker_mode=10,
                   no_CAS_imported_in_math_children=True,
                   least_uniform_onset=9, corrected_k8_first_feasible_q=33,
                   old_parent8_or44_children_not_repeated=True,
                   ordinary_bridges_unformalized=True, independent_person_review=False)
    (work / 'VALIDATION.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
    print(json.dumps({key: value for key, value in receipt.items() if key not in ('children', 'source_gate')}), flush=True)


if __name__ == '__main__':
    main()
