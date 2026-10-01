"""Exact two-pair bifurcation evidence. Actual six-sendov-3, researcher.

Coefficient evidence only; analytic bridges are in PROOF.md.
Ring arithmetic adapts this author's published8315 Laurent/jet mechanism.
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


def certify():
    records={}
    counts={'identities':0,'signs':0,'damaged_math':0,
            'reducing_basis_inputs':5,'reducing_full_vectors':30}
    def zero(name,value,degree=ORDER):
        if isinstance(value,J):ok=not any(c.d for c in value.c[:degree+1])
        elif isinstance(value,Field):ok=not(value.a or value.b)
        elif isinstance(value,list):ok=all(x==0 for x in value)
        else:ok=not value.d
        if not ok:raise RuntimeError('nonzero complete identity: '+name)
        counts['identities']+=1
    def record(name,value):
        if name in records:raise RuntimeError('duplicate evidence name')
        records[name]=value
    def mulpoly(left,right):
        out=[J() for _ in range(len(left)+len(right)-1)]
        for i,x in enumerate(left):
            for j,y in enumerate(right):out[i+j]+=x*y
        return out
    v=R({(1,0):1});rho=R({(0,1):1});a=1/v-1;b=1-a*a;e=J([0,1])
    f=e*e*rho
    energies=(e-f,f)
    pair_polynomials=[]
    for index,s_energy in enumerate(energies):
        dx=4*v**4+2*a*v*v*s_energy
        h=v*v+a*s_energy/2;j=2*v-b*s_energy/2
        raw=[dx,-(2*dx/v-2*s_energy),dx/(v*v)-2*a*s_energy]
        expected=[4*v*v*h,-4*v*v*j,J(4*v*v)]
        for k in range(3):zero('actual cleared reciprocal pair '+str((index,k)),raw[k]-expected[k])
        zero('exact pair energy '+str(index),2*h-2*v*j+2*v*v-s_energy)
        pair_polynomials.append([s_energy/2,s_energy*b/2,J(1)])
    zero('total exact energy',sum(energies,J())-e)
    root=[J()]*4+mulpoly(*pair_polynomials)
    # The reciprocal root polynomial has exact energy degree at most four.
    if any(c.d for x in root for c in x.c[5:]):raise RuntimeError('unexpected root energy degree')
    characteristic=[(9-k)*root[k]-v*(k+1)*(root[k+1] if k+1<len(root) else J())
                    for k in range(len(root))]
    k1=(7*a-4)/2
    A=-8*v+b*e;B=k1*e;C=-3*v*e
    J3,J2,J1,J0=3*b*b/4,b*(3*a+1)/2,5*(2*a-1)/4,-v
    D=e**3*rho-e**4*rho*rho
    target=[D*J0,D*J1,C+D*J2,B+D*J3,A,J(1)]
    expected=[J()]*3+target
    for k in range(9):zero('full eight-critical coefficient '+str(k),characteristic[k]-expected[k])
    record('full_eight_original_reciprocal', [x.wire() for x in root])
    record('full_eight_critical_reciprocal', [x.wire() for x in characteristic])
    record('rescaled_quintic', [x.wire() for x in target])

    s=(16*a-7)/(36*v)
    S=J(rho*s);P=J(rho/3)
    def factors():
        Ac=A+e*e*S
        Bc=B+D*J3+e*e*S*Ac-e*e*P
        Cc=C+D*J2+e*e*S*Bc-e*e*P*Ac
        return Ac,Bc,Cc
    def equations():
        Ac,Bc,Cc=factors();dc=Cc.divide_e();db=Bc.divide_e()
        return P*dc-(rho-e*rho*rho)*J0,-S*dc+P*db-(rho-e*rho*rho)*J1
    for n in range(1,3):
        fp,_=equations();P.c[n]=fp.c[n]/(3*v)
        _,fs=equations();S.c[n]=-fs.c[n]/(3*v)
    fp,fs=equations()
    for index,eq in enumerate((fp,fs)):
        zero('coefficient IFT residual '+str(index),eq,2)
    zero('limiting IFT determinant',(-3*v)*(3*v)-(-9*v*v))
    Ac,Bc,Cc=factors()
    factored=mulpoly([e*e*P,-e*e*S,J(1)],[Cc,Bc,Ac,J(1)])
    for k in range(6):zero('whole factorization through energy5 '+str(k),factored[k]-target[k])
    record('S_energy_jet_through2',S.wire()[:3])
    record('P_energy_jet_through2',P.wire()[:3])
    record('whole_factored_quintic_through5',[x.wire() for x in factored])

    def cubic(q):
        r=q-v;return r**3+Ac*r*r+Bc*r+Cc
    qfar=J(9*v)
    for n in range(1,5):qfar.c[n]=-cubic(qfar).c[n]/(64*v*v)
    zero('far root full residual through degree4',cubic(qfar),4)
    def sqrt4(value,constant):
        coeffs=[R(constant)]
        zero('square root constant',coeffs[0]*coeffs[0]-value.c[0])
        for n in range(1,5):
            coeffs.append((value.c[n]-sum((coeffs[k]*coeffs[n-k] for k in range(1,n)),R()))/(2*coeffs[0]))
        result=J(coeffs)
        zero('complete square-root residual through degree4',result*result-value,4)
        return result
    external_product=-((-v)**3+Ac*v*v-Bc*v+Cc)
    main=sqrt4(external_product/qfar,v)
    aux=sqrt4(v*v+v*e*e*S+e*e*P,v)
    objective=3*v+2*aux+qfar+2*main
    gap=J([x-x.at_rho(0) for x in objective.c])
    for n in range(3):zero('zero lower gap energy coefficient '+str(n),gap.c[n])
    h1=(208-184*v-239*v*v)/(2304*v**5)
    h2=(-245888+771984*v-786792*v*v+246931*v**3)/(4718592*v**8)
    gamma=(4+v)**2/(10368*v**5)
    qcoef=(-1840+1672*v+2153*v*v)/(20736*v**5)
    zero('whole cubic energy gap coefficient',gap.c[3]-rho*h1)
    zero('whole fourth energy gap coefficient',gap.c[4]-rho*h2-rho*rho*qcoef)
    zero('quadratic coefficient normalization',qcoef-(gamma-h1))
    # Here rho is temporarily the whole-family fraction u=f/e.
    # The imported complete angular loss has this cleared numerator.
    delta=9-32*rho+32*rho*rho
    Cd=(4+v)**2/(8192*v**5)
    angular_numerator=64*Cd*rho*rho*(1-rho)**2/9
    barrier_numerator=gamma*rho**3*(14-23*rho)
    zero('whole-family denominator floor',delta-(1+32*(rho-F(1,2))**2))
    zero('whole-family leading angular barrier',angular_numerator-gamma*rho*rho*delta-barrier_numerator)
    # In this isolated identity the formal variable v is renamed P.
    # The relation 8P^2-3P+u(1-u)=0 gives the nonzero IFT determinant.
    jac_relation=(3-16*v)**2-delta-32*(8*v*v-3*v+rho-rho*rho)
    zero('whole-family limiting Jacobian relation',jac_relation)
    record('whole_family_delta',delta.wire())
    record('whole_family_angular_loss_cleared',angular_numerator.wire())
    record('whole_family_barrier_cleared',barrier_numerator.wire())
    for name,value in [('far_root_energy_through4',qfar),('main_modulus_energy_through4',main),
                       ('aux_modulus_energy_through4',aux),('gap_energy_through4',gap)]:
        record(name,value.wire()[:5])
    record('rho_squared_coefficient',qcoef.wire())

    vv=Field(0,1)
    def endpoint(value):
        if any(j for i,j in value.d):raise RuntimeError('endpoint expression depends on rho')
        return sum((Field(c)*vv**i for (i,j),c in value.d.items()),Field())
    lo,hi=F(3,5),F(5,8)
    def threshold(x):return 239*x*x+184*x-208
    if not threshold(lo)<0<threshold(hi):raise RuntimeError('positive field branch not isolated')
    counts['signs']+=1
    for _ in range(64):
        mid=(lo+hi)/2
        if threshold(mid)<0:lo=mid
        elif threshold(mid)>0:hi=mid
        else:raise RuntimeError('unexpected rational threshold root')
    def positive(name,value):
        bounds=Field(value).interval(lo,hi)
        if bounds[0]<=0:raise RuntimeError('strict sign not certified: '+name)
        record('positive_'+name,[[x.numerator,x.denominator] for x in bounds])
        counts['signs']+=1
    zero('positive threshold polynomial',239*vv*vv+184*vv-208)
    sqrt101=(239*vv+92)/24
    zero('positive sqrt101 square',sqrt101*sqrt101-101)
    h2minus=endpoint(h2);gminus=endpoint(gamma)
    lam=sqrt101/(48*vv**3)
    h1_derivative=R({(i-1,j):i*c for (i,j),c in h1.d.items() if i})*(-v*v)
    zero('transverse derivative',endpoint(h1_derivative)-lam)
    zero('h1 threshold zero',endpoint(h1))
    zero('quartic threshold coefficient',endpoint(qcoef)-gminus)
    beta=-h2minus/(2*gminus)
    gain=h2minus*h2minus/(4*gminus)
    rational_gain=-F(11,5)*h2minus-F(121,25)*gminus
    zero('stationary endpoint energy transfer',h2minus+2*gminus*beta)
    zero('stationary endpoint gain',h2minus*beta+gminus*beta*beta+gain)
    positive('gamma',gminus)
    positive('lambda',lam)
    positive('minus_h2',-h2minus)
    positive('window_derivative_at_rho6',12*gminus-lam/5)
    positive('beta_lower',beta-F(2219843,1000000))
    positive('beta_upper',F(2219844,1000000)-beta)
    positive('gain_lower',gain-F(107206,1000000))
    positive('gain_upper',F(107207,1000000)-gain)
    positive('rational_gain_lower',rational_gain-F(107198,1000000))
    positive('rational_gain_upper',F(107199,1000000)-rational_gain)
    for name,value in [('gamma_endpoint',gminus),('lambda_endpoint',lam),
                       ('h2_endpoint',h2minus),('stationary_beta_endpoint',beta),
                       ('stationary_gain_endpoint',gain),('rational_split_gain_endpoint',rational_gain)]:
        record(name,value.wire())
    record('positive_threshold_interval',[[x.numerator,x.denominator] for x in (lo,hi)])

    # Five complete linear inputs span the fixed-v four-root block model.
    # These check the whole left/right vectors, not selected entries.
    reducing=[]
    for index in range(5):
        u=[F(0)]*8
        if index<4:u[index]=F(1)
        else:u[4:]=[F(1)]*4
        matrix=[[u[i]*(int(i==j)+1) for j in range(8)] for i in range(8)]
        for direction in range(3):
            vector=[F(0)]*8;vector[4+direction]=F(1);vector[7]=F(-1)
            right=[sum((matrix[i][j]*vector[j] for j in range(8)),F(0)) for i in range(8)]
            left=[sum((vector[i]*matrix[i][j] for i in range(8)),F(0)) for j in range(8)]
            expected_vector=vector if index==4 else [F(0)]*8
            zero('full right reducing vector '+str((index,direction)),[x-y for x,y in zip(right,expected_vector)])
            zero('full left reducing vector '+str((index,direction)),[x-y for x,y in zip(left,expected_vector)])
            reducing.append({'input':index,'direction':direction,
                'right':[[x.numerator,x.denominator] for x in right],
                'left':[[x.numerator,x.denominator] for x in left]})
    record('complete_reducing_vectors',reducing)

    damages=[characteristic[3]-target[0]+D,
             sum(energies,J())+f-e,
             fp+J(1),gap.c[4]-rho*h2,
             gap.c[3]-2*rho*h1,endpoint(qcoef)-gminus+Field(1),
             h2minus+2*gminus*beta+Field(1),
             delta-(1+31*(rho-F(1,2))**2),
             angular_numerator-gamma*rho*rho*delta,
             (3-16*v)**2-delta-31*(8*v*v-3*v+rho-rho*rho)]
    for value in damages:
        if isinstance(value,J):nonzero=any(c.d for c in value.c)
        elif isinstance(value,Field):nonzero=bool(value.a or value.b)
        else:nonzero=bool(value.d)
        if not nonzero:raise RuntimeError('damaged mathematics passed')
        counts['damaged_math']+=1
    return {'schema':'sendov-two-pair-bifurcation-v1','agent':'six-sendov-3','role':'researcher',
            'factor_jet_order':5,'objective_jet_order':4,'counts':counts,'records':records,
            'trust_boundary':'exact polynomial/coefficient/sign evidence; analytic bifurcation is in PROOF.md'}


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
    else:args.write_fixture.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    digest=hashlib.sha256(json.dumps(result['records'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
    print(json.dumps({'agent':'six-sendov-3','role':'researcher','schema':result['schema'],
                      'counts':result['counts'],'record_count':len(result['records']),
                      'record_sha256':digest,'status':result['trust_boundary']},sort_keys=True))


if __name__=='__main__':main()
