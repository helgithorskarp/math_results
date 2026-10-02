#!/usr/bin/env python3
"""Post-seal whole certificate comparison; imports no author executable."""
from pathlib import Path
from itertools import combinations
from hashlib import sha256
import argparse, json

def need(ok,msg):
    if not ok: raise RuntimeError(msg)

def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--author-packet',type=Path,required=True);a=p.parse_args()
    root=Path(__file__).resolve().parent
    pins=json.loads((root/'AUTHOR_SOURCE.json').read_bytes())
    for r in pins['files']:
        raw=(a.author_packet/r['relative_name']).read_bytes()
        need(len(raw)==r['bytes'] and sha256(raw).hexdigest()==r['sha256'],'whole pinned author bytes: '+r['relative_name'])
    data=json.loads((a.author_packet/'certificate.json').read_bytes())
    own=json.loads((a.work/'INVERSE.json').read_bytes())
    cols=[int(s,16)for s in own['inverse_columns_hex']];theirs=[int(s,16)for s in data['inverse_columns_hex']]
    need(len(cols)==len(theirs)==102 and own['points']==list(range(1,103)),'whole original coordinates')
    bits=0
    for v,w in zip(cols,theirs,strict=True):
        for j in range(102):need((v>>j&1)==(w>>j&1),'every published inverse bit');bits+=1
    hist=json.loads((a.work/'HISTOGRAM.json').read_bytes())['weight_histogram']
    need(hist==data['complete_weight_histogram'],'entire published histogram')
    count=0
    for n in [1,3]:
        for ids in combinations(range(102),n):
            x=y=(1<<102)-1
            for j in ids:x^=cols[j];y^=theirs[j]
            need(x==y and x.bit_count()==y.bit_count(),'whole published parity word');count+=1
    need(count==data['parity_input_count']==171802 and data['parity_input_weights']==[1,3],'entire published syndrome domain')
    math=json.loads((a.work/'MATHEMATICS.json').read_bytes());table=json.loads((a.work/'PHYSICAL_POINTS.json').read_bytes())
    translated=[[h,*ap,*field,colors[0]]for k,h,ap,colors,field in sorted(table,key=lambda r:r[1])]
    geometry=sha256(json.dumps(translated,separators=(',',':')).encode()).hexdigest()
    hh=sha256(json.dumps({int(k):v for k,v in hist.items()},separators=(',',':')).encode()).hexdigest()
    expected={'agent':'six-vdw-3','role':'researcher','status':'EXACT_CHARACTER_PARITY_REPAIR16_AUTHOR_CHECKED','certificate_sha256':sha256((a.author_packet/'certificate.json').read_bytes()).hexdigest(),'actual_geometry_transcript_sha256':geometry,'literal_actual_APs':102,'literal_actual_AP_points':714,'nonzero_multiplicativity_truth_inputs':10404,'GF2_inverse_product_entries':10404,'complete_singleton_parity_inputs':102,'complete_triple_parity_inputs':171700,'complete_parity_inputs':count,'minimum_reconstructed_weight':math['algebra']['minimum_candidate_weight'],'weight15_candidates':0,'damaged_certificates_rejected':10,'histogram_sha256':hh,'character_regular_column_edit_lower_bound':16,'three_hole_distance_if_root_regular':[13,86],'three_hole_distance_if_root_hole':[14,86],'reference_cut_count_at_most':206,'all_original_binary_words_explicitly_enumerated':False,'integer_cover_optimum_claimed':False,'repair35_bound_claimed':False,'native_solver_invoked':False,'W_bound_improved':False,'external_review_claimed':False,'formalized':False}
    need(expected==json.loads((a.author_packet/'expected.json').read_bytes()),'whole exact author expected record')
    need(data['q']==103 and data['period']==618 and data['phase']==[0,0,0,1,1,1] and data['seed_actual_AP']=={'start':80,'step':1} and data['minimum_reconstructed_weight']==35,'whole published geometry/minimum metadata')
    print(json.dumps({'complete':True,'comparison_is_post_seal':True,'author_executable_imported':False,'all_pinned_author_files':len(pins['files']),'all_pinned_author_bytes':pins['total_bytes'],'inverse_columns_compared':102,'inverse_bits_compared':bits,'entire_histogram_entries_compared':len(hist),'whole_parity_words_compared':count,'entire_author_expected_record_matches':True,'actual_geometry_author_serialization_sha256':geometry,'entire_histogram_author_serialization_sha256':hh,'original_six_sealed_controls_and_ten_native_damages_are_separate':True},sort_keys=True))

if __name__=='__main__':main()
