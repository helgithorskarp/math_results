#!/usr/bin/env python3
"""Complete exact residual table; standard library, no generated input."""

import argparse
import json
from itertools import combinations
from pathlib import Path

from completion import (compatibility_graph, regular_completion, validate_completion,
                        validate_through)
from local import build_local_table, require

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--all-local-labels', action='store_true',
                        help='Independently check the symmetry reduction by omitting it.')
    args = parser.parse_args()
    fixtures = json.loads((ROOT / 'families.json').read_text())['classes']
    columns, allowed, compatible, local_summary, _ = build_local_table(not args.all_local_labels)
    output = []
    for case, record in enumerate(fixtures):
        rows, upper = record['rows'], record['completion']
        validate_through(rows)
        validate_completion(rows, upper)
        blocks, adjacency, graph_summary = compatibility_graph(rows, columns, allowed, compatible)
        if len(upper) == 10:
            index = {block: i for i, block in enumerate(blocks)}
            require(all(b in index for b in upper), 'known completion fails local admissibility')
            require(all(adjacency[index[b]] >> index[c] & 1 for b, c in combinations(upper, 2)),
                    'known completion fails local pair compatibility')
        witness, search_summary = regular_completion(rows, blocks, adjacency)
        if case < 4:
            require(witness is not None and len(upper) == 10, 'sharp ten-block case changed')
        else:
            require(witness is None and len(upper) == 11, 'eleven-block exclusion failed')
        output.append(dict(label=record['label'], minimum=len(upper),
                           graph=graph_summary, search=search_summary, found_ten_block_witness=witness))
    require(len(output) == 6, 'six-family census mismatch')
    print(json.dumps(dict(status='VERIFIED_RESIDUAL_MINIMA_10_10_10_10_11_11',
                          local=local_summary, cases=output), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
