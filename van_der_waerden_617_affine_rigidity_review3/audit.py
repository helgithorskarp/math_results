"""Independent QR617 audit: Euler quotient encoding and watched-literal CNF.

six-reviewer-3, reviewer. Python 3.11+ and the standard-library C++17 kernel.
No target code, input coloring or solver library is imported.
"""
import argparse
import hashlib
from itertools import product
import json
from math import isqrt
from pathlib import Path
import random
import subprocess

P = 617


def require(condition, message):
    if not condition:
        raise ValueError(message)


class Incomplete(RuntimeError):
    pass


def invoke_cases(checker, cases, options=(), expected_exit=0):
    rows = []
    for n, clauses in cases:
        rows.append(f"{n} {len(clauses)}")
        rows.extend(" ".join(map(str, c)) + " 0" for c in clauses)
    result = subprocess.run([str(checker), *options],
                            input="\n".join(rows)+"\n", text=True,
                            capture_output=True, timeout=130)
    records = [json.loads(line) for line in result.stdout.splitlines()]
    if result.returncode == 2 and expected_exit == 0:
        raise Incomplete("native bounded search unfinished; no classification")
    require(result.returncode == expected_exit and not result.stderr,
            "kernel failure: " + result.stderr)
    if expected_exit:
        require(records == [dict(status="INCOMPLETE")], "bad incomplete status")
    else:
        require(len(records) == len(cases), "missing case result")
        for record, (n, clauses) in zip(records, cases):
            require(record['status'] in ('SAT', 'UNSAT'), "bad decision status")
            if record['status'] == 'SAT':
                bits = record['witness']
                require(len(bits) == n and all(bit in (0, 1) for bit in bits),
                        "bad native witness")
                require(all(any(bits[abs(lit)-1] == (lit > 0) for lit in c)
                            for c in clauses), "native witness violates clause")
    return records


def quotient_edges(m):
    """Euler homomorphism x -> x^(616/m), then spacing-one and scaling."""
    require(m in (8, 44, 56), "only audited indices8,44,56 are supported")
    order = 616 // m
    images = {pow(3, order*j, P): j for j in range(m)}
    require(len(images) == m, "quotient image has wrong order")
    labels = [m] + [images[pow(x, order, P)] for x in range(1, P)]
    full = set()
    for start in range(P):
        base = {labels[(start+j) % P] for j in range(7)}
        for shift in range(m):
            full.add(sum(1 << (m if v == m else (v+shift) % m)
                         for v in base))
    punctured = sorted(edge for edge in full if not edge & (1 << m))
    return sorted(full), punctured


def clauses_for(edges):
    clauses = []
    for edge in edges:
        require(edge > 0, "empty hyperedge")
        variables = tuple(i+1 for i in range(edge.bit_length())
                          if edge & (1 << i))
        clauses.append(variables)
        clauses.append(tuple(-i for i in variables))
    return clauses


def solver_controls(checker):
    comparisons = 0
    # All 256 families of the eight n=2 nonempty, nontautological clauses.
    families = [tuple((i+1)*s for i, s in enumerate(choice) if s)
                for choice in product((-1, 0, 1), repeat=2) if any(choice)]
    cases = [[c for i, c in enumerate(families) if mask & (1 << i)]
             for mask in range(1 << len(families))]
    rng = random.Random(390617)
    for n in range(3, 9):
        for _ in range(40):
            cs = []
            for _ in range(2*n):
                clause = tuple((i+1)*rng.choice((-1, 1)) for i in range(n)
                               if rng.randrange(3) == 0)
                cs.append(clause)
            cases.append(cs)
    instances = []
    expectations = []
    for clauses in cases:
        n = max((abs(lit) for c in clauses for lit in c), default=2)
        expected = any(all(any(bits[abs(lit)-1] == (lit > 0) for lit in c)
                           for c in clauses)
                       for bits in product((False, True), repeat=n))
        instances.append((n, clauses))
        expectations.append(expected)
    for record, expected in zip(invoke_cases(checker, instances), expectations):
        require((record['status'] == 'SAT') == expected, "CNF/brute disagreement")
        comparisons += 1
    for options in (('--nodes', '0'), ('--seconds', '0')):
        invoke_cases(checker, [(2, [(1, 2), (-1, -2)])], options,
                     expected_exit=2)
    incomplete = 2
    require(invoke_cases(checker, [(4, [(-1,), (-2,)])])[0]['status'] == 'SAT',
            "empty constraint control is not SAT")
    return dict(brute_force_cnf_comparisons=comparisons,
                rejected_incomplete_searches=incomplete,
                missing_constraint_sat_control=True)


def affine_checks():
    squares = {x*x % P for x in range(1, P)}
    require(len(squares) == 308, "bad squares")
    color = [0 if x in squares else 1 for x in range(P)]
    zero_progressions = 0
    # Removing zero from a progression through zero leaves both nonzero
    # colors, so either choice at zero works, as does complementation.
    for d in range(1, P):
        for zero_slot in range(7):
            points = [((j-zero_slot)*d) % P for j in range(7)]
            colors = {color[x] for x in points if x}
            require(colors == {0, 1}, "zero-color obstruction")
            zero_progressions += 1
    # Exact full-word comparison verifies the 4*617 forms are distinct.
    words = set()
    for center in range(P):
        for at_center in (0, 1):
            word = bytes(at_center if x == center else color[(x-center) % P]
                         for x in range(P))
            words.add(word)
            words.add(bytes(1-bit for bit in word))
    require(len(words) == 4*P, "affine forms are not distinct")
    counts = []
    all_bits = (1 << P)-1
    for at_zero in (0, 1):
        ones = {x for x in range(P) if (at_zero if x == 0 else color[x])}
        original = sum(1 << x for x in ones)
        stabilizers = []
        for multiplier in range(1, P):
            scaled = sum(1 << ((multiplier*x) % P) for x in ones)
            for offset in range(P):
                moved = ((scaled << offset) |
                         (scaled >> (P-offset))) & all_bits
                if moved == original:
                    stabilizers.append((multiplier, offset))
        require(stabilizers == [(x, 0) for x in sorted(squares)],
                "unexpected affine stabilizer")
        counts.append(len(stabilizers))
    return dict(through_zero_progressions=zero_progressions,
                distinct_high_symmetry_full_field_colorings=len(words),
                affine_maps_per_representative=P*(P-1),
                representative_stabilizer_orders=counts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--compare-native", type=Path)
    parser.add_argument("--kernel", type=Path)
    args = parser.parse_args()
    if args.kernel is None:
        build = Path(__file__).resolve().parent / 'build'
        build.mkdir(exist_ok=True)
        checker = build / 'kernel'
        run = subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra',
                              '-Wconversion', '-Wshadow', '-Wpedantic',
                              str(Path(__file__).with_name('kernel.cpp')),
                              '-o', str(checker)], capture_output=True, text=True)
        require(run.returncode == 0 and not run.stderr, 'compilation: '+run.stderr)
    else:
        checker = args.kernel.resolve(strict=True)
    require(all(P % d for d in range(2, isqrt(P)+1)), "617 not prime")
    require(pow(3, 616, P) == 1 and
            all(pow(3, 616//r, P) != 1 for r in (2, 7, 11)),
            "3 is not primitive")
    controls = solver_controls(checker)
    records = []
    for m in (44, 56):
        full, edges = quotient_edges(m)
        if args.compare_native:
            native = [int(s) for s in
                      (args.compare_native/f"edges-{m}.txt").read_text().split()]
            require(full == native, "native/Euler entire edge sets disagree")
        parity = sum(1 << i for i in range(m) if i % 2)
        require(all(edge & parity and edge & ~parity for edge in edges),
                "quadratic orientation fails")
        # Nonalternating even cyclic words have an equal adjacent pair.
        # The edge family is shift-invariant and color complement invariant.
        # Shift that pair to0,1 and complement to fix both colors to0.
        edge_set = set(edges)
        require(all((((edge << 1) | (edge >> (m-1))) & ((1 << m)-1))
                    in edge_set for edge in edges),
                "cyclic normalization not supported by constraints")
        search = invoke_cases(checker, [(m, clauses_for(edges)+[(-1,), (-2,)])])[0]
        require(search['status'] == 'UNSAT',
                "nonquadratic adjacent-equal word exists")
        record = dict(m=m, full_edges=len(full), punctured_edges=len(edges),
                      full_edge_masks_sha256=hashlib.sha256(
                          "\n".join(map(str, full)).encode()).hexdigest(),
                      adjacent_equal_status="UNSAT",
                      signed_clauses=2*len(edges), nodes=search['nodes'],
                      conflicts=search['conflicts'],
                      propagated_units=search['propagated_units'])
        records.append(record)
        print(json.dumps(dict(completed_index=record), sort_keys=True), flush=True)
    full8, edges8 = quotient_edges(8)
    survivors = [word for word in range(256) if
                 all(edge & word and edge & ~word for edge in edges8)]
    require(survivors == [85, 170], "index8 control mismatch")
    divisors = [m for m in range(1, 617) if 616 % m == 0]
    indices = [m for m in divisors if 616//m >= 11]
    require(all(44 % m == 0 or 56 % m == 0 for m in indices),
            "finite-group coverage incomplete")
    small_orders = [order for order in divisors if order < 11]
    require(small_orders == [1, 2, 4, 7, 8], "wrong residual orders")
    affine = affine_checks()
    print(json.dumps(dict(
        verified=True, agent="six-reviewer-3", role="reviewer",
        cases=records, controls=controls, index8_survivors=survivors,
        covered_indices=indices, possible_nonquadratic_stabilizer_orders=small_orders,
        affine_corollary_checks=affine), sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Incomplete as failure:
        print(json.dumps(dict(status="INCOMPLETE", message=str(failure))))
        raise SystemExit(2)
