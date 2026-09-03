#!/usr/bin/env python3
"""Generate the four SAT instances used for the order-14 lower bound.

The generated DIMACS files are solver inputs and should be written under
/scratch, not committed to this repository.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool


def arc(pool: IDPool, i: int, j: int) -> int:
    """Literal asserting i -> j; an edge variable means low -> high."""
    if i == j:
        raise ValueError("loops are not tournament arcs")
    var = pool.id(("edge", min(i, j), max(i, j)))
    return var if i < j else -var


def gate(clauses: list[list[int]], literal: int) -> list[list[int]]:
    return [[literal, *clause] for clause in clauses]


def add_basic_hall_obstruction(cnf: CNF, pool: IDPool, n: int, x: int) -> None:
    """Encode one arbitrary deficient Hall set at x."""
    s_lits: list[int] = []
    t_lits: list[int] = []
    for y in range(n):
        if y == x:
            continue
        s = pool.id(("hall-left", x, y))
        s_lits.append(s)
        cnf.append([-s, arc(pool, x, y)])
    for z in range(n):
        if z == x:
            continue
        t = pool.id(("hall-neighbor", x, z))
        t_lits.append(t)
        products: list[int] = []
        for y in range(n):
            if y == x or y == z:
                continue
            s = pool.id(("hall-left", x, y))
            product = pool.id(("product", x, y, z))
            yz = arc(pool, y, z)
            products.append(product)
            cnf.append([-product, s])
            cnf.append([-product, yz])
            cnf.append([product, -s, -yz])
            cnf.append([-product, -arc(pool, z, x), t])
        cnf.append([-t, arc(pool, z, x)])
        cnf.append([-t, *products])
    # |T| < |S| iff |T| + sum(1-s_y) <= (n-1)-1.
    cnf.extend(
        CardEnc.atmost(
            [*t_lits, *[-s for s in s_lits]],
            bound=n - 2,
            vpool=pool,
            encoding=EncType.seqcounter,
        ).clauses
    )


def build_n13() -> tuple[CNF, IDPool]:
    """A regular 13-tournament in which every vertex fails Hall."""
    n = 13
    pool = IDPool()
    cnf = CNF()
    for x in range(n):
        degree = [arc(pool, x, y) for y in range(n) if y != x]
        cnf.extend(
            CardEnc.equals(
                degree, bound=6, vpool=pool, encoding=EncType.seqcounter
            ).clauses
        )
    for y in range(1, 7):
        cnf.append([arc(pool, 0, y)])
    for z in range(7, 13):
        cnf.append([arc(pool, z, 0)])
    for x in range(n):
        add_basic_hall_obstruction(cnf, pool, n, x)
    return cnf, pool


def add_minimal_hall_obstruction(
    cnf: CNF, pool: IDPool, n: int, x: int, high: int
) -> None:
    """Encode a minimal Hall obstruction, gated off when d+(x) >= 7."""
    clauses: list[list[int]] = []
    s_lits: list[int] = []
    t_lits: list[int] = []
    for y in range(n):
        if y == x:
            continue
        s = pool.id(("hall-left", x, y))
        s_lits.append(s)
        clauses.append([-s, arc(pool, x, y)])
    for z in range(n):
        if z == x:
            continue
        t = pool.id(("hall-neighbor", x, z))
        t_lits.append(t)
        products: list[int] = []
        for y in range(n):
            if y == x or y == z:
                continue
            s = pool.id(("hall-left", x, y))
            product = pool.id(("product", x, y, z))
            yz = arc(pool, y, z)
            products.append(product)
            clauses.append([-product, s])
            clauses.append([-product, yz])
            clauses.append([product, -s, -yz])
            clauses.append([-product, -arc(pool, z, x), t])
        clauses.append([-t, arc(pool, z, x)])
        clauses.append([-t, *products])
        twice = CardEnc.atleast(
            products, bound=2, vpool=pool, encoding=EncType.seqcounter
        )
        clauses.extend([[-t, *clause] for clause in twice.clauses])

    clauses.extend(
        CardEnc.atleast(
            s_lits, bound=3, vpool=pool, encoding=EncType.seqcounter
        ).clauses
    )
    for y in range(n):
        if y == x:
            continue
        internal: list[int] = []
        for z in range(n):
            if z == x or z == y:
                continue
            product = pool.id(("internal-product", x, y, z))
            sz = pool.id(("hall-left", x, z))
            yz = arc(pool, y, z)
            internal.append(product)
            clauses.append([-product, sz])
            clauses.append([-product, yz])
            clauses.append([product, -sz, -yz])
        clauses.append([-pool.id(("hall-left", x, y)), *internal])

    clauses.extend(
        CardEnc.equals(
            [*t_lits, *[-s for s in s_lits]],
            bound=n - 2,
            vpool=pool,
            encoding=EncType.seqcounter,
        ).clauses
    )
    cnf.extend(gate(clauses, high))


def build_n14(root_hall_size: int) -> tuple[CNF, IDPool]:
    """Order-14 counterexample encoding for one root Hall-set size."""
    if root_hall_size not in (3, 4, 5):
        raise ValueError("the complete root cases are 3, 4, and 5")
    n = 14
    pool = IDPool()
    cnf = CNF()
    high_lits: list[int] = []
    for x in range(n):
        degree = [arc(pool, x, y) for y in range(n) if y != x]
        cnf.extend(
            CardEnc.atleast(
                degree, bound=6, vpool=pool, encoding=EncType.seqcounter
            ).clauses
        )
        high = pool.id(("degree-at-least-seven", x))
        high_lits.append(high)
        cnf.extend(
            gate(
                CardEnc.atleast(
                    degree, bound=7, vpool=pool, encoding=EncType.seqcounter
                ).clauses,
                -high,
            )
        )
        cnf.extend(
            gate(
                CardEnc.atmost(
                    degree, bound=6, vpool=pool, encoding=EncType.seqcounter
                ).clauses,
                high,
            )
        )
    cnf.extend(
        CardEnc.atmost(
            high_lits, bound=7, vpool=pool, encoding=EncType.seqcounter
        ).clauses
    )

    cnf.append([-high_lits[0]])
    for y in range(1, 7):
        cnf.append([arc(pool, 0, y)])
    for z in range(7, n):
        cnf.append([arc(pool, z, 0)])
    for y in range(1, n):
        s = pool.id(("hall-left", 0, y))
        cnf.append([s if 1 <= y <= root_hall_size else -s])
    for z in range(1, n):
        t = pool.id(("hall-neighbor", 0, z))
        in_initial_neighbor_set = 7 <= z < 7 + root_hall_size - 1
        cnf.append([t if in_initial_neighbor_set else -t])

    for x in range(n):
        add_minimal_hall_obstruction(cnf, pool, n, x, high_lits[x])
    return cnf, pool


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("case", choices=("n13", "n14-s3", "n14-s4", "n14-s5"))
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if not args.output.is_absolute() or args.output.parts[:2] != ("/", "scratch"):
        raise SystemExit("output must be an absolute path below /scratch")
    cnf, pool = (
        build_n13()
        if args.case == "n13"
        else build_n14(int(args.case[-1]))
    )
    cnf.to_file(args.output)
    print(
        json.dumps(
            {
                "case": args.case,
                "variables": pool.top,
                "clauses": len(cnf.clauses),
                "sha256": sha256(args.output),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
