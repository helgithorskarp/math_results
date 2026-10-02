"""Run two independent algorithms and exact whole-record checks, serially."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import controls
from conclude import conclusion

def require(condition,message):
    if not condition:raise ValueError(message)
def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);args=p.parse_args()
    require(not args.work.exists(),'fresh work directory required');args.work.mkdir(parents=True)
    root=Path(__file__).resolve().parent
    env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
    mode=['-O'] if sys.flags.optimize else []
    for filename,output in (('produce.py','producer.json'),('verify.py','independent.json')):
        subprocess.run([sys.executable,*mode,str(root/filename),'--out',str(args.work/output)],check=True,env=env)
    first=(args.work/'producer.json').read_bytes();second=(args.work/'independent.json').read_bytes()
    require(first==second,'whole physical row and inventory records disagree')
    data=json.loads(first);expected=json.loads((root/'expected.json').read_text())
    require(data['inventory']==expected,'whole frozen inventory differs')
    result=dict(agent='six-code-3',role='researcher',fixture_sha256=hashlib.sha256((root/'fixtures.json').read_bytes()).hexdigest(),
                all426_physical_row_records_sha256=hashlib.sha256(json.dumps(data['rows'],sort_keys=True,separators=(',',':')).encode()).hexdigest(),
                whole_inventory_sha256=hashlib.sha256(json.dumps(expected,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
                conclusion=conclusion(expected),controls=controls.run(json.loads((root/'fixtures.json').read_text()),expected))
    require(result['conclusion']==json.loads((root/'certificate.json').read_text()),'frozen scalar certificate differs')
    (args.work/'RESULT.json').write_text(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
