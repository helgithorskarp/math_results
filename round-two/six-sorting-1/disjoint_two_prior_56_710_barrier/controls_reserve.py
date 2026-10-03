"""Semantic corruptions of future CLASS reserve and an actual ORIGINAL cube.

Checksums are repaired. The true classification is never modified.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from controls import operations_allow

ROOT = Path(__file__).resolve().parent
PILOT = ROOT
WORK = ROOT/'work'
ENV = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
           MKL_NUM_THREADS='1', BLIS_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1',
           VECLIB_MAXIMUM_THREADS='1', PYTHONHASHSEED='0')


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def gate(value, a, b):
    return value ^ (1 << a) ^ (1 << b) if (value >> a & 1) > (value >> b & 1) else value


def seal(record):
    record['finite']['classification_sha256'] = digest(record['classifications'])
    record['finite_sha256'] = digest(record['finite'])
    return record


def main():
    operations_allow()
    started = time.monotonic()
    original_path = WORK/'reserve-preparation-classifications.json'
    before = original_path.read_bytes()
    proposal = json.loads(before)
    normal = json.loads((WORK/'reserve-preparations-checked.json').read_text())
    optimized = json.loads((WORK/'reserve-preparations-checked-O.json').read_text())
    need(normal['finite'] == optimized['finite'] and
         normal['finite']['producer_reserve_classification_finite_sha256'] == proposal['finite_sha256'],
         'Actual positive normal/O partition must precede controls')
    seed = json.loads((WORK/'reserve-seed-checked.json').read_text())
    domains = seed['activity_domains']
    classes = {}
    for row in domains:
        r = row['original_record']
        classes[r[3]] = max(classes.get(r[3], 0), r[4])
    first = next(i for i, r in enumerate(proposal['classifications']) if r['witness'] is not None)
    witness = proposal['classifications'][first]['witness']
    false_depth = copy.deepcopy(proposal)
    false_depth['classifications'][first]['witness']['reserved_marked_touches'] += 1
    false_depth['classifications'][first]['witness']['certified_total_cost_lower_bound'] += 1
    p = json.loads((PILOT/'work/branch02.json').read_text())
    word = p['functions'][proposal['classifications'][first]['function_id']]['shortest_word']
    dead = [2, 3, 4, 5, 7, 8]
    index = {q: i for i, q in enumerate(dead)}
    t = witness['first_reported_preparation_identity_index']
    chosen = None
    for row in domains:
        values = {i for i in range(64) if row['dead_projected_image_mask'] >> i & 1}
        for a, b in word[:t]:
            values = {gate(value, index[a], index[b]) for value in values}
        a, b = word[t]
        if any((value >> index[a] & 1) > (value >> index[b] & 1) for value in values):
            chosen = row
            break
    need(chosen is not None, 'No actual active-original countercontrol available')
    false_identity = copy.deepcopy(proposal)
    record = chosen['original_record']
    E = classes[record[3]]
    false_identity['classifications'][first]['witness'].update(
        original_HIGH_mask=chosen['original_HIGH_mask'], original_seed_record=record,
        current_HIGH_class_maximum_E=E, reserved_marked_touches=9-E,
        original_activity_image_mask=chosen['dead_projected_image_mask'],
        certified_total_cost_lower_bound=record[4]+record[5]+1+9-E+35)
    controls = []
    for name, corrupted, reason in [
            ('false-future-depth', false_depth, 'Reported future CLASS maximum or marked-touch reserve differs'),
            ('actual-active-original', false_identity, 'Chosen ORIGINAL is active at the reported identity gate')]:
        file = WORK/('damaged-reserve-'+name+'.json')
        file.write_text(json.dumps(seal(corrupted), indent=2)+'\n')
        for optimized in (False, True):
            operations_allow()
            command = [sys.executable]+(['-O'] if optimized else [])+[
                str(ROOT/'verify_reserve_preps.py'), str(file)]
            child_started = time.monotonic()
            result = subprocess.run(command, env=ENV, capture_output=True, text=True, timeout=55)
            output = result.stdout+result.stderr
            (WORK/('control-reserve-'+name+('-O' if optimized else '')+'.log')).write_text(output)
            need(result.returncode != 0 and reason in output,
                 'Damage not rejected for intended semantic reason: '+name)
            controls.append({'damage': name, 'optimized': optimized,
                             'returncode': result.returncode, 'intended_rejection': reason,
                             'superficial_bindings_repaired': True,
                             'seconds': time.monotonic()-child_started})
    need(original_path.read_bytes() == before, 'Valid original classification changed')
    result = {'agent': 'six-sorting-1', 'role': 'researcher',
              'status': 'TWO_ACTUAL_RESERVED_ORIGINAL_SEMANTIC_DAMAGES_REJECT_NORMAL_O',
              'positive_scalar_finite_sha256': normal['finite_sha256'],
              'controls': controls, 'original_classification_bytes_unchanged': True,
              'actual_active_original_fixture': {'retained_offset': first,
                  'original_HIGH_mask': chosen['original_HIGH_mask'], 'gate_index': t},
              'seconds': time.monotonic()-started,
              'scope': 'Checker controls only, no new mathematical negative or independent-person verdict.'}
    (WORK/'reserve-controls.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
