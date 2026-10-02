#!/usr/bin/env python3
"""Exact local consequences, conditional on the eleven checked refutations."""
import argparse
import itertools
import json
from pathlib import Path


def need(condition,message):
    if not condition:
        raise ValueError(message)


def scope(cover,expected):
    # cover_check.py must separately establish this complete input domain.
    # This census checks how the selected refutations and the cited zero-case
    # theorem restrict it. It is not a standalone UNSAT verifier.
    proved = expected['proved_case_numbers']
    need(proved == list(range(1,12)), 'Declared checked family changed')
    need(len(cover['cases']) == 15, 'Incomplete singleton input cover')
    cases = expected['cases']
    need([c['number'] for c in cases] == list(range(1,16)), 'Frozen model family changed')
    excluded = set()
    all_inputs = set()
    for number,(input_case,model_case) in enumerate(zip(cover['cases'],cases),1):
        model = model_case['model']
        need(model['holes'] == input_case['holes'] and
             model['opposite_satellite'] == input_case['unique_opposite_satellite'] and
             model['regular_core'] == input_case['regular_core'] and
             model['fixed_core_bits'] == input_case['fixed_core_bits'],
             'Model does not match its exact singleton input class')
        members = {(tuple(r['holes']),r['opposite']) for r in input_case['represented_inputs']}
        need(len(members)==2 and not members.intersection(all_inputs), 'Repeated/incomplete raw inputs')
        all_inputs.update(members)
        if number in proved:
            need(model_case['proof']['mathematical_exclusion'] is True and
                 model_case['proof']['cnf_sha256'] == model['cnf_sha256'],
                 'Missing declared checked refutation')
            excluded.update(members)
    need(len(all_inputs)==30 and len(excluded)==22, 'Wrong quantified negative cover')
    need(expected['zero_case_dependency']['height']==9205 and
         expected['zero_case_dependency']['reference']=='bafkreibbwtzo6m3c2ahfo33ldjbtfz3qiz4lnugwa4ahjy5mr5cuhcgqoi',
         'Zero-case mathematical premise changed')
    seed = set(range(5))
    local = set(cover['thirteen_pattern'])
    holes = sorted({h for h,x in all_inputs})
    records = []
    for h in holes:
        satellites = tuple(sorted(local-set(h)-seed))
        need(len(satellites)==5, 'Wrong regular satellite domain')
        accepted = []
        for bits in itertools.product((0,1),repeat=5):
            opposite = tuple(x for x,b in zip(satellites,bits) if b)
            if not opposite:  # Imported conditional zero-satellite theorem9205.
                continue
            if len(opposite)==1 and (h,opposite[0]) in excluded:
                continue
            accepted.append(bits)
        singleton = sorted(x for hh,x in all_inputs-excluded if hh==h)
        records.append({'holes':list(h),'regular_satellites':list(satellites),
                        'singleton_choices_excluded':sorted(x for hh,x in excluded if hh==h),
                        'singleton_choices_remaining_unresolved':singleton,
                        'necessary_local_binary_patterns_remaining':len(accepted),
                        'opposite_satellite_lower_bound':min(sum(b) for b in accepted)})
    result = {'all_exceptional_hole_geometries':6,'local_binary_patterns_before_global_cuts':192,
              'zero_patterns_excluded_by_cited_dependency':6,
              'new_singleton_raw_inputs_excluded':22,'new_singleton_reflection_classes_excluded':11,
              'singleton_raw_inputs_remaining_unresolved':8,
              'necessary_local_binary_patterns_remaining':sum(r['necessary_local_binary_patterns_remaining'] for r in records),
              'at_least_two_hole_geometries':[r['holes'] for r in records if r['opposite_satellite_lower_bound']==2],
              'geometry_records':records,'uniform_six_geometry_at_least_two_proved':False,
              'admissible_global_colorings_counted':False,'W_bound_improved':False}
    need(result == expected['restricted_profile_scope'], 'Declared local consequence/census changed')
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cover',type=Path,required=True)
    p.add_argument('--expected',type=Path,required=True)
    a=p.parse_args()
    print(json.dumps(scope(json.loads(a.cover.read_text()),json.loads(a.expected.read_text()))))
