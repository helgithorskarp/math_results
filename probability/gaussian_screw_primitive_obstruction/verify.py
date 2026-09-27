#!/usr/bin/env python3
"""Exact ancillary certificates; no Gaussian integration or motion search."""
from fractions import Fraction as F
from pathlib import Path
from itertools import combinations, product
from copy import deepcopy
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def dot(x, y):
    return sum((a*b for a, b in zip(x, y)), F(0))


def sub(x, y):
    return tuple(a-b for a, b in zip(x, y))


def sq(x):
    return dot(x, x)


def d2(x, y):
    return sq(sub(x, y))


def rank(rows):
    a = [list(map(F, row)) for row in rows]
    if not a:
        return 0
    r = 0
    for c in range(len(a[0])):
        k = next((k for k in range(r, len(a)) if a[k][c]), None)
        if k is None:
            continue
        a[r], a[k] = a[k], a[r]
        v = a[r][c]
        a[r] = [x/v for x in a[r]]
        for k in range(r+1, len(a)):
            v = a[k][c]
            if v:
                a[k] = [x-v*y for x, y in zip(a[k], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def det(rows):
    n = len(rows)
    require(all(len(row) == n for row in rows), 'square determinant required')
    a = [list(map(F, row)) for row in rows]
    result = F(1)
    for c in range(n):
        k = next((k for k in range(c, n) if a[k][c]), None)
        if k is None:
            return F(0)
        if k != c:
            a[k], a[c] = a[c], a[k]
            result = -result
        v = a[c][c]
        result *= v
        for k in range(c+1, n):
            t = a[k][c]/v
            for j in range(c+1, n):
                a[k][j] -= t*a[c][j]
    return result


def j(u):
    return (-u[1], u[0])


def p0(u):
    return (u[0]+u[1], u[1]-u[0])


def a(v):
    return (*v, (1+sq(v))/2)


def b(u):
    return (*u, -sq(u))


def fixture():
    us = [tuple(map(F, u)) for u in
          [(0,0),(1,0),(-1,0),(2,0),(-2,0),(0,1),(0,-1),(1,1)]]
    vs = {p0(u) for u in us}
    for u, axis, sign in product(us[:2], range(2), [-1,1]):
        v = list(p0(u))
        v[axis] += F(sign,4)
        vs.add(tuple(v))
    vs = sorted(vs)
    xs = [a(v) for v in vs]+[b(u) for u in us]
    ys = [a(v) for v in vs]+[(*j(u), 1-sq(u)) for u in us]
    return us, vs, xs, ys


def loss_form(v, u):
    """17 exact coefficients: M[0:9], t[9:12], c[12:15], d, constant."""
    av, bu = a(v), b(u)
    return ([2*av[i]*bu[k] for i in range(3) for k in range(3)]
            +[2*x for x in av]+[-2*x for x in bu]+[F(-1), -2*dot(av,bu)])


def blocked_form(v, u):
    # M=diag(N,1), t=(v0,tau), c=(c_perp,tau).
    q = loss_form(v,u)
    return [q[0],q[1],q[3],q[4],q[9],q[10],q[11]+q[14],
            q[12],q[13],q[15],q[16]+q[8]]


def matched_quadratic(u):
    v = p0(u)
    return ([2*v[i]*u[k] for i in range(2) for k in range(2)]
            +[2*x for x in v]+[1+4*sq(u)]
            +[-2*x for x in u]+[F(-1),-2*dot(v,u)])


def height(xs, ia0, iap, iam, ib0):
    r = {ib0:F(1), ia0:F(-3,2), iap:F(1,4), iam:F(1,4)}
    t = {ia0:F(-1), iap:F(1,2), iam:F(1,2)}
    via_dist = -sum((rr*tt*d2(xs[i],xs[k])
                    for i,rr in r.items() for k,tt in t.items()), F(0))/2
    rv = tuple(sum((c*xs[i][k] for i,c in r.items()),F(0)) for k in range(len(xs[0])))
    tv = tuple(sum((c*xs[i][k] for i,c in t.items()),F(0)) for k in range(len(xs[0])))
    require(via_dist == dot(rv,tv), 'distance height identity')
    return via_dist


def polynomial_product(x, y):
    out = [F(0)]*(len(x)+len(y)-1)
    for i,a0 in enumerate(x):
        for k,b0 in enumerate(y):
            out[i+k] += a0*b0
    return out


def sum_poly(x, y):
    n = max(len(x),len(y))
    return [(x[i] if i<len(x) else 0)+(y[i] if i<len(y) else 0) for i in range(n)]


def anchor_check(xs, ys, omega, rows, claimed_det):
    require(len(omega)==len(xs)==len(ys), 'certificate cardinality')
    require(sum(omega)==0, 'signed mass does not cancel')
    for points in [xs,ys]:
        require(all(sum((c*p[k] for c,p in zip(omega,points)),F(0))==0
                    for k in range(3)), 'signed coordinate sum does not cancel')
    residual = sum((c*(sq(x)-sq(y)) for c,x,y in zip(omega,xs,ys)),F(0))
    require(residual==4, 'anchor obstruction residual')
    require(len(rows)==8 and len(set(rows))==8 and all(0<=i<len(xs) for i in rows),
            'minor requires eight distinct valid labels')
    mat = [list(x)+list(y)+[F(1),sq(x)-sq(y)] for x,y in zip(xs,ys)]
    actual = det([mat[i] for i in rows])
    require(actual != 0 and actual == claimed_det, 'nonzero minor mismatch')
    return residual


def run():
    us,vs,xs,ys = fixture()
    require(len(us)==8 and len(vs)==16, 'fixture cardinality')
    require(len(set(xs))==len(set(ys))==24, 'endpoint collisions')
    require(rank([sub(v,xs[0]) for v in xs[1:16]])==3, 'A does not span')
    require(rank([sub(v,xs[16]) for v in xs[17:]])==3, 'B does not span')
    paired = [list(sub(x,xs[0]))+list(sub(y,ys[0])) for x,y in zip(xs[1:],ys[1:])]
    require(rank(paired)==6, 'paired rank')
    pairs = list(combinations(range(24),2))
    losses = [d2(xs[i],xs[k])-d2(ys[i],ys[k]) for i,k in pairs]
    require(min(losses)==0 and sum(t>0 for t in losses)==120, 'pair sign/count')
    require(min(t for t in losses if t>0)==F(1,16), 'strict margin')
    for i,v in enumerate(vs):
        for k,u in enumerate(us):
            require(d2(xs[i],xs[16+k])-d2(ys[i],ys[16+k])==d2(v,p0(u)),
                    'cross loss identity')

    forms = [loss_form(p0((F(t),F(0))),(F(t),F(0))) for t in [-2,-1,0,1,2]]
    fourth = [sum(F(c)*row[i] for c,row in zip([1,-4,6,-4,1],forms)) for i in range(17)]
    target = [F(0)]*17
    target[8],target[16] = F(-48),F(48)
    require(fourth==target, 'formal fourth difference')
    # Both expressions have bidegree at most (2,2); this tensor grid
    # certifies the identity coefficient by coefficient in all11 symbols.
    for u in product(map(F,[-1,0,1]),repeat=2):
        require(blocked_form(p0(u),u)==matched_quadratic(u), 'quadratic identity')
    samples = us[:3]+us[5:]
    eval_matrix = [[1,u[0],u[1],u[0]**2,u[0]*u[1],u[1]**2] for u in samples]
    unisolvent = det(eval_matrix)
    require(unisolvent != 0, 'quadratic unisolvence')

    candidates = []
    probe_a = vs.index((F(5,4),F(-1)))
    probe_b = 17
    for tau,zeta in product([0,1],[1,-1]):
        k = 1-2*tau
        aa,bb = F(k+zeta,2),F(zeta-k,2)
        n = ((aa,-bb),(bb,aa))
        require(aa*aa+bb*bb==1, 'candidate orthogonality')
        zs = [a(v) for v in vs]+[(dot(n[0],u),dot(n[1],u),F(tau)-sq(u)) for u in us]
        lower_bad,upper_bad = [],[]
        for i,k2 in pairs:
            dz = d2(zs[i],zs[k2])
            if dz < d2(ys[i],ys[k2]): lower_bad.append((i,k2))
            if dz > d2(xs[i],xs[k2]): upper_bad.append((i,k2))
        lp = d2(xs[probe_a],xs[probe_b])-d2(zs[probe_a],zs[probe_b])
        if zeta==1:
            require(not lower_bad and not upper_bad, 'endpoint rejected')
            require(zs==(xs if tau==0 else ys), 'wrong surviving endpoint')
        else:
            require(lp==(-F(1,2) if tau==0 else -F(7,16)) and upper_bad,
                    'spurious candidate not excluded')
        candidates.append({'tau':tau,'zeta':zeta,'N':[[str(v) for v in row] for row in n],
                           'lower_violations':len(lower_bad),'upper_violations':len(upper_bad),
                           'probe_loss':str(lp)})

    ia0 = vs.index(p0(us[0])); iap = vs.index(p0(us[1])); iam = vs.index(p0(us[2]))
    omega = [F(0)]*24
    for idx,c in [(ia0,-2),(iap,1),(iam,1),(16,-2),(17,1),(18,1)]: omega[idx]=F(c)
    mat = [list(x)+list(y)+[F(1),sq(x)-sq(y)] for x,y in zip(xs,ys)]
    require(rank([row[:7] for row in mat])==7 and rank(mat)==8, 'augmented ranks')
    minor = []
    for i,row in enumerate(mat):
        if rank([mat[k] for k in minor]+[row])>len(minor): minor.append(i)
        if len(minor)==8: break
    determinant = det([mat[i] for i in minor])
    residual = anchor_check(xs,ys,omega,minor,determinant)

    # The determinant's absolute value survives independent translations,
    # reflections and rotations. These two exact controls change both frames.
    xp = [(-x[1]+3,x[0]-2,x[2]+5) for x in xs]
    yp = [(y[2]-7,-y[1]+4,y[0]+1) for y in ys]
    changed = [list(x)+list(y)+[F(1),sq(x)-sq(y)] for x,y in zip(xp,yp)]
    require(abs(det([changed[i] for i in minor]))==abs(determinant), 'frame invariance')
    require(height(xs,ia0,iap,iam,16)==0 and height(ys,ia0,iap,iam,16)==1,
            'endpoint intrinsic heights')

    # Polynomial in alpha: norm([(1-alpha)I+(1+alpha)J]v)^2.
    aa = [F(1),F(-1)]; bb = [F(1),F(1)]
    norm_poly = sum_poly(polynomial_product(aa,aa),polynomial_product(bb,bb))
    require(norm_poly==[2,0,2], 'R5 polynomial norm identity')
    require(sum_poly([1,0,-2],norm_poly)==[3,0,0], 'R5 scalar cancellation')
    require(1-2*F(5,8)**2==F(7,32), 'R5 k floor')
    require(2*F(1,16)**2==F(1,128), 'R5 displacement ceiling')
    require(F(7,32)/12-F(1,128)==F(1,96), 'R5 barrier margin')

    rejections = 0
    bad = deepcopy(omega); bad[16] += 1
    trials = [(bad,minor,determinant),(omega,minor,-determinant),
              (omega,minor[:-1]+minor[:1],determinant),
              (omega[:-1],minor,determinant)]
    for om,mi,de in trials:
        try: anchor_check(xs,ys,om,mi,de)
        except ValueError: rejections += 1
        else: raise ValueError('corrupted anchor certificate accepted')
    require(rejections==4, 'rejection coverage')

    pins = json.loads((HERE/'INPUTS.json').read_text())
    for pin in pins:
        raw = (HERE.parent.parent/pin['path']).read_bytes()
        require(hashlib.sha256(raw).hexdigest()==pin['sha256'], 'source pin: '+pin['path'])

    weights = [F(i,300) for i in range(1,25)]
    require(sum(weights)==1 and len(set(weights))==24, 'distinct prior control')
    geometry = {'U':[[str(t) for t in u] for u in us],
                'V':[[str(t) for t in v] for v in vs],
                'P':[[str(t) for t in x] for x in xs],
                'Q':[[str(t) for t in y] for y in ys]}
    return {'status':'SCREW_COMPOSITION_OBSTRUCTION_EXACT_PASS',
            'geometry_sha256':hashlib.sha256(json.dumps(geometry,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
            'labels':24,'unordered_pairs':276,'tight_pairs':156,'strict_pairs':120,
            'minimum_positive_loss':'1/16','paired_affine_rank':6,
            'formal_fourth_difference':{'M33':'-48','constant':'48'},
            'quadratic_formal_grid':9,'quadratic_symbol_coefficients':99,
            'quadratic_evaluation_determinant':str(unisolvent),
            'four_candidates':candidates,
            'anchor_coefficients':[[i,str(c)] for i,c in enumerate(omega) if c],
            'anchor_residual':str(residual),'coordinate_rank':7,'augmented_rank':8,
            'minor_rows':minor,'minor_determinant':str(determinant),
            'intrinsic_heights':['0','1'],'R5_margin':'1/96',
            'distinct_prior_denominator':300,'rejected_corruptions':rejections,
            'source_pins':len(pins),
            'scope':'Exact algebra and geometry only; universal proof in PROOF.md; no Gaussian sign.'}


if __name__=='__main__':
    require(sys.argv[1:] in [[],['--emit']], 'usage: verify.py [--emit]')
    record = run()
    if sys.argv[1:]!=['--emit']:
        require(record==json.loads((HERE/'EXPECTED.json').read_text()), 'expected record mismatch')
    print(json.dumps(record,sort_keys=True,indent=2))
