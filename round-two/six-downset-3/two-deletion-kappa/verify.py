#!/usr/bin/env python3
"""Regenerate the frozen exact evidence; never update EXPECTED.json.

Run from any directory with Python3.11+ and the four pinned sibling
helpers. All matrix allocations have the explicit q<=9 guard.
"""
import bootstrap
from pathlib import Path
import json
import proofs,matrices,bridge,checks
from exact import require,digest

HERE=Path(__file__).resolve().parent

def run():
    expected=json.loads((HERE/'EXPECTED.json').read_text())
    actual={'base':proofs.base(),'cap':proofs.cap_region(),
            'fixtures':[matrices.fixture(q) for q in (7,8,9)],
            'bridge':bridge.run(),
            'entries':[checks.original_entries(q) for q in (7,8,9)]}
    actual['controls']=checks.controls(actual['base'])
    checks.compare(expected,actual)
    require(actual['controls']['rejection_count']==25,'control coverage differs')
    return {'status':'PASS','scope':'every integer q>=7, exactly two bcx deletions',
            'records_sha256':digest(actual),
            'unbounded_floor_determinants':len(actual['base']['lower_floor_determinants']),
            'unbounded_upper_margins':len(actual['base']['weighted_upper_margins']),
            'unbounded_cap_signs':2,
            'literal_orders':[x['N'] for x in actual['fixtures']],
            'whole_ranks':[x['whole_ranks'] for x in actual['fixtures']],
            'original_base_action_columns':actual['bridge']['original_action_columns'],
            'secondary_characteristic_forms':actual['bridge']['secondary_characteristic_forms'],
            'whole_entry_comparisons':sum(x['whole_scaled_and_normalized_entry_comparisons']+x['half_interval_scaled_comparisons'] for x in actual['entries']),
            'rejected_damage_controls':actual['controls']['rejection_count']}

if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
