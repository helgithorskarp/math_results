"""Cold serial regeneration, byte comparison, literal check and controls."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

def need(test,message):
    if not test:
        raise ValueError(message)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--work',required=True)
    args=parser.parse_args()
    source=Path(__file__).resolve().parent
    work=Path(args.work).resolve()
    work.mkdir(parents=True,exist_ok=True)
    expected=json.loads((source/'expected.json').read_text())
    published=(source/'certificates.json').read_bytes()
    env=dict(os.environ)
    for name in('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
        env[name]='1'
    python=[sys.executable]+(['-O'] if sys.flags.optimize else [])
    begin=time.monotonic()
    receipts=[]
    def run(name,arguments):
        started=time.monotonic()
        command=python+[str(source/name)]+list(map(str,arguments))
        try:
            proc=subprocess.run(command,capture_output=True,text=True,timeout=20,env=env)
        except subprocess.TimeoutExpired as error:
            (work/'INCOMPLETE.json').write_text(json.dumps(dict(status='INCOMPLETE20S_SUBPROCESS_GUARD',command=command))+'\n')
            raise RuntimeError('INCOMPLETE20s subprocess guard; no mathematical absence') from error
        (work/(name+'.stdout')).write_text(proc.stdout)
        (work/(name+'.stderr')).write_text(proc.stderr)
        receipts.append(dict(command=command,exit_code=proc.returncode,seconds=time.monotonic()-started))
        (work/'receipts.json').write_text(json.dumps(receipts,sort_keys=True,indent=2)+'\n')
        need(proc.returncode==0,'incomplete or rejected subprocess: '+name)
        return json.loads(proc.stdout)
    generated=work/'regenerated-certificates.json'
    run('generate.py',['--bridge',source/'BRIDGE.json','--seeds',source/'seed_certificates.json','--output',generated])
    need(generated.read_bytes()==published,'regenerated certificate bytes differ from frozen public certificate')
    result=run('verify.py',['--bridge',source/'BRIDGE.json','--certificate',generated])
    summary={k:v for k,v in result.items() if k!='records'}
    need(summary==expected,'whole mathematical checker summary differs from frozen expected')
    controlled=run('controls.py',['--bridge',source/'BRIDGE.json','--certificate',generated])
    need(controlled['damages']==24 and controlled['transported_interfaces']==102,'incomplete semantic controls')
    stable=dict(status='COMPLETE_FROZEN_POSITIVE_COLORS_AND_LITERAL_CHECKS',result=result,controls=controlled,
                certificate_sha256=hashlib.sha256(published).hexdigest())
    (work/'RESULT.json').write_text(json.dumps(stable,sort_keys=True,indent=2)+'\n')
    metadata=dict(agent='six-code-3',role='researcher',optimized=bool(sys.flags.optimize),
                  python=sys.version,threads=1,seconds=time.monotonic()-begin,
                  peak_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                  source_sha256={name:hashlib.sha256((source/name).read_bytes()).hexdigest()
                                 for name in('generate.py','verify.py','controls.py','reproduce.py')},
                  guards='5s/product producer;20s subprocess;64 seeded priorities per new interface',
                  complete_carrier_dependency='9045, not re-enumerated by this residual package')
    (work/'METADATA.json').write_text(json.dumps(metadata,sort_keys=True,indent=2)+'\n')
    print(json.dumps(dict(status=stable['status'],maximum_upper_bound=result['maximum_upper_bound'],
                         interfaces=result['interfaces'],damages=controlled['damages'],seconds=metadata['seconds'])))

if __name__=='__main__':
    main()
