"""PRIVATE complete original inverse, projections and repair endpoints.

Two literal controls only: n4,h2 and n4,h3. The uniform classification is
the ordinary proof in PROOF-PRIVATE.md, not an extrapolation of these cases.
"""
import os
for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[name] = '1'
from pathlib import Path
import sys, json, signal, time, resource, argparse
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fractions import Fraction as F
from exact import require, unit, vecadd, scale, dot, matvec, psd_rank, fingerprint, family_star
from linear import solve
from probe import construct, whole_lift
from energies import energies


class Quadratic:
    """Exact coefficient pair in QQ[e]/(e^2-radicand), no float roots."""
    radicand = None

    def __init__(self, a=0, b=0):
        if isinstance(a, Quadratic):
            self.a, self.b = a.a, a.b
        else:
            self.a, self.b = F(a), F(b)

    def __add__(self, other):
        z = Quadratic(other); return Quadratic(self.a + z.a, self.b + z.b)
    __radd__ = __add__
    def __neg__(self):
        return Quadratic(-self.a, -self.b)
    def __sub__(self, other):
        return self + -Quadratic(other)
    def __rsub__(self, other):
        return Quadratic(other) + -self
    def __mul__(self, other):
        z = Quadratic(other)
        return Quadratic(self.a*z.a + self.b*z.b*self.radicand, self.a*z.b + self.b*z.a)
    __rmul__ = __mul__
    def __eq__(self, other):
        z = Quadratic(other); return self.a == z.a and self.b == z.b
    def __str__(self):
        return str(self.a) + '+' + str(self.b) + '*sqrt(' + str(self.radicand) + ')'


def check(n, h):
    p, metric, frame, floor1, C0, vectors = construct(n, h)
    q, N, s = p['q'], p['N'], p['s']; size = N - 4
    Q0 = whole_lift(C0)
    P = [[F(i == j) - F(1, N) for j in range(N)] for i in range(N)]
    K0 = [[N*P[i][j] - Q0[i][j] for j in range(N)] for i in range(N)]
    gauge = [[K0[i][j] + F(1, N) for j in range(N)] for i in range(N)]
    require(psd_rank(gauge) == N, 'entire original mean-gauged inverse is positive')
    private = 2*q + 6*h
    u = vecadd(*(unit(N, i) for i in range(private, private+3)), scale(-3, unit(N, 0)))
    v = vecadd(unit(N, N-1), scale(-1, unit(N, 0)))
    require((sum(u), sum(v), dot(u, u), dot(v, v), dot(u, v)) == (0, 0, 12, 2, 3), 'actual empty and three free pairs')
    iu, iv = solve(gauge, u), solve(gauge, v)
    require(sum(iu) == sum(iv) == 0 and matvec(K0, iu) == u and matvec(K0, iv) == v,
            'both ENTIRE original inverse equations including mean')
    A, B, C = dot(u, iu), dot(v, iv), dot(u, iv)
    require(A > 0 and B > 0 and A*B > C*C, 'independent original inverse energy Gram')
    compact = energies(q, h)
    require((A, B, C) == tuple(compact[k] for k in ('A', 'B', 'D')), 'all three original inverse energies equal compact formulas')
    if (n, h) == (4, 2):
        require((A, B, C) == (F(37761381802437, 115811625136160), F(8583511214872564211, 138219669048880189920), F(67, 928)),
                'entire useful prior finite inverse baseline, not new research')

    # Reconstruct every physical projection directly from literal original rows.
    rows = [vectors['common']] + vectors['R']
    ru = vecadd(*(scale(z, r) for z, r in zip(u, rows)))
    rv = vecadd(*(scale(z, r) for z, r in zip(v, rows)))
    TS = [vecadd(t[0], t[1], scale(-2, t[2])) for t in vectors['Ts']]
    W = [vecadd(z, scale(-1, r)) for z, r in zip(vectors['U'], vectors['P'])]
    means = [scale(F(1, 3), vecadd(*W[3*i:3*i+3])) for i in range(2*h)]
    WF = [vecadd(W[3*i+2], scale(-1, means[i])) for i in range(2*h)]
    def profile(values, group, i):
        return vecadd(values[group*h+i], scale(-F(1, h), vecadd(*values[group*h:(group+1)*h])))
    oddmean = vecadd(*means[:h], scale(-1, vecadd(*means[h:])))
    evenTS, evenWF = vecadd(*TS), vecadd(*WF)
    oddTS = vecadd(*TS[:h], scale(-1, vecadd(*TS[h:])))
    oddWF = vecadd(*WF[:h], scale(-1, vecadd(*WF[h:])))
    c, b = p['c'], p['b']
    proposed_u = vecadd(scale(c*h/(3*(h-1)), profile(TS, 0, 0)),
                        scale(3, profile(means, 0, 0)), scale(F(3, 2*h), oddmean))
    proposed_v = vecadd(scale(b, vectors['Bs'][1][-1]), scale(c/(3*(h-1)), profile(TS, 1, h-1)),
                        profile(WF, 1, h-1), profile(means, 1, h-1),
                        scale(-c/(6*h), evenTS), scale(F(1, 2*h), evenWF),
                        scale(c/(6*h), oddTS), scale(-F(1, 2*h), oddWF), scale(-F(1, 2*h), oddmean))
    require(ru == proposed_u and rv == proposed_v, 'EVERY physical coordinate of both original projections')
    physical_cap = [[N*metric[i][j] - frame[i][j] for j in range(size)] for i in range(size)]
    pu = solve(physical_cap, matvec(metric, ru)); pv = solve(physical_cap, matvec(metric, rv))
    gu, gv = matvec(metric, pu), matvec(metric, pv)
    wood_u = [(u[i] + dot(rows[i], gu))/N for i in range(N)]
    wood_v = [(v[i] + dot(rows[i], gv))/N for i in range(N)]
    require(wood_u == iu and wood_v == iv, 'ENTIRE original Woodbury inverse, not only scalar energies')

    oldsize = 2*q - 1; offset = oldsize + 6*h; last = N-2
    keep = [i for i in range(N-1) if i not in (0, 1, last)]
    principal = [[C0[i][j] for j in keep] for i in keep]
    require(psd_rank(principal) == size, 'original retained principal strictly positive')
    z = [-F(6*h, 6*h+1)*(1-int(bool((i+1)&1))-int(bool((i+1)&2))) if i < oldsize
         else F(-1) if i >= offset else F(0) for i in keep]
    r = [F(offset <= i < offset+3) for i in keep]
    rinv = solve(principal, r); kappa = dot(r, rinv)
    require(kappa == compact['kappa'] and dot(r, z) == -3, 'ENTIRE original Schur inverse scalar and overlap')
    lower_end = 6/kappa; delta0 = 1/(4*(8+kappa))
    private_masks = []; marked_masks = []
    for facet in range(2*h):
        masks = [1 << (n+2*facet), 1 << (n+2*facet+1), 3 << (n+2*facet)]
        private_masks.extend(masks); marked_masks.extend((1 if facet < h else 2)|a for a in masks)
    family = [0] + list(range(1, 2**n)) + marked_masks + private_masks
    require(len(family) == N and family_star(family) == s, 'actual full downset and star size')
    centered = [[F(bool(a & mark)) - s/N for a in family] for mark in (1, 2)]
    def matrix_at(delta):
        Q = [[Q0[i][j] + delta*(u[i]*v[j]+v[i]*u[j]) for j in range(N)] for i in range(N)]
        L = [[1+z for z in row] for row in Q]
        K = [[N*P[i][j]-Q[i][j] for j in range(N)] for i in range(N)]
        M = [[(L[i][j]-s*int(i == j))/(N-s) for j in range(N)] for i in range(N)]
        for i in range(N):
            require(sum(M[i]) == 1, 'ALL original row sums')
            for j in range(N):
                require(M[i][j] == M[j][i], 'ALL original symmetric positions')
                if family[i] & family[j]:
                    require(M[i][j] == 0, 'ALL original intersection zeros')
        require(Q[0][0] == Q0[0][0] + 6*delta and all(Q[i][i] == Q0[i][i] for i in range(1,N)), 'actual empty loop and unchanged nonempty diagonals')
        for kernel in centered:
            require(not any(matvec(L, kernel)), 'both ENTIRE centered-star kernels')
        return L, K, M
    controls = []
    for delta, lower_rank, cap_rank in ((F(0), N-3, N-1), (delta0, N-2, N-1), (lower_end, N-3, None)):
        L, K, M = matrix_at(delta)
        require(psd_rank(L) == lower_rank, 'whole original lower endpoint/interior rank')
        if cap_rank is not None:
            require(psd_rank(K) == cap_rank, 'whole original cap seed/interior rank')
        controls.append(dict(delta=str(delta), lower_rank=lower_rank, cap_rank=cap_rank, matrix_sha256=fingerprint(M)))
    for delta in (-delta0, lower_end+delta0):
        L, K, M = matrix_at(delta)
        core = [F(0)]*(N-1)
        for i, val in zip(keep, vecadd(scale(-1, z), scale(-delta, rinv))):
            core[i] = val
        core[last] = F(1)
        original = [F(0)] + core
        original = [x-sum(original)/N for x in original]
        scalar = 6*delta-kappa*delta*delta
        require(sum(original) == 0 and dot(original, matvec(L, original)) == scalar and scalar < 0,
                'ENTIRE original negative lower witness beyond either endpoint')
        controls.append(dict(delta=str(delta), lower_negative_energy=str(scalar), full_negative_witness=True))

    # Isolate the positive cap root rationally, using its exact determinant.
    determinant = A*B-C*C
    def cap_polynomial(delta):
        return 1-2*delta*C-delta*delta*determinant
    lo, hi = F(0), F(1)
    for step in range(32):
        if cap_polynomial(hi) < 0:
            break
        hi *= 2
    else:
        raise ValueError('unchanged32-step literal root bracketing guard')
    for step in range(16):
        midpoint = (lo+hi)/2
        if cap_polynomial(midpoint) > 0:
            lo = midpoint
        else:
            hi = midpoint
    require(lo > 0 and cap_polynomial(lo) > 0 and cap_polynomial(hi) < 0, 'strict rational cap endpoint isolation')
    Llo, Klo, ignored = matrix_at(lo); Lhi, Khi, ignored = matrix_at(hi)
    require(psd_rank(Klo) == N-1, 'ENTIRE original cap immediately inside endpoint')
    g00 = A-2*hi*A*C; g01 = C-hi*(A*B+C*C)
    g11 = B-2*hi*B*C
    require(g00*g11-g01*g01 == determinant*cap_polynomial(hi) < 0, 'full inverse span determinant is negative')
    if g00 < 0:
        negative = iu
    elif g00 > 0:
        negative = vecadd(scale(-g01/g00, iu), iv)
    else:
        require(g01 != 0, 'nonzero crossed negative form')
        t = -F(1 if g01 > 0 else -1) * (abs(g11)+1)/(2*abs(g01))
        negative = vecadd(scale(t, iu), iv)
    require(sum(negative) == 0 and dot(negative, matvec(Khi, negative)) < 0,
            'ENTIRE original negative cap witness immediately beyond endpoint')

    # Both algebraic endpoints: check every original null equation over QQ[e].
    Quadratic.radicand = A*B
    endpoint_checks = []
    for sign in (-1, 1):
        delta = Quadratic(-C/determinant, F(sign)/determinant)
        null = [Quadratic(B*x, sign*y) for x, y in zip(iu, iv)]
        require(sum(null) == 0, 'whole endpoint null vector remains in one-perp')
        crossed_v = dot(v, null); crossed_u = dot(u, null)
        image = [dot(K0[i], null) - delta*(u[i]*crossed_v+v[i]*crossed_u) for i in range(N)]
        require(all(z == 0 for z in image), 'EVERY original algebraic cap endpoint null equation')
        endpoint_checks.append(dict(sign=sign, all_original_null_equations=N, empty_retained=True,
                                    delta=str(delta), null_vector_sha256=fingerprint([null])))
    gap = kappa/6-C
    cap_binds = gap <= 0 or A*B > gap*gap
    return dict(n=n, h=h, q=q, N=N, full_original_entries=N*N, complete_physical_coordinates=2*size,
                all_original_inverse_equations=2*N, entire_Woodbury_equalities=2*N,
                original_energies={key:str(value) for key,value in [('A',A),('B',B),('C',C),('kappa',kappa),('AB_minus_C_squared',determinant)]},
                compact_energies_exact=True, original_projections_exact=True,
                whole_empty_star_support_and_rows=True, lower_rank_and_negative_controls=controls,
                cap_endpoint_isolation=[str(lo),str(hi)], full_cap_inside_rank=N-1,
                full_cap_outside_negative_witness=True, both_algebraic_endpoint_checks=endpoint_checks,
                cap_endpoint_strictly_below_lower_for_THIS_fixture=cap_binds,
                endpoint_cap_rank_source='Ordinary whole rank-two congruence, not an unperformed algebraic PSD elimination',
                status='EXACT original finite control only; uniform theorem uses written full-space proof')


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--h',type=int,required=True); args=ap.parse_args()
    require(args.h in (2,3), 'only two distinct literal original controls')
    state=Path('/scratch/research-team-sol61-six-20260929/state')
    require(not any((state/n).exists() for n in ('PAUSED','PAUSED.json','HANDOVER','HANDOVER.json')), 'operational barrier')
    def alarm(a,b):
        raise TimeoutError('unchanged60s original inverse/endpoint control guard')
    signal.signal(signal.SIGALRM,alarm); signal.alarm(60); started=time.monotonic()
    result=check(4,args.h); signal.alarm(0)
    out=dict(agent='six-downset-1',role='researcher',result=result,seconds=time.monotonic()-started,
             peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,optimized=sys.flags.optimize)
    (Path(__file__).resolve().parent/'work'/f'original-n4-h{args.h}-O{sys.flags.optimize}.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='result'} | {k:v for k,v in result.items() if k not in ('lower_rank_and_negative_controls','both_algebraic_endpoint_checks')}),flush=True)


if __name__=='__main__':
    main()
