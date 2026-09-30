#!/usr/bin/env python3
"""Whole five-level degree-nine displacement bound, exact author certificate.
Actual author six-sendov-2, researcher. Standard library and exact rational
arithmetic; no private imports or numerical proof inputs. The kernel
openly adapts the author's preceding five-level/four-level sources.
Written moment, section and collision bridges are outside a formal kernel.
Independent review of this extension is pending.
"""
from fractions import Fraction as F
from itertools import product, combinations, combinations_with_replacement
from math import comb
from pathlib import Path
import argparse, hashlib, json

CHECKS=0
def require(ok, message):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise ValueError(message)

class P:
    """Sparse exact Q[x0,x1,x2]; exponent order is explicit and fixed."""
    def __init__(self, value=0):
        if isinstance(value, P):
            value = value.t
        if isinstance(value, (int, F)):
            value = {(0, 0, 0): F(value)}
        self.t = {tuple(e): F(c) for e, c in value.items() if c}
        if any(len(e) != 3 or any(k < 0 for k in e) for e in self.t):
            raise ValueError('invalid polynomial exponent')

    def __add__(self, other):
        out = dict(self.t)
        for e, c in P(other).t.items():
            out[e] = out.get(e, F(0)) + c
        return P(out)

    __radd__ = __add__

    def __neg__(self):
        return P({e: -c for e, c in self.t.items()})

    def __sub__(self, other):
        return self + -P(other)

    def __rsub__(self, other):
        return P(other) + -self

    def __mul__(self, other):
        out = {}
        for e, c in self.t.items():
            for h, b in P(other).t.items():
                k = tuple(x+y for x, y in zip(e, h))
                out[k] = out.get(k, F(0)) + c*b
        return P(out)

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        return self * (1/F(scalar))

    def __pow__(self, n):
        if n < 0:
            raise ValueError('negative polynomial power')
        out, a = P(1), self
        while n:
            if n & 1:
                out *= a
            a *= a
            n //= 2
        return out

    def __eq__(self, other):
        return self.t == P(other).t

    def dump(self):
        return [[*e, str(c)] for e, c in sorted(self.t.items())]

def subst(poly, variables):
    powers = []
    for axis, v in enumerate(variables):
        degree = max((e[axis] for e in poly.t), default=0)
        row = [P(1)]
        for _ in range(degree):
            row.append(row[-1]*P(v))
        powers.append(row)
    out = P(0)
    for e, c in poly.t.items():
        term = P(c)
        for axis, k in enumerate(e):
            term *= powers[axis][k]
        out += term
    return out

def scalar(poly, values):
    out = subst(poly, values)
    require(not any(any(e) for e in out.t), 'evaluation is scalar')
    return out.t.get((0, 0, 0), F(0))

def prod(values):
    out = P(1)
    for v in values:
        out *= v
    return out

def affine_power(poly, box):
    """Binomial affine substitution performed one axis at a time."""
    data = dict(poly.t)
    for axis, (a, b) in enumerate(box):
        out = {}
        for e, c in data.items():
            for k in range(e[axis]+1):
                h = tuple(k if i == axis else v for i, v in enumerate(e))
                out[h] = out.get(h, F(0)) + c*comb(e[axis], k)*a**(e[axis]-k)*(b-a)**k
        data = {e: c for e, c in out.items() if c}
    return data

def bernstein(poly, box):
    degrees = tuple(max((e[i] for e in poly.t), default=0) for i in range(3))
    normalized = affine_power(poly, box)
    data = dict(normalized)
    for axis, degree in enumerate(degrees):
        out = {}
        for e, c in data.items():
            for k in range(e[axis], degree+1):
                h = tuple(k if i == axis else v for i, v in enumerate(e))
                out[h] = out.get(h, F(0)) + c*F(comb(k, e[axis]), comb(degree, e[axis]))
        data = {e: c for e, c in out.items() if c}
    indices = list(product(*(range(n+1) for n in degrees)))
    coefficients = [data.get(e, F(0)) for e in indices]
    # Independent inverse basis identity in the normalized power coordinates.
    inverse = dict(data)
    for axis, degree in enumerate(degrees):
        out = {}
        for e, c in inverse.items():
            for k in range(e[axis], degree+1):
                h = tuple(k if i == axis else v for i, v in enumerate(e))
                out[h] = out.get(h, F(0)) + c*comb(degree, k)*comb(k, e[axis])*(-1)**(k-e[axis])
        inverse = {e: c for e, c in out.items() if c}
    require(inverse == normalized, 'complete inverse Bernstein reconstruction')
    return coefficients, degrees

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def certificate(name, poly, box, strict=False):
    require(len(box) == 3 and all(a < b for a, b in box), name+' genuine box')
    coefficients, degrees = bernstein(poly, box)
    for value in coefficients:
        require(value > 0 if strict else value >= 0, name+' Bernstein sign')
    return {'name': name, 'box': [[str(a), str(b)] for a, b in box],
            'degrees': list(degrees), 'entries': len(coefficients),
            'zero': sum(c == 0 for c in coefficients), 'minimum': str(min(coefficients)),
            'polynomial_sha256': digest(poly.dump()),
            'coefficient_sha256': digest(list(map(str, coefficients)))}

def solve(a, b):
    n = len(b)
    a = [list(r)+[v] for r, v in zip(a, b)]
    for j in range(n):
        pivots = [i for i in range(j, n) if a[i][j]]
        require(bool(pivots), 'nonzero Gaussian pivot')
        i = pivots[0]
        a[j], a[i] = a[i], a[j]
        t = a[j][j]
        a[j] = [v/t for v in a[j]]
        for i in range(j+1, n):
            t = a[i][j]
            if t:
                a[i] = [u-t*v for u, v in zip(a[i], a[j])]
    out = [F(0)]*n
    for j in range(n-1, -1, -1):
        out[j] = a[j][-1]-sum(a[j][k]*out[k] for k in range(j+1, n))
    return out

def independent_rows(rows):
    pivots, selected = {}, []
    for original in rows:
        r = list(original)
        for j, b in sorted(pivots.items()):
            t = r[j]
            if t:
                r = [u-t*v for u, v in zip(r, b)]
        if any(r):
            j = next(j for j, v in enumerate(r) if v)
            t = r[j]
            pivots[j] = [v/t for v in r]
            selected.append(original)
    return selected

def pinching(theta):
    """Rational Frobenius projection of ww* to the symmetric commutant."""
    n = 8
    require(len(theta) == n and sum(theta) == 0, 'balanced definition control')
    a = [[(theta[i] if i == j else 0)-(theta[i]+theta[j])/n
          for j in range(n)] for i in range(n)]
    pairs = list(combinations_with_replacement(range(n), 2))
    weights = [F(1 if i == j else 2) for i, j in pairs]
    w = [theta[i]*theta[j]/n for i, j in pairs]
    all_rows = []
    for i in range(n):
        for j in range(i+1, n):
            row = []
            for h, k in pairs:
                v = (a[i][h] if k == j else 0)-(a[k][j] if i == h else 0)
                if h != k:
                    v += (a[i][k] if h == j else 0)-(a[h][j] if i == k else 0)
                row.append(v)
            all_rows.append(row)
    rows = independent_rows(all_rows)
    rhs = [sum(c*v for c, v in zip(row, w)) for row in rows]
    gram = [[sum(c*d/g for c, d, g in zip(row, other, weights))
             for other in rows] for row in rows]
    lam = solve(gram, rhs)
    projected = [v-sum(row[k]*b for row, b in zip(rows, lam))/weights[k]
                 for k, v in enumerate(w)]
    for row in all_rows:
        require(sum(c*v for c, v in zip(row, projected)) == 0,
                'original commutation constraint')
    residual = [u-v for u, v in zip(w, projected)]
    require(sum(g*u*v for g, u, v in zip(weights, projected, residual)) == 0,
            'Frobenius orthogonality')
    return sum(g*v*v for g, v in zip(weights, projected)), len(rows)


X,Y,Z=[P({tuple(int(i==j) for j in range(3)):1}) for i in range(3)]

def mm(a,b):
    n=len(a)
    return [[sum((a[i][h]*b[h][j] for h in range(n)),P(0))
             for j in range(n)] for i in range(n)]

def ms(a,c):return [[v*c for v in row] for row in a]
def ma(a,b):return [[u+v for u,v in zip(row,other)] for row,other in zip(a,b)]
def mt(a):return sum((a[i][i] for i in range(len(a))),P(0))

def trace_word_coefficients(degree):
    result={}
    for mask in range(1<<degree):
        positions=[i for i in range(degree) if mask>>i&1]
        if not positions:key=(degree,);coefficient=F(1)
        else:
            gaps=[(positions[(i+1)%len(positions)]-p)%degree or degree
                  for i,p in enumerate(positions)]
            key=tuple(sorted(gaps));coefficient=F((-1)**len(positions),8**len(positions))
        result[key]=result.get(key,F(0))+coefficient
    return result

def det(a):
 n=len(a)
 if n==1:return a[0][0]
 if n==2:return a[0][0]*a[1][1]-a[0][1]*a[1][0]
 out=P(0)
 for j in range(n):
  sub=[[a[i][h] for h in range(n) if h!=j] for i in range(1,n)]
  out+=(-1)**j*a[0][j]*det(sub)
 return out

def adj(a):
 n=len(a);out=[[P(0) for j in range(n)] for i in range(n)]
 for i in range(n):
  for j in range(i,n):
   sub=[[a[r][c] for c in range(n) if c!=i] for r in range(n) if r!=j]
   out[i][j]=(-1)**(i+j)*det(sub);out[j][i]=out[i][j]
 return out

def pmul(a,b):
 out=[P(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):out[i+j]+=x*y
 return out

def roots_poly(roots):
 out=[P(1)]
 for root in roots:out=pmul(out,[-root,P(1)])
 return out

def raw_cases():
 return {'triple':([3,2,1,1,1],[P(-1),X,Y,Z,3-2*X-Y-Z]),
         'double':([2,3,1,1,1],[P(-1),X,Y,Z,2-3*X-Y-Z]),
         'singleton':([1,3,2,1,1],[P(-1),X,Y,Z,1-3*X-2*Y-Z])}

def trace_moments(masses,levels):
 mu=[P(8)]+[sum((m*t**r for m,t in zip(masses,levels)),P(0)) for r in range(1,7)]
 require(mu[1]==0,'balance')
 full=[P(7)]
 for r in range(1,7):
  full.append(sum((c*prod(mu[j] for j in word) for word,c in trace_word_coefficients(r).items()),P(0)))
 active=[P(4)]+[full[r]-sum(((m-1)*t**r for m,t in zip(masses,levels)),P(0)) for r in range(1,7)]
 return mu,full,active

def derive(masses,levels,full_control=False):
 mu,full,s=trace_moments(masses,levels)
 q=[P(0)]*5
 for i,m in enumerate(masses):
  g=roots_poly([t for j,t in enumerate(levels) if j!=i])
  q=[a+m*b for a,b in zip(q,g)]
 require(q[-1]==8,'quartic leading8')
 rr=roots_poly([t for m,t in zip(masses,levels) for _ in range(m-1)])
 hh=roots_poly([t for m,t in zip(masses,levels) for _ in range(m)])
 require(pmul(rr,q)==[(i+1)*hh[i+1] for i in range(8)],'full characteristic derivative factorization')
 # Independent Newton recurrence from the derivative-factor quartic.
 coefficients=[a/8 for a in q]
 for r in range(1,7):
  if r<=4:
   total=s[r]+sum((coefficients[4-i]*s[r-i] for i in range(1,r)),P(0))+r*coefficients[4-r]
  else:total=sum((coefficients[4-i]*s[r-i] for i in range(5)),P(0))
  require(total==0,'active trace Newton recurrence '+str(r))
 gg=[[s[i+j] for j in range(4)] for i in range(4)]
 bb=[mu[2]/8,mu[3]/8,mu[4]/8-mu[2]**2/64,mu[5]/8-mu[2]*mu[3]/32]
 aa=adj(gg)
 dd=sum((gg[0][j]*aa[j][0] for j in range(4)),P(0))
 nn=sum((bb[i]*aa[i][j]*bb[j]*(1 if i==j else 2) for i in range(4) for j in range(i,4)),P(0))
 bound=(786*mu[2]-122*mu[2]**2-224*mu[4])*dd+5760*nn
 if full_control:
  theta=[t for m,t in zip(masses,levels) for _ in range(m)]
  cc=[[(theta[i] if i==j else P(0))-(theta[i]+theta[j])/8 for j in range(8)] for i in range(8)]
  ww=[[theta[i]*theta[j]/8 for j in range(8)] for i in range(8)]
  power=[[P(int(i==j)) for j in range(8)] for i in range(8)]
  for r in range(7):
   if r:power=mm(power,cc)
   if r:require(mt(power)==full[r],'full8x8 trace '+str(r))
   if r<=3:require(mt(mm(ww,power))==bb[r],'full8x8 b'+str(r))
  # All adjugate identities, through a separate full multiplication.
  product=mm(gg,aa)
  require(product==[[dd if i==j else P(0) for j in range(4)] for i in range(4)],'full polynomial Gram adjugate identity')
 return {'masses':masses,'levels':[p.dump() for p in levels],
         'mu2':mu[2].dump(),'mu4':mu[4].dump(),'Q':[p.dump() for p in q],
         'active_traces':[p.dump() for p in s],'b':[p.dump() for p in bb],
         'detG':dd.dump(),'N':nn.dump(),'bound786':bound.dump()}

def load(poly):return P({tuple(row[:3]):F(row[3]) for row in poly})

def definition_controls(name,row):
 m,levels=raw_cases()[name]
 points={'triple':[(F(3,4),F(2,3),F(5,6)),(F(1),F(3,10),F(-3,10)),(F(0),F(1),F(1))],
         'double':[(F(3,4),F(-1,2),F(1,3)),(F(1),F(3,10),F(-3,10)),(F(1,3),F(1,3),F(1,3))],
         'singleton':[(F(1,2),F(-1,3),F(1,4)),(F(1),F(-1),F(3,10)),(F(-1),F(1),F(1))]}[name]
 out=[]
 for point in points:
  ts=[scalar(t,point) for t in levels]
  require(max(map(abs,ts))<=1,'feasible control')
  theta=[t for a,t in zip(m,ts) for _ in range(a)]
  psi,rank=pinching(theta)
  d=scalar(load(row['detG']),point);n=scalar(load(row['N']),point)
  require(n==psi*d,'moment quotient versus full defining pinching')
  require(d>=0,'Gram determinant nonnegative')
  jj=122*sum(t*t for t in theta)+(224*sum(t**4 for t in theta)-5760*psi)/sum(t*t for t in theta)
  out.append({'point':list(map(str,point)),'levels':list(map(str,ts)),'Psi':str(psi),'J':str(jj),'detG':str(d),'quotient_defined':bool(d),'commutant_rank':rank})
 return out

def horner(poly,variables):
 def visit(data,axis):
  if not data:return P(0)
  if axis<0:
   require(set(data)=={(0,0,0)},'Horner coefficient scalar')
   return P(data[(0,0,0)])
  grouped={}
  for e,value in data.items():
   h=tuple(0 if i==axis else power for i,power in enumerate(e))
   grouped.setdefault(e[axis],{})[h]=value
  out=P(0)
  for power in range(max(grouped),-1,-1):
   out=out*variables[axis]+visit(grouped.get(power,{}),axis-1)
  return out
 return visit(poly.t,2)

def charts():
 # Sorted three singleton deficits, radial from their equal point.
 s=2*X;c=s/3
 beta=[c*(1-Y),c*(1-Y)+s*Y*Z/2,c*(1-Y)+s*Y*(1-Z/2)]
 yield 'triple','triple',[P(-1),X,*[1-b for b in beta]],[(0,2),(1,2)]
 yield 'double0','double',[P(-1),(s-1)/3,*[1-b for b in beta]],[(0,2),(1,2)]
 s=2+2*X;c=s/3
 beta=[c*(1-Y)+X*Y*(1-Z),c*(1-Y)+X*Y*(1+Z),c*(1-Y)+2*Y]
 yield 'double1','double',[P(-1),(s-1)/3,*[1-b for b in beta]],[(1,2)]
 beta=[c*(1-Y),c*(1-Y)+Y*(2*X*(1-Z)+(1+X)*Z),c*(1-Y)+Y*(2*(1-Z)+(1+X)*Z)]
 yield 'double2','double',[P(-1),(s-1)/3,*[1-b for b in beta]],[(1,2)]
 q=-1+2*X;a=(q-2+4*Y)/3;b=1-2*Y
 yield 'singleton0','singleton',[P(-1),a,b,1-X+X*Z,1-X-X*Z],[]
 q=3-2*X;a=(1-2*X+(2+2*X)*Y)/3;b=1-(1+X)*Y
 yield 'singleton1','singleton',[P(-1),a,b,-1+X*(1+Z),-1+X*(1-Z)],[(0,2)]

def remove(poly,factors):
 result=poly
 for axis,power in factors:
  require(all(e[axis]>=power for e in result.t),'exact radial/collision factor')
  reduced=P({tuple(n-power if i==axis else n for i,n in enumerate(e)):c for e,c in result.t.items()})
  require(reduced*(X,Y,Z)[axis]**power==result,'factor multiplication back')
  result=reduced
 return result

LABELS={'gram4':'bound','gram3':'bound3','moment':'moment'}

def needed(tree,depth=0):
 require(depth<=24,"bounded tree before computation")
 if isinstance(tree,str):
  require(tree in LABELS,'known terminal proof');return {LABELS[tree]}
 require(isinstance(tree,list) and len(tree)==3 and type(tree[0]) is int and tree[0] in (0,1,2),'both closed cube children')
 return needed(tree[1],depth+1)|needed(tree[2],depth+1)

def split(coefficients,degrees,axis):
 strides=((degrees[1]+1)*(degrees[2]+1),degrees[2]+1,1)
 left=[F(0)]*len(coefficients);right=[F(0)]*len(coefficients)
 other=[i for i in range(3) if i!=axis]
 for pair in product(*(range(degrees[i]+1) for i in other)):
  base=sum(x*strides[i] for i,x in zip(other,pair))
  indices=[base+j*strides[axis] for j in range(degrees[axis]+1)]
  row=[coefficients[j] for j in indices];n=degrees[axis]
  left[indices[0]]=row[0];right[indices[n]]=row[n]
  for level in range(1,n+1):
   row=[(a+b)/2 for a,b in zip(row,row[1:])]
   left[indices[level]]=row[0];right[indices[n-level]]=row[-1]
 return left,right


def minorant3(row):
    ss=[load(p) for p in row['active_traces']]
    bb=[load(p) for p in row['b'][:3]]
    hh=[[ss[i+j] for j in range(3)] for i in range(3)]
    aa=adj(hh);dd=det(hh)
    nn=sum((bb[i]*aa[i][j]*bb[j] for i in range(3) for j in range(3)),P(0))
    mu2,mu4=load(row['mu2']),load(row['mu4'])
    require(mm(hh,aa)==[[dd if i==j else P(0) for j in range(3)] for i in range(3)],
            'three-moment full adjugate identity')
    bound=(786*mu2-122*mu2**2-224*mu4)*dd+5760*nn
    for control in row['definition_controls']:
        point=list(map(F,control['point']))
        d,n=scalar(dd,point),scalar(nn,point)
        require(d>=0 and n<=F(control['Psi'])*d,'three-moment defining pinching control')
    return dd,nn,bound

def triangle_coordinates(beta,vertices):
    a,b,c=vertices
    x1,y1=b[0]-a[0],b[1]-a[1]
    x2,y2=c[0]-a[0],c[1]-a[1]
    area=x1*y2-y1*x2
    if not area:return None
    px,py=beta[0]-a[0],beta[1]-a[1]
    u=(px*y2-py*x2)/area;v=(x1*py-y1*px)/area
    if u<0 or v<0 or u+v>1:return None
    total=u+v
    return total,v/total if total else F(0)

def reverse_chart(kind,levels):
    require(levels[0]==-1,'saturated inverse label')
    if kind in ('triple','double'):
        heavy=levels[1]
        beta=sorted(1-t for t in levels[2:])
        total=2*heavy if kind=='triple' else 1+3*heavy
        center=(total/3,)*3
        aa=(F(0),F(0),total);bb=(F(0),total/2,total/2)
        if kind=='triple' or total<=2:
            result=triangle_coordinates(beta,(center,aa,bb)) if total else (F(0),F(0))
            require(result is not None,'low deficit triangle inverse')
            return ('triple' if kind=='triple' else 'double0'),(heavy if kind=='triple' else total/2,*result)
        dd=((total-2)/2,(total-2)/2,F(2));ee=(F(0),total-2,F(2))
        for name,vertices in (('double1',(center,dd,ee)),('double2',(center,ee,bb))):
            result=triangle_coordinates(beta,vertices)
            if result is not None:return name,((total-2)/2,*result)
        raise ValueError('whole clipped polygon inverse')
    require(kind=='singleton','known inverse kind')
    a,b=levels[1:3];c,d=sorted(levels[3:],reverse=True)
    q=3*a+2*b;v=(c-d)/2
    if q<=1:
        x=(q+1)/2;y=(3*a-q+2)/4
        return 'singleton0',(x,y,v/x if x else F(0))
    x=(3-q)/2;y=(3*a-q+2)/(5-q)
    return 'singleton1',(x,y,v/x if x else F(0))

def subdivision_controls():
    count=0
    # Every Bernstein monomial basis input, on each tensor axis.
    for degree in (0,1,2,10,14,16):
        for power in range(degree+1):
            parent=[F(comb(j,power),comb(degree,power)) if j>=power else F(0)
                    for j in range(degree+1)]
            expected_left=[v/2**power for v in parent]
            expected_right=[sum((F(comb(power,h)*comb(j,h),comb(degree,h)*2**power)
                                 for h in range(min(j,power)+1)),F(0))
                            for j in range(degree+1)]
            for axis in range(3):
                degrees=tuple(degree if i==axis else 0 for i in range(3))
                left,right=split(parent,degrees,axis)
                require(left==expected_left and right==expected_right,
                        'universal midpoint subdivision basis identity')
                count+=1
    return count

def build(data):
    initial_checks=CHECKS
    require(isinstance(data,dict) and set(data)=={'format','cases'} and
            data['format']=='closed-six-cube-bisection-trees-v1','exact cover schema')
    require(isinstance(data['cases'],list),'cover cases')
    lookup={}
    for row in data['cases']:
        require(isinstance(row,dict) and set(row)=={'chart','tree'} and isinstance(row['chart'],str),
                'only chart names and full bisection trees')
        require(row['chart'] not in lookup,'no repeated cube')
        needed(row['tree']);lookup[row['chart']]=row['tree']
    chart_map={name:(kind,levels,factors) for name,kind,levels,factors in charts()}
    require(set(lookup)==set(chart_map) and len(chart_map)==6,'every saturation and section cube required')
    require({tuple(sorted(p,reverse=True)) for p in combinations_with_replacement(range(1,9),5) if sum(p)==8}
            =={(4,1,1,1,1),(3,2,1,1,1),(2,2,2,1,1)},'all five-part partitions')
    basis_controls=subdivision_controls()
    raw={};symbolic={};three={}
    for kind,(m,levels) in raw_cases().items():
        row=derive(m,levels,full_control=kind=='triple')
        row['definition_controls']=definition_controls(kind,row)
        raw[kind]=row;three[kind]=minorant3(row)
        symbolic[kind]={'masses':m,'polynomial_sha256':{key:digest(row[key]) for key in
                         ('levels','mu2','mu4','Q','active_traces','b','detG','N','bound786')},
                        'terms':{key:len(row[key]) for key in ('detG','N','bound786')},
                        'three_moment_sha256':[digest(p.dump()) for p in three[kind]],
                        'definition_controls':row['definition_controls']}
    unit=[(F(0),F(1))]*3
    output=[];cache={};controls=[];profile_refs=[]
    domain_entries=0;sign_entries=0;leaf_count=0;round_trips=0;direct_count=0
    types={'gram4':0,'gram3':0,'moment':0}
    def profile(theta,label):
        key=tuple(sorted(theta))
        require(sum(key)==0 and max(map(abs,key))==1,'definition-level normalization')
        if key not in cache:
            psi,rank=pinching(key);mu2=sum(t*t for t in key);mu4=sum(t**4 for t in key)
            jj=122*mu2+(224*mu4-5760*psi)/mu2
            require(jj<=786,'definition-level bound control')
            cache[key]=len(controls)
            controls.append({'label':label,'theta':list(map(str,key)),'Psi':str(psi),
                             'J':str(jj),'commutant_rank':rank})
        return cache[key],F(controls[cache[key]]['Psi'])
    for name,kind,levels,factors in charts():
        m,_=raw_cases()[kind];row=raw[kind]
        require(sum((a*t for a,t in zip(m,levels)),P(0))==0,name+' mapped balance')
        require([horner(t,levels[1:4]) for t in raw_cases()[kind][1]]==levels,
                name+' exact raw-chart substitution')
        require(all((levels[i]-levels[j]).t for i in range(5) for j in range(i+1,5)),
                name+' generic distinct labels dense')
        physical=[1+sign*t for t in levels for sign in (-1,1)]
        physical.extend(levels[i]-levels[i+1] for i in ([2,3] if kind!='singleton' else [3]))
        for poly in physical:
            values,_=bernstein(poly,unit)
            for value in values:require(value>=0,name+' physical/order Bernstein sign')
            domain_entries+=len(values)
        full=horner(load(row['bound786']),levels[1:4])
        gram4=remove(full,factors)
        denominator=remove(horner(load(row['detG']),levels[1:4]),factors)
        gram3=horner(three[kind][2],levels[1:4])
        mu2=sum((a*t*t for a,t in zip(m,levels)),P(0))
        polynomials={'bound':gram4,'bound3':gram3,'moment':1124-199*mu2}
        masters={key:bernstein(polynomials[key],unit) for key in needed(lookup[name])}
        records=[];direct_done=set()
        def walk(tree,box,values,depth=0):
            nonlocal direct_count
            require(depth<=24,name+' bounded tree')
            if isinstance(tree,str):
                key=LABELS[tree];cs,degrees=values[key]
                for value in cs:require(value>=0,name+' exact continuous leaf sign')
                if key not in direct_done:
                    direct,dd=bernstein(polynomials[key],box)
                    require(direct==cs and dd==degrees,name+' full direct affine leaf reconstruction')
                    direct_done.add(key);direct_count+=1
                records.append({'type':tree,'box':[[str(a),str(b)] for a,b in box],
                                'entries':len(cs),'minimum':str(min(cs)),
                                'coefficient_sha256':digest(list(map(str,cs)))})
                return prod_fraction(b-a for a,b in box)
            axis,lefttree,righttree=tree
            lo,hi=box[axis];mid=(lo+hi)/2
            split_values={key:split(cs,degrees,axis) for key,(cs,degrees) in values.items()}
            volume=F(0)
            for side,child,pair in ((0,lefttree,(lo,mid)),(1,righttree,(mid,hi))):
                childbox=list(box);childbox[axis]=pair
                childvalues={key:(split_values[key][side],values[key][1]) for key in needed(child)}
                volume+=walk(child,childbox,childvalues,depth+1)
            require(volume==prod_fraction(b-a for a,b in box),name+' both entire closed children')
            return volume
        require(walk(lookup[name],unit,masters)==1,name+' entire closed cube')
        sign_entries+=sum(v['entries'] for v in records);leaf_count+=len(records)
        for record in records:types[record['type']]+=1
        output.append({'chart':name,'kind':kind,'masses':m,'factors':[list(v) for v in factors],
                       'polynomial_sha256':{key:digest(p.dump()) for key,p in polynomials.items()},
                       'denominator_reduced_sha256':digest(denominator.dump()),
                       'certificates':records,'direct_controls':sorted(direct_done)})
        points=list(product((F(0),F(1)),repeat=3))+[(F(1,2),)*3,(F(2,3),F(1,4),F(3,5))]
        for index,point in enumerate(points):
            actual=[scalar(t,point) for t in levels]
            theta=[t for a,t in zip(m,actual) for _ in range(a)]
            ref,psi=profile(theta,name+' point'+str(index))
            inverse_name,inverse=reverse_chart(kind,actual)
            require(all(0<=t<=1 for t in inverse),name+' full closed inverse coordinates')
            inverse_levels=chart_map[inverse_name][1]
            inverse_theta=sorted(t for a,p in zip(m,inverse_levels) for t in [scalar(p,inverse)]*a)
            require(inverse_theta==sorted(theta),name+' closed inverse including degenerate faces')
            round_trips+=1
            profile_refs.append({'chart':name,'point':list(map(str,point)),'definition_control':ref,
                                 'inverse_chart':inverse_name,'inverse_point':list(map(str,inverse))})
    require(sign_entries==59671 and leaf_count==49,'complete sign/leaf totals')
    require(types=={'gram4':10,'gram3':17,'moment':22},'all three certificate mechanisms')
    require(F(106496,5*786)==F(53248,1965),'five-phase lower-basin normalization')
    return {'author':'six-sendov-2','role':'researcher','proof_status':'ordinary author proof and exact continuous certificates; independent review pending',
            'remaining_class_bound':'3+2+1+1+1: J<=786; exact maximum not established',
            'whole_five_level_bound':'J<=786, using the credited two-cohort reduction',
            'five_phase_basin_liminf_lower_bound':'53248/1965',
            'symbolic':symbolic,'charts':output,'sign_entries':sign_entries,
            'physical_order_sign_entries':domain_entries,'closed_leaves':leaf_count,'leaf_types':types,
            'universal_subdivision_controls':basis_controls,'direct_affine_leaf_controls':direct_count,
            'full_compression_controls':controls,'profile_references':profile_refs,
            'inverse_round_trips':round_trips,'checks':CHECKS-initial_checks}

def prod_fraction(values):
    out=F(1)
    for v in values:out*=v
    return out

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cover',type=Path,default=Path(__file__).with_name('cover.json'))
    parser.add_argument('--manifest',type=Path,default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--write-manifest',action='store_true',help='author regeneration only')
    args=parser.parse_args()
    require(args.cover.is_file(),'required complete cover absent')
    if not args.write_manifest:require(args.manifest.is_file(),'required regression manifest absent')
    result=build(json.loads(args.cover.read_text()))
    if args.write_manifest:args.manifest.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    else:require(result==json.loads(args.manifest.read_text()),'complete exact record equality')
    print(json.dumps({'status':'PASS','checks':CHECKS,'sign_entries':result['sign_entries'],
                      'physical_order_sign_entries':result['physical_order_sign_entries'],
                      'closed_leaves':result['closed_leaves'],'leaf_types':result['leaf_types'],
                      'full_compression_controls':len(result['full_compression_controls']),
                      'inverse_round_trips':result['inverse_round_trips'],
                      'canonical_record_sha256':digest(result)},sort_keys=True))
if __name__=='__main__':main()
