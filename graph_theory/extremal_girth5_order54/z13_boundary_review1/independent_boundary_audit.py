#!/usr/bin/env python3
"""Clean-room finite audit of the human thirteen-high boundary argument."""
from itertools import combinations


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def local_types():
    rows = []
    negative = set()
    for degree in (6, 7):
        for c in range(degree + 1):
            for a in range(degree - c + 1):
                b = degree - c - a
                epsilon = b + 2 * c - (8 if degree == 6 else 7)
                charge = (c - 3) * epsilon
                rows.append((degree, a, b, c, epsilon, charge))
                if degree == 6:
                    require(charge >= 0, "negative degree-six charge")
                    if c == 5:
                        require(epsilon >= 2 and charge >= 4,
                                "wrong c=5 charge")
                elif charge < 0:
                    negative.add((c, epsilon))
    require(len(rows) == 64, "wrong local-type count")
    require(negative == {(1, 1), (2, 1), (2, 2)},
            "wrong negative degree-seven types")
    return len(rows), negative


def charge_inventory():
    summary = []
    for m in (5, 6, 7):
        total = 0
        for k in range(23 - 3 * m):
            budget = 10 - m - k
            if budget < 0:
                continue
            for six4 in range(budget + 1):
                for six5 in range(budget // 3 + 1):
                    for seven4 in range(budget // 3 + 1):
                        if six4 + 3 * six5 + 3 * seven4 > budget:
                            continue
                        total += 1
                        if six5 == 0:
                            require(six4 + seven4 <= 5 and seven4 <= 1,
                                    "four-only inventory failure")
                        else:
                            require(six5 == 1 and seven4 == 0,
                                    "nonunique five-set inventory")
                            require(six4 <= 7 - m - k,
                                    "too many four-sets with a five-set")
        required = 25 - 2 * m
        relaxed_t = 7 - m
        upper = 7 + relaxed_t * (relaxed_t + 1)
        require(upper < required, "one-five branch does not contradict")
        require(6 < 21 - 2 * m and 4 < 21 - 2 * m,
                "no-five branch does not contradict")
        summary.append((m, relaxed_t, upper, required, total))
    return summary


def fact_one():
    ground = frozenset(range(5))
    pairs = [frozenset(pair) for pair in combinations(ground, 2)]
    counts = [0] * 11
    maximum = 0
    for bits in range(1 << len(pairs)):
        family = [pairs[i] for i in range(len(pairs)) if bits >> i & 1]
        complements = [ground - pair for pair in family]
        if all(len(x & y) <= 1 for x, y in combinations(complements, 2)):
            counts[len(family)] += 1
            maximum = max(maximum, len(family))
            require(all(not x & y for x, y in combinations(family, 2)),
                    "complement intersection did not force disjoint pairs")
    require(counts == [1, 10, 15] + [0] * 8 and maximum == 2,
            "Fact I family count")
    return counts, maximum


def a1_triple_structure():
    high = frozenset(range(13))
    base = [frozenset(range(0, 4)), frozenset(range(4, 8)),
            frozenset(range(8, 12))]
    p = 12
    extras = [frozenset(row) for row in combinations(high, 4)
              if all(len(frozenset(row) & block) <= 1 for block in base)]
    require(len(extras) == 64, "wrong extra four-set count")
    require(all(p in row and all(len(row & block) == 1 for block in base)
                for row in extras), "wrong extra four-set form")

    systems = 0
    for number in range(3):
        for selected in combinations(extras, number):
            if not all(len(x & y) <= 1 for x, y in combinations(selected, 2)):
                continue
            systems += 1
            blocks = base + list(selected)
            disjoint_pairs = [(i, j) for i, j in combinations(range(len(blocks)), 2)
                              if not blocks[i] & blocks[j]]
            disjoint_triples = [triple for triple in combinations(range(len(blocks)), 3)
                                if all(not blocks[i] & blocks[j]
                                       for i, j in combinations(triple, 2))]
            require(disjoint_pairs == [(0, 1), (0, 2), (1, 2)],
                    "new disjoint pair after A1 triple")
            require(disjoint_triples == [(0, 1, 2)],
                    "new disjoint triple after A1 triple")
            for i, j in disjoint_pairs:
                residual = high - blocks[i] - blocks[j]
                eligible = 0
                for two in combinations(residual, 2):
                    three = residual - frozenset(two)
                    if all(len(three & blocks[q]) <= 1
                           for q in range(len(blocks)) if q not in (i, j)):
                        eligible += 1
                require(eligible == 0, "A2 survives an A1 triple")
    require(systems == 929, "wrong normalized A1-extension count")

    complement_triples = [frozenset(range(4)) - {x} for x in range(4)]
    require(all(len(x & y) == 2 for x, y in combinations(complement_triples, 2)),
            "Fact II complement intersection")
    return len(extras), systems, len(complement_triples) ** 2


def arithmetic():
    for z in range(14):
        n6, n7, n8 = z + 4, 50 - 2 * z, z
        require(n6 + n7 + n8 == 54, "degree count total")
        require(6 * n6 + 7 * n7 + 8 * n8 == 374,
                "degree sum")
    for m in range(8):
        require((78 - m) - 3 * (39 + 2 * m) - (65 - 4 * m)
                + 6 * 17 + 24 == 22 - 3 * m,
                "pair-inventory algebra")
        require((39 + 2 * m) - 3 * 17 == 2 * m - 12,
                "six-surplus algebra")
        require((22 - 3 * m) + (2 * m - 12) == 10 - m,
                "charge-budget algebra")
    require(24 * 7 + 13 * 16 - 13 * 5 - 17 * 8 - 24 * 7 == 7,
            "epsilon total")
    for h in range(3):
        require(5 * h + 8 * (3 + h) + 7 * (5 - 2 * h) == 59 - h,
                "high-neighbor epsilon baseline")


def main():
    arithmetic()
    type_count, negative = local_types()
    fact1_counts, fact1_max = fact_one()
    extras, systems, ordered_singletons = a1_triple_structure()
    inventory = charge_inventory()
    print("cleanroom_boundary_audit=PASS")
    print(f"local_neighbor_types={type_count} negative_V7_types="
          + ",".join(f"c{c}e{e}" for c, e in sorted(negative)))
    print(f"fact_I_family_counts={fact1_counts[:3]} fact_I_max={fact1_max}")
    print(f"A1_extra_four_sets={extras} A1_extension_systems={systems} "
          f"fact_II_ordered_singletons={ordered_singletons}")
    print("one_five_bounds=" + ";".join(
        f"m{m}:t{t},upper{upper}<required{required}"
        for m, t, upper, required, _ in inventory))
    print("conclusion=thirteen_high_boundary_impossible")


if __name__ == "__main__":
    main()
