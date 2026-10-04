"""Three-mark rational original-row control; ordinary uniform theorem in PROOF.md.

Author six-downset-1 / researcher. Exact/linear/probe are copied verbatim
from public source7fa, credited in CREDITS.json. This constructor is new.
No two-mark cap, rank or residual coupling is inherited by deletion.
"""
import os
for _name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
              'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[_name] = '1'
from fractions import Fraction as F
from pathlib import Path
import json, time, resource, signal
from exact import require, zero, unit, vecadd, scale, dot, matvec, psd_rank, lift, check, fingerprint, family_star
from probe import construct, whole_lift


def psd_or_witness(matrix):
    """Credited rational congruence algorithm from source7fa/completion_harmonic.

    A failed candidate yields an original-coordinate negative vector.
    A timeout is incompleteness, never nonexistence.
    """
    a = [[F(x) for x in row] for row in matrix]
    n = len(a)
    require(n and all(len(row) == n for row in a), 'whole square PSD input')
    require(all(a[i][j] == a[j][i] for i in range(n) for j in range(n)),
            'whole symmetric PSD input')
    z = [unit(n, i) for i in range(n)]
    rank = 0
    for k in range(n):
        pivot = a[k][k]
        witness = None
        if pivot < 0:
            witness = z[k]
        elif pivot == 0:
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
            z[i] = vecadd(z[i], scale(-a[i][k] / pivot, z[k]))
        for i in range(k + 1, n):
            for j in range(i, n):
                a[i][j] -= a[i][k] * a[k][j] / pivot
                a[j][i] = a[i][j]
    return dict(psd=True, rank=rank)


def parameters(q, h, l):
    q, h, l = F(q), F(h), F(l)
    require(q >= 4 and h > l >= 2, 'three-mark exact candidate domain')
    s = q + 3*h
    sizes = (h, l, l)
    m = 3*sum(sizes)
    ell = m + 1
    c0 = (q*ell + 18*l*(h-l) - 3*h - 12*l - 1)/ell**2
    groups = []
    for k, vg in zip(sizes, (-(q-1)/ell,
            -(q+3*(h-l)-1)/ell, -(q+3*(h-l)-1)/ell)):
        B2 = s*(k-1)/(3*k)
        a = (1+vg)/(2*B2)
        b = -2*a
        c = 9*(1+vg)/(2*s)
        etaL = s-1-c0-a*a*B2-2*s*c*c/3
        etaF = s-1-c0-b*b*B2-2*s*c*c/(3*(k-1))
        pair = -1-c0-a*b*B2
        mu = (2*pair+etaF)/3
        alpha = 2*(2*etaL-pair-etaF)
        beta = etaF-mu
        require(mu+alpha/4+beta/4 == etaL and mu+beta == etaF
                and mu-beta/2 == pair, 'residual algebraic diagonal/support identities')
        groups.append(dict(k=k, v=vg, B2=B2, a=a, b=b, c=c,
                           etaL=etaL, etaF=etaF, pair=pair,
                           mu=mu, alpha=alpha, beta=beta))
    meanS = sum(g['k']*g['mu'] for g in groups)
    require(meanS > 0 and min(g[key] for g in groups
            for key in ('mu', 'alpha', 'beta')) > 0,
            'positive proposed three-group residual scalars')
    for g in groups:
        g['off'] = -g['k']*g['mu']**2/(meanS*(g['k']-1))
        g['nu'] = g['mu']-g['off']
    return dict(q=q, h=h, l=l, s=s, sizes=sizes, m=m, ell=ell,
                N=2*q+2*m, D=3*h, c0=c0, groups=groups, meanS=meanS)


def baseline(n, h):
    """Useful exact public old-metric/balanced TWO-mark reproduction only."""
    require(2**n+12*h <= 80, 'N80 parent guard BEFORE parent construction')
    p, metric, _, _, C, data = construct(n, h)
    marked, private = [], []
    for facet in range(2*h):
        masks = [1 << (n+2*facet), 1 << (n+2*facet+1), 3 << (n+2*facet)]
        private.extend(masks)
        marked.extend((1 if facet < h else 2) | mask for mask in masks)
    family = [0]+list(range(1, 2**n))+marked+private
    record = check(family, lift(C, int(p['s'])), int(p['s']))
    require(record['lower_rank'] == int(p['N'])-3
            and record['upper_rank'] == int(p['N'])-1,
            'entire credited TWO-mark baseline')
    return record, [row[:data['oldsize']] for row in metric[:data['oldsize']]]


def build(n=3, h=3, l=2, reproduce_baseline=True):
    require(type(n) is int and 3 <= n <= 6 and type(h) is int
            and 3 <= h <= 10 and type(l) is int and 2 <= l < h,
            'unchanged literal three-mark domain')
    q = 2**(n-1)
    p = parameters(q, h, l)
    N, s, m, ell, D = (int(p[k]) for k in ('N','s','m','ell','D'))
    require(N <= 80, 'unchanged literal original N80 guard')
    parent, parentold = baseline(n, h) if reproduce_baseline else (None, None)
    sizes = (h, l, l)
    marks = (1, 2, 4)
    starts = (0, h, h+l)
    oldsize = 2*q-1
    d = oldsize+(h-1)+2*l+2*(h+2*l)
    require(d == 2*q+m-2, 'new retained old/marked dimension')
    G0 = zero(d)
    for i in range(oldsize):
        for j in range(oldsize):
            G0[i][j] = F(s*(i==j)+(q-D)*((i+1)^(j+1)==oldsize)-1)
    if parentold is not None:
        require(parentold == [row[:oldsize] for row in G0[:oldsize]],
                'EVERY credited old cube Gram entry reproduced')
    e = lambda i: unit(d, i)
    old = [e(i) for i in range(oldsize)]
    H = [scale(-1, vecadd(*(old[i] for i in range(oldsize)
                            if (i+1)&mark))) for mark in marks]
    B, offset = [], oldsize
    for group, k in enumerate(sizes):
        width = k-1 if group == 0 else k
        for i in range(width):
            for j in range(width):
                G0[offset+i][offset+j] = F(s, 3)*(F(i==j)-F(1,h))
        bs = [e(offset+i) for i in range(width)]
        if group == 0:
            bs.append(scale(-1, vecadd(*bs)))
        B.append(bs)
        offset += width
    T = []
    for facet in range(h+2*l):
        G0[offset][offset] = G0[offset+1][offset+1] = F(2*s, 3)
        G0[offset][offset+1] = G0[offset+1][offset] = F(-s, 3)
        T.append([e(offset), e(offset+1),
                  scale(-1, vecadd(e(offset), e(offset+1)))])
        offset += 2
    require(offset == d and psd_rank(G0) == d, 'ENTIRE new retained metric PD')
    ip = lambda x,y: dot(x, matvec(G0,y))
    V = []
    for group, k in enumerate(sizes):
        for i in range(k):
            facet = starts[group]+i
            V.extend(vecadd(scale(F(1,D),H[group]), B[group][i], t)
                     for t in T[facet])
    K = vecadd(*(old+V))
    z = scale(F(-1,ell), K)
    require(ip(K,K) == q*ell+18*l*(h-l)-3*h-12*l-1,
            'NEW entire retained K norm')
    require(ip(z,z) == p['c0'], 'NEW actual empty/common norm')
    bmeans = [scale(F(1,k), vecadd(*bs)) for k,bs in zip(sizes,B)]
    bc = [[vecadd(b,scale(-1,mean)) for b in bs]
          for bs,mean in zip(B,bmeans)]
    projections = []
    for group,g in enumerate(p['groups']):
        k = sizes[group]
        require(not any(vecadd(*bc[group])), 'entire new B-contrast sum')
        for i in range(k):
            require(ip(z,bc[group][i]) == 0, 'new common orthogonal to B contrast')
            for j in range(k):
                require(ip(bc[group][i],bc[group][j])
                        == F(s,3)*(F(i==j)-F(1,k)), 'ALL B contrast Gram')
            facet = starts[group]+i
            for leaf in range(3):
                require(ip(z,V[3*facet+leaf]) == g['v'],
                        'EVERY new marked-common pairing')
                require(ip(z,T[facet][leaf]) == 0, 'common orthogonal to retained T')
            projections.extend(vecadd(z,scale(g['a'],bc[group][i]),
                scale(g['c'],T[facet][1-leaf])) for leaf in range(2))
            others = vecadd(*(T[starts[group]+j][2] for j in range(k) if j != i))
            projections.append(vecadd(z,scale(g['b'],bc[group][i]),
                                      scale(g['c']/(k-1),others)))
    require(vecadd(*projections) == scale(m,z), 'ENTIRE three-mark private projection sum')
    facetgroups = [g for g,k in enumerate(sizes) for _ in range(k)]
    mean = zero(h+2*l)
    for i,gi in enumerate(facetgroups):
        g = p['groups'][gi]
        for j,gj in enumerate(facetgroups):
            mean[i][j] = (g['mu'] if i==j else g['off'] if gi==gj
                          else -g['mu']*p['groups'][gj]['mu']/p['meanS'])
    require(all(sum(row)==0 for row in mean), 'new THREE-group mean row sums')
    require(psd_rank(mean)==h+2*l-1, 'new residual mean sole ones kernel')
    wa,wf = (F(1,2),F(-1,2),F(0)), (F(-1,2),F(-1,2),F(1))
    W = zero(m)
    for i in range(m):
        fi,ai = divmod(i,3)
        g = p['groups'][facetgroups[fi]]
        for j in range(m):
            fj,aj = divmod(j,3)
            W[i][j] = mean[fi][fj]
            if fi==fj:
                W[i][j] += wa[ai]*wa[aj]*g['alpha']+wf[ai]*wf[aj]*g['beta']
    require(all(sum(row)==0 for row in W) and psd_rank(W)==m-1,
            'new whole private residual sole ones kernel')
    dimension = d+m-1
    require(dimension == N-3, 'candidate WHOLE physical dimension')
    metric = zero(dimension)
    for i in range(d):
        for j in range(d): metric[i][j] = G0[i][j]
    for i in range(m-1):
        for j in range(m-1): metric[d+i][d+j] = W[i][j]
    extend = lambda v: v+[F(0)]*(m-1)
    wr = [unit(dimension,d+i) for i in range(m-1)]
    wr.append(scale(-1,vecadd(*wr)))
    U = [vecadd(extend(v),r) for v,r in zip(projections,wr)]
    proper = [extend(v) for v in old+V]+U
    rows = [extend(z)]+proper
    require(not any(vecadd(*rows)), 'ENTIRE actual empty negative row-sum lift')
    images = [matvec(metric,row) for row in rows]
    Q = [[dot(row,image) for image in images] for row in rows]
    C = [row[1:] for row in Q[1:]]
    require(Q == whole_lift(C) and Q[0][0]==p['c0'],
            'EVERY original lifted Gram position incl empty')
    marked,private = [],[]
    for facet,gi in enumerate(facetgroups):
        masks = [1 << (n+2*facet), 1 << (n+2*facet+1), 3 << (n+2*facet)]
        private.extend(masks)
        marked.extend(marks[gi]|mask for mask in masks)
    family = [0]+list(range(1,2**n))+marked+private
    require(len(family)==N and family_star(family)==s, 'new actual downset/max star')
    point_stars = [sum(bool(a&(1<<i)) for a in family) for i in range(n+2*(h+2*l))]
    require(point_stars[:3] == [s,q+3*l,q+3*l]
            and point_stars.count(s)==1, 'new unique heavy maximum star')
    M = lift(C,s)
    L = [[s*F(i==j)+(N-s)*M[i][j] for j in range(N)] for i in range(N)]
    cap = [[N*F(i==j)-L[i][j] for j in range(N)] for i in range(N)]
    P = [[F(i==j)-F(1,N) for j in range(N)] for i in range(N)]
    floorone = [[(N-1)*P[i][j]-Q[i][j] for j in range(N)] for i in range(N)]
    support_positions = 0
    for i in range(N):
        require(sum(M[i])==1, 'EVERY new original stochastic row')
        for j in range(N):
            require(M[i][j]==M[j][i], 'EVERY new original symmetric position')
            require(L[i][j]==1+Q[i][j], 'EVERY original lower endpoint identity')
            if family[i]&family[j]:
                support_positions += 1
                require(M[i][j]==0 and C[i-1][j-1]==(s-1 if i==j else -1),
                        'EVERY original support/norm equation')
    heavy = [F(bool(a&1)) for a in family[1:]]
    rho = [F(m,ell)]*(oldsize+m)+[F(1)]*m
    require(not any(matvec(C,heavy)) and not any(matvec(C,rho)),
            'ENTIRE two candidate new core relations')
    core = psd_or_witness(C)
    lower = psd_or_witness(L)
    upper = psd_or_witness(cap)
    floor_status = psd_or_witness(floorone)
    physical_frame = [[sum(image[i]*image[j] for image in images)
                       for j in range(dimension)] for i in range(dimension)]
    physical_cap = [[(N-1)*metric[i][j]-physical_frame[i][j]
                     for j in range(dimension)] for i in range(dimension)]
    physical_status = psd_or_witness(physical_cap)
    require(core['psd'] and core['rank']==dimension and psd_rank(metric)==dimension,
            'new original rows span ENTIRE positive physical metric')
    require(lower['psd'] and lower['rank']==N-2,
            'new seed full lower rank')
    record = dict(agent='six-downset-1',role='researcher',status='EXACT FINITE THREE-MARK ORIGINAL CONTROL; generic ordinary proof in PROOF.md; unformalized/unreviewed',
        n=n,counts=[h,l,l],q=q,N=N,s=s,m=m,ell=ell,
        common_norm=str(p['c0']),point_stars=point_stars,
        baseline_two_mark=parent,baseline_transports_new_cap=False,
        scalar_groups=[{key:str(value) for key,value in g.items()} for g in p['groups']],
        meanS=str(p['meanS']),mean_rank=h+2*l-1,
        physical_dimension=dimension,physical_rank=dimension,
        full_core=core,original_lower=lower,original_cap=upper,
        original_cap_floor_one=floor_status,whole_physical_cap_floor_one=physical_status,
        checked_original_positions=N*N,checked_support_positions=support_positions,
        all_actual_empty_equations_checked=True,all_original_rows_spanned=True,
        M_sha256=fingerprint(M),C_sha256=fingerprint(C),
        metric_sha256=fingerprint(metric),frame_sha256=fingerprint(physical_frame))
    defining = dict(agent='six-downset-1',role='researcher',private=True,
        n=n,h=h,l=l,family=family,parameters=p,original_M=M,core_C=C,
        physical_metric=metric,all_physical_rows=rows,
        physical_frame=physical_frame,whole_physical_cap=physical_cap,
        projected_private=[extend(v) for v in projections],
        residual_mean_Gram=mean,record=record)
    return record,defining


def alarm(signum,frame):
    raise TimeoutError('unchanged literal60s guard; incomplete is not absence')


if __name__ == '__main__':
    signal.signal(signal.SIGALRM,alarm)
    signal.alarm(60)
    start = time.monotonic()
    result,defining = build(3,3,2)
    folder = Path(__file__).resolve().parent
    packed = json.dumps(defining,indent=2,default=str)+'\n'
    require(len(packed.encode())<=32*1024*1024, 'unchanged32MiB packing guard')
    (folder/'THREE-MARK-FIRST-MATRIX.json').write_text(packed)
    (folder/'THREE-MARK-FIRST-RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    result['execution'] = dict(seconds=time.monotonic()-start,
        peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        optimized=not __debug__,one_mathematical_child=True,native_threads_one=True)
    signal.alarm(0)
    print(json.dumps(result),flush=True)
