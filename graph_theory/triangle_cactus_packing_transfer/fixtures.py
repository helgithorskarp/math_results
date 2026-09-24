"""Small exact inputs and affine block lists; no external data or solver."""

from itertools import product


def affine_blocks(blocks, dimension=5, repetitions=8):
    """Each labeled K2/K3 has R*3^d copies, each vertex-role degree R.

    Vertices are F_3^d in lexicographic order. Distinct normalized directions
    have last coordinate 1. Three parallel classes, with shifted roles, make
    one balanced triangle layer; one cyclically oriented parallel class makes
    one balanced edge layer. All block lists are mutually edge-disjoint.
    """
    if dimension < 1 or repetitions < 1:
        raise ValueError('positive dimension and repetition count required')
    needed = repetitions * sum(3 if len(b) == 3 else 1 for b in blocks)
    if any(len(b) not in (2, 3) for b in blocks) or needed > 3**(dimension-1):
        raise ValueError('insufficient affine directions or unsupported block')
    points = list(product(range(3), repeat=dimension))
    index = {v: j for j, v in enumerate(points)}
    origins = [v for v in points if v[-1] == 0]
    directions = [v+(1,) for v in product(range(3), repeat=dimension-1)]
    cursor, result = 0, []
    for block in blocks:
        copies = []
        for _ in range(repetitions):
            for offset in range(3 if len(block) == 3 else 1):
                direction = directions[cursor]
                cursor += 1
                for origin in origins:
                    line = [index[tuple((x+a*d) % 3
                                        for x, d in zip(origin, direction))]
                            for a in range(3)]
                    if len(block) == 3:
                        copies.append(tuple(line[(j-offset) % 3] for j in range(3)))
                    else:
                        copies.extend((line[j], line[(j+1) % 3]) for j in range(3))
        result.append(copies)
    return result, [0]*len(points), repetitions*len(points)


def separated_classes(blocks, sizes):
    """One class per abstract role, using a common Latin-square subarray."""
    offsets, classes = [], []
    for i, size in enumerate(sizes):
        if size < 1:
            raise ValueError('empty fixture class')
        offsets.append(len(classes))
        classes.extend([i]*size)
    side = min(sizes)
    lists = []
    for block in blocks:
        if len(block) == 2:
            lists.append([(offsets[block[0]]+x, offsets[block[1]]+y)
                          for x in range(side) for y in range(side)])
        elif len(block) == 3:
            lists.append([(offsets[block[0]]+x, offsets[block[1]]+y,
                           offsets[block[2]]+(x+y) % side)
                          for x in range(side) for y in range(side)])
        else:
            raise ValueError('unsupported block')
    return lists, classes, side*side
