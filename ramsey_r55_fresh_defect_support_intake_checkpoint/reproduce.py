from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE=Path(__file__).resolve().parent

def run(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    manifest=json.loads((HERE/'MANIFEST.json').read_text())
    for name,sha in manifest.items():
        if hashlib.sha256((HERE/name).read_bytes()).hexdigest()!=sha:
            raise ValueError('source identity '+name)
    expected=json.loads((HERE/'EXPECTED.json').read_text())
    receipts={}
    for label,flags in (('normal',[]),('optimized',['-O'])):
        result=out/f'{label}.json'
        p=subprocess.run([sys.executable,*flags,'-B',str(HERE/'verify_intake.py'),str(HERE/'REGISTRY.jsonl'),str(result)],check=True,capture_output=True)
        actual=json.loads(result.read_text());actual.pop('seconds')
        if actual!=expected:raise ValueError('independent census mismatch')
        control=out/f'{label}-controls.json'
        subprocess.run([sys.executable,*flags,'-B',str(HERE/'reference_controls.py'),str(control)],check=True,capture_output=True)
        rejected=0
        for kind in ('score','padding'):
            rows=[json.loads(s) for s in (HERE/'REGISTRY.jsonl').read_text().splitlines()]
            if kind=='score':rows[0]['score']+=1
            else:rows[0]['red_hex']=format(int(rows[0]['red_hex'],16)|(1<<903),'0226x')
            bad=out/f'{label}-bad-{kind}.jsonl';bad.write_text(''.join(json.dumps(r)+'\n' for r in rows))
            q=subprocess.run([sys.executable,*flags,'-B',str(HERE/'verify_intake.py'),str(bad),str(out/f'{label}-bad-{kind}-out.json')],capture_output=True)
            if q.returncode==0:raise ValueError('accepted corrupted registry '+kind)
            rejected+=1
        receipts[label]={'independent_status':actual['status'],'qualifying_centers':actual['qualifying_distinct_centers'],'corruptions_rejected':rejected,'controls':json.loads(control.read_text())['status']}
    answer={'status':'VERIFIED_FAILED_FRESH_INTAKE_GATE','gate_pass':False,'target_found':False,'new_family_exclusions':0,'receipts':receipts}
    (out/'RECEIPT.json').write_text(json.dumps(answer,indent=2,sort_keys=True)+'\n')
    return answer

if __name__=='__main__':print(json.dumps(run(sys.argv[1]),sort_keys=True))
