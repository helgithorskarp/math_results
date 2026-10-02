"""Separate endpoint checker: Q[sqrt(D)], no Schur solve or native field.

Only the frozen 17-orbit integer vector and the pinned original matrix
table are inputs. Signs use rational squares, not root isolation.
"""
from pathlib import Path
from fractions import Fraction as F
from math import comb, gcd, isqrt
import json
import inputs
from literal import require, core_data, domain, action, quadratic
from exact import digest
from claims import POLY

A, B, C = POLY
D = B*B-4*A*C


class Rad:
    def __init__(self, u=0, v=0):
        if isinstance(u, Rad):
            self.u, self.v = u.u, u.v
        else:
            self.u, self.v = F(u), F(v)

    def __add__(self, other):
        other = Rad(other)
        return Rad(self.u+other.u, self.v+other.v)

    __radd__ = __add__

    def __neg__(self):
        return Rad(-self.u, -self.v)

    def __sub__(self, other):
        return self+-Rad(other)

    def __rsub__(self, other):
        return Rad(other)+-self

    def __mul__(self, other):
        other = Rad(other)
        return Rad(self.u*other.u+D*self.v*other.v,
                   self.u*other.v+self.v*other.u)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = Rad(other)
        norm = other.u*other.u-D*other.v*other.v
        require(norm != 0, 'nonzero radical denominator')
        return self*Rad(other.u/norm, -other.v/norm)

    def __eq__(self, other):
        other = Rad(other)
        return self.u == other.u and self.v == other.v

    def sign(self):
        s = lambda value: (value > 0)-(value < 0)
        if not self.v:
            return s(self.u)
        if not self.u:
            return s(self.v)
        if s(self.u) == s(self.v):
            return s(self.u)
        difference = self.u*self.u-D*self.v*self.v
        require(difference != 0, 'irrational radical cannot equal a rational')
        return s(self.u) if difference > 0 else s(self.v)

    def native_record(self, branch):
        """Convert u+v sqrt(D) back to c0+c1*tau_branch."""
        require(branch in (-1, 1), 'two root embeddings only')
        return [str(self.u+branch*B*self.v), str(branch*2*A*self.v)]


def check(fixture=None):
    if fixture is None:
        fixture = json.loads(Path(__file__).with_name('CERTIFICATE.json').read_text())
    require((fixture['q'], fixture['k'], fixture['N']) == (8, 3, 89), 'fixed original family')
    require(fixture['polynomial'] == list(POLY), 'exact declared primitive polynomial')
    require(gcd(A, B, C) == 1 and A > 0 and C > 0 and B < 0 and D > 0,
            'primitive quadratic with positive endpoints')
    require(isqrt(D)**2 < D < (isqrt(D)+1)**2, 'non-square discriminant')
    X, N, s, C0, delta, R, U0 = core_data(8, 3, scan=True)
    require(X == domain(8, 3) and len(X) == N == 89, 'all original members scanned')
    masks = X[1:]
    rows = fixture['orbits']
    require(len(rows) == 17 and type(fixture['dual_integer_scale']) is int
            and fixture['dual_integer_scale'] > 0, 'compact positive-scale orbit fixture')
    keys = [tuple(row['key']) for row in rows]
    require(keys == sorted(set(keys)), 'unique sorted complete orbit keys')
    lookup = {tuple(row['key']): row for row in rows}
    key = lambda mask: (int(bool(mask&1)), (mask&6).bit_count(),
                        (mask&56).bit_count(), (mask>>6).bit_count())
    counts = {k: 0 for k in keys}
    coefficients = []
    for mask in masks:
        k = key(mask)
        require(k in lookup, 'missing original orbit')
        row = lookup[k]
        require(len(row['value']) == 2 and all(type(x) is int for x in row['value']),
                'two exact integer vector coefficients')
        coefficients.append(row['value'])
        counts[k] += 1
    for k, row in lookup.items():
        require(counts[k] == row['count'] == comb(2, k[1])*comb(3, k[2])*comb(5, k[3]),
                'literal and binomial original orbit counts')
    require(sum(counts.values()) == 88, 'all nonempty coordinates covered')
    Sa = [F(bool(mask&1)) for mask in masks]
    z = [F(1-bool(mask&2)-bool(mask&4)
           +int(mask.bit_count() == 3 or mask.bit_count() == 2 and mask&7 == mask))
         for mask in masks]
    ix = {mask: i for i, mask in enumerate(masks)}
    require(not any(action(C0, z)) and not any(action(R, z)), 'unmoved lower z kernel')
    require(not any(action(C0, Sa)) and not any(action(R, Sa))
            and not any(action(delta, Sa)), 'forced lower star kernel in every parameter')
    alpha = quadratic(z, delta)
    require(alpha == F(1071, 29) > 0, 'negative-kappa obstruction and positive perturbation')
    require(Sa[ix[1]] == z[ix[1]] == z[ix[8]] == 1 and Sa[ix[8]] == 0,
            'independent lower null vectors')
    require(not any(R[ix[8]]), 'repair has zero original outside-singleton row')
    embeddings = []
    for branch in (-1, 1):
        tau = Rad(F(-B, 2*A), F(branch, 2*A))
        require(A*tau*tau+B*tau+C == 0, 'root is exact')
        require((tau-F(1, 4)).sign() > 0 and (Rad(F(3, 8))-tau).sign() > 0
                if branch == -1 else (tau-6).sign() > 0 and (Rad(8)-tau).sign() > 0,
                'root orientation and original isolators')
        w = [Rad(a)+b*tau for a, b in coefficients]
        Uw, Rw, Dw = action(U0, w), action(R, w), action(delta, w)
        require(all(u == tau*r for u, r in zip(Uw, Rw)), 'all original endpoint cap-kernel actions')
        u, d, r = (sum(w[i]*v[i] for i in range(88)) for v in (Uw, Dw, Rw))
        require(u == tau*r and r.sign() == branch and d.sign() > 0,
                'opposite R signs and positive Delta signs at both real endpoints')
        outside = Dw[ix[8]]
        require(outside != 0, 'strict boundary obstruction in actual outside row')
        embeddings.append({'branch': branch, 'U0_pairing': u.native_record(branch),
                           'Delta_pairing': d.native_record(branch),
                           'R_pairing': r.native_record(branch),
                           'lower_slope': (d/(-r)).native_record(branch),
                           'upper_slope': (d/r).native_record(branch),
                           'outside_Delta_action': outside.native_record(branch)})
    one, two = embeddings
    for name in ('U0_pairing', 'Delta_pairing', 'R_pairing', 'lower_slope',
                 'upper_slope', 'outside_Delta_action'):
        require(one[name] == two[name], 'both radical embeddings recover the same native element')
    d0, d1 = map(F, one['Delta_pairing']); r0, r1 = map(F, one['R_pairing'])
    rho = r1/2
    require(r0 == rho*F(B, A) and rho > 0, 'complete oriented repair pairing')
    trace = 2*d0-F(B, A)*d1
    require(trace > 0, 'positive trace denominator')
    cap = rho*F(D, A*A)/trace
    require(F(1, 16) < cap < F(1, 14), 'rational enclosure of strict necessary bound')
    rec = {'q': 8, 'k': 3, 'N': N, 'polynomial': list(POLY), 'orbit_count': 17,
           'all_original_coordinates': 88, 'literal_binomial_counts_match': True,
           'embeddings': embeddings, 'negative_kappa_lower_alpha': str(alpha),
           'kappa_strict_necessary_bound': str(cap),
           'imported_schur_or_native_field': False}
    rec['record_sha256'] = digest(rec)
    return rec


if __name__ == '__main__':
    print(json.dumps(check(), sort_keys=True, indent=2))
