"""Independent definition-level CNF audit, with no generator or solver import."""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_cnf(path):
    lines = path.read_text().splitlines()
    header = lines[0].split()
    require(len(header) == 4 and header[:2] == ["p", "cnf"], "bad CNF header")
    n, m = map(int, header[2:])
    require(n > 0 and m >= 0 and len(lines) == m+1, "bad CNF dimensions")
    clauses = []
    for line in lines[1:]:
        tokens = list(map(int, line.split()))
        require(tokens and tokens[-1] == 0 and 0 not in tokens[:-1], "bad clause terminator")
        require(all(1 <= abs(v) <= n for v in tokens[:-1]), "literal outside domain")
        clauses.append(tuple(tokens[:-1]))
    return n, clauses


def direct_edges():
    p = 617
    require(all(p % d for d in range(2, 25)), "nonprime field order")
    # Kernel of x -> x^8 is the order-eight subgroup. Quotient images,
    # rather than discrete logarithms, label its 77 cosets.
    image_to_id = {pow(3, 8*j, p): j for j in range(77)}
    subgroup = {pow(3, 77*j, p) for j in range(8)}
    require(len(image_to_id) == 77 and len(subgroup) == 8, "wrong subgroup")
    require(subgroup == {x for x in range(1, p) if pow(x, 8, p) == 1}, "wrong kernel")
    ids = [None] + [image_to_id[pow(x, 8, p)] for x in range(1, p)]
    edges = set()
    retained = removed = 0
    for a in range(p):
        for d in range(1, p):
            positions = [(a+j*d) % p for j in range(7)]
            if 0 in positions:
                removed += 1
            else:
                edges.add(tuple(sorted({ids[x] for x in positions})))
                retained += 1
    require(removed == 4312 and retained == 375760, "incomplete direct AP coverage")
    return edges, retained, removed


def independent_counter(n, bound, first_input, first_aux):
    width = bound+1
    require(1 <= n <= 100 and 0 <= bound < n, "bad counter domain")
    def s(i, j):
        return first_aux + (i-1)*width + j-1
    # Group by logical role rather than the generator's row traversal.
    clauses = [(-s(i, j),) for j in range(1, width+1) for i in range(1, min(n, j-1)+1)]
    clauses += [(-first_input-i+1, s(i, 1)) for i in range(1, n+1)]
    clauses += [(-s(i, j), s(i+1, j))
                for j in range(1, width+1) for i in range(1, n)]
    clauses += [(-first_input-i, -s(i, j), s(i+1, j+1))
                for j in range(1, width) for i in range(1, n)]
    clauses += [(-s(n, width),)]
    return clauses


def satisfy(clause, values):
    return any(values[abs(v)] == (v > 0) for v in clause)


def counter_controls():
    cases = 0
    for n in range(1, 9):
        for bound in range(n):
            clauses = independent_counter(n, bound, 1, n+1)
            width = bound+1
            for bits in itertools.product((False, True), repeat=n):
                values = {i+1: bit for i, bit in enumerate(bits)}
                prefix = 0
                for i, bit in enumerate(bits, 1):
                    prefix += bit
                    for j in range(1, width+1):
                        values[n+1+(i-1)*width+j-1] = prefix >= j
                if sum(bits) <= bound:
                    require(all(satisfy(c, values) for c in clauses), "counter loses valid input")
                else:
                    # Check that forward propagation, not a chosen extension,
                    # contradicts the counter for each invalid input.
                    forced = {i+1: bit for i, bit in enumerate(bits)}
                    conflict = False
                    while not conflict:
                        changed = False
                        for c in clauses:
                            if any(abs(v) in forced and forced[abs(v)] == (v > 0) for v in c):
                                continue
                            free = [v for v in c if abs(v) not in forced]
                            if not free:
                                conflict = True
                                break
                            if len(free) == 1:
                                forced[abs(free[0])] = free[0] > 0
                                changed = True
                        require(conflict or changed, "counter permits an invalid input")
                cases += 1
    equality = ((1, 2, 3), (-1, -2, 3), (1, -2, -3), (-1, 2, -3))
    for bits in itertools.product((False, True), repeat=3):
        values = dict(enumerate(bits, 1))
        require(all(satisfy(c, values) for c in equality) == (bits[2] == (bits[0] == bits[1])),
                "wrong equal-pair truth table")
    return {"exhaustive_counter_inputs": cases, "equality_truth_cases": 8}


def audit(path, bound):
    require(0 <= bound < 77, "invalid defect bound")
    variables, actual = read_cnf(path)
    require(variables == 154+77*(bound+1), "wrong variable count")
    edges, retained, removed = direct_edges()
    expected = []
    for edge in edges:
        vertices = tuple(x+1 for x in edge)
        expected.extend((vertices, tuple(-x for x in vertices)))
    expected.extend(((-1,), (-2,)))
    for x in range(1, 78):
        y = x % 77+1
        z = 77+x
        expected.extend(((x, y, z), (-x, -y, z), (x, -y, -z), (-x, y, -z)))
    expected.extend(independent_counter(77, bound, 78, 155))
    require(Counter(actual) == Counter(expected), "CNF differs from exact mathematical constraints")
    require(len(edges) == 23177, "wrong punctured edge set")
    return {"status": "EXACT_ORDER8_ENCODING_AUDITED", "variables": variables,
            "clauses": len(actual), "equal_bound": bound, "field_edges": len(edges),
            "rank_histogram": dict(sorted(Counter(map(len, edges)).items())),
            "direct_retained_APs": retained, "direct_zero_APs_removed": removed,
            "cnf_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cnf", type=Path)
    ap.add_argument("--bound", type=int, default=9)
    args = ap.parse_args()
    result = audit(args.cnf, args.bound)
    result["controls"] = counter_controls()
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
