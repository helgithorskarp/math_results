"""Four phases, eight serial isolated normal/-O runs; compare every result byte."""
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
    parser.add_argument('--operations-state', type=Path)
    args = parser.parse_args()
    work = args.work.resolve()
    work.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(BASE))
    import source_gate
    source_gate.verify()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    for name in NATIVE:
        env[name] = '1'
    receipt = {'actual_agent': 'six-downset-3', 'role': 'researcher',
               'UTC': datetime.now(timezone.utc).isoformat(), 'source_only': True,
               'native_threads': 1, 'one_serial_intensive_child': True,
               'child_timeout_seconds': 60, 'children': [], 'completed': False}
    records = {}
    for phase in ('curves', 'monotonicity', 'negative-zone', 'checker'):
        both = []
        for mode, flags in (('normal', []), ('optimized', ['-O'])):
            if args.operations_state is not None and any(
                    (args.operations_state / name).exists()
                    for name in ('PAUSED.json', 'HANDOVER.json')):
                raise RuntimeError('Operations pause/handover barrier; preserve partial receipt')
            source_gate.verify()
            out = work / (phase + '-' + mode + '.json')
            if phase == 'checker':
                script, arguments = 'check.py', []
                for other in ('curves', 'monotonicity', 'negative-zone'):
                    arguments += ['--' + other, str(work / (other + '-' + mode + '.json'))]
            else:
                script, arguments = 'probe.py', [phase, '--k0', '128']
            bootstrap = ('import runpy,sys\n'
                         'sys.path.insert(0,sys.argv.pop(1))\n'
                         'import source_gate\nsource_gate.verify()\n'
                         'sys.argv=sys.argv[1:]\n'
                         'runpy.run_path(sys.argv[0],run_name="__main__")\n'
                         'if any(n=="sympy" or n.startswith("sympy.") for n in sys.modules):\n'
                         '    raise RuntimeError("CAS imported in mathematical child")\n')
            command = [sys.executable, '-I', *flags, '-B', '-c', bootstrap,
                       str(BASE), str(BASE / script), *arguments, '--out', str(out)]
            start = time.monotonic()
            item = {'phase': phase, 'mode': mode, 'command': command}
            try:
                result = subprocess.run(command, cwd=BASE, env=env, capture_output=True,
                                        text=True, timeout=60)
                item.update(exit_code=result.returncode, stdout=result.stdout,
                            stderr=result.stderr, completed=result.returncode == 0)
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
                raise ValueError('Whole mathematical obligation failed: ' + phase + ' ' + mode)
            both.append(data)
            print(phase + ' ' + mode + ' completed ' + format(item['seconds'], '.3f') + 's', flush=True)
        if both[0] != both[1]:
            raise ValueError('ENTIRE normal/-O mathematical records differ: ' + phase)
        records[phase] = both[0]
    payload = json.dumps(records, indent=2, sort_keys=True) + '\n'
    (work / 'RESULT.json').write_text(payload)
    digest = hashlib.sha256(payload.encode()).hexdigest()
    expected = json.loads((BASE / 'EXPECTED.json').read_text())
    if digest != expected['whole_math_SHA256'] or len(payload.encode()) != expected['whole_math_bytes']:
        raise ValueError('Whole regenerated mathematical record differs from expected source seal')
    receipt.update(completed=True, phase_count=4, isolated_normal_O_children=8,
                   entire_normal_optimized_records_equal=True, whole_math_SHA256=digest,
                   whole_math_bytes=len(payload.encode()), no_CAS_imported_in_math_children=True,
                   semantic_damage_rejections_per_mode=8, unformalized=True, independent_review=False)
    (work / 'VALIDATION.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
    print(json.dumps({k: v for k, v in receipt.items() if k != 'children'}), flush=True)


if __name__ == '__main__':
    main()
