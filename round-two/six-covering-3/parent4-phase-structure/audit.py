"""Independent complete replay from literal physical arithmetic progressions.

Does not import the producer. Reverse nested enumeration fills canonical arrays
by explicit mixed-radix indices. Every joint gain is compared via a full-array
hash; witnesses are also checked point by point with integer remainders.
"""
import hashlib
import itertools
import json
from pathlib import Path
import struct
import sys


def require(ok, message):
    if not ok:
        raise ValueError(message)


def independent_case(rows):
    initial = [x for x in range(2520)
               if x % 8 != 0 and x % 9 != 0 and x % 10 != 1
               and x % 14 != 1 and x % 12 != 10]
    points = [x for x in initial if x % 8 != 4 or x % 5 not in rows]
    R = sum(1 << x for x in points)
    inventory = [n for n in range(8, 2521)
                 if 2520 % n == 0 and n not in (8, 9, 10, 12, 14)]
    M = {n: [sum(1 << x for x in range(a, 2520, n)) & R
             for a in range(n)] for n in inventory}
    cap = [[n, max(m.bit_count() for m in M[n])] for n in inventory]
    four = (15, 24, 36, 72)
    seven = four + (18, 20, 28)
    other32 = sum(v for n, v in cap if n not in four)
    threshold = len(points) - other32
    raw = bytearray(2 * 933120)
    accepted = []
    best4, witness4, visited4 = -1, None, 0
    # Reverse order differs from the producer; indices are canonical.
    for d in range(71, -1, -1):
        for c in range(35, -1, -1):
            CD = M[72][d] | M[36][c]
            for b in range(23, -1, -1):
                BCD = CD | M[24][b]
                for a in range(14, -1, -1):
                    U = BCD | M[15][a]
                    gain = U.bit_count()
                    index = ((a * 24 + b) * 36 + c) * 72 + d
                    struct.pack_into('<H', raw, 2 * index, gain)
                    visited4 += 1
                    phase = [a, b, c, d]
                    if gain > best4 or (gain == best4 and phase < witness4):
                        best4, witness4 = gain, phase
                    if gain >= threshold:
                        accepted.append((phase, U))
    accepted.sort(key=lambda item: item[0])
    joint = bytearray(2 * len(accepted) * 10080)
    best7, witness7, visited7 = -1, None, 0
    for slot in range(len(accepted) - 1, -1, -1):
        phase, U = accepted[slot]
        for g in range(27, -1, -1):
            UG = U | M[28][g]
            for f in range(19, -1, -1):
                UGF = UG | M[20][f]
                for e in range(17, -1, -1):
                    gain = (UGF | M[18][e]).bit_count()
                    index = slot * 10080 + (e * 20 + f) * 28 + g
                    struct.pack_into('<H', joint, 2 * index, gain)
                    visited7 += 1
                    phases = phase + [e, f, g]
                    if gain > best7 or (gain == best7 and phases < witness7):
                        best7, witness7 = gain, phases
    require(visited4 == 933120, 'Incomplete independent core enumeration')
    require(visited7 == len(accepted) * 10080,
            'Incomplete independent seven-resource enumeration')
    for labels, phases, claimed in ((four, witness4, best4),
                                   (seven, witness7, best7)):
        literal = sum(any(x % n == a for n, a in zip(labels, phases))
                      for x in points)
        require(literal == claimed, 'Literal maximizing witness mismatch')
    other29 = sum(v for n, v in cap if n not in seven)
    return {
        'rows': list(rows), 'initial_count': len(initial),
        'required_count': len(points), 'capacities': cap,
        'other32_capacity': other32, 'core_threshold': threshold,
        'core_phase_vectors': visited4, 'core_maximum': best4,
        'core_maximizer': witness4, 'retained_core_vectors': len(accepted),
        'all_core_gains_sha256': hashlib.sha256(raw).hexdigest(),
        'conditional7_phase_vectors': visited7, 'conditional7_maximum': best7,
        'conditional7_maximizer': witness7,
        'all_conditional7_gains_sha256': hashlib.sha256(joint).hexdigest(),
        'other29_capacity': other29,
        'conditional_total_capacity': best7 + other29,
        'strict_deficit': len(points) - best7 - other29,
    }


def audit(path):
    candidate = json.loads(Path(path).read_text())
    inventory = [n for n in range(8, 2521)
                 if 2520 % n == 0 and n not in (8, 9, 10, 12, 14)]
    require(candidate.get('schema') == 'prescribed-P-parent4-two-row-v1', 'Schema')
    require(candidate.get('prefix') == [[8, 0], [9, 0], [10, 1], [14, 1], [12, 10]],
            'Wrong prescribed prefix')
    require(candidate.get('base') == inventory, 'Original BASE inventory')
    require(candidate.get('core') == [15, 24, 36, 72], 'Core inventory')
    require(candidate.get('extra') == [18, 20, 28], 'Extra inventory')
    pairs = list(itertools.combinations(range(5), 2))
    require([c.get('rows') for c in candidate.get('cases', [])]
            == [list(s) for s in pairs], 'Incomplete or duplicate two-row cover')
    records = []
    for s, entry in zip(pairs, candidate['cases']):
        actual = independent_case(s)
        require(entry == actual, 'Full record mismatch at rows ' + str(s))
        require(actual['strict_deficit'] == 9, 'Strict deficit not verified')
        records.append(actual)
    return {'complete': True, 'cases': len(records),
            'all_core_phase_vectors': sum(c['core_phase_vectors'] for c in records),
            'all_retained_core_vectors': sum(c['retained_core_vectors'] for c in records),
            'all_conditional7_phase_vectors': sum(c['conditional7_phase_vectors'] for c in records),
            'full_records_sha256': hashlib.sha256(json.dumps(records, sort_keys=True,
                                separators=(',', ':')).encode()).hexdigest(),
            'same_author_independent_algorithm': True,
            'external_review_claimed': False}


if __name__ == '__main__':
    print(json.dumps(audit(sys.argv[1] if len(sys.argv) == 2
                           else Path(__file__).with_name('expected.json')), sort_keys=True))
