#!/usr/bin/env python3
"""Exact audits for inverse-Grassmannian Schubert identity inflation."""

from __future__ import annotations

from fractions import Fraction
from functools import cache
from itertools import permutations
from math import factorial


Permutation = tuple[int, ...]


def require(condition: bool, message: str = "exact check failed") -> None:
    if not condition:
        raise AssertionError(message)


def identity(n: int) -> Permutation:
    return tuple(range(n))


def inverse(w: Permutation) -> Permutation:
    result = [0] * len(w)
    for i, value in enumerate(w):
        result[value] = i
    return tuple(result)


def inversion_count(w: Permutation) -> int:
    return sum(a > b for i, a in enumerate(w) for b in w[i + 1 :])


def strip_fixed_suffix(w: Permutation) -> Permutation:
    while w and w[-1] == len(w) - 1:
        w = w[:-1]
    return w


@cache
def transition_upsilon(w: Permutation) -> int:
    """Principal specialization via the Lascoux transition recurrence."""
    w = strip_fixed_suffix(w)
    if len(w) < 2:
        return 1
    desc = descents(w)
    if not desc:
        return 1
    r = desc[-1]
    s = max(j for j in range(r + 1, len(w)) if w[j] < w[r])
    v = list(w)
    v[r], v[s] = v[s], v[r]
    v = tuple(v)
    length_v = inversion_count(v)
    total = transition_upsilon(v)
    for q in range(r):
        child = list(v)
        child[q], child[r] = child[r], child[q]
        child = tuple(child)
        if inversion_count(child) == length_v + 1:
            total += transition_upsilon(child)
    return total


@cache
def reduced_word_weight_sum(w: Permutation) -> int:
    """Sum of products of one-based letters over all reduced words."""
    if w == identity(len(w)):
        return 1
    total = 0
    for i in descents(w):
        child = list(w)
        child[i], child[i + 1] = child[i + 1], child[i]
        total += (i + 1) * reduced_word_weight_sum(tuple(child))
    return total


def macdonald_upsilon(w: Permutation) -> int:
    value = Fraction(reduced_word_weight_sum(w), factorial(inversion_count(w)))
    require(value.denominator == 1, "Macdonald quotient is nonintegral")
    return value.numerator


def descents(w: Permutation) -> tuple[int, ...]:
    """Zero-based positions of descents."""
    return tuple(i for i in range(len(w) - 1) if w[i] > w[i + 1])


def is_grassmannian(w: Permutation) -> bool:
    return len(descents(w)) <= 1


def is_inverse_grassmannian(w: Permutation) -> bool:
    return is_grassmannian(inverse(w))


def coxeter_support(w: Permutation) -> tuple[int, ...]:
    """One-based type-A simple generators in the Coxeter support."""
    support = []
    seen: set[int] = set()
    for r, value in enumerate(w[:-1], start=1):
        seen.add(value)
        if seen != set(range(r)):
            support.append(r)
    return tuple(support)


def grassmannian_partition(w: Permutation) -> tuple[int, ...]:
    ds = descents(w)
    if not ds:
        return ()
    require(len(ds) == 1, "permutation is not Grassmannian")
    d = ds[0] + 1
    lam = tuple(w[d - i] - (d - i) for i in range(1, d + 1))
    require(all(lam[i] >= lam[i + 1] for i in range(len(lam) - 1)))
    require(all(part >= 0 for part in lam))
    return lam


def inflate_identity(w: Permutation, k: int) -> Permutation:
    require(k >= 1, "inflation factor must be positive")
    return tuple(k * value + residue for value in w for residue in range(k))


def inflated_partition(lam: tuple[int, ...], k: int) -> tuple[int, ...]:
    return tuple(k * part for part in lam for _ in range(k))


def weyl_dimension(lam: tuple[int, ...]) -> int:
    value = Fraction(1)
    for i in range(len(lam)):
        for j in range(i + 1, len(lam)):
            value *= Fraction(lam[i] - lam[j] + j - i, j - i)
    require(value.denominator == 1, "Weyl product is nonintegral")
    return value.numerator


def partitions_in_box(rows: int, columns: int):
    def rec(prefix: tuple[int, ...], ceiling: int):
        if len(prefix) == rows:
            yield prefix
            return
        for part in range(ceiling, -1, -1):
            yield from rec(prefix + (part,), part)

    yield from rec((), columns)


def alternating_inverse_grassmannian(m: int) -> Permutation:
    # One-based (m+1,1,m+2,2,...,2m,m), converted to zero-based.
    return tuple(value for i in range(m) for value in (m + i, i))


def verify_inverse_case(w: Permutation, k: int, direct: bool) -> None:
    require(is_inverse_grassmannian(w))
    u = inverse(w)
    lam = grassmannian_partition(u)
    base = transition_upsilon(w)
    require(base == transition_upsilon(u) == weyl_dimension(lam))

    iw = inflate_identity(w, k)
    iu = inflate_identity(u, k)
    require(inverse(iw) == iu)
    image_lam = grassmannian_partition(iu)
    require(image_lam == inflated_partition(lam, k))
    image_weyl = weyl_dimension(image_lam)
    if direct:
        require(transition_upsilon(iw) == transition_upsilon(iu) == image_weyl)
    require(image_weyl >= base ** (k * k))
    if k > 1:
        expected_equality = not lam or len(set(lam)) == 1
        require((image_weyl == base ** (k * k)) == expected_equality)


def main() -> None:
    formula_cases = 0
    inversion_cases = 0
    for n in range(1, 9):
        for w in permutations(range(n)):
            value = transition_upsilon(w)
            require(value == transition_upsilon(inverse(w)))
            inversion_cases += 1
            if n <= 7:
                require(value == macdonald_upsilon(w))
                formula_cases += 1

    k2_direct_cases = 0
    k3_direct_cases = 0
    for n in range(1, 8):
        for w in permutations(range(n)):
            if not is_inverse_grassmannian(w):
                continue
            verify_inverse_case(w, 2, direct=True)
            k2_direct_cases += 1
            if n <= 5:
                verify_inverse_case(w, 3, direct=True)
                k3_direct_cases += 1

    weyl_cases = 0
    equality_cases = 0
    for rows in range(1, 7):
        for columns in range(0, 7):
            for lam in partitions_in_box(rows, columns):
                base = weyl_dimension(lam)
                for k in range(1, 6):
                    image = weyl_dimension(inflated_partition(lam, k))
                    require(image >= base ** (k * k))
                    if k > 1:
                        expected = len(set(lam)) == 1
                        require((image == base ** (k * k)) == expected)
                        equality_cases += 1
                    weyl_cases += 1

    family_cases = 0
    examples = []
    for m in range(1, 7):
        w = alternating_inverse_grassmannian(m)
        require(descents(w) == tuple(range(0, 2 * m - 1, 2)))
        u = inverse(w)
        require(descents(u) == ((m - 1,) if m > 0 else ()))
        require(grassmannian_partition(u) == tuple(range(m, 0, -1)))
        require(coxeter_support(w) == tuple(range(1, 2 * m)))
        require(coxeter_support(u) == tuple(range(1, 2 * m)))
        verify_inverse_case(w, 2, direct=m <= 4)
        base = weyl_dimension(grassmannian_partition(u))
        image = weyl_dimension(inflated_partition(grassmannian_partition(u), 2))
        examples.append((m, base, image))
        family_cases += 1

    print(f"macdonald_transition_cases={formula_cases}")
    print(f"inversion_symmetry_cases={inversion_cases}")
    print(f"inverse_grassmannian_k2_direct_cases={k2_direct_cases}")
    print(f"inverse_grassmannian_k3_direct_cases={k3_direct_cases}")
    print(f"weyl_pairing_cases={weyl_cases}")
    print(f"weyl_equality_checks={equality_cases}")
    print(f"alternating_family_cases={family_cases}")
    print("alternating_family=" + ";".join(f"m{m}:{base}->{image}" for m, base, image in examples))
    print(
        "cache_states="
        f"transition:{transition_upsilon.cache_info().currsize},"
        f"macdonald:{reduced_word_weight_sum.cache_info().currsize}"
    )
    print("all exact checks passed")


if __name__ == "__main__":
    main()
