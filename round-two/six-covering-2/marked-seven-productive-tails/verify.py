"""Regenerate every mathematical record in two modes with serial child guards."""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def require(ok, message):
    if not ok:
        raise ValueError(message)


def canonical(record):
    return json.dumps(record, sort_keys=True, separators=(',', ':')).encode()


def main():
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument('--scratch', type=Path, default=root / 'generated')
    args = parser.parse_args()
    work = args.scratch.resolve()
    work.mkdir(parents=True, exist_ok=True)
    expected = json.loads((root / 'expected.json').read_text())
    for name, digest in expected['source_sha256'].items():
        require(sha256((root / name).read_bytes()).hexdigest() == digest,
                'Computational source changed: ' + name)
    env = os.environ.copy()
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS', 'NUMEXPR_MAX_THREADS',
                 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
        env[name] = '1'
    runs = []
    both = []
    for mode, options in (('normal', ['-B']), ('O', ['-O', '-B'])):
        producer = work / ('BASE-' + mode + '.json')
        audit = work / ('audit-' + mode + '.json')
        records = {}
        commands = [('producer', 'generate.py', ['--out', str(producer)]),
                    ('literal_audit', 'audit.py', [str(producer), '--out', str(audit)]),
                    ('six_tail', 'six_tail.py', [])]
        for label, source, arguments in commands:
            start = time.monotonic()
            r = subprocess.run([sys.executable, *options, str(root / source), *arguments],
                               cwd=root, env=env, capture_output=True, text=True,
                               timeout=20, check=True)
            record = json.loads(producer.read_text()) if label == 'producer' else json.loads(r.stdout)
            if label == 'producer':
                record.pop('seconds')
            require(sha256(canonical(record)).hexdigest() == expected['whole_record_sha256'][label],
                    'Whole mathematical record differs: ' + label)
            records[label] = record
            runs.append({'mode': mode, 'record': label,
                         'seconds': time.monotonic() - start,
                         'whole_record_sha256': sha256(canonical(record)).hexdigest(),
                         'returncode': r.returncode})
        require(records['producer']['stages'][0]['complete'] and
                len(records['producer']['stages'][0]['rows']) == 270,
                'Initial entire raw-phase stage incomplete')
        require(records['literal_audit']['minimum_BASE_holes'] == 177 and
                records['six_tail']['maximum_six_tail_BASE_holes'] == 150,
                'Necessary-condition comparison changed')
        require(177 > 150 > 120, 'Five/six-tail comparison failed')
        both.append(records)
    require(both[0] == both[1], 'Every normal/O field must agree')
    print(json.dumps({'agent': 'six-covering-2', 'role': 'researcher',
                      'all_full_mathematical_records_equal': True, 'runs': runs,
                      'BASE_holes_lower_bound': 177, 'six_tail_capacity': 150,
                      'marked_essential_domain_productive_TAIL_lower_bound': 7,
                      'six_tail_abstract_model_is_full_cover': False,
                      'global_bound_changed': False, 'independent_reviewer': False,
                      'guard_seconds_per_child': 20, 'native_threads': 1,
                      'one_intensive_child_at_a_time': True}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
