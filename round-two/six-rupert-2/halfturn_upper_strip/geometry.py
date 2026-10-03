"""Literal original J74 data; small helpers adapted from public9961/10016.

Only model8551 and code-only ordered-field7140 are imported. No earlier
local collar, source forest, receiver-width tree, LP solver or floating input is used.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib, importlib.util, json, sys
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
PINS={'model.py':'cc0ce4358eea0139da13962b6abdf25a9710fb934e8e41ee3e6f3cbe3acb8cd7',
      'q5.py':'cef1fe01c185fc5c63d729d8e27588b4efe56d8487c87a73f22a68297b18ed3c'}
for name,pin in PINS.items():
    if hashlib.sha256((BASE/name).read_bytes()).hexdigest()!=pin:
        raise ValueError('original dependency fingerprint BEFORE import: '+name)
sys.path.insert(0,str(BASE))
import q5 as a
Q=a.Q
spec=importlib.util.spec_from_file_location('original_J74_branch_model',BASE/'model.py')
model=importlib.util.module_from_spec(spec);spec.loader.exec_module(model)
V=model.VERTICES
S=Q(0,1);aa,bb,cc=(S-1)/4,(S+1)/4,Q(F(1,2))
I=tuple(tuple(Q(int(i==j)) for j in range(3)) for i in range(3))
H=((Q(-1),Q(),Q()),(Q(),Q(-1),Q()),(Q(),Q(),Q(1)))
MX=((Q(-1),Q(),Q()),(Q(),Q(1),Q()),(Q(),Q(),Q(1)))
MY=((Q(1),Q(),Q()),(Q(),Q(-1),Q()),(Q(),Q(),Q(1)))
G=((aa,-cc,-bb),(-cc,-bb,aa),(-bb,aa,-cc))
t,ell,qx=(3-S)/2,(5*S-9)/22,(S-1)/2
L=qx-ell
U=(Q(),t,Q(1));U2=a.dot(U,U)
x0=(ell+qx)/2
rho,dx,dy=Q(F(1,1000)),Q(F(1,1000)),Q(F(1,100000))
ENDS=tuple((xx,yy) for xx in (x0-dx,x0+dx) for yy in (t,t+dy))
Z=(Q(),)*3
def require(ok,message):
    if not ok:raise ValueError(message)
def enc(x):return [str(x.a),str(x.b)]
def vec(v):return [enc(x) for x in v]
def dec(x):return Q(F(x[0]),F(x[1]))
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()
def act(A,v):return tuple(a.dot(row,v) for row in A)
def mm(A,B):return tuple(tuple(a.dot(row,col) for col in zip(*B)) for row in A)
def det(A):return a.dot(A[0],a.cross(A[1],A[2]))
def proper(A):require(mm(A,tuple(zip(*A)))==I and det(A)==1,'actual original proper motion')
def raw(x,y):return (x,Q(1),-y)
def reflection(r):
    rr=a.dot(r,r)
    return tuple(tuple(I[i][j]-2*r[i]*r[j]/rr for j in range(3)) for i in range(3))
def rotation(c):
    c2=a.dot(c,c);N=1+c2
    K=((Q(),-c[2],c[1]),(c[2],Q(),-c[0]),(-c[1],c[0],Q()))
    return tuple(tuple(((1-c2)*I[i][j]+2*c[i]*c[j]+2*K[i][j])/N for j in range(3)) for i in range(3))
