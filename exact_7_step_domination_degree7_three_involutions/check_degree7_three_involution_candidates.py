#!/usr/bin/env python3
"""Independent checker for the degree-seven three-involution obstruction."""

from __future__ import annotations

import argparse
import collections
import functools
import multiprocessing
from dataclasses import dataclass
from pathlib import Path

RADIUS = 7
SHELL_BOUND = 176
MAXIMUM_ORDER = 6 * SHELL_BOUND


@dataclass(frozen=True)
class BinaryQuotient:
    kernel_code: int

    def __post_init__(self) -> None:
        if self.kernel_code not in (0, 7):
            raise ValueError("the only valid kernels are 0 and <111>")

    @property
    def order(self) -> int:
        return 8 if self.kernel_code == 0 else 4

    def coset(self, vector: int) -> int:
        vector &= 7
        return vector if self.kernel_code == 0 else min(vector, vector ^ 7)

    def add(self, left: int, right: int) -> int:
        return self.coset(left ^ right)


@dataclass(frozen=True)
class Model:
    quotient: BinaryQuotient
    a: int
    b: int
    x: int
    phi_first: int
    phi_second: int

    def __post_init__(self) -> None:
        if not (self.a > 0 and self.b > 0 and 0 <= self.x < self.a):
            raise ValueError("invalid column HNF")
        if not (
            0 <= self.phi_first < self.quotient.order
            and 0 <= self.phi_second < self.quotient.order
        ):
            raise ValueError("invalid gluing homomorphism")

    @property
    def order(self) -> int:
        return self.a * self.b * self.quotient.order

    def encode(self, first: int, second: int, binary: int) -> int:
        return (second * self.a + first) * self.quotient.order + binary

    def decode(self, element: int) -> tuple[int, int, int]:
        lattice, binary = divmod(element, self.quotient.order)
        second, first = divmod(lattice, self.a)
        return first, second, binary

    def reduce(self, first: int, second: int, binary: int) -> int:
        second_quotient, reduced_second = divmod(second, self.b)
        first -= second_quotient * self.x
        if second_quotient & 1:
            binary = self.quotient.add(binary, self.phi_second)
        first_quotient, reduced_first = divmod(first, self.a)
        if first_quotient & 1:
            binary = self.quotient.add(binary, self.phi_first)
        return self.encode(reduced_first, reduced_second, binary)

    def image(self, first: int, second: int, binary_vector: int) -> int:
        return self.reduce(first, second, self.quotient.coset(binary_vector))

    def add(self, left: int, right: int) -> int:
        a_first, a_second, a_binary = self.decode(left)
        b_first, b_second, b_binary = self.decode(right)
        return self.reduce(
            a_first + b_first,
            a_second + b_second,
            self.quotient.add(a_binary, b_binary),
        )

    def inverse(self, element: int) -> int:
        first, second, binary = self.decode(element)
        return self.reduce(-first, -second, binary)

    def subtract(self, left: int, right: int) -> int:
        return self.add(left, self.inverse(right))

    @functools.cached_property
    def steps(self) -> tuple[int, ...]:
        first = self.image(1, 0, 0)
        second = self.image(0, 1, 0)
        return tuple(
            sorted(
                {
                    first,
                    self.inverse(first),
                    second,
                    self.inverse(second),
                    self.image(0, 0, 1),
                    self.image(0, 0, 2),
                    self.image(0, 0, 4),
                }
            )
        )

    @property
    def is_simple_degree_seven(self) -> bool:
        return len(self.steps) == 7 and self.steps[0] != 0

    def sphere_by_bfs(self) -> tuple[int, ...]:
        if not self.is_simple_degree_seven:
            raise ValueError("sphere requested for nonsimple connection set")
        distance = [-1] * self.order
        distance[0] = 0
        queue = collections.deque([0])
        while queue:
            element = queue.popleft()
            for step in self.steps:
                neighbour = self.add(element, step)
                if distance[neighbour] != -1:
                    continue
                distance[neighbour] = distance[element] + 1
                queue.append(neighbour)
        if -1 in distance:
            raise AssertionError("marked generators did not generate quotient")
        return tuple(
            element for element, value in enumerate(distance) if value == RADIUS
        )


def divisor_sum(number: int) -> int:
    return sum(divisor for divisor in range(1, number + 1) if number % divisor == 0)


def universe_count(quotient_order: int) -> int:
    maximum_lattice_index = MAXIMUM_ORDER // quotient_order
    return quotient_order**2 * sum(
        divisor_sum(index) for index in range(1, maximum_lattice_index + 1)
    )


def all_models(kernel_code: int):
    quotient = BinaryQuotient(kernel_code)
    maximum_lattice_index = MAXIMUM_ORDER // quotient.order
    for lattice_index in range(1, maximum_lattice_index + 1):
        for a in range(1, lattice_index + 1):
            if lattice_index % a:
                continue
            b = lattice_index // a
            for x in range(a):
                for phi_first in range(quotient.order):
                    for phi_second in range(quotient.order):
                        yield Model(
                            quotient, a, b, x, phi_first, phi_second
                        )


def descriptor(model: Model, center_count: int, sphere_size: int) -> tuple[int, ...]:
    return (
        center_count,
        model.quotient.kernel_code,
        model.a,
        model.b,
        model.x,
        model.phi_first,
        model.phi_second,
        sphere_size,
    )


def model_from_descriptor(values: tuple[int, ...]) -> tuple[Model, int, int]:
    if len(values) != 8:
        raise ValueError(f"candidate descriptor has {len(values)} fields, not 8")
    center_count, kernel, a, b, x, phi_first, phi_second, sphere_size = values
    if center_count not in (4, 6):
        raise ValueError("center count must be four or six")
    model = Model(BinaryQuotient(kernel), a, b, x, phi_first, phi_second)
    return model, center_count, sphere_size


def has_translate_tiling(
    model: Model, sphere: tuple[int, ...], center_count: int
) -> bool:
    if center_count * len(sphere) != model.order:
        return False
    full = (1 << model.order) - 1

    @functools.lru_cache(maxsize=None)
    def translated(shift: int) -> int:
        result = 0
        for element in sphere:
            result |= 1 << model.add(element, shift)
        return result

    @functools.lru_cache(maxsize=None)
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


def check_descriptor(values: tuple[int, ...]) -> tuple[int, int, int]:
    """Check one emitted model directly and return its exact verdict."""
    model, center_count, stated_sphere_size = model_from_descriptor(values)
    if model.order > MAXIMUM_ORDER:
        raise AssertionError("candidate exceeds proved order bound")
    if not model.is_simple_degree_seven:
        raise AssertionError("candidate connection set is not simple degree seven")
    sphere = model.sphere_by_bfs()
    if len(sphere) != stated_sphere_size:
        raise AssertionError("BFS sphere size disagrees with descriptor")
    if center_count * len(sphere) != model.order:
        raise AssertionError("candidate fails translate-partition count")
    tiling = has_translate_tiling(model, sphere, center_count)
    return model.quotient.kernel_code, center_count, int(tiling)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate_file", type=Path)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--progress-every", type=int, default=1000)
    args = parser.parse_args()
    if args.jobs < 1:
        raise ValueError("--jobs must be positive")
    if args.progress_every < 0:
        raise ValueError("--progress-every must be nonnegative")

    lines = args.candidate_file.read_text(encoding="utf-8").splitlines()
    descriptors = tuple(tuple(map(int, line.split())) for line in lines)
    if len(set(descriptors)) != len(descriptors):
        raise AssertionError("candidate file contains duplicate descriptors")

    expected_universe = {0: universe_count(8), 7: universe_count(4)}
    simple_counts: dict[int, int] = {}
    for kernel in (0, 7):
        models = all_models(kernel)
        scanned = 0
        simple = 0
        for model in models:
            scanned += 1
            simple += int(model.is_simple_degree_seven)
        if scanned != expected_universe[kernel]:
            raise AssertionError("model scan disagrees with divisor-sum universe")
        simple_counts[kernel] = simple

    checked_counts = {(0, 4): 0, (0, 6): 0, (7, 4): 0, (7, 6): 0}
    tiling_counts = {(0, 4): 0, (0, 6): 0, (7, 4): 0, (7, 6): 0}
    if args.jobs == 1:
        verdicts = map(check_descriptor, descriptors)
        pool = None
    else:
        context = multiprocessing.get_context("spawn")
        pool = context.Pool(args.jobs)
        verdicts = pool.imap(check_descriptor, descriptors, chunksize=10)
    try:
        for completed, (kernel, center_count, tiling) in enumerate(verdicts, 1):
            key = (kernel, center_count)
            checked_counts[key] += 1
            tiling_counts[key] += tiling
            if args.progress_every and completed % args.progress_every == 0:
                print(f"candidate_progress={completed}/{len(descriptors)}", flush=True)
    finally:
        if pool is not None:
            pool.close()
            pool.join()

    print(f"radius={RADIUS}")
    print(f"maximum_group_order={MAXIMUM_ORDER}")
    for kernel in (0, 7):
        print(
            f"kernel={kernel} marked_models={expected_universe[kernel]} "
            f"degree_seven_models={simple_counts[kernel]} "
            f"four_candidates_checked={checked_counts[kernel, 4]} "
            f"six_candidates_checked={checked_counts[kernel, 6]} "
            f"four_tilings={tiling_counts[kernel, 4]} "
            f"six_tilings={tiling_counts[kernel, 6]}"
        )
    print(f"candidate_descriptors={len(descriptors)}")

    expected = {
        0: (923584, 902571, 354, 16312, 0, 0),
        7: (920400, 907767, 33, 4226, 0, 0),
    }
    actual = {
        kernel: (
            expected_universe[kernel],
            simple_counts[kernel],
            checked_counts[kernel, 4],
            checked_counts[kernel, 6],
            tiling_counts[kernel, 4],
            tiling_counts[kernel, 6],
        )
        for kernel in (0, 7)
    }
    if actual != expected:
        raise AssertionError(f"unexpected checked result: {actual!r}")


if __name__ == "__main__":
    main()
