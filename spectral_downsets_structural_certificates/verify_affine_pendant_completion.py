"""Independent exact recurrence and complete invariant-space validation."""
from fractions import Fraction as F
from math import ceil
from hashlib import sha256
import argparse
import json
from pathlib import Path
import affine_pendant_completion as build
from affine_completion_identities import certificates
from verify import require, psd_ldl, check
from verify_clique_centers import matvec, core_buffer, fingerprint
from certificates import lift, extract_core


def step(D, C, center):
    """Iterative K-block prescription, independent of the closed history."""
    n, S, B = build.geometry(D, center)
    b = len(B)
    old = D[1:]
    ix = {a: i for i, a in enumerate(old)}
    new = 1 << max(D).bit_length()
    spoke = new | (1 << center)
    E = sorted(D+[new, spoke])

    def entry(a, z):
        if a == z:
            return F(n)
        if a & z:
            return F(-1)
        if a == new or z == new:
            v = z if a == new else a
            return F(1, n) if v in S else -F(n, b)
        if a == spoke or z == spoke:
            return F(1, b)
        if bool(a >> center & 1) != bool(z >> center & 1):
            return (1-F(1, n*b))*(C[ix[a]][ix[z]]+1)-1
        if a in S:
            return F(-1)
        return (1-F(1, b))*(C[ix[a]][ix[z]]+1)-1

    T = [[entry(a, z) for z in E[1:]] for a in E[1:]]
    build.validate_core(E, T, center)
    return E, T


def audit_modes(initial, C0, E, C, center, u, *, decay_bounds=None):
    old, now = initial[1:], E[1:]
    pos, oi = {a: i for i, a in enumerate(now)}, {a: i for i, a in enumerate(old)}
    n0, S, B = build.geometry(initial, center)
    b, m, n = len(B), len(now), n0+u
    A = BETA = F(1)
    for j in range(u):
        A *= 1-F(1, (n0+j)*(b+j))
        BETA *= 1-F(1, b+j)
    require(BETA == F(b-1, b+u-1), 'Beta telescope')
    initial_vectors = []
    for G in (S, B):
        for a in G[:-1]:
            v = [F(0)]*m
            v[pos[a]], v[pos[G[-1]]] = F(1), F(-1)
            initial_vectors.append(v)
            want = [F(0)]*m
            for x in S:
                want[pos[x]] = n*v[pos[x]]+A*sum(C0[oi[x]][oi[y]]*v[pos[y]] for y in B)
            for x in B:
                want[pos[x]] = n*v[pos[x]]+A*sum(C0[oi[x]][oi[y]]*v[pos[y]] for y in S)+BETA*sum((C0[oi[x]][oi[y]]-n0*int(x == y))*v[pos[y]] for y in B)
            require(matvec(C, v) == want, 'Initial invariant images differ')
    groups = [initial_vectors]
    d = max(initial).bit_length()
    for j in range(u):
        single = 1 << (d+j)
        spoke = single | (1 << center)
        v, w = [F(0)]*m, [F(0)]*m
        for a in now:
            if a < single:
                if a >> center & 1:
                    v[pos[a]] = -F(1, n0+j)
                else:
                    w[pos[a]] = -F(1, b+j)
        v[pos[spoke]], w[pos[single]] = F(1), F(1)
        av = bv = F(1)
        for h in range(j+1, u):
            av *= 1-F(1, (n0+h)*(b+h))
            bv *= 1-F(1, b+h)
        nv, nw = 1+F(1, n0+j), 1+F(1, b+j)
        dd, cross = n+bv*(F(n0+j, b+j)-1), -av*nv*nw
        require(matvec(C, v) == [n*x+cross*y/nw for x, y in zip(v, w)],
                'Star contrast image differs')
        require(matvec(C, w) == [cross*x/nv+dd*y for x, y in zip(v, w)],
                'Outside contrast image differs')
        require(psd_ldl([[n*nv, cross], [cross, dd*nw]]) == 2,
                'Exact contrast lower form differs')
        require(psd_ldl([[(len(E)-1-n)*nv, -cross],
                         [-cross, (len(E)-1-dd)*nw]]) == 2,
                'Exact contrast buffered upper form differs')
        if decay_bounds is not None:
            psd_ldl([[(n-n0)*nv, cross], [cross, (dd-n0)*nw]])
            require(psd_ldl([[2*nv, -cross], [-cross, (n+2-dd)*nw]]) == 2,
                    'Exact contrast plus-two upper form differs')
        require(sum(x*x for x in v) == nv and sum(x*x for x in w) == nw,
                'Contrast norms differ')
        groups.append([v, w])
    constants = [[F(bool(a >> center & 1)) for a in now],
                 [F(not a >> center & 1) for a in now]]
    for v in constants:
        require(matvec(C, v) == [0]*m, 'Constant kernel differs')
    groups.append(constants)
    for i, G in enumerate(groups):
        for H in groups[i+1:]:
            for v in G:
                for w in H:
                    require(sum(x*y for x, y in zip(v, w)) == 0,
                            'Complete block orthogonality differs')
    # Within the initial difference basis and each plane independence is
    # immediate from their defining coordinates; constants are disjoint.
    require(sum(len(G) for G in groups) == m, 'Complete dimension differs')
    R = max(sum(abs(x) for x in row) for row in C0)
    Q = 2*R+n0
    if decay_bounds is None:
        require(u >= ceil(Q) and n-Q >= n0 and b+u >= Q,
                'Initial two-sided norm bridge fails')
    else:
        P, T = decay_bounds
        require(P >= 0 and T >= 0 and u >= BETA*T
                and u*(u-BETA*T) >= (A*P)**2,
                'Initial two-sided block-decay bridge fails')
    require(n-2 >= n0 and b+u >= 2,
            'Contrast norm bridge fails')
    return dict(initial_modes=n0+b-2, planes=u, complete_dimension=m,
                positive_mode_bound=str(n0), raw_upper_buffer='1',
                complete_orthogonality=True)


def rejection_controls():
    good = [0, 1, 2, 3, 4, 5]
    malformed = [([0], 0), ([0, True], 0), ([0, 1, 1], 0),
                 ([0, 3], 0), ([1, 2], 0), ([0, -1], 0),
                 ([0, 1, 2], 3), (good, 1), (good, False)]
    rejected = 0
    for D, c in malformed:
        try:
            build.completion(D, c)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('Malformed downset/center accepted')
    E, C, _ = build.centered_seed(good, 0)
    broken = [row[:] for row in C]
    broken[0][0] += 1
    nonsymmetric = [row[:] for row in C]
    nonsymmetric[0][1] += 1
    floated = [row[:] for row in C]
    floated[0][0] = float(floated[0][0])
    requests = [lambda: build.compile_history(E, broken, 0, 1),
                lambda: build.compile_history(E, nonsymmetric, 0, 1),
                lambda: build.compile_history(E, floated, 0, 1),
                lambda: build.compile_history(E, C, 0, False),
                lambda: build.completion(good, 0, 1),
                lambda: build.dense_entries(E, lambda a, z: 0, limit=7)]
    for f in requests:
        try:
            f()
        except ValueError:
            rejected += 1
        else:
            raise ValueError('Malformed core/count/dense request accepted')
    return rejected


def seed_normalizations():
    """All nontrivial labeled downsets on three points; affine seeds only."""
    families = centers = preprocessed = 0
    for mask in range(256):
        D = [a for a in range(8) if mask >> a & 1]
        if len(D) < 2 or D[0] != 0:
            continue
        if any(any(z not in D for z in range(8) if z & a == z) for a in D):
            continue
        families += 1
        s = max(sum(bool(a >> j & 1) for a in D) for j in range(3))
        for c in range(3):
            if sum(bool(a >> c & 1) for a in D) != s:
                continue
            r = max(0, 3-s)
            E = build.add_pendants(D, c, r)
            FAM, C, data = build.centered_seed(E, c)
            build.validate_core(FAM, C, c)
            require(data['seed_s'] == max(s, 3)+1, 'Preprocessed seed star differs')
            require([a for a in FAM if a < 1 << max(D).bit_length()] == D,
                    'Original induced restriction differs')
            centers += 1
            preprocessed += int(r > 0)
    require(families == 18, 'Three-point affine normalization coverage differs')
    return dict(labeled_nontrivial_families=families, maximum_centers=centers,
                preprocessing_branches=preprocessed, scope='affine seed identities only')


def run_case(label):
    D = [0, 1, 2, 3, 4, 5] if label == 'V' else list(range(8))
    initial, C0, seed = build.centered_seed(D, 0)
    E, oracle, data = build.completion(D, 0)
    u = data['history']['further_pendants']
    raw = data['raw_entry']
    C = [[raw(a, z) for z in E[1:]] for a in E[1:]]
    prior, iterative = initial, C0
    for _ in range(u):
        prior, iterative = step(prior, iterative, 0)
    require(prior == E and iterative == C, 'Closed and recurrence matrices differ')
    modes = audit_modes(initial, C0, E, C, 0, u)
    record = dict(case=label, original_N=len(D), original_s=build.geometry(D, 0)[0],
                  seed_N=len(initial), seed_s=seed['seed_s'], seed_b=seed['seed_b'],
                  row_bound=str(seed['row_bound']), delta=str(seed['delta']),
                  seed_tune_pair=seed['pair'], total_pendants=data['total_pendants'],
                  further_pendants=u, N=len(E), s=data['s'], modes=modes,
                  complete_raw_entries=len(C)**2, raw_sha256=fingerprint(C),
                  whole_final_LDL=label == 'V')
    if label == 'cube3':
        v = [F(0)]*len(C0)
        old = initial[1:]
        v[old.index(1)] = v[old.index(8)] = 1
        value = sum(x*y for x, y in zip(v, matvec(C0, v)))
        require(value == -4, 'Exact indefinite seed witness differs')
        record.update(seed_negative_form=str(value), final_repair_matrix_checked=False)
        return record
    N, s = len(E), data['s']
    require(psd_ldl(C) == N-3, 'Full raw rank differs')
    core_buffer(C, N, F(1))
    SS = [i for i, a in enumerate(E[1:]) if a & 1]
    BB = [i for i, a in enumerate(E[1:]) if not a & 1]
    lam = F(seed['seed_s'])
    P = [[F(int(i == j))-F(int(i in SS and j in SS), len(SS))
          -F(int(i in BB and j in BB), len(BB)) for j in range(N-1)] for i in range(N-1)]
    psd_ldl([[C[i][j]-lam*P[i][j] for j in range(N-1)] for i in range(N-1)])
    repaired = [row[:] for row in C]
    a, z = [E[1:].index(x) for x in data['repair_pair']]
    repaired[a][z] += data['epsilon']
    repaired[z][a] += data['epsilon']
    require(psd_ldl(repaired) == N-2, 'Full repair rank differs')
    core_buffer(repaired, N, F(1, 2))
    M = build.dense_entries(E, oracle)
    require(M == lift(repaired, s) and extract_core(M, s) == repaired,
            'Independent empty lift differs')
    require(check(E, M, s) == N-1, 'Whole definition-level H rank differs')
    require(psd_ldl([[F(int(i == j))-M[i][j] for j in range(N)] for i in range(N)]) == N-1,
            'Whole upper slack rank differs')
    require(min(M[0][1:]) >= F(1, 2*(N-s)), 'Empty margin differs')
    require([j for j in range(max(E).bit_length())
             if sum(bool(a >> j & 1) for a in E) == s] == [0], 'Unique maximum star differs')
    preprocessing = []
    for original, expected_r in (([0, 1], 2), (list(range(4)), 1)):
        pre = build.add_pendants(original, 0, expected_r)
        require(pre == D, 'Boundary preprocessing family differs')
        FAM, entry, other = build.completion(original, 0)
        require(FAM == E and other['preprocessing'] == expected_r,
                'Star one/two completion family differs')
        require(other['seed'] == data['seed'] and other['history'] == data['history']
                and other['repair_pair'] == data['repair_pair']
                and other['epsilon'] == data['epsilon'], 'Boundary exact formula data differ')
        for i, a in enumerate(E):
            for z in (0, E[-1]):
                require(entry(a, z) == M[i][E.index(z)], 'Boundary entry oracle differs')
        preprocessing.append(dict(original_N=len(original), initial_s=build.geometry(original, 0)[0],
                                  preliminary_pendants=expected_r, total_pendants=other['total_pendants'],
                                  identical_final_family_and_formula_data=True))
    record.update(repaired_core_rank=N-2, lower_slack_rank=N-1, upper_slack_rank=N-1,
                  epsilon=str(data['epsilon']), matrix_sha256=fingerprint(M),
                  negative_nonempty_offdiagonals=sum(M[i][j] < 0 for i in range(1, N) for j in range(i+1, N)),
                  preprocessing_controls=preprocessing, final_repair_matrix_checked=True)
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', choices=['V', 'cube3', 'all'], default='all')
    parser.add_argument('--progress', type=Path)
    args = parser.parse_args()
    symbolic = certificates()
    result = dict(agent='six-downset-1', role='researcher',
                  seed_normalizations=seed_normalizations(), rejected_controls=rejection_controls(),
                  cleared_identities=len(symbolic['identities']), sign_records=len(symbolic['sign_certificates']),
                  symbolic_sha256=symbolic['canonical_sha256'], records=[])
    for label in ('V', 'cube3'):
        if args.case not in ('all', label):
            continue
        result['records'].append(run_case(label))
        if args.progress:
            args.progress.write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    result['canonical_sha256'] = sha256(json.dumps(result, sort_keys=True,
                                      separators=(',', ':')).encode()).hexdigest()
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
