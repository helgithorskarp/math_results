"""Literal modular-triple encoder and small truth-table audit; no fast encoder imports."""
import itertools


def literal_encoding(p, generator):
    h = {x for x in range(1, p) if pow(x, 20, p) == 1}
    if len(h) != 20:
        raise ValueError("wrong subgroup")
    blocks, remaining = [], set(range(1, p))
    while remaining:
        block = {min(remaining) * a % p for a in h}
        blocks.append(block)
        remaining -= block
    owner, colours, inverse = {}, {}, {}
    permutation = [1, 2, 3, 4, 0, 5]
    for i, block in enumerate(blocks):
        x, row = min(block), list(range(6))
        for _ in range(20):
            if x in owner:
                raise ValueError("multiplier cycle repeated early")
            owner[x], colours[x] = i, row[:]
            inv = [None] * 6
            for a, c in enumerate(row):
                inv[c] = a
            inverse[x] = inv
            x = generator * x % p
            row = [permutation[c] for c in row]
        if x != min(block) or row != list(range(6)):
            raise ValueError("multiplier action does not close")
    clauses = set()
    for i in range(len(blocks)):
        clauses.add(tuple(6 * i + a + 1 for a in range(6)))
        for a in range(6):
            for b in range(a + 1, 6):
                clauses.add((-6 * i - a - 1, -6 * i - b - 1))
    pairs = 0
    for x in range(1, p):
        for y in range(x, p):
            z = (x + y) % p
            if z == 0:
                continue
            pairs += 1
            for c in range(6):
                requirements = [(owner[w], inverse[w][c]) for w in (x, y, z)]
                if any(i == j and a != b for i, a in requirements for j, b in requirements):
                    continue
                clauses.add(tuple(sorted({-6 * i - a - 1 for i, a in requirements})))
    clauses.add((1,))
    return sorted(clauses), blocks, owner, colours, pairs


def small_truth_tables(fast_encoder):
    reports = []
    for p, generator in [(41, 36), (61, 8)]:
        clauses, blocks, owner, colours, pairs = literal_encoding(p, generator)
        fast, _, _ = fast_encoder(p, generator)
        if fast != clauses:
            raise ValueError("small full-CNF disagreement")
        satisfying = []
        checked = 0
        for states in itertools.product(range(6), repeat=len(blocks)):
            palette = {x: colours[x][states[owner[x]]] for x in range(1, p)}
            valid = states[0] == 0 and all(
                (x + y) % p == 0 or palette[x] != palette[y]
                or palette[x] != palette[(x + y) % p]
                for x in range(1, p) for y in range(x, p)
            )
            def truth(lit):
                i, a = divmod(abs(lit) - 1, 6)
                equal = states[i] == a
                return equal if lit > 0 else not equal
            encoded = all(any(truth(lit) for lit in c) for c in clauses)
            if valid != encoded:
                raise ValueError("truth-table mismatch")
            if valid:
                satisfying.append(states)
            checked += 1
        reports.append({"p": p, "assignments": checked, "satisfying": len(satisfying)})
    return reports
