#!/usr/bin/env python3
"""Definition audit, independent of the encoder, solver and proof proposer."""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def label(q, x, y):
    require(x != y, 'loop edge')
    x, y = min(x, y), max(x, y)
    return x*(2*q-x-1)//2+y-x


def parse(text):
    lines = text.splitlines()
    require(bool(lines), 'missing header')
    h = lines[0].split()
    require(len(h) == 4 and h[:2] == ['p', 'cnf'], 'invalid header')
    n, m = map(int, h[2:])
    rows = []
    for line in lines[1:]:
        tokens = list(map(int, line.split()))
        require(tokens and tokens[-1] == 0, 'missing terminator')
        row = tuple(tokens[:-1])
        require(row and all(1 <= abs(x) <= n for x in row), 'invalid literals')
        require(len(row) == len(set(row)) and not any(-x in row for x in row),
                'duplicate literal or tautology')
        require(tuple(sorted(row, key=abs)) == row, 'noncanonical literals')
        rows.append(row)
    require(len(rows) == m and len(set(rows)) == m and rows == sorted(rows),
            'clause order/count/duplicate error')
    return n, set(rows)


def prime_clauses(a_is_false, b_is_true):
    """Derive all prime implicates from a Boolean truth relation.

    Abstract A,B,X,Z use identifiers 1..4. Constants are substituted before
    enumeration. This does not import or repeat the encoder's four clauses.
    """
    ids = [3, 4] + ([] if a_is_false else [1]) + ([] if b_is_true else [2])
    good = []
    for bits in itertools.product((False, True), repeat=len(ids)):
        assignment = dict(zip(ids, bits))
        a = False if a_is_false else assignment[1]
        b = True if b_is_true else assignment[2]
        if assignment[4] == (a or (assignment[3] and b)):
            good.append(assignment)
    implicates = []
    for signs in itertools.product((-1, 0, 1), repeat=len(ids)):
        clause = frozenset(sign*v for sign, v in zip(signs, ids) if sign)
        if clause and all(any(row[abs(lit)] == (lit > 0) for lit in clause) for row in good):
            implicates.append(clause)
    primes = [c for c in implicates if not any(d < c for d in implicates)]
    # Truth-table equivalence, including every rejected assignment.
    for bits in itertools.product((False, True), repeat=len(ids)):
        row = dict(zip(ids, bits))
        satisfies = all(any(row[abs(lit)] == (lit > 0) for lit in c) for c in primes)
        require(satisfies == (row in good), 'prime-clause truth mismatch')
    return primes


TEMPLATES = {(a, b): prime_clauses(a, b) for a in (False, True) for b in (False, True)}


def counter_cells(n, target, offset):
    return {(i, k): offset+sum(min(j, target+1) for j in range(1, i))+k
            for i in range(1, n+1) for k in range(1, min(i, target+1)+1)}


def counter_clauses(inputs, target, offset):
    cells = counter_cells(len(inputs), target, offset)
    clauses = set()
    for (i, k), z in cells.items():
        mapping = {3: inputs[i-1], 4: z}
        if k < i:
            mapping[1] = cells[i-1, k]
        if k > 1:
            mapping[2] = cells[i-1, k-1]
        for clause in TEMPLATES[k == i, k == 1]:
            mapped = [mapping[abs(lit)] * (1 if lit > 0 else -1) for lit in clause]
            clauses.add(tuple(sorted(mapped, key=abs)))
    clauses.add((cells[len(inputs), target],))
    clauses.add((-cells[len(inputs), target+1],))
    return cells, clauses


def audit(text, q, distance):
    require(q >= 7 and all(q % d for d in range(2, math.isqrt(q)+1)), 'nonprime q')
    require(0 < distance < q and distance % 2 == 0, 'invalid distance')
    variables, actual = parse(text)
    expected = set()
    for x in range(1, q):
        for y in range(x+1, q):
            a, b, z = x, y, label(q, x, y)
            expected.update(((a, b, -z), (a, -b, z), (-a, b, z), (-a, -b, -z)))
    xor_clauses = len(expected)
    ladders = set()
    # Full directed domain, rather than the encoder's reversal representatives.
    for a in range(q):
        for r in range(1, q):
            row = tuple(sorted(label(q, (a+j*r) % q, (a+(j+3)*r) % q) for j in range(4)))
            require(len(set(row)) == 4, 'repeated ladder edge')
            ladders.add(row)
            expected.update((row, tuple(-v for v in row)))
    base_variables = q*(q-1)//2
    color = int(distance <= q//2)
    target = distance if color else q-distance
    inputs = [(1 if color else -1)*label(q, x, (x+3) % q) for x in range(q)]
    cells, extra = counter_clauses(inputs, target, base_variables)
    expected.update(extra)
    expected.add(((1 if color else -1)*label(q, 0, 3),))
    require(variables == base_variables+len(cells), 'variable coverage')
    require(actual == expected, 'full definition-level clause coverage differs')
    return {'q': q, 'distance': distance, 'counted_color': color, 'counter_target': target,
            'variables': variables, 'base_variables': base_variables,
            'counter_variables': len(cells), 'clauses': len(actual),
            'model_sha256': hashlib.sha256(text.encode()).hexdigest(),
            'distinct_ladders': len(ladders), 'xor_clauses': xor_clauses,
            'directed_ladders_checked': q*(q-1)}


def satisfied(clauses, assignment):
    return all(any(assignment[abs(v)] == (v > 0) for v in row) for row in clauses)


def controls(text, q, distance):
    n, rows = parse(text)
    mutations = [rows-{next(iter(rows))}, rows|{(n,)},
                 rows|{(-((1 if distance <= q//2 else -1)*label(q, 0, 3)),)}]
    rejected = 0
    for rows in mutations:
        bad = f'p cnf {n} {len(rows)}\n'+''.join(' '.join(map(str, row))+' 0\n' for row in sorted(rows))
        try:
            audit(bad, q, distance)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('corrupted model accepted')
    bad = text.replace(f'p cnf {n} ', f'p cnf {n+1} ', 1)
    try:
        audit(bad, q, distance)
    except ValueError:
        rejected += 1
    else:
        raise ValueError('corrupted header accepted')
    return rejected


def counter_controls():
    cases = 0
    for n in range(2, 9):
        for target in range(1, n):
            for sign in (1, -1):
                inputs = [sign*(i+1) for i in range(n)]
                cells, clauses = counter_clauses(inputs, target, n)
                for bits in itertools.product((False, True), repeat=n):
                    assignment = {i+1: bit for i, bit in enumerate(bits)}
                    counted = [bit if sign > 0 else not bit for bit in bits]
                    for (i, k), v in cells.items():
                        assignment[v] = sum(counted[:i]) >= k
                    require(satisfied(clauses, assignment) == (sum(counted) == target),
                            'wrong exact-cardinality truth value')
                    cases += 1
    return cases


def small_family(text, q, distance):
    audit(text, q, distance)
    _, clauses = parse(text)
    color = int(distance <= q//2)
    target = distance if color else q-distance
    cells = counter_cells(q, target, q*(q-1)//2)
    accepted = normalized = cyclic_checked = 0
    for tail in itertools.product((0, 1), repeat=q-1):
        u = (0,)+tail
        assignment = {label(q, x, y): bool(u[x] ^ u[y])
                      for x in range(q) for y in range(x+1, q)}
        derivative = [u[x] ^ u[(x+3) % q] for x in range(q)]
        counted = [int(bit == color) for bit in derivative]
        for (i, k), variable in cells.items():
            assignment[variable] = sum(counted[:i]) >= k
        ladder_free = all(len({u[(a+j*r) % q] ^ u[(a+(j+3)*r) % q]
                              for j in range(4)}) == 2
                          for a in range(q) for r in range(1, q))
        expected = ladder_free and sum(derivative) == distance and derivative[0] == color
        require(satisfied(clauses, assignment) == expected, 'small model Boolean equivalence')
        if not ladder_free:
            continue
        for h in range(1, q):
            delta = [u[x] ^ u[(x+h) % q] for x in range(q)]
            if sum(delta) != distance:
                continue
            a = delta.index(color)
            step = h*pow(3, -1, q) % q
            transformed = tuple(u[(a+step*x) % q] ^ u[a] for x in range(q))
            mapped = {label(q, x, y): bool(transformed[x] ^ transformed[y])
                      for x in range(q) for y in range(x+1, q)}
            counted = [int((transformed[x] ^ transformed[(x+3) % q]) == color) for x in range(q)]
            for (i, k), variable in cells.items():
                mapped[variable] = sum(counted[:i]) >= k
            require(satisfied(clauses, mapped), 'affine normalization lost an entire small case')
            normalized += 1
        if expected:
            accepted += 1
            c = [u[x % q] ^ int(x % 6 >= 3) for x in range(6*q)]
            for a in range(6*q):
                for d in range(1, 6*q):
                    require(len({c[(a+j*d) % (6*q)] for j in range(7)}) == 2,
                            'small positive model produced an actual cyclic AP')
                    cyclic_checked += 1
    return {'q': q, 'distance': distance, 'orientation_assignments': 1 << (q-1),
            'accepted_orientations': accepted, 'affine_cases_verified': normalized,
            'literal_cyclic_APs_checked': cyclic_checked,
            'status': 'SMALL_COMPLETE_FAMILY_AND_NORMALIZATION_CHECKED'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('model', type=Path)
    parser.add_argument('--q', type=int, default=103)
    parser.add_argument('--distance', type=int, required=True)
    parser.add_argument('--controls', action='store_true')
    parser.add_argument('--small-family', action='store_true')
    args = parser.parse_args()
    text = args.model.read_text()
    result = audit(text, args.q, args.distance)
    if args.small_family:
        require(args.q <= 13, 'small exhaustive control is bounded at13')
        print(json.dumps(small_family(text, args.q, args.distance), sort_keys=True))
        return
    if args.controls:
        result['model_corruptions_rejected'] = controls(text, args.q, args.distance)
        result['small_counter_truth_cases'] = counter_controls()
    result['status'] = 'EXACT_DERIVATIVE_DISTANCE_MODEL_AUDITED'
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
