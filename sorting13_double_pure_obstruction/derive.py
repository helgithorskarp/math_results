"""Reproduce compact evidence using packed thresholds and closed classification.

The independent checker uses scalar ranks/ports and separate route enumeration.
Author: six-sorting-2, researcher.
"""
import argparse
import hashlib
import itertools
import json
from collections import deque
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIELDS = ['max5', 'max6', 'min1', 'high160', 'two_ones', 'union128_254', 'union160_254']
INITIAL = [(5, 6, 1, 160, x, 0, 0) for x in (40, 48)]
PAIRS = tuple(itertools.combinations(range(8), 2))
LOWER = [0, 0, 1, 3, 5, 9, 12, 16, 19, 25, 29, 35]


def move(state, a, b):
    return state ^ ((1 << a) | (1 << b)) if state >> a & 1 and not state >> b & 1 else state


def word_image(states, word, start, end):
    image = set()
    for state in states:
        for a, b in word:
            state = move(state, a, b)
        image.add((state >> start) & ((1 << (end-start))-1))
    return sorted(image)


def minimum_words():
    result = []

    def visit(pos, unary):
        result.append(unary + [[0, pos], [0, 1]])
        if len(unary) == 2:
            return
        for partner in range(2, 9):
            if partner != pos:
                pair = sorted((pos, partner))
                visit(pair[0], unary + [pair])

    visit(5, [])
    return result


def audit_fixture(f):
    words = minimum_words()
    assert words == f['minimum_kernel_words'] and len(words) == 43
    assert hashlib.sha256(json.dumps(words, separators=(',', ':')).encode()).hexdigest() == f['minimum_kernel_sha256']
    assert word_image(f['K_states'], f['pure_minimum'], 1, 10) == f['L_states']
    for case in f['cases']:
        assert word_image(f['L_states'], case['maximum_prefix'], 0, 8) == case['states']
    # Find strongest witnesses for the two specified mixed pairs. Enumeration
    # is discovery/reproduction; the proof only needs the selected witnesses.
    best = [{}, {}, {}]
    physical = [[(a+1, b+1) for a, b in c['maximum_prefix']] for c in f['cases']]
    for colors in itertools.product(range(3), repeat=11):
        values = list(colors); deleted = 0
        for index, section in enumerate((f['prefix'], f['after'] + f['pure_minimum'])):
            for a, b in section:
                deleted += values[a] != 1 or values[b] != 1
                values[a], values[b] = min(values[a], values[b]), max(values[a], values[b])
            if index == 0:
                values = [values[i] for i in f['prefix_output_order']]
        for c, word in enumerate(physical):
            out = list(values); d = deleted
            for a, b in word:
                d += out[a] != 1 or out[b] != 1
                out[a], out[b] = min(out[a], out[b]), max(out[a], out[b])
            x = sum((v == 2) << i for i, v in enumerate(out[1:9]))
            y = sum((v != 0) << i for i, v in enumerate(out[1:9]))
            if (x, y) not in ((128, 254), (160, 254)):
                continue
            cap = 35 - LOWER[colors.count(1)] - d
            if (x, y) not in best[c] or cap < best[c][x, y]['cap']:
                best[c][x, y] = dict(x=x, y=y, cap=cap, deleted=d,
                                     fixed_high=[i for i, v in enumerate(colors) if v == 2],
                                     fixed_low=[i for i, v in enumerate(colors) if v == 0],
                                     middle_count=colors.count(1))
    for c, case in enumerate(f['cases']):
        assert [best[c][key] for key in ((128, 254), (160, 254))] == case['witnesses']
    return dict(ternary_inputs=3**11, minimum_words=len(words), image_sizes=[len(c['states']) for c in f['cases']])


def step(state, pair):
    p5, p6, pmin, high, test, u1, u2 = state
    a, b = pair
    u1 += a == 0 or b == 7
    u2 += a == 0 or bool(high & ((1 << a) | (1 << b)))
    if u1 > 2 or u2 > 3:
        return None
    return (b if p5 == a else p5, b if p6 == a else p6, a if pmin == b else pmin,
            move(high, a, b), move(test, a, b), u1, u2)


def main(path):
    if not __debug__:
        raise RuntimeError('Run without Python optimization')
    f = json.loads((HERE / 'fixture.json').read_text())
    audit = audit_fixture(f)
    seen = set(INITIAL); todo = deque(INITIAL)
    while todo:
        for pair in PAIRS:
            nxt = step(todo[0], pair)
            if nxt is not None and nxt not in seen:
                seen.add(nxt); todo.append(nxt)
        todo.popleft()
    assert not any(s[:5] == (7, 7, 0, 192, 192) for s in seen)
    result = dict(agent='six-sorting-2', role='researcher', wires=8, fields=FIELDS,
                  initials=[list(s) for s in INITIAL], bounds=dict(union128_254=2, union160_254=3),
                  excluded=dict(max5=7, max6=7, min1=0, high160=192, two_ones=192),
                  states=[list(s) for s in sorted(seen)])
    path.write_text(json.dumps(result, separators=(',', ':'), sort_keys=True) + '\n')
    print(json.dumps(dict(audit, closed_states=len(seen), certificate_bytes=path.stat().st_size,
                         certificate_sha256=hashlib.sha256(path.read_bytes()).hexdigest()), sort_keys=True))


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--path', type=Path, required=True)
    main(p.parse_args().path)
