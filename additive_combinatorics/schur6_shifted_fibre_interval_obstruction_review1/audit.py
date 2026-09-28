"""Independent small-model and interval audits for shifted Schur fibres."""

import json
from itertools import combinations, product
from pathlib import Path
from random import Random

SOURCE = Path(__file__).resolve().parents[1] / "schur6_shifted_fibre_interval_obstruction"


def word_from_rows(a, p, axis, fibre):
    n, t = a * p, (p - 1) // 2
    word = [None] * n
    for q in range(1, a):
        word[p * q] = axis[min(q, a - q) - 1]
    for q in range(a):
        for b in range(1, t + 1):
            colour = fibre[q] if fibre[q] else b - 1
            x = p * q + b
            word[x] = word[n - x] = colour
    assert word[0] is None and all(type(c) is int for c in word[1:])
    return word


def literal_ok(word):
    n = len(word)
    for x in range(1, n):
        for y in range(x, n):
            z = (x + y) % n
            if z and word[x] == word[y] == word[z]:
                return False
    return True


def conditions(a, p, axis, fibre):
    t = (p - 1) // 2
    E = [set() for _ in range(6)]
    for q in range(1, a):
        E[axis[min(q, a - q) - 1]].add(q)
    R = {q for q, label in enumerate(fibre) if label == 0}
    C = {colour: {q for q, label in enumerate(fibre) if label == colour}
         for colour in range(t, 6)}

    def sum_free(S):
        return all((x + y) % a not in S for x in S for y in S)

    def differences(S):
        return {(x - y) % a for x in S for y in S}

    if not all(sum_free(S) for S in E):
        return False
    if set().union(*E[:t]) & differences(R):
        return False
    for colour, S in C.items():
        if not sum_free(S):
            return False
        if any((-1 - x - y) % a in S for x in S for y in S):
            return False
        if E[colour] & differences(S):
            return False
    return True


def normalize(a, p, axis, fibre):
    t = (p - 1) // 2
    common_order = list(dict.fromkeys(c for c in (*fibre, *axis) if c >= t))
    special_order = list(dict.fromkeys(c for c in axis if c < t))
    common_map = {c: t + i for i, c in enumerate(common_order)}
    special_map = {c: i for i, c in enumerate(special_order)}
    for c in range(t, 6):
        if c not in common_map:
            common_map[c] = len(common_map) + t
    for c in range(t):
        if c not in special_map:
            special_map[c] = len(special_map)
    new_axis = tuple(common_map[c] if c >= t else special_map[c] for c in axis)
    new_fibre = tuple(common_map[c] if c >= t else 0 for c in fibre)
    return new_axis, new_fibre


def small_cases(a, p):
    t = (p - 1) // 2
    labels = (0, *range(t, 6))
    checked = valid = 0
    for axis in product(range(6), repeat=(a - 1) // 2):
        for tail in product(labels, repeat=a - 1):
            fibre = (0, *tail)
            word = word_from_rows(a, p, axis, fibre)
            direct = literal_ok(word)
            assert direct == conditions(a, p, axis, fibre)
            checked += 1
            if direct:
                valid += 1
                new_axis, new_fibre = normalize(a, p, axis, fibre)
                assert conditions(a, p, new_axis, new_fibre)
                assert literal_ok(word_from_rows(a, p, new_axis, new_fibre))
    return checked, valid


def noncoprime_samples():
    a, p = 7, 7
    labels = (0, 3, 4, 5)
    random = Random(20260928)
    valid = 0
    for _ in range(4096):
        axis = tuple(random.randrange(6) for _ in range((a - 1) // 2))
        fibre = (0, *(random.choice(labels) for _ in range(a - 1)))
        direct = literal_ok(word_from_rows(a, p, axis, fibre))
        assert direct == conditions(a, p, axis, fibre)
        valid += direct
    return 4096, valid


def path_capacity(length, d):
    total = 0
    for residue in range(d):
        vertices = list(range(residue, length, d))
        skip, take = 0, -1000
        for _ in vertices:
            skip, take = max(skip, take), skip + 1
        total += max(skip, take)
    return total


def capacity_boundary():
    capacities = [path_capacity(36, d) for d in range(1, 33)]
    expected = [18, 18, 18, 20, 20, 18, 21, 20, 18, 20, 22, 24, 23, 22,
                21, 20, 19, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                29, 30, 31, 32]
    assert capacities == expected
    all_bits = (1 << 36) - 1
    accepted = []
    examined = 0
    for holes in combinations(range(36), 4):
        bits = all_bits ^ sum(1 << pos for pos in holes)
        missing = [d for d in range(1, 33) if bits & (bits >> d) == 0]
        examined += 1
        if missing:
            assert missing == [32]
            accepted.append(tuple(pos + 37 for pos in holes))
    assert examined == 58905 and len(accepted) == 16
    expected_holes = {
        tuple(sorted(37 + i if bits & (1 << i) else 69 + i for i in range(4)))
        for bits in range(16)
    }
    assert set(accepted) == expected_holes
    return capacities, examined, len(accepted)


def interval_prefixes():
    for p, m in ((5, 2), (5, 20), (5, 32), (5, 36),
                 (7, 2), (7, 22), (7, 26)):
        a = 3 * m + 1
        interval = set(range(m + 1, 2 * m + 1))
        differences = {(x - y) % a for x in interval for y in interval}
        t = (p - 1) // 2
        for x in range(1, p * m):
            q, b = divmod(x, p)
            if b == 0:
                assert q in differences
            else:
                source = q if b <= t else a - 1 - q
                assert source not in interval
    a, p = 109, 5
    interval = set(range(37, 73))
    axis = []
    for x in range(1, 162):
        q, b = divmod(x, p)
        if b == 0:
            axis.append(q)
        else:
            source = q if b <= 2 else a - 1 - q
            assert source not in interval
    assert axis == list(range(1, 33))
    return 7, len(axis)


def published_controls():
    controls = json.loads((SOURCE / "controls.json").read_text(encoding="ascii"))
    endpoints = []
    for data in controls:
        a, p, digits = data["axis_factor"], data["short_factor"], data["word"]
        assert len(digits) == a * p - 1 and set(digits) == set(range(6))
        axis = tuple(digits[p * u - 1] for u in range(1, (a + 1) // 2))
        fibre = tuple(digits[p * q] for q in range(a))
        reconstructed = word_from_rows(a, p, axis, fibre)
        assert reconstructed[1:] == digits and literal_ok(reconstructed)
        assert conditions(a, p, axis, fibre)
        if data.get("full_middle_third_colour") is not None:
            colour = data["full_middle_third_colour"]
            assert {q for q, c in enumerate(fibre) if c == colour} == {
                q for q in range(a) if a < 3 * q < 2 * a
            }
        if a * p - 1 == 304:
            assert [digits.count(c) for c in range(6)] == [44, 42, 100, 38, 40, 40]
            assert digits.index(2) + 1 == 100
        endpoints.append(a * p - 1)
    assert sorted(endpoints) == [34, 64, 234, 304]
    return sorted(endpoints)


def main():
    checked_5, valid_5 = small_cases(5, 5)
    checked_7, valid_7 = small_cases(5, 7)
    sampled, sampled_valid = noncoprime_samples()
    capacities, subsets, supports = capacity_boundary()
    prefixes, early_axis = interval_prefixes()
    endpoints = published_controls()
    print(f"PASS exhaustive_small_p5={checked_5} valid_p5={valid_5} "
          f"exhaustive_small_p7={checked_7} valid_p7={valid_7} "
          f"noncoprime_p7_samples={sampled} noncoprime_valid={sampled_valid} "
          f"capacity_max={max(capacities)} size32_subsets={subsets} "
          f"boundary_supports={supports} prefix_controls={prefixes} "
          f"early_axis_candidates={early_axis} control_endpoints={endpoints}")


if __name__ == "__main__":
    main()
