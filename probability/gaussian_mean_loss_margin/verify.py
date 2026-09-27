#!/usr/bin/env python3
"""Exact finite controls for PROOF.md; not a proof of its compactness step."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parent

def need(value, message):
    if not value:
        raise ValueError(message)

def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))

def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))

def norm2(a):
    return dot(a, a)

def mean(xs, ws):
    return tuple(sum((w*x[j] for w, x in zip(ws, xs)), F(0)) for j in range(3))

def center(xs, ws):
    m = mean(xs, ws)
    return [sub(x, m) for x in xs]

def cross(xs, ys, ws):
    return [[sum((w*x[i]*y[j] for w, x, y in zip(ws, xs, ys)), F(0))
             for j in range(3)] for i in range(3)]

def determinant(a):
    n = len(a)
    if n == 0:
        return F(1)
    if n == 1:
        return a[0][0]
    return sum(((-1)**j*a[0][j]*determinant(
        [[a[i][k] for k in range(n) if k != j] for i in range(1, n)])
        for j in range(n)), F(0))

def positive_semidefinite(a):
    if any(a[i][j] != a[j][i] for i in range(3) for j in range(3)):
        return False
    return all(determinant([[a[i][j] for j in ids] for i in ids]) >= 0
               for n in range(1, 4) for ids in combinations(range(3), n))

def validate(xs, ys, ws, radius, kappa):
    need(len(xs) == len(ys) == len(ws) and len(ws) > 0, 'matching nonempty inputs')
    need(all(len(x) == 3 for x in xs+ys), 'three coordinates')
    need(all(w > 0 for w in ws) and sum(ws) == 1, 'positive probability weights')
    need(mean(xs, ws) == (0, 0, 0) and mean(ys, ws) == (0, 0, 0), 'centered data')
    need(all(norm2(x) <= radius**2 for x in xs), 'source radius')
    covariance = cross(xs, xs, ws)
    need(positive_semidefinite([[covariance[i][j]-(kappa if i == j else 0)
                                for j in range(3)] for i in range(3)]),
         'positive source covariance floor')
    need(positive_semidefinite(cross(xs, ys, ws)), 'identity Procrustes alignment')
    loss = [[norm2(sub(x, xp))-norm2(sub(y, yp)) for xp, yp in zip(xs, ys)]
            for x, y in zip(xs, ys)]
    need(all(d >= 0 for row in loss for d in row), 'pair contraction')
    return covariance, loss

def total_pair(matrix, ws, rows, cols):
    return sum((ws[i]*ws[j]*matrix[i][j] for i in rows for j in cols), F(0))

def enc(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): enc(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [enc(v) for v in value]
    return value

def rejected(fn):
    try:
        fn()
    except ValueError:
        return 1
    raise ValueError('damaged input was accepted')

def run():
    base = [(-1, 0, 0), (-2, 1, 0), (-2, 0, 1), (-2, -1, -1)]
    original_x = [tuple(map(F, x)) for x in base+[(1, 0, 0)]]
    original_y = [tuple(map(F, x)) for x in base+[(-1, 0, 0)]]
    rows = []
    identity_checks = 0
    for exponent in [1, 4, 8, 20, 60]:
        a = F(1, 2**exponent)
        ws = [(1-a)/4]*4+[a]
        xs, ys = center(original_x, ws), center(original_y, ws)
        covariance, loss = validate(xs, ys, ws, F(3), F(3, 32))
        ids = list(range(5))
        D = total_pair(loss, ws, ids, ids)
        Qloss = total_pair([[d*d for d in row] for row in loss], ws, ids, ids)
        need(Qloss == 104*a*(1-a) and Qloss/D == F(52, 7), 'nonvanishing second loss ratio')
        need((Qloss/D)/36 == F(13, 63) > F(1, 2**48), 'scaled family fails the concurrent quartic guard')
        need(F(3, 32)/36 >= F(1, 2**15), 'scaled family keeps the guard covariance floor')
        hs = [sub(y, x) for x, y in zip(xs, ys)]
        M = sum((w*norm2(h) for w, h in zip(ws, hs)), F(0))
        need(D == 14*a*(1-a), 'loss formula')
        need(M == 4*a*(1-a), 'Procrustes error formula')
        need(max(norm2(h) for h in hs) == 4*(1-a)**2, 'large rare displacement')
        need(D == 2*sum((ws[i]*(norm2(xs[i])-norm2(ys[i])) for i in ids), F(0)),
             'centered trace loss')
        A, B = list(range(4)), [4]
        D_AA = total_pair(loss, ws, A, A)
        D_AB = total_pair(loss, ws, A, B)
        D_BB = total_pair(loss, ws, B, B)
        need(D == D_AA+2*D_AB+D_BB, 'loss decomposition')
        need(D_AA == D_BB == 0 and D_AB == 7*a*(1-a), 'rare/core losses')
        M_A = sum((ws[i]*norm2(hs[i]) for i in A), F(0))
        need(M_A == 4*a*a*(1-a), 'quadratically smaller core displacement')
        for i in ids:
            q = sum((ws[j]*loss[i][j] for j in ids), F(0))
            need(q == norm2(xs[i])-norm2(ys[i])+D/2, 'one-label centered loss')
            for j in ids:
                need(-2*dot(sub(xs[i], xs[j]), sub(hs[i], hs[j]))
                     == loss[i][j]+norm2(sub(hs[i], hs[j])), 'symmetric first variation')
                identity_checks += 1
        # Independent operator-level check of the double-centering identity.
        gm = [[dot(xs[i], xs[j])-dot(ys[i], ys[j]) for j in ids] for i in ids]
        dm = [sum((ws[j]*loss[i][j] for j in ids), F(0)) for i in ids]
        for i in ids:
            for j in ids:
                need(gm[i][j] == -(loss[i][j]-dm[i]-dm[j]+D)/2,
                     'double-centered distance kernel')
                identity_checks += 1
        if exponent >= 4:
            delta = F(1, 8)
            need([i for i in ids if norm2(hs[i]) <= delta**2] == A, 'threshold core')
            R, kappa = F(3), F(3, 32)
            K0, L = 2*R**2/kappa, 96*R**3/kappa+6*R
            need(a <= K0*D/delta**2, 'rare probability bound')
            need(M_A <= 32*R/kappa*delta*D+2*L**2*a*a, 'bulk remainder bound')
        rows.append({'alpha': a, 'loss': D, 'second_loss_moment': Qloss, 'second_to_first_loss_ratio': Qloss/D,
                     'mean_square_displacement': M,
                     'sup_displacement': 2*(1-a), 'core_square_displacement': M_A,
                     'D_AA': D_AA, 'D_AB': D_AB, 'D_BB': D_BB,
                     'covariance_determinant': determinant(covariance)})

    # A single point moves closer to each point of a fixed full-rank background.
    bw = [F(1, 4)]*4
    z = center([tuple(map(F, x)) for x in base], bw)
    bm = mean([tuple(map(F, x)) for x in base], bw)
    x, y = sub((F(1), F(0), F(0)), bm), sub((F(-1), F(0), F(0)), bm)
    q = norm2(x)-norm2(y)
    single = [norm2(sub(x, t))-norm2(sub(y, t)) for t in z]
    need(single == list(map(F, [4, 8, 8, 8])) and q == 7, 'one-point half-space losses')
    need(sum((w*d for w, d in zip(bw, single)), F(0)) == q, 'one-point mean loss')
    need(q >= 2*F(3, 16)/3*2, 'one-point covariance coercivity')
    for t, d in zip(z, single):
        need(d == q+2*dot(t, sub(y, x)), 'half-space equation')

    # Malformed data and a genuine expansion must fail independently of asserts.
    ws = [F(3, 16)]*4+[F(1, 4)]
    xs, ys = center(original_x, ws), center(original_y, ws)
    rejects = 0
    rejects += rejected(lambda: validate(xs, ys, [F(-1)]+ws[1:], F(3), F(3, 32)))
    rejects += rejected(lambda: validate(xs[:-1], ys, ws, F(3), F(3, 32)))
    rejects += rejected(lambda: validate(xs, ys, ws, F(1, 8), F(3, 32)))
    rejects += rejected(lambda: validate(xs, ys, ws, F(3), F(100)))
    expanded = [tuple(2*t for t in x) for x in xs]
    rejects += rejected(lambda: validate(xs, expanded, ws, F(3), F(3, 32)))
    singular = [(F(-1), F(0), F(0)), (F(1), F(0), F(0))]
    rejects += rejected(lambda: validate(singular, singular, [F(1, 2)]*2, F(3), F(3, 32)))
    return {'status': 'MEAN_LOSS_MARGIN_CONTROLS_PASS',
            'scope': 'Exact rational calibration and algebra only; no value for the compactness constants and no numerical proof of Theorem 1.',
            'radius': F(3), 'covariance_floor': F(3, 32),
            'fold_controls': rows, 'pair_identity_checks': identity_checks,
            'damaged_input_rejections': rejects,
            'one_point_control': {'losses': single, 'mean_loss': q}}

def main():
    record = (json.dumps(enc(run()), indent=2, sort_keys=True)+'\n').encode()
    expected = ROOT/'EXPECTED.json'
    if sys.argv[1:] == ['--write-expected']:
        need(not expected.exists(), 'refusing to replace existing expected output')
        expected.write_bytes(record)
    else:
        need(not sys.argv[1:], 'usage: verify.py [--write-expected]')
        need(expected.read_bytes() == record, 'expected output mismatch')
    print('MEAN_LOSS_MARGIN_CONTROLS_PASS')
    print('record_sha256='+hashlib.sha256(record).hexdigest())

if __name__ == '__main__':
    main()
