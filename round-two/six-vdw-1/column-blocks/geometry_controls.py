"""Literal small-interval truth tables and a boundary cubic control."""
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def windows(p):
    n = 6 * p + 2
    return [(a, d, tuple(a + j * d for j in range(7)), 1 + (a + 3 * d) % 5)
            for a in range(n - 6) for d in range(1, (n - 1 - a) // 6 + 1)]


def literal(word, aps):
    return sum(weight for _, _, points, weight in aps
               if all(word[x] == word[points[0]] for x in points[1:]))


def check():
    covered = 0
    for p in (7, 11, 13, 17, 19, 23):
        for a, d, points, _ in windows(p):
            ordinary = [x % p for x in points if x % p >= 2]
            require(len(ordinary) == len(set(ordinary)), "ordinary column repeats")
            if len({x % p for x in points}) < 7:
                require(d == p and a in (0, 1), "unexpected repeated column")
            covered += 1
    p = 7
    aps = windows(p)
    word = [0] * 44
    word[2] = word[17] = 1
    points = [r + p * k for r in (2, 3) for k in range(6)]
    values = []
    for mask in range(4096):
        proposed = word.copy()
        for i, x in enumerate(points):
            proposed[x] ^= mask >> i & 1
        values.append(literal(proposed, aps))
    base = values[0]
    linear = [values[1 << i] - base for i in range(12)]
    cross = [[values[(1 << i) | (1 << (j + 6))] - base - linear[i] - linear[j + 6]
              for j in range(6)] for i in range(6)]
    for mask, value in enumerate(values):
        prediction = base + sum(linear[i] for i in range(12) if mask >> i & 1)
        prediction += sum(cross[i][j] for i in range(6) for j in range(6)
                          if mask >> i & 1 and mask >> (j + 6) & 1)
        require(value == prediction, "literal small-interval block mismatch")
    require(any(cross[i][j] for i in range(6) for j in range(6)), "vacuous cross control")
    boundary = [1, 8, 15]
    cubic = 0
    for mask in range(8):
        proposed = [0] * 44
        for i, x in enumerate(boundary):
            proposed[x] = mask >> i & 1
        cubic += (-1) ** (3 - mask.bit_count()) * literal(proposed, aps)
    require(cubic == -3, "boundary third mixed difference must be nonzero")
    return {"status": "LITERAL_GEOMETRY_AND_BOUNDARY_CONTROLS_CHECKED",
            "geometry_windows": covered, "small_prime": p, "small_windows": len(aps),
            "small_assignments": 4096, "boundary_cubic": cubic}


if __name__ == "__main__":
    print(json.dumps(check(), indent=2, sort_keys=True))
