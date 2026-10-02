"""Damaged proof inputs and invalid differentiation domains must reject."""
from copy import deepcopy
from pathlib import Path
import json
import model,replay
HERE=Path(__file__).resolve().parent
def rejected(action):
    try:action()
    except (ValueError,ArithmeticError):return True
    return False
def main():
    z=json.loads((HERE/'PLAN-z-out.json').read_text())
    d=json.loads((HERE/'PLAN-dz-68.json').read_text())
    cases={}
    bad=deepcopy(z);bad['box'][0]='577/1000'
    cases['omitted_lower_domain']=rejected(lambda:replay.replay(bad))
    bad=deepcopy(z);bad['branch']=[1,1]
    cases['wrong_orientation']=rejected(lambda:replay.replay(bad))
    bad=deepcopy(z);bad['tree']='00'
    cases['strict_target_on_unsplit_box']=rejected(lambda:replay.replay(bad))
    bad=deepcopy(d);bad['tree']=bad['tree'][:bad['tree'].index('ff')+1]
    cases['truncated_derivative_partition']=rejected(lambda:replay.replay(bad))
    bad=deepcopy(d);bad['tree']='00'
    cases['derivative_target_replaced_by_packing_predicate']=rejected(lambda:replay.replay(bad))
    cases['whole_box_regularity_required']=rejected(lambda:model.enclosed(model.Q(14,25),model.Q(593,1000),model.Q(-5,2),model.Q(5,2)))
    model.D2.rt=model.D2.rz=model.Q(0)
    cases['zero_radical_not_differentiated']=rejected(lambda:model.D2(0).sqrt())
    if not all(cases.values()):raise ValueError('a damaged proof input was accepted')
    return {'status':'ALL_SEVEN_DAMAGED_CONTROLS_REJECTED','controls':cases}
if __name__=='__main__':print(json.dumps(main(),indent=2))
