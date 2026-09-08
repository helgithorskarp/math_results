#!/usr/bin/env python3
"""Full exact replay in a temporary directory, including the pinned parent."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from dependency import checked_parent

HERE = Path(__file__).resolve().parent


def run(argv, *, data=None, env=None):
    result = subprocess.run(argv, input=data, capture_output=True, check=True, env=env)
    if result.stderr:
        raise ValueError(('unexpected stderr', argv, result.stderr.decode()))
    return result.stdout


def main():
    names = []
    for line in (HERE/'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ', 1)
        if Path(name).name != name or name in names:
            raise ValueError('unsafe/duplicate source manifest path')
        if hashlib.sha256((HERE/name).read_bytes()).hexdigest() != digest:
            raise ValueError(('source manifest mismatch', name))
        names.append(name)
    parent = checked_parent()
    previous = json.loads(run([sys.executable, '-B', str(parent/'reproduce.py')]))
    if previous['status'] != 'REPRODUCED_SEPARATOR18_CLASSIFICATION':
        raise ValueError('prior proof replay did not pass')
    compared = []
    with tempfile.TemporaryDirectory(prefix='r55-max-connectivity-') as temp:
        temp = Path(temp)
        flags = ['-std=c++17', '-Wall', '-Wextra', '-Wconversion', '-Wsign-conversion', '-Werror']
        release = temp/'independent'
        sanitized = temp/'independent-sanitized'
        run(['g++', *flags, '-O3', str(HERE/'independent.cpp'), '-o', str(release)])
        run(['g++', *flags, '-O1', '-g', '-fno-omit-frame-pointer', '-fsanitize=address,undefined',
             str(HERE/'independent.cpp'), '-o', str(sanitized)])
        core_data = run([str(release), 'cores'])
        (temp/'cores.txt').write_bytes(core_data)
        env = dict(os.environ, ASAN_OPTIONS='detect_leaks=1:halt_on_error=1',
                   UBSAN_OPTIONS='halt_on_error=1:print_stacktrace=1')
        if run([str(sanitized), 'cores'], env=env) != core_data:
            raise ValueError('sanitized core enumeration differs')
        native_marked = None
        for mode, name in (([], 'normal'), (['-O'], 'optimized')):
            out = temp/name
            run([sys.executable, *mode, '-B', str(HERE/'enumerate.py'), str(out)])
            if (out/'SUMMARY.json').read_bytes() != (HERE/'SUMMARY.json').read_bytes():
                raise ValueError(('producer summary mismatch', name))
            if native_marked is None:
                jobs = (out/'jobs.txt').read_bytes()
                native_marked = run([str(release), 'marked'], data=jobs)
                if run([str(sanitized), 'marked'], data=jobs, env=env) != native_marked:
                    raise ValueError('sanitized marked enumeration differs')
                (temp/'marked.txt').write_bytes(native_marked)
            programs = [
                ('audit.py', 'AUDIT.json', [str(out), str(temp/'cores.txt'), str(temp/'marked.txt')]),
                ('verify_core.py', 'CORE-AUDIT.json', []),
                ('controls.py', 'CONTROLS.json', [])]
            for program, expected, args in programs:
                result = run([sys.executable, *mode, '-B', str(HERE/program), *args])
                if result != (HERE/expected).read_bytes():
                    raise ValueError(('independent output mismatch', name, program))
                compared.append([name, program])
    print(json.dumps({'status': 'REPRODUCED_MAXIMAL_VERTEX_CONNECTIVITY',
                      'manifest_entries': len(names), 'pinned_parent_replayed': True,
                      'python_modes': 2, 'complete_native_sanitizer_runs': 2,
                      'byte_equal_checker_outputs': len(compared),
                      'complete_physical_marked_graphs_per_mode': 46911,
                      'new_physical_packing_tasks_decided': 0,
                      'good43_found': False}, sort_keys=True))


if __name__ == '__main__':
    main()
