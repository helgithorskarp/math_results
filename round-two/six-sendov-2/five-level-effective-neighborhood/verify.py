#!/usr/bin/env python3
"""Exact complementary angular collars and effective five-level neighborhood.
Actual author six-sendov-2, researcher. Rational transport/full8 utilities
adapt own 9121 source 504c910d39dfae34f8e4711937f5ad050030056d and prior
9019, corrected at 5341085889659547fc1ad953a6adcda071231173.
The known c3/orbit credit 8753/8806; the inherited branch curvature credits
9121. The whole five-level neighborhood corollary also uses 9019/9055.
No runtime campaign imports, CAS or mathematical floating point.
"""
from __future__ import annotations
from fractions import Fraction as Q
from pathlib import Path
from math import comb,gcd,lcm
from itertools import permutations,product
import argparse,hashlib,json,time
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

def primitive_with_positive_scale(poly):
    denominator=lcm(*(v.denominator for v in poly.d.values()))
    content=gcd(*(int(v*denominator) for v in poly.d.values()))
    scale=Q(denominator,content)
    require(scale>0,'primitive scale must preserve sign')
    return poly*scale,scale

def add_z(p,q):
    out=[MP(0)]*max(len(p),len(q))
    for j,c in enumerate(p):out[j]+=c
    for j,c in enumerate(q):out[j]+=c
    return out

def scale_z(p,c):return [a*c for a in p]

def pairing(a,G,b):
    return sum((a[i]*G[i][j]*b[j] for i in range(len(a)) for j in range(len(b))),MP(0))

def axis_transform(coeffs,axis,matrix):
    groups={}
    for key,c in coeffs.items():
        other=key[:axis]+key[axis+1:];groups.setdefault(other,{})[key[axis]]=c
    result={}
    for other,row in groups.items():
        for i,weights in enumerate(matrix):
            total=sum((c*weights[j] for j,c in row.items()),Q(0))
            if total:result[other[:axis]+(i,)+other[axis:]]=total
    return result

def tensor_bernstein(poly,box):
    degrees=tuple(max(k[i] for k in poly.d) for i in range(3));coeffs=poly.d.copy()
    for axis,(lo,hi) in enumerate(box):
        d=degrees[axis]
        weights=[[sum((Q(comb(k,j))*lo**(k-j)*(hi-lo)**j*Q(comb(i,j),comb(d,j)) for j in range(min(i,k)+1)),Q(0)) for k in range(d+1)] for i in range(d+1)]
        coeffs=axis_transform(coeffs,axis,weights)
    return degrees,{key:coeffs.get(key,Q(0)) for key in product(*(range(d+1) for d in degrees))}

def reconstruct_tensor(degrees,coeffs):
    """Complete Bernstein-to-power transport, without using the forward matrices."""
    out={k:c for k,c in coeffs.items() if c}
    for axis,d in enumerate(degrees):
        matrix=[[Q(comb(d,i)*comb(d-i,j-i)*(-1)**(j-i)) if j>=i else Q(0) for i in range(d+1)] for j in range(d+1)]
        out=axis_transform(out,axis,matrix)
    return MP(out)

def record_hash(value):
    return hashlib.sha256(json.dumps(value,separators=(',',':'),sort_keys=True).encode()).hexdigest()

def summarize_polynomial(poly):
    return {'terms':len(poly.d),'degrees':[max(k[i] for k in poly.d) for i in range(3)],'coefficient_sha256':record_hash(encode(poly))}

def bernstein_record(poly,box,reconstruct=True):
    degrees,coeffs=tensor_bernstein(poly,box)
    if reconstruct:
        unit=[MP.variable(i) for i in range(3)]
        require(reconstruct_tensor(degrees,coeffs)==substitute(poly,[lo+(hi-lo)*v for v,(lo,hi) in zip(unit,box)]),'complete independent Bernstein basis reconstruction')
    values=list(coeffs.values());positives=[c for c in values if c>0]
    return {'degrees':list(degrees),'box':[[str(a),str(b)] for a,b in box],
            'coefficients':len(values),'negative':sum(c<0 for c in values),'zeros':sum(c==0 for c in values),
            'positive':len(positives),'minimum':str(min(values)),'minimum_positive':str(min(positives)) if positives else None,
            'coefficient_sha256':record_hash([list(k)+[str(c)] for k,c in sorted(coeffs.items())])}

class IP:
    """Sparse Z[A,s,t] arithmetic; dyadic denominators cleared structurally."""
    def __init__(self,value=0):
        if isinstance(value,IP):self.d=value.d;return
        if isinstance(value,dict):
            require(all(isinstance(c,int) for c in value.values()),'noninteger IP coefficient')
            self.d={k:c for k,c in value.items() if c}
        else:
            require(isinstance(value,int),'noninteger IP scalar')
            self.d={(0,0,0):value} if value else {}
    @staticmethod
    def variable(i):
        key=[0,0,0];key[i]=1;return IP({tuple(key):1})
    def __add__(self,other):
        out=self.d.copy()
        for k,c in IP(other).d.items():out[k]=out.get(k,0)+c
        return IP(out)
    __radd__=__add__
    def __neg__(self):return IP({k:-c for k,c in self.d.items()})
    def __sub__(self,other):return self+-IP(other)
    def __rsub__(self,other):return IP(other)+-self
    def __mul__(self,other):
        out={}
        for (i,j,k),c in self.d.items():
            for (a,b,d),v in IP(other).d.items():
                key=(i+a,j+b,k+d);out[key]=out.get(key,0)+c*v
        return IP(out)
    __rmul__=__mul__
    def __pow__(self,n):
        require(isinstance(n,int) and n>=0,'invalid IP exponent')
        result=IP(1)
        for _ in range(n):result*=self
        return result
    def __eq__(self,other):return self.d==IP(other).d
    def __bool__(self):return bool(self.d)

def izadd(p,q):
    out=[IP() for _ in range(max(len(p),len(q)))]
    for i,c in enumerate(p):out[i]+=c
    for i,c in enumerate(q):out[i]+=c
    return out

def izmul(p,q):
    out=[IP() for _ in range(len(p)+len(q)-1)]
    for i,c in enumerate(p):
        for j,d in enumerate(q):out[i+j]+=c*d
    return out

def izpow(p,n):
    result=[IP(1)]
    for _ in range(n):result=izmul(result,p)
    return result

def izscale(p,c):return [x*c for x in p]
def izderiv(p):return [i*p[i] for i in range(1,len(p))]

def inewton(poly,limit):
    n=len(poly)-1;require(poly[-1]==1,'integer Newton monicity')
    ps=[IP(n)]
    for k in range(1,limit+1):
        if k<=n:value=-k*poly[n-k]-sum((poly[n-j]*ps[k-j] for j in range(1,k)),IP())
        else:value=-sum((poly[n-j]*ps[k-j] for j in range(1,n+1)),IP())
        ps.append(value)
    return ps

def idet3(G):
    a,b,c=G[0];d,e,f=G[1];g,h,i=G[2]
    return a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)

def ideterminant(G):
    result=IP()
    for permutation in permutations(range(len(G))):
        term=IP((-1)**sum(permutation[i]>permutation[j] for i in range(len(G)) for j in range(i+1,len(G))))
        for i,j in enumerate(permutation):term*=G[i][j]
        result+=term
    return result

def irational(p):return MP(p.d)
def base_ip(p):return IP({k:c for k,c in p.d.items() if k[1:]==(0,0)})

def build_dual_kernel(chart):
    A,s,t=[IP.variable(i) for i in range(3)]
    R=[-A+s,IP(1)];L=[-1+t,IP(1)]
    if chart=='32111':
        profile=[A-s]*3+[1-t]*2+[A+3*s,1+2*t,-4*A-3]
        K=izmul(izmul([-A-3*s,IP(1)],[-1-2*t,IP(1)]),[4*A+3,IP(1)])
        f=izmul(izpow(R,3),izmul(izpow(L,2),K))
        factor=izmul(izpow(R,2),L)
        eight_h=izadd(izmul(izadd(izscale(L,3),izscale(R,2)),K),izmul(izmul(R,L),izderiv(K)))
        W=12*s*s+6*t*t
    elif chart=='22211':
        profile=[A-s]*2+[A+s]*2+[1-t]*2+[1+2*t,-4*A-3]
        M=[-A-s,IP(1)];factor=izmul(izmul(R,M),L)
        K=izmul([-1-2*t,IP(1)],[4*A+3,IP(1)])
        f=izmul(izpow(factor,2),K)
        eight_h=izadd(izscale(izmul(izderiv(factor),K),2),izmul(factor,izderiv(K)))
        W=4*s*s+6*t*t
    else:raise ValueError('unknown chart')
    require(izderiv(f)==izmul(factor,eight_h),'entire original derivative')
    require(len(eight_h)==5 and eight_h[-1]==8,'quartic degree and leading coefficient')
    # h8(z)=8^4*h(z/8) is monic and integral; its roots are8*lambda.
    h8=[eight_h[i]*8**(3-i) for i in range(4)]+[IP(1)]
    S=inewton(f,5)
    require(all(S[j]==sum((u**j for u in profile),IP()) for j in range(6)),'all six literal profile Newton moments')
    N,S3,S4,S5=S[2:6];N0=20*A*A+24*A+12
    require(S[1]==0 and N==N0+W,'balance and orthogonal raw variance')
    M2=8*S4-N*N;M3=4*S5-N*S3
    mu8=[N,8*S3,8*M2,128*M3]
    p=inewton(h8,6);G=[[p[i+j] for j in range(4)] for i in range(4)]
    adj=[[(-1)**(i+j)*idet3([[G[k][l] for l in range(4) if l!=i] for k in range(4) if k!=j]) for j in range(4)] for i in range(4)]
    D4=sum((G[0][j]*adj[j][0] for j in range(4)),IP())
    require(D4==ideterminant(G),'entire24-permutation determinant')
    require(all(sum((G[i][k]*adj[k][j] for k in range(4)),IP())==(D4 if i==j else 0) for i in range(4) for j in range(4)),'all16 integer adjugate entries')
    n=8*(N*N*D4-sum((mu8[i]*adj[i][j]*mu8[j] for i in range(4) for j in range(4)),IP()))
    d=M2*D4
    content=gcd(*(abs(c) for pp in [n,d] for c in pp.d.values()))
    require(content>0,'positive common integer content')
    n=IP({k:c//content for k,c in n.d.items()});d=IP({k:c//content for k,c in d.d.items()})
    nb=8*(A-1)**2*(5*A+3)**2;db=(15*A*A+24*A+10)*(35*A*A+38*A+11)
    gap=nb*d-db*n-50*W*db*d
    gap_content=gcd(*(abs(c) for c in gap.d.values()))
    gap=IP({k:c//gap_content for k,c in gap.d.items()})
    require(all(k[1]+k[2]>=2 for k in gap.d),'complete quadratic vanishing')
    require(base_ip(nb*d-db*n)==0,'entire base branch ratio')
    baseGram=(8**12*9//16)*(A-1)**6*(A+1)**2*(5*A+3)**2*(15*A*A+24*A+10)
    require(base_ip(D4)==baseGram,'exact nonsingular base Gram factor')
    if chart=='22211':
        require(all(k[1]%2==0 for pp in [n,d,gap,D4] for k in pp.d),'entire negative-pair swap symmetry')
    return {'N':irational(N),'S3':irational(S3),'M2':irational(M2),'M3':irational(M3),
            'D4_scaled':irational(D4),'n':irational(n),'d':irational(d),'gap50':irational(gap),
            'nb':irational(nb),'db':irational(db),'W':irational(W),'h8':[irational(c) for c in h8],
            'common_content':content,'gap_content':gap_content,'positive_rational_kernel_scale':Q(8**13,content)}

def affine_collar_power(poly,box):
    """Different full expansion; both split axes have zero lower endpoint."""
    (lo,hi),(slo,shi),(tlo,thi)=box
    require(slo==tlo==0,'affine control requires split axes based at zero')
    out={}
    for (i,j,k),c in poly.d.items():
        split_factor=c*shi**j*thi**k
        for a in range(i+1):
            key=(a,j,k)
            out[key]=out.get(key,Q(0))+split_factor*comb(i,a)*lo**(i-a)*(hi-lo)**a
    return MP(out)

def collar_record(poly,box):
    degrees,coeffs=tensor_bernstein(poly,box)
    require(reconstruct_tensor(degrees,coeffs)==affine_collar_power(poly,box),'complete collar basis reconstruction')
    values=list(coeffs.values());positive=[c for c in values if c>0]
    return {'degrees':list(degrees),'box':[[str(a),str(b)] for a,b in box],
            'coefficients':len(values),'negative':sum(c<0 for c in values),
            'zero':sum(c==0 for c in values),'positive':len(positive),
            'minimum':str(min(values)),'minimum_positive':str(min(positive)) if positive else None,
            'coefficient_sha256':record_hash([list(k)+[str(c)] for k,c in sorted(coeffs.items())])}

def dual_profile(chart,A,s,t):
    if chart=='32111':return [A-s]*3+[1-t]*2+[A+3*s,1+2*t,-4*A-3]
    if chart=='22211':return [A-s]*2+[A+s]*2+[1-t]*2+[1+2*t,-4*A-3]
    raise ValueError('unknown literal chart')

def dual_control(chart,point,kernel,inside=True):
    A,s,t=point;u=dual_profile(chart,A,s,t)
    N=sum(x*x for x in u);m2=sum(x**4 for x in u)-N*N/8
    require(sum(u)==0 and m2>0,'literal balanced profile, positive fourth moment')
    values={name:evaluate(kernel[name],point) for name in ['N','M2','D4_scaled','n','d','nb','db','W']}
    require(values['N']==N and values['M2']==8*m2,'independent literal norms')
    require(values['D4_scaled']>0 and values['d']>0 and values['db']>0,'literal positive denominators, including collisions')
    C=(N*N-full_pinching(u))/m2
    require(C==values['n']/values['d'],'different full8 commutant equals four-moment formula')
    gap=values['nb']/values['db']-C-50*values['W']
    if inside:require(gap>=0,'literal double-split inequality')
    return {'chart':chart,'point':list(map(str,point)),'profile':list(map(str,u)),
            'levels':len(set(u)),'N':str(N),'C':str(C),'branch_gap50':str(gap)}

def verify_dual():
    records={};kernels={}
    A,s,t=[MP.variable(i) for i in range(3)]
    width=Q(1,200);Abox=(Q(-43,50),Q(-17,20))
    for chart in ['32111','22211']:
        k=build_dual_kernel(chart);kernels[chart]=k
        for name,p in k.items():
            if isinstance(p,MP):records[chart+'_'+name]=summarize_polynomial(p)
        records[chart+'_h8']=[encode(p) for p in k['h8']]
        records[chart+'_positive_kernel_scale']=str(k['positive_rational_kernel_scale'])
        if chart=='32111':
            for sign_s,sign_t in [(1,1),(1,-1),(-1,1),(-1,-1)]:
                polynomial=MP({key:c*sign_s**key[1]*sign_t**key[2] for key,c in k['gap50'].d.items()})
                result=collar_record(polynomial,(Abox,(Q(0),width),(Q(0),width)))
                require(result['negative']==0 and result['zero']==84 and result['positive']==5985,'entire32111 collar certificate')
                records['32111_box_'+str(sign_s)+'_'+str(sign_t)]=result
        else:
            require(all(key[1]%2==0 for key in k['gap50'].d),'entire even gap')
            even=MP({(i,j//2,l):c for (i,j,l),c in k['gap50'].d.items()})
            for sign_t in [1,-1]:
                polynomial=MP({key:c*sign_t**key[2] for key,c in even.d.items()})
                result=collar_record(polynomial,(Abox,(Q(0),width*width),(Q(0),width)))
                require(result['negative']==0 and result['zero']==42 and result['positive']==3171,'entire22211 collar certificate')
                records['22211_box_'+str(sign_t)]=result
    # Complete inherited branch transformation, curvature and Euclidean geometry.
    X=-5*A-3
    nbX=8*X*X*(X+8)**2;dbX=21*X**4-30*X**3+23*X*X-4*X+20
    require(kernels['32111']['nb']*dbX==kernels['32111']['db']*nbX,'entire9121 inherited branch pullback')
    nb=kernels['32111']['nb'];db=kernels['32111']['db']
    derivative=nb.derivative(0)*db-nb*db.derivative(0)
    Qalpha=4575*A**4+11695*A**3+11175*A*A+4737*A+746
    require(derivative==16*(A-1)*(5*A+3)*Qalpha,'entire inherited stationary-root identity')
    records['stationary_polynomial']=encode(Qalpha)
    Qcoeff=[Qalpha.d.get((i,0,0),Q(0)) for i in range(5)]
    require(count(sturm(Qcoeff),Q(-427,500),Q(-853,1000))==1,'exact alpha isolation in the collar interval')
    records['alpha_isolation']=['-427/500','-853/1000']
    second=derivative.derivative(0)*db-2*derivative*db.derivative(0)
    curvature,positive_scale=primitive_with_positive_scale(-second-1600*db**3)
    curvaturebox=(Abox,(Q(0),Q(1)),(Q(0),Q(1)))
    result=bernstein_record(curvature,curvaturebox)
    require(Q(result['minimum'])>0,'Fsecond<=-1600, entire branch interval')
    records['branch_curvature']=result;records['branch_curvature_scale']=str(positive_scale)
    records['branch_denominator']=bernstein_record(db,curvaturebox)
    require(Q(records['branch_denominator']['minimum'])>0,'positive entire branch denominator')
    Nmin=Q(121,20);Wmax=18*width*width;vmax=Wmax/Nmin
    require(1-vmax>Q(119,121)**2,'normalization chord bound')
    L=96/(Nmin*Nmin)
    N0=20*A*A+24*A+12
    require(20*N0-(20*A+12)**2==96,'entire normalized branch-speed identity')
    require(50*Nmin==300*Q(121,120) and 800>300*L,'Euclidean coefficient300')
    records['Euclidean_geometry']={'Nmin':str(Nmin),'maxW':str(Wmax),'maxv':str(vmax),
                                 'square_root_margin':str(1-vmax-Q(119,121)**2),
                                 'branch_metric_bound':str(L),'branch_coercivity_margin':str(800-300*L),'coefficient':300}
    # Exact radius-to-chart scalar bounds; the finite partition classification is
    # proved in PROOF.md, not inferred from this scalar arithmetic.
    radius=Q(1,10000);gamma_lower=Q(2,5);b_lower=gamma_lower-radius
    alpha_lo,alpha_hi=Q(-427,500),Q(-853,1000)
    alpha_nmax=max(20*a*a+24*a+12 for a in [alpha_lo,alpha_hi])
    require(alpha_nmax<Q(25,4),'gamma>2/5')
    Aerror=(1-alpha_lo)*radius/b_lower
    require(alpha_lo-Aerror>Abox[0] and alpha_hi+Aerror<Abox[1],'entire average-ratio interval')
    new_s=radius/b_lower;new_t=2*radius/(3*b_lower)
    old_U=10*radius/b_lower;old_epsilon=5*radius/b_lower
    require(new_s<width and new_t<width and old_U<Q(1,16) and old_epsilon<Q(1,16),'radius mapped into all three collar domains')
    original_cluster_gap=4*gamma_lower*(alpha_lo+1)
    require(original_cluster_gap>2*radius and gamma_lower*(-5*alpha_hi-3)>2*radius,'original cluster separation')
    records['effective_neighborhood_geometry']={'radius':str(radius),'positive_cluster_mean_lower':str(b_lower),
        'alpha_bracket':[str(alpha_lo),str(alpha_hi)],'average_ratio_error_upper':str(Aerror),
        's_upper':str(new_s),'t_upper':str(new_t),'old_U_upper':str(old_U),'old_epsilon_upper':str(old_epsilon),
        'positive_singleton_cluster_gap_lower':str(original_cluster_gap),
        'negative_singleton_cluster_gap_lower':str(gamma_lower*(-5*alpha_hi-3)),
        'scope':'all at-most-five-level profiles with largest multiplicity<=3 inside dist<=1/10000; combined with9019, all at-most-five-level C<=c3'}
    controls=[]
    control_points=[(Q(-171,200),Q(0),Q(0)),
                    (Abox[0],width,width),(Abox[1],width,-width),
                    (Q(-171,200),-width,width),(Q(-171,200),width,Q(0)),
                    (Q(-171,200),Q(0),-width)]
    for chart in ['32111','22211']:
        for point in control_points:controls.append(dual_control(chart,point,kernels[chart]))
    records['full8_controls']=controls
    # The initial larger1/100 width genuinely fails the proposed raw50 bound.
    damaged=dual_control('32111',(Q(-17,20),Q(1,100),Q(0)),kernels['32111'],inside=False)
    require(Q(damaged['branch_gap50'])<0,'wrong1/100 domain rejected by actual profile')
    records['wrong_larger_domain_control']=damaged
    small=MP({(0,0,0):3,(2,1,0):-5,(1,0,2):Q(7,3)})
    smallbox=((Q(1,4),Q(3,4)),(Q(-1,3),Q(1,2)),(Q(0),Q(1,5)))
    require(tensor_bernstein(small,smallbox)==bernstein(small,smallbox),'different dense tensor control')
    records['dense_transport_control']=summarize_polynomial(small)
    tiny=MP({(2,0,0):1});degrees,coeffs=tensor_bernstein(tiny,((Q(0),Q(1)),)*3)
    coeffs[(0,0,0)]+=1
    require(reconstruct_tensor(degrees,coeffs)!=tiny,'damaged Bernstein entry rejected')
    k=kernels['32111'];point=(Q(-171,200),width,-width)
    v={name:evaluate(k[name],point) for name in ['n','d','N','S3','M2','M3','D4_scaled']}
    require(v['M2']*v['D4_scaled']>0,'moments control uses nonsingular physical denominator')
    h=[evaluate(c,point) for c in k['h8']];traces=[Q(4)]
    for j in range(1,7):
        if j<=4:next_trace=-j*h[4-j]-sum((h[4-i]*traces[j-i] for i in range(1,j)),Q(0))
        else:next_trace=-sum((h[4-i]*traces[j-i] for i in range(1,5)),Q(0))
        traces.append(next_trace)
    G=[[traces[i+j] for j in range(4)] for i in range(4)]
    true_mu=[v['N'],8*v['S3'],8*v['M2'],128*v['M3']]
    true_eta=sum(a*b for a,b in zip(true_mu,fraction_solve(G,true_mu)))
    actual=(v['N']**2-true_eta)/(v['M2']/8)
    require(actual==v['n']/v['d'],'different rational Gaussian solution of literal four-moment Gram')
    # Keeping8-scaled roots but original unscaled moments is a real scaling error.
    wrong_mu=[v['N'],v['S3'],v['M2']/8,v['M3']/4]
    wrong_eta=sum(a*b for a,b in zip(wrong_mu,fraction_solve(G,wrong_mu)))
    wrong_C=(v['N']**2-wrong_eta)/(v['M2']/8)
    require(wrong_C!=actual,'unscaled-moments mistake detected')
    records['wrong_scaled_moments_control']={'point':list(map(str,point)),'actual_C':str(actual),'wrong_C':str(wrong_C)}
    records['damage_controls']={'wrong_larger_domain_rejected':True,'damaged_Bernstein_reconstruction_rejected':True,'unscaled_moments_with_scaled_roots_detected':True}
    return records

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--expected',type=Path,default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--emit',type=Path)
    args=parser.parse_args();t0=time.monotonic();records=verify_dual()
    if args.emit:args.emit.write_text(json.dumps(records,indent=2)+'\n')
    else:require(records==json.loads(args.expected.read_text()),'entire expected fixture mismatch')
    boxes=[v for name,v in records.items() if '_box_' in name]
    print(json.dumps({'status':'PASS','recorded_checks':len(records),'full8_controls':len(records['full8_controls'])+1,
        'collar_boxes':len(boxes),'Bernstein_coefficients':sum(v['coefficients'] for v in boxes),
        'positive_coefficients':sum(v['positive'] for v in boxes),'zero_coefficients':sum(v['zero'] for v in boxes),
        'whole_collar_reconstructions':len(boxes),'record_sha256':record_hash(records),
        'elapsed_seconds':round(time.monotonic()-t0,4)}))

if __name__=='__main__':main()
