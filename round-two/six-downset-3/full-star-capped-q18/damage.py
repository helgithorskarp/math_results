"""Serial semantic controls for the fresh finite certificate, both modes."""
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
    a=deepcopy(seed);a['q']=16;yield 'old-carrier-label',a
    a=deepcopy(seed);a['maximum_star_s']=52;yield 'old-star-size',a
    a=deepcopy(seed);a['free_original_entry_denominator']=1024;yield 'old-coefficient-units',a
    a=deepcopy(seed);a['free_original_entry_orbit_keys'].pop();yield 'missing-free-orbit',a
    a=deepcopy(seed);a['free_original_entry_numerators'][0]+=1;yield 'changed-original-coefficient',a
    a=deepcopy(seed);a['claimed_original_floor']='1';yield 'overstated-full-original-floor',a
    a=deepcopy(seed);a['positive_sector_certificates'].pop('ZW_upper');yield 'missing-nonfixed-upper',a
    a=deepcopy(seed);a['positive_sector_certificates']['TT_upper']=deepcopy(a['positive_sector_certificates']['TT_lower']);yield 'wrong-endpoint-factor',a
    a=deepcopy(seed);a['positive_sector_certificates']['Z_lower']['factor_lower_triangle_numerators'][0][0]+=1;yield 'changed-standard-factor',a
    a=deepcopy(seed);a['positive_sector_certificates']['TT_upper']['whole_residual_row_margin_numerators'][0]+=1;yield 'false-original-residual',a
    a=deepcopy(seed);a['positive_sector_certificates']['TT_lower']['factor_denominator']=1<<31;yield 'wrong-factor-units',a
    a=deepcopy(seed);a['positive_sector_certificates']['ZZ_upper']['scalar_gram_numerator']+=1;yield 'false-pair-sector',a


def run(certificate):
    seed=json.loads(certificate.read_bytes());start=time.monotonic()
    env=os.environ.copy()
    for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS',
              'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):env[k]='1'
    receipts=[]
    with tempfile.TemporaryDirectory(prefix='q18-controls-') as td:
        td=Path(td)
        for name,data in variants(seed):
            p=td/(name+'.json');p.write_text(json.dumps(data)+'\n')
            for optimized in (False,True):
                cmd=[sys.executable,'-I','-B']+(['-O'] if optimized else [])
                cmd += [str(BASE/'check.py'),'--certificate',str(p),'--out',str(td/'rejected.json')]
                t=time.monotonic();r=subprocess.run(cmd,env=env,text=True,capture_output=True,timeout=45)
                if r.returncode==0 or 'ValueError:' not in r.stderr or any(x in r.stderr for x in ('ImportError','ModuleNotFoundError')):
                    raise ValueError('semantic control did not exit by mathematical validation: '+name)
                receipts.append(dict(defect=name,optimized=optimized,exit_code=r.returncode,
                                     seconds=time.monotonic()-t,error=r.stderr.strip().splitlines()[-1]))
    return dict(actual_agent='six-downset-3',role='researcher',author_controls=True,
                certificate_SHA256=hashlib.sha256(certificate.read_bytes()).hexdigest(),
                defects=12,normal_and_optimized_rejections=24,receipts=receipts,
                timeout_or_incomplete_is_not_rejection=True,native_threads=1,serial_children=1,
                child_guard_seconds=45,seconds=time.monotonic()-start)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    r=run(a.certificate);a.out.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='receipts'},sort_keys=True))


if __name__=='__main__':main()
