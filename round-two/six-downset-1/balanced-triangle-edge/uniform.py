"""PRIVATE exact QQ(h) signs at q2, under unchanged algebra guards."""
import os
for v in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[v]='1'
from pathlib import Path
import sys,json,signal,time,resource
sys.path.insert(0,str(Path(__file__).resolve().parent))
from fractions import Fraction as F
from bivariate import P,R,ATOMS,PROBES,DEN_CACHE,atom
from bareiss import leading_polynomial_minors
from clearing import shift,encode,clear_original
from sectors import sectors
from exact import require
def main():
 state=Path('/scratch/research-team-sol61-six-20260929/state')
 require(not any((state/n).exists() for n in ('PAUSED','PAUSED.json','HANDOVER','HANDOVER.json')),'operational pause/handover barrier')
 def alarm(a,b):raise TimeoutError('unchanged60s balanced uniform sign guard')
 signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
 ATOMS.clear();PROBES.clear();DEN_CACHE.clear();h=R(P({(1,0):1}))
 for z in (h,h-1,6*h+1,3*h+2,2*h-1):atom(R(z).num)
 p,g,s,c=sectors(h)
 catalogue=[(name,[[p[name]]]) for name in ('alpha','beta','mu')]+list(c.items())
 rows=[];forms={};status='INCOMPLETE'
 try:
  for group,matrix in catalogue:
   raw=[[R(z) for z in row] for row in matrix]
   cleared,domains,removed,constants=clear_original(raw)
   forms[group]=dict(raw_original=[[{'numerator':encode(z.num),'denominator_factors':[{'factor':encode(ATOMS[key]),'power':power} for key,power in z.den.items()]} for z in row] for row in raw],cleared=[[encode(z) for z in row] for row in cleared],domains=domains,removed=removed,constants=constants)
   for k,det in enumerate(leading_polynomial_minors(cleared),1):
    shifted=shift(det);positive=shifted.positive()
    require(all(e[1]==0 for e in det.a),'exact QQ[h] polynomial specialization')
    rows.append(dict(group=group,order=k,original=encode(det),shifted=encode(shifted),positive=positive,degree=det.degree(),original_terms=len(det.a),shifted_terms=len(shifted.a)))
    print(json.dumps(dict(stage='balanced exact leading minor',group=group,order=k,positive=positive,degree=det.degree())),flush=True)
  require(len(rows)==17 and all(r['positive'] for r in rows),'ALL3 residual and14 complete-sector cap signs strictly positive by h2+u coefficients')
  status='ALL17 ORIGINAL QQ(h) SIGNS GENERATED; separate reconstruction and uniform physical bridge outstanding'
 except (ValueError,TimeoutError) as e:status='STOPPED: '+str(e)
 finally:
  signal.alarm(0)
  result=dict(agent='six-downset-1',role='researcher',status=status,domain='n=2, real h>=2 for sign forms only; original balanced family requires integer h>=2',fixed_sector_dimensions=[4,4],rows=rows,forms=forms,seconds=time.monotonic()-start,peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,optimized=sys.flags.optimize,guards=dict(child_seconds=60,polynomial_terms=512,packing_bytes=33554432,native_threads=1))
  output=Path(__file__).resolve().parent/'work'/f'uniform-O{sys.flags.optimize}.json'
  output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('rows','forms')}),flush=True)
if __name__=='__main__':main()
