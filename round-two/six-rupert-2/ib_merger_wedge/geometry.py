"""Original J74 data and small helpers credited to the G/HB merger packets.

Runtime dependencies are only the original model8551 and ordered-field7140.
No earlier collar, source-entry forest, optimization or private file is imported.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,importlib.util,json,sys
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
PINS={'model.py':'cc0ce4358eea0139da13962b6abdf25a9710fb934e8e41ee3e6f3cbe3acb8cd7',
      'q5.py':'cef1fe01c185fc5c63d729d8e27588b4efe56d8487c87a73f22a68297b18ed3c'}
for name,pin in PINS.items():
    if hashlib.sha256((BASE/name).read_bytes()).hexdigest()!=pin:raise ValueError('before-import original dependency pin: '+name)
sys.path.insert(0,str(BASE));import q5 as a
Q=a.Q
spec=importlib.util.spec_from_file_location('original_J74_ib_model',BASE/'model.py')
model=importlib.util.module_from_spec(spec);spec.loader.exec_module(model)
V=model.VERTICES;Z=(Q(),)*3;S=Q(0,1)
aa,bb,cc=(S-1)/4,(S+1)/4,Q(F(1,2));t,qx=(3-S)/2,(S-1)/2
I=tuple(tuple(Q(int(i==j)) for j in range(3)) for i in range(3))
H=((Q(-1),Q(),Q()),(Q(),Q(-1),Q()),(Q(),Q(),Q(1)))
MX=((Q(-1),Q(),Q()),(Q(),Q(1),Q()),(Q(),Q(),Q(1)))
MY=((Q(1),Q(),Q()),(Q(),Q(-1),Q()),(Q(),Q(),Q(1)))
B=((-aa,-cc,-bb),(cc,-bb,aa),(-bb,-aa,cc))
G=((aa,-cc,-bb),(-cc,-bb,aa),(-bb,aa,-cc))
def require(ok,msg):
    if not ok:raise ValueError(msg)
def enc(x):return [str(x.a),str(x.b)]
def dec(x):return Q(F(x[0]),F(x[1]))
def vec(v):return [enc(x) for x in v]
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()
def act(A,v):return tuple(a.dot(row,v) for row in A)
def mm(A,B):return tuple(tuple(a.dot(row,col) for col in zip(*B)) for row in A)
def proper(A):require(mm(A,tuple(zip(*A)))==I and a.dot(A[0],a.cross(A[1],A[2]))==1,'actual proper original source motion')
def raw(ep,et):return (qx-ep,Q(1),-t-et)
def support(i,j,ep=Q(),et=Q()):
    m=a.cross(raw(ep,et),a.sub(V[j],V[i]));return m,a.dot(m,V[i])
def projection(v,ep,et):return (v[0]-(qx-ep)*v[1],v[2]+(t+et)*v[1])
def det2(u,v):return u[0]*v[1]-u[1]*v[0]
def reflection(r):
    rr=a.dot(r,r)
    return tuple(tuple(I[i][j]-2*r[i]*r[j]/rr for j in range(3)) for i in range(3))
def companion(A,ep,et):return mm(mm(reflection(raw(ep,et)),A),MY)
def rotation(c):
    c2=a.dot(c,c);K=((Q(),-c[2],c[1]),(c[2],Q(),-c[0]),(-c[1],c[0],Q()))
    return tuple(tuple(((1-c2)*I[i][j]+2*c[i]*c[j]+2*K[i][j])/(1+c2) for j in range(3)) for i in range(3))
