"""Exact joint three-pair ratio normal form. Actual six-sendov-3, researcher.

Standalone standard-library coefficient/sign evidence. Laurent/jet kernels
adapt this author's published8405 source; no independence claim. The actual
modulus, analytic continuation and family classification are in PROOF.md.
"""
from fractions import Fraction as F
import json


class R:
    """Q[v,v^-1,t,w]; nonzero monomials alone are inverted."""
    def __init__(self,x=0):
        if isinstance(x,R):x=x.d
        elif isinstance(x,(int,F)):x={(0,0,0):F(x)}
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
                kh=tuple(a+b for a,b in zip(k,h));d[kh]=d.get(kh,F(0))+c*a
        return R(d)
    __rmul__=__mul__
    def inverse(self):
        if len(self.d)!=1:raise RuntimeError('only nonzero monomial inversion')
        k,c=next(iter(self.d.items()))
        if any(k[1:]):raise RuntimeError('only v monomials may be inverted')
        return R({tuple(-i for i in k):1/c})
    def __truediv__(self,x):
        if isinstance(x,J):return NotImplemented
        return self*R(x).inverse()
    def __rtruediv__(self,x):return R(x)*self.inverse()
    def __pow__(self,n):
        if n<0:return self.inverse()**(-n)
        out=R(1)
        for _ in range(n):out*=self
        return out
    def wire(self):return [[list(k),[c.numerator,c.denominator]] for k,c in sorted(self.d.items())]


ORDER=7
class J:
    """Energy jets modulo e^8; use only explicitly checked orders."""
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
        if n<0:return self.inverse()**(-n)
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
    global ORDER
    ORDER=7
    counts={'identities':0,'signs':0,'damaged_math':0}
    records={}
    v=R({(1,0,0):F(1)});t=R({(0,1,0):F(1)});w=R({(0,0,1):F(1)})
    a=1/v-1;b=1-a*a;e=J([R(),R(1)]);k1=(7*a-4)/2
    def conv(left,right):
        out=[J() for _ in range(len(left)+len(right)-1)]
        for i,x in enumerate(left):
            for j,y in enumerate(right):out[i+j]+=x*y
        return out
    def shift(x,n):return [J()]*n+list(x)
    def add(left,right):
        return [(left[i] if i<len(left) else J())+(right[i] if i<len(right) else J())
                for i in range(max(len(left),len(right)))]
    def zero(label,x,through=None):
        def bad(y):
            if isinstance(y,J):return any(c.d for c in (y.c if through is None else y.c[:through+1]))
            if isinstance(y,list):return any(bad(c) for c in y)
            if isinstance(y,Field):return bool(y.a or y.b)
            return bool(y.d)
        if bad(x):raise RuntimeError(label)
        counts['identities']+=1

    def wire(x):
        if isinstance(x,(R,J,Field)):return x.wire()
        if isinstance(x,list):return [wire(c) for c in x]
        if isinstance(x,dict):return {key:wire(value) for key,value in x.items()}
        return x
    def record(key,x):
        if key in records:raise RuntimeError('duplicate whole record')
        records[key]=wire(x)

    j=[J(-v),J(5*(2*a-1)/4),J(b*(3*a+1)/2),J(3*b*b/4)]
    k=[J(F(1,2)),J(b/2)]
    term=add(shift([9*x for x in k],1),[-x for x in conv([J(v),J(1)],[2*k[0],5*k[1]])])
    l4=conv(conv(k,k),term)
    zero('L4 constant',l4[0]+v/4)
    zero('L4 linear',l4[1]-(9*a-2)/8)
    d2=e**3*t-e**4*(t*t-w)
    d3=e**5*w-e**6*t*w
    c3=[-3*v*e,k1*e,-8*v+b*e,J(1)]
    c7=add(add(shift(c3,4),shift([d2*x for x in j],2)),[d3*x for x in l4])

    # Literal actual reciprocal product, symmetric in the two small energies.
    # Its energy degree is at most six, so ORDER7 does not truncate this stage.
    pairmain=[(e-e**2*t)*k[0],(e-e**2*t)*k[1],J(1)]
    aux4=add(add([e**4*w*x for x in conv(k,k)],shift([e**2*t*x for x in k],2)),[J(),J(),J(),J(),J(1)])
    original8=shift(conv(pairmain,aux4),2)
    characteristic=[]
    for i in range(9):
        coefficient=(9-i)*original8[i]
        if i+1<9:coefficient-=v*(i+1)*original8[i+1]
        characteristic.append(coefficient)
    zero('complete actual eight-critical characteristic', [x-y for x,y in zip(characteristic,shift(c7,1))])
    record('whole_original8',original8)
    record('whole_critical8',characteristic)
    record('whole_septic7',c7)

    def normalized(x,n):
        for _ in range(n):x=x.divide_e()
        return x

    def components(S3,P2,S1,P0):
        s3=e**2*S3;p2=e**2*P2;s1=e**4*S1;p0=e**4*P0
        ac=c7[6]+s3
        bc=c7[5]+s3*ac-p2
        cc=c7[4]+s3*bc-p2*ac+s1
        q4=[p0,-s1,p2,-s3,J(1)]
        cubic=[cc,bc,ac,J(1)]
        low=[normalized(p2*cc-s1*bc+p0*ac-c7[2],3),
             normalized(-s3*cc+p2*bc-s1*ac+p0-c7[3],3),
             normalized(p0*cc-c7[0],5),
             normalized(-s1*cc+p0*bc-c7[1],5)]
        return q4,cubic,low

    # Complete normalized outer Jacobian at e0, all sixteen entries.
    limzero=components(J(),J(),J(),J())[2]
    jac=[]
    for index in range(4):
        args=[J(),J(),J(),J()]
        args[index]=J(1)
        changed=components(*args)[2]
        jac.append([(changed[j]-limzero[j]).c[0] for j in range(4)])
    # Column order above is S3,P2,S1,P0; reorder to P2,S3,P0,S1.
    jac=[[jac[index][row] for index in [1,0,3,2]] for row in range(4)]
    want=[[-3*v,R(),R(),R()],[k1,3*v,R(),R()],[R(),R(),-3*v,R()],[R(),R(),k1,3*v]]
    zero('entire normalized outer Jacobian',[[x-y for x,y in zip(row,target)] for row,target in zip(jac,want)])
    record('normalized_outer_jacobian',jac)

    S3=P2=S1=P0=J()
    for n in range(3):
        errors=components(S3,P2,S1,P0)[2]
        dp2=errors[0].c[n]/(3*v)
        ds3=-(errors[1].c[n]+k1*dp2)/(3*v)
        dp0=errors[2].c[n]/(3*v)
        ds1=-(errors[3].c[n]+k1*dp0)/(3*v)
        def increment(x,c):
            data=list(x.c);data[n]+=c;return J(data)
        P2=increment(P2,dp2);S3=increment(S3,ds3)
        P0=increment(P0,dp0);S1=increment(S1,ds1)
        zero('all normalized factor residuals through '+str(n),components(S3,P2,S1,P0)[2],n)
    q4,cubic,errors=components(S3,P2,S1,P0)
    zero('whole factor through energy5',[x-y for x,y in zip(conv(q4,cubic),c7)],5)
    s=(16*a-7)/(36*v);r=(10*a-1)/(36*v)
    zero('limiting sum',S3.c[0]-t*s)
    zero('limiting product sum',P2.c[0]-t/3)
    zero('limiting mixed sum',S1.c[0]-w*r)
    zero('limiting product',P0.c[0]-w/12)

    record('normalized_S3_through2',[x for x in S3.c[:3]])
    record('normalized_P2_through2',[x for x in P2.c[:3]])
    record('normalized_S1_through2',[x for x in S1.c[:3]])
    record('normalized_P0_through2',[x for x in P0.c[:3]])
    record('complete_low_equations_through2',[[x for x in y.c[:3]] for y in errors])

    # Energy-four objective needs only the now-checked cubic/base coefficients.
    ORDER=4
    cubic=[J(x.c[:5]) for x in cubic]
    c3=[J(x.c[:5]) for x in c3]
    q4=[J(x.c[:5]) for x in q4]
    def cubic_modulus(cubic):
        cc,bc,ac,_=cubic
        far=J(9*v)
        for n in range(1,5):
            residual=(far-v)**3+ac*(far-v)**2+bc*(far-v)+cc
            data=list(far.c);data[n]-=residual.c[n]/(64*v*v);far=J(data)
        zero('complete cubic far jet', (far-v)**3+ac*(far-v)**2+bc*(far-v)+cc)
        product=-((-v)**3+ac*v*v-bc*v+cc)
        near=(product/far).sqrt(v)
        return far+2*near,far,near
    main,far,near=cubic_modulus(cubic)
    mainq,farq,nearq=cubic_modulus(c3)
    base=5*v-q4[3]+q4[2]/v+main
    gap=base-(5*v+mainq)
    h1=(208-184*v-239*v*v)/(2304*v**5)
    h2=(-245888+771984*v-786792*v*v+246931*v**3)/(4718592*v**8)
    gamma=(4+v)**2/(10368*v**5)
    q2=gamma-h1;alpha=h1-F(15,4)*gamma
    for n in range(3):zero('whole lower gap '+str(n),gap.c[n])
    zero('whole third coefficient',gap.c[3]-h1*t)
    den=t*t-3*w
    ns=w*(3*t*t*s*r-F(3,4)*t*t*s*s-9*w*r*r)
    correction=ns/(2*v)+den*(t*t*(v*s+F(1,3))**2/(4*v**3)-w*r/(2*v*v)-w/(24*v**3))
    target=(h2*t+q2*t*t+alpha*w)*den+9*gamma*w*w
    zero('complete rational fourth coefficient',gap.c[4]*den-correction-target)


    record('quartic_factor_through4',q4)
    record('external_cubic_through4',cubic)
    record('far_root_through4',far)
    record('main_modulus_through4',near)
    record('gap_before_small_pair_correction',gap)
    record('small_pair_correction_numerator',correction)
    record('joint_normal_form_numerator',target)
    record('joint_normal_form_denominator',den)
    record('linear_energy_coefficients',[h1,h2])
    record('gamma_and_cross',[gamma,alpha,9*gamma])
    zero('credited H4 boundary coefficient',2*q2+alpha+h1+F(7,4)*gamma)

    # The blown-up ratio variable uses the third exponent, now labelled u.
    u=w;du=1-3*u;bn=1-F(27,4)*u+F(81,4)*u*u
    zero('complete ratio square remainder',bn-F(3,4)*du-(1-9*u)**2/4)
    zero('complete blowup coefficient',((gamma-h1)+(h1-F(15,4)*gamma)*u)*du+9*gamma*u*u-(gamma*bn-h1*(1-u)*du))
    def derivative_u(x):
        return R({(i,j,k-1):k*c for (i,j,k),c in x.d.items() if k})
    def at_u(x,value):
        return R({(i,j,0):sum((c*value**k for (h,l,k),c in x.d.items() if h==i and l==j),F(0)) for i,j,_ in x.d})
    first=derivative_u(bn)*du-bn*derivative_u(du)
    zero('complete ratio derivative',first+F(3,4)*(1-9*u)*(5-9*u))
    second=derivative_u(first)*du-2*first*derivative_u(du)
    zero('ratio second derivative at optimum',at_u(second,F(1,9))-F(243,4)*at_u(du,F(1,9))**3)
    zero('optimal ratio value',at_u(bn,F(1,9))-F(3,4)*at_u(du,F(1,9)))
    record('ratio_variable_labels',['v','t','u'])
    record('ratio_b_numerator',bn)
    record('ratio_b_denominator',du)
    record('ratio_b_prime_numerator',first)
    record('ratio_square_remainder',(1-9*u)**2/4)

    # Generic limiting internal Jacobian: the variables here mean S+,delta,S-.
    pp=(1+t)/6;pm=(1-t)/6
    innerjac=[[R(1),R(1),R(),R()],[R(),R(),R(1),R(1)],
              [pm,pp,w,v],[R(),R(),pm,pp]]
    from itertools import permutations
    def determinant(matrix):
        out=R()
        for permutation in permutations(range(len(matrix))):
            inversions=sum(permutation[i]>permutation[j] for i in range(len(matrix)) for j in range(i+1,len(matrix)))
            term=R((-1)**inversions)
            for i,j in enumerate(permutation):term*=matrix[i][j]
            out+=term
        return out
    zero('generic inner Jacobian determinant',determinant(innerjac)+t*t/9)
    record('internal_jacobian_variable_labels',['Splus','delta','Sminus'])
    record('complete_limiting_internal_jacobian',innerjac)
    record('inner_jacobian_determinant',-t*t/9)

    vv=Field(0,1)
    def endpoint(x):
        if any(j or k for i,j,k in x.d):raise RuntimeError('endpoint has auxiliary parameters')
        return sum((Field(c)*vv**i for (i,j,k),c in x.d.items()),Field())
    lo=F(3,5);hi=F(5,8)
    def threshold(x):return 239*x*x+184*x-208
    if threshold(lo)>=0 or threshold(hi)<=0:raise RuntimeError('threshold root not isolated')
    for _ in range(64):
        mid=(lo+hi)/2
        if threshold(mid)<0:lo=mid
        elif threshold(mid)>0:hi=mid
        else:raise RuntimeError('unexpected rational threshold root')
    def positive(name,value):
        value=Field(value);bounds=value.interval(lo,hi)
        if bounds[0]<=0:raise RuntimeError('strict sign not certified: '+name)
        counts['signs']+=1
        record('positive_'+name,[[q.numerator,q.denominator] for q in bounds])
    gm=endpoint(gamma);hm=endpoint(h2)
    sqrt101=(239*vv+92)/24;lam=sqrt101/(48*vv**3)
    zero('threshold h1',endpoint(h1));zero('sqrt101 identity',sqrt101*sqrt101-101)
    tau=2*lam/(3*gm);beta3=-2*hm/(3*gm)
    gain3=lam*lam/(3*gm);gain2=lam*lam/(4*gm)
    nu3=hm*hm/(3*gm);nu2=hm*hm/(4*gm)
    zero('exact window gain improvement',gain3-F(4,3)*gain2)
    zero('exact endpoint gain improvement',nu3-F(4,3)*nu2)
    zero('exact endpoint total energy comparison',beta3-F(4,3)*(-hm/(2*gm)))
    positive('lambda',lam);positive('gamma',gm);positive('minus_h2',-hm)
    positive('radial_hessian',F(3,2)*gm)
    positive('ratio_hessian',27*lam*lam/gm)
    positive('relative_gain_over_two_pair',gain3-gain2)
    positive('endpoint_gain',nu3)
    positive('ratio_denominator_lower_bound',F(1,4))
    positive('internal_jacobian_absolute_lower_bound',F(1,36))
    record('threshold_v_interval',[[q.numerator,q.denominator] for q in [lo,hi]])
    record('window_tau_and_gain',[tau,gain3,gain3-gain2])
    record('endpoint_total_energy_and_gain',[beta3,nu3])

    # A separate exact quadratic isolation suffices for the leading energy ratio.
    sqlo=F(2);sqhi=F(9,4)
    if sqlo*sqlo>=5 or sqhi*sqhi<=5:raise RuntimeError('sqrt5 root not isolated')
    for _ in range(64):
        mid=(sqlo+sqhi)/2
        if mid*mid<5:sqlo=mid
        elif mid*mid>5:sqhi=mid
        else:raise RuntimeError('unexpected rational sqrt5')
    rlo=(3-sqhi)/6;rhi=(3-sqlo)/6
    if not 0<rlo<rhi<F(1,2):raise RuntimeError('ordered energy fraction not physical')
    ratio=[(7+3*sqlo)/2,(7+3*sqhi)/2]
    if not F(6854101,1000000)<ratio[0]<ratio[1]<F(6854102,1000000):raise RuntimeError('leading ratio bounds fail')
    counts['signs']+=1
    record('sqrt5_interval',[[q.numerator,q.denominator] for q in [sqlo,sqhi]])
    record('ordered_energy_fraction_interval',[[q.numerator,q.denominator] for q in [rlo,rhi]])
    record('leading_energy_ratio_interval',[[q.numerator,q.denominator] for q in ratio])

    damages=[gap.c[3]-2*h1*t,
             gap.c[4]*den-correction-((h2*t+q2*t*t+alpha*w)*den+8*gamma*w*w),
             bn-F(3,4)*du-(1-8*u)**2/4,
             first+F(1,4)*(1-9*u)*(5-9*u),
             determinant(innerjac)-t*t/9,
             gain3-F(3,2)*gain2,
             nu3-nu2]
    for expression in damages:
        if isinstance(expression,Field):nonzero=bool(expression.a or expression.b)
        else:nonzero=bool(expression.d)
        if not nonzero:raise RuntimeError('damaged mathematical control passed')
        counts['damaged_math']+=1
    return {'schema':'sendov-three-pair-ratio-minimum-v1','agent':'six-sendov-3','role':'researcher',
            'actual_characteristic_energy_degree':6,'base_normalized_factor_order':2,'objective_order':4,
            'base_variable_labels':['v','t','w'],'counts':counts,'records':records,
            'trust_boundary':'exact coefficient/sign evidence; uniform actual objective and scaled-family optimizer are ordinary proof in PROOF.md'}

def main():
    import argparse, hashlib
    from pathlib import Path
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fixture',type=Path,default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--write-fixture',type=Path,help='explicit generation; skips fixture comparison')
    args=parser.parse_args();result=certify()
    if args.write_fixture is None:
        if not args.fixture.is_file():raise RuntimeError('mandatory whole fixture missing')
        if json.loads(args.fixture.read_text())!=result:raise RuntimeError('whole mandatory fixture differs')
    else:args.write_fixture.write_text(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n')
    digest=hashlib.sha256(json.dumps(result['records'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
    print(json.dumps({'agent':result['agent'],'role':result['role'],'schema':result['schema'],
        'counts':result['counts'],'record_count':len(result['records']),'record_sha256':digest,
        'status':result['trust_boundary']},sort_keys=True))

if __name__=='__main__':main()
