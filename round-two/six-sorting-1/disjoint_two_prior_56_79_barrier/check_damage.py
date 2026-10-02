"""Serial semantic controls for complete tail cover, budgets, images and bounds.

All mutations are confined to this agent's generated pilot arrays, checksummed
to pass the initial transport checks, and restored byte-for-byte in finally.
No source or imported theorem is changed. Run after other mathematical jobs.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
SOURCE = Path(__file__).resolve().parent
OUT = ROOT / 'work'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def operations_allow():
    from controls import operations_allow as authorize
    authorize()


def main():
    operations_allow()
    start = time.monotonic()
    front_path = OUT / 'fronts01-00000-00128.json'
    constant_path = OUT / 'constant-catalogue01-00000-01000.json'
    original_bytes = {p: p.read_bytes() for p in (front_path, constant_path)}
    front = json.loads(original_bytes[front_path])
    constant = json.loads(original_bytes[constant_path])
    case_index = next(i for i, case in enumerate(constant['cases'])
                      if case['constant16_exceeds44'])
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1',
               BLIS_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1', PYTHONHASHSEED='0')
    rows = []
    try:
        for name in ('missing_tail_function', 'wrong_remaining_budget', 'wrong_whole_image', 'wrong_original_deletion_count'):
            operations_allow()
            if name == 'wrong_original_deletion_count':
                changed = copy.deepcopy(constant)
                witness = changed['cases'][case_index]['selected_witnesses'][0]
                witness['outer_record'][4] += 1
                witness['label'] += 1
                changed['cases'][case_index]['selected_mass'] = sum(1 << w['label'] for w in changed['cases'][case_index]['selected_witnesses'])
                changed['cases_sha256'] = digest(changed['cases'])
                path, script = constant_path, 'verify_constant.py'
                args = ['catalogue', '0', '1000', str(case_index), str(case_index+1)]
                reason = 'Original scalar deletion/identity record differs'
            else:
                changed = copy.deepcopy(front)
                path, script = front_path, 'verify_fronts.py'
                args = ['1', '0', '128']
                if name == 'missing_tail_function':
                    del changed['survivors'][0]
                    reason = 'One necessary tail function is silently missing'
                elif name == 'wrong_remaining_budget':
                    changed['survivors'][0]['remaining_gate_budget'] += 1
                    reason = 'Literal prefix/budget differs'
                else:
                    record = changed['survivors'][0]
                    extra = next(i for i in range(512) if i not in record['nine_core_states'])
                    record['nine_core_states'] = sorted(record['nine_core_states']+[extra])
                    record['nine_core_sha256'] = digest(record['nine_core_states'])
                    reason = 'Whole physical nine-core image differs'
                changed['survivors_sha256'] = digest(changed['survivors'])
            path.write_text(json.dumps(changed, indent=2)+'\n')
            try:
                for optimized in (False, True):
                    operations_allow()
                    command = [sys.executable]+(['-O'] if optimized else [])+[str(SOURCE / script), *args]
                    process = subprocess.run(command, env=env, capture_output=True, text=True, timeout=55)
                    output = process.stdout+process.stderr
                    need(process.returncode != 0 and reason in output, 'Damage not rejected for intended semantic reason: '+name)
                    rows.append({'control': name, 'optimized': optimized, 'returncode': process.returncode,
                                 'intended_semantic_rejection': reason})
                    print(json.dumps(rows[-1]), flush=True)
            finally:
                path.write_bytes(original_bytes[path])
    finally:
        for p, original in original_bytes.items():
            p.write_bytes(original)
    need(all(p.read_bytes() == original for p, original in original_bytes.items()), 'Pilot arrays not restored exactly')
    report = {'agent': 'six-sorting-1', 'role': 'researcher', 'status': 'FOUR_SEMANTIC_DAMAGE_CONTROLS_REJECT_NORMAL_O',
              'controls': rows, 'restored_byte_for_byte': True,
              'closed_catalogue_control_case_index': case_index,
              'restored_sha256': {p.name: hashlib.sha256(v).hexdigest() for p, v in original_bytes.items()},
              'seconds': time.monotonic()-start, 'scope': 'Checker controls, not another mathematical exclusion or independent-person review.'}
    (OUT / 'damage-summary.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'status': report['status'], 'seconds': report['seconds']}), flush=True)


if __name__ == '__main__':
    main()
