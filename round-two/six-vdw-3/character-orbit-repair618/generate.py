#!/usr/bin/env python3
"""Find one actual bad AP; Euler character bits are checked separately."""
import argparse
import json
from pathlib import Path


def generate():
    bits = [None if x == 0 else int(pow(x, 51, 103) == 102) for x in range(103)]
    seed = None
    for d in range(1, 618):
        for a in range(618):
            terms = [(a + j*d) % 618 for j in range(7)]
            if any(t % 103 == 0 for t in terms):
                continue
            colors = [bits[t % 103] ^ int(t % 6 >= 3) for t in terms]
            if len(set(colors)) == 1:
                seed = {'start': a, 'step': d, 'color': colors[0],
                        'field_support': sorted(t % 103 for t in terms)}
                break
        if seed is not None:
            break
    if seed is None:
        raise ValueError('No witness found; this is not a nonexistence certificate')
    return {'agent': 'six-vdw-3', 'role': 'researcher', 'q': 103, 'period': 618,
            'phase': [0, 0, 0, 1, 1, 1],
            'character_word': ''.join('-' if b is None else str(b) for b in bits),
            'seed_actual_AP': seed, 'fractional_edge_weight': [1, 7],
            'zero_argument_column_free': True, 'W_bound_improved': False}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    a.output.write_text(json.dumps(generate(), indent=2) + '\n')
