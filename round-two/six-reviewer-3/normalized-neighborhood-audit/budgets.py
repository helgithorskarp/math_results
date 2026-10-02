"""Exact universal analytic budgets in u=sqrt(eta), delta; no eta samples."""
from dataclasses import dataclass, replace
from fractions import Fraction as Q
from math import comb, factorial


def need(condition, message):
    if not condition:
        raise ValueError(message)


@dataclass(frozen=True)
class Monomial:
    coefficient: Q
    u: int = 0
    delta: int = 0

    def __post_init__(self):
        object.__setattr__(self, 'coefficient', Q(self.coefficient))
        need(type(self.u) is int and type(self.delta) is int, 'integral sqrt-eta/delta exponents')

    def __mul__(self, other):
        other = box(other)
        return Monomial(self.coefficient * other.coefficient, self.u + other.u, self.delta + other.delta)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = box(other)
        need(other.coefficient > 0, 'positive symbolic divisor')
        return Monomial(self.coefficient / other.coefficient, self.u - other.u, self.delta - other.delta)

    def __rtruediv__(self, other):
        return box(other) / self

    def __pow__(self, exponent):
        need(type(exponent) is int, 'integral symbolic power')
        need(self.coefficient > 0 or exponent >= 0, 'nonzero negative power')
        return Monomial(self.coefficient**exponent, self.u * exponent, self.delta * exponent)

    def record(self):
        return {'coefficient': str(self.coefficient), 'sqrt_eta_exponent': self.u, 'delta_exponent': self.delta}


def box(value):
    return value if isinstance(value, Monomial) else Monomial(value)


def power2(exponent, u=0, delta=0):
    return Monomial(Q(2)**exponent, u, delta)


U = Monomial(1, 1)
ETA = U**2
DELTA = Monomial(1, 0, 1)
UMAX, DMAX = Q(1, 256), Q(1, 2)


class Certificates:
    def __init__(self):
        self.rows = []

    def comparison(self, name, terms, right, strict=True):
        terms = terms if isinstance(terms, (tuple, list)) else [terms]
        ratios = [box(term) / right for term in terms]
        for ratio in ratios:
            need(ratio.coefficient >= 0, 'nonnegative majorant: ' + name)
            need(ratio.u >= 0 and ratio.delta >= 0, 'uncovered singular ratio: ' + name)
        upper = sum((x.coefficient * UMAX**x.u * DMAX**x.delta for x in ratios), Q(0))
        need(upper < 1 if strict else upper <= 1, 'unproved whole-domain budget: ' + name)
        self.rows.append({'name': name, 'normalized_nonnegative_monomials': [x.record() for x in ratios], 'upper_on_complete_domain': str(upper), 'strict': strict})

    def equal(self, name, left, right):
        need(left == right, 'symbolic exponent/constant identity: ' + name)
        self.rows.append({'name': name, 'identity': left.record()})


@dataclass(frozen=True)
class Domain:
    rho: Q = Q(1,64)
    epsilon: Q = Q(1,32)
    L: int = 2**10
    B1: int = 2**27
    B2: int = 2**39
    s: Q = Q(1,2**52)
    d: Q = Q(1,2**92)
    b: Q = Q(1,2**227)
    G: int = 2**26
    beta: int = 2**11
    gamma: int = 2**16
    R: Monomial = power2(-320,delta=1)
    t: Monomial = power2(-322,delta=1)
    critical: Monomial = power2(-332,4,1)
    coefficient: Monomial = power2(-1999,26,6)


def certificate(p=Domain()):
    c=Certificates()
    r,eps=p.rho,p.epsilon
    eta_complex=eps**2
    m=4*r
    radicand=r+m*m
    n=r*(1+14*(1+r))/2
    du=2*n
    c.comparison('joint complex radicand displacement below2rho',box(radicand),box(2*r))
    c.comparison('joint square-root lower modulus greater1/2',[radicand,Q(1,4)],box(1))
    c.comparison('joint square-root upper modulus less3/2',[Q(3,2),radicand],box(Q(9,4)))
    c.comparison('all heavy u modulus below2',[1,r,du],box(2))
    c.comparison('all heavy h modulus below2',[m,Q(3,2)],box(2))
    c.comparison('small critical scaled modulus below5/64',box(eps*(1+r)+r),box(Q(5,64)))
    c.comparison('heavy critical scaled modulus below33/16',box(2*eps+2),box(Q(33,16)),False)
    c.comparison('exact total first critical coefficient majorant17',box(8*(1+r)+eps*r),box(17))
    az,zz=1+eta_complex,Q(17,16)
    gs=[]
    for k in range(2,9):
        g=sum((comb(2,i)*Q(33,16)**i*comb(6,k-i)*Q(5,64)**(k-i) for i in range(3) if 0<=k-i<=6),Q(0))
        gs.append(g)
    P=9*az**8+Q(9,8)*17*(zz**8+az**8)+sum(Q(9,9-k)*g*eps**(k-2)*(zz**(9-k)+az**(9-k)) for k,g in zip(range(2,9),gs))
    c.comparison('complete anchored polynomial joint Rouche majorant',box(P),box(128))
    rr=Q(1,16)
    c.comparison('fixed ninth-root circle reference lower bound exceeds1/4',[36*(1+rr)**7*rr**2,Q(1,4)],box(9*rr))
    c.comparison('whole joint perturbation smaller than reference1/4',box(128*eps**2),box(Q(1,4)))
    c.comparison('fixed root disks disjoint at separation greater1/2',box(2*rr),box(Q(1,2)))
    normal_M=((1+rr)**2+1)/2
    c.comparison('literal companion root-product half-normal modulus below2',box(normal_M),box(2))
    c.comparison('maximum modulus after complete beta zero order2',box(2/eps**2),box(p.beta),False)
    c.comparison('maximum modulus after complete gamma zero order3',box(2/eps**3),box(p.gamma),False)
    c.comparison('joint reciprocal squared-distance change below1/2',box(10*eta_complex+9*eta_complex**2),box(Q(1,2)))
    numerator=32+8+eta_complex*(8+2*4*p.beta)
    c.comparison('deflated objective undivided numerator below64',box(numerator),box(64))
    c.comparison('double eta zero gives whole joint Graw bound',box(64/eta_complex**2),box(p.G),False)
    c.comparison('actual branch remains within rho/4',19*ETA,box(r/4))
    c.comparison('actual normalized inverse norm below L',box(800),box(p.L))
    c.comparison('sixteen-dimensional normalized first Cauchy derivative',box(p.gamma*32/r),box(p.B1),False)
    c.comparison('sixteen-dimensional normalized second Cauchy derivative',box(2*p.gamma*(32/r)**2),box(p.B2),False)
    c.comparison('complete tail/free product lies inside inner raw rho/2',box(p.s),box(r/4))
    c.comparison('target radius less than complete tail radius',box(p.d),box(p.s))
    c.comparison('full off-branch nonlinear contraction at most1/8',box(p.L*p.B2*p.s),box(Q(1,8)),False)
    c.comparison('full center target drift below tail/4',box(p.L*(p.B1+1)*p.d),box(p.s/4))
    c.comparison('all inactive actual half-normal changes below eta/8',2*ETA*p.B1*p.s,ETA/8)
    c.comparison('real heavy-small separation exceeds sqrteta/4',box(5*r+Q(1,4)),box(Q(1,2)))
    K2=box(2*p.G*(32/p.d)**2)
    K3_exact=box(6*p.G*(32/p.d)**3)
    K3=power2(44)/box(p.d)**3
    c.comparison('full eliminated third derivative factorial accounted',K3_exact,K3)
    c.comparison('entire normalized inward box lies inside d/2',box(2*p.b),box(p.d))
    c.comparison('whole free Euclidean R-ball lies inside inward max box',p.R,box(p.b))
    c.comparison('coarse individual alpha derivative loss at most1/64',K2*p.b,box(Q(1,64)),False)
    c.comparison('actual individual alpha chain rule sharper uniform loss',[(ETA/2)*K2*p.b,(U/2)*K2*p.b],box(Q(257,2**23)),False)
    c.comparison('all four original individual gradients stay above17/64',box(Q(17,64)+Q(1,64)),box(Q(9,32)),False)
    c.comparison('full eliminated Taylor loss bounded by delta eta squared',ETA**2*K3*p.R/6,DELTA*ETA**2/6,False)
    c.comparison('literal twelve-free-coordinate Euclidean entry',12*p.t**2,p.R**2)
    c.comparison('raw-box normals enter entire inward b-box',p.B1*p.t,box(p.b))
    c.comparison('raw-box heavy coordinates lie in full uniqueness s-ball',p.t,box(p.s))
    c.comparison('branch critical modulus less1/32',[4*ETA**2,2*ETA],box(Q(1,1024)))
    c.comparison('critical disks pairwise disjoint even at sixfold small collision',p.critical,ETA/4)
    c.comparison('critical disks contained in unit disk',[Q(1,32),p.critical],box(1))
    c.comparison('heavy critical Rouche contour dominates small-cluster threshold',p.critical**5,Q(9,64)*U**5)
    c.comparison('critical derivative coefficient perturbation strictly less Rouche lower bound',36*p.coefficient,ETA*p.critical**6)
    c.comparison('all eight critical u transports fit raw metric',p.critical/ETA,p.t/1024)
    c.comparison('all eight critical h transports fit raw metric',p.critical/U,p.t/1024)
    c.comparison('heavy T transport fits raw metric',5*p.critical/U,5*p.t/1024)
    c.comparison('total V includes its additional eta divisor',8*p.critical/U**3,8*p.t/1024)
    c.comparison('total M transports every heavy/free cross product',[16*p.critical/ETA,16*p.critical/U,8*p.critical**2/U**3],40*p.t/1024)
    critical_conversion=sum(Q(9,9-k)*comb(7,k-1) for k in range(1,9))
    need(critical_conversion==Q(2295,8),'complete anchored critical coefficient conversion constant')
    need(8*critical_conversion**2<1024**2,'all eight critical displacement energy controls anchored coefficients')
    need(8*max(comb(8,k-1) for k in range(1,10))**2<200**2,'all eight original displacement energy controls every coefficient')
    need(Q(1,4)-Q(33,16)*UMAX**2>Q(1,8),'fixed k1/4 whole-eta gap')
    for name,left,right in [('s',box(p.s),1/(8*box(p.L)*p.B2)),('d',box(p.d),1/(64*box(p.L)**2*p.B1*p.B2)),('b',box(p.b),box(p.d)**2/2**43),('R',p.R,DELTA*box(p.d)**3/2**44),('t',p.t,p.R/4),('critical',p.critical,ETA**2*p.t/2**10),('coefficient',p.coefficient,ETA*p.critical**6/2**7),('fixed k1/4 coefficient',p.coefficient/DELTA**6/2**18,power2(-2017,26))]:
        c.equal('complete symbolic identity '+name,left,right)
    return {'radii':{name:(getattr(p,name).record() if isinstance(getattr(p,name),Monomial) else str(getattr(p,name))) for name in p.__dataclass_fields__},'joint_majorants':{'Gk':list(map(str,gs)),'anchored_polynomial_P':str(P),'literal_half_normal_M':str(normal_M),'raw_objective_numerator':str(numerator)},'K2':K2.record(),'K3_with_factorial':K3_exact.record(),'K3_conservative':K3.record(),'individual_alpha_sharp_loss':str(Q(257,2**23)),'universal_domain':{'sqrt_eta':['positive',str(UMAX)],'delta':['positive',str(DMAX)]},'all_whole_domain_obligations':c.rows,'critical_to_coefficient_constant':str(critical_conversion)}


def controls():
    p=Domain()
    damages=[('joint epsilon root domain too large',replace(p,epsilon=Q(1,8))),
             ('understated removable beta bound',replace(p,beta=2**10)),
             ('understated removable gamma bound',replace(p,gamma=2**15)),
             ('understated double-deflated objective bound',replace(p,G=2**25)),
             ('uncovered actual normalized inverse',replace(p,L=512)),
             ('missing sixteen-dimensional first Cauchy sum',replace(p,B1=2**26)),
             ('missing second Cauchy factorial',replace(p,B2=2**38)),
             ('whole tail loses off-branch contraction',replace(p,s=32*p.s)),
             ('entire target product loses closed-ball drift',replace(p,d=32*p.d)),
             ('individual alpha gradient box too large',replace(p,b=64*p.b)),
             ('zero-slack Taylor ball too large',replace(p,R=8*p.R)),
             ('twelve-free-coordinate Euclidean entry fails',replace(p,t=2*p.t)),
             ('V moment transport misses eta divisor',replace(p,critical=1024*p.critical)),
             ('sixfold critical Rouche coefficient too large',replace(p,coefficient=8*p.coefficient))]
    rejected=[]
    for label,bad in damages:
        try:certificate(bad)
        except ValueError as error:rejected.append({'damage':label,'rejected_by':str(error)})
        else:raise ValueError('semantic damage accepted: '+label)
    for label,term in [('uncovered eta0 inverse',U**-1),('uncovered zero-gap inverse',DELTA**-1)]:
        try:Certificates().comparison(label,term,box(1))
        except ValueError as error:rejected.append({'damage':label,'rejected_by':str(error)})
        else:raise ValueError('singular-domain damage accepted')
    return rejected
