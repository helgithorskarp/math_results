"""Serial thread-one, 20-second-child reproduction; fail on incomplete evidence."""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scratch', type=Path, required=True)
    args = parser.parse_args()
    out = args.scratch.resolve()
    out.mkdir(parents=True, exist_ok=True)
    source = Path(__file__).resolve().parent
    frozen = json.loads((source/'certificate.json').read_text())
    env = dict(os.environ)
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
        env[key] = '1'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    children = []
    mathematics = []
    controls = []
    for mode in ('normal', 'optimized'):
        data = out/mode
        (data/'scratch').mkdir(parents=True, exist_ok=True)
        prefix = [sys.executable, *(['-O'] if mode == 'optimized' else []), '-B']
        commands = [prefix+[str(source/'generate-root.py')],
                    prefix+[str(source/'extend.py')],
                    prefix+[str(source/'check.py')],
                    prefix+[str(source/'controls.py'), '--data', str(data),
                            '--scratch', str(out/(mode+'-damages')), '--group', 'metadata'],
                    prefix+[str(source/'controls.py'), '--data', str(data),
                            '--scratch', str(out/(mode+'-damages')), '--group', 'records']]
        for index, command in enumerate(commands):
            start = time.monotonic()
            result = subprocess.run(command, cwd=data, env=env, text=True,
                                    capture_output=True, timeout=20)
            seconds = time.monotonic()-start
            (out/(mode+'-'+str(index)+'.stdout')).write_text(result.stdout)
            (out/(mode+'-'+str(index)+'.stderr')).write_text(result.stderr)
            children.append({'mode': mode, 'stage': index, 'command': command,
                             'seconds': seconds, 'exit': result.returncode})
            if result.returncode != 0:
                raise RuntimeError('Incomplete/failed child, no proof: '+result.stderr)
            if index == 2:
                fields = json.loads(result.stdout)
                fields.pop('seconds')
                if fields != frozen:
                    raise ValueError('Complete independent AP mathematical fields differ from frozen record')
                mathematics.append(fields)
            elif index >= 3:
                fields = json.loads(result.stdout)
                fields.pop('seconds')
                controls.append(fields)
            print(json.dumps({'mode': mode, 'stage': index, 'seconds': seconds, 'exit': result.returncode}), flush=True)
    if mathematics[0] != mathematics[1] or controls[:2] != controls[2:]:
        raise ValueError('Full normal/optimized fields differ')
    canonical = json.dumps(mathematics[0], sort_keys=True, separators=(',', ':')).encode()
    record = {'agent': 'six-covering-3', 'role': 'researcher',
              'status': 'AUTHOR_CHECKED_COMPLETE',
              'all_complete_fields_normal_optimized_frozen_equal': True,
              'all_controls_normal_optimized_equal': True,
              'mathematical': mathematics[0], 'controls': controls[:2],
              'complete_mathematical_sha256': sha256(canonical).hexdigest(),
              'source_manifest_sha256': {p.name: sha256(p.read_bytes()).hexdigest()
                                        for p in sorted(source.iterdir()) if p.is_file()},
              'children': children, 'threads': 1, 'one_CPU_child': True,
              'child_guard_seconds': 20, 'retained_frontier_cap': 300,
              'max_child_seconds': max(x['seconds'] for x in children),
              'RSS_KiB': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              'external_review': False, 'ordinary_bridges_unformalized': True,
              'publication_metadata_not_part_of_reproduction': True}
    (out/'verification.json').write_text(json.dumps(record, indent=2, sort_keys=True)+'\n')
    print(json.dumps({k: record[k] for k in ('status', 'complete_mathematical_sha256',
                                          'max_child_seconds', 'RSS_KiB')}, indent=2))


if __name__ == '__main__':
    main()
