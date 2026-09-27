"""Exact supplementary checks, not a Gaussian-profile computation or review."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def affine_le(left, right, lower=F(8)):
    """Certificate for a*q+b <= c*q+d on the whole half-line q>=lower."""
    slope = right[0] - left[0]
    start = slope * lower + right[1] - left[1]
    need(slope >= 0 and start >= 0, 'invalid universal affine bound')
    return [str(slope), str(start)]


def exponent_checks():
    def combine(terms, constant=0):
        return (sum(a*n for n, (a, b) in terms),
                constant+sum(b*n for n, (a, b) in terms))

    # Positive affine bounds for negative logs of lower bounds, or logs of
    # upper bounds. Derive the seven expressions from the cutoff formula.
    radius, inv_kappa, inv_w = (1, 0), (1, 0), (4, 0)
    K0 = K2 = (4, 0)
    alignment, inv_c0, inv_delta = (8, 0), (16, 0), (32, 0)
    raw = [
        combine([(2, inv_kappa), (2, radius), (1, K0)], 2),
        combine([(2, inv_delta), (1, K0)], 1),
        combine([(1, inv_kappa), (2, inv_delta), (2, radius), (1, K0)], 3),
        combine([(4, inv_w), (2, inv_kappa), (2, inv_delta),
                 (4, radius), (1, K0)], 8),
        combine([(1, inv_kappa), (1, inv_delta), (1, radius)], -1),
        combine([(1, inv_c0), (4, inv_delta), (2, alignment), (2, K0)], 3),
        combine([(2, inv_c0), (4, inv_delta), (2, K2), (3, K0)], 6),
    ]
    rounded = [9, 69, 72, 91, 34, 169, 181]
    certs = [affine_le(a, (b, 0)) for a, b in zip(raw, rounded)]
    for b in rounded:
        affine_le((b, 0), (256, 0))
    affine_le((F(8, 128)+F(1, 4), 0), (1, 0))
    affine_le((F(32, 128)+F(9, 4), 0), (4, 0))
    intermediate = [((3, 1), (4, 0)), ((2, 4), (4, 0)),
                    ((3, 1), (4, 0)), ((4, 7), (8, 0)),
                    ((9, 4), (16, 0)), ((20, 2), (32, 0)),
                    ((256, 0), (8192, -1)),
                    ((16, 7), (3*8192, 0))]
    for a, b in intermediate:
        affine_le(a, b)
    need(F(5, 1024) < 1, 'core radius bound')
    # Dyadic induction bases for sqrt(m) and 64m<=2^m.
    need(F(21, 2) <= 2**7, 'sqrt induction base')
    need(F(22, 2) <= 21, 'sqrt induction step at least as strong')
    need(64*16 <= 2**16 and F(17, 16) <= 2, 'tail polynomial absorption')
    need(8 < 9 and 9*32 < 17**2, 'Gaussian exponential moment bounds')
    need(F(17, 16) < F(3, 2), 'conditional covariance lower bound')
    need(F(256, 169) < 2, 'normalization upper bound')
    schedules = []
    for L, b in [(1, 20), (2, 20), (1, 100), (17, 60), (200, 1000)]:
        m = 2**20*(L*L+b+1)
        q = F(m, 8192)
        need(q >= 2816 and L*L <= q/128 and b+1 <= q/128, 'schedule')
        schedules.append({'L': L, 'b': b, 'M': m, 'q': str(q)})
    damaged = 0
    for a, b in [((90, 8), (90, 0)), ((180, 6), (180, 0)),
                 ((9, 4), (8, 0))]:
        try:
            affine_le(a, b)
        except ValueError:
            damaged += 1
    need(damaged == 3, 'damaged certificates not rejected')
    return {'raw_exponents': raw, 'rounded_coefficients': rounded,
            'universal_affine_certificates': certs,
            'schedules': schedules, 'damaged_certificates_rejected': damaged}


def dot(x, y):
    return sum((a*b for a, b in zip(x, y)), F(0))


def sub(x, y):
    return tuple(a-b for a, b in zip(x, y))


def finite_controls():
    # Finite symmetric latent-noise laws test algebra only, not Gaussian tails.
    vs = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    us = [tuple(F(a, 4) for a in v) for v in vs]
    cases = pairs = retained = scaled_pairs = 0
    for p in [F(1, 8), F(1, 32), F(1, 256)]:
        for outer in [4, 8]:
            sigma = F(1, 8)
            data = []
            for u in us:
                for radius, mass, core in [(1, 1-p, True), (outer, p, False)]:
                    for j in range(3):
                        for sign in [-1, 1]:
                            z = tuple(F(sign*radius if k == j else 0) for k in range(3))
                            x = tuple(a+sigma*b for a, b in zip(u, z))
                            y = (min(x[0], F(2, 5)-x[0]), x[1]/2, x[2])
                            data.append((x, y, mass/24, core))
            need(sum(a[2] for a in data) == 1, 'full probability')
            means = [[sum(w*x[j] for x, y, w, a in data),
                      sum(w*x[j] for x, y, w, a in data if a)/(1-p)] for j in range(3)]
            need(all(v == [0, 0] for v in means), 'latent truncation changed centering')
            for i in range(3):
                for j in range(3):
                    cov = sum(w*x[i]*x[j] for x, y, w, a in data if a)/(1-p)
                    expected = F(1, 16)+sigma*sigma/3 if i == j else F(0)
                    need(cov == expected, 'conditional covariance identity')
            d = cc = tail = F(0)
            for x, y, w, a in data:
                for xp, yp, wp, ap in data:
                    dx, dy = sub(x, xp), sub(y, yp)
                    loss = dot(dx, dx)-dot(dy, dy)
                    need(loss >= 0, 'expanding finite control')
                    weight_loss = w*wp*loss
                    d += weight_loss
                    if a and ap:
                        cc += weight_loss
                    else:
                        tail += weight_loss
                    pairs += 1
                    sx = tuple(F(3, 2)*v for v in dx)
                    sy = tuple(F(3, 2)*v for v in dy)
                    need((dot(sx, sx)-dot(sy, sy))/F(9, 4) == loss,
                         'variance normalization')
                    scaled_pairs += 1
            d0 = cc/(1-p)**2
            need(d == (1-p)**2*d0+tail, 'retained loss decomposition')
            moment = sum(w*dot(x, x) for x, y, w, a in data)
            tail_moment = sum(w*dot(x, x) for x, y, w, a in data if not a)
            need(tail <= 2*tail_moment+2*p*moment, 'union moment estimate')
            target_mean = tuple(sum(w*y[j] for x, y, w, a in data) for j in range(3))
            target_moment = sum(w*dot(y, y) for x, y, w, a in data)
            need(d == 2*(moment-target_moment+dot(target_mean, target_mean)),
                 'pair versus variance loss')
            if tail <= d/2:
                need(d/2 <= d0 <= 2*d, 'relative retention implication')
                retained += 1
            cases += 1
    # An arbitrarily small tail can carry ALL loss: mass alone is insufficient.
    for n in [2, 8, 20]:
        p = F(1, 2**n)
        law = [(F(0), 1-p), (F(1), p/2), (F(-1), p/2)]
        d = sum(w*wp*(x-xp)**2 for x, w in law for xp, wp in law)
        need(d == 2*p > 0, 'lost-tail control')
        need(not (d/2 <= 0), 'missing retention premise not detected')
    need(retained > 0, 'no retained finite controls')
    return {'finite_laws': cases, 'ordered_pairs': pairs,
            'variance_scalings': scaled_pairs, 'relative_retention_cases': retained,
            'all_loss_in_small_tail_controls': 3}


def run():
    pins = json.loads((ROOT/'INPUTS.json').read_text())
    for item in pins['files']:
        raw = (ROOT/item['path']).read_bytes()
        need(hashlib.sha256(raw).hexdigest() == item['sha256'], 'dependency hash mismatch')
    return {'status': 'REGULARIZED_CONTACT_MARGIN_PASS',
            'pinned_inputs': len(pins['files']),
            'exponents': exponent_checks(), 'finite_algebra': finite_controls(),
            'gaussian_profile_computed': False, 'independent_review': False,
            'unrestricted_sign_proved': False}


if __name__ == '__main__':
    need(sys.argv[1:] in ([], ['--emit']), 'usage: verify.py [--emit]')
    result = run()
    if sys.argv[1:] == ['--emit']:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        expected = json.loads((ROOT/'EXPECTED.json').read_text())
        # JSON round trip treats tuples in the internally generated record as lists.
        need(json.loads(json.dumps(result)) == expected, 'expected-record mismatch')
        print(result['status'])
        print('Seven universal cutoff budgets; six finite conditional-law controls.')
