"""exact arbitrary-count completion; full original forms; uniform proof in PROOF.md.

Parent physical recipe/source95 is reused verbatim through probe.construct.
The projections and residual means implement the all-count construction.
Author reuse and exact finite checks do not constitute independent review.
"""
import os
for _name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
              'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[_name] = '1'
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fractions import Fraction as F
from exact import (require, psd_rank, dot, matvec, unit, scale, vecadd,
                   zero, lift, fingerprint, check, family_star)
from probe import construct, whole_lift
import json, time, signal, resource


def psd_or_witness(matrix):
    """Full rational congruence; an actual negative original vector on failure."""
    a = [[F(x) for x in row] for row in matrix]
    n = len(a)
    require(n and all(len(row) == n for row in a), 'whole square PSD input')
    require(all(a[i][j] == a[j][i] for i in range(n) for j in range(n)),
            'whole symmetric PSD input')
    z = [unit(n, i) for i in range(n)]
    rank = 0
    for k in range(n):
        p = a[k][k]
        witness = None
        if p < 0:
            witness = z[k]
        elif p == 0:
            j = next((j for j in range(k + 1, n) if a[k][j]), None)
            if j is not None:
                t = -a[k][j] / (abs(a[j][j]) + 1)
                witness = vecadd(z[k], scale(t, z[j]))
            else:
                continue
        if witness is not None:
            energy = dot(witness, matvec(matrix, witness))
            require(energy < 0, 'negative WHOLE original energy')
            return dict(psd=False, vector=[str(v) for v in witness],
                        energy=str(energy), first_pivot=k)
        rank += 1
        for i in range(k + 1, n):
            z[i] = vecadd(z[i], scale(-a[i][k] / p, z[k]))
        for i in range(k + 1, n):
            for j in range(i, n):
                a[i][j] -= a[i][k] * a[k][j] / p
                a[j][i] = a[i][j]
    return dict(psd=True, rank=rank)


def build(n, h, l, baseline=True):
    require(type(n) is int and 3 <= n <= 6 and type(h) is int and 3 <= h <= 10
            and type(l) is int and 2 <= l < h,
            'literal arbitrary-count domain')
    require(2**n+12*h <= 80, 'unchanged parent original N80 guard before construction')
    p, oldmetric, _, _, parentC, data = construct(n, h)
    q, s = p['q'], int(p['s'])
    if baseline:
        parentfamily = [0] + list(range(1, 2**n))
        marked, private = [], []
        for facet in range(2*h):
            masks = [1 << (n+2*facet), 1 << (n+2*facet+1),
                     3 << (n+2*facet)]
            private.extend(masks)
            marked.extend((1 if facet < h else 2) | mask for mask in masks)
        parentfamily += marked + private
        parent = check(parentfamily, lift(parentC, s), s)
        require(parent['lower_rank'] == p['N'] - 3 and
                parent['upper_rank'] == p['N'] - 1, 'complete original baseline')
        if (n, h) == (3, 4):
            require(parent['matrix_sha256'] ==
                    'c52e14420449867003a80014fd03d5fef4f99d09503258074afc84b57add98b4',
                    'entire source95 baseline M')
    else:
        parent = None
    m = 3*(h+l)
    N = 2*q + 6*(h+l)
    require(N <= 80, 'unchanged literal N80 guard')
    d = data['wi']
    G0 = [row[:d] for row in oldmetric[:d]]
    truncate = lambda v: v[:d]
    old = [truncate(r) for r in data['R'][:data['oldsize']]]
    V = [truncate(r) for r in data['V'][:3*(h+l)]]
    K = vecadd(*(old + V))
    z = scale(F(-1, m+1), K)
    ip = lambda a, b: dot(a, matvec(G0, b))
    require(ip(K, K) == q*(m+1)+9*l*(h-l)-3*h-6*l-1, 'complete retained K norm')
    common2 = F(q*(m+1)+9*l*(h-l)-3*h-6*l-1, (m+1)**2)
    require(ip(z, z) == common2, 'new common norm identity')
    sizes = (h, l)
    means = [F(-(q-1), m+1), F(-(q+3*(h-l)-1), m+1)]
    Bs = [[truncate(v) for v in data['Bs'][0]],
          [truncate(v) for v in data['Bs'][1][:l]]]
    ymean = scale(F(1, l), vecadd(*Bs[1]))
    Bs[1] = [vecadd(v, scale(-1, ymean)) for v in Bs[1]]
    Ts = [[truncate(v) for v in t] for t in data['Ts'][:h+l]]
    scalars, P = [], []
    for group, k in enumerate(sizes):
        require(not any(vecadd(*Bs[group])), 'entire contrast sum')
        for i in range(k):
            require(ip(z, Bs[group][i]) == 0, 'new z orthogonal contrasts')
            for j in range(k):
                require(ip(Bs[group][i], Bs[group][j]) ==
                        F(s, 3)*(int(i == j)-F(1, k)),
                        'ALL recentered contrast Gram entries')
        B2 = F(s*(k-1), 3*k)
        v = means[group]
        a = (1+v)/(2*B2)
        b = -2*a
        c = F(9, 2*s)*(1+v)
        etaL = s-1-common2-a*a*B2-F(2*s, 3)*c*c
        etaF = s-1-common2-b*b*B2-F(2*s, 3*(k-1))*c*c
        pp = -1-common2-a*b*B2
        mu = (2*pp+etaF)/3
        alpha = 2*(2*etaL-pp-etaF)
        beta = etaF-mu
        require(min(mu, alpha, beta) > 0, 'positive proposed residual scalars')
        scalars.append(dict(k=k, v=v, B2=B2, a=a, b=b, c=c,
                            etaL=etaL, etaF=etaF, p=pp, mu=mu,
                            alpha=alpha, beta=beta))
        start = 0 if group == 0 else h
        for i in range(k):
            facet = start+i
            for leaf in range(3):
                require(ip(z, V[3*facet+leaf]) == v,
                        'every original marked-common pairing')
                require(ip(z, Ts[facet][leaf]) == 0,
                        'new z orthogonal ALL retained T directions')
            P.extend(vecadd(z, scale(a, Bs[group][i]),
                            scale(c, Ts[facet][1-leaf])) for leaf in range(2))
            other = vecadd(*(Ts[start+j][2] for j in range(k) if j != i))
            P.append(vecadd(z, scale(b, Bs[group][i]),
                            scale(c/(k-1), other)))
    require(vecadd(*P) == scale(m, z), 'entire new private projection sum')
    mux, muy = scalars[0]['mu'], scalars[1]['mu']
    tau = mux*muy/(h*mux+l*muy)
    offs = [(l*tau-mux)/(h-1), (h*tau-muy)/(l-1)]
    nus = [(h*mux-l*tau)/(h-1), (l*muy-h*tau)/(l-1)]
    require(tau > 0 and min(nus) > 0, 'positive harmonic mean coupling')
    wa, wf = (F(1, 2), F(-1, 2), F(0)), (F(-1, 2), F(-1, 2), F(1))
    W = zero(m)
    for i in range(m):
        fi, ai = divmod(i, 3)
        gi = int(fi >= h)
        for j in range(m):
            fj, aj = divmod(j, 3)
            gj = int(fj >= h)
            v = -tau if gi != gj else scalars[gi]['mu'] if fi == fj else offs[gi]
            if fi == fj:
                v += wa[ai]*wa[aj]*scalars[gi]['alpha']
                v += wf[ai]*wf[aj]*scalars[gi]['beta']
            W[i][j] = v
    require(all(sum(row) == 0 for row in W), 'entire new residual zero sums')
    require(psd_rank(W) == m-1, 'entire residual sole ones kernel')
    dimension = d+m-1
    Gamma = zero(dimension)
    for i in range(d):
        for j in range(d): Gamma[i][j] = G0[i][j]
    for i in range(m-1):
        for j in range(m-1): Gamma[d+i][d+j] = W[i][j]
    extend = lambda v: v+[F(0)]*(m-1)
    residual = [unit(dimension, d+i) for i in range(m-1)]
    residual.append(scale(-1, vecadd(*residual)))
    U = [vecadd(extend(v), r) for v, r in zip(P, residual)]
    rows = [extend(r) for r in old+V]+U
    empty = extend(z)
    require(not any(vecadd(empty, *rows)), 'WHOLE actual empty row sum')
    images = [matvec(Gamma, r) for r in rows]
    C = [[dot(r, im) for im in images] for r in rows]
    Q = whole_lift(C)
    whole = [empty]+rows
    fullimages = [matvec(Gamma, r) for r in whole]
    require(Q == [[dot(r, im) for im in fullimages] for r in whole],
            'EVERY original Q entry equals the full physical Gram')
    require(Q[0][0] == common2, 'actual reconstructed empty norm')
    marked, private = [], []
    for facet in range(h+l):
        masks = [1 << (n+2*facet), 1 << (n+2*facet+1), 3 << (n+2*facet)]
        private.extend(masks)
        marked.extend((1 if facet < h else 2) | mask for mask in masks)
    family = [0] + list(range(1, 2**n)) + marked + private
    require(len(family) == N and family_star(family) == s, 'actual downset/largest star')
    L = [[1+v for v in row] for row in Q]
    M = lift(C, s)
    upper = [[F(i == j)-M[i][j] for j in range(N)] for i in range(N)]
    for i in range(N):
        require(sum(M[i]) == 1, 'EVERY original stochastic row')
        for j in range(N):
            require(M[i][j] == M[j][i], 'EVERY original symmetric entry')
            if family[i] & family[j]:
                require(M[i][j] == 0, 'EVERY original forbidden entry')
    lower_status = psd_or_witness(L)
    upper_status = psd_or_witness(upper)
    core_status = psd_or_witness(C)
    heavy = [F(bool(a & 1)) for a in family[1:]]
    require(not any(matvec(C, heavy)), 'full heavy-star core kernel')
    result = dict(agent='six-downset-1', role='researcher',
        status='EXACT FINITE ORIGINAL CONTROL; uniform statement uses PROOF.md; independently unreviewed',
        n=n, h=h, counts=[h,l], q=q, N=N, s=s, common_norm=str(common2),
        scalar_groups=[{k:str(v) for k,v in g.items()} for g in scalars],
        tau=str(tau), mean_contrasts=[str(v) for v in nus],
        ambient_metric_dimension=dimension, ambient_metric_rank=psd_rank(Gamma),
        full_core=core_status, original_lower=lower_status, original_cap=upper_status,
        matrix_sha256=fingerprint(M), core_sha256=fingerprint(C), baseline=parent,
        checked_all_original_entries=N*N, full_original_support_rows_empty=True,
        physical_actual_empty_identity=True, scalar_completeness_unformalized=True)
    defining = dict(agent='six-downset-1', role='researcher', n=n,h=h,
        family=family, scalars=result['scalar_groups'], tau=str(tau),
        original_M=[[str(v) for v in row] for row in M],
        core_C=[[str(v) for v in row] for row in C],
        physical_metric=[[str(v) for v in row] for row in Gamma],
        all_physical_rows=[[str(v) for v in row] for row in whole])
    return result, defining, C, M, family


def alarm(signum, frame):
    raise TimeoutError('unchanged literal60s guard; unfinished is not absence')


if __name__ == '__main__':
    signal.signal(signal.SIGALRM, alarm)
    signal.alarm(60)
    start = time.monotonic()
    result, defining, C, M, family = build(3, 5, 2)
    folder = Path(__file__).resolve().parent
    packed = json.dumps(defining, indent=2)+'\n'
    require(len(packed.encode()) <= 32*1024*1024, 'unchanged32MiB packing guard')
    (folder/'UNRESTRICTED-FIRST-MATRIX.json').write_text(packed)
    (folder/'UNRESTRICTED-FIRST-RESULT.json').write_text(json.dumps(result, indent=2)+'\n')
    result['execution'] = dict(seconds=time.monotonic()-start,
        peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        optimized=not __debug__, native_threads_one=True,
        actual_numerical_matrices_all_rational=True)
    signal.alarm(0)
    print(json.dumps(result), flush=True)
