"""Independent direct-predicate bitset graph checker; imports no producer/solver."""
import argparse
import itertools
import json
from pathlib import Path


def ensure(condition, message):
    if not condition:
        raise RuntimeError(message)


def block_rows(spec):
    ensure(set(spec) == {'internal','cross','joins'}, 'spec schema')
    ensure(len(spec['internal']) == 7 and all(type(x) is int and x in (0,1) for x in spec['internal']),
           'bad internal bits')
    ensure(len(spec['cross']) == 21 and all(type(x) is int and 0 <= x < 8 for x in spec['cross']),
           'bad cross masks')
    ensure(spec['joins'] is None or (len(spec['joins']) == 7 and all(type(x) is int and x in (0,1)
           for x in spec['joins'])), 'bad fixed joins')
    masks = dict(zip(itertools.combinations(range(7),2),spec['cross']))
    n = 21 if spec['joins'] is None else 22
    rows = [0]*n
    for u in range(n):
        for v in range(u+1,n):
            if v == 21:
                red = spec['joins'][u//3]
            elif u//3 == v//3:
                red = spec['internal'][u//3]
            else:
                red = masks[u//3,v//3] >> ((v%3-u%3)%3) & 1
            if red:
                rows[u] |= 1 << v
                rows[v] |= 1 << u
    return rows


def summary(rows):
    n = len(rows)
    full = (1 << n)-1
    for i,row in enumerate(rows):
        ensure(row & ~full == 0 and not row >> i & 1, 'literal loop/range')
        ensure(all((row >> j & 1) == (rows[j] >> i & 1) for j in range(n)), 'asymmetric rows')
    hist = [{},{}]
    bad = []
    for u in range(n):
        for v in range(u+1,n):
            red = rows[u] >> v & 1
            pages = (rows[u] & rows[v]) if red else full & ~(rows[u]|rows[v]|(1 << u)|(1 << v))
            count = pages.bit_count()
            part = hist[0 if red else 1]
            part[str(count)] = part.get(str(count),0)+1
            if count > (3 if red else 6):
                bad.append(dict(spine=[u,v],color='red' if red else 'blue',
                                pages=[w for w in range(n) if pages >> w & 1]))
    degrees = [row.bit_count() for row in rows]
    return dict(vertices=n,edges=sum(degrees)//2,degrees=degrees,
                degrees_histogram={str(d):degrees.count(d) for d in sorted(set(degrees))},
                red_histogram=hist[0],blue_histogram=hist[1],caps_valid=not bad,violations=bad)


def read_rows(path):
    lines = path.read_bytes().splitlines()
    n = len(lines)
    ensure(n in (21,22) and all(len(line)==n and set(line) <= {48,49} for line in lines),
           'adjacency shape/alphabet')
    return [sum(1 << j for j,bit in enumerate(line) if bit==49) for line in lines]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--spec',type=Path)
    parser.add_argument('--rows',type=Path)
    parser.add_argument('--require-valid',action='store_true')
    args = parser.parse_args()
    ensure(bool(args.spec) != bool(args.rows), 'choose exactly one graph input')
    rows = block_rows(json.loads(args.spec.read_text())) if args.spec else read_rows(args.rows)
    result = summary(rows)
    if args.require_valid:
        ensure(result['caps_valid'], 'candidate contains a forbidden book')
    print(json.dumps(result,sort_keys=True))


if __name__ == '__main__':
    main()
