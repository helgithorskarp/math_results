"""Replay the independent checker on one valid and eight altered certificates."""
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

S = Path('round-two/six-code-3/scratch')


def need(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    base = Path.cwd().resolve()
    area = base / S / 'pass19-certificate-damage-replays'
    need(not area.exists(), 'fresh damage replay area required')
    original = json.loads((base / S / 'pass19-high-T-cut-producer.json').read_text())
    checker = Path(__file__).resolve().with_name('pass19-check-high-T-cuts.py')
    need(checker.is_file(), 'actual independent checker source required')
    cases = [('valid-original', None, None)]
    cases += [
        ('omitted-certificate', 'omit', 'every full certificate'),
        ('wrong-D-target-multiplicity', 'target', 'every full certificate'),
        ('wrong-total-multiplicity', 'total', 'every full certificate'),
        ('weakened-radius-bound', 'radius', 'every full certificate'),
        ('changed-closed-unit-degree', 'parity', 'every full certificate'),
        ('invented-unit-capacity', 'capacity', 'every full certificate'),
        ('forged-sensitivity-control', 'control', 'independently reconstructed sensitivity controls'),
        ('omitted-survivor', 'survivor', 'complete ordered surviving census stream'),
    ]
    outcomes = []
    interpreter = [sys.executable] + (['-O'] if sys.flags.optimize else [])
    env = dict(os.environ)
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        env[name] = '1'
    for label, mutation, error in cases:
        work = area / label
        scratch = work / S
        scratch.mkdir(parents=True)
        for name in ('pass19-high-T-polynomial.json', 'pass19-high-T-producer.json'):
            shutil.copy2(base / S / name, scratch / name)
        data = copy.deepcopy(original)
        if mutation == 'omit':
            data['records'].pop(0)
        elif mutation == 'target':
            data['records'][0]['target_rows'][0]['pre_support_typed_allocations'] += 1
        elif mutation == 'total':
            data['records'][0]['pre_support_typed_allocations'] += 1
        elif mutation == 'radius':
            next(r for r in data['records'] if r['kind'] == 'GENERALIZED_RADIUS')['two_step_ball_upper'] += 1
        elif mutation == 'parity':
            next(r for r in data['records'] if r['kind'] == 'CLOSED_UNIT_PARITY')['closed_unit_degree_sum'] += 1
        elif mutation == 'capacity':
            next(r for r in data['records'] if r['kind'] == 'UNIT_CAPACITY')['internal_incidence_upper'] += 1
        elif mutation == 'control':
            data['controls']['mixed_support_weakened_C4'] = 0
        elif mutation == 'survivor':
            data['necessary_populations'].pop(0)
        (scratch / 'pass19-high-T-cut-producer.json').write_text(json.dumps(data, sort_keys=True) + '\n')
        child = subprocess.run(interpreter + [str(checker)], cwd=work, env=env, capture_output=True, text=True, timeout=60)
        if mutation is None:
            need(child.returncode == 0, 'valid original certificate rejected: ' + child.stderr)
            result = json.loads((scratch / 'pass19-independent-high-T-cuts.json').read_text())
            need(result['status'] == 'COMPLETE_INDEPENDENT_T3_T4_CERTIFICATE_AGREEMENT', 'valid checker must complete')
            outcomes.append(dict(case=label, status='ACCEPTED_COMPLETE_ORIGINAL'))
        else:
            need(child.returncode != 0 and error in child.stderr and 'ValueError' in child.stderr,
                 'altered certificate must be rejected for the specified semantic reason: ' + label)
            need(not (scratch / 'pass19-independent-high-T-cuts.json').exists(), 'no successful output for an altered certificate')
            outcomes.append(dict(case=label, status='REJECTED_FOR_EXPECTED_SEMANTIC_REASON', checked_error=error))
    result = dict(agent='six-code-3', role='researcher', status='COMPLETE_EXACT_CERTIFICATE_DAMAGE_AUDIT',
                  valid_original_accepted=1, semantic_alterations_rejected=8, outcomes=outcomes,
                  native_threads=1, serial_children=True, child_timeout_seconds=60,
                  mathematical_new_claim=None, external_review=False)
    out = base / S / 'pass19-certificate-damages.json'
    need(not out.exists(), 'fresh damage audit output required')
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
