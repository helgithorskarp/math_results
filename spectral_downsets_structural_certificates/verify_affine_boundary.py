"""Smallest centered affine domain and elementary coloring calibration."""
from fractions import Fraction as F
from math import ceil
import json
from hashlib import sha256
import affine_pendant_completion as build
from verify_affine_pendant_completion import step, audit_modes
from certificates import lift, coloring_certificate
from verify import require, psd_ldl, check
from verify_clique_centers import core_buffer, fingerprint


def coloring_baseline():
    D = list(range(8))
    s, S, B = build.geometry(D, 0)
    E = build.add_pendants(D, 0, len(B))
    d = max(D).bit_length()
    colors = {a: i for i, a in enumerate(S)}
    for j, a in enumerate(B):
        colors[a] = colors[(1 << (d+j)) | 1] = s+j
        colors[1 << (d+j)] = 0
    ss = build.geometry(E, 0)[0]
    M = coloring_certificate([colors[a] for a in E[1:]], ss)
    rank = check(E, M, ss)
    v = [F(a != 0 and colors[a] == 0) for a in E]
    value = sum(v[i]*(F(int(i == j))-M[i][j])*v[j]
                for i in range(len(E)) for j in range(len(E)))
    require(value == -8 and rank == 7, 'Elementary coloring baseline differs')
    return dict(status='routine H baseline, no novelty claim', original_N=len(D),
                original_s=s, pendants=len(B), N=len(E), s=ss,
                lower_rank=rank, maximal_possible_lower_rank=len(E)-1,
                upper_slack_negative_form=str(value),
                witness_support=[E[i] for i, x in enumerate(v) if x],
                matrix_sha256=fingerprint(M))


def minimum_boundary():
    D = [0, 1, 2, 3, 4, 5]
    n, S, B = build.geometry(D, 0)
    require(n == 3 and len(B) == 2, 'Minimum affine sizes differ')
    outside = {(3, 2): -1, (3, 4): 1, (5, 2): 1, (5, 4): -1}

    def seed_entry(a, z):
        if a == z:
            return F(2)
        if a in S and z in S:
            return F(-1)
        if a in B and z in B:
            return F(-2)
        x, y = (a, z) if a in S else (z, a)
        return F(outside.get((x, y), 0))

    C0 = [[seed_entry(a, z) for z in D[1:]] for a in D[1:]]
    build.validate_core(D, C0, 0)
    require(psd_ldl(C0) == 3, 'Boundary seed lower rank differs')
    try:
        core_buffer(C0, len(D), F(1))
    except ValueError:
        lacks_unit_buffer = True
    else:
        raise ValueError('Boundary seed unexpectedly has unit upper buffer')
    R = max(sum(abs(x) for x in row) for row in C0)
    u = ceil(2*R+n)
    E, raw, _ = build.compile_history(D, C0, 0, u)
    C = [[raw(a, z) for z in E[1:]] for a in E[1:]]
    prior, iterative = D, C0
    for _ in range(u):
        prior, iterative = step(prior, iterative, 0)
    require(E == prior and C == iterative, 'Boundary entire recurrence differs')
    modes = audit_modes(D, C0, E, C, 0, u)
    N, s = len(E), n+u
    require(psd_ldl(C) == N-3, 'Boundary raw rank differs')
    core_buffer(C, N, F(1))
    eps = min(F(1, 2), F(n, 2*(len(B)+u+2)))
    a = 1 << (max(E).bit_length()-1)
    d = B[0]
    ai, di = E[1:].index(a), E[1:].index(d)
    repaired = [row[:] for row in C]
    repaired[ai][di] += eps
    repaired[di][ai] += eps
    require(psd_ldl(repaired) == N-2, 'Boundary repaired rank differs')
    core_buffer(repaired, N, F(1, 2))
    M = lift(repaired, s)
    require(check(E, M, s) == N-1, 'Boundary definition-level lower rank differs')
    require(psd_ldl([[F(int(i == j))-M[i][j] for j in range(N)] for i in range(N)]) == N-1,
            'Boundary upper rank differs')
    require(min(M[0][1:]) >= F(1, 2*(N-s)), 'Boundary empty margin differs')
    return dict(seed_N=len(D), seed_s=n, seed_b=len(B), row_bound=str(R),
                seed_without_unit_upper_buffer=lacks_unit_buffer,
                pendants=u, N=N, s=s, epsilon=str(eps), modes=modes,
                full_raw_entries=len(C)**2, raw_rank=N-3,
                repaired_core_rank=N-2, lower_slack_rank=N-1,
                upper_slack_rank=N-1, matrix_sha256=fingerprint(M),
                raw_sha256=fingerprint(C), whole_final_LDL=True)


def main():
    result = dict(agent='six-downset-1', role='researcher',
                  coloring_baseline=coloring_baseline(), minimum_boundary=minimum_boundary())
    result['canonical_sha256'] = sha256(json.dumps(result, sort_keys=True,
                                      separators=(',', ':')).encode()).hexdigest()
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
