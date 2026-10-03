"""PRIVATE exact Newton-integer positivity, requiring complete degree grids.

The degree bounds are original-field polynomial bounds. This is not
positive finite sampling: every required forward difference is retained.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json,time,signal

def require(ok,msg):
    if not ok:raise ValueError(msg)
def coefficients(poly):
    require(type(poly['denominator']) is int and poly['denominator']>0,'positive coefficient denominator')
    require(len(poly['terms'])<=512,'unchanged512 coefficient guard');out={}
    for (a,b),value in poly['terms']:
        require(a==0 and type(b) is int and b>=0 and b not in out,'exact q-only exponent')
        c=int(value);require(str(c)==value and c,'canonical integer coefficient');out[b]=F(c,poly['denominator'])
    return out

def main():
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--output');args=ap.parse_args()
    def alarm(signum,frame):raise TimeoutError('unchanged60s Newton coefficient guard')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    raw=Path('work/raw-bounds.json').read_bytes();anchor=json.loads(raw);digest=sha256(raw).hexdigest()
    points={};point_hashes={};rows=[];positive=True;negative=[];total=0
    for h in range(3,3+anchor['maximum_h_grid_size']):
        path=Path(f'work/newton/h{h}.json');data=path.read_bytes();d=json.loads(data)
        require(d['h']==h and d['raw_anchor_sha256']==digest,'EVERY point original anchor binding')
        require([(r['group'],r['order']) for r in d['rows']]==[(r['group'],r['order']) for r in anchor['bounds']],'ENTIRE point row catalogue')
        points[h]={(r['group'],r['order']):coefficients(r['q4_shifted']) for r in d['rows']};point_hashes[str(h)]=sha256(data).hexdigest()
    for bound in anchor['bounds']:
        key=(bound['group'],bound['order']);dh,dq=bound['h_degree_bound'],bound['q_degree_bound'];require(dh+1<=512,'unchanged per-column coefficient guard')
        columns=[];count=0
        for e in range(dq+1):
            values=[points[3+j][key].get(e,F(0)) for j in range(dh+1)];diff=[]
            while values:
                diff.append(values[0]);values=[b-a for a,b in zip(values,values[1:])]
            for m,c in enumerate(diff):
                if c<0:
                    positive=False;negative.append(dict(group=key[0],order=key[1],q_power=e,Newton_order=m,coefficient=str(c)))
            count+=sum(bool(c) for c in diff);columns.append([str(c) for c in diff])
        constant=F(columns[0][0]);require(constant>0,'actual h3/q4 positive constant')
        rows.append(dict(**bound,Newton_coefficients_by_q_power=columns,all_coefficients_nonnegative=all(F(c)>=0 for col in columns for c in col),strict_constant=str(constant),nonzero_coefficients=count))
        total+=count
        print(json.dumps(dict(group=key[0],order=key[1],nonnegative=rows[-1]['all_coefficients_nonnegative'],h_degree_bound=dh,q_degree_bound=dq,nonzero_coefficients=count)),flush=True)
    signal.alarm(0)
    status='ALL24 Newton signs generated for integer h>=3 and real q>=4; separate point/checker proof outstanding' if positive else 'Newton coefficient positivity FAILS; no arbitrary-h verdict'
    out=dict(agent='six-downset-1',role='researcher',status=status,raw_anchor_sha256=digest,point_hashes=point_hashes,domain='integer h>=3, real q>=4',basis='binom(h-3,m)*(q-4)^e',rows=rows,all_coefficients_nonnegative=positive,negative_coefficients=negative,nonzero_coefficients=total,independent_point_check_complete=False,arbitrary_h_final_theorem=False)
    Path(args.output or 'work/newton-coefficients.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('rows','point_hashes','negative_coefficients')}|{'negative_coefficient_count':len(negative)}))
if __name__=='__main__':main()
