#!/usr/bin/env python3
"""Independent, standard-library audit of the order-20 action's exact CNF."""

import hashlib
import itertools
import json


P = 541
H = 497
EXPECTED = "7f781fb01397d2bf6b02de540a8d44fa6a98faa05abdffdebee94f44187c6dee"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    require(all(P % d for d in range(2, 24)), "modulus is not prime")
    powers = [pow(H, j, P) for j in range(20)]
    require(len(set(powers)) == 20 and pow(H, 20, P) == 1,
            "generator has the wrong order")
    require(powers[10] == P - 1, "reflection is absent")

    # Build the action table by multiplying each least coset representative.
    table = {}
    reps = []
    for r in range(1, P):
        if r in table:
            continue
        i = len(reps)
        reps.append(r)
        for j, power in enumerate(powers):
            x = r * power % P
            require(x not in table, "coset overlap")
            table[x] = (i, j)
    require(len(reps) == 27 and len(table) == 540, "cosets incomplete")

    def variable(i, state):
        return 6 * i + state + 1

    def state_for(x, colour):
        i, j = table[x]
        return i, ((colour - j) % 5 if colour < 5 else 5)

    clauses = set()
    for i in range(27):
        clauses.add(tuple(variable(i, state) for state in range(6)))
        for a, b in itertools.combinations(range(6), 2):
            clauses.add((-variable(i, a), -variable(i, b)))
    clauses.add((1,))  # Scale a cycling-colour occurrence to 1 and rotate labels.

    pairs = diagonal = wrapped = 0
    for x in range(1, P):
        for y in range(x, P):
            z = (x + y) % P
            if z == 0:
                continue
            pairs += 1
            diagonal += x == y
            wrapped += x + y > P
            for colour in range(6):
                required = [state_for(w, colour) for w in (x, y, z)]
                assignment = dict(required)
                if any(assignment[i] != state for i, state in required):
                    continue
                clauses.add(tuple(sorted(-variable(i, state)
                                         for i, state in assignment.items())))

    canonical = sorted(clauses)
    cnf = (f"p cnf 162 {len(canonical)}\n" +
           "".join(" ".join(map(str, clause)) + " 0\n"
                   for clause in canonical)).encode("ascii")
    digest = hashlib.sha256(cnf).hexdigest()
    require((pairs, diagonal, len(canonical), digest) ==
            (145800, 540, 13420, EXPECTED), "CNF or count mismatch")

    possible_orders = sorted({kernel * image
                              for kernel in (2, 4)
                              for image in (1, 2, 3, 4, 5, 6)
                              if 540 % (kernel * image) == 0})
    require(possible_orders == [2, 4, 6, 10, 12, 20],
            "algebraic order list mismatch")
    print(json.dumps({"cosets": len(reps), "pairs": pairs,
                      "diagonal_pairs": diagonal, "wrapped_pairs": wrapped,
                      "clauses": len(canonical), "cnf_sha256": digest,
                      "pre_certificate_group_orders": possible_orders},
                     sort_keys=True))


if __name__ == "__main__":
    main()
