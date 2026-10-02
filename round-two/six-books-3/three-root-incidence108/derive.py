"""Complete necessary low-incidence census for equality-three, not a host census."""
import argparse
import hashlib
import sys
import itertools
import json
from pathlib import Path

PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
PERMS = tuple(itertools.permutations(range(4)))


def compositions(total, length):
    if length == 1:
        yield (total,)
    else:
        for v in range(total + 1):
            for tail in compositions(total-v, length-1):
                yield (v,)+tail


def transform(counts, perm):
    result = [0]*15
    for mask, count in enumerate(counts, 1):
        new = sum(1 << perm[i] for i in range(4) if mask & (1 << i))
        result[new-1] = count
    return tuple(result)


def canonical(counts):
    return min(transform(counts, p) for p in PERMS)


def census(triples, quadruples):
    labeled = set()
    for omissions in compositions(triples, 4):
        for singles in compositions(3, 4):
            budgets = tuple(triples+2*quadruples-omissions[i]-singles[i]
                            for i in range(4))
            if min(budgets) < 1:
                continue
            row = [9-singles[i]-(triples-omissions[i])-quadruples
                   for i in range(4)]
            upper = [4-triples+omissions[i]+omissions[j]-quadruples
                     for i, j in PAIRS]
            for ab in range(upper[0]+1):
                for ac in range(upper[1]+1):
                    ad = row[0]-ab-ac
                    twice_bc = row[1]-ab+row[2]-ac-row[3]+ad
                    if twice_bc % 2:
                        continue
                    bc = twice_bc//2
                    bd = row[1]-ab-bc
                    cd = row[2]-ac-bc
                    pairs = (ab, ac, ad, bc, bd, cd)
                    if any(v < 0 or v > cap for v, cap in zip(pairs, upper)):
                        continue
                    counts = [0]*15
                    for i in range(4):
                        counts[(1 << i)-1] = singles[i]
                        counts[(15 ^ (1 << i))-1] = omissions[i]
                    for (i, j), v in zip(PAIRS, pairs):
                        counts[(1 << i)+(1 << j)-1] = v
                    counts[14] = quadruples
                    if sum(counts) != 18 or any(sum(v for m, v in enumerate(counts, 1)
                                                    if m & (1 << i)) != 9
                                             for i in range(4)):
                        raise RuntimeError('Broken complete pair solution')
                    labeled.add(tuple(counts))
    quotient = sorted({canonical(c) for c in labeled})
    return dict(triples=triples, quadruples=quadruples,
                labeled=sorted(labeled), canonical=quotient)


def main():
    result = {'scope': 'q0/equality-three necessary incidence; all lows degree9; all low blue caps; mixed row slack parity',
              'sectors': [census(3, 0), census(1, 1)]}
    raw = (json.dumps(result, sort_keys=True, separators=(',', ':'))+'\n').encode()
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', type=Path)
    parser.add_argument('--full', action='store_true')
    args = parser.parse_args()
    if args.check and args.check.read_bytes() != raw:
        raise ValueError('Whole necessary incidence census differs')
    if args.full:
        sys.stdout.buffer.write(raw)
        return
    print(json.dumps({'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw),
                      'sectors': [dict(triples=x['triples'], quadruples=x['quadruples'],
                                       labeled=len(x['labeled']), canonical=len(x['canonical']))
                                  for x in result['sectors']]}, sort_keys=True))


if __name__ == '__main__':
    main()
