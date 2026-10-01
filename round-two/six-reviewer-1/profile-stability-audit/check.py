#!/usr/bin/env python3
"""Independent quantitative-profile audit; only the reviewer's published field
kernel is reused. No target source is imported. See REVIEW.md for analytic scope.
"""
import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path

HELPER_SHA = '2386fae932fcbc1c2ac04ad05c21729f490f044f525ca36ad5659adf891823b3'
helper = Path(__file__).resolve().parent.parent / 'quartic-boundary-audit' / 'check.py'
if hashlib.sha256(helper.read_bytes()).hexdigest() != HELPER_SHA:
    raise RuntimeError('published reviewer field kernel differs')
spec = importlib.util.spec_from_file_location('reviewer_field', helper)
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
K, c = prior.K, prior.CROOT


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


class Ring:
    def __init__(self, n, first_cap=None, total_cap=None):
        self.n, self.first_cap, self.total_cap = n, first_cap, total_cap
        self.zero = (0,) * n

    def scalar(self, x=0):
        return P(self, {self.zero: K(x)})

    def variable(self, j):
        key = list(self.zero)
        key[j] = 1
        return P(self, {tuple(key): K(1)})


class P:
    def __init__(self, ring, terms):
        self.ring = ring
        self.a = {k: K(v) for k, v in terms.items() if K(v)}

    def coerce(self, x):
        if isinstance(x, P):
            require(x.ring is self.ring, 'ring alignment')
            return x
        return self.ring.scalar(x)

    def __eq__(self, x):
        return self.a == self.coerce(x).a

    def __bool__(self):
        return bool(self.a)

    def __neg__(self):
        return P(self.ring, {k: -v for k, v in self.a.items()})

    def __add__(self, x):
        r = self.a.copy()
        for k, v in self.coerce(x).a.items():
            r[k] = r.get(k, K()) + v
        return P(self.ring, r)

    __radd__ = __add__

    def __sub__(self, x):
        return self + -self.coerce(x)

    def __rsub__(self, x):
        return self.coerce(x) + -self

    def __mul__(self, x):
        r = {}
        for k, v in self.a.items():
            for l, u in self.coerce(x).a.items():
                key = tuple(a+b for a,b in zip(k,l))
                if self.ring.first_cap is not None and key[0] > self.ring.first_cap:
                    continue
                if self.ring.total_cap is not None and sum(key) > self.ring.total_cap:
                    continue
                r[key] = r.get(key, K()) + v*u
        return P(self.ring, r)

    __rmul__ = __mul__

    def __truediv__(self, x):
        return self * K(x).inverse()

    def __pow__(self, n):
        require(n >= 0, 'polynomial power')
        r = self.ring.scalar(1)
        for _ in range(n):
            r = r*self
        return r

    def conjugate(self):
        return P(self.ring, {k:v.conjugate() for k,v in self.a.items()})

    def real(self):
        return (self+self.conjugate())/2

    def coefficient_first(self, n):
        return P(self.ring, {(0,)+k[1:]:v for k,v in self.a.items() if k[0] == n})

    def specialize_last(self, value):
        r = {}
        for key, v in self.a.items():
            new = key[:-1]+(0,)
            r[new] = r.get(new, K())+v*K(value)**key[-1]
        return P(self.ring,r)


class Z:
    """Formal i over a real-symbol polynomial ring; i^2=-1."""
    def __init__(self, real, imag=None):
        self.r = real
        self.i = real.ring.scalar() if imag is None else imag

    def coerce(self, x):
        return x if isinstance(x, Z) else Z(self.r.coerce(x))

    def __neg__(self):
        return Z(-self.r,-self.i)

    def __add__(self, x):
        x=self.coerce(x)
        return Z(self.r+x.r,self.i+x.i)

    __radd__=__add__

    def __sub__(self,x):
        return self+-self.coerce(x)

    def __mul__(self,x):
        x=self.coerce(x)
        return Z(self.r*x.r-self.i*x.i,self.r*x.i+self.i*x.r)

    __rmul__=__mul__

    def __truediv__(self,x):
        return Z(self.r/x,self.i/x)


def evaluate(poly, z):
    r = z.ring.scalar()
    for a in reversed(poly):
        r = r*z+a
    return r


def multiply(a,b):
    r = [a[0].ring.scalar() for _ in range(len(a)+len(b)-1)]
    for i,v in enumerate(a):
        for j,u in enumerate(b):
            r[i+j] += v*u
    return r


def binomial(a, exponent, order=3):
    require(a.coefficient_first(0)==1,'unit constant binomial series')
    t=a-1
    result=a.ring.scalar(1)
    coefficient=F(1)
    for n in range(1,order+1):
        coefficient*= (exponent-n+1)/n
        result+=t**n*coefficient
    return result


def polynomial_record(poly):
    record=[]
    for z_degree, a in enumerate(poly):
        for (eta_degree,s_degree),v in a.a.items():
            record.append([[eta_degree,z_degree,s_degree],list(map(str,prior.cubic(v)))])
    return sorted(record)


def digest(value):
    return hashlib.sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()


def build():
    checks=0
    def check(condition,label):
        nonlocal checks
        require(condition,label)
        checks+=1
    y=1/(3*(1+c)); x=F(2,3)-y; H=14*y; U0=-8*x
    rho=(c-5)/3; L=-7*(2*c+1)/18
    alpha=F(-527,360)+F(41,90)*c+F(13,90)*c*c
    beta=F(1369,648)+F(74,81)*c+F(8,81)*c*c
    sigma=alpha+rho*rho/2
    Bstar=F(2311,108)+F(4934,27)*c-F(1976,9)*c*c
    C=F(8,3)+y; q=beta+alpha/2
    uz=(U0+rho*H)/8; up=uz-rho*H/2
    d=2*c*c-1; v=2*d*d-1
    weights=[F(2,3)*(7-(1-d)/(c+d)),1/(c+d)]
    A=[K(F(3,2)),1+c]; B=[K(F(3,2)),1-d]
    constants={'C':C,'H':H,'U0':U0,'Bstar':Bstar,'L':L,'rho':rho,
               'alpha':alpha,'beta':beta,'mu':q,'u_zero':uz,'u_pair':up,
               '9beta+4alpha':9*beta+4*alpha}
    prior.positive(9*beta+4*alpha,'all-six-directions Hessian positive')
    checks+=1

    # Generic power-sum approach to the real/imaginary coefficient parity.
    # These are independent moment symbols, not the author's eighteen-variable
    # critical-factor expansion.  Actual bounded moments satisfy these orders.
    names=['U','H','V','B','W','D','J3','J21','J12','J30','J4','J31','J22','J5','J41','J6']
    rg=Ring(1+len(names),first_cap=6)
    eps=rg.variable(0); t={n:rg.variable(j+1) for j,n in enumerate(names)}
    U,HH,V,BB,WW,DD,J3,J21,J12,J30,J4,J31,J22,J5,J41,J6=[t[n] for n in names]
    zero=rg.scalar()
    moments=[Z(zero),Z(U*eps**2+WW*eps**4,V*eps**3),
             Z(-HH*eps**2+DD*eps**4,BB*eps**3),
             Z(-3*J21*eps**4+J30*eps**6,-J3*eps**3+3*J12*eps**5),
             Z(J4*eps**4-6*J22*eps**6,-4*J31*eps**5),
             Z(5*J41*eps**6,J5*eps**5),Z(-J6*eps**6)]
    moments += [Z(zero),Z(zero)]
    es=[Z(rg.scalar(1))]
    for k in range(1,9):
        a=Z(zero)
        for j in range(1,k+1):a+=es[k-j]*moments[j]*((-1)**(j-1))
        es.append(a/k)
    primitive=[Z(zero) for _ in range(10)]
    for k in range(9):primitive[9-k]=es[k]*(9*(-1)**k)/(9-k)
    anchor=1-eps**2
    ar,ai=zero,zero
    for a in reversed(primitive):ar=ar*anchor+a.r;ai=ai*anchor+a.i
    primitive[0]=Z(-ar,-ai)
    g2=[zero for _ in range(10)];g4=[zero for _ in range(10)]
    g2[8],g2[7]=-9*U/8,9*HH/14;g2[0]=9-sum(g2[1:],zero)
    g4[8],g4[7]=-9*WW/8,9*(U**2-DD)/14
    g4[6],g4[5]=-3*U*HH/4+3*J21/2,9*HH**2/40-9*J4/20
    g4[0]=-36-9*U+9*HH/2-sum(g4[1:],zero)
    real_count=imag_count=0
    for k,a in enumerate(primitive):
        check(all(key[0]%2==0 for key in a.r.a),'all real coefficients even')
        check(all(key[0]%2==1 and key[0]>=3 for key in a.i.a),'all imaginary coefficients odd/order3')
        residual=a.r-(int(k==9)-int(k==0))-g2[k]*eps**2-g4[k]*eps**4
        check(all(key[0]>=6 for key in residual.a),'full real remainder order6')
        real_count+=len(a.r.a);imag_count+=len(a.i.a)
    generic_record=[[[k,list(key)],list(map(str,v.a)),component]
                    for k,a in enumerate(primitive) for component,part in [('real',a.r),('imag',a.i)]
                    for key,v in sorted(part.a.items())]

    # Exact six-coordinate chart Hessian, using q_chart^2 rather than radicals.
    rh=Ring(6,total_cap=4);coords=[rh.variable(j) for j in range(6)]
    S=sum(coords,rh.scalar());T=sum((a*a for a in coords),rh.scalar());ss=-S/2
    q2=rh.scalar(H/2)-T/2-ss*ss
    chartJ3=2*ss**3+6*ss*q2+sum((a**3 for a in coords),rh.scalar())
    chartJ4=2*ss**4+12*ss**2*q2+2*q2**2+sum((a**4 for a in coords),rh.scalar())
    cost=alpha*(chartJ4-H*H/2)+beta*chartJ3**2/H
    quadratic=H*(-alpha*T+(9*beta+4*alpha)*ss**2)
    remainder=cost-quadratic
    check(all(sum(key)==4 for key in remainder.a),'full chart cost residual degree4')
    check(all(sum(key)>=3 for key in (chartJ3-3*H*ss).a),'chart cubic-moment linearization')
    check(all(sum(key)==4 for key in (chartJ4-H*H/2-H*(4*ss**2-T)).a),'chart fourth-moment quadratic identity')

    # Family calculations are polynomial identities in the entire profile
    # parameter s; no interpolation or selected s values establish coverage.
    rf=Ring(2,first_cap=3);eta=rf.variable(0);s=rf.variable(1);one=rf.scalar(1)
    HA=H*(1-s)/2;HB=H*s/2
    uA=rf.scalar(uz)-rho*HA;uB=rf.scalar(uz)-rho*HB
    U2=4*uz*uz+2*uA*uA+2*uB*uB
    mixed=2*uA*HA+2*uB*HB;fourth=2*HA*HA+2*HB*HB
    check(fourth==rf.scalar(H*H/2)-H*H*s*(1-s),'all-s fourth moment')
    check(4*uz+2*uA+2*uB==U0,'all-s real mean')
    curvature=[];TT=[]
    for index in range(2):
        rr,sin2=(K(-1),K(F(3,4))) if index==0 else(-2*c,1-c*c)
        curv=-((F(7,2)*x*x+6*x*y*rr+F(5,2)*y*y*rr*rr)*sin2)
        C6,C5=(K(0),K(F(3,2))) if index==0 else(K(F(3,2)),1-v)
        TT.append(4+U0-H/2+B[index]*U0*U0/14+C6*(-U0*H/12+mixed/6)
                  +C5*(rf.scalar(H*H/40)-fourth/20)+curv)
        curvature.append(curv)
    a,b=A[0]/8,B[0]/14;e,f=A[1]/8,B[1]/14;det=a*f-b*e
    W=(TT[0]*f-TT[1]*b)/det;D=(a*TT[1]-e*TT[0])/det
    gamma=(U2-D)/(2*H)
    center=[uz*eta+W*eta**2/8+100*eta**3,uA*eta+W*eta**2/8+100*eta**3,uB*eta+W*eta**2/8+100*eta**3]
    derivative=[one]
    for _ in range(4):derivative=multiply(derivative,[-center[0],one])
    for i,pair_norm in [(1,HA),(2,HB)]:
        pair=multiply([-center[i],one],[-center[i],one]);pair[0]+=pair_norm*eta*(1+gamma*eta)**2
        derivative=multiply(derivative,pair)
    derivative=[9*a for a in derivative]
    poly=[rf.scalar()]+[a/(j+1) for j,a in enumerate(derivative)]
    poly[0]=-evaluate(poly,1-eta)
    radial=[]
    for k in range(9):
        omega=prior.WROOT**k;branch=rf.scalar(omega)
        for n in range(1,4):branch+=-evaluate(poly,branch).coefficient_first(n)*eta**n/(9*omega**8)
        check(evaluate(poly,branch)==0,'all-s original root residual')
        half=(branch*branch.conjugate()-1)/2
        if k==0:check(branch==1-eta,'all-s marked original root')
        elif k in (3,4,5,6):
            check(half.coefficient_first(1)==0,'all-s active first radial zero')
            check(half.coefficient_first(2)==0,'all-s active second radial zero')
            at0=half.coefficient_first(3).specialize_last(0)
            require(len(at0.a)==1,'third coefficient at s0 scalar')
            prior.negative(next(iter(at0.a.values())),'third inward at s0')
            checks+=1
        else:
            first=half.coefficient_first(1)
            require(len(first.a)==1,'inactive first radial independent of s')
            prior.negative(next(iter(first.a.values())),'nonactive all-s first inward')
            checks+=1
        radial.append({'k':k,'radial_eta1':polynomial_record([half.coefficient_first(1)]),
                       'radial_eta2':polynomial_record([half.coefficient_first(2)]),
                       'radial_eta3_s0':polynomial_record([half.coefficient_first(3).specialize_last(0)])})
    objective=4*binomial(1-eta-center[0],F(-1))
    for j,pair_norm in [(1,HA),(2,HB)]:
        objective+=2*binomial((1-eta-center[j])**2+pair_norm*eta*(1+gamma*eta)**2,F(-1,2))
    coefficient=objective.coefficient_first(2)
    check(objective.coefficient_first(0)==8,'family objective constant')
    check(objective.coefficient_first(1)==C,'family objective slope')
    check(coefficient==rf.scalar(Bstar)-alpha*H*H*s*(1-s),'full all-s quadratic objective')
    # Joint orbit distance is independently derived from squared pair norms.
    # t=sqrt(1-s): polynomialization gives s=1-t^2 and h distance=2H(1-t).
    rt=Ring(1,total_cap=4);tt=rt.variable(0);st=1-tt*tt
    h_distance=H*((tt-1)**2+st)
    u_distance=4*(rho*H*st/2)**2
    check(h_distance==2*H*(1-tt),'exact nearest h distance')
    check(u_distance==rho*rho*H*H*st**2,'exact matching u distance')

    # Numerical penalty transfer: t=128*kappa, eps=(1-t)/2 and lambda=(1-t)/(2t).
    # Rational identity proves every fixed0<kappa<1/128, not only tested choices.
    rp=Ring(1,total_cap=4);tau=rp.variable(0)
    check((1-(1-tau)/2)*2*tau==tau*(1+tau),'all-kappa transfer identity after clearing denominators')
    for kappa in [F(1,256),F(1,512),F(3,512),F(7,1024)]:
        t0=128*kappa;eps0=(1-t0)/2;lam=(1-t0)/(2*t0)
        check(0<eps0<1 and lam>0 and (1-eps0)/(128*(1+lam))==kappa,'explicit penalty parameters')

    # Damage actual residual inputs; controls do not establish universal claims.
    damaged=poly.copy();damaged[0]+=eta**2
    damagedobjective=objective+eta**2*s
    brokenchart=quadratic+H*T
    mutations=[('anchor',lambda:evaluate(damaged,1-eta)==0),
               ('all-s objective',lambda:damagedobjective.coefficient_first(2)==coefficient),
               ('six-direction Hessian',lambda:brokenchart==quadratic),
               ('penalty denominator',lambda:F(1,256)==F(3,4)/(128*F(3,2))+F(1,128))]
    rejected=[]
    for label,test in mutations:
        try:require(test(),label)
        except RuntimeError:rejected.append(label)
        else:raise RuntimeError('undetected '+label)
    dr,pr,ob=polynomial_record(derivative),polynomial_record(poly),polynomial_record([objective])
    result={'checks':checks,'constants':{k:list(map(str,prior.cubic(a))) for k,a in sorted(constants.items())},
            'generic_moment_kernel':{'real_terms':real_count,'imag_terms':imag_count,'full_anchored_hash':digest(generic_record),'epsilon_order':6,'independent_moment_symbols':16},
            'family':{'derivative_terms':len(dr),'derivative_hash':digest(dr),'primitive_terms':len(pr),'primitive_hash':digest(pr),'objective_hash':digest(ob),'quadratic_objective':polynomial_record([coefficient]),'all_nine_radial_records':radial},
            'penalty_refinement':'every fixed0<kappa<1/128, including1/256; K_M,kappa and collar existential',
            'mutations_rejected':rejected,'helper_sha256':HELPER_SHA,
            'trust_boundary':'finite exact algebra; uniform analytic root maps, projections and disk-rectangle proof in REVIEW.md'}
    return result


def bridge(record,path):
    author=json.loads(Path(path).read_text())
    require(record['constants']==author['constants'],'all author constant bridge')
    family=record['family'];af=author['two_pair_family']
    require(family['derivative_hash']==af['derivative_hash'],'every derivative coefficient bridge')
    require(family['primitive_hash']==af['polynomial_hash'],'every primitive coefficient bridge')
    require(family['objective_hash']==af['objective_hash'],'every objective coefficient bridge')
    require(family['quadratic_objective']==af['second_coefficient'],'full quadratic response bridge')
    for index,k in enumerate((3,4)):
        require(family['all_nine_radial_records'][k]['radial_eta3_s0'][0][1]==af['inward_third_at_sigma0'][index],'inward third coefficient bridge')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');parser.add_argument('--author')
    args=parser.parse_args();record=build();data=json.dumps(record,indent=2,sort_keys=True)+'\n'
    expected=Path(__file__).with_name('expected.json')
    if args.write:expected.write_text(data)
    else:require(expected.read_text()==data,'complete independent record')
    if args.author:bridge(record,args.author)
    print(f"PASS: {record['checks']} independent exact checks; four damaged inputs rejected.")
    print('Record SHA256 '+hashlib.sha256(data.encode()).hexdigest())
    print('Full all-s two-pair identities; numerical original-polynomial penalty1/256 and every fixed kappa<1/128.')


if __name__=='__main__':main()
