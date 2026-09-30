#!/usr/bin/env python3
"""Standalone exact author derivation for PROOF.md.

Agent six-sendov-2, role researcher. Q[d±1,v±1][j]/(j²+v/4).
Laurent arithmetic is adapted from this author's three-block checker;
no campaign checker, floating-point package or solver is imported."""
from fractions import Fraction as Q
from hashlib import sha256
from math import factorial, comb
from pathlib import Path
import json

class L:
    def __init__(self, value=0):
        if isinstance(value, L):
            value = value.t
        if isinstance(value, (int, Q)):
            value = {(0, 0): Q(value)}
        self.t = {p: Q(c) for p, c in value.items() if c}

    def __add__(self, other):
        other = L(other)
        t = dict(self.t)
        for p, c in other.t.items():
            t[p] = t.get(p, Q(0)) + c
        return L(t)

    __radd__ = __add__

    def __neg__(self):
        return L({p: -c for p, c in self.t.items()})

    def __sub__(self, other):
        return self + -L(other)

    def __rsub__(self, other):
        return L(other) + -self

    def __mul__(self, other):
        other = L(other)
        t = {}
        for p, c in self.t.items():
            for r, b in other.t.items():
                s = (p[0] + r[0], p[1] + r[1])
                t[s] = t.get(s, Q(0)) + c*b
        return L(t)

    __rmul__ = __mul__

    def __pow__(self, n):
        if n < 0:
            if len(self.t) != 1:
                raise ValueError('inverse requires one monomial unit')
            p, c = next(iter(self.t.items()))
            return L({(p[0]*n, p[1]*n): c**n})
        out = L(1)
        for _ in range(n):
            out *= self
        return out

    def __truediv__(self, other):
        return self * L(other)**-1

    def __rtruediv__(self, other):
        return L(other) * self**-1

    def __eq__(self, other):
        return self.t == L(other).t

    def at(self, d0, v0=None):
        out = L(0)
        for (dp, kp), c in self.t.items():
            if v0 is None:
                out += L({(0, kp): c*Q(d0)**dp})
            else:
                out += c*Q(d0)**dp*Q(v0)**kp
        return out

    def dump(self):
        return [[p[0], p[1], str(c)] for p, c in sorted(self.t.items())]


d = L({(1,0):1})
v = L({(0,1):1})
u = (v-1)/3
a = d-1
gamma = v/4
SIZE = 7
checks = 0

def check(label,x,y=0):
    global checks
    if x != y:
        raise ArithmeticError(label+': '+str(x))
    checks += 1

class G:
    def __init__(self,re=0,im=0):
        if isinstance(re,G):
            self.re,self.im=re.re,re.im
        else:
            self.re,self.im=L(re),L(im)
    def __add__(self,o):
        o=G(o); return G(self.re+o.re,self.im+o.im)
    __radd__=__add__
    def __neg__(self):return G(-self.re,-self.im)
    def __sub__(self,o):return self+-G(o)
    def __rsub__(self,o):return G(o)+-self
    def __mul__(self,o):
        o=G(o)
        return G(self.re*o.re-gamma*self.im*o.im,self.re*o.im+self.im*o.re)
    __rmul__=__mul__
    def __truediv__(self,o):
        o=G(o)
        if o.im != 0:raise ValueError('only real monomial divisions')
        return G(self.re/o.re,self.im/o.re)
    def __eq__(self,o):
        o=G(o);return self.re==o.re and self.im==o.im
    def conj(self):return G(self.re,-self.im)
    def dump(self):return {'re':self.re.dump(),'im':self.im.dump()}
    def __repr__(self):return str(self.dump())

def c(x):return [G(x)]+[G() for _ in range(SIZE-1)]
def add(x,y):return [a+b for a,b in zip(x,y)]
def neg(x):return [-a for a in x]
def sub(x,y):return add(x,neg(y))
def scale(x,s):return [a*s for a in x]
def mul(x,y):
    return [sum((x[j]*y[i-j] for j in range(i+1)),G()) for i in range(SIZE)]
def inv(x):
    out=[G(1)/x[0]]
    for i in range(1,SIZE):
        out.append(-sum((x[j]*out[i-j] for j in range(1,i+1)),G())/x[0])
    check('inverse',mul(x,out),c(1))
    return out
def sqrt(x,base):
    check('sqrt base',G(base)*G(base),x[0]);out=[G(base)]
    for i in range(1,SIZE):
        out.append((x[i]-sum((out[j]*out[i-j] for j in range(1,i)),G()))/(2*base))
    check('sqrt square',mul(out,out),x)
    return out

def cos(q):
    return [G((-1)**(i//2)*q**(i//2)/factorial(i)) if i%2==0 else G() for i in range(SIZE)]
C1=cos(L(1));Cb=cos(u)
T=[G(),G(1)]+[G() for _ in range(SIZE-2)]
def q(z,ct):return add(add(mul(z,z),scale(mul(ct,z),2)),c(1))
def residual(z):
    q1=q(z,C1);qb=q(z,Cb)
    der=add(scale(mul(add(z,C1),qb),6),scale(mul(add(z,Cb),q1),2))
    return add(mul(q1,qb),mul(sub(z,c(a)),der))

def specialize_v(x,v0):
    out=L(0)
    for (i,j),cf in x.t.items():out+=L({(i,0):cf*Q(v0)**j})
    return out

def polynomial_product(x,y):
    """Polynomials in z, with coefficients that are exact t-series."""
    out=[c(0) for _ in range(len(x)+len(y)-1)]
    for i,xi in enumerate(x):
        for j,yj in enumerate(y):out[i+j]=add(out[i+j],mul(xi,yj))
    return out

def product_rule_controls():
    q1=[c(1),scale(C1,2),c(1)]
    qb=[c(1),scale(Cb,2),c(1)]
    za=[c(-a),c(1)]
    p=za
    for factor in (q1,q1,q1,qb):p=polynomial_product(p,factor)
    actual=[scale(p[i],i) for i in range(1,len(p))]
    first=polynomial_product(q1,qb)
    x=polynomial_product([C1,c(1)],qb)
    y=polynomial_product([Cb,c(1)],q1)
    derivative=[add(scale(xi,6),scale(yi,2)) for xi,yi in zip(x,y)]
    second=polynomial_product(za,derivative)
    rp=[add(x,y) for x,y in zip(first,second)]
    factored=polynomial_product(polynomial_product(q1,q1),rp)
    for i in range(9):check('product rule coefficient '+str(i),actual[i],factored[i])
    # H0(h) is recovered coefficient by coefficient without sampling h.
    leading=[]
    for r in range(4):
        leading.append(sum((rp[i][3-r]*comb(i,r)*(-1)**(i-r)
                            for i in range(r,len(rp))),G()))
    check('desingularized leading polynomial',leading,
          [G(),G(-2*d*v),G(),G(-8*d)])
    return rp

def balanced_endpoint():
    """Separate residual quadratic for p=(z-a)q1^4 at u=1."""
    def rq(z):
        return add(add(scale(mul(z,z),9),
                       mul(sub(scale(C1,10),c(8*a)),z)),
                   sub(c(1),scale(C1,8*a)))
    far=c((8*a-1)/9)
    for i in range(1,5):far[i]=-rq(far)[i]/(8*d)
    check('balanced quadratic residual',rq(far)[:5],[G() for _ in range(5)])
    near=sub(scale(sub(c(8*a),scale(C1,10)),Q(1,9)),far)
    norm=sub(c(d**2),scale(sub(c(1),C1),2*a))
    f=add(add(inv(sub(c(a),far)),inv(sub(c(a),near))),
          scale(inv(sqrt(norm,d)),6))
    return f

def derivation():
    rp=product_rule_controls()
    far=c((8*a-1)/9)
    for i in range(1,5):far[i]=-residual(far)[i]/(512*d**3/81)
    check('far implicit coefficients',residual(far)[:5],[G() for _ in range(5)])
    near=[]
    for h0 in (G(),G(0,1),G(0,-1)):
        h=c(h0);derivative=-2*d*v if h0==0 else 4*d*v
        for i in range(1,4):
            zz=add(c(-1),mul(T,h))
            h[i]=-residual(zz)[3+i]/derivative
        zz=add(c(-1),mul(T,h))
        check('near implicit coefficients',residual(zz),[G() for _ in range(SIZE)])
        near.append(zz)
    for i in range(5):check('conjugate labels',near[1][i].conj(),near[2][i])
    root_factors=[c(9)]
    for z in [far]+near:
        root_factors=polynomial_product(root_factors,[neg(z),c(1)])
    for i in range(5):
        check('complete quartic coefficient '+str(i),root_factors[i][:5],rp[i][:5])
    def modulus_reciprocal(z,base):
        distance=sub(c(a),z)
        norm=mul(distance,[x.conj() for x in distance])
        for i in range(5):check('real norm',norm[i].im)
        return inv(sqrt(norm,base))
    # Individual residual roots count four critical points; q1² counts four.
    F=add(add(modulus_reciprocal(far,d/9),modulus_reciprocal(near[0],d)),
          add(modulus_reciprocal(near[1],d),modulus_reciprocal(near[2],d)))
    norm1=sub(c(d**2),scale(sub(c(1),C1),2*a))
    F=add(F,scale(inv(sqrt(norm1,d)),4))
    def eroot(ct):
        delta=sub(c(1),ct)
        return scale(mul(delta,inv(sub(c(d**2),scale(delta,2*a)))),2/d**2)
    E=add(scale(eroot(C1),6),scale(eroot(Cb),2))
    mu2=6+2*u
    N=2058+21912*u-15876*u**2+19224*u**3+3402*u**4
    D=(3+u)*v**2
    p=Q(10985,33554432)
    check('F0',F[0],16/d)
    for i in (1,3):check('F odd',F[i])
    for i in range(5):check('F real',F[i].im)
    check('far w2',far[2],(3+u)*(4*d-9)/(288*d))
    check('F2 free a',F[2],mu2*(a-Q(5,8))/d**3)
    check('E2 free a',E[2],mu2/d**4)
    for i in (0,1,3):check('energy zero/odd',E[i])
    check('cutoff F4 angular identity',F[4].re.at(Q(13,8)), -2*p*N/v**2/Q(13,8)**8)
    check('E4 free a',E[4],(6+2*u**2)*(a/d**6-1/(12*d**4)))
    A0=-768+1280*v+1632*v**2+8208*v**3-443*v**4
    A1=-6144+10240*v-36096*v**2-1920*v**3-856*v**4
    A2=-12288+20480*v+13824*v**2-768*v**3+784*v**4
    numerator=A0+d*A1+d**2*A2
    check('varying a energy quartic',(d*(a-Q(5,8))*E[4].re-F[4].re)*d**5*v**2, numerator/36864)
    r0=4*u/v;rp=3*(1-u)**2/(8*v);psi=r0**2+2*rp**2
    check('classical weight sum',r0+2*rp,mu2/8)
    check('cutoff angular comparison',-F[4].re.at(Q(13,8))*Q(13,8)**8, p*(224*(6+2*u**2)+122*mu2**2-5760*psi))
    check('scalar J numerator',N,(224*(6+2*u**2)+122*mu2**2-5760*psi)*v**2/2)
    old_k6=d**3*((48*d**2-40*d-53)/3072+(16*d**2-216*d+405)/16384)
    check('three block u0 free a',specialize_v(numerator,1)*d**3,36864*36*old_k6)
    balanced=balanced_endpoint()
    for i in range(5):
        check('balanced endpoint coefficient '+str(i),specialize_v(F[i].re,4),balanced[i].re)
        check('balanced endpoint imaginary part',balanced[i].im)
    return {'F':[x.re.dump() for x in F[:5]],'E':[x.re.dump() for x in E[:5]],
            'far':[x.dump() for x in far[:5]],
            'near':[[x.dump() for x in z[:5]] for z in near]}

def pa(x,y):
    out=[Q(0)]*max(len(x),len(y))
    for i,a in enumerate(x):out[i]+=a
    for i,a in enumerate(y):out[i]+=a
    return out

def pm(x,y):
    out=[Q(0)]*(len(x)+len(y)-1)
    for i,a in enumerate(x):
        for j,b in enumerate(y):out[i+j]+=a*b
    return out

def pd(x):return [i*x[i] for i in range(1,len(x))]

def pe(x,t):
    out=Q(0)
    for a in reversed(x):out=out*t+a
    return out

def optimizer_controls():
    n=[Q(x) for x in (2058,21912,-15876,19224,3402)]
    den=[Q(x) for x in (3,19,33,9)]
    pol=[Q(x) for x in (26634,-231084,-907290,376920,971190,224532,30618)]
    check('factored J denominator',den,pm([3,1],pm([1,3],[1,3])))
    check('derivative polynomial',pa(pm(pd(n),den),[-x for x in pm(n,pd(den))]),pol)
    signs=[1 if x>0 else -1 for x in pol if x]
    check('Descartes variations',sum(x!=y for x,y in zip(signs,signs[1:])),2)
    points=[Q(0),Q(2,25),Q(9,100),Q(1,10),Q(1)]
    values=[pe(pol,t) for t in points]
    expected=[Q(26634),Q(628449891402,244140625),
              Q(-586386216716331,500000000000),Q(-2535492531,500000),Q(491520)]
    check('isolating exact signs and values',values,expected)
    check('endpoint J0',pe(n,0)/pe(den,0),686)
    check('endpoint J1',pe(n,1)/pe(den,1),480)
    interior=pe(n,Q(1,10))/pe(den,Q(1,10))
    check('strict global control',interior>686,True)
    check('interior value',interior,Q(20550021,26195))
    # Strict positivity of N: N=positive polynomial+15876*u*(1-u).
    check('positive N decomposition',n,
          pa([2058,6036,0,19224,3402],[0,15876,-15876]))
    controls=[]
    for t in (Q(0),Q(1,9),Q(9,100),Q(1)):
        j=pe(n,t)/pe(den,t);b=Q(106496,5)/j
        controls.append({'u':str(t),'J':str(j),'B':str(b)})
    check('three block endpoint B',Q(controls[0]['B']),Q(53248,1715))
    check('rational inner witness B',Q(controls[1]['B']),Q(23296,855))
    check('balanced two block endpoint B',Q(controls[3]['B']),Q(3328,75))
    check('strict improvement',Q(controls[2]['B'])<Q(controls[0]['B']),True)
    lo,hi=Q(2,25),Q(9,100)
    for _ in range(45):
        mid=(lo+hi)/2;val=pe(pol,mid)
        if not val:raise ArithmeticError('unexpected exact root; certificate must be revised')
        if val>0:lo=mid
        else:hi=mid
    check('refined root signs',pe(pol,lo)>0 and pe(pol,hi)<0,True)
    def interval(coef):
        low=high=Q(0)
        for i,a in enumerate(coef):
            x,y=a*lo**i,a*hi**i;low+=min(x,y);high+=max(x,y)
        return low,high
    nl,nh=interval(n);dl,dh=interval(den)
    check('positive interval denominators',nl>0 and dl>0,True)
    lower=Q(106496,5)*dl/nh;upper=Q(106496,5)*dh/nl
    check('certified B lower',Q(27106707,1000000)<lower,True)
    check('certified B upper',upper<Q(27106708,1000000),True)
    return {'N':[str(x) for x in n],'D':[str(x) for x in den],
            'P':[str(x) for x in pol],
            'sign_controls':[{'u':str(t),'P':str(y)} for t,y in zip(points,values)],
            'profiles':controls,'u_star_interval':[str(lo),str(hi)],
            'B_star_interval':['27106707/1000000','6776677/250000']}

def phase_jet_controls():
    # A different reduction for F2: far logarithmic implicit equation,
    # derivative-root Vieta moments, and individual modulus coefficients.
    separation=8*d/9
    gz=8*d/separation**2
    gzz=-16*d/separation**3
    mixed=-10*d/(9*separation**3)  # coefficient of i*mu1 in g_zt
    # c1=-i*mu1/72, so the product of the two i factors is -1.
    mean_square_far=-(-gzz/(2*72**2)+mixed/72)/gz
    moment_far=(d/(9*separation**3))*(separation/2-1)/gz
    check('general far mean-square coefficient',mean_square_far,1/(512*d))
    check('general far second-moment coefficient',moment_far,(4*d-9)/(576*d))
    check('Vieta derivative-root second moment',Q(49,64)-Q(3,4),Q(1,64))
    moment_f2=4/(9*d**2)+80*moment_far/d**2-3/(8*d**3)
    mean_f2=80*mean_square_far/d**2-1/(128*d**3)-9/(128*d**3)
    check('general F2 second-moment coefficient',moment_f2,(a-Q(5,8))/d**3)
    check('general F2 mean-square coefficient',mean_f2,5/(64*d**3))
    check('cutoff nonlinear phase mean coefficient',mean_f2.at(Q(13,8),1),Q(40,2197))
    return {'cutoff_phase_mean_t4_coefficient':'40/2197',
            'phase_multiplicities':[3,3,1,1]}

def manifest():
    coefficient=derivation()
    payload=json.dumps(coefficient,sort_keys=True,separators=(',',':')).encode()
    optimizer=optimizer_controls()
    phase_jet=phase_jet_controls()
    return {'agent':'six-sendov-2','role':'researcher','critical_count':8,
            'coefficient_ring':'Q[d,d^-1,v,v^-1][j]/(j^2+v/4)',
            'coefficient_sha256':sha256(payload).hexdigest(),
            'exact_checks':checks,'optimizer':optimizer,'phase_jet':phase_jet}

def compare(actual,expected):
    if actual!=expected:raise ValueError('complete manifest mismatch')

def rejection_controls(actual):
    from copy import deepcopy
    candidates=[]
    for field in ('critical_count','coefficient_sha256','exact_checks'):
        x=deepcopy(actual);x[field]='changed';candidates.append(x)
    x=deepcopy(actual);x['optimizer']['P'][0]='26635';candidates.append(x)
    x=deepcopy(actual);x['optimizer']['u_star_interval'].reverse();candidates.append(x)
    x=deepcopy(actual);x['optimizer']['profiles'][1]['B']='53248/1715';candidates.append(x)
    for x in candidates:
        try:compare(actual,x)
        except ValueError:continue
        raise ArithmeticError('malformed manifest accepted')
    return len(candidates)

if __name__=='__main__':
    actual=manifest()
    expected=json.loads(Path(__file__).with_name('expected.json').read_text())
    compare(actual,expected)
    rejected=rejection_controls(actual)
    print(json.dumps({'exact_checks':actual['exact_checks'],
                      'coefficient_sha256':actual['coefficient_sha256'],
                      'B_star_interval':actual['optimizer']['B_star_interval'],
                      'rejected_corrupt_manifests':rejected},sort_keys=True))
