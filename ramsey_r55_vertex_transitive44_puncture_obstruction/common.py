#!/usr/bin/env python3
"""Production primitives for the degree-44 transitive-action certificate."""

from functools import lru_cache
from itertools import combinations


N = 44
PAIRS = tuple(combinations(range(N), 2))
PAIR_INDEX = {edge: i for i, edge in enumerate(PAIRS)}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def read_catalog(path):
    actions = []
    for expected, line in enumerate(path.read_text().splitlines(), 1):
        fields = line.split("|")
        need(len(fields) == 3, f"catalog line {expected}")
        index, order = int(fields[0]), int(fields[1])
        need(index == expected, f"catalog index {index}")
        generators = tuple(
            tuple(int(x) - 1 for x in text.split(","))
            for text in fields[2].split(";")
        )
        need(generators, f"no generators at {index}")
        for generator in generators:
            need(len(generator) == N and sorted(generator) == list(range(N)),
                 f"bad permutation at {index}")
        actions.append((index, order, generators))
    need(len(actions) == 2113, f"expected 2113 actions, got {len(actions)}")
    return actions


def point_transitive(generators):
    seen = {0}
    stack = [0]
    while stack:
        point = stack.pop()
        for generator in generators:
            image = generator[point]
            if image not in seen:
                seen.add(image)
                stack.append(image)
    return len(seen) == N


def edge_partition(generators):
    """Canonical unordered-pair orbit labels, by union-find."""
    parent = list(range(len(PAIRS)))

    def find(item):
        while parent[item] != item:
            parent[item] = parent[parent[item]]
            item = parent[item]
        return item

    def union(first, second):
        first, second = find(first), find(second)
        if first != second:
            parent[second] = first

    for generator in generators:
        for i, (u, v) in enumerate(PAIRS):
            a, b = generator[u], generator[v]
            if a > b:
                a, b = b, a
            union(i, PAIR_INDEX[(a, b)])
    names = {}
    labels = []
    for i in range(len(PAIRS)):
        root = find(i)
        if root not in names:
            names[root] = len(names)
        labels.append(names[root])
    return tuple(labels)


def refines(fine, coarse):
    """Whether every cell of fine is contained in one cell of coarse."""
    images = {}
    for small, large in zip(fine, coarse):
        previous = images.setdefault(small, large)
        if previous != large:
            return False
    return True


def maximal_partition_representatives(partitions):
    """First catalog index for every directly maximal labeled refinement."""
    first = {}
    for index, partition in enumerate(partitions, 1):
        first.setdefault(partition, index)
    unique = tuple(first)
    cell_count = {p: 1 + max(p) for p in unique}
    retained = []
    for coarse in unique:
        if not any(cell_count[fine] > cell_count[coarse]
                   and refines(fine, coarse) for fine in unique):
            retained.append(first[coarse])
    return tuple(retained), first


class WorkLimit(Exception):
    pass


def dpll(variable_count, clauses, work_limit=None, collect_reasons=False):
    """Exact bit-mask DPLL; clauses are (positive_mask, negative_mask)."""
    clauses = tuple(clauses)
    full = (1 << variable_count) - 1
    stats = {"calls": 0, "conflicts": 0, "units": 0, "branches": 0}
    used = set()

    @lru_cache(maxsize=None)
    def search(true_mask, false_mask):
        stats["calls"] += 1
        if work_limit is not None and stats["calls"] > work_limit:
            raise WorkLimit
        while True:
            changed = False
            all_satisfied = True
            for clause_index, (positive, negative) in enumerate(clauses):
                if positive & true_mask or negative & false_mask:
                    continue
                all_satisfied = False
                remaining = (positive | negative) & ~(true_mask | false_mask)
                if not remaining:
                    stats["conflicts"] += 1
                    if collect_reasons:
                        used.add(clause_index)
                    return False
                if remaining & (remaining - 1) == 0:
                    stats["units"] += 1
                    if collect_reasons:
                        used.add(clause_index)
                    if positive & remaining:
                        true_mask |= remaining
                    else:
                        false_mask |= remaining
                    changed = True
                    break
            if all_satisfied:
                return True
            if not changed:
                break

        scores = [0] * variable_count
        for positive, negative in clauses:
            if positive & true_mask or negative & false_mask:
                continue
            remaining = (positive | negative) & ~(true_mask | false_mask)
            while remaining:
                bit = remaining & -remaining
                scores[bit.bit_length() - 1] += 1
                remaining -= bit
        unassigned = full & ~(true_mask | false_mask)
        if not unassigned:
            raise AssertionError("DPLL state has no branch variable")
        choices = [i for i in range(variable_count) if unassigned >> i & 1]
        variable = max(choices, key=lambda i: (scores[i], -i))
        bit = 1 << variable
        stats["branches"] += 1
        return search(true_mask | bit, false_mask) or search(true_mask, false_mask | bit)

    try:
        satisfiable = search(0, 0)
    except WorkLimit:
        return None, stats, set()
    stats["cached_states"] = search.cache_info().currsize
    return satisfiable, stats, used


class SplitMix64:
    """Fully specified deterministic 64-bit sampler."""
    MASK = (1 << 64) - 1

    def __init__(self, seed):
        self.state = seed & self.MASK

    def next(self):
        self.state = (self.state + 0x9E3779B97F4A7C15) & self.MASK
        value = self.state
        value = ((value ^ (value >> 30)) * 0xBF58476D1CE4E5B9) & self.MASK
        value = ((value ^ (value >> 27)) * 0x94D049BB133111EB) & self.MASK
        return (value ^ (value >> 31)) & self.MASK


def sampled_five(rng):
    """Floyd sampling of one five-subset of {0,...,43}."""
    selected = set()
    for upper in range(N - 5, N):
        candidate = rng.next() % (upper + 1)
        selected.add(upper if candidate in selected else candidate)
    need(len(selected) == 5, "Floyd sampler")
    return tuple(sorted(selected))


def support(partition, five):
    return tuple(sorted({partition[PAIR_INDEX[edge]]
                         for edge in combinations(five, 2)}))


def records_from_supports(supports):
    ordered = sorted(supports.items())
    records = []
    for orbit_set, five in ordered:
        mask = sum(1 << orbit for orbit in orbit_set)
        records.append((mask, 0, "blue", five))
    for orbit_set, five in ordered:
        mask = sum(1 << orbit for orbit in orbit_set)
        records.append((0, mask, "red", five))
    return records
