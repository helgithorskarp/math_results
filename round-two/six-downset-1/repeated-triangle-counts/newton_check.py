"""PRIVATE separate proof of degree bounds and complete Newton reconstruction.

Standard-library integer/Fraction arithmetic only. No producer polynomial
engine, physical model, factorization/GCD arithmetic or CAS is imported.
"""
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
from math import comb
from functools import lru_cache
import json,signal,time,resource
from point_check import decode,value,require,key

def maximum_degree(matrix):
    n=len(matrix)
    @lru_cache(None)
    def visit(mask):
        i=mask.bit_count()
        if i==n:return 0
        possible=[matrix[i][j]+visit(mask|(1<<j)) for j in range(n) if not (mask>>j)&1 and matrix[i][j]>=0]
        return max(possible,default=-100000)
    result=visit(0);require(result>=0,'nonzero determinant degree permutation');return result

def check(certificate_path='work/newton-coefficients.json'):
    raw=Path('work/raw-bounds.json').read_bytes();anchor=json.loads(raw);digest=sha256(raw).hexdigest()
    cert_bytes=Path(certificate_path).read_bytes();cert=json.loads(cert_bytes)
    require(cert['raw_anchor_sha256']==digest and cert['domain']=='integer h>=3, real q>=4' and cert['basis']=='binom(h-3,m)*(q-4)^e','ENTIRE exact domain/basis/anchor')
    expected=[(r['group'],r['order']) for r in anchor['bounds']];require([(r['group'],r['order']) for r in cert['rows']]==expected,'ALL24 Newton obligations')
    computed={};domains=0
    for name,form in anchor['forms'].items():
        n=len(form['raw']);require(len(form['positive_row_domains'])==n and all(len(row)==n for row in form['raw']),'ENTIRE raw form shape')
        deg=[[],[]]
        for row,common in zip(form['raw'],form['positive_row_domains']):
            dc={}
            for item in common:
                factor=decode(item['factor']);power=item['power'];fk=key(item['factor'])
                require(type(power) is int and power>0 and fk not in dc,'canonical row domain')
                require(all(i+j<=1 for i,j in factor[0]),'EVERY original pole is affine')
                require(factor[0].get((1,0),0)>=0 and factor[0].get((0,1),0)>=0 and value(factor,2,4)>0,'strict positive original factor on entire h>=2/q>=4 domain')
                dc[fk]=(factor,power);domains+=1
            entries=[[],[]]
            for z in row:
                numerator=decode(z['numerator']);dd={}
                for item in z['denominator_factors']:
                    fk=key(item['factor']);power=item['power'];require(type(power) is int and power>0 and fk not in dd and fk in dc,'ENTIRE raw denominator included')
                    dd[fk]=power
                require(all(dd.get(fk,0)<=power for fk,(p,power) in dc.items()),'exact polynomial row clearing')
                for variable in range(2):
                    d=-1 if not numerator[0] else max(ex[variable] for ex in numerator[0])+sum((power-dd.get(fk,0))*max(ex[variable] for ex in p[0]) for fk,(p,power) in dc.items())
                    entries[variable].append(d)
            for variable in range(2):deg[variable].append(entries[variable])
        require(deg==form['cleared_entry_separate_degree_upper_bounds'],'EVERY independent original-entry separate degree bound')
        for k in range(1,n+1):
            computed[(name,k)]=[maximum_degree([row[:k] for row in a[:k]]) for a in deg]
    bounds={(r['group'],r['order']):r for r in anchor['bounds']}
    for name,k in expected:
        b=bounds[(name,k)];require(computed[(name,k)]==[b['h_degree_bound'],b['q_degree_bound']],'EVERY complete determinant degree bound')
    maxh=3+max(z[0] for z in computed.values());points={};point_records=[]
    for h in range(3,maxh+1):
        path=Path(f'work/newton/h{h}.json');data=path.read_bytes();point=json.loads(data)
        require(cert['point_hashes'][str(h)]==sha256(data).hexdigest() and point['raw_anchor_sha256']==digest and point['h']==h,'EVERY complete point hash/anchor')
        checked=json.loads(Path(f'work/newton/h{h}-checked.json').read_text())
        require(checked['point_sha256']==sha256(data).hexdigest() and checked['raw_anchor_sha256']==digest and checked['complete24_obligations'] is True,'EVERY independent raw point determinant receipt')
        require([(r['group'],r['order']) for r in point['rows']]==expected,'complete point catalogue')
        points[h]={(r['group'],r['order']):decode(r['q4_shifted'],1) for r in point['rows']};point_records.append(checked)
    total=0;identities=0;row_records=[]
    for row in cert['rows']:
        name,k=row['group'],row['order'];dh,dq=computed[(name,k)]
        require(row['h_degree_bound']==dh and row['q_degree_bound']==dq,'ENTIRE row scope/bounds')
        columns=row['Newton_coefficients_by_q_power'];require(len(columns)==dq+1,'EVERY q coefficient column')
        count=0
        for e,col in enumerate(columns):
            require(len(col)==dh+1 and len(col)<=512,'ENTIRE bounded Newton basis')
            a=[F(c) for c in col];require(all(str(c)==v for c,v in zip(a,col)) and all(c>=0 for c in a),'canonical nonnegative exact Newton coefficients')
            count+=sum(bool(c) for c in a)
            for u in range(dh+1):
                actual=points[3+u][(name,k)];coefficient=F(actual[0].get((0,e),0),actual[1])
                require(coefficient==sum(a[m]*comb(u,m) for m in range(u+1)),'EVERY degree-complete Newton reconstruction identity');identities+=1
        require(F(columns[0][0])>0 and str(F(columns[0][0]))==row['strict_constant'],'strict h3/q4 constant')
        require(count==row['nonzero_coefficients'] and row['all_coefficients_nonnegative'] is True,'ENTIRE coefficient count/sign metadata')
        total+=count;row_records.append(dict(group=name,order=k,h_degree_bound=dh,q_degree_bound=dq,nonnegative_coefficients=count,all_complete_grid_identities=True))
    require(total==cert['nonzero_coefficients'] and cert['all_coefficients_nonnegative'] is True and cert['negative_coefficients']==[],'ENTIRE certificate positivity')
    return dict(agent='six-downset-1',role='researcher',status='PASS: complete degree/point/Newton certificate for integer h>=3, real q>=4; physical/rank bridge ordinary unformalized',raw_anchor_sha256=digest,Newton_certificate_sha256=sha256(cert_bytes).hexdigest(),rows=row_records,nonnegative_coefficients=total,complete_Newton_identity_points=identities,independent_raw_points=len(point_records),full_determinant_identity_points=sum(z['full_determinant_identity_points'] for z in point_records),full_shift_identity_points=sum(z['full_shift_identity_points'] for z in point_records),positive_original_row_factor_occurrences=domains,formalization=False,external_person_review=False,source_published=False,graph_submitted=False)

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',default='work/newton-coefficients.json');args=ap.parse_args()
    def alarm(signum,frame):raise TimeoutError('unchanged60s independent Newton guard')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic();out=check(args.certificate);signal.alarm(0)
    out.update(optimized=not __debug__)
    name='optimized' if not __debug__ else 'normal';Path(f'work/newton-checked-{name}.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
