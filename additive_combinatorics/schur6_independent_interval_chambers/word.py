"""Independent definition-level checker. No solver or encoder imports."""
import argparse
import json
import math
from pathlib import Path


def verify_word(data):
    a = data['axis_factor']
    k = data.get('colours', 6)
    word = data['word']
    n = 5*a
    assert type(a) is int and a >= 1 and a % 2 and len(word) == n-1
    assert all(type(c) is int and 0 <= c < k for c in word)
    row = [None, *word]
    assert all(row[x] == row[n-x] for x in range(1, n))
    for q in range(a):
        assert row[5*q+1] in [0, *range(2, k)]
        assert row[5*q+2] in [1, *range(2, k)]
    fixed = data.get('fixed_class')
    if fixed:
        c = fixed['colour']
        assert {q for q in range(a) if row[5*q+1] == c} == set(fixed['first_column'])
        assert {q for q in range(a) if row[5*q+2] == c} == set(fixed['second_column'])
        assert {q for q in range(1, a) if row[5*q] == c} == set(fixed['axis_class'])
    ordinary = modular = doublings = 0
    for x in range(1, n):
        for y in range(x, n):
            z = (x+y) % n
            if z:
                modular += 1
                assert not (row[x] == row[y] == row[z]), ('modular', x, y, z)
            if x+y < n:
                ordinary += 1
                doublings += (x == y)
                assert not (row[x] == row[y] == row[x+y]), ('integer', x, y, x+y)
    return dict(status='COMPLETE_WORD_VERIFIED', endpoint=n-1,
                class_sizes=[word.count(c) for c in range(k)],
                ordinary_pairs=ordinary, modular_pairs=modular,
                integer_doublings=doublings,
                columns_equal=all((row[5*q+1] if row[5*q+1] >= 2 else -1) ==
                                  (row[5*q+2] if row[5*q+2] >= 2 else -1) for q in range(a)))


def transform_word(word, u):
    n = len(word)+1
    assert n % 5 == 0 and math.gcd(u, n) == 1
    swap = u % 5 in (2, 3)
    image = [None]*n
    for x, c in enumerate(word, 1):
        image[u*x % n] = 1-c if swap and c in (0, 1) else c
    assert all(c is not None for c in image[1:])
    return image[1:]



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('word_json')
    args = parser.parse_args()
    print(json.dumps(verify_word(json.loads(Path(args.word_json).read_text())), indent=2))
