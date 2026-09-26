"""Exact affine quotient of the complete two-eight-plane catalogue."""
from itertools import permutations, product

POINTS = tuple(product(range(5), repeat=2))
NORMALS = tuple((1, a) for a in range(5)) + ((0, 1),)
VALUES = tuple(tuple((a*x+b*y) % 5 for x, y in POINTS)
               for a, b in NORMALS)


def validate(word):
    if len(word) != 25 or any(c not in "01234" for c in word):
        raise ValueError("invalid quotient word")
    w = tuple(map(int, word))
    if sum(w) != 72:
        raise ValueError("incorrect total")
    profiles = tuple(tuple(sum(w[i] for i in range(25) if values[i] == b)
                           for b in range(5)) for values in VALUES)
    if any(max(profile) > 16 for profile in profiles):
        raise ValueError("plane upper bound violated")
    if profiles[0] != (8, 16, 16, 16, 16) or profiles[5] != profiles[0]:
        raise ValueError("distinguished profiles are not AA")
    return profiles


def orbit(word):
    profiles = validate(word)
    low = [(d, b) for d, profile in enumerate(profiles)
           for b, size in enumerate(profile) if size == 8]
    result = set()
    for (d, b), (e, c) in permutations(low, 2):
        if d == e:
            continue
        for scale_x, scale_y in product(range(1, 5), repeat=2):
            perm = [5*(scale_x*(VALUES[d][i]-b) % 5)
                    + scale_y*(VALUES[e][i]-c) % 5 for i in range(25)]
            if len(set(perm)) != 25:
                raise RuntimeError("noninvertible affine normalization")
            transformed = [""]*25
            for i, j in enumerate(perm):
                transformed[j] = word[i]
            result.add("".join(transformed))
    return result


def classify(words):
    words = set(words)
    remaining = set(words)
    result = []
    while remaining:
        representative = min(remaining)
        images = orbit(representative)
        if not images <= remaining or min(images) != representative:
            raise RuntimeError("orbit coverage or canonicalization failure")
        remaining -= images
        result.append({"weights": representative, "orbit_size": len(images)})
    if sum(r["orbit_size"] for r in result) != len(words):
        raise RuntimeError("incorrect orbit multiplicities")
    return result
