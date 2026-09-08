"""Standard C5[C5] core and a deterministic one-vertex obstruction."""
from itertools import combinations


def cycle_edge(i, j):
    return (i-j) % 5 in (1, 4)


def core_edge(u, v):
    i, a = divmod(u, 5)
    j, b = divmod(v, 5)
    return cycle_edge(a, b) if i == j else cycle_edge(i, j)


def inner(word):
    red = next(([i,j] for i,j in combinations(range(5),2)
                if word >> i & 1 and word >> j & 1 and cycle_edge(i,j)), None)
    blue = next(([i,j] for i,j in combinations(range(5),2)
                 if not (word >> i & 1) and not (word >> j & 1) and not cycle_edge(i,j)), None)
    tag = int(red is not None) + 2*int(blue is not None)
    if not tag:
        raise ValueError('inner cycle covering lemma failed')
    return dict(word=word, tag=tag, red_pair=red, blue_pair=blue)


def outer(tags):
    for color, flag in (('red',1), ('blue',2)):
        for i,j in combinations(range(5),2):
            if tags[i] & flag and tags[j] & flag and cycle_edge(i,j) == (color == 'red'):
                return dict(tags=list(tags), color=color, blocks=[i,j])
    raise ValueError('outer cycle covering lemma failed')


def obstruction(word):
    if type(word) is not int or not 0 <= word < (1 << 25):
        raise ValueError('25-bit attachment')
    parts = [inner((word >> (5*i)) & 31) for i in range(5)]
    out = outer([p['tag'] for p in parts])
    pair_key = out['color']+'_pair'
    vertices = [25]
    for i in out['blocks']:
        vertices.extend(5*i+j for j in parts[i][pair_key])
    return dict(color=out['color'], vertices=sorted(vertices))
