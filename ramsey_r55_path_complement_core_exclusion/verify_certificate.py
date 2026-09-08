"""Ten-pair literal certificates; no interface/producer import."""
from itertools import combinations
import json
import sys


def verify(candidate, certificate):
    n = candidate['n']
    if type(n) is not int or n != 43:
        raise ValueError('order')
    h = candidate['red_bits_hex']
    if (type(h) is not str or len(h) != 226 or
            any(c not in '0123456789abcdef' for c in h) or int(h, 16) >= 1 << 903):
        raise ValueError('physical bit string')
    if set(certificate) != {'kind', 'color', 'vertices'}:
        raise ValueError('certificate fields')
    s, color = certificate['vertices'], certificate['color']
    if (type(s) is not list or len(s) != 5 or len(set(s)) != 5 or
            any(type(v) is not int or not 0 <= v < 43 for v in s) or
            type(color) is not int or color not in (0, 1)):
        raise ValueError('certificate labels/color')
    if not set(s) <= set(candidate['core']):
        raise ValueError('certificate outside supplied core')
    kind = certificate['kind']
    if kind not in ('induced_path', 'monochromatic5'):
        raise ValueError('certificate kind')
    word = int(h, 16)
    for i, j in combinations(range(5), 2):
        u, v = sorted((s[i], s[j]))
        # Closed form for lexicographic pair position, independently of a
        # generated pair-index table.
        index = u*(2*n-u-1)//2 + v-u-1
        actual = word >> index & 1
        expected = color if kind == 'monochromatic5' or j == i+1 else 1-color
        if actual != expected:
            raise ValueError('wrong physical edge')
    return {'status': 'VERIFIED_TEN_PHYSICAL_PAIRS', 'pairs': 10, 'kind': kind}


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: verify_certificate.py CANDIDATE.json CERTIFICATE.json')
    with open(sys.argv[1]) as f:
        graph = json.load(f)
    with open(sys.argv[2]) as f:
        cert = json.load(f)
    print(json.dumps(verify(graph, cert), indent=2, sort_keys=True))
