#!/usr/bin/env python3
"""Exact remaining four-level angular certificate, standard library only.
Sparse Fraction kernel adapted from own8800/source167af56c25651784f7c8106a3ec1d85e52b51c82.
Degree-bounded integer Sylvester checks credit reviewer8859/source67721b3d70cfa96def249295f182a5f63b4969a5.
Credits the spectral invariant formula of graph7883; no runtime campaign imports.
"""
from __future__ import annotations
from fractions import Fraction as Q
from pathlib import Path
from math import comb,gcd,lcm,factorial
from itertools import permutations
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


def coeff_in_V(poly):
    deg=max(k[1] for k in poly.d);out=[[Q(0)] for _ in range(deg+1)]
    for (i,j,k),v in poly.d.items():
        require(k==0 and v.denominator==1,'noninteger chart coefficient')
        if len(out[j])<=i:out[j]+=[Q(0)]*(i+1-len(out[j]))
        out[j][i]+=v
    return [trim(x) for x in out]


def sylvester(p,q,j):
    m,n=len(p)-1,len(q)-1;width=m+n-j;rows=[]
    for coefficients,shifts in [(p,n-j),(q,m-j)]:
        for shift in range(shifts-1,-1,-1):
            row=[[Q(0)]]*width
            for degree,entry in enumerate(coefficients):row[width-1-degree-shift]=entry
            rows.append(row)
    return rows


def integer_det(matrix):
    require(all(Q(x).denominator==1 for row in matrix for x in row),'noninteger determinant entry')
    A=[[int(x) for x in row] for row in matrix];n=len(A);previous=1;sign=1
    for k in range(n-1):
        pivot=next((i for i in range(k,n) if A[i][k]),None)
        if pivot is None:return 0
        if pivot!=k:A[k],A[pivot]=A[pivot],A[k];sign=-sign
        value=A[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                raw=value*A[i][j]-A[i][k]*A[k][j]
                require(raw%previous==0,'inexact integer Bareiss division')
                A[i][j]=raw//previous
            A[i][k]=0
        previous=value
    return sign*A[-1][-1]


def evaluate_matrix(rows,x):
    return [[int(pe(p,Q(x))) for p in row] for row in rows]


def encode(value):
    if isinstance(value,MP):return [[list(k),str(v)] for k,v in sorted(value.d.items())]
    if isinstance(value,dict):return {str(k):encode(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [encode(v) for v in value]
    if isinstance(value,Q):return str(value)
    return value



RESULTANT_CONSTANT=-38548364790109088594101492776960000000000
FACTORS=[([-3, 1], 1, []), ([-2, 1], 1, []), ([1, 1], 14, []), ([-5, 3], 14, []), ([-1, 1], 41, []), ([-505, 993, -660, 145], 5, []), ([-7175, 19130, -19925, 9724, -1829, -142, 73], 1, []), ([-966, 4909, -9288, 9619, -5782, 1983, -356, 25], 1, [['17738947/44086634', '17746771/44106079']]), ([10094475, -77924460, 275654834, -593607988, 869879101, -916379176, 712904868, -413050280, 176905293, -54585868, 11504650, -1484740, 88571], 1, [['879863/1222944', '790092/1098169']]), ([-10046500, 135186500, -813460970, 2930012194, -7131255914, 12519766390, -16484141238, 16668960846, -13125337793, 8098178845, -3914107206, 1472119782, -424852280, 91904260, -14356874, 1524442, -98617, 2981], 1, [['2054307/1605941', '3053246/2386855']]), ([107262770393261802568750, -1846815420772997844379375, 15196428095792483068292875, -79443418230196734776346375, 295868308694731441407828125, -834330076144407706093084405, 1848811212729043306656396551, -3300019317017124317165844901, 4833655954885929168646062219, -5911866925139337467761335443, 6173610169892680569026312533, -5698305151979712125656502143, 4884011181840528493429184529, -4066200718711285499591823881, 3291697557862062893516888891, -2447376649154099411621671973, 1519878036539122499595403871, -669404475316208731051335941, 83279990328305867507936155, 181818414274796630706875315, -212849992948122126143389193, 144287252738283419455467217, -70698310923332136663002667, 25856407266466330808428025, -6692168978875479170444247, 901405297579071559347359, 154466721276970634059343, -138413192852407699718253, 47723089434375201404539, -10951120815183544341331, 1809924273513338206025, -215479780567391967471, 17684873354616305055, -900123977610823320, 21473279758948950], 1, [['2818709/2607070', '429694/397431']])]

def moments_from_monic(poly,kmax):
    degree=len(poly)-1
    require(poly[-1]==1,'nonmonic original polynomial')
    powers=[MP(degree)]
    for k in range(1,kmax+1):
        if k<=degree:
            val=-k*poly[degree-k]-sum(poly[degree-j]*powers[k-j] for j in range(1,k))
        else:val=-sum(poly[degree-j]*powers[k-j] for j in range(1,degree+1))
        powers.append(val)
    return powers

def gram_kernel(N,S3,S4,h):
    mu2=S4-N*N/8
    powers=moments_from_monic(h,4)
    G=[[powers[i+j] for j in range(3)] for i in range(3)]
    D=det3(G);mu=[N,S3,mu2];E=MP(0)
    for i in range(3):
        for j in range(3):
            rows=[k for k in range(3) if k!=j];cols=[k for k in range(3) if k!=i]
            minor=G[rows[0]][cols[0]]*G[rows[1]][cols[1]]-G[rows[0]][cols[1]]*G[rows[1]][cols[0]]
            E+=(-1)**(i+j)*mu[i]*minor*mu[j]
    nraw,draw=N*N*D-E,mu2*D
    denominator=lcm(*(v.denominator for p in [nraw,draw] for v in p.d.values()))
    content=gcd(*(int(v*denominator) for p in [nraw,draw] for v in p.d.values()))
    scalar=Q(denominator,content)
    require(scalar>0,'nonpositive ratio normalization')
    return {'N':N,'S3':S3,'S4':S4,'mu2':mu2,'h':h,'D':D,
            'n':scalar*nraw,'d':scalar*draw,'positive_scalar':scalar}

def family_kernel():
    a,V=[MP.variable(i) for i in range(2)];d=4-3*a
    moments=[3*a**k+d**k+4*sum(comb(k,j)*(-1)**(k-j)*V**(j//2)
              for j in range(0,k+1,2)) for k in range(1,5)]
    A=[-a,MP(1)];B=[1-V,MP(2),MP(1)];S=[-d,MP(1)]
    f=zpm(zpm(zpow(A,3),zpow(B,2)),S)
    h=[-V*a+Q(3,2)*V-Q(3,2)*a*a+3*a-Q(3,2),
       -V/2-Q(3,2)*a*a+5*a-Q(9,2),2*a-2,MP(1)]
    require([Q(i,8)*f[i] for i in range(1,9)]==zpm(zpm(zpow(A,2),B),h),
            'full original derivative factorization')
    require(moments==moments_from_monic(f,4)[1:],'literal versus Newton raw moments')
    require(moments[0]==0,'balance')
    return gram_kernel(*moments[1:],h)

def paired_kernel():
    alpha,tau,c=[MP.variable(i) for i in range(3)]
    g=[c,-tau,-alpha,MP(0),MP(1)]
    f=zpow(g,2);h=[-tau/4,-alpha/2,MP(0),MP(1)]
    require([Q(i,8)*f[i] for i in range(1,9)]==zpm(g,h),
            'paired full original derivative factorization')
    powers=moments_from_monic(f,4)
    require(powers[1]==0 and powers[2]==4*alpha and powers[3]==6*tau
            and powers[4]==4*alpha*alpha-8*c,'paired raw Newton moments')
    return gram_kernel(*powers[2:5],h),g

def strip_bernstein(n,d,interval,constant=Q(49,2)):
    # Six Bernstein coefficient polynomials in V, enclosed over the a strip.
    compare=constant*d-n;deg=max(k[1] for k in compare.d)
    require(deg==5,'wrong vertical comparison degree')
    power=[]
    for j in range(deg+1):
        coefficient=[Q(0)]*(1+max(k[0] for k in compare.d))
        for (i,l,k),v in compare.d.items():
            require(k==0,'unexpected chart indeterminate')
            if l==j:coefficient[i]+=v
        power.append(trim(coefficient))
    coefficients=[]
    for k in range(deg+1):
        polynomial=[Q(0)]
        for j in range(k+1):polynomial=pa(polynomial,ps(power[j],Q(comb(k,j),comb(deg,j))))
        coefficients.append(ivpoly(polynomial,interval))
    return coefficients

def specialize_first(poly,value):
    out={}
    for (i,j,k),v in poly.d.items():
        key=(0,j,k);out[key]=out.get(key,Q(0))+v*value**i
    return MP(out)

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

def invariant_at(poly,values):
    return sum(c*values[0]**i*values[1]**j*values[2]**k for (i,j,k),c in poly.d.items())

def verify(progress=False):
    records={}
    def check(name,actual,expected):
        require(actual==expected,name+' failed');records[name]=encode(actual)
    def note(message):
        if progress:print(message,file=sys.stderr,flush=True)
    derived=family_kernel();note('original3+2+2+1 moment kernel regenerated')
    a,V=[MP.variable(i) for i in range(2)]
    check('chart normalization',derived['N'],8+12*(a-1)**2+4*V)
    for name in ['N','S3','S4','mu2','h','D','n','d','positive_scalar']:records[name]=encode(derived[name])
    n,d=derived['n'],derived['d']
    P=(n.derivative(0)*d-n*d.derivative(0)).primitive_integer()
    Qp=(n.derivative(1)*d-n*d.derivative(1)).primitive_integer()
    p,q=coeff_in_V(P),coeff_in_V(Qp)
    check('gradient V degrees',[len(p)-1,len(q)-1],[9,8])
    wp,wq=max(i+2*j for i,j,k in P.d),max(i+2*j for i,j,k in Qp.d)
    require(wp<=19 and wq<=18,'gradient weighted degree bounds failed')
    records['gradient weighted degrees']=[wp,wq]
    bound=8*19+9*18-2*(sum(range(17))-sum(range(8))-sum(range(9)))
    check('resultant proven degree bound',bound,170)
    rows=sylvester(p,q,0);check('resultant matrix dimensions',[len(rows),len(rows[0])],[17,17])
    check('factored resultant degree',sum((len(f)-1)*m for f,m,b in FACTORS),162)
    values=[]
    for x in range(bound+1):
        actual=integer_det(evaluate_matrix(rows,x));expected=RESULTANT_CONSTANT
        for factor,multiplicity,boxes in FACTORS:expected*=int(pe(factor,Q(x)))**multiplicity
        require(actual==expected,'degree-bounded resultant identity at'+str(x));values.append(actual)
    records['171 exact integer determinant checks']=len(values)
    records['resultant determinant values sha256']=hashlib.sha256(json.dumps(values,separators=(',',':')).encode()).hexdigest()
    note('171 universal stationary resultant checks complete')
    root_strips=0
    for factor,multiplicity,boxes0 in FACTORS:
        degree=len(factor)-1
        if degree==1:
            root=Q(-factor[0],factor[1])
            require(root==1 or not 0<root<Q(4,3),'unhandled competitive linear factor')
            records['linear factor root '+str(root)]=str(root)
            continue
        chain=sturm(factor);boxes=[tuple(map(Q,b)) for b in boxes0]
        require(pe(factor,Q(0)) and pe(factor,Q(4,3)),'chart endpoint root')
        check('degree'+str(degree)+' all chart roots',count(chain,Q(0),Q(4,3)),len(boxes))
        previous=Q(0)
        for j,box in enumerate(boxes):
            require(previous<box[0]<box[1]<Q(4,3),'overlapping/outside chart isolations')
            require(all(pe(factor,x) for x in box),'isolation endpoint root')
            previous=box[1]
            check('degree'+str(degree)+' root'+str(j+1)+' Sturm isolation',count(chain,*box),1)
            coefficients=strip_bernstein(n,d,box)
            require(all(co[0]>0 for co in coefficients),'whole-root-strip Bernstein positivity failed')
            records['degree'+str(degree)+' root'+str(j+1)+' interval']=encode(box)
            records['degree'+str(degree)+' root'+str(j+1)+' six positive coefficient bounds']=encode(coefficients)
            root_strips+=1
    check('full nonexceptional root strip count',root_strips,4)
    # Explicit derivative-side boundary identities, not a monotonicity claim.
    n0=MP({k:v for k,v in n.d.items() if k[1]==0})
    d0=MP({k:v for k,v in d.d.items() if k[1]==0})
    bnum=72*a**4-96*a**3-208*a*a+160*a+200
    bden=110*a**4-644*a**3+1427*a*a-1410*a+525
    check('V=0 inherited three-level ratio',n0*bden-d0*bnum,MP(0))
    # Retain the exact obstruction to a proposed global boundary comparison.
    def at(poly,x,y):return sum(c*x**i*y**j for (i,j,k),c in poly.d.items())
    check('failed boundary shortcut actual ratio',at(n,Q(1,10),Q(1,4))/at(d,Q(1,10),Q(1,4)),
          Q(345593988944,434411238715))
    check('failed boundary shortcut boundary ratio',at(n,Q(1,10),Q(0))/at(d,Q(1,10),Q(0)),
          Q(1069156,1988185))
    pair,g=paired_kernel();alpha,tau,c=[MP.variable(i) for i in range(3)]
    K=alpha*alpha-4*c;I=alpha*alpha+12*c
    Delta=128*alpha**3-432*tau*tau
    check('paired Gram determinant discriminant',256*pair['D'],Delta)
    check('paired fourth excess identity',pair['mu2'],2*K)
    check('paired exact nonnegative invariant deficit',
          ((16*pair['d']-pair['n'])*alpha*alpha-12*K*pair['d'])*Delta*K,
          576*tau*tau*I*I*pair['d'])
    for name in ['n','d']:records['paired original '+name]=encode(pair[name])
    # Derive I as a sum of squares in the literal four real labels.
    x,y,z=[MP.variable(i) for i in range(3)];w=-x-y-z
    labels=[x,y,z,w]
    alp=-sum(labels[i]*labels[j] for i in range(4) for j in range(i+1,4))
    product=x*y*z*w
    sos=((x-y)**2*(z-w)**2+(x-z)**2*(y-w)**2+(x-w)**2*(y-z)**2)/2
    check('paired quartic invariant sum of squares',alp*alp+12*product,sos)
    S2=sum(t*t for t in labels);S4=sum(t**4 for t in labels)
    check('balanced four-label moment identity',2*S4-S2*S2,-8*product)
    check('singular six-plus-two X',Q(6+2*81,24**2),Q(7,24))
    check('singular paired strong upper bound',28-96*Q(7,24),Q(0))
    note('global paired invariant deficit regenerated')
    controls321=[([1]*3+[-5]*2+[-15]*2+[37],Q(1,10),Q(1,4)),
                 ([75]*3+[-64]*4+[31],Q(75,64),Q(0)),
                 ([2]*4+[-1]*2+[-3]*2,Q(1),Q(1,4))]
    for j,(profile,av,vv) in enumerate(controls321):
        norm=sum(x*x for x in profile);excess=Q(sum(x**4 for x in profile))-Q(norm*norm,8)
        actual=(norm*norm-full_pinching(profile))/excess
        check('full original-coordinate321 pinching control'+str(j+1),
              actual,at(n,av,vv)/at(d,av,vv))
    for j,labels in enumerate([[-3,-1,1,3],[-5,1,1,3],[1,1,1,-3]]):
        profile=[x for x in labels for _ in range(2)]
        norm=sum(x*x for x in profile);excess=Q(sum(x**4 for x in profile))-Q(norm*norm,8)
        actual=(norm*norm-full_pinching(profile))/excess
        if len(set(labels))==2:expected=Q(0)
        else:
            alpha0=-sum(labels[i]*labels[j] for i in range(4) for j in range(i+1,4))
            tau0=sum(labels[i]*labels[j]*labels[k] for i in range(4) for j in range(i+1,4) for k in range(j+1,4))
            values=[Q(alpha0),Q(tau0),Q(labels[0]*labels[1]*labels[2]*labels[3])]
            expected=invariant_at(pair['n'],values)/invariant_at(pair['d'],values)
        check('full original-coordinate paired pinching control'+str(j+1),actual,expected)
    check('uniform full-eigenspace mass-square',full_pinching([1]*4+[-1]*4),Q(64))
    note('seven separate full-coordinate commutant controls complete')
    controls=0
    wrong_h=list(pair['h']);wrong_h[0]=tau/4
    f=zpow(g,2)
    bad=[values[0]==-values[0],count(sturm(FACTORS[-1][0]),Q(0),Q(4,3))==0,
         all(co[0]>0 for co in strip_bernstein(n,d,tuple(map(Q,FACTORS[-1][2][0])),Q(-1))),
         [Q(i,8)*f[i] for i in range(1,9)]==zpm(g,wrong_h)]
    for condition in bad:
        try:require(condition,'mathematical damaged certificate')
        except ValueError:controls+=1
    require(controls==4,'damage controls failed')
    return {'records':records,'checks':len(records),'damage_controls':controls}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write-expected',action='store_true')
    parser.add_argument('--expected',type=Path);parser.add_argument('--progress',action='store_true')
    args=parser.parse_args();start=time.monotonic();output=verify(args.progress)
    raw=json.dumps(output,sort_keys=True,separators=(',',':')).encode()
    output['record_sha256']=hashlib.sha256(raw).hexdigest()
    fixture=args.expected or Path(__file__).with_name('expected.json')
    if args.write_expected:fixture.write_text(json.dumps(output,sort_keys=True,indent=2)+'\n')
    else:require(json.loads(fixture.read_text())==output,'expected fixture differs')
    summary={k:v for k,v in output.items() if k!='records'};summary['elapsed_seconds']=round(time.monotonic()-start,6)
    print(json.dumps(summary,sort_keys=True))

if __name__=='__main__':
    try:main()
    except (ValueError,OSError) as error:
        print('verification failed: '+str(error),file=sys.stderr);sys.exit(1)
