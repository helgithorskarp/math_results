"""Supplementary exact count control; independent of the native verifier."""
import hashlib
import json
from math import comb
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def count(n, k):
    s = 2**(n-1)-n
    Z, T = 2*s-2, 4*s-4
    K = sum(comb(n, a) for a in range(2, k+1))
    G = sum(comb(n, a) for a in range(k+1, n-k))
    require(G == Z-2*K, 'Correct bulk count')
    require(G != T-2*K, 'Original typo must reject')
    require(s*(2*G+4*K)-(G+2*K)**2 == T, 'Unchanged energy constant')
    if n <= 12:
        low = bulk = high = 0
        for bitset in range(1, 1 << n):
            a = bitset.bit_count()
            if a > n-2:
                continue
            if a <= k:
                low += 1
            elif a >= n-k:
                high += 1
            else:
                bulk += 1
        require((low, bulk, high) == (n+K, G, K), 'Every actual vertex')
    return {'n': n, 'k': k, 'low': n+K, 'bulk': G, 'high': K, 'Z': Z, 'T': T}


def main():
    rows = [count(n, k) for n in range(6, 129)
            for k in range(2, (n-2)//2+1)]
    require(rows[0] == {'n': 6, 'k': 2, 'low': 21, 'bulk': 20,
                       'high': 15, 'Z': 50, 'T': 100}, 'n6/k2 exact control')
    expected = Path(__file__).with_name('expected.json').read_bytes()
    require(len(expected) == 73825 and hashlib.sha256(expected).hexdigest() ==
            '249b2778b1c92125ec9334a42846e86829c0df6074482b3a43a47d43f973304d',
            'Original frozen mathematical evidence')
    raw = json.dumps(rows, sort_keys=True, separators=(',', ':')).encode()
    print(json.dumps({'checked_count_pairs': len(rows),
                      'literal_n': list(range(6, 13)),
                      'n6_k2': rows[0],
                      'complete_count_record_bytes': len(raw),
                      'complete_count_record_sha256': hashlib.sha256(raw).hexdigest(),
                      'original_frozen_record_unchanged': True},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
