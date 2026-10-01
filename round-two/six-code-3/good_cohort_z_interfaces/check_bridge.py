"""Literal 34-map/45-triangle and two-seed certificate checks.

No producer, star-enumeration module, graph module or solver is imported.
This does not prove carrier completeness by itself; verify.py supplies that.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

FIXTURE_PIN = 'c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7'
SEED_PIN = '521f0b322523a340c302fa5f4ea86fd3803a73e3665194e8cff556c0d0635ff6'

def need(test, message):
    if not test:
        raise ValueError(message)

def decode(masks):
    need(all(type(m) is int and 0 < m < (1 << 18) for m in masks), 'word mask out of domain')
    words = [frozenset(p for p in range(18) if m >> p & 1) for m in masks]
    need(len(set(words)) == len(words) and all(len(w) == 5 for w in words), 'invalid literal words')
    need(all(len(a & b) <= 2 for a, b in itertools.combinations(words, 2)), 'literal packing collision')
    return words

def check(bridge, fixture, seeds):
    entries = bridge['raw_positive_maps']
    need(len(entries) == 34, 'wrong raw positive population')
    keys = [(row['product_index'], tuple(row['point_map'])) for row in entries]
    need(len(set(keys)) == 34, 'duplicated relative point map')
    retained = []
    triangles = []
    for row in entries:
        fi, (u, v, y) = row['first']
        si, (su, sv, sx, sb) = row['second']
        phi = row['point_map']
        need(len(phi) == 17 and set(phi) == set(range(18))-{y}, 'point map not a bijection')
        need((phi[su], phi[sv], phi[sx]) == (u, v, 17), 'distinguished point images differ')
        first_words = [frozenset(q) | {17} for q in fixture['stars'][fi]]
        second_words = [frozenset(phi[p] for p in q) | {y} for q in fixture['stars'][si]]
        words = decode(row['word_masks'])
        need(set(words) == set(first_words + second_words) and len(words) == 36, 'actual block images differ')
        need(sum(17 in w for w in words) == sum(y in w for w in words) == 20, 'center degree differs')
        need(sum({17, y} <= w for w in words) == 4, 'center pair count differs')
        points = []
        for t in sorted(set(range(18)) - {17, y, u, v}):
            multiplicities = [sum(pair <= w for w in words) for pair in ({17, y}, {17, t}, {y, t})]
            if multiplicities == [4, 4, 4] and not any({17, y, t} <= w for w in words):
                points.append(t)
                triangles.append(dict(product_index=row['product_index'], point_map=phi,
                                      triple=sorted((17, y, t)), pair_multiplicities=multiplicities))
        need(row['triangle_points'] == points, 'literal triangle witness list differs')
        if not points:
            retained.append(row)
    need(len(retained) == 2 and len(triangles) == 45, 'R0 survivor or witness population differs')
    caps = []
    for row in retained:
        matching = [seed for seed in seeds['seeds'] if seed['core_masks'] == row['word_masks']]
        need(len(matching) == 1, 'literal survivor not one of the published seeds')
        seed = matching[0]
        words = decode(seed['core_masks'])
        centers = seed['saturated_centers']
        need(set(centers) == {17, row['first'][1][2]}, 'published degree20 centers differ')
        need(len(words) == 36 and all(sum(p in w for w in words) == 20 for p in centers), 'seed center degrees')
        triples = [tuple(sorted(t)) for word in words for t in itertools.combinations(word, 3)]
        need(len(triples) == len(set(triples)) == 360, 'seed triple ownership')
        used = set(triples)
        candidates = [frozenset(q) for q in itertools.combinations(sorted(set(range(18))-set(centers)), 5)
                      if all(tuple(t) not in used for t in itertools.combinations(q, 3))]
        masks = [sum(1 << p for p in word) for word in candidates]
        candidate_sha = hashlib.sha256((json.dumps(masks, sort_keys=True, separators=(',', ':'))+'\n').encode()).hexdigest()
        need(candidate_sha == seed['candidate_sha256'] and len(candidates) == seed['candidate_count'], 'seed residual universe')
        colors = seed['colors']
        capacity = seed['capacity']
        need(len(colors) == len(candidates) and type(capacity) is int and capacity > 0, 'color population')
        need(all(type(c) is int and 0 <= c < capacity for c in colors), 'color label outside capacity')
        edges = 0
        for i, j in itertools.combinations(range(len(candidates)), 2):
            if len(candidates[i] & candidates[j]) <= 2:
                need(colors[i] != colors[j], 'compatible candidates share a color')
                edges += 1
        need(36+capacity == seed['upper_bound'], 'seed numerical total')
        caps.append(dict(product_index=row['product_index'], seed=seed['seed'],
                         words=36, candidates=len(candidates), edges=edges, colors=capacity, upper_bound=36+capacity))
    need(sorted(c['upper_bound'] for c in caps) == [61, 64], 'unexpected literal seed caps')
    return dict(status='PASS_LITERAL_BRIDGE_AND_SEED_CAPS', raw_positive_maps=34, rejected_maps=32,
                triangle_witnesses=45, retained_maps=2, caps=caps,
                triangles_sha256=hashlib.sha256(json.dumps(triangles, sort_keys=True, separators=(',', ':')).encode()).hexdigest())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bridge', required=True)
    parser.add_argument('--fixtures', required=True)
    parser.add_argument('--seeds', required=True)
    args = parser.parse_args()
    raw_fixture, raw_seeds = Path(args.fixtures).read_bytes(), Path(args.seeds).read_bytes()
    need(hashlib.sha256(raw_fixture).hexdigest() == FIXTURE_PIN, 'fixture source pin differs')
    need(hashlib.sha256(raw_seeds).hexdigest() == SEED_PIN, 'seed source pin differs')
    result = check(json.loads(Path(args.bridge).read_text()), json.loads(raw_fixture), json.loads(raw_seeds))
    print(json.dumps(result, sort_keys=True))

if __name__ == '__main__':
    main()
