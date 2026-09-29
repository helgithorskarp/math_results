#!/usr/bin/env python3
"""Exact small controls for the residual-multiset reduction (stdlib only)."""

from collections import deque
from fractions import Fraction
from hashlib import sha256
from itertools import product
from math import comb, gcd, lcm
from pathlib import Path
import json
import sys


class IncompleteSearch(RuntimeError):
    """A resource limit is not a mathematical nonexistence result."""


def divisors(n):
    if not isinstance(n, int) or n < 1:
        raise ValueError("positive integer required")
    return tuple(d for d in range(1, n + 1) if n % d == 0)


def check_parameters(p, cofactor, minimum):
    if p < 2 or any(p % d == 0 for d in range(2, p)):
        raise ValueError("p must be prime")
    if cofactor < 1 or gcd(p, cofactor) != 1 or minimum < 2:
        raise ValueError("invalid cofactor or minimum")


def canonical(masks):
    return tuple(sorted(mask for mask in masks if mask))


def rotation_orbit(mask, cofactor):
    all_bits = (1 << cofactor) - 1
    return min(((mask << t) | (mask >> (cofactor - t))) & all_bits
               for t in range(cofactor))


def rotated_state(state, cofactor):
    return canonical(rotation_orbit(u, cofactor) for u in state)


def tree_subset_type(mask, q, depth):
    if depth == 0:
        return bool(mask)
    children = []
    for r in range(q):
        child = sum(((mask >> (r + q * y)) & 1) << y for y in range(q**(depth - 1)))
        children.append(tree_subset_type(child, q, depth - 1))
    return tuple(sorted(children))


def masks_for(cofactor, d):
    return tuple(sum(1 << y for y in range(b, cofactor, d)) for b in range(d))


def place_layer(state, cofactor, ds, width=None):
    """Use each d at most once on one currently active, anonymous fiber."""
    ds = tuple(ds)
    # Even concentrating all available classes cannot empty any member here.
    if width is not None and len(state) > width:
        total_points = sum(cofactor // d for d in ds)
        if all(u.bit_count() > total_points for u in state):
            return set()
    states = {canonical(state)}
    for offset, d in enumerate(ds):
        residue_masks = masks_for(cofactor, d)
        following = set()
        for current in states:
            # Each remaining resource can empty at most one member.
            if width is not None and len(current) - (len(ds) - offset) > width:
                continue
            following.add(current)  # omit this modulus
            for i, u in enumerate(current):
                if i and u == current[i - 1]:
                    continue  # interchangeable equal members
                for mask in residue_masks:
                    v = u & ~mask
                    if v == u:
                        continue  # already represented by omission
                    following.add(canonical(current[:i] + (v,) + current[i + 1:]))
        states = following
    if width is not None:
        states = {s for s in states if len(s) <= width}
    return states


def transition(state, p, cofactor, ds, width=None):
    children = canonical(u for u in state for _ in range(p))
    return place_layer(children, cofactor, ds, width)


def initial_states(p, cofactor, minimum, depth, prune=True):
    check_parameters(p, cofactor, minimum)
    ds = divisors(cofactor)
    width = (len(ds) - 1) // (p - 1) if prune else None
    allowed = tuple(d for d in ds if d >= minimum)
    states = place_layer(((1 << cofactor) - 1,), cofactor, allowed, width)
    for e in range(1, depth + 1):
        allowed = tuple(d for d in ds if p**e * d >= minimum)
        states = set().union(*(transition(s, p, cofactor, allowed, width) for s in states))
    return states


def unrestricted_exponent(p, cofactor, minimum, max_states=20000):
    """Complete BFS, or explicit exception; never interpret a cutoff as UNSAT."""
    check_parameters(p, cofactor, minimum)
    s = 0
    while p**s < minimum:
        s += 1
    remaining = minimum
    while remaining % p == 0:
        remaining //= p
    if cofactor % remaining:
        return {"exists": False, "reason": "minimum does not divide any period"}
    ds = divisors(cofactor)
    width = (len(ds) - 1) // (p - 1)
    starts = initial_states(p, cofactor, minimum, s)
    queue = deque((state, s) for state in sorted(starts))
    visited = set(starts)
    if len(visited) > max_states:
        raise IncompleteSearch("initial state budget exceeded")
    while queue:
        state, depth = queue.popleft()
        if state == ():
            return {"exists": True, "first_exponent_at_least_s": depth,
                    "visited_states": len(visited), "width_bound": width}
        for nxt in sorted(transition(state, p, cofactor, ds, width)):
            if nxt not in visited:
                visited.add(nxt)
                if len(visited) > max_states:
                    raise IncompleteSearch("reachable state budget exceeded")
                queue.append((nxt, depth + 1))
    # Queue exhaustion, not a depth or resource limit, proves closure.
    encoding = json.dumps(sorted(visited), separators=(",", ":")).encode()
    return {"exists": False, "reason": "complete nonterminal reachable closure",
            "visited_states": len(visited), "width_bound": width,
            "closure_sha256": sha256(encoding).hexdigest()}


def literal_feasible(p, cofactor, minimum, depth):
    """Independent definition-level enumeration of all completed residue choices."""
    period = p**depth * cofactor
    if period % minimum:
        return False
    moduli = tuple(d for d in divisors(period) if d >= minimum)
    if not moduli:
        return False
    if sum(Fraction(1, d) for d in moduli) < 1:
        return False  # ordinary union bound, including the equality case
    # This routine uses literal integer residues, not p-prefix transitions.
    for residues in product(*(range(d) for d in moduli)):
        if all(any(x % d == a for d, a in zip(moduli, residues))
               for x in range(period)):
            return True
    return False


def literal_one_layer(u, p, cofactor):
    """Definition-level continuation sets for p labeled children of one fiber."""
    period = p * cofactor
    ds = divisors(cofactor)
    states = set()
    # -1 means omit. CRT is implicit in integer congruence tests here.
    for residues in product(*(range(-1, p * d) for d in ds)):
        residual = []
        for r in range(p):
            mask = 0
            for x in range(r, period, p):
                y = x % cofactor
                if (u >> y) & 1 and not any(
                        a >= 0 and x % (p * d) == a
                        for d, a in zip(ds, residues)):
                    mask |= 1 << y
            residual.append(mask)
        states.add(canonical(residual))
    return states


def literal_multiple_fibers(state, p, cofactor):
    """Literal integer continuation, including two parents with different residuals."""
    old_period = 1
    while old_period < len(state):
        old_period *= p
    parents = state + (0,) * (old_period - len(state))
    new_power = p * old_period
    period = new_power * cofactor
    ds = divisors(cofactor)
    states = set()
    for residues in product(*(range(-1, new_power * d) for d in ds)):
        residual = []
        for r in range(new_power):
            mask = 0
            for x in range(r, period, new_power):
                y = x % cofactor
                if (parents[x % old_period] >> y) & 1 and not any(
                        a >= 0 and x % (new_power * d) == a
                        for d, a in zip(ds, residues)):
                    mask |= 1 << y
            residual.append(mask)
        states.add(canonical(residual))
    return states


def valuation(n, p):
    e = 0
    while n % p == 0:
        e += 1
        n //= p
    return e


def audit_cover(classes):
    moduli = [d for _, d in classes]
    if len(set(moduli)) != len(moduli) or any(d < 2 or not 0 <= a < d for a, d in classes):
        raise ValueError("malformed distinct cover")
    period = lcm(*moduli)
    if not all(any(x % d == a for a, d in classes) for x in range(period)):
        raise ValueError("witness does not cover its full period")
    factors = tuple(p for p in divisors(period) if p > 1 and
                    not any(p % d == 0 for d in range(2, p)))
    profiles = []
    for p in factors:
        largest = valuation(period, p)
        cofactor = period // p**largest
        count = len(divisors(cofactor))
        actual = []
        bounds = []
        for e in range(largest + 1):
            selected = [(a, d, valuation(d, p)) for a, d in classes if valuation(d, p) <= e]
            nonempty = 0
            for r in range(p**e):
                u = [y for y in range(cofactor) if not any(
                    r % p**j == a % p**j and y % (d // p**j) == a % (d // p**j)
                    for a, d, j in selected)]
                nonempty += bool(u)
            capacity = sum(Fraction(sum(p**j * d >= min(moduli) for d in divisors(cofactor)),
                                    p**(j - e)) for j in range(e + 1, largest + 1))
            bound = capacity.numerator // capacity.denominator
            assert nonempty <= bound
            assert nonempty <= (count - 1) // (p - 1)
            actual.append(nonempty)
            bounds.append(bound)
        profiles.append({"p": p, "cofactor": cofactor,
                         "residual_fibers_by_depth": actual,
                         "finite_horizon_bounds": bounds})
    return {"minimum": min(moduli), "lcm": period, "number_of_classes": len(classes),
            "profiles": profiles}


def main():
    if sys.version_info < (3, 10):
        raise RuntimeError("Python >=3.10 required")
    if sys.flags.optimize:
        raise RuntimeError("run without Python optimization: the checks require assertions")
    # Full successor-set equality checks use a different, literal representation.
    transition_checks = 0
    for p, cofactor in ((2, 1), (2, 3), (2, 5), (3, 2)):
        for u in range(1, 1 << cofactor):
            assert transition((u,), p, cofactor, divisors(cofactor)) == literal_one_layer(u, p, cofactor)
            transition_checks += 1
    for state in ((1, 3), (7, 19), (341, 511)):
        assert transition(state, 2, 9, divisors(9)) == literal_multiple_fibers(state, 2, 9)
        transition_checks += 1
    rotation_transport_checks = 0
    for cofactor in (3, 5):
        for u in range(1, 1 << cofactor):
            original = {rotated_state(t, cofactor) for t in transition((u,), 2, cofactor, divisors(cofactor))}
            normalized = {rotated_state(t, cofactor) for t in transition(
                rotated_state((u,), cofactor), 2, cofactor, divisors(cofactor))}
            assert original == normalized
            rotation_transport_checks += 1
    for state in ((1, 3), (7, 19), (341, 511)):
        original = {rotated_state(t, 9) for t in transition(state, 2, 9, divisors(9))}
        normalized = {rotated_state(t, 9) for t in transition(rotated_state(state, 9), 2, 9, divisors(9))}
        assert original == normalized
        rotation_transport_checks += 1
    rotations = {}
    for cofactor in range(1, 10):
        burnside = sum(1 << gcd(cofactor, t) for t in range(cofactor))
        assert burnside % cofactor == 0
        actual = len({rotation_orbit(u, cofactor) for u in range(1 << cofactor)})
        assert actual == burnside // cofactor
        rotations[str(cofactor)] = actual
    trees = {}
    for q, depth in ((2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (5, 1)):
        predicted = 2
        for _ in range(depth):
            predicted = comb(predicted + q - 1, q)
        actual = len({tree_subset_type(u, q, depth) for u in range(1 << q**depth)})
        assert actual == predicted
        trees[f"{q}^{depth}"] = actual
    # The equality boundary k/(p-1) is deliberately rejected.
    assert initial_states(2, 1, 2, 1) == set()
    assert transition((1, 1), 2, 3, divisors(3), width=1) == set()
    try:
        unrestricted_exponent(2, 5, 2, max_states=1)
    except IncompleteSearch:
        pass
    else:
        raise AssertionError("a state budget must raise, not return a mathematical verdict")
    comparisons = 0
    for p, cofactor, max_depth in ((2, 1, 3), (2, 3, 2), (2, 5, 2), (3, 2, 1), (3, 4, 1)):
        for minimum in range(2, 9):
            for depth in range(max_depth + 1):
                quotient = () in initial_states(p, cofactor, minimum, depth)
                # Completion converts at-least-m to exactly-m only if m|L.
                quotient = quotient and p**depth * cofactor % minimum == 0
                assert quotient == literal_feasible(p, cofactor, minimum, depth), (p, cofactor, minimum, depth)
                comparisons += 1
    closures = []
    for p, cofactor, minimum, expected in (
            (2, 1, 2, False), (2, 3, 2, True), (2, 3, 3, False),
            (2, 5, 2, True), (2, 3, 8, False), (2, 5, 8, False),
            (2, 7, 8, False), (2, 9, 8, False), (2, 15, 8, False),
            (3, 4, 2, True)):
        result = unrestricted_exponent(p, cofactor, minimum)
        assert result["exists"] is expected
        closures.append({"p": p, "cofactor": cofactor, "minimum": minimum, **result})
    fixtures = json.loads(Path(__file__).with_name("fixtures.json").read_text())
    audits = {name: audit_cover(record["classes"]) for name, record in fixtures.items()}
    report = {"literal_transition_set_comparisons": transition_checks,
              "cofactor_rotation_transport_checks": rotation_transport_checks,
              "subset_rotation_orbit_counts": rotations,
              "subset_residue_tree_orbit_counts": trees,
              "literal_feasibility_comparisons": comparisons,
              "complete_small_controls": closures, "attributed_cover_audits": audits,
              "minimum_eight_exponent_cutoffs_M9": {
                  "unquotiented": 3 + comb(511 + 2, 2) - 1,
                  "translations": 3 + comb(rotations["9"] - 1 + 2, 2) - 1,
                  "residue_tree": 3 + comb(trees["3^2"] - 1 + 2, 2) - 1}}
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
