"""PRIVATE semantic q2 certificate rejection, never treating timeout as rejection."""
import os
for v in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[v]='1'
from pathlib import Path
import sys,json,signal,time,resource
sys.path.insert(0,str(Path(__file__).resolve().parent))
from copy import deepcopy
from hashlib import sha256
from check_uniform import check,require

def main():
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('certificate');args=ap.parse_args()
    state=Path('/scratch/research-team-sol61-six-20260929/state')
    require(not any((state/n).exists() for n in ('PAUSED','PAUSED.json','HANDOVER','HANDOVER.json')),'operational pause/handover barrier')
    def alarm(a,b):raise TimeoutError('unchanged60s semantic q2 guard')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    raw=Path(args.certificate).read_bytes();source=json.loads(raw);cases=[]
    for name in ['wrong_original_domain','wrong_fixed_quotient','missing_minor','wrong_positive_shift_coefficient','wrong_original_rational_coefficient','wrong_positive_row_clearing','wrong_removed_factor_power','missing_physical_fixed_row']:
        d=deepcopy(source)
        if name=='wrong_original_domain':d['domain']=d['domain'].replace('q=2','q=4')
        elif name=='wrong_fixed_quotient':d['fixed_quotient']=10
        elif name=='missing_minor':d['rows'].pop()
        elif name=='wrong_positive_shift_coefficient':
            term=d['rows'][0]['shifted']['terms'][0];term[1]=str(int(term[1])+1)
        elif name=='wrong_original_rational_coefficient':
            term=d['forms']['alphaH']['raw_original'][0][0]['numerator']['terms'][0];term[1]=str(int(term[1])+1)
        elif name=='wrong_positive_row_clearing':
            term=d['forms']['alphaH']['cleared'][0][0]['terms'][0];term[1]=str(int(term[1])+1)
        elif name=='wrong_removed_factor_power':
            found=next(f for f in d['forms'].values() if any(f['removed']))
            row=next(row for row in found['removed'] if row);row[0]['power']+=1
        else:d['forms']['fixed']['raw_original'].pop()
        try:check(d)
        except ValueError as exc:cases.append(dict(name=name,rejected=True,reason=str(exc)))
        else:raise ValueError('semantic damage accepted: '+name)
    signal.alarm(0)
    result=dict(agent='six-downset-1',role='researcher',complete=True,cases=cases,certificate_sha256=sha256(raw).hexdigest(),seconds=time.monotonic()-start,peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,optimized=sys.flags.optimize)
    path=Path(__file__).resolve().parent/'work'/f'damages-O{sys.flags.optimize}.json'
    path.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
