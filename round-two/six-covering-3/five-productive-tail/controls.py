"""Semantic rejection controls for the full BASE-hole proof, not an enumeration."""
import argparse
from contextlib import redirect_stdout
from hashlib import sha256
import io
import json
from pathlib import Path
import runpy
import shutil
import os
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=Path, required=True)
    parser.add_argument('--scratch', type=Path, required=True)
    parser.add_argument('--group', choices=('metadata', 'records'), required=True)
    args = parser.parse_args()
    data, out = args.data.resolve(), args.scratch.resolve()
    out.mkdir(parents=True, exist_ok=True)
    checker = Path(__file__).with_name('check.py').resolve()
    files = ['scratch/four-tail-global-base-pilot.json',
             'scratch/four-tail-global-base-pilot.bin',
             'scratch/full-base-threshold-pilot/stage24.json',
             'scratch/full-base-threshold-pilot/stage24.bin',
             'scratch/full-base-threshold-pilot/stage36.json',
             'scratch/full-base-threshold-pilot/stage36.bin']
    names = (['wrong_early_cutoff', 'omitted_previous_tuple', 'duplicate_retained_tuple']
             if args.group == 'metadata'
             else ['changed_first_raw_phase', 'changed_last_raw_upper', 'truncated_final_stream'])
    started = time.monotonic()
    results = []
    for name in names:
        case = out/name
        for relative in files:
            target = case/relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(data/relative, target)
        if args.group == 'metadata':
            target = case/'scratch/full-base-threshold-pilot/stage24.json'
            record = json.loads(target.read_text())
            if name == 'wrong_early_cutoff':
                record['target'] = 1290
            elif name == 'omitted_previous_tuple':
                record['previous_tuples'].pop()
            else:
                record['retained_tuples'][1] = record['retained_tuples'][0]
            target.write_text(json.dumps(record))
            expected = ('Omitted or altered previous complete frontier'
                        if name == 'omitted_previous_tuple'
                        else 'Complete stage metadata/frontier differs')
        else:
            target = case/('scratch/four-tail-global-base-pilot.bin'
                           if name == 'changed_first_raw_phase'
                           else 'scratch/full-base-threshold-pilot/stage36.bin')
            raw = bytearray(target.read_bytes())
            if name == 'changed_first_raw_phase':
                raw[0] ^= 1
                expected = 'PhysicalAP field mismatch at record0'
            elif name == 'changed_last_raw_upper':
                raw[-2] ^= 1
                expected = 'PhysicalAP field mismatch at record287'
            else:
                raw = raw[:-76]
                expected = 'Omitted/extra/truncated rawrecord'
            target.write_bytes(raw)
        previous_cwd = Path.cwd()
        failure = None
        try:
            os.chdir(case)
            with redirect_stdout(io.StringIO()):
                runpy.run_path(str(checker), run_name='__main__')
        except ValueError as error:
            failure = str(error)
        finally:
            os.chdir(previous_cwd)
        if failure != expected:
            raise ValueError('Damage '+name+' was not rejected for its intended reason: '+str(failure))
        results.append({'damage': name, 'rejected': True, 'reason': failure})
    print(json.dumps({'group': args.group, 'damages': results,
                      'checker_sha256': sha256(checker.read_bytes()).hexdigest(),
                      'seconds': time.monotonic()-started}, indent=2))


if __name__ == '__main__':
    main()
