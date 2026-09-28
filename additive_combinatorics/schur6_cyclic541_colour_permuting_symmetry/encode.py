"""Exact CNF for an order-20 multiplier acting as (0 1 2 3 4)(5)."""
import itertools
import math


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encode(p=541, generator=497):
    require(p > 2 and all(p % q for q in range(2, math.isqrt(p) + 1)), "not prime")
    powers = [pow(generator, j, p) for j in range(20)]
    require(len(set(powers)) == 20 and pow(generator, 20, p) == 1, "wrong order")
    require(powers[10] == p - 1, "wrong reflection")
    location, representatives = {}, []
    for r in range(1, p):
        if r in location:
            continue
        i = len(representatives)
        representatives.append(r)
        for j, h in enumerate(powers):
            location[r * h % p] = (i, j % 5)
    require(len(location) == p - 1, "incomplete cosets")
    var = lambda i, a: 6 * i + a + 1
    clauses = set()
    for i in range(len(representatives)):
        clauses.add(tuple(var(i, a) for a in range(6)))
        for a, b in itertools.combinations(range(6), 2):
            clauses.add((-var(i, a), -var(i, b)))
    for x in representatives:
        for y in range(1, p):
            z = (x + y) % p
            if z == 0:
                continue
            for colour in range(6):
                forbidden = {}
                for w in (x, y, z):
                    i, phase = location[w]
                    state = (colour - phase) % 5 if colour < 5 else 5
                    if i in forbidden and forbidden[i] != state:
                        break  # This monochromatic assignment is impossible.
                    forbidden[i] = state
                else:
                    clauses.add(tuple(sorted(-var(i, a) for i, a in forbidden.items())))
    # A nonfixed colour occurs; scale it to 1, then rotate the five labels.
    clauses.add((1,))
    return sorted(clauses), representatives, location


def dimacs(clauses, variables):
    return (f"p cnf {variables} {len(clauses)}\n"
            + "".join(" ".join(map(str, c)) + " 0\n" for c in clauses)).encode("ascii")
