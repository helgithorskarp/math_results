"""PRIVATE complete balanced q4 certificate checker: different QQ[h]/Gaussian tools."""
import os
for v in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[v]='1'
from pathlib import Path
import sys,json,signal,time,resource
sys.path.insert(0,str(Path(__file__).resolve().parent))
from fractions import Fraction as F
from math import comb,prod
from hashlib import sha256
from independent import Rat,poly,pmul,pvalue,require,forms

def decode(p,positive=False):
    require(type(p['denominator']) is int and p['denominator']>0,'positive coefficient denominator')
    require(len(p['terms'])<=512,'unchanged512 terms');a={}
    for ex,c in p['terms']:
        require(type(ex) is list and len(ex)==2 and type(ex[0]) is int and ex[0]>=0 and type(ex[1]) is int and ex[1]==0,'strict univariate h exponent')
        v=int(c);require(str(v)==c and v and ex[0] not in a,'canonical unique nonzero coefficient');a[ex[0]]=F(v,p['denominator'])
    if positive:require(a.get(0,F(0))>0 and all(z>=0 for z in a.values()),'strict complete h2 shifted signs')
    return poly([a.get(i,F(0)) for i in range(max(a,default=-1)+1)])
def shifted(a):return poly([sum((a[j]*comb(j,i)*2**(j-i) for j in range(i,len(a))),F(0)) for i in range(len(a))])
def determinant(A):
    A=[[F(z) for z in row] for row in A];out=F(1)
    for j in range(len(A)):
        pivot=next((i for i in range(j,len(A)) if A[i][j]),None)
        if pivot is None:return F(0)
        if pivot!=j:A[pivot],A[j]=A[j],A[pivot];out=-out
        d=A[j][j];out*=d
        for i in range(j+1,len(A)):
            z=A[i][j]/d
            for k in range(j+1,len(A)):A[i][k]-=z*A[j][k]
    return out
def check(data):
    require(data['domain']=='n=3, q=4, real h>=2 for sign forms only; original balanced family requires integer h>=2' and data['fixed_sector_dimensions']==[5,4],'fixed q4 domain')
    names=['alpha','beta','mu']
    sizes={name:1 for name in names}|{'anti':2,'standard':4,'fixed-even':5,'fixed-odd':4}
    expected=[(name,k) for name,n in sizes.items() for k in range(1,n+1)]
    require([(r['group'],r['order']) for r in data['rows']]==expected,'complete18 obligations in order')
    require(list(data['forms'])==list(sizes),'complete64 original form entries')
    decoded={};coefficients=0
    for row in data['rows']:
        original,new=decode(row['original']),decode(row['shifted'],True)
        require(shifted(original)==new,'independent complete coefficient h2 composition')
        require(row['positive'] is True and row['degree']==len(original)-1 and row['original_terms']==sum(bool(z) for z in original) and row['shifted_terms']==sum(bool(z) for z in new),'entire exact sign metadata')
        decoded[(row['group'],row['order'])]=original;coefficients+=sum(bool(z) for z in new)
    h=Rat((0,1));live=forms(h);original_entries=0;clearing_entries=0;factor_occurrences=0;matrices={}
    allowed=[poly(a) for a in [(0,1),(-1,1),(1,6),(4,3),(-1,2)]]
    for name,n in sizes.items():
        record=data['forms'][name]
        require(len(record['raw_original'])==len(record['cleared'])==len(record['domains'])==len(record['removed'])==len(record['constants'])==n,'entire row catalogue dimensions')
        raw=record['raw_original'];A=[[decode(z) for z in row] for row in record['cleared']]
        require(all(len(row)==n for row in raw+A),'entire square form')
        for i in range(n):
            products=[]
            for group in [record['domains'][i],record['removed'][i]]:
                out=Rat(1)
                for z in group:
                    old,new=decode(z['original']),decode(z['shifted'],True)
                    require(old in allowed and shifted(old)==new,'every stated positive affine factor')
                    exponent=z['power'];require(type(exponent) is int and exponent>0,'positive factor exponent')
                    out*=Rat(old)**exponent;factor_occurrences+=1
                products.append(out)
            const=F(record['constants'][i]);require(const>0,'positive row normalization')
            for j in range(n):
                z=raw[i][j];numerator=decode(z['numerator']);den=Rat(1)
                for term in z['denominator_factors']:
                    factor=decode(term['factor']);power=term['power']
                    require(factor in allowed and type(power) is int and power>0,'only five exact positive original poles')
                    den*=Rat(factor)**power
                rational=Rat(numerator)/den
                require(rational==live[name][i][j],'EVERY separate original QQ[h] formula coefficient identity');original_entries+=1
                require(Rat(A[i][j])*products[1]==rational*products[0]*const,'EVERY independent original row-clearing coefficient identity');clearing_entries+=1
        matrices[name]=A
    require(original_entries==clearing_entries==64,'complete original matrices, no prefix')
    checks=[];nodes=0
    for name,n in sizes.items():
        for k in range(1,n+1):
            a=[row[:k] for row in matrices[name][:k]];d=decoded[(name,k)]
            bound=max(len(d)-1,sum(max((len(z)-1 for z in row),default=0) for row in a))
            require(bound<=512,'unchanged polynomial degree/term guard')
            for hvalue in range(2,3+bound):
                require(pvalue(d,hvalue)==determinant([[pvalue(z,hvalue) for z in row] for row in a]),'EVERY degree-complete independent Gaussian determinant identity');nodes+=1
            checks.append(dict(group=name,order=k,degree=len(d)-1,determinant_identity_bound=bound,nodes=bound+1))
    return dict(complete=True,original_field_coefficient_identities=original_entries,clearing_coefficient_identities=clearing_entries,positive_affine_factor_occurrences=factor_occurrences,whole_shift_coefficient_identities=18,strict_positive_coefficients=coefficients,full_Gaussian_determinant_nodes=nodes,checks=checks,trust='Independent same-author standard-library univariate rational/Gaussian computation. Geometric quotient and universal original-space bridges remain unformalized; no independent review.')

def main():
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('certificate');ap.add_argument('--output');args=ap.parse_args()
    state=Path('/scratch/research-team-sol61-six-20260929/state')
    require(not any((state/n).exists() for n in ('PAUSED','PAUSED.json','HANDOVER','HANDOVER.json')),'operational pause/handover barrier')
    def alarm(a,b):raise TimeoutError('unchanged60s balanced separate checker guard')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    raw=Path(args.certificate).read_bytes();result=check(json.loads(raw));signal.alarm(0)
    record=dict(agent='six-downset-1',role='researcher',status='PASS: complete separate q4 identities and signs',certificate_sha256=sha256(raw).hexdigest(),result=result,seconds=time.monotonic()-start,peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,optimized=sys.flags.optimize)
    output=Path(args.output or Path(__file__).resolve().parent/'work'/f'checked-O{sys.flags.optimize}.json')
    output.write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({k:v for k,v in record.items() if k!='result'}|{k:v for k,v in result.items() if k!='checks'}))
if __name__=='__main__':main()
