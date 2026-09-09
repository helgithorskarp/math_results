"""Regenerate and audit the complete branch; do not run a target solver."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import time
from counter import require

HERE=Path(__file__).resolve().parent

def call(command,path):
    p=subprocess.run(list(map(str,command)),capture_output=True)
    path.write_bytes(p.stdout+p.stderr)
    require(p.returncode==0,'command failed: '+str(command))
    return p.stdout

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();out=args.out;require(not out.exists(),'output exists');out.mkdir(parents=True)
    begin=time.monotonic()
    text=call([sys.executable,'-B',HERE/'counter.py',out/'counter.cnf'],out/'COUNTER.json')
    require(json.loads(text)==json.loads((HERE/'COUNTER.json').read_text()),'counter replay')
    for flags,suffix in [([], 'normal'),(['-O'],'optimized')]:
        text=call([sys.executable,*flags,'-B',HERE/'factor_check.py'],out/('factor-'+suffix+'.json'))
        require(json.loads(text)==json.loads((HERE/'FACTOR_CONTROLS.json').read_text()),'factor replay')
    for name in ['host','audit']:
        call(['g++','-std=c++17','-O3','-Wall','-Wextra','-Werror',HERE/(name+'.cpp'),'-o',out/name],out/('compile-'+name+'.log'))
    text=call([out/'host',out/'counter.cnf',out/'input.cnf'],out/'GENERATION.json')
    require(json.loads(text)==json.loads((HERE/'GENERATION.json').read_text()),'complete generation')
    text=call([out/'audit',out/'input.cnf',out/'counter.cnf'],out/'AUDIT.json')
    require(json.loads(text)==json.loads((HERE/'AUDIT.json').read_text()),'independent audit')
    expected=json.loads((HERE/'PREPARATION.json').read_text())
    for name,field in [('input.cnf','cnf_sha256'),('counter.cnf','counter_sha256')]:
        require(hashlib.sha256((out/name).read_bytes()).hexdigest()==expected[field],'input hash '+name)
    summary={'status':'COMPLETE_BRANCH_ENCODING_REPRODUCED_NO_PHYSICAL_VERDICT','target_solvers_run':0,
             'cnf_sha256':expected['cnf_sha256'],'clauses':15223518,'variables':10317,
             'seconds':time.monotonic()-begin}
    (out/'REPLAY.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,indent=2,sort_keys=True))

if __name__=='__main__':main()
