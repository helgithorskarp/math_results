"""Independent full seven-slot rational Gaussian/Sturm route. Own older rational helpers credited to REVIEW10244/10234; no new-author native access."""
from fractions import Fraction as Q
from pathlib import Path
import json,argparse,signal

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
def raw_sturm(p):
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


def sturm(p):
    if p[0]:
        out=raw_sturm(p);out['zero_distinct_roots']=0
        out['negative_distinct_roots']=out['real_distinct_roots']-out['positive_distinct_roots'];return out
    insist(len(p)>1 and p[1]!=0,'simple zero-root license')
    out=raw_sturm(p[1:]);out['zero_distinct_roots']=1
    out['negative_distinct_roots']=out['real_distinct_roots']-out['positive_distinct_roots']
    out['real_distinct_roots']+=1;out['explicit_zero_factored_before_Sturm']=True;return out
def actual(a,lam,even,damage):
    if even:
        d=[Q(-1),Q(0),Q(1)];q=[Q(6),Q(0),Q(-5),Q(0),Q(1)]
        s=Q(0);a=Q(1)
    else:
        s=1/a-a;d=[Q(-1),s,Q(1)];B=[Q(-1),-s,Q(1)]
        q=add(mul(B,B),scale([s*s-1,-2*s,Q(1)],lam))
    f=mul(mul(d,d),q);h=scale(diff(f),Q(1,8));H,rem=divide(h,d)
    insist(rem==[0]and len(H)==6,'whole actual quintic')
    qs=sturm(q);ds=sturm(d);hs=sturm(h);Hs=sturm(H)
    insist(qs['real_distinct_roots']==4 and qs['positive_distinct_roots']==2 and qs['negative_distinct_roots']==2 and qs['zero_distinct_roots']==0,'all four actual original singles and signs')
    insist(gcd(q,d)==[Q(1)]and gcd(q,diff(q))==[Q(1)]and gcd(f,h)==d,'exact original double/single collision license')
    insist(hs['real_distinct_roots']==7 and Hs['real_distinct_roots']==5 and gcd(h,diff(h))==[Q(1)],'all actual critical slots simple')
    insist(ds['positive_distinct_roots']==ds['negative_distinct_roots']==1,'opposite original doubles')
    if even:insist(hs['zero_distinct_roots']==1,'singular even zero critical explicitly retained')
    mu=newton(f,8);N=mu[2];X=mu[4];D=X-N*N/8
    insist(mu[1]==mu[3]==mu[5]==0 and N>0 and D>0,'all8 actual moments and strict normalization')
    M=companion(h)
    if damage=='seven-slot':M=companion(H)
    insist(len(M)==7,'all seven literal critical slots')
    R=evaluate(diff(h),M);RI=inverse(R);mass=ms(mmul(evaluate(f,M),RI),Q(-8))
    if damage=='literal-mass':mass=ms(mass,Q(1,8))
    insist(mmul(R,RI)==eye(7)==mmul(RI,R),'entire literal two-sided inverse')
    insist(trace(mass)==N,'entire seven-slot mass sum')
    mass2=trace(mmul(mass,mass));C=(N*N-mass2)/D
    if damage=='raw-normalization':C=(N*N-mass2)/X
    if not even:
        pin=json.loads((Path(__file__).resolve().parent/'INPUT.json').read_text())
        def value(rows):return sum((Q(x)*(-1)**(i//2)*s**i*lam**j for i,j,x in rows),Q(0))
        insist(C==value(pin['num_p_t'])/value(pin['den_p_t']),'whole actual normalized angular trace')
        insist(C<(16 if lam<0 else Q(47,2)),'actual sector strict value')
    else:insist(C<Q(47,2),'actual even strict example, not the universal even proof')
    return {'a':a,'s':s,'lambda':lam,'even':even,'original_octic':f,'original_single_quartic':q,'all8_original_moments':mu[1:],'original_double_factor':d,'actual_H5':H,'all7_critical_polynomial':h,'quartic_Sturm':qs,'double_Sturm':ds,'quintic_Sturm':Hs,'seven_slot_Sturm':hs,'all7_companion':M,'all49_inverse_positions':RI,'all49_mass_positions':mass,'full_mass_sum':trace(mass),'full_squared_mass_sum':mass2,'Draw':D,'C':C}
def main(damage):
    rows=[actual(Q(9,10),Q(-1),False,damage),actual(Q(4,5),Q(-3),False,damage),actual(Q(9,10),Q(9,10),False,damage),actual(Q(1),Q(0),True,damage)]
    # The endpoint4-double branch has zero D; no quotient is assigned.
    f=[Q(1)]
    for _ in range(4):f=mul(f,[Q(-1),Q(0),Q(1)])
    mu=newton(f,8);insist(mu[4]-mu[2]**2/8==0,'sign-collapsed quotient undefined')
    return encode({'agent':'six-reviewer-1','role':'independent mathematical reviewer','profiles':rows,'whole392_inverse_and_mass_positions':392,'collapsed_octic':f,'collapsed_quotient_undefined':True})
if __name__=='__main__':
    signal.alarm(45)
    cli=argparse.ArgumentParser();cli.add_argument('--record',type=Path);cli.add_argument('--damage');args=cli.parse_args()
    insist(args.damage in [None,'seven-slot','literal-mass','raw-normalization'],'known literal defect')
    data=json.dumps(main(args.damage),sort_keys=True,separators=(',',':')).encode()
    if args.record:args.record.write_bytes(data)
    else:print(data.decode())
