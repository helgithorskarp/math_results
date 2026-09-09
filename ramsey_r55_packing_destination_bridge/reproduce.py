"""Fresh deterministic replay. No solver, candidate search, or q10 child input."""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent

def need(ok,why):
    if not ok:raise ValueError(why)

def stable(obj):
    if isinstance(obj,dict):return {k:stable(v) for k,v in obj.items() if k!='seconds'}
    if isinstance(obj,list):return [stable(v) for v in obj]
    return obj

def verify_expected(result):
    expected=json.loads((HERE/'EXPECTED.json').read_text())
    need(result==expected,'committed expectation mismatch')
    for path in (('census','affected_tasks'),('physical','edge_identities'),('formulas','clauses_checked')):
        bad=json.loads(json.dumps(expected));bad[path[0]][path[1]]+=1
        need(result!=bad,'accepted altered expected count')
    return {'status':'VERIFIED_COMPLETE_PACKING_BRIDGE_EXPECTATION','altered_counts_rejected':3}

def run(cache,out,record=False):
    cache=Path(cache).resolve();out=Path(out).resolve();out.mkdir()
    start=time.monotonic()
    def call(script,args,label,optimized=False):
        command=[sys.executable]+(['-O'] if optimized else [])+['-B',str(HERE/script)]+[str(x) for x in args]
        with (out/(label+'.log')).open('xb') as log:
            result=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT)
        need(result.returncode==0,'stage failed: '+label+'; inspect '+str(out/(label+'.log')))
        print(json.dumps({'completed':label}),flush=True)
    call('lookup.py',[cache,out/'tables'],'lookup')
    call('census.py',[cache,out],'census')
    normal=None
    for optimized in (False,True):
        mode='optimized' if optimized else 'normal'
        call('check_census.py',[cache,out,'--receipt',out/(mode+'-census.json')],mode+'-census',optimized)
        call('corruptions.py',[cache,out],mode+'-corruptions',optimized)
        call('controls.py',[cache,out/'tables',out/(mode+'-physical')],mode+'-physical',optimized)
        call('audit_formulas.py',[cache,out/(mode+'-formulas')],mode+'-formulas',optimized)
        receipt={
            'lookup':json.loads((out/'tables'/'LOOKUP.json').read_text()),
            'census':json.loads((out/'CENSUS.json').read_text()),
            'independent_census':json.loads((out/(mode+'-census.json')).read_text()),
            'physical':json.loads((out/(mode+'-physical')/'PHYSICAL.json').read_text()),
            'formulas':json.loads((out/(mode+'-formulas')/'FORMULAS_CHECK.json').read_text()),
            'corruptions':json.loads((out/(mode+'-corruptions.log')).read_text())}
        receipt=stable(receipt)
        if normal is None:normal=receipt
        else:need(normal==receipt,'normal/optimized evidence differs')
    # Explicitly record a producer output, or enforce the committed expectation.
    if not record:
        verify_expected(normal)
    (out/'RESULT.json').write_text(json.dumps(normal,indent=2,sort_keys=True)+'\n')
    result={'status':'RECORDED_COMPLETE_PACKING_BRIDGE' if record else 'REPRODUCED_COMPLETE_PACKING_BRIDGE',
            'seconds':time.monotonic()-start,'python':sys.version,'platform':platform.platform(),
            'normal_and_optimized_agree':True,'target_found':False,'new_task_decisions':0,
            'result_sha256':hashlib.sha256((out/'RESULT.json').read_bytes()).hexdigest()}
    (out/'REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('cache');p.add_argument('out');p.add_argument('--record',action='store_true');args=p.parse_args()
    print(json.dumps(run(args.cache,args.out,args.record),sort_keys=True))
