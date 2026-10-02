"""Thirteen conditional branch masks for the literal parent-four P/A4 frame.

Membership in a mask does not certify A4, BASE realizability, or a cover.
The ordinary completeness proof is in proof.md. No solver is used here.
"""
from itertools import combinations


PREFIX = ((8, 0), (9, 0), (10, 1), (14, 1), (12, 10))
UNIVERSE = tuple(y for y in range(315) if y % 9)


def branch_masks():
    """Return (name, allowed residues, cardinality cap) for all 13 cases."""
    return (
        ("small87", UNIVERSE, 87),
        *((f"rows{a}{b}", tuple(y for y in UNIVERSE if y % 5 in (a, b)), None)
          for a, b in combinations(range(5), 2)),
        *((f"color{c}", tuple(y for y in UNIVERSE if y % 3 == c), None)
          for c in (1, 2)),
    )


def memberships(holes, phase21):
    """List applicable branches; require distinct literal residues and phase21.

    H must lie in U after the chosen ORIGINAL modulus-21 class is removed.
    This function deliberately does not presume or establish the A4 hypothesis.
    An arbitrary input can therefore have no memberships.
    """
    if type(phase21) is not int or not 0 <= phase21 < 21:
        raise ValueError("Expected one original phase of modulus21 in 0..20")
    h = tuple(holes)
    if (any(type(y) is not int or not 0 <= y < 315 or not y % 9 for y in h)
            or len(set(h)) != len(h)):
        raise ValueError("Expected distinct literal residues of the parent4 universe")
    if any(y % 21 == phase21 for y in h):
        raise ValueError("A hole is covered by the supplied original21 phase")
    hs = set(h)
    return tuple(name for name, allowed, cap in branch_masks()
                 if hs <= set(allowed) and (cap is None or len(h) <= cap))


def three_tail_phases(color):
    """Original16/32/96 phases covering every parent4 point of this color.

    This is an existential bridge when all other BASE holes are already gone.
    The three original resources must be free, as they are after the BASE stage.
    """
    if type(color) is not int or color not in (0, 1, 2):
        raise ValueError("Expected a mod3 color")
    a96 = next(a for a in range(96) if a % 32 == 28 and a % 3 == color)
    return ((16, 4), (32, 12), (96, a96))
