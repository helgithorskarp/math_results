"""Recompute the compact certificate and reject semantic damage."""
import copy
import hashlib
import json
from pathlib import Path
import time

from verify import compute, need


def validate(record, regenerated):
    need(record == regenerated, 'certificate differs from the complete exact enumeration')


def main():
    start = time.monotonic()
    root = Path(__file__).resolve().parent
    certificate = json.loads((root / 'certificate.json').read_text())
    regenerated = compute()
    validate(certificate, regenerated)
    changes = [
        ('tail phase', lambda x: x['large_union_rows'][0].__setitem__(2, x['large_union_rows'][0][2] + 1)),
        ('tail union', lambda x: x['large_union_rows'][0].__setitem__(4, '0' * 45)),
        ('tail count', lambda x: x.__setitem__('effective_tail_phase_pairs', 178)),
        ('tail bound', lambda x: x['large_union_rows'][0].__setitem__(7, 160)),
        ('original label', lambda x: x['original_free_d'].__setitem__(0, 2)),
        ('first capacity', lambda x: x['first_complement_bounds'][0].__setitem__('total_capacity', 420)),
        ('core bound', lambda x: x['first_complement_bounds'][4]['groups'][0].__setitem__('maximum', 226)),
        ('core completion', lambda x: x['first_complement_bounds'][4]['groups'][0].__setitem__('raw_phase_tuples', 10367999)),
    ]
    for name, change in changes:
        damaged = copy.deepcopy(certificate)
        change(damaged)
        try:
            validate(damaged, regenerated)
        except RuntimeError:
            continue
        raise RuntimeError('accepted damaged ' + name)
    print(json.dumps({'status': 'EXACT_CONDITIONAL_COPY_OCCUPANCY_CHECKED',
                      'tail_large_unions': len(certificate['large_union_rows']),
                      'surviving_tail_assignments': sum(row[-1] for row in certificate['large_union_rows']),
                      'compulsory_counts': [r['compulsory_count'] for r in certificate['first_complement_bounds']],
                      'first_capacities': [r['total_capacity'] for r in certificate['first_complement_bounds']],
                      'damage_rejections': len(changes),
                      'certificate_sha256': hashlib.sha256((root / 'certificate.json').read_bytes()).hexdigest(),
                      'seconds': time.monotonic() - start,
                      'global_L_min_8_bound_improved': False}))


if __name__ == '__main__':
    main()
