"""Literal controls for the blue-five-cycle local obstruction in EIGHT.md.
Author: six-books-2, role researcher. Imports no campaign program.
These sample matching signs and outside blocks; the local proof is analytic.
"""
from itertools import combinations, product
import json
from math import prod
from random import Random

Q = 11
PAIRS = tuple(combinations(range(Q), 2))
BLUE = {(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)}
CHORDS = ((0, 2), (2, 4), (1, 4), (1, 3), (0, 3))
CLASSES = {
    'no_red': set(),
    'one_red': {(0, 2)},
    'two_red_adjacent': {(0, 2), (2, 4)},
    'two_red_disjoint': {(0, 2), (1, 4)},
    'three_red_path': {(0, 2), (2, 4), (1, 4)},
    'three_red_path_and_edge': {(0, 2), (2, 4), (1, 3)},
    'four_red': {(0, 2), (2, 4), (1, 4), (1, 3)},
    'five_red': set(CHORDS),
}


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def classify(red):
    for name, representative in CLASSES.items():
        for shift, direction in product(range(5), (1, -1)):
            mapping = lambda i: (shift + direction * i) % 5
            image = {tuple(sorted((mapping(i), mapping(j)))) for i, j in representative}
            if red == image:
                return name
    raise RuntimeError('uncovered blue-cycle chord class')


def lift(red, word, seed):
    rng = Random(seed)
    w = [[0] * Q for _ in range(Q)]
    s = [[0] * Q for _ in range(Q)]
    for i, j in PAIRS:
        if (i, j) in BLUE:
            value = -1
        elif (i, j) in red:
            value = 1
        elif i >= 5:
            value = (0, 1, -1, rng.choice((-1, 0, 1)))[seed]
        else:
            value = 0
        w[i][j] = w[j][i] = value
        if value == 0:
            s[i][j] = s[j][i] = rng.choice((-1, 1))
    outside_word = (0, 63, 21, rng.randrange(64))[seed]
    inside = [(word >> i & 1) if i < 5 else (outside_word >> (i - 5) & 1)
              for i in range(Q)]
    red_neighbor = [set() for _ in range(2 * Q)]

    def add(a, b):
        red_neighbor[a].add(b)
        red_neighbor[b].add(a)

    for i in range(Q):
        if inside[i]:
            add(2 * i, 2 * i + 1)
    for i, j in PAIRS:
        for a, b in product(range(2), repeat=2):
            if w[i][j] == 1 or (w[i][j] == 0 and (a == b) == (s[i][j] == 1)):
                add(2 * i + a, 2 * j + b)
    vertices = set(range(2 * Q))
    blue_neighbor = [vertices - {i} - red_neighbor[i] for i in range(2 * Q)]
    return w, s, inside, red_neighbor, blue_neighbor


def main():
    rows = tuple(product((-1, 1), repeat=6))
    orthogonal_pairs = 0
    for left, right in product(rows, repeat=2):
        if sum(a * b for a, b in zip(left, right)) == 0:
            orthogonal_pairs += 1
            require(prod(left) == -prod(right), 'six-sign orthogonality graph is bipartite')
    require(orthogonal_pairs == 1280, 'complete ordered orthogonal-pair control')
    positive = ((1, 1, 1, 1), (1, 1, -1, -1), (1, -1, 1, -1))
    require(all(sum(a * b for a, b in zip(left, right)) == 0
                for left, right in combinations(positive, 2)), 'order-four positive control')
    classes = {name: 0 for name in CLASSES}
    lifts = literal_spines = matching_pairs = uniform_pairs = inside_spines = 0
    for chord_word in range(32):
        red = {edge for bit, edge in enumerate(CHORDS) if chord_word >> bit & 1}
        classes[classify(red)] += 1
        for word, seed in product(range(32), range(4)):
            w, s, inside, rn, bn = lift(red, word, seed)
            u = [sum(row) for row in w]
            counts = {}
            found_book = False
            for a, b in combinations(range(10), 2):
                is_red = b in rn[a]
                pages = len((rn[a] & rn[b]) if is_red else (bn[a] & bn[b]))
                counts[a, b] = pages
                literal_spines += 1
                if pages > (3 if is_red else 6):
                    found_book = True
            require(found_book, 'every sampled lift has a literal forbidden core spine')
            for i in range(5):
                expected = 2 * sum(v == (1 if inside[i] else -1) for v in w[i])
                require(counts[2 * i, 2 * i + 1] == expected, 'literal inside-spine identity')
                inside_spines += 1
            for i, j in combinations(range(5), 2):
                w2 = sum(w[i][k] * w[k][j] for k in range(Q))
                s2 = sum(s[i][k] * s[k][j] for k in range(Q))
                if w[i][j] == 0:
                    red_bit = 0 if s[i][j] == 1 else 1
                    rpages = counts[2 * i, 2 * j + red_bit]
                    bpages = counts[2 * i, 2 * j + 1 - red_bit]
                    require(2 * rpages == 9 + u[i] + u[j] + w2 + s[i][j] * s2,
                            'literal matching red-spine identity')
                    require(2 * bpages == 9 - u[i] - u[j] + w2 - s[i][j] * s2,
                            'literal matching blue-spine identity')
                    matching_pairs += 1
                else:
                    color = w[i][j]
                    outside = sum((1 + color * w[i][k]) * (1 + color * w[j][k])
                                  for k in range(Q) if k not in (i, j))
                    own = 2 * (inside[i] + inside[j] if color == 1 else 2 - inside[i] - inside[j])
                    first, second = counts[2 * i, 2 * j], counts[2 * i, 2 * j + 1]
                    require(first + second == outside + own, 'literal uniform-spine sum identity')
                    require(first - second == s2, 'literal uniform-spine Gram difference')
                    uniform_pairs += 1
            lifts += 1
    require(classes == {name: 1 if name in ('no_red', 'five_red') else 5 for name in CLASSES},
            'complete eight-class chord coverage')
    require((lifts, literal_spines, matching_pairs, uniform_pairs, inside_spines)
            == (4096, 184320, 10240, 30720, 20480), 'complete literal control coverage')
    print(json.dumps({'agent': 'six-books-2', 'role': 'researcher', 'complete': True,
                      'chord_assignments': 32, 'dihedral_chord_classes': classes,
                      'six_sign_ordered_pairs': 4096,
                      'orthogonal_six_sign_ordered_pairs': orthogonal_pairs,
                      'all_orthogonal_pairs_have_opposite_row_products': True,
                      'order_four_positive_control': True,
                      'deterministic_lifted_graphs': lifts,
                      'literal_core_spine_checks': literal_spines,
                      'matching_pair_formula_checks': matching_pairs,
                      'uniform_pair_sum_and_difference_checks': uniform_pairs,
                      'inside_spine_formula_checks': inside_spines,
                      'every_sample_has_literal_book_spine': True,
                      'core_inside_patterns': 32, 'sign_seeds': [0, 1, 2, 3],
                      'outside_block_patterns': ['all_matching', 'all_red', 'all_blue', 'seeded_mixture'],
                      'full_matching_sign_enumeration': False,
                      'controls_not_local_theorem_premise': True}, indent=2))


if __name__ == '__main__':
    main()
