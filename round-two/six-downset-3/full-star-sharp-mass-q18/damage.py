"""Serial semantic controls for the new sparse point/line/dual certificate."""
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
    a=deepcopy(seed);a['maximum_star_s']=52;yield 'wrong-original-star',a
    a=deepcopy(seed);a['free_original_entry_denominator']=49545216;yield 'wrong-common-endpoint-units',a
    a=deepcopy(seed);a['free_original_entry_orbit_keys'].pop();yield 'missing-original-free-orbit',a
    a=deepcopy(seed);a['free_original_entry_numerators'][0]+=1;yield 'changed-original-coefficient',a
    a=deepcopy(seed);a['positive_sector_certificates'].pop('ZW_upper');yield 'missing-nonfixed-upper-sector',a
    a=deepcopy(seed);a['positive_sector_certificates']['TT_upper']=deepcopy(a['positive_sector_certificates']['TT_lower']);yield 'wrong-endpoint-factor',a
    a=deepcopy(seed);a['positive_sector_certificates']['Z_lower']['factor_lower_triangle_numerators'][0][0]+=1;yield 'changed-standard-factor',a
    a=deepcopy(seed);a['positive_sector_certificates']['TT_lower']['whole_residual_denominator']=1<<64;yield 'incorrect-nondyadic-residual-clearing',a
    a=deepcopy(seed);a['claimed_tauMax_original_floor']='1/8';yield 'overstated-fresh-original-floor',a
    a=deepcopy(seed);a['positive_sector_certificates']['ZZ_upper']['scalar_gram_numerator']+=1;yield 'false-nonfixed-scalar',a
    a=deepcopy(seed);a['real_tau_interval']=['0','1/64'];yield 'unpaid-larger-real-interval',a
    a=deepcopy(seed);a['claimed_slope_Frobenius_squared']='1';yield 'false-whole-derivative-norm',a
    a=deepcopy(seed);a['claimed_uniform_original_floor']='1/16';yield 'overstated-uniform-original-floor',a
    a=deepcopy(seed);a['claimed_sharp_positive_NN_mass_intercept']='1';yield 'false-universal-dual-intercept',a
    a=deepcopy(seed);a['claimed_sharp_positive_NN_mass_slope']=40;yield 'missing-loop-in-dual-slope',a


def run(certificate):
    seed=json.loads(certificate.read_bytes());start=time.monotonic();env=os.environ.copy()
    for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS',
              'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):env[k]='1'
    receipts=[]
    with tempfile.TemporaryDirectory(prefix='q18-sharp-controls-') as td:
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
    return dict(actual_agent='six-downset-3',role='researcher',
                certificate_SHA256=hashlib.sha256(certificate.read_bytes()).hexdigest(),
                defects=15,normal_and_optimized_rejections=30,receipts=receipts,
                timeout_or_incomplete_is_not_rejection=True,native_threads=1,serial_children=1,
                child_guard_seconds=45,seconds=time.monotonic()-start)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    r=run(a.certificate);a.out.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='receipts'},sort_keys=True))


if __name__=='__main__':main()
