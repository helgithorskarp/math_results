"""Domain/inventory boundary controls; no invalid tree is used as proof."""
import copy
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    'aligned_fourteen_reproduce', Path(__file__).with_name('reproduce.py'))
reproduce = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reproduce)
N, ROOT = reproduce.N, reproduce.ROOT
application_data = reproduce.application_data
require_applications = reproduce.require_applications
require_domain = reproduce.require_domain


def controls():
    good = {'L': N, 'minimum': 8, 'complete': True,
            'root_anchors': [list(row) for row in ROOT]}
    require_domain(good)  # Domain acceptance only, not a certificate acceptance.
    cases = []
    def add(name, edit):
        data = copy.deepcopy(good)
        edit(data)
        cases.append((name, data))
    add('wrong period', lambda t: t.__setitem__('L', 20160))
    add('boolean period', lambda t: t.__setitem__('L', True))
    add('wrong minimum', lambda t: t.__setitem__('minimum', 9))
    add('boolean minimum', lambda t: t.__setitem__('minimum', True))
    add('incomplete', lambda t: t.__setitem__('complete', False))
    add('integer completion flag', lambda t: t.__setitem__('complete', 1))
    add('extra known resource', lambda t: t['root_anchors'].append([16, 2]))
    add('missing original root', lambda t: t['root_anchors'].pop())
    add('wrong twelve phase', lambda t: t['root_anchors'][4].__setitem__(1, 6))
    add('wrong fourteen parity', lambda t: t['root_anchors'][3].__setitem__(1, 1))
    add('boolean phase', lambda t: t['root_anchors'][0].__setitem__(1, False))
    add('changed root order', lambda t: t['root_anchors'].reverse())
    for name, data in cases:
        try:
            require_domain(data)
        except ValueError:
            continue
        raise ValueError('Invalid domain accepted: ' + name)
    valid = application_data()
    require_applications(valid)
    damaged = []
    def alter(name, edit):
        data = copy.deepcopy(valid)
        edit(data)
        damaged.append((name, data))
    alter('hidden consumed16', lambda t: t['all_unused_moduli'].remove(16))
    alter('missing TOP', lambda t: t['all_unused_moduli'].remove(10080))
    alter('extra excluded root', lambda t: t['roots'].append({'root': [list(r) for r in ROOT]}))
    alter('missing remaining root', lambda t: t['roots'].pop())
    alter('false remaining status', lambda t: t['roots'][0].__setitem__('proof_status', 'EXCLUDED'))
    alter('wrong residual count', lambda t: t['roots'][0].__setitem__('residual', t['roots'][0]['residual'] + 1))
    alter('wrong residual bitset', lambda t: t['roots'][0].__setitem__('residual_bitset_hex', '0'))
    alter('restricted TOP phases', lambda t: t.__setitem__('top_phases', 'ZERO ONLY'))
    for name, data in damaged:
        try:
            require_applications(data)
        except ValueError:
            continue
        raise ValueError('Invalid application inventory accepted: ' + name)
    return {'agent': 'six-covering-2', 'role': 'researcher',
            'rejected_domains': [n for n, d in cases],
            'rejected_inventories': [n for n, d in damaged],
            'remaining_roots': len(valid['roots']),
            'unused_original_resources_per_remaining_root': len(valid['all_unused_moduli'])}


if __name__ == '__main__':
    print(json.dumps(controls(), sort_keys=True))
