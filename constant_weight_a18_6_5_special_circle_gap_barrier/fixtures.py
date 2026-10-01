"""Standalone literal verification of three compact 68-word fixtures."""
from itertools import combinations
from common import digest, points, require


def check_fixture(circles, fixture):
    words = fixture['words']
    require(len(words) == len(set(words)) == 68, 'fixture repeats or omits a word')
    require(all(type(w) is int and 0 <= w < (1 << 18) for w in words),
            'fixture word outside 18-bit universe')
    sets = [frozenset(i for i in range(18) if w >> i & 1) for w in words]
    require(all(len(w) == 5 for w in sets), 'fixture has wrong weight')
    distances = [len(a ^ b) for a, b in combinations(sets, 2)]
    require(len(distances) == 2278 and min(distances) >= 6, 'fixture has incompatible pair')
    design = tuple(frozenset(points(c)) for c in circles)
    original = set(design) & set(sets)
    through = [w - {17} for w in sets if 17 in w]
    owners, fixed = [], []
    for q in through:
        candidates = [c for c, pts in zip(circles, design) if q <= pts]
        require(len(candidates) <= 1, 'replacement ownership ambiguous')
        if candidates:
            owners.append(candidates[0])
        else:
            fixed.append(sum(1 << p for p in q))
    require(len(owners) == len(set(owners)), 'fixture gives two words to one circle')
    original_masks = {sum(1 << p for p in c) for c in original}
    gaps = sorted(set(circles) - original_masks - set(owners))
    s = len([w for w in sets if 17 not in w and w not in set(design)])
    counts = {'size': len(words), 's': s, 't': len(fixed), 'a': len(owners),
              'R': 68 - len(original), 'g': len(gaps)}
    require(counts['size'] == 68 + s + counts['t'] - counts['g'], 'word count identity fails')
    for name, value in fixture['counts'].items():
        require(counts[name] == value, 'fixture parameter differs: ' + name)
    require(gaps == fixture['gaps'] and sorted(fixed) == [15], 'fixture gaps or fixed word differ')
    n = frozenset([4, 5, 6, 7, 16])
    q = frozenset([0, 1, 2, 3])
    require(any(len(frozenset(points(c)) & n) == len(frozenset(points(c)) & q) == 2
                for c in gaps), 'fixture has no special gap')
    return {'counts': counts, 'minimum_distance': min(distances),
            'words_sha256': digest(sorted(words))}
