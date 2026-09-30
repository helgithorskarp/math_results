"""Exhaustive small-word controls, with independent union-find cut checks."""
import itertools
import json
import resource
import time
from pathlib import Path
from filtered_encoding import Encoding, canonicalize


def simulate(n, gates, x):
    row = list(map(int, f'{x:0{n}b}'[::-1]))
    for a, b in gates:
        if row[a] > row[b]:
            row[a], row[b] = row[b], row[a]
    return row


def sorts(n, gates, states):
    return all(simulate(n, gates, x) == sorted(simulate(n, (), x)) for x in states)


def component_condition(n, gates):
    """Connected components of future gates, independent of boundary literals."""
    for t, (a, b) in enumerate(gates):
        parent = list(range(n))

        def root(i):
            while parent[i] != i:
                i = parent[i]
            return i

        for u, v in gates[t + 1:]:
            parent[root(v)] = root(u)
        blocks = {}
        for i in range(n):
            blocks.setdefault(root(i), []).append(i)
        blocks = sorted(blocks.values())
        if any(B != list(range(B[0], B[-1] + 1)) for B in blocks):
            return False
        ia = next(i for i, B in enumerate(blocks) if a in B)
        ib = next(i for i, B in enumerate(blocks) if b in B)
        if abs(ia - ib) > 1:
            return False
    return True


def lex_condition(gates):
    return all(not (p > q and len(set(p + q)) == 4)
               for p, q in zip(gates, gates[1:]))


def main():
    started = time.monotonic()
    records = []
    for n, max_m in ((3, 4), (4, 5)):
        pairs = list(itertools.combinations(range(n), 2))
        for m in range(max_m + 1):
            constant = Encoding(n, m, intervals=False, pure_sides=True, disjoint_lex=False)
            structural = Encoding(n, m, constants=True, pure_sides=False, disjoint_lex=False)
            filtered = Encoding(n, m)
            for x in range(2 ** n):
                constant.add_row(x)
                filtered.add_row(x)
            counts = {'n': n, 'budget': m, 'words': 0, 'sorters': 0,
                      'filtered_sorters': 0, 'nonredundant_sorters': 0}
            for gates in itertools.product(pairs, repeat=m):
                correct = sorts(n, gates, range(2 ** n))
                condition = component_condition(n, gates)
                assert constant.solver.solve(assumptions=constant.assume_gates(gates)) == correct
                assert structural.solver.solve(assumptions=structural.assume_gates(gates)) == condition
                expected = correct and condition and lex_condition(gates)
                assert filtered.solver.solve(assumptions=filtered.assume_gates(gates)) == expected
                if correct:
                    canonical, _ = canonicalize(gates)
                    assert sorts(n, canonical, range(2 ** n))
                    assert lex_condition(canonical)
                    nonredundant = all(not sorts(n, gates[:t] + gates[t + 1:], range(2 ** n))
                                       for t in range(m))
                    if nonredundant:
                        assert condition and component_condition(n, canonical)
                    counts['nonredundant_sorters'] += nonredundant
                counts['words'] += 1
                counts['sorters'] += correct
                counts['filtered_sorters'] += expected
            for enc in (constant, structural, filtered):
                enc.solver.delete()
            records.append(counts)
            print(json.dumps(counts), flush=True)
    # An internal future-component gate must remain admissible.
    inside = [(0, 2), (0, 1), (1, 2)]
    assert sorts(3, inside, range(8)) and component_condition(3, inside)
    enc = Encoding(3, 3)
    for x in range(8):
        enc.add_row(x)
    assert enc.solver.solve(assumptions=enc.assume_gates(inside))
    enc.solver.delete()
    mixed_checks = 0
    pairs = list(itertools.combinations(range(3), 2))
    for colors in itertools.product(range(3), repeat=3):
        x = sum((v == 2) << i for i, v in enumerate(colors))
        y = sum((v != 0) << i for i, v in enumerate(colors))
        for bound in range(4):
            enc = Encoding(3, 3, intervals=False, pure_sides=False, disjoint_lex=False)
            enc.add_row(x, final_sorted=False)
            enc.add_row(y, final_sorted=False)
            enc.mixed_touch_bound(x, y, bound)
            for gates in itertools.product(pairs, repeat=3):
                row = list(colors)
                count = 0
                for a, b in gates:
                    count += row[a] != 1 or row[b] != 1
                    row[a], row[b] = min(row[a], row[b]), max(row[a], row[b])
                assert enc.solver.solve(assumptions=enc.assume_gates(gates)) == (count <= bound)
                mixed_checks += 1
            enc.solver.delete()
    route_checks = 0
    alphabet = [(0, 1), (0, 5), (1, 5), (6, 9), (9, 10),
                (0, 10), (1, 10), (4, 7)]
    partial = [1024, 512, 2045]
    for m in (3, 4):
        for branch in ('max_once', 'min_once'):
            enc = Encoding(11, m, intervals=False, pure_sides=False, disjoint_lex=False)
            for x in partial:
                enc.add_row(x)
            enc.route_branch(branch)
            enc.phase_redundancies()
            for gates in itertools.product(alphabet, repeat=m):
                correct = sorts(11, gates, partial)
                if branch == 'max_once':
                    wanted = sum(10 in p for p in gates) == 1
                else:
                    zero = 1
                    touches = 0
                    for a, b in gates:
                        if zero in (a, b):
                            touches += 1
                            zero = a
                    wanted = touches == 1
                assert enc.solver.solve(assumptions=enc.assume_gates(gates)) == (correct and wanted)
                route_checks += 1
            enc.solver.delete()
    phase_checks = 0
    for m in range(5):
        enc = Encoding(11, m, intervals=False, pure_sides=False, disjoint_lex=False)
        enc.phase_redundancies()
        for gates in itertools.product(alphabet, repeat=m):
            pivot = next((t for t, p in enumerate(gates) if p == (0, 1)), None)
            expected = pivot is not None
            if expected:
                expected = ((1, 10) not in gates[:pivot] and
                            (0, 10) not in gates[pivot + 1:])
            assert enc.solver.solve(assumptions=enc.assume_gates(gates)) == expected
            phase_checks += 1
        enc.solver.delete()
    result = {'agent': 'six-sorting-1', 'role': 'researcher', 'status': 'passed',
              'all_short_word_controls': records,
              'internal_future_component_control': inside,
              'mixed_touch_controls': mixed_checks,
              'eleven_wire_route_branch_controls': route_checks,
              'first_pivot_phase_controls': phase_checks,
              'elapsed_seconds': time.monotonic() - started,
              'peak_rss_kib_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    out = Path(__file__).resolve().parent / 'scratch' / 'filter-controls.json'
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result), flush=True)
    return result


if __name__ == '__main__':
    main()
