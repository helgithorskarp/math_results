"""Early invariant separation from fixed known examples and catalog families."""
import argparse
import json
from collections import Counter
from hashlib import sha256
from pathlib import Path

from check import need, red

def rank(matrix):
    return binary_rank([sum(v << j for j, v in enumerate(row)) for row in matrix])


def g6(line):
    need(line and ord(line[0])-63 == 42, 'catalog order42')
    bits = [((ord(c)-63) >> j) & 1 for c in line[1:] for j in range(5, -1, -1)]
    need(len(bits) >= 861 and len(bits) < 867 and not any(bits[861:]), 'graph6 length/padding')
    rows = [0]*42
    k = 0
    for v in range(1, 42):
        for u in range(v):
            if bits[k]:
                rows[u] |= 1 << v
                rows[v] |= 1 << u
            k += 1
    return rows


def binary_rank(rows):
    basis = {}
    for row in rows:
        while row:
            j = row.bit_length()-1
            if j in basis:
                row ^= basis[j]
            else:
                basis[j] = row
                break
    return len(basis)


def complement(rows):
    return [((1 << len(rows))-1) ^ row ^ (1 << u) for u, row in enumerate(rows)]


def cyclic(toggles):
    lengths = {1, 2, 7, 10, 12, 13, 14, 16, 18, 20, 21}
    a = [[int(u != v and min(abs(u-v), 43-abs(u-v)) in lengths)
          for v in range(43)] for u in range(43)]
    for u in toggles:
        v = (u+1) % 43
        a[u][v] ^= 1
        a[v][u] ^= 1
    return a


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('catalog', type=Path)
    args = ap.parse_args()
    raw = args.catalog.read_bytes()
    need(sha256(raw).hexdigest() == '067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb', 'pinned catalog identity')
    graphs = [g6(line) for line in raw.decode().splitlines()]
    need(len(graphs) == 328, 'all supplied catalog records')
    histogram = Counter((binary_rank(a), binary_rank(complement(a))) for a in graphs)
    minimum = min(min(pair) for pair in histogram)
    need(minimum-2 > 26, 'all catalog switch/extension families separated')
    examples = {}
    for name, toggles in [
        ('cyclic43', []),
        ('primary_q2', [0,1,2,8,9,10,11,17,18,19,25,26,27,28,34,35,36,37]),
        ('known_secondary_q7', [2,5,8,11,14,17,20,22,25,28,31,34,37,40])
    ]:
        a = cyclic(toggles)
        ranks = [rank(a), rank([[int(i != j) ^ b for j, b in enumerate(row)]
                                for i, row in enumerate(a)])]
        need(min(ranks) > 26, 'named example separated in both orientations')
        examples[name] = ranks
    squares = {i*i % 41 for i in range(1, 41)}
    p41 = [[int(u != v and (u-v) % 41 in squares) for v in range(41)] for u in range(41)]
    r41 = rank(p41)
    # Binary rank alone does not separate Paley41. Instead use Seidel squares.
    # For any 41-point principal block T of a switch of S49, T^2-49I has
    # rank at most 1+8=9. For a switch of S41 it is -8I-ww^t, of rank41.
    p49 = [[red(u,v) for v in range(49)] for u in range(49)]
    base_ranks = [rank(p49), rank([[int(u != v) ^ p49[u][v] for v in range(49)] for u in range(49)])]
    need(base_ranks == [24, 24], 'base binary ranks in both colors')
    for n, a in [(41, p41), (49, p49)]:
        seidel = [[0 if i == j else 1-2*a[i][j] for j in range(n)] for i in range(n)]
        need(all(sum(seidel[i][k]*seidel[k][j] for k in range(n))
                 == n*int(i == j)-1 for i in range(n) for j in range(n)),
             'exact Seidel square identity')
    print(json.dumps({'status': 'VERIFIED_INVARIANT_SEPARATION_FROM_NAMED_OLD_FAMILIES',
                      'family_rank_upper_bound_both_colors': 26,
                      'paley49_base_red_blue_ranks': base_ranks,
                      'catalog_sha256': sha256(raw).hexdigest(),
                      'catalog_records': len(graphs),
                      'catalog_color_rank_pair_histogram': {str(k): v for k,v in sorted(histogram.items())},
                      'catalog_switch_extension_rank_lower_bound': minimum-2,
                      'paley41_rank': r41,
                      'paley41_binary_rank_test_separates': r41-2 > 26,
                      'paley41_seidel_square_rank_required': 41,
                      'paley49_41_point_seidel_square_rank_upper_bound': 9,
                      'named_example_red_blue_ranks': examples,
                      'scope': 'Separates all supplied catalog switch-plus-one families, the Paley41 switch-plus-two family, and the three named cyclic examples under relabeling and color reversal. Does not exhaust every vertex of the old cyclic sublevel components or claim historical novelty.'},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
