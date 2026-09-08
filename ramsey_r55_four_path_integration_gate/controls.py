"""Reject corrupted arithmetic and event certificates after the full count audit."""
import copy
import json
from pathlib import Path
import check


def main():
    certificate = json.loads(Path(__file__).with_name('CERTIFICATE.json').read_text())
    changes = {
        'missing_PP_event': lambda c: c['events']['PP'].pop(),
        'wrong_PK_color': lambda c: c['events']['PK'][0].update(color=0),
        'wrong_PP_mask': lambda c: c['events']['PP'][0].update(mask=1),
        'inflated_union_bound': lambda c: c['pair_lower_bounds'].update(PP=27262977),
        'wrong_KK_count': lambda c: c['pair_exact_counts'].update(KK=37824),
        'wrong_root_count': lambda c: c['root_counts'].update(KB=1932),
        'wrong_core_count': lambda c: c['core_counts'].update({'11': 546357}),
        'wrong_baseline_term': lambda c: c['baseline_terms'][0].update(term=0),
        'wrong_P': lambda c: c.update(P=c['P']+1),
        'wrong_product': lambda c: c.update(macro_raw_lower=c['macro_raw_lower']+1),
        'wrong_group': lambda c: c.update(group_order=c['group_order']//2),
        'wrong_normalized_lower': lambda c: c.update(normalized_lower=c['normalized_lower']+1),
        'wrong_ratio': lambda c: c.update(raw_to_group_P_floor=13),
        'wrong_outcome': lambda c: c.update(status='TARGET_FOUND'),
    }
    # Full physical enumeration is performed by the preceding replay checker;
    # cache only those exact domain counts in these negative controls.
    cache = {'KK': (37823, 1998), 'KB': (35714, 1931)}
    rejected = []
    for name, change in changes.items():
        bad = copy.deepcopy(certificate)
        change(bad)
        try:
            check.validate(bad, cache)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('corrupted certificate accepted: '+name)
    print(json.dumps({'status': 'REJECTED_CORRUPTED_CERTIFICATES',
                      'count': len(rejected), 'controls': rejected}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
