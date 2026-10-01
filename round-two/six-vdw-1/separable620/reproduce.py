"""Source-only exact replay. Never creates or edits the frozen expected file."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(work):
    source = Path(__file__).absolute().parent
    expected_path = source / 'expected.json'
    require(expected_path.is_file(), 'a pre-existing frozen expected.json is required')
    frozen = json.loads(expected_path.read_text())
    work = work.absolute()
    work.mkdir(parents=True, exist_ok=True)
    receipts = work / 'receipts'
    receipts.mkdir(exist_ok=True)
    env = dict(os.environ)
    for name in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS']:
        env[name] = '1'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    python = str(Path(sys.executable).absolute())
    index = 0
    started = time.monotonic()

    def call(argv, failure=False):
        nonlocal index
        state = env.get('DISCOVERY_RESEARCH_TEAM_ROOT')
        if state:
            require(not any((Path(state) / n).exists() for n in ['PAUSED.json', 'HANDOVER.json']), 'operational barrier')
        index += 1
        begin = time.monotonic()
        command = list(map(str, argv))
        try:
            answer = subprocess.run(command, env=env, text=True, capture_output=True, timeout=35)
        except subprocess.TimeoutExpired as error:
            (receipts / f'{index:03}.json').write_text(json.dumps({'command': command, 'status': 'INCOMPLETE_TIMEOUT',
                'elapsed_seconds': time.monotonic()-begin}, indent=2)+'\n')
            raise RuntimeError('incomplete stage; no mathematical exclusion') from error
        receipt = {'command': command, 'exit': answer.returncode, 'stdout': answer.stdout, 'stderr': answer.stderr,
                   'elapsed_seconds': time.monotonic()-begin}
        (receipts / f'{index:03}.json').write_text(json.dumps(receipt, indent=2)+'\n')
        require((answer.returncode != 0) if failure else (answer.returncode == 0),
                'unexpected child status: '+json.dumps(receipt))
        return answer.stdout

    flags = ['-std=c++17', '-Wall', '-Wextra', '-pedantic']
    producer = work / 'enumerate'
    checker = work / 'check_walks'
    for name, output in [('enumerate.cpp', producer), ('check_walks.cpp', checker)]:
        call(['g++', '-O2', *flags, source / name, '-o', output])
    versions = {'python': sys.version, 'compiler': call(['g++', '--version']).splitlines()[0]}
    normal = work / 'normal'
    optimized = work / 'optimized'
    normal.mkdir(exist_ok=True)
    optimized.mkdir(exist_ok=True)
    call([python, '-B', source / 'census.py', normal])
    call([python, '-O', '-B', source / 'census.py', optimized])
    require((normal / 'rows.json').read_bytes() == (optimized / 'rows.json').read_bytes(), 'normal/-O complete row bytes differ')
    a = call([python, '-B', source / 'check_rows.py', normal / 'rows.json'])
    b = call([python, '-O', '-B', source / 'check_rows.py', normal / 'rows.json'])
    require(json.loads(a) == json.loads(b), 'normal/-O literal row audits differ')
    produced = call([producer, normal])
    checked = call([checker, normal])
    controls = call([checker, '--controls'])
    native_guards = 0
    good = (normal / 'case10.bin').read_bytes()
    modifications = {}
    modifications['omitted-record'] = good[:-9]
    modifications['truncated-record'] = good[:-1]
    modifications['duplicate-record'] = good[:9] + good[:9] + good[18:]
    modifications['extra-record'] = good + good[:9]
    altered = bytearray(good); altered[8] ^= 1; modifications['wrong-color'] = bytes(altered)
    altered = bytearray(good); altered[6:8] = b'\0\0'; modifications['zero-step'] = bytes(altered)
    altered = bytearray(good); altered[3] |= 128; modifications['outside-field'] = bytes(altered)
    altered = bytearray(good); altered[4:6] = b'\xff\xff'; modifications['outside-start'] = bytes(altered)
    modifications['missing-case'] = None
    for label, damaged in modifications.items():
        directory = work / 'damages' / label
        directory.mkdir(parents=True, exist_ok=True)
        for path in normal.glob('case*.bin'):
            target = directory / path.name
            target.unlink(missing_ok=True)
            target.symlink_to(path.absolute())
        if damaged is None:
            (directory / 'case8.bin').unlink()
        else:
            target = directory / 'case10.bin'; target.unlink(); target.write_bytes(damaged)
        call([checker, directory], failure=True)
        native_guards += 1
    row_guards = 0
    original = json.loads((normal / 'rows.json').read_text())
    for label in ['omitted-row', 'zero-step', 'omitted-orbit-member', 'wrong-signature', 'wrong-author']:
        bad = json.loads(json.dumps(original))
        if label == 'omitted-row': bad['rejection_records'].pop()
        elif label == 'zero-step': bad['rejection_records'][0][2] = 0
        elif label == 'omitted-orbit-member': bad['orbits'][-1]['members'].pop()
        elif label == 'wrong-signature': bad['orbits'][0]['patterns'].pop()
        elif label == 'wrong-author': bad['author'] = 'incorrect'
        path = work / 'damages' / (label + '.json')
        path.write_text(json.dumps(bad)+'\n')
        for option in [[], ['-O']]:
            call([python, *option, '-B', source / 'check_rows.py', path], failure=True)
            row_guards += 1
    # Full optimized/native versus address+undefined sanitizer coverage;
    # every regenerated certificate byte is compared, rather than only totals.
    sanitized = work / 'sanitized'
    sanitized.mkdir(exist_ok=True)
    sanitized_outputs = {}
    for name in ['enumerate', 'check_walks']:
        executable = work / (name + '-sanitized')
        call(['g++', '-O1', '-g', '-fsanitize=address,undefined', '-fno-omit-frame-pointer',
              *flags, source / (name + '.cpp'), '-o', executable])
        sanitized_outputs[name] = call([executable, sanitized if name == 'enumerate' else normal])
    require(sanitized_outputs['enumerate'] == produced and sanitized_outputs['check_walks'] == checked,
            'sanitized/optimized exact outputs differ')
    for file in normal.glob('case*.bin'):
        require(file.read_bytes() == (sanitized / file.name).read_bytes(), 'sanitized full evidence differs: '+file.name)
    actual = {'rows_sha256': sha(normal / 'rows.json'),
              'record_files': {p.name: {'bytes': p.stat().st_size, 'sha256': sha(p)} for p in sorted(normal.glob('case*.bin'))},
              'producer': produced, 'checker': checked, 'row_audit': json.loads(a),
              'controls': controls, 'native_corruption_rejections': native_guards,
              'python_corruption_rejections_normal_and_optimized': row_guards}
    (work / 'actual.json').write_text(json.dumps(actual, sort_keys=True, indent=2)+'\n')
    require(actual == frozen, 'complete deterministic evidence differs from the pre-existing frozen fixture')
    report = {'author': 'six-vdw-1', 'role': 'researcher', 'status': 'COMPLETE_AUTHOR_CHECKED_SEPARABLE620_EXCLUSION',
              'frozen_expected_existed_before_replay': True, 'complete_frozen_evidence_agreement': True,
              'independent_literal_records': sum(v['bytes']//9 for v in actual['record_files'].values()),
              'record_bytes': sum(v['bytes'] for v in actual['record_files'].values()),
              'versions': versions, 'sequential_children': index, 'child_deadline_seconds': 35, 'threads': 1,
              'elapsed_seconds': time.monotonic()-started,
              'child_peak_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              'proof_limit': 'Only arbitrary F31 XOR C20 products; no unrestricted period620 or interval exclusion, new W bound, optimal cutoff or independent peer verdict.'}
    (work / 'verification.json').write_text(json.dumps(report, sort_keys=True, indent=2)+'\n')
    print(json.dumps(report, sort_keys=True), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    run(parser.parse_args().work)
