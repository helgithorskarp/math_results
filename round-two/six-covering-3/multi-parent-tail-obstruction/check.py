"""Independent physical2520-point AP audit, with every record compared.

No producer import. Original labels are independently generated from prime
powers; phases come from all270 integer pair indices. AP masks and reverse
phase marginal loops differ from the compressed-residue producer.
"""
from hashlib import sha256
from pathlib import Path
import argparse
import json
import struct


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(c):
    p = [[8, 0], [9, 0], [10, 1], [14, 1], [12, 10]]
    labels = sorted(2**i * 3**j * 5**k * 7**ell
                    for i in range(4) for j in range(3)
                    for k in range(2) for ell in range(2)
                    if 2**i * 3**j * 5**k * 7**ell >= 8
                    and 2**i * 3**j * 5**k * 7**ell not in (8, 9, 10, 12, 14))
    remaining = [n for n in labels if n not in (15, 18)]
    require(type(c['schema']) is int and c['schema'] == 1 and c['period'] == 2520
            and c['prefix'] == p and c['parents'] == [1, 2, 3, 5, 6, 7],
            'Wrong literal prefix/period/parent family')
    require(all(type(v) is int for row in c['prefix'] for v in row)
            and all(type(v) is int for v in c['parents']), 'Boolean/noninteger phase or parent')
    require(c['original_base_labels'] == labels and len(labels) == 36
            and sum(labels) == 9279 and 21 in labels and 16 not in labels,
            'Missing, duplicate or aliased original resource')
    require(c['fixed_originals'] == [15, 18] and c['remaining_originals'] == remaining
            and c['pair_phase_domains'] == [list(range(15)), list(range(18))]
            and c['raw_original_phase_actions'] == 9279
            and c['records_per_parent'] == 270 and c['symmetry_reduction'] is False
            and c['native_solver'] is False,
            'Incomplete pair/original phase domain')
    require(all(type(v) is int for row in c['pair_phase_domains'] for v in row),
            'Boolean/noninteger raw phase')
    require(c['row_encoding'] == '38 unsigned little-endian 16-bit integers'
            and c['row_fields'] == 'a15,a18,gain,34 ascending-original marginals,K',
            'Wrong canonical record convention')
    require(len(c['cases']) == 6, 'Missing parent case')
    sizes = [1206, 1223, 1206, 1206, 1223, 1206]
    for r, size, case in zip([1, 2, 3, 5, 6, 7], sizes, c['cases']):
        require(type(case['parent']) is int and case['parent'] == r
                and case['required'] == size and case['records'] == 270
                and case['stream_bytes'] == 270 * 76,
                'Skipped/mislabelled parent or raw pair')
        require(case['remaining_phase_actions'] == sum(remaining)
                and case['original_marginal_entries'] == 270 * 34
                and case['phase_intersections'] == 270 * sum(remaining),
                'Skipped marginal or original phase')
        row = case['maximum_row']
        require(len(row) == 38 and all(type(v) is int and 0 <= v < 65536 for v in row)
                and 0 <= row[0] < 15 and 0 <= row[1] < 18
                and row[-1] == case['total_upper_range'][1], 'Malformed maximum witness')
        require(case['universal_outside_holes_at_least'] == size - row[-1]
                and size - row[-1] > 0, 'No strict universal deficit')
    return p, labels, remaining


def catalogue(parent, p, labels):
    unavailable = {x for n, a in p for x in range(a, 2520, n)}
    required = sorted(set(range(2520)) - unavailable - set(range(parent, 2520, 8)))
    R = sum(1 << x for x in required)
    actions = {}
    for n in reversed(labels):
        actions[n] = []
        for a in range(n):
            actions[n].append(sum(1 << x for x in range(a, 2520, n)
                                  if (R >> x) & 1))
        require(all(m & ~R == 0 for m in actions[n]), 'Literal AP outside required set')
    require(sum(len(v) for v in actions.values()) == 9279, 'Incomplete AP catalogue')
    return required, R, actions


def run(parent, c, records):
    p, labels, remaining = validate(c)
    require(type(parent) is int and parent in [1, 2, 3, 5, 6, 7], 'Wrong requested parent')
    expected = next(case for case in c['cases'] if case['parent'] == parent)
    required, R, actions = catalogue(parent, p, labels)
    require(records.stat().st_size == 270 * 76, 'Missing, extra or truncated raw record')
    digest = sha256()
    min_upper, max_upper = 65536, -1
    min_gain, max_gain = 65536, -1
    maxrow = None
    with records.open('rb') as stream:
        for pair_index in range(270):
            a15, a18 = divmod(pair_index, 18)
            covered = actions[18][a18] | actions[15][a15]
            residual = R ^ covered
            gain = len(required) - residual.bit_count()
            caps = []
            for n in remaining:
                best = 0
                for a in range(n - 1, -1, -1):
                    hit = (actions[n][a] & residual).bit_count()
                    if hit > best:
                        best = hit
                caps.append(best)
            bound = gain + sum(caps)
            row = [a15, a18, gain, *caps, bound]
            require(len(row) == 38 and all(0 <= v < 65536 for v in row), 'Record overflow')
            encoded = stream.read(76)
            require(list(struct.unpack('<38H', encoded)) == row,
                    'Producer/AP entry-level difference at pair ' + str(pair_index))
            digest.update(encoded)
            min_upper, max_upper = min(min_upper, bound), max(max_upper, bound)
            min_gain, max_gain = min(min_gain, gain), max(max_gain, gain)
            if maxrow is None or bound > maxrow[-1]:
                maxrow = row
        require(stream.read(1) == b'', 'Extra raw record')
    actual = dict(parent=parent, required=len(required), records=270,
                  required_points_sha256=sha256(struct.pack(
                      '<' + str(len(required)) + 'H', *required)).hexdigest(),
                  unconditioned_upper=sum(max(m.bit_count() for m in actions[n]) for n in labels),
                  union_gain_range=[min_gain, max_gain], total_upper_range=[min_upper, max_upper],
                  maximum_row=maxrow, all_rows38H_sha256=digest.hexdigest(),
                  stream_bytes=270 * 76, remaining_phase_actions=sum(remaining),
                  original_marginal_entries=270 * 34, phase_intersections=270 * sum(remaining),
                  universal_outside_holes_at_least=len(required) - max_upper)
    require(actual == expected, 'Complete independent case certificate differs')
    return actual | dict(independent_literal_AP_audit=True, all270_records_entrywise_equal=True,
                         all_raw_original_phase_actions=9279, external_review_claimed=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--parent', type=int, choices=(1, 2, 3, 5, 6, 7), required=True)
    parser.add_argument('--records', type=Path, required=True)
    parser.add_argument('--certificate', type=Path, default=Path(__file__).with_name('certificate.json'))
    args = parser.parse_args()
    print(json.dumps(run(args.parent, json.loads(args.certificate.read_text()), args.records),
                     sort_keys=True))
