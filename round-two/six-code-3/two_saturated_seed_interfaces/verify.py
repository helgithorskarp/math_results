"""Standalone literal two-seed completion bounds; standard library only."""
import argparse
import copy
import hashlib
from itertools import combinations
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(value):
    return hashlib.sha256((json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()).hexdigest()


def check(row):
    masks = row['core_masks']
    require(type(masks) is list and len(masks) == 36 and
            all(type(q) is int and 0 <= q < (1 << 18) for q in masks), 'literal36 mask domain')
    words = [frozenset(i for i in range(18) if q & (1 << i)) for q in masks]
    require(len(set(words)) == 36 and all(len(w) == 5 for w in words), 'literal36 distinct five-sets')
    occupied = set()
    for word in words:
        for triple in combinations(sorted(word), 3):
            require(triple not in occupied, 'literal36 repeated triple')
            occupied.add(triple)
    require(len(occupied) == 360, 'literal36 complete triple ownership')
    centers = row['saturated_centers']
    require(centers == [17, 11] and all(sum(p in w for w in words) == 20 for p in centers),
            'literal36 completed degree20 centers')
    require(all(set(centers) & w for w in words) and sum(set(centers) <= w for w in words) == 4,
            'literal36 complete two-star union')
    ordinary = [p for p in range(18) if p not in centers]
    # Literal triple ownership reconstructs all4368 eligible ordinary five-sets.
    candidates = [w for w in combinations(ordinary, 5)
                  if all(t not in occupied for t in combinations(w, 3))]
    masks = [sum(1 << p for p in w) for w in candidates]
    require(len(candidates) == row['candidate_count'] and sha(masks) == row['candidate_sha256'],
            'literal complete4368 candidate universe')
    colors = row['colors']
    require(type(colors) is list and len(colors) == len(candidates) and
            all(type(c) is int and c >= 0 for c in colors), 'literal proper-color coverage/domain')
    capacity = max(colors, default=-1) + 1
    require(type(row['capacity']) is int and row['capacity'] == capacity and
            row['upper_bound'] == 36 + capacity, 'literal capacity declaration')
    sets = [set(w) for w in candidates]
    edges = 0
    for i, a in enumerate(sets):
        for j in range(i + 1, len(sets)):
            if len(a & sets[j]) <= 2:
                require(colors[i] != colors[j], 'literal improper color certificate')
                edges += 1
    return {'seed': row['seed'], 'core_words': 36, 'distinct_core_triples': 360,
            'candidates': len(candidates), 'edges': edges, 'capacity': capacity,
            'upper_bound': 36 + capacity, 'core_masks_sha256': sha(row['core_masks']),
            'candidate_sha256': row['candidate_sha256']}


def controls(row):
    bad = []
    changed = copy.deepcopy(row); changed['core_masks'][1] = changed['core_masks'][0]; bad.append(changed)
    changed = copy.deepcopy(row); changed['core_masks'].pop(); bad.append(changed)
    changed = copy.deepcopy(row); changed['core_masks'][0] |= 1 << 18; bad.append(changed)
    changed = copy.deepcopy(row); changed['saturated_centers'] = [17, 10]; bad.append(changed)
    changed = copy.deepcopy(row); changed['candidate_count'] -= 1; bad.append(changed)
    changed = copy.deepcopy(row); changed['candidate_sha256'] = '0' * 64; bad.append(changed)
    changed = copy.deepcopy(row); changed['colors'].pop(); bad.append(changed)
    changed = copy.deepcopy(row); changed['colors'][0] = -1; bad.append(changed)
    changed = copy.deepcopy(row); changed['colors'][0] = True; bad.append(changed)
    changed = copy.deepcopy(row); changed['capacity'] -= 1; bad.append(changed)
    changed = copy.deepcopy(row); changed['upper_bound'] -= 1; bad.append(changed)
    changed = copy.deepcopy(row); changed['colors'] = [0] * len(row['colors']); changed['capacity'] = 1
    changed['upper_bound'] = 37; bad.append(changed)
    for changed in bad:
        try:
            check(changed)
        except ValueError:
            continue
        raise ValueError('damaged seed completion certificate accepted')
    return len(bad)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('certificate', type=Path)
    parser.add_argument('--controls', action='store_true')
    args = parser.parse_args()
    raw = args.certificate.read_bytes(); data = json.loads(raw)
    require([r['seed'] for r in data['seeds']] == [17, 18], 'literal exact two-seed domain')
    records = [check(row) for row in data['seeds']]
    result = {'status': 'PASS_EXACT_TWO_SEED_COLOR_CERTIFICATES', 'seeds': records,
              'certificate_sha256': hashlib.sha256(raw).hexdigest(), 'records_sha256': sha(records),
              'scope': 'Only the two literal seeds, with degree20 retained at their centers17/11.'}
    if args.controls:
        result['damaged_controls_rejected'] = sum(controls(row) for row in data['seeds'])
    print(json.dumps(result, sort_keys=True))
