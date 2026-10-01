"""Sequential bounded reproduction; large intermediate witnesses stay local."""
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

HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repository-root', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    need(sys.version_info >= (3, 11), 'CPython >= 3.11 required')
    root = args.repository_root.resolve()
    inputs = json.loads((HERE / 'INPUTS.json').read_text())
    for name, expected in inputs['files_sha256'].items():
        path = root / name
        need(path.resolve().is_relative_to(root), 'Input outside repository')
        need(hashlib.sha256(path.read_bytes()).hexdigest() == expected, 'Changed pinned input: ' + name)
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=False)
    expected = json.loads((HERE / 'EXPECTED.json').read_text())
    author = root / 'round-two/six-tammes-2/robust-eight-core/AUDIT_EXPECTED.json'
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
               MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')
    stages = []
    began = time.monotonic()

    def run(label, script, arguments, optimized=False, stdout_json=False):
        destination = output / (label + '.json')
        log = output / (label + '.log')
        command = [sys.executable, '-B'] + (['-O'] if optimized else [])
        command += [str(HERE / script)] + [str(x) for x in arguments]
        started = time.monotonic()
        with log.open('w') as stream:
            process = subprocess.Popen(command, stdout=stream, stderr=subprocess.STDOUT,
                                       env=env, start_new_session=True)
            try:
                result = process.wait(timeout=55)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
                raise RuntimeError(label + ': operational timeout; no mathematical verdict')
        need(result == 0, label + ': verification failed; see ' + str(log))
        if stdout_json:
            destination.write_text(log.read_text())
        stages.append({'stage': label, 'seconds': time.monotonic()-started})
        return json.loads(destination.read_text())

    exports = {}
    for strip in ['lower', 'upper']:
        path = output / (strip + '-parent.json')
        exports[strip] = path
        run(strip+'-parent', 'replay_parent.py',
            ['--repository-root', root, '--strip', strip, '--output', path])
    results = {}
    for optimized in [False, True]:
        mode = 'optimized' if optimized else 'normal'
        for strip in ['lower', 'upper']:
            label = strip + '-' + mode
            path = output / (label + '.json')
            result = run(label, 'audit.py', ['--export', exports[strip],
                         '--author-expected', author, '--output', path], optimized)
            stable = {k: v for k, v in result.items()
                      if k not in ['python', 'optimization', 'seconds', 'maxrss_kib']}
            need(stable == expected['audits'][strip], label + ': full stable receipt mismatch')
            results[label] = result
        label = 'controls-' + mode
        result = run(label, 'controls.py', ['--upper-export', exports['upper'],
                     '--author-expected', author], optimized, stdout_json=True)
        need(result == expected['controls'], label + ': complete controls mismatch')
    receipt = {'agent': 'six-reviewer-5', 'role': 'independent reviewer',
               'status': 'SCOPED_REVIEW_AND_LARGER_TOLERANCE_VERIFIED',
               'input_files_checked': len(inputs['files_sha256']),
               'python': sys.version.split()[0], 'stages': stages,
               'total_seconds': time.monotonic()-began,
               'max_child_rss_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
               'audits': results, 'controls': expected['controls'],
               'trust_boundary': inputs['trust_boundary']}
    (output / 'VALIDATION.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
