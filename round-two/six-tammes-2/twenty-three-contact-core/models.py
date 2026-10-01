"""Derive all four orientations in the quadratic algebra theta^2=rho(t).

No irreducibility is assumed; only polynomial operations use theta. Every
geometric division is audited by check.py. Exact rational-function primitives
are reused, with attribution, from the published 24-contact core.
"""
import itertools
b=c=R=zero=one=t=None

def div(a,z):
 a,z=R.convert(a),R.convert(z)
 b.need(bool(z.n),'generic denominator nonzero polynomial')
 return a*R(z.d,z.n)
def dotr(x,y,H):return sum((x[i]*H[i][j]*y[j] for i in range(3) for j in range(3)),zero)
def cross(x,y):return [x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],x[0]*y[1]-x[1]*y[0]]
def mv(A,x):return [sum((a*b for a,b in zip(row,x)),zero) for row in A]
def inv(A):
 D=c.determinant(A)
 result=[[div((-1)**(i+j)*c.determinant([[A[a][z] for z in range(3) if z!=i]
                    for a in range(3) if a!=j]),D) for j in range(3)] for i in range(3)]
 for i in range(3):
  for j in range(3):
   b.need(sum((A[i][k]*result[k][j] for k in range(3)),zero)==(one if i==j else zero),
          'every rational inverse identity')
 return result

class E:
 rho=None
 def __init__(self,a=None,z=None):self.a,self.z=R.convert(zero if a is None else a),R.convert(zero if z is None else z)
 @staticmethod
 def cv(x):return x if isinstance(x,E) else E(x)
 def __add__(self,x):
  x=self.cv(x);return E(self.a+x.a,self.z+x.z)
 __radd__=__add__
 def __neg__(self):return E(-self.a,-self.z)
 def __sub__(self,x):return self+-self.cv(x)
 def __rsub__(self,x):return self.cv(x)+-self
 def __mul__(self,x):
  x=self.cv(x);return E(self.a*x.a+self.rho*self.z*x.z,self.a*x.z+self.z*x.a)
 __rmul__=__mul__
 def __eq__(self,x):
  x=self.cv(x);return self.a==x.a and self.z==x.z
 def manifest(self):return {'a':{'n':list(self.a.n),'d':list(self.a.d)},
                            'b':{'n':list(self.z.n),'d':list(self.z.d)}}

def dote(x,y,H):return sum((E.cv(x[i])*H[i][j]*E.cv(y[j]) for i in range(3) for j in range(3)),E())
def mve(A,x):return [sum((E.cv(z)*a for a,z in zip(row,x)),E()) for row in A]
def evaluate(f,z):return b.value(f.n,z)/b.value(f.d,z)

def derive(base,core):
 global b,c,R,zero,one,t
 b,c=base,core;R=c.Rat
 zero,one,t=R(),R(b.ONE),R(b.T)
 H=[[one if i==j else t for j in range(3)] for i in range(3)]
 HI=inv(H);r=div(2*t,one+t)
 B={i:[one if j==k else zero for j in range(3)] for k,i in enumerate((1,2,4))}
 for n,i,j,o in ((8,2,4,1),(10,1,2,4),(12,1,10,2),(13,2,8,4)):
  B[n]=[r*(a+z)-d for a,z,d in zip(B[i],B[j],B[o])]
 k=div(t*(9*t*t-2*t-3),(one+t)**2)
 gamma=div(k,one+k)
 mu=div((t-one)*(t+one)*(2*t+one)*(3*t-one),9*t**3-t*t-t+one)
 w=dotr(B[10],B[13],H)
 v=[div(2*t,one+w)*(a+z)-d for a,z,d in zip(B[10],B[13],B[2])]
 z=dotr(v,B[12],H);G=one-z*z
 alpha=div(k-t*z,G);beta=div(t-k*z,G)
 w0=[alpha*a+beta*q for a,q in zip(v,B[12])]
 d=mv(HI,cross(v,B[12]));dn=dotr(d,d,H)
 rho=div(one-dotr(w0,w0,H),dn);E.rho=rho
 RI=inv([[r,r,-one],[-one,r,r],[r,-one,r]])
 functions={'kappa':k,'gamma':gamma,'mu':mu,'common_w':w,'z':z,'plane_gram':G,
            'normal_squared_norm':dn,'rho':rho}
 models={};gaps={}
 for eps in (-1,1):
  W=[E(a,eps*q) for a,q in zip(w0,d)]
  b.need(dote(W,W,H)==one and dote(W,v,H)==k and dote(W,B[12],H)==t,'both W intersections')
  for sig in (-1,1):
   U=[(a+z)*gamma+y*(sig*mu) for a,z,y in zip(W,v,mve(HI,cross(list(map(E.cv,v)),W)))]
   b.need(dote(U,U,H)==one and dote(U,W,H)==k and dote(U,v,H)==k,'both equilateral U choices')
   P={i:list(map(E.cv,x)) for i,x in B.items()}
   for j,i in enumerate((0,5,11)):
    P[i]=[sum((E.cv(x[a])*RI[l][j] for l,x in enumerate((U,W,v))),E()) for a in range(3)]
   P.update({6:U,7:W,9:list(map(E.cv,v))})
   for x in P.values():b.need(dote(x,x,H)==one,'thirteen model unit identities')
   edges=set()
   for anchors in ((0,5,11),(1,2,4)):
    edges.update(tuple(sorted(e)) for e in itertools.combinations(anchors,2))
   for n,i,j,o in ((6,0,11,5),(7,0,5,11),(9,5,11,0),(8,2,4,1),
                   (10,1,2,4),(12,1,10,2),(13,2,8,4)):
    b.need(all(tuple(sorted(e)) in edges for e in ((i,j),(i,o),(j,o))),
           'retained old triangles for all seven reflections')
    edges.update((tuple(sorted((n,i))),tuple(sorted((n,j)))))
   edges.update(((7,12),(9,10),(9,13)))
   b.need(len(edges)==23,'twenty-three distinct contact constraints')
   for i,j in edges:b.need(dote(P[i],P[j],H)==t,'every retained contact on every branch')
   key=f'{eps}_{sig}'
   models[key]=P
   gaps[key]={f'{i}_{j}':dote(P[i],P[j],H)-t for i,j in ((1,7),(10,11),(6,8))}
   for tag,g in gaps[key].items():
    functions[key+'_'+tag+'_a']=g.a
    functions[key+'_'+tag+'_b']=g.z
    functions[key+'_'+tag+'_square']=g.a*g.a-rho*g.z*g.z
   if key=='1_-1':
    for i,j in itertools.combinations(sorted(P),2):
     if (i,j) in edges or (i,j)==(6,8):continue
     g=dote(P[i],P[j],H)
     functions[f'noncontact_{i}_{j}_a']=g.a
     functions[f'noncontact_{i}_{j}_b']=g.z

 b.need(gaps['-1_-1']['1_7']==gaps['-1_1']['1_7'],'both rejected W branches have the same gap')
 functions.update({'Fprime':R(tuple(i*b.F[i] for i in range(1,len(b.F)))),
                   'common_height2':one-div(2*t*t,one+w),'detH':c.determinant(H),
                   'reflection_determinant':c.determinant([[r,r,-one],[-one,r,r],[r,-one,r]]),
                   'packing_threshold_factor':div(functions['1_-1_6_8_square'],R(b.F))})
 b.need(functions['reflection_determinant']==div((3*t-one)*(3*t+one)**2,(one+t)**3),
        'reflection inverse has no exceptional parameter in the interval')
 b.need(dn*functions['detH']==G,'normal metric determinant identity')
 b.need(mu*mu*(one+k)**2==functions['detH']*(one+2*k),'complete equilateral U choices')
 return functions,gaps,models,H
