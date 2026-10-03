"""PRIVATE one exact h-point of fixed original row clearing, q-polynomial.

No variable h polynomial is expanded. Existing polynomial guard512,
integer packing32MiB and child60s remain unchanged.
"""
import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ[name]='1'
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
import sys,json,signal,time,resource
from bivariate import P
from bareiss import leading_polynomial_minors
from clearing import encode,shift
from exact import require

def evaluate_h(data,h):
    out={}
    for (a,b),c in data['terms']:
        key=(0,b);out[key]=out.get(key,0)+int(c)*h**a
    return P(out,data['denominator'])
def factor_key(p):return json.dumps(p,sort_keys=True,separators=(',',':'))

def main():
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--h',type=int,required=True);args=ap.parse_args();h=args.h
    require(3<=h<=133,'degree-bounded interpolation point scope')
    def alarm(signum,frame):raise TimeoutError('unchanged60s Newton point guard')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    source=Path('work/raw-bounds.json');raw=source.read_bytes();anchor=json.loads(raw);rows=[]
    bounds={(z['group'],z['order']):z for z in anchor['bounds']}
    for name,form in anchor['forms'].items():
        a=[]
        for row,domain in zip(form['raw'],form['positive_row_domains']):
            common={factor_key(z['factor']):(z['factor'],z['power']) for z in domain};entry=[]
            for z in row:
                num=evaluate_h(z['numerator'],h);den={factor_key(z['factor']):z['power'] for z in z['denominator_factors']}
                require(all(key in common for key in den),'EVERY raw denominator cleared')
                for key,(factor,power) in common.items():
                    exponent=power-den.get(key,0);require(exponent>=0,'complete positive row clearing')
                    num=num*evaluate_h(factor,h)**exponent
                entry.append(num)
            a.append(entry)
        determinants=leading_polynomial_minors(a)
        for k,det in enumerate(determinants,1):
            bound=bounds[(name,k)];require(all(ex[0]==0 and ex[1]<=bound['q_degree_bound'] for ex in det.a),'EVERY complete q degree bound')
            shifted=shift(det)
            rows.append(dict(group=name,order=k,original=encode(det),q4_shifted=encode(shifted),q_degree_bound=bound['q_degree_bound']))
    signal.alarm(0);out=dict(agent='six-downset-1',role='researcher',status='Exact point data only, not arbitrary-h positivity',h=h,raw_anchor_sha256=sha256(raw).hexdigest(),rows=rows)
    directory=Path('work/newton');directory.mkdir(parents=True,exist_ok=True)
    (directory/f'h{h}.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='rows'}|{'complete_point_rows':len(rows)}))
if __name__=='__main__':main()
