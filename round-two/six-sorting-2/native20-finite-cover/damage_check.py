"""Reject nine damaged generated certificates in normal and optimized modes.

Run after run.py. Each case has its own private overlay; original evidence
is never changed. This audit tests checker guards, not mathematical coverage.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def change(data, case):
    if case == 'pre6_missing_history':
        data['all_event_words'].pop()
    elif case == 'preparation_missing_function':
        next(group for group in data if group['n'] == 4)['functions'].pop()
    elif case == 'tf_missing_composition':
        data['TF'].pop()
    elif case == 'joint_wrong_length':
        data['joint_roots'][0]['prefix_length'] += 1
    elif case == 'post_wrong_budget':
        data['roots'][0]['suffix_budget'] += 1
    elif case == 'constant_wrong_R':
        witness = min((w for r in data['sufficient_records'] for w in r['selected']),
                      key=lambda w: tuple(w['original']))
        witness['R'] += 1
    elif case == 'nested_wrong_root_cover':
        data['sufficient_records'][0]['root'] = data['sufficient_records'][1]['root']
    else:
        witness = next(w for r in data['sufficient_records']
                       for w in r['selected_domains'] if not w['constant_only'])
        if case == 'nested_wrong_inner_bound':
            witness['inner_bound'] += 1
        elif case == 'nested_wrong_pruning_function':
            witness['pruning']['retained_prefix'][0].reverse()
        else:
            raise ValueError('unknown damage case')


CASES = [
    ('pre6_missing_history', 'pre6-cover.json', 'phase_verify', [],
     'full event history cover differs'),
    ('preparation_missing_function', 'preparation-functions.json', 'phase_verify', [],
     'preparation function set not closed'),
    ('tf_missing_composition', 'tf-cover.json', 'phase_verify', [],
     'preparation function composition omitted'),
    ('joint_wrong_length', 'joint-cover.json', 'images_verify', ['joint'],
     'joint prefix length differs'),
    ('post_wrong_budget', 'postjoint-cover.json', 'images_verify', ['post'],
     'nine-root budget differs'),
    ('constant_wrong_R', 'constant-screen-0-135.json', 'constants_verify', [],
     'numeric semantic record differs'),
    ('nested_wrong_root_cover', 'nested-screen-0-20.json', 'nested_verify', ['0', '20'],
     'nested root cover differs from exact constant-stage remainder'),
    ('nested_wrong_inner_bound', 'nested-screen-0-20.json', 'nested_verify', ['0', '20'],
     'inner exact records/leaves/bounds differ'),
    ('nested_wrong_pruning_function', 'nested-screen-0-20.json', 'nested_verify', ['0', '20'],
     'complete carrier/pruning fields differ'),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence-dir', required=True)
    parser.add_argument('--output-dir', required=True)
    args = parser.parse_args()
    evidence = Path(args.evidence_dir).resolve()
    output = Path(args.output_dir).resolve()
    need(output != evidence and not output.is_relative_to(evidence),
         'Keep audit overlays outside original evidence')
    output.mkdir(parents=True, exist_ok=True)
    need(json.loads((evidence / 'checks.json').read_text())['status'] ==
         'NATIVE20_COMPLETE_SIZE44_EXCLUSION_VERIFIED', 'Complete evidence required')
    rows = []
    for case, filename, checker, extra, reason in CASES:
        overlay = output / case
        overlay.mkdir()  # Refuse to reuse an earlier overlay.
        for source in evidence.glob('*.json'):
            target = overlay / source.name
            if source.stat().st_size < 20000 or source.name.startswith('verify-'):
                shutil.copyfile(source, target)
            else:
                target.symlink_to(source)
        target = overlay / filename
        data = json.loads((evidence / filename).read_text())
        change(data, case)
        target.unlink()
        target.write_text(json.dumps(data, separators=(',', ':')) + '\n')
        damaged_sha = hashlib.sha256(target.read_bytes()).hexdigest()
        if filename in ('pre6-cover.json', 'preparation-functions.json'):
            # Re-pin the mutation, testing mathematics beyond a file-hash guard.
            pin_path = overlay / 'initial-artifacts.json'
            pins = json.loads(pin_path.read_text())
            pins[filename] = damaged_sha
            pin_path.write_text(json.dumps(pins) + '\n')
        del data
        env = dict(os.environ, NATIVE20_WORKDIR=str(overlay), OPENBLAS_NUM_THREADS='1',
                   OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')
        for optimized in (False, True):
            command = [sys.executable] + (['-O'] if optimized else []) + [
                '-B', str(HERE / (checker + '.py')), *extra]
            start = time.monotonic()
            result = subprocess.run(command, capture_output=True, text=True,
                                    env=env, timeout=55)
            log = result.stdout + result.stderr
            mode = 'optimized' if optimized else 'normal'
            (overlay / (mode + '.log')).write_text(log)
            need(result.returncode != 0 and 'ValueError: ' + reason in log,
                 'Expected explicit rejection failed: ' + case + ' / ' + mode)
            row = {'case': case, 'mode': mode, 'checker': checker, 'args': extra,
                   'file': filename, 'damaged_sha256': damaged_sha,
                   'reason': reason, 'returncode': result.returncode,
                   'seconds': time.monotonic() - start}
            rows.append(row)
            print(json.dumps(row, sort_keys=True), flush=True)
    summary = {'agent': 'six-sorting-2', 'role': 'researcher',
               'status': 'ALL_NINE_DAMAGES_REJECTED_IN_BOTH_MODES',
               'cases': 9, 'checks': rows,
               'boundary': 'Guard audit only; complete positive checks establish the mathematical cover.'}
    (output / 'checks.json').write_text(json.dumps(summary, indent=2) + '\n')


if __name__ == '__main__':
    main()
