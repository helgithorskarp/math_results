"""PRIVATE semantic rejection of altered complete variable-q certificates.

Timeout, interruption or a killed process is never counted as rejection.
"""
import os
for v in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[v]='1'
from pathlib import Path
import sys,json,signal,time,resource,argparse,io
sys.path.insert(0,str(Path(__file__).resolve().parent))
from copy import deepcopy
from contextlib import redirect_stdout
from hashlib import sha256
from check_gaussian import check,require

def main():
    ap=argparse.ArgumentParser();ap.add_argument('certificate');args=ap.parse_args()
    state=Path('/scratch/research-team-sol61-six-20260929/state')
    require(not any((state/n).exists() for n in ('PAUSED','PAUSED.json','HANDOVER','HANDOVER.json')),'operational barrier')
    def alarm(a,b):raise TimeoutError('unchanged60s semantic variable-q rejection guard')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    raw=Path(args.certificate).read_bytes();source=json.loads(raw);cases=[]
    names=['wrong_physical_domain','missing_pivot','missing_untouched_old_sector','wrong_shift_coefficient','wrong_original_form_coefficient','wrong_Gaussian_after_coefficient','wrong_Gaussian_source_link','negative_denominator_domain']
    for name in names:
        data=deepcopy(source)
        if name=='wrong_physical_domain':data['domain']=data['domain'].replace('n>=3','n>=2')
        elif name=='missing_pivot':data['rows'].pop()
        elif name=='missing_untouched_old_sector':data['forms'].pop('untouched-odd')
        elif name=='wrong_shift_coefficient':
            term=data['rows'][0]['shifted_numerator']['terms'][0];term[1]=str(int(term[1])+1)
        elif name=='wrong_original_form_coefficient':
            term=data['forms']['standard'][0][0]['numerator']['terms'][0];term[1]=str(int(term[1])+1)
        elif name in ('wrong_Gaussian_after_coefficient','wrong_Gaussian_source_link'):
            record=next(z for z in data['updates'] if z['group']=='standard')
            key='after' if name=='wrong_Gaussian_after_coefficient' else 'left'
            term=record[key]['numerator']['terms'][0];term[1]=str(int(term[1])+1)
        elif name=='negative_denominator_domain':
            term=data['forms']['alpha'][0][0]['denominator_factors'][0]
            term['factor']={'denominator':1,'terms':[[[0,0],'-99'],[[1,0],'1']]}
        rejected=False;reason=None
        try:
            with redirect_stdout(io.StringIO()):check(data)
        except (ValueError,KeyError) as exc:rejected=True;reason=str(exc)
        require(rejected,'altered semantic certificate falsely accepted: '+name)
        cases.append(dict(case=name,rejected=True,reason=reason))
    signal.alarm(0)
    out=dict(agent='six-downset-1',role='researcher',complete=True,certificate_sha256=sha256(raw).hexdigest(),cases=cases,seconds=time.monotonic()-start,peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,optimized=sys.flags.optimize)
    (Path(__file__).resolve().parent/'work'/f'damages-O{sys.flags.optimize}.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out),flush=True)
if __name__=='__main__':main()
