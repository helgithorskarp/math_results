#!/usr/bin/env python3
"""Exhaustive small list-graph checks and deliberate malformed-certificate controls."""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import construct as C


def brute(masks, edges):
    for colors in product(range(4), repeat=len(masks)):
        if all((m >> c) & 1 for m, c in zip(masks, colors)) and all(colors[i] != colors[j] for i, j in edges):
            return colors
    return None


def main():
    counts = Counter()
    for n in range(4):
        possible_edges = list(combinations(range(n), 2))
        for masks in product(range(1, 16), repeat=n):
            for selected in range(1 << len(possible_edges)):
                edges = [e for bit, e in enumerate(possible_edges) if selected >> bit & 1]
                witness = brute(masks, edges)
                try:
                    colors, _ = C.extend_lists(masks, edges)
                except ValueError as error:
                    if str(error) == 'propagation contradiction':
                        assert witness is None
                        counts['proved_contradictions'] += 1
                    else:
                        assert str(error) == 'cyclic residual'
                        counts['cyclic_residual_rejections'] += 1
                else:
                    assert witness is not None
                    assert all((m >> c) & 1 for m, c in zip(masks, colors))
                    assert all(colors[i] != colors[j] for i, j in edges)
                    counts['successful_constructed_colourings'] += 1
                counts['exhaustive_cases'] += 1
    # A colourable cyclic residual is deliberately rejected: the constructor is sufficient only.
    cycle = [(0, 1), (0, 3), (1, 2), (2, 3)]
    assert brute([3] * 4, cycle) is not None
    try:
        C.extend_lists([3] * 4, cycle)
    except ValueError as error:
        assert str(error) == 'cyclic residual'
    else:
        raise AssertionError('cyclic residual not rejected')
    rejected = 0
    for callback in [lambda: C.extend_lists([0], []), lambda: C.extend_lists([16], []),
                     lambda: C.extend_lists([3], [(0, 0)]),
                     lambda: C.extend_lists([3, 3], [(0, 1), (0, 1)]),
                     lambda: C.check_colors([0, 0], [15, 15], [(0, 1)]),
                     lambda: C.check_colors([4], [15], []),
                     lambda: C.check_colors([0], [2], [])]:
        try:
            callback()
        except ValueError:
            rejected += 1
        else:
            raise AssertionError('invalid fixture accepted')
    with TemporaryDirectory() as work:
        p = Path(work) / 'colors.txt'
        for raw in (b'0124\n', b'0123', b'0123\n\n'):
            p.write_bytes(raw)
            try:
                C.read_colors(p, 4)
            except ValueError:
                rejected += 1
            else:
                raise AssertionError('invalid colour encoding accepted')
    print(json.dumps({'small_graph_orders': [0, 1, 2, 3], **dict(sorted(counts.items())),
                      'colourable_four_cycle_deliberately_rejected': True,
                      'malformed_list_graph_or_colour_controls_rejected': rejected}, indent=2))


if __name__ == '__main__':
    main()
