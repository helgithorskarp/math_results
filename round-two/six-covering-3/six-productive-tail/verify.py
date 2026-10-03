"""Source-only isolated replay. Each arithmetic child retains its 20s guard."""
from pathlib import Path
from hashlib import sha256
import argparse
import contextlib
import io
import json
import os
import resource
import runpy
import shutil
import struct
import subprocess
import sys
import time


def require(test, message):
    if not test:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text())


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def mathematical(value):
    return {key: item for key, item in value.items() if key != 'seconds'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, default=Path('scratch/six-tail-source-replay'))
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    manifest = read(source / 'source-manifest.json')
    actual = {p.name for p in source.iterdir() if p.is_file() and p.name != 'source-manifest.json'}
    require(actual == set(manifest['files']), 'Source inventory differs')
    for name, expected in manifest['files'].items():
        raw = (source / name).read_bytes()
        require(len(raw) == expected['bytes'] and sha256(raw).hexdigest() == expected['sha256'],
                'Source whole bytes differ: ' + name)
    expected = read(source / 'expected.json')
    work = args.work.resolve()
    require(not work.exists(), 'Replay work path already exists; preserve it and choose a new path')
    work.mkdir(parents=True)
    scratch = work / 'scratch'
    scratch.mkdir()
    for name in expected['executed_sources']:
        shutil.copyfile(source / name, scratch / name)
    env = os.environ.copy()
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                'BLIS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        env[key] = '1'
    records = []
    started = time.monotonic()

    def run(name, script, arguments=(), optimized=False):
        command = [sys.executable, *(['-O'] if optimized else []), '-B', 'scratch/' + script, *arguments]
        before = time.monotonic()
        try:
            result = subprocess.run(command, cwd=work, env=env, capture_output=True, text=True, timeout=20)
        except subprocess.TimeoutExpired as error:
            raise RuntimeError('INCOMPLETE_TIMEOUT_NO_EXCLUSION: ' + name) from error
        (scratch / (name + '-stdout.json')).write_text(result.stdout)
        (scratch / (name + '-stderr.txt')).write_text(result.stderr)
        require(result.returncode == 0 and not result.stderr, 'Incomplete/failed child, no exclusion: ' + name)
        row = {'name': name, 'seconds': time.monotonic() - before,
               'exit': result.returncode, 'guard_seconds': 20, 'threads': 1}
        records.append(row)
        print(json.dumps(row), flush=True)
        return result.stdout

    def controls(name, script, data, count, optimized=False):
        # The existing control harness itself is orchestration: each checker
        # subprocess inside it is serial, thread1, and guarded at20s. Do not
        # put a larger arithmetic-child guard around this loop.
        out = 'scratch/' + name
        argv = [script, '--data', data, '--out', out, *(['--optimized'] if optimized else [])]
        old_argv, old_cwd = sys.argv, Path.cwd()
        capture = io.StringIO()
        before = time.monotonic()
        try:
            sys.argv = argv
            os.chdir(work)
            with contextlib.redirect_stdout(capture):
                runpy.run_path(str(scratch / script), run_name='__main__')
        finally:
            sys.argv = old_argv
            os.chdir(old_cwd)
            (scratch / (name + '-stdout.jsonl')).write_text(capture.getvalue())
        result = read(work / out / 'verification.json')
        verdicts = [{k: v for k, v in row.items() if k != 'seconds'} for row in result['damages']]
        require(result['all_intended_reason_rejections'] and len(verdicts) == count,
                'Semantic controls incomplete: ' + name)
        require(verdicts == expected['controls'][script], 'Full damage verdicts differ: ' + name)
        require(result['guard_seconds_per_child'] == 20 and result['threads'] == 1 and result['one_CPU_child'],
                'Semantic-control resource contract changed')
        for row in result['damages']:
            records.append({'name': name + '/' + row['damage'], 'seconds': row['seconds'],
                            'exit': row['exit'], 'guard_seconds': 20, 'threads': 1})
        print(json.dumps({'name': name, 'complete_damages': count,
                          'orchestration_seconds': time.monotonic() - before}), flush=True)

    run('root-seed', 'published9859-generate-root.py')
    require(digest(mathematical(read(scratch / 'four-tail-global-base-pilot.json'))) == expected['producer_math_sha256']['seed'],
            'Complete seed fields differ')
    raw = (scratch / 'four-tail-global-base-pilot.bin').read_bytes()
    require(len(raw) == 270 * 76 and sha256(raw).hexdigest() == expected['root_stream_sha256'],
            'Regenerated entire raw-root stream differs')
    maths = {}
    producers = {}
    for optimized in (False, True):
        mode = 'optimized' if optimized else 'normal'
        path = 'scratch/root48-' + mode
        run('quotient-producer-' + mode, 'root48-generate.py', ['--out', path], optimized)
        producer = mathematical(read(work / path / 'result.json'))
        require(digest(producer) == expected['producer_math_sha256']['quotient'], 'Complete quotient producer fields differ')
        ap = read(source / 'quotient-certificate.json')
        observed = mathematical(json.loads(run('quotient-check-' + mode, 'root48-check.py', ['--data', path], optimized)))
        require(observed == ap, 'Entire quotient AP fields differ')
        controls('quotient-damages-' + mode, 'root48-controls.py', path, 8, optimized)
        maths['quotient-' + mode] = observed
        producers['quotient-' + mode] = producer
    require(maths['quotient-normal'] == maths['quotient-optimized']
            and producers['quotient-normal'] == producers['quotient-optimized'], 'Quotient normal/O mismatch')
    quotient = maths['quotient-normal']
    metadata = {'mathematical': quotient, 'full_math_sha256': digest(quotient),
                'complete_normal_optimized_AP_fields_equal': True, 'all_semantic_controls_pass': True,
                'root_input_sha256': sha256(raw).hexdigest()}
    (scratch / 'root48-verified.json').write_text(json.dumps(metadata, indent=2) + '\n')

    # Literal identity entries from the newly audited full phase stream.
    shared = read(source / 'shared-anchor-corollary.json')
    labels = producers['quotient-normal']['all_original_modulus_labels']
    stream = (scratch / 'root48-normal/original-phase-maps.bin').read_bytes()
    offset = identities = non9 = 0
    for generator in range(8):
        for label in labels:
            values = struct.unpack_from('<' + str(label) + 'H', stream, offset)
            offset += 2 * label
            if label in shared['full1728group_fixes_all_phases_of_labels']:
                require(values == tuple(range(label)), 'Shared anchor phase moved')
                identities += label
            if label == 9:
                require(values[0] == 0, 'Shared9 anchor moved')
                identities += 1
            if label == 10:
                require(values[1] == 1, 'Shared10 anchor moved')
                identities += 1
            if generator < 5 and label % 9:
                require(values == tuple(range(label)), 'Non9 phase moved by mod9 subgroup')
                non9 += label
    require(offset == len(stream) and identities == shared['complete_identity_anchor_phase_checks'] == 896
            and non9 == shared['complete_mod9_non9_identity_phase_entries'] == 60340,
            'Entire shared-anchor identity inventory differs')
    require([label for label in labels if label % 9] == shared['mod9_subgroup_fixes_every_phase_of_non9_original_labels'],
            'Non9 original-label inventory differs')

    for optimized in (False, True):
        mode = 'optimized' if optimized else 'normal'
        path = 'scratch/root48-base-' + mode
        run('BASE-producer-' + mode, 'root48-base-generate.py', ['--out', path], optimized)
        producer = mathematical(read(work / path / 'result.json'))
        require(digest(producer) == expected['producer_math_sha256']['BASE'], 'Complete BASE producer fields differ')
        observed = mathematical(json.loads(run('BASE-check-' + mode, 'root48-base-check.py', ['--data', path], optimized)))
        require(observed == read(source / 'BASE162-certificate.json'), 'Entire BASE AP fields differ')
        controls('BASE-damages-' + mode, 'root48-base-controls.py', path, 7, optimized)
        maths['BASE-' + mode], producers['BASE-' + mode] = observed, producer
        path = 'scratch/five-footprint-' + mode
        run('five-producer-' + mode, 'five-tail-footprint-pilot.py', ['--out', path], optimized)
        producer = mathematical(read(work / path / 'result.json'))
        require(digest(producer) == expected['producer_math_sha256']['five'], 'Complete five-capacity producer fields differ')
        observed = mathematical(json.loads(run('five-check-' + mode, 'check-five-tail-footprint.py', ['--data', path], optimized)))
        require(observed == read(source / 'five-capacity-certificate.json'), 'Entire five-capacity AP fields differ')
        maths['five-' + mode], producers['five-' + mode] = observed, producer
        for script, certificate in [('root48-live-prefix-map.py', 'live-Q15-certificate.json'),
                                    ('three-pair-capacity-control.py', 'three-pair-capacity-certificate.json')]:
            observed = mathematical(json.loads(run(script + '-' + mode, script, optimized=optimized)))
            require(observed == read(source / certificate), 'Entire literal corollary fields differ: ' + script)
            maths[script + '-' + mode] = observed
    for name in ('BASE', 'five', 'root48-live-prefix-map.py', 'three-pair-capacity-control.py'):
        require(maths[name + '-normal'] == maths[name + '-optimized'], 'Entire normal/O fields differ: ' + name)
    for name in ('BASE', 'five'):
        require(producers[name + '-normal'] == producers[name + '-optimized'], 'Entire normal/O producer fields differ')
    result = {'agent': 'six-covering-3', 'role': 'researcher', 'status': 'COMPLETE_SOURCE_ONLY_ISOLATED_REPLAY',
              'Python': sys.version.split()[0], 'all_source_manifest_whole_bytes_equal': True,
              'all_frozen_producer_and_AP_fields_equal': True, 'semantic_damages': 30,
              'complete_shared_anchor_identity_entries': identities + non9,
              'mathematical_sha256': {key: digest(value) for key, value in maths.items()},
              'children': records, 'max_child_seconds': max(row['seconds'] for row in records),
              'RSS_KiB_on_Linux': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              'seconds': time.monotonic() - started, 'guard_seconds_per_arithmetic_child': 20,
              'threads': 1, 'one_CPU_intensive_child_at_a_time': True,
              'productive_original_TAIL_at_least': 6, 'exactly_six_occupied_parents': 2,
              'formalized': False, 'external_review': False, 'global_Lmin8_bound_improved': False,
              'fullP_exclusion_claimed': False, 'new_covering_witness_claimed': False}
    (work / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: value for key, value in result.items() if key != 'children'}, indent=2), flush=True)


if __name__ == '__main__':
    main()
