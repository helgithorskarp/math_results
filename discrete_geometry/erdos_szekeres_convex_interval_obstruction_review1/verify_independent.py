#!/usr/bin/env python3
"""Independent set-level audit of the convex-interval blow-up theorem.

This checker does not import the target implementation.  Instead of checking
only binomial coefficients, it constructs the injection into the Boolean
lattice that is implicit in the proof, and verifies every individual image.
"""

from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
from math import comb
import platform


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


@lru_cache(maxsize=None)
def masks(size, weight):
    """All weight-``weight`` subsets of range(size), as exact bitmasks."""
    if weight < 0 or weight > size:
        return ()
    answer = []
    for chosen in combinations(range(size), weight):
        value = 0
        for bit in chosen:
            value |= 1 << bit
        answer.append(value)
    return tuple(answer)


def envelope(x):
    t = [x[0]]
    for value in x[1:]:
        t.append(max(value, t[-1] + 1))
    return tuple(t)


def profile_value(n, x, y):
    return (
        sum(comb(n, r) for r in range(x[0] + 1))
        + sum(comb(x[i] + y[i - 1], x[i]) for i in range(1, len(x)))
        + sum(comb(n, r) for r in range(y[-1] + 1))
    )


def convex_feasible(n, x, y):
    """Original active constraints with maximal ranks s[h,j]=j-h+1."""
    vertices = len(x) + 1
    for j in range(1, vertices):
        for h in range(j):
            if x[h] + y[j - 1] > n - (j - h):
                return False
        if j < vertices - 1 and x[j] + y[j - 1] > n + 1:
            return False
    return True


def numerical_hypothesis(n, x, y):
    """The target's local certificate, without any geometric premise."""
    t = envelope(x)
    if any(t[j - 1] + y[j - 1] > n - 1 for j in range(1, len(x) + 1)):
        return False
    if any(t[i] + y[i - 1] > n + 1 for i in range(1, len(x))):
        return False
    return True


def equality_shape(n, x, y):
    """The classified active equality profiles, including N=2."""
    if len(x) == 1:
        return x[0] + y[0] == n - 1
    for i in range(1, len(x)):
        jump = x[i] - x[i - 1]
        if jump not in (1, 2) or y[i - 1] != n + jump - 1 - x[i]:
            return False
    return x[-1] + y[-1] == n - 1


def boolean_injection(n, x, y):
    """Map every counted object to a distinct subset of an n-set.

    Interior objects are first raised from x_i-subsets of [x_i+y_i] to
    t_i-subsets of [t_i+y_i] by adjoining fixed new elements.  A one-level
    envelope step embeds directly in level t_i.  A longer step applies the
    literal Pascal bijection at element n, landing in levels t_i-1 and t_i.
    Endpoint objects use the lower levels and complements of the lower levels.
    """
    require(numerical_hypothesis(n, x, y), "certificate hypothesis")
    t = envelope(x)
    full = (1 << n) - 1
    images = []

    for r in range(x[0] + 1):
        images.extend(masks(n, r))

    for i in range(1, len(x)):
        old_size = x[i] + y[i - 1]
        raised_size = t[i] + y[i - 1]
        added = sum(1 << bit for bit in range(old_size, raised_size))
        jump = t[i] - t[i - 1]
        for source in masks(old_size, x[i]):
            raised = source | added
            require(raised.bit_count() == t[i], "raising weight")
            if jump == 1:
                require(raised_size <= n, "one-level universe")
                image = raised
                allowed = {t[i]}
            else:
                require(raised_size <= n + 1, "Pascal universe")
                image = raised & full
                allowed = {t[i] - 1, t[i]}
            require(image.bit_length() <= n, "image outside Boolean lattice")
            require(image.bit_count() in allowed, "wrong allocated level")
            require(t[i - 1] < image.bit_count() <= t[i], "wrong level block")
            images.append(image)

    for r in range(y[-1] + 1):
        images.extend(full ^ subset for subset in masks(n, r))

    expected = profile_value(n, x, y)
    require(len(images) == expected, "domain cardinality")
    require(len(set(images)) == expected, "injection collision")
    require(expected <= 1 << n, "Boolean-lattice bound")
    return frozenset(images)


def all_active_profiles(n, vertices):
    """Definition-level enumeration, with no envelope pruning."""
    width = vertices - 1
    for x in product(range(n), repeat=width):
        for y in product(range(n), repeat=width):
            yield x, y


def equality_count_formula(n, vertices):
    gaps = vertices - 2
    return sum(
        comb(gaps, twos) * (n - gaps - twos)
        for twos in range(gaps + 1)
        if n - gaps - twos > 0
    )


def generate_equality_shapes(n, vertices):
    gaps = vertices - 2
    for jumps in product((1, 2), repeat=gaps):
        total = sum(jumps)
        for first in range(n - total):
            x = [first]
            for jump in jumps:
                x.append(x[-1] + jump)
            y = [n + jumps[i - 1] - 1 - x[i] for i in range(1, len(x))]
            y.append(n - 1 - x[-1])
            yield tuple(x), tuple(y)


def seed_rank_feasible(n, x, y, ranks):
    """Full active cross-constraints for a supplied endpoint-rank matrix."""
    vertices = len(x) + 1
    for j in range(1, vertices):
        for h in range(j):
            if x[h] + y[j - 1] > n + 1 - ranks[h][j]:
                return False
        if j < vertices - 1 and x[j] + y[j - 1] > n + 1:
            return False
    return True


def update_digest(digest, *values):
    digest.update((repr(values) + "\n").encode("ascii"))


def main():
    digest = sha256()
    convex_profiles = 0
    numerical_profiles = 0
    injected_objects = 0
    convex_equalities = 0

    # Exhaust every convex-feasible active profile in a range large enough to
    # include nonmonotone envelopes, one/two/long jumps, and all boundaries.
    for n in range(1, 6):
        for vertices in range(2, min(n + 1, 5) + 1):
            for x, y in all_active_profiles(n, vertices):
                if not convex_feasible(n, x, y):
                    continue
                require(numerical_hypothesis(n, x, y), "convex implies certificate")
                images = boolean_injection(n, x, y)
                value = profile_value(n, x, y)
                equal = value == 1 << n
                require(equal == equality_shape(n, x, y), "equality classification")
                require(equal == (len(images) == 1 << n), "injection surjectivity")
                convex_profiles += 1
                convex_equalities += int(equal)
                injected_objects += value
                update_digest(digest, "convex", n, vertices, x, y, value, equal)

    # Audit the purely numerical certificate on every bounded profile, even
    # when it is not feasible for a convex seed.
    for n in range(1, 6):
        for vertices in range(2, min(4, n + 2) + 1):
            for x, y in all_active_profiles(n, vertices):
                if not numerical_hypothesis(n, x, y):
                    continue
                images = boolean_injection(n, x, y)
                value = profile_value(n, x, y)
                require((value == 1 << n) == equality_shape(n, x, y),
                        "numerical equality classification")
                numerical_profiles += 1
                injected_objects += value
                update_digest(digest, "numeric", n, vertices, x, y, value, len(images))

    # Proved strengthening: every classified equality shape is feasible for
    # the worst possible endpoint ranks, hence for every seed, and its count
    # has the displayed closed formula.
    universal_shapes = 0
    for n in range(1, 13):
        for vertices in range(2, n + 2):
            generated = list(generate_equality_shapes(n, vertices))
            require(len(generated) == len(set(generated)), "duplicate shape")
            require(len(generated) == equality_count_formula(n, vertices),
                    "closed equality count")
            for x, y in generated:
                require(equality_shape(n, x, y), "generated shape")
                require(convex_feasible(n, x, y), "universal worst-rank feasibility")
                require(len(boolean_injection(n, x, y)) == 1 << n,
                        "universal profile is extremal")
                universal_shapes += 1
                update_digest(digest, "universal", n, vertices, x, y)

    # Small adversarial controls.
    require(boolean_injection(1, (0,), (0,)) == frozenset((0, 1)),
            "N=2,n=1 boundary")
    x, y = (2, 0), (0, 0)
    require(convex_feasible(4, x, y) and envelope(x) == (2, 3),
            "nonmonotone envelope control")
    boolean_injection(4, x, y)
    x, y = (0, 3), (3, 0)
    require(convex_feasible(5, x, y) and envelope(x) == (0, 3),
            "long-jump control")
    boolean_injection(5, x, y)

    # Smallest scope warning: a nonconvex four-point endpoint-rank table can
    # have B=2^n outside both the certificate and the convex classification.
    ranks = (
        (0, 2, 3, 3),
        (0, 0, 2, 3),
        (0, 0, 0, 2),
        (0, 0, 0, 0),
    )
    x = y = (0, 0, 0)
    require(seed_rank_feasible(2, x, y, ranks), "nonconvex scope feasibility")
    require(profile_value(2, x, y) == 4, "nonconvex extra equality")
    require(not numerical_hypothesis(2, x, y), "scope must evade certificate")
    require(not equality_shape(2, x, y), "scope must evade convex classification")

    print("VERIFIED: independent Boolean-lattice injection")
    print(f"python={platform.python_version()}")
    print(f"convex_profiles={convex_profiles}")
    print(f"numerical_certificate_profiles={numerical_profiles}")
    print(f"convex_equality_profiles={convex_equalities}")
    print(f"universal_equality_shapes={universal_shapes}")
    print(f"injected_objects={injected_objects}")
    print(f"evidence_sha256={digest.hexdigest()}")


if __name__ == "__main__":
    main()
