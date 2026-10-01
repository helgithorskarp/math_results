"""Serial exact replay. Large generated records/binaries stay in --work."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time
import model as m

ROOT = Path(__file__).resolve().parent


def run(command, env, timeout=40, stdout=None):
    result = subprocess.run(command, env=env, text=True, stdout=stdout or subprocess.PIPE,
                            stderr=subprocess.PIPE, timeout=timeout)
    if result.returncode:
        raise RuntimeError('command failed: '+result.stderr[-2000:])
    return result.stdout


def replay(work, resume, generate):
    start = time.monotonic()
    expected = ROOT/'expected.json'
    frozen_before = expected.is_file()
    m.need(generate or frozen_before, 'expected fixture must pre-exist the replay')
    m.need(not generate or not frozen_before, 'generation may not replace an existing fixture')
    work.mkdir(parents=True, exist_ok=True)
    m.need(resume or not list(work.iterdir()), 'nonempty work directory requires explicit --resume')
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')
    source = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ROOT.iterdir())
              if p.is_file() and p.name != 'expected.json'}
    manifest = work/'source.json'
    if resume:
        m.need(manifest.is_file() and json.loads(manifest.read_text()) == source, 'resumption source mismatch')
    else:
        manifest.write_text(json.dumps(source, sort_keys=True)+'\n')
    executable = work/'independent'
    run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-pedantic', str(ROOT/'independent.cpp'), '-o', str(executable)], env, 30)
    position = 0
    for path in sorted(work.glob('producer-*.json')):
        phase = json.loads(path.read_text())
        m.need(phase['first'] == position and phase['next'] == position+len(phase['records']), 'resumption producer gap')
        position = phase['next']
    while position < 4768:
        path = work/f'producer-{position:05d}.json'
        print(run([sys.executable, str(ROOT/'prove.py'), '--first', str(position), '--seconds', '30', '--out', str(path)], env).strip(), flush=True)
        phase = json.loads(path.read_text())
        m.need(phase['first'] == position and phase['next'] > position, 'producer no completed case')
        position = phase['next']
    for p, total in ((1, 1225), (2, 20825)):
        position = 0
        for path in sorted(work.glob(f'native{p}-*.jsonl')):
            lines = [json.loads(line) for line in path.read_text().splitlines()]
            phase = lines[-1]
            m.need(phase.get('segment') is True and phase['first'] == position and phase['next'] == position+len(lines)-1, 'resumption native gap')
            position = phase['next']
        while position < total:
            path = work/f'native{p}-{position:05d}.jsonl'
            with path.open('w') as out:
                run([str(executable.resolve()), '--promotions', str(p), '--first', str(position), '--seconds', '30'], env, stdout=out)
            phase = json.loads(path.read_text().splitlines()[-1])
            m.need(phase.get('segment') is True and phase['first'] == position and phase['next'] > position, 'native no completed case')
            position = phase['next']
            print(json.dumps(phase), flush=True)
    for optimized, name in ((False, 'normal'), (True, 'optimized')):
        command = [sys.executable] + (['-O'] if optimized else []) + [str(ROOT/'check.py'), '--work', str(work),
                   '--out', str(work/f'check-{name}.json'), '--controls']
        if not generate:
            command += ['--expected', str(expected)]
        run(command, env, 40)
    normal = json.loads((work/'check-normal.json').read_text())
    optimized = json.loads((work/'check-optimized.json').read_text())
    m.need(normal == optimized, 'normal/optimized evidence mismatch')
    if generate:
        m.need(not frozen_before, 'generation may not replace an existing fixture')
        expected.write_text(json.dumps(normal['evidence'], indent=2, sort_keys=True)+'\n')
    summary = dict(status='FIXTURE_GENERATED' if generate else 'COMPLETE_FROZEN_REPLAY',
                   fixture_preexisted=frozen_before, fixture_compared=not generate,
                   seconds=time.monotonic()-start, child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                   threads=1, case_phase_seconds=30, source=source,
                   versions=dict(python=sys.version.split()[0], cpp=run(['g++', '--version'], env, 10).splitlines()[0]),
                   expected_sha256=hashlib.sha256(expected.read_bytes()).hexdigest(),
                   stats=normal['evidence']['stats'], damage_controls=normal['damage_controls'])
    (work/'manifest.json').write_text(json.dumps(summary, indent=2, sort_keys=True)+'\n')
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--resume', action='store_true')
    parser.add_argument('--generate-expected', action='store_true', help='explicit initial fixture generation; is not fixture agreement')
    args = parser.parse_args()
    replay(args.work, args.resume, args.generate_expected)
