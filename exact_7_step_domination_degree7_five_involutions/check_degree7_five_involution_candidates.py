#!/usr/bin/env python3
"""Independent checker for the degree-seven five-involution obstruction."""

from __future__ import annotations

import argparse
import collections
import itertools
from dataclasses import dataclass
from functools import cached_property, lru_cache
from pathlib import Path

RADIUS = 7
MAXIMUM_ORDER = 6 * 64


def reduced_basis(vectors: tuple[int, ...]) -> tuple[int, ...]:
    """Canonical reduced binary row basis, with pivots from high to low."""
    rows = list(vectors)
    pivot = 0
    for bit in range(4, -1, -1):
        selected = next(
            (index for index in range(pivot, len(rows)) if rows[index] >> bit & 1),
            None,
        )
        if selected is None:
            continue
        rows[pivot], rows[selected] = rows[selected], rows[pivot]
        for index in range(len(rows)):
            if index != pivot and rows[index] >> bit & 1:
                rows[index] ^= rows[pivot]
        pivot += 1
    return tuple(rows[:pivot])


def binary_subspaces() -> tuple[tuple[int, ...], ...]:
    bases: set[tuple[int, ...]] = {()}
    for size in range(1, 6):
        for vectors in itertools.combinations(range(1, 32), size):
            basis = reduced_basis(vectors)
            if len(basis) == size:
                bases.add(basis)
    return tuple(sorted(bases, key=lambda basis: (len(basis), basis)))


def span(basis: tuple[int, ...]) -> frozenset[int]:
    result = {0}
    for vector in basis:
        result |= {value ^ vector for value in result}
    return frozenset(result)


def valid_kernel(kernel: frozenset[int]) -> bool:
    images = (1, 2, 4, 8, 16)
    return all(value not in kernel for value in images) and all(
        left ^ right not in kernel
        for left, right in itertools.combinations(images, 2)
    )


@dataclass(frozen=True)
class BinaryQuotient:
    kernel: frozenset[int]

    @cached_property
    def representative(self) -> tuple[int, ...]:
        return tuple(min(value ^ element for element in self.kernel)
                     for value in range(32))

    @cached_property
    def representatives(self) -> tuple[int, ...]:
        return tuple(value for value in range(32)
                     if self.representative[value] == value)

    @cached_property
    def index(self) -> tuple[int, ...]:
        by_representative = {
            value: index for index, value in enumerate(self.representatives)
        }
        return tuple(by_representative[self.representative[value]]
                     for value in range(32))

    @property
    def order(self) -> int:
        return len(self.representatives)

    def coset(self, vector: int) -> int:
        return self.index[vector]

    def add(self, left: int, right: int) -> int:
        return self.coset(self.representatives[left] ^ self.representatives[right])


@dataclass(frozen=True)
class Model:
    quotient: BinaryQuotient
    generator_order: int
    intersection_vector: int | None

    @cached_property
    def intersection_coset(self) -> int | None:
        if self.intersection_vector is None:
            return None
        result = self.quotient.coset(self.intersection_vector)
        if result == 0:
            raise ValueError("intersection vector lies in the relation kernel")
        return result

    @property
    def cyclic_size(self) -> int:
        return (
            self.generator_order
            if self.intersection_vector is None
            else self.generator_order // 2
        )

    @property
    def order(self) -> int:
        return self.cyclic_size * self.quotient.order

    def encode(self, cyclic: int, binary: int) -> int:
        return cyclic * self.quotient.order + binary

    def decode(self, element: int) -> tuple[int, int]:
        return divmod(element, self.quotient.order)

    def add(self, left: int, right: int) -> int:
        a, x = self.decode(left)
        b, y = self.decode(right)
        cyclic = a + b
        binary = self.quotient.add(x, y)
        if cyclic >= self.cyclic_size:
            cyclic -= self.cyclic_size
            if self.intersection_coset is not None:
                binary = self.quotient.add(binary, self.intersection_coset)
        return self.encode(cyclic, binary)

    def inverse(self, element: int) -> int:
        cyclic, binary = self.decode(element)
        if cyclic == 0:
            return element
        if self.intersection_coset is not None:
            binary = self.quotient.add(binary, self.intersection_coset)
        return self.encode(self.cyclic_size - cyclic, binary)

    def subtract(self, left: int, right: int) -> int:
        return self.add(left, self.inverse(right))

    @cached_property
    def steps(self) -> tuple[int, ...]:
        generator = self.encode(1, 0)
        result = {
            generator,
            self.inverse(generator),
            *(self.encode(0, self.quotient.coset(1 << index))
              for index in range(5)),
        }
        if len(result) != 7 or 0 in result:
            raise ValueError("connection set is not simple degree seven")
        return tuple(sorted(result))

    def sphere(self) -> tuple[int, ...]:
        distance = [-1] * self.order
        distance[0] = 0
        queue = collections.deque([0])
        while queue:
            element = queue.popleft()
            for step in self.steps:
                neighbour = self.add(element, step)
                if distance[neighbour] == -1:
                    distance[neighbour] = distance[element] + 1
                    queue.append(neighbour)
        if -1 in distance:
            raise AssertionError("displayed generators did not generate the model")
        return tuple(element for element, value in enumerate(distance)
                     if value == RADIUS)


def kernel_mask(kernel: frozenset[int]) -> int:
    return sum(1 << value for value in kernel)


def all_models() -> tuple[Model, ...]:
    result: list[Model] = []
    for basis in binary_subspaces():
        kernel = span(basis)
        if not valid_kernel(kernel):
            continue
        quotient = BinaryQuotient(kernel)
        for generator_order in range(3, MAXIMUM_ORDER // quotient.order + 1):
            model = Model(quotient, generator_order, None)
            if model.order % 4 == 0 or model.order % 6 == 0:
                result.append(model)
        for intersection in quotient.representatives[1:]:
            maximum_generator_order = 2 * MAXIMUM_ORDER // quotient.order
            for generator_order in range(4, maximum_generator_order + 1, 2):
                model = Model(quotient, generator_order, intersection)
                if model.order % 4 == 0 or model.order % 6 == 0:
                    result.append(model)
    return tuple(result)


def descriptor(model: Model, center_count: int,
               sphere: tuple[int, ...]) -> tuple[int, ...]:
    intersection = -1 if model.intersection_vector is None else model.intersection_vector
    return (
        center_count,
        model.generator_order,
        kernel_mask(model.quotient.kernel),
        intersection,
        len(sphere),
    )


def permute_vector(vector: int, permutation: tuple[int, ...]) -> int:
    result = 0
    for index in range(5):
        if vector >> index & 1:
            result |= 1 << permutation[index]
    return result


def permutation_canonical_descriptor(key: tuple[int, ...]) -> tuple[int, ...]:
    center_count, generator_order, encoded_kernel, intersection, sphere_size = key
    kernel = frozenset(value for value in range(32)
                       if encoded_kernel >> value & 1)
    images = []
    for permutation in itertools.permutations(range(5)):
        transformed_kernel = frozenset(
            permute_vector(value, permutation) for value in kernel
        )
        transformed_intersection = permute_vector(intersection, permutation)
        transformed_intersection = min(
            transformed_intersection ^ value for value in transformed_kernel
        )
        images.append((
            center_count,
            generator_order,
            kernel_mask(transformed_kernel),
            transformed_intersection,
            sphere_size,
        ))
    return min(images)


def has_translate_tiling(model: Model, sphere: tuple[int, ...],
                         center_count: int) -> bool:
    if center_count * len(sphere) != model.order:
        return False
    full = (1 << model.order) - 1

    @lru_cache(maxsize=None)
    def translated(shift: int) -> int:
        result = 0
        for element in sphere:
            result |= 1 << model.add(element, shift)
        return result

    @lru_cache(maxsize=None)
    def search(covered: int, remaining: int) -> bool:
        if remaining == 0:
            return covered == full
        uncovered = full ^ covered
        if uncovered == 0:
            return False
        first = (uncovered & -uncovered).bit_length() - 1
        tried: set[int] = set()
        for sphere_element in sphere:
            shift = model.subtract(first, sphere_element)
            if shift in tried:
                continue
            tried.add(shift)
            candidate = translated(shift)
            if covered & candidate == 0 and search(
                covered | candidate, remaining - 1
            ):
                return True
        return False

    return search(translated(0), center_count - 1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate_file", type=Path)
    args = parser.parse_args()

    subspaces = binary_subspaces()
    if len(subspaces) != 374:
        raise AssertionError("unexpected binary-subspace count")
    valid = tuple(basis for basis in subspaces if valid_kernel(span(basis)))
    if len(valid) != 32:
        raise AssertionError("unexpected valid-kernel count")

    emitted = {
        tuple(map(int, line.split()))
        for line in args.candidate_file.read_text(encoding="utf-8").splitlines()
    }
    if len(emitted) != len(
        args.candidate_file.read_text(encoding="utf-8").splitlines()
    ):
        raise AssertionError("duplicate candidate descriptor")

    models = all_models()
    split_models = sum(model.intersection_vector is None for model in models)
    nonsplit_models = len(models) - split_models
    rescanned: dict[tuple[int, ...], tuple[Model, tuple[int, ...]]] = {}
    for model in models:
        sphere = model.sphere()
        for center_count in (4, 6):
            if center_count * len(sphere) == model.order:
                key = descriptor(model, center_count, sphere)
                if key in rescanned:
                    raise AssertionError("duplicate model descriptor")
                rescanned[key] = (model, sphere)
    if set(rescanned) != emitted:
        raise AssertionError("independent BFS rescan differs from candidate file")

    permutation_orbits = {
        permutation_canonical_descriptor(key) for key in rescanned
    }
    fiber_profiles = {
        tuple(
            sum(model.decode(element)[0] == residue for element in sphere)
            for residue in range(model.cyclic_size)
        )
        for model, sphere in rescanned.values()
    }

    four_candidates = 0
    six_candidates = 0
    four_tilings = 0
    six_tilings = 0
    for key, (model, sphere) in rescanned.items():
        center_count = key[0]
        tiling = has_translate_tiling(model, sphere, center_count)
        if center_count == 4:
            four_candidates += 1
            four_tilings += int(tiling)
        else:
            six_candidates += 1
            six_tilings += int(tiling)

    print(f"binary_subspaces={len(subspaces)}")
    print(f"valid_relation_kernels={len(valid)}")
    print(f"split_models={split_models}")
    print(f"nonsplit_models={nonsplit_models}")
    print(f"candidate_descriptors={len(rescanned)}")
    print(f"candidate_permutation_orbits={len(permutation_orbits)}")
    print(f"candidate_cyclic_fiber_profiles={len(fiber_profiles)}")
    print(f"four_center_candidates_checked={four_candidates}")
    print(f"six_center_candidates_checked={six_candidates}")
    print(f"four_center_tilings={four_tilings}")
    print(f"six_center_tilings={six_tilings}")

    expected = (1052, 10796, 5, 2, 0, 61, 0, 0)
    actual = (
        split_models,
        nonsplit_models,
        len(permutation_orbits),
        len(fiber_profiles),
        four_candidates,
        six_candidates,
        four_tilings,
        six_tilings,
    )
    if actual != expected:
        raise AssertionError(f"unexpected checker result: {actual}")


if __name__ == "__main__":
    main()
