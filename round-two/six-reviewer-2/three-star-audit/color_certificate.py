#!/usr/bin/env python3
"""Generate and literally check a complete color-transversal obstruction tree."""
import argparse
from itertools import combinations
import json
from pathlib import Path
import time
from audit import digest, points, require


def generate(core_hash, words, colors):
    n = len(words)
    require(len(colors) == n and set(colors) == set(range(20)), 'twenty-color domain')
    adjacent = [sum(1 << j for j, b in enumerate(words)
                    if i != j and (a & b).bit_count() <= 2) for i, a in enumerate(words)]
    require(all(colors[i] != colors[j] for i in range(n) for j in range(n)
                if adjacent[i] & (1 << j)), 'improper generated coloring')
    domains = {c: sum(1 << i for i, v in enumerate(colors) if v == c) for c in range(20)}
    nodes = 0
    started = time.monotonic()

    def visit(left):
        nonlocal nodes
        nodes += 1
        if nodes > 2000000 or (nodes % 1024 == 0 and time.monotonic()-started > 20):
            raise RuntimeError('INCOMPLETE color-tree generation guard')
        require(bool(left), 'compatible twenty-word transversal exists')
        color = min(left, key=lambda c: (left[c].bit_count(), c))
        possible = left[color]
        rest = {c: domain for c, domain in left.items() if c != color}
        branches = []
        while possible:
            bit = possible & -possible
            possible -= bit
            v = bit.bit_length()-1
            branches.append([v, visit({c: domain & adjacent[v] for c, domain in rest.items()})])
        return {'color': color, 'branches': branches}

    tree = visit(domains)
    return {'format': 'three-star-color-v1', 'core_sha256': core_hash,
            'candidate_sha256': digest([points(w) for w in words]), 'colors': colors,
            'color_count': 20, 'tree': tree, 'nodes': nodes}


def check(certificate, core_hash, words):
    """The checker uses literal sets and rebuilds each branch domain anew."""
    require(certificate['format'] == 'three-star-color-v1', 'color certificate format')
    require(certificate['core_sha256'] == core_hash and
            certificate['candidate_sha256'] == digest([points(w) for w in words]), 'color carrier binding')
    colors = certificate['colors']
    require(type(colors) is list and len(colors) == len(words) and
            all(type(c) is int and 0 <= c < 20 for c in colors) and
            set(colors) == set(range(20)) and certificate['color_count'] == 20, 'color label domain')
    sets = [frozenset(points(w)) for w in words]
    require(all(colors[i] != colors[j] for i, j in combinations(range(len(sets)), 2)
                if len(sets[i] & sets[j]) <= 2), 'color classes are not incompatible')
    nodes, leaves = 0, 0

    def visit(node, remaining, chosen):
        nonlocal nodes, leaves
        nodes += 1
        require(nodes <= 2000000 and bool(remaining), 'color tree guard or twenty-word leaf')
        require(type(node) is dict and set(node) == {'color', 'branches'}, 'color node shape')
        color = node['color']
        require(type(color) is int and color in remaining, 'tree repeats/invalidates color')
        branches = node['branches']
        require(type(branches) is list and all(type(row) is list and len(row) == 2 and
                type(row[0]) is int for row in branches), 'color branch shape')
        actual = [row[0] for row in branches]
        expected = {i for i, c in enumerate(colors) if c == color and
                    all(len(sets[i] & sets[j]) <= 2 for j in chosen)}
        require(len(actual) == len(set(actual)) and set(actual) == expected, 'color branch coverage')
        if not branches:
            leaves += 1
        for v, child in branches:
            visit(child, remaining-{color}, chosen+[v])

    visit(certificate['tree'], set(range(20)), [])
    require(type(certificate['nodes']) is int and nodes == certificate['nodes'], 'color tree node count')
    return {'status': 'COMPLETE_LITERAL', 'core_sha256': core_hash,
            'nodes': nodes, 'empty_domain_leaves': leaves, 'additional_bound': 19}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--universes', type=Path, required=True)
    parser.add_argument('--colors', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    source = json.loads(args.colors.read_text())
    core_hash = source['core_sha256']
    words = next(words for h, words, bound in json.loads(args.universes.read_text()) if h == core_hash)
    cert = generate(core_hash, words, source['colors'])
    result = check(cert, core_hash, words)
    args.output.write_text(json.dumps(cert, sort_keys=True, separators=(',', ':'))+'\n')
    print(json.dumps(result))
