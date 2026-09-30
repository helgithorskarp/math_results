#!/usr/bin/env python3
"""Standalone author coefficient derivation for PROOF.md; exact arithmetic only.

Agent six-sendov-2, role researcher. No imported campaign proof/checker.
Laurent ring Q[d,d^-1,k,k^-1], with d=1+a>0 and k=2,4,6.
"""
from fractions import Fraction as Q
from hashlib import sha256
from math import factorial
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

    def at(self, d0, k0=None):
        out = L(0)
        for (dp, kp), c in self.t.items():
            if k0 is None:
                out += L({(0, kp): c*Q(d0)**dp})
            else:
                out += c*Q(d0)**dp*Q(k0)**kp
        return out

    def dump(self):
        return [[p[0], p[1], str(c)] for p, c in sorted(self.t.items())]


d = L({(1, 0): 1})
k = L({(0, 1): 1})
N = 3  # coefficients through delta squared


def const(c):
    return [L(c)] + [L(0) for _ in range(N-1)]


def add(x, y):
    return [a+b for a, b in zip(x, y)]


def neg(x):
    return [-a for a in x]


def sub(x, y):
    return add(x, neg(y))


def scale(x, c):
    return [a*c for a in x]


def mul(x, y):
    return [sum((x[j]*y[i-j] for j in range(i+1)), L(0))
            for i in range(N)]


def inv(x):
    y = [1/x[0]]
    for i in range(1, N):
        y.append(-sum((x[j]*y[i-j] for j in range(1, i+1)), L(0))/x[0])
    return y


def sqrt(x, b0):
    if L(b0)**2 != x[0]:
        raise ValueError('wrong specified square-root base')
    y = [L(b0)]
    for i in range(1, N):
        y.append((x[i]-sum((y[j]*y[i-j] for j in range(1, i)), L(0)))/(2*b0))
    return y


delta = [L(0), L(1), L(0)]
a = d-1


def residual(w):
    # Exact product-rule cubic R0(z)+delta Q(z).
    zp = add(w, const(1))
    r0 = mul(mul(zp, zp), add(scale(w, 9), const(1-8*a)))
    q = add(add(scale(mul(w, w), -(18-k)),
                scale(w, (16-k)*a-(k+2))), const(k*a))
    return add(r0, mul(delta, q))


def derive():
    w = const((8*a-1)/9)
    derivative = 64*d**2/9
    for j in range(1, N):
        w[j] = -residual(w)[j]/derivative
    W = sub(const(a), w)
    V = sub(const(d**2), scale(delta, 2*a))
    far_q = inv(W)
    pair_product = scale(mul(scale(V, d), far_q), Q(1, 9))
    pair_qmod = inv(sqrt(pair_product, d))
    repeated_qmod = inv(sqrt(V, d))
    total = add(add(add(const((7-k)/d), scale(repeated_qmod, k-2)),
                    far_q), scale(pair_qmod, 2))
    energy = mul(scale(delta, 2*k/d**2), inv(V))
    total_sum = const(-(27-8*d)/9)
    total_sum[1] = (18-k)/9
    near_sum = sub(total_sum, w)
    c1 = const(11-16*a)
    c1[1] = (16-k)*a-(k+2)
    near_product = sub(scale(c1, Q(1,9)), mul(w, near_sum))
    discriminant = sub(mul(near_sum, near_sum), scale(near_product, 4))
    return {'w': w, 'R': residual(w), 'W': W, 'V': V, 'far_q': far_q,
            'pair_product': pair_product, 'pair_qmod': pair_qmod,
            'repeated_qmod': repeated_qmod, 'F': total, 'E': energy,
            'near_sum': near_sum, 'near_product': near_product,
            'near_discriminant': discriminant}


class G:
    """Exact Q(i sqrt(gamma)); its real embedding needs gamma>0."""
    def __init__(self, re=0, im=0, gamma=Q(1)):
        self.re, self.im, self.gamma = Q(re), Q(im), Q(gamma)

    def lift(self, other):
        if not isinstance(other, G):
            return G(other, gamma=self.gamma)
        if other.gamma != self.gamma:
            if other.im:
                raise ValueError('different quadratic extensions')
            return G(other.re, gamma=self.gamma)
        return other

    def __add__(self, other):
        other = self.lift(other)
        return G(self.re+other.re, self.im+other.im, self.gamma)

    __radd__ = __add__

    def __neg__(self):
        return G(-self.re, -self.im, self.gamma)

    def __sub__(self, other):
        return self + -self.lift(other)

    def __rsub__(self, other):
        return self.lift(other) + -self

    def __mul__(self, other):
        other = self.lift(other)
        return G(self.re*other.re-self.gamma*self.im*other.im,
                 self.re*other.im+self.im*other.re, self.gamma)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.lift(other)
        norm = other.re**2+self.gamma*other.im**2
        if not norm:
            raise ZeroDivisionError('quadratic-extension zero')
        return self*G(other.re/norm, -other.im/norm, self.gamma)

    def __rtruediv__(self, other):
        return self.lift(other)/self

    def __eq__(self, other):
        other = self.lift(other)
        return self.re == other.re and self.im == other.im

    def conj(self):
        return G(self.re, -self.im, self.gamma)


def gc(value, size, gamma):
    return [G(value, gamma=gamma)]+[G(0,gamma=gamma) for _ in range(size-1)]


def ga(x, y):
    return [a+b for a,b in zip(x,y)]


def gs(x, c):
    return [a*c for a in x]


def gm(x, y):
    size = len(x)
    return [sum((x[j]*y[i-j] for j in range(i+1)), G(0,gamma=x[0].gamma))
            for i in range(size)]


def gi(x):
    y = [1/x[0]]
    for i in range(1,len(x)):
        y.append(-sum((x[j]*y[i-j] for j in range(1,i+1)),G(0,gamma=x[0].gamma))/x[0])
    return y


def gmod(x, positive_base):
    norm = gm(x,[c.conj() for c in x])
    if norm[0] != positive_base**2:
        raise ValueError('modulus base mismatch')
    y = [G(positive_base,gamma=x[0].gamma)]
    for i in range(1,len(x)):
        y.append((norm[i]-sum((y[j]*y[i-j] for j in range(1,i)),G(0,gamma=x[0].gamma)))/(2*positive_base))
    if any(c.im for c in y):
        raise ValueError('non-real modulus coefficient')
    return y, norm


def direct_profile(a0, k0, check):
    """Separate individual-critical-root route in t, not the pair-product sum.

    Both algorithms are author checks, not independent reviewer evidence.
    """
    size, d0 = 6, 1+a0
    gamma = Q(8-k0,8)
    c = gc(0,size,gamma)
    for j in range(0,size,2):
        c[j] = G(Q((-1)**(j//2),factorial(j)),gamma=gamma)
    def r(z):
        zp = ga(z,gc(1,size,gamma))
        quad = ga(ga(gm(z,z),gs(gm(c,z),2)),gc(1,size,gamma))
        first = gm(ga(gs(z,9-k0),gc(1-(8-k0)*a0,size,gamma)),quad)
        second = gs(gm(gm(ga(z,gc(-a0,size,gamma)),zp),ga(z,c)),k0)
        return ga(first,second)

    root = gc(Q(8*a0-1,9),size,gamma)
    derivative = Q(64,9)*d0**2
    for j in range(1,size):
        root[j] = -r(root)[j]/derivative
    roots = [root]
    for sign in [-1,1]:
        h = gc(0,size,gamma)
        h[0] = G(0,sign,gamma)
        den = -16*d0*h[0]
        for j in range(1,4):
            z = gc(-1,size,gamma)
            for ell in range(1,5):
                z[ell] = h[ell-1]
            h[j] = -r(z)[j+2]/den
        z = gc(-1,size,gamma)
        for ell in range(1,5):
            z[ell] = h[ell-1]
        roots.append(z)
    qmods = []
    for branch,z in enumerate(roots):
        for j in range(6):
            check('direct cubic residual', r(z)[j],0)
        dist = ga(gc(a0,size,gamma),gs(z,-1))
        qr = gi(dist)
        for j,res in enumerate(gm(dist,qr)):
            check('direct critical inverse residual',res,1 if j == 0 else 0)
        base = 9/d0 if branch == 0 else 1/d0
        b,norm = gmod(qr,base)
        for x,y in zip(gm(b,b),norm):
            check('direct critical modulus residual',x,y)
        qmods.append([x.re for x in b[:5]])

    # Original roots and repeated critical factors are expanded in Q(i).
    exp = gc(0,size,Q(1))
    for j in range(size):
        exp[j] = G(Q([1,0,-1,0][j%4],factorial(j)),
                   Q([0,1,0,-1][j%4],factorial(j)))
    original_distance = ga(gc(a0,size,Q(1)),exp)
    u = gi(original_distance)
    for j,res in enumerate(gm(original_distance,u)):
        check('direct original inverse residual',res,1 if j == 0 else 0)
    umod,unorm = gmod(u,1/d0)
    for x,y in zip(gm(umod,umod),unorm):
        check('direct repeated modulus residual',x,y)
    motion = ga(u,gc(-1/d0,size,Q(1)))
    energy = gs(gm(motion,[x.conj() for x in motion]),k0)
    total = [(k0-2)*umod[j].re+sum(row[j] for row in qmods)
             +(Q(7-k0)/d0 if j == 0 else 0) for j in range(5)]
    for j in range(5):
        check('direct energy real',energy[j].im,0)
    return total,[x.re for x in energy[:5]]


def product_coefficients():
    """Product differentiation in the polynomial variable, over delta series."""
    c = sub(const(1),delta)
    def padd(x,y):
        size = max(len(x),len(y))
        return [add(x[j] if j<len(x) else const(0),
                    y[j] if j<len(y) else const(0)) for j in range(size)]
    def pmul(x,y):
        out = [const(0) for _ in range(len(x)+len(y)-1)]
        for i,a0 in enumerate(x):
            for j,b0 in enumerate(y):
                out[i+j] = add(out[i+j],mul(a0,b0))
        return out
    first = pmul([const(1-(8-k)*a),const(9-k)],
                 [const(1),scale(c,2),const(1)])
    second = pmul(pmul([const(-a),const(1)],[const(1),const(1)]),
                   [c,const(1)])
    return padd(first,[scale(x,k) for x in second])


def main():
    data = derive()
    names = []
    def check(name, lhs, rhs):
        if lhs != rhs:
            raise AssertionError(name)
        names.append(name)
    for j, c in enumerate(data['R']):
        check('far-root cubic residual '+str(j), c, 0)
    check('far implicit derivative', 9*((8*a-1)/9+1)**2, 64*d**2/9)
    check('collapse total', data['F'][0], 16/d)
    check('free-radius gap delta coefficient', data['F'][1], 2*k*(a-Q(5,8))/d**3)
    check('energy delta coefficient', data['E'][1], 2*k/d**4)
    check('pair discriminant constant', data['near_discriminant'][0], 0)
    check('pair discriminant first coefficient', data['near_discriminant'][1], -(8-k))
    for j,c in enumerate(sub(data['pair_product'],
            add(sub(const(a**2),scale(data['near_sum'],a)),data['near_product']))):
        check('pair Vieta distance product '+str(j), c, 0)
    check('cutoff fourth coefficient', data['F'][2].at(Q(13,8)),
          -70*k*(11*k+32)/13**5)
    a2 = k*(L(Q(885,128))-Q(405,4096)*k
             +d*(Q(-163,16)+Q(27,512)*k)
             +d**2*(Q(29,8)-Q(1,256)*k))/d**5
    check('free-radius second delta coefficient',data['F'][2],a2)
    kappa = d*(a-Q(5,8))
    Ka = d**3*((48*d**2-40*d-53)/(512*k)
              +(16*d**2-216*d+405)/16384)
    check('free-radius quartic in energy',data['E'][1]**2*Ka,
          kappa*data['E'][2]-data['F'][2])
    coeff = [const(1-8*a),const(11-16*a),const(19-8*a),const(9)]
    coeff[0][1],coeff[1][1],coeff[2][1] = k*a,(16-k)*a-(k+2),-(18-k)
    for x,y in zip(product_coefficients(),coeff):
        for aa,bb in zip(x,y):
            check('generic product-rule coefficient',aa,bb)
    for x,y in zip(mul(data['W'],data['far_q']),const(1)):
        check('generic far inverse residual',x,y)
    for key,target in [('repeated_qmod',data['V']),('pair_qmod',data['pair_product'])]:
        for x,y in zip(mul(mul(data[key],data[key]),target),const(1)):
            check('generic inverse modulus square '+key,x,y)
    for x,y in zip(mul(mul(data['E'],const(d**2)),data['V']),scale(delta,2*k)):
        check('generic energy cleared residual',x,y)
    generic_count = len(names)
    # Univariate t substitution of delta=1-cos(t) is a distinct root algorithm.
    profiles,entries,controls = [],0,[]
    for a0 in [Q(1,4),Q(1,2),Q(5,8),Q(3,4),Q(7,8)]:
        for k0 in [2,4,6]:
            f,e = direct_profile(a0,k0,check)
            fdelta = [x.at(1+a0,k0) for x in data['F']]
            edelta = [x.at(1+a0,k0) for x in data['E']]
            expected_f = [fdelta[0],L(0),fdelta[1]/2,L(0),fdelta[2]/4-fdelta[1]/24]
            expected_e = [L(0),L(0),edelta[1]/2,L(0),edelta[2]/4-edelta[1]/24]
            for j in range(5):
                check('separate root vs product F coefficient',L(f[j]),expected_f[j])
                check('separate root vs product E coefficient',L(e[j]),expected_e[j])
                entries += 2
            profiles.append([str(a0),k0])
            controls.append([str(a0),k0,[str(x) for x in f],[str(x) for x in e]])
    table = []
    for k0 in [2,4,6]:
        cutoff_f = data['F'][2].at(Q(13,8),k0)
        f4 = next(iter(cutoff_f.t.values()))/4
        e2 = Q(k0)/Q(13,8)**4
        K = -f4/e2**2
        B = Q(13,8)**4/(k0*K)
        expected_K = Q(76895*(11*k0+32),33554432*k0)
        check('profile energy coefficient',L(K),L(expected_K))
        check('profile squared basin constant',L(B),L(Q(106496,35*(11*k0+32))))
        table.append({'k':k0,'root_quartic':str(-f4),'energy_quartic':str(K),
                      'squared_basin_constant':str(B)})
    check('three-block comparison ratio',L(Q(53248,1715)/Q(3328,75)),L(Q(240,343)))
    wrong = [Q(3767855,100663296)+Q(1,100663296),
             Q(3767855,100663296)-Q(1,100663296),
             Q(560235,8388608),Q(2076165,33554432)]
    actual = Q(3767855,100663296)
    rejected = sum(candidate != actual for candidate in wrong)
    if rejected != 4:
        raise AssertionError('quartic mutation unexpectedly accepted')
    if data['near_discriminant'][1].at(Q(13,8),6) == 2:
        raise AssertionError('wrong discriminant sign accepted')
    if Q(53248,1715) == Q(3328,75):
        raise AssertionError('two-block constant mutation accepted')
    digest_input = {'generic':{key:[x.dump() for x in val] for key,val in sorted(data.items())},
                    'direct':controls}
    digest = sha256(json.dumps(digest_input,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    out = {'agent':'six-sendov-2','role':'researcher',
           'proof_status':'ordinary author proof; independent review pending; not formalized',
           'arithmetic':'Python 3.11 standard library; no imported campaign checker or floating point',
           'generic_identities':generic_count,'total_exact_checks':len(names),
           'direct_profiles':len(profiles),'separate_F_E_entries':entries,
           'rejected_mutations':rejected+2,'coefficient_sha256':digest,
           'profile_table':table,'ratio_to_reviewed_two_block_squared':'240/343'}
    manifest = Path(__file__).with_name('expected.json')
    if manifest.exists() and json.loads(manifest.read_text()) != out:
        raise AssertionError('fixed manifest mismatch')
    print(json.dumps(out,indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
