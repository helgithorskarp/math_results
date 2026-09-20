#!/usr/bin/env python3
"""Independent bit-mask audit of the L_13 deletion capacities."""

from itertools import combinations


def bitset(items):
    answer = 0
    for item in items:
        answer |= 1 << (item - 1)
    return answer


points = range(1, 10)
all4 = [bitset(c) for c in combinations(points, 4)]
base = all4[:13]
remaining = all4[13:]

# Derived afresh from block masks rather than importing verify.py.
base_avoid = [sum(not (block & (1 << i)) for block in base) for i in range(9)]
caps = [11 - value for value in base_avoid]


def admissible(extra):
    used = [0] * 9
    for block in extra:
        for i in range(9):
            used[i] += not (block & (1 << i))
    return all(used[i] <= caps[i] for i in range(9))


hard = [block for block in remaining if block & bitset((8, 9)) == bitset((8, 9))]

assert base_avoid == [0, 0, 7, 7, 9, 10, 10, 11, 11]
assert caps == [11, 11, 4, 4, 2, 1, 1, 0, 0]
assert len(remaining) == 113 and len(hard) == 21
assert sum(admissible((block,)) for block in remaining) == 21

counts = []
degree_signatures = set()
for size in range(1, 5):
    survivors = [extra for extra in combinations(hard, size) if admissible(extra)]
    counts.append(len(survivors))
    if size == 3:
        for extra in survivors:
            degrees = []
            for vertex in range(1, 8):
                degrees.append(sum(block & (1 << (vertex - 1)) != 0 for block in extra))
            degree_signatures.add(tuple(degrees))

assert counts == [21, 45, 9, 0]
assert all(signature[4] >= 1 for signature in degree_signatures)
assert all(signature[5] >= 2 and signature[6] >= 2 for signature in degree_signatures)

# Independent closed counts: at distance two, either edge 67 is present
# (20 choices for the other edge), or one chooses 6a and 7b with a,b in [5].
assert counts[1] == 20 + 5 * 5
# At distance three, include 67, then choose 6a and 7b, with a=5 or b=5.
assert counts[2] == 5 * 5 - 4 * 4

print("base avoidance:", base_avoid)
print("deletion capacities:", caps)
print("surviving counts m=1..4:", counts)
print("independent bit-mask audit: PASS")
