"""Fresh original linear-equation/Euclidean-metric audit; stdlib exact rationals."""
import argparse
from fractions import Fraction as F
import hashlib
import itertools
import json
from math import comb
from pathlib import Path


def need(p, label):
    if not p:
        raise ValueError(label)


def dump(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':')).encode()+b'\n'


def rational(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, list):
        return [rational(y) for y in x]
    if isinstance(x, dict):
        return {k: rational(v) for k, v in x.items()}
    return x


def sha(x):
    return hashlib.sha256(dump(rational(x))).hexdigest()


def tr(a):
    return [list(x) for x in zip(*a)]


def mul(a, b):
    bt = tr(b)
    return [[sum(x*y for x, y in zip(row, col)) for col in bt] for row in a]


def identity(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def sub(a, b):
    return [[x-y for x, y in zip(r, s)] for r, s in zip(a, b)]


def scale(a, c):
    return [[c*x for x in row] for row in a]


def inverse(a):
    n = len(a)
    a = [list(map(F, row))+identity(n)[i] for i, row in enumerate(a)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j]), None)
        need(pivot is not None, 'singular inverse')
        a[j], a[pivot] = a[pivot], a[j]
        d = a[j][j]
        a[j] = [x/d for x in a[j]]
        for i in range(n):
            if i != j and a[i][j]:
                d = a[i][j]
                a[i] = [x-d*y for x, y in zip(a[i], a[j])]
    ans = [r[n:] for r in a]
    return ans


def sparse_rank(rows):
    pivots = {}
    for source in rows:
        row = {i: F(x) for i, x in source.items() if x}
        while row:
            j = min(row)
            if j not in pivots:
                c = row[j]
                pivots[j] = {i: x/c for i, x in row.items()}
                break
            c = row[j]
            for i, x in pivots[j].items():
                row[i] = row.get(i, F(0))-c*x
                if not row[i]:
                    del row[i]
    return len(pivots)


def psd(a):
    """Complete exact symmetric Schur elimination, including zero rows."""
    a = [list(map(F, r)) for r in a]
    n = len(a)
    need(a == tr(a), 'PSD symmetry')
    rank = 0
    for j in range(n):
        d = a[j][j]
        need(d >= 0, 'negative PSD pivot')
        if not d:
            need(all(not a[j][i] for i in range(j, n)), 'nonzero zero-pivot row')
            continue
        rank += 1
        for i in range(j+1, n):
            for k in range(i, n):
                a[i][k] -= a[i][j]*a[j][k]/d
                a[k][i] = a[i][k]
    return rank


def hereditary(maxima):
    return sorted({b for top in maxima for b in range(top+1) if b & top == b})


def all_active(n):
    """Exhaustive small control census, without quotienting by isomorphism."""
    for flags in range(1, 1 << (1 << n), 2):
        d = [b for b in range(1 << n) if flags >> b & 1]
        if not all((1 << i) in d for i in range(n)):
            continue
        if all((b & ~(1 << i)) in d for b in d for i in range(n) if b >> i & 1):
            yield d


def system(name, d, damage):
    n = max(d).bit_length()
    need(d[0] == 0 and len(set(d)) == len(d), 'actual original vertices')
    need(all((1 << i) in d for i in range(n)), 'active singletons')
    N = len(d)
    stars = [sum(bool(b >> i & 1) for b in d) for i in range(n)]
    s = max(stars)
    maxpoints = [i for i in range(n) if stars[i] == s]
    if damage == 'force-small-stars' and name == 'asymmetric-four':
        maxpoints = list(range(n))
    p = len(maxpoints)
    qverts = [b for b in d if b and b not in [1 << i for i in maxpoints]]
    m = len(qverts)
    a = [[F((b & sum(1 << i for i in maxpoints)).bit_count()-1) for b in qverts]]
    for v in d[1:]:
        if v in [1 << i for i in maxpoints]:
            a.append([F(-bool(v & b)) for b in qverts])
        else:
            a.append([F(v == b) for b in qverts])
    if damage == 'drop-empty-row' and name == 'near-four':
        a[0] = [F(0)]*m
    pairs = list(itertools.combinations_with_replacement(range(N), 2))
    pos = {ij: t for t, ij in enumerate(pairs)}
    def equation(entries, rhs):
        row = {}
        for i, j, c in entries:
            index = pos[tuple(sorted((i, j)))]
            row[index] = row.get(index, F(0))+c
        row[len(pairs)] = F(rhs)
        return {i: x for i, x in row.items() if x}
    equations = []
    # Construct literal ORIGINAL constraints, independently of the decoder.
    for i, v in enumerate(d):
        equations.append(equation([(i, j, 1) for j in range(N)], N))
        for j in range(i, N):
            if v & d[j]:
                equations.append(equation([(i, j, 1)], s if i == j else 0))
        for point in [i for i in range(n) if stars[i] == s]:
            equations.append(equation([(i, j, 1) for j, b in enumerate(d) if b >> point & 1], s))
    coefficient_rows = [{i: x for i, x in row.items() if i < len(pairs)} for row in equations]
    rank = sparse_rank(coefficient_rows)
    need(sparse_rank(equations) == rank, 'original affine consistency')
    free = [(i, j) for i, b in enumerate(qverts) for j in range(i+1, m) if not b & qverts[j]]
    if damage == 'omit-complements' and name == 'near-four':
        free = [(i, j) for i, j in free if qverts[i] | qverts[j] != (1 << n)-1]
    need(len(pairs)-rank == len(free), 'ENTIRE original affine dimension')
    t = [[F(s-1) if i == j else F(-1) if b & c else F(0)
          for j, c in enumerate(qverts)] for i, b in enumerate(qverts)]
    if m:
        g = mul(tr(a), a)
        inv = inverse(g)
        need(mul(g, inv) == identity(m), 'full metric inverse')
        gm = [[F(i == j)+sum(F(bool(b >> k & 1) and bool(c >> k & 1)) for k in maxpoints)
               +F(1-(b & sum(1 << k for k in maxpoints)).bit_count())*
               F(1-(c & sum(1 << k for k in maxpoints)).bit_count())
               for j, c in enumerate(qverts)] for i, b in enumerate(qverts)]
        if damage == 'omit-empty-metric' and name == 'near-four':
            gm = [[x-F(1-(b & sum(1 << k for k in maxpoints)).bit_count())*
                   F(1-(c & sum(1 << k for k in maxpoints)).bit_count())
                   for x, c in zip(row, qverts)] for row, b in zip(gm, qverts)]
        need(g == gm, 'actual original Gram metric')
        projector = sub(sub(identity(N), [[F(1, N)]*N for _ in d]), mul(mul(a, inv), tr(a)))
        need(mul(projector, projector) == projector, 'full original orthogonal projector')
        need(sum(projector[i][i] for i in range(N)) == p, 'projector rank')
    else:
        g = []
        inv = []
        projector = sub(identity(N), [[F(1, N)]*N for _ in d])
    def lift(tmat, constant):
        core = mul(mul(a, tmat), tr(a)) if m else [[F(0)]*N for _ in d]
        return [[x+constant for x in row] for row in core]
    def verify(l, constant):
        values = [l[i][j] for i, j in pairs]
        for row in equations:
            need(sum(values[i]*x for i, x in row.items() if i < len(values)) ==
                 constant*row.get(len(values), F(0)), 'literal original support/row/star equation')
    base = lift(t, 1)
    verify(base, 1)
    if m:
        physical_cap = sub(scale(identity(N), N), base)
        cap_decomposition = [[x+y for x, y in zip(r, z)]
                             for r, z in zip(scale(projector, N),
                                 mul(mul(a, sub(scale(inv, N), t)), tr(a)))]
        need(physical_cap == cap_decomposition, 'ENTIRE original cap decomposition')
    matrices = [base, a, g, projector]
    entry_checks = N*N
    for i, j in free:
        z = [[F(0)]*m for _ in range(m)]
        z[i][j] = z[j][i] = 1
        direction = lift(z, 0)
        verify(direction, 0)
        need(direction[d.index(qverts[i])][d.index(qverts[j])] == 1, 'individual coordinate injectivity')
        matrices.append(direction)
        entry_checks += N*N
    comp = [(i, j) for i, j in itertools.combinations(range(m), 2)
            if qverts[i] ^ qverts[j] == (1 << n)-1 and not qverts[i] & qverts[j]]
    face_checks = []
    choices = [[pair] for pair in comp]+([comp] if len(comp) > 1 else [])
    for selected in choices:
        endpoints = {x for pair in selected for x in pair}
        fixed = [[x for x in row] for row in t]
        extra = []
        for i, j in selected:
            for u in range(m):
                value = F(s-1) if u in (i, j) else F(-1)
                fixed[u][i] = fixed[i][u] = fixed[u][j] = fixed[j][u] = value
            # PSD-forced exact original selected columns; NOT bare value equations.
            for endpoint in (i, j):
                actual = d.index(qverts[endpoint])
                for u, v in enumerate(d):
                    value = N-2*s if not v else s if v in (qverts[i], qverts[j]) else 0
                    extra.append(equation([(u, actual, 1)], value))
        facefree = [(i, j) for i, j in free if i not in endpoints and j not in endpoints]
        full = equations+extra
        face_rank = sparse_rank([{i: x for i, x in row.items() if i < len(pairs)} for row in full])
        need(sparse_rank(full) == face_rank, 'forced-column affine consistency')
        need(len(pairs)-face_rank == len(facefree), 'ENTIRE saturated-column affine dimension')
        l = lift(fixed, 1)
        for row in full:
            need(sum(l[pairs[i][0]][pairs[i][1]]*x for i, x in row.items() if i < len(pairs)) ==
                 row.get(len(pairs), F(0)), 'all exact selected original columns')
        matrices.append(l)
        for i, j in facefree:
            z = [[F(0)]*m for _ in range(m)]
            z[i][j] = z[j][i] = 1
            change = lift(z, 0)
            for row in full:
                need(sum(change[pairs[k][0]][pairs[k][1]]*x for k, x in row.items() if k < len(pairs)) == 0,
                     'ENTIRE remaining individual face direction')
            matrices.append(change)
        face_checks.append({'selected': [[qverts[i], qverts[j]] for i, j in selected], 'dimension': len(facefree)})
    return {'name': name, 'vertices': d, 'N': N, 's': s, 'max_points': maxpoints,
            'retained_smaller_singletons': [b for b in qverts if b.bit_count() == 1],
            'original_variables': len(pairs), 'original_equations': len(equations),
            'original_rank': rank, 'free_dimension': len(free), 'entry_checks': entry_checks,
            'faces': face_checks, 'complete_generated_matrices_sha256': sha(matrices)}, (d, a, t, g, inv, projector, free)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--damage', default='')
    arg = parser.parse_args()
    damage = arg.damage
    controls = [(f'exhaustive-active-{n}-{i}', d)
                for n in range(1, 4) for i, d in enumerate(all_active(n))]
    controls += [('near-four', [b for b in range(16) if b.bit_count() <= 2]),
                 ('cube-four', list(range(16))),
                 ('asymmetric-four', hereditary([7, 12])),
                 ('path-four', hereditary([3, 6, 12])),
                 ('cycle-four', hereditary([3, 6, 12, 9]))]
    rows = []
    originals = {}
    for name, d in controls:
        row, original = system(name, d, damage)
        rows.append(row)
        originals[name] = original
    # Fresh literal wrong-metric witness distinct from the author's stated -156.
    d, a, t, g, gi, pu, free = originals['near-four']
    for i, j in free:
        t[i][j] = t[j][i] = F(15, 8)
    need(psd(t) == len(t), 'wrong-metric witness T positive definite')
    need(psd(sub(scale(identity(len(t)), len(d)), t)) == len(t), 'naive cap positive definite')
    l = [[1+x for x in r] for r in mul(mul(a, t), tr(a))]
    upper = sub(scale(identity(len(d)), len(d)), l)
    v = [sum(r) for r in a]
    energy = sum(v[i]*upper[i][j]*v[j] for i in range(len(d)) for j in range(len(d)))
    witness_hash = sha([t, l, upper, v])
    need(energy == F(-117, 4), 'actual original negative cap energy')
    if damage == 'naive-cap':
        need(energy >= 0, 'naive cap fails literal original energy')
    # Nonvacuous N=2s, q=1, D_S=1 control for the larger-upper-kernel extension.
    d = hereditary([3, 6])
    s = 3
    N = 6
    maxpoint = 1
    qv = [1, 4, 3, 6]
    a = [[F(bool(b >> maxpoint & 1))-1 for b in qv]]
    for b in d[1:]:
        a.append([F(-bool(b & c)) for c in qv] if b == 2 else [F(b == c) for c in qv])
    t = [[F(2) if i == j else F(-1) if b & c else F(0) for j, c in enumerate(qv)]
         for i, b in enumerate(qv)]
    for j in range(4):
        val = F(2) if j in (0, 3) else F(-1)
        t[j][0] = t[0][j] = t[j][3] = t[3][j] = val
    l = [[1+x for x in r] for r in mul(mul(a, t), tr(a))]
    if damage == 'alter-seed-empty-loop':
        l[0][0] += 1
    for i, b in enumerate(d):
        need(sum(l[i]) == N, 'literal path seed row sum')
        for j, c in enumerate(d):
            if b & c:
                need(l[i][j] == (s if i == j else 0), 'literal path seed support including smaller stars')
        need(sum(l[i][j] for j, c in enumerate(d) if c >> 1 & 1) == s, 'literal path seed maximum star')
    lower_basis = [[F(bool(b >> 1 & 1))-F(1, 2), F(b == 1)-F(b == 6)] for b in d]
    upper_basis = [[F(1), F(b in (1, 6))] for b in d]
    if damage == 'omit-upper-pair-sum':
        upper_basis = [[F(1)] for b in d]
    def proj(basis):
        return mul(mul(basis, inverse(mul(tr(basis), basis))), tr(basis))
    lower_p = proj(lower_basis)
    upper_p = proj(upper_basis)
    cap = sub(scale(identity(N), N), l)
    need(mul(l, lower_basis) == [[F(0)]*2 for _ in d], 'exact lower seed kernel')
    need(mul(cap, upper_basis) == [[F(0)]*len(upper_basis[0]) for _ in d], 'exact upper seed kernel')
    eps = F(1, 2)
    need(psd(l) == 4 and psd(cap) == 4, 'seed both greatest permitted ranks')
    need(psd(sub(l, scale(sub(identity(N), lower_p), eps))) == 4, 'full original lower floor')
    need(psd(sub(cap, scale(sub(identity(N), upper_p), eps))) == 4, 'full original larger-upper-kernel floor')
    z = [[F(0)]*4 for _ in qv]
    z[1][2] = z[2][1] = 1
    direction = mul(mul(a, z), tr(a))
    need(mul(direction, lower_basis) == [[F(0)]*2 for _ in d], 'direction lower annihilation')
    need(mul(direction, upper_basis) == [[F(0)]*2 for _ in d], 'direction upper annihilation')
    gamma_small = sum(sum(x*x for x in row) for row in a)
    radius_small = eps/(4*gamma_small)
    for sign in (-1, 1):
        moved = [[x+sign*radius_small*y for x, y in zip(r, z)] for r, z in zip(l, direction)]
        moved_cap = sub(scale(identity(N), N), moved)
        need(psd(sub(moved, scale(sub(identity(N), lower_p), F(3, 8)))) == 4, 'path lower endpoint')
        need(psd(sub(moved_cap, scale(sub(identity(N), upper_p), F(3, 8)))) == 4, 'path upper endpoint')
    # Exact n28 counts in two independent orientations, plus all weighted degrees.
    n = 28
    N = (1 << n)-n-1
    s = (1 << (n-1))-n
    q = sum(comb(n, k) for k in range(2, 9))
    oriented = sum(comb(n, a)*comb(n-a, b) for a in range(9, 20)
                   for b in range(9, min(19, n-a)+1))
    unused = sum(comb(n, c)*sum(comb(n-c, a) for a in range(9, n-c-8)) for c in range(11))
    need(oriented == unused and oriented % 2 == 0, 'two complete disjoint-pair counts')
    D = oriented//2
    if damage == 'missing-swap-factor':
        D = oriented
    need(D == 3629809216575, 'unordered free-coordinate dimension')
    gamma = n*(n-1)*((1 << (n-2))-n+1)+2*(N-n-1)
    degrees = []
    for a in range(9, 20):
        unweighted = sum(comb(n-a, b) for b in range(9, min(19, n-a)+1))
        weighted = sum(F(comb(n-a, b))*F(2)**(a-b) for b in range(9, min(19, n-a)+1))
        degrees.append({'size': a, 'degree': unweighted, 'weighted_degree': weighted})
    delta = max(x['degree'] for x in degrees)
    weighted_delta = max(x['weighted_degree'] for x in degrees)
    if damage == 'wrong-weighted-degree':
        weighted_delta = degrees[1]['weighted_degree']
    need(weighted_delta == F(169870299, 1024), 'all eleven exact weighted rows')
    eps = F(1, 100000000)
    radius = eps/(4*gamma*weighted_delta)
    old_radius = eps/(4*gamma*delta)
    need(radius == F(1, 3402127283957218293750000), 'refined closed REAL radius')
    need(old_radius == F(1, 7270700478476198400000000), 'target radius')
    need(radius/old_radius == F(121010176, 56623433) and radius > 2*old_radius, 'strict factor larger than two')
    orbits = [(a, b) for a in range(9, 20) for b in range(a, min(19, n-a)+1)]
    need(len(orbits) == 36 and D-36 == 3629809216539, 'complete invariant orbit slice')
    result = {'method': 'fresh literal original equations and exact rational Euclidean checks',
              'systems': rows, 'control_census': {'all_active_n_le_3': len(controls)-5, 'additional': 5},
              'wrong_metric': {'complement_T_entry': F(15, 8), 'T_rank': 6, 'naive_cap_rank': 6,
                               'original_cap_energy': energy, 'full_matrix_sha256': witness_hash},
              'N_equals_two_s_seed': {'N': 6, 's': 3, 'p': 1, 'q': 1, 'dimension': 1,
                                     'vertices': d, 'selected_pair': [1, 6], 'remaining_pair': [4, 3],
                                     'L': l, 'lower_kernel_basis': lower_basis, 'upper_kernel_basis': upper_basis,
                                     'both_ranks': 4, 'epsilon': F(1, 2), 'gamma': gamma_small,
                                     'closed_radius': radius_small, 'both_retained_gaps': F(3, 8)},
              'n28_conditional_only': {'N': N, 's': s, 'q': q, 'D': D, 'gamma': gamma,
                                      'degree_rows': degrees, 'delta': delta, 'weighted_delta': weighted_delta,
                                      'old_radius': old_radius, 'new_radius': radius,
                                      'improvement_factor': radius/old_radius,
                                      'lower_rank': N-28-q, 'cap_rank': N-1,
                                      'invariant_orbits': orbits, 'noninvariant_slice_dimension': D-36,
                                      'L_gap': 3*eps/4, 'M_gap': 3*eps/(4*(N-s)), 'empty_loop_slope': 338}}
    arg.out.write_bytes(dump(rational(result)))
    print(json.dumps({'systems': len(rows), 'faces': sum(len(r['faces']) for r in rows),
                      'record_bytes': arg.out.stat().st_size, 'record_sha256': hashlib.sha256(arg.out.read_bytes()).hexdigest()}))


if __name__ == '__main__':
    main()
