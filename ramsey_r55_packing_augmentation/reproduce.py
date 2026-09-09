"""Fresh-output replay, independent checking, and optimized-mode controls."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE=Path(__file__).resolve().parent

def run(out):
    out=Path(out); out.mkdir(parents=True,exist_ok=False)
    manifest=json.loads((HERE/'MANIFEST.json').read_text())
    for name,sha in manifest.items():
        if hashlib.sha256((HERE/name).read_bytes()).hexdigest()!=sha:
            raise ValueError('source identity '+name)
    receipts={}
    for label,flags in (('normal',[]),('optimized',['-O'])):
        result=out/f'{label}.json'
        p=subprocess.run([sys.executable,*flags,'-B',str(HERE/'count.py')],check=True,capture_output=True)
        result.write_bytes(p.stdout)
        if json.loads(p.stdout)!=json.loads((HERE/'EXPECTED.json').read_text()):
            raise ValueError('expected count')
        check=subprocess.run([sys.executable,*flags,'-B',str(HERE/'independent_check.py'),str(result)],check=True,capture_output=True)
        physical=subprocess.run([sys.executable,*flags,'-B',str(HERE/'controls.py'),str(out/f'{label}-controls')],check=True,capture_output=True)
        rejected=0
        for which in ('marginal','global','composite'):
            bad=json.loads(p.stdout)
            if which=='marginal':bad['levels'][3]['allowed']+=1
            elif which=='global':bad['new_carrier']+=1
            else:bad['new_composite_upper']['numerator']+=1
            path=out/f'{label}-bad-{which}.json'; path.write_text(json.dumps(bad)+'\n')
            r=subprocess.run([sys.executable,*flags,'-B',str(HERE/'independent_check.py'),str(path)],capture_output=True)
            if r.returncode==0:raise ValueError('accepted numerical corruption')
            rejected+=1
        receipts[label]={'count':json.loads(check.stdout),'physical':json.loads(physical.stdout),'numeric_corruptions_rejected':rejected}
    answer={'status':'REPRODUCED_GLOBAL_PACKING_AUGMENTATION_REDUCTION','receipts':receipts,'python':sys.version}
    (out/'RECEIPT.json').write_text(json.dumps(answer,indent=2,sort_keys=True)+'\n')
    return answer

if __name__=='__main__':
    print(json.dumps(run(sys.argv[1]),sort_keys=True))
