#!/usr/bin/env python3
"""Optional replay of the single bounded solver experiment, into fresh scratch."""
import argparse
from itertools import combinations
import hashlib
import json
from pathlib import Path
import threading
import time

import pysat
from pysat.solvers import Glucose3

from formula import generate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    args.output.mkdir()
    fixed, free, clauses, text = generate()
    (args.output/'extension.cnf').write_text(text)
    with Glucose3(bootstrap_with=clauses, with_proof=True) as solver:
        solver.conf_budget(1000000)
        timer = threading.Timer(300, solver.interrupt)
        start = time.monotonic()
        timer.start()
        try:
            answer = solver.solve_limited(expect_interrupt=True)
        finally:
            timer.cancel()
        status = 'SAT' if answer else ('UNSAT' if answer is False else 'UNKNOWN')
        result = {'status': status, 'elapsed_seconds': time.monotonic()-start,
                  'stats': solver.accum_stats(), 'calls': 1,
                  'conflict_budget': 1000000, 'wall_seconds': 300,
                  'python_sat': pysat.__version__, 'solver': 'Glucose3',
                  'cnf_sha256': hashlib.sha256(text.encode()).hexdigest(),
                  'variables': len(free), 'clauses': len(clauses),
                  'good43_found': False, 'global43_branch_decided': False}
        if answer:
            model = solver.get_model()
            (args.output/'model.json').write_text(json.dumps(model)+'\n')
            values = {abs(x): x > 0 for x in model}
            physical = {**fixed, **{e: int(values[v]) for e, v in free.items()}}
            for size, color in ((4, 1), (5, 0)):
                for q in combinations(range(24), size):
                    if all(physical[e] == color for e in combinations(q, 2)):
                        raise ValueError('solver model fails literal extension check')
            code = sum(physical[e] << i for i, e in enumerate(sorted(physical)))
            (args.output/'extension.json').write_text(json.dumps(
                {'n': 24, 'red_hex': format(code, '069x')}, indent=2)+'\n')
        elif answer is False:
            # An unexpected UNSAT result needs proof checking; never promote
            # this status to an exclusion of the global branch automatically.
            (args.output/'extension.drat').write_text('\n'.join(solver.get_proof())+'\n')
    (args.output/'result.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
