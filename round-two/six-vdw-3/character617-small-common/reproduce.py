"""Reproduce the small-common theorem from source, serially with20-second children."""
import argparse
import hashlib
import json
import os
import platform
import resource
import subprocess
import sys
import time
from pathlib import Path

PROGRAMS = ('ordered_quads.py', 'reverse_quads.py', 'merge_direct_quads.py',
            'extend_quads.py', 'check_extensions.py', 'merge_extensions.py',
            'select_weighted_domain.py', 'weighted_columns.py', 'check_weighted_columns.py',
            'merge_weighted_columns.py', 'weighted_orbits.py', 'tail_cases.py',
            'check_tail_cases.py', 'merge_tail_cases.py')
PHASES = ('quads', 'extensions', 'weighted', 'orbits', 'tails')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, obj):
    temp = path.with_name(path.name + '.tmp')
    temp.write_text(json.dumps(obj, sort_keys=True, indent=2) + '\n')
    temp.replace(path)


def tasks(work):
    # A task is phase, key, script, optimized, flag/value pairs, output.
    def task(phase, key, script, optimized, args, output):
        return phase, key, script, optimized, args, output
    for kind, first, program in (('ordered', 1, 'ordered_quads.py'), ('reverse', 3, 'reverse_quads.py')):
        for start in range(first, 308, 16):
            stop = min(start + 16, 308)
            for mode, optimized in (('normal', False), ('optimized', True)):
                yield task('quads', f'{kind}-{mode}-{start:03d}-{stop:03d}', program, optimized,
                           ['--start', str(start), '--stop', str(stop)],
                           work / 'quads' / f'{kind}-{mode}' / f'range-{start:03d}-{stop:03d}.json')
    quad = work / 'quads.json'
    yield task('quads', 'merge-quads', 'merge_direct_quads.py', False,
               ['--ordered', work / 'quads/ordered-normal', '--ordered-optimized', work / 'quads/ordered-optimized',
                '--reverse', work / 'quads/reverse-normal', '--reverse-optimized', work / 'quads/reverse-optimized'], quad)
    ext = work / 'extensions'
    for start in range(0, 64108, 64):
        stop = min(start + 64, 64108)
        for mode, script, optimized in (('producer', 'extend_quads.py', False), ('checker', 'check_extensions.py', False), ('optimized', 'check_extensions.py', True)):
            yield task('extensions', f'extensions-{mode}-{start:05d}-{stop:05d}', script, optimized,
                       ['--quads', quad, '--start', str(start), '--stop', str(stop)], ext / mode / f'range-{start:05d}-{stop:05d}.json')
    prefixes = work / 'prefixes.json'
    yield task('extensions', 'merge-extensions', 'merge_extensions.py', False,
               ['--producer', ext / 'producer', '--checker', ext / 'checker', '--optimized', ext / 'optimized'], prefixes)
    for mode, algorithm, optimized in (('producer', 'producer', False), ('checker', 'checker', False), ('optimized', 'checker', True)):
        yield task('weighted', f'selection-{mode}', 'select_weighted_domain.py', optimized,
                   ['--input', prefixes, '--mode', algorithm], work / f'selected-{mode}.json')
    selected = work / 'selected-producer.json'
    weight = work / 'weighted'
    for start in range(0, 16880, 512):
        stop = min(start + 512, 16880)
        for mode, script, optimized in (('producer', 'weighted_columns.py', False), ('checker', 'check_weighted_columns.py', False), ('optimized', 'check_weighted_columns.py', True)):
            yield task('weighted', f'weighted-{mode}-{start:05d}-{stop:05d}', script, optimized,
                       ['--prefixes', selected, '--start', str(start), '--stop', str(stop)], weight / mode / f'range-{start:05d}-{stop:05d}.json')
    weighted = work / 'weighted.json'
    yield task('weighted', 'merge-weighted', 'merge_weighted_columns.py', False,
               ['--producer', weight / 'producer', '--checker', weight / 'checker', '--optimized', weight / 'optimized', '--domain', selected], weighted)
    for mode, algorithm, optimized in (('producer', 'producer', False), ('checker', 'checker', False), ('optimized', 'checker', True)):
        yield task('orbits', f'orbits-{mode}', 'weighted_orbits.py', optimized,
                   ['--input', weighted, '--mode', algorithm], work / f'canonical-{mode}.json')
    canonical = work / 'canonical-producer.json'
    tail = work / 'tails'
    for start in range(0, 21247, 500):
        stop = min(start + 500, 21247)
        producer = tail / 'producer' / f'range-{start:05d}-{stop:05d}.json'
        yield task('tails', f'tails-producer-{start:05d}-{stop:05d}', 'tail_cases.py', False,
                   ['--prefixes', selected, '--canonical', canonical, '--start', str(start), '--stop', str(stop)], producer)
        for mode, optimized in (('checker', False), ('optimized', True)):
            yield task('tails', f'tails-{mode}-{start:05d}-{stop:05d}', 'check_tail_cases.py', optimized,
                       ['--input', producer, '--canonical', canonical], tail / mode / producer.name)
    yield task('tails', 'merge-tails', 'merge_tail_cases.py', False,
               ['--producer', tail / 'producer', '--checker', tail / 'checker', '--optimized', tail / 'optimized', '--canonical', canonical], work / 'tails.json')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--work', type=Path)
    p.add_argument('--max-new-children', type=int, default=0)
    p.add_argument('--through', choices=PHASES, default='tails')
    p.add_argument('--barrier-file', action='append', type=Path, default=[])
    p.add_argument('--plan', action='store_true')
    o = p.parse_args()
    if o.max_new_children < 0 or (not o.plan and o.work is None):
        p.error('A work directory and nonnegative child limit are required')
    work = (o.work or Path('.')).resolve()
    source = Path(__file__).resolve().parent
    planned = [t for t in tasks(work) if PHASES.index(t[0]) <= PHASES.index(o.through)]
    if o.plan:
        print(json.dumps({'children_by_phase': {name: sum(t[0] == name for t in planned) for name in PHASES},
                          'whole_children': len(planned), 'guard_seconds': 20, 'threads': 1,
                          'quadruples': 64108, 'raw_extensions': 19488832, 'canonical_column_incidences': 21247}, sort_keys=True))
        return

    def barrier():
        if any(q.exists() for q in o.barrier_file):
            raise ValueError('Supplied operations pause/handover barrier; preserve')

    barrier()
    pins = {name: sha(source / name) for name in (*PROGRAMS, 'reproduce.py')}
    journal_path = work / 'journal.json'
    if work.exists():
        j = json.loads(journal_path.read_text())
        if j['source_pins'] != pins:
            raise ValueError('Source changed after recorded computation; preserve')
        if j['status'] == 'INCOMPLETE_NO_EXCLUSION' or any(e['status'] == 'STARTED' for e in j['children']):
            raise ValueError('First failed/interrupted input frozen; identical retry prohibited')
    else:
        work.mkdir(parents=True)
        j = {'agent': 'six-vdw-3', 'role': 'researcher', 'python': platform.python_version(), 'source_pins': pins,
             'guard_seconds': 20, 'threads': 1, 'status': 'PARTIAL_NO_NEW_CONCLUSION', 'children': []}
        save(journal_path, j)
    complete = {e['key']: e for e in j['children'] if e['status'] == 'COMPLETE'}
    env = os.environ.copy()
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
        env[name] = '1'
    added = 0
    for phase, key, script, optimized, values, out in planned:
        if key in complete:
            if not out.exists() or sha(out) != complete[key]['output_sha256']:
                raise ValueError('Previously completed output changed; preserve')
            continue
        barrier()
        normalized = []
        input_hashes = {}
        for flag, value in zip(values[::2], values[1::2]):
            if isinstance(value, Path):
                normalized.extend((flag, 'CONTENT_PINNED'))
                if value.is_dir():
                    input_hashes[flag] = {q.name: sha(q) for q in sorted(value.glob('*.json'))}
                else:
                    input_hashes[flag] = sha(value)
            else:
                normalized.extend((flag, value))
        identity = {'program_sha256': pins[script], 'inputs': input_hashes, 'arguments': normalized,
                    'optimized': optimized, 'guard_seconds': 20, 'threads': 1}
        fingerprint = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
        if any(e['input_fingerprint'] == fingerprint for e in j['children']):
            raise ValueError('Repeated mathematical input under another output/task name')
        out.parent.mkdir(parents=True, exist_ok=True)
        e = {'key': key, 'phase': phase, 'input': identity, 'input_fingerprint': fingerprint, 'status': 'STARTED'}
        j['children'].append(e)
        save(journal_path, j)
        begin = time.monotonic()
        args = [str(v) for v in values]
        command = [sys.executable] + (['-O'] if optimized else []) + [str(source / script), *args, '--output', str(out)]
        try:
            with (work / (key + '.stdout')).open('w') as stdout, (work / (key + '.stderr')).open('w') as stderr:
                result = subprocess.run(command, env=env, stdout=stdout, stderr=stderr, timeout=20)
            if result.returncode:
                raise ValueError(f'Child exit{result.returncode}; preserve stderr')
            comparison = []
            if key in ('selection-optimized', 'orbits-optimized'):
                prefix = 'selected' if key.startswith('selection') else 'canonical'
                comparison = [work / (prefix + '-producer.json'), work / (prefix + '-checker.json')]
            elif optimized and phase == 'quads':
                comparison = [out.parent.with_name(out.parent.name.replace('-optimized', '-normal')) / out.name]
            elif optimized and phase in ('extensions', 'weighted', 'tails'):
                comparison = [out.parent.with_name(mode) / out.name for mode in ('producer', 'checker')]
            if any(out.read_bytes() != q.read_bytes() for q in comparison):
                raise ValueError('Whole independent normal/optimized physical transcripts differ')
            e.update(status='COMPLETE', output_sha256=sha(out), output_bytes=out.stat().st_size)
        except BaseException as error:
            e.update(status='INCOMPLETE_NO_EXCLUSION', error=str(error))
            j['status'] = 'INCOMPLETE_NO_EXCLUSION'
            save(work / 'FIRST_FAILURE.json', e)
            raise
        finally:
            e.update(seconds=time.monotonic() - begin, peak_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
            save(journal_path, j)
        added += 1
        if added <= 2 or key.startswith('merge-'):
            print(json.dumps({'key': key, 'seconds': e['seconds'], 'children': len(j['children'])}), flush=True)
        if o.max_new_children and added >= o.max_new_children:
            return
    if o.through == 'tails':
        result = json.loads((work / 'tails.json').read_text())
        if result['survivors'] or result['incidences_by_balance'] != {'11/13': 908, '12/12': 20339}:
            raise ValueError('Claimed whole tail result differs; preserve')
    j['status'] = 'COMPLETE_' + o.through.upper()
    save(journal_path, j)
    print(j['status'], flush=True)


if __name__ == '__main__':
    main()
