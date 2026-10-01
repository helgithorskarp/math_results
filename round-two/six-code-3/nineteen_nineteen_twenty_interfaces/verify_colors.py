"""Standalone literal verifier for each44-core residual color certificate.

No producer, old packing helper, mask graph or coloring code is imported.
Triple ownership generates all eligible five-sets; point intersections
verify every color conflict. Core coverage is the separate census premise.
"""
from itertools import combinations
import hashlib
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(value):
    return hashlib.sha256((json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()).hexdigest()


def check_record(core, row, index, domain_hash):
    require(row['status'] == 'COMPLETE_EXACT_PROPER_COLOR' and type(row['index']) is int
            and row['index'] == index and row['domain_sha256'] == domain_hash,
            'literal certificate status/index/domain')
    masks = core['blocks']
    require(type(masks) is list and len(masks) == 44 and
            all(type(mask) is int and 0 <= mask < (1 << 18) for mask in masks), 'literal44 mask domain')
    points = [tuple(i for i in range(18) if mask & (1 << i)) for mask in masks]
    require(all(len(word) == 5 for word in points) and len(set(points)) == 44, 'literal44 word size/distinctness')
    require(sha(masks) == core['core_sha256'] == row['core_sha256'], 'literal44 core checksum')
    occupied = set()
    for word in points:
        for triple in combinations(word, 3):
            require(triple not in occupied, 'literal44 repeated triple')
            occupied.add(triple)
    require(len(occupied) == 440, 'literal44 triple coverage')
    degrees = [sum(point in word for word in points) for point in (17, 15, 16)]
    pairs = [sum(a in word and b in word for word in points) for a, b in ((17, 15), (17, 16), (15, 16))]
    require(degrees == [19, 19, 20] and pairs == [5, 5, 4] and (15, 16, 17) not in occupied,
            'literal44 center/pair/uncovered hypotheses')
    candidates = [word for word in combinations(range(15), 5)
                  if not any(triple in occupied for triple in combinations(word, 3))]
    require(len(candidates) == row['candidate_count'] and sha(candidates) == row['candidate_sha256'],
            'literal full3003 candidate universe')
    colors = row['colors']
    require(type(colors) is list and len(colors) == len(candidates) and
            all(type(color) is int and color >= 0 for color in colors), 'literal color coverage/domain')
    capacity = max(colors, default=-1) + 1
    require(type(row['capacity']) is int and row['capacity'] == capacity, 'literal capacity declaration')
    sets = [frozenset(word) for word in candidates]
    edges = 0
    for i, first in enumerate(sets):
        for j in range(i + 1, len(sets)):
            if len(first & sets[j]) <= 2:
                require(colors[i] != colors[j], 'literal improper color certificate')
                edges += 1
    return {'candidates': len(candidates), 'edges': edges, 'capacity': capacity}
