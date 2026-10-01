"""Exact three-pair split instability evidence. Actual six-sendov-3, researcher.

Coefficient evidence only; analytic bridges are in PROOF.md.
Ring arithmetic adapts this author's published8315/8364 Laurent/jet mechanism.
"""
from fractions import Fraction as F
import json


class R:
    """Q[v,v^-1,rho]; nonzero monomials alone are inverted."""
    def __init__(self,x=0):
        if isinstance(x,R):x=x.d
        elif isinstance(x,(int,F)):x={(0,0):F(x)}
        self.d={tuple(k):F(c) for k,c in x.items() if c}
    def __add__(self,x):
        if isinstance(x,J):return NotImplemented
        x=R(x);d=dict(self.d)
        for k,c in x.d.items():d[k]=d.get(k,F(0))+c
        return R(d)
    __radd__=__add__
    def __neg__(self):return R({k:-c for k,c in self.d.items()})
    def __sub__(self,x):
        if isinstance(x,J):return NotImplemented
        return self+-R(x)
    def __rsub__(self,x):return R(x)+-self
    def __mul__(self,x):
        if isinstance(x,J):return NotImplemented
        x=R(x);d={}
        for k,c in self.d.items():
            for h,a in x.d.items():
                kh=(k[0]+h[0],k[1]+h[1]);d[kh]=d.get(kh,F(0))+c*a
        return R(d)
    __rmul__=__mul__
    def inverse(self):
        if len(self.d)!=1:raise RuntimeError('only monomial inversion')
        k,c=next(iter(self.d.items()));return R({(-k[0],-k[1]):1/c})
    def __truediv__(self,x):
        if isinstance(x,J):return NotImplemented
        return self*R(x).inverse()
    def __rtruediv__(self,x):return R(x)*self.inverse()
    def __pow__(self,n):
        if n<0:return self.inverse()**(-n)
        out=R(1)
        for _ in range(n):out*=self
        return out
    def at_rho(self,x):
        out=R()
        for (i,j),c in self.d.items():out+=R({(i,0):c*x**j})
        return out
    def rho_coefficient(self,n):return R({(i,0):c for (i,j),c in self.d.items() if j==n})
    def wire(self):return [[list(k),[c.numerator,c.denominator]] for k,c in sorted(self.d.items())]


ORDER=5
class J:
    """Energy jets modulo e^6; objective evidence uses only degree four."""
    def __init__(self,x=0):
        if isinstance(x,J):x=x.c
        elif isinstance(x,(int,F,R)):x=[R(x)]
        self.c=[R(x[i]) if i<len(x) else R() for i in range(ORDER+1)]
    def __add__(self,x):
        x=J(x);return J([a+b for a,b in zip(self.c,x.c)])
    __radd__=__add__
    def __neg__(self):return J([-c for c in self.c])
    def __sub__(self,x):return self+-J(x)
    def __rsub__(self,x):return J(x)+-self
    def __mul__(self,x):
        x=J(x);return J([sum((self.c[k]*x.c[n-k] for k in range(n+1)),R()) for n in range(ORDER+1)])
    __rmul__=__mul__
    def inverse(self):
        c=[self.c[0].inverse()]
        for n in range(1,ORDER+1):c.append(-c[0]*sum((self.c[k]*c[n-k] for k in range(1,n+1)),R()))
        return J(c)
    def __truediv__(self,x):return self*J(x).inverse()
    def __rtruediv__(self,x):return J(x)*self.inverse()
    def __pow__(self,n):
        out=J(1)
        for _ in range(n):out*=self
        return out
    def divide_e(self):
        if self.c[0].d:raise RuntimeError('not divisible by energy')
        return J(self.c[1:]+[R()])
    def sqrt(self,constant):
        c=[R(constant)]
        if (c[0]*c[0]-self.c[0]).d:raise RuntimeError('wrong square-root constant')
        for n in range(1,ORDER+1):c.append((self.c[n]-sum((c[k]*c[n-k] for k in range(1,n)),R()))/(2*c[0]))
        out=J(c)
        if any(c.d for c in (out*out-self).c):raise RuntimeError('full square-root jet residual')
        return out
    def wire(self):return [c.wire() for c in self.c]


class Field:
    """Q[v]/(239v^2+184v-208); its real branch is isolated separately."""
    def __init__(self, a=0, b=0):
        if isinstance(a, Field):
            a, b = a.a, a.b
        self.a, self.b = F(a), F(b)

    def __add__(self, x):
        x = Field(x)
        return Field(self.a + x.a, self.b + x.b)

    __radd__ = __add__

    def __neg__(self):
        return Field(-self.a, -self.b)

    def __sub__(self, x):
        return self + -Field(x)

    def __rsub__(self, x):
        return Field(x) + -self

    def __mul__(self, x):
        x = Field(x)
        return Field(self.a * x.a + self.b * x.b * F(208, 239),
                     self.a * x.b + self.b * x.a
                     - self.b * x.b * F(184, 239))

    __rmul__ = __mul__

    def inverse(self):
        conj = Field(self.a - self.b * F(184, 239), -self.b)
        norm = self * conj
        if norm.b or not norm.a:
            raise ValueError('invalid field norm')
        return Field(conj.a / norm.a, conj.b / norm.a)

    def __truediv__(self, x):
        return self * Field(x).inverse()

    def __rtruediv__(self, x):
        return Field(x) * self.inverse()

    def __pow__(self, n):
        if n < 0:
            return self.inverse() ** (-n)
        out = Field(1)
        for _ in range(n):
            out *= self
        return out

    def wire(self):
        return [[x.numerator, x.denominator] for x in (self.a, self.b)]

    def interval(self, lo, hi):
        return (self.a + self.b * lo, self.a + self.b * hi) if self.b >= 0 \
            else (self.a + self.b * hi, self.a + self.b * lo)


class G:
    """Full Laurent polynomials in v, with independent e,f,g parameters."""
    def __init__(self,x=0):
        if isinstance(x,G):x=x.d
        elif isinstance(x,(int,F)):x={(0,0,0,0):F(x)}
        self.d={tuple(k):F(c) for k,c in x.items() if c}
        if any(len(k)!=4 for k in self.d):raise RuntimeError('wrong full-polynomial dimension')
    def __add__(self,x):
        x=G(x);d=dict(self.d)
        for k,c in x.d.items():d[k]=d.get(k,F(0))+c
        return G(d)
    __radd__=__add__
    def __neg__(self):return G({k:-c for k,c in self.d.items()})
    def __sub__(self,x):return self+-G(x)
    def __rsub__(self,x):return G(x)+-self
    def __mul__(self,x):
        x=G(x);d={}
        for k,c in self.d.items():
            for h,a in x.d.items():
                kh=tuple(ki+hi for ki,hi in zip(k,h));d[kh]=d.get(kh,F(0))+c*a
        return G(d)
    __rmul__=__mul__
    def inverse(self):
        if len(self.d)!=1:raise RuntimeError('only monomial inversion')
        k,c=next(iter(self.d.items()));return G({tuple(-ki for ki in k):1/c})
    def __truediv__(self,x):return self*G(x).inverse()
    def __rtruediv__(self,x):return G(x)*self.inverse()
    def __pow__(self,n):
        if n<0:return self.inverse()**(-n)
        out=G(1)
        for _ in range(n):out*=self
        return out
    def diff(self,axis):
        d={}
        for k,c in self.d.items():
            if k[axis]:
                h=list(k);h[axis]-=1;d[tuple(h)]=c*k[axis]
        return G(d)
    def at_zero(self,axis):return G({k:c for k,c in self.d.items() if k[axis]==0})
    def wire(self):return [[list(k),[c.numerator,c.denominator]] for k,c in sorted(self.d.items())]


def certify():
    records={};counts={'identities':0,'signs':0,'damaged_math':0,
                       'reducing_basis_inputs':5,'reducing_full_vectors':30,
                       'angular_compression_inputs':8,'angular_compression_entries':512}
    def zero(name,value,degree=ORDER):
        if isinstance(value,J):ok=not any(c.d for c in value.c[:degree+1])
        elif isinstance(value,Field):ok=not(value.a or value.b)
        elif isinstance(value,list):ok=all(x==0 for x in value)
        else:ok=not value.d
        if not ok:raise RuntimeError('nonzero complete identity: '+name)
        counts['identities']+=1
    def record(name,value):
        if name in records:raise RuntimeError('duplicate evidence record')
        records[name]=value
    def mulpoly(left,right,scalar):
        out=[scalar() for _ in range(len(left)+len(right)-1)]
        for i,x in enumerate(left):
            for j,y in enumerate(right):out[i+j]+=x*y
        return out
    def addpoly(left,right,scalar):
        return [(left[i] if i<len(left) else scalar())+(right[i] if i<len(right) else scalar())
                for i in range(max(len(left),len(right)))]

    # Independent e,f,g: no energy truncation in the actual three-pair model.
    vg=G({(1,0,0,0):1});eg=G({(0,1,0,0):1})
    fg=G({(0,0,1,0):1});gg=G({(0,0,0,1):1});ag=1/vg-1;bg=1-ag*ag
    energies=[eg-fg-gg,fg,gg];pairs=[]
    for i,energy in enumerate(energies):
        dx=4*vg**4+2*ag*vg*vg*energy
        product=vg*vg+ag*energy/2;summation=2*vg-bg*energy/2
        raw=[dx,-(2*dx/vg-2*energy),dx/(vg*vg)-2*ag*energy]
        expected=[4*vg*vg*product,-4*vg*vg*summation,4*vg*vg]
        for k in range(3):zero('full actual pair transform '+str((i,k)),raw[k]-expected[k])
        zero('full actual pair energy '+str(i),2*product-2*vg*summation+2*vg*vg-energy)
        pairs.append([energy/2,energy*bg/2,G(1)])
    zero('full total original energy',sum(energies,G())-eg)
    root=[G(),G()]+mulpoly(mulpoly(pairs[0],pairs[1],G),pairs[2],G)
    char=[(9-k)*root[k]-vg*(k+1)*(root[k+1] if k+1<len(root) else G())
          for k in range(9)]
    d2=eg*(fg+gg)-fg*fg-gg*gg-fg*gg;d3=(eg-fg-gg)*fg*gg
    k=[G(F(1,2)),bg/2]
    c3=[-3*vg*eg,(7*ag-4)*eg/2,-8*vg+bg*eg,G(1)]
    j=[-vg,5*(2*ag-1)/4,bg*(3*ag+1)/2,3*bg*bg/4]
    inside=addpoly([G(),9*k[0],9*k[1]],[-x for x in mulpoly([vg,G(1)],[G(1),5*bg/2],G)],G)
    l4=mulpoly(mulpoly(k,k,G),inside,G)
    c7=addpoly([G()]*4+c3,[G(),G()]+[d2*x for x in j],G)
    c7=addpoly(c7,[d3*x for x in l4],G)
    for i in range(9):zero('full original critical coefficient '+str(i),char[i]-(G() if i==0 else c7[i-1]))
    record('full_eight_original_reciprocal',[x.wire() for x in root])
    record('full_eight_critical_reciprocal',[x.wire() for x in char])
    record('complete_septic',[x.wire() for x in c7])
    record('complete_L4',[x.wire() for x in l4])

    d=fg*(eg-fg)
    c5=[d*j[0],d*j[1],c3[0]+d*j[2],c3[1]+d*j[3],c3[2],G(1)]
    dg=[x.diff(3).at_zero(3) for x in c7]
    pi=G(F(1,4));sigma=(8*ag+1)/(16*vg)
    numerator=addpoly(dg,[-pi*x for x in c5],G)
    numerator=addpoly(numerator,[G()]+[sigma*x for x in c5],G)
    for i in [0,1]:zero('full new-pair derivative divisibility '+str(i),numerator[i])
    l5=numerator[2:]
    derivative=addpoly([pi*x for x in c5],[G()]+[-sigma*x for x in c5],G)
    derivative=addpoly(derivative,[G(),G()]+l5,G)
    for i in range(8):zero('full g derivative characteristic '+str(i),derivative[i]-dg[i])
    zero('full L4 constant',l4[0]+vg/4)
    zero('full L4 linear',l4[1]-(9*ag-2)/8)
    record('new_pair_product_derivative',pi.wire())
    record('new_pair_sum_derivative',sigma.wire())
    record('full_external_quintic_derivative',[x.wire() for x in l5])

    # Verify the exact rho=0 continuation, in untruncated e, against8315.
    sv=(16*ag-7)/(36*vg);uv=sv-sigma;pv=G(F(1,12))
    lzero=[x.at_zero(2) for x in l5]
    ap=lzero[4]+uv
    bp=lzero[3]+uv*c3[2]-pv
    cp=lzero[2]+uv*c3[1]-pv*c3[2]
    fullzero=addpoly(mulpoly([pv,-uv],c3,G),[G(),G(),cp,bp,ap],G)
    for i in range(5):zero('full rho0 factor continuation '+str(i),fullzero[i]-lzero[i])
    old_ap=sv;old_bp=eg*j[3]+sv*c3[2]-F(1,3)
    old_cp=eg*j[2]+sv*c3[1]-c3[2]/3
    for i,(actual,want) in enumerate([(ap,old_ap),(bp,old_bp),(cp,old_cp)]):
        zero('exact rho0 cubic derivative '+str(i),actual-want)
    zero('exact rho0 summed auxiliary product',pi+pv-F(1,3))
    zero('exact rho0 summed auxiliary sum',sigma+uv-sv)

    # Rescaled f=e^2rho jets; reused openly from the author's8364 arithmetic.
    v=R({(1,0):1});rho=R({(0,1):1});a=1/v-1;b=1-a*a;e=J([0,1]);f=e*e*rho
    k1=(7*a-4)/2;A=-8*v+b*e;B=k1*e;C=-3*v*e
    J3,J2,J1,J0=3*b*b/4,b*(3*a+1)/2,5*(2*a-1)/4,-v
    D=f*(e-f);s=(16*a-7)/(36*v)
    S=J(rho*s);P=J(rho/3)
    def factors():
        Ac=A+e*e*S
        Bc=B+D*J3+e*e*S*Ac-e*e*P
        Cc=C+D*J2+e*e*S*Bc-e*e*P*Ac
        return Ac,Bc,Cc
    def equations():
        Ac,Bc,Cc=factors()
        return P*Cc.divide_e()-(rho-e*rho*rho)*J0, \
               -S*Cc.divide_e()+P*Bc.divide_e()-(rho-e*rho*rho)*J1
    for n in range(1,3):
        fp,_=equations();P.c[n]=fp.c[n]/(3*v)
        _,fs=equations();S.c[n]=-fs.c[n]/(3*v)
    for i,residual in enumerate(equations()):zero('base rescaled factor equation '+str(i),residual,2)
    Ac,Bc,Cc=factors();s2=e*e*S;p2=e*e*P
    C5=[D*J0,D*J1,C+D*J2,B+D*J3,A,J(1)]
    for i,(actual,want) in enumerate(zip(mulpoly([p2,-s2,J(1)],[Cc,Bc,Ac,J(1)],J),C5)):
        zero('whole base factor coefficient '+str(i),actual-want)
    k=[J(F(1,2)),J(b/2)]
    inside=addpoly([J(),9*k[0],9*k[1]],[-x for x in mulpoly([J(v),J(1)],[J(1),J(5*b/2)],J)],J)
    L4=mulpoly(mulpoly(k,k,J),inside,J)
    pi1=R(F(1,4));sigma1=(8*a+1)/(16*v)
    numerator=addpoly([-pi1*x for x in C5],[J()]+[sigma1*x for x in C5],J)
    numerator=addpoly(numerator,[J(),J()]+[(e-f)*x for x in [J(J0),J(J1),J(J2),J(J3)]],J)
    numerator=addpoly(numerator,[D*x for x in L4],J)
    for i in [0,1]:zero('rescaled g derivative divisibility '+str(i),numerator[i])
    L5=numerator[2:]
    U=J();V=J()
    def derivative_factors():
        Ap=L5[4]+U
        Bp=L5[3]+s2*Ap+U*Ac-V
        Cp=L5[2]+s2*Bp-p2*Ap+U*Bc-V*Ac
        return Ap,Bp,Cp
    def derivative_equations():
        Ap,Bp,Cp=derivative_factors()
        return (p2*Cp+V*Cc-L5[0]).divide_e(), \
               (-s2*Cp+p2*Bp-U*Cc+V*Bc-L5[1]).divide_e()
    for n in range(3):
        rp,_=derivative_equations();V.c[n]=rp.c[n]/(3*v)
        _,rs=derivative_equations();U.c[n]=-rs.c[n]/(3*v)
    for i,residual in enumerate(derivative_equations()):zero('existing-pair derivative equation '+str(i),residual,2)
    zero('existing pair limiting product derivative',V.c[0]-F(1,12))
    zero('existing pair limiting sum derivative',U.c[0]-(s-sigma1))
    zero('limiting derivative Jacobian',(-3*v)*(3*v)+9*v*v)
    Ap,Bp,Cp=derivative_factors()
    whole=addpoly(mulpoly([V,-U],[Cc,Bc,Ac,J(1)],J),mulpoly([p2,-s2,J(1)],[Cp,Bp,Ap],J),J)
    for i,(actual,want) in enumerate(zip(whole,L5)):zero('whole derivative factor coefficient '+str(i),actual-want,3)
    record('existing_pair_sum_derivative_through2',U.wire()[:3])
    record('existing_pair_product_derivative_through2',V.wire()[:3])
    def cubic(q):
        r=q-v;return r**3+Ac*r*r+Bc*r+Cc
    qfar=J(9*v)
    for n in range(1,3):qfar.c[n]=-cubic(qfar).c[n]/(64*v*v)
    zero('far root through2',cubic(qfar),2)
    r=qfar-v
    qprime=-(Ap*r*r+Bp*r+Cp)/(3*r*r+2*Ac*r+Bc)
    zero('far derivative whole residual',qprime*(3*r*r+2*Ac*r+Bc)+(Ap*r*r+Bp*r+Cp),2)
    external_product=-((-v)**3+Ac*v*v-Bc*v+Cc)
    external_product_prime=-(Ap*v*v-Bp*v+Cp)
    main=(external_product/qfar).sqrt(v)
    aux=(v*v+v*s2+p2).sqrt(v)
    H4=sigma1+pi1/v+(v*U+V)/aux+qprime+main*(external_product_prime/external_product-qprime/qfar)
    h1=(208-184*v-239*v*v)/(2304*v**5)
    h2=(-245888+771984*v-786792*v*v+246931*v**3)/(4718592*v**8)
    gamma=(4+v)**2/(10368*v**5)
    cross=(-3856+3256*v+4295*v*v)/(41472*v**5)
    zero('zero constant H4',H4.c[0])
    zero('whole linear energy H4',H4.c[1]-h1)
    zero('whole quadratic energy H4',H4.c[2]-h2-rho*cross)
    zero('cross coefficient identity',cross+h1+F(7,4)*gamma)
    record('H4_energy_through2',H4.wire()[:3])
    record('rho_cross_coefficient',cross.wire())
    record('far_root_derivative_through2',qprime.wire()[:3])
    record('far_root_through2',qfar.wire()[:3])

    vv=Field(0,1);lo,hi=F(3,5),F(5,8)
    def threshold(x):return 239*x*x+184*x-208
    if not threshold(lo)<0<threshold(hi):raise RuntimeError('positive branch not isolated')
    counts['signs']+=1
    for _ in range(64):
        mid=(lo+hi)/2
        if threshold(mid)<0:lo=mid
        elif threshold(mid)>0:hi=mid
        else:raise RuntimeError('unexpected rational root')
    def endpoint(value):
        if any(j for i,j in value.d):raise RuntimeError('endpoint depends on rho')
        return sum((Field(c)*vv**i for (i,j),c in value.d.items()),Field())
    def positive(name,value):
        bounds=Field(value).interval(lo,hi)
        if bounds[0]<=0:raise RuntimeError('strict sign not certified: '+name)
        record('positive_'+name,[[x.numerator,x.denominator] for x in bounds])
        counts['signs']+=1
    h2minus=endpoint(h2);gminus=endpoint(gamma);mu=endpoint(cross)
    sqrt101=(239*vv+92)/24;lam=sqrt101/(48*vv**3)
    zero('sqrt101 field identity',sqrt101*sqrt101-101)
    zero('h1 endpoint zero',endpoint(h1))
    zero('negative endpoint cross',mu+F(7,4)*gminus)
    beta=-h2minus/(2*gminus)
    zero('branch relative derivative coefficient',lam-lam*mu/(2*gminus)-F(15,8)*lam)
    zero('branch endpoint derivative coefficient',h2minus+mu*beta-F(15,8)*h2minus)
    positive('lambda',lam);positive('gamma',gminus)
    positive('minus_h2',-h2minus);positive('relative_saddle_coefficient',F(15,8)*lam)
    positive('endpoint_descent_coefficient',-F(15,8)*h2minus)
    record('relative_branch_coefficient',(F(15,8)*lam).wire())
    record('endpoint_H4_coefficient',(F(15,8)*h2minus).wire())
    record('positive_threshold_interval',[[x.numerator,x.denominator] for x in [lo,hi]])

    # Whole left/right vectors:5 inputs span independent external u1..u4,v.
    reducing=[]
    for index in range(5):
        original=[F(0)]*8
        if index<4:original[index]=F(1)
        else:original[4:]=[F(1)]*4
        matrix=[[original[i]*(int(i==j)+1) for j in range(8)] for i in range(8)]
        for direction in range(3):
            vector=[F(0)]*8;vector[4+direction]=F(1);vector[7]=F(-1)
            right=[sum((matrix[i][j]*vector[j] for j in range(8)),F(0)) for i in range(8)]
            left=[sum((vector[i]*matrix[i][j] for i in range(8)),F(0)) for j in range(8)]
            want=vector if index==4 else [F(0)]*8
            zero('complete right reducing vector '+str((index,direction)),[x-y for x,y in zip(right,want)])
            zero('complete left reducing vector '+str((index,direction)),[x-y for x,y in zip(left,want)])
            reducing.append({'input':index,'direction':direction,'right':[[x.numerator,x.denominator] for x in right],
                             'left':[[x.numerator,x.denominator] for x in left]})
    record('complete_reducing_vectors',reducing)
    projector=[[F(int(i==j))-F(1,4) if i>=4 and j>=4 else F(0) for j in range(8)] for i in range(8)]
    def matmul(left,right):
        return [[sum((left[i][k]*right[k][j] for k in range(8)),F(0)) for j in range(8)] for i in range(8)]
    squared=matmul(projector,projector)
    zero('full orthogonal projector idempotence',[squared[i][j]-projector[i][j] for i in range(8) for j in range(8)])
    compressions=[]
    for index in range(8):
        derivative=[[F(int(i==index))*(int(i==j)+1) for j in range(8)] for i in range(8)]
        diagonal=[[F(int(i==index and i==j)) for j in range(8)] for i in range(8)]
        actual=matmul(matmul(projector,derivative),projector)
        want=matmul(matmul(projector,diagonal),projector)
        zero('full first angular compression '+str(index),[actual[i][j]-want[i][j] for i in range(8) for j in range(8)])
        zero('full symmetric compression '+str(index),[actual[i][j]-actual[j][i] for i in range(8) for j in range(8)])
        if index<4:zero('external angular compression zero '+str(index),[x for row in actual for x in row])
        compressions.append([[[x.numerator,x.denominator] for x in row] for row in actual])
    record('full_angular_compressions',compressions)

    damages=[char[1]-c7[0]+eg,dg[0]-pi*c5[0]+fg,
             H4.c[2]-h2, H4.c[1]-2*h1,
             cross+h1+F(3,2)*gamma,
             mu+2*gminus,lam-lam*mu/(2*gminus)-F(7,8)*lam]
    for value in damages:
        if isinstance(value,J):nonzero=any(c.d for c in value.c)
        elif isinstance(value,Field):nonzero=bool(value.a or value.b)
        else:nonzero=bool(value.d)
        if not nonzero:raise RuntimeError('damaged mathematics passed')
        counts['damaged_math']+=1
    return {'schema':'sendov-four-block-split-instability-v1','agent':'six-sendov-3','role':'researcher',
            'base_factor_jet_order':5,'derivative_jet_order':2,'counts':counts,'records':records,
            'trust_boundary':'exact actual-polynomial/coefficient/sign evidence; analytic continuation and angular saddle proof in PROOF.md'}


def main():
    import argparse,hashlib
    from pathlib import Path
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fixture',type=Path,default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--write-fixture',type=Path,help='explicit generation; skips fixture comparison')
    args=parser.parse_args();result=certify()
    if args.write_fixture is None:
        if not args.fixture.is_file():raise RuntimeError('mandatory complete fixture missing')
        if json.loads(args.fixture.read_text())!=result:raise RuntimeError('complete mandatory fixture differs')
    else:args.write_fixture.write_text(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n')
    digest=hashlib.sha256(json.dumps(result['records'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
    print(json.dumps({'agent':'six-sendov-3','role':'researcher','schema':result['schema'],'counts':result['counts'],
                      'record_count':len(result['records']),'record_sha256':digest,'status':result['trust_boundary']},sort_keys=True))


if __name__=='__main__':main()
