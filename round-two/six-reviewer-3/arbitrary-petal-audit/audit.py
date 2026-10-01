#!/usr/bin/env python3
"""six-reviewer-3: independent arbitrary-petal attachment and margin audit.

Uses this reviewer's hash-pinned published8682 projector/Bareiss toolkit.
No author Python imports. The all-parameter proof is in REVIEW.md.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement, product
from pathlib import Path
import importlib.util
import json


def need(ok, message):
    if not ok:
        raise ValueError(message)


def load_prior(path):
    raw = path.read_bytes()
    need(sha256(raw).hexdigest() == '2382479d58813caf97b33f2b6cbc3fc318a4cd10e1c382aa9f6b4436108cd3c1', 'published independent toolkit hash')
    spec = importlib.util.spec_from_file_location('review8682_independent_toolkit', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sparse_lift(c):
    """Multiply the literal signed E using its sparse columns."""
    rows = list(map(sum, c))
    return [[sum(rows)]+[-x for x in rows]]+[
        [-rows[i]]+list(row) for i, row in enumerate(c)]


def add_identity(a, value):
    return [[x+value*(i == j) for j, x in enumerate(row)] for i, row in enumerate(a)]


def unique_parameters(stars, prior):
    need(len(stars) >= 2 and stars[0] > stars[1], 'unique largest star')
    need(all(type(x) is int and x > 0 and x & (x-1) == 0 for x in stars), 'dyadic integer stars')
    need(stars == sorted(stars, reverse=True), 'descending star order')
    t, r = stars[0], len(stars)
    A = t-1
    lead = 2 if r % 2 == 0 else 3
    if lead == 2:
        u = stars[1]
        G0 = [[F(A)]*2 for _ in range(2)]
        beta0 = F((2*u-1)*(t-2*u+1), A)
        mode = 'two_aligned'
    else:
        G0, beta0 = prior.parameters(stars[:3])
        if stars[1] == stars[2] == 1:
            mode = 'three_centered:two_singletons'
        elif t == 2*stars[1] and stars[2] == 1:
            mode = 'three_centered:adjacent_singleton_trace'
        elif t == 2*stars[1]:
            mode = 'three_aligned:adjacent_aligned'
        else:
            need(t >= 4*stars[1], 'exhaustive dyadic split')
            mode = 'three_centered:widely_unequal_balanced'
    centered = 'centered' in mode
    alpha0 = [F(t-2*u+1, A) for u in stars[:lead]]
    if centered:
        need(prior.mm(G0, [[x] for x in alpha0]) == [[0]]*lead, 'centered leading empty vector')
    else:
        need(G0 == [[F(A)]*lead for _ in range(lead)], 'aligned leading Gram')
        delta0 = lead*A+F(sum(2*u-2 for u in stars[:lead]), A)
        need(delta0 >= 2*t, 'aligned diagonal norm')
    G = [[F(0)]*r for _ in range(r)]
    for i in range(lead):
        G[i][:lead] = G0[i][:]
    pairs, mass, energy, diagonal_max = [], 0, F(0), F(0)
    for i in range(lead, r, 2):
        v, w = stars[i:i+2]
        need(v >= w >= 1 and 2*v <= t, 'opposite-pair domain')
        delta = 2*A+F(2*(v+w-2), A)
        e = F(4*(v-w)**2, A)
        mass_i = 2*(v+w-1)
        need(delta < 2*t and 0 <= e <= mass_i-2, 'pair attachment budgets')
        for q in [v, w]:
            if q >= 2:
                residual = F(t, A)*max(2*(q-1) if q >= 3 else 0, 2*(t-q))
                need(residual <= delta, 'exact pair residual dominated by its diagonal frame')
        G[i][i] = G[i+1][i+1] = F(A)
        G[i][i+1] = G[i+1][i] = F(-A)
        pairs.append({'stars': [v, w], 'delta': str(delta), 'energy': str(e), 'mass': mass_i})
        mass += mass_i
        energy += e
        diagonal_max = max(diagonal_max, delta)
    count = len(pairs)
    nlead = 1+sum(2*u-1 for u in stars[:lead])
    N = nlead+mass
    old_beta = min(mass+beta0, F(nlead-2*t+2*count)) if centered else beta0+2*count
    if centered:
        beta = beta0 if not count else min(mass+beta0, N-diagonal_max-energy)
    else:
        beta = beta0+mass-energy
    need(beta >= old_beta > 0, 'stronger strict seed margin')
    gram_rank = prior.psd(G)
    # General rational Gaussian inverse, not the author's Sherman--Morrison formula.
    diagonal = [1+F(2*u-2, A*A) for u in stars]
    alpha = [F(t-2*u+1, A) for u in stars]
    R = [[diagonal[i]*(i == j)+alpha[i]*alpha[j] for j in range(r)] for i in range(r)]
    Rinv = prior.inverse(R)
    need(prior.mm(R, Rinv) == [[F(i == j) for j in range(r)] for i in range(r)], 'full Gaussian inverse')
    for b in [old_beta, beta]:
        prior.psd([[(N-b)*Rinv[i][j]-G[i][j] for j in range(r)] for i in range(r)])
    if not centered and not energy:
        delta0 = lead*A+F(sum(2*u-2 for u in stars[:lead]), A)
        kappa0 = delta0+A*sum(alpha0)**2
        need(N-kappa0 == beta, 'exact fixed-Gram optimal margin for balanced attached pairs')
    return G, {'leading_count': lead, 'mode': mode, 'beta0': str(beta0), 'old_beta': str(old_beta),
               'beta': str(beta), 'tail_mass': mass, 'tail_energy': str(energy),
               'tail_diagonal_max': str(diagonal_max), 'pairs': pairs, 'Gram_rank': gram_rank,
               'Gram_sha256': prior.fingerprint(G), 'centered': centered}


def unique(orders, prior, improved=False):
    data = prior.vertices(orders)
    family = [0]+[row[3] for row in data]
    stars = [1 << (a-1) for a in orders]
    t, N = stars[0], len(family)
    G, info = unique_parameters(stars, prior)
    seedcore = prior.projected_core(orders, G)
    shiftcore = prior.shifted_core(orders)
    qseed, qshift = sparse_lift(seedcore), sparse_lift(shiftcore)
    if N <= 24:
        need(qseed == prior.lift_q(seedcore) and qshift == prior.lift_q(shiftcore), 'sparse/dense literal E action')
    beta_old, beta = F(info['old_beta']), F(info['beta'])
    B = sum(u-1+(t-u)*(2*u-1) for u in stars)
    need(sum(map(sum, shiftcore)) == B, 'shifted constant form')
    zold = max(0, 2*t+B-N)
    old_epsilon = beta_old/(2*(beta_old+zold))
    Lambda = t+1+B
    K = 2*sum(u*u*(t-u) for u in stars)
    eta = min(F(Lambda-2*t), F(K, Lambda))
    need(eta > 0 and K == (t+1)*B-sum(sum(row)**2 for row in shiftcore), 'credited strict shifted deficit')
    z = max(0, Lambda-N)
    endpoint = beta/(beta+z)
    need(0 < old_epsilon < endpoint <= 1, 'closed repair coefficient enlargement')
    epsilon = endpoint if improved else old_epsilon
    q = [[(1-epsilon)*qseed[i][j]+epsilon*qshift[i][j] for j in range(N)] for i in range(N)]
    matrix = prior.matrix_from_q(q, t)
    gap = (1-epsilon)*beta+epsilon*(N-Lambda+eta) if improved else beta_old/2
    need(gap > 0, 'strict repaired endpoint cap')
    forced_seed = t+len(stars)+sum(1 < u < t for u in stars)-info['Gram_rank']
    seed = prior.matrix_from_q(qseed, t)
    seed_check = prior.checks(family, seed, t, forced_seed)
    prior.gap(seed, t, beta)
    part = family, matrix, t
    observed = prior.checks(*part, t)
    prior.gap(matrix, t, gap)
    if improved:
        prior.psd([[F(Lambda-eta)*(F(i == j)-F(1, N))-qshift[i][j]
                    for j in range(N)] for i in range(N)])
    info.update(observed)
    info.update(old_epsilon=str(old_epsilon), epsilon=str(epsilon), B=B,
                Lambda=Lambda, eta=str(eta), scaled_upper_gap=str(gap),
                positive_lower_gap=str(epsilon*(t-stars[1])), seed_lower_rank=seed_check['lower_rank'],
                seed_sha256=seed_check['matrix_sha256'])
    return part, info


def all_petals(orders, prior, improved=False):
    prior.vertices(orders)  # Validate the literal cohort before allocating packets.
    k = orders.count(orders[0])
    t = 1 << (orders[0]-1)
    if k == 1:
        part, info = unique(orders, prior, improved)
        return part, {'orders': list(orders), 'r': len(orders), 'k': 1, 'assembly': 'unique', **info}
    if k < len(orders):
        packet_orders = (orders[0],)+tuple(orders[k:])
        packet, info = unique(packet_orders, prior, improved)
        packets = [packet]
    else:
        packet_orders, info = (), None
        packets = [prior.cube(orders[0])]
    packets += [prior.cube(orders[0]) for _ in range(k-1)]
    part = prior.union(packets)
    observed = prior.checks(*part, k*t)
    return part, {'orders': list(orders), 'r': len(orders), 'k': k, 'assembly': 'equal-star packets',
                  'unique_packet_orders': list(packet_orders), 'packet': info, **observed}


def pairings(values):
    if not values:
        yield []
    else:
        first = values[0]
        for j in range(1, len(values)):
            remaining = values[1:j]+values[j+1:]
            for tail in pairings(remaining):
                yield [(first, values[j])]+tail


def pairing_check():
    cases, comparisons = 0, 0
    for length in [2, 4, 6]:
        for values in combinations_with_replacement([1, 2, 4], length):
            adjacent = sum((values[i]-values[i+1])**2 for i in range(0, length, 2))
            for pairs in pairings(list(values)):
                need(sum((v-w)**2 for v, w in pairs) >= adjacent, 'adjacent pairing energy optimum')
                comparisons += 1
            cases += 1
    return {'sorted_tail_cases': cases, 'perfect_pairings_compared': comparisons}


def reject(fn):
    try:
        fn()
    except (ValueError, StopIteration):
        return
    raise ValueError('invalid control accepted')


def run(author, prior):
    original, improved_rows, built = [], [], {}
    for old in author['cube_unions']:
        orders = tuple(old['orders'])
        part, row = all_petals(orders, prior)
        for key in ['N', 's', 'lower_rank', 'upper_rank', 'matrix_sha256']:
            need(row[key] == old[key], 'original union comparison '+key)
        if 'beta' in old:
            for newkey, oldkey in [('old_beta', 'beta'), ('old_epsilon', 'epsilon'),
                                   ('seed_lower_rank', 'seed_lower_rank'), ('seed_sha256', 'seed_sha256'),
                                   ('Gram_sha256', 'Gram_sha256'), ('Gram_rank', 'Gram_rank')]:
                need(row[newkey] == old[oldkey], 'original seed comparison '+oldkey)
        original.append(row)
        built[orders] = part
        if row['k'] == 1:
            _, improved = all_petals(orders, prior, True)
            improved_rows.append(improved)
    p4 = built[(2, 1, 1, 1)]
    p5 = all_petals((2, 1, 1, 1, 1), prior)[0]
    pmany = all_petals((2, 2, 1, 1, 1), prior)[0]
    products = []
    product_cases = [([p4, p4], [2, 2]), ([p4, p5], [2, 2]), ([p4, pmany], [2, 4])]
    for (parts, nullities), old in zip(product_cases, author['products']):
        part = prior.tensor(parts)
        density = max(F(p[2], len(p[0])) for p in parts)
        forced = sum(nullities[i]
                     for i in range(len(parts)) if F(parts[i][2], len(parts[i][0])) == density)
        observed = prior.checks(*part, forced)
        for key in observed:
            need(observed[key] == old[key], 'strict tensor comparison '+key)
        products.append(observed)
    common = []
    for parts, old in zip([[prior.cube(1), p4], [prior.cube(2), p4],
                           [prior.cube(2), built[(3, 2, 1, 1)]],
                           [prior.cube(1), p4, all_petals((1, 1), prior)[0]]], author['common_core_products']):
        c = max(parts[0][0]).bit_length()
        part = prior.tensor(parts)
        observed = prior.checks(*part, 1 << (c-1), 1 << (c-1))
        for key in observed:
            need(observed[key] == old[key], 'common-core tensor comparison '+key)
        common.append(observed)
    extras = []
    for orders in [(3, 2, 2, 2, 2), (5, 3, 3, 3, 3),
                   (3, 2, 2, 2), (3,)+(2,)*21, (3,)+(2,)*22]:
        part, row = all_petals(orders, prior, True)
        extras.append(row)
    sample = extras[0]
    need((F(sample['beta']), F(sample['epsilon']), F(sample['scaled_upper_gap'])) ==
         (F(22, 3), F(11, 35), F(176, 315)), 'exact five-petal improvement example')
    G, meta = unique_parameters([4, 2, 2, 2, 2], prior)
    bad = [row[:] for row in G]; bad[0][1] += 1
    family, matrix, s = p4
    badmatrix = [row[:] for row in matrix]; badmatrix[1][1] += 1
    controls = [lambda: all_petals((1, 3, 2, 1), prior),
                lambda: all_petals((3, 2, 1, 0), prior),
                lambda: all_petals((3, True), prior),
                lambda: all_petals((6, 6), prior),
                lambda: unique_parameters([4, 4, 1, 1], prior),
                lambda: unique_parameters([7, 3, 2, 1], prior),
                lambda: prior.psd(bad),
                lambda: prior.checks(family, badmatrix, s, s),
                lambda: prior.gap(matrix, s, F(100)),
                lambda: prior.psd([[0, 1], [1, 0]])]
    for fn in controls:
        reject(fn)
    return {'actual_agent': 'six-reviewer-3', 'role': 'independent mathematical reviewer',
            'original_unions': original, 'original_products': products,
            'original_common_core_products': common, 'improved_unique_unions': improved_rows,
            'new_boundary_and_many_petal_examples': extras, 'pairing_optimum_checks': pairing_check(),
            'rejected_controls': len(controls),
            'proof_status': 'Scoped ordinary unformalized audit of8700 with credited seed/equality inputs; actual pair-energy margins and credited closed repair; general H/I open.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--author-results', type=Path, required=True)
    parser.add_argument('--prior-audit', type=Path, default=Path(__file__).parent.parent/'three-petal-audit'/'audit.py')
    parser.add_argument('--write', type=Path)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    raw = args.author_results.read_bytes()
    need(sha256(raw).hexdigest() == '3f1b9bd966a3ba795892e80152927935ccb6967407d75c2849c3021d17cf0a68', 'public author receipt hash')
    result = run(json.loads(raw), load_prior(args.prior_audit))
    raw = (json.dumps(result, sort_keys=True, indent=2)+'\n').encode()
    if args.write:
        args.write.write_bytes(raw)
    if args.check:
        need(result == json.loads(args.check.read_bytes()), 'independent receipt mismatch')
    print(json.dumps({'ok': True, 'original_unions': len(result['original_unions']),
                      'original_products': len(result['original_products'])+len(result['original_common_core_products']),
                      'improved_unique_unions': len(result['improved_unique_unions']),
                      'extra_examples': len(result['new_boundary_and_many_petal_examples']),
                      'maximum_petal_count': max(x['r'] for x in result['new_boundary_and_many_petal_examples']),
                      'rejected_controls': result['rejected_controls'], 'expected_sha256': sha256(raw).hexdigest()}, sort_keys=True))


if __name__ == '__main__':
    main()
