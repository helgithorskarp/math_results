"""Meaningful boundary controls; the three literal exclusions are separate."""
from copy import deepcopy
import json
from pathlib import Path
from reproduce import N, PHASES, R, require_domain, check_applications

HERE = Path(__file__).resolve().parent


def check():
    rejected = []
    for phase in PHASES:
        valid = {'L': N, 'minimum': 8, 'complete': True,
                 'root_anchors': [list(p) for p in R + ((20, phase),)]}
        require_domain(valid, phase)
        for name in ('period', 'minimum', 'incomplete', 'root'):
            bad = deepcopy(valid)
            if name == 'period':
                bad['L'] = 5040
            elif name == 'minimum':
                bad['minimum'] = 9
            elif name == 'incomplete':
                bad['complete'] = False
            else:
                bad['root_anchors'][-1][1] = (phase + 1) % 20
            try:
                require_domain(bad, phase)
            except ValueError:
                rejected.append([phase, name])
            else:
                raise ValueError('Bad domain accepted: ' + name)
    manifest = json.loads((HERE / 'manifest.json').read_text())
    prefixes = manifest['affine_frontier']['remaining_prefixes']
    fixture = json.loads((HERE / 'application-next.json').read_text())
    if check_applications(fixture, prefixes) != 13:
        raise ValueError('Incomplete positive application inventory')
    damage_names = ('period', 'minimum', 'missing_resource', 'duplicate_root',
                    'wrong_phase', 'false_bitset', 'false_count', 'missing_top',
                    'fixed_top', 'false_status')
    for name in damage_names:
        bad = deepcopy(fixture)
        if name == 'period':
            bad['period'] = 15120
        elif name == 'minimum':
            bad['minimum_exactly'] = 9
        elif name == 'missing_resource':
            bad['all_unused_moduli'].pop()
        elif name == 'duplicate_root':
            bad['roots'][1] = deepcopy(bad['roots'][0])
        elif name == 'wrong_phase':
            bad['roots'][0]['root'][4][1] ^= 1
        elif name == 'false_bitset':
            bad['roots'][0]['residual_bitset_hex'] = '0'
        elif name == 'false_count':
            bad['roots'][0]['residual'] += 1
        elif name == 'missing_top':
            bad['four_top_resources'].pop()
        elif name == 'fixed_top':
            bad['top_phases'] = 'FIXED'
        else:
            bad['roots'][0]['proof_status'] = 'EXCLUDED'
        try:
            check_applications(bad, prefixes)
        except ValueError:
            rejected.append(['application', name])
        else:
            raise ValueError('Bad application accepted: ' + name)
    return {'agent': 'six-covering-2', 'role': 'researcher',
            'valid_root_domains': list(PHASES), 'application_roots': 13,
            'unused_resources': len(fixture['all_unused_moduli']),
            'damaged_cases_rejected': rejected,
            'scope': 'Domain/inventory guards only; not a covering exclusion'}


if __name__ == '__main__':
    print(json.dumps(check(), sort_keys=True))
