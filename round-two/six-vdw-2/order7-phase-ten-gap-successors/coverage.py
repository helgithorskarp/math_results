"""Exact rooted gap counts by transfer DP and separate zero-run double counting."""
from collections import Counter
from fractions import Fraction
import itertools
import json
import math
import time


def require(ok, message):
    if not ok:
        raise ValueError(message)


def transfer(n, total, cap):
    # The first deficit is zero: the first selected gap is two.
    states = {(0, 0): 1}
    for _ in range(n - 1):
        nxt = Counter()
        for (subtotal, last), ways in states.items():
            for digit in range(min(cap, total - subtotal) + 1):
                if last == 0 and digit > 1:
                    continue
                nxt[subtotal + digit, digit] += ways
        states = nxt
    # The closing successor is zero, so it always satisfies the turn rule.
    return sum(v for (s, _), v in states.items() if s == total)


def positive_coefficient(slots, total, cap):
    if total < 0:
        return 0
    poly = [1]
    for _ in range(slots):
        out = [0] * (len(poly) + cap)
        for i, ways in enumerate(poly):
            for digit in range(2, cap + 1):
                out[i + digit] += ways
        poly = out
    return poly[total] if total < len(poly) else 0


def runs(n, total, cap):
    # z zeros may occur only in slots immediately preceding a positive one.
    # Rooting at a zero instead of a positive multiplies by z/(n-z).
    result = Fraction(int(total == 0))  # The all-zero cyclic word.
    for z in range(1, n):
        p = n - z
        subtotal = 0
        for q in range(1, p + 1):
            subtotal += (math.comb(p, q) *
                         positive_coefficient(p - q, total - q, cap) *
                         math.comb(z + q - 1, q - 1))
        result += Fraction(z * subtotal, p)
    require(result.denominator == 1, 'nonintegral rooted zero-run count')
    return result.numerator


def unconstrained(slots, total, cap):
    # Independent inclusion-exclusion for bounded weak compositions.
    return sum((-1) ** k * math.comb(slots, k) *
               math.comb(total - (cap + 1) * k + slots - 1, slots - 1)
               for k in range(min(slots, total // (cap + 1)) + 1))


def phase_fixed(n, j, background):
    anchors = {0, 2, j}
    return {i: 1 - background if i in anchors else background
            for i in range(n) if i in anchors or 3 <= i < j or
            any(min((i - a) % n, (a - i) % n) < 2 for a in anchors)}


def main():
    began = time.monotonic()
    literal_words = count_controls = 0
    for n in range(3, 9):
        literal = Counter()
        for tail in itertools.product(range(3), repeat=n - 1):
            word = (0,) + tail
            if all(a != 0 or word[(i + 1) % n] <= 1
                   for i, a in enumerate(word)):
                literal[sum(word)] += 1
                literal_words += 1
        for total in range(2 * (n - 1) + 1):
            require(transfer(n, total, 2) == runs(n, total, 2) == literal[total],
                    'tiny literal, transfer and run counts differ')
            count_controls += 1

    head_controls = 0
    for n in range(8, 13):
        for word in itertools.product((0, 1), repeat=n):
            for background in (0, 1):
                selected = [i for i, v in enumerate(word) if v != background]
                if len(selected) < 3 or selected[:2] != [0, 2]:
                    continue
                gaps = [(selected[(i + 1) % len(selected)] - a) % n
                        for i, a in enumerate(selected)]
                if not all(2 <= g <= 8 for g in gaps):
                    continue
                j = selected[2]
                require(4 <= j <= 10 and
                        all(word[i] == v for i, v in phase_fixed(n, j, background).items()),
                        'literal first-next normalization differs')
                head_controls += 1

    before = unconstrained(9, 24, 6)
    after = transfer(10, 24, 6)
    require(after == runs(10, 24, 6) and 0 < after < before,
            'independent forty-four-cycle counts differ')
    cases = []
    for j in range(10, 5, -1):
        for background in (0, 1):
            fixed = phase_fixed(44, j, background)
            free = 44 - len(fixed)
            require(free == 41 - j and sum(v != background for v in fixed.values()) == 3,
                    'wrong forbidden head dimensions')
            cases.append(dict(stem=f'next-2-{j}-b-{background}',
                              variables=16 + 10 * free, free_phases=free,
                              remaining_selected=7))
    print(json.dumps(dict(agent='six-vdw-2', role='researcher',
        status='EXACT_PHASE10_GAP_SUCCESSOR_COVER', forbidden_case_count=10,
        forbidden_next_indices=[6, 7, 8, 9, 10], allowed_next_indices=[4, 5],
        all_gap_two_successors=[2, 3], cases=cases,
        rooted_phase_profiles_before_per_background=before,
        rooted_phase_profiles_after_per_background=after,
        eliminated_rooted_phase_profiles_per_background=before-after,
        count_controls=count_controls, literal_tiny_words=literal_words,
        first_next_binary_controls=head_controls,
        counts_are_field_colorings=False, counts_are_rotation_orbits=False,
        global_W_bound=False, seconds=time.monotonic()-began)), flush=True)


if __name__ == '__main__':
    main()
