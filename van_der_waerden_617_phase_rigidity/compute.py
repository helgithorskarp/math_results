#!/usr/bin/env python3
"""Exact rectangular coverage of incompatible affine QR block pairs.

No solver or input certificate is used. Python integers implement phase sets.
"""
import hashlib
import json

P = 617
K = 7
D = 28


def residue_colors():
    assert all(P % d for d in range(2, 25)), "617 must be prime"
    return [-1] + [0 if pow(x, (P - 1) // 2, P) == 1 else 1
                   for x in range(1, P)]


def coverage():
    q = residue_colors()
    # A bit represents a phase, not a point. Neither color set contains a pole.
    masks = [[sum(1 << s for s in range(P) if q[(x + s) % P] == b)
              for x in range(P)] for b in (0, 1)]
    full_phase = (1 << P) - 1
    forbidden = [0] * P
    prefix_counts = []
    crossing_progressions = 0
    horizon_27_nontrivial = []
    for d in range(1, D + 1):
        for a in range(P - 6 * d, P):
            crossing_progressions += 1
            left = [a + j * d for j in range(K) if a + j * d < P]
            right = [a + j * d - P for j in range(K) if a + j * d >= P]
            for b in (0, 1):
                lmask = full_phase
                rmask = [full_phase, full_phase]
                for x in left:
                    lmask &= masks[b][x]
                for x in right:
                    rmask[0] &= masks[b][x]
                    rmask[1] &= masks[1 - b][x]
                right_pairs = rmask[0] | (rmask[1] << P)
                while lmask:
                    bit = lmask & -lmask
                    s = bit.bit_length() - 1
                    lmask ^= bit
                    forbidden[s] |= right_pairs
        prefix_counts.append(sum(2 * P - row.bit_count() for row in forbidden))
        if d == 27:
            for s, row in enumerate(forbidden):
                bits = ((1 << (2 * P)) - 1) ^ row ^ (1 << s)
                while bits:
                    bit = bits & -bits
                    t = bit.bit_length() - 1
                    bits ^= bit
                    horizon_27_nontrivial.append([s, t % P, t // P])
            assert horizon_27_nontrivial == [[154, 463, 1], [155, 464, 1]]
    full_pairs = (1 << (2 * P)) - 1
    for s, row in enumerate(forbidden):
        # Entry-level assertion: the only surviving column is (phase=s, flip=0).
        assert full_pairs ^ row == 1 << s, (s, full_pairs ^ row)

    # Definition-level cyclic check, with a hole omitted. Multiplicativity also
    # reduces this to d=1, but this separate direct check enumerates every d.
    modular_progressions = 0
    for a in range(P):
        for d in range(1, P):
            colors = {q[(a + j * d) % P] for j in range(K)} - {-1}
            assert colors == {0, 1}, (a, d, colors)
            modular_progressions += 1
    force_residues = [(1 - j * 47) % P for j in range(1, K)]
    assert all(q[x] == 1 for x in force_residues)
    # Enumerate the multiplier version used in the arbitrary-phase bridge.
    for r in range(1, P):
        step = r * 47 % P
        assert 1 <= step < P
        assert all(q[(r - j * step) % P] == 1 - q[r]
                   for j in range(1, K))
    return {
        "prime": P,
        "progression_length": K,
        "maximum_obstruction_difference": D,
        "crossing_progressions": crossing_progressions,
        "normalized_phase_orientation_pairs": 2 * P * P,
        "excluded_normalized_pairs": 2 * P * P - P,
        "surviving_normalized_pairs": P,
        "survivors": "exactly (s,t,e)=(s,s,0), for 0<=s<617",
        "survivor_counts_by_difference": prefix_counts,
        "horizon_27_nontrivial_survivors": horizon_27_nontrivial,
        "all_modular_nonzero_difference_progressions": modular_progressions,
        "forcing_step_for_residue_one": 47,
        "forcing_predecessor_residues": force_residues,
        "forcing_multiplier_cases": P - 1,
        "valid_ordered_two_block_parameter_choices": P * 2 * 4,
        "total_ordered_two_block_parameter_choices": (P * 2 * 2) ** 2,
        "valid_six_block_plus_one_colorings": 2 * (2 ** 7 - 2),
        "valid_six_block_plus_two_colorings": 0,
        "qr_nonzero_color_sha256": hashlib.sha256(bytes(q[1:])).hexdigest(),
    }


if __name__ == "__main__":
    print(json.dumps(coverage(), indent=2, sort_keys=True))
