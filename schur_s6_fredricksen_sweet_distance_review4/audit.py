"""Independent two-slack audit for the 54-edit S(6) baseline obstruction.

Uses the previous independent input/CNF audit, never the reviewed checker.
Run: python3 -B audit.py --workers 4
"""

import argparse
from concurrent.futures import ProcessPoolExecutor
import importlib.util
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREVIOUS = HERE.parent / 'schur_s6_fredricksen_sweet_distance_review3' / 'audit.py'
spec = importlib.util.spec_from_file_location('previous_distance_review', PREVIOUS)
previous = importlib.util.module_from_spec(spec)
spec.loader.exec_module(previous)


def require(value, message):
    if not value:
        raise ValueError(message)


def one_slack_rows(base, edges, colour, groups, j):
    """Exact one-slack clauses; tags say when a second slack changes a row."""
    free = {v for group in groups for v in group} | {j}
    extended = base + [colour]
    rows = []

    def add(clause, tag=()):
        rows.append((tuple(clause), tuple(tag)))

    for v in sorted(free):
        add([previous.var(v, d) for d in range(1, 7)])
        for d in range(1, 7):
            for e in range(1, d):
                add([-previous.var(v, d), -previous.var(v, e)])
    add([-previous.var(j, base[j])])
    for group in groups:
        regular = [v for v in group if v != j]
        # This clause remains valid after a second slack inside the group:
        # the two-slack model still requires a regular edit outside both.
        add([-previous.var(v, base[v]) for v in regular])
        for a_index, a in enumerate(regular):
            for b in regular[:a_index]:
                add([previous.var(a, base[a]), previous.var(b, base[b])],
                    (a, b))
    for edge in edges:
        fixed = [v for v in edge if v not in free]
        for d in range(1, 7):
            if any(extended[v] != d for v in fixed):
                continue
            changing = [v for v in edge if v in free]
            require(changing, f'fixed Schur triple {edge}')
            add([-previous.var(v, d) for v in changing],
                (v for v in fixed if v <= 536))
    return rows


def core_or_residual(rows, assumptions):
    """Trace reasons for a unit contradiction under branch assumptions."""
    assignment = dict(assumptions)
    reason = {}
    while True:
        changed = False
        for index, (clause, _) in enumerate(rows):
            if any(assignment.get(abs(lit)) == (lit > 0) for lit in clause):
                continue
            pending = [lit for lit in clause if abs(lit) not in assignment]
            if not pending:
                core = set()
                stack = [index]
                while stack:
                    i = stack.pop()
                    if i in core:
                        continue
                    core.add(i)
                    stack.extend(reason[abs(lit)] for lit in rows[i][0]
                                 if abs(lit) in reason)
                return core, None
            if len(pending) == 1:
                lit = pending[0]
                assignment[abs(lit)] = lit > 0
                reason[abs(lit)] = index
                changed = True
        if not changed:
            residual = []
            for clause, _ in rows:
                if any(assignment.get(abs(lit)) == (lit > 0)
                       for lit in clause):
                    continue
                residual.append(tuple(lit for lit in clause
                                      if abs(lit) not in assignment))
            return None, residual


def unsat_core(rows, assumptions=None):
    if assumptions is None:
        assumptions = {}
    core, residual = core_or_residual(rows, assumptions)
    if core is not None:
        return core, False
    require(residual, 'one-slack formula is satisfiable')
    variable, preferred = previous.choose_literal(residual)
    left, _ = unsat_core(rows, {**assumptions, variable: preferred})
    right, _ = unsat_core(rows, {**assumptions, variable: not preferred})
    return left | right, True


def candidate_cases():
    base, data, edges = previous.read_input()
    all_cases = []
    summary = []
    for colour in (2, 4, 5, 6):
        groups, free, witnesses = previous.groups_for(base, data, colour)
        no_slack = previous.clauses_for(base, edges, colour, groups, free)
        first_core = previous.unit_core(no_slack)
        first = sorted({v for i in first_core for v in no_slack[i][1]})
        found = set()
        branching_first = 0
        for j in first:
            rows = one_slack_rows(base, edges, colour, groups, j)
            core, branched = unsat_core(rows)
            require(not previous.satisfiable([rows[i][0] for i in core]),
                    f'one-slack core not unsatisfiable {(colour, j)}')
            branching_first += branched
            for k in {v for i in core for v in rows[i][1]}:
                if k != j:
                    found.add(tuple(sorted((j, k))))
        summary.append((colour, len(first), branching_first, len(found)))
        all_cases.extend((colour, j, k) for j, k in sorted(found))
        print(f'colour={colour} first_slack={len(first)} '
              f'branching_first={branching_first} candidate_pairs={len(found)}',
              flush=True)
    require(summary == [(2, 16, 0, 151), (4, 16, 0, 178),
                        (5, 36, 6, 959), (6, 16, 0, 225)],
            f'candidate list differs: {summary}')
    return all_cases


_WORKER = None


def worker_init():
    global _WORKER
    base, data, edges = previous.read_input()
    groups = {c: previous.groups_for(base, data, c)[0] for c in (2, 4, 5, 6)}
    degree = [0] * 538
    unique_edges = []
    for edge in edges:
        vertices = tuple(sorted(set(edge)))
        unique_edges.append(vertices)
        for v in vertices:
            degree[v] += 1
    _WORKER = base, groups, unique_edges, degree


def contradiction(domains, regulars, edges):
    """Sound exact-one-group and Schur-domain propagation."""
    while True:
        changed = False
        for group, original in regulars:
            forced = [v for v in group if not (domains[v] & original[v])]
            possible = [v for v in group if domains[v] & ~original[v]]
            if len(forced) > 1 or not possible:
                return True
            if forced:
                for v in group:
                    if v == forced[0]:
                        continue
                    new = domains[v] & original[v]
                    if not new:
                        return True
                    changed |= new != domains[v]
                    domains[v] = new
            if len(possible) == 1:
                v = possible[0]
                new = domains[v] & ~original[v]
                if not new:
                    return True
                changed |= new != domains[v]
                domains[v] = new
        for vertices in edges:
            singleton = [(v, domains[v]) for v in vertices
                         if domains[v].bit_count() == 1]
            if len(singleton) < len(vertices) - 1:
                continue
            if len({mask for _, mask in singleton}) != 1:
                continue
            open_vertices = [v for v in vertices if domains[v].bit_count() > 1]
            if not open_vertices:
                return True
            v = open_vertices[0]
            new = domains[v] & ~singleton[0][1]
            if not new:
                return True
            changed |= new != domains[v]
            domains[v] = new
        if not changed:
            return False


def solve(domains, regulars, edges, degree, stats):
    stats[0] += 1
    domains = domains[:]
    if contradiction(domains, regulars, edges):
        return False
    open_vertices = [v for v in range(1, len(domains))
                     if domains[v].bit_count() > 1]
    if not open_vertices:
        return True
    v = min(open_vertices, key=lambda x: (domains[x].bit_count(), -degree[x], x))
    chosen = domains[v] & -domains[v]
    for allowed in (chosen, domains[v] & ~chosen):
        child = domains[:]
        child[v] = allowed
        if solve(child, regulars, edges, degree, stats):
            return True
    return False


def solver_controls():
    """Compare exact domain search with every small 2-colour edge system."""
    universe = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4),
                (1, 2, 3), (1, 2, 4), (1, 3, 4), (2, 3, 4)]
    regulars = [([1, 2], {1: 1, 2: 1}),
                ([3, 4], {3: 1, 4: 1})]
    for mask in range(1 << len(universe)):
        edges = [edge for i, edge in enumerate(universe) if mask >> i & 1]
        degree = [0] * 5
        for edge in edges:
            for v in edge:
                degree[v] += 1
        actual = solve([0, 3, 3, 3, 3], regulars, edges, degree, [0])
        expected = any(
            sum(values[v - 1] == 2 for v in (1, 2)) == 1
            and sum(values[v - 1] == 2 for v in (3, 4)) == 1
            and all(len({values[v - 1] for v in edge}) > 1 for edge in edges)
            for values in product((1, 2), repeat=4))
        require(actual == expected, f'domain solver control failed at {mask}')
    print('PASS domain_solver_controls=1024', flush=True)


def check_case(case):
    require(_WORKER is not None, 'worker missing data')
    base, groups_by_colour, edges, degree = _WORKER
    colour, j, k = case
    slack = {j, k}
    groups = groups_by_colour[colour]
    free = set().union(*groups) | slack
    fixed = base + [colour]
    domains = [0] + [63 if v in free else 1 << (fixed[v] - 1)
                     for v in range(1, 538)]
    for v in slack:
        domains[v] &= ~(1 << (base[v] - 1))
    regulars = []
    for group in groups:
        regular = [v for v in group if v not in slack]
        if not regular:
            return colour, j, k, 1, True
        regulars.append((regular, {v: 1 << (base[v] - 1) for v in regular}))
    stats = [0]
    sat = solve(domains, regulars, edges, degree, stats)
    return colour, j, k, stats[0], not sat


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--candidates-only', action='store_true')
    args = parser.parse_args()
    require(1 <= args.workers <= 8, 'workers must be 1..8')
    solver_controls()
    cases = candidate_cases()
    require(len(cases) == 1513, 'wrong number of exact cases')
    if args.candidates_only:
        print('PASS independently_derived_candidate_pairs=1513', flush=True)
        return
    results = []
    with ProcessPoolExecutor(max_workers=args.workers, initializer=worker_init) as pool:
        for row in pool.map(check_case, cases):
            require(row[-1], f'possible 537-colouring in case {row[:3]}')
            results.append(row)
            if len(results) % 200 == 0:
                print(f'checked={len(results)}/{len(cases)}', flush=True)
    for c in (2, 4, 5, 6):
        rows = [row for row in results if row[0] == c]
        print(f'colour={c} checked={len(rows)} branch_cases='
              f'{sum(row[3] > 1 for row in rows)} max_nodes='
              f'{max(row[3] for row in rows)}', flush=True)
    print('PASS independent_distance_at_least=54 checked_pairs=1513', flush=True)


if __name__ == '__main__':
    main()
