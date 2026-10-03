"""Late, disclosed native-data decoder into the presealed reviewer checkers."""
import argparse
import hashlib
import json
from pathlib import Path
from core import validate as core_validate
from field import P, cover, need
from interval import validate as interval_validate

def compare(native, independent):
    normal = native/'normal'
    geometries = cover()
    checked_rules = different_core_witnesses = 0
    for group in geometries:
        t = group[0]
        record = json.loads((normal/'core'/f't{t:03}.json').read_text())
        need(record['roots'] == [0, 1, t] and record['survivor_words'] == [170, 204, 240], 'native whole core identity')
        decoded = {'t': t, 'witnesses': [[w]+record['witnesses'][str(w)] for w in record['blocked_words']]}
        checked_rules += core_validate(decoded, t)
        original = json.loads((independent/'normal'/('core-'+str(t)+'.json')).read_text())
        different_core_witnesses += sum(a != b for a, b in zip(decoded['witnesses'], original['witnesses']))
    checked_units = cases = differing_units = 0
    for lower in range(0, P, 16):
        upper = min(P, lower+16)
        record = json.loads((normal/'roots'/f'roots{lower:03}-{upper:03}.json').read_text())
        need(record['third_root_range'] == [lower, upper], 'native interval batch range')
        rows = record['cases']
        wanted = [(t, r) for t in range(lower, upper) if t not in (1, 2) for r in (1, 2, t)]
        need([(r['t'], r['projected_root']) for r in rows] == wanted, 'native entire physical domain')
        original = json.loads((independent/'normal'/('units-'+str(lower)+'.json')).read_text())
        for k, source in enumerate(original):
            t = source['t']
            decoded = {'t': t, 'cases': []}
            for row in rows[3*k:3*k+3]:
                need(row['status'] == 'LITERAL_UNIT_VERTICAL_CONTRADICTION' and row['certificate'] is not None, 'native positive unit status')
                cert = row['certificate']
                need(cert['missing_points'] == [], 'native complete unit cover')
                decoded['cases'].append({'root': row['projected_root'], 'column': cert['column'], 'units': cert['unit_demands']})
            checked_units += interval_validate(decoded, t)
            cases += 3
            for a, b in zip(decoded['cases'], source['cases']):
                differing_units += sum(x != y for x, y in zip(a['units'], b['units']))
    final = (normal/'final.json').read_bytes()
    need(final == (native/'optimized'/'final.json').read_bytes(), 'native whole final mode equality')
    need(json.loads(final)['maximum_AP_free_interval_in_this_family'] == 3703, 'native claimed endpoint')
    return {'actual_agent': 'six-reviewer-4', 'role': 'independent mathematical reviewer',
            'method': 'late data-only decoder into unchanged pre-native core and interval validators; not presealed or blind',
            'native_core_rules_rechecked': checked_rules, 'native_physical_projection_cases_rechecked': cases,
            'native_unit_APs_rechecked': checked_units, 'different_canonical_positive_APs': different_core_witnesses,
            'different_integer_unit_APs': differing_units, 'native_final_sha256': hashlib.sha256(final).hexdigest()}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--native', type=Path, required=True)
    parser.add_argument('--independent', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(compare(args.native, args.independent), sort_keys=True, indent=2))
