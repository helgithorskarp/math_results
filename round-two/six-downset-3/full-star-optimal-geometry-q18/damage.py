"""Bounded semantic controls of new geometry data; no parent PSD replay."""
from copy import deepcopy
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time

BASE=Path(__file__).resolve().parent


def variants(seed):
    d=deepcopy(seed);d['s']=52;yield 'wrong-original-star',d
    d=deepcopy(seed);d['real_tau_interval']=['0','1/64'];yield 'unpaid-larger-interval',d
    d=deepcopy(seed);d['eta']='1/1073741824';yield 'unpaid-larger-perturbation',d
    d=deepcopy(seed);d['free_original_perturbation_numerators'][0]+=1;yield 'changed-degree-balanced-physical-perturbation',d
    d=deepcopy(seed);d['bad_incidence_rank_witness_edges'][-1]=deepcopy(d['bad_incidence_rank_witness_edges'][0]);yield 'duplicate-original-incidence-column',d
    d=deepcopy(seed);d['claimed_affine_dimension']=20712;yield 'false-full-real-affine-dimension',d


def run(geometry):
    seed=json.loads(geometry.read_bytes());env=os.environ.copy();receipts=[];start=time.monotonic()
    for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS',
              'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):env[k]='1'
    with tempfile.TemporaryDirectory(prefix='q18-geometry-controls-') as td:
        td=Path(td)
        for name,data in variants(seed):
            p=td/(name+'.json');p.write_text(json.dumps(data)+'\n')
            for optimized in (False,True):
                cmd=[sys.executable,'-I','-B']+(['-O'] if optimized else [])
                cmd += [str(BASE/'check.py'),'--geometry',str(p),'--out',str(td/'rejected.json')]
                t=time.monotonic();r=subprocess.run(cmd,env=env,text=True,capture_output=True,timeout=45)
                if r.returncode==0 or 'ValueError:' not in r.stderr or any(x in r.stderr for x in ('ImportError','ModuleNotFoundError')):
                    raise ValueError('semantic control did not fail at mathematical validation: '+name)
                receipts.append(dict(defect=name,optimized=optimized,exit_code=r.returncode,
                    seconds=time.monotonic()-t,error=r.stderr.strip().splitlines()[-1]))
    return dict(actual_agent='six-downset-3',role='researcher',
        geometry_SHA256=hashlib.sha256(geometry.read_bytes()).hexdigest(),defects=6,
        normal_and_optimized_rejections=12,receipts=receipts,native_threads=1,serial_children=1,
        child_guard_seconds=45,timeout_or_incomplete_is_not_rejection=True,seconds=time.monotonic()-start)


def main():
    p=argparse.ArgumentParser();p.add_argument('--geometry',type=Path,default=BASE/'GEOMETRY.json')
    p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=run(a.geometry)
    a.out.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='receipts'},sort_keys=True))


if __name__=='__main__':main()
