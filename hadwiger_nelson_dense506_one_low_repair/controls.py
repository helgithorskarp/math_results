#!/usr/bin/env python3
"""Exhaustive list criterion, exact small-screen comparison, and rejection controls."""
from itertools import combinations, product
from pathlib import Path
from collections import Counter
import argparse
import json
from engine import Census, G, S, obstructed, colour_triple


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate-work', type=Path, required=True)
    args = parser.parse_args()
    cases = badcount = 0
    for mask in range(1, 16):
        if mask.bit_count() != 2:
            continue
        for a, b in product(range(1, 16), repeat=2):
            for e0, e1, e2 in product([False, True], repeat=3):
                if e2 and a == b and a.bit_count() == 1:
                    continue
                edges = [e for yes, e in zip((e0, e1, e2), ((0, 1), (0, 2), (1, 2))) if yes]
                brute = not any(all((m >> c) & 1 for m, c in zip((mask, a, b), col))
                                and all(col[i] != col[j] for i, j in edges)
                                for col in product(range(4), repeat=3))
                predicted = obstructed(mask, a, b, e0, e1, e2)
                assert brute == predicted
                cases += 1
                badcount += brute
    census = Census(args.candidate_work)
    limit = 12
    all_rows = []
    for i, j in combinations(range(limit), 2):
        if census.colors[i] == census.colors[j]:
            continue
        mask = 15 ^ ((1 << census.colors[i]) | (1 << census.colors[j]))
        common = census.adj[i] & census.adj[j]
        for c, allowed in enumerate(census.data['available_masks']):
            if allowed & ~mask == 0 and not common & census.adj[506 + c]:
                all_rows.append((i, j, c))
    exact_centres, exact_positive = census.exact(all_rows)
    screened, info = census.screen(limit)
    screened_centres, screened_positive = census.exact(screened)
    assert exact_centres == screened_centres and exact_positive == screened_positive
    # Direct palette fixtures exercise both obstruction types and a flexible successful pair.
    assert colour_triple(3, 1, 2, False) is None
    assert colour_triple(3, 3, 3, True) is None
    assert colour_triple(3, 3, 3, False) is not None
    wrong_roots_rejected = 0
    for p, z, r in ((10007, 284, 6718), (10007, 283, 6719)):
        if z * z % p != 33 or r * r % p != (-408 + 72 * z) % p:
            wrong_roots_rejected += 1
    assert wrong_roots_rejected == 2
    print(json.dumps({'list_criterion_cases': cases, 'obstruction_cases': badcount,
                      'all_predictions_match_brute_force': True,
                      'small_host_limit': limit, 'unscreened_eligible_external_triples': len(all_rows),
                      'small_modular_survivors': len(screened),
                      'small_exact_positive_triples': len(exact_positive),
                      'small_exact_centres': len(exact_centres),
                      'small_exact_positive_sha256': G.digest(exact_positive),
                      'screen_vs_unscreened_entry_level_match': True,
                      'direct_palette_fixtures': 3, 'wrong_modular_roots_rejected': wrong_roots_rejected}, indent=2))


if __name__ == '__main__':
    main()
