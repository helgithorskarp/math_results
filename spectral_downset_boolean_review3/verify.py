#!/usr/bin/env python3
"""Independent exact audit by six-reviewer-3; no author modules or fixtures."""
import argparse
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path


class Failure(Exception):
    pass


def require(ok, message):
    if not ok:
        raise Failure(message)


def rank(rows):
    basis = {}
    for row in rows:
        x = {i: F(a) for i, a in enumerate(row) if a}
        while x:
            p = min(x)
            if p not in basis:
                a = x[p]
                basis[p] = {i: b / a for i, b in x.items()}
                break
            a = x[p]
            for i, b in basis[p].items():
                y = x.get(i, 0) - a * b
                if y:
                    x[i] = y
                else:
                    x.pop(i, None)
    return len(basis)


def psd_rank(matrix):
    """Exact Schur elimination, including zero-pivot row condition."""
    n = len(matrix)
    require(all(len(row) == n for row in matrix), 'square')
    require(all(matrix[i][j] == matrix[j][i] for i in range(n) for j in range(n)), 'symmetric')
    a = [[F(x) for x in row] for row in matrix]
    r = 0
    for k in range(n):
        d = a[k][k]
        require(d >= 0, 'negative Schur pivot')
        if d == 0:
            require(all(a[k][j] == 0 for j in range(k + 1, n)), 'nonzero zero-pivot row')
            continue
        r += 1
        for i in range(k + 1, n):
            for j in range(i, n):
                a[i][j] -= a[i][k] * a[k][j] / d
                a[j][i] = a[i][j]
    return r


def cube(n, proper=True):
    require(n >= (2 if proper else 1), 'cube order')
    return list(range((1 << n) - int(proper)))


def base_matrix(n, proper=True):
    labels = cube(n, proper)
    count = len(labels)
    s = (1 << (n - 1)) - int(proper)
    full = (1 << n) - 1
    if not proper:
        return [[F(int(b == (a ^ full))) for b in labels] for a in labels]
    m = [[F(0) for _ in labels] for _ in labels]
    m[0][0] = F(1 - s, s + 1)
    for a in labels[1:]:
        m[0][a] = m[a][0] = F(1, s + 1)
        m[a][a ^ full] = F(s, s + 1)
    require(count == 2 * s + 1, 'proper normalization')
    return m


def slack(m, s, upper=False):
    n = len(m)
    if upper:
        return [[int(i == j) - m[i][j] for j in range(n)] for i in range(n)]
    return [[(n - s) * m[i][j] + s * int(i == j) for j in range(n)] for i in range(n)]


def check_h(labels, m, s):
    n = len(labels)
    require(len(m) == n and all(len(r) == n for r in m), 'H dimensions')
    require(all(m[i][j] == m[j][i] for i in range(n) for j in range(n)), 'H symmetry')
    require(all(sum(r) == 1 for r in m), 'H row sums')
    require(all(not (a & b) or m[i][j] == 0 for i, a in enumerate(labels) for j, b in enumerate(labels)), 'H support')
    return psd_rank(slack(m, s)), n - psd_rank(slack(m, s, True))


def family_ok(family, target):
    require(len(family) == target and len(set(family)) == target, 'family size')
    require(all(a & b for a in family for b in family), 'family intersects including itself')


def weighted_exchange(n, a, proper=True):
    """Positive generic integer threshold; distinct from author's seeded greedy sweep."""
    full = (1 << n) - 1
    require(0 < a < full, 'exchange endpoints')
    k = a.bit_count()
    scale = 1 << (n + 1)
    weights = [scale * ((n - k) if (a >> i) & 1 else (k - 1)) + (1 << i) for i in range(n)]
    require(all(w > 0 for w in weights) and sum(weights) % 2 == 1, 'generic positive weights')
    selected = [b for b in cube(n, proper) if 2 * sum(w for i, w in enumerate(weights) if (b >> i) & 1) > sum(weights)]
    require(a in selected and not any(b != a and (b & a) == b for b in selected), 'minimal selected endpoint')
    switched = [b for b in selected if b != a] + [a ^ full]
    target = (1 << (n - 1)) - int(proper)
    family_ok(selected, target)
    family_ok(switched, target)
    require(set(selected) ^ set(switched) == {a, a ^ full}, 'one complementary exchange')
    return selected, switched


def maxima(labels):
    """Complete pivoted maximal-clique enumeration with valid cardinality pruning."""
    vertices = [a for a in labels if a]  # Empty has a loop, so cannot enter a family.
    adj = [sum(1 << j for j, b in enumerate(vertices) if a & b and i != j) for i, a in enumerate(vertices)]
    best, output, nodes = 0, set(), 0

    def visit(chosen, pending, excluded):
        nonlocal best, output, nodes
        nodes += 1
        if len(chosen) + pending.bit_count() < best:
            return
        if not pending and not excluded:
            size = len(chosen)
            family = tuple(sorted(vertices[i] for i in chosen))
            if size > best:
                best, output = size, {family}
            elif size == best:
                output.add(family)
            return
        pool = pending | excluded
        candidates = []
        while pool:
            bit = pool & -pool
            i = bit.bit_length() - 1
            candidates.append(i)
            pool ^= bit
        pivot = max(candidates, key=lambda i: ((pending & adj[i]).bit_count(), -i))
        branches = pending & ~adj[pivot]
        while branches:
            bit = branches & -branches
            i = bit.bit_length() - 1
            visit(chosen + (i,), pending & adj[i], excluded & adj[i])
            pending ^= bit
            excluded |= bit
            branches ^= bit

    visit((), (1 << len(vertices)) - 1, 0)
    for family in output:
        family_ok(family, best)
    return best, output, nodes


def all_family_count(labels):
    """Independent fixed-order include recursion, used only for small baselines."""
    vertices = [a for a in labels if a]
    adj = [sum(1 << j for j, b in enumerate(vertices) if j > i and a & b) for i, a in enumerate(vertices)]
    def count(pending):
        total = 1
        while pending:
            bit = pending & -pending
            i = bit.bit_length() - 1
            pending ^= bit
            total += count(pending & adj[i])
        return total
    return count((1 << len(vertices)) - 1)


def selector_census(n, proper):
    """Second complete method: all choices from complementary pairs."""
    full = (1 << n) - 1
    pairs = [(a, a ^ full) for a in range(1, full) if a < (a ^ full)]
    output = set()
    for choices in range(1 << len(pairs)):
        family = [pair[(choices >> i) & 1] for i, pair in enumerate(pairs)]
        if not proper:
            family.append(full)
        if all(a & b for a in family for b in family):
            output.add(tuple(sorted(family)))
    return output


def equality_check(actual, predicted):
    require(actual == predicted, 'complete equality family set')


def forced_variable_rank(n):
    """Original supported symmetric M variables, homogeneous row/kernel constraints."""
    labels = cube(n)
    full = (1 << n) - 1
    variables = [(i, j) for i in labels for j in labels if i <= j and not (i & j)]
    positions = {pair: k for k, pair in enumerate(variables)}
    def add(row, i, j, value):
        key = positions.get(tuple(sorted((i, j))))
        if key is not None:
            row[key] += value
    rows = []
    for i in labels:
        row = [0] * len(variables)
        for j in labels:
            add(row, i, j, 1)
        rows.append(row)
    for a in labels[1:]:
        b = a ^ full
        if a > b:
            continue
        for i in labels:
            row = [0] * len(variables)
            add(row, i, a, 1)
            add(row, i, b, -1)
            rows.append(row)
    r = rank(rows)
    require(r == len(variables), 'forced supported uniqueness')
    return len(variables), r


def tensor(spec):
    tuples = list(itertools.product(*(cube(n, proper) for proper, n in spec)))
    shifts, cursor = [], 0
    for proper, n in spec:
        shifts.append(cursor)
        cursor += n
    labels = [sum(a << shift for a, shift in zip(t, shifts)) for t in tuples]
    bases = [base_matrix(n, proper) for proper, n in spec]
    m = []
    for a in tuples:
        row = []
        for b in tuples:
            value = F(1)
            for j, base in enumerate(bases):
                value *= base[a[j]][b[j]]
            row.append(value)
        m.append(row)
    stars = [sum(bool(a & (1 << i)) for a in labels) for i in range(cursor)]
    s = max(stars)
    return labels, tuples, m, s


def predicted_families(spec, tuples, labels, base_censuses):
    full_indices = [j for j, (proper, n) in enumerate(spec) if not proper]
    output = set()
    if full_indices:
        m = sum(spec[j][1] for j in full_indices)
        max_base = base_censuses[(False, m)][1]
        def projection(t):
            value, shift = 0, 0
            for j in full_indices:
                value |= t[j] << shift
                shift += spec[j][1]
            return value
        for base in max_base:
            b = set(base)
            output.add(tuple(sorted(label for label, t in zip(labels, tuples) if projection(t) in b)))
    else:
        order = max(n for proper, n in spec)
        for j, (proper, n) in enumerate(spec):
            if n == order:
                for base in base_censuses[(True, n)][1]:
                    b = set(base)
                    output.add(tuple(sorted(label for label, t in zip(labels, tuples) if t[j] in b)))
    return output


def reject(call):
    try:
        call()
    except Failure:
        return True
    raise Failure('negative control was accepted')


def run():
    result = {'reviewer': 'six-reviewer-3', 'arithmetic': 'CPython stdlib integers and Fraction', 'proper_bases': [], 'full_bases': [], 'products': []}
    censuses = {}
    exchange_total = 0
    for proper, orders in [(True, range(2, 8)), (False, range(1, 6))]:
        for n in orders:
            labels = cube(n, proper)
            s = (1 << (n - 1)) - int(proper)
            m = base_matrix(n, proper)
            r, unit = check_h(labels, m, s)
            expected_nullity = s + 1 if proper else s
            require(r == len(labels) - expected_nullity, 'base lower rank')
            require(unit == (1 if proper else s), 'base unit multiplicity')
            L = slack(m, s)
            for a in range(1, (1 << n) - 1):
                first, second = weighted_exchange(n, a, proper)
                for family in (first, second):
                    f = set(family)
                    z = [len(labels) * int(b in f) - s for b in labels]
                    require(all(sum(x * y for x, y in zip(row, z)) == 0 for row in L), 'centered exchange kernel')
                exchange_total += 1
            row = {'order': n, 'N': len(labels), 's': s, 'lower_rank': r, 'lower_nullity': expected_nullity, 'unit_multiplicity': unit}
            if n <= 5:
                best, families, nodes = maxima(labels)
                censuses[(proper, n)] = (best, families, nodes)
                require(best == s, 'literal base optimum')
                equality_check(families, selector_census(n, proper))
                family_rows = [[len(labels) * int(a in family) - s for a in labels] for family in families]
                span = rank(family_rows)
                require(span == expected_nullity, 'complete maximum-family forced span')
                row.update(maxima=len(families), census_nodes=nodes, forced_span=span, complementary_selector_crosscheck=True)
                if proper:
                    variables, vr = forced_variable_rank(n)
                    row.update(supported_variables=variables, forced_variable_rank=vr)
                    if n <= 4:
                        row['all_intersecting_families'] = all_family_count(labels)
            result['proper_bases' if proper else 'full_bases'].append(row)
    result['weighted_exchanges'] = exchange_total
    specs = [((True,2),(True,2)), ((True,2),(True,3)), ((True,3),(True,3)), ((True,2),(True,2),(True,2)), ((False,1),(True,2)), ((False,2),(True,2)), ((False,1),(True,3)), ((False,1),(True,2),(True,2)), ((False,2),(False,1),(True,2)), ((False,2),(False,1))]
    for spec in specs:
        labels, tuples, m, s = tensor(spec)
        r, unit = check_h(labels, m, s)
        full_order = sum(n for proper, n in spec if not proper)
        if full_order:
            nullity = 1 << (full_order - 1)
            expected_unit = nullity
        else:
            top = max(n for proper, n in spec)
            nullity = sum(n == top for proper, n in spec) * (1 << (top - 1))
            expected_unit = 1
        require(r == len(labels) - nullity and unit == expected_unit, 'product endpoint rank')
        row = {'factors': [['proper' if p else 'full', n] for p,n in spec], 'N': len(labels), 's': s, 'lower_rank': r, 'lower_nullity': nullity, 'unit_multiplicity': unit}
        if len(labels) <= 27:
            best, actual, nodes = maxima(labels)
            expected = predicted_families(spec, tuples, labels, censuses)
            require(best == s, 'complete product optimum')
            equality_check(actual, expected)
            row.update(maxima=len(actual), census_nodes=nodes, equality_census_complete=True)
        result['products'].append(row)
    # An explicitly noncentered supported core; the affine lift always has H rows/support.
    n, s = 3, 3
    labels = cube(n)
    full = (1 << n) - 1
    C = [[s * int(a == b or a == (b ^ full)) - 1 for b in labels[1:]] for a in labels[1:]]
    C[0][1] += 1; C[1][0] += 1  # {1} and {2}: allowed disjoint off-diagonal.
    require(any(sum(row) for row in C), 'noncentered control')
    sums = list(map(sum, C))
    L = [[1 + sum(sums)] + [1 - v for v in sums]]
    L += [[1 - sums[i]] + [1 + x for x in row] for i, row in enumerate(C)]
    require(all(sum(row) == len(labels) for row in L), 'uncentered affine lift rows')
    require(all(L[i][j] == (s if i == j else 0) for i,a in enumerate(labels) for j,b in enumerate(labels) if a & b), 'uncentered affine lift support')
    result['uncentered_lift_checked'] = True
    reject(lambda:psd_rank(C))
    # Aggregate full order three: majority depends on both original full factors.
    spec = ((False,2),(False,1),(True,2))
    labels, tuples, m, s = tensor(spec)
    majority = tuple(sorted(a for a,t in zip(labels,tuples) if (t[0] | (t[1] << 2)).bit_count() >= 2))
    family_ok(majority, s)
    for j in (0, 1):
        require(any(len({int(a in majority) for a,t in zip(labels,tuples) if t[j] == b}) == 2 for b in cube(spec[j][1], False)), 'majority not single original full-factor cylinder')
    result['mixed_majority_witness_masks'] = list(majority)
    controls = []
    complete = censuses[(True,3)][1]
    incomplete = set(sorted(complete)[1:])
    full_three = censuses[(False,3)][1]
    dictators = {tuple(a for a in cube(3,False) if a & (1 << i)) for i in range(3)}
    for name, call in [('empty-loop-family',lambda:family_ok([0],1)), ('zero-Schur-row',lambda:psd_rank([[0,1],[1,1]])), ('negative-pivot',lambda:psd_rank([[1,2],[2,1]])), ('nonsymmetric',lambda:psd_rank([[1,1],[0,1]])), ('invalid-proper-order',lambda:cube(1)), ('missing-maximum-family',lambda:equality_check(incomplete,complete)), ('false-mixed-cylinders',lambda:equality_check(full_three,dictators))]:
        reject(call); controls.append(name)
    wrong = base_matrix(3);wrong[0][0] += F(1,2)
    reject(lambda:check_h(cube(3),wrong,3));controls.append('wrong-empty-diagonal')
    result['rejected_negative_controls'] = controls
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', type=Path)
    parser.add_argument('--write', type=Path)
    args = parser.parse_args()
    result = run()
    text = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.check:
        require(json.loads(args.check.read_text()) == result, 'expected summary mismatch')
    if args.write:
        args.write.write_text(text)
    print(json.dumps({'status':'verified', 'summary_sha256':hashlib.sha256(text.encode()).hexdigest(), 'weighted_exchanges':result['weighted_exchanges'], 'product_instances':len(result['products']), 'negative_controls':len(result['rejected_negative_controls'])}, sort_keys=True))


if __name__ == '__main__':
    main()
