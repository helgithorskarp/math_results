"""Different complete labeled count-vector enumeration; literal low blue pages."""
import argparse
import hashlib
import sys
import itertools
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def enumerate_sector(triple_count, quad_count):
    masks = (3, 5, 9, 6, 10, 12)
    pair_index = {}
    for values in itertools.product(range(5), repeat=6):
        if sum(values) != 15-triple_count-quad_count:
            continue
        degrees = tuple(sum(v for mask, v in zip(masks, values) if mask >> i & 1)
                        for i in range(4))
        pair_index.setdefault(degrees, []).append(values)
    output = set()
    for small in itertools.product(range(4), repeat=4):
        if sum(small) != 3:
            continue
        for large in itertools.product(range(triple_count+1), repeat=4):
            if sum(large) != triple_count:
                continue
            fixed = []
            for i in range(4):
                fixed.extend([1 << i]*small[i])
                fixed.extend([15-(1 << i)]*large[i])
            fixed.extend([15]*quad_count)
            p = tuple(sum(1 for mask in fixed if mask.bit_count() == 3 and mask >> i & 1)
                      for i in range(4))
            f = tuple(sum(1 for mask in fixed if mask.bit_count() == 4 and mask >> i & 1)
                      for i in range(4))
            if any(p[i]+2*f[i]-small[i] < 1 for i in range(4)):
                continue
            remainder = tuple(9-sum(mask >> i & 1 for mask in fixed) for i in range(4))
            for values in pair_index.get(remainder, ()):
                types = list(fixed)
                for mask, multiplicity in zip(masks, values):
                    types.extend([mask]*multiplicity)
                require(len(types) == 18, 'wrong high cardinality')
                red = [{4+x for x, mask in enumerate(types) if mask >> i & 1}
                       for i in range(4)]
                require(all(len(row) == 9 for row in red), 'wrong actual low degree')
                blue = [set(range(22))-red[i]-{i} for i in range(4)]
                if any(len(blue[i] & blue[j]) > 6 for i, j in itertools.combinations(range(4), 2)):
                    continue
                output.add(tuple(types.count(mask) for mask in range(1, 16)))
    canonical = set()
    for counts in output:
        possibilities = []
        for ordering in itertools.permutations(range(4)):
            transport = []
            for target in range(1, 16):
                original = sum(1 << ordering[i] for i in range(4) if target >> i & 1)
                transport.append(counts[original-1])
            possibilities.append(tuple(transport))
        canonical.add(min(possibilities))
    return dict(triples=triple_count, quadruples=quad_count,
                labeled=sorted(output), canonical=sorted(canonical))


def main():
    actual = {'scope': 'q0/equality-three necessary incidence; all lows degree9; all low blue caps; mixed row slack parity',
              'sectors': [enumerate_sector(3, 0), enumerate_sector(1, 1)]}
    raw = (json.dumps(actual, sort_keys=True, separators=(',', ':'))+'\n').encode()
    parser = argparse.ArgumentParser()
    parser.add_argument('--record', type=Path, default=Path(__file__).with_name('incidence.json'))
    parser.add_argument('--full', action='store_true')
    args = parser.parse_args()
    source = args.record.read_bytes()
    require(raw == source, 'Entire independently regenerated labeled/canonical census differs')
    if args.full:
        sys.stdout.buffer.write(raw)
        return
    print(json.dumps({'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw),
                      'sectors': [dict(triples=x['triples'], quadruples=x['quadruples'],
                                       labeled=len(x['labeled']), canonical=len(x['canonical']))
                                  for x in actual['sectors']]}, sort_keys=True))


if __name__ == '__main__':
    main()
