"""Actual semantic certificate alterations, using independent original checkers.

Re-sealing the raw test inputs avoids rejecting merely for a stale checksum.
The six capacity alterations and five column alterations must instead
reject at the stated complete mathematical comparison. All children are
serial and keep the original 60-second wrapper and kernel guards.
"""
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

R = Path('round-two/six-code-3')
S = R / 'scratch'
B = R / 'four_hub_p21_endpoint_cut'

def need(c, m):
    if not c:
        raise ValueError(m)

def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':')).encode()

def main():
    work = S / 'semantic-damage-work'
    out = S / 'pass22-semantic-damages.json'
    need(not work.exists() and not out.exists(), 'fresh actual damage namespace')
    work.mkdir()
    interpreter = [sys.executable] + (['-O'] if sys.flags.optimize else [])
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    for k in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS']:
        env[k] = '1'
    checks = []

    def prepare(label, inputs):
        target = work / label
        target.mkdir()
        for p in inputs:
            q = target / p
            q.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, q)
        return target

    def run(script, target, arguments=()):
        return subprocess.run(interpreter + [str(script.resolve())] + list(arguments),
                              cwd=target, env=env, capture_output=True, text=True, timeout=60)

    capacity_name = 'pass21-T1-capacity-producer.json'
    capacity = json.loads((S / capacity_name).read_text())
    inputs = [B / 'fixtures.json', B / 'expected.json',
              S / 'pass21-T1-live-column-cases.json',
              S / 'pass21-T1-capacity-source-preparation.json',
              S / 'pass21-T1-hub-friend-catalogue.json', S / capacity_name]
    valid = prepare('valid-capacity', inputs)
    result = run(S / 'pass21-T1-capacity-check.py', valid)
    need(result.returncode == 0, 'valid actual capacity certificate failed: ' + result.stderr)
    need((valid / S / 'pass21-T1-capacity-independent.json').read_bytes() ==
         (S / 'pass21-T1-capacity-independent.json').read_bytes(), 'valid whole capacity bytes')
    alterations = []
    damaged = copy.deepcopy(capacity)
    damaged['records'].pop()
    alterations.append(('missing_actual_case', damaged, 'complete original29 capacity certificates'))
    case = next(i for i, r in enumerate(capacity['records']) if r['positive_entry_capacity'] == 5)
    reason = 'entire actual capacity record matches independent physical matching'
    for label, field, value in [('wrong_actual_multiplicity', 'type18_multiplicity', 5),
                                ('missing_eligible_role', 'eligible_hub_roles', []),
                                ('wrong_capacity', 'positive_entry_capacity', 6),
                                ('wrong_gap', 'gap', 0),
                                ('wrong_actual_ordinal', 'live_case_ordinal', 28)]:
        damaged = copy.deepcopy(capacity)
        damaged['records'][case][field] = value
        alterations.append((label, damaged, reason))
    for label, damaged, reason in alterations:
        target = prepare(label, inputs)
        (target / S / capacity_name).write_bytes(canonical(damaged) + b'\n')
        result = run(S / 'pass21-T1-capacity-check.py', target)
        need(result.returncode != 0 and reason in result.stderr,
             'actual capacity damage not rejected for its mathematical reason: ' + label)
        checks.append(dict(kernel='capacity', damage=label, expected_semantic_rejection=reason))

    # This complete 64-population interval contains actual positive ordinal1116.
    author_name = 'pass21-T1-N-1088-1152.json'
    author_path = S / author_name
    author = json.loads(author_path.read_text())
    inputs = [B / 'expected.json', S / 'pass21-T1-column-scope.json',
              S / 'pass21-T1-hub-friend-catalogue.json', S / 'pass21-T1-producer.json',
              S / 'pass21-T1-polynomial.json', author_path]
    arguments = ['--author', str(author_path), '--output', str(S / 'damage-column-check.json')]
    valid = prepare('valid-column', inputs)
    result = run(S / 'pass21-T1-N-check.py', valid, arguments)
    need(result.returncode == 0, 'valid actual positive interval failed: ' + result.stderr)
    valid_data = json.loads((valid / S / 'damage-column-check.json').read_text())
    need(valid_data['status'] == 'PRIVATE_COMPLETE_TWO_ALGORITHM_JOINT_N_INTERVAL' and
         valid_data['total_coupled_tuples'] == author['total_coupled_tuples'] > 0,
         'actual positive column control')
    pos = next(i for i, r in enumerate(author['records']) if r['survivor_ordinal'] == 1116)
    carrier = next(i for i, r in enumerate(author['records'][pos]['carrier_results']) if r['coupled_N4'])
    alterations = []
    damaged = copy.deepcopy(author)
    damaged['records'].pop()
    alterations.append(('missing_column_population', damaged, 'exact complete supplied interval'))
    for label in ['missing_actual_N_tuple', 'wrong_coordinate_N_set', 'wrong_actual_failure']:
        damaged = copy.deepcopy(author)
        record = damaged['records'][pos]['carrier_results'][carrier]
        if label == 'missing_actual_N_tuple':
            record['coupled_N4'].pop()
        elif label == 'wrong_coordinate_N_set':
            record['coordinate_N_sets'][0].append(99)
        else:
            record['first_failure'] = 'invented_failure'
        alterations.append((label, damaged, 'every coordinate N set, joint N4 tuple and failure agrees'))
    damaged = copy.deepcopy(author)
    damaged['canonical_carriers'][0]['lambda6'][0] += 1
    alterations.append(('wrong_global_carrier', damaged, 'entire independent actualT1 carrier stream'))
    for label, damaged, reason in alterations:
        target = prepare(label, inputs)
        (target / author_path).write_bytes(canonical(damaged) + b'\n')
        result = run(S / 'pass21-T1-N-check.py', target, arguments)
        need(result.returncode != 0 and reason in result.stderr,
             'actual column damage not rejected for its mathematical reason: ' + label)
        checks.append(dict(kernel='columns', damage=label, expected_semantic_rejection=reason))
    record = dict(agent='six-code-3', role='researcher',
                  status='VALID_ACTUAL_RECORDS_PASS_ALL11_SEMANTIC_DAMAGES_REJECT',
                  capacity_damages=6, column_damages=5, actual_positive_column_control=True,
                  all29_capacity_records_control=True, checks=checks,
                  serial_children=True, native_threads=1, child_timeout_seconds=60,
                  resource_escalation=False, independent_person_review=False)
    out.write_bytes(canonical(record) + b'\n')
    print(json.dumps(record, sort_keys=True))

if __name__ == '__main__':
    main()
