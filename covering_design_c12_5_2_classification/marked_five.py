"""Different decomposition: five blocks through a marked degree-five point.

The four-away-block point-signature search is adapted from the independent
local audit in covering_design_c13_6_3_exceptional_profile_exclusion.  The
through-family census here removes that earlier application's triple cap.
"""
from collections import defaultdict
from itertools import permutations
import json
from pathlib import Path
import sys
from audit import graph, isomorphic
ROOT = Path(__file__).resolve().parent
TABLES = {}
for k in range(1, 6):
    TABLES[k] = [tuple((sum((1 << p[j] for j in range(k) if m >> j & 1)) for m in range(1 << k))) for p in permutations(range(k))]

def canonical(counts, k):
    return min((tuple((counts[m] for m in mapping)) for mapping in TABLES[k]))

def census():
    states = {(11,)}
    levels = []
    for k in range(5):
        new = set()
        raw = set()
        for counts in sorted(states):
            occupied = [m for m, n in enumerate(counts) if n]
            selection = [0] * len(counts)

            def extend(i, left):
                if i == len(occupied):
                    if left:
                        return
                    if any((sum((selection[m] for m in occupied if m >> j & 1)) > 3 for j in range(k))):
                        return
                    out = tuple((counts[m] - selection[m] for m in range(1 << k))) + tuple(selection)
                    if out[0] > 4 * (4 - k):
                        return
                    if out not in raw:
                        raw.add(out)
                        new.add(canonical(out, k + 1))
                    return
                m = occupied[i]
                for n in range(min(counts[m], left) + 1):
                    selection[m] = n
                    extend(i + 1, left - n)
                selection[m] = 0
            extend(0, 4)
        states = new
        levels.append(len(states))
    return (sorted(states), levels)

def enumerate_dual(columns):
    adjacency = [{q for q in range(11) if q != p and columns[p] & columns[q] == 0} for p in range(11)]
    order = sorted(range(11), key=lambda p: (-len(adjacency[p]), -columns[p].bit_count(), p))
    initial = []
    for p in order:
        lo = max((len(adjacency[p]) + 3) // 4, 3 - columns[p].bit_count(), 0)
        hi = min(4, 5 - columns[p].bit_count())
        initial.append(tuple((m for m in range(16) if lo <= m.bit_count() <= hi)))
    weights = [0] * 4
    histories = [0] * 4
    assigned = {}
    answers = set()
    nodes = 0

    def visit(depth, domains):
        nonlocal nodes
        nodes += 1
        if depth == 11:
            if weights != [5] * 4:
                return
            rows = tuple(sorted((sum((1 << p for p, m in assigned.items() if m >> r & 1)) for r in range(4))))
            if len(set(rows)) != 4:
                return
            answers.add(rows)
            return
        if any((not d for d in domains)):
            return
        needed = [5 - w for w in weights]
        if any((n < 0 for n in needed)):
            return
        if sum((min((m.bit_count() for m in d)) for d in domains)) > sum(needed):
            return
        if sum((max((m.bit_count() for m in d)) for d in domains)) < sum(needed):
            return
        for r, n in enumerate(needed):
            if sum((any((m >> r & 1 for m in d)) for d in domains)) < n:
                return
            if sum((all((m >> r & 1 for m in d)) for d in domains)) > n:
                return
        groups = defaultdict(list)
        for r, h in enumerate(histories):
            groups[h].append(r)
        canonical = []
        for m in domains[0]:
            if any(([m >> r & 1 for r in g] != sorted([m >> r & 1 for r in g], reverse=True) for g in groups.values())):
                continue
            canonical.append(m)
        p = order[depth]
        old_hist = histories.copy()
        for m in canonical:
            for r in range(4):
                weights[r] += m >> r & 1
                histories[r] = histories[r] << 1 | m >> r & 1
            assigned[p] = m
            saturated = sum((1 << r for r, w in enumerate(weights) if w == 5))
            future = []
            for q, domain in zip(order[depth + 1:], domains[1:]):
                future.append(tuple((v for v in domain if not v & saturated and (q not in adjacency[p] or v & m))))
            visit(depth + 1, tuple(future))
            del assigned[p]
            for r in range(4):
                weights[r] -= m >> r & 1
            histories[:] = old_hist
    visit(0, tuple(initial))
    return (sorted(answers), nodes)

def main():
    catalogue = json.loads((ROOT / 'CATALOGUE.json').read_text())
    pointed = []
    for design in catalogue['designs']:
        rows = design['point_signatures']
        for orbit in design['point_orbits']:
            p = orbit[0]
            if rows[p].bit_count() == 5:
                pointed.append((design['id'], p, graph(rows, p)))
    states, levels = census()
    nodes = total = feasible = 0
    found = set()
    cases = []
    for index, counts in enumerate(states):
        columns = [m for m, n in enumerate(counts) for _ in range(n)]
        covers, count = enumerate_dual(columns)
        nodes += count
        if not covers:
            continue
        feasible += 1
        total += len(covers)
        through = [1 << 11 | sum((1 << p for p, m in enumerate(columns) if m >> j & 1)) for j in range(5)]
        matches = set()
        for away in covers:
            blocks = through + list(away)
            rows = [sum((1 << j for j, b in enumerate(blocks) if b >> p & 1)) for p in range(12)]
            g = graph(rows, 11)
            matching = [(d, p) for d, p, target in pointed if isomorphic(g, target)]
            if len(matching) != 1:
                raise ValueError('marked-degree-five completion disagrees with the catalogue')
            found.add(matching[0])
            matches.add(matching[0])
        cases.append(dict(through_type=index, completions=len(covers), pointed_classes=sorted(matches)))
    if found != {(d, p) for d, p, _ in pointed}:
        raise ValueError('marked-degree-five census is not onto the pointed catalogue')
    result = dict(status='INDEPENDENT_MARKED_DEGREE5_CENSUS_PASSED', through_levels=levels, through_types=len(states), feasible_types=feasible, labelled_completions=total, pointed_classes=len(found), search_nodes=nodes, cases=cases)
    result = json.loads(json.dumps(result))
    if sys.argv[1:] == ['--write-reference']:
        (ROOT / 'MARKED_EXPECTED.json').write_text(json.dumps(result, indent=2) + '\n')
    elif sys.argv[1:]:
        raise SystemExit('usage: python3 marked_five.py [--write-reference]')
    elif result != json.loads((ROOT / 'MARKED_EXPECTED.json').read_text()):
        raise ValueError('marked-degree-five audit differs from MARKED_EXPECTED.json')
    print(json.dumps(result, indent=2))
if __name__ == '__main__':
    main()
