"""Five required pre-arithmetic source failures; exact exit/error/marker checks."""
from source_binding import verify_source as _verify_source
_verify_source()
import os
for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
             'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[name] = '1'
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import signal
import subprocess
import sys

from source_binding import FILES, require


def invoke(path, arguments, mode):
    if mode == 'cold':
        code = ('import runpy,sys;sys.path.insert(0,' + repr(str(path.parent))
                + ');sys.argv=' + repr([str(path)] + arguments)
                + ';runpy.run_path(' + repr(str(path)) + ",run_name='__main__')")
        return [sys.executable, '-I', '-B', '-c', code]
    return [sys.executable, '-B'] + (['-O'] if mode == 'optimized' else []) + [str(path)] + arguments


def barrier():
    state = os.environ.get('DISCOVERY_RESEARCH_TEAM_ROOT')
    if state:
        require(not any((Path(state) / n).exists() for n in
                        ('PAUSED', 'PAUSED.json', 'HANDOVER', 'HANDOVER.json')),
                'operational barrier before source child')


def main():
    def expire(signum, frame):
        raise TimeoutError('fixed60s source child; timeout is not rejection')
    signal.signal(signal.SIGALRM, expire)
    signal.alarm(60)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--mode', choices=['normal', 'optimized', 'cold'], required=True)
    args = parser.parse_args()
    require(not args.out.exists(), 'fresh source adverse directory')
    args.out.mkdir(parents=True)
    base = Path(__file__).resolve().parent
    records = []
    observations = []
    for target in ('PROOF.md', 'reader.py', 'EXPECTED.json', 'source_binding.py', 'census'):
        barrier()
        case = (args.out / target.replace('.', '-')).resolve()
        case.mkdir()
        for name in FILES + ('SOURCE.json',):
            shutil.copyfile(base / name, case / name)
        marker = case / 'ARITHMETIC-IMPORTED'
        geometry = (case / 'geometry.py').read_text()
        geometry = geometry.replace('_verify_source()\n',
            '_verify_source()\nfrom pathlib import Path as _MarkerPath\n'
            + '_MarkerPath(' + repr(str(marker)) + ").write_text('unexpected arithmetic import')\n", 1)
        (case / 'geometry.py').write_text(geometry)
        source = json.loads((case / 'SOURCE.json').read_text())
        source['defining_files']['geometry.py'] = {
            'bytes': len(geometry.encode()), 'sha256': hashlib.sha256(geometry.encode()).hexdigest()}
        if target == 'census':
            del source['defining_files']['RANK-BRIDGE.md']
            required = 'source census'
        else:
            with (case / target).open('a') as out:
                out.write('\n# designated source corruption\n' if target.endswith('.py')
                          else '\n')
            required = 'source file binding: ' + target
        raw = json.dumps(source, indent=2).encode() + b'\n'
        (case / 'SOURCE.json').write_bytes(raw)
        env = dict(os.environ, SMALL_CUBE_SOURCE_SHA256=hashlib.sha256(raw).hexdigest())
        command = invoke(case / 'control.py', ['--n', '2', '--counts', '5,4',
                         '--out', str(case / 'UNEXPECTED-OUTPUT')], args.mode)
        child = subprocess.run(command, capture_output=True, text=True, env=env, timeout=60)
        require(child.returncode == 1 and child.stderr.splitlines()
                and child.stderr.splitlines()[-1] == 'ValueError: ' + required
                and not marker.exists() and not (case / 'UNEXPECTED-OUTPUT').exists(),
                'wrong source rejection outcome: ' + target)
        records.append({'target': target, 'rejected': True, 'exit': 1,
                        'exact_gate': required, 'arithmetic_imported': False})
        observations.append({'target': target, 'command': command,
                             'returncode': child.returncode, 'stderr': child.stderr})
    result = {'agent': 'six-downset-1', 'role': 'researcher', 'complete': True,
              'source_rejections': records}
    (args.out / 'WHOLE-REJECTIONS.json').write_text(
        json.dumps(result, sort_keys=True, separators=(',', ':')) + '\n')
    (args.out / 'CHILDREN.json').write_text(json.dumps(observations, indent=2) + '\n')
    signal.alarm(0)
    print(json.dumps({'complete': True, 'designated_exit1_children': len(records),
                      'all_exact_source_guards_before_arithmetic': True}))


if __name__ == '__main__':
    main()
