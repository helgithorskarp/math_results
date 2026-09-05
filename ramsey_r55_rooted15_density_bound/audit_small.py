#!/usr/bin/env python3
"""All-cross-matrices validation over a small asymmetric root split."""
from hashlib import sha256
from itertools import product
import json
import census
import fast_search
import literal_search
import reference_search
from verify import check_graph, decode


def main():
    H, B = census.graph(3, 1), census.graph(2, 1)
    records = []
    for low in range(4):
        for high in range(3, 6):
            for target in range(16):
                expected = []
                for rows in product(range(4), repeat=3):
                    try:
                        check_graph(decode(H, B, rows), low, high, target)
                    except ValueError:
                        continue
                    expected.append(rows)
                for module in (fast_search, literal_search, reference_search):
                    actual = module.search(H, B, target, minimum=low, maximum=high)['solutions']
                    census.require(actual == expected, ('literal model-set mismatch', module.__name__, low, high, target))
                records.append([low, high, target, expected])
    allowed = [e for e in range(121) if 14 * e <= 16 * 55 and 14 * (120 - e) <= 16 * 55]
    census.require(allowed == list(range(58, 63)), 'order-sixteen averaging endpoints')
    digest = sha256(json.dumps(records, separators=(',', ':')).encode()).hexdigest()
    print('PASS 192 degree/threshold cases; all 64 cross matrices each; all three full model sets agree')
    print('PASS order-sixteen deletion-averaging interval is exactly 58 through 62')
    print('model_stream_sha256=' + digest)


if __name__ == '__main__':
    main()
