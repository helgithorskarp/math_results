#!/usr/bin/env python3
"""Dense physical checker, independent of producer, rank and Ramsey bounds."""
import hashlib
import json
import sys


def verify(obj, cert):
    if type(obj) is not dict or set(obj) != {'n', 'red_hex', 'cut', 'color'}:
        raise ValueError('fields')
    if type(obj['n']) is not int or obj['n'] != 43:
        raise ValueError('order')
    s = obj['red_hex']
    if type(s) is not str or len(s) != 226 or set(s) - set('0123456789abcdef'):
        raise ValueError('encoding')
    w = int(s, 16)
    if w.bit_length() > 903:
        raise ValueError('padding')
    cut = obj['cut']
    if type(cut) is not list or not 0 < len(cut) < 43:
        raise ValueError('cut')
    if any(type(x) is not int or x not in range(43) for x in cut) or sorted(set(cut)) != cut:
        raise ValueError('cut labels')
    if type(obj['color']) is not int or obj['color'] not in [0, 1]:
        raise ValueError('color')
    keys = {'status', 'input_sha256', 'zero_pair', 'route', 'five', 'five_color'}
    if type(cert) is not dict or set(cert) != keys or cert['status'] != 'EXCLUDED_WITH_PHYSICAL_FIVE':
        raise ValueError('certificate')
    if cert['input_sha256'] != hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()).hexdigest():
        raise ValueError('binding')
    mat = [[0] * 43 for _ in range(43)]
    for i in range(43):
        for j in range(i + 1, 43):
            mat[i][j] = mat[j][i] = w % 2
            w //= 2
    z = cert['zero_pair']
    if type(z) is not list or len(z) != 2 or any(type(x) is not int or x not in range(43) for x in z):
        raise ValueError('zero pair')
    u, v = z
    rest = [x for x in range(43) if x not in cut]
    c = obj['color']
    if u not in cut or v not in rest or any(mat[u][x] == c for x in rest) or any(mat[v][x] == c for x in cut):
        raise ValueError('family gate')
    route = 'mixed_eighteen' if sum(mat[u][x] == c for x in range(43) if x != u) >= 18 else 'low_degree_twenty_five'
    if cert['route'] != route:
        raise ValueError('route')
    q = cert['five']
    if type(q) is not list or len(q) != 5 or any(type(x) is not int or x not in range(43) for x in q) or q != sorted(set(q)):
        raise ValueError('five-set')
    t = cert['five_color']
    if type(t) is not int or t not in [0, 1]:
        raise ValueError('five color')
    for i in range(5):
        for j in range(i + 1, 5):
            if mat[q[i]][q[j]] != t:
                raise ValueError('physical pair')
    return {'status': 'VERIFIED_PHYSICAL_FIVE', 'pairs_checked': 10}


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        obj = json.load(f)
    with open(sys.argv[2]) as f:
        cert = json.load(f)
    print(json.dumps(verify(obj, cert), sort_keys=True))
