"""Exact raw-pair bounds, using compressed required-point bit positions.

No symmetry reduction: all 270 original15/18 pairs are streamed. Binary
records are local verification inputs, not public proof corpora.
"""
from hashlib import sha256
from pathlib import Path
import argparse
import json
import struct

PREFIX = ((8, 0), (9, 0), (10, 1), (14, 1), (12, 10))
BASE = tuple(n for n in range(8, 2521)
             if 2520 % n == 0 and n not in (8, 9, 10, 12, 14))
PARENTS = (1, 2, 3, 5, 6, 7)
FIXED = (15, 18)


def metadata():
    return dict(schema=1, agent='six-covering-3', role='researcher', period=2520,
                prefix=[list(p) for p in PREFIX], parents=list(PARENTS),
                original_base_labels=list(BASE), fixed_originals=list(FIXED),
                pair_phase_domains=[list(range(15)), list(range(18))],
                remaining_originals=[n for n in BASE if n not in FIXED],
                raw_original_phase_actions=sum(BASE), records_per_parent=270,
                row_encoding='38 unsigned little-endian 16-bit integers',
                row_fields='a15,a18,gain,34 ascending-original marginals,K',
                symmetry_reduction=False, native_solver=False)


def run(parent, records):
    if type(parent) is not int or parent not in PARENTS:
        raise ValueError('Wrong excluded-parent domain')
    points = [x for x in range(2520) if x % 8 != parent
              and all(x % n != a for n, a in PREFIX)]
    masks = {n: [0] * n for n in BASE}
    for j, x in enumerate(points):
        for n in BASE:
            masks[n][x % n] |= 1 << j
    remaining = [n for n in BASE if n not in FIXED]
    digest = sha256()
    count = 0
    upper_min, upper_max = 65536, -1
    gain_min, gain_max = 65536, -1
    maxrow = None
    with records.open('wb') as stream:
        for a15 in range(15):
            for a18 in range(18):
                covered = masks[15][a15] | masks[18][a18]
                gain = covered.bit_count()
                caps = [max((m & ~covered).bit_count() for m in masks[n])
                        for n in remaining]
                bound = gain + sum(caps)
                row = [a15, a18, gain, *caps, bound]
                if len(row) != 38 or any(type(v) is not int or not 0 <= v < 65536
                                         for v in row):
                    raise ValueError('Canonical record arity/overflow')
                encoded = struct.pack('<38H', *row)
                stream.write(encoded)
                digest.update(encoded)
                count += 1
                upper_min, upper_max = min(upper_min, bound), max(upper_max, bound)
                gain_min, gain_max = min(gain_min, gain), max(gain_max, gain)
                if maxrow is None or bound > maxrow[-1]:
                    maxrow = row
    return dict(parent=parent, required=len(points), records=count,
                required_points_sha256=sha256(struct.pack(
                    '<' + str(len(points)) + 'H', *points)).hexdigest(),
                unconditioned_upper=sum(max(m.bit_count() for m in masks[n]) for n in BASE),
                union_gain_range=[gain_min, gain_max], total_upper_range=[upper_min, upper_max],
                maximum_row=maxrow, all_rows38H_sha256=digest.hexdigest(),
                stream_bytes=count * 76, remaining_phase_actions=sum(remaining),
                original_marginal_entries=count * len(remaining),
                phase_intersections=count * sum(remaining),
                universal_outside_holes_at_least=len(points) - upper_max)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--parent', type=int, required=True, choices=PARENTS)
    parser.add_argument('--records', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = run(args.parent, args.records)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, sort_keys=True))
