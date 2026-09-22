"""Construct optimal toggle words for bounded posets of height at most three.

Python 3.11+, standard library. See PROOF.md for the universal theorem.
This module constructs words; verify.py checks them from the game definition.
"""

from collections import deque


def compile_incidence(m, neighborhoods):
    """Return a word for the incidence poset with m >= 1 coatoms.

    neighborhoods[a] is a nonempty iterable of distinct indices in range(m).
    Labels: bottom 0; atoms 1,...,a; coatoms a+1,...,a+m; top a+m+1.
    Isolated coatoms are allowed. Latticehood is not required.
    """
    if type(m) is not int or m < 1:
        raise ValueError("m must be a positive integer")
    rows = []
    for row in neighborhoods:
        row = tuple(row)
        if not row or any(type(c) is not int or c < 0 or c >= m for c in row):
            raise ValueError("every atom must have valid coatom neighbors")
        if len(set(row)) != len(row):
            raise ValueError("repeated incidence")
        rows.append(frozenset(row))
    a = len(rows)
    neighbors = [set() for _ in range(m)]
    for v, row in enumerate(rows, start=1):
        for c in row:
            neighbors[c].add(v)

    # BFS in the incidence graph gives a connected coatom ordering.
    seen_c, seen_a, orders = set(), set(), []
    for seed in range(m):
        if seed in seen_c:
            continue
        queue, order = deque([seed]), []
        seen_c.add(seed)
        while queue:
            c = queue.popleft()
            order.append(c)
            for v in sorted(neighbors[c]):
                if v in seen_a:
                    continue
                seen_a.add(v)
                for d in sorted(rows[v - 1]):
                    if d not in seen_c:
                        seen_c.add(d)
                        queue.append(d)
        orders.append(order)

    # A zero in these provisional words is a bottom ADDITION slot.
    # Its permission in the full poset is checked only after all splicing.
    clusters = []
    for order in orders:
        covered = set(neighbors[order[0]])
        word = [a + 1 + order[0]]
        for c in order[1:]:
            shared = sorted(neighbors[c] & covered)
            if not shared:
                raise RuntimeError("disconnected coatom ordering")
            for i, v in enumerate(shared):
                if i:
                    word.append(0)
                word.append(v)
            word.append(a + 1 + c)
            covered.update(neighbors[c])
        clusters.append(word)

    # Merge two private components by replacing one addition slot.
    while len(clusters) > 1:
        host = next((i for i, word in enumerate(clusters) if 0 in word), None)
        if host is None:
            break
        donor = len(clusters) - 1 if host != len(clusters) - 1 else 0
        inserted = clusters.pop(donor)
        if donor < host:
            host -= 1
        word = clusters[host]
        k = word.index(0)
        clusters[host] = word[:k] + inserted + word[k + 1:]

    # If several clusters survive, they have no addition slots. The zeros
    # introduced here are bottom REMOVALS between completed clusters.
    result = []
    for i, word in enumerate(clusters):
        if i:
            result.append(0)
        result.extend(word)
    return result


def compile_poset(order):
    """Accept a Boolean reflexive order matrix on arbitrary labels 0,...,n-1.

    Reject a malformed, unbounded, or height-greater-than-three order.
    The clarity-first validation costs O(n^3); no search of game states is used.
    """
    n = len(order)
    if not n or any(len(row) != n for row in order):
        raise ValueError("nonempty square order matrix required")
    if any(type(entry) is not bool for row in order for entry in row):
        raise ValueError("order entries must be Boolean")
    if any(not order[v][v] for v in range(n)):
        raise ValueError("order is not reflexive")
    if any(order[v][w] and order[w][v] for v in range(n) for w in range(v + 1, n)):
        raise ValueError("order is not antisymmetric")
    if any(order[u][v] and order[v][w] and not order[u][w]
           for u in range(n) for v in range(n) for w in range(n)):
        raise ValueError("order is not transitive")
    bottoms = [v for v in range(n) if all(order[v])]
    tops = [v for v in range(n) if all(order[u][v] for u in range(n))]
    if len(bottoms) != 1 or len(tops) != 1:
        raise ValueError("unique bottom and top required")
    bottom, top = bottoms[0], tops[0]
    if n == 1:
        return []
    if n == 2:
        return [bottom]
    interior = [v for v in range(n) if v not in (bottom, top)]
    coatoms = [v for v in interior
               if not any(v != w and order[v][w] for w in interior)]
    atoms = [v for v in interior if v not in coatoms]
    if any(v != w and order[v][w] for v in atoms for w in atoms):
        raise ValueError("height exceeds three")
    rows = [[i for i, c in enumerate(coatoms) if order[v][c]] for v in atoms]
    labels = [bottom] + atoms + coatoms + [top]
    return [labels[v] for v in compile_incidence(len(coatoms), rows)]
