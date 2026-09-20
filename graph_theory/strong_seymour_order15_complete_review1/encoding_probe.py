#!/usr/bin/env python3
"""Semantic probes for the submitted order-15 CNF encoder.

The direct oracle below is independent.  The only imported target code is the
encoder being tested.  Tests fix complete labelled tournaments, then ask a SAT
solver whether the encoder's one-vertex obstruction agrees with direct Hall
enumeration.  Degree-six tests use only tournaments in which the root is a
minimum-degree vertex, exactly the scope of the imported witness lemma.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import random

from pysat.formula import CNF, IDPool
from pysat.solvers import Solver


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
BASE_PATH = REPOSITORY_ROOT / "strong_seymour_order15" / "generate_cnf.py"
EXPECTED_BASE_SHA256 = "5dda45c3e5e9aeeb286bfa6844e911bf8d9cb47918e2cf21f0fb00e2482d0517"
N = 15


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def load_base():
    spec = importlib.util.spec_from_file_location("reviewed_ss15_encoder", BASE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {BASE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def direct_strong(out: list[int], root: int = 0) -> bool:
    a = out[root]
    b = ((1 << N) - 1) ^ a ^ (1 << root)
    selected = a
    while selected:
        neighbors = 0
        active = selected
        while active:
            bit = active & -active
            neighbors |= out[bit.bit_length() - 1] & b
            active ^= bit
        if neighbors.bit_count() < selected.bit_count():
            return False
        selected = (selected - 1) & a
    return True


def random_root_tournament(rng: random.Random, degree: int = 7) -> list[int]:
    out = [0] * N
    for i in range(N):
        for j in range(i + 1, N):
            if i == 0:
                i_wins = j <= degree
            else:
                i_wins = bool(rng.getrandbits(1))
            winner, loser = (i, j) if i_wins else (j, i)
            out[winner] |= 1 << loser
    return out


def forced_witness_tournament(rng: random.Random, size: int) -> list[int]:
    """A degree-seven root with an explicit inclusion-minimal Hall witness."""
    out = random_root_tournament(rng, 7)
    s = set(range(1, 1 + size))
    r = set(range(8, 8 + size - 1))
    for tail in s:
        for head in range(8, 15):
            if head in r:
                out[tail] |= 1 << head
                out[head] &= ~(1 << tail)
            else:
                out[head] |= 1 << tail
                out[tail] &= ~(1 << head)
    assert not direct_strong(out)
    return out


def cyclic_regular() -> list[int]:
    out = [0] * N
    for i in range(N):
        for offset in range(1, 8):
            out[i] |= 1 << ((i + offset) % N)
    return out


def reverse_cycle(out: list[int], triple: tuple[int, int, int]) -> bool:
    vertices = set(triple)
    internal = [(u, v) for u in vertices for v in vertices if u < v]
    # A three-vertex tournament is cyclic exactly when every internal degree is one.
    if any(sum(out[u] >> v & 1 for v in vertices if v != u) != 1 for u in vertices):
        return False
    for u, v in internal:
        if out[u] >> v & 1:
            out[u] &= ~(1 << v)
            out[v] |= 1 << u
        else:
            out[v] &= ~(1 << u)
            out[u] |= 1 << v
    return True


def minimum_degree_six_samples(rng: random.Random, count: int) -> list[list[int]]:
    samples = []
    regular = cyclic_regular()
    while len(samples) < count:
        for _ in range(60):
            reverse_cycle(regular, tuple(rng.sample(range(N), 3)))
        choices = [v for v in range(1, N) if regular[0] >> v & 1]
        head = rng.choice(choices)
        out = regular.copy()
        out[0] &= ~(1 << head)
        out[head] |= 1
        degrees = [mask.bit_count() for mask in out]
        assert degrees[0] == 6 and min(degrees) == 6
        samples.append(out)
    return samples


def forced_degree_six_nonstrong(rng: random.Random, count: int) -> list[list[int]]:
    """Construct minimum-degree-six roots with a size-three Hall obstruction."""
    samples = []
    while len(samples) < count:
        out = [0] * N

        # Root shores: A=1..6, B=7..14.
        for vertex in range(1, 7):
            out[0] |= 1 << vertex
        for vertex in range(7, 15):
            out[vertex] |= 1

        s = (1, 2, 3)
        c = (4, 5, 6)
        r = (7, 8)
        d = tuple(range(9, 15))

        # S is a directed triangle, dominates R and C, and loses to D.
        for tail, head in ((1, 2), (2, 3), (3, 1)):
            out[tail] |= 1 << head
        for tail in s:
            for head in (*r, *c):
                out[tail] |= 1 << head
            for head in d:
                out[head] |= 1 << tail

        # C dominates B.  R dominates D.  These choices keep C and R safely
        # above degree six while preserving Gamma_root(S)=R.
        for tail in c:
            for head in (*r, *d):
                out[tail] |= 1 << head
        for tail in r:
            for head in d:
                out[tail] |= 1 << head

        # Orient C and R internally at random.
        for block in (c, r):
            for i, u in enumerate(block):
                for v in block[i + 1 :]:
                    winner, loser = (u, v) if rng.getrandbits(1) else (v, u)
                    out[winner] |= 1 << loser

        # D needs internal minimum out-degree two.  Rejection is tiny for six
        # vertices and produces diverse exact examples.
        while True:
            trial = out.copy()
            for i, u in enumerate(d):
                for v in d[i + 1 :]:
                    winner, loser = (u, v) if rng.getrandbits(1) else (v, u)
                    trial[winner] |= 1 << loser
            if min((trial[u] & sum(1 << v for v in d)).bit_count() for u in d) >= 2:
                out = trial
                break

        degrees = [mask.bit_count() for mask in out]
        assert degrees[0] == 6 and min(degrees) == 6
        assert not direct_strong(out)
        samples.append(out)
    return samples


def fixed_clauses(base, pool: IDPool, out: list[int]) -> list[list[int]]:
    clauses = []
    for i in range(N):
        for j in range(i + 1, N):
            literal = base.arc(pool, i, j)
            clauses.append([literal if out[i] >> j & 1 else -literal])
    return clauses


def obstruction_sat(base, out: list[int]) -> bool:
    pool = IDPool()
    cnf = CNF()
    at_least_seven, at_least_eight = base.add_degree_flags(cnf, pool, 0)
    base.add_minimal_hall_obstruction(
        cnf,
        pool,
        0,
        at_least_seven,
        at_least_eight,
        every_vertex_is_minimum=False,
    )
    cnf.extend(fixed_clauses(base, pool, out))
    with Solver(bootstrap_with=cnf.clauses) as solver:
        return solver.solve()


def degree_flag_probe(base) -> dict[str, int]:
    satisfiable = rejected_below_six = wrong_flags_rejected = 0
    for degree in range(15):
        out = random_root_tournament(random.Random(1000 + degree), degree)
        pool = IDPool()
        cnf = CNF()
        flag7, flag8 = base.add_degree_flags(cnf, pool, 0)
        cnf.extend(fixed_clauses(base, pool, out))
        with Solver(bootstrap_with=cnf.clauses) as solver:
            sat = solver.solve()
            if degree < 6:
                assert not sat
                rejected_below_six += 1
                continue
            assert sat
            satisfiable += 1
            expected7 = degree >= 7
            expected8 = degree >= 8
            wrong7 = -flag7 if expected7 else flag7
            wrong8 = -flag8 if expected8 else flag8
            assert not solver.solve(assumptions=[wrong7])
            assert not solver.solve(assumptions=[wrong8])
            wrong_flags_rejected += 2
    return {
        "rejected_below_six": rejected_below_six,
        "satisfiable_degrees": satisfiable,
        "wrong_flags_rejected": wrong_flags_rejected,
    }


def compare_samples(base, samples: list[list[int]], label: str) -> dict[str, object]:
    strong = nonstrong = formula_sat = 0
    record = hashlib.sha256()
    for index, out in enumerate(samples):
        oracle = direct_strong(out)
        encoded = obstruction_sat(base, out)
        assert encoded == (not oracle), (label, index, oracle, encoded)
        strong += oracle
        nonstrong += not oracle
        formula_sat += encoded
        record.update(
            f"{index}:{','.join(map(str, out))}:{int(oracle)}:{int(encoded)}\n".encode()
        )
    return {
        "formula_sat": formula_sat,
        "nonstrong": nonstrong,
        "record_sha256": record.hexdigest(),
        "strong": strong,
        "tested": len(samples),
    }


def main() -> None:
    assert sha256(BASE_PATH) == EXPECTED_BASE_SHA256
    base = load_base()
    rng = random.Random(20260920)
    degree7_random = [random_root_tournament(rng) for _ in range(48)]
    degree7_forced = [
        forced_witness_tournament(rng, size)
        for size in range(1, 7)
        for _ in range(8)
    ]
    degree6_minimum = [
        *minimum_degree_six_samples(rng, 24),
        *forced_degree_six_nonstrong(rng, 24),
    ]
    report = {
        "base_generator_sha256": EXPECTED_BASE_SHA256,
        "degree6_minimum": compare_samples(base, degree6_minimum, "degree6_minimum"),
        "degree7_forced_nonstrong": compare_samples(base, degree7_forced, "degree7_forced"),
        "degree7_random": compare_samples(base, degree7_random, "degree7_random"),
        "degree_flags": degree_flag_probe(base),
        "status": "VERIFIED",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
