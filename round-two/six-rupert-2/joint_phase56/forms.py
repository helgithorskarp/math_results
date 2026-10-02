"""Exact fresh J74 whole-phase56 joint receiver/source forms.

This file constructs inequalities, not an exhaustive cover. Original physical
translation is eliminated only by actual nonnegative equilibrium stresses.
The two gauges apply only after the published source canonicalization.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations, product
import importlib.util, sys, json, hashlib

HERE = Path(__file__).resolve().parent
LOCAL = HERE.parent / 'whole_phase56_collar'
pins=json.loads((HERE/'DEPENDENCIES.json').read_text())
expected_dependencies={'../whole_phase56_collar/check.py','../whole_phase56_collar/algebra.py','../whole_phase56_collar/certificate.json','../whole_phase56_collar/DEPENDENCIES.json','../three_cube_cover/poly.py'}
if set(pins['sha256'])!=expected_dependencies:raise ValueError('literal five-source prerequisites')
for name,digest in pins['sha256'].items():
    if hashlib.sha256((HERE/name).read_bytes()).hexdigest()!=digest:
        raise ValueError('before-import published prerequisite fingerprint: '+name)
sys.path.insert(0, str(LOCAL))
spec = importlib.util.spec_from_file_location('original_phase56_local', LOCAL / 'check.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
a, Q = c.a, c.Q
data, TRI, EDGES = c.certificate()
RAWS = [c.raw(v) for v in TRI]
E = [a.sub(c.V[j], c.V[i]) for i,j in EDGES]
M = Q(F(15,4))
TAU = Q(F(661,221))
LIFT = ((Q(1),M,Q(),Q()),(Q(-1),M,Q(),Q()),
        (Q(),Q(),M,Q(1)),(Q(),Q(),-M,Q(1)))
EYE4 = tuple(tuple(Q(int(i==j)) for j in range(4)) for i in range(4))
PAIRS = ((0,1),(0,2),(1,2))
ZERO4 = tuple(tuple(Q() for j in range(4)) for i in range(4))

def add(*matrices):
    return tuple(tuple(sum((A[i][j] for A in matrices),Q()) for j in range(4)) for i in range(4))

def scale(A,x):
    return tuple(tuple(x*v for v in row) for row in A)

def congruence(A):
    return c.mm(c.mm(c.transpose(LIFT),A),LIFT)

def rotation_form(n,P):
    z=a.dot(n,P); f=a.cross(P,n)
    return ((z,*f),)+tuple((f[i],)+tuple(n[i]*P[j]+P[i]*n[j]-z*int(i==j) for j in range(3)) for i in range(3))

def qform(A,z):
    return sum((z[i]*A[i][j]*z[j] for i in range(4) for j in range(4)),Q())

def rotation_homogeneous(z):
    h,x,y,w=c.act(LIFT,z)
    return ((h*h+x*x-y*y-w*w,2*(x*y-h*w),2*(x*w+h*y)),
            (2*(x*y+h*w),h*h-x*x+y*y-w*w,2*(y*w-h*x)),
            (2*(x*w-h*y),2*(y*w+h*x),h*h-x*x-y*y+w*w))

def triangular_controls(fn):
    diag=[fn(r) for r in RAWS]
    # Homogeneous receiving degree two; pair stresses are elevated by r_y.
    return diag+[scale(add(fn(a.add(RAWS[i],RAWS[j])),scale(diag[i],-1),scale(diag[j],-1)),Q(F(1,2))) for i,j in PAIRS]

def trace_hole(g,comp,r):
    r2=a.dot(r,r); rows=[]
    for axis in range(3):
        if comp:
            row=a.sub(a.scale(r2,g[axis]),a.scale(2*r[axis],tuple(sum((r[k]*g[k][j] for k in range(3)),Q()) for j in range(3))))
            row=c.act(c.MX,row)
        else:
            row=g[axis]
        rows.append(rotation_form(tuple(Q(int(k==axis)) for k in range(3)),row))
    return congruence(add(*rows,scale(EYE4,-TAU*(r2 if comp else Q(1)))))

def gauge(which,r):
    r2=a.dot(r,r)
    v=(r[0],Q(),-M*r[1],-r[2]) if which==0 else (-r[2],M*r[1],Q(),-r[0])
    return tuple(tuple(v[i]*v[j]-r2*int(i==j==0) for j in range(4)) for i in range(4))

def stress_inventory():
    result=[]
    for i,j in combinations(range(len(E)),2):
        if a.add(E[i],E[j])==c.Z:
            # r_y=1 in the actual chart; this positive homogeneous elevation
            # keeps every physical form at receiving degree two.
            result.append({'kind':'pair','indices':(i,j),'weight_vectors':((Q(),Q(1),Q()),)*2})
    for ids in combinations(range(len(E)),3):
        i,j,k=ids
        vectors=(a.cross(E[j],E[k]),a.cross(E[k],E[i]),a.cross(E[i],E[j]))
        ws=[[a.dot(v,r) for v in vectors] for r in RAWS]
        orient=1 if all(x>=0 for row in ws for x in row) else -1 if all(x<=0 for row in ws for x in row) else 0
        if not orient or any(sum((orient*x for x in row),Q())==0 for row in ws):
            continue
        result.append({'kind':'triple','indices':ids,'weight_vectors':tuple(a.scale(orient,v) for v in vectors)})
    c.require(len(result)==230 and sum(x['kind']=='pair' for x in result)==5,'fresh complete admissible230-stress inventory')
    return result

STRESSES = stress_inventory()
HOLES = [triangular_controls(lambda r:trace_hole(c.H,True,r)),
         [trace_hole(c.POSES[4],False,RAWS[0])],
         triangular_controls(lambda r:trace_hole(c.POSES[3],True,r))]
GAUGES = [triangular_controls(lambda r:gauge(i,r)) for i in range(2)]

class ExactForms:
    def __init__(self):
        self.edge_cache={}
        self.cut_cache={}

    def cut(self,ci,ks):
        c.require(type(ci) is int and ci in range(230),'literal fresh stress index')
        rec=STRESSES[ci]; ids=rec['indices']; ks=tuple(ks)
        c.require(len(ks)==len(ids) and all(type(k) is int and k in range(60) for k in ks),'literal original source vertex for each stressed actual edge')
        key=(ci,*ks)
        if key not in self.cut_cache:
            weights=[[a.dot(v,r) for v in rec['weight_vectors']] for r in RAWS]
            parts=[]
            for edge,k in zip(ids,ks):
                ekey=(edge,k)
                if ekey not in self.edge_cache:
                    mats=[]
                    for r in RAWS:
                        m=a.cross(E[edge],r); h=a.dot(m,c.V[EDGES[edge][0]])
                        mats.append(congruence(add(rotation_form(m,c.V[k]),scale(EYE4,-h))))
                    self.edge_cache[ekey]=mats
                parts.append(self.edge_cache[ekey])
            controls=[add(*(scale(parts[k][i],weights[i][k]) for k in range(len(ids)))) for i in range(3)]
            for i,j in PAIRS:
                controls.append(scale(add(*(add(scale(parts[k][j],weights[i][k]),scale(parts[k][i],weights[j][k])) for k in range(len(ids)))),Q(F(1,2))))
            self.cut_cache[key]=controls
        return self.cut_cache[key]

def barycentric_restriction(vertices):
    out=[]
    for u,v in [(v,v) for v in vertices]+[(vertices[i],vertices[j]) for i,j in PAIRS]:
        out.append([u[i]*v[i] for i in range(3)]+[u[i]*v[j]+u[j]*v[i] for i,j in PAIRS])
    return out

def source_box(depth,code):
    c.require(type(depth) is int and type(code) is int and 0<=depth<=40 and 0<=code<2**depth,'closed dyadic source cube')
    lo=[F(-1)]*3; hi=[F(1)]*3
    for level in range(depth):
        axis=level%3; mid=(lo[axis]+hi[axis])/2
        if code>>(depth-level-1)&1:lo[axis]=mid
        else:hi[axis]=mid
    return lo,hi

def source_moments(depth,code):
    lo,hi=source_box(depth,code); out=[]
    for idx in product(range(3),repeat=3):
        first=[lo[k]+(hi[k]-lo[k])*F(idx[k],2) for k in range(3)]
        second=[(lo[k]*lo[k],lo[k]*hi[k],hi[k]*hi[k])[idx[k]] for k in range(3)]
        z=[F(1),*first]; W=[[x*y for y in z] for x in z]
        for k in range(3):W[k+1][k+1]=second[k]
        out.append((idx,W))
    return out

def tensor_coefficients(matrices,vertices,depth,code,unused_source_axis=None):
    W=source_moments(depth,code)
    if unused_source_axis is not None:
        col=unused_source_axis+1
        c.require(all(A[col][j]==0 and A[j][col]==0 for A in matrices for j in range(4)),'advertised unused gauge source axis is identically absent')
        W=[v for v in W if v[0][unused_source_axis]==0]
    source=[[sum((A[i][j]*w[i][j] for i in range(4) for j in range(4)),Q()) for idx,w in W] for A in matrices]
    if len(matrices)==1:return source[0]
    c.require(len(matrices)==6,'six homogeneous triangular receiving controls')
    T=barycentric_restriction(vertices)
    return [sum((T[i][k]*source[k][j] for k in range(6)),Q()) for i in range(6) for j in range(len(W))]

def receiver_split(vertices,edge):
    c.require(type(edge) is int and edge in range(3),'actual receiver edge')
    i,j=PAIRS[edge]; k=3-i-j
    mid=tuple((x+y)/2 for x,y in zip(vertices[i],vertices[j]))
    return [(vertices[i],mid,vertices[k]),(mid,vertices[j],vertices[k])]

UNIT_TRI = tuple(tuple(F(int(i==j)) for j in range(3)) for i in range(3))

def literal_cut(ci,ks,r,z):
    rec=STRESSES[ci]; R=rotation_homogeneous(z)
    norm=a.dot(c.act(LIFT,z),c.act(LIFT,z)); out=Q()
    for edge,k,v in zip(rec['indices'],ks,rec['weight_vectors']):
        w=a.dot(v,r); m=a.cross(E[edge],r); h=a.dot(m,c.V[EDGES[edge][0]])
        out+=w*(a.dot(m,c.act(R,c.V[k]))-h*norm)
    return out
