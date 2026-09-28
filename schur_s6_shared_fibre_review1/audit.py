"""Independent literal group audit for the shared-fibre projection lemma."""
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1] / "additive_combinatorics" / "schur6_shared_fibre_projection"


def symmetric_state(half, middle):
    return [middle, *half, *half[::-1]]


def colour_words(axis, fibre):
    a = len(axis)
    six = []
    five = []
    for n in range(1, 5 * a):
        u, b = n % a, n % 5
        if b == 0:
            six.append(axis[u])
        elif fibre[u]:
            six.append(fibre[u])
        else:
            six.append(0 if b in (1, 4) else 1)
    for n in range(1, 2 * a):
        u = n % a
        old = axis[u] if n % 2 == 0 else fibre[u]
        five.append(0 if old in (0, 1) else old - 1)
    return six, five


def violations(word):
    modulus = len(word) + 1
    classes = {}
    for residue, colour in enumerate(word, 1):
        classes.setdefault(colour, set()).add(residue)
    bad = []
    for colour, points in classes.items():
        for x in sorted(points):
            for y in sorted(v for v in points if v >= x):
                z = (x + y) % modulus
                if z and z in points:
                    bad.append((x, y, z, colour))
    return sorted(bad)


def sum_free(points, modulus):
    return all((x + y) % modulus not in points
               for x in points for y in points)


def differences(points, modulus):
    return {(x - y) % modulus for x in points for y in points}


def criterion(axis, fibre):
    a = len(axis)
    e = [{u for u in range(1, a) if axis[u] == colour}
         for colour in range(6)]
    r = {u for u in range(a) if fibre[u] == 0}
    c = {colour: {u for u in range(a) if fibre[u] == colour}
         for colour in (2, 3, 4, 5)}
    return (all(sum_free(points, a) for points in e)
            and all(sum_free(points, a) for points in c.values())
            and not ((e[0] | e[1]) & differences(r, a))
            and all(not (e[colour] & differences(c[colour], a))
                    for colour in c))


def mergeable(axis):
    a = len(axis)
    merged = {u for u in range(1, a) if axis[u] in (0, 1)}
    return sum_free(merged, a)


def fixtures():
    data = json.loads((HERE / "fixtures.json").read_text())
    out = []
    for row in data:
        a = row["axis_factor"]
        axis = symmetric_state(row["axis_half"], -1)
        fibre = symmetric_state(row["fibre_half"], 0)
        six, five = colour_words(axis, fibre)
        if six != row["word"] or five != row["projection"]:
            raise ValueError(f"fixture {a}: word mismatch")
        if not criterion(axis, fibre) or violations(six):
            raise ValueError(f"fixture {a}: invalid six-colouring")
        projection_bad = violations(five)
        if bool(projection_bad) == mergeable(axis):
            raise ValueError(f"fixture {a}: projection mismatch")
        if a == 47 and (projection_bad or len(six) != 234 or len(five) != 93):
            raise ValueError("47-axis calibration failure")
        if a == 7 and len(projection_bad) != 4:
            raise ValueError("7-axis negative control failure")
        out.append((a, len(projection_bad)))
    return out


def exhaustive_seven():
    total = valid = merge = 0
    for axis_half in itertools.product(range(6), repeat=3):
        axis = symmetric_state(axis_half, -1)
        for fibre_half in itertools.product((0, 2, 3, 4, 5), repeat=3):
            fibre = symmetric_state(fibre_half, 0)
            six, five = colour_words(axis, fibre)
            literal = not violations(six)
            if literal != criterion(axis, fibre):
                raise ValueError("criterion disagreement")
            total += 1
            if not literal:
                continue
            valid += 1
            merged = mergeable(axis)
            bad = violations(five)
            if bool(bad) == merged:
                raise ValueError("projection disagreement")
            if any(x % 2 or y % 2 or z % 2 or colour != 0
                   for x, y, z, colour in bad):
                raise ValueError("defect outside merged axis")
            merge += merged
    return total, valid, merge


def main():
    fixed = fixtures()
    totals = exhaustive_seven()
    if fixed != [(47, 0), (7, 4)] or totals != (27000, 3096, 2664):
        raise ValueError((fixed, totals))
    print("PASS fixtures_47_7=yes assignments=27000 valid=3096 "
          "mergeable=2664 literal_projection_checks=yes")


if __name__ == "__main__":
    main()
