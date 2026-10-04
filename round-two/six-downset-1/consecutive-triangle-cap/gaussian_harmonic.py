"""bounded exact coefficient-positivity attempt for new cap sectors.

Unchanged source2252 polynomial field engine; no interpolation inference.
A stopped computation is incomplete, never a negative mathematical theorem.
"""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[name]='1'
from pathlib import Path
from fractions import Fraction as F
from math import comb
import sys,json,signal,time,resource,traceback
from bivariate import P,R,ATOMS,PROBES,DEN_CACHE,atom
from sectors_harmonic import sectors
from exact import require


def encode(p):
    return dict(denominator=p.den,terms=[[list(e),str(c)] for e,c in sorted(p.a.items())])


def shift3(p):
    out={}
    for (a,b),c in p.a.items():
        for i in range(a+1):
            for j in range(b+1):
                ex=(i,j)
                out[ex]=out.get(ex,0)+c*comb(a,i)*3**(a-i)*comb(b,j)*4**(b-j)
    return P(out,p.den)


def coded(z):
    z=R(z)
    return dict(numerator=encode(z.num),denominator_factors=[
        dict(factor=encode(ATOMS[k]),power=e) for k,e in sorted(z.den.items())])


def main():
    def alarm(a,b):raise TimeoutError('unchanged60s symbolic child guard')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    ATOMS.clear();PROBES.clear();DEN_CACHE.clear()
    rows=[];forms={};updates=[];stage='initialize';status='INCOMPLETE';trace=None
    h=R(P({(1,0):1}));q=R(P({(0,1):1}))
    try:
        for z in (h,h-1,h-2,6*h-2,q+3*h,q,q-1,q-2):atom(R(z).num)
        stage='construct new sectors'
        p,g,s,c,_=sectors(q,h)
        catalogue=[]
        for label,group in zip(('x','y'),p['groups']):
            for name in ('alpha','beta','mu','nu'):
                catalogue.append((label+'-'+name,[[group[name]]]))
        catalogue.append(('tau',[[p['tau']]]))
        catalogue += [(name,[[R(z)/g[name][i][i] for z in row] for i,row in enumerate(c[name])])
                      for name in ('anti-x','anti-y','standard-x','standard-y','aggregate',
                                   'untouched-even','untouched-odd')]
        for group,matrix in catalogue:
            a=[[R(z) for z in row] for row in matrix]
            forms[group]=[[coded(z) for z in row] for row in a]
            for k in range(len(a)):
                stage='pivot '+group+' '+str(k+1)
                pivot=a[k][k]
                denominator_positive=all(shift3(ATOMS[key]).positive() for key in pivot.den)
                shifted=shift3(pivot.num)
                positive=shifted.positive()
                rows.append(dict(group=group,order=k+1,pivot=coded(pivot),
                    shifted_numerator=encode(shifted),positive=positive,
                    denominator_positive=denominator_positive,degree=pivot.num.degree(),
                    terms=len(pivot.num.a),shifted_terms=len(shifted.a)))
                print(json.dumps({key:rows[-1][key] for key in ('group','order','positive',
                    'denominator_positive','degree','terms','shifted_terms')}),flush=True)
                require(denominator_positive,'pivot denominator positivity unproved')
                require(positive,'pivot numerator coefficient positivity unproved')
                atom(pivot.num)
                for i in range(k+1,len(a)):
                    for j in range(k+1,len(a)):
                        stage='Schur '+group+' '+str((k,i,j))
                        before=a[i][j];xx=a[i][k];yy=a[k][j]
                        after=before-(xx/pivot)*yy
                        require(pivot*(before-after)==xx*yy,'EXACT field Schur identity')
                        updates.append(dict(group=group,k=k,i=i,j=j,before=coded(before),
                            left=coded(xx),right=coded(yy),pivot=coded(pivot),after=coded(after)))
                        a[i][j]=after
        require(len(rows)==33 and all(z['positive'] and z['denominator_positive'] for z in rows),
                'ALL33 complete new scalar/sector pivot signs')
        status='ALL33 EXACT PIVOTS POSITIVE; coefficient production only; original-coordinate bridge uses PROOF.md and separate reader'
    except (ValueError,TimeoutError) as e:
        status='INCOMPLETE: '+str(e);trace=traceback.format_exc()
    finally:
        signal.alarm(0)
        result=dict(agent='six-downset-1',role='researcher',status=status,stage=stage,
            traceback=trace,domain='Auxiliary real h>=3,q>=4; physical h integer,q=2^(n-1),n>=3',
            rows=rows,forms=forms,updates=updates,seconds=time.monotonic()-start,
            peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,optimized=sys.flags.optimize,
            guards=dict(child_seconds=60,polynomial_terms=512,packing_bytes=33554432,native_threads=1))
        packed=json.dumps(result,indent=2)+'\n'
        require(len(packed.encode())<=32*1024*1024,'unchanged32MiB certificate packing guard')
        path=Path.cwd()/'GAUSSIAN-HARMONIC-FIRST.json'
        path.write_text(packed)
        print(json.dumps({k:v for k,v in result.items() if k not in ('rows','forms','updates','traceback')}),flush=True)


if __name__=='__main__':main()
