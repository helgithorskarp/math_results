"""Separate Fraction-only full seven-root companion and actual Sturm checks.

No check.py, CAS, author program, author expected output or generic record import.
Rational matrix/Sturm routines credited to own REVIEW10234 source7ac6959e.
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
    sign0=[1 if a[0]>0 else-1 for a in seq if a[0]]
    v0=sum(a!=b for a,b in zip(sign0,sign0[1:]))
    return {'zero_variations':v0,'positive_distinct_roots':v0-variation(1),'sequence':seq,'negative_infinity_variations':variation(-1),'positive_infinity_variations':variation(1),'real_distinct_roots':variation(-1)-variation(1)}
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


def actual(r,tau,control,damage):
    u=r*r;p=r+r**3;T=(u-1)**2*(u+1);y=p*p
    insist(r>1 and tau>=0 and tau<=T and tau<1/(y+1),'actual physical parameter, endpoint control indicated')
    insist((control=='four-double')==(tau==0)and(control=='three-double')==(tau==T),'exact original stratum/control labeling')
    L=[Q(1),-p,Q(1)];U=mul(L,L);q=[p*p+1,-2*p,Q(1)]
    A=add(U,scale(q,-tau));f=mul(U,[x*(-1)**i for i,x in enumerate(A)])
    h=scale(diff(f),Q(1,8));H,rem=divide(h,L)
    insist(rem==[0]and len(H)==6,'whole quintic derivative factorization')
    powers=newton(f,8);N=powers[2];X=powers[4]
    insist(powers[1]==powers[3]==powers[5]==0 and N==4*y-8+2*tau and X==4*y*y-16*y+8-4*tau+2*tau*tau,'all8 original power slots')
    expected_gcd=L
    if control=='three-double':expected_gcd=mul(L,[r**3,Q(1)])
    if control=='four-double':expected_gcd=mul(L,[Q(1),p,Q(1)])
    insist(gcd(f,h)==expected_gcd,'all exact original-double derivative factors')
    roots=sturm(h);quintic=sturm(H);originals=sturm(A)
    counts={'interior':4,'three-double':3,'four-double':2}
    insist(originals['positive_distinct_roots']==originals['real_distinct_roots']==counts[control]and A[0]>0,'entire original companion positivity and no zero')
    insist(roots['real_distinct_roots']==7 and quintic['real_distinct_roots']==5,'entire actual critical root counts')
    M=companion(h)
    if damage=='lost-critical-slot':M=companion(H)
    insist(len(M)==7,'all7 companion slots retained')
    R=evaluate(diff(h),M);RI=inverse(R)
    insist(mmul(R,RI)==eye(7)==mmul(RI,R),'whole actual derivative inverse')
    masses=ms(mmul(evaluate(f,M),RI),Q(-8))
    if damage=='lost-mass-factor':masses=ms(masses,Q(1,8))
    masssum=trace(masses);mass2=trace(mmul(masses,masses))
    insist(masssum==N,'all7 mass normalization including zero masses')
    denominator=X-N*N/8
    if damage=='lost-angular-normalization':denominator=X
    insist(denominator>0,'actual strict angular denominator')
    C=(N*N-mass2)/denominator
    pin=json.loads((Path(__file__).resolve().parent/'POLYNOMIALS.json').read_text())
    def value(rows):return sum((Q(v)*p**i*tau**j for i,j,v in rows),Q(0))
    insist(C==value(pin['num_p_t'])/value(pin['den_p_t'])<16,'independent actual full angular rational identity')
    insist(N*(C+4)**2<800*y,'whole-stratum distance10 bound checked without floating point')
    if y<6:
        insist(C<16-32*(u-1)and N*(C+16)**2<2048*y,'compact parameter32 and distance16 bounds')
    else:insist(C<10,'remaining large-parameter bound')
    return {'r':r,'tau':tau,'control':control,'all9_original_coefficients':f,'all8_original_moments':powers[1:],'L':L,'H5':H,'all7_critical_coefficients':h,'original_gcd':expected_gcd,'all7_companion':M,'all7_derivative_inverse':RI,'all7_mass_operator':masses,'all7_mass_sum':masssum,'all7_squared_mass_sum':mass2,'strict_angular_denominator':denominator,'C':C,'all7_Sturm':roots,'all5_Sturm':quintic,'actual_companion_Sturm':originals}


def main(damage):
    params=[]
    for r,b in [(Q(103,100),Q(1,3)),(Q(26,25),Q(2,3)),(Q(11,10),Q(1,2)),(Q(21,20),Q(3,4)),(Q(21,20),Q(1)),(Q(21,20),Q(0))]:
        T=(r*r-1)**2*(r*r+1);control='three-double'if b==1 else'four-double'if b==0 else'interior';params.append((r,b*T,control))
    for r in [Q(6,5),Q(2)]:params.append((r,1/(2*((r+r**3)**2+1)),'interior'))
    profiles=[actual(r,tau,label,damage)for r,tau,label in params]
    difference=profiles[3]['C']-profiles[4]['C'];insist(difference>0,'actual fixed-p endpoint-monotonicity counterexample')
    boundary=[Q(1)]
    for _ in range(4):boundary=mul(boundary,[Q(-1),Q(0),Q(1)])
    powers=newton(boundary,4);insist(powers[2]==8 and powers[4]-powers[2]**2/8==0,'collapsed angular denominator is zero')
    return encode({'agent':'six-reviewer-1','role':'independent mathematical reviewer','profiles':profiles,'whole_fixed_p_counterexample_difference':difference,'collapsed_octic':boundary,'collapsed_angular_undefined':True})


if __name__=='__main__':
    cli=argparse.ArgumentParser();cli.add_argument('--damage');cli.add_argument('--record',type=Path);args=cli.parse_args()
    if args.damage not in [None,'lost-critical-slot','lost-mass-factor','lost-angular-normalization']:raise ValueError('unknown mathematical defect')
    data=json.dumps(main(args.damage),sort_keys=True,separators=(',',':')).encode()
    if args.record:args.record.write_bytes(data)
    else:print(data.decode())
