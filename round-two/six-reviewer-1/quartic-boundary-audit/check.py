#!/usr/bin/env python3
"""Independent, standard-library exact audit in Q[w]/(w^6+w^3+1).

No author code is imported.  --author optionally checks the separate record bridge.
Finite algebra is checked here; the quantified analytic argument is in REVIEW.md.
"""
import argparse
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import json
from pathlib import Path


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


class K:
    """Six rational coordinates, reduction w^6=-w^3-1."""
    __slots__ = ('a',)

    def __init__(self, a=0):
        if isinstance(a, K):
            self.a = a.a
        elif isinstance(a, (int, F, str)):
            self.a = (F(a),) + (F(0),) * 5
        else:
            self.a = tuple(map(F, a))
            require(len(self.a) == 6, 'field dimension')

    def __hash__(self):
        return hash(self.a)

    def __bool__(self):
        return any(self.a)

    def __eq__(self, b):
        return self.a == K(b).a

    def __neg__(self):
        return K(tuple(-x for x in self.a))

    def __add__(self, b):
        if not isinstance(b, (K, int, F, str, tuple, list)):
            return NotImplemented
        b = K(b)
        return K(tuple(x + y for x, y in zip(self.a, b.a)))

    __radd__ = __add__

    def __sub__(self, b):
        return self + -K(b)

    def __rsub__(self, b):
        return K(b) + -self

    def __mul__(self, b):
        if not isinstance(b, (K, int, F, str, tuple, list)):
            return NotImplemented
        b = K(b)
        if not self or not b:
            return K()
        a = [F(0)] * 11
        for i, x in enumerate(self.a):
            if x:
                for j, y in enumerate(b.a):
                    if y:
                        a[i + j] += x * y
        for n in range(10, 5, -1):
            a[n - 3] -= a[n]
            a[n - 6] -= a[n]
        return K(a[:6])

    __rmul__ = __mul__

    @lru_cache(None)
    def inverse(self):
        require(bool(self), 'division by zero')
        columns = [self * K(tuple(int(i == j) for i in range(6))) for j in range(6)]
        matrix = [[columns[j].a[i] for j in range(6)] + [F(i == 0)] for i in range(6)]
        for j in range(6):
            pivot = next(i for i in range(j, 6) if matrix[i][j])
            matrix[j], matrix[pivot] = matrix[pivot], matrix[j]
            divisor = matrix[j][j]
            matrix[j] = [a / divisor for a in matrix[j]]
            for i in range(6):
                if i != j:
                    factor = matrix[i][j]
                    matrix[i] = [a - factor * b for a, b in zip(matrix[i], matrix[j])]
        result = K(tuple(matrix[i][6] for i in range(6)))
        require(self * result == 1, 'inverse residual')
        return result

    def __truediv__(self, b):
        return self * K(b).inverse()

    def __rtruediv__(self, b):
        return K(b) * self.inverse()

    def __pow__(self, n):
        if n < 0:
            return self.inverse() ** -n
        a, b = K(1), self
        while n:
            if n & 1:
                a = a * b
            b = b * b
            n //= 2
        return a

    def conjugate(self):
        return sum((x * WROOT ** (8 * i) for i, x in enumerate(self.a)), K())

    def real(self):
        return (self + self.conjugate()) / 2


WROOT = K((0, 1, 0, 0, 0, 0))
CROOT = -(WROOT ** 4 + WROOT ** 5) / 2


def cubic(a):
    """Recover coordinates 1,c,c^2 by solving in the six-coordinate field."""
    a = K(a)
    basis = [K(1), CROOT, CROOT ** 2]
    matrix = [[basis[j].a[i] for j in range(3)] + [a.a[i]] for i in range(6)]
    row = 0
    for j in range(3):
        pivot = next(i for i in range(row, 6) if matrix[i][j])
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        f = matrix[row][j]
        matrix[row] = [v / f for v in matrix[row]]
        for i in range(6):
            if i != row:
                f = matrix[i][j]
                matrix[i] = [v - f * u for v, u in zip(matrix[i], matrix[row])]
        row += 1
    answer = tuple(matrix[i][3] for i in range(3))
    require(sum((x * b for x, b in zip(answer, basis)), K()) == a, 'real subfield bridge')
    return answer


def interval_add(a, b):
    return a[0] + b[0], a[1] + b[1]


def interval_mul(a, b):
    products = [x * y for x in a for y in b]
    return min(products), max(products)


def c_interval():
    low, high = F(3, 4), F(1)
    f = lambda t: 8 * t ** 3 - 6 * t - 1
    require(f(low) < 0 < f(high), 'embedding bracket')
    # f'>0 on [3/4,1], so this brackets the largest real root.
    for _ in range(100):
        mid = (low + high) / 2
        if f(mid) < 0:
            low = mid
        else:
            high = mid
    return low, high


C_INTERVAL = c_interval()


def enclosure(a):
    bounds = (F(0), F(0))
    for coefficient in reversed(cubic(a)):
        bounds = interval_add(interval_mul(bounds, C_INTERVAL), (coefficient, coefficient))
    return bounds


def positive(a, label):
    require(enclosure(a)[0] > 0, label)


def negative(a, label):
    positive(-a, label)


def sqrt_interval(a):
    require(a >= 0, 'sqrt domain')
    low, high = F(0), max(F(1), a)
    for _ in range(110):
        mid = (low + high) / 2
        if mid * mid < a:
            low = mid
        else:
            high = mid
    return low, high


# Ordinary truncated univariate series.  The generic ring below uses epsilon,
# while these series use eta and are constructed directly from q'(z).
ORDER = 3


def sa(a, b):
    return [a[i] + b[i] for i in range(ORDER + 1)]


def sm(a, b):
    return [sum((a[j] * b[i - j] for j in range(i + 1)), K()) for i in range(ORDER + 1)]


def sp(a, n):
    r = [K(1)] + [K()] * ORDER
    for _ in range(n):
        r = sm(r, a)
    return r


def scale(a, f):
    return [v * f for v in a]


def eval_poly(polynomial, z):
    answer = [K()] * (ORDER + 1)
    for coefficient in reversed(polynomial):
        answer = sa(sm(answer, z), coefficient)
    return answer


def poly_mul(a, b):
    r = [[K()] * (ORDER + 1) for _ in range(len(a) + len(b) - 1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] = sa(r[i + j], sm(x, y))
    return r


def binomial_series(a, exponent):
    require(a[0] == 1, 'binomial constant')
    t = a.copy()
    t[0] = K()
    result = [K(1)] + [K()] * ORDER
    coefficient = F(1)
    for k in range(1, ORDER + 1):
        coefficient *= (exponent - k + 1) / k
        result = sa(result, scale(sp(t, k), coefficient))
    return result


# A sparse formal ring: epsilon truncated at order4, i^2=-1, and nine
# independent real moment symbols.  This verifies identities, not samples.
NAMES = ('U', 'H', 'V', 'B', 'W', 'D', 'J3', 'J21', 'J4')
ZERO_KEY = (0,) * (2 + len(NAMES))


class Sym:
    def __init__(self, a=0):
        if isinstance(a, Sym):
            self.a = a.a.copy()
        elif isinstance(a, dict):
            self.a = {key: K(v) for key, v in a.items() if K(v)}
        else:
            self.a = {ZERO_KEY: K(a)} if K(a) else {}

    @classmethod
    def variable(cls, index):
        key = list(ZERO_KEY)
        key[index] = 1
        return cls({tuple(key): K(1)})

    def __eq__(self, b):
        return self.a == Sym(b).a

    def __neg__(self):
        return Sym({k: -v for k, v in self.a.items()})

    def __add__(self, b):
        r = self.a.copy()
        for k, v in Sym(b).a.items():
            r[k] = r.get(k, K()) + v
        return Sym(r)

    __radd__ = __add__

    def __sub__(self, b):
        return self + -Sym(b)

    def __rsub__(self, b):
        return Sym(b) + -self

    def __mul__(self, b):
        r = {}
        for k, v in self.a.items():
            for l, u in Sym(b).a.items():
                key = [a + b for a, b in zip(k, l)]
                if key[0] > 4:
                    continue
                sign = -1 if key[1] >= 2 else 1
                key[1] %= 2
                key = tuple(key)
                r[key] = r.get(key, K()) + v * u * sign
        return Sym(r)

    __rmul__ = __mul__

    def __truediv__(self, b):
        return self * K(b).inverse()

    def __pow__(self, n):
        r = Sym(1)
        for _ in range(n):
            r = r * self
        return r

    def conjugate(self):
        return Sym({k: v.conjugate() * (-1 if k[1] else 1) for k, v in self.a.items()})

    def real(self):
        return (self + self.conjugate()) / 2

    def substitute(self, replacements):
        r = Sym()
        for key, value in self.a.items():
            term = Sym(value) * EPS ** key[0] * IMAG ** key[1]
            for j, name in enumerate(NAMES):
                term = term * replacements.get(name, VARIABLES[name]) ** key[j + 2]
            r = r + term
        return r


EPS = Sym.variable(0)
IMAG = Sym.variable(1)
VARIABLES = {name: Sym.variable(j + 2) for j, name in enumerate(NAMES)}


def symbolic_polynomial(z, coefficients):
    answer = Sym()
    for value in reversed(coefficients):
        answer = answer * z + value
    return answer


def audit():
    count = 0
    def check(condition, label):
        nonlocal count
        require(condition, label)
        count += 1

    check(WROOT ** 9 == 1 and WROOT ** 3 != 1, 'primitive ninth root')
    check(8 * CROOT ** 3 - 6 * CROOT - 1 == 0, 'real embedding identity')
    c = CROOT
    d, v = 2 * c ** 2 - 1, c - 2 * c ** 2 + 1
    y = 1 / (3 * (1 + c))
    x, H = F(2, 3) - y, 14 * y
    U0 = -8 * x
    A = [F(3, 2), 1 + c]
    B = [F(3, 2), 1 - d]
    weights = [F(2, 3) * (7 - (1 - d) / (c + d)), 1 / (c + d)]
    check(sum((weights[k] * A[k] / 8 for k in range(2)), K()) == 1, 'dual real row')
    check(sum((weights[k] * B[k] / 14 for k in range(2)), K()) == F(1, 2), 'dual square row')
    C = 8 - sum(weights)
    positive(weights[0], 'first dual weight positive')
    positive(weights[1], 'second dual weight positive')
    positive(4-C, 'concentration slope ceiling')
    count += 3
    rho = F(-3, 2) + weights[1] / 4
    sigma = F(3, 8) - (F(3, 2) * weights[0] + (1 - v) * weights[1]) / 20
    L = -7 * (2 * c + 1) / 18
    alpha, beta = sigma - rho ** 2 / 2, (L + rho) ** 2 / 2
    q = beta + alpha / 2

    # Newton identities are derived from the formal power sums, then integrated
    # and anchored.  High moments have epsilon-order at least5 and vanish here.
    U, HH, V, BB, WW, DD, J3, J21, J4 = (VARIABLES[n] for n in NAMES)
    # Generic inverse distance with alpha=eta*u and beta=sqrt(eta)*h.
    distance_offset = (-2*(1+U)+HH**2)*EPS**2+(1+U)**2*EPS**4
    reciprocal = 1-distance_offset/2+F(3,8)*distance_offset**2
    check(reciprocal == 1+(1+U-HH**2/2)*EPS**2
          +((1+U)**2-F(3,2)*(1+U)*HH**2+F(3,8)*HH**4)*EPS**4,
          'generic reciprocal fourth-order identity')
    moments = [Sym(), U * EPS ** 2 + IMAG * V * EPS ** 3 + WW * EPS ** 4,
               -HH * EPS ** 2 + IMAG * BB * EPS ** 3 + DD * EPS ** 4,
               -IMAG * J3 * EPS ** 3 - 3 * J21 * EPS ** 4, J4 * EPS ** 4]
    moments += [Sym()] * 4
    elementary = [Sym(1)]
    for k in range(1, 9):
        elementary.append(sum((elementary[k-j] * moments[j] * (-1) ** (j-1)
                               for j in range(1, k+1)), Sym()) / k)
    primitive = [Sym()] * 10
    for k in range(9):
        primitive[9-k] = elementary[k] * (9 * (-1) ** k) / (9-k)
    anchor = 1 - EPS ** 2
    primitive[0] = -symbolic_polynomial(anchor, primitive)
    g2 = [Sym()] * 10
    g3 = [Sym()] * 10
    g4 = [Sym()] * 10
    g2[0], g2[8], g2[7] = 9 + 9 * U / 8 - 9 * HH / 14, -9 * U / 8, 9 * HH / 14
    g3[8], g3[7], g3[6] = -9 * IMAG * V / 8, -9 * IMAG * BB / 14, IMAG * J3 / 2
    g3[0] = -sum(g3[1:], Sym())
    g4[8] = -9 * WW / 8
    g4[7] = 9 * (U ** 2 - DD) / 14
    g4[6] = -3 * U * HH / 4 + 3 * J21 / 2
    g4[5] = 9 * HH ** 2 / 40 - 9 * J4 / 20
    g4[0] = -36 - 9 * U + 9 * HH / 2 - sum(g4[1:], Sym())
    for z_degree in range(10):
        target = g2[z_degree] * EPS ** 2 + g3[z_degree] * EPS ** 3 + g4[z_degree] * EPS ** 4
        target += Sym(int(z_degree == 9) - int(z_degree == 0))
        check(primitive[z_degree] == target, f'generic Newton coefficient z^{z_degree}')

    curvatures, tangent_rows = [], []
    T_constants = []
    for index, k in enumerate((3, 4)):
        omega = WROOT ** k
        replacements = {'U': Sym(U0), 'H': Sym(H)}
        t2 = -symbolic_polynomial(omega, g2).substitute(replacements) / (9 * omega ** 8)
        t3 = -symbolic_polynomial(omega, g3).substitute(replacements) / (9 * omega ** 8)
        g2prime = [g2[j] * j for j in range(1, 10)]
        t4 = -(symbolic_polynomial(omega, g4).substitute(replacements)
               + symbolic_polynomial(omega, g2prime).substitute(replacements) * t2
               + t2 ** 2 * (36 * omega ** 7)) / (9 * omega ** 8)
        half4 = (t4 / omega).real() + (t2 * t2.conjugate()) / 2
        r, s = (K(-1), K(F(3, 4))) if k == 3 else (-2*c, 1-c**2)
        curvature = -((F(7, 2)*x*x + 6*x*y*r + F(5, 2)*y*y*r*r)*s)
        C6, C5 = (K(0), K(F(3, 2))) if k == 3 else (K(F(3, 2)), 1-v)
        baseline = 4 + U0 - H/2 + B[index]*U0**2/14 - C6*U0*H/12 + C5*H**2/40 + curvature
        target = Sym(baseline) + C6*J21/6 - C5*J4/20 - A[index]*WW/8 - B[index]*DD/14
        check(half4 == target, f'active half-modulus fourth order k{k}')
        # The odd radial term cancels by conjugate averaging even before imposing
        # the limiting sine constraints; these constraints cancel it individually.
        opposite = -(symbolic_polynomial(omega.conjugate(), g3).substitute(replacements)) / (9 * omega.conjugate() ** 8)
        check((t3 / omega).real() + (opposite / omega.conjugate()).real() == 0,
              f'odd pair averaging k{k}')
        check((t3 / omega).real().substitute({'V': 8*Sym(L)*J3/7, 'B': 2*Sym(L)*J3}) == 0,
              f'sine compatibility k{k}')
        curvatures.append(curvature)
        T_constants.append(baseline)
        tangent_rows.append((A[index]/8, B[index]/14))
    K0 = 8 + 2*U0 - 3*H/2 + sum((weights[k]*T_constants[k] for k in range(2)), K())
    K1 = K0 + (U0 + rho*H)**2/16
    Bstar = K1 + alpha*H**2/2
    check(Bstar == F(2311,108) + F(4934,27)*c - F(1976,9)*c*c, 'claimed sharp coefficient')
    negative(Bstar, 'second coefficient negative')
    positive(Bstar+F(754160683222,10**12), 'sharp decimal enclosure lower endpoint')
    positive(-F(754160683221,10**12)-Bstar, 'sharp decimal enclosure upper endpoint')
    negative(alpha, 'quartic multiplier negative')
    positive(q-F(5,2), 'q > 5/2')
    positive(H*q/2-F(1,2), 'first coercivity branch >1/2')
    positive(-H*alpha/4-F(1,2), 'second coercivity branch >1/2')
    positive(F(9,2)-rho*rho*H, 'rho squared H <9/2')
    positive(F(25,4)-(L+rho)**2, 'L plus rho squared <25/4')
    count += 9

    uz = (U0 + rho*H)/8
    up = uz - rho*H/2
    U2 = 6*uz**2+2*up**2
    J21star, J4star = H*up, H**2/2
    rhs = [T_constants[k] + (0 if k == 0 else F(1,4))*J21star
           - (F(3,2) if k == 0 else 1-v)*J4star/20 for k in range(2)]
    a, b = tangent_rows[0]
    e, f = tangent_rows[1]
    determinant = a*f-b*e
    W = (rhs[0]*f-rhs[1]*b)/determinant
    D = (a*rhs[1]-e*rhs[0])/determinant
    gamma = (U2-D)/(2*H)
    check(determinant == -3*(c+d)/224, 'active determinant')
    check(6*uz+2*up == U0, 'optimizer mean')
    check(K0+U2/2+rho*J21star+sigma*J4star == Bstar, 'optimizer value')

    constants = {'c':c,'d':d,'v':v,'x':x,'y':y,'H':H,'U0':U0,'C':C,
                 'w3':weights[0],'w4':weights[1],'mixed':rho,'fourth':sigma,
                 'L':L,'alpha':alpha,'beta':beta,'const':K0,'base':K1,'Bstar':Bstar,
                 'u_zero':uz,'u_pair':up,'U2':U2,'J21':J21star,'J4':J4star,
                 'W':W,'D':D,'gamma':gamma}
    families = {}
    mutation_material = None
    for M in (0, 2, 100):
        AS = [K(), uz, W/8, K(M)]
        BS = [K(), up, W/8, K(M)]
        one = [K(1), K(), K(), K()]
        linearA, linearB = [scale(AS,-1),one], [scale(BS,-1),one]
        derivative = [one]
        for _ in range(6):
            derivative = poly_mul(derivative,linearA)
        pair = poly_mul(linearB,linearB)
        pair[0] = sa(pair[0],[K(),H/2,H*gamma,H*gamma**2/2])
        derivative = [scale(v,9) for v in poly_mul(derivative,pair)]
        polynomial = [[K()]*(ORDER+1)] + [scale(v,F(1,j+1)) for j,v in enumerate(derivative)]
        marked = [K(1),K(-1),K(),K()]
        polynomial[0] = scale(eval_poly(polynomial,marked),-1)
        branches = []
        for k in range(9):
            omega = WROOT**k
            branch = [omega,K(),K(),K()]
            # Formal implicit solving by residual coefficient, no hand-coded
            # second/third root formulas.  The derivative at eta0 is 9 omega^8.
            for n in range(1,ORDER+1):
                residual = eval_poly(polynomial,branch)[n]
                branch[n] = -residual/(9*omega**8)
            check(not any(eval_poly(polynomial,branch)),f'root residual M{M} k{k}')
            modulus = sm(branch,[z.conjugate() for z in branch])
            half = scale(modulus,F(1,2))
            if k == 0:
                check(branch == marked,f'marked root M{M}')
            elif k in (1,2,7,8):
                negative(half[1],f'nonactive strict first motion M{M} k{k}')
                count += 1
            else:
                check(half[1] == 0 and half[2] == 0,f'active lower tangencies M{M} k{k}')
                if M in (2,100):
                    negative(half[3],f'active inward third motion M{M} k{k}')
                    count += 1
            branches.append({'k':k,'half_modulus':[[str(v) for v in cubic(z)] for z in half[1:]]})
            if M == 2 and k == 4:
                mutation_material = (polynomial, branch)
        da = sa(marked,scale(AS,-1))
        db = sa(marked,scale(BS,-1))
        pair_distance = sa(sm(db,db),[K(),H/2,H*gamma,H*gamma**2/2])
        objective = sa(scale(binomial_series(da,F(-1)),6),
                       scale(binomial_series(pair_distance,F(-1,2)),2))
        if M == 2:
            mutation_distance = pair_distance
        check(objective[:3] == [K(8),C,Bstar],f'objective first three coefficients M{M}')
        terms = []
        for z_degree, jet in enumerate(polynomial):
            for eta_degree, coefficient in enumerate(jet):
                if coefficient:
                    terms.append([[eta_degree,z_degree],[str(v) for v in cubic(coefficient)]])
        families[str(M)] = {'primitive':sorted(terms), 'branches':branches,
                            'objective':[[str(v) for v in cubic(z)] for z in objective]}
    def value(triple):
        return sum((F(z)*CROOT**i for i,z in enumerate(triple)),K())
    thresholds = []
    for index,k in enumerate((3,4)):
        old = value(families['100']['branches'][k]['half_modulus'][2])
        threshold = 100+old/A[index]
        thresholds.append(threshold)
        check(value(families['2']['branches'][k]['half_modulus'][2]) == old+98*A[index],
              f'linear inward repair k{k}')
    positive(thresholds[1]-thresholds[0],'outer pair dominates repair threshold')
    positive(thresholds[1]-F(1614,1000),'threshold lower enclosure')
    positive(F(1615,1000)-thresholds[1],'threshold upper enclosure')
    positive(value(families['0']['branches'][4]['half_modulus'][2]),'M0 escaping branch')
    check(value(families['100']['objective'][3])-value(families['2']['objective'][3]) == 784,
          'third objective reduction')
    count += 4

    # Identity for the completed square, using the three exact linear constraints.
    # The squared norm of g(h) follows from 1.h=0, h.h=H, h.h^2=J3.
    a0 = (U0+rho*H)/8
    g_norm = 8*Sym(a0*a0) + (L+rho)**2*J3**2/H - 2*a0*rho*Sym(H) + rho*rho*J4 - 2*rho*(L+rho)*J3**2/H
    u_dot_g = Sym(a0*U0)+(L+rho)*L*J3**2/H-rho*J21
    UU = Sym.variable(2)  # U symbol serves as an independent U2 placeholder here.
    completed = Sym(K1)+alpha*J4+beta*J3**2/H+(UU-2*u_dot_g+g_norm)/2
    check(completed == Sym(K0)+UU/2+rho*J21+sigma*J4,'completed square identity')

    # Deterministic exact control profiles.  For integer x, h=sqrt(H/norm)x;
    # all g(h) and objective values remain in K.  The sole extra radical in
    # the distance to the selected opposed pair receives a rational bracket.
    profile_count = 0
    def profile_test(values, residual):
        nonlocal profile_count
        norm = sum(a*a for a in values)
        third = sum(a**3 for a in values)
        fourth = sum(a**4 for a in values)
        require(sum(values) == 0 and norm > 0, 'control balanced profile')
        gg = [a0+(L+rho)*H*third*F(a,norm*norm)-rho*H*F(a*a,norm) for a in values]
        uu = [a+K(b) for a,b in zip(gg,residual)]
        check(sum(uu,K()) == U0, 'control u mean')
        check(sum((values[j]*residual[j] for j in range(8)),F()) == 0,
              'control residual orthogonality')
        objective = K0+sum((a*a for a in uu),K())/2
        objective += rho*sum((H*F(values[j]**2,norm)*uu[j] for j in range(8)),K())
        objective += sigma*H*H*F(fourth,norm*norm)
        gap = objective-Bstar
        moment_defect = H*H*(F(1,2)+F(third*third,2*norm**3)-F(fourth,norm**2))
        check(enclosure(moment_defect)[0] >= 0, 'control moment inequality')
        check(gap == q*H*H*F(third*third,norm**3)-alpha*moment_defect
              +sum((K(r*r) for r in residual),K())/2, 'control square identity')
        i,j = max(range(8),key=lambda j:values[j]),min(range(8),key=lambda j:values[j])
        opposite_u = [up if k in (i,j) else uz for k in range(8)]
        u_cost = sum(((a-b)**2 for a,b in zip(uu,opposite_u)),K())
        radius = sqrt_interval(F(2,norm))
        h_cost = interval_add(enclosure(2*H),interval_mul(enclosure(-H*(values[i]-values[j])),radius))
        joint_cost = interval_add(h_cost,enclosure(u_cost))
        if gap == 0:
            check(fourth*2 == norm*norm and not third and not any(residual), 'zero-gap equality profile')
        else:
            check(enclosure(128*gap)[0] > joint_cost[1], 'control joint coercivity')
        profile_count += 1
    profiles = [(1,-1,0,0,0,0,0,0), (1,1,-1,-1,0,0,0,0), (7,-1,-1,-1,-1,-1,-1,-1)]
    for n in range(1,25):
        row = [((n*j+j*j)%9)-4 for j in range(1,8)]
        row.append(-sum(row))
        if any(row):
            profiles.append(tuple(row))
    for row in profiles:
        profile_test(row,[F()] * 8)
        # A nonzero null vector of [1; x] on a triple, including repetitions.
        residual = [F()] * 8
        residual[0],residual[1],residual[2] = F(row[1]-row[2],7),F(row[2]-row[0],7),F(row[0]-row[1],7)
        if not any(residual):
            residual[3],residual[4],residual[5] = F(row[4]-row[5],7),F(row[5]-row[3],7),F(row[3]-row[4],7)
        profile_test(row,residual)

    # Corrupt actual inputs to the checks, rather than merely comparing two
    # different constants.  Each damaged witness must fail its residual.
    polynomial,branch = mutation_material
    leading = [jet.copy() for jet in polynomial]
    leading[9][0] = K(F(8,9))
    anchor_damage = [jet.copy() for jet in polynomial]
    anchor_damage[0][2] += 1
    root_damage = branch.copy()
    root_damage[3] += WROOT**4
    reciprocal_damage = binomial_series(mutation_distance,F(-1,2))
    reciprocal_damage[2] += 1
    expected_one = [K(1)]+[K()] * ORDER
    generic_damage = primitive[6] + J21*EPS**4
    mutations = [
        ('degree-nine normalization', lambda: not any(eval_poly(leading,branch))),
        ('anchored constant', lambda: not any(eval_poly(anchor_damage,branch))),
        ('original root third jet', lambda: not any(eval_poly(polynomial,root_damage))),
        ('reciprocal quadratic jet', lambda: sm(mutation_distance,sm(reciprocal_damage,reciprocal_damage)) == expected_one),
        ('generic mixed moment', lambda: generic_damage == primitive[6]),
        ('optimizer mean', lambda: 6*uz+2*(up+1) == U0),
    ]
    rejected = []
    for label,test in mutations:
        try:
            require(test(),label)
        except RuntimeError:
            rejected.append(label)
        else:
            raise RuntimeError('undetected corruption: '+label)
    output = {'arithmetic':'Q[w]/(w^6+w^3+1); w=e^(2 pi i/9)',
              'checks':count,'embedding_interval':list(map(str,C_INTERVAL)),
              'constants':{k:list(map(str,cubic(a))) for k,a in sorted(constants.items())},
              'curvatures':[list(map(str,cubic(a))) for a in curvatures],
              'thresholds':[list(map(str,cubic(a))) for a in thresholds],
              'threshold_enclosures':[list(map(str,enclosure(a))) for a in thresholds],
              'Bstar_enclosure':list(map(str,enclosure(Bstar))),
              'families':families,'mutations_rejected':rejected,
              'finite_profile_controls':profile_count,
              'trust_boundary':'finite exact identities/signs only; analytic arguments and coercivity proof are in REVIEW.md'}
    return output


def author_bridge(record,path):
    author=json.loads(Path(path).read_text())
    require(record['constants']==author['constants'],'all author constant normal forms')
    require(record['curvatures']==[v['curvature'] for v in author['active_root_checks']], 'active curvature bridge')
    require(record['families']['100']['primitive']==author['explicit_family']['primitive'], 'all primitive coefficient bridge')
    require(record['families']['100']['objective']==[v[1] for v in author['explicit_objective_jet']], 'objective bridge')
    for index,k in enumerate((3,4)):
        require(record['families']['100']['branches'][k]['half_modulus'][2] ==
                author['explicit_family']['active_pairs'][index]['half_squared_modulus_eta3'], 'third modulus bridge')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--author',help='optional author expected.json; not needed for independent run')
    parser.add_argument('--write',action='store_true',help='write the computed compact expected.json')
    args=parser.parse_args()
    record=audit()
    serialized=json.dumps(record,indent=2,sort_keys=True)+'\n'
    expected=Path(__file__).with_name('expected.json')
    if args.write:
        expected.write_text(serialized)
    else:
        require(expected.read_text()==serialized,'independent record exact match')
    if args.author:
        author_bridge(record,args.author)
    print(f"PASS: {record['checks']} independent exact checks; {len(record['mutations_rejected'])} damaged identities rejected.")
    print('Record SHA256 '+hashlib.sha256(serialized.encode()).hexdigest())
    print('M=2 gives all nine roots strictly inside for sufficiently small eta; threshold lies in (1.614,1.615).')


if __name__=='__main__':
    main()
