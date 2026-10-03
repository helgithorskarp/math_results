"""Complete exact midpoint square-collar replay. CPython3.11+, stdlib only."""
from pathlib import Path
import argparse,hashlib,json,resource,sys,time
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from primitives import need,digest
import geometry,polynomial,continuum

def verify(cert):
    g=geometry.verify(cert)
    return {'original_geometry_and_square_axis':g['data'],
            'physical_three_width_and_translation_closure':polynomial.verify(cert,g),
            'fresh_whole_segment_original_sufficiency':continuum.verify(cert,g)}

def summarize(mat):
    g=mat['original_geometry_and_square_axis']
    p=mat['physical_three_width_and_translation_closure']
    c=mat['fresh_whole_segment_original_sufficiency']
    return {'agent':'six-rupert-3','role':'researcher',
        'whole_mathematical_record_sha256':digest(mat),
        'actual_named_vertex_sha256':g['actual_original_named_vertex_sha256'],
        'source_cayley':g['original_source_cayley'],'receiving_chart':'r=(x,0,1)',
        'entire_closed_receiving_x_interval':p['entire_closed_receiving_x_interval'],
        'closed_physical_left_Cayley_radius':g['closed_physical_left_Cayley_radius'],
        'physical_trace_gate':g['physical_trace_gate'],
        'physical_squared_Frobenius_gate':g['physical_squared_Frobenius_gate'],
        'actual_square_positive_source_labels':g['complete_actual_paired_square_faces'][1]['positive_original_labels'],
        'actual_square_inradius_squared':g['actual_square_inradius_squared'],
        'strict_cusp_squared_margin':g['strict_cusp_squared_margin'],
        'all_actual_paired_face_support_controls':g['all_original_face_support_controls'],
        'all_actual_paired_width_endpoint_controls':p['all480_endpoint_paired_support_controls'],
        'direct_full_physical_Rodrigues_fixtures':len(p['all18_direct_physical_Rodrigues_fixtures']),
        'full_two_width_determinant_coefficients':p['full_two_support_determinant_coefficients'],
        'fresh_original_continuum_endpoint_support_controls':c['all_full_closed_endpoint_receiving_and_moving_support_controls'],
        'fresh_original_continuum_endpoint_cyclic_turn_controls':c['all_full_closed_endpoint_cyclic_turn_controls'],
        'all_nondegenerate_cyclic_triple_witnesses':len(c['all_strict_nondegenerate_triples']),
        'all_distinct_whole_interval_planar_pair_controls':len(c['all153_distinct_planar_pair_controls']),
        'midpoint_affinity_fixtures':c['additional_exact_midpoint_affinity_support_fixtures']+c['additional_exact_midpoint_affinity_turn_fixtures'],
        'old_fixed_source_feasibility_theorem_dependency':False,
        'old_line_inventory_stress_or_source_forest_input':False,
        'original_quantified_classification':'Every original physical t and lambda>=1; in the stated closed physical left collar, fit iff parent motion,lambda1,originalt0. Ordinary proper body/right and receiving-axis half-turn covariance covers SET R*G union H_rR*G.',
        'source_gate_is_a_hypothesis':True,'all_source_cover_claimed':False,
        'two_dimensional_receiver_domain_claimed':False,
        'new_group_enumeration_or_distinct_motion_count_claimed':False,
        'strict_Rupert_passage_claimed':False,'global_RID':'OPEN',
        'proof_status':'author checked, unformalized, independently UNREVIEWED'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);p.add_argument('--compare',type=Path)
    args=p.parse_args();start=time.monotonic()
    if args.output:need(not args.output.exists(),'fresh output required')
    cert=json.loads((HERE/'certificate.json').read_text());mat=verify(cert);summary=summarize(mat)
    if args.compare:need(summary==json.loads(args.compare.read_text()),'full mathematical record fingerprint or scope differs')
    source_names=['check.py','geometry.py','polynomial.py','continuum.py','primitives.py','field.py','certificate.json','expected.json','controls.py']
    out={'mathematical':mat,'summary':summary,'seconds':round(time.monotonic()-start,3),
         'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'optimized':not __debug__,
         'threads':1,'external_child_guard_seconds':20,
         'runtime_source_sha256':{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in source_names}}
    if args.output:args.output.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'summary':summary,'seconds':out['seconds'],'peak_kib':out['peak_kib'],'optimized':out['optimized']},sort_keys=True))
if __name__=='__main__':main()
