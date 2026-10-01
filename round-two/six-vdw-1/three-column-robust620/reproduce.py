"""Source-only replay; the frozen expected file must exist before any stage."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

THIRDS = [2, 3, 4, 5, 6, 12]
MASKS = [8, 10, 12, 16, 20, 34, 72]
CASES = [(t, m) for t in THIRDS for m in MASKS]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(work):
    source = Path(__file__).absolute().parent
    require((source / 'expected.json').is_file(), 'pre-existing frozen expected.json required')
    frozen = json.loads((source / 'expected.json').read_text())
    work = work.absolute(); work.mkdir(parents=True, exist_ok=True)
    receipts = work / 'receipts'; receipts.mkdir(exist_ok=True)
    env = dict(os.environ)
    for name in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS']:
        env[name] = '1'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    python = str(Path(sys.executable).absolute())
    index = 0; begin_all = time.monotonic()

    def call(argv, failure=False):
        nonlocal index
        state = env.get('DISCOVERY_RESEARCH_TEAM_ROOT')
        if state:
            require(not any((Path(state)/n).exists() for n in ['PAUSED.json', 'HANDOVER.json']), 'operational barrier')
        index += 1; begin = time.monotonic(); command = list(map(str, argv))
        try:
            answer = subprocess.run(command, env=env, text=True, capture_output=True, timeout=35)
        except subprocess.TimeoutExpired as error:
            (receipts/f'{index:03}.json').write_text(json.dumps({'command': command,
                'status': 'INCOMPLETE_TIMEOUT', 'elapsed_seconds': time.monotonic()-begin}, indent=2)+'\n')
            raise RuntimeError('incomplete stage; no mathematical exclusion') from error
        receipt = {'command': command, 'exit': answer.returncode, 'stdout': answer.stdout,
                   'stderr': answer.stderr, 'elapsed_seconds': time.monotonic()-begin}
        (receipts/f'{index:03}.json').write_text(json.dumps(receipt, indent=2)+'\n')
        require(answer.returncode != 0 if failure else answer.returncode == 0,
                'unexpected child status: '+json.dumps(receipt))
        return answer.stdout

    flags = ['-std=c++17', '-Wall', '-Wextra', '-pedantic']
    producer = work/'enumerate'; checker = work/'check'
    for name, output in [('enumerate.cpp', producer), ('check.cpp', checker)]:
        call(['g++', '-O2', *flags, source/name, '-o', output])
    versions = {'python': sys.version, 'compiler': call(['g++', '--version']).splitlines()[0]}
    normal = work/'normal'; optimized = work/'optimized'
    normal.mkdir(exist_ok=True); optimized.mkdir(exist_ok=True)
    for name, datafile in [('census.py', 'rows.json'), ('orbits.py', 'triples.json')]:
        call([python, '-B', source/name, normal])
        call([python, '-O', '-B', source/name, optimized])
        require((normal/datafile).read_bytes() == (optimized/datafile).read_bytes(), 'normal/-O full census differs')
    audited = {}
    for name, datafile in [('check_rows.py', 'rows.json'), ('check_orbits.py', 'triples.json')]:
        first = json.loads(call([python, '-B', source/name, normal/datafile]))
        second = json.loads(call([python, '-O', '-B', source/name, normal/datafile]))
        require(first == second, 'normal/-O independent census audit differs')
        audited[name] = first
    arithmetic = json.loads(call([python, '-B', source/'check_arithmetic.py']))
    require(arithmetic == json.loads(call([python, '-O', '-B', source/'check_arithmetic.py'])), 'arithmetic normal/-O differs')
    produced = call([producer, normal]); checked = []
    names = {f'case{t}-{m}.bin' for t, m in CASES}
    require({p.name for p in normal.glob('case*.bin')} == names, 'wrong case-file partition')
    for t in THIRDS:
        for m in MASKS:
            checked.append(call([checker, normal, t, m]))
        print('literal/domain cover checked for third='+str(t), flush=True)
    controls = call([checker, '--controls'])
    native_guards = 0
    good = (normal/'case2-10.bin').read_bytes()
    modifications = {'omitted-record': good[:-9], 'truncated-record': good[:-1],
                     'duplicate-record': good[:9]+good[:9]+good[18:], 'extra-record': good+good[:9],
                     'missing-case': None}
    for label, position, payload in [('wrong-color', 8, bytes([good[8]^1])), ('zero-step', 6, b'\0\0'),
                                    ('outside-start', 4, b'\xff\xff')]:
        bad = bytearray(good); bad[position:position+len(payload)] = payload; modifications[label] = bytes(bad)
    bad = bytearray(good); bad[3] |= 128; modifications['outside-field'] = bytes(bad)
    bad = bytearray(good); bad[0] |= 1; modifications['undefined-hole-bit'] = bytes(bad)
    bad = bytearray(good); bad[4:8] = b'\0\0\2\0'; modifications['touch-exception'] = bytes(bad)
    for label, payload in modifications.items():
        directory = work/'damages'/label; directory.mkdir(parents=True, exist_ok=True)
        for p in normal.glob('case*.bin'):
            target = directory/p.name; target.unlink(missing_ok=True); target.symlink_to(p.absolute())
        if payload is None:
            (directory/'case2-8.bin').unlink(); t, m = 2, 8
        else:
            target = directory/'case2-10.bin'; target.unlink(); target.write_bytes(payload); t, m = 2, 10
        call([checker, directory, t, m], failure=True); native_guards += 1
    python_guards = {'rows': 0, 'triples': 0}
    for family in python_guards:
        original = json.loads((normal/(family+'.json')).read_text())
        labels = ['omitted-row', 'zero-step', 'omitted-member', 'wrong-signature', 'wrong-author'] if family == 'rows' else \
                 ['omitted-class', 'omitted-member', 'duplicate-member', 'wrong-representative', 'wrong-order']
        for label in labels:
            bad = json.loads(json.dumps(original))
            if family == 'rows':
                if label == 'omitted-row': bad['rejection_records'].pop()
                elif label == 'zero-step': bad['rejection_records'][0][2] = 0
                elif label == 'omitted-member': bad['orbits'][-1]['members'].pop()
                elif label == 'wrong-signature': bad['orbits'][0]['patterns'].pop()
                elif label == 'wrong-author': bad['author'] = 'incorrect'
                program = 'check_rows.py'
            else:
                if label == 'omitted-class': bad['classes'].pop()
                elif label == 'omitted-member': bad['classes'][0]['members'].pop()
                elif label == 'duplicate-member': bad['classes'][0]['members'].append(bad['classes'][0]['members'][0])
                elif label == 'wrong-representative': bad['classes'][-1]['holes'][-1] = 13
                elif label == 'wrong-order': bad['affine_group_order'] = 929
                program = 'check_orbits.py'
            path = work/'damages'/(family+'-'+label+'.json'); path.write_text(json.dumps(bad)+'\n')
            for option in [[], ['-O']]:
                call([python, *option, '-B', source/program, path], failure=True); python_guards[family] += 1
    sanitized = work/'sanitized'; sanitized.mkdir(exist_ok=True)
    sp = work/'enumerate-sanitized'; sc = work/'check-sanitized'
    for name, output in [('enumerate.cpp', sp), ('check.cpp', sc)]:
        call(['g++', '-O1', '-g', '-fsanitize=address,undefined', '-fno-omit-frame-pointer', *flags, source/name, '-o', output])
    require(call([sp, sanitized]) == produced, 'sanitized producer output differs')
    for p in normal.glob('case*.bin'):
        require(p.read_bytes() == (sanitized/p.name).read_bytes(), 'sanitized complete record bytes differ')
    sanitized_checks = []
    for t in THIRDS:
        for m in MASKS:
            sanitized_checks.append(call([sc, normal, t, m]))
        print('sanitized literal/domain cover checked for third='+str(t), flush=True)
    require(sanitized_checks == checked, 'sanitized exact entry-coverage metadata differs')
    actual = {'rows_sha256': sha(normal/'rows.json'), 'triples_sha256': sha(normal/'triples.json'),
              'record_files': {p.name: {'bytes': p.stat().st_size, 'sha256': sha(p)} for p in sorted(normal.glob('case*.bin'))},
              'producer': produced, 'checker': ''.join(checked), 'audits': audited, 'arithmetic': arithmetic,
              'controls': controls, 'native_corruption_rejections': native_guards,
              'python_corruption_rejections_normal_and_optimized': python_guards}
    (work/'actual.json').write_text(json.dumps(actual, sort_keys=True, indent=2)+'\n')
    require(actual == frozen, 'entire deterministic evidence differs from the pre-existing frozen fixture')
    report = {'author': 'six-vdw-1', 'role': 'researcher', 'status': 'COMPLETE_AUTHOR_CHECKED_THREE_COLUMN_ROBUST620_LEMMA',
              'frozen_expected_existed_before_replay': True, 'complete_frozen_evidence_agreement': True,
              'cases': len(CASES), 'independent_literal_records': sum(v['bytes']//9 for v in actual['record_files'].values()),
              'record_bytes': sum(v['bytes'] for v in actual['record_files'].values()), 'versions': versions,
              'sequential_children': index, 'child_deadline_seconds': 35, 'threads': 1,
              'elapsed_seconds': time.monotonic()-begin_all,
              'child_peak_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              'proof_limit': 'Only common-row products repaired in at most three mod31 classes; no four-column/full-period620/interval exclusion or new W bound, existence, optimal cutoff or independent peer verdict.'}
    (work/'verification.json').write_text(json.dumps(report, sort_keys=True, indent=2)+'\n')
    print(json.dumps(report, sort_keys=True), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--work', type=Path, required=True)
    run(parser.parse_args().work)
