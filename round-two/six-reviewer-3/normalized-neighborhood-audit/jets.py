"""Universal moment/Newton/root jets over rational polynomial rings.

No author program or result is an input. Epsilon series are truncated at
degree four, i^2=-1, and the ninth-root coordinate obeys omega^9=1.
"""
from fractions import Fraction as Q
from math import comb


def need(ok, message):
    if not ok:
        raise ValueError(message)


class Ring:
    def __init__(self, names, truncated=None, period=None, gaussian=None):
        self.names = tuple(names.split())
        self.truncated = truncated
        self.period = period
        self.gaussian = gaussian

    def poly(self, value=0):
        if isinstance(value, Poly):
            need(value.r is self, 'polynomial ring mismatch')
            return value
        return Poly(self, {tuple(0 for _ in self.names): Q(value)})

    def variable(self, name):
        exponents = [0]*len(self.names)
        exponents[self.names.index(name)] = 1
        return Poly(self, {tuple(exponents): Q(1)})


class Poly:
    def __init__(self, ring, terms):
        self.r = ring
        self.terms = {}
        for key, coefficient in terms.items():
            key, coefficient = list(key), Q(coefficient)
            if ring.truncated:
                name, bound = ring.truncated
                if key[ring.names.index(name)] >= bound:
                    continue
            if ring.period:
                name, period = ring.period
                index = ring.names.index(name)
                key[index] %= period
            if ring.gaussian:
                index = ring.names.index(ring.gaussian)
                coefficient *= (-1)**(key[index]//2)
                key[index] %= 2
            key = tuple(key)
            self.terms[key] = self.terms.get(key, Q(0)) + coefficient
        self.terms = {key: value for key, value in self.terms.items() if value}

    def __add__(self, other):
        other = self.r.poly(other)
        terms = dict(self.terms)
        for key, coefficient in other.terms.items():
            terms[key] = terms.get(key, Q(0)) + coefficient
        return Poly(self.r, terms)

    __radd__ = __add__

    def __neg__(self):
        return Poly(self.r, {key: -value for key, value in self.terms.items()})

    def __sub__(self, other):
        return self + -self.r.poly(other)

    def __rsub__(self, other):
        return self.r.poly(other) + -self

    def __mul__(self, other):
        other = self.r.poly(other)
        terms = {}
        for a, x in self.terms.items():
            for b, y in other.terms.items():
                key = tuple(i+j for i, j in zip(a, b))
                terms[key] = terms.get(key, Q(0)) + x*y
        return Poly(self.r, terms)

    __rmul__ = __mul__

    def __truediv__(self, number):
        need(Q(number) != 0, 'nonzero scalar divisor')
        return self * (1/Q(number))

    def __pow__(self, exponent):
        need(type(exponent) is int, 'integral polynomial power')
        if exponent < 0:
            need(len(self.terms) == 1, 'negative power requires monomial')
            key, coefficient = next(iter(self.terms.items()))
            return Poly(self.r, {tuple(exponent*i for i in key): coefficient**exponent})
        result = self.r.poly(1)
        for _ in range(exponent):
            result *= self
        return result

    def substitute(self, name, value):
        value = self.r.poly(value)
        index = self.r.names.index(name)
        result = self.r.poly(0)
        for key, coefficient in self.terms.items():
            exponent, rest = key[index], list(key)
            rest[index] = 0
            result += Poly(self.r, {tuple(rest): coefficient}) * value**exponent
        return result

    def coefficient(self, name, exponent):
        index = self.r.names.index(name)
        terms = {}
        for key, value in self.terms.items():
            if key[index] == exponent:
                rest = list(key)
                rest[index] = 0
                terms[tuple(rest)] = value
        return Poly(self.r, terms)

    def equal(self, other, description):
        other = self.r.poly(other)
        need(self.terms == other.terms, description)
        return description

    def record(self):
        return [{'powers': {name: exponent for name, exponent in zip(self.r.names, key) if exponent},
                 'coefficient': str(value)} for key, value in sorted(self.terms.items())]


def moments(drop_balance=False, drop_h3=False):
    names = 'eta y T V M q ' + ' '.join('h'+str(j) for j in range(6)) + ' ' + ' '.join('u'+str(j) for j in range(6))
    r = Ring(names)
    eta, y, T, V, M, q = [r.variable(name) for name in ['eta', 'y', 'T', 'V', 'M', 'q']]
    hs = [r.variable('h'+str(j)) for j in range(6)]
    us = [r.variable('u'+str(j)) for j in range(6)]
    sh, su, shu = sum(hs), sum(us), sum(h*u for h, u in zip(hs, us))
    m = (eta*V-(0 if drop_balance else sh))/2
    n = (M-shu-2*m*y)/2
    h = hs + [m+q, m-q]
    u = us + [y+n*q**-1, y-n*q**-1]
    def reduce_q(poly):
        index = r.names.index('q')
        result = r.poly(0)
        for key, value in poly.terms.items():
            exponent, rest = key[index], list(key)
            need(exponent >= 0, 'uncancelled moment square-root divisor')
            rest[index] = exponent % 2
            result += Poly(r, {tuple(rest): value}) * (T-m*m)**(exponent//2)
        return result
    checks = [sum(u).equal(su+2*y, 'all eight u sum, including heavy moment'),
              sum(h).equal(eta*V, 'total h cancels free balance and retains eta V'),
              reduce_q(sum(x*x for x in h)).equal(sum(x*x for x in hs)+2*T, 'all h squared cancels heavy mean'),
              reduce_q(sum(x*z for x,z in zip(h,u))).equal(M, 'all eight hu sum, including eta-dependent heavy mean')]
    m0 = m.substitute('eta', 0)
    H3 = sum(x**3 for x in hs) + (0 if drop_h3 else 6*m0*T-4*m0**3)
    checks.append(reduce_q(sum(x**3 for x in h)).substitute('eta',0).equal(H3, 'generic limiting cubic moment includes heavy balance'))
    need(H3.terms != sum(x**3 for x in hs).terms, 'heavy cubic moment cannot be omitted')
    return {'universal_exact_identities': checks, 'generic_H3': H3.record()}


def newton(drop_anchor=False, drop_trace=False):
    r = Ring('eps z U H V M H3 i', truncated=('eps',4), gaussian='i')
    eps,z,U,H,V,M,H3,i = [r.variable(name) for name in r.names]
    powers = [r.poly(0), eps**2*U+(0 if drop_trace else i*eps**3*V), -eps**2*H+2*i*eps**3*M, -i*eps**3*H3]
    powers += [r.poly(0)]*5  # Every critical factor is O(eps).
    elementary = [r.poly(1)]
    for k in range(1,9):
        elementary.append(sum((-1)**(j-1)*elementary[k-j]*powers[j] for j in range(1,k+1))/k)
    anchor = r.poly(1) if drop_anchor else 1-eps**2
    p = z**9-anchor**9 + sum(Q(9,9-k)*(-1)**k*elementary[k]*(z**(9-k)-anchor**(9-k)) for k in range(1,9))
    P2 = 9-Q(9,8)*U*(z**8-1)+Q(9,14)*H*(z**7-1)
    Q3 = -Q(9,8)*V*(z**8-1)-Q(9,7)*M*(z**7-1)+H3*(z**6-1)/2
    checks = [elementary[1].equal(eps**2*U+i*eps**3*V, 'first exact Newton coefficient'),
              elementary[2].equal(eps**2*H/2-i*eps**3*M, 'second exact Newton coefficient'),
              elementary[3].equal(-i*eps**3*H3/3, 'third exact Newton coefficient'),
              p.equal(z**9-1+eps**2*P2+i*eps**3*Q3, 'complete anchored ninth-degree jet through epsilon cubed'),
              p.coefficient('eps',1).equal(0,'no epsilon1 term for arbitrary free h sum'),
              p.substitute('z',anchor).equal(0,'marked anchor retained in complete universal jet')]
    return {'checks':checks,'P2':P2.record(),'Q3':Q3.record(),'elementary_coefficients':[x.record() for x in elementary[1:]]}


def root_normals(drop_reversal=False, wrong_half=False):
    r = Ring('omega U H V M H3 i',period=('omega',9),gaussian='i')
    w,U,H,V,M,H3,i = [r.variable(name) for name in r.names]
    P = 9-Q(9,8)*U*(w**8-1)+Q(9,14)*H*(w**7-1)
    Q3 = -Q(9,8)*V*(w**8-1)-Q(9,7)*M*(w**7-1)+H3*(w**6-1)/2
    inv = w**-1
    Psharp, Qsharp = P.substitute('omega', inv), Q3.substitute('omega', inv)
    motion2, sharp2 = -P*w/9, -Psharp*inv/9
    motion3, sharp3 = -i*Q3*w/9, (-1 if drop_reversal else 1)*i*Qsharp*inv/9
    N2 = (inv*motion2+w*sharp2)/(1 if wrong_half else 2)
    N3 = (inv*motion3+w*sharp3)/2
    tau = (w+inv)/2
    expected = -1+(tau-1)*U/8+(1-tau*tau)*H/7
    checks = [N2.equal(expected,'literal second root-product coefficient gives beta0 at every ninth root'),
              N2.substitute('omega',inv).equal(N2,'even second coefficient under root reflection'),
              N3.substitute('omega',inv).equal(-N3,'odd third coefficient under root reflection'),
              (N3+N3.substitute('omega',inv)).equal(0,'beta odd numerator coefficient cancels'),
              N2.substitute('omega',1).equal(-1,'marked half-normal eta coefficient is -1 for a=1-eta'),
              N3.substitute('omega',1).equal(0,'marked odd half-normal coefficient vanishes')]
    need(N3.terms, 'generic gamma leading coefficient is not identically zero')
    return {'checks':checks,'beta0':N2.record(),'gamma0':N3.record(),
            'vanishing_orders':{'each_actual_half_normal':2,'averaged_beta_numerator':2,'odd_gamma_numerator':3},
            'parity':'companion reverses epsilon; averaged numerator even, difference odd; both normalized quotients even'}


def dual(module, parent):
    K = module.K
    c = K([0,1,0])
    mu = [K(row) for row in parent['exact_initial_normal_and_dual']['individual_root_multipliers']]
    tau = [K(Q(-1,2)), -c]
    need(-2*sum(m*(t-1)/8 for m,t in zip(mu,tau)) == K(1), 'all-complex-raw dual U coefficient')
    need(-2*sum(m*(1-t*t)/7 for m,t in zip(mu,tau)) == K(Q(-1,2)), 'all-complex-raw dual H coefficient')
    return {'identities':['-2 sum mu(tau-1)/8=1','-2 sum mu(1-tau^2)/7=-1/2'],
            'objective_eta1':'8+U-H/2','constant_C':(K(8)-2*sum(mu)).record(),
            'double_eta_divisibility':'F-8-eta(C-2mu dot beta(eta,v)) has both eta0 and eta1 coefficients identically zero for every complex raw v'}


def record(module, parent):
    return {'raw_moments':moments(),'generic_newton_jet':newton(),'literal_original_root_products':root_normals(),'deflation_dual':dual(module,parent)}


def controls():
    damages=[('lost free heavy balance',lambda:moments(drop_balance=True)),
             ('omitted generic heavy cubic moment',lambda:moments(drop_h3=True)),
             ('lost moving marked-root anchor',lambda:newton(drop_anchor=True)),
             ('lost total imaginary critical trace',lambda:newton(drop_trace=True)),
             ('complex companion did not reverse epsilon',lambda:root_normals(drop_reversal=True)),
             ('wrong literal half-normal convention',lambda:root_normals(wrong_half=True))]
    result=[]
    for label,run in damages:
        try:run()
        except ValueError as error:result.append({'damage':label,'rejected_by':str(error)})
        else:raise ValueError('symbolic damage accepted: '+label)
    return result
