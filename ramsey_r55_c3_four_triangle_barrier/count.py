#!/usr/bin/env python3
"""Count distinct labeled graphs in the union by their exact triangle support."""
import json
from math import comb


def need(ok, message):
    if not ok:
        raise ValueError(message)


def run():
    exact = []
    for r in range(5):
        value = sum((-1)**j * comb(r, j) * 2**(3*comb(r-j, 2)+r-j)
                    for j in range(r+1))
        recursive = 2**(3*comb(r, 2)+r) - sum(comb(r, s)*exact[s] for s in range(r))
        need(value == recursive, 'inclusion-exclusion and support recurrence')
        exact.append(value)
    controls = 0
    for r in range(4):
        supports = [1 << i for i in range(r)]
        supports += [(1 << i) | (1 << j) for i in range(r) for j in range(i+1, r)
                     for _ in range(3)]
        histogram = [0]*(r+1)
        for word in range(1 << len(supports)):
            touched = 0
            for i, support in enumerate(supports):
                if word & (1 << i):
                    touched |= support
            histogram[touched.bit_count()] += 1
            controls += 1
        need(histogram == [comb(r, s)*exact[s] for s in range(r+1)], 'literal support count')
    rows = [{'support_size': r, 'triangle_subsets': comb(14, r),
             'exact_support_words': exact[r], 'distinct_graphs': comb(14, r)*exact[r]}
            for r in range(5)]
    total = sum(row['distinct_graphs'] for row in rows)
    return {'status': 'VERIFIED_EXACT_SUPPORT_COUNT', 'support_rows': rows,
            'distinct_labeled_graphs': total, 'nontrivial_graphs': total-1,
            'block_assignment_slots': 1001*(1 << 22),
            'literal_small_support_words_checked': controls}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
