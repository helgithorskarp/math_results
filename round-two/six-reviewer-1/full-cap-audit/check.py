"""Independent complete algebra for the relative full-cap theorem.

CPython 3.12; standard library only. No producer program or data imported.
All guards remain active under -O. Output is a regenerated record, not input.
"""
from fractions import Fraction as F
import argparse
import hashlib
import json
import signal
from pathlib import Path

signal.alarm(45)


class E:
    """Q[c]/(8c^3-6c-1), coefficient order 1,c,c^2."""
    def __init__(self, a=0):
        if isinstance(a, E):
            self.a = a.a
            return
        q = [F(x) for x in a] if isinstance(a, (list, tuple)) else [F(a)]
        q += [F(0)] * max(0, 3-len(q))
        for j in range(len(q)-1, 2, -1):
            q[j-3] += q[j]/8
            q[j-2] += 3*q[j]/4
        self.a = tuple(q[:3])

    def __add__(self, b):
        if isinstance(b, P):
            return NotImplemented
        b = E(b)
        return E([x+y for x, y in zip(self.a, b.a)])
    __radd__ = __add__
    def __neg__(self):
        return E([-x for x in self.a])
    def __sub__(self, b):
        if isinstance(b, P):
            return NotImplemented
        return self + -E(b)
    def __rsub__(self, b):
        return E(b) + -self
    def __mul__(self, b):
        if isinstance(b, P):
            return NotImplemented
        b = E(b)
        q = [F(0)] * 5
        for i, x in enumerate(self.a):
            for j, y in enumerate(b.a):
                q[i+j] += x*y
        return E(q)
    __rmul__ = __mul__
    def __pow__(self, n):
        if n < 0:
            return self.inverse() ** (-n)
        q = E(1)
        for _ in range(n):
            q *= self
        return q
    def inverse(self):
        cols = [(self*E([0]*j+[1])).a for j in range(3)]
        m = [[cols[j][i] for j in range(3)]+[F(i == 0)] for i in range(3)]
        for j in range(3):
            pivot = next((i for i in range(j, 3) if m[i][j]), None)
            if pivot is None:
                raise ValueError('noninvertible field element')
            m[j], m[pivot] = m[pivot], m[j]
            t = m[j][j]
            m[j] = [x/t for x in m[j]]
            for i in range(3):
                if i != j:
                    t = m[i][j]
                    m[i] = [x-t*y for x, y in zip(m[i], m[j])]
        q = E([m[j][3] for j in range(3)])
        if (self*q).a != (F(1), F(0), F(0)):
            raise ValueError('full inverse product')
        return q
    def __truediv__(self, b):
        return self*E(b).inverse()
    def __rtruediv__(self, b):
        return E(b)*self.inverse()
    def __eq__(self, b):
        return self.a == E(b).a
    def __bool__(self):
        return any(self.a)
    def record(self):
        return [str(x) for x in self.a]


DIM = 26
ZERO = (0,) * DIM


class P:
    """Sparse independent exponent tuples; no packing or degree truncation."""
    def __init__(self, a=0):
        if isinstance(a, P):
            self.a = dict(a.a)
        elif isinstance(a, dict):
            self.a = {k: E(v) for k, v in a.items() if E(v)}
        else:
            self.a = {ZERO: E(a)} if E(a) else {}
    def __add__(self, b):
        q = dict(self.a)
        for k, v in P(b).a.items():
            q[k] = q.get(k, E())+v
        return P(q)
    __radd__ = __add__
    def __neg__(self):
        return P({k: -v for k, v in self.a.items()})
    def __sub__(self, b):
        return self+-P(b)
    def __rsub__(self, b):
        return P(b)+-self
    def __mul__(self, b):
        q = {}
        for k, v in self.a.items():
            for l, w in P(b).a.items():
                n = tuple(x+y for x, y in zip(k, l))
                q[n] = q.get(n, E())+v*w
        return P(q)
    __rmul__ = __mul__
    def __pow__(self, n):
        q = P(1)
        for _ in range(n):
            q *= self
        return q
    def __truediv__(self, b):
        return self*E(b).inverse()
    def __eq__(self, b):
        return self.a == P(b).a
    def record(self):
        return [[list(k), v.record()] for k, v in sorted(self.a.items())]


def variable(i):
    q = list(ZERO)
    q[i] = 1
    return P({tuple(q): 1})


def interval(e, lo, hi):
    qlo = qhi = F(0)
    for a in reversed(E(e).a):
        vals = [qlo*lo, qlo*hi, qhi*lo, qhi*hi]
        qlo, qhi = min(vals)+a, max(vals)+a
    return qlo, qhi


def cosine_bracket():
    lo, hi = F(15, 16), F(47, 50)
    f = lambda t: 8*t**3-6*t-1
    if not f(lo) < 0 < f(hi) or not 24*lo**2-6 > 0:
        raise ValueError('physical unique cosine bracket')
    for _ in range(100):
        mid = (lo+hi)/2
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    return lo, hi


def compute(fault=None):
    records = []
    def same(name, a, b):
        a, b = P(a), P(b)
        if a != b:
            raise ValueError(name)
        records.append({'identity': name, 'whole_polynomial': a.record()})
    lo, hi = cosine_bracket()
    def positive(name, a):
        u, v = interval(a, lo, hi)
        if u <= 0:
            raise ValueError(name)
        records.append({'sign': name, 'element': E(a).record(),
                        'strict_rational_interval': [str(u), str(v)]})
    c = E([0, 1])
    roots = [s*F(1, d) for s in (-1, 1) for d in (1, 2, 4, 8)]
    if any(8*t**3-6*t-1 == 0 for t in roots):
        raise ValueError('irreducible physical cubic')
    records.append({'irreducibility': 'degree three rational-root test',
                    'all_candidates': [str(t) for t in roots],
                    'all_nonzero_values': [str(8*t**3-6*t-1) for t in roots]})
    y = 1/(3*(1+c)); x = E(F(2, 3))-y; H = 14*y; b2 = H/2
    rho = (c-5)/3; k = -7*(1+2*c)/18
    alpha = E(F(-527, 360))+41*c/90+13*c**2/90
    kappa = (k+rho)**2/2+10*alpha/27
    G = E(F(183619658945, 2519424))+444829186913*c/1259712-288729410449*c**2/629856
    e = E(F(50960, 243))+1218245*c/972-125944*c**2/81
    aT = E(F(-11564, 405))-20482*c/81+123284*c**2/405
    bT = E(F(49, 180))-105889*c/486+305123*c**2/1215
    L = E(F(-101920, 243))-1218245*c/486+251888*c**2/81
    mustar = -3*L/8
    Gm = E(F(340367352475, 839808))+808137564635*c/419904-1052841914857*c**2/419904
    w4 = 1/(c+2*c**2-1); w3 = E(F(2, 3))*(7-(2-2*c**2)*w4)
    A = E(F(-13638695, 972))-16011613*c/243+20901119*c**2/243
    Bdivsin = (1448+6982*c-8224*c**2)/243
    Q = (8+25*c+20*c**2)/162
    if fault == 'transverse-sign':
        alpha = -alpha
    if fault == 'weight':
        w4 += 1
    same('cubic minimal polynomial', 8*c**3-6*c-1, 0)
    same('old real linear coefficient', -2*e, L)
    same('complete real square center', G-3*L**2/16, Gm)
    same('transverse imaginary coefficient', aT/b2, -alpha*H)
    same('mean imaginary coefficient', (E(F(2, 3))*aT+4*bT)/(9*b2*H**2), kappa/H)
    same('positive dual first response', (w3*E(F(3, 2))+w4*(1+c))/8, 1)
    same('positive dual second response', (w3*E(F(3, 2))+w4*(2-2*c**2))/7, 1)
    for name, a in [('H', H), ('b2', b2), ('kappa', kappa), ('negative alpha', -alpha),
                    ('negative Gm', -Gm), ('w3', w3), ('w4', w4),
                    ('A', A), ('B divided by positive sine', Bdivsin), ('Q', Q),
                    ('mustar', mustar), ('16 minus mustar', 16-mustar)]:
        positive(name, a)
    q, mu = variable(0), variable(1)
    v = [variable(i) for i in range(2, 7)]
    v.append(-sum(v, P()))
    r = [variable(i) for i in range(7, 12)]
    r.append(-sum(r, P()))
    told = [-q/3+v[i] for i in range(6)]
    rold = [-mu/3+r[i] for i in range(6)]
    if fault == 'missing-coordinate':
        told[0] = -q/3
    S, R = sum(told, P()), sum(rold, P())
    same('imaginary inverse coordinate', -S/2, q)
    same('real inverse coordinate', -R/2, mu)
    for i in range(6):
        same(f'imaginary inverse residual {i}', told[i]-S/6, v[i])
        same(f'real inverse residual {i}', rold[i]-R/6, r[i])
    same('imaginary residual balance', sum(v, P()), 0)
    same('real residual balance', sum(r, P()), 0)
    old = G+e*R+aT*sum((t*t for t in told), P())+bT*S*S
    old += sum((t*t for t in rold), P())/2+R*R/4
    axis = Gm+(mu-mustar)**2*F(4, 3)+9*kappa*H*b2*q*q
    axis += sum((t*t for t in r), P())/2-alpha*H*b2*sum((t*t for t in v), P())
    if fault == 'mean-square':
        axis -= (mu-mustar)**2/3
    same('entire twelve-coordinate finite cost', old, axis)
    same('physical endpoint squared', (kappa/H)*(-H*Gm/kappa), -Gm)
    up = (-8*x+rho*H)/8-rho*H/2
    uz = (-8*x+rho*H)/8
    D = E(F(-4270, 27))-29492*c/27+4012*c**2/3
    Gamma = (6*uz**2+2*up**2-D)/(2*H)
    W = E(F(2512, 27))+5840*c/9-21392*c**2/27
    xi = [Gamma+q, -Gamma+q]+told
    nu = [W/8+mu+b2*(rho+3*k)*q, W/8+mu-b2*(rho+3*k)*q]
    nu += [W/8-mu/3+t for t in r]
    same('whole projected imaginary mean', sum(xi, P()), 0)
    same('whole projected imaginary norm', b2*(xi[0]-xi[1]), H*Gamma)
    same('whole projected real mean', sum(nu, P()), W)
    same('whole mixed affine constraint', nu[0]-nu[1]-(rho+3*k)*b2*(xi[0]+xi[1]), 0)
    # Literal cube of all eight scaled critical slots, retaining every eta order.
    eta = variable(12)
    h0 = [1, -1]+[0]*6
    full = sum(((P(z)+eta*a)**3 for z, a in zip(h0, xi)), P())
    expanded = sum((P(z**3)+3*z*z*eta*a+3*z*eta**2*a*a+eta**3*a**3
                    for z, a in zip(h0, xi)), P())
    same('whole original eight-slot cubic polynomial', full, expanded)
    leading = P({tuple(0 if j == 12 else k for j, k in enumerate(n)): a
                 for n, a in full.a.items() if n[12] == 1})
    factor = 6 if fault != 'cubic-factor' else 3
    same('physical cubic first variation', leading, factor*q)
    same('physical t divided by b', b2*leading, 3*H*q)
    # Six complete imaginary second tangents, seven real tangents.
    tau = [variable(i) for i in range(13, 19)]
    tau = [-sum(tau, P())/2, -sum(tau, P())/2]+tau
    sig = [variable(i) for i in range(19, 26)]
    sig.append(-sum(sig, P()))
    same('full six-dimensional second imaginary balance', sum(tau, P()), 0)
    same('full second imaginary norm tangent', b2*(tau[0]-tau[1]), 0)
    same('full seven-dimensional second real balance', sum(sig, P()), 0)
    same('full second cost differential', 2*k*b2*(tau[0]-tau[1])+uz*sum(sig, P()), 0)
    # Each independent third-coordinate response; all eight real and imaginary.
    cosines = [E(1), c]
    for _ in range(2, 17):
        cosines.append(2*c*cosines[-1]-cosines[-2])
    for channel in ('imaginary', 'real'):
        for i in range(8):
            U = E(int(channel == 'real'))
            T = b2*int(channel == 'imaginary')*((i == 0)-(i == 1))
            primitive = {0: 9*U/8-9*T/7, 7: 9*T/7, 8: -9*U/8}
            derivative = {j-1: j*a for j, a in primitive.items() if j and a}
            expected = {j: a for j, a in {6: 9*T, 7: -9*U}.items() if a}
            if derivative != expected or sum(primitive.values(), E()) != 0:
                raise ValueError('whole primitive derivative and mark anchor')
            normals = []
            for j in range(9):
                # cos(theta_j)=cos(2j*pi/9); periodicity for cos(2theta_j).
                aa = 1-cosines[2*j]
                bb = 1-cosines[(4*j) % 18 if (4*j) % 18 <= 16 else 18-(4*j)%18]
                normals.append(-aa*U/8+bb*T/7)
            dual = U-T+w3*(normals[3]+normals[6])/2+w4*(normals[4]+normals[5])/2
            if fault == 'slack-sign' and U:
                dual = U-T-w3*(normals[3]+normals[6])/2-w4*(normals[4]+normals[5])/2
            same(f'entire third-response dual {channel} {i}', dual, 0)
            records.append({'third_coordinate': [channel, i],
                            'primitive': [[j, a.record()] for j, a in sorted(primitive.items())],
                            'all_nine_actual_normal_rows': [a.record() for a in normals]})
    return {'format': 1, 'agent': 'six-reviewer-1', 'role': 'independent mathematical reviewer',
            'cosine_bracket': [str(lo), str(hi)], 'records': records,
            'record_count': len(records), 'whole_cost_monomials': len(axis.a)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    parser.add_argument('--fault', choices=['transverse-sign', 'weight', 'missing-coordinate',
                                         'mean-square', 'cubic-factor', 'slack-sign'])
    args = parser.parse_args()
    r = compute(args.fault)
    raw = (json.dumps(r, sort_keys=True, separators=(',', ':'))+'\n').encode()
    if args.output:
        args.output.write_bytes(raw)
    print(json.dumps({'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
                      'record_count': r['record_count'],
                      'whole_cost_monomials': r['whole_cost_monomials']}, sort_keys=True))


if __name__ == '__main__':
    main()
