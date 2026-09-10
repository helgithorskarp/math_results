#!/usr/bin/env python3
"""Independent exact audit of the distant-partition profile contradiction."""

from collections import Counter, defaultdict
from itertools import combinations


PROFILES = {
    1: ({2: 2, 3: 15}, {1: 6, 2: 15, 3: 3}),
    2: ({2: 2, 3: 15}, {0: 1, 1: 3, 2: 18, 3: 2}),
    4: ({2: 3, 3: 13, 4: 1}, {1: 5, 2: 17, 3: 2}),
    6: ({2: 4, 3: 11, 4: 2}, {1: 4, 2: 19, 3: 1}),
}


def require(condition):
    if not condition:
        raise AssertionError("independent audit invariant failed")


def advance(states, degree, high_count, multiplicity, ceiling):
    choices = range(-3, 4) if degree == 6 else range(-2, 4)
    if degree == 7:
        choices = [value for value in choices if value <= ceiling]
    result = states
    for _ in range(multiplicity):
        following = defaultdict(int)
        for (epsilon_sum, weighted_sum, gap, special), count in result.items():
            for epsilon in choices:
                cost = epsilon * epsilon if degree == 6 else epsilon * (epsilon - 1)
                if gap + cost <= 9:
                    key = (
                        epsilon_sum + epsilon,
                        weighted_sum + high_count * epsilon,
                        gap + cost,
                        special
                        + int(degree == 7 and high_count == 2 and epsilon == 1),
                    )
                    following[key] += count
        result = following
    return result


def aggregate_states(six_histogram, seven_histogram):
    require(sum(six_histogram.values()) == 17)
    require(sum(seven_histogram.values()) == 24)
    require(sum(c * n for c, n in six_histogram.items()) == 49)
    require(sum(c * n for c, n in seven_histogram.items()) == 45)
    deficit = sum(
        ((c - 3) * (c - 4) // 2) * n for c, n in six_histogram.items()
    ) + sum(((c - 1) * (c - 2) // 2) * n for c, n in seven_histogram.items())
    require(deficit == 5)
    positive_excess = sum(
        max(high_count - 3, 0) * multiplicity
        for histogram in (six_histogram, seven_histogram)
        for high_count, multiplicity in histogram.items()
    )
    states = {(0, 0, 0, 0): 1}
    for high_count, multiplicity in sorted(six_histogram.items()):
        states = advance(states, 6, high_count, multiplicity, None)
    ceilings = {}
    for high_count, multiplicity in sorted(seven_histogram.items()):
        ceiling = (high_count - 1 + positive_excess) // 3
        ceilings[high_count] = ceiling
        states = advance(states, 7, high_count, multiplicity, ceiling)
    admissible = {
        state: count
        for state, count in states.items()
        if state[0] == 7
        and state[1] == 10
        and state[2] <= 9
        and (9 - state[2]) % 2 == 0
    }
    return positive_excess, ceilings, admissible


def packing_counts():
    universe = frozenset(range(5))
    pairs = tuple(map(frozenset, combinations(universe, 2)))
    counts = Counter()
    for mask in range(1 << len(pairs)):
        family = [pairs[index] for index in range(len(pairs)) if mask >> index & 1]
        complements = [universe - pair for pair in family]
        if all(
            len(left & right) <= 1
            for left, right in combinations(complements, 2)
        ):
            counts[len(family)] += 1
    return [counts[size] for size in range(11)]


def main():
    rows = []
    for profile, histograms in PROFILES.items():
        positive_excess, ceilings, states = aggregate_states(*histograms)
        q_values = sorted({state[3] for state in states})
        rows.append((profile, positive_excess, ceilings, len(states), q_values))
    require(rows == [
        (1, 0, {1: 0, 2: 0, 3: 0}, 0, []),
        (2, 0, {0: -1, 1: 0, 2: 0, 3: 0}, 0, []),
        (4, 1, {1: 0, 2: 0, 3: 1}, 0, []),
        (6, 2, {1: 0, 2: 1, 3: 1}, 32, list(range(4, 16))),
    ])
    counts = packing_counts()
    require(counts == [1, 10, 15] + [0] * 8)
    special_required_minimum = min(rows[-1][4])
    special_packing_maximum = max(size for size, count in enumerate(counts) if count)
    require(special_required_minimum == 4 > 2 == special_packing_maximum)
    print("independent_distant_partition_audit=PASS")
    for profile, positive_excess, ceilings, count, q_values in rows:
        encoded = ",".join(f"{key}:{value}" for key, value in ceilings.items())
        print(
            f"profile={profile} positive_excess={positive_excess} "
            f"ceilings={encoded} aggregate_state_types={count} q_values={q_values}"
        )
    print("five_point_packing_counts=" + ",".join(map(str, counts)))
    print(
        f"special_required_minimum={special_required_minimum} "
        f"special_packing_maximum={special_packing_maximum}"
    )
    print("all_four_profiles=INFEASIBLE")


if __name__ == "__main__":
    main()
