#!/usr/bin/env python3
"""Exact certificate of an asymmetric angular obstruction to 208/9.

Pure standard-library rational arithmetic. Three checks of the squared
compression-weight sum: Newton residue trace, companion-matrix trace,
and an independent three-moment Gram inverse. No numerical roots.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import hashlib
import json
import sys


def require(value,message):
    if not value:raise ValueError(message)


def trim(p):
    p=list(p)
    while len(p)>1 and not p[-1]:p.pop()
    return p


def add(p,q):
    out=[Q(0)]*max(len(p),len(q))
    for i,c in enumerate(p):out[i]+=c
    for i,c in enumerate(q):out[i]+=c
    return trim(out)


def scale(p,c):return trim([x*c for x in p])


def mul(p,q):
    out=[Q(0)]*(len(p)+len(q)-1)
    for i,c in enumerate(p):
        for j,d in enumerate(q):out[i+j]+=c*d
    return trim(out)


def derivative(p):return trim([i*p[i] for i in range(1,len(p))] or [Q(0)])


def div(p,q):
    p,q=trim(p),trim(q);require(q!=[0],'zero denominator')
    out=[Q(0)]*max(1,len(p)-len(q)+1)
    while p!=[0] and len(p)>=len(q):
        k,c=len(p)-len(q),p[-1]/q[-1]
        out[k]+=c;p=add(p,scale([Q(0)]*k+q,-c))
    return trim(out),p


def remainder(p,h):return div(p,h)[1]


def inverse(p,h):
    a,b=h,remainder(p,h);u,v=[Q(0)],[Q(1)]
    while b!=[0]:
        quotient,nextb=div(a,b)
        a,b=b,nextb;u,v=v,add(u,scale(mul(quotient,v),-1))
    require(len(a)==1 and a[0]!=0,'noninvertible polynomial')
    out=remainder(scale(u,1/a[0]),h)
    require(remainder(mul(out,p),h)==[Q(1)],'Bezout certificate failed')
    return out


def evaluate(p,x):
    out=Q(0)
    for c in reversed(p):out=out*x+c
    return out


def newton(h,n):
    m=len(h)-1;require(h[-1]==1,'nonmonic Newton polynomial')
    values=[Q(m)]
    for k in range(1,n+1):
        if k<=m:value=-k*h[m-k]-sum(h[m-j]*values[k-j] for j in range(1,k))
        else:value=-sum(h[m-j]*values[k-j] for j in range(1,m+1))
        values.append(value)
    return values


def tracepoly(q,h):return sum(c*s for c,s in zip(q,newton(h,len(q)-1)))


def matmul(a,b):
    n=len(a)
    return [[sum(a[i][k]*b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def companion_trace(q,h):
    n=len(h)-1;C=[[Q(0)]*n for _ in range(n)]
    for j in range(n-1):C[j+1][j]=Q(1)
    for i in range(n):C[i][n-1]=-h[i]
    power=[[Q(int(i==j)) for j in range(n)] for i in range(n)]
    out=[[Q(0)]*n for _ in range(n)]
    for k,c in enumerate(q):
        for i in range(n):
            for j in range(n):out[i][j]+=c*power[i][j]
        if k+1<len(q):power=matmul(power,C)
    return sum(out[i][j]*out[j][i] for i in range(n) for j in range(n))


def gram_inverse_value(G,mu):
    """Exact elimination using only the three spectral moments, no residues."""
    n=len(mu);a=[list(row)+[mu[i]] for i,row in enumerate(G)]
    for k in range(n):
        pivot=next((i for i in range(k,n) if a[i][k]),None)
        require(pivot is not None,'singular Gram matrix')
        a[k],a[pivot]=a[pivot],a[k]
        a[k]=[x/a[k][k] for x in a[k]]
        for i in range(n):
            if i!=k:
                factor=a[i][k];a[i]=[a[i][j]-factor*a[k][j] for j in range(n+1)]
    return sum(mu[i]*a[i][-1] for i in range(n))


# Pairs denote a+b sqrt(3), with the positive real embedding fixed in PROOF.md.
def qa(p,q):return p[0]+q[0],p[1]+q[1]
def qm(p,q):return p[0]*q[0]+3*p[1]*q[1],p[0]*q[1]+p[1]*q[0]
def qpower(p,n):
    out=(Q(1),Q(0))
    for _ in range(n):out=qm(out,p)
    return out


def encode(value):
    if isinstance(value,dict):return {k:encode(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [encode(v) for v in value]
    return str(value)


def verify():
    records={}
    def check(name,actual,expected):
        require(actual==expected,name+' failed');records[name]=encode(actual)
    roots=[(Q(1),Q(10))]*3+[(Q(1),-Q(10))]*3+[(Q(7),Q(0)),(-Q(13),Q(0))]
    moments=[]
    for k in [1,2,3,4]:
        total=(Q(0),Q(0))
        for root in roots:total=qa(total,qpower(root,k))
        moments.append(total)
    check('exact_root_moments',moments,[(Q(0),Q(0)),(Q(2024),Q(0)),(Q(3552),Q(0)),(Q(581768),Q(0))])
    require(Q(17,10)**2<3<Q(7,4)**2,'real root separation failed')
    check('root_separation_squared_bracket',[Q(17,10)**2,Q(7,4)**2],[Q(289,100),Q(49,16)])
    A=[-Q(299),-Q(2),Q(1)];B=[-Q(91),Q(6),Q(1)]
    f=mul(mul(mul(A,A),A),B);h=[-Q(156),-Q(149),Q(4),Q(1)]
    check('expanded_real_root_polynomial',f,list(map(Q,[2432511809,-111572448,-54029300,725504,366630,-1184,-1012,0,1])))
    check('compression_polynomial_factorization',scale(derivative(f),Q(1,8)),mul(mul(A,A),h))
    check('inner_root_compression_values',[evaluate(h,Q(7)),evaluate(h,-Q(13))],[-Q(660),Q(260)])
    den=Q(1220287)
    q=remainder(scale(mul(mul(A,B),inverse(derivative(h),h)),-8),h)
    check('derived_active_residue_polynomial',q,[Q(1807004888)/den,-Q(4876192)/den,-Q(9460696)/den])
    check('residue_congruence',remainder(add(mul(q,derivative(h)),scale(mul(A,B),8)),h),[Q(0)])
    ps=newton(h,4)
    check('active_root_power_sums',ps,list(map(Q,[3,-4,314,-1384,51698])))
    N=Q(2024);S3=Q(3552);S4=Q(581768);mu2=S4-N*N/8
    check('independent_spectral_moment_vector',[N,S3,mu2],[Q(2024),Q(3552),Q(69696)])
    check('residue_spectral_moments',[tracepoly(q,h),tracepoly(mul(q,[Q(0),Q(1)]),h),tracepoly(mul(q,[Q(0),Q(0),Q(1)]),h)],[N,S3,mu2])
    G=[[ps[i+j] for j in range(3)] for i in range(3)]
    check('spectral_Gram_matrix',G,[[Q(3),-Q(4),Q(314)],[-Q(4),Q(314),-Q(1384)],[Q(314),-Q(1384),Q(51698)]])
    determinant=G[0][0]*(G[1][1]*G[2][2]-G[1][2]*G[2][1])-G[0][1]*(G[1][0]*G[2][2]-G[1][2]*G[2][0])+G[0][2]*(G[1][0]*G[2][1]-G[1][1]*G[2][0])
    check('Gram_discriminant',determinant,Q(14643444))
    eta_u=tracepoly(mul(q,q),h)
    check('Newton_residue_squared_trace',eta_u,Q(2980684990912,1220287))
    check('companion_matrix_squared_trace',companion_trace(q,h),eta_u)
    check('independent_three_moment_Gram_inverse',gram_inverse_value(G,[N,S3,mu2]),eta_u)
    X=S4/(N*N);eta=eta_u/(N*N)
    check('normalized_fourth_moment',X,Q(601,4232))
    check('normalized_collision_weight_sum',eta,Q(46573202983,78109350583))
    check('fourth_moment_excess',X-Q(1,8),Q(9,529))
    Phi=9*eta_u+208*S4-35*N*N
    check('negative_universal_extension_certificate',Phi,-Q(474603485184,1220287))
    require(Phi<0,'counterexample sign lost')
    deficit=eta-1+Q(208,9)*(X-Q(1,8))
    check('normalized_208_9_deficit',deficit,-Q(823964384,78109350583))
    C=(1-eta)/(X-Q(1,8))
    check('necessary_universal_constant',C,Q(3504016400,147654727))
    check('constant_excess_over_restricted_value',C-Q(208,9),Q(823964384,1328892543))
    require(Q(208,9)<C<Q(144,5),'constant outside stated range')
    check('uniform_objective_gap_at_Rstar',-Q(208,9)*(X-Q(1,8))+1-eta,Q(823964384,78109350583))
    radius=[-Q(584718545),Q(8514352856),Q(5295721648)]
    check('radius_equation_coefficients',add(scale(list(map(Q,[-720,896,768])),C.denominator),scale(list(map(Q,[25,40,16])),C.numerator)),scale(radius,Q(32)))
    lo=Q(659677,10**7);hi=Q(659678,10**7)
    require(evaluate(radius,lo)<0<evaluate(radius,hi),'radius root bracket failed')
    check('radius_root_bracket',[lo,hi],[Q(659677,10**7),Q(329839,5*10**6)])
    # Explicit eight-distinct-slopes witness: centers1/2,1,3/2 around
    # +/-10sqrt3, then7,-13. Its norm is exactly45.
    fd=[Q(1)];distinct_roots=[]
    for center in [Q(1,2),Q(1),Q(3,2)]:
        fd=mul(fd,[center*center-300,-2*center,Q(1)])
        distinct_roots += [(center,Q(10)),(center,-Q(10))]
    fd=mul(fd,B);distinct_roots += [(Q(7),Q(0)),(-Q(13),Q(0))]
    check('distinct_root_polynomial',fd,[Q(38854696881,16),-Q(445210935,4),-Q(431872325,8),Q(2901225,4),Q(5866953,16),-Q(1185),-Q(2025,2),Q(0),Q(1)])
    md=[]
    for k in [1,2,4]:
        total=(Q(0),Q(0))
        for root in distinct_roots:total=qa(total,qpower(root,k))
        md.append(total)
    check('distinct_root_moments',md,[(Q(0),Q(0)),(Q(2025),Q(0)),(Q(2334297,4),Q(0))])
    gd=scale(derivative(fd),Q(1,8))
    qd=remainder(scale(mul(fd,inverse(derivative(gd),gd)),-8),gd)
    check('distinct_residue_congruence',remainder(add(mul(qd,derivative(gd)),scale(fd,8)),gd),[Q(0)])
    eta_d=tracepoly(mul(qd,qd),gd)
    check('distinct_companion_Newton_trace_agreement',companion_trace(qd,gd),eta_d)
    check('distinct_residue_mass',tracepoly(qd,gd),Q(2025))
    phi_d=9*eta_d+208*Q(2334297,4)-35*Q(2025)**2
    check('distinct_negative_certificate',phi_d,-Q(1746288997284374824819986419052268279175827203851276237295,7980145913653001587422178012567716983879010063343874))
    require(phi_d<0,'distinct counterexample sign lost')
    return records


def damage_controls():
    h=list(map(Q,[-156,-149,4,1]));A=list(map(Q,[-299,-2,1]));B=list(map(Q,[-91,6,1]))
    q=[Q(1807004888,1220287),-Q(4876192,1220287),-Q(9460696,1220287)]
    tests=[lambda:inverse([Q(0)],h),lambda:div([Q(1)],[Q(0)]),
           lambda:require(remainder(add(mul(add(q,[Q(1)]),derivative(h)),scale(mul(A,B),8)),h)==[Q(0)],'damaged residue accepted'),
           lambda:require(Q(3504016400,147654727)<Q(208,9),'reversed comparison accepted')]
    rejected=0
    for test in tests:
        try:test()
        except ValueError:rejected+=1
    require(rejected==len(tests),'damage control did not reject')
    return rejected


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected',type=Path,default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--write-expected',action='store_true')
    args=parser.parse_args();records=verify()
    digest=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    if args.write_expected:args.expected.write_text(json.dumps(records,sort_keys=True,indent=2)+'\n')
    require(json.loads(args.expected.read_text())==records,'expected fixture differs')
    print(json.dumps({'status':'exact asymmetric counterexample verified','checks':len(records),'damage_controls':damage_controls(),'record_sha256':digest},sort_keys=True))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,json.JSONDecodeError) as error:
        print('verification failed: '+str(error),file=sys.stderr);raise SystemExit(1)
