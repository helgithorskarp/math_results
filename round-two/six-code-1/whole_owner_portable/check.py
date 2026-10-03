"""Compare all completed records and compact expectations after cold generation."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'literal'))
from model import digest, encode, need


def math(directory):
    p = json.loads((directory / 'progress.json').read_bytes())
    m = json.loads((directory / 'mathematical-record.json').read_bytes())
    need(p['complete'] and p['mathematical_sha256'] == digest(m), 'entire completed mathematical record')
    return m


def packet(work):
    p = json.loads((work / 'progress.json').read_bytes())
    need(p['complete'] and p['modes'] == ['normal', 'optimized'], 'both complete cold modes required')
    children = {}
    for mode in p['modes']:
        rows = [c for c in p['completed_children'] if c['mode'] == mode]
        need(len(rows) == len({c['name'] for c in rows}), 'each child exactly once')
        children[mode] = {}
        for c in rows:
            m = math(work / mode / c['name'])
            need(digest(m) == c['mathematical_sha256'], 'entire parent/child mathematical binding')
            children[mode][c['name']] = digest(m)
    need(children['normal'] == children['optimized'], 'all complete mathematical records identical across modes')
    streams = []
    for fi in range(23):
        streams.extend(['fixture-%02d/complete-owner-records.jsonl' % fi,
                        'fixture-%02d/selected-physical-owners.json' % fi])
    streams.extend(['aggregate/decorated-classes.json', 'derived/complete-owner-records.jsonl',
                    'derived/all697.json', 'derived/input-1426.json', 'derived/input-1599.json'])
    for t in [1426, 1599]:
        streams.extend(['prepare-%d/whole-free-bindings.json' % t,
                        'assemble-%d/complete-decisions.jsonl' % t,
                        'assemble-%d/actual37-certificates.json' % t,
                        'gate-%d/complete-pair-decisions.jsonl' % t])
    for name in streams:
        need((work / 'normal' / name).read_bytes() == (work / 'optimized' / name).read_bytes(),
             'every actual complete output byte across modes: ' + name)
    n = work / 'normal'
    aggregate = math(n / 'aggregate')
    bases = []
    for t in [1426, 1599]:
        interfaces = math(n / ('interfaces-%d' % t))
        gate = math(n / ('gate-%d' % t))
        assembled = math(n / ('assemble-%d' % t))
        bases.append({'type_id': t, 'all_original_rows': interfaces['all_original_owner_rows'],
                      'whole_cases': assembled['whole_case_count'],
                      'whole_case_records_sha256': assembled['whole_case_records_sha256'],
                      'whole37_certificates_sha256': assembled['whole37_certificates_sha256'],
                      'actual37_maps': interfaces['actual37_map_count'],
                      'literal37_unions': interfaces['literal_distinct37_unions'],
                      'literal_right_interfaces': interfaces['literal_distinct_right_interfaces'],
                      'all_literal_right_records_sha256': digest(interfaces['all_actual37_right_interface_records']),
                      'all_actual_SAT_patterns': interfaces['all_actual_SAT_only_incidence_patterns'],
                      'whole697_pair_cases': gate['complete_pair_cases'],
                      'entire_pair_record_sha256': gate['entire_pair_record_sha256'],
                      'realized_pairs': gate['realized_D2_pairs']})
    transport = math(n / 'transport')
    return {'actual_agent': 'six-code-1', 'role': 'researcher', 'complete': True,
            'all_source_only_children_per_mode': len(children['normal']),
            'all_children_mathematical_sha256': [[name, sha] for name, sha in sorted(children['normal'].items())],
            'all_mode_output_bytes_identical': True, 'explicit_complete_streams_compared': len(streams),
            'inventory': {k: aggregate[k] for k in ['all_physical_T1_owners',
                'selected_zero_Hub_z0_physical_owners', 'all_original_named_rows',
                'all_original_colored_classes', 'D2_original_type_ids',
                'entire_original_named_record_list_sha256', 'entire_original_decorated_classes_sha256']},
            'all_base_results': bases,
            'whole697_inventory_actions': transport['complete_inventory_action_pairs'],
            'all_inventory_actions_bijective': transport['all12_inventory_actions_closed_bijections'],
            'all48_original_rows_covered': transport['all_original_owner_rows_covered'],
            'all_original_row_count': transport['complete_original_owner_rows'],
            'entire_whole_star_transport_sha256': digest(transport),
            'conditionally_excluded_types': transport['conditionally_excluded_types'],
            'normalization_and_application_bridges': 'ordinary unformalized',
            'independent_person_review': 'pending', 'global_endpoint_change': False}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', type=Path, required=True)
    args = ap.parse_args()
    manifest = json.loads((ROOT / 'PUBLIC_MANIFEST.json').read_bytes())
    for pin in manifest['source_files']:
        raw = (ROOT / pin['name']).read_bytes()
        need(len(raw) == pin['bytes'] and hashlib.sha256(raw).hexdigest() == pin['sha256'],
             'entire public source: ' + pin['name'])
    result = packet(args.work)
    expected = json.loads((ROOT / 'EXPECTED.json').read_bytes())
    need(result == expected, 'entire completed mathematical packet versus compact expectations')
    print(json.dumps({'complete': True, 'whole_mathematical_sha256': digest(result),
                      'children': 2 * result['all_source_only_children_per_mode'],
                      'original_rows': result['all_original_row_count'],
                      'excluded_types': result['conditionally_excluded_types']}))


if __name__ == '__main__':
    main()
