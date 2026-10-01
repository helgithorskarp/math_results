#!/usr/bin/env python3
"""Literal rational checks, full uniform images, kernels and credited baselines."""
import argparse
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path
import sys

import certificates as base
import deletions as inherited
import strict_deletion_repair as build
from strict_deletion_identities import certificates as identities
from verify import check, psd_ldl, require
from verify_clique_centers import matvec, basis_rank, image_block, core_buffer, fingerprint
from verify_deletions import check_case as inherited_check, summary as inherited_summary
from verify_two_centers import maximum_intersecting_families


def uniform_images(n, t):
    family = build.members(n, [])[1:]
    C = [[build.uniform_entry(n, t, a, b) for b in family] for a in family]
    positions = {x: i for i, x in enumerate(family)}
    edges = list(combinations(range(n), 2)); basis = []
    def vector(entries):
        out = [F(0)] * len(family)
        for mask, value in entries: out[positions[mask]] += value
        return out
    masks = [1 << i for i in range(n)]
    pivots = {(0, 1), (0, 2), (1, 2)} | {(0, i) for i in range(3, n)}
    kappa = F(n*(n-1), n-2)
    for i, j in edges:
        if (i, j) in pivots: continue
        entries = [(masks[i] | masks[j], 1), (3, int(1 not in (i, j))),
                   (5, int(2 not in (i, j))), (6, -1)]
        entries += [(masks[0] | masks[k], -int(k in (i, j))) for k in range(3, n)]
        v = vector(entries)
        require(all(sum(v[positions[masks[a] | masks[b]]] for a, b in edges if k in (a, b)) == 0
                    for k in range(n)), 'Incidence-kernel basis failed')
        require(matvec(C, v) == [(kappa+t)*x for x in v], 'Incidence-kernel image failed')
        basis.append(v)
    a = n-(n-2)*(n-3)*t
    for i in range(n-1):
        x = [int(k == i)-int(k == n-1) for k in range(n)]
        B = [vector([(masks[k], x[k]) for k in range(n)]),
             vector([(masks[c] | masks[d], x[c]+x[d]) for c, d in edges])]
        image_block(C, B, [[a, -a], [-a, a]], [F(1), F(n-2)])
        basis += B
    B = [vector([(x, 1) for x in masks]),
         vector([(masks[i] | masks[j], 1) for i, j in edges])]
    a = n*(n-1)*(n-2)*(n-3)*t
    image_block(C, B, [[a, -a/2], [-a/2, a/4]], [F(n), F(n*(n-1), 2)])
    basis += B
    require(len(basis) == len(C) and basis_rank(basis) == len(C), 'Uniform decomposition incomplete')
    require(psd_ldl(C) == n*(n-1)//2, 'Uniform perturbed rank failed')
    C0 = [[build.uniform_entry(n, F(0), a, b) for b in family] for a in family]
    E = [[(C[i][j]-C0[i][j])/t for j in range(len(C))] for i in range(len(C))]
    gamma = F((n-2)*(n-3)*(2*n-1), 2)
    for sign in (-1, 1):
        psd_ldl([[gamma*int(i == j)+sign*E[i][j] for j in range(len(C))]
                 for i in range(len(C))])
    return dict(n=n, basis_rank=len(C), core_rank=n*(n-1)//2,
                t=str(t), perturbation_norm=str(gamma))


def literal_case(n, edges):
    data = build.parameters(n, edges)
    D, M, s = build.certificate(n, edges); N = len(D); m = N-1
    require(s == n and N > 2*n, 'Strict eligible density failed')
    r = data['r']; comps = data['components']; bcount = len(comps)
    require(check(D, M, s) == N-r, 'Final lower rank failed')
    require(psd_ldl([[F(i == j)-M[i][j] for j in range(N)] for i in range(N)]) == m,
            'Cap/simple top failed')
    C = base.extract_core(M, s)
    core_buffer(C, N, data['mu']/(4 if bcount else 2))
    raw = [[build.uniform_entry(n, data['t'], a, b) for b in D[1:]] for a in D[1:]]
    require(psd_ldl(raw) == m-r-bcount, 'Retained principal rank failed')
    core_buffer(raw, N, data['mu']/2)
    incidence = [[F(i in edge) for i in range(n)] for edge in data['edges']]
    if incidence:
        require(basis_rank(incidence) == n-r-bcount, 'Deleted-constraint nullity failed')
    stars = [[F(bool(mask & (1 << i))) for mask in D[1:]] for i in data['untouched']]
    extras = [[sum(F(component['signs'][i])*int(bool(mask & (1 << i)))
                   for i in range(n)) for mask in D[1:]] for component in comps]
    require(basis_rank(stars+extras) == r+bcount, 'Principal kernel basis dependent')
    for v in stars+extras:
        require(matvec(raw, v) == [0]*m, 'Principal kernel relation failed')
    partitions = []
    for j, colors in enumerate(data['colors']):
        require(all(colors[a] != colors[c] for a in range(m) for c in range(a+1, m)
                    if D[a+1] & D[c+1]), 'Recoloring not proper')
        for i in data['untouched']:
            require(sorted(colors[a] for a, mask in enumerate(D[1:]) if mask >> i & 1) == list(range(n)),
                    'Maximum-star colors changed')
        P = [[F(n*int(c == d)-1) for d in colors] for c in colors]
        psd_ldl(P)
        for v in stars: require(matvec(P, v) == [0]*m, 'Partition does not kill maximum star')
        G = [[sum(x[i]*y[i] for i in range(m)) for y in [matvec(P, v) for v in extras]]
             for x in extras]
        require(G == [[F(2*n*int(a == j and c == j)) for c in range(bcount)]
                       for a in range(bcount)], 'Component quotient differs')
        partitions.append(P)
    # Reconstruct entries with the closed lift, independently of build.retained_core/base.lift.
    independent = [[build.uniform_entry(n, data['t'], a, c) for c in D[1:]] for a in D[1:]]
    if bcount:
        e = data['epsilon']
        independent = [[(1-e)*independent[i][j] +
                        e*sum(n*int(colors[i] == colors[j])-1 for colors in data['colors'])/bcount
                        for j in range(m)] for i in range(m)]
    direct = [[F(0)]*N for _ in range(N)]
    for i in range(m):
        for j in range(m):
            direct[i+1][j+1] = (independent[i][j]+1-n*int(i == j))/(N-n)
        direct[0][i+1] = direct[i+1][0] = (1-sum(independent[i]))/(N-n)
    direct[0][0] = (1-n+sum(map(sum, independent)))/(N-n)
    require(direct == M, 'Closed full entry formula differs')
    maxima = maximum_intersecting_families(D)
    target = {tuple(mask for mask in D[1:] if mask >> i & 1) for i in data['untouched']}
    require(maxima == target, 'Literal complete equality census differs')
    return dict(n=n, deleted_edges=[list(e) for e in data['edges']], N=N, s=s, r=r,
                nonisolated_bipartite_components=bcount, L_rank=N-r,
                retained_rank=m-r-bcount, upper_rank=m, scalar=str(data['scalar']),
                mu=str(data['mu']), t=str(data['t']), epsilon=None if not bcount else str(data['epsilon']),
                beta=data['beta'], maximum_families=len(maxima), matrix_sha256=fingerprint(M))


def controls():
    bad = [(3, []), (True, []), (4.0, []), (4, [(0, 0)]), (4, [(0, 4)]),
           (4, [(False, 1)]), (4, [(0, 1), (1, 0)]), (4, [(0, 1, 2)]),
           (4, ['01']), (4, [(0, 1), (2, 3)]),
           (4, [(0, 1), (0, 2), (1, 2)]),
           (5, [(0, 1), (1, 2), (2, 3), (3, 0)])]
    count = 0
    for n, edges in bad:
        try: build.certificate(n, edges)
        except ValueError: count += 1
        else: raise ValueError('Malformed/out-of-domain certificate accepted')
    for call in [lambda: build.certificate(4, [], -1), lambda: build.certificate(4, [], True),
                 lambda: build.matching_certificate(4, 2), lambda: build.matching_certificate(4, True),
                 lambda: build.partial_star_certificate(4, 3), lambda: build.partial_star_certificate(4, -1)]:
        try: call()
        except ValueError: count += 1
        else: raise ValueError('Malformed convenience API accepted')
    for matrix in [[[F(-1)]], [[F(0), F(1)], [F(1), F(1)]]]:
        try: psd_ldl(matrix)
        except ValueError: pass
        else: raise ValueError('Invalid PSD control accepted')
    # t=0 has the credited extra kernel, and no perturbation can be inferred from it.
    D = build.members(4, [])
    C0 = [[build.uniform_entry(4, F(0), a, b) for b in D[1:]] for a in D[1:]]
    require(check(D, base.lift(C0, 4), 4, upper=True) == len(D)-4-1, 'Zero-perturbation rank control failed')
    return dict(malformed_or_out_of_domain_rejected=count, PSD_controls=2,
                unperturbed_uniform_lower_rank=6,
                nonexistence_claim=False)


def run():
    symbolic = identities()
    baseline = []; choices = set(); strict_small = 0; boundary_small = 0; uncapped_small = 0
    for n in range(3, 6):
        edges = list(combinations(range(n-1), 2))
        for mask in range(1 << len(edges)):
            removed = [e for i, e in enumerate(edges) if mask >> i & 1]
            baseline.append(inherited_check(n, removed))
            if n == 3: continue
            _, scalar = inherited.cap_test(n, removed)
            if scalar < 1:
                strict_small += 1; choices.add((n, tuple(removed)))
            elif scalar == 1: boundary_small += 1
            else: uncapped_small += 1
    expected_baseline = json.loads(Path(__file__).with_name('deletions_expected.json').read_text())['labelled_deletion_cohort']
    require(inherited_summary(baseline) == expected_baseline, 'Published complete labelled baseline differs')
    for n in range(4, 9):
        for k in range((n-1)//2+1): choices.add((n, tuple((i, n-1-i) for i in range(k))))
        for k in range(1, n-1): choices.add((n, tuple((0, i) for i in range(1, k+1))))
    special = [(6, [(0, 1), (1, 2)]), (6, [(0, 1), (1, 2), (0, 2)]),
               (7, [(0, 1), (1, 2), (2, 3), (0, 3)]),
               (7, [(0, 1), (1, 2), (2, 3), (3, 4)]),
               (8, [(0, 1), (1, 2), (3, 4)]),
               (8, [(0, 1), (1, 2), (0, 2), (3, 4)])]
    for n, edges in special: choices.add((n, tuple(sorted(edges))))
    images = [uniform_images(n, build.parameters(n, [])['t']) for n in range(4, 9)]
    cases = []
    for index, (n, edges) in enumerate(sorted(choices)):
        cases.append(literal_case(n, edges))
        if (index+1) % 20 == 0: print('strict deletion cases: '+str(index+1), file=sys.stderr, flush=True)
    tensors = []
    factors = [(build.matching_certificate(4, 1), build.matching_certificate(4, 1, 4), 4),
               (build.partial_star_certificate(4, 2), ([a << 4 for a in [0, 1, 2]],
                [[F(0), F(1, 2), F(1, 2)], [F(1, 2), F(0), F(1, 2)],
                 [F(1, 2), F(1, 2), F(0)]], 1), 1)]
    for left, right, expected_stars in factors:
        check(*left, upper=True); check(*right, upper=True)
        D, M, s = base.product_certificate([left, right]); N = len(D)
        require(check(D, M, s) == N-expected_stars, 'Tensor lower rank failed')
        require(psd_ldl([[F(i == j)-M[i][j] for j in range(N)] for i in range(N)]) == N-1,
                'Tensor cap/simple top failed')
        tensors.append(dict(N=N, s=s, L_rank=N-expected_stars, eligible_stars=expected_stars,
                            matrix_sha256=fingerprint(M)))
    shifted = build.certificate(5, [(0, 1), (1, 2)], 7)
    unshifted = build.certificate(5, [(0, 1), (1, 2)])
    require(shifted == ([a << 7 for a in unshifted[0]], unshifted[1], unshifted[2]), 'Shift API differs')
    require(build.matching_certificate(5, 2) == build.certificate(5, [(0, 4), (1, 3)]), 'Matching API differs')
    require(build.partial_star_certificate(5, 3) == build.certificate(5, [(0, 1), (0, 2), (0, 3)]), 'Star API differs')
    result = dict(agent='six-downset-1', role='researcher', symbolic_certificate=symbolic,
                  published_baseline=expected_baseline, strict_small_cohort=strict_small,
                  boundary_small_cohort=boundary_small, uncapped_inherited_small_cohort=uncapped_small,
                  literal_cases=cases, uniform_images=images, products=tensors,
                  input_controls=controls(), base_N_max=max(x['N'] for x in cases))
    return result


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--check', action='store_true')
    args = parser.parse_args(); result = run()
    if args.check:
        expected = json.loads(Path(__file__).with_name('strict_deletion_repair_expected.json').read_text())
        require(result == expected, 'Complete expected result differs')
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__': main()
