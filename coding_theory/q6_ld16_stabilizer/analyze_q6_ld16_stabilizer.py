#!/usr/bin/env python3
"""Solver-free certificate for the symmetry structure of the optimum Q_6 code."""

from __future__ import annotations

import itertools
from collections import Counter
from dataclasses import dataclass


DIMENSION = 6
VERTEX_COUNT = 1 << DIMENSION
IDENTITY_PERMUTATION = tuple(range(DIMENSION))

# Bit i is coordinate x_{6-i}; printed words use x_1 ... x_6.
QUADRATIC_CODE = frozenset(
    {0, 5, 11, 14, 18, 23, 25, 28, 34, 36, 41, 47, 51, 53, 56, 62}
)
CANONICAL_CODE = frozenset(
    {0, 3, 5, 10, 20, 27, 29, 30, 38, 41, 44, 47, 49, 50, 55, 56}
)


@dataclass(frozen=True, order=True)
class Automorphism:
    """The map word |-> permute(word, permutation) XOR translation."""

    permutation: tuple[int, ...]
    translation: int

    def __call__(self, word: int) -> int:
        return permute_word(word, self.permutation) ^ self.translation


IDENTITY = Automorphism(IDENTITY_PERMUTATION, 0)


def permute_word(word: int, permutation: tuple[int, ...]) -> int:
    """Move source bit i to destination bit permutation[i]."""
    image = 0
    for source, destination in enumerate(permutation):
        image |= ((word >> source) & 1) << destination
    return image


def compose(first: Automorphism, second: Automorphism) -> Automorphism:
    """Return first after second."""
    permutation = tuple(
        first.permutation[second.permutation[i]] for i in range(DIMENSION)
    )
    translation = (
        first.translation
        ^ permute_word(second.translation, first.permutation)
    )
    return Automorphism(permutation, translation)


def power(element: Automorphism, exponent: int) -> Automorphism:
    result = IDENTITY
    for _ in range(exponent):
        result = compose(element, result)
    return result


def order(element: Automorphism) -> int:
    for exponent in range(1, 65):
        if power(element, exponent) == IDENTITY:
            return exponent
    raise AssertionError("element order exceeds ambient group exponent")


def image(code: frozenset[int], automorphism: Automorphism) -> frozenset[int]:
    return frozenset(automorphism(word) for word in code)


def all_cube_automorphisms() -> list[Automorphism]:
    return [
        Automorphism(permutation, translation)
        for permutation in itertools.permutations(range(DIMENSION))
        for translation in range(VERTEX_COUNT)
    ]


def action_orbits(
    points: set[int], group: frozenset[Automorphism]
) -> list[frozenset[int]]:
    remaining = set(points)
    orbits: list[frozenset[int]] = []
    while remaining:
        representative = min(remaining)
        orbit = frozenset(g(representative) for g in group)
        assert orbit <= remaining | set().union(*orbits)
        orbits.append(orbit)
        remaining -= orbit
    return orbits


def neighborhood(vertex: int) -> frozenset[int]:
    return frozenset(
        {vertex, *(vertex ^ (1 << coordinate) for coordinate in range(DIMENSION))}
    )


def signature(vertex: int) -> frozenset[int]:
    return QUADRATIC_CODE & neighborhood(vertex)


def main() -> None:
    ambient = all_cube_automorphisms()
    assert len(ambient) == 64 * 720 == 46_080

    stabilizer = frozenset(
        g for g in ambient if image(QUADRATIC_CODE, g) == QUADRATIC_CODE
    )
    assert len(stabilizer) == 32

    # In coordinate notation these maps are
    # r(x)=(x1+1,x5,x3,x6,x4+1,x2),
    # s(x)=(x1+1,x2,x3,x4+1,x6,x5),
    # k(x)=x+(0,0,1,0,1,1).
    r = Automorphism((2, 4, 1, 3, 0, 5), 0b100010)
    s = Automorphism((1, 0, 2, 3, 4, 5), 0b100100)
    k = Automorphism(IDENTITY_PERMUTATION, 0b001011)

    assert order(r) == 8
    assert order(s) == order(k) == 2
    assert compose(compose(s, r), s) == power(r, 7)
    assert compose(compose(k, r), k) == power(r, 5)
    assert compose(s, k) == compose(k, s)

    normal_forms = frozenset(
        compose(compose(power(r, i), power(s, j)), power(k, ell))
        for i in range(8)
        for j in range(2)
        for ell in range(2)
    )
    assert len(normal_forms) == 32
    assert normal_forms == stabilizer
    dihedral_subgroup = frozenset(
        compose(power(r, i), power(s, j)) for i in range(8) for j in range(2)
    )
    assert len(dihedral_subgroup) == 16

    translation_kernel = frozenset(
        g.translation
        for g in stabilizer
        if g.permutation == IDENTITY_PERMUTATION
    )
    assert translation_kernel == frozenset({0, 11, 23, 28})
    assert translation_kernel == frozenset(
        {0, k.translation, power(r, 4).translation, k.translation ^ power(r, 4).translation}
    )
    projection = {g.permutation for g in stabilizer}
    assert len(projection) == 8
    projected_r = Automorphism(r.permutation, 0)
    projected_s = Automorphism(s.permutation, 0)
    assert order(projected_r) == 4
    assert order(projected_s) == 2
    assert compose(compose(projected_s, projected_r), projected_s) == power(
        projected_r, 3
    )
    assert {
        compose(power(projected_r, i), power(projected_s, j)).permutation
        for i in range(4)
        for j in range(2)
    } == projection

    # The displayed coordinate permutation y=(x3,x2,x6,x5,x4,x1)
    # has bit permutation (3,2,1,5,4,0) and no translation.
    bridge = Automorphism((3, 2, 1, 5, 4, 0), 0)
    assert image(QUADRATIC_CODE, bridge) == CANONICAL_CODE
    all_bridges = [g for g in ambient if image(QUADRATIC_CODE, g) == CANONICAL_CODE]
    assert len(all_bridges) == 32

    complement = set(range(VERTEX_COUNT)) - set(QUADRATIC_CODE)
    code_orbits = action_orbits(set(QUADRATIC_CODE), stabilizer)
    complement_orbits = action_orbits(complement, stabilizer)
    assert [len(orbit) for orbit in code_orbits] == [16]
    assert sorted(len(orbit) for orbit in complement_orbits) == [16, 16, 16]
    signature_sizes = {
        min(orbit): frozenset(len(signature(vertex)) for vertex in orbit)
        for orbit in complement_orbits
    }
    assert sorted(next(iter(sizes)) for sizes in signature_sizes.values()) == [1, 2, 3]

    signatures = [signature(vertex) for vertex in sorted(complement)]
    assert all(signatures)
    assert len(set(signatures)) == 48
    assert Counter(map(len, signatures)) == Counter({1: 16, 2: 16, 3: 16})

    element_orders = Counter(order(g) for g in stabilizer)
    assert element_orders == Counter({1: 1, 2: 15, 4: 8, 8: 8})

    print("ambient cube automorphisms: 46080")
    print("stabilizer order: 32")
    print("presentation: <r,s,k | r^8=s^2=k^2=1, srs=r^-1, krk=r^5, sk=ks>")
    print("isomorphism: D_16 semidirect C_2 (D_16 has order 16)")
    print("element orders: 1:1 2:15 4:8 8:8")
    print("translation kernel: 000000 001011 010111 011100")
    print("coordinate-permutation projection order: 8 (dihedral)")
    print("code orbit size: 16")
    for orbit in sorted(complement_orbits, key=lambda item: len(signature(min(item)))):
        print(
            f"complement orbit representative {min(orbit):06b}: "
            f"size {len(orbit)}, signature size {len(signature(min(orbit)))}"
        )
    print("bridge to canonical code: y=(x3,x2,x6,x5,x4,x1)")
    print("verified: stabilizer presentation and four-orbit decomposition")


if __name__ == "__main__":
    main()
