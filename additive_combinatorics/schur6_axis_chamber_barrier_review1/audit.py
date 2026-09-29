"""Independent dense-vector audit of the axis-only Schur chamber certificate.

Uses no code from the reviewed construction or checker. All arithmetic in
certificate identities is exact. Run with assertions enabled.
"""

from collections import Counter
from fractions import Fraction
from itertools import groupby, product
from math import gcd
from pathlib import Path
import json

if not __debug__:
    raise RuntimeError("Assertions must be enabled")

SOURCE = Path(__file__).resolve().parents[1] / "schur6_axis_chamber_barrier"


def add(*vectors):
    return tuple(sum(entries) for entries in zip(*vectors))


def mul(n, vector):
    return tuple(n * entry for entry in vector)


def subtract(left, right):
    return add(left, mul(-1, right))


def value(form, lengths):
    return sum(coef * length for coef, length in zip(form[:-1], lengths)) + form[-1]


def modular_rows(word):
    modulus = len(word) + 1
    assert modulus % 2 == 1
    assert word == list(reversed(word))
    assert all(type(colour) is int and 0 <= colour < 6 for colour in word)
    checked = 0
    for left in range(1, modulus):
        for right in range(left, modulus):
            target = (left + right) % modulus
            if target == 0:
                continue
            assert len({word[left - 1], word[right - 1], word[target - 1]}) > 1
            checked += 1
    return checked


def unit_word(axis, multiplier):
    modulus = len(axis) + 1
    image = [None] * (modulus - 1)
    for position, colour in enumerate(axis, 1):
        image[(multiplier * position) % modulus - 1] = colour
    assert all(colour is not None for colour in image)
    return image


def runs(word):
    half = word[:len(word) // 2]
    pairs = [(colour, len(list(group))) for colour, group in groupby(half)]
    return [pair[0] for pair in pairs], [pair[1] for pair in pairs]


def affine_intervals(colours):
    dimension = len(colours)
    zero = (0,) * (dimension + 1)
    one = zero[:-1] + (1,)
    variables = [tuple(int(i == j) for i in range(dimension)) + (0,)
                 for j in range(dimension)]
    modulus = (2,) * dimension + (1,)
    by_colour = [[] for _ in range(6)]
    cursor = one
    for j, colour in enumerate(colours):
        following = add(cursor, variables[j])
        by_colour[colour].append((cursor, subtract(following, one)))
        cursor = following
    for colour in range(6):
        originals = list(by_colour[colour])
        by_colour[colour].extend((subtract(modulus, right), subtract(modulus, left))
                                 for left, right in originals)
    return by_colour, modulus, one


def numeric_intervals(word):
    colours, lengths = runs(word)
    modulus = len(word) + 1
    by_colour = [[] for _ in range(6)]
    cursor = 1
    for colour, length in zip(colours, lengths):
        by_colour[colour].append((cursor, cursor + length - 1))
        cursor += length
    assert cursor == (modulus + 1) // 2
    for colour in range(6):
        originals = list(by_colour[colour])
        by_colour[colour].extend((modulus - right, modulus - left)
                                 for left, right in originals)
    return colours, lengths, by_colour


def literal_membership(seed, witness):
    old_colours, old_lengths, old = numeric_intervals(seed)
    new_colours, new_lengths, new = numeric_intervals(witness)
    assert old_colours == new_colours
    checked = 0
    for colour in range(6):
        assert len(old[colour]) == len(new[colour])
        for i, j, k in product(range(len(old[colour])), repeat=3):
            for wrap in (0, 1):
                sides = []
                for modulus, intervals in ((len(seed) + 1, old), (len(witness) + 1, new)):
                    left, right = intervals[colour][i]
                    other_left, other_right = intervals[colour][j]
                    target_left, target_right = intervals[colour][k]
                    target_left += wrap * modulus
                    target_right += wrap * modulus
                    before = right + other_right < target_left
                    after = target_right < left + other_left
                    assert before != after
                    sides.append(before)
                assert sides[0] == sides[1]
                checked += 1
    return checked, new_lengths


def proof_record(chamber, seed_axis):
    multiplier = chamber["multiplier"]
    image = unit_word(seed_axis, multiplier)
    assert image == unit_word(seed_axis, 71 - multiplier)
    modular_rows(image)
    colours, lengths = runs(image)
    assert chamber["dimension"] == len(lengths)
    assert chamber["run_colours"] == colours
    intervals, modulus, one = affine_intervals(colours)
    dimension = len(lengths)
    derived = []
    terms = Counter()

    def premise(reason):
        kind = reason[0]
        if kind == "positive_run_length":
            assert len(reason) == 2 and 0 <= reason[1] < dimension
            vector = list((0,) * (dimension + 1))
            vector[reason[1]] = -1
            vector[-1] = 1
            form = tuple(vector)
        elif kind == "integer_rounding":
            assert len(reason) == 2 and 0 <= reason[1] < len(derived)
            form = derived[reason[1]]
        else:
            assert kind == "axis_sum" and len(reason) == 7
            _, colour, i, j, k, wrap, side = reason
            assert 0 <= colour < 6 and wrap in (0, 1)
            assert side in ("left_before_right", "right_before_left")
            assert all(0 <= index < len(intervals[colour]) for index in (i, j, k))
            low_i, high_i = intervals[colour][i]
            low_j, high_j = intervals[colour][j]
            low_k, high_k = intervals[colour][k]
            low_sum, high_sum = add(low_i, low_j), add(high_i, high_j)
            low_target = add(low_k, mul(wrap, modulus))
            high_target = add(high_k, mul(wrap, modulus))
            if side == "left_before_right":
                form = add(subtract(high_sum, low_target), one)
            else:
                form = add(subtract(high_target, low_sum), one)
            common = gcd(*form)
            assert common >= 1
            form = tuple(entry // common for entry in form)
        assert value(form, lengths) <= 0, (multiplier, reason)
        terms[kind] += 1
        return form

    def identity(proof):
        result = tuple(Fraction(0) for _ in range(dimension + 1))
        for term in proof["terms"]:
            weight = Fraction(term["weight"])
            assert weight > 0
            result = add(result, mul(weight, premise(term["reason"])))
        return result

    for cut in chamber["rounding_cuts"]:
        if "coordinate" in cut:
            j = cut["coordinate"]
            assert 0 <= j < dimension
            objective = tuple(int(i == j) for i in range(dimension))
        else:
            objective = tuple(cut["coefficients"])
            assert len(objective) == dimension
            assert all(type(entry) is int for entry in objective)
        upper = Fraction(cut["upper"])
        assert identity(cut) == objective + (-upper,)
        floor = upper.numerator // upper.denominator
        derived.append(objective + (-floor,))
    upper = Fraction(chamber["upper_bound_axis_factor"])
    assert identity(chamber) == subtract(modulus, (0,) * dimension + (upper,))
    cap = upper.numerator // upper.denominator
    while cap % 2 == 0 or cap % 3 == 0:
        cap -= 1
    return cap, terms, len(derived), len(lengths)


def main():
    cert = json.loads((SOURCE / "certificate.json").read_text())
    seed = json.loads((SOURCE / "seed.json").read_text())
    witness = json.loads((SOURCE / "axis_witness.json").read_text())
    assert cert["seed_word"] == seed["word"]
    assert cert["seed_axis_factor"] == seed["axis_factor"] == 71
    full = seed["word"]
    assert len(full) == 354
    full_rows = modular_rows(full)
    axis = [full[5 * q - 1] for q in range(1, 71)]
    axis_rows = modular_rows(axis)
    expected_units = list(range(1, 36))
    assert [chamber["multiplier"] for chamber in cert["chambers"]] == expected_units
    bounds = {}
    terms = Counter()
    cuts = 0
    dimensions = []
    for chamber in cert["chambers"]:
        bound, used, cut_count, dimension = proof_record(chamber, axis)
        bounds[chamber["multiplier"]] = bound
        terms.update(used)
        cuts += cut_count
        dimensions.append(dimension)
    assert max(bounds.values()) == 107
    assert sum(terms.values()) == 614 and cuts == 11
    assert min(dimensions) == 18 and max(dimensions) == 33
    word = witness["axis_word"]
    assert witness["multiplier"] == 15
    assert len(word) + 1 == witness["axis_factor"] == 107
    witness_rows = modular_rows(word)
    comparisons, lengths = literal_membership(unit_word(axis, 15), word)
    assert comparisons == 7536 and lengths == witness["run_lengths"]
    assert Counter(word) == Counter(dict(enumerate(witness["class_sizes"])))
    print("PASS units=35 terms=614 cuts=11 axis_cap=107 full_endpoint_cap=534 "
          f"seed_modular_rows={full_rows} axis_modular_rows={axis_rows} "
          f"witness_modular_rows={witness_rows} membership_comparisons={comparisons}")


if __name__ == "__main__":
    main()
