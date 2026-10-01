#!/usr/bin/env python3
"""Exact fourfold original-root angular bound; standard-library Fraction arithmetic.
Sparse Fraction kernel adapted from own8800/source167af56c25651784f7c8106a3ec1d85e52b51c82.
Quartic matching identity credits graph7883/source0706544236f9ae7ab6d29920d2eb7e743a3c430e.
Full-coordinate commutant control adapts own8957/source90144c5427d52bdeacb2ff36ac7ab6fef8afd6cd.
Actual author six-sendov-2, researcher. No runtime campaign imports, CAS or floats.
"""
from __future__ import annotations
from fractions import Fraction as Q
from pathlib import Path
from math import comb,gcd,lcm,factorial
from itertools import permutations,product
import argparse,hashlib,json,sys,time

def require(value, message):
    if not value:
        raise ValueError(message)


def trim(p):
    p=list(p)
    while len(p)>1 and not p[-1]:p.pop()
    return p


def pa(p,q):
    out=[Q(0)]*max(len(p),len(q))
    for i,c in enumerate(p):out[i]+=c
    for i,c in enumerate(q):out[i]+=c
    return trim(out)


def ps(p,c):return trim([x*c for x in p])


def pm(p,q):
    out=[Q(0)]*(len(p)+len(q)-1)
    for i,c in enumerate(p):
        for j,d in enumerate(q):out[i+j]+=c*d
    return trim(out)


def pd(p):return trim([i*p[i] for i in range(1,len(p))] or [Q(0)])


def pe(p,x):
    value=Q(0)
    for c in reversed(p):value=value*x+c
    return value


def pdiv(p,q):
    p,q=trim(list(map(Q,p))),trim(list(map(Q,q)))
    require(q!=[0],'zero polynomial denominator')
    quotient=[Q(0)]*max(1,len(p)-len(q)+1)
    while p!=[0] and len(p)>=len(q):
        k,c=len(p)-len(q),p[-1]/q[-1]
        quotient[k]+=c;p=pa(p,ps([Q(0)]*k+q,-c))
    return trim(quotient),p


def pgcd(p,q):
    while q!=[0]:p,q=q,pdiv(p,q)[1]
    return ps(p,1/p[-1])


class MP:
    """Sparse Q-polynomials in three indeterminates, no CAS dependency."""
    def __init__(self,value=0):
        if isinstance(value,MP):self.d=value.d;return
        if isinstance(value,dict):self.d={k:Q(v) for k,v in value.items() if v}
        else:self.d={(0,0,0):Q(value)} if value else {}
    @staticmethod
    def variable(i):
        k=[0,0,0];k[i]=1;return MP({tuple(k):1})
    def __add__(self,other):
        out=dict(self.d)
        for k,v in MP(other).d.items():out[k]=out.get(k,Q(0))+v
        return MP(out)
    __radd__=__add__
    def __neg__(self):return MP({k:-v for k,v in self.d.items()})
    def __sub__(self,other):return self+-MP(other)
    def __rsub__(self,other):return MP(other)+-self
    def __mul__(self,other):
        out={}
        for k,v in self.d.items():
            for l,w in MP(other).d.items():
                key=tuple(a+b for a,b in zip(k,l));out[key]=out.get(key,Q(0))+v*w
        return MP(out)
    __rmul__=__mul__
    def __truediv__(self,other):return self*(Q(1)/other)
    def __pow__(self,n):
        out=MP(1)
        for _ in range(n):out=out*self
        return out
    def __eq__(self,other):return self.d==MP(other).d
    def __bool__(self):return bool(self.d)
    def derivative(self,i):
        out={}
        for k,v in self.d.items():
            if k[i]:
                l=list(k);l[i]-=1;out[tuple(l)]=v*k[i]
        return MP(out)
    def square_variable(self):
        require(all(k[0]%2==0 for k in self.d),'odd center power')
        return MP({(k[0]//2,k[1],k[2]):v for k,v in self.d.items()})
    def third_to_one(self):
        out={}
        for k,v in self.d.items():
            key=(k[0],k[1],0);out[key]=out.get(key,Q(0))+v
        return MP(out)
    def primitive_integer(self):
        denominator=lcm(*(v.denominator for v in self.d.values()))
        ints={k:int(v*denominator) for k,v in self.d.items()}
        content=gcd(*ints.values())
        return MP({k:v//content for k,v in ints.items()})


def zpm(p,q):
    out=[MP(0)]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q):out[i+j]=out[i+j]+x*y
    return out
def zpow(p,n):
    out=[MP(1)]
    for _ in range(n):out=zpm(out,p)
    return out
def det3(G):
    out=MP(0)
    for p in permutations(range(3)):
        sign=(-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
        out+=sign*G[0][p[0]]*G[1][p[1]]*G[2][p[2]]
    return out


def sturm(p):
    def norm(a):return ps(a,1/abs(a[-1]))
    a,b=norm(trim(list(map(Q,p)))),norm(pd(list(map(Q,p))));out=[a,b]
    while True:
        r=ps(pdiv(a,b)[1],-1)
        if r==[0]:break
        r=norm(r);out.append(r);a,b=b,r
    return out
def variations(chain,x):
    signs=[]
    for p in chain:
        if x=='+inf':a=p[-1]
        else:a=pe(p,x)
        if a:signs.append(1 if a>0 else -1)
    return sum(a!=b for a,b in zip(signs,signs[1:]))
def count(chain,a,b):return variations(chain,a)-variations(chain,b)
def ivadd(a,b):return a[0]+b[0],a[1]+b[1]
def ivmul(a,b):
    v=[x*y for x in a for y in b];return min(v),max(v)
def ivpoly(p,x):
    out=(Q(0),Q(0))
    for c in reversed(p):out=ivadd(ivmul(out,x),(c,c))
    return out
def ivquot(n,d,x):
    a,b=ivpoly(n,x),ivpoly(d,x);require(b[0]>0 or b[1]<0,'lift interval denominator containszero')
    return ivmul(a,(1/b[1],1/b[0]))
def ivmp(p,boxes):
    powers=[]
    for box in boxes:
        values=[(Q(1),Q(1))]
        for _ in range(10):values.append(ivmul(values[-1],box))
        powers.append(values)
    out=(Q(0),Q(0))
    for exponents,c in p.d.items():
        term=(c,c)
        for i,k in enumerate(exponents):term=ivmul(term,powers[i][k])
        out=ivadd(out,term)
    return out


def determinant(G):
    dimension=len(G)
    out=MP(0)
    for permutation in permutations(range(dimension)):
        term=MP((-1)**sum(permutation[i]>permutation[j]
                         for i in range(dimension) for j in range(i+1,dimension)))
        for i,j in enumerate(permutation):term*=G[i][j]
        out+=term
    return out


def newton(poly,limit):
    degree=len(poly)-1
    require(poly[-1]==1,'Newton polynomial must be monic')
    powers=[MP(degree)]
    for k in range(1,limit+1):
        if k<=degree:
            value=-k*poly[degree-k]-sum((poly[degree-j]*powers[k-j]
                                      for j in range(1,k)),MP(0))
        else:
            value=-sum((poly[degree-j]*powers[k-j]
                        for j in range(1,degree+1)),MP(0))
        powers.append(value)
    return powers


def evaluate(p,point):
    out=Q(0)
    for exponents,coefficient in p.d.items():
        term=coefficient
        for coordinate,power in zip(point,exponents):term*=coordinate**power
        out+=term
    return out


def encode(p):
    return [[*exponents,str(coefficient)] for exponents,coefficient in sorted(p.d.items())]


def decode(terms):
    return MP({tuple(row[:3]):Q(row[3]) for row in terms})


def shared_positive_normalize(n,d):
    common_denominator=lcm(*(v.denominator for p in [n,d] for v in p.d.values()))
    common_content=gcd(*(int(v*common_denominator) for p in [n,d] for v in p.d.values()))
    scale=Q(common_denominator,common_content)
    require(scale>0,'normalization must preserve denominator positivity')
    return n*scale,d*scale,scale


def build_kernel():
    A,B,D=[MP.variable(i) for i in range(3)]
    shift=[MP(-1),MP(1)]
    g=zpow(shift,4)
    for j,c in enumerate(zpow(shift,2)):g[j]+=A*c
    for j,c in enumerate(shift):g[j]-=B*c
    g[0]+=D
    f=zpm(zpow([MP(1),MP(1)],4),g)
    h=[A/4+3*B/8+D/2,-A-5*B/8-1,3*A/4+3,MP(-3),MP(1)]
    require([Q(j,8)*f[j] for j in range(1,len(f))]==zpm(zpow([MP(1),MP(1)],3),h),
            'original derivative and independent active quartic differ')
    powers_original=newton(f,5)
    require(powers_original[1]==0,'original degree-eight profile is not balanced')
    N,S3,S4,S5=powers_original[2:6]
    m2=S4-N*N/8;m3=S5-N*S3/4
    require(N==8-2*A and S3==-6*A+3*B,'original lower moment formula')
    require(m2==3*A*A/2-8*A+12*B-4*D,'original second mass moment formula')
    require(m3==7*A*A-7*A*B/2-8*A+24*B-20*D,'original third mass moment formula')
    powers_active=newton(h,6)
    G=[[powers_active[i+j] for j in range(4)] for i in range(4)]
    det=determinant(G)
    adj=[[(-1)**(i+j)*det3([[G[k][l] for l in range(4) if l!=i]
                           for k in range(4) if k!=j]) for j in range(4)]
         for i in range(4)]
    mu=[N,S3,m2,m3]
    square=sum((mu[i]*adj[i][j]*mu[j] for i in range(4) for j in range(4)),MP(0))
    n,d,scale=shared_positive_normalize(N*N*det-square,m2*det)
    gradients=[(n.derivative(i)*d-n*d.derivative(i)).primitive_integer() for i in range(3)]
    return {'h':h,'f':f,'N':N,'S3':S3,'m2':m2,'m3':m3,'gram_det':det,
            'n':n,'d':d,'positive_shared_scale':scale,'gradients':gradients}


def invariants(delta):
    require(len(delta)==4 and sum(delta)==0,'deviation profile is not balanced')
    e=[Q(1),Q(0),Q(0),Q(0),Q(0)]
    for x in delta:
        for j in range(4,0,-1):e[j]+=x*e[j-1]
    return tuple(e[2:])


def fraction_solve(matrix,rhs):
    rows=[list(map(Q,row))+[Q(v)] for row,v in zip(matrix,rhs)]
    size=len(rows)
    for j in range(size):
        pivot=next((i for i in range(j,size) if rows[i][j]),None)
        require(pivot is not None,'singular exact projection Gram')
        rows[j],rows[pivot]=rows[pivot],rows[j]
        scalar=rows[j][j];rows[j]=[x/scalar for x in rows[j]]
        for i in range(size):
            if i!=j and rows[i][j]:
                scalar=rows[i][j];rows[i]=[x-scalar*y for x,y in zip(rows[i],rows[j])]
    return [row[-1] for row in rows]

def full_pinching(profile):
    """Different finite control: full eight-coordinate symmetric commutant.

    Frobenius projection of uu^T onto {S=S^T: SH=HS}, without an active
    cubic or spectral residues. H is scaled by8 to make entries integral.
    """
    require(len(profile)==8 and sum(profile)==0,'invalid literal profile')
    slots=[(i,j) for i in range(8) for j in range(i,8)]
    index={slot:k for k,slot in enumerate(slots)}
    H=[[Q((8*profile[i] if i==j else 0)-profile[i]-profile[j]) for j in range(8)] for i in range(8)]
    rows=[]
    for i in range(8):
        for j in range(i+1,8):
            row=[Q(0)]*len(slots)
            for k in range(8):
                row[index[tuple(sorted((i,k)))]]+=H[k][j]
                row[index[tuple(sorted((k,j)))]]-=H[i][k]
            rows.append(row)
    pivots=[];position=0
    for j in range(len(slots)):
        pivot=next((i for i in range(position,len(rows)) if rows[i][j]),None)
        if pivot is None:continue
        rows[position],rows[pivot]=rows[pivot],rows[position]
        scalar=rows[position][j];rows[position]=[x/scalar for x in rows[position]]
        for i in range(len(rows)):
            if i!=position and rows[i][j]:
                scalar=rows[i][j];rows[i]=[x-scalar*y for x,y in zip(rows[i],rows[position])]
        pivots.append(j);position+=1
        if position==len(rows):break
    basis=[]
    for free in range(len(slots)):
        if free in pivots:continue
        vector=[Q(0)]*len(slots);vector[free]=1
        for i,pivot in enumerate(pivots):vector[pivot]=-rows[i][free]
        basis.append(vector)
    weight=[1 if i==j else 2 for i,j in slots]
    target=[Q(profile[i]*profile[j]) for i,j in slots]
    def dot(x,y):return sum(w*a*b for w,a,b in zip(weight,x,y))
    Gram=[[dot(x,y) for y in basis] for x in basis];rhs=[dot(x,target) for x in basis]
    solution=fraction_solve(Gram,rhs)
    return sum(x*y for x,y in zip(solution,rhs))


def substitute(poly,values):
 powers=[]
 for i,val in enumerate(values):
  row=[MP(1)]
  for j in range(max(k[i] for k in poly.d)):row.append(row[-1]*val)
  powers.append(row)
 return sum((c*powers[0][i]*powers[1][j]*powers[2][l] for (i,j,l),c in poly.d.items()),MP(0))

def divide_variable(poly,variable,power):
 require(all(k[variable]>=power for k in poly.d),'missing monomial factor')
 out={}
 for k,c in poly.d.items():
  l=list(k);l[variable]-=power;out[tuple(l)]=c
 return MP(out)

def divide_one_minus_y(poly):
 out={}
 for i,l in {(k[0],k[2]) for k in poly.d}:
  coefficients=[poly.d.get((i,j,l),Q(0)) for j in range(max(k[1] for k in poly.d)+1)]
  require(sum(coefficients)==0,'comparison does not vanish at y=1')
  running=Q(0)
  for j,c in enumerate(coefficients[:-1]):
   running+=c
   if running:out[(i,j,l)]=running
 return MP(out)

def bernstein(poly,box):
 unit_vars=[MP.variable(i) for i in range(3)]
 unit=substitute(poly,[lo+(hi-lo)*var for (lo,hi),var in zip(box,unit_vars)])
 degrees=tuple(max(k[i] for k in unit.d) for i in range(3))
 coefficients={}
 for index in product(*(range(d+1) for d in degrees)):
  total=Q(0)
  for powers,c in unit.d.items():
   if all(k<=i for k,i in zip(powers,index)):
    term=c
    for i,k,d in zip(index,powers,degrees):term*=Q(comb(i,k),comb(d,k))
    total+=term
  coefficients[index]=total
 return degrees,coefficients


def reconstruct_Bernstein(degrees,coefficients):
    variables=[MP.variable(i) for i in range(3)]
    basis=[]
    for variable,degree in zip(variables,degrees):
        basis.append([comb(degree,i)*variable**i*(1-variable)**(degree-i)
                      for i in range(degree+1)])
    return sum((coefficient*basis[0][i]*basis[1][j]*basis[2][l]
                for (i,j,l),coefficient in coefficients.items()),MP(0))


def primitive_with_positive_scale(poly):
    denominator=lcm(*(v.denominator for v in poly.d.values()))
    content=gcd(*(int(v*denominator) for v in poly.d.values()))
    scale=Q(denominator,content)
    require(scale>0,'primitive scale must preserve sign')
    return poly*scale,scale


def three_moment_kernel(k):
    powers=newton(k['h'],4)
    G=[[powers[i+j] for j in range(3)] for i in range(3)]
    det=det3(G)
    adj=[[(-1)**(i+j)*determinant([[G[r][c] for c in range(3) if c!=i]
                                 for r in range(3) if r!=j]) for j in range(3)]
         for i in range(3)]
    mu=[k['N'],k['S3'],k['m2']]
    square=sum((mu[i]*adj[i][j]*mu[j] for i in range(3) for j in range(3)),MP(0))
    n,d,scale=shared_positive_normalize(k['N']**2*det-square,k['m2']*det)
    A,B,D=[MP.variable(i) for i in range(3)]
    K=18*A**3-14*A*A-18*A*B-64*A*D+16*A+75*B*B-36*B+32*D
    require(det==-3*K/16,'three-moment Gram determinant factor')
    require(d==-(3*A*A-16*A+24*B-8*D)*K,'positive denominator factor')
    require(scale==Q(32,3),'positive physical three-moment normalization')
    return {'n':n,'d':d,'gram_det':det,'positive_scale':scale}


def json_native(value):
    if isinstance(value,MP):return encode(value)
    if isinstance(value,Q):return str(value)
    if isinstance(value,dict):return {str(k):json_native(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [json_native(v) for v in value]
    return value


def specialize_D(poly,A,B):
    out=[Q(0)]*(1+max(k[2] for k in poly.d))
    for (i,j,l),v in poly.d.items():out[l]+=v*A**i*B**j
    return trim(out)


def verify():
    records={};checks=0
    def check(name,value,expected=True):
        nonlocal checks
        require(value==expected,name+' failed')
        checks+=1;records[name]=json_native(value)
    k=build_kernel();r=three_moment_kernel(k)
    A,B,D=[MP.variable(i) for i in range(3)]
    check('full quartic n,d term counts',[len(k['n'].d),len(k['d'].d)],[50,50])
    check('relaxation n,d term counts',[len(r['n'].d),len(r['d'].d)],[17,19])
    records['original moments']={key:encode(k[key]) for key in ['N','S3','m2','m3']}
    records['active quartic']=[encode(poly) for poly in k['h']]
    records['three-moment positive scale']=str(r['positive_scale'])
    records['three-moment n']=encode(r['n']);records['three-moment d']=encode(r['d'])
    # Independent balanced four-root identities, using roots rather than the chart.
    x,y,z=[MP.variable(i) for i in range(3)]
    delta=[x,y,z,-x-y-z]
    ae=sum((delta[i]*delta[j] for i in range(4) for j in range(i+1,4)),MP(0))
    be=sum((delta[i]*delta[j]*delta[l] for i in range(4)
            for j in range(i+1,4) for l in range(j+1,4)),MP(0))
    de=delta[0]*delta[1]*delta[2]*delta[3]
    matching=sum(((delta[i]-delta[j])**2*(delta[l]-delta[m])**2
                  for i,j,l,m in [(0,1,2,3),(0,2,1,3),(0,3,1,2)]),MP(0))/2
    check('root-derived matching SOS',ae*ae+12*de==matching)
    quartic=[D,-B,A,MP(0),MP(1)];powers=newton(quartic,4)
    check('quartic raw Newton moments',powers,[MP(4),MP(0),-2*A,3*B,2*A*A-4*D])
    delta_G=[[powers[i+j] for j in range(3)] for i in range(3)]
    check('quartic moment determinant',det3(delta_G),-8*A**3+32*A*D-36*B*B)
    t,y,v=[MP.variable(i) for i in range(3)]
    values=[-6*t*t,-8*t**3*y,t**4*(-3+12*(1-y*y)*v)]
    check('enclosed matching SOS',substitute(A*A+12*D,values),144*t**4*(1-y*y)*v)
    check('enclosed moment determinant',substitute(det3(delta_G),values),
          2304*t**6*(1-y*y)*(1-v))
    n,d=[divide_variable(substitute(r[key],values),0,4) for key in ['n','d']]
    nt=8*(t+2)**2*(3*t-2)**2
    dt=(10*t*t-4*t+1)*(11*t*t-16*t+8)
    check('three-level endpoint comparison',substitute(n,[t,MP(1),MP(0)])*dt,
          substitute(d,[t,MP(1),MP(0)])*nt)
    comparison,scale1=primitive_with_positive_scale(
        divide_one_minus_y(divide_variable(nt*d-dt*n,0,1)))
    upper,scale2=primitive_with_positive_scale(Q(49,2)*d-n)
    check('small comparison factorization',nt*d-dt*n==t*(1-y)*comparison/scale1)
    check('large bound factorization',Q(49,2)*d-n==upper/scale2)
    certificates=[]
    for name,poly,box,degrees0,minimum0 in [
        ('small radius',comparison,((Q(0),Q(1,4)),(Q(-1),Q(1)),(Q(0),Q(1))),
         (9,3,2),Q(3614625,65536)),
        ('large radius',upper,((Q(1,4),Q(5,6)),(Q(-1),Q(1)),(Q(0),Q(1))),
         (6,4,2),Q(176175,2048))]:
        degrees,coefficients=bernstein(poly,box)
        check(name+' Bernstein degrees',degrees,degrees0)
        check(name+' all coefficients positive',all(c>0 for c in coefficients.values()))
        check(name+' exact minimum',min(coefficients.values()),minimum0)
        unit=[MP.variable(i) for i in range(3)]
        check(name+' independent Bernstein basis reconstruction',
              reconstruct_Bernstein(degrees,coefficients)==
              substitute(poly,[lo+(hi-lo)*x for (lo,hi),x in zip(box,unit)]))
        certificates.append({'name':name,'box':json_native(box),'degrees':list(degrees),
                             'positive_scale':str(scale1 if name=='small radius' else scale2),
                             'primitive_polynomial':encode(poly),
                             'Bernstein_coefficients':[[*index,str(c)] for index,c in sorted(coefficients.items())]})
    records['two complete positivity boxes']=certificates
    # A genuine five-level path approaching the triple collision. This proves
    # sharpness by an exact rational limit, rather than assuming continuity.
    epsilon=MP.variable(1)
    path_values=[-6*t*t-epsilon**2,-8*t**3+2*t*epsilon**2,
                 -3*t**4+3*t*t*epsilon**2]
    path_n,path_d=[divide_variable(substitute(k[key],path_values),1,2) for key in ['n','d']]
    leading_n,leading_d=[MP({index:c for index,c in poly.d.items() if index[1]==0})
                         for poly in [path_n,path_d]]
    check('sharp path leading numerator',leading_n==2654208*t**6*(t+2)**6*(3*t-2)**2)
    check('sharp path leading denominator',leading_d==331776*t**6*(t+2)**4*dt)
    check('sharp genuine-five-level limit',leading_n*dt==leading_d*nt)
    records['sharp path']='delta=(t+epsilon,t-epsilon,t,-3t); n,d vanish to order2 in epsilon'
    # Full eight-coordinate commutant pinching controls do not use active roots.
    controls=[]
    for deviation,expected,genuine in [
        ([Q(-3),Q(-1),Q(1),Q(3)],Q(26085736,10566307),True),
        ([Q(-3,2),Q(-1,2),Q(1,2),Q(3,2)],Q(15899372,3686489),True),
        ([Q(-1),Q(-1,3),Q(1,3),Q(1)],Q(10129144,1338153),True),
        ([Q(11,64)]*3+[Q(-33,64)],Q(27899524,1137183),False),
        ([Q(-11,64)]*3+[Q(33,64)],None,False),
        ([Q(2,3)]*3+[Q(-2)],Q(0),False)]:
        point=invariants(deviation);profile=[Q(-1)]*4+[1+x for x in deviation]
        N=sum(x*x for x in profile);S3=sum(x**3 for x in profile)
        m2=sum(x**4 for x in profile)-N*N/8
        check('literal N '+str(len(controls)),evaluate(k['N'],point),N)
        check('literal S3 '+str(len(controls)),evaluate(k['S3'],point),S3)
        check('literal m2 '+str(len(controls)),evaluate(k['m2'],point),m2)
        mass_square=full_pinching(profile);actual=(N*N-mass_square)/m2
        if expected is not None:check('literal full pinching C '+str(len(controls)),actual,expected)
        rn,rd=[evaluate(r[key],point) for key in ['n','d']]
        check('literal positive relaxation denominator '+str(len(controls)),rd>0)
        check('literal Bessel upper bound '+str(len(controls)),actual<=rn/rd)
        if genuine:
            qn,qd=[evaluate(k[key],point) for key in ['n','d']]
            check('literal full-quartic denominator '+str(len(controls)),qd>0)
            check('literal four-moment/full-matrix equality '+str(len(controls)),qn/qd,actual)
        else:check('literal triple endpoint exactness '+str(len(controls)),rn/rd,actual)
        controls.append({'deviations':list(map(str,deviation)),'N':str(N),'C':str(actual),
                         'Bessel_upper':str(rn/rd),'genuine_five_levels':genuine,
                         'full_matrix_control':True})
    records['six independent full-coordinate controls']=controls
    check('retained singleton zero',Q(0) in [1+x for x in [Q(-1),Q(-1,3),Q(1,3),Q(1)]])
    check('retained negative singleton',Q(-1,2) in [1+x for x in [Q(-3,2),Q(-1,2),Q(1,2),Q(3,2)]])
    check('sharp witness exceeds49over2',Q(27899524,1137183)>Q(49,2))
    # Exact obstruction to the discarded coefficient-convexity shortcut.
    q=specialize_D(k['gradients'][2],Q(-1),Q(0))
    box=(Q(1029,10000),Q(103,1000))
    check('D stationary unique root',count(sturm(q),*box),1)
    check('D maximum crossing',pe(q,box[0])>0 and pe(q,box[1])<0)
    curvature=ivpoly(pd(q),box)
    check('D stationary negative curvature',curvature[1]<0)
    ns,ds=[specialize_D(k[key],Q(-1),Q(0)) for key in ['n','d']]
    margin=ivpoly(pa(ps(ds,Q(9)),ps(ns,-1)),box)
    check('D stationary maximum below9',margin[0]>0)
    records['discarded-convexity obstruction']={'A':'-1','B':'0','D_interval':json_native(box),
             'primitive_D_gradient':json_native(q),'q_prime_interval':json_native(curvature),
             '9d-n_interval':json_native(margin),'N':'10','C_less_than':'9'}
    # Mathematical corruption controls, all explicit guards survive python -O.
    check('damage: altered active quartic fails derivative',
          zpm(zpow([MP(1),MP(1)],3),[k['h'][0]+1]+k['h'][1:])!=
          [Q(j,8)*k['f'][j] for j in range(1,len(k['f']))])
    check('damage: omitted D in mass moment is false',k['m2']!=3*A*A/2-8*A+12*B)
    check('damage: wrong SOS matching factor is false',ae*ae+12*de!=2*matching)
    check('damage: false49over2 universal bound rejected',
          Q(49,2)-Q(controls[3]['C'])<0)
    records['recorded_checks']=checks;records['mathematical_damage_controls']=4
    return json_native(records)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit',action='store_true',help='emit regenerated exact records after all proof checks')
    parser.add_argument('--expected',type=Path,default=Path(__file__).with_name('expected.json'))
    args=parser.parse_args();start=time.monotonic();records=verify()
    canonical=json.dumps(records,sort_keys=True,separators=(',',':')).encode()
    digest=hashlib.sha256(canonical).hexdigest()
    if args.emit:print(json.dumps(records,indent=2));return
    require(records==json.loads(args.expected.read_text()),'regenerated mathematical fixture mismatch')
    print(json.dumps({'status':'PASS','recorded_checks':records['recorded_checks'],
                     'mathematical_damage_controls':4,'full_matrix_controls':6,
                     'Bernstein_coefficients':225,'record_sha256':digest,
                     'elapsed_seconds':round(time.monotonic()-start,4)}))


if __name__=='__main__':main()
