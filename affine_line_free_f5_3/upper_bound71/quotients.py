"""Full affine partition across the normalized AA, AB and BB catalogues."""
from itertools import permutations, product

POINTS = tuple(product(range(5), repeat=2))
NORMALS = tuple((1, a) for a in range(5)) + ((0, 1),)
VALUES = tuple(tuple((a*x+b*y) % 5 for x, y in POINTS)
               for a, b in NORMALS)
A = (8, 16, 16, 16, 16)
B = (9, 15, 16, 16, 16)
PROFILES = ((A, A), (A, B), (B, B))


def validate(key):
    kind, word = key
    if kind not in range(3) or len(word) != 25 or any(c not in "01234" for c in word):
        raise ValueError("invalid typed quotient word")
    weight = tuple(map(int, word))
    if sum(weight) != 72:
        raise ValueError("incorrect total")
    profiles = tuple(tuple(sum(weight[i] for i in range(25) if values[i] == b)
                           for b in range(5)) for values in VALUES)
    if any(max(profile) > 16 or min(profile) < 8 for profile in profiles):
        raise ValueError("plane bounds violated")
    if (profiles[0], profiles[5]) != PROFILES[kind]:
        raise ValueError("distinguished profiles disagree with the type")
    if weight[0] > (2 if kind == 2 else 1):
        raise ValueError("intersection pencil bound violated")
    if any(weight[i] > 3 or weight[5*i] > 3 for i in range(5)):
        raise ValueError("axis pencil bound violated")
    return profiles


def orbit(key):
    profiles = validate(key)
    word = key[1]
    low = []
    for direction, profile in enumerate(profiles):
        for label, size in enumerate(profile):
            if size not in (8, 9):
                continue
            scales = range(1, 5) if size == 8 else (pow((profile.index(15)-label) % 5, -1, 5),)
            low.append((direction, label, size, scales))
    result = set()
    for (d, b, first, scales_x), (e, c, second, scales_y) in permutations(low, 2):
        if d == e or first > second:
            continue
        new_type = int(first == 9)+int(second == 9)
        for scale_x, scale_y in product(scales_x, scales_y):
            permutation = [5*(scale_x*(VALUES[d][i]-b) % 5)
                           + scale_y*(VALUES[e][i]-c) % 5 for i in range(25)]
            if len(set(permutation)) != 25:
                raise RuntimeError("singular affine normalization")
            image = [""]*25
            for i, j in enumerate(permutation):
                image[j] = word[i]
            result.add((new_type, "".join(image)))
    return result


def classify(keys):
    keys = set(keys)
    remaining = set(keys)
    representatives = []
    while remaining:
        representative = min(remaining)
        images = orbit(representative)
        if not images <= remaining or min(images) != representative:
            raise RuntimeError("orbit coverage or canonicalization failure")
        for image in images:
            validate(image)
        remaining -= images
        representatives.append({"type": representative[0], "weights": representative[1],
                                "orbit_size": len(images)})
    if sum(r["orbit_size"] for r in representatives) != len(keys):
        raise RuntimeError("incomplete typed catalogue partition")
    return representatives
