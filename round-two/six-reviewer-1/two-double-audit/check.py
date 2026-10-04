"""Portable Fraction-only whole two-double audit; no CAS or author imports.

Own CAS-produced POLYNOMIALS.json is checked coefficient for coefficient against
new sparse subset-DP/cofactor companion mathematics before any sign inference.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import permutations
from math import comb
import json,signal,time,resource,argparse,hashlib
cli=argparse.ArgumentParser();cli.add_argument("--record",type=Path);cli.add_argument("--damage");args=cli.parse_args()
if args.damage not in [None,'lost-mass-factor','lost-terminal-num','lost-tensor-coefficient']:raise ValueError('unknown mathematical defect')
signal.alarm(45);start=time.monotonic()
def need(ok,msg):
    if not ok:raise ValueError(msg)
class P(dict):
    def __add__(a,b):
        if not isinstance(b,P):b=const(b)
        o=P(a)
        for k,v in b.items():
            o[k]=o.get(k,F(0))+v
            if not o[k]:del o[k]
        return o
    __radd__=__add__
    def __neg__(a):return P({k:-v for k,v in a.items()})
    def __sub__(a,b):return a+-aspoly(b)
    def __rsub__(a,b):return aspoly(b)+-a
    def __mul__(a,b):
        b=aspoly(b);o=P()
        for (i,j),v in a.items():
            for (k,l),w in b.items():
                key=(i+k,j+l);o[key]=o.get(key,F(0))+v*w
        return P({k:v for k,v in o.items()if v})
    __rmul__=__mul__
    def __truediv__(a,b):return a*F(1,b)
    def __pow__(a,n):
        o=const(1)
        for _ in range(n):o=o*a
        return o
def aspoly(x):return x if isinstance(x,P)else const(x)
def const(x):return P({(0,0):F(x)})if x else P()
one=const(1);zero=P();p=P({(1,0):F(1)});t=P({(0,1):F(1)})
def matrix(n):return [[P()for _ in range(n)]for _ in range(n)]
def eye(n):
    a=matrix(n)
    for i in range(n):a[i][i]=one
    return a
def add(a,b):return [[x+y for x,y in zip(ar,br)]for ar,br in zip(a,b)]
def scale(a,v):return [[x*v for x in row]for row in a]
def multiply(a,b):
    n=len(a);o=matrix(n)
    for i in range(n):
        for k in range(n):
            if a[i][k]:
                for j in range(n):o[i][j]=o[i][j]+a[i][k]*b[k][j]
    return o
def trace(a):return sum((a[i][i]for i in range(len(a))),P())
def det(a):
    n=len(a);dp={0:one}
    for mask in range(1,1<<n):
        row=mask.bit_count()-1;o=P()
        for j in range(n):
            if mask>>j&1:o=o+dp[mask^(1<<j)]*a[row][j]*(-1)**((mask>>(j+1)).bit_count())
        dp[mask]=o
    return dp[(1<<n)-1]
def adj(a):
    n=len(a);o=matrix(n)
    for i in range(n):
        for j in range(n):o[i][j]=det([[a[k][l]for l in range(n)if l!=i]for k in range(n)if k!=j])*(-1)**(i+j)
    return o
def evalm(c,a):
    out=matrix(len(a));unit=eye(len(a))
    for v in c[::-1]:out=add(multiply(out,a),scale(unit,v))
    return out
def zmul(a,b):
    o=[P()for _ in range(len(a)+len(b)-1)]
    for i,x in enumerate(a):
        for j,y in enumerate(b):o[i+j]=o[i+j]+x*y
    return o
def zdiff(c):return [c[i]*i for i in range(1,len(c))]
L=[one,-p,one];U=zmul(L,L);q=[p*p+1,-2*p,one];A=[U[i]-(t*q[i]if i<3 else zero)for i in range(5)];f=zmul(U,[a*(-1)**i for i,a in enumerate(A)])
H=[p**3*t/4,p*p*t/4-p*p/2-3*t/4+1,-p**3/2-3*p*t/4+p,-p*p/2-3*t/4+2,p,one]
need([x/8 for x in zdiff(f)]==zmul(L,H),'whole derivative')
N=4*p*p-8+2*t;X=4*p**4-16*p*p+8-4*t+2*t*t;D=X-N*N/8
M=matrix(5)
for i in range(1,5):M[i][i-1]=one
for i in range(5):M[i][4]=-H[i]
need(evalm(H,M)==matrix(5),'full companion quotient')
der=evalm(zdiff(H),M);delta=det(der);inverse=adj(der)

need(multiply(der,inverse)==scale(eye(5),delta)==multiply(inverse,der),'full two sided inverse')
mass=scale(multiply(evalm(zmul(L,[x*(-1)**i for i,x in enumerate(A)]),M),inverse),-8)
need(trace(mass)==N*delta,'full five mass normalization')
if args.damage=='lost-mass-factor':mass=scale(mass,F(1,8))
need(trace(mass)==N*delta,'full mass normalization after optional damage')
enum=trace(multiply(mass,mass));top=N*N*delta*delta-enum;bottom=D*delta*delta
record=json.loads((Path(__file__).resolve().parent/'POLYNOMIALS.json').read_text())
def decode(rows):
    need(isinstance(rows,list)and rows,'nonempty sparse coefficient list');out=P()
    for row in rows:
        need(isinstance(row,list)and len(row)==3,'typed whole sparse row')
        i,j,v=row
        need(type(i)is int and type(j)is int and 0<=i<=64 and 0<=j<=32,'typed bounded exact exponents')
        need(type(v)is str and str(F(v))==v and F(v)!=0,'canonical nonzero rational coefficient')
        need((i,j)not in out,'unique coefficient position');out[(i,j)]=F(v)
    return out
num=decode(record['num_p_t']);den=decode(record['den_p_t'])
if args.damage=='lost-terminal-num':num.pop(max(num))
need(delta==decode(record['delta_p_t']),'whole derivative norm independent algorithm')
need(top*den==bottom*num,'all cleared angular coefficients')
need(all(i%2==0 for i,j in num.keys()|den.keys()),'entire even p symmetry')

u=p;b=t;y=u*(1+u)**2;T=(u-1)**2*(u+1)*b
def substitute_even(q):
    need(all(i%2==0 for i,j in q),'complete p parity')
    yp=[y**i for i in range(max(i//2 for i,j in q)+1)]
    tp=[T**j for j in range(max(j for i,j in q)+1)]
    return sum((yp[i//2]*tp[j]*v for (i,j),v in q.items()),P())
def divide_u(a,c):
    need(c and all(j==0 for i,j in c),'pure u divisor')
    n=max(i for i,j in c);lc=c[(n,0)];out=P();rem=P(a)
    while rem and max(i for i,j in rem)>=n:
        i,j=max(rem);mon=P({(i-n,j):rem[(i,j)]/lc});out=out+mon;rem=rem-mon*c
    need(not rem,'complete zero division remainder')
    return out
factor=(u-1)**4*(u+1)**6
numub=divide_u(substitute_even(num),factor);denub=divide_u(substitute_even(den),factor)
gap=divide_u(16*denub-numub,u-1)
def bernstein(q,n=None,m=None):
    n=max(i for i,j in q)if n is None else n;m=max(j for i,j in q)if m is None else m
    need(all(i<=n and j<=m for i,j in q),'whole tensor degree')
    w=F(9,40);translated=P()
    for (i,j),v in q.items():
        for k in range(i+1):translated=translated+P({(k,j):v*comb(i,k)*w**k})
    controls=[[sum((v*F(comb(i,k),comb(n,k))*F(comb(j,l),comb(m,l))for (k,l),v in translated.items()if k<=i and l<=j),F(0))for j in range(m+1)]for i in range(n+1)]
    first=[[sum((controls[i][j]*comb(n,i)*comb(n-i,k-i)*(-1)**(k-i)for i in range(k+1)),F(0))for j in range(m+1)]for k in range(n+1)]
    original=P()
    for k in range(n+1):
        for l in range(m+1):
            v=sum((first[k][j]*comb(m,j)*comb(m-j,l-j)*(-1)**(l-j)for j in range(l+1)),F(0))
            if v:original[(k,l)]=v
    need(original==translated,'entire tensor inverse reconstruction')
    return controls
dc=bernstein(denub);gc=bernstein(gap)
if args.damage=='lost-tensor-coefficient':dc[0][0]=F(0)
need(all(x>0 for row in dc+gc for x in row),'every denominator and divided gap control')


strong=bernstein(gap-32*denub)
need(all(x>0 for row in strong for x in row),'all strengthened32 divided gap controls')
# Whole moment, stationary, physical-cutoff and distance identities.
def newton(poly,kmax):
    degree=len(poly)-1;s=[const(degree)]
    for k in range(1,kmax+1):s.append(-sum((poly[degree-j]*s[k-j]for j in range(1,k)),P())-k*poly[degree-k])
    return s
powers=newton(f,8)
need(powers[1]==powers[3]==powers[5]==P()and powers[2]==N and powers[4]==X,'all8 original moment slots')
stationary=[-p**3,3*p*p+1,-3*p,one]
left=zmul(zdiff(U),q);right=zmul(U,zdiff(q))
need([x-y for x,y in zip(left,right)]==[2*x for x in zmul(L,stationary)],'all stationary ratio coefficients')
Y=p*p
need(20*D-N*N==24*Y*Y-96*Y-64-56*Y*t+32*t+26*t*t,'entire large region16 gap')
need(F(25,2)*D-N*N==9*Y*Y-36*Y-64-41*Y*t+32*t+F(59,4)*t*t,'entire strengthened large region10 gap')
need(F(49,40)*(1+F(49,40))**2>6 and 1+2*F(49,40)-F(49,40)**2-F(49,40)**3>0,'whole closed rectangle endpoints')
B0=1+2*u-u*u-u**3;T0=(u-1)**2*(u+1)
need(1-T0*(y+1)==u**3*B0,'actual compact upper endpoint below zero-root wall')
Nub=4*y-8+2*T;A=2*(u*u+3*u+4+(u*u-1)*b)
need(Nub-2*y==(u-1)*A,'complete collapsed squared distance numerator')
need(Nub+2*y-A==(u-1)*(8*u*u+14*u+12+2*(1-b)*(u+1)*(2-u)),'compact distance denominator dominance')
need(16*denub-numub==(u-1)*gap and max(i for i,j in denub)==26 and max(j for i,j in denub)==9,'whole removed gap factor and degree')
need(all(sum((v for (i,j),v in numub.items()if j==k),F(0))==16*sum((v for (i,j),v in denub.items()if j==k),F(0))for k in range(10)),'whole b-polynomial sharp16 boundary')
def encode(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,P):return [[i,j,str(v)]for (i,j),v in sorted(x.items())]
    if isinstance(x,list):return [encode(v)for v in x]
    if isinstance(x,dict):return {k:encode(v)for k,v in x.items()}
    return x
out=encode({'agent':'six-reviewer-1','role':'independent mathematical reviewer','coefficient_domain':'QQ[p,tau]; subsequently QQ[u,b]','original_octic':f,'all8_original_moments':powers[1:],'H5':H,'whole5_companion':M,'whole5_derivative_norm':delta,'whole5_cofactor_inverse':inverse,'full5_mass_numerator':mass,'full_squared_mass_numerator':enum,'all500_cleared_identity_coefficients':top*den,'num_u_b':numub,'den_u_b':denub,'divided16_gap_u_b':gap,'all270_den_controls':dc,'all260_gap_controls':gc,'all270_strengthened32_controls':strong,'whole5_mass_normalization':True,'whole_tensor_inverse_reconstructions':True,'sharp_boundary_full_b_polynomial':True,'compact_parameter32_and_distance16':True,'large_region_C_strict10':True,'whole_stratum_distance10':True})
data=json.dumps(out,sort_keys=True,separators=(',',':')).encode()
if args.record:args.record.write_bytes(data)
else:print(data.decode())
