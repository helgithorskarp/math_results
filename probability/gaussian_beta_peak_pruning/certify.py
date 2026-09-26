"""Exact rational peak certificates for a growing block of Gaussian beta signs.

Standard library, Python3.11+. Analytic premises are in PROOF.md.
A positive block is not a certificate of full Gaussian majorisation.
"""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path


def rational(x):
    if type(x) is int or isinstance(x,F):
        return F(x)
    if not isinstance(x,str):
        raise ValueError('only integers or integer/fraction strings are allowed')
    bits=x.split('/')
    if len(bits) not in (1,2) or any(not b.lstrip('+-').isdigit() for b in bits):
        raise ValueError('invalid rational syntax')
    return F(x)


def distance(x,y):
    return sum((a-b)**2 for a,b in zip(x,y))


def parse(case):
    if not isinstance(case,dict) or case.get('dimension')!=3:
        raise ValueError('dimension must be three')
    x=[[rational(v) for v in p] for p in case['x']]
    y=[[rational(v) for v in p] for p in case['y']]
    w=[rational(v) for v in case['weights']]
    s=rational(case['variance'])
    if not x or len(x)!=len(y) or len(x)!=len(w):
        raise ValueError('inconsistent nonempty arrays')
    if any(len(p)!=3 for p in x+y):
        raise ValueError('points must have three coordinates')
    if s<=0 or min(w)<0 or sum(w)!=1:
        raise ValueError('positive variance and probability weights required')
    # Zero-mass labels are irrelevant to the law and removed explicitly.
    keep=[i for i,a in enumerate(w) if a>0]
    x,y,w=([v[i] for i in keep] for v in (x,y,w))
    for i in range(len(w)):
        for j in range(i):
            if distance(y[i],y[j])>distance(x[i],x[j]):
                raise ValueError('positive-mass labelled map is not a contraction')
    return x,y,w,s


def common_peak(case):
    x,y,w,s=parse(case)
    loss=F(0)
    for i in range(len(w)):
        for j in range(i):
            d=distance(y[i],y[j])
            loss+=2*w[i]*w[j]*d/(4*s+d)
    pair=1-loss/2
    groups={}
    for p,a in zip(y,w):
        key=tuple(p);groups[key]=groups.get(key,F(0))+a
    rho=max(groups.values())
    if len(groups)==1:
        sep=F(1);dmin=None
    else:
        pts=list(groups)
        dmin=min(distance(pts[i],pts[j]) for i in range(len(pts)) for j in range(i))
        sep=(8*s+rho*dmin)/(8*s+dmin)
    bound=min(pair,sep)
    if not 0<bound<=1:
        raise ArithmeticError('invalid peak bound')
    return {'positive_labels':len(w),'distinct_target_centers':len(groups),
            'variance':str(s),'largest_target_cluster_mass':str(rho),
            'minimum_distinct_target_squared_distance':None if dmin is None else str(dmin),
            'pair_peak_bound':str(pair),'separation_peak_bound':str(sep),
            'common_normalized_peak_upper_bound':str(bound)}


def pressure_block(N,M):
    if type(N) is not int or N<0:
        raise ValueError('row must be a nonnegative integer')
    M=rational(M)
    if not 0<M<=1:
        raise ValueError('certified normalized peak must be in (0,1]')
    # q=N-j, and q <= (1-M)(N+2). Never expand a moment stream.
    a=(1-M)*(N+2)
    qmax=min(N,a.numerator//a.denominator)
    return {'N':N,'maximum_q':qmax,'first_j':N-qmax,'last_j':N,
            'signed_entries':qmax+1,'unresolved_by_this_rule':N-qmax,
            'criterion':'N-j <= (1-M)*(N+2)'}


def certificate(case,rows):
    peak=common_peak(case)
    if not rows:
        raise ValueError('at least one row required')
    return {'status':'EXACT_PRESSURE_BETA_BLOCK_CERTIFICATE',
            'scope':'Only the listed pressure blocks; not full majorisation.',
            'peak':peak,'rows':[pressure_block(N,peak['common_normalized_peak_upper_bound']) for N in rows]}


def verify_certificate(case,claim):
    if not isinstance(claim,dict) or not isinstance(claim.get('rows'),list):
        raise ValueError('malformed certificate')
    rows=[r['N'] for r in claim['rows']]
    expected=certificate(case,rows)
    if claim!=expected:
        raise ValueError('certificate mismatch')
    return True


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input',type=Path)
    p.add_argument('--rows',nargs='+',type=int,default=[7])
    p.add_argument('--verify',type=Path)
    args=p.parse_args()
    try:
        case=json.loads(args.input.read_text())
        if args.verify:
            verify_certificate(case,json.loads(args.verify.read_text()))
            out={'status':'EXACT_PRESSURE_BETA_BLOCK_CERTIFICATE_VERIFIED'}
        else:
            out=certificate(case,args.rows)
    except (ValueError,TypeError,KeyError,ZeroDivisionError) as e:
        p.error(str(e))
    print(json.dumps(out,sort_keys=True,indent=2))

if __name__=='__main__':
    main()
