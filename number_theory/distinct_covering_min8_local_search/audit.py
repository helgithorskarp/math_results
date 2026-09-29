"""Separate point-by-point predicate audit; imports no other source module."""
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    data = json.loads((ROOT / 'cover.json').read_text())
    pairs = data['congruences']
    expected = json.loads((ROOT / 'expected.json').read_text())
    if not pairs or any(type(a) is not int or type(m) is not int or not 0 <= a < m or m < 8 for a, m in pairs):
        raise ValueError('invalid congruences')
    names = [m for a, m in pairs]
    if len(set(names)) != len(names) or min(names) != 8:
        raise ValueError('incorrect distinctness or exact minimum')
    # Independent LCM by prime exponents, without importing math.lcm.
    exponents = {}
    for m in names:
        n, prime = m, 2
        while prime * prime <= n:
            exponent = 0
            while n % prime == 0:
                n //= prime
                exponent += 1
            if exponent:
                exponents[prime] = max(exponents.get(prime, 0), exponent)
            prime += 1
        if n > 1:
            exponents[n] = max(exponents.get(n, 0), 1)
    period = 1
    for prime, exponent in exponents.items():
        period *= prime ** exponent
    if period != data['lcm'] or period != expected['lcm']:
        raise ValueError('actual period differs')
    if period > 100000:
        raise ValueError('audit period exceeds declared bound')
    private = {m: 0 for m in names}
    multiplicities = []
    for x in range(period):
        hits = [m for a, m in pairs if x % m == a]
        if not hits:
            raise ValueError(f'uncovered integer representative {x}')
        multiplicities.append(len(hits))
        if len(hits) == 1:
            private[hits[0]] += 1
    result = {'agent': 'six-covering-1', 'role': 'researcher',
              'minimum_modulus': 8, 'lcm': period, 'classes': len(pairs), 'uncovered': 0,
              'coverage_multiplicities': {str(k): v for k, v in sorted(Counter(multiplicities).items())},
              'multiplicity_bytes_sha256': hashlib.sha256(bytes(multiplicities)).hexdigest(),
              'private_points_by_modulus': [[m, private[m]] for a, m in pairs]}
    if result != expected:
        raise ValueError('literal audit disagrees with manifest')
    print(json.dumps(result, sort_keys=True))
    print('POINT-BY-POINT AUDIT PASSED')


if __name__ == '__main__':
    main()
