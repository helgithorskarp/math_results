#!/usr/bin/env python3
"""Graph6 and direct physical K5 interpretation, independent of C++ production."""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path

CATALOG_SHA = "067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb"


def require(test, message):
    if not test:
        raise ValueError(message)


def decode(record):
    require(record and all(63 <= ord(ch) <= 126 for ch in record), "Bad graph6 bytes")
    n = ord(record[0]) - 63
    require(4 <= n <= 42, "Unsupported graph6 core order")
    bits = "".join(f"{ord(ch)-63:06b}" for ch in record[1:])
    require(len(bits) == ((n * (n - 1) // 2 + 5) // 6) * 6, "graph6 length")
    require(not any(ch == "1" for ch in bits[n*(n-1)//2:]), "graph6 padding")
    graph = [[0]*n for _ in range(n)]
    for v in range(1, n):
        for u in range(v):
            graph[u][v] = graph[v][u] = int(bits[v*(v-1)//2+u])
    return graph


def catalog(path):
    raw = Path(path).read_bytes()
    require(sha256(raw).hexdigest() == CATALOG_SHA, "Catalog hash mismatch")
    records = raw.decode("ascii").splitlines()
    require(len(records) == 328 and len(set(records)) == 328, "Catalog record count")
    require(all(len(decode(row)) == 42 for row in records), "Catalog order")
    return records


def rows(path, variables):
    text = Path(path).read_text().splitlines()
    header = text[0].split()
    require(len(header) == 4 and header[:2] == ["p", "cnf"], "DIMACS header")
    require(int(header[2]) == variables and int(header[3]) == len(text)-1, "DIMACS dimensions")
    result = []
    for line in text[1:]:
        values = tuple(map(int, line.split()))
        require(values and values[-1] == 0 and all(1 <= abs(x) <= variables for x in values[:-1]),
                "DIMACS literal")
        row = frozenset(values[:-1])
        require(len(row) == len(values)-1 and len({abs(x) for x in row}) == len(row), "Duplicate/polarity")
        result.append(row)
    require(len(set(result)) == len(result), "Duplicate clauses")
    return set(result)


def check_physical(graph, clauses):
    """Each input clause must directly prohibit a single physical monochromatic K5."""
    n = len(graph)
    counts = Counter()
    for clause in clauses:
        bits = {abs(lit): int(lit < 0) for lit in clause}
        spin = {v: bit for v, bit in bits.items() if v < n}
        external = {v-n: bit for v, bit in bits.items() if v >= n}
        if external:
            require(len(external) == 4 and all(0 <= v < n for v in external), "Not one added K5")
            vertices = sorted(external)
            require(set(spin) == set(vertices)-{0}, "Wrong switches for added-edge clause")
            require(len(set(external.values())) == 1, "Added colors disagree")
            colors = set(external.values())
        else:
            require(len(spin) in (4, 5), "Not a core K5")
            vertices = sorted(spin) if len(spin) == 5 else [0] + sorted(spin)
            colors = set()
        spin[0] = 0
        colors.update(graph[u][v] ^ spin[u] ^ spin[v] for u, v in combinations(vertices, 2))
        require(len(colors) == 1, "Clause does not force a physical monochromatic K5")
        counts[f"{'added' if external else 'core'}_color_{colors.pop()}"] += 1
    return dict(sorted(counts.items()))
