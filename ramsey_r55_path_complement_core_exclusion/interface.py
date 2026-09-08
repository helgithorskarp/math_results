"""Discriminate an explicitly supplied 26-core in a full physical graph."""
from itertools import combinations, permutations
import json
import sys


def inspect(candidate):
    if set(candidate) != {'n', 'red_bits_hex', 'core'} or candidate['n'] != 43:
        raise ValueError('Expected n=43, red_bits_hex, core')
    h = candidate['red_bits_hex']
    if (type(h) is not str or len(h) != 226 or
            any(c not in '0123456789abcdef' for c in h) or int(h, 16) >= 2**903):
        raise ValueError('Expected 903 physical bits in 226 lowercase hex digits')
    core = candidate['core']
    if (type(core) is not list or len(core) != 26 or
            any(type(v) is not int or not 0 <= v < 43 for v in core) or
            core != sorted(set(core))):
        raise ValueError('Expected sorted 26 distinct physical core labels')
    edges = {uv: (int(h, 16) >> k) & 1
             for k, uv in enumerate(combinations(range(43), 2))}
    pairs = list(combinations(range(5), 2))
    patterns = {}
    for perm in permutations(range(5)):
        path = {tuple(sorted((perm[i], perm[i+1]))) for i in range(4)}
        word = sum(1 << k for k, uv in enumerate(pairs) if uv in path)
        patterns.setdefault(word, (1, perm))
        patterns.setdefault(1023-word, (0, perm))
    homogeneous = None
    checked = 0
    for s in combinations(core, 5):
        checked += 1
        word = sum(edges[s[i], s[j]] << k for k, (i, j) in enumerate(pairs))
        if word in patterns:
            color, order = patterns[word]
            return {'status': 'OUTSIDE_SPECIFIED_EXCLUDED_CLASS',
                    'meaning': 'This supplied core contains a path or its complement; no target verdict',
                    'certificate': {'kind': 'induced_path', 'color': color,
                                    'vertices': [s[i] for i in order]},
                    'core_five_sets_checked': checked}
        if word in (0, 1023) and homogeneous is None:
            homogeneous = {'kind': 'monochromatic5', 'color': int(word == 1023),
                           'vertices': list(s)}
    if homogeneous is None:
        raise RuntimeError('A class member violates the proved upper bound; audit required')
    return {'status': 'EXCLUDED_CLASS_WITH_PHYSICAL_K5_CERTIFICATE',
            'meaning': 'The supplied core is path/complement-path free and the full graph fails good43',
            'certificate': homogeneous, 'core_five_sets_checked': checked}


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: interface.py CANDIDATE.json')
    with open(sys.argv[1]) as stream:
        candidate = json.load(stream)
    print(json.dumps(inspect(candidate), indent=2, sort_keys=True))
