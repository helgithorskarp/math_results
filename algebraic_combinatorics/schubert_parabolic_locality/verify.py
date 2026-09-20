#!/usr/bin/env python3
"""Exact checks for Coxeter-support locality of Schubert specializations."""

from __future__ import annotations

from fractions import Fraction
from functools import cache
from itertools import permutations
from math import factorial


Permutation = tuple[int, ...]


def identity(n: int) -> Permutation:
    return tuple(range(n))


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
    descents = [i for i in range(len(w) - 1) if w[i] > w[i + 1]]
    if not descents:
        return 1
    r = descents[-1]
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
    for i in range(len(w) - 1):
        if w[i] > w[i + 1]:
            child = list(w)
            child[i], child[i + 1] = child[i + 1], child[i]
            total += (i + 1) * reduced_word_weight_sum(tuple(child))
    return total


def macdonald_upsilon(w: Permutation) -> int:
    value = Fraction(reduced_word_weight_sum(w), factorial(inversion_count(w)))
    assert value.denominator == 1
    return value.numerator


def coxeter_support(w: Permutation) -> tuple[int, ...]:
    """One-based simple generators in the Coxeter support of w."""
    support = []
    seen: set[int] = set()
    for i, value in enumerate(w[:-1], start=1):
        seen.add(value)
        if seen != set(range(i)):
            support.append(i)
    return tuple(support)


def support_intervals(w: Permutation) -> tuple[tuple[int, int], ...]:
    support = coxeter_support(w)
    if not support:
        return ()
    intervals: list[list[int]] = [[support[0], support[0]]]
    for generator in support[1:]:
        if generator == intervals[-1][1] + 1:
            intervals[-1][1] = generator
        else:
            intervals.append([generator, generator])
    return tuple((a, b) for a, b in intervals)


def parabolic_components(w: Permutation) -> tuple[Permutation, ...]:
    """Nonidentity factors, embedded in the same symmetric group as w."""
    result = []
    for a, b in support_intervals(w):
        # Generator interval [a,b] acts on zero-based positions [a-1,b].
        component = list(range(len(w)))
        component[a - 1 : b + 1] = w[a - 1 : b + 1]
        result.append(tuple(component))
    return tuple(result)


def compose(u: Permutation, v: Permutation) -> Permutation:
    """Function composition u after v."""
    return tuple(u[v[i]] for i in range(len(u)))


def inflate_identity(w: Permutation, k: int) -> Permutation:
    return tuple(k * value + offset for value in w for offset in range(k))


def is_grassmannian(w: Permutation) -> bool:
    return sum(w[i] > w[i + 1] for i in range(len(w) - 1)) <= 1


def grassmannian_partition(w: Permutation) -> tuple[int, ...]:
    descents = [i for i in range(len(w) - 1) if w[i] > w[i + 1]]
    if not descents:
        return ()
    assert len(descents) == 1
    d = descents[0] + 1
    lam = tuple(w[d - i] - (d - i) for i in range(1, d + 1))
    assert all(lam[i] >= lam[i + 1] for i in range(len(lam) - 1))
    assert all(part >= 0 for part in lam)
    return lam


def weyl_dimension(lam: tuple[int, ...]) -> int:
    value = Fraction(1)
    for i in range(len(lam)):
        for j in range(i + 1, len(lam)):
            value *= Fraction(lam[i] - lam[j] + j - i, j - i)
    assert value.denominator == 1
    return value.numerator


def inflated_partition(lam: tuple[int, ...], k: int) -> tuple[int, ...]:
    return tuple(k * part for part in lam for _ in range(k))


def verify_component_factorization(w: Permutation, k: int | None = None) -> None:
    components = parabolic_components(w)
    product = identity(len(w))
    for component in components:
        product = compose(component, product)
    assert product == w
    assert inversion_count(w) == sum(inversion_count(c) for c in components)
    base = transition_upsilon(w)
    component_product = 1
    for component in components:
        component_product *= transition_upsilon(component)
    assert base == component_product
    if k is not None:
        image = transition_upsilon(inflate_identity(w, k))
        image_product = 1
        for component in components:
            image_product *= transition_upsilon(inflate_identity(component, k))
        assert image == image_product


def verify_grassmannian(w: Permutation, k: int) -> None:
    assert is_grassmannian(w)
    lam = grassmannian_partition(w)
    base = transition_upsilon(w)
    assert base == weyl_dimension(lam)
    image_w = inflate_identity(w, k)
    image_lam = grassmannian_partition(image_w)
    assert image_lam == inflated_partition(lam, k)
    image = transition_upsilon(image_w)
    assert image == weyl_dimension(image_lam)
    assert image >= base ** (k * k)


def main() -> None:
    formula_cases = 0
    factor_cases = 0
    inflated_factor_cases = 0
    k3_inflated_factor_cases = 0
    componentwise_cases = 0
    k3_componentwise_cases = 0
    strict_multidescent_cases = 0

    for n in range(1, 9):
        for w in permutations(range(n)):
            assert transition_upsilon(w) == macdonald_upsilon(w)
            formula_cases += 1
            verify_component_factorization(w)
            factor_cases += 1

    for n in range(1, 7):
        for w in permutations(range(n)):
            verify_component_factorization(w, 2)
            inflated_factor_cases += 1
            components = parabolic_components(w)
            if components and all(is_grassmannian(c) for c in components):
                base = transition_upsilon(w)
                image = transition_upsilon(inflate_identity(w, 2))
                assert image >= base**4
                componentwise_cases += 1
                if sum(w[i] > w[i + 1] for i in range(n - 1)) >= 2 and base > 3:
                    strict_multidescent_cases += 1

    grassmannian_cases = 0
    for n in range(1, 8):
        for w in permutations(range(n)):
            if not is_grassmannian(w):
                continue
            verify_grassmannian(w, 2)
            grassmannian_cases += 1

    k3_grassmannian_cases = 0
    for n in range(1, 6):
        for w in permutations(range(n)):
            verify_component_factorization(w, 3)
            k3_inflated_factor_cases += 1
            components = parabolic_components(w)
            if components and all(is_grassmannian(c) for c in components):
                base = transition_upsilon(w)
                image = transition_upsilon(inflate_identity(w, 3))
                assert image >= base**9
                k3_componentwise_cases += 1
            if is_grassmannian(w):
                verify_grassmannian(w, 3)
                k3_grassmannian_cases += 1

    w = (0, 2, 1, 4, 3)
    assert coxeter_support(w) == (2, 4)
    assert transition_upsilon(w) == 8
    assert transition_upsilon(inflate_identity(w, 2)) == 6720

    print(f"macdonald_transition_cases={formula_cases}")
    print(f"base_factorization_cases={factor_cases}")
    print(f"k2_inflated_factorization_cases={inflated_factor_cases}")
    print(f"k3_inflated_factorization_cases={k3_inflated_factor_cases}")
    print(f"grassmannian_weyl_cases={grassmannian_cases}")
    print(f"k3_grassmannian_weyl_cases={k3_grassmannian_cases}")
    print(f"componentwise_grassmannian_k2_cases={componentwise_cases}")
    print(f"componentwise_grassmannian_k3_cases={k3_componentwise_cases}")
    print(f"new_multidescent_nontrivial_cases={strict_multidescent_cases}")
    print("example=13254 base=8 inflated_k2=6720 rhs=4096")
    print(
        "cache_states="
        f"transition:{transition_upsilon.cache_info().currsize},"
        f"macdonald:{reduced_word_weight_sum.cache_info().currsize}"
    )
    print("all exact checks passed")


if __name__ == "__main__":
    main()
