"""Receiver-dependent exact stress forms for the J74 rectangle experiment.

All raw receiving/source labels are actual originals. The numerical helper
only proposes a forest. Its values are not proof inputs.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import importlib.util,json,sys

ROOT=Path(__file__).resolve().parent
name='j74_rectangle_local'
if name in sys.modules:p=sys.modules[name]
else:
    spec=importlib.util.spec_from_file_location(name,ROOT/'local.py')
    p=importlib.util.module_from_spec(spec);sys.modules[name]=p;spec.loader.exec_module(p)
c,a,Q=p.c,p.a,p.Q

class Forms:
    def __init__(self,halfwidth=F(1,1000),hole_gate=F(1,17)):
        self.eta=Q(halfwidth)
        self.data=json.loads((c.HERE/'certificate.json').read_text())
        u,self.cycle,self.N,self.R2=c.original_geometry()
        self.raw=a.scale(-1/u[2],u)
        self.E=[a.sub(c.V[j],c.V[i]) for i,j in zip(self.cycle,self.cycle[1:]+self.cycle[:1])]
        self.M=[[a.cross(e,v) for e in self.E] for v in (self.raw,p.EX,p.EY)]
        self.h=[[a.dot(m,c.V[i]) for m,i in zip(ms,self.cycle)] for ms in self.M]
        self.circuits=c.force_circuits(self.N);self.beta=[]
        corners=[a.add(self.raw,(sx*self.eta,sy*self.eta,Q())) for sx,sy in product((-1,1),repeat=2)]
        for indices,weights in self.circuits:
            if len(indices)==2:
                c.require(a.add(self.E[indices[0]],self.E[indices[1]])==c.ZERO,'globally opposite spatial edge circuit')
                coeff=[[Q(1),Q(1)],[Q(),Q()],[Q(),Q()]]
            else:
                i,j,k=indices
                vectors=[a.cross(self.E[j],self.E[k]),a.cross(self.E[k],self.E[i]),a.cross(self.E[i],self.E[j])]
                sign=1 if all(a.dot(v,self.raw)>0 for v in vectors) else -1
                c.require(all(sign*a.dot(v,r)>0 for v in vectors for r in corners),'entire receiving-box cofactor positivity')
                coeff=[[sign*a.dot(v,r) for v in vectors] for r in (self.raw,p.EX,p.EY)]
            T=sum((x*self.h[0][i] for x,i in zip(coeff[0],indices)),Q())
            c.require(T>0,'positive point stress normalization')
            b=[[x/T for x in row] for row in coeff]
            c.require(all(b0*self.h[0][i]==mu for b0,i,mu in zip(b[0],indices,weights)),
                      'literal point stress equals published normalized force circuit')
            vector_terms=[[(0,0)],[(0,1),(1,0)],[(0,2),(2,0)],[(1,1)],[(1,2),(2,1)],[(2,2)]]
            for terms in vector_terms:
                force=tuple(sum((b[bi][column]*self.M[mi][i][axis]
                                 for bi,mi in terms for column,i in enumerate(indices)),Q()) for axis in range(3))
                c.require(force==c.ZERO,'all three exact receiver-polynomial force components')
            self.beta.append(b)
        self.point_holes=[]
        Mn=tuple(tuple(c.IDENTITY[i][j]-2*self.raw[i]*self.raw[j]/a.dot(self.raw,self.raw) for j in range(3)) for i in range(3))
        Mx=((Q(-1),Q(),Q()),(Q(),Q(1),Q()),(Q(),Q(),Q(1)))
        self.hole_gate=Q(hole_gate);threshold=(3-self.hole_gate*self.hole_gate)/(1+self.hole_gate*self.hole_gate)
        c.require((2*self.hole_gate+6*self.eta)*(2*self.hole_gate+6*self.eta)<Q(F(4,257)),
                  'derived old-center hole enters moving relative gate1/16 on entire raw box')
        for item in self.data['poses']:
            g=c.matrix(item['proper_matrix_rows'])
            for ref in (g,c.matmul(c.matmul(Mn,g),Mx)):
                H=[[Q() for j in range(4)] for i in range(4)]
                for axis in range(3):
                    L=c.rotation_form(c.IDENTITY[axis],ref[axis])
                    for i in range(4):
                        for j in range(4):H[i][j]+=L[i][j]
                for i in range(4):H[i][i]-=threshold
                self.point_holes.append(H)
        self.cache={}

    def component_forms(self,circuit,ks):
        key=(circuit,*ks)
        if key in self.cache:return self.cache[key]
        rows,_=self.circuits[circuit];beta=self.beta[circuit]
        c.require(len(ks)==len(rows) and all(type(k) is int and k in range(60) for k in ks),'actual original cut label range')
        matrices=[]
        for normals,heights in zip(self.M,self.h):
            forms=[]
            for i,k in zip(rows,ks):
                L=c.rotation_form(normals[i],c.V[k])
                for j in range(4):L[j][j]-=heights[i]
                forms.append(L)
            matrices.append(forms)
        terms=[[(0,0)],[(0,1),(1,0)],[(0,2),(2,0)],[(1,1)],[(1,2),(2,1)],[(2,2)]]
        components=[]
        for pairs in terms:
            A=[[sum((beta[bi][k]*matrices[mi][k][i][j] for bi,mi in pairs for k in range(len(rows))),Q())
                for j in range(4)] for i in range(4)]
            c.require(all(A[i][j]==A[j][i] for i in range(4) for j in range(4)),'symmetric literal biquadratic form')
            components.append(A)
        # Independently compare the receiver-center form with the prior normalized construction.
        normalized=[c.rotation_form(self.N[i],c.V[k]) for i,k in zip(rows,ks)]
        weights=self.circuits[circuit][1]
        prior=[[sum((w*L[i][j] for w,L in zip(weights,normalized)),Q())-int(i==j)
                for j in range(4)] for i in range(4)]
        c.require(components[0]==prior,'whole literal matrix matches normalized point circuit')
        self.cache[key]=components
        return components

    def receiver_control_forms(self,circuit,ks):
        return receiver_controls(self.component_forms(circuit,ks),self.eta)

    def exact_leaf_coefficients(self,leaf):
        chart,depth,code,kind=leaf[:4];lo,hi=c.box(depth,code);W=quaternion_moments(chart,lo,hi)
        if kind=='H':
            c.require(len(leaf)==5 and type(leaf[4]) is int and leaf[4] in range(12),'actual point equality-reference index')
            return moment_coefficients(self.point_holes[leaf[4]],W)
        c.require(kind=='C','joint cut or derived equality hole')
        ci=leaf[4];ks=leaf[5:]
        c.require(type(ci) is int and ci in range(len(self.circuits)),'literal actual stress index')
        return [x for B in self.receiver_control_forms(ci,ks) for x in moment_coefficients(B,W)]

PAIRS=[(i,j) for i in range(4) for j in range(i+1,4)]
def quaternion_moments(chart,lo,hi):
    other=[i for i in range(4) if i!=chart];width=[y-x for x,y in zip(lo,hi)];out=[]
    for I in product(range(3),repeat=3):
        first={chart:F(1)};second={chart:F(1)}
        for k,index in enumerate(other):
            first[index]=lo[k]+width[k]*F(I[k],2)
            second[index]=lo[k]*lo[k]+lo[k]*width[k]*I[k]+width[k]*width[k]*F(I[k]*(I[k]-1),2)
        out.append([second[i] for i in range(4)]+[first[i]*first[j] for i,j in PAIRS])
    return out
def moment_coefficients(B,W):
    entries=[B[i][i] for i in range(4)]+[2*B[i][j] for i,j in PAIRS]
    return [c.linear(entries,weights) for weights in W]

def receiver_controls(components,e):
    D,Dx,Dy,Dxx,Dxy,Dyy=components;e2=e*e;out=[]
    for i,j in product(range(3),repeat=2):
        sx=-1 if i==1 else 1;sy=-1 if j==1 else 1
        out.append([[D[u][v]+e*((i-1)*Dx[u][v]+(j-1)*Dy[u][v])
                 +e2*(sx*Dxx[u][v]+(i-1)*(j-1)*Dxy[u][v]+sy*Dyy[u][v])
                  for v in range(4)] for u in range(4)])
    return out
