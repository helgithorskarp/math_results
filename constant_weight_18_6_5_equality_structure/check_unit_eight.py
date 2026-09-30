#!/usr/bin/env python3
"""Exclude the eight-edge high core in an all-unit twenty-block star."""
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import json
import time

HERE = Path(__file__).resolve().parent
HIGH = tuple(range(5))
LOW = tuple(range(5, 17))
ATTACHED = tuple(range(5, 9))
MATCHED = tuple(range(9, 17))
ALL_PAIRS = tuple(combinations(range(17), 2))
LEAVE = frozenset((set(combinations(HIGH, 2)) - {(0, 1), (2, 3)}) |
                  {(i, i + 5) for i in range(4)} |
                  {(9, 10), (11, 12), (13, 14), (15, 16)})


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, separators=(",", ":"), sort_keys=True) + "\n").encode("ascii")


def pairs(points):
    return frozenset(combinations(points, 2))


def image(points, permutation):
    return tuple(sorted(permutation[x] for x in points))


def leave_group():
    """All actual leave permutations: eight high maps times 384 low maps."""
    result = []
    high_matching = {frozenset((0, 1)), frozenset((2, 3))}
    for h in permutations(range(4)):
        if {frozenset((h[0], h[1])), frozenset((h[2], h[3]))} != high_matching:
            continue
        for order in permutations(range(4)):
            for flips in product(range(2), repeat=4):
                p = list(range(17))
                for i in range(4):
                    p[i], p[i + 5] = h[i], h[i] + 5
                for i in range(4):
                    for j in range(2):
                        p[9 + 2*i + j] = 9 + 2*order[i] + (j ^ flips[i])
                p = tuple(p)
                require(len(set(p)) == 17, "nonpermutation")
                require({image(e, p) for e in LEAVE} == set(LEAVE),
                        "permutation does not preserve the actual leave")
                result.append(p)
    require(len(result) == len(set(result)) == 3072, "wrong group order")
    # Generators check closure without quadratic group-pair comparisons.
    generators = []
    for swaps in [((0, 1), (5, 6)), ((2, 3), (7, 8)),
                  ((0, 2), (1, 3), (5, 7), (6, 8)),
                  ((9, 10),), ((9, 11), (10, 12)),
                  ((11, 13), (12, 14)), ((13, 15), (14, 16))]:
        p = list(range(17))
        for a, b in swaps:
            p[a], p[b] = p[b], p[a]
        generators.append(tuple(p))
    listed = set(result)
    generated = {tuple(range(17))}
    pending = list(generated)
    while pending:
        p = pending.pop()
        for s in generators:
            q = tuple(s[p[i]] for i in range(17))
            require(q in listed, "generator closure escaped listed group")
            if q not in generated:
                generated.add(q)
                pending.append(q)
    require(generated == listed, "listed maps not a generated group")
    return tuple(result)


def frame_image(frame, permutation):
    a, b, zeros = frame
    if {permutation[0], permutation[1]} == {0, 1}:
        tails = image(a, permutation), image(b, permutation)
    else:
        tails = image(b, permutation), image(a, permutation)
    return tails + (tuple(sorted(image(z, permutation) for z in zeros)),)


def fixed_quads(frame):
    a, b, zeros = frame
    return ((0, 1) + a, (2, 3) + b) + zeros


def legal_fixed(quads):
    covered = set()
    for q in quads:
        e = pairs(q)
        if e & LEAVE or e & covered:
            return False
        covered.update(e)
    return True


def generate_frames():
    """Ordinary incidence lemma forces four distinct matched tail points."""
    result = set()
    tail_counts = Counter()
    frame_counts = Counter()
    for a in combinations(MATCHED, 2):
        if a in LEAVE:
            continue
        for b in combinations(MATCHED, 2):
            if b in LEAVE or set(a) & set(b):
                continue
            missing = sum(e in LEAVE for e in combinations(sorted(a+b), 2))
            tail_counts[missing] += 1
            for s in combinations(ATTACHED, 2):
                other_s = tuple(x for x in ATTACHED if x not in s)
                for x in a:
                    for y in b:
                        z1 = tuple(sorted(s + (x, y)))
                        z2 = tuple(sorted(other_s + tuple(v for v in a+b if v not in (x, y))))
                        if z1 >= z2:
                            continue
                        frame = (a, b, (z1, z2))
                        if legal_fixed(fixed_quads(frame)):
                            result.add(frame)
                            frame_counts[missing] += 1
    require(len(result) == 2448, "wrong raw frame count")
    require(dict(sorted(tail_counts.items())) == {0: 96, 1: 192, 2: 24},
            "wrong tail incidence counts")
    require(dict(sorted(frame_counts.items())) == {0: 1152, 1: 1152, 2: 144},
            "wrong raw frame fibers")
    return frozenset(result), tail_counts, frame_counts


def normalized_frames():
    group = leave_group()
    raw, tail_counts, frame_counts = generate_frames()
    unseen = set(raw)
    result = []
    while unseen:
        root = min(unseen)
        orbit = {frame_image(root, p) for p in group}
        require(orbit <= raw and orbit <= unseen, "invalid or overlapping frame orbit")
        stabilizer = [p for p in group if frame_image(root, p) == root]
        require(len(orbit) * len(stabilizer) == len(group), "orbit-stabilizer failure")
        unseen.difference_update(orbit)
        result.append((root, len(orbit), len(stabilizer)))
    require(len(result) == 7 and sum(x[1] for x in result) == len(raw),
            "incomplete seven-frame quotient")
    return result, {'group_order': len(group), 'raw_frames': len(raw),
                    'group_sha256': sha256(encoded(sorted(group))).hexdigest(),
                    'raw_frames_sha256': sha256(encoded(sorted(raw))).hexdigest(),
                    'tail_counts': dict(sorted(tail_counts.items())),
                    'frame_counts': dict(sorted(frame_counts.items()))}


def exact_instance(prefix):
    require(legal_fixed(prefix), "invalid fixed prefix")
    used = set().union(*(pairs(q) for q in prefix))
    rows = tuple(e for e in ALL_PAIRS if e not in LEAVE and e not in used)
    row_set = set(rows)
    # The ordinary block-count proof forces every remaining block to have
    # exactly one high point. The separate checker scans all 2380 quadruples.
    columns = tuple((h,) + t for h in HIGH for t in combinations(LOW, 3)
                    if pairs((h,) + t) <= row_set)
    require(len(rows) == 96, "wrong residual pair count")
    return rows, columns


class CoverFound(Exception):
    """A positive cover disproves this claimed obstruction."""


class Incomplete(Exception):
    """No mathematical verdict: the unchanged search guard was reached."""


def rejection_tree(rows, columns, node_limit=200000, seconds=10):
    index = {e: i for i, e in enumerate(rows)}
    masks = tuple(sum(1 << index[e] for e in pairs(q)) for q in columns)
    options = [0] * len(rows)
    for j, m in enumerate(masks):
        require(m.bit_count() == 6, "column does not cover six pairs")
        for i in range(len(rows)):
            if m >> i & 1:
                options[i] |= 1 << j
    conflicts = []
    for m in masks:
        c = 0
        for i in range(len(rows)):
            if m >> i & 1:
                c |= options[i]
        conflicts.append(c)
    count = 0
    start = time.monotonic()

    def visit(left, active):
        nonlocal count
        count += 1
        if count > node_limit or (count % 128 == 0 and time.monotonic()-start > seconds):
            raise Incomplete("INCOMPLETE: rejection-tree guard reached")
        if not left:
            raise CoverFound("positive exact cover found")
        _, pivot, available = min(((options[r] & active).bit_count(), r, options[r] & active)
                                  for r in range(len(rows)) if left >> r & 1)
        children = []
        while available:
            bit = available & -available
            j = bit.bit_length() - 1
            available ^= bit
            require(masks[j] & left == masks[j], "active column covers a used pair")
            children.append([j, visit(left ^ masks[j], active & ~conflicts[j])])
        return [pivot, children]

    return visit((1 << len(rows))-1, (1 << len(columns))-1), count


def generate():
    frames, summary = normalized_frames()
    cases = []
    for i, (frame, orbit_size, stabilizer_order) in enumerate(frames):
        prefix = fixed_quads(frame)
        rows, columns = exact_instance(prefix)
        cases.append({'index': i, 'tail01': frame[0], 'tail23': frame[1],
                      'zero_quads': frame[2], 'orbit_size': orbit_size,
                      'stabilizer_order': stabilizer_order, 'fixed_quads': prefix,
                      'rows': rows, 'columns': columns,
                      'input_sha256': sha256(encoded([prefix, rows, columns])).hexdigest()})
    return cases, summary


def build():
    cases, summary = generate()
    records = []
    node_counts = []
    for case in cases:
        tree, count = rejection_tree(case['rows'], case['columns'])
        node_counts.append(count)
        records.append({k: case[k] for k in ('index', 'tail01', 'tail23', 'zero_quads',
                       'orbit_size', 'stabilizer_order', 'fixed_quads', 'input_sha256')}
                       | {'tree': tree})
    certificate = {'schema': 'all-unit-eight-core-v1', 'carrier_summary': summary,
                   'cases': records}
    report = {'agent': 'six-code-1', 'role': 'researcher',
              'status': 'COMPLETE_EXACT_NO_COVERS', 'frames': 7, 'raw_frames': 2448,
              'leave_group_order': 3072, 'nodes': sum(node_counts),
              'maximum_nodes_per_case': max(node_counts),
              'nodes_per_case': node_counts,
              'columns_per_case': [len(c['columns']) for c in cases],
              'rows_per_case': [len(c['rows']) for c in cases],
              'input_stream_sha256': sha256(encoded([[c['fixed_quads'], c['rows'], c['columns']]
                                                   for c in cases])).hexdigest(),
              'certificate_sha256': sha256(encoded(certificate)).hexdigest(),
              'certificate_bytes': len(encoded(certificate)),
              'global_72_word_exclusion': False, 'independent_peer_review': False,
              'ordinary_bridges_formalized': False}
    return certificate, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-certificate', action='store_true')
    args = parser.parse_args()
    certificate, report = build()
    if args.write_certificate:
        (HERE / 'unit_eight_certificate.json').write_bytes(encoded(certificate))
        (HERE / 'unit_eight_expected.json').write_bytes(encoded(report))
    else:
        require((HERE / 'unit_eight_certificate.json').read_bytes() == encoded(certificate),
                "certificate differs entry by entry")
        require(json.loads((HERE / 'unit_eight_expected.json').read_text()) == report,
                "expected report differs")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
