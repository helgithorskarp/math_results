"""Independent constraint encoding from every literal four-vertex set.

Fixed-order search, unlike forward-domain propagation. No decomposition into
mixed clique types is used to generate constraints; all 4-sets are inspected.
"""
from itertools import combinations


def search(H, B, threshold=56, stop=False, minimum=6, maximum=8):
    n, m = len(H), len(B)
    root = n + m
    # For each monochromatic possibility, store the required cross-edge bits
    # grouped by H row. Any two fixed edges of different colors discharge it.
    clauses = set()
    for S in combinations(range(root + 1), 4):
        fixed = set()
        row_masks = {}
        for a, b in combinations(S, 2):
            if a < n <= b < root:
                row_masks[a] = row_masks.get(a, 0) | (1 << (b - n))
            elif b == root:
                fixed.add(a < n)
            elif b < n:
                fixed.add(bool(H[a] >> b & 1))
            else:
                fixed.add(bool(B[a - n] >> (b - n) & 1))
        if len(fixed) > 1:
            continue
        if not row_masks:
            raise ValueError('fixed monochromatic four-set')
        for color in fixed or (False, True):
            clauses.add((color, tuple(sorted(row_masks.items()))))
    unary = [[] for _ in range(n)]
    pairs = {}
    long = [[] for _ in range(n)]
    for color, masks in sorted(clauses):
        if len(masks) == 1:
            row, mask = masks[0]
            unary[row].append((color, mask))
        elif len(masks) == 2:
            (i, s), (j, t) = masks
            pairs.setdefault((i, j), []).append((color, s, t))
        else:
            mask = sum(s << (i * m) for i, s in masks)
            long[masks[-1][0]].append((color, mask))
    domains = [[s for s in range(1 << m)
                if minimum <= 1 + H[i].bit_count() + s.bit_count() <= maximum
                and not any((s & t == t) if red else (s & t == 0) for red, t in unary[i])]
               for i in range(n)]
    # Tables come only from the literal clauses, not the production predicates.
    compatibility = {}
    cache = {}
    for pair, constraints in pairs.items():
        key = tuple(constraints)
        if key not in cache:
            cache[key] = [[not any(((s & a == a) and (t & b == b)) if red
                                   else ((s & a == 0) and (t & b == 0))
                                   for red, a, b in constraints)
                           for t in range(1 << m)] for s in range(1 << m)]
        compatibility[pair] = cache[key]
    need = threshold - n - sum(x.bit_count() for x in H) // 2 - sum(x.bit_count() for x in B) // 2
    maxs = [max((s.bit_count() for s in d), default=-100) for d in domains]
    suffix = [sum(maxs[i:]) for i in range(n + 1)]
    low = [minimum - x.bit_count() for x in B]
    high = [maximum - x.bit_count() for x in B]
    nodes = [0] * (n + 1)
    solutions = []

    def visit(rows, columns, total, bits):
        i = len(rows)
        nodes[i] += 1
        if total + suffix[i] < need:
            return False
        if i == n:
            if total >= need and all(columns[b] >= low[b] for b in range(m)):
                solutions.append(tuple(rows))
                return stop
            return False
        for s in domains[i]:
            newtotal = total + s.bit_count()
            if newtotal + suffix[i + 1] < need:
                continue
            newcols = [columns[b] + int(s >> b & 1) for b in range(m)]
            if any(newcols[b] > high[b] or newcols[b] + n - i - 1 < low[b] for b in range(m)):
                continue
            if any((j, i) in compatibility and not compatibility[j, i][t][s]
                   for j, t in enumerate(rows)):
                continue
            newbits = bits | (s << (i * m))
            if any((newbits & mask == mask) if red else (newbits & mask == 0)
                   for red, mask in long[i]):
                continue
            if visit(rows + [s], newcols, newtotal, newbits):
                return True
        return False

    visit([], [0] * m, 0, 0)
    return {'nodes': nodes, 'solutions': sorted(solutions),
            'domains': list(map(len, domains)), 'need': need,
            'literal_four_sets': len(list(combinations(range(root + 1), 4))),
            'distinct_forbidden_patterns': len(clauses)}
