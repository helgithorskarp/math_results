"""PRIVATE exact rational Gaussian pivots, preserving denominator factors.

The raw Bareiss product hits512 terms. This algorithm cancels exact factors
before expansion; it retains the same512-term and32MiB packing bounds.
"""
import os
for v in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[v]='1'
from pathlib import Path
import sys,json,signal,time,resource,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from bivariate import P,R,ATOMS,PROBES,DEN_CACHE,atom
from clearing import shift,encode
from sectors import sectors
from exact import require

def coded(z):
    z=R(z)
    return dict(numerator=encode(z.num),denominator_factors=[dict(factor=encode(ATOMS[k]),power=e) for k,e in sorted(z.den.items())])

def main():
    state=Path('/scratch/research-team-sol61-six-20260929/state')
    require(not any((state/n).exists() for n in ('PAUSED','PAUSED.json','HANDOVER','HANDOVER.json')),'operational barrier')
    def alarm(a,b):raise TimeoutError('unchanged60s Gaussian variable-q guard')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    ATOMS.clear();PROBES.clear();DEN_CACHE.clear();rows=[];forms={};updates=[];stage='initialize';status='INCOMPLETE';trace=None
    h=R(P({(1,0):1}));q=R(P({(0,1):1}))
    try:
        for z in (h,h-1,6*h+1,q+3*h,2*h-1,q,q-1,q-2):atom(R(z).num)
        p,g,s,c=sectors(q,h)
        catalogue=[(name,[[p[name]]]) for name in ('alpha','beta','mu')]
        catalogue += [(name,[[R(z)/g[name][i][i] for z in row] for i,row in enumerate(c[name])]) for name in ('anti','standard','fixed-even','fixed-odd','untouched-even','untouched-odd')]
        for group,matrix in catalogue:
            a=[[R(z) for z in row] for row in matrix];forms[group]=[[coded(z) for z in row] for row in a]
            for k in range(len(a)):
                stage='pivot '+group+' '+str(k+1);pivot=a[k][k];positive=shift(pivot.num).positive()
                require(all(shift(ATOMS[key]).positive() for key in pivot.den),'all pivot denominator factors coefficient-positive')
                rows.append(dict(group=group,order=k+1,pivot=coded(pivot),shifted_numerator=encode(shift(pivot.num)),positive=positive,degree=pivot.num.degree(),terms=len(pivot.num.a),shifted_terms=len(shift(pivot.num).a)))
                print(json.dumps({key:rows[-1][key] for key in ('group','order','positive','degree','terms','shifted_terms')}),flush=True)
                require(positive,'pivot coefficient positivity unproved')
                atom(pivot.num)
                for i in range(k+1,len(a)):
                    for j in range(k+1,len(a)):
                        stage='Schur '+group+' '+str((k,i,j))
                        before=a[i][j];x=a[i][k];y=a[k][j];after=before-(x/pivot)*y
                        require(pivot*(before-after)==x*y,'exact original field Schur update')
                        updates.append(dict(group=group,k=k,i=i,j=j,before=coded(before),left=coded(x),right=coded(y),pivot=coded(pivot),after=coded(after)))
                        a[i][j]=after
        require(len(rows)==20 and all(z['positive'] for z in rows),'complete20 exact Gaussian pivot signs')
        status='ALL20 RATIONAL GAUSSIAN PIVOTS COEFFICIENT-POSITIVE; independent reconstruction and uniform physical bridge outstanding'
    except (ValueError,TimeoutError) as e:
        status='STOPPED: '+str(e);trace=traceback.format_exc()
    finally:
        signal.alarm(0)
        result=dict(agent='six-downset-1',role='researcher',status=status,stage=stage,traceback=trace,domain='auxiliary h>=2,q>=4; physical integer h>=2,q=2^(n-1),n>=3',rows=rows,forms=forms,updates=updates,seconds=time.monotonic()-start,peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,optimized=sys.flags.optimize,guards=dict(child_seconds=60,polynomial_terms=512,packing_bytes=33554432,native_threads=1))
        (Path(__file__).resolve().parent/'work'/f'gaussian-O{sys.flags.optimize}.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:v for k,v in result.items() if k not in ('rows','forms','updates')}),flush=True)
if __name__=='__main__':main()
