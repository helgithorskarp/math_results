"""Literal fixture and CNF audit. Imports neither generator nor solver."""
import argparse
from collections import Counter
from itertools import combinations
import hashlib
import json
from pathlib import Path


def check_prefix(word, k):
    assert word and all(type(c) is int and 1 <= c <= k for c in word)
    rows = 0
    for z in range(2, len(word)+1):
        for x in range(1, z//2+1):
            assert not (word[x-1] == word[z-x-1] == word[z-1])
            rows += 1
    return rows


def check_block(prefix, word, k):
    assert word and all(type(c) is int and 1 <= c <= k for c in word)
    rows = 0
    for y in range(len(word)):
        for x in range(max(0, y-len(prefix)), y):
            assert not (word[x] == word[y] == prefix[y-x-1]), (x, y)
            rows += 1
    return rows


def expected_clauses(prefix, length, k):
    result = []
    for x in range(length):
        result.append(tuple(k*x+c for c in range(1, k+1)))
        result.extend(tuple(sorted((-k*x-c, -k*x-d)))
                      for c, d in combinations(range(1, k+1), 2))
    for y in range(length):
        for x in range(max(0, y-len(prefix)), y):
            c = prefix[y-x-1]
            result.append(tuple(sorted((-k*x-c, -k*y-c))))
    return Counter(result)


def check_cnf(path, data):
    raw = Path(path).read_bytes()
    lines = raw.decode().splitlines()
    header = lines[0].split()
    assert header == ['p', 'cnf', str(data['upper_variables']), str(data['upper_clauses'])]
    actual = []
    for line in lines[1:]:
        row = list(map(int, line.split()))
        assert row and row[-1] == 0 and 0 not in row[:-1]
        assert all(1 <= abs(t) <= data['upper_variables'] for t in row[:-1])
        actual.append(tuple(sorted(row[:-1])))
    prefix = list(map(int, data['prefix']))
    expected = expected_clauses(prefix, data['upper_length'], data['palette_size'])
    assert len(actual) == data['upper_clauses'] and Counter(actual) == expected
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == data['upper_cnf_sha256']
    return {'variables': data['upper_variables'], 'clauses': len(actual), 'sha256': digest}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--cnf')
    args = p.parse_args()
    data = json.loads(Path(__file__).with_name('data.json').read_text())
    k = data['palette_size']
    prefix = list(map(int, data['prefix']))
    block = list(map(int, data['compatible_block']))
    assert len(prefix) == 77 and len(block) == data['span'] == 82
    result = {'prefix_length': len(prefix), 'prefix_Schur_rows': check_prefix(prefix, k),
              'compatible_length': len(block), 'compatible_pairs': check_block(prefix, block, k)}
    full = list(map(int, data['attaining_word']))
    assert full == prefix+[6]*78+block and len(full) == 237
    result['attaining_full_word_length'] = len(full)
    result['attaining_full_Schur_rows'] = check_prefix(full, 6)
    result['attaining_full_doubling_rows'] = len(full)//2
    partial = list(map(int, data['source_partial_uv']))
    assert all(1 <= c <= k for c in partial)
    points = list(range(1, 78))+list(range(155, 305))
    assert len(partial) == len(points) and partial[:77] == prefix
    fixed = dict(zip(points, partial))
    bad = [(x, z-x, z) for z in points for x in range(1, z//2+1)
           if x in fixed and z-x in fixed and fixed[x] == fixed[z-x] == fixed[z]]
    assert bad == [(1, 232, 233), (3, 231, 234)]
    empty = 0
    for z in range(305, 460):
        forbidden = {fixed[x] for x in range(1, z//2+1)
                     if x in fixed and z-x in fixed and fixed[x] == fixed[z-x]}
        empty += len(forbidden) == k
    assert empty == 0
    result['source_partial_base_defects'] = bad
    result['source_partial_empty_tail_lists'] = empty
    control = data['positive_control']
    cp, cb = list(map(int, control['prefix'])), list(map(int, control['compatible_block']))
    assert len(cp) == 77 and len(cb) == control['length'] == 155
    result['control_prefix_rows'] = check_prefix(cp, k)
    result['control_compatible_pairs'] = check_block(cp, cb, k)
    # Explicitly verify that the semantic checker rejects a monochromatic adjacent pair.
    altered = list(block)
    altered[0] = altered[1] = prefix[0]
    try:
        check_block(prefix, altered, k)
    except AssertionError:
        result['corrupted_block_rejected'] = True
    else:
        raise AssertionError('corrupted block accepted')
    if args.cnf:
        result['cnf'] = check_cnf(args.cnf, data)
    result['upper_bound_checked_by_this_script'] = False
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
