#!/usr/bin/env python3
"""Independent bit-intersection check of the old QR-617 construction family."""

import hashlib
import json


P = 617
N = 6 * P + 1


def mono_aps(bits):
    all_bits = (1 << N) - 1
    hits = []
    for color_bits in (bits, all_bits ^ bits):
        for d in range(1, (N - 1) // 6 + 1):
            starts = color_bits
            for j in range(1, 7):
                starts &= color_bits >> (j * d)
            while starts:
                bit = starts & -starts
                hits.append((bit.bit_length() - 1, d))
                starts ^= bit
    return sorted(hits)


def main():
    nonresidue_bits = sum(1 << x for x in range(N)
                          if x % P and pow(x % P, (P - 1) // 2, P) == P - 1)
    exceptional_bits = sum(1 << (j * P) for j in range(7))
    if mono_aps(nonresidue_bits) != [(0, P)]:
        raise ValueError("Unexpected progression when all exceptions are zero")
    if mono_aps(nonresidue_bits | exceptional_bits) != [(0, P)]:
        raise ValueError("Unexpected progression when all exceptions are one")
    # Any monochromatic AP under a mixed exceptional assignment would also
    # be monochromatic in one of the two constant exceptional assignments.
    seed_bits = nonresidue_bits | (1 << (N - 1))
    if mono_aps(seed_bits):
        raise ValueError("The canonical incumbent has a monochromatic AP")
    seed = ''.join(str((seed_bits >> x) & 1) for x in range(N))
    print(json.dumps({
        "verified_length": N,
        "canonical_seed_sha256_without_newline": hashlib.sha256(seed.encode()).hexdigest(),
        "monochromatic_seven_term_aps": 0,
        "covered_seven_term_aps": sum(N - 6 * d for d in range(1, (N - 1) // 6 + 1)),
        "valid_exceptional_assignments": (1 << 7) - 2,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
