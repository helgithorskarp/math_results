#!/usr/bin/env python3
"""Enumerate every possible vertex-critical kernel for the small graph lemma."""

from itertools import combinations, product
import hashlib


def require(condition, message):
    if not condition:
        raise ValueError(message)


def graphs_with_degree_sequence(degrees):
    """Generate each labelled simple graph with this degree sequence once."""
    n = len(degrees)
    residual = list(degrees)
    adjacency = [0] * n

    def visit(i):
        if i == n:
            if not any(residual):
                yield tuple(adjacency)
            return
        eligible = [j for j in range(i + 1, n) if residual[j] > 0]
        needed = residual[i]
        if needed < 0 or needed > len(eligible):
            return
        old = residual[i]
        residual[i] = 0
        for chosen in combinations(eligible, needed):
            for j in chosen:
                residual[j] -= 1
                adjacency[i] |= 1 << j
                adjacency[j] |= 1 << i
            if (
                all(0 <= residual[j] <= n - i - 2 for j in range(i + 1, n))
                and sum(residual) % 2 == 0
            ):
                yield from visit(i + 1)
            for j in chosen:
                residual[j] += 1
                adjacency[i] ^= 1 << j
                adjacency[j] ^= 1 << i
        residual[i] = old

    yield from visit(0)


def graph_mask(adjacency):
    value = 0
    for bit, (a, b) in enumerate(combinations(range(len(adjacency)), 2)):
        value |= ((adjacency[a] >> b) & 1) << bit
    return value


def contains_k5(adjacency):
    for vertices in combinations(range(len(adjacency)), 5):
        if all(adjacency[a] >> b & 1 for a, b in combinations(vertices, 2)):
            return True
    return False


def four_colouring(adjacency):
    """Return a deterministic palette-normalized colouring, or None."""
    n = len(adjacency)
    colours = [-1] * n

    def visit(done):
        if done == n:
            return tuple(colours)
        uncoloured = [v for v in range(n) if colours[v] < 0]

        def priority(v):
            neighbour_colours = {
                colours[w]
                for w in range(n)
                if adjacency[v] >> w & 1 and colours[w] >= 0
            }
            uncoloured_degree = sum(
                colours[w] < 0 for w in range(n) if adjacency[v] >> w & 1
            )
            return len(neighbour_colours), uncoloured_degree, adjacency[v].bit_count(), -v

        v = max(uncoloured, key=priority)
        forbidden = {
            colours[w]
            for w in range(n)
            if adjacency[v] >> w & 1 and colours[w] >= 0
        }
        highest = min(3, max(colours) + 1)
        for colour in range(highest + 1):
            if colour in forbidden:
                continue
            colours[v] = colour
            answer = visit(done + 1)
            if answer is not None:
                return answer
            colours[v] = -1
        return None

    answer = visit(0)
    if answer is not None:
        require(
            max(answer) < 4
            and all(
                answer[a] != answer[b]
                for a, b in combinations(range(n), 2)
                if adjacency[a] >> b & 1
            ),
            "invalid four-colouring",
        )
    return answer


def run():
    reports = []
    global_receipt = hashlib.sha256()
    for n in range(5, 9):
        allowed = tuple(d for d in (4, 5) if d < n)
        total = with_k5 = k5_free = coloured = 0
        receipt = hashlib.sha256()
        graph_set = hashlib.sha256()
        degree_sequences = 0
        for degrees in product(allowed, repeat=n):
            if sum(degrees) % 2:
                continue
            degree_sequences += 1
            for adjacency in graphs_with_degree_sequence(degrees):
                require(
                    tuple(a.bit_count() for a in adjacency) == degrees,
                    "degree-sequence generator mismatch",
                )
                total += 1
                encoded = graph_mask(adjacency)
                graph_set.update(f"{encoded}\n".encode())
                if contains_k5(adjacency):
                    with_k5 += 1
                    row = f"{encoded}:K5\n"
                else:
                    k5_free += 1
                    word = four_colouring(adjacency)
                    require(word is not None, "K5-free uncolourable kernel")
                    coloured += 1
                    row = f"{encoded}:{''.join(map(str, word))}\n"
                receipt.update(row.encode())
                global_receipt.update(f"{n}:{row}".encode())
        require(total == with_k5 + k5_free, "kernel partition")
        require(k5_free == coloured, "uncoloured K5-free graph")
        reports.append(
            {
                "vertices": n,
                "degree_sequences_considered": degree_sequences,
                "labelled_min4_max5_graphs": total,
                "graphs_containing_K5": with_k5,
                "K5_free_graphs": k5_free,
                "explicit_four_colourings": coloured,
                "graph_set_sha256": graph_set.hexdigest(),
                "colouring_receipt_sha256": receipt.hexdigest(),
            }
        )
    require(
        [r["labelled_min4_max5_graphs"] for r in reports]
        == [1, 76, 6912, 848932],
        "unexpected kernel counts",
    )
    return {
        "critical_reduction": "a vertex-minimal non-four-colourable subgraph has all degrees in {4,5}",
        "orders_checked": [5, 6, 7, 8],
        "kernels": reports,
        "global_receipt_sha256": global_receipt.hexdigest(),
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run(), indent=2, sort_keys=True))
