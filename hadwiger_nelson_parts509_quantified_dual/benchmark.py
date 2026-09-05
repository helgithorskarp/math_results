#!/usr/bin/env python3
"""Bounded controls and an independently checked fixed509 SAT proof."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import resource
import subprocess
import time
import encode_dual as enc
import verify_dual


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--depqbf',type=Path,required=True)
    ap.add_argument('--kissat',type=Path,required=True)
    ap.add_argument('--drat-trim',type=Path,required=True)
    ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('--real-seconds',type=int,default=30)
    ap.add_argument('--proof-seconds',type=int,default=120)
    args=ap.parse_args()
    enc.require(args.real_seconds>0 and args.proof_seconds>0,'positive limits')
    args.work.mkdir(parents=True,exist_ok=True)
    enc.require(not (args.work/'result.json').exists(),'fresh work directory required')
    result=dict(status='running bounded controls',tools={k:dict(path=str(p.resolve()),sha256=sha256(p.read_bytes()).hexdigest())
        for k,p in [('depqbf',args.depqbf),('kissat',args.kissat),('drat_trim',args.drat_trim)]},rows=[])
    started=time.monotonic()

    def save():
        result['total_seconds']=time.monotonic()-started
        result['maximum_child_peak_rss_kib']=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
        tmp=args.work/'result.json.tmp'
        tmp.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
        tmp.replace(args.work/'result.json')

    def call(name,cmd,seconds):
        begin=time.monotonic()
        with (args.work/(name+'.log')).open('w') as f:
            try:
                rc=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=seconds).returncode
            except subprocess.TimeoutExpired:
                rc='watchdog_timeout'
        return dict(returncode=rc,seconds=time.monotonic()-begin,command=cmd)

    def qbf(name,raw,expected,limit):
        path=args.work/(name+'.qdimacs');path.write_bytes(raw)
        row=call(name,[str(args.depqbf.resolve()),'--qdo',f'--max-secs={limit}',str(path.resolve())],limit+5)
        row.update(name=name,expected=expected,qdimacs_sha256=sha256(raw).hexdigest(),solver_limit_seconds=limit)
        row['truth']=True if row['returncode']==10 else False if row['returncode']==20 else None
        enc.require(row['truth'] is None or row['truth']==expected,('native contradiction',name))
        result['rows'].append(row);save()
        print(json.dumps(dict(name=name,truth=row['truth'],seconds=row['seconds'])),flush=True)

    enc.original()
    expectations={r['name']:r['dual_truth'] for r in json.loads((enc.HERE/'expected.json').read_text())['abstract_controls']}
    for case in verify_dual.fixtures():
        raw,_=enc.encode(**{k:case[k] for k in ['n','edges','cross','patterns','budget']})
        qbf(case['name'],raw,expectations[case['name']],5)
    old=enc.original();source,U=old.pool_input()
    controls={}
    for name,deleted,expected in [('record509',None,False),('delete397',397,True)]:
        indices=[i for i,v in enumerate(U) if v<509 and v!=deleted]
        H=old.restrict(source,indices)
        raw,meta=enc.encode(**H,budget=H['n'],selection=set(range(H['n'])))
        qbf(name,raw,expected,args.real_seconds)
        cnf=args.work/(name+'.cnf');cnf.write_bytes(enc.to_cnf(raw))
        controls[name]=(cnf,meta)
        if name=='delete397' and result['rows'][-1]['truth'] is True:
            result['delete397_witness']=verify_dual.decode_native((args.work/(name+'.log')).read_text(),H,raw,meta)
            save()
    cnf,_=controls['record509'];proof=args.work/'record509.drat'
    row=call('record509_kissat',[str(args.kissat.resolve()),f'--time={args.proof_seconds}',str(cnf.resolve()),str(proof.resolve())],args.proof_seconds+5)
    enc.require(row['returncode']!=10,'known509 control contradicted by SAT solver')
    row.update(cnf_sha256=sha256(cnf.read_bytes()).hexdigest(),proof_bytes=proof.stat().st_size,
               proof_sha256=sha256(proof.read_bytes()).hexdigest())
    result['record509_proof']=row;save()
    if row['returncode']==20:
        checked=call('record509_drat_check',[str(args.drat_trim.resolve()),str(cnf.resolve()),str(proof.resolve())],3600)
        log=(args.work/'record509_drat_check.log').read_text()
        checked['verified']=checked['returncode']==0 and 's VERIFIED' in log
        enc.require(checked['verified'],'DRAT proof rejected')
        result['record509_proof']['checker']=checked
    result['status']='bounded controls completed; full family unstarted';save()
    print(json.dumps(dict(status=result['status'],proof_returncode=row['returncode'],proof_bytes=row['proof_bytes'],
        proof_verified=row.get('checker',{}).get('verified',False),total_seconds=result['total_seconds'])),flush=True)


if __name__=='__main__':
    main()
