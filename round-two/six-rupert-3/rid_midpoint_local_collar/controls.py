"""Reject eight semantically false geometric/contact/closure certificates."""
from pathlib import Path
import argparse,copy,json,sys,time,resource
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
import collar,bridge
from primitives import need

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);args=p.parse_args()
    if args.output:need(not args.output.exists(),'fresh output required')
    start=time.monotonic();cert=json.loads((HERE/'certificate.json').read_text());record=collar.verify(cert)
    outcomes=[]
    cases=[]
    q=copy.deepcopy(cert);q['preimages'][0][1]=37;cases.append(('false_actual_spatial_preimage',q))
    q=copy.deepcopy(cert);q['ring'][1]=37;cases.append(('false_actual_receiving_support',q))
    q=copy.deepcopy(cert);q['duals'][0]['selected_labels'][1]=q['duals'][0]['selected_labels'][0];cases.append(('singular_torque_stencil',q))
    q=copy.deepcopy(cert);q['duals'].pop(3);cases.append(('missing_signed_coordinate_target',q))
    q=copy.deepcopy(cert);q['duals'][0]['mass_bound']=1;cases.append(('false_positive_mass_upper_bound',q))
    q=copy.deepcopy(cert);q['left_Cayley_radius']='1/1000';cases.append(('nonabsorbing_physical_closed_radius',q))
    q=copy.deepcopy(cert);q['quadratic_error_bound']='1';cases.append(('understated_geometric_quadratic_error',q))
    for label,q in cases:
        try:collar.verify(q)
        except ValueError as e:outcomes.append({'damage':label,'rejected':True,'reason':str(e)})
        else:raise ValueError('false certificate accepted: '+label)
    q=copy.deepcopy(record);q['all6_exact_uniform_torque_duals'][0]['three_actual_spatial_contacts'][0]=[0,36]
    try:bridge.verify(q,cert)
    except ValueError as e:outcomes.append({'damage':'false_original_nonlinear_contact_bridge','rejected':True,'reason':str(e)})
    else:raise ValueError('false genuine-contact coupling accepted')
    need(len(outcomes)==8,'semantic controls incomplete')
    mathematical={'agent':'six-rupert-3','role':'researcher','all8_false_certificates_rejected':outcomes,'production_valid_certificate_passed':True,'review_verdict_claimed':False}
    out={'mathematical':mathematical,'seconds':round(time.monotonic()-start,3),'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'optimized':not __debug__,'threads':1,'external_child_guard_seconds':20}
    if args.output:args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
