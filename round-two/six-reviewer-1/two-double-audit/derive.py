"""Fresh whole QQ[p,tau] companion-cofactor derivation. No author inputs.

Requires SymPy1.14.0. Coefficient ring characteristic zero; p then tau.
Original written mathematics exposed, native programs and fixtures not read.
"""
from pathlib import Path
from itertools import permutations
import json,time,signal,argparse
import sympy as sp
from sympy.polys.rings import ring
from sympy import QQ
signal.alarm(45)
cli=argparse.ArgumentParser();cli.add_argument("--record",type=Path);args=cli.parse_args()
start=time.monotonic()
R,p,t=ring('p,t',QQ)
one=R.one;zero=R.zero
def need(ok,msg):
    if not ok:raise ValueError(msg)
def matrix(n):return [[zero for _ in range(n)]for _ in range(n)]
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
                for j in range(n):o[i][j]+=a[i][k]*b[k][j]
    return o
def trace(a):return sum((a[i][i]for i in range(len(a))),zero)
def det(a):
    out=zero;n=len(a)
    for perm in permutations(range(n)):
        term=one*(-1)**sum(perm[i]>perm[j]for i in range(n)for j in range(i+1,n))
        for i,j in enumerate(perm):term*=a[i][j]
        out+=term
    return out
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
    o=[zero]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):o[i+j]+=x*y
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
der=evalm(zdiff(H),M)

delta=det(der);inverse=adj(der)

need(multiply(der,inverse)==scale(eye(5),delta)==multiply(inverse,der),'full two sided inverse')
mass=scale(multiply(evalm(zmul(L,[x*(-1)**i for i,x in enumerate(A)]),M),inverse),-8)
need(trace(mass)==N*delta,'full five mass normalization')
enum=trace(multiply(mass,mass));top=N*N*delta*delta-enum;bottom=D*delta*delta

cn,cd=top.cancel(bottom)
need(top*cd==bottom*cn,'whole cleared quotient')

def enc(poly):return [[i,j,str(v)]for (i,j),v in sorted(poly.items())]
out={'sympy':sp.__version__,'num_p_t':enc(cn),'den_p_t':enc(cd),'delta_p_t':enc(delta),'raw_enum_terms':len(enum),'cleared_identity_terms':len(top*cd)}
data=json.dumps(out,sort_keys=True,separators=(',',':')).encode()
if args.record:args.record.write_bytes(data)
else:print(data.decode())
