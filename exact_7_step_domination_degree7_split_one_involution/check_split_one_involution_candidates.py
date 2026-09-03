#!/usr/bin/env python3
"""Definition-level checker for split one-involution exact-7 candidates."""

from __future__ import annotations

import argparse
import collections
import functools
import multiprocessing
from dataclasses import dataclass
from pathlib import Path

RADIUS = 7
SHELL_BOUND = 344
MAXIMUM_GROUP_ORDER = 6 * SHELL_BOUND
MAXIMUM_BASE_ORDER = MAXIMUM_GROUP_ORDER // 2


@dataclass(frozen=True)
class Model:
    """B x C2 for B=Z^3/L in column-HNF coordinates."""

    a: int
    b: int
    c: int
    x: int
    y: int
    z: int

    def __post_init__(self) -> None:
        if not (
            self.a > 0
            and self.b > 0
            and self.c > 0
            and 0 <= self.x < self.a
            and 0 <= self.y < self.a
            and 0 <= self.z < self.b
        ):
            raise ValueError("invalid column HNF")

    @property
    def base_order(self) -> int:
        return self.a * self.b * self.c

    @property
    def order(self) -> int:
        return 2 * self.base_order

    def base_encode(self, value: tuple[int, int, int]) -> int:
        return value[0] + self.a * (value[1] + self.b * value[2])

    def base_decode(self, encoded: int) -> tuple[int, int, int]:
        encoded, first = divmod(encoded, self.a)
        third, second = divmod(encoded, self.b)
        return first, second, third

    def base_reduce(self, value: tuple[int, int, int]) -> int:
        first, second, third = value
        q3, third = divmod(third, self.c)
        first -= q3 * self.y
        second -= q3 * self.z
        q2, second = divmod(second, self.b)
        first -= q2 * self.x
        first %= self.a
        return self.base_encode((first, second, third))

    def encode(self, base: int, parity: int) -> int:
        return 2 * base + parity

    def decode(self, element: int) -> tuple[int, int]:
        return divmod(element, 2)

    def image(self, value: tuple[int, int, int], parity: int = 0) -> int:
        return self.encode(self.base_reduce(value), parity & 1)

    def add(self, left: int, right: int) -> int:
        left_base, left_parity = self.decode(left)
        right_base, right_parity = self.decode(right)
        u = self.base_decode(left_base)
        v = self.base_decode(right_base)
        base = self.base_reduce(tuple(u[i] + v[i] for i in range(3)))
        return self.encode(base, left_parity ^ right_parity)

    def inverse(self, element: int) -> int:
        base, parity = self.decode(element)
        value = self.base_decode(base)
        return self.image(tuple(-entry for entry in value), parity)

    def subtract(self, left: int, right: int) -> int:
        return self.add(left, self.inverse(right))

    @functools.cached_property
    def steps(self) -> tuple[int, ...]:
        raw = []
        for coordinate in range(3):
            for sign in (-1, 1):
                value = [0, 0, 0]
                value[coordinate] = sign
                raw.append(self.image(tuple(value)))
        raw.append(self.image((0, 0, 0), 1))
        return tuple(sorted(set(raw)))

    @property
    def is_simple_degree_seven(self) -> bool:
        return len(self.steps) == 7 and self.steps[0] != 0

    def sphere_by_bfs(self) -> tuple[int, ...]:
        if not self.is_simple_degree_seven:
            raise ValueError("connection set is not simple degree seven")
        distance = [-1] * self.order
        distance[0] = 0
        queue = collections.deque([0])
        while queue:
            current = queue.popleft()
            for step in self.steps:
                neighbour = self.add(current, step)
                if distance[neighbour] >= 0:
                    continue
                distance[neighbour] = distance[current] + 1
                queue.append(neighbour)
        if -1 in distance:
            raise AssertionError("marked generators did not generate the model")
        return tuple(i for i, distance_i in enumerate(distance) if distance_i == RADIUS)


def hnf_count(order: int) -> int:
    result = 0
    for a in range(1, order + 1):
        if order % a:
            continue
        quotient = order // a
        for b in range(1, quotient + 1):
            if quotient % b == 0:
                result += a * a * b
    return result


def eligible_hnf_count() -> int:
    return sum(
        hnf_count(order)
        for order in range(1, MAXIMUM_BASE_ORDER + 1)
        if order % 2 == 0 or order % 3 == 0
    )


def euler_phi(number: int) -> int:
    result = number
    prime = 2
    while prime * prime <= number:
        if number % prime == 0:
            result = result // prime * (prime - 1)
            while number % prime == 0:
                number //= prime
        prime += 1
    if number > 1:
        result = result // number * (number - 1)
    return result


def jordan_totient_three(number: int) -> int:
    result = number**3
    remainder = number
    prime = 2
    while prime * prime <= remainder:
        if remainder % prime == 0:
            result = result // prime**3 * (prime**3 - 1)
            while remainder % prime == 0:
                remainder //= prime
        prime += 1
    if remainder > 1:
        result = result // remainder**3 * (remainder**3 - 1)
    return result


def eligible_cyclic_hnf_count() -> int:
    result = 0
    for order in range(1, MAXIMUM_BASE_ORDER + 1):
        if order % 2 and order % 3:
            continue
        result += jordan_totient_three(order) // euler_phi(order)
    return result


def is_cyclic(model: Model) -> bool:
    minors = (
        model.a * model.b,
        model.a * model.z,
        model.x * model.z - model.b * model.y,
        model.a * model.c,
        model.x * model.c,
        model.b * model.c,
    )
    from math import gcd

    divisor = 0
    for minor in minors:
        divisor = gcd(divisor, abs(minor))
    return divisor == 1


def parse(line: str) -> tuple[int, int, Model, int]:
    values = tuple(map(int, line.split()))
    if len(values) != 9:
        raise ValueError(f"candidate descriptor has {len(values)} fields, not 9")
    centers, group_order, a, b, c, x, y, z, sphere_size = values
    if centers not in (4, 6):
        raise ValueError("center count must be four or six")
    return centers, group_order, Model(a, b, c, x, y, z), sphere_size


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
        for element in sphere:
            shift = model.subtract(first, element)
            if shift in tried:
                continue
            tried.add(shift)
            candidate = translated(shift)
            if not covered & candidate and search(covered | candidate, remaining - 1):
                return True
        return False

    return search(translated(0), center_count - 1)


def check_descriptor(values: tuple[int, ...]) -> tuple[int, int]:
    centers, group_order, model, stated_sphere_size = parse(
        " ".join(map(str, values))
    )
    if group_order != model.order or group_order > MAXIMUM_GROUP_ORDER:
        raise AssertionError("candidate group order is invalid")
    if model.base_order % 2 and model.base_order % 3:
        raise AssertionError("candidate cannot satisfy the divisibility condition")
    if not model.is_simple_degree_seven:
        raise AssertionError("candidate connection set is not simple degree seven")
    if is_cyclic(model):
        raise AssertionError("noncyclic candidate file contains a cyclic quotient")
    sphere = model.sphere_by_bfs()
    if len(sphere) != stated_sphere_size:
        raise AssertionError("BFS sphere size disagrees with descriptor")
    if centers * len(sphere) != model.order:
        raise AssertionError("candidate fails the translate-partition count")
    return centers, int(has_translate_tiling(model, sphere, centers))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate_file", type=Path, nargs="+")
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--progress-every", type=int, default=1000)
    args = parser.parse_args()

    descriptors = []
    for path in args.candidate_file:
        descriptors.extend(
            tuple(map(int, line.split()))
            for line in path.read_text(encoding="utf-8").splitlines()
        )
    if len(set(descriptors)) != len(descriptors):
        raise AssertionError("candidate files contain duplicate descriptors")

    counts = {4: 0, 6: 0}
    tilings = {4: 0, 6: 0}
    if args.jobs == 1:
        verdicts = map(check_descriptor, descriptors)
        pool = None
    else:
        pool = multiprocessing.get_context("spawn").Pool(args.jobs)
        verdicts = pool.imap(check_descriptor, descriptors, chunksize=10)
    try:
        for completed, (centers, tiling) in enumerate(verdicts, 1):
            counts[centers] += 1
            tilings[centers] += tiling
            if args.progress_every and completed % args.progress_every == 0:
                print(f"candidate_progress={completed}/{len(descriptors)}", flush=True)
    finally:
        if pool is not None:
            pool.close()
            pool.join()

    print(f"radius={RADIUS}")
    print(f"maximum_group_order={MAXIMUM_GROUP_ORDER}")
    all_hnfs = eligible_hnf_count()
    cyclic_hnfs = eligible_cyclic_hnf_count()
    print(f"eligible_hnfs={all_hnfs}")
    print(f"cyclic_quotient_hnfs={cyclic_hnfs}")
    print(f"noncyclic_quotient_hnfs={all_hnfs - cyclic_hnfs}")
    print(f"candidate_hnfs={len(descriptors)}")
    print(f"four_center_candidates_checked={counts[4]}")
    print(f"six_center_candidates_checked={counts[6]}")
    print(f"four_center_tilings={tilings[4]}")
    print(f"six_center_tilings={tilings[6]}")


if __name__ == "__main__":
    main()
