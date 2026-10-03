"""Exact collision-value and boundary-derivative corroboration; stdlib only.

QQ[x,E,G], characteristic zero, ascending z coefficients, monic quotients.
Ordinary feasibility, interlacing and projection arguments are in PROOF.md.
Finite controls never enumerate the actual real-original-root domain.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import time


def require(condition, label):
    if not condition:
        raise ValueError(label)


class Poly:
    """Sparse QQ[x,E,G] polynomials with complete coefficient records."""
    def __init__(self, terms=0):
        if isinstance(terms, Poly):
            terms = terms.terms
        if not isinstance(terms, dict):
            terms = {(0, 0, 0): F(terms)}
        self.terms = {m: F(a) for m, a in terms.items() if a}

    def __add__(self, other):
        d = dict(self.terms)
        for m, a in Poly(other).terms.items():
            d[m] = d.get(m, F(0)) + a
        return Poly(d)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -a for m, a in self.terms.items()})

    def __sub__(self, other):
        return self + -Poly(other)

    def __rsub__(self, other):
        return Poly(other) - self

    def __mul__(self, other):
        d = {}
        for m, a in self.terms.items():
            for n, b in Poly(other).terms.items():
                k = tuple(x + y for x, y in zip(m, n))
                d[k] = d.get(k, F(0)) + a * b
        return Poly(d)

    __rmul__ = __mul__

    def __pow__(self, power):
        require(power >= 0, 'nonnegative polynomial power')
        out = Poly(1)
        for _ in range(power):
            out *= self
        return out

    def __eq__(self, other):
        return self.terms == Poly(other).terms

    def __bool__(self):
        return bool(self.terms)

    def derivative(self, index):
        out = {}
        for m, a in self.terms.items():
            if m[index]:
                n = list(m)
                n[index] -= 1
                out[tuple(n)] = a * m[index]
        return Poly(out)

    def evaluate(self, values):
        out = F(0)
        for m, a in self.terms.items():
            for index, exponent in enumerate(m):
                a *= values[index] ** exponent
            out += a
        return out

    def record(self):
        return [[list(m), str(a)] for m, a in sorted(self.terms.items())]


class Dual:
    """QQ[eps]/(eps^2), retaining moving critical-node derivatives."""
    def __init__(self, a=0, b=0):
        if isinstance(a, Dual):
            self.a, self.b = a.a, a.b
        else:
            self.a, self.b = F(a), F(b)

    def __add__(self, other):
        other = Dual(other)
        return Dual(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Dual(-self.a, -self.b)

    def __sub__(self, other):
        return self + -Dual(other)

    def __rsub__(self, other):
        return Dual(other) - self

    def __mul__(self, other):
        other = Dual(other)
        return Dual(self.a * other.a, self.a * other.b + self.b * other.a)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = Dual(other)
        require(other.a != 0, 'dual divisor is a unit')
        return Dual(self.a / other.a,
                    (self.b * other.a - self.a * other.b) / other.a ** 2)

    def __rtruediv__(self, other):
        return Dual(other) / self

    def __bool__(self):
        return bool(self.a or self.b)

    def __eq__(self, other):
        other = Dual(other)
        return self.a == other.a and self.b == other.b

    def __pow__(self, power):
        require(power >= 0, 'nonnegative dual power')
        out = Dual(1)
        for _ in range(power):
            out *= self
        return out


class Jet:
    """QQ[eps]/(eps^3); c is the quadratic coefficient, half the derivative."""
    def __init__(self, a=0, b=0, c=0):
        if isinstance(a, Jet):
            self.a, self.b, self.c = a.a, a.b, a.c
        else:
            self.a, self.b, self.c = F(a), F(b), F(c)

    def __add__(self, other):
        o = Jet(other)
        return Jet(self.a+o.a, self.b+o.b, self.c+o.c)
    __radd__ = __add__

    def __neg__(self):
        return Jet(-self.a, -self.b, -self.c)

    def __sub__(self, other):
        return self + -Jet(other)

    def __rsub__(self, other):
        return Jet(other) - self

    def __mul__(self, other):
        o = Jet(other)
        return Jet(self.a*o.a, self.a*o.b+self.b*o.a,
                   self.a*o.c+self.b*o.b+self.c*o.a)
    __rmul__ = __mul__

    def __truediv__(self, other):
        o = Jet(other)
        require(o.a != 0, 'jet divisor is a unit')
        a = self.a/o.a
        b = (self.b-a*o.b)/o.a
        c = (self.c-a*o.c-b*o.b)/o.a
        return Jet(a,b,c)

    def __rtruediv__(self, other):
        return Jet(other)/self

    def __pow__(self, power):
        require(power >= 0, 'nonnegative jet power')
        out = Jet(1)
        for _ in range(power):
            out *= self
        return out

    def __bool__(self):
        return bool(self.a or self.b or self.c)

    def __eq__(self, other):
        o = Jet(other)
        return (self.a,self.b,self.c) == (o.a,o.b,o.c)


def transpose(a):
    return [list(row) for row in zip(*a)]


def matvec(a, x):
    return [sum(v * w for v, w in zip(row, x)) for row in a]


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def matmul(a, b):
    return [[dot(row, col) for col in transpose(b)] for row in a]


def solve(a, b):
    n = len(a)
    aug = [list(row) + [value] for row, value in zip(a, b)]
    for col in range(n):
        def unit(value):
            return value.a != 0 if isinstance(value, (Dual, Jet)) else bool(value)
        pivot = next((r for r in range(col, n) if unit(aug[r][col])), None)
        require(pivot is not None, 'nonsingular exact linear system')
        aug[col], aug[pivot] = aug[pivot], aug[col]
        divisor = aug[col][col]
        aug[col] = [x / divisor for x in aug[col]]
        for row in range(n):
            if row != col:
                factor = aug[row][col]
                aug[row] = [x - factor * y for x, y in zip(aug[row], aug[col])]
    return [row[-1] for row in aug]


def trim(p):
    p = list(p)
    while p and not p[-1]:
        p.pop()
    return p


def mul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return trim(out)


def divrem(a, b):
    a, b = trim(a), trim(b)
    require(bool(b), 'polynomial divisor nonzero')
    q = [0] * max(0, len(a) - len(b) + 1)
    while len(a) >= len(b):
        k = len(a) - len(b)
        factor = a[-1] / b[-1]
        q[k] += factor
        for i, x in enumerate(b):
            a[i + k] -= factor * x
        a = trim(a)
    return trim(q), a


def derivative(p):
    return [i * p[i] for i in range(1, len(p))]


def newton(h, count):
    n = len(h) - 1
    out = [F(n)]
    for k in range(1, count + 1):
        if k <= n:
            value = -sum(h[n - i] * out[k - i] for i in range(1, k)) - k * h[n - k]
        else:
            value = -sum(h[n - i] * out[k - i] for i in range(1, n + 1))
        out.append(value)
    return out


def sturm_count(p):
    chain = [trim(p), trim(derivative(p))]
    while chain[-1]:
        _, remainder = divrem(chain[-2], chain[-1])
        if not remainder:
            break
        chain.append([-x for x in remainder])
    def variations(signs):
        signs = [x for x in signs if x]
        return sum(x != y for x, y in zip(signs, signs[1:]))
    positive = [1 if q[-1] > 0 else -1 for q in chain]
    negative = [v * (-1) ** (len(q) - 1) for q, v in zip(chain, positive)]
    return variations(negative) - variations(positive)


def chart(x, e, g):
    j = -x**7 + F(3,8)*x**5 - e*x**3 - g*x
    c = 7*x**8-F(5,2)*x**6+6*e*x**4+4*g*x**2
    q = [7*x**6-F(5,2)*x**4+6*e*x**2+4*g,
         6*x**5-2*x**3+4*e*x, 5*x**4-F(3,2)*x**2+2*e,
         4*x**3-x, 3*x**2-F(1,2), 2*x, F(1)]
    r = [x**6-F(3,8)*x**4+e*x**2+g,
         x**5-F(3,8)*x**3+e*x, x**4-F(3,8)*x**2+e,
         x**3-F(3,8)*x, x**2-F(3,8), x, F(1)]
    f = [c,8*j,4*g,0,2*e,0,-F(1,2),0,F(1)]
    h = [j,g,0,e,0,-F(3,8),0,F(1)]
    return j,c,q,r,f,h


def peval(p, x):
    return sum(a*x**i for i,a in enumerate(p))


def coupling(j,e,g):
    return [F(1),F(0),F(3,8)-8*e,F(0),F(9,64)-4*e-24*g,-56*j]


def universal():
    x,e,g = [Poly({tuple(int(i==k) for i in range(3)):1}) for k in range(3)]
    j,c,q,r,f,h = chart(x,e,g)
    require(mul(mul([-x,Poly(1)],[-x,Poly(1)]),q)==f,'entire double-factor identity')
    require(mul([-x,Poly(1)],r)==h,'entire canceled critical identity')
    require(derivative(f)==[8*a for a in h],'full original derivative')
    require(peval(q,x)==4*peval(derivative(h),x),'Q(x)=4 hprime(x)')
    require(j.derivative(0)==-peval(derivative(h),x),'Jx=-hprime(x)')
    require(c.derivative(0)==8*x*peval(derivative(h),x),'cx=8x hprime(x)')
    tau = [Poly(a) for a in newton(h,10)]
    sigma = [Poly(a) for a in newton(r,10)]
    require(all(sigma[k]==tau[k]-x**k for k in range(11)), 'all eleven canceled traces')
    nu = [Poly(a) for a in coupling(j,e,g)]
    zr = [Poly(0)]+r
    xq = mul([-x,Poly(1)],q)
    numerator = trim([8*(a-b) for a,b in zip(zr,xq)])
    require(len(numerator)==6,'whole canceled resolvent degree five')
    reverse = list(reversed(r))
    derived = []
    for k in range(6):
        derived.append(numerator[5-k]-sum(reverse[i]*derived[k-i] for i in range(1,k+1)))
    require(derived==nu,'entire canceled resolvent moments')
    K = [[sigma[i+k] for k in range(6)] for i in range(6)]
    mu = [Poly(a) for a in newton(f,7)]
    require(mu[1]==0 and mu[2]==1 and mu[3]==0 and mu[5]==0,'all original normalizations and two zero odd moments')
    require(mu[4]-F(1,8)==F(3,8)-8*e and mu[7]==-56*j,'whole D and seventh original moment')
    rec = {'J':j.record(),'c':c.record(),'Q':[a.record() if isinstance(a,Poly) else Poly(a).record() for a in q],
           'r':[Poly(a).record() for a in r],'f':[Poly(a).record() for a in f],
           'h':[Poly(a).record() for a in h], 'h_traces':[a.record() for a in tau],
           'r_traces':[a.record() for a in sigma], 'nu':[a.record() for a in nu],
           'canceled_resolvent_numerator':[a.record() for a in numerator],
           'K':[[a.record() for a in row] for row in K],
           'K_derivatives':[[[a.derivative(t).record() for a in row] for row in K] for t in range(3)],
           'nu_derivatives':[[a.derivative(t).record() for a in nu] for t in range(3)],
           'original_moments':[a.record() for a in mu]}
    return rec,K,nu


def quotient_eta(r, numerator, freeze_nodes=False):
    # Bezout inversion of r', then Newton trace of the full mass square.
    if freeze_nodes:
        r = [Dual(a.a) if isinstance(a,Dual) else a for a in r]
    n = len(r)-1
    rp = derivative(r)
    columns = []
    for k in range(n):
        remainder = divrem([0]*k+rp,r)[1]
        columns.append(remainder+[0]*(n-len(remainder)))
    target = divrem(numerator,r)[1]
    target += [0]*(n-len(target))
    p = solve(transpose(columns),target)
    pp = mul(p,p)
    traces = newton(r,2*n-2)
    return sum(a*traces[k] for k,a in enumerate(pp)),p


def boundary_eta(x,e,g, freeze_nodes=False):
    _,_,q,r,_,_ = chart(x,e,g)
    return quotient_eta(r,[-8*a for a in mul([-x,F(1)],q)],freeze_nodes)


def schur_H(tau,nu,j):
    even=[0,2,4];odd=[1,3,5]
    A=[[tau[i+k] for k in even] for i in even]
    B=[[tau[i+k] for k in odd] for i in odd]
    U=[[F(0),F(0),F(0)],[F(0),F(0),F(-7)],[F(0),F(-7),-F(27,8)]]
    y=solve(A,[nu[i] for i in even])
    w=[a-b for a,b in zip([0,0,-56],matvec(transpose(U),y))]
    AU=transpose([solve(A,col) for col in transpose(U)])
    W=matmul(transpose(U),AU)
    S=[[B[i][k]-j*j*W[i][k] for k in range(3)] for i in range(3)]
    s=solve(S,w)
    return dot(s,matvec(B,s))


def control(label,x,e,g,require_six_Q=True):
    j,c,q,r,f,h=chart(x,e,g)
    nq,nr=sturm_count(q),sturm_count(r)
    if require_six_Q:
        require(nq==6,'six actual real simple remaining original roots')
    require(nr==6,'six real distinct canceled critical nodes')
    D=F(3,8)-8*e
    require(D>0,'positive quartic variance')
    sigma=newton(r,10);tau=newton(h,10);nu=coupling(j,e,g)
    K=[[sigma[i+k] for k in range(6)] for i in range(6)]
    beta=solve(K,nu);R=dot(nu,beta);C=(1-R)/D
    eta,p=boundary_eta(x,e,g)
    require(eta==R and p==beta,'whole six-node quotient and moment reconstruction agree')
    rec={'label':label,'x_E_G_J_c':[str(a) for a in [x,e,g,j,c]],
         'Q_real_distinct_count':nq,'r_real_distinct_count':nr,
         'h_real_distinct_count':sturm_count(h),'Qx':str(peval(q,x)),
         'whole_beta':[str(a) for a in beta],'eta_D_C':[str(a) for a in [eta,D,C]]}
    if not require_six_Q:
        require(nq<6,'explicit infeasible primitive retained')
        return rec
    record,Kp,nup=universal()
    gradients=[]
    for t in range(3):
        values=[x,e,g]
        Kt=[[a.derivative(t).evaluate(values) for a in row] for row in Kp]
        nut=[a.derivative(t).evaluate(values) for a in nup]
        Rt=2*dot(beta,nut)-dot(beta,matvec(Kt,beta))
        Ct=((8*C if t==1 else 0)-Rt)/D
        dv=[Dual(a,int(i==t)) for i,a in enumerate(values)]
        moving,pp=boundary_eta(*dv)
        require(moving.a==eta and moving.b==Rt,'entire moving-node eta derivative')
        cd=(1-moving)/(F(3,8)-8*dv[1])
        require(cd.a==C and cd.b==Ct,'full C derivative including D motion')
        gradients.append(Ct)
    vx=[x**i for i in range(6)]
    M=[[tau[i+k] for k in range(6)] for i in range(6)]
    bstar=solve(M,nu);pstar=dot(vx,bstar)
    L=1-dot(vx,solve(M,vx));R6=dot(nu,bstar)
    require(L>0 and eta==R6+pstar*pstar/L,'exact rank-one collision deficit')
    H=schur_H(tau,nu,j)
    require(H>196*(D+F(1,14))**2,'strict quantitative parity bound at actual boundary')
    rec.update({'all_three_moving_C_derivatives':[str(a) for a in gradients],
                'whole_center_beta':[str(a) for a in bstar],
                'pstar_L_R6_H':[str(a) for a in [pstar,L,R6,H]]})
    hp=peval(derivative(h),x)
    if hp:
        # Full degree-seven c derivative: the canceled node has zero mass,
        # but its motion-free constant-fiber response must still be retained.
        fd=[Dual(a,int(i==0)) for i,a in enumerate(f)]
        hd=[Dual(a) for a in h]
        ef,_=quotient_eta(hd,[-8*a for a in fd])
        g0=-ef.b/D
        split=-peval(q,x)*g0
        require(split==64*pstar/(D*L),'whole legal splitting derivative')
        require(g0==-16*pstar/(D*hp*L),'full constant derivative sign')
        perturbed=list(f);perturbed[0]-=F(1,10**12)*peval(q,x)
        require(sturm_count(perturbed)==8,'exact small legal splitting control')
        require(-8*peval(perturbed,x)/hp==32*F(1,10**12),'exact new critical mass is 32t')
        rec.update({'g0_splitting_derivative':[str(g0),str(split)],'small_split_distinct_real_originals':8})
    else:
        require(peval(q,x)==0 and peval(derivative(q),x)!=0,'exact triple original, not fourfold')
        require(pstar==0 and peval(beta,x)==0 and bstar==beta,'triple zero mass and exact algebraic center')
        require(L==F(1,2) and gradients[0]==0,'triple duplicate leverage and zero first x derivative')
        pprime=peval(derivative(beta),x);hpp=peval(derivative(derivative(h)),x)
        predicted=(2*j*hpp*H-4*pprime*pprime)/D
        etajet,_=boundary_eta(Jet(x,1),Jet(e),Jet(g))
        cjet=(1-etajet)/D
        require(cjet.a==C and cjet.b==0 and 2*cjet.c==predicted,'whole triple curvature with moving nodes')
        rec.update({'triple_pprime_hsecond_Cxx':[str(pprime),str(hpp),str(predicted)]})
    return rec


def build_record():
    uni,_,_=universal()
    controls=[control('zero double',F(0),F(11,288),-F(1,1152)),
              control('nonsymmetric positive center at a single double',F(1,100),F(11,288),-F(1,1152)),
              control('positive center near paired boundary',F(1,4),F(21,512),-F(859439,640000000)),
              control('negative center at a single double',F(1,3),F(13,288),-F(12811771,7290000000)),
              control('triple original with repeated full critical',F(1,40),F(1,40),-F(189007,4096000000)),
              control('second triple control',F(1,20),F(3,125),-F(10777,64000000)),
              control('infeasible six-node critical spectrum',F(1,20),F(11,288),-F(1,1152),False)]
    require(F(controls[1]['pstar_L_R6_H'][0])>0 and F(controls[3]['pstar_L_R6_H'][0])<0,
            'both physical splitting signs occur')
    require(all(F(controls[k]['triple_pprime_hsecond_Cxx'][2])>0 for k in [4,5]),
            'both stated actual triple controls have positive curvature')
    damages={}
    def reject(label,fn):
        try:fn()
        except ValueError:damages[label]='rejected'
        else:raise ValueError('mathematical damage escaped: '+label)
    reject('omitted original feasibility',lambda:require(controls[-1]['Q_real_distinct_count']==6,'six r nodes do not imply six Q roots'))
    reject('splitting universally improves',lambda:require(F(controls[3]['g0_splitting_derivative'][1])>0,'actual negative splitting derivative'))
    reject('wrong normal sign',lambda:require(F(controls[1]['g0_splitting_derivative'][1])<0,'actual positive splitting derivative'))
    reject('triple treated as simple full critical',lambda:require(controls[4]['h_real_distinct_count']==7,'exact full critical collision'))
    reject('triple angular mass nonzero',lambda:require(F(controls[4]['pstar_L_R6_H'][0])>0,'exact zero repeated-node mass'))
    reject('triple leverage discarded',lambda:require(F(controls[4]['pstar_L_R6_H'][1])==1,'exact duplicate leverage is one half'))
    reject('rank-one cost dropped',lambda:require(F(controls[1]['eta_D_C'][0])==F(controls[1]['pstar_L_R6_H'][2]),'strict actual collision cost'))
    x,e,g=map(F,controls[1]['x_E_G_J_c'][:3])
    moving,_=boundary_eta(Dual(x),Dual(e,1),Dual(g))
    frozen,_=boundary_eta(Dual(x),Dual(e,1),Dual(g),True)
    reject('frozen critical nodes',lambda:require(frozen.b==moving.b,'whole moving-node derivative differs'))
    C=F(controls[1]['eta_D_C'][2]);D=F(controls[1]['eta_D_C'][1])
    reject('omitted denominator derivative',lambda:require(-moving.b/D==F(controls[1]['all_three_moving_C_derivatives'][1]),'D_E=-8 is essential'))
    return {'actual_agent':'six-sendov-2','role':'researcher',
            'status':'complete ordinary author proof with exact corroboration; unformalized and independently unreviewed',
            'universal':uni,'controls':controls,'mathematical_damages':damages}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--expected',type=Path,default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--emit',type=Path)
    args=parser.parse_args();start=time.monotonic()
    record=build_record();encoded=(json.dumps(record,sort_keys=True,separators=(',',':'))+'\n').encode()
    if args.emit:args.emit.write_bytes(encoded)
    else:require(args.expected.read_bytes()==encoded,'external whole canonical expected fixture')
    print(json.dumps({'verified':True,'record_sha256':hashlib.sha256(encoded).hexdigest(),
                      'record_bytes':len(encoded),'controls':len(record['controls']),
                      'mathematical_damages':len(record['mathematical_damages']),
                      'seconds':time.monotonic()-start}))


if __name__=='__main__':main()
