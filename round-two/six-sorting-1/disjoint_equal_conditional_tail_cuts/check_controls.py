"""Eight semantic corruptions, each with repaired whole finite hashes."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

from run import digest,operations_allow,ENV

ROOT=Path(__file__).resolve().parent


def main():
    original=(ROOT/'work/proposal.json').read_bytes();valid=json.loads(original)
    cases=[];start=time.monotonic()
    def case(name,reason,mutate):
        bad=deepcopy(valid);mutate(bad['finite']);bad['finite_sha256']=digest(bad['finite'])
        cases.append((name,reason,bad))
    def first(f):return f['route_records'][0]
    case('false-original-cost','False original seed D/R cost',
         lambda f:first(f).__setitem__('actual_original_seed_D',8))
    case('missing-conditional-input','Missing or substituted original conditional assignment',
         lambda f:first(f)['complete_original_conditional_assignments'].pop())
    case('false-attained-maximum','False attained conditional maximum',
         lambda f:first(f).__setitem__('attained_conditional_maximum_mask',63))
    case('nonzero-output-head','Actual nonzero output used as a zero head',
         lambda f:first(f)['conservative_output_envelope'][0]['bindings'][0].__setitem__('head_port',5))
    case('erased-head-move','Actual singleton head root was not routed',
         lambda f:next(b for b in f['route_records'][1]['conservative_output_envelope'][1]['bindings']
                       if b['head_port']==8).__setitem__('actual_head_root',7))
    case('marked-tail-gate-called-identity','False literal tail or original identity position',
         lambda f:first(f)['conservative_output_envelope'][0]['bindings'][0].__setitem__('identity_tail_index',0))
    case('false-fixed-zero-port','False fixed zero-head labels',
         lambda f:first(f).__setitem__('fixed_head_ports',[2,3,5]))
    case('whole-route-overclaim','Outside claimed scope or complete finite fields differ',
         lambda f:f.__setitem__('entire_six_routes_excluded',True))
    records=[]
    for name,reason,bad in cases:
        file=ROOT/'work'/('damage-'+name+'.json');file.write_text(json.dumps(bad,indent=2)+'\n')
        for optimized in (False,True):
            operations_allow()
            cmd=[sys.executable]+(['-O'] if optimized else [])+[str(ROOT/'verify.py'),str(file)]
            result=subprocess.run(cmd,env=ENV,capture_output=True,text=True,timeout=55)
            if result.returncode==0 or reason not in result.stderr:
                raise ValueError('Damage did not fail for intended mathematical reason: '+name)
            records.append({'damage':name,'optimized':optimized,'returncode':result.returncode,
                            'intended_semantic_reason':reason,'whole_finite_transport_hash_repaired':True})
    if (ROOT/'work/proposal.json').read_bytes()!=original:
        raise ValueError('Genuine proposal bytes changed')
    finite={'genuine_proposal_finite_sha256':valid['finite_sha256'],'controls':records,
            'all16_intended_semantic_rejections':True,'genuine_proposal_bytes_unchanged':True}
    result={'agent':'six-sorting-1','role':'researcher','finite':finite,
            'finite_sha256':digest(finite),'seconds':time.monotonic()-start}
    (ROOT/'work/controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'finite_sha256':result['finite_sha256'],'seconds':result['seconds']}),flush=True)


if __name__=='__main__':main()
