"""Reject ten altered mathematical face/width/continuum/translation fixtures."""
from pathlib import Path
import argparse,copy,json,resource,sys,time
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from primitives import need,digest
import check

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);args=p.parse_args()
    if args.output:need(not args.output.exists(),'fresh output required')
    start=time.monotonic();cert=json.loads((HERE/'certificate.json').read_text())
    valid=check.verify(cert);cases=[]
    q=copy.deepcopy(cert);q['faces'][1]['positive_original_labels'][0]=36
    cases.append(('false_actual_positive_square_vertex',q))
    q=copy.deepcopy(cert);q['faces'][1]['negative_original_labels'].pop()
    cases.append(('lost_genuine_antipodal_square_vertex',q))
    q=copy.deepcopy(cert);q['faces'][1]['orthonormal_square_half_edges'][0][0]=['0','0']
    cases.append(('false_literal_square_half_edge',q))
    q=copy.deepcopy(cert);q['square_inradius_squared']=['4','0']
    cases.append(('overstated_actual_square_inradius',q))
    q=copy.deepcopy(cert);q['left_Cayley_radius']='1/8'
    q['physical_trace_gate']=['191/65','0'];q['physical_squared_Frobenius_gate']=['8/65','0']
    cases.append(('larger_gate_loses_actual32_factor_sign',q))
    q=copy.deepcopy(cert);q['width_edges'][0][1]=37
    cases.append(('false_actual_receiving_width_edge',q))
    q=copy.deepcopy(cert);q['width_rows']['96'][1]=37
    cases.append(('false_actual_nonlinear_source_row',q))
    q=copy.deepcopy(cert);q['receiving_ring'][1]=37
    cases.append(('false_complete_original_receiving_ring',q))
    q=copy.deepcopy(cert);q['translation_source']=40
    cases.append(('nonpersistent_original_translation_contact',q))
    q=copy.deepcopy(cert);q['translation_axis']=[['0','0']]*3
    cases.append(('nonspanning_original_translation_normals',q))
    outcomes=[]
    for label,q in cases:
        try:check.verify(q)
        except ValueError as e:outcomes.append({'damage':label,'rejected':True,'reason':str(e)})
        else:raise ValueError('altered false mathematical certificate accepted: '+label)
    need(len(outcomes)==10,'semantic mathematical controls incomplete')
    mat={'agent':'six-rupert-3','role':'researcher','full_valid_record_sha256':digest(valid),
         'all10_false_mathematical_fixtures_rejected':outcomes,'review_verdict_claimed':False}
    out={'mathematical':mat,'seconds':round(time.monotonic()-start,3),
         'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'optimized':not __debug__,
         'threads':1,'external_child_guard_seconds':20}
    if args.output:args.output.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'all10_rejected':True,'control_mathematical_sha256':digest(mat),
                      'seconds':out['seconds'],'peak_kib':out['peak_kib']},sort_keys=True))
if __name__=='__main__':main()
