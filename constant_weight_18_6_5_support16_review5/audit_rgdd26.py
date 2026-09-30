#!/usr/bin/env python3
"""Independent replay of the classical nonexistence of a 3-RGDD of type 2^6.

six-reviewer-5; known result, no novelty claim. Complete first-class quotient
by the four-block incidence multigraph. No researcher input or module used.
"""
import argparse
from itertools import combinations, permutations
from collections import Counter
from functools import lru_cache
import hashlib
import json
import time
from pathlib import Path


def need(value, message):
    if not value:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path)
    parser.add_argument('--write', type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    nodes = 0
    rows = [(x, y) for x, y in combinations(range(12), 2) if x//2 != y//2]
    index = {p: i for i, p in enumerate(rows)}
    triples = [q for q in combinations(range(12), 3) if len({x//2 for x in q}) == 3]
    by_point = {x: [q for q in triples if x in q] for x in range(12)}
    classes = []

    def partitions(unused, selected):
        if not unused:
            classes.append(tuple(selected))
            return
        for q in by_point[min(unused)]:
            if set(q) <= unused:
                partitions(unused-set(q), selected+[q])
    partitions(set(range(12)), [])
    need(len(triples) == 160 and all(len(p) == 4 for p in classes), 'wrong finite universe')

    def incidence_edges(p):
        block = {x: i for i, q in enumerate(p) for x in q}
        return tuple(sorted(tuple(sorted((block[2*g], block[2*g+1]))) for g in range(6)))

    permutations4 = list(permutations(range(4)))

    @lru_cache(None)
    def canonical(edges):
        return min(tuple(sorted(tuple(sorted((pi[x], pi[y]))) for x, y in edges))
                   for pi in permutations4)

    orbit_classes = {}
    for p in classes:
        edges = incidence_edges(p)
        need(all(x != y for x, y in edges), 'group has both points in a block')
        degree = Counter(x for pair in edges for x in pair)
        need(all(degree[x] == 3 for x in range(4)), 'incidence multigraph not cubic')
        orbit_classes.setdefault(canonical(edges), []).append(p)
    masks = [sum(1 << index[pair] for q in p for pair in combinations(q, 2)) for p in classes]
    need(all(mask.bit_count() == 12 for mask in masks), 'parallel class repeats a pair')
    full = (1 << len(rows))-1
    reports = []
    for key, representatives in sorted(orbit_classes.items()):
        first = representatives[0]
        firstmask = sum(1 << index[pair] for q in first for pair in combinations(q, 2))
        allowed = [mask for mask in masks if not (mask & firstmask)]
        options = [[mask for mask in allowed if mask >> j & 1] for j in range(len(rows))]
        failed = set()
        case_nodes = 0

        def search(remaining):
            nonlocal nodes, case_nodes
            nodes += 1
            case_nodes += 1
            if nodes > 1000000 or (nodes % 128 == 0 and time.monotonic()-started > 45):
                raise TimeoutError('INCOMPLETE classical design replay')
            if not remaining:
                return []
            if remaining in failed:
                return None
            scan = remaining
            best = None
            while scan:
                low = scan & -scan
                here = [mask for mask in options[low.bit_length()-1] if mask & remaining == mask]
                if not here:
                    failed.add(remaining)
                    return None
                if best is None or len(here) < len(best):
                    best = here
                scan ^= low
            for mask in best:
                witness = search(remaining ^ mask)
                if witness is not None:
                    return [mask]+witness
            failed.add(remaining)
            return None

        # Positive controls for this actual class universe, including two
        # disjoint classes. Check every returned mask, not just status.
        positive = []
        second = allowed[0]
        third = next(mask for mask in allowed if not (mask & second))
        for target in (second, second | third):
            witness = search(target)
            need(witness is not None, 'partial positive resolution rejected')
            used = 0
            for mask in witness:
                need(mask in allowed and not (used & mask), 'invalid positive class')
                used |= mask
            need(used == target, 'positive witness omits prescribed pairs')
            positive.append(len(witness))
        case_nodes = 0
        failed.clear()
        need(search(full ^ firstmask) is None, 'classical negative has a witness')
        reports.append({'cubic_incidence_edges': key, 'labeled_first_classes': len(representatives),
                        'representative': first, 'remaining_parallel_classes': len(allowed),
                        'search_nodes': case_nodes, 'failed_states': len(failed),
                        'status': 'COMPLETE_NO_RESOLUTION', 'positive_partial_classes': positive})
    report = {'reviewer': 'six-reviewer-5', 'role': 'independent mathematical reviewer',
              'scope': 'classical no resolvable 3-GDD of type 2^6, not a new theorem',
              'cross_group_pairs': len(rows), 'legal_triples': len(triples),
              'parallel_classes': len(classes), 'first_class_orbits': len(reports),
              'parallel_classes_sha256': hashlib.sha256(
                  (json.dumps(classes, separators=(',', ':'))+'\n').encode()).hexdigest(),
              'cases': reports, 'complete_negative': True}
    if args.expected:
        need(json.loads(args.expected.read_text()) == json.loads(json.dumps(report)),
             'compact design evidence differs')
    if args.write:
        args.write.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
