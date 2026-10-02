"""Reject damaged full functions, incomplete covers and wrong original labels.

Run after run.py, with no other computation using this work directory.
Only ignored generated data are changed temporarily and restored exactly.
No failure caused by a timeout or unexpected error is counted as a rejection.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from controls import operations_allow

ROOT = Path(__file__).resolve().parent
WORK = ROOT/'work'


def need(test, message):
    if not test:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def main():
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                 'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        os.environ[name] = '1'
    functions_path = WORK/'branch00.json'
    selected_path = WORK/'residual-constant00.json'
    originals = {p: p.read_bytes() for p in (functions_path, selected_path)}
    functions = json.loads(originals[functions_path])
    selected = json.loads(originals[selected_path])
    controls = []
    bad = copy.deepcopy(functions)
    bad['functions'][0]['full_six_variable_columns'][0] ^= 1
    controls.append(('wrong-full-function', functions_path, bad,
                     'verify_preparations.py', [0, 1],
                     'Whole six-input columns differ from scalar function'))
    bad = copy.deepcopy(functions)
    bad['functions'].pop()
    controls.append(('missing-preparation-function', functions_path, bad,
                     'verify_preparations.py', [0, 1],
                     'Complete independent function set differs'))
    bad = copy.deepcopy(selected)
    offset = next(i for i, r in enumerate(bad['cases']) if r['constant16_exceeds44'])
    bad['cases'][offset]['selected_witnesses'][0]['outer_record'][4] += 1
    bad['cases_sha256'] = digest(bad['cases'])
    controls.append(('wrong-original-deletions', selected_path, bad,
                     'verify_constant.py', [0, offset, offset+1],
                     'Whole original scalar D/R/identity record differs'))
    rows = []
    for optimize in (False, True):
        for name, path, damaged, checker, args, expected in controls:
            operations_allow()
            try:
                path.write_text(json.dumps(damaged, indent=2)+'\n')
                command = [sys.executable]+(['-O'] if optimize else [])+[
                    str(ROOT/checker), *map(str, args)]
                result = subprocess.run(command, capture_output=True, text=True, timeout=55)
                need(result.returncode == 1 and 'ValueError: '+expected in result.stderr,
                     'Damage not rejected for its intended reason: '+name+' '+result.stderr[-1800:])
                row = {'control': name, 'optimized': optimize, 'intended_error': expected,
                       'status': 'DAMAGED_CERTIFICATE_REJECTED_FOR_INTENDED_REASON'}
                rows.append(row)
                print(json.dumps(row, sort_keys=True), flush=True)
            finally:
                path.write_bytes(originals[path])
    need(all(path.read_bytes() == raw for path, raw in originals.items()),
         'Generated data not restored byte for byte')
    report = {'agent': 'six-sorting-1', 'role': 'researcher',
              'status': 'ALL_THREE_DAMAGED_CONTROLS_REJECTED_NORMAL_AND_O',
              'checks': rows, 'generated_data_restored_exactly': True,
              'external_person_review_claimed': False}
    (WORK/'damage-summary.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
