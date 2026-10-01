"""Independent scalar bounds plus whole exact slacks at smaller counts.

The producer uses a closed entry history. This checker uses the separate
iterative block recurrence, complete invariant images, exact LDL and an
independent rational square-root bracket for the scalar criterion.
"""
from fractions import Fraction as F
from hashlib import sha256
from math import ceil
from pathlib import Path
import argparse
import json
import affine_pendant_completion as build
from verify_affine_pendant_completion import step, audit_modes
from verify import require, psd_ldl, check
from verify_clique_centers import core_buffer, fingerprint, matvec
from certificates import lift, extract_core


def independent_profile(D, C, center):
    old = D[1:]
    S = [i for i, a in enumerate(old) if a >> center & 1]
    B = [i for i, a in enumerate(old) if not a >> center & 1]
    n, b = len(S), len(B)
    require(n >= 3 and b >= n-1, 'Profile domain differs')
    row = max(sum(abs(C[i][j]) for j in B) for i in S)
    col = max(sum(abs(C[i][j]) for i in S) for j in B)
    radicand = row*col
    lo, hi = -1, 1
    while F(hi*hi) < radicand:
        hi *= 2
    while hi-lo > 1:
        q = (hi+lo)//2
        if F(q*q) >= radicand:
            hi = q
        else:
            lo = q
    require(F(hi*hi) >= radicand and (hi == 0 or F((hi-1)**2) < radicand),
            'Independent exact square-root bracket differs')
    R = max(sum(abs(x) for x in row) for row in C)
    D0 = [[C[i][j]-n*(F(int(i == j))-F(1, b)) for j in B] for i in B]
    require(all(sum(row) == 0 for row in D0), 'Outside centered deviation differs')
    require(all(sum(C[i][j] for j in B) == 0 for i in S), 'Cross row balance differs')
    require(all(sum(C[i][j] for i in S) == 0 for j in B), 'Cross column balance differs')
    outside = max(sum(abs(x) for x in row) for row in D0)
    return dict(seed_s=n, seed_b=b, row_bound=R, cross_row_bound=row,
                cross_column_bound=col, cross_bound=min(R, F(hi)),
                outside_row_bound=outside, outside_bound=min(R+n, outside),
                row_sufficient_count=ceil(2*R+n))


def independent_count(profile):
    n, b = profile['seed_s'], profile['seed_b']
    P, T = profile['cross_bound'], profile['outside_bound']
    A = B = F(1)
    for u in range(1, profile['row_sufficient_count']+1):
        A *= F((n+u-1)*(b+u-1)-1, (n+u-1)*(b+u-1))
        B = F(b-1, b+u-1)
        margin = u-B*T
        determinant = F(u)*margin-A*A*P*P
        if u >= 2 and margin >= 0 and determinant >= 0:
            require(psd_ldl([[F(u), -A*P], [-A*P, margin]]) in (1, 2),
                    'Scalar comparison is not PSD')
            return u, dict(alpha_product=A, beta_product=B,
                           outside_margin=margin, determinant=determinant)
    raise ValueError('No sufficient scalar count before guaranteed row bound')


def minimum_seed():
    D = [0, 1, 2, 3, 4, 5]
    outside = {(3, 2): -1, (3, 4): 1, (5, 2): 1, (5, 4): -1}
    def entry(a, z):
        if a == z:
            return F(2)
        if a & 1 and z & 1:
            return F(-1)
        if not a & 1 and not z & 1:
            return F(-2)
        x, y = (a, z) if a & 1 else (z, a)
        return F(outside.get((x, y), 0))
    C = [[entry(a, z) for z in D[1:]] for a in D[1:]]
    build.validate_core(D, C, 0)
    return D, C


def intersecting_census(D, s):
    """Exhaust all nonempty intersecting subfamilies; bounded small control."""
    require(len(D) <= 20, 'Census control limit exceeded')
    largest, maxima, visited = 0, [], 0
    def visit(chosen, remaining):
        nonlocal largest, maxima, visited
        visited += 1
        if len(chosen) > largest:
            largest, maxima = len(chosen), [chosen]
        elif len(chosen) == largest:
            maxima.append(chosen)
        for j, a in enumerate(remaining):
            visit(chosen+[a], [z for z in remaining[j+1:] if a & z])
    visit([], D[1:])
    require(largest == s and maxima == [[a for a in D if a & 1]],
            'Exact bounded equality census differs')
    return dict(scope='all intersecting subfamilies of this fixture only',
                visited_nonempty_and_empty_subfamilies=visited,
                largest_size=largest, maximum_families=len(maxima))


def full_check(label):
    if label == 'minimum':
        original, initial, C0 = None, *minimum_seed()
    else:
        original = [0, 1, 2, 3, 4, 5] if label == 'V' else list(range(8))
        initial, C0, _ = build.centered_seed(original, 0)
    profile = independent_profile(initial, C0, 0)
    require(profile == build.block_decay_profile(initial, C0, 0),
            'Producer and independent norm bounds differ')
    u, scalar = independent_count(profile)
    produced_u, produced = build.block_decay_count(initial, C0, 0)
    require(u == produced_u and produced == dict(profile, sufficient_count=u, **scalar),
            'Producer and independent sufficient thresholds differ')
    E, raw, history = build.compile_history(initial, C0, 0, u)
    C = [[raw(a, z) for z in E[1:]] for a in E[1:]]
    prior, iterative = initial, C0
    for _ in range(u):
        prior, iterative = step(prior, iterative, 0)
    require(E == prior and C == iterative, 'Full closed/recurrence comparison differs')
    require(history['alpha_product'] == scalar['alpha_product']
            and history['beta_product'] == scalar['beta_product'], 'History products differ')
    modes = audit_modes(initial, C0, E, C, 0, u,
                        decay_bounds=(profile['cross_bound'], profile['outside_bound']))
    N, s = len(E), profile['seed_s']+u
    require(psd_ldl(C) == N-3, 'Whole raw rank differs')
    core_buffer(C, N, F(1))
    ss = [i for i, a in enumerate(E[1:]) if a & 1]
    bb = [i for i, a in enumerate(E[1:]) if not a & 1]
    projection = [[F(int(i == j))-F(int(i in ss and j in ss), len(ss))
                   -F(int(i in bb and j in bb), len(bb))
                   for j in range(N-1)] for i in range(N-1)]
    psd_ldl([[C[i][j]-profile['seed_s']*projection[i][j] for j in range(N-1)]
             for i in range(N-1)])
    newest = 1 << (max(E).bit_length()-1)
    other = next(a for a in initial[1:] if not a & 1 and a.bit_count() == 1)
    eps = min(F(1, 2), F(profile['seed_s'], 2*(len(bb)+2)))
    repaired = [row[:] for row in C]
    ai, di = E[1:].index(newest), E[1:].index(other)
    repaired[ai][di] += eps
    repaired[di][ai] += eps
    require(psd_ldl(repaired) == N-2, 'Whole repaired rank differs')
    core_buffer(repaired, N, F(1, 2))
    M = lift(repaired, s)
    require(check(E, M, s) == N-1, 'Whole definition-level lower slack differs')
    require(psd_ldl([[F(int(i == j))-M[i][j] for j in range(N)]
                     for i in range(N)]) == N-1, 'Whole upper slack differs')
    require(extract_core(M, s) == repaired, 'Independent reverse lift differs')
    require(min(M[0][1:]) >= F(1, 2*(N-s)), 'Empty margin differs')
    require([c for c in range(max(E).bit_length())
             if sum(bool(a >> c & 1) for a in E) == s] == [0], 'Unique largest star differs')
    preprocessing = []
    if original is not None:
        family, entry, data = build.completion(original, 0, threshold='decay')
        require(family == E and build.dense_entries(E, entry) == M,
                'Whole completion oracle and independent lift differ')
        require(data['block_decay'] == produced and data['epsilon'] == eps,
                'Whole completion criterion or repair differs')
        if label == 'V':
            for D, r in (([0, 1], 2), (list(range(4)), 1)):
                FAM, oracle, dd = build.completion(D, 0, threshold='decay')
                require(FAM == E and build.dense_entries(FAM, oracle) == M
                        and dd['preprocessing'] == r, 'Smaller-star whole completion differs')
                preprocessing.append(dict(original_N=len(D), preliminary_pendants=r,
                                          total_pendants=dd['total_pendants'], same_matrix=True))
    record = dict(case=label, seed_N=len(initial),
        profile={k: str(v) if isinstance(v, F) else v for k,v in profile.items()},
        scalar={k: str(v) for k,v in scalar.items()}, further_pendants=u,
        N=N, s=s, complete_raw_entries=(N-1)**2, modes=modes,
        epsilon=str(eps), raw_rank=N-3, repaired_core_rank=N-2,
        lower_slack_rank=N-1, upper_slack_rank=N-1, raw_sha256=fingerprint(C),
        matrix_sha256=fingerprint(M), whole_final_LDL=True,
        negative_nonempty_offdiagonals=sum(M[i][j] < 0 for i in range(1, N)
                                         for j in range(i+1, N)),
        preprocessing_controls=preprocessing)
    if original is not None:
        record['total_pendants'] = u+1
    if label == 'cube3':
        v = [F(int(a in (1, 8))) for a in initial[1:]]
        value = sum(x*y for x,y in zip(v, matvec(C0, v)))
        require(value == -4, 'Indefinite seed form differs')
        record['seed_negative_form'] = str(value)
    if N <= 20:
        record['bounded_equality_census'] = intersecting_census(E, s)
    return record


def controls():
    D, C = minimum_seed()
    u, _ = build.block_decay_count(D, C, 0)
    require(u == 2, 'Minimum-plane boundary count differs')
    rejected = 0
    for f in (lambda: build.completion([0, 1, 2, 3, 4, 5], 0, 3, threshold='decay'),
              lambda: build.completion(list(range(8)), 0, 11, threshold='decay'),
              lambda: build.completion([0, 1, 2, 3, 4, 5], 0, threshold='unknown')):
        try:
            f()
        except ValueError:
            rejected += 1
        else:
            raise ValueError('Below-sufficient or unknown criterion accepted')
    # Check preservation of the original default count and exact metadata.
    for D, total in (([0, 1, 2, 3, 4, 5], 25), (list(range(8)), 50)):
        _, _, dd = build.completion(D, 0)
        require(dd['total_pendants'] == total and 'block_decay' not in dd,
                'Original row-bound API changed')
    return rejected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = dict(agent='six-downset-1', role='researcher',
                  rejected_controls=controls(),
                  records=[full_check(label) for label in ('minimum', 'V', 'cube3')])
    result['canonical_sha256'] = sha256(json.dumps(result, sort_keys=True,
                                      separators=(',', ':')).encode()).hexdigest()
    if args.check:
        expected = json.loads(Path(__file__).with_name('affine_decay_expected.json').read_text())
        require(result == expected, 'Complete decay output differs from frozen fixture')
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
