#!/usr/bin/env python3
"""Check the consumed HN3 interface and the scope of the frontier change."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def main():
    cert = json.loads((HERE / 'certificate.json').read_text())
    source = HERE.parent / 'hadwiger_nelson_complex_radix_four_curve_gate' / 'exact_four_interface.json'
    data = json.loads(source.read_text())
    if hashlib.sha256(source.read_bytes()).hexdigest() != '76c806cdb5458bbc45e730f7dcd9e3231d6ffc6f4dc99c2013e0f19966c562eb':
        raise ValueError('HN3 source interface bytes')
    if digest(data['no_circle_signature_patterns']) != cert['eligible_patterns_sha256']:
        raise ValueError('entire HN3 no-circle pattern interface')
    pairs = data['pair_representatives']['exact_four_no_circle']
    if len(pairs) != 2528 or any(data['circle_id'] in p for p in pairs):
        raise ValueError('exact-four no-circle pair interface')
    previous = json.loads((HERE.parent / 'hadwiger_nelson_radix_unit_circle' / 'FRONTIER_EFFECT.json').read_text())
    result = {
        'verified': True,
        'minimum_active_curves_for_nonfour_before': 4,
        'minimum_active_curves_for_nonfour_after': 5,
        'eligible_four_active_quartets_closed': cert['eligible_quartets'],
        'exactly_four_active_global_system_obligations_closed': len(pairs),
        'exactly_four_active_global_system_obligations_remaining': 0,
        'whole_global_pair_systems_removed_by_this_result': 0,
        'remaining_global_pair_orbit_representatives': previous['remaining_global_pair_orbit_representatives'],
        'remaining_parameter_orbit_allowance': previous['remaining_parameter_orbit_allowance'],
        'remaining_pair_representatives_sha256': previous['remaining_pair_representatives_sha256'],
        'forbidden_incidence_sets': cert['forbidden_incidence_count'],
        'forbidden_incidence_list_sha256': cert['forbidden_incidence_list_sha256'],
        'scope': 'All retained pair systems now need at least five active curves at a counterexample. No new distinct-root count or whole-system deletion is claimed.',
    }
    if result != json.loads((HERE / 'FRONTIER_EFFECT.json').read_text()):
        raise ValueError('frontier effect checkpoint')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
