#!/usr/bin/env python3
"""Independent scalar-characteristic and Gram-polynomial Sendov audit.

No author imports. Exact sparse Laurent polynomials, Gaussian extension,
Newton identities and contour logarithmic coefficients. Standard library.
"""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import argparse
import json
import time

NAMES=('m','v','mu2','mu3','mu4','psi','zeta','X','z')
NV=len(NAMES);ZE=(0,)*NV;HERE=Path(__file__).resolve().parent
LABELS=[]
def demand(ok,label):
    if not ok:raise ValueError(label)

class P:
    def __init__(self,terms=0):
        self.t=({e:F(c) for e,c in terms.items() if c} if isinstance(terms,dict)
                else ({ZE:F(terms)} if terms else {}))
    @staticmethod
    def cast(x):return x if isinstance(x,P) else P(x)
    def __add__(self,x):
        out=dict(self.t)
        for e,c in P.cast(x).t.items():out[e]=out.get(e,F(0))+c
        return P(out)
    __radd__=__add__
    def __neg__(self):return P({e:-c for e,c in self.t.items()})
    def __sub__(self,x):return self+-P.cast(x)
    def __rsub__(self,x):return P.cast(x)+-self
    def __mul__(self,x):
        out=defaultdict(F)
        for e,c in self.t.items():
            for f,d in P.cast(x).t.items():out[tuple(a+b for a,b in zip(e,f))]+=c*d
        return P(out)
    __rmul__=__mul__
    def __truediv__(self,x):
        demand(isinstance(x,(int,F)) and x!=0,'constant divisor only')
        return P({e:c/F(x) for e,c in self.t.items()})
    def __pow__(self,n):
        demand(type(n) is int and n>=0,'nonnegative polynomial power')
        out=P(1);base=self
        while n:
            if n&1:out=out*base
            base,n=base*base,n//2
        return out
    def coef(self,name,degree):
        index=NAMES.index(name);out={}
        for e,c in self.t.items():
            if e[index]==degree:
                f=list(e);f[index]=0;out[tuple(f)]=c
        return P(out)
    def substitute(self,name,value):
        index=NAMES.index(name);out=P()
        for e,c in self.t.items():
            demand(e[index]>=0,'negative substitution exponent')
            f=list(e);f[index]=0;out=out+P({tuple(f):c})*P.cast(value)**e[index]
        return out
    def evaluate(self,values):
        return sum(c*product(F(values[NAMES[j]])**e[j] for j in range(NV) if e[j])
                   for e,c in self.t.items())
    def record(self):return [[*e,c.numerator,c.denominator] for e,c in sorted(self.t.items())]

def product(seq):
    out=F(1)
    for x in seq:out*=x
    return out
def monomial(**powers):
    e=list(ZE)
    for name,power in powers.items():e[NAMES.index(name)]=power
    return P({tuple(e):1})
M,V,Q2,Q3,Q4,PSI,ZETA,X,Z=[monomial(**{name:1}) for name in NAMES]
MI=monomial(m=-1);VI=monomial(v=-1)

class G:
    def __init__(self,re=0,im=0):self.re,self.im=P.cast(re),P.cast(im)
    @staticmethod
    def cast(x):return x if isinstance(x,G) else G(x)
    def __add__(self,x):
        x=G.cast(x);return G(self.re+x.re,self.im+x.im)
    __radd__=__add__
    def __neg__(self):return G(-self.re,-self.im)
    def __sub__(self,x):return self+-G.cast(x)
    def __mul__(self,x):
        x=G.cast(x);return G(self.re*x.re-self.im*x.im,self.re*x.im+self.im*x.re)
    __rmul__=__mul__

def identity(label,left,right=0):
    d=G.cast(left)-right;demand(not d.re.t and not d.im.t,'identity: '+label);LABELS.append(label)
def add(a,b):return [x+y for x,y in zip(a,b)]
def scale(a,x):return [y*x for y in a]
def mul(a,b):return [sum((a[j]*b[k-j] for j in range(k+1)),G()) for k in range(5)]
def cutoff_zero(label,p):
    """Substitute v=2m/(3m+2) and clear all monomial denominators."""
    if not p.t:identity(label,p);return
    top=max(0,max(e[1] for e in p.t))
    lift=max(0,-min(e[0]+e[1] for e in p.t))
    out=P()
    for e,c in p.t.items():
        f=list(e);f[0]=e[0]+e[1]+lift;f[1]=0
        out=out+P({tuple(f):c*F(2)**e[1]})*(3*M+2)**(top-e[1])
    identity(label,out)

def scalar_characteristic():
    c2=V**2/2-V**3;c3=V**2/6-V**3+V**4
    c4=-V**2/24+7*V**3/12-3*V**4/2+V**5
    # Power sums of u_j-v through t^4; sum theta_j=0.
    s1=[G(),G(),G(c2*Q2),G(0,c3*Q3),G(c4*Q4)]
    s2=[G(),G(),G(-V**4*Q2),G(0,-2*V**2*c2*Q3),G((c2**2+2*V**2*c3)*Q4)]
    s3=[G(),G(),G(),G(0,V**6*Q3),G(-3*V**4*c2*Q4)]
    s4=[G(),G(),G(),G(),G(V**8*Q4)]
    elementary=[[G() for _ in range(5)] for _ in range(5)]
    elementary[0][0]=G(1);sums=[None,s1,s2,s3,s4]
    for j in range(1,5):
        combined=[G() for _ in range(5)]
        for ell in range(1,j+1):
            combined=add(combined,scale(mul(elementary[j-ell],sums[ell]),F((-1)**(ell-1),j)))
        elementary[j]=combined
        # Check the Newton recurrence after independent power-sum assembly.
        lhs=scale(elementary[j],j);rhs=[G() for _ in range(5)]
        for ell in range(1,j+1):rhs=add(rhs,scale(mul(elementary[j-ell],sums[ell]),(-1)**(ell-1)))
        for t in range(5):identity('Newton e'+str(j)+' order'+str(t),lhs[t],rhs[t])
    # G(q)=n prod(q-u)-q*d/dq prod(q-u).
    # With q=v+zeta, G/G0=1+sum(-1)^ell e_ell zeta^-ell
    #                      *((ell+1)zeta-(m-ell)v)/(zeta-mv).
    pole=P()
    for j in range(5):pole=pole-monomial(m=-j-1,v=-j-1,zeta=j)
    W=[G() for _ in range(5)]
    for ell in range(1,5):
        factor=(-1)**ell*monomial(zeta=-ell)*((ell+1)*ZETA-(M-ell)*V)*pole
        W=add(W,scale(elementary[ell],factor))
    identity('balanced characteristic W0',W[0]);identity('balanced characteristic W1',W[1])
    logarithm=add(W,scale(mul(W,W),F(-1,2)))
    # Because W starts at t^2, all cubic logarithm terms are O(t^6).
    moments={}
    for ell in (2,3,4):
        coefficients=[]
        for j in range(5):
            z=logarithm[j]
            coefficients.append(G(-ell*z.re.coef('zeta',-ell),-ell*z.im.coef('zeta',-ell)))
        moments[ell]=coefficients
    T2=(M-2)*MI*Q2;T3=(M-3)*MI*Q3
    R=MI*Q2;U=MI*Q4-MI**2*Q2**2;T4=(M-4)*MI*Q4+2*MI**2*Q2**2
    gap=M*V;invgap=MI*VI;NN=M+1
    expected2=c2**2*(T4+2*U+R**2)+2*V**2*c3*(T4+2*U)
    expected2=expected2+2*NN*c2*V**4*invgap*(3*U+R**2)-2*NN*V**8*invgap**2*U+NN**2*V**8*invgap**2*R**2
    expected3=-3*c2*V**4*(T4+U)-3*NN*V**8*invgap*U
    expected4=V**8*T4
    identity('scalar contour M2 fourth',moments[2][4],expected2)
    identity('scalar contour M3 fourth',moments[3][4],expected3)
    identity('scalar contour M4 fourth',moments[4][4],expected4)
    identity('scalar contour M2 second',moments[2][2],-V**4*T2)
    identity('scalar contour M3 third',moments[3][3],G(0,V**6*T3))
    for ell in (2,3,4):
        for j in range(ell):identity('moment lower order '+str((ell,j)),moments[ell][j])
    cR=c2+NN*V**3*MI
    real_square=c2**2*T4+2*c2*cR*U+cR**2*PSI
    fourth=2*c4*Q4-moments[2][4].re*VI/2+real_square*VI/2+moments[3][4].re*VI**2/6-moments[4][4].re*VI**3/8
    desired=M*(M+2)*(-M*(M**2-4*M-4)*Q4-(13*M+18)*Q2**2+9*M**2*(M+2)*PSI)
    cutoff_zero('complete angular F4 from scalar characteristic',fourth*(3*M+2)**5-desired)
    quadratic=2*c2*Q2-moments[2][2].re*VI/2
    cutoff_zero('cutoff cancels balanced quadratic',quadratic)
    cutoff_zero('cutoff c2',4*M*c2+(M-2)*V**3)
    cutoff_zero('cutoff rank-one cR',4*M*cR-3*(M+2)*V**3)
    return {'M2_fourth':moments[2][4].re.record(),'M3_fourth':moments[3][4].re.record(),
            'M4_fourth':moments[4][4].re.record(),'F4_before_cutoff':fourth.record()}

def concentration():
    # Denominators are explicit positive products for m>=4.
    delta=M**2-3*M+3-M*(M-1)*X
    h=(M-3)*Z-2*(M-2)*X+(M-2)
    D=(M-4)*X*M*(M-1)*(M-2)+2*(M-1)*(M-2)-(M-2)**3-M*(M-1)*(M-3)**2*Z
    N=M*(M-1)*(M-2)*X-(2*M-3)*(M-2)-M*(M-1)*(M-3)*Z
    B=(M-2)+M*(M-1)*Z
    L=M*(M-1)*X-(2*M-3)
    BL=B*(M-3)-L*(M-1)
    identity('Gram D representation',D,(M-2)**2*delta-M*(M-1)*(M-3)*h)
    identity('Gram N representation',N,(M-2)*delta-M*(M-1)*h)
    identity('cleared Gram concentration certificate',BL*D+(M-3)*N**2,M*(M-1)*delta*h)
    # Pearson and the reversed-quartic discriminant imply delta>=0.
    identity('combine Pearson and upper scalar bound',
             (M-1)*(M*(M-1)*X-(M**2-3*M+3))/2,
             M*(M-1)*((M-2)*(X-F(1,2))-(M-3)*(X-MI)/2))
    slope=M*(M**2-4*M-4)*(M-2)*(M-3)-9*(M+2)*M*(M-1)
    polynomial=M**4-9*M**3+13*M**2-13*M-6
    identity('optimizer affine slope',slope,M*polynomial)
    identity('m>=8 positive polynomial',polynomial.substitute('m',M+8),M**4+23*M**3+181*M**2+515*M+210)
    # D=0, delta>0 forces N=-delta/(m-3), contradiction to q=0.
    identity('singular-case numerator', (M-3)- (M-2),-1)
    return {'D_numerator':D.record(),'N_numerator':N.record(),
            'lhs_certificate':(BL*D+(M-3)*N**2).record(),
            'certificate':(M*(M-1)*delta*h).record()}

def finite_matrix_checks():
    def matmul(A,B):
        return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
    def trace(A):return sum(A[i][i] for i in range(len(A)))
    profiles=0
    for m in range(3,13):
        vectors=[]
        for r in range(1,m):vectors.append([F(m-r)]*r+[F(-r)]*(m-r))
        vectors += [[F(1),F(-1)]+[F(0)]*(m-2),[F(j) for j in range(1,m)]+[F(-m*(m-1),2)]]
        for profile_index,theta in enumerate(vectors):
            Pm=[[F(int(i==j))-F(1,m) for j in range(m)] for i in range(m)]
            Theta=[[theta[i] if i==j else F(0) for j in range(m)] for i in range(m)]
            A=matmul(matmul(Pm,Theta),Pm);Ak=A
            powers={k:sum(x**k for x in theta) for k in range(1,5)};demand(powers[1]==0,'finite balance')
            expected={1:F(0),2:F(m-2,m)*powers[2],3:F(m-3,m)*powers[3],4:F(m-4,m)*powers[4]+F(2,m*m)*powers[2]**2}
            for k in range(1,5):
                demand(trace(Ak)==expected[k],'finite direct-matrix trace');Ak=matmul(Ak,A)
            coupling=sum(theta[i]*A[i][j]*theta[j] for i in range(m) for j in range(m))/m
            A2=matmul(A,A);second=sum(theta[i]*A2[i][j]*theta[j] for i in range(m) for j in range(m))/m
            demand(coupling==powers[3]/m and second==powers[4]/m-powers[2]**2/(m*m),'finite direct coupling')
            Aw=[sum(A[i][j]*theta[j] for j in range(m)) for i in range(m)]
            if profile_index<m-1:
                r=profile_index+1
                demand(Aw==[(m-2*r)*x for x in theta],'two-block one active weight')
            elif profile_index==m-1:
                A2w=[sum(A[i][j]*Aw[j] for j in range(m)) for i in range(m)]
                demand(coupling==0 and A2w==[F(m-2,m)*x for x in theta],
                       'moving-pair two equal active weights')
            Xv=powers[4]/powers[2]**2;zv=powers[3]**2/powers[2]**3
            demand(Xv<=F(1,2)+F(m-3,2*(m-2))*zv and zv<=Xv-F(1,m),'finite moment inequalities')
            profiles+=1
    return profiles

def rational_geometry():
    tests={
      'small window delta':F(14,25)/56==F(1,100),
      'skewness lower':F(9,14)-F(12,5)*F(1,100)==F(1083,1750),
      'root gap lower':F(1083,1750)+F(1,2)>F(11,10),
      'skewness rational':F(1083,1750)>F(31,40)**2,
      'root gap upper':F(8,7)<F(15,14)**2,
      'root count imbalance':F(448,11)*F(1,100)<F(4,9),
      'zero positive root count':F(14,15)>F(2,3),
      'multiple positive root count':F(67,70)>F(2,3),
      'projection scale':F(7,8)*F(11,10)>F(7,8)**2,
      'coarse geometry':F(8,7)*F(56,11)==F(64,11) and F(64,11)<6,
      'c from coarse distance':1-F(6,2)*F(1,100)==F(97,100),
      'tau bound':1-F(97,100)**2<F(3,50),
      'tau square-root majorant':F(3,50)<F(1,16),
      'contrast coordinate':56>7**2,
      'contrast fourth coefficient':2*F(43,56)-6*F(1,56)==F(10,7),
      'contrast fourth tail':F(43,56)+1-6*F(1,56)==F(93,56),
      'contrast lower coefficient':F(10,7)-F(1,7)-F(93,56)*F(3,50)==F(3321,2800),
      'contrast coercivity':F(3321,2800)>F(7,6),
      'distance exact conversion':2/(1+F(97,100))*F(6,7)==F(1200,1379),
      'improved distance constant':F(1200,1379)<F(7,8),
      'energy distance conversion':F(7,8)/56==F(1,64),
      'improvement factor':F(1,64)/F(3,28)==F(7,48)}
    for label,ok in tests.items():demand(ok,label);LABELS.append('geometry '+label)
    return len(tests)

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write',action='store_true');args=parser.parse_args()
    start=time.monotonic();scalar=scalar_characteristic();gram=concentration();profiles=finite_matrix_checks();geometry=rational_geometry()
    p=F(10985,33554432);maxvalue=204*p
    p7=F(9*23**3,256*7**7)
    singleton7=p7*(7*17*F(31,42)+109-81)
    pair7=p7*(7*17*F(1,2)+109-F(81,2))
    demand(pair7>singleton7,'m=7 is outside singleton optimizer theorem')
    LABELS.append('m=7 excluded optimizer range control')
    demand(maxvalue==F(560235,8388608) and 60*p==F(164775,8388608),'degree9 extrema')
    # Universal certificate mutations, not numerical samples.
    bad=0
    lhs=P({tuple(row[:NV]):F(row[NV],row[NV+1]) for row in gram['lhs_certificate']})
    rhs=P({tuple(row[:NV]):F(row[NV],row[NV+1]) for row in gram['certificate']})
    for changed in (rhs+1,rhs-1,2*rhs,-rhs,rhs+M,rhs+X):
        if (lhs-changed).t:bad+=1
    demand(bad==6,'mutation controls')
    symbolic={'scalar_characteristic':scalar,'Gram_certificate':gram}
    output={'reviewer':'six-reviewer-3','role':'independent mathematical reviewer',
            'status':'SCALAR CHARACTERISTIC, SPECTRAL CONCENTRATION, OPTIMIZER AND IMPROVED GEOMETRY VERIFIED',
            'symbolic_checks':len(LABELS),'finite_direct_matrix_profiles':profiles,
            'rational_geometry_checks':geometry,'rejected_mutations':bad,
            'coefficient_and_certificate_sha256':sha256(json.dumps(symbolic,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
            'identity_labels_sha256':sha256(('\n'.join(LABELS)+'\n').encode()).hexdigest(),
            'degree9_maximum':[maxvalue.numerator,maxvalue.denominator],
            'degree9_minimum':[(60*p).numerator,(60*p).denominator],
            'improved_squared_distance_bound':'distance^2 <= delta/(64*p), for delta<=14*p/25, p=10985/33554432',
            'squared_distance_coefficient_ratio_to_target':[7,48],
            'excluded_m7_control':{'singleton':[singleton7.numerator,singleton7.denominator],
                                    'moving_pair':[pair7.numerator,pair7.denominator]},
            'analytic_bridge_formalized':False}
    raw=json.dumps(output,sort_keys=True,indent=2)+'\n'
    if args.write:(HERE/'expected.json').write_text(raw)
    else:demand(json.loads((HERE/'expected.json').read_text())==output,'expected manifest differs')
    print(raw,end='');print('Elapsed seconds:',round(time.monotonic()-start,3))

if __name__=='__main__':main()
