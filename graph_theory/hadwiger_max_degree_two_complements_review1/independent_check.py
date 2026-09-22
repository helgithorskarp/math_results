#!/usr/bin/env python3
"""Definition-level audit of Hadwiger numbers in co-degree-two graphs.

This implementation does not use the producer's forbidden-graph certificates.
It enumerates component multisets from integer partitions and computes the
Hadwiger number directly: a K_t minor is a partition of some vertex subset
into t connected, pairwise adjacent branch sets.  A distinguished unused
block turns this into a restricted-growth partition of n+1 objects.

Python 3.11+, standard library only.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import itertools
import json


EXPECTED_DEFICIT_CORES = (
    "C3",
    "C4",
    "P4",
    "P5",
    "P2+C5",
    "P3+C5",
    "P2+C6",
    "P3+C6",
)


def integer_partitions(total: int, minimum: int = 1):
    if total == 0:
        yield ()
        return
    for first in range(minimum, total + 1):
        for tail in integer_partitions(total - first, first):
            yield (first,) + tail


def component_signatures(total: int):
    """All unlabeled max-degree-two graphs, via sizes then P/C choices."""
    for sizes in integer_partitions(total):
        counts = Counter(sizes)
        variable = [(size, count) for size, count in counts.items() if size >= 3]
        for cycle_counts in itertools.product(
            *(range(count + 1) for _, count in variable)
        ):
            selected = dict(zip((size for size, _ in variable), cycle_counts, strict=True))
            signature = []
            for size in sorted(counts):
                cycles = selected.get(size, 0)
                signature.extend(("P", size) for _ in range(counts[size] - cycles))
                signature.extend(("C", size) for _ in range(cycles))
            yield tuple(signature)


def signature_text(signature):
    counts = Counter(signature)
    terms = []
    for (kind, size), count in sorted(counts.items(), key=lambda item: (item[0][1], item[0][0])):
        term = f"{kind}{size}"
        terms.append(term if count == 1 else f"{count}{term}")
    return "+".join(terms)


def strip_isolates(signature):
    return tuple(component for component in signature if component != ("P", 1))


def build_h(signature):
    n = sum(size for _, size in signature)
    adjacency = [0] * n
    start = 0
    for kind, size in signature:
        for offset in range(size - 1):
            u, v = start + offset, start + offset + 1
            adjacency[u] |= 1 << v
            adjacency[v] |= 1 << u
        if kind == "C":
            u, v = start + size - 1, start
            adjacency[u] |= 1 << v
            adjacency[v] |= 1 << u
        start += size
    return tuple(adjacency)


def complement(adjacency):
    all_vertices = (1 << len(adjacency)) - 1
    return tuple(all_vertices ^ adjacency[v] ^ (1 << v) for v in range(len(adjacency)))


def independent(mask: int, adjacency) -> bool:
    rest = mask
    while rest:
        bit = rest & -rest
        v = bit.bit_length() - 1
        rest ^= bit
        if adjacency[v] & rest:
            return False
    return True


def independence_number(adjacency) -> int:
    return max(
        mask.bit_count()
        for mask in range(1 << len(adjacency))
        if independent(mask, adjacency)
    )


def chromatic_number(adjacency) -> int:
    """Exact DSATUR search, independent of the component clique-cover formula."""
    n = len(adjacency)
    colors = [-1] * n
    best = n

    def visit(used: int):
        nonlocal best
        if used >= best:
            return
        uncolored = [v for v in range(n) if colors[v] < 0]
        if not uncolored:
            best = used
            return
        vertex = max(
            uncolored,
            key=lambda v: (
                len({colors[u] for u in range(n) if adjacency[v] >> u & 1 and colors[u] >= 0}),
                adjacency[v].bit_count(),
                -v,
            ),
        )
        forbidden = {colors[u] for u in range(n) if adjacency[vertex] >> u & 1 and colors[u] >= 0}
        for color in range(min(used + 1, best)):
            if color in forbidden:
                continue
            colors[vertex] = color
            visit(max(used, color + 1))
            colors[vertex] = -1

    visit(0)
    return best


def connected_masks(adjacency):
    n = len(adjacency)
    result = [False] * (1 << n)
    neighbor_union = [0] * (1 << n)
    for mask in range(1, 1 << n):
        bit = mask & -mask
        vertex = bit.bit_length() - 1
        neighbor_union[mask] = neighbor_union[mask ^ bit] | adjacency[vertex]
        reached = bit
        while True:
            expanded = reached | (neighbor_union[reached] & mask)
            if expanded == reached:
                break
            reached = expanded
        result[mask] = reached == mask
    return result, neighbor_union


def clique_minor_model(adjacency, target: int):
    """Search all t branch blocks plus one distinguished unused block."""
    n = len(adjacency)
    if target == 0:
        return [], 1
    is_connected, neighbor_union = connected_masks(adjacency)
    blocks = [0] * (target + 1)
    leaves = 0

    def valid_leaf():
        nonlocal leaves
        leaves += 1
        branch_sets = blocks[1:]
        if any(not is_connected[mask] for mask in branch_sets):
            return False
        return all(
            neighbor_union[left] & right
            for i, left in enumerate(branch_sets)
            for right in branch_sets[i + 1 :]
        )

    def search(vertex: int, maximum_label: int):
        if maximum_label + (n - vertex) < target:
            return None
        if vertex == n:
            if maximum_label == target and valid_leaf():
                return tuple(blocks[1:])
            return None

        bit = 1 << vertex
        # New blocks first favors the many-singleton models forced near the
        # counting upper bound. Existing blocks and the unused block follow.
        choices = []
        if maximum_label < target:
            choices.append(maximum_label + 1)
        choices.extend(range(1, maximum_label + 1))
        choices.append(0)
        for label in choices:
            blocks[label] |= bit
            answer = search(vertex + 1, max(maximum_label, label))
            blocks[label] ^= bit
            if answer is not None:
                return answer
        return None

    return search(0, 0), lambda: leaves


def verify_model(adjacency, model):
    is_connected, neighbor_union = connected_masks(adjacency)
    used = 0
    for block in model:
        if not block or used & block or not is_connected[block]:
            return False
        used |= block
    return all(
        neighbor_union[left] & right
        for i, left in enumerate(model)
        for right in model[i + 1 :]
    )


def exact_hadwiger(adjacency, upper: int):
    examined = 0
    for target in range(upper, 0, -1):
        model, leaf_counter = clique_minor_model(adjacency, target)
        examined += leaf_counter()
        if model is not None:
            if len(model) != target or not verify_model(adjacency, model):
                raise AssertionError("minor-search result failed direct replay")
            return target, model, examined
    raise AssertionError("every nonempty graph has a K1 minor")


def maximum_matching_size(adjacency):
    n = len(adjacency)
    memo = {0: 0}

    def solve(mask):
        if mask in memo:
            return memo[mask]
        bit = mask & -mask
        vertex = bit.bit_length() - 1
        rest = mask ^ bit
        answer = solve(rest)
        partners = adjacency[vertex] & rest
        while partners:
            partner = partners & -partners
            answer = max(answer, 1 + solve(rest ^ partner))
            partners ^= partner
        memo[mask] = answer
        return answer

    return solve((1 << n) - 1)


def auxiliary_matching_boundary(limit: int = 12):
    failures = defaultdict(list)
    for n in range(1, limit + 1):
        for signature in component_signatures(n):
            allowed = complement(build_h(signature))
            if maximum_matching_size(allowed) < n // 2:
                failures[str(n)].append(signature_text(signature))
    return dict(failures)


def main():
    max_order = 12
    counts = {}
    deficit_cores = set()
    deficit_instances = 0
    graphs_checked = 0
    minor_partition_leaves = 0
    models_digest = hashlib.sha256()
    smallest = {}

    for n in range(1, max_order + 1):
        signatures = list(component_signatures(n))
        counts[str(n)] = len(signatures)
        for signature in signatures:
            h = build_h(signature)
            g = complement(h)
            alpha = independence_number(h)
            upper = (n + alpha) // 2
            eta, model, leaves = exact_hadwiger(g, upper)
            chi = chromatic_number(g)
            minor_partition_leaves += leaves
            graphs_checked += 1
            if chi > eta:
                raise AssertionError(f"Hadwiger inequality failed for {signature_text(signature)}")
            deficit = upper - eta
            if deficit not in (0, 1):
                raise AssertionError(f"unexpected deficit for {signature_text(signature)}")
            if deficit:
                deficit_instances += 1
                deficit_cores.add(signature_text(strip_isolates(signature)))
            encoded_model = [
                [v for v in range(n) if block >> v & 1]
                for block in model
            ]
            models_digest.update(
                json.dumps(
                    [signature_text(signature), alpha, chi, eta, encoded_model],
                    separators=(",", ":"),
                ).encode()
            )
            if signature_text(signature) in {"P4", "C5", "C6", "P2+C5", "P4+C5", "2C3"}:
                smallest[signature_text(signature)] = {
                    "alpha": alpha,
                    "chi_of_complement": chi,
                    "hadwiger": eta,
                    "upper": upper,
                }

    if tuple(sorted(deficit_cores)) != tuple(sorted(EXPECTED_DEFICIT_CORES)):
        raise AssertionError(sorted(deficit_cores))

    matching_failures = auxiliary_matching_boundary()
    expected_matching_failures = {"2": ["P2"], "3": ["C3"], "4": ["P1+C3"]}
    if matching_failures != expected_matching_failures:
        raise AssertionError(matching_failures)

    result = {
        "auxiliary_complement_matching_failures_through_order_12": matching_failures,
        "component_signature_counts": counts,
        "deficit_cores_discovered": sorted(deficit_cores),
        "deficit_instances_through_order_12": deficit_instances,
        "exact_hadwiger_numbers_from_branch_partitions": graphs_checked,
        "minor_partition_leaves_examined": minor_partition_leaves,
        "model_digest_sha256": models_digest.hexdigest(),
        "selected_adversarial_boundaries": smallest,
        "trust_boundary": (
            "finite definition-level audit only; the unbounded classification "
            "uses the written forbidden-graph and Dirac argument"
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
