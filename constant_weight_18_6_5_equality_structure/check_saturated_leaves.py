"""Literal positive controls for saturated leaves and the deficit budget.

This checks examples and arithmetic, not the universal imported finite
classifications. The ordinary universal proof is SATURATED_LEAVES.md.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import json
import resource
import time
from check_pair_completion import field_plane

HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def check_link(blocks):
    blocks = tuple(frozenset(q) for q in blocks)
    need(len(blocks) == len(set(blocks)) == 20 and all(len(q) == 4 and q <= set(range(17)) for q in blocks),
         'invalid twenty-quadruple fixture')
    used = Counter(frozenset(e) for q in blocks for e in combinations(q, 2))
    need(len(used) == 120 and set(used.values()) == {1}, 'fixture repeats a pair')
    rho = [sum(x in q for q in blocks) for x in range(17)]
    high = {x for x in range(17) if rho[x] < 5}
    leave = {frozenset(e) for e in combinations(range(17), 2)} - set(used)
    need(len(leave) == 16 and max(rho) <= 5 and sum(5 - r for r in rho) == 5,
         'fixture degree identity differs')
    low_low = [e for e in leave if not e & high]
    need(not low_low, 'positive fixture has a low-low leave edge')
    high_core = sorted(sorted(e) for e in leave if e <= high)
    need(len(high_core) == len(high) - 1, 'fixture high-core identity differs')
    return {'positive_deficits': sorted((5 - r for r in rho if r < 5), reverse=True),
            'high_points': sorted(high), 'high_core': high_core, 'low_low_edges': 0}


def completion_examples():
    plane = tuple(sorted(field_plane(), key=lambda q: tuple(sorted(q))))
    distinct = set()
    profiles = Counter()
    for i, j in combinations(range(20), 2):
        for a, b in product(plane[i], plane[j]):
            t1, t2 = plane[i] - {a}, plane[j] - {b}
            if t1 & t2:
                continue
            blocks = tuple(q for k, q in enumerate(plane) if k not in (i, j))
            blocks += (t1 | {16}, t2 | {16})
            report = check_link(blocks)
            need(sum(16 in q for q in blocks) == 2, 'completion fixture hub degree differs')
            profiles[tuple(report['positive_deficits'])] += 1
            key = tuple(sorted(sum(1 << x for x in q) for q in blocks))
            need(key not in distinct, 'two-line fixture repetition')
            distinct.add(key)
    need(len(distinct) == 1600 and profiles == {(3, 2): 160, (3, 1, 1): 1440},
         'two-line fixture domain differs')
    return {'parameter_choices_and_distinct_packings': len(distinct),
            'profiles': {str(k): v for k, v in sorted(profiles.items())},
            'fixture_stream_sha256': sha256(json.dumps(sorted(distinct), separators=(',', ':')).encode()).hexdigest()}


def cycle_example():
    plane = tuple(field_plane())
    changed = [(frozenset(range(4)), 0), (frozenset(range(4, 8)), 5),
               (frozenset((0, 4, 8, 12)), 4), (frozenset((1, 5, 9, 13)), 1)]
    need(all(line in plane for line, _ in changed), 'rectangle lines absent')
    blocks = tuple(q for q in plane if q not in {line for line, _ in changed})
    blocks += tuple((line - {a}) | {16} for line, a in changed)
    report = check_link(blocks)
    need(report['high_points'] == [0, 1, 4, 5, 16] and report['high_core'] == [[0, 1], [0, 4], [1, 5], [4, 5]],
         'four-cycle/isolated-high fixture differs')
    return {**report, 'word_masks': sorted(sum(1 << x for x in q) for q in blocks)}


def budget_example():
    raw = (HERE / 'baseline69.txt').read_bytes()
    need(sha256(raw).hexdigest() == 'cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d',
         'known baseline input bytes differ')
    words = tuple(frozenset(i for i in range(18) if int(row, 2) >> i & 1) for row in raw.splitlines())
    need(len(words) == len(set(words)) == 69 and all(len(q) == 5 for q in words)
         and all(len(q & r) <= 2 for q, r in combinations(words, 2)), 'invalid known69 code')
    r = [sum(x in q for q in words) for x in range(18)]
    saturated = {x for x in range(18) if r[x] == 20}
    unsaturated = set(range(18)) - saturated
    covered = {frozenset(t) for q in words for t in combinations(q, 3)}
    uncovered = {frozenset(t) for t in combinations(range(18), 3)} - covered
    pair = {(x, y): sum({x, y} <= q for q in words) for x, y in combinations(range(18), 2)}
    delta = {e: 5 - value for e, value in pair.items()}
    need(min(delta.values()) >= 0 and max(r) <= 20, 'baseline cap differs')
    support = {frozenset(e) for e, value in delta.items() if value > 0}
    a = [sum(len(t & unsaturated) == j for t in uncovered) for j in range(4)]
    j_sat = sum(sum(x in t and sum(frozenset((x, y)) in support for y in t - {x}) in (0, 2)
                        for x in saturated) for t in uncovered)
    excess = sum(max(delta[tuple(sorted((x, y)))] - 1, 0)
                 for x in saturated for y in range(18) if y != x)
    w_u = sum(value for e, value in delta.items() if set(e) <= unsaturated)
    for x in saturated:
        low = set(range(18)) - {x} - {y for y in range(18) if y != x and frozenset((x, y)) in support}
        need(not any(x in t and t - {x} <= low for t in uncovered), 'known saturated star has low-low edge')
    eta = j_sat - a[0]
    k, d = len(unsaturated), 72 - len(words)
    need(eta >= 0 and excess + a[2] + 2 * a[3] + eta == 12 * k + 20 * d - 24,
         'literal deficit budget identity differs')
    need(a[2] + 3 * a[3] == k * (k - 1) // 2 + 3 * w_u,
         'literal unsaturated-pair identity differs')
    return {'known_words': len(words), 'k': k, 'd': d, 'uncovered_by_unsaturated_count': a,
            'E_S': excess, 'W_U': w_u, 'z_U': a[3], 'J_S': j_sat, 'eta': eta,
            'budget_lhs_with_eta': excess + k * (k - 1) // 2 + 3 * w_u - a[3] + eta,
            'budget_rhs': 12 * k + 20 * d - 24, 'new_construction': False}


def main():
    began = time.monotonic()
    out = {'agent': 'six-code-1', 'role': 'researcher', 'status': 'COMPLETE_POSITIVE_AND_BUDGET_CONTROLS',
           'two_line_examples': completion_examples(), 'cyclic_high_core': cycle_example(),
           'known69_budget': budget_example(),
           'scope': 'Examples and exact counting controls; universal finite-input exclusions are not rerun here.'}
    out.update(seconds=round(time.monotonic() - began, 6), peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
