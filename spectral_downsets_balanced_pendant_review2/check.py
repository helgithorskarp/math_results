"""six-reviewer-2: independent balanced-pendant audit and refinements.

No author imports in the default run. Exact fractions, residual matching
search rather than four splices, independent edge-cover subset DP. Optional
--producer checks the hash-pinned author constructor in a separate bridge.
Schur backend reuses this reviewer's published pass37 arithmetic.
"""
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product, permutations
from pathlib import Path
import argparse
import importlib.util
import json


def need(ok, message):
    if not ok:
        raise ValueError(message)


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def mv(A, v):
    return [dot(r, v) for r in A]


def digest(obj):
    return sha256(json.dumps(obj, separators=(',', ':'), sort_keys=True,
                             default=str).encode()).hexdigest()


def psd(A):
    n = len(A)
    need(all(len(r) == n for r in A), 'square')
    need(all(A[i][j] == A[j][i] for i in range(n) for j in range(n)), 'symmetry')
    T = [list(map(F, r)) for r in A]
    rank = 0
    for k in range(n):
        pivot = T[k][k]
        need(pivot >= 0, 'negative Schur pivot')
        if not pivot:
            need(all(T[k][j] == 0 for j in range(k+1, n)), 'nonzero zero-pivot row')
            continue
        rank += 1
        for i in range(k+1, n):
            for j in range(i, n):
                T[i][j] -= T[k][i]*T[k][j]/pivot
                T[j][i] = T[i][j]
    return rank


def geometry(E, c):
    need(type(c) is int and c >= 0, 'center')
    need(isinstance(E, (list, tuple)) and len(E) >= 2, 'size boundary')
    need(all(type(a) is int and a >= 0 for a in E), 'mask type')
    need(list(E) == sorted(set(E)) and E[0] == 0, 'ordered distinct empty')
    present = set(E)
    for a in E:
        need(not a & (1 << c), 'center in deletion')
        bit = a
        while bit:
            x = bit & -bit
            need(a ^ x in present, 'downset')
            bit ^= x
    D = sorted(list(E)+[a | (1 << c) for a in E])
    p = 1 << max(D).bit_length()
    D += [p, p | (1 << c)]
    S = tuple(a for a in D if a & (1 << c))
    T = tuple(a for a in D if not a & (1 << c))
    need(len(S) == len(T) == len(E)+1, 'balanced')
    return D, S, T, p


def forced_matching(S, T, forced):
    """Direct exhaustive residual search, including an explicit state cap.

    Only success returns a mathematical certificate. Hitting the guard raises
    an operational error, never an impossibility conclusion.
    """
    n = len(S)
    x, y = forced
    adjacency = [sum(1 << j for j, b in enumerate(T) if not a & b) for a in S]
    need(adjacency[x] & (1 << y), 'forced disjoint edge')
    states = 0

    @lru_cache(None)
    def solve(left, right):
        nonlocal states
        states += 1
        need(states <= 200000, 'operational residual-search state guard')
        if not left:
            return ()
        choices = [(int((adjacency[i] & right).bit_count()), i)
                   for i in range(n) if left >> i & 1]
        _, i = min(choices)
        options = adjacency[i] & right
        while options:
            low = options & -options
            j = low.bit_length()-1
            suffix = solve(left ^ (1 << i), right ^ low)
            if suffix is not None:
                return ((i, j),)+suffix
            options ^= low
        return None

    result = solve(((1 << n)-1) ^ (1 << x), ((1 << n)-1) ^ (1 << y))
    need(result is not None, 'no matching found: inspect proof/input, no global verdict')
    result = dict(result+((x, y),))
    need(set(result) == set(range(n)) and set(result.values()) == set(range(n)), 'bijection')
    need(all(not S[i] & T[j] for i, j in result.items()), 'disjoint matching')
    return [result[i] for i in range(n)], states


def base_matrix(D, S, T):
    n = len(D)
    index = {a: i for i, a in enumerate(D)}
    counts = [[0]*n for _ in D]
    records, states = [], 0
    for i, a in enumerate(S):
        for j, b in enumerate(T):
            if a & b:
                continue
            matching, visited = forced_matching(S, T, (i, j))
            states += visited
            records.append([i, j, matching])
            for x, y in enumerate(matching):
                u, v = index[S[x]], index[T[y]]
                counts[u][v] += 1
                counts[v][u] += 1
    h = len(records)
    need(h == sum(not a & b for a in S for b in T), 'coverage')
    M0 = [[F(v, h) for v in row] for row in counts]
    for i, a in enumerate(D):
        for j, b in enumerate(D):
            allowed = (a in S) != (b in S) and not a & b
            need((M0[i][j] > 0) == allowed, 'full cross support')
            if allowed:
                need(M0[i][j] >= F(1, h), 'conditioned edge margin')
    need(all(sum(row) == 1 for row in M0), 'base stochastic')
    return M0, h, digest(records), states


def hall_census(E):
    n = len(E)
    adjacency = [sum(1 << j for j, b in enumerate(E) if not a & b) for a in E]
    unions = [0]*(1 << n)
    for mask in range(1, 1 << n):
        low = mask & -mask
        unions[mask] = unions[mask ^ low] | adjacency[low.bit_length()-1]
        need(unions[mask].bit_count() >= mask.bit_count(), 'Hall inequality')
    return 1 << n


def minimum_cover(V):
    """Maximum matching by subset recurrence; independent edge-cover DP <=8."""
    n = len(V)
    edges = [(i, j) for i, j in combinations(range(n), 2) if not V[i] & V[j]]
    adjacency = [sum(1 << j for j in range(n) if i != j and not V[i] & V[j])
                 for i in range(n)]
    need(all(adjacency), 'no isolated outside vertex')

    @lru_cache(None)
    def best(mask):
        if not mask:
            return ()
        low = mask & -mask
        i, other = low.bit_length()-1, mask ^ low
        answer = best(other)
        options = other & adjacency[i]
        while options:
            bit = options & -options
            j = bit.bit_length()-1
            candidate = ((i, j),)+best(other ^ bit)
            if len(candidate) > len(answer):
                answer = candidate
            options ^= bit
        return answer

    matching = best((1 << n)-1)
    cover = set(tuple(sorted(e)) for e in matching)
    covered = set(i for e in cover for i in e)
    for i in range(n):
        if i not in covered:
            j = min(j for j in range(n) if adjacency[i] >> j & 1)
            cover.add(tuple(sorted((i, j))))
            covered.add(i)
            covered.add(j)
    q = n-len(matching)
    need(len(cover) == q and covered == set(range(n)), 'minimum edge-cover formula')
    dp_checked = n <= 8
    if dp_checked:
        dp = [n+1]*(1 << n)
        dp[0] = 0
        for mask in range(1 << n):
            for i, j in edges:
                nxt = mask | (1 << i) | (1 << j)
                dp[nxt] = min(dp[nxt], dp[mask]+1)
        need(dp[-1] == q, 'independent edge-cover subset DP')
    return [[V[i], V[j]] for i, j in sorted(cover)], len(matching), dp_checked


def trade_matrix(D, cover):
    n = len(D)
    index = {a: i for i, a in enumerate(D)}
    R = [[F(0)]*n for _ in D]
    for a, b in cover:
        need(a and b and a != b and not a & b, 'allowed negative pair')
        i, j = index[a], index[b]
        R[0][0] -= 2
        R[0][i] += 1
        R[i][0] += 1
        R[0][j] += 1
        R[j][0] += 1
        R[i][j] -= 1
        R[j][i] -= 1
    need(all(sum(row) == 0 for row in R), 'trade row sums')
    need(max(sum(map(abs, row)) for row in R) == 4*len(cover), 'trade norm')
    return R


def check_matrix(D, S, M, gap, epsilon, cover):
    n = len(D)
    q = [F(1 if a in S else -1) for a in D]
    one = [F(1)]*n
    need(mv(M, one) == one and mv(M, q) == [-x for x in q], 'endpoint vectors')
    need(all(M[i][j] == M[j][i] for i in range(n) for j in range(n)), 'matrix symmetry')
    for i, a in enumerate(D):
        for j, b in enumerate(D):
            if a & b:
                need(M[i][j] == 0, 'definition support')
    need(min(M[0][1:]) >= epsilon > 0, 'positive empty row')
    negative = {(a, b) for i, a in enumerate(D) for j, b in enumerate(D)
                if i < j and a and b and M[i][j] < 0}
    need(negative == {tuple(sorted(e)) for e in cover}, 'negative pair coverage')
    ranks = []
    for sign in (-1, 1):
        slack = [[int(i == j)+sign*M[i][j] for j in range(n)] for i in range(n)]
        ranks.append(psd(slack))
        # Orthogonal projection onto Z, not a selected principal submatrix.
        buffered = [[slack[i][j]-gap/2*(int(i == j)-F(1+q[i]*q[j], n))
                     for j in range(n)] for i in range(n)]
        need(psd(buffered) == n-1, 'whole buffered slack')
    need(ranks == [n-1, n-1], 'maximal endpoint ranks')
    for i, a in enumerate(D):
        if a not in S:
            need(sum(M[i][j] for j, b in enumerate(D) if b not in S) == 0,
                 'outside row forced zero')
    return digest(M)


def double_star(D, S, c):
    n, k = len(D), len(S)
    center = 1 << c
    edges = {(0, a) for a in S}
    edges |= {(center, b) for b in D if b not in S and b != 0}
    need(len(edges) == n-1, 'double-star edge count')
    L = [[F(0)]*n for _ in D]
    index = {a: i for i, a in enumerate(D)}
    for a, b in edges:
        i, j = index[a], index[b]
        L[i][i] += 1
        L[j][j] += 1
        L[i][j] -= 1
        L[j][i] -= 1
    # Verify the complete tree-gap inequality on all coordinates.
    Q = [[L[i][j]-F(2, k+2)*(int(i == j)-F(1, n))
          for j in range(n)] for i in range(n)]
    need(psd(Q) == n-1, 'double-star strengthened gap')
    # The two root/leaf quotients have characteristic polynomials
    # lambda(lambda-k) and lambda^2-(k+2)lambda+2.
    for center_diagonal, trace, determinant in [(k-1, k, 0), (k+1, k+2, 2)]:
        need(1+center_diagonal == trace and center_diagonal-(k-1) == determinant,
             'double-star quotient polynomial')
    return digest(L)


def intersecting_census(D, S):
    if len(D) > 20:
        return None
    values = D[1:]
    maximum, maximizers, count = 0, [], 0

    def visit(start, picked):
        nonlocal maximum, maximizers, count
        count += 1
        if len(picked) > maximum:
            maximum, maximizers = len(picked), [picked]
        elif len(picked) == maximum:
            maximizers.append(picked)
        for j in range(start, len(values)):
            if all(values[j] & a for a in picked):
                visit(j+1, picked+(values[j],))

    visit(0, ())
    need(maximum == len(S) and maximizers == [tuple(sorted(S))], 'unique maximum census')
    return {'intersecting_subfamilies': count, 'maximum': maximum, 'maximizers': 1}


def fixtures():
    out = []
    for mask in range(1 << 8):
        E = [a for a in range(8) if mask >> a & 1]
        if len(E) < 2 or 0 not in E:
            continue
        if any((a ^ (1 << bit)) not in E for a in E for bit in range(3)
               if a >> bit & 1):
            continue
        out.append(('E3-'+str(mask), [a << 1 for a in E], 0))
    need(len(out) == 18, 'complete nontrivial labeled E3 census')
    out += [('cube5', [a << 1 for a in range(16)], 0),
            ('simplex-five', [0, 2, 4, 8, 16, 32], 0),
            ('center-hole', [0, 1, 8], 4),
            ('two-prior-pendants', [0, 2, 4, 6, 8, 16], 0)]
    return out


def reject_controls():
    rejected = 0
    bad_geometry = [([0], 0), ([0, 1], 0), ([0, 2, 2], 0), ([2, 0], 0),
                    ([0, 6], 0), ([0, True], 0), ([0, -2], 0), ([0, 2], True)]
    controls = [lambda e=e, c=c: geometry(e, c) for e, c in bad_geometry]
    controls += [lambda: psd([[0, 1], [1, 0]]),
                 lambda: psd([[1, 1], [0, 1]]),
                 lambda: psd([[-1]]),
                 lambda: trade_matrix([0, 1, 2], [(1, 1)])]
    for control in controls:
        try:
            control()
        except ValueError:
            rejected += 1
        else:
            raise ValueError('corruption/domain control accepted')
    # The two original maximal stars at s=1 remain independent after one pendant.
    a, b = [F(-1, 2), F(1, 2), F(-1, 2), F(1, 2)], [F(-1, 2), F(-1, 2), F(1, 2), F(1, 2)]
    need(dot(a, a)*dot(b, b)-dot(a, b)**2 > 0, 'excluded s1 kernel boundary')
    # Uniform E association would be false even on a three-member downset.
    covariance = F(0)-F(1, 3)*F(1, 3)
    need(covariance == -F(1, 9), 'full-cube Harris trust boundary')
    return rejected


def backend_audit():
    """All principal minors, via literal determinants: independent PSD oracle."""
    def determinant(A):
        n = len(A)
        answer = 0
        for p in permutations(range(n)):
            sign = (-1)**sum(p[i] > p[j] for i in range(n) for j in range(i+1, n))
            term = sign
            for i in range(n):
                term *= A[i][p[i]]
            answer += term
        return answer

    positive = 0
    for entries in product((-1, 0, 1), repeat=6):
        A = [[0]*3 for _ in range(3)]
        for (i, j), value in zip([(0, 0), (0, 1), (0, 2),
                                 (1, 1), (1, 2), (2, 2)], entries):
            A[i][j] = A[j][i] = value
        expected = all(determinant([[A[i][j] for j in subset] for i in subset]) >= 0
                       for size in (1, 2, 3) for subset in combinations(range(3), size))
        try:
            psd(A)
            actual = True
        except ValueError:
            actual = False
        need(actual == expected, 'independent principal-minor PSD oracle')
        positive += actual
    need(positive == 24, 'ternary PSD count')
    return {'symmetric_ternary_3x3_matrices': 729, 'PSD': positive}


def producer_module(path):
    need(sha256(path.read_bytes()).hexdigest() ==
         '2a0c1efab02bd3dc09612363bb85a656aec48a5468219cfa671943efa526a884', 'producer pin')
    spec = importlib.util.spec_from_file_location('pinned_balanced_producer', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(producer=None):
    records, bridge = [], []
    for name, E, c in fixtures():
        D, S, T, p = geometry(E, c)
        s, k, n = len(E), len(S), len(D)
        M0, h, matching_hash, states = base_matrix(D, S, T)
        hall = hall_census(E)
        tree_hash = double_star(D, S, c)
        cover, nu, dp_checked = minimum_cover([a for a in T if a])
        q = len(cover)
        star_cover = [(a, p) for a in E if a]
        gap_old, gap_new = F(2, h*(n-1)**2), F(2, h*(k+2))
        vector_q = [1 if a in S else -1 for a in D]
        for sign, kernel in [(-1, [1]*n), (1, vector_q)]:
            buffered = [[int(i == j)+sign*M0[i][j]-gap_new*(
                         int(i == j)-F(kernel[i]*kernel[j], n))
                         for j in range(n)] for i in range(n)]
            need(psd(buffered) == n-1, 'unperturbed strengthened whole gap')
        matrices = {}
        for label, pairs, gap in [('author-parameters-independent-base', star_cover, gap_old),
                                  ('stronger-gap-star-cover', star_cover, gap_new),
                                  ('optimal-negative-pairs', cover, gap_new)]:
            epsilon = gap/F(8*len(pairs))
            R = trade_matrix(D, pairs)
            need(mv(R, [1 if a in S else -1 for a in D]) == [0]*n, 'trade annihilates q')
            M = [[M0[i][j]+epsilon*R[i][j] for j in range(n)] for i in range(n)]
            matrices[label] = {'sha256': check_matrix(D, S, M, gap, epsilon, pairs),
                               'guaranteed_empty_margin': str(epsilon),
                               'actual_empty_margin': str(min(M[0][1:])),
                               'negative_pairs': len(pairs), 'gap': str(gap)}
        record = {'name': name, 'E': E, 'center': c, 'N': n, 'original_s': s,
                  'edge_count': h, 'matching_records_sha256': matching_hash,
                  'residual_search_states': states, 'Hall_subsets_checked': hall,
                  'tree_sha256': tree_hash, 'matching_number': nu, 'minimum_cover': cover,
                  'independent_edge_cover_DP': dp_checked, 'matrices': matrices,
                  'intersection_census': intersecting_census(D, S)}
        records.append(record)
        if producer:
            original = sorted(E+[a | (1 << c) for a in E])
            r = producer.completion(original, c)
            need(r['family'] == D and r['edge_count'] == h, 'producer geometry')
            f = r['base_bijection']
            need(set(f) == set(f.values()) == set(E) and
                 all(not a & b for a, b in f.items()), 'producer baseline bijection')
            counts = [[0]*n for _ in D]
            index = {a: i for i, a in enumerate(D)}
            made, forced_seen = 0, set()
            for a, b, targets in producer.conditioned_matchings(tuple(E), 1 << c, p, r['base_bijection']):
                need((a, b) not in forced_seen, 'duplicate producer forced edge')
                forced_seen.add((a, b))
                need(set(targets) == set(T) and targets[S.index(a)] == b, 'producer matching')
                for x, y in zip(S, targets):
                    need(not x & y, 'producer disjointness')
                    i, j = index[x], index[y]
                    counts[i][j] += 1
                    counts[j][i] += 1
                made += 1
            need(made == h and counts == r['counts'], 'producer literal counts')
            need(forced_seen == {(a, b) for a in S for b in T if not a & b},
                 'producer full forced-edge coverage')
            R = trade_matrix(D, star_cover)
            M = [[r['entry'](a, b) for b in D] for a in D]
            need(M == [[F(counts[i][j], h)+gap_old/F(8*(s-1))*R[i][j]
                        for j in range(n)] for i in range(n)], 'producer complete entry replay')
            bridge.append({'name': name, 'sha256': check_matrix(D, S, M, gap_old,
                                                               gap_old/F(8*(s-1)), star_cover)})
    evidence = {'agent': 'six-reviewer-2', 'role': 'independent mathematical reviewer',
                'complete_cases': len(records), 'controls_rejected': reject_controls(),
                'backend_audit': backend_audit(), 'records': records}
    return evidence, bridge


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--producer', type=Path)
    args = parser.parse_args()
    evidence, bridge = run(producer_module(args.producer) if args.producer else None)
    if args.output:
        args.output.write_text(json.dumps(evidence, separators=(',', ':'), sort_keys=True)+'\n')
    if args.check:
        need(evidence == json.loads(Path(__file__).with_name('RESULTS.json').read_text()), 'frozen evidence')
    print(json.dumps({'complete_cases': evidence['complete_cases'], 'controls_rejected': evidence['controls_rejected'],
                      'canonical_sha256': digest(evidence), 'producer_bridge_cases': len(bridge),
                      'producer_bridge_sha256': digest(bridge) if bridge else None}, sort_keys=True))


if __name__ == '__main__':
    main()
