"""Check saved compact result provenance and scope; not a second proof run."""
from pathlib import Path
import argparse
import json
from audit import BASE, digest
from incidence import need


def run(record, controls, strengthening=None):
    result=json.loads(record.read_text())
    expected=json.loads((BASE/'expected.json').read_text())
    need(result['status']=='COMPLETE direct all-labeling audit' and digest(result)==expected['audit_record_sha256'],'saved full audit record mismatch')
    need(result['raw_assignments']==64*1296*5040 and result['ordered_joint_classes']==128 and result['maximum_code_upper']==66,'incorrect scope/counts')
    need(2*result['unordered_center_classes']==result['ordered_joint_classes']+result['center_swap_fixed_ordered_classes'],'center-swap Burnside count differs')
    checks=json.loads(controls.read_text())
    need(checks['status']=='COMPLETE independent controls' and digest(checks)==expected['control_record_sha256'],'saved control record mismatch')
    need(checks['sanitizer_diagnostics']==0 and checks['literal_fiber_nodes']==4*5040 and checks['sanitizer_full_assignments']==1296*5040,'incorrect control scope')
    if strengthening is not None:
        improved=json.loads(strengthening.read_text())
        need(improved==json.loads((BASE/'improvement.json').read_text()) and improved['maximum_code_upper']==65,'saved strengthening record mismatch')
    print(json.dumps(dict(status='VERIFIED saved audit/control provenance; no new enumeration',audit_sha256=digest(result),controls_sha256=digest(checks),strengthening_checked=strengthening is not None)),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--record',type=Path,required=True);p.add_argument('--control-record',type=Path,required=True);p.add_argument('--strengthening-record',type=Path);a=p.parse_args();run(a.record,a.control_record,a.strengthening_record)
