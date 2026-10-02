#!/usr/bin/env python3
"""Check exact contiguous finite coverage and whole-record commitments."""
import argparse
import hashlib
import json
from pathlib import Path


def need(ok,why):
    if not ok:raise ValueError(why)


def merge(cover,core,roots,seed,transport):
    geometries=cover['geometries']
    need(len(geometries)==103 and geometries==sorted(set(geometries)),'geometry inventory')
    digest=hashlib.sha256();pairs=0;states=0;blocked=0
    for t in geometries:
        source_path=core/f't{t:03}.json';checked_path=core/f't{t:03}-check.json'
        source=json.loads(source_path.read_text());checked=json.loads(checked_path.read_text())
        need(source['roots']==[0,1,t] and checked['t']==t,'geometry identity')
        need(checked['status']=='EXACT_CORE_FILTER_CHECKED' and checked['complete_pairs_replayed']==190036,'complete core domain')
        need(checked['transcript_sha256']==source['transcript_sha256'],'checked core transcript')
        need(checked['survivor_words']==source['survivor_words']==[170,204,240],'complete exact projection classification')
        need(checked['blocked_words']==source['blocked_words'] and len(source['blocked_words'])==125,'all nonprojections refuted')
        need(set(source['blocked_words'])|set(source['survivor_words'])==set(range(0,256,2)),'complete truth domain')
        for path in (source_path,checked_path):digest.update(path.name.encode()+b'\0'+path.read_bytes())
        pairs+=checked['complete_pairs_replayed'];states+=128;blocked+=125
    core_digest=digest.hexdigest()
    need(transport['status']=='COMPLETE_RAW_THREE_ROOT_CORE_CLASSIFICATION','raw field transport')
    need(transport['raw_states_with_literal_positive_witness']==76875 and transport['raw_core_survivors']==1845,'raw state coverage')
    digest=hashlib.sha256();seen=[];units=points=vertical=0
    for start in range(0,617,16):
        stop=min(start+16,617)
        source_path=roots/f'roots{start:03}-{stop:03}.json';checked_path=roots/f'roots{start:03}-{stop:03}-check.json'
        source=json.loads(source_path.read_text());checked=json.loads(checked_path.read_text())
        need(source['third_root_range']==checked['third_root_range']==[start,stop],'contiguous root range')
        need(checked['status']=='COMPLETE_LITERAL_INTERVAL_EXCLUSION' and checked['incomplete_cases']==[],'complete literal interval proof')
        want=[(t,r) for t in range(start,stop) if t not in (1,2) for r in (1,2,t)]
        actual=[(r['t'],r['projected_root']) for r in source['cases']]
        need(actual==want and checked['projection_cases']==checked['closed_cases']==len(want),'root/projection coverage')
        seen.extend(actual)
        for path in (source_path,checked_path):digest.update(path.name.encode()+b'\0'+path.read_bytes())
        units+=checked['literal_unit_APs'];points+=checked['fixed_support_points_checked'];vertical+=checked['vertical_AP_points_checked']
    need(seen==[(t,r) for t in range(617) if t not in (1,2) for r in (1,2,t)],'whole physical projection cover')
    need(units==12915 and points==77490 and vertical==12915,'literal implication totals')
    need(seed['status']=='KNOWN_3703_SEED_INDEPENDENTLY_RECONSTRUCTED_AND_CHECKED' and seed['ordinary_nonconstant_seven_term_APs_checked']==1140833,'known seed exact coverage')
    return {'schema':'boolean617-final-v1','agent':'six-vdw-3','role':'researcher',
            'status':'EXACT_3703_CAP_FOR_AT_MOST_THREE_AFFINE_CHARACTER_INPUTS_CONSTANT_PHASE_NO_EXTRA_EDITS',
            'canonical_field_geometries':103,'canonical_truth_states':states,'canonical_nonprojection_rules_refuted':blocked,
            'complete_canonical_start_step_pairs':pairs,'raw_three_root_truth_states':78720,
            'raw_nonprojection_positive_APs':76875,'raw_projection_survivors':1845,
            'all_geometry_whole_records_sha256':core_digest,
            'field_transport_record_sha256':hashlib.sha256((json.dumps(transport,sort_keys=True,indent=2)+'\n').encode()).hexdigest(),
            'raw_witness_transcript_sha256':transport['raw_witness_transcript_sha256'],
            'physical_projection_cases_literal_refuted':len(seen),'literal_unit_APs':units,
            'unit_fixed_support_points':points,'vertical_AP_points':vertical,
            'whole_interval_records_sha256':digest.hexdigest(),
            'known_seed_APs_checked':1140833,'known_seed_ascii_bits_sha256':seed['coloring_ascii_bits_sha256'],
            'maximum_AP_free_interval_in_this_family':3703,
            'new_3704_coloring':False,'numerical_W_bound_improved':False,
            'phase_scope':'constant; all original root occurrences independently free; zero additional edited nonroot columns',
            'field_affine_quotient_is_not_a_full_interval_quotient':True}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--cover',type=Path,required=True);parser.add_argument('--core',type=Path,required=True);parser.add_argument('--roots',type=Path,required=True);parser.add_argument('--seed',type=Path,required=True);parser.add_argument('--transport',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);parser.add_argument('--expected',type=Path)
    args=parser.parse_args()
    result=merge(json.loads(args.cover.read_text()),args.core,args.roots,json.loads(args.seed.read_text()),json.loads(args.transport.read_text()))
    if args.expected:need(result==json.loads(args.expected.read_text()),'whole compact expected record differs')
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
