"""One-pendant capped, maximal-rank H completion for |D|=2s, s>=2.

Exact rational construction; see BALANCED_PENDANT_COMPLETION.md.  The
constructor retains O(s^2) integers and uses O(s^3) matching-count work.
The bounded dense helper is for finite validation, not an all-order proof.
"""
from collections import deque
from fractions import Fraction as F


def require(condition, message):
    if not condition:
        raise ValueError(message)


def geometry(family, center):
    require(isinstance(family, (list, tuple)) and len(family) >= 2,
            "Nontrivial finite family required")
    require(all(isinstance(a, int) and not isinstance(a, bool) and a >= 0
                for a in family), "Nonnegative integer set masks required")
    require(list(family) == sorted(set(family)) and family[0] == 0,
            "Sorted distinct masks including empty required")
    present = set(family)
    for a in family:
        bits = a
        while bits:
            bit = bits & -bits
            require(a ^ bit in present, "Family is not a downset")
            bits ^= bit
    require(isinstance(center, int) and not isinstance(center, bool)
            and 0 <= center < max(family).bit_length(), "Bad center")
    c = 1 << center
    E = tuple(a for a in family if not a & c)
    s = sum(bool(a & c) for a in family)
    require(len(family) == 2 * s and s >= 2,
            "Balanced chosen star of size at least two required")
    require(present == set(E) | {a | c for a in E},
            "Balanced deletion bijection failed")
    return E, c, 1 << max(family).bit_length()


def disjoint_bijection(E):
    """Deterministic augmenting paths; Hall/Harris proves existence for E.

    A failure raises an exception; it is never reported as nonexistence.
    No recursion, random choice, floating arithmetic or external solver.
    """
    order = sorted(E, key=lambda a: (-a.bit_count(), a))
    neighbors = {a: tuple(b for b in E if not a & b) for a in E}
    left, right = {}, {}
    for root in order:
        queue = deque([root])
        seen_left, predecessor = {root}, {}
        free = None
        while queue and free is None:
            a = queue.popleft()
            for b in neighbors[a]:
                if b in predecessor:
                    continue
                predecessor[b] = a
                if b not in right:
                    free = b
                    break
                other = right[b]
                if other not in seen_left:
                    seen_left.add(other)
                    queue.append(other)
        require(free is not None, "Incomplete matching: implementation/input failure")
        b = free
        while True:
            a = predecessor[b]
            old = left.get(a)
            left[a], right[b] = b, a
            if old is None:
                break
            b = old
    require(set(left) == set(E) and set(left.values()) == set(E)
            and all(not a & b for a, b in left.items()), "Bad disjoint bijection")
    return left


def conditioned_matchings(E, c, p, f):
    """For each allowed S/T edge yield one perfect matching containing it.

    Matching targets are ordered by old left vertices c|E, then c|p.
    """
    inverse = {b: a for a, b in f.items()}
    for A in E:
        for B in E:
            if A & B:
                continue
            g = dict(f)
            if B != f[A]:
                C = inverse[B]
                g[A], g[C], spoke = B, p, f[A]
            else:
                C = next(x for x in E if x != A)
                g[C], spoke = p, f[C]
            yield A | c, B, tuple(g[x] for x in E) + (spoke,)
        g = dict(f)
        g[A] = p
        yield A | c, p, tuple(g[x] for x in E) + (f[A],)
    for B in E:
        g = dict(f)
        g[inverse[B]] = p
        yield c | p, B, tuple(g[x] for x in E) + (B,)


def completion(family, center):
    E, c, p = geometry(family, center)
    s, k = len(E), len(E) + 1
    augmented = sorted(list(family) + [p, c | p])
    N = len(augmented)
    S, T = tuple(a | c for a in E) + (c | p,), E + (p,)
    h = sum(not a & b for a in S for b in T)
    f = disjoint_bijection(E)
    ix = {a: i for i, a in enumerate(augmented)}
    counts = [[0] * N for _ in augmented]
    made = 0
    for a, b, targets in conditioned_matchings(E, c, p, f):
        require(len(targets) == k and set(targets) == set(T),
                "Conditioned matching is not a bijection")
        require(targets[S.index(a)] == b, "Required matching edge missing")
        for x, y in zip(S, targets):
            require(not x & y, "Intersecting matching edge")
            i, j = ix[x], ix[y]
            counts[i][j] += 1
            counts[j][i] += 1
        made += 1
    require(made == h, "Incomplete allowed-edge coverage")
    epsilon = F(1, 4 * h * (s - 1) * (N - 1) ** 2)
    gap = F(2, h * (N - 1) ** 2)
    old_nonempty = set(E) - {0}

    def trade(a, b):
        if a == b == 0:
            return -2 * (s - 1)
        if (a == 0 and b == p) or (b == 0 and a == p):
            return s - 1
        if (a == 0 and b in old_nonempty) or (b == 0 and a in old_nonempty):
            return 1
        if (a == p and b in old_nonempty) or (b == p and a in old_nonempty):
            return -1
        return 0

    def entry(a, b):
        require(a in ix and b in ix, "Entry outside augmented family")
        return F(counts[ix[a]][ix[b]], h) + epsilon * trade(a, b)

    return dict(family=augmented, original_family=list(family), center=center,
                original_s=s, s=k, N=N, E=E, S=S, T=T, fresh=p,
                base_bijection=f, edge_count=h, counts=counts,
                epsilon=epsilon, gap=gap, entry=entry)


def dense_entries(record, limit=64):
    require(record['N'] <= limit, "Dense validation exceeds explicit size limit")
    return [[record['entry'](a, b) for b in record['family']]
            for a in record['family']]
