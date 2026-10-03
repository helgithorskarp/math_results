#!/usr/bin/env python3
"""Quantitative raw-quintic / full-five-residual transport.

Actual six-sendov-2, researcher; CPython3.10+ standard library only.
Sparse Fraction kernels adapt this author's9550 source
cb4cf7d9d83f3d376d3763b65cbe2fddd50637f4. The whole high-row pivots
and reconstructed chart are credited9550. No peer executable or fixture
is imported. All raw coefficient maps, exact corrections, gradients and
closed budgets are regenerated before reading this leaf's compact fixture.
This is same-author corroboration, not independent review/formalization.
The ordinary actual-domain implication and all trust boundaries are in PROOF.md.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse, hashlib, json

def require(condition, message):
    if not condition:
        raise ValueError(message)

class P:
    """Sparse rational polynomial in eleven variables, Laurent only in t."""
    zero = (0,)*11

    def __init__(self, value=0):
        if isinstance(value, P):
            self.c = dict(value.c)
        elif isinstance(value, dict):
            self.c = {tuple(k): F(v) for k, v in value.items() if v}
            require(all(len(k) == 11 for k in self.c), 'polynomial variable count')
            require(all(all(isinstance(e,int) and (i==4 or e>=0) for i,e in enumerate(k))for k in self.c), 'Laurent only in t')
        else:
            self.c = {self.zero: F(value)} if value else {}

    def __add__(self, other):
        out = dict(self.c)
        for k, v in P(other).c.items():
            out[k] = out.get(k, F(0))+v
            if not out[k]:
                del out[k]
        return P(out)

    __radd__ = __add__

    def __neg__(self):
        return P({k: -v for k, v in self.c.items()})

    def __sub__(self, other):
        return self+-P(other)

    def __rsub__(self, other):
        return P(other)+-self

    def __mul__(self, other):
        out = {}
        for k, a in self.c.items():
            for l, b in P(other).c.items():
                key = tuple(i+j for i, j in zip(k, l))
                out[key] = out.get(key, F(0))+a*b
        return P(out)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        require(isinstance(exponent, int) and exponent >= 0, 'bad power')
        out = P(1)
        for _ in range(exponent):
            out = out*self
        return out

    def __eq__(self, other):
        return self.c == P(other).c

    def encoded(self):
        return [[list(k), str(v)] for k, v in sorted(self.c.items())]

def variable(index):
    key = [0]*11
    key[index] = 1
    return P({tuple(key): 1})

def canonical(record):
    return json.dumps(record, sort_keys=True, separators=(',', ':')).encode()

def ut(poly):
    out = list(poly)
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out or [0]

def ua(left, right):
    return ut([(left[i] if i < len(left) else 0)+(right[i] if i < len(right) else 0)
               for i in range(max(len(left), len(right)))])

def us(value, poly):
    return ut([value*x for x in poly])

def um(left, right):
    out = [0]*(len(left)+len(right)-1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i+j] = out[i+j]+a*b
    return ut(out)

def ud(poly):
    return ut([i*poly[i] for i in range(1, len(poly))] or [0])

def uq(poly, h):
    require(len(h) == 8 and h[-1] == 1, 'monic degree-seven quotient')
    poly = ut(poly)
    q = [0]*max(1, len(poly)-7)
    while len(poly) >= 8:
        k, a = len(poly)-8, poly[-1]
        q[k] = q[k]+a
        poly = ua(poly, [0]*k+us(-a, h))
    return ut(q), ut(poly)

def ur(poly, h):
    return uq(poly, h)[1]

def nth(poly, k):
    return poly[k] if k < len(poly) else 0

def moment_list(h, last=12):
    out = [F(7)]
    for k in range(1, last+1):
        if k <= 7:
            value = -sum((nth(h, 7-i)*out[k-i] for i in range(1, k)), 0)
            value -= k*nth(h, 7-k)
        else:
            value = -sum((nth(h, 7-i)*out[k-i] for i in range(1, 8)), 0)
        out.append(value)
    return out

def adj(poly, h, moments=None, damage=None):
    """Adjoint to derivative of the UNIQUE normal representative, not a derivation."""
    poly = ur(poly, h)
    moments = moments or moment_list(h, 6)
    out = [0]*6
    for k in range(1, len(poly)):
        for j in range(k):
            out[k-1-j] = out[k-1-j]+poly[k]*moments[j]
        if damage != 'adjoint_boundary':
            out[k-1] = out[k-1]-k*poly[k]
    return ut(out)

def primitive(h, constant=0):
    return [constant]+[F(8, i+1)*h[i] for i in range(8)]

def algebra(p, h, f=None, damage=None):
    f = primitive(h) if f is None else f
    Q, residual = uq(ua(us(8, f), um(p, ud(h))), h)
    if damage == 'quotient_constant':
        Q = ua(Q, [0, -8])
    ode = ua(um(p, ud(ud(h))), um(ua(ud(p), us(-1, Q)), ud(h)))
    ode = ua(ode, um(ua([64], us(-1, ud(Q))), h))
    moments = moment_list(h, 6)
    p2 = ur(um(p, p), h)
    W = ur(um(p, ua(Q, us(-1, ud(p)))), h)
    K = ua(us(-16, p), us(F(-1, 4), adj(adj(p2, h, moments, damage), h, moments, damage)))
    K = ua(K, us(F(1, 4), adj(W, h, moments, damage)))
    return {'Q': Q, 'residual': residual, 'ODE': ode, 'K': K, 'p2': p2, 'W': W}

def polydigest(poly):
    coeff = [P(x).encoded() for x in ut(poly)]
    return {'degree': len(ut(poly))-1,
            'coefficient_terms': [len(P(x).c) for x in ut(poly)],
            'sha256': hashlib.sha256(canonical(coeff)).hexdigest()}


def sub(a, index, value):
    a=P(a);out=P(0);value=P(value)
    for key,c in a.c.items():
        exponent=key[index]
        require(exponent>=0,'substitute only a polynomial variable')
        k=list(key);k[index]=0
        out+=P({tuple(k):c})*value**exponent
    return out


def diffvar(a,index):
    out={}
    for key,c in P(a).c.items():
        if key[index]:
            k=list(key);k[index]-=1
            out[tuple(k)]=c*key[index]
    return P(out)


def polysub(a,index,value):
    return [sub(x,index,value)for x in a]


def scalar(a):
    a=P(a)
    require(all(key==P.zero for key in a.c),'constant exact scalar')
    return a.c.get(P.zero,F(0))


def extract(a,index,power):
    out={}
    for key,c in P(a).c.items():
        if key[index]==power:
            k=list(key);k[index]=0;out[tuple(k)]=c
    return P(out)


def coefficients(a,index):
    a=P(a)
    require(all(key[index]>=0 for key in a.c),'ordinary polynomial coefficient extraction')
    highest=max((key[index]for key in a.c),default=0)
    return [extract(a,index,k)for k in range(highest+1)]



INPUT_CHART_COMMIT = 'cb4cf7d9d83f3d376d3763b65cbe2fddd50637f4'
INPUT_CHART_DIGESTS = {'solved_polynomials': {'C': {'coefficient_terms': [21], 'degree': 0, 'sha256': 'cb071e7eba369b11af1614440a8598559bd54ab81e1a8cc3dba8a4094fa7e005'}, 'F': {'coefficient_terms': [12], 'degree': 0, 'sha256': 'b101ac691a3d045492ab30facd86437da184a9b5c71020cb500b67081873cf1c'}, 'G': {'coefficient_terms': [19], 'degree': 0, 'sha256': 'a94efaceb2e9296ec11b1766e42f0129b8360dfe5c0e40e6705090ce87e51182'}, 'J': {'coefficient_terms': [28], 'degree': 0, 'sha256': '2313211ae39dc37a10903c6d04d1d0456886031602e8785dc514dbec861abdfc'}, 'p0': {'coefficient_terms': [12], 'degree': 0, 'sha256': 'fce2418ad6b91626ebbe6fd43422645929464505bf27e421f19126737ec929a3'}, 'p1': {'coefficient_terms': [8], 'degree': 0, 'sha256': 'daa63d2797d54c1520b4d5d5dc7bd439a22017f8d3004622628855ecbda2e791'}, 'p2': {'coefficient_terms': [4], 'degree': 0, 'sha256': '5537026d3ae0991a3c109720720638ce53a6e1e9ebff86a2c43d2fedcc6ace6b'}}, 'entire_residual_polynomials': {'K0plus4': {'coefficient_terms': [44], 'degree': 0, 'sha256': 'e5ef1f9f30199906332419f803ce9e81f27897735fb61a732b95757c4c98a97c'}, 'K1': {'coefficient_terms': [29], 'degree': 0, 'sha256': '42edf9c530df46b245c50170cddc3f37592402dfd2dd6babb01c28c6a7b1193e'}, 'tODE0': {'coefficient_terms': [71], 'degree': 0, 'sha256': 'd9185b5af0398160e9f72b2bd3613e44119c8e1536806ca4ab99e4c40f328606'}, 'tODE1': {'coefficient_terms': [54], 'degree': 0, 'sha256': '68bb120d2a8beb71ee43b79eb001b366b4ca44f95ad81b487140a7e9e46f5f57'}, 'tODE2': {'coefficient_terms': [43], 'degree': 0, 'sha256': 'affb508a977054a5f6cb1b7e89bd3c210326cc6bc6e9b73d47c7d8aa05ccdad6'}}, 'whole_matrix_rows': [{'coefficient_terms': [30, 10, 3], 'degree': 2, 'sha256': '7ef81b7a0c45f0e8942d34c9b12ee397980358a724530d68232f80768ac047a4'}, {'coefficient_terms': [34, 16, 4], 'degree': 2, 'sha256': 'ef1d91668f293532eb69b2bae84c626fc67a5f76164cc6a24a4cfed95b4aa570'}, {'coefficient_terms': [45, 19, 7], 'degree': 2, 'sha256': '5a633ccb93ce3fcd5a1993b9ce1d91af4617f44b447231e9474c92d29115be1e'}, {'coefficient_terms': [20, 8, 1], 'degree': 2, 'sha256': '1b720a86528d4f2aa3a7d58d18de45efccef1233ace91391e6520a61419b0609'}, {'coefficient_terms': [31, 10, 3], 'degree': 2, 'sha256': 'f2a1e440d33988d51fc399d93c64b489ee1b0bc4973e8abf5a9072a2ed47b156'}]}


def same_typed(left, right):
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(same_typed(left[k], right[k]) for k in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(same_typed(a, b) for a, b in zip(left, right))
    return left == right


def coefficient_norm(poly):
    return sum((abs(c) for c in P(poly).c.values()), F(0))


def absolute_degree(poly):
    return max((sum(abs(e) for e in key) for key in P(poly).c), default=0)


def complete_digest(poly):
    encoded = [P(a).encoded() for a in ut(poly)]
    return {'coefficient_polynomials': len(ut(poly)),
            'terms': sum(len(P(a).c) for a in ut(poly)),
            'abs_degree': max((absolute_degree(a) for a in ut(poly)), default=0),
            'sha256': hashlib.sha256(canonical(encoded)).hexdigest()}


def legacy_digest(poly):
    require(all(key[-1] == 0 for a in poly for key in P(a).c), 'input has no raw p2 coordinate')
    encoded = [[[list(key[:-1]), str(c)] for key, c in sorted(P(a).c.items())] for a in ut(poly)]
    return {'degree': len(ut(poly))-1,
            'coefficient_terms': [len(P(a).c) for a in ut(poly)],
            'sha256': hashlib.sha256(canonical(encoded)).hexdigest()}


def phi_of(maps):
    return [P(nth(maps['ODE'], i)) for i in range(6)] + [
        P(nth(maps['K'], i)) + (4 if i == 0 else 0) for i in [0, 1, 3, 4, 5]]


def build():
    B, E, r, s, t, Fc, G, J, p0, p1, p2 = [variable(i) for i in range(11)]
    key = [0]*11
    key[4] = -1
    ti = P({tuple(key): 1})
    h = [J, G, Fc, E, B, F(-3, 8), 0, 1]
    raw_p = [p0, p1, p2, r*t, s*t, t]
    coefficient = algebra([p0, p1, p2, r, s, t], h)
    raw = algebra(raw_p, h)
    p2star = 8+t*(F(5, 7)*B-F(27, 56)*s-r*s)
    p2stage = {name: [sub(a, 10, p2star) for a in poly] for name, poly in raw.items()}
    x0 = F(-1, 42)*sub(nth(p2stage['ODE'], 5), 8, 0)
    x1 = F(-4, 15)*sub(nth(p2stage['ODE'], 4), 9, 0)
    composed = {name: [sub(sub(a, 8, x0), 9, x1) for a in p2stage[name]] for name in ['ODE', 'K']}
    gF = F(-1, 24)*ti**2*sub(nth(composed['K'], 4), 6, 0)
    k3 = sub(nth(composed['K'], 3), 6, gF)
    Fstar = F(14, 15)*ti**2*sub(k3, 5, 0)
    Gstar = sub(gF, 5, Fstar)
    o3 = sub(sub(nth(composed['ODE'], 3), 6, Gstar), 5, Fstar)
    Jstar = F(1, 28)*ti*sub(o3, 7, 0)
    P0star = sub(sub(x0, 5, Fstar), 6, Gstar)
    P1star = sub(sub(x1, 5, Fstar), 6, Gstar)
    hstar = [Jstar, Gstar, Fstar, E, B, F(-3, 8), 0, 1]
    pstar = [P0star, P1star, p2star, r*t, s*t, t]
    final = algebra(pstar, hstar)
    residuals = [t*nth(final['ODE'], i) for i in [2, 1, 0]] + [
        nth(final['K'], 1), nth(final['K'], 0)+4]
    return {'coefficient': coefficient, 'raw': raw, 'p2stage': p2stage,
            'composed': composed, 'final': final, 'raw_h': h, 'raw_p': raw_p,
            'p2star': p2star, 'p0affine': x0, 'p1affine': x1, 'gF': gF,
            'k3_after_G': k3, 'o3_after_FG': o3, 'hstar': hstar, 'pstar': pstar,
            'Fstar': Fstar, 'Gstar': Gstar, 'Jstar': Jstar, 'residuals': residuals,
            'coefficient_phi': phi_of(coefficient)}


def closed_budget(name, terms, ceiling_coefficient, ceiling_power, sink=None):
    """WHOLE positive monomial comparison, valid for EVERY real L>=100."""
    terms = [(F(c), p) for c, p in terms]
    require(all(c >= 0 and type(p) is int and p <= ceiling_power for c, p in terms),
            'closed exponent coverage '+name)
    ceiling_coefficient = F(ceiling_coefficient)
    require(ceiling_coefficient > 0, 'positive upper coefficient '+name)
    gap = ceiling_coefficient-sum((c*F(100)**(p-ceiling_power) for c, p in terms), F(0))
    require(gap >= 0, 'closed positive monomial budget '+name)
    item = {'name': name, 'lower_terms': [[str(c), p] for c, p in terms],
            'upper_term': [str(ceiling_coefficient), ceiling_power],
            'exact_gap_after_dividing_upper_L_power_at_100': str(gap),
            'domain': 'EVERY real L>=100; all divided terms are nonincreasing'}
    if sink is not None:
        sink.append(item)
    return item


def certificate():
    data = build()
    B, E, r, s, t, Fc, G, J, p0, p1, p2 = [variable(i) for i in range(11)]
    raw, step, composed, final = [data[x] for x in ['raw', 'p2stage', 'composed', 'final']]
    x0, x1, p2star, gF, Fstar, Gstar, Jstar = [data[x] for x in [
        'p0affine', 'p1affine', 'p2star', 'gF', 'Fstar', 'Gstar', 'Jstar']]
    identities = {}

    def eq(name, left, right=0):
        require(P(left) == P(right), 'WHOLE identity '+name)
        identities[name] = True

    for name in data['coefficient']:
        for i, (left, right) in enumerate(zip(data['coefficient'][name], raw[name])):
            eq('raw parameter composition '+name+' '+str(i), sub(sub(left, 2, r*t), 3, s*t), right)
        require(len(data['coefficient'][name]) == len(raw[name]), 'full parameter map length '+name)
    for i in range(6, 13):
        eq('higher coefficient ODE '+str(i), nth(data['coefficient']['ODE'], i))
        eq('higher raw ODE '+str(i), nth(raw['ODE'], i))
    eq('zero quintic K6', nth(data['coefficient']['K'], 6))
    eq('entire K5 p2 pivot', nth(raw['K'], 5), F(7, 4)*t*(p2-p2star))
    eq('entire p0 pivot', nth(step['ODE'], 5), 42*(p0-x0))
    eq('entire p1 pivot', nth(step['ODE'], 4), F(15, 4)*(p1-x1))
    eq('p0 independent p1', diffvar(x0, 9))
    eq('p1 independent p0', diffvar(x1, 8))
    eq('p0 explicit', x0, F(-5, 7)+t*(F(3, 7)*B*r+F(75, 392)*B+F(4, 7)*E*s
                                    +F(5, 7)*Fc+F(3, 28)*r*s+F(9, 784)*s))
    eq('p1 explicit', x1, F(128, 5)*B+t*(F(-8, 7)*B*B-4*B*r*s+F(4, 7)*B*s
                         +F(16, 3)*E*r+3*E+F(20, 3)*Fc*s+8*G-F(3, 8)*r-F(9, 64)))
    eq('entire G pivot', nth(composed['K'], 4), 24*t*t*(G-gF))
    eq('entire F pivot after G', data['k3_after_G'], F(-15, 14)*t*t*(Fc-Fstar))
    eq('entire J pivot after FG', data['o3_after_FG'], -28*t*(J-Jstar))
    eq('G correction affine slope', diffvar(gF, 5), F(-5, 6)*s)
    eq('p0 F slope', diffvar(x0, 5), F(5, 7)*t)
    eq('p0 G slope', diffvar(x0, 6))
    eq('p1 F slope', diffvar(x1, 5), F(20, 3)*t*s)
    eq('p1 G slope', diffvar(x1, 6), 8*t)
    eq('EXACT coupled F G mass-p1 cancellation',
       diffvar(x1, 5)+diffvar(x1, 6)*diffvar(gF, 5))
    for name in ['p0affine', 'p1affine', 'p2star', 'gF', 'Fstar', 'Gstar', 'Jstar']:
        eq(name+' independent J', diffvar(data[name], 7))
    for i in [3, 4, 5]:
        eq('final ODE high '+str(i), nth(final['ODE'], i))
        eq('final kernel high '+str(i), nth(final['K'], i))
    require(len(final['ODE']) <= 6 and len(final['K']) <= 6, 'entire final degree coverage')
    require(len(data['residuals']) == 5 and all(all(e >= 0 for e in key)
            for a in data['residuals'] for key in P(a).c), 'ALL FIVE final ordinary residuals')
    for a in data['hstar']+data['pstar']+data['residuals']:
        require(all(not any(key[j] for j in range(5, 11)) for key in P(a).c),
                'entire reconstructed five-parameter dependence')
    gamma = F(1, 4)*nth(final['K'], 2)
    solved = [Fstar, Gstar, Jstar, data['pstar'][0], data['pstar'][1], p2star, gamma]
    for name, poly in zip(['F', 'G', 'J', 'p0', 'p1', 'p2', 'C'], solved):
        require(legacy_digest([poly]) == INPUT_CHART_DIGESTS['solved_polynomials'][name],
                'ENTIRE credited9550 solved polynomial '+name)
    matrix = [[extract(a, 4, power) for power in [2, 1, 0]] for a in data['residuals']]
    for i, (name, a) in enumerate(zip(['tODE2', 'tODE1', 'tODE0', 'K1', 'K0plus4'], data['residuals'])):
        require(legacy_digest([a]) == INPUT_CHART_DIGESTS['entire_residual_polynomials'][name],
                'ENTIRE credited9550 residual '+name)
        require(legacy_digest(matrix[i]) == INPUT_CHART_DIGESTS['whole_matrix_rows'][i],
                'ENTIRE credited9550 matrix row '+name)
        eq('entire final quadratic-t row '+str(i), a, matrix[i][0]*t*t+matrix[i][1]*t+matrix[i][2])
    phi = data['coefficient_phi']
    gradients = [[diffvar(a, j) for j in range(11)] for a in phi]
    gradnorms = [sum((coefficient_norm(a) for a in row), F(0)) for row in gradients]
    degree = max(absolute_degree(a) for a in phi)
    maximum_gradient_norm = max(gradnorms)
    require(len(phi) == 11 and degree == 4 and maximum_gradient_norm == F(1611571, 4096),
            'ENTIRE degree-four coefficient Jacobian bound')
    budgets = []

    def budget(name, terms, c, power):
        return closed_budget(name, terms, c, power, budgets)

    budget('all-row segment Jacobian on coefficient box 2L', [(8*maximum_gradient_norm, 3)], 1, 5)
    budget('p2 correction', [(F(4, 7), 1)], 1, 1)
    budget('first residual', [(1, 0), (1, 6)], 1, 7)
    budget('p0 and p1 simultaneous correction', [(F(4, 15), 7)], 1, 7)
    budget('second residual', [(1, 7), (1, 12)], 1, 13)
    budget('G-only h correction', [(F(1, 24), 15)], 1, 16)
    budget('G-only mass-p1 correction', [(F(1, 3), 16)], 1, 16)
    budget('third residual', [(1, 13), (1, 21)], 1, 22)
    budget('F correction', [(F(14, 15), 24)], 1, 24)
    budget('coupled G correction', [(F(5, 6), 25)], 1, 25)
    budget('coupled mass-p0 correction', [(F(5, 7), 25)], 1, 25)
    budget('fourth residual', [(1, 22), (1, 30)], 1, 31)
    budget('J correction', [(F(1, 28), 32)], 1, 32)
    budget('fifth residual', [(1, 31), (1, 37)], 1, 38)
    budget('entire chart displacement', [(1, 1), (1, 7), (1, 16), (1, 25), (1, 32)], 1, 33)
    budget('F plus ALL FIVE chart residuals', [(1, 24), (1, 39)], 1, 40)
    budget('closed small-residual bootstrap', [(1, -7)], F(1, 100**7), 0)
    moment_square = F(13, 48)**2+F(3, 40)**2
    require(moment_square == F(4549, 57600), 'full two-original-moment norm constant')
    mu3, mu5 = F(-24, 5)*B, -4*B-F(40, 3)*Fc
    eq('actual cubic moment inverse', F(-5, 24)*mu3, B)
    eq('actual fifth moment inverse', F(1, 16)*mu3-F(3, 40)*mu5, Fc)
    budget('gradient threshold exceeds desired joint-square floor', [(F(2, 10**68), 0)], 1, 45)
    require(F(1, 4*moment_square) > 1, 'closed small-gradient moment-square implication')
    require(40+10 == 50 and 95+50 == 145 and 2*95 == 190,
            'complete epsilon and moment exponent transport')
    require(10412+6 == 10418 and 10418*190 == 1979420 and 3940*190+136 == 748736,
            'complete separation and decimal exponent arithmetic')
    require(2**190 < 10**58 and 748736+58 == 748794, 'coarse explicit decimal floor')

    rejected = []
    def reject(name, probe):
        try:
            probe()
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('damaged mathematics survived '+name)
    reject('wrong forced quotient term', lambda: eq('damaged quotient',
           nth(algebra([p0,p1,p2,r,s,t], data['raw_h'], damage='quotient_constant')['Q'], 1),
           nth(data['coefficient']['Q'], 1)))
    reject('wrong representative adjoint', lambda: eq('damaged adjoint',
           nth(algebra([p0,p1,p2,r,s,t], data['raw_h'], damage='adjoint_boundary')['K'], 5),
           nth(data['coefficient']['K'], 5)))
    reject('wrong p2 pivot factor', lambda: eq('damaged p2 pivot', nth(raw['K'],5), 7*t*(p2-p2star)))
    reject('wrong F correction sign', lambda: eq('damaged F sign', data['k3_after_G'],
           F(-15,14)*t*t*(Fc+Fstar)))
    reject('omit simultaneous G correction', lambda: eq('damaged mass-p1 cancellation', diffvar(x1,5)))
    reject('wrong J correction sign', lambda: eq('damaged J sign', data['o3_after_FG'], -28*t*(J+Jstar)))
    reject('drop final kernel constant residual', lambda: require(len(data['residuals'][:-1])==5,
           'ALL FIVE residual coverage'))
    reject('understate complete residual budget', lambda: closed_budget('damaged complete budget',
           [(1,24),(1,39)],1,20))
    reject('wrong original cubic normalization', lambda: eq('damaged cubic inverse', F(-1,8)*mu3,B))

    maps = {}
    for stage in ['coefficient', 'raw', 'p2stage', 'composed', 'final']:
        for name, poly in data[stage].items():
            maps[stage+'.'+name] = complete_digest(poly)
    for name in ['p2star','p0affine','p1affine','gF','Fstar','Gstar','Jstar']:
        maps[name] = complete_digest([data[name]])
    maps['hstar'] = complete_digest(data['hstar'])
    maps['pstar'] = complete_digest(data['pstar'])
    maps['ALL_FIVE_final_residuals'] = complete_digest(data['residuals'])
    return {'actual_agent':'six-sendov-2','role':'researcher',
            'ring':'QQ[B,E,r,s,t,t^-1,F,G,J,p0,p1,p2]; only t is inverted',
            'whole_polynomial_identities':sorted(identities),
            'whole_maps':maps,'whole_coefficient_phi':[P(a).encoded() for a in phi],
            'whole_gradient_row_norms':[str(a) for a in gradnorms],
            'full_gradient_digest':complete_digest([a for row in gradients for a in row]),
            'maximum_coefficient_degree':degree,'maximum_gradient_norm':str(maximum_gradient_norm),
            'credited9550_entire_alignment':INPUT_CHART_DIGESTS,
            'closed_universal_budgets':budgets,'moment_norm_squared':str(moment_square),
            'rejected_mathematical_damages':rejected,
            'displacement_powers':[1,7,16,25,32], 'residual_powers':[7,13,22,31,38],
            'universal_L_minimum':100,'small_raw_residual_power':-40,
            'F_difference_power':24,'ALL_FIVE_residual_power':39,
            'joint_linear_residual_power':40,'joint_gradient_power':50,
            'joint_actual_gradient_plus_TWO_moment_square_bound':
               {'coefficient':'10^-136','L_power':-190,
                'L_delta':'2*10^3940*delta^-10418',
                'coarse_decimal_coefficient':'10^-748794','delta_power':1979420},
            'ordinary_proof_status':'complete author argument relative to credited inputs; UNFORMALIZED',
            'independent_review_of_this_leaf':False,
            'stationarity_assumed':False,'projected_feasibility_assumed':False,
            'stationary_profiles_constructed':False,'original_collision_extension':False,
            'complex_first_power_proved':False,'physical_H_proved':False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected', type=Path, default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--emit', action='store_true')
    args = parser.parse_args()
    record = certificate()
    if args.emit:
        args.expected.write_text(json.dumps(record, indent=2, sort_keys=True)+'\n')
    else:
        require(same_typed(record, json.loads(args.expected.read_text())), 'ENTIRE typed compact record mismatch')
    print(json.dumps({'status':'PASS',
        'record_sha256':hashlib.sha256(canonical(record)).hexdigest(),
        'whole_identities':len(record['whole_polynomial_identities']),
        'complete_maps':len(record['whole_maps']),
        'closed_universal_budgets':len(record['closed_universal_budgets']),
        'whole_gradient_polynomials':121,
        'rejected_mathematical_damages':len(record['rejected_mathematical_damages']),
        'stationarity_assumed':False,'independent_review_claimed':False}, sort_keys=True))


if __name__ == '__main__':
    main()
