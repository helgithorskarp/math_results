"""PRIVATE full original q2 controls; no uniform theorem inferred."""
import os
for v in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[v]='1'
from pathlib import Path
import sys,json,signal,time,resource
sys.path.insert(0,str(Path(__file__).resolve().parent))
from fractions import Fraction as F
from model import actual
from sectors import literal_blocks,boundary_sectors
from exact import require
def main():
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--h',type=int,required=True);args=ap.parse_args()
 def alarm(a,b):raise TimeoutError('unchanged60s q2 original control guard')
 state=Path('/scratch/research-team-sol61-six-20260929/state')
 require(not any((state/n).exists() for n in ('PAUSED','PAUSED.json','HANDOVER','HANDOVER.json')),'operational pause/handover barrier')
 signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
 p,_,_,_=boundary_sectors(F(args.h))
 six={k:str(p[k]) for k in ('alphaH','betaH','alphaL','betaL','nu','muL')}
 require(all(p[k]>0 for k in six),'six exact positive q2 residual scalars')
 sector=literal_blocks(args.h,F(2))
 require(sector['all_reduced_sectors_PD'],'complete q2 representative cap PD')
 result=dict(agent='six-downset-1',role='researcher',scope='PRIVATE literal original q2 control only; uniform h is unproved',residual_scalars=six,sectors=sector,original=actual(args.h,2))
 signal.alarm(0);result.update(seconds=time.monotonic()-start,peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,optimized=sys.flags.optimize)
 out=Path(__file__).resolve().parent/'work'/f'control-h{args.h}-O{sys.flags.optimize}.json'
 out.write_text(json.dumps(result,indent=2,default=str)+'\n');print(json.dumps(result,default=str))
if __name__=='__main__':main()
