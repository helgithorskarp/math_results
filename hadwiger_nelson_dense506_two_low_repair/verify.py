#!/usr/bin/env python3
"""Check all equal-palette pairs with a common eligible completion neighbour."""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import json
import common as C


def verify(candidate_work, centre_work):
    table, data, masks = C.load(candidate_work, centre_work)
    points = table['points']
    neighbors = list(map(set, table['eligible_candidate_neighbors']))
    all_pairs = same = 0
    pairs, norms = [], []
    witnesses = sha256()
    triples = []
    for i, j in combinations(range(len(points)), 2):
        all_pairs += 1
        if masks[i] != masks[j]:
            continue
        same += 1
        shared = sorted(neighbors[i] & neighbors[j])
        if not shared:
            continue
        pairs.append((i, j, shared))
        norm = C.squared_distance(points[i], points[j])
        C.S.require(norm != (1, 1, 0, 0, 0), 'unit-distance obstruction pair')
        norms.append((i, j, norm))
        for c in shared:
            cp = min(k for k in range(4) if data['available_masks'][c] >> k & 1)
            cx = min(k for k in range(4) if masks[i] >> k & 1 and k != cp)
            C.S.require(masks[j] >> cx & 1 and cp != cx, 'invalid explicit colouring')
            triples.append((i, j, c))
            witnesses.update(json.dumps([i, j, c, cx, cx, cp], separators=(',', ':')).encode() + b'\n')
    histogram = sorted(Counter(n for _, _, n in norms).items())
    C.S.require(histogram == C.read_certificate(), 'distance-spectrum certificate mismatch')
    result = {'outside_points': len(points), 'all_pairs_considered': all_pairs,
              'equal_palette_pairs': same, 'pairs_with_common_eligible_neighbor': len(pairs),
              'common_neighbor_triples': len(triples), 'squared_distance_classes': len(histogram),
              'pair_sha256': C.G.digest(pairs), 'pair_neighbor_triple_sha256': C.G.digest(triples),
              'norm_stream_sha256': C.G.digest(norms),
              'colouring_stream_sha256': witnesses.hexdigest(), 'unit_pairs': 0}
    return pairs, norms, result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate-work', type=Path, required=True)
    parser.add_argument('--centre-work', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=False)
    pairs, norms, result = verify(args.candidate_work, args.centre_work)
    (args.work / 'pairs.json').write_text(json.dumps(pairs, separators=(',', ':')) + '\n')
    (args.work / 'norms.json').write_text(json.dumps(norms, separators=(',', ':')) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
