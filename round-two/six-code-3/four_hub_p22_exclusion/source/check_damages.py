"""Actual valid images and seventeen semantic damages, using separate checkers.

No timeout, kill or unrelated failure accepts a damage. Every alteration
keeps or rebinds the actual raw input pins and must fail at its specified
mathematical or complete-domain comparison. The selected column interval
contains an actual coupled positive choice. All child jobs are serial.
"""
import copy
import datetime
from decimal import Decimal
import hashlib
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

def operations():
    state_value = os.environ.get('MATH_RESEARCH_OPERATIONS_STATE')
    if state_value is None:
        return
    state = Path(state_value)
    for root in [state, state / 'monitor']:
        for name in ['PAUSED', 'PAUSED.json', 'HANDOVER', 'HANDOVER.json']:
            p = root / name
            if p.exists() and not (name == 'HANDOVER.json' and json.loads(p.read_text()).get('phase') == 'completed'):
                raise ValueError('active operations barrier; preserve prefix')
    health = json.loads((state / 'monitor/health.json').read_text())
    budget = health['credit_budget']
    age = (datetime.datetime.now(datetime.timezone.utc) - datetime.datetime.fromisoformat(
        health['checked_at'].replace('Z', '+00:00'))).total_seconds()
    need(0 <= age <= 180 and budget['status'] == 'authorized' and
         Decimal(budget['observed_spent_credits']) < Decimal(budget['stop_at_observed_spend_credits']),
         'operations stop or stale health')

def main():
    root = S / 'semantic-damage-work'
    output = S / 'pass24-semantic-damages.json'
    need(not root.exists() and not output.exists(), 'fresh actual damage namespace')
    root.mkdir()
    interpreter = [sys.executable] + (['-O'] if sys.flags.optimize else [])
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    for name in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS']:
        env[name] = '1'
    checked = []
    valid = []
    seals = {}

    def prepare(label, inputs):
        target = root / label
        target.mkdir()
        for p in inputs:
            seals[str(p)] = hashlib.sha256(p.read_bytes()).hexdigest()
            q = target / p
            q.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(p, q)
        return target

    def run(kernel, target, arguments):
        operations()
        p = S / kernel
        seals[str(p)] = hashlib.sha256(p.read_bytes()).hexdigest()
        result = subprocess.run(interpreter + [str(p.resolve())] + arguments,
                                cwd=target, env=env, capture_output=True, text=True, timeout=60)
        (target / 'stdout').write_text(result.stdout)
        (target / 'stderr').write_text(result.stderr)
        return result

    def damage(kernel, name, data, inputs, target_path, args, reason):
        target = prepare(name, inputs)
        (target / target_path).write_bytes(canonical(data) + b'\n')
        result = run(kernel, target, args)
        need(result.returncode == 1 and 'ValueError: ' + reason in result.stderr,
             'semantic damage did not reject for its intended reason: ' + name + '\n' + result.stderr)
        checked.append(dict(kernel=kernel, damage=name, expected_semantic_rejection=reason))

    capacity_path = S / 'pass23-T0-capacity-producer.json'
    capacity = json.loads(capacity_path.read_text())
    inputs = [B / 'expected.json', B / 'fixtures.json', S / 'pass23-T0-live-column-cases.json',
              S / 'pass23-T0-hub-friend-catalogue.json', capacity_path]
    args = ['--author', str(capacity_path), '--output', str(S / 'capacity-audit.json')]
    target = prepare('valid-capacity', inputs)
    result = run('pass23-T0-capacity-check.py', target, args)
    need(result.returncode == 0 and (target / S / 'capacity-audit.json').read_bytes() ==
         (S / 'pass23-T0-capacity-independent.json').read_bytes(), 'actual whole capacity control')
    valid.append('capacity')
    damaged = copy.deepcopy(capacity)
    damaged['records'].pop()
    damage('pass23-T0-capacity-check.py', 'missing_capacity_case', damaged, inputs, capacity_path, args,
           'entire T0 input domain')
    index = next(i for i, r in enumerate(capacity['records']) if r['eligible_hub_roles'])
    original = capacity['records'][index]
    values = [('wrong_capacity_multiplicity', 'type18_multiplicity', original['type18_multiplicity'] + 1),
              ('missing_capacity_role', 'eligible_hub_roles', []),
              ('wrong_capacity', 'weighted_positive_entry_capacity', original['weighted_positive_entry_capacity'] + 1),
              ('wrong_capacity_gap', 'gap', original['gap'] + 1),
              ('wrong_capacity_ordinal', 'live_case_ordinal', 969)]
    for name, field, value in values:
        damaged = copy.deepcopy(capacity)
        damaged['records'][index][field] = value
        damage('pass23-T0-capacity-check.py', name, damaged, inputs, capacity_path, args,
               'all original fields/weighted capacity match independent literal matching')

    # Pick a complete interval containing an actual positive coupled tuple.
    live = json.loads((S / 'pass23-T0-live-column-cases.json').read_text())['live_cases']
    ordinal = live[0]['survivor_ordinal']
    begin = ordinal // 64 * 64
    stop = min(begin + 64, 11077)
    column_path = S / ('pass23-T0-N-%04d-%04d.json' % (begin, stop))
    column = json.loads(column_path.read_text())
    inputs = [B / 'expected.json', S / 'pass23-T0-column-scope.json',
              S / 'pass23-T0-hub-friend-catalogue.json', S / 'pass23-T0-producer.json',
              S / 'pass23-T0-polynomial.json', column_path]
    args = ['--author', str(column_path), '--output', str(S / 'column-audit.json')]
    target = prepare('valid-column', inputs)
    result = run('pass23-T0-N-check.py', target, args)
    need(result.returncode == 0, 'valid actual positive column interval: ' + result.stderr)
    audit = json.loads((target / S / 'column-audit.json').read_text())
    need(audit['total_coupled_tuples'] == column['total_coupled_tuples'] > 0, 'actual positive column control')
    valid.append('columns')
    position = next(i for i, r in enumerate(column['records']) if r['survivor_ordinal'] == ordinal)
    carrier = next(i for i, r in enumerate(column['records'][position]['carrier_results']) if r['coupled_N4'])
    for name in ['missing_column_population', 'missing_N_tuple', 'wrong_coordinate_N', 'wrong_column_failure', 'wrong_carrier']:
        damaged = copy.deepcopy(column)
        reason = 'every coordinate N set, joint N4 tuple and failure agrees'
        if name == 'missing_column_population':
            damaged['records'].pop()
            reason = 'exact complete supplied interval'
        elif name == 'wrong_carrier':
            damaged['canonical_carriers'][0]['lambda6'][0] += 1
            reason = 'entire independent actualT0 carrier stream'
        else:
            record = damaged['records'][position]['carrier_results'][carrier]
            if name == 'missing_N_tuple':
                record['coupled_N4'].pop()
            elif name == 'wrong_coordinate_N':
                record['coordinate_N_sets'][0].append(99)
            else:
                record['first_failure'] = 'invented_failure'
        damage('pass23-T0-N-check.py', name, damaged, inputs, column_path, args, reason)

    row_path = S / 'pass23-T0-row-base.json'
    row = json.loads(row_path.read_text())
    cat_path = S / 'pass23-T0-hub-friend-catalogue.json'
    catalogue = json.loads(cat_path.read_text())
    inputs = [B / 'expected.json', B / 'fixtures.json', S / 'pass23-T0-live-column-cases.json',
              S / 'pass23-T0-capacity-producer.json', cat_path, row_path]
    args = ['--author', str(row_path), '--output', str(S / 'row-audit.json')]
    target = prepare('valid-rows', inputs)
    result = run('pass23-T0-check-row-projections.py', target, args)
    need(result.returncode == 0 and (target / S / 'row-audit.json').read_bytes() ==
         (S / 'pass23-T0-row-base-independent.json').read_bytes(), 'actual entire row certificate control')
    valid.append('rows')
    index = next(i for i, r in enumerate(row['records']) if r['bounds'])
    for name in ['missing_row_case', 'missing_allowed_row', 'altered_row_target', 'false_excluding_minimum',
                 'unbound_row_carrier', 'wrong_literal_witness']:
        damaged = copy.deepcopy(row)
        target = prepare(name, inputs)
        reason = 'every original physical choice, entire ordered bound prefix and first failure agrees'
        if name == 'missing_row_case':
            damaged['records'].pop()
            reason = 'entire actual377-case remainder'
        elif name == 'missing_allowed_row':
            damaged['records'][index]['admissible_original_rows'][0]['actual_catalogue_indices'].pop()
        elif name == 'altered_row_target':
            damaged['records'][index]['bounds'][0]['target'] += 1
        elif name == 'false_excluding_minimum':
            record = damaged['records'][index]
            bound = record['bounds'][record['first_failure']['bound_index']]
            bound['minimum'] = bound['target'] - 1
            bound['passes'] = True
        elif name == 'unbound_row_carrier':
            damaged['records'][index]['carrier']['lambda6'][0] += 1
        else:
            changed = copy.deepcopy(catalogue)
            r = next(r for r in changed['records'] if r['type_id'] == 18 and r['hub_deficits'][0] == 2)
            roles = r['witness']['hub_roles']
            roles[0], roles[1] = roles[1], roles[0]
            raw = canonical(changed) + b'\n'
            (target / cat_path).write_bytes(raw)
            damaged['catalogue_sha256'] = hashlib.sha256(raw).hexdigest()
            reason = 'entire original physical signature critical fields'
        (target / row_path).write_bytes(canonical(damaged) + b'\n')
        result = run('pass23-T0-check-row-projections.py', target, args)
        need(result.returncode == 1 and 'ValueError: ' + reason in result.stderr,
             'row damage did not reject for its intended reason: ' + name + '\n' + result.stderr)
        checked.append(dict(kernel='pass23-T0-check-row-projections.py', damage=name,
                            expected_semantic_rejection=reason))
    for name, digest in seals.items():
        need(hashlib.sha256(Path(name).read_bytes()).hexdigest() == digest, 'original undamaged source/input changed')
    need(len(checked) == 17 and valid == ['capacity', 'columns', 'rows'], 'complete intended semantic controls')
    result = dict(agent='six-code-3', role='researcher', status='THREE_ACTUAL_VALID_IMAGES_PASS_ALL17_SEMANTIC_DAMAGES_REJECT',
                  valid_images=valid, actual_positive_column_control=True, complete_capacity_control=969,
                  complete_row_control=377, capacity_damages=6, column_damages=5, row_damages=6,
                  checks=checked, serial_children=True, native_threads=1, child_timeout_seconds=60,
                  resource_escalation=False, independent_person_review=False)
    output.write_bytes(canonical(result) + b'\n')
    print(json.dumps(result, sort_keys=True))

if __name__ == '__main__':
    main()
