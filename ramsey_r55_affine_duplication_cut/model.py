#!/usr/bin/env python3
"""Physical family map; every internal pair is initially arbitrary."""
import json
import sys


def generate(obj):
    if type(obj) is not dict or set(obj) != {'doubled_rows','internal_hex'}:
        raise ValueError('parameter fields')
    D = obj['doubled_rows']
    if type(D) is not list or len(D) != 5 or any(type(x) is not int or not 1 <= x <= 15 for x in D) or D != sorted(set(D)):
        raise ValueError('doubled rows')
    text = obj['internal_hex']
    if type(text) is not str or len(text) != 111 or set(text)-set('0123456789abcdef'):
        raise ValueError('internal bits')
    word = int(text,16)
    if word >= 1 << 443:
        raise ValueError('padding')
    A = list(range(1,16))+D
    B = list(range(1,16))+list(range(1,16,2))
    red = 0
    i = 0
    for u in range(43):
        for v in range(u+1,43):
            if u < 20 <= v:
                bit = (A[u]&B[v-20]).bit_count() % 2
            else:
                bit = word % 2
                word //= 2
            red |= bit << i
            i += 1
    return {'n':43,'red_hex':format(red,'0226x')}


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        params = json.load(f)
    print(json.dumps(generate(params),sort_keys=True))
