"""Bounded fresh logical proof proposal using the frozen integer packing.

One CPU job at a time, at most six eight-second/400-probe windows; no native
solver is used. Each dependency and each window is independently checked.
Incomplete fresh work has no exclusion meaning. The frozen replay is separate.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time
import check_probe
import check_transfer
import probe_units
import prune_probe
import prune_transfer

HERE=Path(__file__).absolute().parent


def encode(path,data):
    raw=(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode();path.write_bytes(raw)
    return hashlib.sha256(raw).hexdigest()


def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True)
    p.add_argument('--max-windows',type=int,choices=range(1,7),default=6);a=p.parse_args();a.work=a.work.absolute()
    if HERE.resolve()==a.work.resolve() or HERE.resolve() in a.work.resolve().parents:raise ValueError('Fresh outputs belong outside the source directory')
    if a.work.exists() and any(a.work.iterdir()):raise ValueError('Use an empty fresh output directory')
    a.work.mkdir(parents=True,exist_ok=True);started=time.monotonic();base=HERE/'base/phase611.json'
    prop=probe_units.Proposal(base.read_bytes(),[197,None]);known=prop.initial();x=3159
    if prop.colors[x]!=0 or known[x]>=0:raise ValueError('Fresh original0 premise point')
    trial=known.copy();trial[x]=1;unused,rows,term=prop.close(trial)
    if term is None:
        print(json.dumps({'status':'INCOMPLETE_PREMISE','no_exclusion_claimed':True}),flush=True);return
    shared={'format':'QR617_SCOPED_UNIT_TRACE_1','phase':611,'caps':[197,None],'root':-1,
            'base_certificate_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'next_cursor':0,'terminal':None,
            'steps':[{'kind':'failed_literal','point':x,'value':0,'trial':{'assumption':[x,1],'steps':rows,'terminal':term}}]}
    check_probe.check(base,shared);shared,pruning=prune_probe.prune(base,shared,targets={x})
    check_probe.check(base,shared);shared_path=a.work/'shared.json';shared_sha=encode(shared_path,shared)
    packing=json.loads((HERE/'certificates/packing.json').read_text());packing['shared_trace_sha256']=shared_sha
    packing_path=a.work/'packing.json';encode(packing_path,packing);ctx=check_transfer.Context(base,shared_path,packing_path)
    previous=None;windows=[];status='INCOMPLETE_BOUNDED_FRESH_PROPOSAL';proof_result=None
    env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
    for i in range(a.max_windows):
        outdir=a.work/f'window{i+1}'
        python=[str(Path(sys.executable).absolute())]+(['-O'] if sys.flags.optimize else [])
        command=python+[str(HERE/'propose_transfer.py'),'--base',str(base),'--shared',str(shared_path),
                 '--packing',str(packing_path),'--outdir',str(outdir)]
        if previous is not None:command+=['--resume',str(previous)]
        r=subprocess.run(command,check=True,capture_output=True,text=True,env=env);windows.append(json.loads(r.stdout))
        previous=outdir/'trace.json';trace=json.loads(previous.read_text());checked=ctx.check(trace)
        (outdir/'exact.json').write_text(json.dumps(checked,sort_keys=True,separators=(',',':'))+'\n')
        if not checked['excluded']:continue
        reduced,external=prune_transfer.prune(ctx,trace);proof_result=ctx.check(reduced)
        if not proof_result['excluded']:raise ValueError('Fresh pruning lost its contradiction')
        encode(a.work/'exclusion.json',reduced);status='VERIFIED_FRESH_PHASE611_197198_EXCLUSION';break
    summary={'agent':'six-vdw-3','role':'researcher','status':status,'phase':611,'caps':[197,198],
             'fresh_shared_rows':len(shared['steps']),'fresh_shared_fixed_positions':len(ctx.known),
             'fresh_shared_sha256':shared_sha,'windows':windows,'new_W_bound':False,'no_solver_trusted':True,
             'no_mathematical_exclusion_from_incomplete_work':True,'threads':1,'seconds':time.monotonic()-started,
             'parent_peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
             'child_peak_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
    if proof_result is not None:summary['exact']= {k:v for k,v in proof_result.items() if k!='known_candidate_values'}
    (a.work/'fresh-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary),flush=True)


if __name__=='__main__':main()
