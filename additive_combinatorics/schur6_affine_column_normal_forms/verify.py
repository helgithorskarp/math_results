"""Independent definition-level checker. No solver or encoder imports."""
import argparse
import json
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


def verify_controls():
    root = Path(__file__).resolve().parent
    controls = json.loads((root/'controls.json').read_text())
    reports = []
    for data in controls:
        result = verify_word(data)
        a, word = data['axis_factor'], data['word']
        q1 = [word[5*q] if word[5*q] >= 2 else 0 for q in range(a)]
        q2 = [word[5*q+1] if word[5*q+1] >= 2 else 0 for q in range(a)]
        if 'lam' in data:
            assert all(q2[q] == q1[(data['lam']*q+data['delta']) % a] for q in range(a))
        if data['name'] == 'doubling_cap_attainment':
            assert a == 43 and q1 == q2 == [0]*43
            assert all(word[5*q-1] >= 2 for q in range(1,a))
            assert result['endpoint'] == 214
        if data['name'] == 'outside_all_affine_relations':
            assert (q1.count(0), q2.count(0)) == (37,9)
            assert all(c in q1 and c in q2 for c in range(2,6))
            # No bijection of the coordinates can relate sets of these sizes.
            result['residual_sizes'] = [37,9]
            result['outside_all_invertible_affine_relations'] = True
        result['name'] = data['name']
        reports.append(result)
    seed = json.loads((root/'scaffold.json').read_text())
    A = set(range(39,73))-{63}
    B = set(range(37,68))|{77}
    E = set(range(41,69))
    assert A == set(seed['first_column']) and B == set(seed['second_column'])
    assert E == set(seed['axis_class'])
    points = {5*q for q in E}
    for column,b in ((A,1),(B,2)):
        for q in column:
            points.update((5*q+b,545-5*q-b))
    assert points == set(seed['positions']) and len(points) == 158 and min(points) == 158
    assert all((x+y)%545 not in points for x in points for y in points)
    expected = json.loads((root/'expected.json').read_text())
    assert reports == expected['controls']
    return dict(status='PASS', controls=reports, scaffold='ONE_CLASS_ONLY',
                scaffold_points=158, scaffold_uncoloured=386)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('word_json', nargs='?')
    args = parser.parse_args()
    result = verify_word(json.loads(Path(args.word_json).read_text())) if args.word_json else verify_controls()
    print(json.dumps(result, indent=2))
