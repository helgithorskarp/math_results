"""PRIVATE unchanged-guard sign exploration; incomplete output is no theorem."""
import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ[name]='1'
from fractions import Fraction as F
from pathlib import Path
import sys,signal,time,json,resource
from bivariate import P,R,ATOMS,PROBES,DEN_CACHE,atom,denominator,rational_value
from bareiss import leading_polynomial_minors
from clearing import shift,encode,clear_original
from sectors import sectors
from exact import require

def main():
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--fixed',action='store_true');ap.add_argument('--h',type=int);ap.add_argument('--output');args=ap.parse_args()
    def alarm(signum,frame):raise TimeoutError('unchanged60s general count sign guard')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    require(args.h is None or 2<=args.h<=10,'fixed heavy-count research bound')
    ATOMS.clear();PROBES.clear();DEN_CACHE.clear();h=R(P({(1,0):1})) if args.h is None else F(args.h);q=R(P({(0,1):1}))
    for z in [h,h-1,3*h+4,q,q-1,q+3*h-4,q+3*h-3,q+3*h]:
        z=R(z)
        if z.num.constant() is None:atom(z.num)
    p,G,S,cap=sectors(h,q)
    print(json.dumps(dict(stage='complete original rational sectors generated')),flush=True)
    catalogue=[(name,[[p[name]]]) for name in ['alphaH','betaH','alphaL','betaL','nu','muL']]
    catalogue+=list(cap.items()) if args.fixed else [(name,z) for name,z in cap.items() if name!='fixed']
    rows=[];forms={};status='INCOMPLETE'
    try:
        for group,matrix in catalogue:
            raw=[[R(z) for z in row] for row in matrix]
            cleared,domains,removed,constants=clear_original(raw)
            forms[group]=dict(raw_original=[[{'numerator':encode(z.num),'denominator_factors':[{'factor':encode(ATOMS[key]),'power':power} for key,power in z.den.items()]} for z in row] for row in raw],cleared=[[encode(z) for z in row] for row in cleared],domains=domains,removed=removed,constants=constants)
            dets=leading_polynomial_minors(cleared)
            for k,det in enumerate(dets,1):
                sdet=shift(det);positive=sdet.positive()
                rows.append(dict(group=group,order=k,original=encode(det),shifted=encode(sdet),positive=positive,total_degree=det.degree(),original_terms=len(det.a),shifted_terms=len(sdet.a)))
                print(json.dumps(dict(stage='leading sign',group=group,order=k,positive=positive,total_degree=det.degree(),original_terms=len(det.a),shifted_terms=len(sdet.a))),flush=True)
                require(positive,'NOT proved positive shifted coefficient signs '+group+'/'+str(k))
        status='ALL REQUESTED SIGNS GENERATED; separate checking and physical uniform bridge outstanding'
    except (ValueError,TimeoutError) as e:
        status='STOPPED: '+str(e)
    finally:
        signal.alarm(0)
        record=dict(agent='six-downset-1',role='researcher',status=status,complete_cap_requested=args.fixed,fixed_heavy_count=args.h,uniform_h_theorem=False,coefficient_domain='QQ(h,q), h=2+u,q=4+v,u/v>=0' if args.h is None else 'QQ(q), q=4+v,v>=0',rows=rows,forms=forms)
        name='all' if args.fixed else 'initial'
        suffix='' if args.h is None else '-h'+str(args.h)
        Path(args.output or 'work/uniform-'+name+suffix+'.json').write_text(json.dumps(record,indent=2)+'\n')
        print(json.dumps({k:v for k,v in record.items() if k not in ['rows','forms']}),flush=True)
if __name__=='__main__':main()
