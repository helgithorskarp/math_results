"""PRIVATE separate integer/Fraction check of one complete raw h-point.

Imports no research producer, polynomial engine, physical model or CAS.
Every degree-bounded Gaussian determinant and q-shift identity is checked.
The ordinary raw-to-physical formula bridge remains written mathematics.
"""
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
from math import prod
import json,signal,time,resource

def require(ok,msg):
    if not ok:raise ValueError(msg)
def decode(p,dim=2):
    require(type(p['denominator']) is int and p['denominator']>0,'positive coefficient denominator')
    require(len(p['terms'])<=512,'unchanged512 polynomial coefficient guard');out={}
    for ex,c in p['terms']:
        require(type(ex) is list and len(ex)==2 and all(type(i) is int and i>=0 for i in ex),'exact exponent tuple')
        if dim==1:require(ex[0]==0,'univariate q exponent')
        co=int(c);require(str(co)==c and co and tuple(ex) not in out,'canonical nonzero coefficient')
        out[tuple(ex)]=co
    return out,p['denominator']
def value(p,h,q):return F(sum(c*h**i*q**j for (i,j),c in p[0].items()),p[1])
def determinant(a):
    a=[[F(v) for v in row] for row in a];out=F(1)
    for j in range(len(a)):
        pivot=next((i for i in range(j,len(a)) if a[i][j]),None)
        if pivot is None:return F(0)
        if pivot!=j:a[j],a[pivot]=a[pivot],a[j];out=-out
        d=a[j][j];out*=d
        for i in range(j+1,len(a)):
            t=a[i][j]/d
            for k in range(j+1,len(a)):a[i][k]-=t*a[j][k]
    return out
def key(p):return json.dumps(p,sort_keys=True,separators=(',',':'))

def check(h):
    raw=Path('work/raw-bounds.json').read_bytes();anchor=json.loads(raw);digest=sha256(raw).hexdigest()
    path=Path(f'work/newton/h{h}.json');d=json.loads(path.read_text())
    require(d['h']==h and d['raw_anchor_sha256']==digest,'whole point original anchor binding')
    expected=[(r['group'],r['order']) for r in anchor['bounds']];require([(r['group'],r['order']) for r in d['rows']]==expected,'complete24 point obligations')
    bounds={(r['group'],r['order']):r for r in anchor['bounds']};points={(r['group'],r['order']):r for r in d['rows']}
    count=0;shift_count=0
    for name,form in anchor['forms'].items():
        parsed=[];domains=[]
        for row,dom in zip(form['raw'],form['positive_row_domains']):
            domains.append([(decode(z['factor']),z['power']) for z in dom])
            parsed.append([(decode(z['numerator']),[(decode(z['factor']),z['power']) for z in z['denominator_factors']]) for z in row])
        maximum=max(bounds[(name,k)]['q_degree_bound'] for k in range(1,len(parsed)+1))
        polys={}
        for k in range(1,len(parsed)+1):
            point=points[(name,k)];a,b=decode(point['original'],1),decode(point['q4_shifted'],1);bound=bounds[(name,k)]['q_degree_bound']
            require(point['q_degree_bound']==bound and all(j<=bound for i,j in a[0]) and all(j<=bound for i,j in b[0]),'complete q degree bound')
            polys[k]=(a,b)
        for q in range(4,5+maximum):
            domain_values=[prod(value(z,h,q)**e for z,e in fs) for fs in domains]
            require(all(x>0 for x in domain_values),'every original row domain positive at identity point')
            matrix=[[value(num,h,q)/prod(value(z,h,q)**e for z,e in den) for num,den in row] for row in parsed]
            for k in range(1,len(parsed)+1):
                bound=bounds[(name,k)]['q_degree_bound']
                if q>4+bound:continue
                a,b=polys[k];actual=determinant([row[:k] for row in matrix[:k]])*prod(domain_values[:k])
                require(actual==value(a,h,q),'EVERY complete raw-row determinant polynomial identity')
                require(value(a,h,q)==value(b,h,q-4),'EVERY complete q4-shift identity')
                count+=1;shift_count+=1
    return dict(agent='six-downset-1',role='researcher',h=h,raw_anchor_sha256=digest,point_sha256=sha256(path.read_bytes()).hexdigest(),complete24_obligations=True,full_determinant_identity_points=count,full_shift_identity_points=shift_count,status='PASS: independent integer/Fraction complete point identities')

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--h',type=int,required=True);args=ap.parse_args()
    def alarm(signum,frame):raise TimeoutError('unchanged60s independent point guard')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic();out=check(args.h);signal.alarm(0)
    out.update()
    Path(f'work/newton/h{args.h}-checked.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
