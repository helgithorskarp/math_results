"""Reject damaged scope/inventory/coverage and first-case gain receipts.

Imports only the independent auditor, never the producer. Numeric damage
controls invoke the actual auditor and must reject with the expected reason.
"""
import copy
import json
from pathlib import Path
import tempfile
from audit import audit, require


def rejected(candidate, reason):
    with tempfile.TemporaryDirectory(prefix='covering-parent4-control-') as tmp:
        path = Path(tmp) / 'damaged.json'
        path.write_text(json.dumps(candidate))
        try:
            audit(path)
        except ValueError as e:
            require(reason in str(e), 'Damage rejected for the wrong reason: ' + str(e))
        else:
            raise ValueError('Damaged candidate accepted')


def controls():
    original = json.loads(Path(__file__).with_name('expected.json').read_text())
    bad = copy.deepcopy(original)
    bad['prefix'][3][1] = 0
    rejected(bad, 'Wrong prescribed prefix')
    bad = copy.deepcopy(original)
    bad['base'].append(16)
    rejected(bad, 'Original BASE inventory')
    bad = copy.deepcopy(original)
    bad['cases'].pop()
    rejected(bad, 'Incomplete or duplicate two-row cover')
    bad = copy.deepcopy(original)
    bad['cases'][1]['rows'] = bad['cases'][0]['rows']
    rejected(bad, 'Incomplete or duplicate two-row cover')
    for field, value in (
        ('core_threshold', 316),
        ('retained_core_vectors', 59),
        ('conditional7_maximum', 561),
        ('all_conditional7_gains_sha256', '0' * 64),
    ):
        bad = copy.deepcopy(original)
        bad['cases'][0][field] = value
        rejected(bad, 'Full record mismatch at rows (0, 1)')
    return {'rejected_damages': 8, 'all_expected_reasons_checked': True}


if __name__ == '__main__':
    print(json.dumps(controls(), sort_keys=True))
