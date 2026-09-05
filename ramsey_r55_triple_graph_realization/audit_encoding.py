#!/usr/bin/env python3
"""Exact checks of the optional bounded discovery formulation."""
import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path

from generate import build, CounterEncoder
from verify import require, Y


def counter_controls():
    tested = 0
    for n in range(8):
        for lower in range(n+2):
            for upper in range(-1,n+1):
                enc = CounterEncoder(n, [])
                enc.interval(list(range(1,n+1)),lower,upper)
                for mask in range(1 << n):
                    assignment = {i+1: bool(mask >> i & 1) for i in range(n)}
                    variable = n
                    if lower <= upper and lower <= n and upper >= 0:
                        high = min(upper,n)
                        for i in range(1,n+1):
                            for j in range(1,min(i,high+1)+1):
                                variable += 1
                                assignment[variable] = (mask & ((1 << i)-1)).bit_count() >= j
                    require(variable == enc.variables, 'counter coordinate count')
                    satisfied = all(any(assignment[abs(lit)] == (lit > 0) for lit in clause)
                                    for clause in enc.clauses)
                    require(satisfied == (lower <= mask.bit_count() <= upper), 'counter truth table')
                    tested += 1
    return tested


def literal_mixed():
    signatures = [None]*3+[s for s,n in enumerate(Y) for _ in range(n)]
    index = {e:i+1 for i,e in enumerate(combinations(range(3,43),2))}
    answer = set()
    for five in combinations(range(43),5):
        if min(five) >= 3:
            continue
        fixed_colors = []
        free = []
        for u,v in combinations(five,2):
            if v < 3:
                fixed_colors.append(1)
            elif u < 3:
                fixed_colors.append(signatures[v] >> u & 1)
            else:
                free.append(index[u,v])
        if all(fixed_colors):
            answer.add(tuple(sorted(-var for var in free)))
        if not any(fixed_colors):
            answer.add(tuple(sorted(free)))
    return answer


def neighborhood_clauses():
    signatures = [None]*3+[s for s,n in enumerate(Y) for _ in range(n)]
    index = {e:i+1 for i,e in enumerate(combinations(range(3,43),2))}
    answer = set()
    for root in range(3):
        for adjacent in (0,1):
            neighborhood = [u for u in range(3,43) if (signatures[u] >> root & 1) == adjacent]
            sign = 1 if adjacent else -1
            for five in combinations(neighborhood,5):
                answer.add(tuple(sign*index[e] for e in combinations(five,2)))
    return answer


def formula_hash(encoder):
    data = f'p cnf {encoder.variables} {len(encoder.clauses)}\n'+''.join(
        ' '.join(map(str,clause))+' 0\n' for clause in encoder.clauses)
    return hashlib.sha256(data.encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--report',type=Path)
    args = parser.parse_args()
    _, _, mixed = build(False)
    _, _, full = build(True)
    base, extra = literal_mixed(), neighborhood_clauses()
    require(set(mixed.clauses[:len(base)]) == base, 'literal mixed formula mismatch')
    require(full.clauses[:len(base)] == mixed.clauses[:len(base)], 'mixed prefix changed')
    require(set(full.clauses[len(base):len(base)+len(extra)]) == extra, 'neighborhood family mismatch')
    require(full.clauses[len(base)+len(extra):] == mixed.clauses[len(base):], 'counter suffix changed')
    report = {'mixed_primary_clauses':len(base), 'new_neighborhood_clauses':len(extra),
              'mixed_total_clauses':len(mixed.clauses), 'neighborhood_total_clauses':len(full.clauses),
              'variables_in_both':mixed.variables,
              'mixed_formula_sha256':formula_hash(mixed),
              'neighborhood_formula_sha256':formula_hash(full),
              'counter_truth_table_cases':counter_controls()}
    require(report['mixed_formula_sha256'] == 'e7e37dde6a3553a8110b15c2c5afc2a3139e2affafb3a88eee07071defa740bf', 'mixed source/run mismatch')
    require(report['neighborhood_formula_sha256'] == '1480325fd9f354642e4aae4d836723c77a5349e0e721f41a7e3284844e344093', 'neighborhood source/run mismatch')
    if args.report:
        args.report.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,sort_keys=True))


if __name__ == '__main__':
    main()
