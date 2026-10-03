"""Replay the six standalone arithmetic partitions against compact records."""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys


def need(ok,why):
    if not ok:raise RuntimeError(why)


def main():
    parts=['parity']+['column-'+str(q) for q in range(5)]
    parser=argparse.ArgumentParser()
    parser.add_argument('--part',choices=['all']+parts,default='all')
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    expected=json.loads((root/'expected.json').read_text())
    need(set(expected)=={'parity','columns'} and len(expected['columns'])==5,'expected complete domain')
    env=os.environ.copy()
    for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS',
                 'VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):
        env[name]='1'
    selected=parts if args.part=='all' else [args.part]
    records={}
    for part in selected:
        if part=='parity':
            script='audit_parity.py';arguments=[];reference=expected['parity']
        else:
            q=int(part.rsplit('-',1)[1])
            script='audit_column.py';arguments=['--column',str(q)];reference=expected['columns'][q]
            need(reference['column_partition']==q,'expected column partition order')
        need(reference['source_sha256']==sha256((root/script).read_bytes()).hexdigest(),'audit source changed')
        command=[sys.executable]+([] if __debug__ else ['-O'])+[script]+arguments
        try:
            p=subprocess.run(command,cwd=root,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=14)
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError('audit incomplete; no nonexistence inference') from exc
        need(p.returncode==0 and not p.stderr,'audit failed: '+p.stderr.decode())
        record=json.loads(p.stdout)
        need(record==reference,'complete mathematical record differs: '+part)
        records[part]=record
    canonical=json.dumps(records,sort_keys=True,separators=(',',':')).encode()
    print(json.dumps({'status':'STANDALONE_LITERAL_LOCAL_RECORDS_VERIFIED','parts':selected,
                      'records':records,'records_sha256':sha256(canonical).hexdigest(),
                      'ordinary_unformalized_proof_required':True,'all_allocations_enumerated':False,
                      'independent_external_review':False},sort_keys=True))


if __name__=='__main__':main()
