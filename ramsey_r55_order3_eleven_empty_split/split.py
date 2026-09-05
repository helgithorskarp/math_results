#!/usr/bin/env python3
"""Complete z=1 versus z>=2 split in the existing fixed-signature order."""
CASES = ((11, 'one'), (11, 'many'), (13, 'one'), (13, 'many'))
EQUALITY_MASKS = (0, 4, 4, 2, 2, 6, 1, 1, 5, 3)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def units(branch):
    if branch == 'many':
        return [-222, -223, -224]
    require(branch == 'one', 'unknown branch')
    # The first three zero bits are already units in the signature parent.
    return [v if mask & (1 << i) else -v
            for row, mask in enumerate(EQUALITY_MASKS) if row > 0
            for i in range(3) for v in [211+11*row+i]]


def name(core, branch):
    require((core, branch) in CASES, 'unknown case')
    return f'c{core}_{branch}'
