#!/usr/bin/env python3
"""Replay a frozen expected record and reject six damaged hypotheses."""
from fractions import Fraction as F
from pathlib import Path
import argparse,copy,hashlib,json,resource,subprocess,sys,time

HERE=Path(__file__).resolve().parent

def require(ok,message):
    if not ok:raise ValueError(message)

def mode():
    # Record existence and bytes before importing/running the checker.
    fixture=HERE/'expected.json'
    existed=fixture.is_file();require(existed,'frozen expected record absent at entry')
    expected_bytes=fixture.read_bytes();expected=json.loads(expected_bytes)
    certificate_bytes=(HERE/'certificate.json').read_bytes()
    certificate=json.loads(certificate_bytes)
    import check as C
    record=C.check(certificate)
    record['certificate_sha256']=hashlib.sha256(certificate_bytes).hexdigest()
    require(record==expected,'frozen expected record changed or replay differs')
    mutations=[]
    item=copy.deepcopy(certificate)
    item['contacts'][0][0],item['contacts'][0][1]=item['contacts'][0][1],item['contacts'][0][0]
    mutations.append(('reversed_support_normal',item,{},'positive original support height'))
    item=copy.deepcopy(certificate);item['contacts'][0][2]=0
    mutations.append(('nonendpoint_contact',item,{},'original contact labels and normal scale'))
    item=copy.deepcopy(certificate);item['contacts'][0][3]=4
    mutations.append(('normal_remainder_bound_overstated',item,{},'uniform selected normal length < 2'))
    item=copy.deepcopy(certificate);item['correction_rows'][-1]=item['correction_rows'][-2]
    mutations.append(('duplicate_correction_column',item,{},'five distinct correction rows'))
    item=copy.deepcopy(certificate)
    fixed=next(i for i in range(6) if i not in item['correction_rows'])
    item['fixed_weight_numerators'][fixed]=0
    mutations.append(('zero_fixed_stress_weight',item,{},'one positive fixed weight; only correction weights omitted'))
    mutations.append(('overstated_cayley_radius',certificate,{'eta':F(1,1000)},'nonlinear Cayley contraction gate'))
    refused=[]
    for name,item,kwargs,message in mutations:
        try:C.check(item,**kwargs)
        except ValueError as e:
            require(str(e)==message,'unexpected failure for damaged control '+name+': '+str(e))
            refused.append({'name':name,'reason':message})
        else:raise ValueError('damaged control accepted: '+name)
    require(fixture.read_bytes()==expected_bytes,'validation rewrote the frozen fixture')
    return {'fixture_existed_before_validation':existed,
            'fixture_sha256':hashlib.sha256(expected_bytes).hexdigest(),
            'certificate_sha256':hashlib.sha256(certificate_bytes).hexdigest(),
            'frozen_expected_record_reproduced':True,'damaged_controls_rejected':refused}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--single-mode',action='store_true')
    parser.add_argument('--output',type=Path)
    parser.add_argument('--timing-output',type=Path)
    args=parser.parse_args();start=time.monotonic()
    if args.single_mode:
        print(json.dumps(mode(),sort_keys=True));return
    modes=[];timings=[]
    for optimized in (False,True):
        command=[sys.executable]+(['-O'] if optimized else [])+['-B',str(Path(__file__).resolve()),'--single-mode']
        stamp=time.monotonic()
        result=subprocess.run(command,capture_output=True,text=True,timeout=55,cwd=HERE)
        require(result.returncode==0,'mode validation failed: '+result.stderr)
        modes.append(json.loads(result.stdout));timings.append(time.monotonic()-stamp)
    require(modes[0]==modes[1],'normal/optimized validation differs')
    output={'agent':'six-rupert-1','role':'researcher',
            'status':'NORMAL_AND_OPTIMIZED_EXACT_CHECKS_AND_SIX_DAMAGE_CONTROLS_PASSED',
            'python_requirement':'3.11+ standard library only','threads':1,
            'normal_and_optimized_records_identical':True,
            'fixture_provenance':'Expected record created from the exact checker for this contribution, then frozen before these replays; no pre-existing regression fixture or independent audit claimed',
            **modes[0]}
    if args.output:args.output.write_text(json.dumps(output,sort_keys=True,indent=2)+'\n')
    else:print(json.dumps(output,sort_keys=True,indent=2))
    if args.timing_output:
        timing={'normal_seconds':timings[0],'optimized_seconds':timings[1],
                'total_seconds':time.monotonic()-start,
                'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                'peak_parent_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
        args.timing_output.write_text(json.dumps(timing,sort_keys=True,indent=2)+'\n')

if __name__=='__main__':main()
