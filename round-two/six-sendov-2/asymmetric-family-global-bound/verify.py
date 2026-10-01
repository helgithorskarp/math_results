#!/usr/bin/env python3
"""Exact asymmetric3+3+1+1 angular-family certificate kernel.

Basic Q-polynomial routines adapted with credit from the author's
angular-three-level-transition source6efce877eb9dcde6e12b6a90930d65382b29dd89.
New sparse moment/Gram identities and fraction-free Sylvester determinants.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys
from math import comb, gcd, lcm
from itertools import permutations
import time


def require(value, message):
    if not value:
        raise ValueError(message)


def trim(p):
    p=list(p)
    while len(p)>1 and not p[-1]:p.pop()
    return p


def pa(p,q):
    out=[Q(0)]*max(len(p),len(q))
    for i,c in enumerate(p):out[i]+=c
    for i,c in enumerate(q):out[i]+=c
    return trim(out)


def ps(p,c):return trim([x*c for x in p])


def pm(p,q):
    out=[Q(0)]*(len(p)+len(q)-1)
    for i,c in enumerate(p):
        for j,d in enumerate(q):out[i+j]+=c*d
    return trim(out)


def pd(p):return trim([i*p[i] for i in range(1,len(p))] or [Q(0)])


def pe(p,x):
    value=Q(0)
    for c in reversed(p):value=value*x+c
    return value


def pdiv(p,q):
    p,q=trim(list(map(Q,p))),trim(list(map(Q,q)))
    require(q!=[0],'zero polynomial denominator')
    quotient=[Q(0)]*max(1,len(p)-len(q)+1)
    while p!=[0] and len(p)>=len(q):
        k,c=len(p)-len(q),p[-1]/q[-1]
        quotient[k]+=c;p=pa(p,ps([Q(0)]*k+q,-c))
    return trim(quotient),p


def pgcd(p,q):
    while q!=[0]:p,q=q,pdiv(p,q)[1]
    return ps(p,1/p[-1])


class MP:
    """Sparse Q-polynomials in three indeterminates, no CAS dependency."""
    def __init__(self,value=0):
        if isinstance(value,MP):self.d=value.d;return
        if isinstance(value,dict):self.d={k:Q(v) for k,v in value.items() if v}
        else:self.d={(0,0,0):Q(value)} if value else {}
    @staticmethod
    def variable(i):
        k=[0,0,0];k[i]=1;return MP({tuple(k):1})
    def __add__(self,other):
        out=dict(self.d)
        for k,v in MP(other).d.items():out[k]=out.get(k,Q(0))+v
        return MP(out)
    __radd__=__add__
    def __neg__(self):return MP({k:-v for k,v in self.d.items()})
    def __sub__(self,other):return self+-MP(other)
    def __rsub__(self,other):return MP(other)+-self
    def __mul__(self,other):
        out={}
        for k,v in self.d.items():
            for l,w in MP(other).d.items():
                key=tuple(a+b for a,b in zip(k,l));out[key]=out.get(key,Q(0))+v*w
        return MP(out)
    __rmul__=__mul__
    def __truediv__(self,other):return self*(Q(1)/other)
    def __pow__(self,n):
        out=MP(1)
        for _ in range(n):out=out*self
        return out
    def __eq__(self,other):return self.d==MP(other).d
    def __bool__(self):return bool(self.d)
    def derivative(self,i):
        out={}
        for k,v in self.d.items():
            if k[i]:
                l=list(k);l[i]-=1;out[tuple(l)]=v*k[i]
        return MP(out)
    def square_variable(self):
        require(all(k[0]%2==0 for k in self.d),'odd center power')
        return MP({(k[0]//2,k[1],k[2]):v for k,v in self.d.items()})
    def third_to_one(self):
        out={}
        for k,v in self.d.items():
            key=(k[0],k[1],0);out[key]=out.get(key,Q(0))+v
        return MP(out)
    def primitive_integer(self):
        denominator=lcm(*(v.denominator for v in self.d.values()))
        ints={k:int(v*denominator) for k,v in self.d.items()}
        content=gcd(*ints.values())
        return MP({k:v//content for k,v in ints.items()})


def zpm(p,q):
    out=[MP(0)]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q):out[i+j]=out[i+j]+x*y
    return out
def zpow(p,n):
    out=[MP(1)]
    for _ in range(n):out=zpm(out,p)
    return out
def det3(G):
    out=MP(0)
    for p in permutations(range(3)):
        sign=(-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
        out+=sign*G[0][p[0]]*G[1][p[1]]*G[2][p[2]]
    return out


def family_moment_kernel():
    c,U,V=[MP.variable(i) for i in range(3)]
    moments=[]
    for k in [1,2,3,4]:
        outer=6*sum(comb(k,j)*c**(k-j)*U**(j//2) for j in range(0,k+1,2))
        inner=2*sum(comb(k,j)*(-3*c)**(k-j)*V**(j//2) for j in range(0,k+1,2))
        moments.append(outer+inner)
    N,S3,S4=moments[1:];mu2=S4-N*N/8
    A=[c*c-U,-2*c,MP(1)];B=[9*c*c-V,6*c,MP(1)]
    f=zpm(zpow(A,3),B);h=[-6*c**3+Q(3,4)*c*(V-U),c*c-(U+3*V)/4,4*c,MP(1)]
    g=[Q(i,8)*f[i] for i in range(1,9)]
    require(g==zpm(zpow(A,2),h),'all-parameter characteristic factorization failed')
    powers=[MP(3)]
    for k in range(1,5):
        if k<=3:val=-k*h[3-k]-sum(h[3-j]*powers[k-j] for j in range(1,k))
        else:val=-sum(h[3-j]*powers[k-j] for j in range(1,4))
        powers.append(val)
    G=[[powers[i+j] for j in range(3)] for i in range(3)];D=det3(G);mu=[N,S3,mu2];E=MP(0)
    for i in range(3):
        for j in range(3):
            rows=[a for a in range(3) if a!=j];cols=[a for a in range(3) if a!=i]
            minor=G[rows[0]][cols[0]]*G[rows[1]][cols[1]]-G[rows[0]][cols[1]]*G[rows[1]][cols[0]]
            E+=(-1)**(i+j)*mu[i]*minor*mu[j]
    return {'balance':moments[0],'N':N.square_variable(),'S4':S4.square_variable(),
            'mu2':mu2.square_variable(),'D':D.square_variable(),
            'ratio_numerator':(N*N*D-E).square_variable(),'ratio_denominator':(mu2*D).square_variable()}


# Separate integer-polynomial arithmetic for fraction-free determinants.
def ita(p):
    p=list(p)
    while len(p)>1 and p[-1]==0:p.pop()
    return p
def iad(p,q):
    out=[0]*max(len(p),len(q))
    for i,x in enumerate(p):out[i]+=x
    for i,x in enumerate(q):out[i]+=x
    return ita(out)
def isc(p,c):return ita([x*c for x in p])
def imu(p,q):
    out=[0]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        if x:
            for j,y in enumerate(q):
                if y:out[i+j]+=x*y
    return ita(out)
def idiv(p,q):
    p=ita(p);q=ita(q);require(q!=[0],'zero integer divisor');out=[0]*max(1,len(p)-len(q)+1)
    while p!=[0] and len(p)>=len(q):
        require(p[-1]%q[-1]==0,'nonintegral Bareiss polynomial quotient')
        k,c=len(p)-len(q),p[-1]//q[-1];out[k]+=c
        p=iad(p,isc([0]*k+q,-c))
    require(p==[0],'Bareiss polynomial division has remainder')
    return ita(out)
def ipow(p,n):
    out=[1]
    for _ in range(n):out=imu(out,p)
    return out
def bareiss(M):
    a=[[list(x) for x in row] for row in M];n=len(a);prev=[1];sign=1
    for k in range(n-1):
        pivot=next((i for i in range(k,n) if a[i][k]!=[0]),None)
        if pivot is None:return [0]
        if pivot!=k:a[k],a[pivot]=a[pivot],a[k];sign=-sign
        pk=a[k][k]
        for i in range(k+1,n):
            aik=a[i][k]
            for j in range(k+1,n):a[i][j]=idiv(iad(imu(pk,a[i][j]),isc(imu(aik,a[k][j]),-1)),prev)
            a[i][k]=[0]
        prev=pk
    return isc(a[-1][-1],sign)


def coefficients_in_U(p):
    degree=max(k[1] for k in p.d);out=[[0] for _ in range(degree+1)]
    for (i,j,k),v in p.d.items():
        require(k==0 and v.denominator==1,'noninteger chart coefficient')
        if len(out[j])<=i:out[j]+=[0]*(i+1-len(out[j]))
        out[j][i]+=int(v)
    return [ita(x) for x in out]
def sylvester_rows(p,q,j):
    m,n=len(p)-1,len(q)-1;width=m+n-j
    rows=[]
    for coefficients,shifts in [(p,n-j),(q,m-j)]:
        for shift in range(shifts-1,-1,-1):
            row=[[0]]*width
            for degree,entry in enumerate(coefficients):row[width-1-degree-shift]=entry
            rows.append(row)
    return rows


def sturm(p):
    def norm(a):return ps(a,1/abs(a[-1]))
    a,b=norm(trim(list(map(Q,p)))),norm(pd(list(map(Q,p))));out=[a,b]
    while True:
        r=ps(pdiv(a,b)[1],-1)
        if r==[0]:break
        r=norm(r);out.append(r);a,b=b,r
    return out
def variations(chain,x):
    signs=[]
    for p in chain:
        if x=='+inf':a=p[-1]
        else:a=pe(p,x)
        if a:signs.append(1 if a>0 else -1)
    return sum(a!=b for a,b in zip(signs,signs[1:]))
def count(chain,a,b):return variations(chain,a)-variations(chain,b)
def ivadd(a,b):return a[0]+b[0],a[1]+b[1]
def ivmul(a,b):
    v=[x*y for x in a for y in b];return min(v),max(v)
def ivpoly(p,x):
    out=(Q(0),Q(0))
    for c in reversed(p):out=ivadd(ivmul(out,x),(c,c))
    return out
def ivquot(n,d,x):
    a,b=ivpoly(n,x),ivpoly(d,x);require(b[0]>0 or b[1]<0,'lift interval denominator containszero')
    return ivmul(a,(1/b[1],1/b[0]))
def ivmp(p,boxes):
    powers=[]
    for box in boxes:
        values=[(Q(1),Q(1))]
        for _ in range(10):values.append(ivmul(values[-1],box))
        powers.append(values)
    out=(Q(0),Q(0))
    for exponents,c in p.d.items():
        term=(c,c)
        for i,k in enumerate(exponents):term=ivmul(term,powers[i][k])
        out=ivadd(out,term)
    return out


def encode(value):
    if isinstance(value,MP):return [[list(k),str(v)] for k,v in sorted(value.d.items())]
    if isinstance(value,dict):return {str(k):encode(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [encode(v) for v in value]
    if isinstance(value,Q):return str(value)
    return value


NUM_TERMS=[((4, 1, 0), 786432), ((4, 0, 1), 2359296), ((3, 2, 0), -196608), ((3, 1, 1), 1835008), ((3, 0, 2), -589824), ((2, 3, 0), 18432), ((2, 2, 1), -194560), ((2, 1, 2), -75776), ((2, 0, 3), 55296), ((1, 4, 0), -768), ((1, 3, 1), 512), ((1, 2, 2), 80896), ((1, 1, 3), -12800), ((1, 0, 4), -2304), ((0, 5, 0), 12), ((0, 4, 1), 244), ((0, 3, 2), 184), ((0, 2, 3), -1112), ((0, 1, 4), 636), ((0, 0, 5), 36)]
RESULTANT_CONSTANT=899679616715369403548229400563231388599310834535159790285851983872
RESULTANT_FACTORS=[([81, 125], 5), ([0, 1], 7), ([-1, 16], 14), ([64, -4369, -30195, -49900, 250000], 1), ([1, 14, 1633, 9530, 19874, 11100, 3625], 1), ([64, 3241, -6416, -34966, 23828, 109985, 82500, 22500], 1), ([5038848, -12189970584, -207098915535, 16450339488516, -199286026683996, -1179788998549176, 40227992581570522, -175059981086037512, -1187369990398617128, -1528684269391186496, -1529810534666677091, -3713341102056530540, -7154447918441392100, -7346176678195664000, -3691662594253760000, -634889742720000000, 52034400000000000], 1)]
F16_BOXES=[['25440488932734262271002747929854655/61960964052944443773704869957817851423', '26467669065253947562470068829337477/64462687641482038832691632276301695334'], ['854510618783674331073464501005951617355/50510220516115515585898377716787501212', '1075390642070700489088678779585362898233/63566463982946934903979430045402669649']]


def displayed_ratio():
    k,U,V=[MP.variable(i) for i in range(3)]
    Num=MP(dict(NUM_TERMS))
    M=64*k*k+64*k*V+(U-V)**2
    Delta=2304*k**3-32*k*k*U+6624*k*k*V-23*k*U*U+942*k*U*V-855*k*V*V+(U+3*V)**3
    return Num,M*Delta,M,Delta


def verify():
    records={}
    def check(name,actual,expected):
        require(actual==expected,name+' failed');records[name]=encode(actual)
    Num,Den,M,Delta=displayed_ratio();derived=family_moment_kernel()
    check('universal balance',derived['balance'],MP(0))
    check('universal moment gap',2*derived['mu2'],3*M)
    check('universal Gram determinant',16*derived['D'],Delta)
    check('universal ratio numerator',32*derived['ratio_numerator'],3*Num)
    check('universal ratio denominator',32*derived['ratio_denominator'],3*Den)
    k,U,V=[MP.variable(i) for i in range(3)]
    def at_k0(poly):return MP({ex:co for ex,co in poly.d.items() if ex[0]==0})
    num0=4*(3*U**3+67*U*U*V+177*U*V*V+9*V**3)
    check('symmetric removable ratio',at_k0(Num),num0*(U-V)**2)
    check('symmetric208/9 square',(208*(U+3*V)**3-9*num0),4*(U+3*V)*(5*U-21*V)**2)
    n,d=Num.third_to_one(),Den.third_to_one()
    P=(n.derivative(0)*d-n*d.derivative(0)).primitive_integer()
    Qp=(n.derivative(1)*d-n*d.derivative(1)).primitive_integer()
    p,q=coefficients_in_U(P),coefficients_in_U(Qp)
    check('gradient U degrees',[len(p)-1,len(q)-1],[9,8])
    R=bareiss(sylvester_rows(p,q,0));expected=[RESULTANT_CONSTANT]
    for factor,power in RESULTANT_FACTORS:expected=imu(expected,ipow(factor,power))
    check('full resultant factorization',R==expected,True)
    records['resultant_degree']=len(R)-1
    records['resultant_coefficient_sha256']=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
    rows=sylvester_rows(p,q,1);leading=[row[:14] for row in rows]
    D1=bareiss([head+[row[14]] for head,row in zip(leading,rows)])
    D0=bareiss([head+[row[15]] for head,row in zip(leading,rows)])
    records['linear_minor_degrees']=[len(D0)-1,len(D1)-1]
    def evaluate_chart(coefficients,value):return [pe(list(map(Q,x)),value) for x in coefficients]
    check('exception kappa1/16 stationary gcd',pgcd(evaluate_chart(p,Q(1,16)),evaluate_chart(q,Q(1,16))),[Q(0),Q(0),Q(1)])
    F4=next(f for f,power in RESULTANT_FACTORS if len(f)==5)
    F6=next(f for f,power in RESULTANT_FACTORS if len(f)==7)
    F7=next(f for f,power in RESULTANT_FACTORS if len(f)==8)
    F16=next(f for f,power in RESULTANT_FACTORS if len(f)==17)
    require(all(x>0 for x in F6),'degree6 positive coefficients failed')
    check('degree7 positive root count',count(sturm(F7),Q(0),'+inf'),0)
    N4=ps(pdiv(D0,F4)[1],-1);L4=pdiv(D1,F4)[1]
    check('quartic lift denominator gcd',pgcd(L4,F4),[Q(1)])
    relation=pa(N4,ps(pm([Q(1),Q(16)],L4),-1))
    check('quartic common-level identity',pdiv(pa(pm(relation,relation),ps(pm([Q(0),Q(1)],pm(L4,L4)),-64)),F4)[1],[Q(0)])
    N16=ps(pdiv(D0,F16)[1],-1);L16=pdiv(D1,F16)[1]
    check('degree16 lift denominator gcd',pgcd(L16,F16),[Q(1)])
    ch=sturm(F16);check('degree16 all positive root count',count(ch,Q(0),'+inf'),2)
    boxes=[tuple(map(Q,box)) for box in F16_BOXES]
    uboxes=[(Q(411732,10**5),Q(411734,10**5)),(Q(5151525,10**5),Q(5151527,10**5))]
    vboxes=[(Q(23),Q(24)),(Q(7),Q(8))]
    for i,(box,ubox,vbox) in enumerate(zip(boxes,uboxes,vboxes),1):
        require(Q(0)<box[0]<box[1],'invalid positive root interval')
        check('degree16 root'+str(i)+' isolation',count(ch,*box),1)
        # Preserve the determinant polynomials for interval evaluation;
        # reduction modulo F16 can introduce avoidable cancellation.
        lift=ivquot(ps(D0,-1),D1,box)
        require(ubox[0]<lift[0]<lift[1]<ubox[1],'degree16 lift enclosure failed')
        nb,db=ivmp(n,(box,ubox,(Q(1),Q(1)))),ivmp(d,(box,ubox,(Q(1),Q(1))))
        require(db[0]>0,'ratio interval denominator not positive')
        value=ivmul(nb,(1/db[1],1/db[0]))
        require(vbox[0]<value[0]<value[1]<vbox[1],'degree16 stationary value separation failed')
        records['degree16 root'+str(i)+' verified boxes']=encode({'kappa':box,'U':ubox,'ratio':vbox})
    # Generic rational witness from the predecessor, and the integer4+3+1 profile.
    def at(poly,k,u,v):return sum(co*k**i*u**j*v**l for (i,j,l),co in poly.d.items())
    check('previous exact benchmark ratio',at(Num,Q(1),Q(300),Q(100))/at(Den,Q(1),Q(300),Q(100)),Q(3504016400,147654727))
    check('three-level integer benchmark ratio',at(Num,Q(121),Q(19321),Q(9025))/at(Den,Q(121),Q(19321),Q(9025)),Q(27899524,1137183))
    controls=0
    for condition in [R==isc(expected,-1),32*derived['ratio_numerator']==3*Num+1,
                      pdiv(pa(pm(relation,relation),ps(pm([Q(0),Q(1)],pm(L4,L4)),-63)),F4)[1]==[Q(0)],
                      count(ch,Q(0),'+inf')==1]:
        try:require(condition,'damaged certificate rejected')
        except ValueError:controls+=1
    require(controls==4,'damage control failed')
    return {'records':records,'checks':len(records),'damage_controls':controls}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write-expected',action='store_true')
    parser.add_argument('--expected',type=Path);args=parser.parse_args();start=time.monotonic()
    output=verify();raw=json.dumps(output,sort_keys=True,separators=(',',':')).encode()
    output['record_sha256']=hashlib.sha256(raw).hexdigest()
    fixture=args.expected or Path(__file__).with_name('expected.json')
    if args.write_expected:fixture.write_text(json.dumps(output,sort_keys=True,indent=2)+'\n')
    else:require(json.loads(fixture.read_text())==output,'expected fixture differs')
    summary={k:v for k,v in output.items() if k!='records'};summary['elapsed_seconds']=round(time.monotonic()-start,6)
    print(json.dumps(summary,sort_keys=True))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError) as error:
        print('verification failed: '+str(error),file=sys.stderr);sys.exit(1)
