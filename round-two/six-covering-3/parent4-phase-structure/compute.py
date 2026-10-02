"""Exact producer for the prescribed-P two-row BASE obstruction.

No imported research modules, solver, symmetry quotient, or numerical tolerance.
Bit positions enumerate the required points, rather than physical residues.
"""
import hashlib
import itertools
import json
import struct

PREFIX = ((8, 0), (9, 0), (10, 1), (14, 1), (12, 10))
BASE = tuple(n for n in range(8, 2521) if 2520 % n == 0
             and n not in {m for m, _ in PREFIX})
CORE = (15, 24, 36, 72)
EXTRA = (18, 20, 28)


def case(rows):
    initial = [x for x in range(2520)
               if all(x % n != a for n, a in PREFIX)]
    required = [x for x in initial
                if not (x % 8 == 4 and x % 5 in rows)]
    masks = {}
    caps = []
    for n in BASE:
        buckets = [0] * n
        for j, x in enumerate(required):
            buckets[x % n] |= 1 << j
        masks[n] = buckets
        caps.append([n, max(m.bit_count() for m in buckets)])
    other32 = sum(c for n, c in caps if n not in CORE)
    threshold = len(required) - other32
    left = [(a, b, masks[15][a] | masks[24][b])
            for a, b in itertools.product(range(15), range(24))]
    right = [(c, d, masks[36][c] | masks[72][d])
             for c, d in itertools.product(range(36), range(72))]
    retained = []
    gains = bytearray(2 * 15 * 24 * 36 * 72)
    best4 = -1
    witness4 = None
    visited4 = 0
    for a, b, L in left:
        for c, d, R in right:
            union = L | R
            gain = union.bit_count()
            struct.pack_into('<H', gains, 2 * visited4, gain)
            visited4 += 1
            if gain > best4:
                best4, witness4 = gain, [a, b, c, d]
            if gain >= threshold:
                retained.append(([a, b, c, d], union))
    core_hash = hashlib.sha256(gains).hexdigest()
    extras = [(e, f, g, masks[18][e] | masks[20][f] | masks[28][g])
              for e, f, g in itertools.product(range(18), range(20), range(28))]
    joint = bytearray(2 * len(retained) * 18 * 20 * 28)
    best7 = -1
    witness7 = None
    visited7 = 0
    for phases, union in retained:
        for e, f, g, added in extras:
            gain = (union | added).bit_count()
            struct.pack_into('<H', joint, 2 * visited7, gain)
            visited7 += 1
            if gain > best7:
                best7, witness7 = gain, phases + [e, f, g]
    if visited4 != 933120 or visited7 != len(retained) * 10080:
        raise RuntimeError('Incomplete phase enumeration')
    other29 = sum(c for n, c in caps if n not in CORE + EXTRA)
    return {
        'rows': list(rows), 'initial_count': len(initial),
        'required_count': len(required), 'capacities': caps,
        'other32_capacity': other32, 'core_threshold': threshold,
        'core_phase_vectors': visited4, 'core_maximum': best4,
        'core_maximizer': witness4, 'retained_core_vectors': len(retained),
        'all_core_gains_sha256': core_hash,
        'conditional7_phase_vectors': visited7, 'conditional7_maximum': best7,
        'conditional7_maximizer': witness7,
        'all_conditional7_gains_sha256': hashlib.sha256(joint).hexdigest(),
        'other29_capacity': other29,
        'conditional_total_capacity': best7 + other29,
        'strict_deficit': len(required) - best7 - other29,
    }


def record():
    return {'schema': 'prescribed-P-parent4-two-row-v1',
            'agent': 'six-covering-3', 'role': 'researcher',
            'prefix': [list(p) for p in PREFIX], 'base': list(BASE),
            'core': list(CORE), 'extra': list(EXTRA),
            'cases': [case(s) for s in itertools.combinations(range(5), 2)]}


if __name__ == '__main__':
    print(json.dumps(record(), sort_keys=True, indent=2))
