"""first original asymmetric cap at greatest lower rank, if verified."""
from pathlib import Path
from fractions import Fraction as F
import json, time, signal, resource
from completion_harmonic import build, psd_or_witness, alarm
from exact import (require, psd_rank, dot, matvec, vecadd, scale, lift,
                   fingerprint, check)
from probe import whole_lift
from linear import solve


def repair(n, h):
    seed, defining, C, M, family = build(n, h)
    N, s = seed['N'], seed['s']
    require(seed['full_core'] == dict(psd=True, rank=N-3),
            'full new core rank')
    require(seed['original_lower'] == dict(psd=True, rank=N-2),
            'full new seed lower rank')
    require(seed['original_cap'] == dict(psd=True, rank=N-1),
            'full new seed cap rank')
    Q = whole_lift(C)
    P0 = [[F(i == j)-F(1, N) for j in range(N)] for i in range(N)]
    floor1 = [[(N-1)*P0[i][j]-Q[i][j] for j in range(N)] for i in range(N)]
    floor1_status = psd_or_witness(floor1)
    require(floor1_status == dict(psd=True, rank=N-1),
            'ALL ORIGINAL seed scaled cap floor1')
    m = 6*h-3
    oldsize = 2**n-1
    offset = oldsize+m
    last = N-2
    keep = [i for i in range(N-1) if i not in (0, last)]
    require(family[1] == 1 and family[last+1] & 3 == 0,
            'deleted old heavy singleton and private full')
    A = [[C[i][j] for j in keep] for i in keep]
    require(psd_rank(A) == N-3, 'entire deleted original principal PD')
    r = [F(1) if i >= offset else F(m, m+1) for i in range(N-1)]
    heavy = [F(bool(a & 1)) for a in family[1:]]
    require(not any(matvec(C, r)) and not any(matvec(C, heavy)),
            'entire TWO original seed kernel vectors')
    z = [-r[i]+F(m, m+1)*heavy[i] for i in keep]
    b0 = [C[i][last] for i in keep]
    require(matvec(A, z) == b0 and dot(z, b0) == s-1,
            'ALL original removed-column reconstruction equations')
    targets = list(range(offset, offset+3))
    require(all(not (family[i+1] & family[last+1]) for i in targets),
            'three actual FREE private pairs')
    trade = [F(i in targets) for i in keep]
    inverse = solve(A, trade)
    kappa = dot(trade, inverse)
    require(kappa > 0 and matvec(A, inverse) == trade and dot(trade, z) == -3,
            'ALL inverse equations, positive energy and overlap')
    nx,ny=map(F,seed['mean_contrasts'])
    tau=F(seed['tau']);betay=F(seed['scalar_groups'][1]['beta'])
    closed_kappa=F(h-1,h)/nx+F(h-2,h-1)/ny+F(1,h*(h-1))/tau+4/betay
    require(kappa==closed_kappa, 'whole inverse equals new explicit residual-dual formula')
    delta = F(1)/(4*(8+kappa))
    bb = vecadd(b0, scale(delta, trade))
    zz = vecadd(z, scale(delta, inverse))
    schur = 6*delta-kappa*delta*delta
    require(matvec(A, zz) == bb and s-1-dot(bb, zz) == schur and schur > 0,
            'ENTIRE original Schur repair with positive residual')
    sharp = [row[:] for row in C]
    for i in targets:
        sharp[i][last] += delta
        sharp[last][i] += delta
    require(not any(matvec(sharp, heavy)), 'whole forced heavy-star kernel retained')
    output = lift(sharp, s)
    final = check(family, output, s)
    require(psd_rank(sharp) == N-2 and final['lower_rank'] == N-1
            and final['upper_rank'] == N-1, 'both greatest original ranks')
    floor = 1-8*delta
    require(floor > F(3,4), 'strict original scaled upper gap')
    QR = whole_lift(sharp)
    repaired_floor = [[(N-floor)*P0[i][j]-QR[i][j] for j in range(N)]
                      for i in range(N)]
    require(psd_rank(repaired_floor) == N-1, 'ALL ORIGINAL repaired upper margin')
    require(QR[0][0] == Q[0][0]+6*delta, 'actual repaired empty norm change')
    require(all(sum(row) == 0 for row in QR), 'every repaired original Gram row')
    result = dict(agent='six-downset-1', role='researcher',
        status='EXACT LITERAL asymmetric completion and cap repair; finite control; uniform statement uses PROOF.md and coefficient certificate',
        n=n,h=h,counts=[h,h-1],N=N,s=s,seed=seed,
        seed_floor1=floor1_status, final=final,
        deleted_principal=N-3, every_inverse_equation=True,
        kappa=str(kappa),closed_kappa_verified=True,delta=str(delta),schur=str(schur),scaled_cap_floor=str(floor),
        repaired_empty_norm=str(QR[0][0]),forced_heavy_star=True,
        max_rank_bound='Actual unique largest star forces lower rank<=N-1; constant forces cap<=N-1',
        all_original_entries=N*N, full_original_support_empty_metric_retained=True,
        ordinary_bridges_unformalized=True, independent_review=False)
    certificate = dict(agent='six-downset-1',role='researcher',n=n,h=h,
        family=family,delta=str(delta),kappa=str(kappa),schur=str(schur),
        seed_matrix_sha256=seed['matrix_sha256'],
        changed_unordered_nonempty_pairs=[[i,last] for i in targets],
        deleted_principal_indices=keep, removed_column_coefficients=[str(v) for v in z],
        inverse_vector=[str(v) for v in inverse],
        core_seed=[[str(v) for v in row] for row in C],
        core_repaired=[[str(v) for v in row] for row in sharp],
        original_repaired_M=[[str(v) for v in row] for row in output])
    return result, certificate


if __name__ == '__main__':
    signal.signal(signal.SIGALRM, alarm);signal.alarm(60)
    start=time.monotonic()
    result,certificate=repair(4,3)
    folder=Path.cwd()
    packed=json.dumps(certificate,indent=2)+'\n'
    require(len(packed.encode()) <= 32*1024*1024, 'unchanged32MiB packing guard')
    (folder/'HARMONIC-FIRST-REPAIR.json').write_text(packed)
    (folder/'HARMONIC-FIRST-REPAIR-RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    result['execution']=dict(seconds=time.monotonic()-start,
        peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        optimized=not __debug__, native_threads_one=True)
    signal.alarm(0)
    print(json.dumps(result),flush=True)
