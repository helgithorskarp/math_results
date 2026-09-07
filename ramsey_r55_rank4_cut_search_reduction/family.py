#!/usr/bin/env python3
"""All rank-four 20-by-23 cuts, with arbitrary internal edges."""
import json
import sys


def rank(rows):
    basis = {}
    for x in rows:
        while x:
            k = x.bit_length() - 1
            if k not in basis:
                basis[k] = x
                break
            x ^= basis[k]
    return len(basis)


def generate(obj):
    if not isinstance(obj, dict) or set(obj) != {'left', 'right', 'internal_hex'}:
        raise ValueError('parameter fields')
    for key, size in [('left', 20), ('right', 23)]:
        labels = obj[key]
        if not isinstance(labels, list) or len(labels) != size:
            raise ValueError('label count')
        if any(type(x) is not int or not 0 <= x < 16 for x in labels):
            raise ValueError('four-bit label')
        if rank(labels) != 4:
            raise ValueError('labels must span dimension four')
    word = obj['internal_hex']
    if not isinstance(word, str) or len(word) != 111 or any(c not in '0123456789abcdef' for c in word):
        raise ValueError('443 internal bits')
    word = int(word, 16)
    if word >= 1 << 443:
        raise ValueError('internal padding')
    red = 0
    pair = internal = 0
    for u in range(43):
        for v in range(u + 1, 43):
            if u < 20 <= v:
                bit = (obj['left'][u] & obj['right'][v - 20]).bit_count() % 2
            else:
                bit = (word >> internal) & 1
                internal += 1
            red |= bit << pair
            pair += 1
    return {'n': 43, 'red_hex': format(red, '0226x'), 'cut': list(range(20)), 'color': 1}


def filter_status(obj):
    # Validate even an input which the filter would discard.
    generate(obj)
    return ('EXCLUDED_ZERO_TYPES' if 0 in obj['left'] and 0 in obj['right']
            else 'SURVIVES_ZERO_TYPE_FILTER')


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        obj = json.load(f)
    print(json.dumps({'status': filter_status(obj), 'graph': generate(obj)}, sort_keys=True))
