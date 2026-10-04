"""Separate Fraction-only full seven-root companion and actual Sturm checks.

No check.py, arithmetic.py, author program, expected output or generic record import.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse, json


def insist(ok,label):
    if not ok:raise ValueError(label)
def trim(a):
    a=list(a)
    while len(a)>1 and not a[-1]:a.pop()
    return a
def add(a,b):return trim([(a[i]if i<len(a)else Q(0))+(b[i]if i<len(b)else Q(0))for i in range(max(len(a),len(b)))])
def scale(a,b):return trim([x*b for x in a])
def mul(a,b):
    c=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return trim(c)
def diff(a):return trim([i*a[i]for i in range(1,len(a))])
def divide(a,b):
    a=trim(a);b=trim(b);insist(b!=[0],'literal division domain');out=[Q(0)]*max(1,len(a)-len(b)+1)
    while a!=[0]and len(a)>=len(b):
        k=len(a)-len(b);t=a[-1]/b[-1];out[k]+=t
        a=add(a,[Q(0)]*k+scale(b,-t))
    return trim(out),a
def gcd(a,b):
    while b!=[0]:a,b=b,divide(a,b)[1]
    return scale(a,1/a[-1])
def newton(p,kmax):
    n=len(p)-1;s=[Q(n)]
    for k in range(1,kmax+1):s.append(-sum((p[n-j]*s[k-j]for j in range(1,k)),Q(0))-k*p[n-k])
    return s
def sturm(p):
    seq=[p,diff(p)]
    while seq[-1]!=[0]:
        rem=divide(seq[-2],seq[-1])[1]
        if rem==[0]:break
        seq.append(scale(rem,-1))
    def variation(infty):
        signs=[(1 if a[-1]>0 else-1)*(infty**(len(a)-1))for a in seq]
        return sum(a!=b for a,b in zip(signs,signs[1:]))
    return {'sequence':seq,'negative_infinity_variations':variation(-1),'positive_infinity_variations':variation(1),'real_distinct_roots':variation(-1)-variation(1)}
def zeros(n):return [[Q(0)for _ in range(n)]for _ in range(n)]
def eye(n):
    a=zeros(n)
    for i in range(n):a[i][i]=Q(1)
    return a
def mmul(a,b):
    n=len(a)
    return [[sum((a[i][k]*b[k][j]for k in range(n)),Q(0))for j in range(n)]for i in range(n)]
def madd(a,b):return [[x+y for x,y in zip(ar,br)]for ar,br in zip(a,b)]
def ms(a,s):return [[x*s for x in row]for row in a]
def evaluate(p,a):
    out=zeros(len(a));one=eye(len(a))
    for x in p[::-1]:out=madd(mmul(out,a),ms(one,x))
    return out
def trace(a):return sum((a[i][i]for i in range(len(a))),Q(0))
def inverse(a):
    n=len(a);c=[row[:]+e for row,e in zip(a,eye(n))]
    for k in range(n):
        pivot=next((j for j in range(k,n)if c[j][k]),None);insist(pivot is not None,'actual derivative inverse')
        c[k],c[pivot]=c[pivot],c[k];t=c[k][k];c[k]=[x/t for x in c[k]]
        for j in range(n):
            if j!=k:
                t=c[j][k];c[j]=[x-t*y for x,y in zip(c[j],c[k])]
    insist([row[:n]for row in c]==eye(n),'whole Gaussian identity')
    return [row[n:]for row in c]
def companion(p):
    n=len(p)-1;insist(p[-1]==1,'monic actual quotient');a=zeros(n)
    for i in range(1,n):a[i][i-1]=Q(1)
    for i in range(n):a[i][-1]=-p[i]
    return a
def encode(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,list):return [encode(v)for v in x]
    if isinstance(x,dict):return {k:encode(v)for k,v in x.items()}
    return x


NUM=list(map(Q,[11664,-140292,390636,2706508,4127676,-4018836,-10848244,-4236516,
17047308,12783956,-6621324,-9943644,-1928908,1914084,1688580,864756,315252,69984,11664]))
DEN=list(map(Q,[972,-12555,49377,-112415,-740283,-494007,1712969,1974573,-484767,
-1842073,-739929,173139,269519,231123,166179,76383,27135,5832,972]))
def val(p,x):
    out=Q(0)
    for t in p[::-1]:out=out*x+t
    return out


def actual(r,damage):
    u=r*r;p=r+r**3;B=1+2*u-u*u-u**3;beta=r**3
    insist(r>1 and B>0,'actual physical parameter')
    L=[Q(1),-p,Q(1)];D3=mul(L,[beta,Q(1)]);Q2=[B,2*r,Q(1)]
    f=mul(mul(D3,D3),Q2);h=scale(diff(f),Q(1,8));H,rem=divide(h,D3)
    insist(rem==[0]and len(H)==5,'whole derivative factorization')
    powers=newton(f,8);N=powers[2];X=powers[4]
    insist(powers[1]==powers[3]==powers[5]==0 and N==6*r**6+6*r**4+2*r*r-6,'all8 original power slots')
    insist(gcd(f,h)==D3,'all3 original-double derivative roots')
    roots=sturm(h);quartic=sturm(H)
    insist(roots['real_distinct_roots']==7 and quartic['real_distinct_roots']==4,'entire actual real critical root counts')
    M=companion(h)
    if damage=='lost-critical-slot':M=companion(H)
    insist(len(M)==7,'all7 companion slots retained')
    R=evaluate(diff(h),M);RI=inverse(R)
    insist(mmul(R,RI)==eye(7)==mmul(RI,R),'whole actual derivative inverse')
    masses=ms(mmul(evaluate(f,M),RI),Q(-8))
    if damage=='lost-mass-factor':masses=ms(masses,Q(1,8))
    masssum=trace(masses);mass2=trace(mmul(masses,masses))
    insist(masssum==N,'all7 full-mass sum including3zeros')
    denominator=X-N*N/8
    if damage=='lost-angular-normalization':denominator=X
    insist(denominator>0,'actual strict angular denominator')
    C=(N*N-mass2)/denominator;claimed=val(NUM,u)/val(DEN,u)
    insist(C==claimed<16-34*(u-1),'exact actual angular identity and stronger margin')
    # The distance proof is ordinary; these controls pay its exact factor identities.
    A=4*u*u+6*u+6
    insist(N-2*p*p==(u-1)*A and N+2*p*p-A==(u-1)*(8*u*u+14*u+12)>0,
            'actual collapsed distance factor and signs')
    return {'r':r,'u':u,'B':B,'all9_original_coefficients':f,'all8_original_power_slots':powers[1:],
            'D3':D3,'H4':H,'all7_critical_coefficients':h,'whole7_companion':M,
            'whole7_derivative_inverse':RI,'all7_mass_operator':masses,'all7_mass_sum':masssum,
            'all7_squared_mass_sum':mass2,'angular_denominator':denominator,'C':C,
            'all7_Sturm':roots,'all4_Sturm':quartic}


def main(damage):
    profiles=[actual(r,damage)for r in [Q(21,20),Q(11,10),Q(10,9)]]
    # Collapsed boundary has an undefined angular quotient, not C=16 at D=0.
    boundary=[Q(1)]
    for _ in range(4):boundary=mul(boundary,[Q(-1),Q(0),Q(1)])
    s=newton(boundary,4);insist(s[2]==8 and s[4]-s[2]**2/8==0,'collapsed angular denominator is zero')
    return encode({'agent':'six-reviewer-1','role':'independent mathematical reviewer','profiles':profiles,
                   'collapsed_octic':boundary,'collapsed_angular_undefined':True})


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--damage');p.add_argument('--record',type=Path);a=p.parse_args()
    data=json.dumps(main(a.damage),sort_keys=True,separators=(',',':')).encode()
    if a.record:a.record.write_bytes(data)
    print(data.decode())
