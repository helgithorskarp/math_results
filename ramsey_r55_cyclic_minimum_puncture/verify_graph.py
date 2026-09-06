#!/usr/bin/env python3
"""Stand-alone edge-list verifier, independent of extension certificates."""
import itertools
import json
import sys


def check_text(text):
    lines = text.splitlines()
    if not lines:
        raise ValueError('empty graph')
    header = lines[0].split()
    if len(header) != 2:
        raise ValueError('expected n m header')
    n,m = map(int,header)
    if not 1 <= n <= 43 or not 0 <= m <= n*(n-1)//2 or len(lines) != m+1:
        raise ValueError('wrong graph size')
    matrix,rows,last = [[0]*n for _ in range(n)], [0]*n, (-1,-1)
    for line in lines[1:]:
        pair = tuple(map(int,line.split()))
        if len(pair) != 2:
            raise ValueError('edge length')
        u,v = pair
        if not 0 <= u < v < n or pair <= last:
            raise ValueError('edge ordering/labels')
        last = pair
        matrix[u][v] = matrix[v][u] = 1
        rows[u] |= 1 << v
        rows[v] |= 1 << u
    counts = [0,0]
    for q in itertools.combinations(range(n),5):
        color = matrix[q[0]][q[1]]
        if all(matrix[u][v] == color for u,v in itertools.combinations(q,2)):
            counts[color] += 1
    def count(rows):
        def visit(mask,k):
            if k == 1:
                return mask.bit_count()
            total = 0
            while mask.bit_count() >= k:
                bit = mask & -mask
                mask ^= bit
                total += visit(mask & rows[bit.bit_length()-1],k-1)
            return total
        return visit((1 << n)-1,5)
    blue = [((1 << n)-1) ^ (1 << v) ^ r for v,r in enumerate(rows)]
    if [count(blue),count(rows)] != counts:
        raise ValueError('independent clique counts disagree')
    return {'n':n,'red_edges':m,'blue_red_fives':counts,'ramsey_5_5':counts == [0,0]}


if __name__ == '__main__':
    with open(sys.argv[1],encoding='utf8') as f:
        print(json.dumps(check_text(f.read()),sort_keys=True))
