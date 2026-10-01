"""Exact author controls for SUPPORT.md; no computation is a theorem premise.
Actual author: six-books-2, role researcher. Standard library, sequential.
The literal lifts sample complement blocks and signs; they are not witnesses.
"""
from itertools import combinations, product
import argparse
import json
from pathlib import Path
from random import Random


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def partitions(total, least=1):
    """Nondecreasing positive partitions, including () at total zero."""
    if total == 0:
        yield ()
    for first in range(least, total + 1):
        for rest in partitions(total - first, first):
            yield (first,) + rest


def degree_budget_control():
    counts = {}
    boundary = []
    for total in range(0, 11, 2):
        sequences = list(partitions(total))
        require(len(sequences) == len(set(sequences)), 'partition uniqueness')
        counts[str(total)] = len(sequences)
        for sequence in sequences:
            require(sum(sequence) == total, 'partition degree budget')
            v = len(sequence)
            h = sum(degree >= 3 for degree in sequence)
            require(v + 2 * h <= total, 'all positive degrees imply v+2h budget')
            if v + h >= 9:
                boundary.append(list(reversed(sequence)))
    require(counts == {'0': 1, '2': 2, '4': 5, '6': 11, '8': 22, '10': 42},
            'complete degree-partition counts')
    require(boundary == [[1] * 10, [2] + [1] * 8, [3] + [1] * 7],
            'only the three written boundary degree sequences')
    return {'even_degree_sums': list(range(0, 11, 2)),
            'partition_counts': counts, 'positive_degree_sequences': sum(counts.values()),
            'v_plus_h_at_least_nine': boundary,
            'nongraphical_sequences_included': True,
            'finite_theorem_premise': False}


def run_controls():
    rows = list(product((-1, 1), repeat=8))
    ones = (1,) * 8
    row_domains = {}
    for target in (-4, 2):
        candidates = [r for r in rows if dot(ones, r) == target]
        attempts = len(candidates) ** 2
        triples = sum(dot(a, b) == target for a, b in product(candidates, repeat=2))
        require(triples == 0, 'impossible normalized three-row target')
        row_domains[str(target)] = {'second_rows': len(candidates),
                                   'third_row_attempts': attempts, 'triples': triples}
    require(row_domains == {'-4': {'second_rows': 28, 'third_row_attempts': 784, 'triples': 0},
                            '2': {'second_rows': 56, 'third_row_attempts': 3136, 'triples': 0}},
            'complete normalized eight-sign domains')
    require(dot((1,) * 9, (1,) * 6 + (-1,) * 3) == 3,
            'two-row entirely-matching algebra positive control')
    pairs = tuple(combinations(range(11), 2))
    triangle = ((0, 1), (0, 2), (1, 2))
    classes = {1: 0, -1: 0}
    lifts = spines = inside_spines = formulas = 0
    general_matching_spines = red_uniform_sums = 0
    for signs in product((-1, 1), repeat=3):
        t = signs[0] * signs[1] * signs[2]
        switches = (1, t * signs[0], t * signs[1])
        require(all(switches[i] * signs[k] * switches[j] == t
                    for k, (i, j) in enumerate(triangle)), 'complete triangle switching')
        b = [[0 if i == j else t for j in range(3)] for i in range(3)]
        gram = [[(10 if i == j else 0) - 3 * b[i][j]
                 - sum(b[i][k] * b[k][j] for k in range(3))
                 for j in range(3)] for i in range(3)]
        require(gram == [[8 if i == j else (-4 if t == 1 else 2)
                          for j in range(3)] for i in range(3)], 'exact reduced Gram')
        classes[t] += 1
        for word, seed in product(range(8), range(4)):
            rng = Random(seed)
            w = [[0] * 11 for _ in range(11)]
            s = [[0] * 11 for _ in range(11)]
            for i, j in pairs:
                value = 0 if i < 3 else (0, 1, -1, rng.choice((-1, 0, 1)))[seed]
                w[i][j] = w[j][i] = value
                if not value:
                    sign = signs[triangle.index((i, j))] if j < 3 else rng.choice((-1, 1))
                    s[i][j] = s[j][i] = sign
            outside = (0, 255, 85, rng.randrange(256))[seed]
            inside = [(word >> i & 1) if i < 3 else (outside >> (i - 3) & 1)
                      for i in range(11)]
            rn = [set() for _ in range(22)]

            def add(a, b):
                rn[a].add(b)
                rn[b].add(a)

            for i in range(11):
                if inside[i]:
                    add(2 * i, 2 * i + 1)
            for i, j in pairs:
                for a, c in product(range(2), repeat=2):
                    if w[i][j] == 1 or (not w[i][j] and (a == c) == (s[i][j] == 1)):
                        add(2 * i + a, 2 * j + c)
            vertices = set(range(22))
            bn = [vertices - {i} - rn[i] for i in range(22)]
            u = [sum(row) for row in w]
            for i, j in pairs:
                if not w[i][j]:
                    w2 = sum(w[i][k] * w[k][j] for k in range(11))
                    s2 = sum(s[i][k] * s[k][j] for k in range(11))
                    for a, c in product(range(2), repeat=2):
                        x, y = 2 * i + a, 2 * j + c
                        red = y in rn[x]
                        pages = len(rn[x] & rn[y]) if red else len(bn[x] & bn[y])
                        correction = u[i] + u[j] + s[i][j] * s2
                        require(2 * pages == 9 + w2 + (correction if red else -correction),
                                'general matching page identity (1)')
                        general_matching_spines += 1
                elif w[i][j] == 1:
                    actual_sum = sum(len(rn[2 * i] & rn[2 * j + c]) for c in range(2))
                    quotient_sum = sum((1 + w[i][k]) * (1 + w[j][k])
                                       for k in range(11) if k not in (i, j))
                    require(actual_sum == quotient_sum + 2 * (inside[i] + inside[j]),
                            'general red uniform sum identity (3)')
                    red_uniform_sums += 1
            bad = False
            for i, j in triangle:
                s2 = sum(s[i][k] * s[k][j] for k in range(11))
                for a, c in product(range(2), repeat=2):
                    x, y = 2 * i + a, 2 * j + c
                    red = y in rn[x]
                    pages = len(rn[x] & rn[y]) if red else len(bn[x] & bn[y])
                    require(2 * pages == 9 + (s[i][j] * s2 if red else -s[i][j] * s2),
                            'literal entirely-matching spine formula')
                    spines += 1
                    formulas += 1
                    bad |= pages > (3 if red else 6)
            require(bad, 'every sampled pure-matching triangle has a forbidden spine')
            for i in range(3):
                a, c = 2 * i, 2 * i + 1
                pages = len(rn[a] & rn[c]) if inside[i] else len(bn[a] & bn[c])
                require(pages == 0, 'inside entirely-matching spine has zero pages')
                inside_spines += 1
            lifts += 1
    require(classes == {1: 4, -1: 4}, 'all eight sign triangles')
    require((lifts, spines, inside_spines, formulas) == (256, 3072, 768, 3072),
            'complete literal sampling coverage')
    return {'agent': 'six-books-2', 'role': 'researcher', 'complete': True,
                      'written_analytic_proof': 'SUPPORT.md', 'row_domains': row_domains,
                      'all_triangle_blocks': 8,
                      'triangle_product_classes': {str(k): v for k, v in classes.items()},
                      'deterministic_full_size_lifts': lifts,
                      'literal_triangle_spines': spines, 'literal_formula_checks': formulas,
                      'literal_inside_spines': inside_spines,
                      'general_matching_spine_checks': general_matching_spines,
                      'red_uniform_sum_checks': red_uniform_sums,
                      'every_sample_has_triangle_book_spine': True,
                      'all_other_blocks_arbitrary_in_written_proof': True,
                      'sample_outside_block_patterns': ['all_matching', 'all_red', 'all_blue', 'mixed'],
                      'controls_not_theorem_premise': True,
                      'full_matching_sign_enumeration': False,
                      'two_row_positive_control': True,
                      'degree_budget': degree_budget_control()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path,
                        default=Path(__file__).with_name('support_expected.json'))
    parser.add_argument('--emit', action='store_true',
                        help='emit regenerated controls without reading the expected summary')
    args = parser.parse_args()
    actual = run_controls()
    if not args.emit:
        expected = json.loads(args.expected.read_text())
        require(actual == expected, 'exact expected-summary mismatch')
    print(json.dumps(actual, indent=2) + '\n', end='')


if __name__ == '__main__':
    main()
