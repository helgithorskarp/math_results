"""Wrong-domain/inventory controls; supplement rather than exclusion proofs."""
from copy import deepcopy
import json
from pathlib import Path
from phase_controls import transport
from reproduce import ROOT, application_data, require_applications, require_domain


def reject(function, value):
    try:
        function(value)
    except (ValueError, KeyError, TypeError):
        return
    raise RuntimeError('Damaged evidence was accepted')


def main():
    base = {'L': 10080, 'minimum': 8, 'complete': True, 'root_anchors': ROOT}
    require_domain(base)
    bad = []
    for field, value in (('L', 10079), ('L', 10080.0), ('minimum', 9),
                         ('complete', False), ('complete', 1)):
        case = deepcopy(base)
        case[field] = value
        bad.append(case)
    for index, replacement in ((5, (16, 2)), (4, (12, 10)), (3, (14, 1))):
        case = deepcopy(base)
        case['root_anchors'] = list(case['root_anchors'])
        case['root_anchors'][index] = replacement
        bad.append(case)
    case = deepcopy(base)
    case['root_anchors'] = ROOT[:-1]
    bad.append(case)
    case = deepcopy(base)
    case['root_anchors'] = ROOT + ((16, 1),)
    bad.append(case)
    for case in bad:
        reject(require_domain, case)
    app = application_data()
    require_applications(app)
    require_applications(json.loads((Path(__file__).parent / 'application-next.json').read_text()))
    damaged = []
    for field, value in (('period', 10079), ('minimum_exactly', 9),
                         ('top_phases', 'one prescribed phase')):
        case = deepcopy(app)
        case[field] = value
        damaged.append(case)
    case = deepcopy(app)
    case['roots'][0]['residual'] -= 1
    damaged.append(case)
    case = deepcopy(app)
    case['roots'][1]['residual_bitset_hex'] = '0'
    damaged.append(case)
    case = deepcopy(app)
    case['all_unused_moduli'].pop()
    damaged.append(case)
    case = deepcopy(app)
    case['all_unused_moduli'].append(16)
    damaged.append(case)
    case = deepcopy(app)
    case['roots'][1]['root'][-1] = [16, 2]
    damaged.append(case)
    for case in damaged:
        reject(require_applications, case)
    for value in (-1, 16, True, 2.0, 0, 8):
        reject(transport, value)
    print(json.dumps({'status': 'Boundary controls only; not exclusion',
                      'wrong_domains_rejected': len(bad),
                      'wrong_applications_rejected': len(damaged),
                      'wrong_transports_rejected': 6,
                      'all_guards_active': True}, sort_keys=True))


if __name__ == '__main__':
    main()
