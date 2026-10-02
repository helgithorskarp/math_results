"""Exact marginal screens on compressed required-point masks.

Each call is one planned bounded stage, retaining at most300 phase tuples.
The certificate supplies only the previous retained frontier. Reproduce ALL
four stages in order, plus the separate literal arithmetic-progression audit.
No native solver, large corpus, aliasing, or random choices are used.
"""
from hashlib import sha256
from itertools import product
from pathlib import Path
import argparse
import json
import struct

PREFIX = ((8, 0), (9, 0), (10, 1), (14, 1), (12, 10))
BASE = tuple(n for n in range(8, 2521)
             if 2520 % n == 0 and n not in (8, 9, 10, 12, 14))
ORDER = (15, 18, 24, 36, 20)
REPS15 = (0, 1, 2, 4, 6, 11)
REPS18 = (0, 1, 2, 3, 4, 5, 6, 9, 12, 15)
LIMIT = 300


def metadata():
    return dict(schema=1, agent='six-covering-3', role='researcher', period=2520,
                prefix=[list(p) for p in PREFIX], parent=4, required=1118,
                original_base_labels=list(BASE), fixed_order=list(ORDER),
                canonical15=list(REPS15), canonical18=list(REPS18),
                normalization_group=288, retained_frontier_limit=LIMIT)


def parents(stage, certificate):
    if type(stage) is not int or stage not in (1, 2, 3, 4):
        raise ValueError('Stage must be1,2,3,4')
    if any(certificate.get(k) != v for k, v in metadata().items()):
        raise ValueError('Wrong literal prefix/original inventory/domain')
    if stage == 1:
        return list(product(REPS15, REPS18))
    earlier = certificate['stages'][stage - 2]
    p = earlier['retained_phase_vectors']
    fixed = ORDER[:stage]
    if not p or len(p) > LIMIT or len(p) != earlier['retained_vectors']:
        raise ValueError('Invalid preceding retained frontier')
    tuples = [tuple(row) for row in p]
    if tuples != sorted(set(tuples)) or any(len(row) != len(fixed)
            or any(type(a) is not int or not 0 <= a < n
                   for n, a in zip(fixed, row)) for row in tuples):
        raise ValueError('Wrong/duplicate preceding original phase tuple')
    return tuples


def run(stage, certificate):
    parent = parents(stage, certificate)
    fixed = ORDER[:stage + 1]
    remaining = [n for n in BASE if n not in fixed]
    points = [x for x in range(2520)
              if x % 8 != 4 and all(x % n != a for n, a in PREFIX)]
    if len(points) != 1118:
        raise ValueError('Literal required set has wrong size')
    masks = {n: [0] * n for n in BASE}
    for j, x in enumerate(points):
        for n in BASE:
            masks[n][x % n] |= 1 << j
    digest = sha256()
    parent_digest = sha256(json.dumps(parent, separators=(',', ':')).encode()).hexdigest()
    count = 0
    retained = []
    minimum, maximum = 65536, -1
    gain_min, gain_max = 65536, -1
    excluded_min, excluded_max = 65536, -1
    retained_min, retained_max = 65536, -1
    maxrow = None
    for p in parent:
        # Stage1's parents are already the complete two-resource root.
        before = 0
        for n, a in zip(fixed, p):
            before |= masks[n][a]
        extensions = (None,) if stage == 1 else range(fixed[-1])
        for a in extensions:
            phases = p if a is None else (*p, a)
            covered = before if a is None else before | masks[fixed[-1]][a]
            gain = covered.bit_count()
            marginal = [max((m & ~covered).bit_count() for m in masks[n])
                        for n in remaining]
            bound = gain + sum(marginal)
            row = [*phases, gain, *marginal, bound]
            if len(row) != 38 or any(not 0 <= v < 65536 for v in row):
                raise ValueError('Canonical38H record overflow/arity')
            digest.update(struct.pack('<38H', *row))
            count += 1
            minimum = min(minimum, bound)
            gain_min, gain_max = min(gain_min, gain), max(gain_max, gain)
            if bound > maximum:
                maximum, maxrow = bound, row
            if bound >= 1118:
                if len(retained) == LIMIT:
                    raise RuntimeError('Retained frontier cap: incomplete, no exclusion')
                retained.append(list(phases))
                retained_min, retained_max = min(retained_min, bound), max(retained_max, bound)
            else:
                excluded_min, excluded_max = min(excluded_min, bound), max(excluded_max, bound)
    return dict(stage=stage, fixed_originals=list(fixed), remaining_originals=remaining,
                parent_vectors=len(parent), parent_vectors_sha256=parent_digest,
                records=count, required_points_sha256=sha256(struct.pack(
                    '<1118H', *points)).hexdigest(), union_gain_range=[gain_min, gain_max],
                total_upper_range=[minimum, maximum],
                excluded_upper_range=None if excluded_max < 0 else [excluded_min, excluded_max],
                retained_upper_range=None if retained_max < 0 else [retained_min, retained_max],
                all_rows38H_sha256=digest.hexdigest(), maximum_row=maxrow,
                retained_vectors=len(retained), retained_phase_vectors=retained)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', type=int, required=True, choices=(1, 2, 3, 4))
    parser.add_argument('--certificate', type=Path, default=Path(__file__).with_name('certificate.json'))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = run(args.stage, json.loads(args.certificate.read_text()))
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items()
                      if k != 'retained_phase_vectors'}, sort_keys=True))
