"""Explicit congruence-partition stabilizers for period43200.

Actual author six-covering-3, researcher. These maps preserve coverings;
no covering existence or nonexistence is asserted by this module.
"""
N, Q = 43200, 3600
ANCHORS = (8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 30, 36, 40, 45)


def literal(value, bound):
    if type(value) is not int or not 0 <= value < bound:
        raise ValueError('Expected a literal residue in the stated range')


def parent_ok(parent):
    if not isinstance(parent, (tuple, list)) or len(parent) != len(ANCHORS):
        raise ValueError('Expected fourteen prescribed anchor phases')
    for value, modulus in zip(parent, ANCHORS):
        literal(value, modulus)


def binary_map(period, root=6):
    if period not in (N, Q):
        raise ValueError('Only the stated full and projected periods are implemented')
    literal(root, 8)
    return [(x + 16200) % period if x % 16 == root else
            (x - 16200) % period if x % 16 == root+8 else x
            for x in range(period)]


def quinary_map(period, source, target, fixed25=None, fixed_leaves=()):
    if period not in (N, Q):
        raise ValueError('Only the stated full and projected periods are implemented')
    literal(source, 25)
    literal(target, 25)
    if source % 5 != target % 5:
        raise ValueError('Second-digit leaves must have the same first digit')
    raw_pins = tuple(fixed_leaves)
    for leaf in raw_pins:
        literal(leaf, 25)
    pins = set(raw_pins)
    if fixed25 is not None:
        literal(fixed25, 25)
        pins.add(fixed25)
    for leaf in pins:
        literal(leaf, 25)
    if source != target and pins.intersection((source, target)):
        raise ValueError('The transposition moves a prescribed quinary leaf')
    cofactor = period // 25
    shift = cofactor * ((target - source) * pow(cofactor, -1, 25) % 25)
    return [(x + shift) % period if x % 25 == source else
            (x - shift) % period if x % 25 == target else x
            for x in range(period)]


def binary_rep(phase48, fixed16):
    literal(phase48, 48)
    literal(fixed16, 16)
    leaf = phase48 % 16
    root = leaf % 8
    target = leaf if root == fixed16 % 8 else root
    return next(target+16*j for j in range(3) if (target+16*j) % 3 == phase48 % 3)


def quinary_rep(phase50, fixed25):
    literal(phase50, 50)
    literal(fixed25, 25)
    leaf = phase50 % 25
    root = leaf % 5
    if root != fixed25 % 5:
        target = root
    elif leaf == fixed25:
        target = fixed25
    else:
        target = next(root + 5 * j for j in range(5) if root + 5 * j != fixed25)
    return target if target % 2 == phase50 % 2 else target + 25


def joint_rep(phase48, phase50, fixed16, fixed25):
    return binary_rep(phase48, fixed16), quinary_rep(phase50, fixed25)


def pinned75_rep(phase75, fixed25, fixed50):
    literal(phase75, 75)
    literal(fixed25, 25)
    literal(fixed50, 50)
    pins = {fixed25, fixed50 % 25}
    leaf = phase75 % 25
    root = leaf % 5
    target = leaf if leaf in pins else next(root + 5*j for j in range(5)
                                           if root + 5*j not in pins)
    return next(target + 25*j for j in range(3)
                if (target + 25*j) % 3 == phase75 % 3)
