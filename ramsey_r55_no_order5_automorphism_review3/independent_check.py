#!/usr/bin/env python3
"""Independent orbit/CNF audit for the final order-five Ramsey exclusion.

No target code is imported.  The actual order-five action is used to build
edge orbits, assign their Boolean semantics, project every five-set, and
recreate both DIMACS byte streams.  The h=1 normalization is also checked on
all internal profiles and all five-bit anchor words.
"""

from collections import Counter
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import json


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parent
TARGET = REPOSITORY/"ramsey_r55_no_order5_automorphism"
INCIDENCE = {0: (0,1,2,3,5,5,6,6), 1: tuple(range(8))}
CYCLE_PAIRS = tuple(combinations(range(8), 2))
TRUE = 149


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def rotate_vertex(vertex, steps=1):
    if vertex < 3:
        return vertex
    cycle, phase = divmod(vertex-3, 5)
    return 3+5*cycle+(phase+steps) % 5


def edge_orbit(edge):
    return tuple(sorted({tuple(sorted((rotate_vertex(edge[0], shift),
                                      rotate_vertex(edge[1], shift))))
                         for shift in range(5)}))


def build_orbits():
    grouped = {}
    for edge in combinations(range(43), 2):
        orbit = edge_orbit(edge)
        grouped.setdefault(orbit, set()).add(edge)
    require(all(set(orbit) == edges for orbit, edges in grouped.items()),
            "edge orbit partition")
    histogram = Counter(map(len, grouped))
    require(histogram == {1: 3, 5: 180}, histogram)
    require(sum(size*count for size, count in histogram.items()) == 903,
            "edge orbit total")
    return tuple(grouped)


def cross_variable(first, second, difference):
    require(first < second, ("cross order", first, second))
    return 9+5*CYCLE_PAIRS.index((first, second))+difference


def direct_literal(h, edge):
    low, high = edge
    if high < 3:
        return TRUE if edge == (0,1) else 0
    high_cycle, high_phase = divmod(high-3, 5)
    if low < 3:
        return TRUE if INCIDENCE[h][high_cycle] & (1 << low) else 0
    low_cycle, low_phase = divmod(low-3, 5)
    if low_cycle == high_cycle:
        distance = (high_phase-low_phase) % 5
        return low_cycle+1 if distance in (1,4) else -(low_cycle+1)
    return cross_variable(low_cycle, high_cycle,
                          (high_phase-low_phase) % 5)


def semantic_edge_table(h, orbits):
    table = {}
    semantic_counts = Counter()
    for orbit in orbits:
        values = {direct_literal(h, edge) for edge in orbit}
        require(len(values) == 1, ("orbit semantic mismatch", orbit, values))
        value = values.pop()
        semantic_counts[value] += 1
        for edge in orbit:
            require(edge not in table, ("duplicate edge", edge))
            table[edge] = value
    require(len(table) == 903, "semantic edge table size")
    require(set(abs(value) for value in semantic_counts if 0 < abs(value) <= 148)
            == set(range(1,149)), "not all variables represented")
    require(semantic_counts[TRUE] == 13 and semantic_counts[0] == 14,
            ("constant edge orbits", semantic_counts[TRUE], semantic_counts[0]))
    return table


def project_clause(red_literals, require_red):
    """Project 'some red' or 'some blue' after constants and complements."""
    variables = set(red_literals)-{0, TRUE}
    if any(-literal in variables for literal in variables):
        return None
    if require_red:
        if TRUE in red_literals:
            return None
        return tuple(sorted(variables))
    if 0 in red_literals:
        return None
    return tuple(sorted(-literal for literal in variables))


def base_clauses(h, table):
    clauses = set()
    raw = 0
    for vertices in combinations(range(43), 5):
        red_literals = {table[(a,b)] for a,b in combinations(vertices, 2)}
        for require_red in (True, False):
            raw += 1
            clause = project_clause(red_literals, require_red)
            if clause is not None:
                clauses.add(clause)
    require(raw == 2*962598, raw)
    return tuple(sorted(clauses, key=lambda clause: (len(clause), clause)))


def rotations(word):
    return tuple(word[shift:]+word[:shift] for shift in range(5))


def symmetry_clauses(h):
    if h == 0:
        return ()
    clauses = [(1,)]
    minimal_words = 0
    forbidden_words = 0
    for cycle in range(1, 8):
        for number in range(32):
            word = tuple((number >> difference) & 1 for difference in range(5))
            if word == min(rotations(word)):
                if cycle == 1:
                    minimal_words += 1
                continue
            forbidden_words += 1
            clauses.append(tuple(-cross_variable(0,cycle,difference) if bit
                                 else cross_variable(0,cycle,difference)
                                 for difference, bit in enumerate(word)))
    require((minimal_words, forbidden_words) == (8,168),
            (minimal_words, forbidden_words))
    return tuple(clauses)


def dimacs(h, base, symmetry):
    clauses = base+symmetry
    text = f"p cnf 148 {len(clauses)}\n"
    text += "".join(" ".join(map(str, clause))+" 0\n" for clause in clauses)
    return text.encode("ascii")


def normalization_audit():
    # Multiplication by 2 interchanges distance-one and distance-two on every
    # moving cycle.  Apply it iff the anchor orientation is initially false.
    for bits in product((False, True), repeat=8):
        normalized = bits if bits[0] else tuple(not bit for bit in bits)
        require(normalized[0], ("orientation normalization", bits))

    allowed = []
    forbidden = []
    clauses = symmetry_clauses(1)[1:25]  # one anchor pair, all 24 exclusions
    variables = tuple(cross_variable(0,1,difference) for difference in range(5))
    for word in product((False, True), repeat=5):
        can_normalize = min(rotations(word))
        canonical = word == can_normalize
        assignment = dict(zip(variables, word))
        clause_ok = all(any(assignment[abs(literal)] == (literal > 0)
                            for literal in clause) for clause in clauses)
        require(clause_ok == canonical, ("word clauses", word, clause_ok, canonical))
        (allowed if clause_ok else forbidden).append(word)
        require(can_normalize in rotations(word), "rotation minimizer")
    require((len(allowed), len(forbidden)) == (8,24), "necklace split")

    # Phase shifts of seven nonanchor cycles act on seven disjoint anchor-word
    # variable blocks, so their minimizing choices commute and are independent.
    blocks = [{cross_variable(0,cycle,d) for d in range(5)} for cycle in range(1,8)]
    require(all(first.isdisjoint(second) for first,second in combinations(blocks,2)),
            "anchor blocks overlap")
    return len(allowed), len(forbidden)


def main():
    reference = json.loads((TARGET/"result.json").read_text())
    orbits = build_orbits()
    summaries = []
    for h in (0,1):
        table = semantic_edge_table(h, orbits)
        base = base_clauses(h, table)
        symmetry = symmetry_clauses(h)
        encoded = dimacs(h, base, symmetry)
        expected = reference["cases"][h]
        digest = sha256(encoded).hexdigest()
        require(len(base) == expected["base_clauses"], ("base count", h, len(base)))
        require(len(symmetry) == expected["symmetry_clauses"],
                ("symmetry count", h, len(symmetry)))
        require(len(encoded) == expected["cnf"]["bytes"],
                ("CNF bytes", h, len(encoded)))
        require(digest == expected["cnf"]["sha256"], ("CNF digest", h, digest))
        histogram = Counter(map(len, base))
        summaries.append((h, len(base), len(symmetry), digest,
                          ",".join(f"{length}:{histogram[length]}"
                                   for length in sorted(histogram))))

    allowed, forbidden = normalization_audit()
    print("PASS actual edge-orbit partition: 3 singleton + 180 five-edge = 183")
    print("PASS semantic variables: 8 internal + 140 cross = 148")
    print("PASS projected every 5-set twice: 1925196 raw Ramsey constraints per case")
    for h, base_count, symmetry_count, digest, histogram in summaries:
        print(f"PASS h={h}: base={base_count} symmetry={symmetry_count} CNF={digest}")
        print(f"INFO h={h} base clause-length histogram={histogram}")
    print(f"PASS h=1 normalization: 256 internal profiles; words allowed/forbidden={allowed}/{forbidden}")
    print("SCOPE CNF reconstruction only; UNSAT requires the separately replayed DRAT proofs")


if __name__ == "__main__":
    main()
