#!/usr/bin/env python3
"""Exact effective32111 angular collar; stdlib rational arithmetic.
Actual author six-sendov-2, researcher. Sparse arithmetic and full8 commutant
control adapted from own9019 sourcec51020e79a1872c88bb98a8bd3a472489860ca4a,
with documentation correction5341085889659547fc1ad953a6adcda071231173.
The three-level optimum and collision-continuity theorem credit8753/8806.
This program has no runtime campaign imports, CAS, root approximation or
mathematical floating point. The final comparison verifies every fixture entry.
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

def build_triple_kernel():
    x,q,r=[MP.variable(i) for i in range(3)]
    shift=[MP(-3),MP(1)];K=zpow(shift,3)
    K=add_z(K,scale_z(zpow(shift,2),2*x));K=add_z(K,scale_z(shift,q));K[0]-=r
    L=[-3-x,MP(1)];R=[MP(5),MP(1)]
    f=zpm(zpow(R,3),zpm(zpow(L,2),K))
    h=scale_z(add_z(zpm([1-3*x,MP(5)],K),zpm(zpm(R,L),[j*K[j] for j in range(1,len(K))])),Q(1,8))
    require([Q(j,8)*f[j] for j in range(1,len(f))]==zpm(zpm(zpow(R,2),L),h),'original derivative')
    S=newton(f,5);require(S[1]==0,'balance')
    N,S3,S4,S5=S[2:6];m2=S4-N*N/8;m3=S5-N*S3/4
    p=newton(h,6);G3=[[p[i+j] for j in range(3)] for i in range(3)]
    D3=det3(G3)
    a3=[[(-1)**(i+j)*determinant([[G3[k][l] for l in range(3) if l!=i] for k in range(3) if k!=j]) for j in range(3)] for i in range(3)]
    mu=[N,S3,m2];v=p[3:6]
    n3=N*N*D3-pairing(mu,a3,mu);z=m3*D3-pairing(v,a3,mu)
    D4=p[6]*D3-pairing(v,a3,v)
    G4=[[p[i+j] for j in range(4)] for i in range(4)]
    require(D4==determinant(G4),'complete Schur versus permutation determinant')
    a4=[[(-1)**(i+j)*det3([[G4[k][l] for l in range(4) if l!=i] for k in range(4) if k!=j]) for j in range(4)] for i in range(4)]
    require(all(sum((G4[i][k]*a4[k][j] for k in range(4)),MP(0))==(D4 if i==j else 0) for i in range(4) for j in range(4)),'all16 adjugate entries')
    n4raw=N*N*D4-pairing(mu+[m3],a4,mu+[m3])
    require(n4raw*D3==n3*D4-z*z,'complete Schur correction identity')
    n4,d4,scale=shared_positive_normalize(n4raw,m2*D4)
    return {'h':h,'N':N,'S3':S3,'m2':m2,'m3':m3,'D3':D3,'D4':D4,'z':z,'n3':n3,'n4':n4,'d4':d4,'positive_scale':scale}

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

def original_control(profile,kernel):
    require(sum(profile)==0 and len(profile)==8,'literal balanced profile')
    x=profile[3]-3;ys=[t-3 for t in profile[5:]]
    q=sum(ys[i]*ys[j] for i in range(3) for j in range(i+1,3));r=ys[0]*ys[1]*ys[2]
    point=(x,q,r);v={name:evaluate(p,point) for name,p in kernel.items() if isinstance(p,MP)}
    N=sum(t*t for t in profile);m2=sum(t**4 for t in profile)-N*N/8
    require(v['N']==N and v['m2']==m2 and m2>0,'different literal original moments')
    actual=(N*N-full_pinching(profile))/m2
    if v['D4']:
        require(v['D3']>0 and v['D4']>0 and v['d4']>0,'positive physical denominators')
        upper=v['n3']/(m2*v['D3']);correction=v['z']**2/(m2*v['D3']*v['D4'])
        require(actual==v['n4']/v['d4']==upper-correction,'full8 commutant equalsfour-moment equalsSchur')
    else:upper=correction=None
    return {'profile':list(map(str,profile)),'point':list(map(str,point)),'original_levels':len(set(profile)),'N':str(N),'C':str(actual),'R3':str(upper) if upper is not None else None,'Schur_correction':str(correction) if correction is not None else None}

def cluster_profile(X,U,epsilon):
    return [Q(-5)]*3+[3+X-U]*2+[3+X+U+epsilon,3+X+U-epsilon,3-4*X]

def branch_fraction(x):return 8*x*x*(x+8)**2/(21*x**4-30*x**3+23*x*x-4*x+20)

def verify():
    records={};k=build_triple_kernel()
    for name,p in k.items():
        if isinstance(p,MP):records['kernel_'+name]=summarize_polynomial(p)
    records['kernel_active_quartic']=[encode(p) for p in k['h']]
    records['kernel_positive_scale']=str(k['positive_scale'])
    X,U,V=[MP.variable(i) for i in range(3)]
    qq=(X+U)**2-V-8*X*(X+U);rr=-4*X*((X+U)**2-V)
    cluster={name:substitute(k[name],[X-U,qq,rr]) for name in ['n4','d4','D4','z','N']}
    require(cluster['N']==120+20*X*X+4*U*U+2*V,'cluster norm')
    for name,p in cluster.items():records['cluster_'+name]=summarize_polynomial(p)
    nb=8*X*X*(X+8)**2;db=21*X**4-30*X**3+23*X*X-4*X+20
    # Deflate the full collision polynomial in the actual symmetric splitting.
    pathn=substitute(k['n4'],[X,-7*X*X-U,-4*X**3+4*X*U])
    pathd=substitute(k['d4'],[X,-7*X*X-U,-4*X**3+4*X*U])
    pn=divide_variable(pathn,1,1);pden=divide_variable(pathd,1,1)
    require(substitute(pn,[X,MP(0),MP(0)])*db==substitute(pden,[X,MP(0),MP(0)])*nb,'entire collision ratioC0')
    records['symmetric_path_deflated_n']=summarize_polynomial(pn)
    records['symmetric_path_deflated_d']=summarize_polynomial(pden)
    W=4*U*U+2*V;gap=nb*cluster['d4']-db*cluster['n4']-2*W*db*cluster['d4']
    require(min(key[1]+2*key[2] for key in gap.d)>=4,'complete weighted vanishing')
    gap,positive_scale=primitive_with_positive_scale(gap)
    records['collar_gap']=summarize_polynomial(gap);records['collar_gap_positive_scale']=str(positive_scale)
    for sign,width,label in [(1,Q(1,4),'positiveU'),(-1,Q(1,16),'negativeU')]:
        box=((Q(5,4),Q(13,10)),(Q(0),width),(Q(0),width**2))
        polynomial=substitute(gap,[X,sign*U,V])
        result=bernstein_record(polynomial,box)
        require(result['negative']==0 and result['zeros']==114 and result['positive']==3135,'complete collar positivity')
        records['collar_'+label]=result
    # A small dense expansion verifies the alternative coefficient transports.
    small=MP({(0,0,0):3,(2,1,0):-5,(1,0,2):Q(7,3)})
    smallbox=((Q(1,4),Q(3,4)),(Q(-1,3),Q(1,2)),(Q(0),Q(1,5)))
    require(tensor_bernstein(small,smallbox)==bernstein(small,smallbox),'different dense coefficient transport')
    records['transport_control']=summarize_polynomial(small)
    derivative=nb.derivative(0)*db-nb*db.derivative(0)
    second=derivative.derivative(0)*db-2*derivative*db.derivative(0)
    curvature,curvature_scale=primitive_with_positive_scale(-second-64*db**3)
    curvature_box=((Q(5,4),Q(13,10)),(Q(0),Q(1)),(Q(0),Q(1)))
    result=bernstein_record(curvature,curvature_box)
    require(result['negative']==0 and result['zeros']==0,'C0 second derivative<=-64')
    records['branch_curvature']=result;records['branch_curvature_positive_scale']=str(curvature_scale)
    dbrecord=bernstein_record(db,curvature_box)
    require(Q(dbrecord['minimum'])>0,'positive branch denominator')
    records['branch_denominator']=dbrecord
    alpha=-(X+3)/5
    inherited_n=8*(alpha-1)**2*(5*alpha+3)**2
    inherited_d=(15*alpha**2+24*alpha+10)*(35*alpha**2+38*alpha+11)
    require(nb*inherited_d==db*inherited_n,'entire inherited431 curve pullback')
    Qalpha=4575*alpha**4+11695*alpha**3+11175*alpha**2+4737*alpha+746
    px=Qalpha.primitive_integer()
    left,right=Q(1267,1000),Q(1268,1000)
    coefficient=[px.d.get((i,0,0),Q(0)) for i in range(5)]
    require(count(sturm(coefficient),left,right)==1,'exactxstar root isolation')
    rootfactor=X*(X+8)*px
    firstkey=next(key for key in derivative.d if rootfactor.d.get(key))
    scalar=derivative.d[firstkey]/rootfactor.d[firstkey]
    require(derivative==scalar*rootfactor,'entire inherited maximizing-root derivative')
    records['branch_critical_polynomial']=encode(px);records['branch_derivative_scalar']=str(scalar)
    records['branch_root_bracket']=[str(left),str(right)]
    Nmin=Q(605,4);maxW=Q(3,8);maxv=maxW/Nmin
    # sqrt(1-v)>=119/121 ensures2(1-sqrt(1-v))<=121v/120.
    require(1-maxv>Q(119,121)**2,'normalization chord bound')
    L=Q(2400)/(Nmin*Nmin)
    require(300*Q(121,120)==2*Nmin and 300*L<32,'Euclidean coercivity300')
    records['normalization_geometry']={'Nmin':str(Nmin),'maxW':str(maxW),'max_cluster_unit_variance':str(maxv),'square_root_margin':str(1-maxv-Q(119,121)**2),'branch_metric_upper':str(L),'branch_coercivity_margin':str(32-300*L),'unit_distance_coefficient':300}
    controls=[]
    for profile in [[Q(-5)]*3+[Q(4)]*2+list(map(Q,[0,2,5])),[Q(-5)]*3+[Q(5)]*2+list(map(Q,[-1,2,4])),
                    cluster_profile(Q(1267,1000),Q(0),Q(1,1000)),
                    cluster_profile(Q(5,4),Q(1,4),Q(1,4)),
                    cluster_profile(Q(13,10),Q(-1,16),Q(1,16)),
                    cluster_profile(Q(51,40),Q(1,16),Q(0)),
                    cluster_profile(Q(51,40),Q(1,32),Q(1,16)),
                    cluster_profile(Q(51,40),Q(0),Q(0))]:
        controls.append(original_control(profile,k))
    records['full8_controls']=controls
    # Each collar control separately checks the claimed inequality in raw units.
    for X0,U0,eps in [(Q(1267,1000),Q(0),Q(1,1000)),(Q(5,4),Q(1,4),Q(1,4)),
                      (Q(13,10),Q(-1,16),Q(1,16)),(Q(51,40),Q(1,16),Q(0)),
                      (Q(51,40),Q(1,32),Q(1,16)),(Q(51,40),Q(0),Q(0))]:
        u=cluster_profile(X0,U0,eps);N=sum(t*t for t in u);m2=sum(t**4 for t in u)-N*N/8
        C=(N*N-full_pinching(u))/m2
        require(C<=branch_fraction(X0)-2*(4*U0*U0+2*eps*eps),'literal collar/collision inequality')
    obstruction=controls[2];actual=Q(obstruction['C']);upper=Q(obstruction['R3']);lo,hi=Q('24.53389668'),Q('24.53389670')
    require(actual<lo and upper>hi,'realizable R3 obstruction, not C counterexample')
    records['realizable_R3_obstruction']={'actual_C':str(actual),'R3':str(upper),'C_below_c3_lower':str(lo-actual),'R3_above_c3_upper':str(upper-hi)}
    # The stronger proposed raw coefficient3 fails on this actual profile.
    false3gap=branch_fraction(Q(1267,1000))-actual-6*Q(1,1000)**2
    require(false3gap<0,'wrong coefficient3 rejected on realizable profile')
    records['mathematical_damage_controls']={
        'wrong_Schur_correction':upper!=actual,
        'wrong_raw_coefficient3_gap':str(false3gap),
        'wrong_stationary_root_denominator':derivative!=scalar*X*px,
        'wrong_Bernstein_constant_detected':False,
    }
    tiny=MP({(2,0,0):1})
    deg,coeff=tensor_bernstein(tiny,((Q(0),Q(1)),)*3);coeff[(0,0,0)]+=1
    require(reconstruct_tensor(deg,coeff)!=tiny,'damagedBernstein reconstruction')
    records['mathematical_damage_controls']['wrong_Bernstein_constant_detected']=True
    require(all(records['mathematical_damage_controls'][key] for key in ['wrong_Schur_correction','wrong_stationary_root_denominator','wrong_Bernstein_constant_detected']),'damage rejection')
    return records

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--expected',type=Path,default=Path(__file__).with_name('expected.json'));parser.add_argument('--emit',type=Path)
    args=parser.parse_args();t0=time.monotonic();records=verify()
    if args.emit:args.emit.write_text(json.dumps(records,indent=2)+'\n')
    else:
        expected=json.loads(args.expected.read_text())
        require(records==expected,'complete expected-fixture mismatch')
    print(json.dumps({'status':'PASS','recorded_checks':len(records),'full8_controls':len(records['full8_controls']),
                      'collar_Bernstein_coefficients':sum(records['collar_'+s]['coefficients'] for s in ['positiveU','negativeU']),
                      'positive_collar_coefficients':6270,'structural_zero_coefficients':228,
                      'complete_basis_reconstructions':4,'mathematical_damage_controls':4,
                      'record_sha256':record_hash(records),'elapsed_seconds':round(time.monotonic()-t0,4)}))

if __name__=='__main__':main()
