"""Complete affine partition of the mixed catalogue after the two-eight lemma."""
from itertools import product

POINTS = tuple(product(range(5), repeat=2))
NORMALS = tuple((1, a) for a in range(5)) + ((0, 1),)
VALUES = tuple(tuple((a*x+b*y) % 5 for x, y in POINTS)
               for a, b in NORMALS)
A = (8, 16, 16, 16, 16)
B = (9, 15, 16, 16, 16)


def validate(word):
    if len(word) != 25 or any(c not in "01234" for c in word):
        raise ValueError("invalid quotient word")
    weight = tuple(map(int, word))
    if sum(weight) != 72:
        raise ValueError("incorrect total")
    profiles = tuple(tuple(sum(weight[i] for i in range(25) if values[i] == b)
                           for b in range(5)) for values in VALUES)
    if any(max(profile) > 16 for profile in profiles):
        raise ValueError("plane upper bound violated")
    if profiles[0] != A or profiles[5] != B:
        raise ValueError("distinguished profiles are not AB")
    if weight[0] > 1 or any(weight[i] > 3 or weight[5*i] > 3 for i in range(5)):
        raise ValueError("pencil bound violated")
    return profiles


def eight_count(word):
    return sum(profile.count(8) for profile in validate(word))


def orbit(word):
    profiles = validate(word)
    eights = [(d, b) for d, profile in enumerate(profiles)
              for b, size in enumerate(profile) if size == 8]
    nines = [(d, b) for d, profile in enumerate(profiles)
             for b, size in enumerate(profile) if size == 9]
    if len(eights) != 1:
        raise ValueError("the orbit stage requires exactly one eight-line")
    result = set()
    for d, b in eights:
        for e, c in nines:
            if d == e:
                raise RuntimeError("parallel low lines at total 72")
            # The other four parallel lines total 63, hence their sizes are
            # 15,16,16,16. This unique scaling puts the 15-line at label one.
            fifteen = profiles[e].index(15)
            scale_y = pow((fifteen-c) % 5, -1, 5)
            for scale_x in range(1, 5):
                permutation = [5*(scale_x*(VALUES[d][i]-b) % 5)
                               + scale_y*(VALUES[e][i]-c) % 5 for i in range(25)]
                if len(set(permutation)) != 25:
                    raise RuntimeError("singular affine normalization")
                image = [""]*25
                for i, j in enumerate(permutation):
                    image[j] = word[i]
                result.add("".join(image))
    return result


def classify(words):
    words = set(words)
    discarded = {word for word in words if eight_count(word) >= 2}
    remaining = words - discarded
    representatives = []
    while remaining:
        representative = min(remaining)
        images = orbit(representative)
        if not images <= remaining or min(images) != representative:
            raise RuntimeError("orbit coverage or canonicalization failure")
        for image in images:
            if eight_count(image) != 1:
                raise RuntimeError("affine orbit changed the eight-line count")
        remaining -= images
        representatives.append({"weights": representative, "orbit_size": len(images)})
    if len(discarded)+sum(r["orbit_size"] for r in representatives) != len(words):
        raise RuntimeError("incomplete catalogue partition")
    return representatives, len(discarded)
